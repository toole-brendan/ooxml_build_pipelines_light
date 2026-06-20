#!/usr/bin/env python3
"""
Measure classification coverage of the competable-substrate corpora (Phase B1).

Runs the registry-first + taxonomy-ladder classification over both programs'
full-history subaward corpora and reports how many supplier dollars land in a
named work-type bucket vs `unbucketed`. The unclassified vendor queue it emits
is the work list for the entity-lookup extension (B2) and registry additions (B3):
work it top-down until ~90% of FY22-25 supplier dollars are classified per program.

Outputs (to projects/distributed_shipbuilding/sam/award_classification/corpus/extracted/):
  coverage_by_bucket.csv      program, window, role, bucket, basis, n_records,
                              dollars_$M, share_of_supplier_dollars
  coverage_unclassified_top.csv  per-vendor queue of unbucketed supplier dollars,
                              desc by FY22-25 $, with cumulative share columns

Usage: python3 measure_classification_coverage.py [--programs submarines,ddg]
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import (EXTRACTED, PROGRAMS, UNBUCKETED, in_window, iter_records,
                     load_enrichment, load_registry)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--programs", default="submarines,ddg")
    args = ap.parse_args()
    programs = [p.strip() for p in args.programs.split(",") if p.strip()]

    EXTRACTED.mkdir(parents=True, exist_ok=True)
    registry = load_registry()

    bucket_rows = []
    queue_rows = []

    for program in programs:
        enrichment = load_enrichment(program)
        # (window, role, bucket, basis) -> [n, $M]
        agg = defaultdict(lambda: [0, 0.0])
        # vendor_key -> per-vendor rollup of unbucketed supplier dollars
        vend = {}
        supplier_total = {"fy22_25": 0.0, "all": 0.0}
        grand_total = {"fy22_25": 0.0, "all": 0.0}
        n_records = 0

        for rec in iter_records(program, registry=registry, enrichment=enrichment):
            n_records += 1
            windows = ["all"] + (["fy22_25"] if in_window(rec) else [])
            for w in windows:
                grand_total[w] += rec["dollar_m"]
                key = (w, rec["role"], rec["bucket"] or "-", rec["basis"])
                agg[key][0] += 1
                agg[key][1] += rec["dollar_m"]
                if rec["role"] == "supplier":
                    supplier_total[w] += rec["dollar_m"]

            if rec["role"] == "supplier" and rec["bucket"] == UNBUCKETED:
                v = vend.get(rec["vendor_key"])
                if v is None:
                    v = vend[rec["vendor_key"]] = {
                        "vendor_key_uei": rec["vendor_key"],
                        "entity_uei": rec["entity_uei"],
                        "parent_uei": rec["parent_uei"],
                        "vendor_name": rec["parent_name"] or rec["vendor"],
                        "dollars_fy22_25_$M": 0.0, "dollars_all_$M": 0.0,
                        "n_awards": 0, "naics4": rec["naics4"],
                        "current_basis": rec["basis"],
                    }
                v["n_awards"] += 1
                v["dollars_all_$M"] += rec["dollar_m"]
                if in_window(rec):
                    v["dollars_fy22_25_$M"] += rec["dollar_m"]
                if not v["naics4"] and rec["naics4"]:
                    v["naics4"] = rec["naics4"]

        for (w, role, bucket, basis), (n, dollars) in sorted(
                agg.items(), key=lambda kv: (kv[0][0], -kv[1][1])):
            share = dollars / supplier_total[w] if supplier_total[w] else 0.0
            bucket_rows.append({
                "program": program, "window": w, "role": role, "bucket": bucket,
                "basis": basis, "n_records": n, "dollars_$M": round(dollars, 3),
                "share_of_supplier_dollars": round(share, 5) if role == "supplier" else "",
            })

        unb = {w: sum(d for (ww, role, b, _), (_n, d) in agg.items()
                      if ww == w and role == "supplier" and b == UNBUCKETED)
               for w in ("fy22_25", "all")}
        print(f"[{program}] records={n_records:,}  "
              f"FY22-25: total=${grand_total['fy22_25']:,.0f}M  "
              f"supplier=${supplier_total['fy22_25']:,.0f}M  "
              f"unbucketed=${unb['fy22_25']:,.0f}M "
              f"({unb['fy22_25'] / supplier_total['fy22_25']:.1%} of supplier $)"
              if supplier_total['fy22_25'] else f"[{program}] no FY22-25 supplier dollars")

        cum = 0.0
        for v in sorted(vend.values(), key=lambda x: -x["dollars_fy22_25_$M"]):
            cum += v["dollars_fy22_25_$M"]
            queue_rows.append({
                "program": program, **{k: (round(x, 3) if isinstance(x, float) else x)
                                       for k, x in v.items()},
                "cum_unbucketed_fy22_25_$M": round(cum, 3),
                "cum_share_of_supplier_fy22_25":
                    round(cum / supplier_total["fy22_25"], 5)
                    if supplier_total["fy22_25"] else "",
            })

    with (EXTRACTED / "coverage_by_bucket.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(bucket_rows[0].keys()))
        w.writeheader()
        w.writerows(bucket_rows)
    with (EXTRACTED / "coverage_unclassified_top.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(queue_rows[0].keys()))
        w.writeheader()
        w.writerows(queue_rows)
    print(f"\nWrote {EXTRACTED / 'coverage_by_bucket.csv'} ({len(bucket_rows)} rows)")
    print(f"Wrote {EXTRACTED / 'coverage_unclassified_top.csv'} ({len(queue_rows)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
