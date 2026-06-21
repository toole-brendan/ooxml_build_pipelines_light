#!/usr/bin/env python3
"""
Aggregate SAM.gov subaward pulls + compare to USAspending pulls.

Per SAM_GOV_HOWTO.md:
  - subAwardReportId is unique → no dedup needed (but verify)
  - Numeric fields are STRINGS → coerce with float()
  - Use subAwardDate for FY attribution (not submittedDate)
  - Use subParentUei for parent rollup with two-pass back-mapping

Outputs (in extracted/):
  sam_subaward_annual_by_prime.csv    Per-FY subAwardAmount summed per PIID
  sam_subaward_top_parents.csv        Top recipients across all PIIDs (parent UEI rollup)
  sam_vs_usaspending_per_piid.csv     Side-by-side comparison: records + $ recovered
  sam_subaward_full_dedup_check.txt   Diagnostics
"""
import csv
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

# Shared contaminant exclusion list (IVECO + DDG-1000 + WPN/OPN weapons).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from aggregate_new_construction import OUT_OF_SCOPE_PIIDS as EXCLUDED_PIIDS
except ImportError:
    EXCLUDED_PIIDS = {}

SAM_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/sam_subawards"
USA_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/usaspending_subawards"
OUT = "/Users/brendantoole/projects2/destroyer_outsourced_work/extracted"
os.makedirs(OUT, exist_ok=True)


def fy_from_date(d):
    if not d:
        return None
    try:
        dt = datetime.fromisoformat(str(d)[:10])
    except Exception:
        return None
    return dt.year + 1 if dt.month >= 10 else dt.year


def load_all_sam_records():
    records = []
    for fname in sorted(os.listdir(SAM_DIR)):
        if not fname.endswith("_subawards.json") or fname.startswith("_"):
            continue
        path = os.path.join(SAM_DIR, fname)
        with open(path) as f:
            data = json.load(f)
        piid = data.get("piid")
        if (piid or "").replace("-", "") in EXCLUDED_PIIDS:
            continue  # IVECO / DDG-1000 / WPN-OPN weapons — see aggregate_new_construction.py
        for r in data.get("published") or []:
            records.append((piid, r))
    return records


def build_sub_to_parent_lookup(records):
    lookup = {}
    for _, r in records:
        sub = (r.get("subEntityUei") or "").strip()
        parent = (r.get("subParentUei") or "").strip()
        if sub and parent:
            lookup.setdefault(sub, parent)
    return lookup


def recipient_key_and_name(r, sub_to_parent_lookup):
    sub_uei = (r.get("subEntityUei") or "").strip()
    parent_uei = (r.get("subParentUei") or "").strip()
    if not parent_uei and sub_uei:
        parent_uei = sub_to_parent_lookup.get(sub_uei, "")
    key = parent_uei or sub_uei or ""
    parent_name = (r.get("subEntityParentLegalBusinessName") or "").strip()
    sub_name = (r.get("subEntityLegalBusinessName") or "").strip()
    name = parent_name or sub_name or "UNKNOWN"
    return key.upper(), name.upper()


def dedup_check(records):
    ids = defaultdict(int)
    blanks = 0
    for _, r in records:
        rid = r.get("subAwardReportId")
        if rid:
            ids[rid] += 1
        else:
            blanks += 1
    dups = {k: v for k, v in ids.items() if v > 1}
    return {
        "total_records": len(records),
        "records_with_id": sum(ids.values()),
        "unique_ids": len(ids),
        "blank_ids": blanks,
        "collision_count": len(dups),
        "max_collision_repeats": max(dups.values()) if dups else 0,
    }


def aggregate_per_fy_per_piid(records):
    by_fy_piid = defaultdict(lambda: defaultdict(float))
    by_fy_piid_count = defaultdict(lambda: defaultdict(int))
    for piid, r in records:
        fy = fy_from_date(r.get("subAwardDate"))
        if not fy:
            continue
        amt = float(r.get("subAwardAmount") or 0)
        by_fy_piid[fy][piid] += amt
        by_fy_piid_count[fy][piid] += 1
    return by_fy_piid, by_fy_piid_count


def aggregate_top_parents(records, sub_to_parent_lookup, top_n=200):
    by_parent = defaultdict(lambda: {"amount": 0.0, "count": 0, "name": ""})
    for _, r in records:
        key, name = recipient_key_and_name(r, sub_to_parent_lookup)
        if not key:
            continue
        slot = by_parent[key]
        slot["amount"] += float(r.get("subAwardAmount") or 0)
        slot["count"] += 1
        if name and (not slot["name"] or len(name) > len(slot["name"])):
            slot["name"] = name
    ranked = sorted(by_parent.items(), key=lambda kv: kv[1]["amount"], reverse=True)
    return ranked[:top_n]


def write_per_fy_csv(by_fy_piid, by_fy_piid_count):
    fys = sorted(by_fy_piid.keys())
    piids = sorted({p for d in by_fy_piid.values() for p in d.keys()})
    out = os.path.join(OUT, "sam_subaward_annual_by_prime.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["FY"] + [f"{p}_$M" for p in piids] + ["FY_TOTAL_$M"] +
                   [f"{p}_count" for p in piids])
        for fy in fys:
            amt_row = [fy]
            total = 0
            for p in piids:
                v = by_fy_piid[fy].get(p, 0)
                amt_row.append(round(v / 1e6, 2))
                total += v
            amt_row.append(round(total / 1e6, 2))
            for p in piids:
                amt_row.append(by_fy_piid_count[fy].get(p, 0))
            w.writerow(amt_row)
    print(f"Wrote {out}  ({len(fys)} FY × {len(piids)} PIIDs)")


def write_top_parents_csv(top, total_records):
    out = os.path.join(OUT, "sam_subaward_top_parents.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Parent UEI or fallback key", "Display name", "Total $M",
                    "Sub action count", "% of total"])
        grand_total = sum(s["amount"] for _, s in top)
        for key, slot in top:
            pct = 100 * slot["amount"] / grand_total if grand_total else 0
            w.writerow([key, slot["name"], round(slot["amount"] / 1e6, 2),
                        slot["count"], f"{pct:.2f}%"])
    print(f"Wrote {out}  (top {len(top)} parents)")


def write_sam_vs_usaspending_csv():
    sam_path = os.path.join(SAM_DIR, "_summary.json")
    if not os.path.exists(sam_path):
        print("SAM summary missing — skip comparison")
        return
    with open(sam_path) as f:
        sam_sum = json.load(f).get("piids", {})

    usa_path = os.path.join(USA_DIR, "_summary.json")
    usa_sum = {}
    if os.path.exists(usa_path):
        with open(usa_path) as f:
            usa_sum = json.load(f).get("piids", {})

    out = os.path.join(OUT, "sam_vs_usaspending_per_piid.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["PIID", "Label", "SAM records", "USA records",
                    "Recovered (SAM - USA)", "SAM $M", "USA $M",
                    "$M delta (SAM - USA)"])
        for piid, sam_meta in sam_sum.items():
            sam_recs = sam_meta.get("published_count", 0)
            sam_amt = sam_meta.get("published_total_$", 0)
            usa_meta = usa_sum.get(piid, {})
            usa_recs = usa_meta.get("subaward_count", 0)
            usa_amt = usa_meta.get("subaward_total", 0)
            w.writerow([
                piid,
                sam_meta.get("label", ""),
                sam_recs,
                usa_recs,
                sam_recs - usa_recs,
                round(sam_amt / 1e6, 2),
                round(usa_amt / 1e6, 2),
                round((sam_amt - usa_amt) / 1e6, 2),
            ])
    print(f"Wrote {out}")


def main():
    records = load_all_sam_records()
    if not records:
        print("No SAM records found — has the pull completed?")
        return
    print(f"Loaded {len(records):,} SAM published records across all PIIDs")

    diag = dedup_check(records)
    diag_path = os.path.join(OUT, "sam_subaward_full_dedup_check.txt")
    with open(diag_path, "w") as f:
        f.write("SAM.gov subaward dedup verification\n")
        f.write("=" * 50 + "\n")
        for k, v in diag.items():
            f.write(f"  {k}: {v}\n")
        f.write("\nPer SAM_GOV_HOWTO.md: subAwardReportId should be unique.\n")
        if diag["collision_count"] == 0:
            f.write("RESULT: VERIFIED CLEAN — naive sum of subAwardAmount is correct.\n")
        else:
            f.write(f"WARN: {diag['collision_count']} collisions found — investigate before summing.\n")
    print(f"Wrote {diag_path}")
    for k, v in diag.items():
        print(f"  {k}: {v}")

    sub_to_parent = build_sub_to_parent_lookup(records)
    print(f"Built sub→parent UEI lookup: {len(sub_to_parent):,} mappings")

    by_fy_piid, by_fy_piid_count = aggregate_per_fy_per_piid(records)
    write_per_fy_csv(by_fy_piid, by_fy_piid_count)

    top = aggregate_top_parents(records, sub_to_parent, top_n=200)
    write_top_parents_csv(top, len(records))

    write_sam_vs_usaspending_csv()

    print("\nTop 15 parent recipients (across all DDG PIIDs):")
    for i, (key, slot) in enumerate(top[:15], 1):
        print(f"  {i:>2}. {slot['name'][:60]:<60s}  ${slot['amount']/1e6:>9,.1f}M  ({slot['count']:>5,} subs)")


if __name__ == "__main__":
    main()
