#!/usr/bin/env python3
"""
Join FFATA-visible subaward dollars (from nc_annual_by_piid.csv) into the
cost_funnel_summary.csv per (class, FY).

Uses nc_scope_summary.json's PIID -> class mapping to aggregate the subaward
data per class per FY.

Adds columns to the funnel:
  ffata_visible_subs_$M               — sum of visible non-MIB subs for this
                                        (class, FY)
  ffata_pct_of_basic_construction     — visible / basic_construction_$M
  ffata_pct_of_total_ship_cost        — visible / total_ship_estimate_$M

Also writes a per-class per-FY rollup view that re-states the data in deck
funnel order:
  - Total ship cost (P-5c)
  - GFE breakdown (Propulsion + Electronics + Ordnance)
  - Prime contract layer (Basic Construction + Change Orders)
  - Within Basic Construction:
      Industry-baseline estimated outsourcing (placeholder for Phase 3 inputs)
      FFATA-visible first-tier subawards (this is the named-vendor pie)
      Gap (purchased material + lower-tier + non-compliance + HII teaming)
"""
import csv
import json
import os
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
# .../projects/distributed_shipbuilding/submarines/research/scripts -> .../ooxml_build_pipelines_light
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", ".."))
EXTRACTED = os.path.join(_REPO, "projects", "distributed_shipbuilding", "submarines", "workbook", "extracted")


def load_scope_summary():
    path = os.path.join(EXTRACTED, "nc_scope_summary.json")
    with open(path) as f:
        return json.load(f)


def load_funnel():
    """Load cost_funnel_summary.csv as list of dicts."""
    path = os.path.join(EXTRACTED, "cost_funnel_summary.csv")
    with open(path) as f:
        r = csv.DictReader(f)
        return list(r)


def load_ffata_by_piid_fy():
    """Read nc_annual_by_piid.csv. The columns are:
       FY, <PIID>_$M (one per PIID), FY_TOTAL_$M, <PIID>_count, FY_TOTAL_count.
       Returns: {(piid, fy_int) -> dollars_$M}."""
    path = os.path.join(EXTRACTED, "nc_annual_by_piid.csv")
    out = defaultdict(float)
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        # PIID columns are like 'N0002417C2100_$M'
        piid_cols = []
        for col_idx, col_name in enumerate(header):
            if col_name.endswith("_$M") and col_name != "FY_TOTAL_$M":
                piid_cols.append((col_idx, col_name.replace("_$M", "")))
        for row in r:
            try:
                fy = int(row[0])
            except (ValueError, IndexError):
                continue
            for col_idx, piid in piid_cols:
                try:
                    val = float(row[col_idx])
                except (ValueError, IndexError):
                    val = 0.0
                if val != 0.0:
                    out[(piid, fy)] = val
    return out


def main():
    scope = load_scope_summary()
    in_scope_piids = scope["in_scope_piids"]  # {piid: {prime, class, label}}

    funnel_rows = load_funnel()
    ffata = load_ffata_by_piid_fy()

    # Aggregate FFATA per (class, fy)
    ffata_by_class_fy = defaultdict(float)
    for (piid, fy), val in ffata.items():
        if piid not in in_scope_piids:
            continue
        cls = in_scope_piids[piid]["class"]
        ffata_by_class_fy[(cls, fy)] += val

    # Build joined output
    out_rows = []
    for row in funnel_rows:
        cls = row["Class"]
        fy = int(row["FY"])
        ffata_m = ffata_by_class_fy.get((cls, fy), 0.0)

        # Parse numeric values
        def f(col):
            v = row.get(col, "").strip()
            return float(v) if v else None

        bc = f("basic_construction_$M")
        total = f("total_ship_estimate_$M")

        ffata_pct_bc = (ffata_m / bc) if (bc and bc > 0) else None
        ffata_pct_total = (ffata_m / total) if (total and total > 0) else None

        row_out = dict(row)
        row_out["ffata_visible_subs_$M"] = f"{ffata_m:.3f}"
        row_out["ffata_pct_of_basic_construction"] = (
            f"{ffata_pct_bc:.4f}" if ffata_pct_bc is not None else ""
        )
        row_out["ffata_pct_of_total_ship_cost"] = (
            f"{ffata_pct_total:.4f}" if ffata_pct_total is not None else ""
        )
        out_rows.append(row_out)

    # Write augmented funnel CSV
    out_path = os.path.join(EXTRACTED, "cost_funnel_with_subawards.csv")
    if out_rows:
        fieldnames = list(out_rows[0].keys())
        with open(out_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(out_rows)
    print(f"Wrote {out_path}")

    # Also write a deck-narrative rollup that puts the funnel in slide order.
    # The "outsourced inside Basic Construction" is shown as a BAND (50/60/65%)
    # because no primary-source Navy/GAO/CBO statement gives a clean make/buy
    # ratio — the band is industry analyst consensus for complex shipbuilding.
    # See research_primary_sources/SUMMARY.md for sourcing and the 'NOT FOUND'
    # row in extracted/industry_baseline_citations.csv.
    narrative_path = os.path.join(EXTRACTED, "cost_funnel_narrative.csv")
    with open(narrative_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "Class", "FY", "Procurement Qty",
            "Total Ship Cost $M",
            "Plans $M",
            "GFE Sum $M (Propulsion+Electronics+Ordnance)",
            "Other+Change Orders $M",
            "Basic Construction $M (prime contract base)",
            "Basic Construction % of Total",
            # Outsourced inside Basic Construction — banded estimate
            "Industry Low Estimate (50% of BC) $M",
            "Industry Mid Estimate (60% of BC) $M",
            "Industry High Estimate (65% of BC) $M",
            # FFATA-visible
            "FFATA-Visible First-Tier Subawards $M",
            "FFATA-Visible % of BC",
            # Implied unseen layer at mid case
            "Unseen Layer at Mid (60% - FFATA) $M",
            # Sourcing notes
            "Sourcing Notes",
        ])

        sourcing_note = (
            "Total Ship Cost / GFE / Basic Construction: SCN budget books P-5c "
            "(primary, see scn_p5c_per_fy_reconciled.csv). FFATA-Visible: "
            "SAM.gov subaward filings (primary, see nc_annual_by_piid.csv). "
            "Industry low/mid/high (50/60/65% of BC): analyst consensus for "
            "complex shipbuilding purchased+subbed content. NOT primary-sourced "
            "for submarines specifically — no GAO/CRS/CBO report we reviewed "
            "states a make/buy ratio. Supporting evidence: 70% sole-source "
            "suppliers (CRS-RL32418/R41129); 70% smaller supplier base than "
            "historical (GAO-21-257); $10B+ DOD submarine industrial base "
            "investment (GAO-26-109068)."
        )

        for row in out_rows:
            cls = row["Class"]
            fy = row["FY"]

            def f(col):
                v = row.get(col, "").strip()
                return float(v) if v else None

            qty = f("procurement_qty")
            total = f("total_ship_estimate_$M")
            plans = f("plan_costs_$M") or 0.0
            gfe = f("gfe_sum_$M") or 0.0
            other = (f("other_cost_$M") or 0.0) + (f("change_orders_$M") or 0.0)
            bc = f("basic_construction_$M")
            ffata = f("ffata_visible_subs_$M") or 0.0

            bc_pct = (bc / total) if (bc and total) else None
            low_est = (0.50 * bc) if bc else None
            mid_est = (0.60 * bc) if bc else None
            high_est = (0.65 * bc) if bc else None
            ffata_pct_bc = (ffata / bc) if bc else None
            unseen_at_mid = (mid_est - ffata) if mid_est is not None else None

            def fmt(v, prec=3):
                return f"{v:.{prec}f}" if v is not None else ""

            w.writerow([
                cls, fy,
                fmt(qty, 0) if qty is not None else "",
                fmt(total),
                fmt(plans),
                fmt(gfe),
                fmt(other),
                fmt(bc),
                f"{bc_pct:.4f}" if bc_pct is not None else "",
                fmt(low_est),
                fmt(mid_est),
                fmt(high_est),
                fmt(ffata),
                f"{ffata_pct_bc:.4f}" if ffata_pct_bc is not None else "",
                fmt(unseen_at_mid),
                sourcing_note,
            ])
    print(f"Wrote {narrative_path}")


if __name__ == "__main__":
    main()
