#!/usr/bin/env python3
"""
Cost-funnel reconciliation for the DDG-51 (Arleigh Burke) program.

Destroyer analogue of submarine_outsourced_work/scripts/build_cost_funnel.py.
Builds a per-FY funnel that ties the SCN P-5c cost categories (LI 2122) to the
yard-side FFATA-visible subaward floor, split by the two prime yards (BIW + Ingalls).

  TOTAL SHIP ESTIMATE (P-5c)
    - Plan Costs                  engineering / lead-yard (BIW Design Agent)
    - Electronics  ┐ GFE (Navy buys, ships to yard): Aegis/SPY-6/SEWIP/CEC ...
    - Ordnance     ┘            Mk41 VLS / Mk45 gun / CIWS
    - HM&E                        hull/mech/elec (CFE; LM2500 propulsion sits here)
    - Other Cost / Change Orders
    = BASIC CONSTRUCTION          the prime base (BIW or Ingalls)
        - yard self-performed
        - OUTSOURCED within BC    sized via supplier-content band (see below)
            - FFATA-visible        first-tier subawards (SAM FSRS) -- the FLOOR

IMPORTANT CAVEATS (see METHODOLOGY.md sec 4):
  * MULTI-VINTAGE. Input scn_li_cost_categories.csv is now reconciled across the
    FY22..FY27 SCN books (extract_scn_destroyer_lines.py), per (FY, category) to the
    most-recent settled vintage -- matching the submarine pipeline. This closes the
    pre-FY2024 HM&E gap: FY2022 (164.030, PB2023) and FY2023 (295.732, PB2025) HM&E
    are now itemized, so FY2022-2027 categories sum to Total Ship Estimate and the
    "other non-BC" residual reconciles to ~0.
  * NO separate Propulsion line for DDG in the P-5c (unlike submarines); LM2500 GFE
    is folded into HM&E, not broken out. GFE here = Electronics + Ordnance only --
    a LOWER BOUND on GFE. (HM&E sits in the "other non-BC" bucket, not GFE.)
  * FY2026 base procurement reads anomalously low (~$306M) -- it is largely
    advance-procurement-funded in prior years; treat FY2026 base as incomplete.

  * The BC-outsourced band (35/42/50%) is the yard supplier-content share from
    extracted/outsourcing_assumptions.md (Method B labor decomposition), NOT a
    primary-source make/buy ratio. Reported as a band, never a point.

Inputs:
  extracted/scn_li_cost_categories.csv   (P-5c cost categories, multi-vintage reconciled)
  extracted/nc_annual_by_piid.csv        (subaward $ per PIID per FY)
  extracted/nc_scope_summary.json        (in-scope PIID -> label, for yard mapping)

Outputs:
  extracted/cost_funnel_per_class.csv    (long form: one row per metric per FY)
  extracted/cost_funnel_summary.csv      (wide deck-ready: one row per FY)
"""
import csv
import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
# .../projects/distributed_shipbuilding/tam/ddg_research/research/scripts -> .../ooxml_build_pipelines_light
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", "..", ".."))
EXTRACTED = os.path.join(_REPO, "projects", "distributed_shipbuilding", "tam", "ddg_research", "extracted")

# Supplier-content band applied to Basic Construction (from outsourcing_assumptions.md)
BAND_LOW, BAND_MID, BAND_HIGH = 0.35, 0.42, 0.50

# Canonical P-5c category labels (source uses a couple of variants we normalize)
CAT_TOTAL = "Total Ship Estimate"
CAT_PLANS = "Plan Costs"
CAT_BC = "Basic Construction/Conversion"
CAT_CO = "Change Orders"
CAT_ELEC = "Electronics"
CAT_ORD = "Ordnance"
CAT_HME = "Hull, Mechanical, and Electrical"  # match by prefix (source appends "(HM&E)")
CAT_OTHER = "Other Cost"


def parse_value(v):
    """'$1,234.5' / '1,253.175' / '-' / '' -> float or None. Parens => negative."""
    if v is None:
        return None
    s = str(v).strip()
    if not s or s in ("-", "--"):
        return None
    s = s.replace(",", "").replace("$", "").strip()
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def norm_cat(raw):
    """Normalize a source cost-category label to a canonical key."""
    r = raw.strip()
    if r.startswith("Hull, Mechanical"):
        return CAT_HME
    return r


def load_cost_categories():
    """Parse scn_li_cost_categories.csv into {fy:int -> {canonical_cat -> $M}}.

    Quirk handling: most rows carry one value per FY. The 'Plan Costs' row carries
    interleaved (quantity, cost) pairs (2*N values for N FYs); we take the cost
    (odd indices). '-' is a real value slot (=> None), not a trailing empty.
    """
    per_fy = {}
    path = os.path.join(EXTRACTED, "scn_li_cost_categories.csv")
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        # v0..v15 live after the first 4 columns (LI, P-1 Line, Cost Category, FY Headers)
        for row in r:
            if len(row) < 5:
                continue
            cat = norm_cat(row[2])
            fys = [int(x) for x in row[3].split("|") if x.strip().isdigit()]
            n = len(fys)
            if n == 0:
                continue
            cells = row[4:]
            # Trim trailing truly-empty cells but keep interior '-' slots.
            last = -1
            for i, c in enumerate(cells):
                if str(c).strip() != "":
                    last = i
            vals = cells[: last + 1]
            if len(vals) == 2 * n:          # (qty, cost) pairs -> take costs
                costs = vals[1::2]
            elif len(vals) == n:            # one value per FY
                costs = vals
            else:
                # Best effort: if more values than FYs, assume trailing extras; clip.
                print(f"  WARN: '{cat}' has {len(vals)} vals for {n} FYs; clipping")
                costs = vals[:n]
            for fy, c in zip(fys, costs):
                per_fy.setdefault(fy, {})[cat] = parse_value(c)
    return per_fy


def load_yard_ffata():
    """Return ({fy -> {'biw':$M,'ingalls':$M}}, biw_piids, ingalls_piids).

    Yard construction PIIDs = in-scope PIIDs whose label is prefixed 'GD-BIW:' or
    'HII-Ingalls:', EXCLUDING DDG-1000/Zumwalt PIIDs (out of class per scope rules).
    GFE primes (LM/RTX/BAE/GE/NG/DRS) are intentionally NOT yard subawards.
    """
    scope = json.load(open(os.path.join(EXTRACTED, "nc_scope_summary.json")))
    piid_meta = scope["in_scope_piids"]
    ddg1000_kw = ("DDG 1000", "DDG 1002", "DDG1000", "BYMP")

    biw, ingalls = set(), set()
    for piid, meta in piid_meta.items():
        if not isinstance(meta, dict):
            continue
        group = meta.get("group", "")
        label = (meta.get("label", "") or "").upper()
        cls = meta.get("class", "")
        if cls == "DDG-1000" or any(k in label for k in ddg1000_kw):
            continue  # Zumwalt out of class
        if group == "GD-BIW":
            biw.add(piid)
        elif group == "HII-Ingalls":
            ingalls.add(piid)

    per_fy = {}
    path = os.path.join(EXTRACTED, "nc_annual_by_piid.csv")
    with open(path) as f:
        rr = csv.DictReader(f)
        for row in rr:
            try:
                fy = int(row["FY"])
            except (ValueError, KeyError):
                continue
            b = sum(parse_value(row.get(f"{p}_$M")) or 0.0 for p in biw)
            i = sum(parse_value(row.get(f"{p}_$M")) or 0.0 for p in ingalls)
            per_fy[fy] = {"biw": b, "ingalls": i}
    return per_fy, sorted(biw), sorted(ingalls)


def main():
    print("Loading SCN cost categories (multi-vintage reconciled)...")
    cats = load_cost_categories()
    print(f"  {len(cats)} FYs: {sorted(cats)}")

    print("Loading yard FFATA-visible subawards...")
    ffata, biw_piids, ingalls_piids = load_yard_ffata()
    print(f"  BIW yard PIIDs: {len(biw_piids)} | Ingalls yard PIIDs: {len(ingalls_piids)}")

    fys = sorted(cats)

    # --- long form ---
    long_path = os.path.join(EXTRACTED, "cost_funnel_per_class.csv")
    with open(long_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "Class", "FY", "Source", "Metric", "Value $M", "Note"])
        for fy in fys:
            c = cats[fy]
            for cat in (CAT_TOTAL, CAT_PLANS, CAT_BC, CAT_CO, CAT_ELEC,
                        CAT_ORD, CAT_HME, CAT_OTHER):
                if c.get(cat) is not None:
                    w.writerow(["2122", "DDG-51", fy, "P-5c", cat, f"{c[cat]:.3f}", ""])
            fe = ffata.get(fy, {})
            if fe:
                w.writerow(["2122", "DDG-51", fy, "FFATA", "Yard subawards BIW",
                            f"{fe['biw']:.3f}", "SAM FSRS"])
                w.writerow(["2122", "DDG-51", fy, "FFATA", "Yard subawards Ingalls",
                            f"{fe['ingalls']:.3f}", "SAM FSRS"])
    print(f"Wrote {long_path}")

    # --- wide deck-ready ---
    wide_path = os.path.join(EXTRACTED, "cost_funnel_summary.csv")
    with open(wide_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "LI", "Class", "FY",
            "total_ship_estimate_$M", "plan_costs_$M", "basic_construction_$M",
            "change_orders_$M", "electronics_$M", "ordnance_$M", "hme_$M", "other_cost_$M",
            "gfe_elec_ord_$M",            # Electronics + Ordnance (GFE lower bound)
            "gfe_pct_of_total",
            "bc_pct_of_total",
            "bc_outsourced_low_$M", "bc_outsourced_mid_$M", "bc_outsourced_high_$M",
            "ffata_visible_biw_$M", "ffata_visible_ingalls_$M", "ffata_visible_yards_$M",
            "ffata_pct_of_bc_outsourced_mid",
            "data_flag",
        ])
        for fy in fys:
            c = cats[fy]
            tot = c.get(CAT_TOTAL)
            pl = c.get(CAT_PLANS)
            bc = c.get(CAT_BC)
            co = c.get(CAT_CO)
            el = c.get(CAT_ELEC)
            ordn = c.get(CAT_ORD)
            hme = c.get(CAT_HME)
            ot = c.get(CAT_OTHER)

            gfe = (el or 0) + (ordn or 0) if (el is not None or ordn is not None) else None
            gfe_pct = (gfe / tot) if (gfe is not None and tot) else None
            bc_pct = (bc / tot) if (bc is not None and tot) else None
            bc_lo = bc * BAND_LOW if bc is not None else None
            bc_mid = bc * BAND_MID if bc is not None else None
            bc_hi = bc * BAND_HIGH if bc is not None else None

            fe = ffata.get(fy, {})
            f_biw = fe.get("biw")
            f_ing = fe.get("ingalls")
            f_yards = (f_biw or 0) + (f_ing or 0) if fe else None
            ffata_pct = (f_yards / bc_mid) if (f_yards is not None and bc_mid) else None

            flags = []
            if hme is None and fy <= 2023:
                flags.append("HM&E missing (pre-FY24 extraction gap)")
            if tot is not None and tot < 1000:
                flags.append("base proc anomalously low (AP-funded?)")

            def fmt(v, p=3):
                return f"{v:.{p}f}" if v is not None else ""

            w.writerow([
                "2122", "DDG-51", fy,
                fmt(tot), fmt(pl), fmt(bc), fmt(co), fmt(el), fmt(ordn), fmt(hme), fmt(ot),
                fmt(gfe),
                f"{gfe_pct:.4f}" if gfe_pct is not None else "",
                f"{bc_pct:.4f}" if bc_pct is not None else "",
                fmt(bc_lo), fmt(bc_mid), fmt(bc_hi),
                fmt(f_biw), fmt(f_ing), fmt(f_yards),
                f"{ffata_pct:.4f}" if ffata_pct is not None else "",
                "; ".join(flags),
            ])
    print(f"Wrote {wide_path}")


if __name__ == "__main__":
    main()
