#!/usr/bin/env python3
"""
Final consolidator: per-FY budget vs subawards with the MIB / BlueForge stripped out.

Three pairings of (budget denominator, subaward numerator):
  A. Total SCN TOA            vs Total subs (everything)
  B. SCN minus Plan Costs     vs Subs minus BlueForge (strips MIB consortium)
  C. Basic Construction only  vs Subs minus BlueForge (cleanest "shipyard outsourcing")

Note that the Basic Construction figure is a SHIP-LEVEL cost commitment as of
authorization FY. The subaward $ is actual cash flow in that calendar FY.
They are NOT one-for-one (a ship's construction spans 5-10 years and its sub spend
flows over that whole period). But for order-of-magnitude comparison, they show
how much of "what's spent on building submarines" reaches first-tier subs.

Reads:
  extracted/scn_per_fy_actual_toa.csv         (Total Obligation Authority per FY)
  extracted/scn_p5c_per_fy_reconciled.csv     (Basic Construction + Plan Costs per ship-FY)
  sam_subawards/*.json                         (raw SAM subaward records)

Writes:
  extracted/annual_budget_vs_subawards_v2.csv  Final headline table
"""
import csv
import json
import os
import re
from collections import defaultdict
from datetime import datetime

EXTRACT = "/Users/brendantoole/projects2/submarine_outsourced_work/extracted"
SAM_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/sam_subawards"
WINDOW_FYS = list(range(2020, 2028))


def parse_dollar(s):
    if not s or s.strip() in ("-", "*.***", "0.000", "0"):
        return 0.0
    return float(str(s).replace(",", "").replace("$", ""))


def fy_from_date(d):
    if not d: return None
    try: dt = datetime.fromisoformat(str(d)[:10])
    except: return None
    return dt.year + 1 if dt.month >= 10 else dt.year


def load_toa_per_fy():
    """Per-FY Total Obligation Authority — sum across LIs (Columbia + Virginia)."""
    out = defaultdict(float)
    with open(os.path.join(EXTRACT, "scn_per_fy_actual_toa.csv")) as f:
        for row in csv.DictReader(f):
            if row["Row Label"] != "Total Obligation Authority ($ in Millions)":
                continue
            fy = int(row["FY"])
            out[fy] += parse_dollar(row["Best Value"])
    return out


def load_p5c_per_fy(cost_category):
    """Per-FY sum across LIs for a specific cost category."""
    out = defaultdict(float)
    with open(os.path.join(EXTRACT, "scn_p5c_per_fy_reconciled.csv")) as f:
        for row in csv.DictReader(f):
            if row["Cost Category"] != cost_category:
                continue
            fy = int(row["FY"])
            out[fy] += parse_dollar(row["Best Value $M"])
    return out


def load_sam_subaward_by_fy_split_blueforge():
    """Return (total_by_fy, blueforge_by_fy, other_by_fy) summed across all PIIDs."""
    total = defaultdict(float)
    blueforge = defaultdict(float)
    other = defaultdict(float)
    for fname in os.listdir(SAM_DIR):
        if not fname.endswith("_subawards.json") or fname.startswith("_"):
            continue
        with open(os.path.join(SAM_DIR, fname)) as f:
            data = json.load(f)
        for r in data.get("published", []):
            fy = fy_from_date(r.get("subAwardDate"))
            if not fy:
                continue
            amt = float(r.get("subAwardAmount") or 0)
            name = (r.get("subEntityParentLegalBusinessName") or
                    r.get("subEntityLegalBusinessName") or "").upper()
            total[fy] += amt
            if "BLUEFORGE" in name or "BLUE FORGE" in name:
                blueforge[fy] += amt
            else:
                other[fy] += amt
    return total, blueforge, other


def main():
    toa = load_toa_per_fy()
    basic = load_p5c_per_fy("Basic Construction/Conversion")
    plans = load_p5c_per_fy("Plan Costs")
    total_subs, bf_subs, other_subs = load_sam_subaward_by_fy_split_blueforge()

    out_path = os.path.join(EXTRACT, "annual_budget_vs_subawards_v2.csv")
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "FY",
            "SCN TOA $M",
            "Plan Costs $M (includes MIB)",
            "TOA - Plan Costs $M (≈ non-MIB SCN)",
            "Basic Construction $M",
            "Total subs $M (SAM)",
            "BlueForge subs $M",
            "Non-BlueForge subs $M",
            "A. Total subs / TOA",
            "B. Non-BF subs / (TOA - Plans)",
            "C. Non-BF subs / Basic Construction",
            "Notes",
        ])
        print(f"{'FY':<5}{'TOA':>9}{'Plans':>9}{'Basic':>9}{'AllSubs':>9}{'BF':>8}{'NonBF':>8}{'A%':>6}{'B%':>6}{'C%':>6}")
        for fy in WINDOW_FYS:
            t = toa.get(fy, 0)
            pl = plans.get(fy, 0)
            bc = basic.get(fy, 0)
            ts = total_subs.get(fy, 0) / 1e6
            bf = bf_subs.get(fy, 0) / 1e6
            nbf = other_subs.get(fy, 0) / 1e6
            non_plan_toa = t - pl
            a = (100 * ts / t) if t else 0
            b = (100 * nbf / non_plan_toa) if non_plan_toa else 0
            c = (100 * nbf / bc) if bc else 0
            notes = []
            if fy == 2025:
                notes.append("subaward $ lag-depressed")
            if fy == 2026:
                notes.append("FY26 estimate; subs heavily lag-depressed")
            if fy == 2027:
                notes.append("FY27 request; no subs yet")
            w.writerow([
                fy, round(t, 1), round(pl, 1), round(non_plan_toa, 1), round(bc, 1),
                round(ts, 1), round(bf, 1), round(nbf, 1),
                f"{a:.1f}%", f"{b:.1f}%", f"{c:.1f}%",
                "; ".join(notes),
            ])
            print(f"{fy:<5}{t:>9,.0f}{pl:>9,.0f}{bc:>9,.0f}{ts:>9,.0f}{bf:>8,.0f}{nbf:>8,.0f}"
                  f"{a:>5.1f}%{b:>5.1f}%{c:>5.1f}%")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
