#!/usr/bin/env python3
"""
Aggregate the FPDS + USAspending raw pulls into per-FY annual outsourcing rollups.

This is the "how much did GDEB outsource per year" answer in tabular form.

Outputs (in extracted/):
  fpds_annual_by_prime.csv    Per-FY sum of obligatedAmount on GDEB/HII-NNS/BPMI
                              prime contracts (per-mod, by signed_date FY).
  subaward_annual_by_prime.csv  Per-FY sum of subaward action_date amounts grouped
                                by prime PIID, plus top-5 sub recipients per PIID.
  subaward_top_recipients.csv   Across all submarine PIIDs, the top sub recipients
                                summed across the whole window.
  outsourcing_summary.csv       One-row summary per FY: total GDEB sub spend visible,
                                + BPMI prime spend (GFE), + LM Trident etc.

Run after pull_fpds_sub_primes.py and pull_usaspending_subawards.py have completed.
"""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import datetime

FPDS_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/fpds_raw"
USA_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/usaspending_subawards"
OUT = "/Users/brendantoole/projects2/submarine_outsourced_work/extracted"
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


SUB_PRIME_VENDOR_PATTERNS = {
    "GDEB": re.compile(r"ELECTRIC BOAT", re.I),
    "HII-NNS": re.compile(r"NEWPORT NEWS SHIPBUILDING|HUNTINGTON INGALLS", re.I),
    "BPMI": re.compile(r"BECHTEL PLANT MACHINERY", re.I),
    "LM": re.compile(r"LOCKHEED MARTIN", re.I),
    "NG": re.compile(r"NORTHROP GRUMMAN", re.I),
    "BAE": re.compile(r"BAE SYSTEMS", re.I),
    "L3Harris": re.compile(r"L3HARRIS|L-?3 TECHNOLOGIES|KOLLMORGEN", re.I),
    "Curtiss-Wright": re.compile(r"CURTISS.?WRIGHT", re.I),
    "Rolls-Royce": re.compile(r"ROLLS.?ROYCE", re.I),
    "BlueForge": re.compile(r"BLUEFORGE|BLUE FORGE", re.I),
}


def normalize_vendor_to_group(name):
    if not name:
        return None
    for group, pat in SUB_PRIME_VENDOR_PATTERNS.items():
        if pat.search(name):
            return group
    return None


def aggregate_fpds_annual():
    """Per-FY sum of obligatedAmount (this-mod, NOT cumulative) across all FPDS pull files.

    Per the lessons learned: dedupe by (PIID, mod_number, signed_date) to avoid double-
    counting records that appear in multiple queries. Bucket the THIS-MOD obligatedAmount
    by signed_date FY. This gives the true annual delta — NOT the cumulative
    totalObligatedAmount, which would massively over-count."""
    by_fy_group = defaultdict(lambda: defaultdict(float))  # fy → group → sum
    by_fy_group_piid_count = defaultdict(lambda: defaultdict(set))
    seen_records = set()

    for fname in os.listdir(FPDS_DIR):
        if not fname.endswith("_raw.json") or fname.startswith("_"):
            continue
        path = os.path.join(FPDS_DIR, fname)
        with open(path) as f:
            data = json.load(f)
        for r in data.get("records", []):
            sig = (r.get("full_piid") or r.get("piid"), r.get("mod_number"), r.get("signed_date"))
            if sig in seen_records:
                continue
            seen_records.add(sig)
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

    # Per-FY per-PIID
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

    # Top recipients overall
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
