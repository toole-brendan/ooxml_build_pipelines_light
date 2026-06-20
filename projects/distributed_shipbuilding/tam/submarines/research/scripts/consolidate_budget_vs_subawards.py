#!/usr/bin/env python3
"""
Build the final per-FY budget-vs-subaward comparison table.

Reads:
  extracted/scn_per_fy_actual_toa.csv          (per-FY TOA, multi-vintage reconciled)
  extracted/subaward_annual_by_prime.csv       (USAspending subaward $ by FY)

Writes:
  extracted/annual_budget_vs_subawards.csv     One row per FY, with:
    - Columbia TOA ($M)
    - Virginia TOA ($M)
    - Total submarine SCN TOA ($M)
    - USAspending subaward $ visible ($M)
    - Implied % of SCN that's first-tier subawarded
    - Ship counts (Columbia + Virginia procured that FY)
"""
import csv
import os
import re
from collections import defaultdict

EXTRACT = "/Users/brendantoole/projects2/submarine_outsourced_work/extracted"

WINDOW_FYS = list(range(2020, 2028))  # FY20-27 inclusive


def parse_dollar(s):
    """Parse '1,820.927' or '-' → float. Returns 0.0 for blanks/dashes/stars."""
    if not s or s.strip() in ("-", "*.***", "0.000", "0"):
        return 0.0
    return float(s.replace(",", "").replace("$", ""))


def load_toa():
    """Return {(li, fy): (toa_$M, source_vintage)} from reconciled CSV."""
    out = {}
    path = os.path.join(EXTRACT, "scn_per_fy_actual_toa.csv")
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            if row["Row Label"] != "Total Obligation Authority ($ in Millions)":
                continue
            li = int(row["LI"])
            fy = int(row["FY"])
            out[(li, fy)] = (parse_dollar(row["Best Value"]), row["Source Vintage (PB Year)"])
    return out


def load_quantity():
    """Return {(li, fy): qty} from reconciled CSV."""
    out = {}
    path = os.path.join(EXTRACT, "scn_per_fy_actual_toa.csv")
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            if row["Row Label"] != "Procurement Quantity (Units in Each)":
                continue
            li = int(row["LI"])
            fy = int(row["FY"])
            v = row["Best Value"]
            try:
                out[(li, fy)] = int(v) if v and v != "-" else 0
            except ValueError:
                out[(li, fy)] = 0
    return out


def load_usa_subaward_total_by_fy():
    """Return {fy: total_$M} summed across all PIIDs from USAspending CSV."""
    out = defaultdict(float)
    path = os.path.join(EXTRACT, "subaward_annual_by_prime.csv")
    if not os.path.exists(path):
        return out
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                fy = int(row["FY"])
            except (ValueError, KeyError):
                continue
            try:
                out[fy] = float(row["FY_TOTAL_$M"])
            except (ValueError, KeyError):
                pass
    return out


def load_sam_subaward_total_by_fy():
    """Return {fy: total_$M} summed across all PIIDs from SAM.gov CSV."""
    out = defaultdict(float)
    path = os.path.join(EXTRACT, "sam_subaward_annual_by_prime.csv")
    if not os.path.exists(path):
        return out
    with open(path) as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                fy = int(row["FY"])
            except (ValueError, KeyError):
                continue
            try:
                out[fy] = float(row["FY_TOTAL_$M"])
            except (ValueError, KeyError):
                pass
    return out


def main():
    toa = load_toa()
    qty = load_quantity()
    usa_subs = load_usa_subaward_total_by_fy()
    sam_subs = load_sam_subaward_total_by_fy()

    out_path = os.path.join(EXTRACT, "annual_budget_vs_subawards.csv")
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "FY",
            "Columbia TOA $M",
            "Columbia source",
            "Columbia qty",
            "Virginia TOA $M",
            "Virginia source",
            "Virginia qty",
            "Total SCN sub TOA $M",
            "SAM subaward $M (FY20-26 window, authoritative)",
            "USA subaward $M (full history, capped)",
            "SAM % of SCN TOA",
            "Notes",
        ])
        for fy in WINDOW_FYS:
            col_toa, col_src = toa.get((1045, fy), (0, ""))
            vir_toa, vir_src = toa.get((2013, fy), (0, ""))
            col_q = qty.get((1045, fy), 0)
            vir_q = qty.get((2013, fy), 0)
            total = col_toa + vir_toa
            sam_amt = sam_subs.get(fy, 0)
            usa_amt = usa_subs.get(fy, 0)
            pct = (100 * sam_amt / total) if total else 0
            notes = []
            if fy == 2025:
                notes.append("subaward $ lag-depressed; expect 2-4x growth as filings catch up")
            if fy == 2026:
                notes.append("FY26 = estimate; subaward $ heavily lag-depressed")
            if fy == 2027:
                notes.append("FY27 = request; no subawards yet")
            w.writerow([
                fy,
                round(col_toa, 1),
                col_src,
                col_q,
                round(vir_toa, 1),
                vir_src,
                vir_q,
                round(total, 1),
                round(sam_amt, 1),
                round(usa_amt, 1),
                f"{pct:.1f}%",
                "; ".join(notes),
            ])
    print(f"Wrote {out_path}")
    # Stdout preview
    print()
    print(f"{'FY':<5}{'Columbia':>12}{'Virginia':>12}{'Total':>12}{'SAM($M)':>10}{'USA($M)':>10}{'% sub':>8}")
    for fy in WINDOW_FYS:
        col_toa, _ = toa.get((1045, fy), (0, ""))
        vir_toa, _ = toa.get((2013, fy), (0, ""))
        total = col_toa + vir_toa
        sam_amt = sam_subs.get(fy, 0)
        usa_amt = usa_subs.get(fy, 0)
        pct = (100 * sam_amt / total) if total else 0
        print(f"{fy:<5}{col_toa:>12,.0f}{vir_toa:>12,.0f}{total:>12,.0f}{sam_amt:>10,.0f}{usa_amt:>10,.0f}{pct:>7.1f}%")


if __name__ == "__main__":
    main()
