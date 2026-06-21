#!/usr/bin/env python3
"""
DDG-51 new-construction aggregator.

Filters existing SAM.gov subaward JSON pulls down to:
  - in-scope DDG-51 new-construction PIIDs (drops any EOH / sustainment / DDG MOD work
    if those show up in the discovery)
  - excludes industrial-base / workforce / pass-through UEIs (none known for DDG yet,
    but the list is here for future additions — submarines have BlueForge etc.)

Outputs:
  extracted/nc_annual_by_piid.csv     per FY × PIID, with FY totals
  extracted/nc_annual_by_vendor.csv   per FY top vendors (parent-UEI rolled)
  extracted/nc_lifetime_vendors.csv   top vendors across whole window
  extracted/nc_records_long.csv       one row per subaward action (for the workbook)
  extracted/nc_scope_summary.json     audit trail: what was kept / excluded

This script reads its in-scope PIID list from
usaspending_subawards/_discovered_piids.json (produced by --discover mode of the
USAspending pull). Override by hardcoding IN_SCOPE_PIIDS_OVERRIDE below if needed.
"""
import csv
import glob
import json
import os
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
OUT = REPO / "extracted"
OUT.mkdir(exist_ok=True)

# Override: if you want to pin a specific set of PIIDs as in-scope, fill this in.
# Format: { "PIID": ("group", "class", "label") }. Empty = use discovered PIIDs.
IN_SCOPE_PIIDS_OVERRIDE = {}

# Out-of-scope PIIDs — excluded from the in-scope DDG-51 NEW-CONSTRUCTION set and
# enforced in main() (popped from in_scope, so they drop out of every nc_* output and
# the scope summary). Three contaminant classes identified 2026-05-28; see
# METHODOLOGY.md sec 8. Raw pulls remain on disk under sam_subawards/ — only the
# aggregation excludes them. Also imported by aggregate_sam_subawards.py.
OUT_OF_SCOPE_PIIDS = {
    # Marine Corps contamination (not DDG, not even Navy SCN)
    "M6785416C0006": "MARCORSYSCOM Mk110 gun (IVECO) — Marine Corps, not DDG",
    # DDG-1000 Zumwalt — out of class (LI 2119, OPN-funded modernization)
    "N0002423C2324": "DDG-1000 Zumwalt BYMP — out of class",
    "N0002422C2300": "DDG-1002 Zumwalt CSA — out of class",
    "N0002410C5126": "DDG-1002 MSE — DDG-1000 out of class",
    "N0002417C5145": "DDG-1000 MSE/TSCE — out of class",
    "N0002422C5522": "DDG-1000 systems engineering — out of class",
    "N0002413C5212": "DDG-1000 opt year 4 — out of class",
    # WPN/OPN weapons — different appropriation than SCN (would double-count)
    "N0002415C5420": "ESSM Block 2 EMD — WPN/OPN weapon (also the Thales $4.2B artifact PIID)",
    "N0002421C5408": "ESSM Block 2 spares — WPN/OPN weapon",
    "N0002416C5433": "ESSM design agent — WPN/OPN weapon",
    "N0002426C5434": "ESSM CY26-30 design agent — WPN/OPN weapon",
    "N0002424C5406": "CIWS FY25 production — WPN/OPN weapon",
    "N0002418C5406": "CIWS Mk15 Phalanx U&C — WPN/OPN weapon",
    "N0038319F0VP0": "CIWS PBL support — WPN/OPN weapon (sustainment)",
    "N0010418F0E40": "CIWS PBL definitization — WPN/OPN weapon",
    "N0038321F0ZM0": "CIWS long-term contract — WPN/OPN weapon",
}

# Industrial-base / workforce / pass-through UEIs to exclude on the recipient side.
# Add UEIs here as DDG-specific MIB-style flows are identified.
MIB_EXCLUDED_UEIS = {}


def fy_of(date_str):
    if not date_str or len(date_str) < 10:
        return None
    y, m = int(date_str[:4]), int(date_str[5:7])
    return y + 1 if m >= 10 else y


def recipient_uei(rec):
    return (rec.get("subParentUei") or rec.get("subEntityUei") or "").strip()


def recipient_name(rec):
    return ((rec.get("subEntityParentLegalBusinessName") or
             rec.get("subEntityLegalBusinessName") or "UNKNOWN")
            .upper().strip())


def is_foreign(rec):
    addr = rec.get("entityPhysicalAddress") or {}
    country = (addr.get("country") or {}).get("code", "") or ""
    return country.upper() not in ("USA", "")


def load_in_scope_piids():
    """Resolve in-scope PIIDs: override > discovered. Returns dict matching
    submarine project's format {PIID: (group, class, label)}."""
    if IN_SCOPE_PIIDS_OVERRIDE:
        return IN_SCOPE_PIIDS_OVERRIDE
    disc_path = REPO / "extracted" / "_discovered_piids.json"
    if disc_path.exists():
        disc = json.load(open(disc_path))
        # Format from discovery: [(piid, label, vendor)] where label = "GROUP: descr"
        out = {}
        for tup in disc:
            piid, label, vendor = tup[0], tup[1], tup[2] if len(tup) > 2 else ""
            group = label.split(":", 1)[0] if ":" in label else ""
            out[piid] = (group, "DDG-51", label)
        return out
    return {}


def main():
    in_scope = load_in_scope_piids()
    removed = [p for p in OUT_OF_SCOPE_PIIDS if in_scope.pop(p, None) is not None]
    if removed:
        print(f"Excluded {len(removed)} out-of-scope PIIDs (IVECO + DDG-1000 + WPN/OPN weapons): "
              + ", ".join(removed))
    if not in_scope:
        print("No in-scope PIIDs found. Run pull_usaspending_subawards.py --discover first,")
        print("or hardcode IN_SCOPE_PIIDS_OVERRIDE in this script.")
        return
    print(f"Loaded {len(in_scope)} in-scope DDG-51 PIIDs from discovery output")

    in_records = []
    excluded_piid_records = 0
    excluded_mib_records = 0
    excluded_mib_dollars = 0.0

    for f in sorted(glob.glob(str(REPO / "sam_subawards" / "N*.json"))):
        piid_file = Path(f).stem.split("_")[0]
        if piid_file not in in_scope:
            d = json.load(open(f))
            excluded_piid_records += len(d.get("published", []))
            continue
        d = json.load(open(f))
        for r in d.get("published", []):
            uei = recipient_uei(r)
            if uei in MIB_EXCLUDED_UEIS:
                excluded_mib_records += 1
                excluded_mib_dollars += float(r.get("subAwardAmount") or 0)
                continue
            in_records.append(r)

    print(f"Kept: {len(in_records):,} records "
          f"(after filtering {excluded_piid_records:,} out-of-scope PIID records + "
          f"{excluded_mib_records:,} MIB vendor records = ${excluded_mib_dollars/1e6:,.1f}M)",
          flush=True)

    # ---- Build per-FY × PIID table -------------------------------------------
    by_fy_piid_amt = defaultdict(float)
    by_fy_piid_cnt = defaultdict(int)
    fys = set()
    for r in in_records:
        fy = fy_of(r.get("subAwardDate"))
        if fy is None:
            continue
        amt = float(r.get("subAwardAmount") or 0)
        piid = r["piid"]
        by_fy_piid_amt[(fy, piid)] += amt
        by_fy_piid_cnt[(fy, piid)] += 1
        fys.add(fy)

    piids_sorted = sorted(in_scope.keys())
    fys_sorted = sorted(fys)

    with open(OUT / "nc_annual_by_piid.csv", "w", newline="") as fout:
        w = csv.writer(fout)
        w.writerow(["FY"] + [f"{p}_$M" for p in piids_sorted] + ["FY_TOTAL_$M"] +
                   [f"{p}_count" for p in piids_sorted] + ["FY_TOTAL_count"])
        for fy in fys_sorted:
            amts = [by_fy_piid_amt[(fy, p)] / 1e6 for p in piids_sorted]
            cnts = [by_fy_piid_cnt[(fy, p)] for p in piids_sorted]
            w.writerow([fy] + [f"{a:.2f}" for a in amts] + [f"{sum(amts):.2f}"] +
                       cnts + [sum(cnts)])

    # ---- Build per-FY × vendor table -----------------------------------------
    by_fy_vendor = defaultdict(
        lambda: {"name": "", "amt": 0.0, "n": 0, "foreign": False}
    )
    for r in in_records:
        fy = fy_of(r.get("subAwardDate"))
        if fy is None:
            continue
        uei = recipient_uei(r)
        v = by_fy_vendor[(fy, uei)]
        if not v["name"]:
            v["name"] = recipient_name(r)
        v["amt"] += float(r.get("subAwardAmount") or 0)
        v["n"] += 1
        if is_foreign(r):
            v["foreign"] = True

    rows_by_vendor = []
    for (fy, uei), v in by_fy_vendor.items():
        rows_by_vendor.append({
            "fy": fy, "uei": uei, "vendor": v["name"],
            "foreign": "Yes" if v["foreign"] else "",
            "amount_M": v["amt"] / 1e6, "records": v["n"],
        })
    rows_by_vendor.sort(key=lambda r: (r["fy"], -r["amount_M"]))

    with open(OUT / "nc_annual_by_vendor.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["fy", "uei", "vendor", "foreign",
                                              "amount_M", "records"])
        w.writeheader()
        for row in rows_by_vendor:
            row["amount_M"] = f"{row['amount_M']:.4f}"
            w.writerow(row)

    # ---- Lifetime top-vendor rollup ------------------------------------------
    lifetime = defaultdict(
        lambda: {"name": "", "amt": 0.0, "n": 0, "fys": set(), "piids": set(),
                 "foreign": False}
    )
    for r in in_records:
        uei = recipient_uei(r)
        v = lifetime[uei]
        if not v["name"]:
            v["name"] = recipient_name(r)
        v["amt"] += float(r.get("subAwardAmount") or 0)
        v["n"] += 1
        fy = fy_of(r.get("subAwardDate"))
        if fy:
            v["fys"].add(fy)
        v["piids"].add(r["piid"])
        if is_foreign(r):
            v["foreign"] = True

    lifetime_rows = sorted(
        ({"rank": 0, "uei": uei, "vendor": v["name"],
          "foreign": "Yes" if v["foreign"] else "",
          "amount_M_lifetime": v["amt"] / 1e6,
          "records": v["n"],
          "fy_count": len(v["fys"]),
          "fys": ",".join(str(y) for y in sorted(v["fys"])),
          "piid_count": len(v["piids"]),
          "piids": ",".join(sorted(v["piids"])),
         } for uei, v in lifetime.items()),
        key=lambda x: -x["amount_M_lifetime"],
    )
    for i, row in enumerate(lifetime_rows, start=1):
        row["rank"] = i

    with open(OUT / "nc_lifetime_vendors.csv", "w", newline="") as fout:
        w = csv.DictWriter(fout, fieldnames=["rank", "uei", "vendor", "foreign",
                                              "amount_M_lifetime", "records",
                                              "fy_count", "fys",
                                              "piid_count", "piids"])
        w.writeheader()
        for row in lifetime_rows:
            row["amount_M_lifetime"] = f"{row['amount_M_lifetime']:.4f}"
            w.writerow(row)

    # ---- Long-form record table ----------------------------------------------
    with open(OUT / "nc_records_long.csv", "w", newline="") as fout:
        w = csv.writer(fout)
        w.writerow(["piid", "fy", "subAwardDate", "subAwardAmount_$",
                    "subAwardReportId", "subAwardNumber",
                    "sub_parent_uei", "sub_entity_uei", "sub_name", "foreign",
                    "prime_entity_name", "prime_naics_code", "prime_naics_desc",
                    "description_of_requirement"])
        for r in in_records:
            fy = fy_of(r.get("subAwardDate"))
            pnaics = r.get("primeNaics") or {}
            w.writerow([
                r.get("piid"), fy, r.get("subAwardDate"),
                f"{float(r.get('subAwardAmount') or 0):.2f}",
                r.get("subAwardReportId"), r.get("subAwardNumber"),
                r.get("subParentUei") or "", r.get("subEntityUei") or "",
                recipient_name(r), "Yes" if is_foreign(r) else "",
                r.get("primeEntityName") or "",
                pnaics.get("code") or "", pnaics.get("description") or "",
                r.get("descriptionOfRequirement") or "",
            ])

    # ---- Audit / scope summary -----------------------------------------------
    summary = {
        "in_scope_piids": {p: {"group": g, "class": c, "label": lbl}
                            for p, (g, c, lbl) in in_scope.items()},
        "out_of_scope_piids": OUT_OF_SCOPE_PIIDS,
        "excluded_mib_ueis": MIB_EXCLUDED_UEIS,
        "records_kept": len(in_records),
        "records_excluded_out_of_scope_piids": excluded_piid_records,
        "records_excluded_mib": excluded_mib_records,
        "dollars_excluded_mib_$M": excluded_mib_dollars / 1e6,
        "fy_range": [min(fys_sorted), max(fys_sorted)] if fys_sorted else None,
        "total_dollars_in_scope_$M": sum(r.get("subAwardAmount") and float(r["subAwardAmount"]) or 0
                                          for r in in_records) / 1e6,
        "unique_parent_ueis_in_scope": len({recipient_uei(r) for r in in_records}),
    }
    with open(OUT / "nc_scope_summary.json", "w") as fout:
        json.dump(summary, fout, indent=2, default=str)

    print()
    print(f"Records kept (in-scope, MIB stripped): {summary['records_kept']:,}")
    print(f"Dollars kept: ${summary['total_dollars_in_scope_$M']:,.1f}M")
    print(f"Unique parent UEIs: {summary['unique_parent_ueis_in_scope']:,}")
    print(f"FY range: {summary['fy_range']}")
    print()
    print("Per-FY totals (in scope, MIB stripped):")
    for fy in fys_sorted:
        total = sum(by_fy_piid_amt[(fy, p)] for p in piids_sorted) / 1e6
        cnt = sum(by_fy_piid_cnt[(fy, p)] for p in piids_sorted)
        print(f"  FY{fy}: ${total:>9,.1f}M   ({cnt:>5,} records)")

    print()
    print("Top 10 vendors lifetime (in scope, MIB stripped):")
    for row in lifetime_rows[:10]:
        print(f"  {row['rank']:>2}. {row['vendor'][:50]:<50}  "
              f"${float(row['amount_M_lifetime']):>8,.1f}M   "
              f"FYs={row['fy_count']}  PIIDs={row['piid_count']}")


if __name__ == "__main__":
    main()
