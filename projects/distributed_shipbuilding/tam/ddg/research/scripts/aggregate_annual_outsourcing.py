#!/usr/bin/env python3
"""
Aggregate the FPDS + USAspending raw pulls into per-FY annual outsourcing rollups.

This is the "how much did HII-Ingalls + GD-BIW outsource per year" answer in tabular
form, plus the GFE prime spend (LM-Aegis, Raytheon, GE-LM2500, BAE-guns, etc.) that
flows around the yards.

Outputs (in extracted/):
  fpds_annual_by_prime.csv    Per-FY sum of obligatedAmount on DDG primes + GFE
                              vendors (per-mod, by signed_date FY).
  subaward_annual_by_prime.csv  Per-FY sum of subaward action_date amounts grouped
                                by prime PIID, plus top-5 sub recipients per PIID.
  subaward_top_recipients.csv   Across all DDG PIIDs, the top sub recipients summed
                                across the whole window.

Run after pull_fpds_ddg_primes.py and pull_usaspending_subawards.py have completed.
"""
import csv
import json
import os
import re
import sys
from collections import defaultdict
from datetime import datetime

# Shared contaminant exclusion list (IVECO + DDG-1000 + WPN/OPN weapons).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from aggregate_new_construction import OUT_OF_SCOPE_PIIDS as EXCLUDED_PIIDS
except ImportError:
    EXCLUDED_PIIDS = {}

FPDS_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/fpds_raw"
FPDS_V2_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/fpds_raw_v2"  # de-capped BIW + Rolls-Royce recovery
USA_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/usaspending_subawards"
OUT = "/Users/brendantoole/projects2/destroyer_outsourced_work/extracted"
os.makedirs(OUT, exist_ok=True)


def signed_date_to_fy(d):
    """US federal fiscal year: starts Oct 1. e.g. 2024-10-15 → FY25."""
    if not d:
        return None
    try:
        dt = datetime.fromisoformat(d[:10])
    except Exception:
        return None
    return dt.year + 1 if dt.month >= 10 else dt.year


# DDG-specific vendor groups. Both shipyards are PRIMES of DDG construction (HII-Ingalls
# and GD-BIW). The other groups are GFE primes — large mission systems shipped to the
# yards for installation rather than subcontracted by the yards.
DDG_VENDOR_PATTERNS = {
    "HII-Ingalls": re.compile(r"INGALLS SHIPBUILDING|HUNTINGTON INGALLS", re.I),
    "GD-BIW": re.compile(r"BATH IRON WORKS", re.I),
    "LM-Aegis": re.compile(r"LOCKHEED MARTIN", re.I),
    "Raytheon": re.compile(r"RAYTHEON|RTX(\b|[^A-Z])", re.I),
    "GE-Propulsion": re.compile(r"GENERAL ELECTRIC|GE AEROSPACE", re.I),
    "Rolls-Royce": re.compile(r"ROLLS.?ROYCE", re.I),
    "BAE-Guns/VLS": re.compile(r"BAE SYSTEMS", re.I),
    "L3Harris": re.compile(r"L3HARRIS|L-?3 TECHNOLOGIES", re.I),
    "NG": re.compile(r"NORTHROP GRUMMAN", re.I),
    "DRS": re.compile(r"LEONARDO DRS|DRS SYSTEMS|DRS LAUREL|DRS NAVAL", re.I),
    "GD-MissionSys": re.compile(r"GENERAL DYNAMICS MISSION", re.I),
}


def normalize_vendor_to_group(name):
    if not name:
        return None
    for group, pat in DDG_VENDOR_PATTERNS.items():
        if pat.search(name):
            return group
    return None


def aggregate_fpds_annual():
    """Per-FY sum of obligatedAmount (this-mod, NOT cumulative) across all FPDS pull files.

    Dedupe by (PIID, mod_number, signed_date) to avoid double-counting records that
    appear in multiple queries. Bucket the THIS-MOD obligatedAmount by signed_date FY."""
    by_fy_group = defaultdict(lambda: defaultdict(float))
    by_fy_group_piid_count = defaultdict(lambda: defaultdict(set))
    seen_records = set()

    # Read the original pull AND the de-capped recovery (fpds_raw_v2). Dedup by
    # (piid, mod, signed_date) unions them: v2 supersedes the capped BIW/RR slugs.
    for fpds_dir in (FPDS_DIR, FPDS_V2_DIR):
        if not os.path.isdir(fpds_dir):
            continue
        for fname in os.listdir(fpds_dir):
            if not fname.endswith("_raw.json") or fname.startswith("_"):
                continue
            path = os.path.join(fpds_dir, fname)
            with open(path) as f:
                data = json.load(f)
            for r in data.get("records", []):
                sig = (r.get("full_piid") or r.get("piid"), r.get("mod_number"), r.get("signed_date"))
                if sig in seen_records:
                    continue
                seen_records.add(sig)
                if (r.get("piid") or "").replace("-", "") in EXCLUDED_PIIDS:
                    continue  # contaminants: DDG-1000 / WPN-OPN weapons / IVECO
                fy = signed_date_to_fy(r.get("signed_date"))
                if not fy:
                    continue
                group = normalize_vendor_to_group(r.get("vendor_name"))
                if not group:
                    continue
                by_fy_group[fy][group] += r.get("this_obligated") or 0
                by_fy_group_piid_count[fy][group].add(r.get("piid"))

    fys = sorted(by_fy_group.keys())
    groups = sorted({g for d in by_fy_group.values() for g in d.keys()})

    with open(os.path.join(OUT, "fpds_annual_by_prime.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["FY"] + [f"{g}_obligated_$M" for g in groups] +
                   [f"{g}_piid_count" for g in groups])
        for fy in fys:
            row = [fy]
            for g in groups:
                row.append(round(by_fy_group[fy].get(g, 0) / 1e6, 2))
            for g in groups:
                row.append(len(by_fy_group_piid_count[fy].get(g, set())))
            w.writerow(row)
    print(f"Wrote fpds_annual_by_prime.csv ({len(fys)} FY rows × {len(groups)} groups)")
    return by_fy_group


def aggregate_subaward_annual():
    """Per-FY sum of subaward action_date amounts across all PIID-keyed subaward files."""
    by_fy_piid = defaultdict(lambda: defaultdict(float))
    by_fy_recipient = defaultdict(lambda: defaultdict(float))
    by_piid_recipient = defaultdict(lambda: defaultdict(float))
    overall_recipient = defaultdict(float)

    summary_path = os.path.join(USA_DIR, "_summary.json")
    if not os.path.exists(summary_path):
        print("USAspending summary not present yet; skipping subaward aggregation")
        return None
    with open(summary_path) as f:
        summary = json.load(f).get("piids", {})

    for piid, meta in summary.items():
        if not meta.get("found"):
            continue
        if (piid or "").replace("-", "") in EXCLUDED_PIIDS:
            continue  # contaminants: DDG-1000 / WPN-OPN weapons / IVECO (incl. Thales artifact)
        sub_path = meta.get("output_file")
        if not sub_path or not os.path.exists(sub_path):
            continue
        with open(sub_path) as f:
            data = json.load(f)
        for s in data.get("subawards", []):
            action_date = s.get("action_date") or s.get("sub_award_date")
            fy = signed_date_to_fy(action_date)
            if not fy:
                continue
            amt = s.get("amount") or 0
            recip = (s.get("recipient_name") or "UNKNOWN").upper().strip()
            by_fy_piid[fy][piid] += amt
            by_fy_recipient[fy][recip] += amt
            by_piid_recipient[piid][recip] += amt
            overall_recipient[recip] += amt

    fys = sorted(by_fy_piid.keys())
    piids = sorted({p for d in by_fy_piid.values() for p in d.keys()})

    with open(os.path.join(OUT, "subaward_annual_by_prime.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["FY"] + [f"{p}_$M" for p in piids] + ["FY_TOTAL_$M"])
        for fy in fys:
            row = [fy]
            total = 0
            for p in piids:
                val = by_fy_piid[fy].get(p, 0)
                row.append(round(val / 1e6, 2))
                total += val
            row.append(round(total / 1e6, 2))
            w.writerow(row)
    print(f"Wrote subaward_annual_by_prime.csv ({len(fys)} FY × {len(piids)} PIIDs)")

    top = sorted(overall_recipient.items(), key=lambda kv: kv[1], reverse=True)[:200]
    with open(os.path.join(OUT, "subaward_top_recipients.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Recipient", "Total_$M_across_window"])
        for r, a in top:
            w.writerow([r, round(a / 1e6, 2)])
    print(f"Wrote subaward_top_recipients.csv (top {len(top)} recipients)")

    return by_fy_piid


def main():
    print("=== FPDS annual rollup ===")
    aggregate_fpds_annual()
    print()
    print("=== USAspending subaward annual rollup ===")
    aggregate_subaward_annual()


if __name__ == "__main__":
    main()
