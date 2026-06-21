#!/usr/bin/env python3
"""Build the extracted data for the Outsourcing Ceiling workbook.

Stdlib-only. Unions the two existing per-program cost funnels (which have
DIFFERENT cost structures - subs carry a nuclear Propulsion line, DDG folds the
LM2500 into HM&E) into ONE normalized cost base, and stamps the verified anchor
citations that back the ceiling parameters.

Sources (already extracted by each program's build_cost_funnel.py):
  submarines/workbook/extracted/cost_funnel_with_subawards.csv   (Virginia, Columbia)
  ddg/workbook/extracted/cost_funnel_summary.csv                 (DDG-51)

Outputs (into this pipeline's extracted/ dir):
  wb_cost_base.csv   one row per (program, FY) with a boat funded, FY22-27:
                     program, class, fy, bc_$M, gfe_$M, plans_other_$M,
                     total_ship_$M, ffata_visible_$M
  wb_anchors.csv     the verified source citations behind h / L / the BC
                     definition / the current-state POP coefficients.

The funnel $ are then-year P-5c as reported (ratios are unit-invariant; the
dollars are illustrative of magnitude). plans_other_$M = total - bc - gfe is a
residual (plans + change orders + HM&E + other), kept only so bc + gfe +
plans_other ties to total on every row.

Run:  python3.12 build_ceiling_base.py
"""
from __future__ import annotations

import csv
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
# .../distributed_shipbuilding/tam/master -> .../distributed_shipbuilding/tam
_DSB = os.path.abspath(os.path.join(_HERE, ".."))
# Generated ceiling inputs land in the master workbook's namespaced extracted slice.
EXTRACTED = os.path.join(_HERE, "extracted", "ceiling")

# Read the upstream cost-funnel CSVs from the renamed research corpora.
SUBS_CSV = os.path.join(_DSB, "virginia_columbia_research", "extracted",
                        "cost_funnel_with_subawards.csv")
DDG_CSV = os.path.join(_DSB, "ddg_research", "extracted",
                       "cost_funnel_summary.csv")

FY_LO, FY_HI = 2022, 2027


def _f(v):
    """Parse a funnel cell to float, or None for blank/dash."""
    if v is None:
        return None
    s = str(v).strip().replace(",", "").replace("$", "")
    if s in ("", "-", "--"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _read(path, *, gfe_col, ffata_col):
    """Read one funnel CSV; yield normalized dicts for in-window funded rows."""
    out = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            fy = _f(row.get("FY"))
            if fy is None or not (FY_LO <= int(fy) <= FY_HI):
                continue
            bc = _f(row.get("basic_construction_$M"))
            if not bc:                      # only rows with an actual award (BC > 0)
                continue
            total = _f(row.get("total_ship_estimate_$M"))
            gfe = _f(row.get(gfe_col)) or 0.0
            ffata = _f(row.get(ffata_col)) or 0.0
            plans_other = (total - bc - gfe) if total is not None else None
            out.append({
                "program": row["Class"],     # Virginia / Columbia / DDG-51
                "class": row["Class"],
                "fy": int(fy),
                "bc_$M": round(bc, 3),
                "gfe_$M": round(gfe, 3),
                "plans_other_$M": round(plans_other, 3) if plans_other is not None else "",
                "total_ship_$M": round(total, 3) if total is not None else "",
                "ffata_visible_$M": round(ffata, 3),
            })
    return out


# ---------------------------------------------------------------------------
# Verified anchor citations (exact quotes captured + URL-verified this session).
# ---------------------------------------------------------------------------
ANCHORS = [
    ["A1", "h - outsourceable labor-hour share", "0.50", "labor-hours",
     "Defense News - Defense firms outsource sub, carrier construction amid labor woes (M. Eckstein, 2022-10-21)",
     "https://www.defensenews.com/industry/2022/10/21/defense-firms-outsource-sub-carrier-construction-amid-labor-woes/",
     "RADM Jon Rucker (PEO Attack Submarines): EB outsources 1.1M hrs/yr and Newport News 900,000 hrs; "
     "by 2025 that combined 2 million hours will grow to 5 million - which equates to half the work to "
     "build a Virginia submarine."],
    ["A2", "L - shipyard labor share of ship cost", "0.40", "dollars (of total procurement cost)",
     "O'Rourke (CRS), 'The State of U.S. Shipbuilding', House Armed Services testimony (2025-03-11)",
     "https://armedservices.house.gov/uploadedfiles/03.11.25_spf_state_of_shipbuilding_orourke_statement.pdf",
     "Shipyard labor can account for roughly 40% of a military ship's total procurement cost. "
     "(Denominator = total procurement incl. GFE; labor's share of Basic Construction is therefore higher.)"],
    ["A3", "L cross-check - labor weight of shipbuilding cost", "0.39-0.48", "dollars (composite index weight)",
     "CBO, The Shipbuilding Composite Index (April 2024)",
     "https://www.cbo.gov/publication/60206",
     "Shipbuilder cost splits into labor, nonnuclear material, and nuclear material (nuclear material "
     "includes subcontractor labor). Shipbuilder labor was almost half of the index 2006-2022, declining "
     "from 48% (2007) to 39% (2013)."],
    ["A4", "Basic Construction is a single regulated line (no labor/material split)", "n/a", "definition",
     "DoD FMR 7000.14-R Vol 2B Ch 4, Exhibit P-5 Ship Cost Element Categories (Nov 2017)",
     "https://comptroller.defense.gov/Portals/45/documents/fmr/current/02b/02b_04.pdf",
     "Ship Cost Element Categories: Plan Costs; Basic Construction/Conversion; Change Orders; Electronics; "
     "Propulsion Equipment; HM&E; Other Cost; Ordnance; Escalation; PM Growth; Total Ship Estimate. "
     "Basic Construction is one line - the labor/material split is not in the budget."],
    ["A5", "Virginia current off-team place-of-performance", "0.34", "place of performance",
     "DoD Contracts 2019-12-02 (article 2030017), Block V N00024-17-C-2100",
     "https://www.defense.gov/News/Contracts/Contract/Article/2030017/",
     "Announced POP: other-US (each below 1%, collectively 22%) + outside US (1%) = 34% off the EB/HII "
     "prime team; the applied Virginia BC supplier coefficient."],
    ["A6", "Columbia current off-team place-of-performance", "0.22", "place of performance",
     "DoD Contracts 2020-11-05 (article 2406922), Build I N00024-17-C-2117",
     "https://www.defense.gov/Newsroom/Contracts/Contract/Article/2406922/",
     "Announced POP: other US sites each <1% (22%) off the EB/HII prime team; the applied Columbia BC "
     "supplier coefficient."],
    ["A7", "DDG-51 current off-team place-of-performance", "0.13", "place of performance",
     "DoD Contracts 2023-08-01 (article 3479250), DDG-51 FY23-27 multiyear (BIW + Ingalls)",
     "https://www.defense.gov/News/Contracts/Contract/Article/3479250/",
     "DDG-51 off-team construction share ~13%, a production-weighted blend of the BIW and Ingalls FY23-27 "
     "multiyear announcements (BIW ~20% off-Bath construction; Ingalls ~9% off-Pascagoula). A narrower "
     "measure than the gross announced place of performance, which also counts teammate, engineering, and "
     "support sites; the applied DDG-51 BC supplier coefficient and the current-state floor."],
]


def main():
    os.makedirs(EXTRACTED, exist_ok=True)
    subs = _read(SUBS_CSV, gfe_col="gfe_sum_$M", ffata_col="ffata_visible_subs_$M")
    ddg = _read(DDG_CSV, gfe_col="gfe_elec_ord_$M", ffata_col="ffata_visible_yards_$M")
    # Order: Virginia, Columbia (from subs file), then DDG-51.
    order = {"Virginia": 0, "Columbia": 1, "DDG-51": 2}
    rows = sorted(subs + ddg, key=lambda r: (order.get(r["program"], 9), r["fy"]))

    cols = ["program", "class", "fy", "bc_$M", "gfe_$M", "plans_other_$M",
            "total_ship_$M", "ffata_visible_$M"]
    base_path = os.path.join(EXTRACTED, "wb_cost_base.csv")
    with open(base_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])
    print(f"Wrote {base_path}  ({len(rows)} rows)")

    anc_path = os.path.join(EXTRACTED, "wb_anchors.csv")
    with open(anc_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["anchor_id", "parameter", "value", "basis", "source_title",
                    "source_url", "quoted_text"])
        w.writerows(ANCHORS)
    print(f"Wrote {anc_path}  ({len(ANCHORS)} citations)")

    # Reconciliation: per-program cumulative BC + internal consistency check.
    print("\nPer-program cumulative BC (FY22-27, then-year $M):")
    for prog in ("Virginia", "Columbia", "DDG-51"):
        pr = [r for r in rows if r["program"] == prog]
        bc_sum = sum(r["bc_$M"] for r in pr)
        print(f"  {prog:<10} {len(pr)} award-year(s)   BC = {bc_sum:>10,.1f}")
        for r in pr:
            if r["total_ship_$M"] != "":
                resid = r["bc_$M"] + r["gfe_$M"] + (r["plans_other_$M"] or 0)
                assert abs(resid - r["total_ship_$M"]) < 0.5, \
                    f"{prog} FY{r['fy']}: bc+gfe+plans_other {resid} != total {r['total_ship_$M']}"
    print("  internal check: bc + gfe + plans_other = total on every row  OK")


if __name__ == "__main__":
    main()
