#!/usr/bin/env python3
"""
Cost funnel reconciliation for Va + Col submarine programs.

Builds a per-(class, FY) funnel that ties together:
  - P-40 metrics: procurement qty, gross/unit cost, PY/CY AP, net procurement, TOA
  - P-5c cost categories: Basic Construction, Plans, Propulsion, Electronics,
    HM&E, Ordnance, Other, Change Orders, Total Ship Estimate

The funnel reconciles across budget book vintages PB22..PB27 by picking the most
recent book that shows each FY as a settled actual (PB year >= FY+2). Falls back
to the most recent available book if no settled actual exists yet.

Inputs (already extracted):
  extracted/scn_li_per_fy_long.csv     (long-form P-40 across all vintages)
  extracted/scn_p5c_per_fy_reconciled.csv (P-5c reconciled — best per FY)

Outputs:
  extracted/cost_funnel_per_class.csv  (long-form: one row per metric per FY per class)
  extracted/cost_funnel_summary.csv    (wide deck-ready: one row per (class, FY))

Funnel logic (deck-narrative slicing):
  Total Ship Estimate (P-5c)
    ├── Plan Costs        ← engineering / non-recurring
    ├── Propulsion        ← GFE (BPMI nuclear plant)
    ├── Electronics       ← GFE (combat sys / sonar / EW)
    ├── HM&E              ← part GFE, part Basic Construction
    ├── Ordnance          ← GFE (Col only — weapons systems)
    ├── Other Cost        ← misc
    ├── Change Orders     ← contract mods
    └── Basic Construction ← the prime contract base (= GDEB build)

The 'gfe_sum_$M' column groups Propulsion + Electronics + Ordnance (HM&E is mixed,
so reported separately).
"""
import csv
import os
import re
from collections import defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
# .../projects/distributed_shipbuilding/submarines/research/scripts -> .../ooxml_build_pipelines_light
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "..", ".."))
EXTRACTED = os.path.join(_REPO, "projects", "distributed_shipbuilding", "tam", "submarines", "extracted")

# P-40 rows we extract for the funnel
FUNNEL_P40_ROWS = [
    "Procurement Quantity (Units in Each)",
    "Gross/Weapon System Cost ($ in Millions)",
    "Gross/Weapon System Unit Cost ($ in Millions)",
    "Less PY Advance Procurement ($ in Millions)",
    "Plus CY Advance Procurement ($ in Millions)",
    "Net Procurement (P-1) ($ in Millions)",
    "Total Obligation Authority ($ in Millions)",
]

# P-5c cost category labels
P5C_CATEGORIES = [
    "Basic Construction/Conversion",
    "Plan Costs",
    "Propulsion Equipment",
    "Electronics",
    "Hull, Mechanical, and Electrical",
    "Ordnance",
    "Other Cost",
    "Change Orders",
    "Technology Insertion",
    "Total Ship Estimate",
]

LI_TO_CLASS = {
    "1045": "Columbia",
    "2013": "Virginia",
}

TARGET_LIS = ["1045", "2013"]
TARGET_FYS = list(range(2020, 2028))


def parse_value(v):
    """Parse string like '$1,234.5' or '1,253.175' or '-' into float, or None."""
    if v is None:
        return None
    s = str(v).strip()
    if not s or s in ("-", "--"):
        return None
    s = s.replace(",", "").replace("$", "").strip()
    # Parens => negative
    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]
    try:
        return float(s)
    except ValueError:
        return None


def load_p40_data():
    """Read scn_li_per_fy_long.csv.
    Returns: dict keyed by (li, p1_section, row_label, fy_int) -> {pb_year: value}.
    Only keeps FUNNEL_P40_ROWS and 'base' p1_section."""
    idx = defaultdict(dict)
    with open(os.path.join(EXTRACTED, "scn_li_per_fy_long.csv")) as f:
        r = csv.DictReader(f)
        for row in r:
            if row["row_label"] not in FUNNEL_P40_ROWS:
                continue
            if row["p1_section"] != "base":
                continue
            if row["li"] not in TARGET_LIS:
                continue
            # Accept 'FY YYYY' (plain outyear) or 'FY YYYY Total' (request year sum).
            m = re.match(r"^FY (\d{4})(?: Total)?$", row["fy_label"])
            if not m:
                continue
            fy_int = int(m.group(1))
            val = parse_value(row["value"])
            if val is None:
                continue
            key = (row["li"], row["p1_section"], row["row_label"], fy_int)
            pb = int(row["pb_year"])
            # Prefer 'Total' over plain — but for same (book, fy) they're equivalent.
            # If both, last-written wins, which is fine.
            idx[key][pb] = val
    return idx


def reconcile_best_vintage(vintage_vals, fy):
    """Pick most recent PB year that shows FY as settled actual (PB >= FY+2).
    Fall back to most recent vintage available."""
    if not vintage_vals:
        return None, None
    settled = {pb: v for pb, v in vintage_vals.items() if pb >= fy + 2}
    if settled:
        best_pb = max(settled.keys())
    else:
        best_pb = max(vintage_vals.keys())
    return vintage_vals[best_pb], best_pb


def load_p5c_data():
    """Read scn_p5c_per_fy_reconciled.csv. Returns (li, fy_int, category) -> value."""
    out = {}
    with open(os.path.join(EXTRACTED, "scn_p5c_per_fy_reconciled.csv")) as f:
        r = csv.DictReader(f)
        for row in r:
            li = row["LI"]
            try:
                fy = int(row["FY"])
            except (ValueError, KeyError):
                continue
            cat = row["Cost Category"]
            val = parse_value(row["Best Value $M"])
            if val is not None:
                out[(li, fy, cat)] = val
    return out


def main():
    print("Loading P-40 data...")
    p40 = load_p40_data()
    print(f"  {len(p40)} (li, sec, label, fy) keys with vintage data")

    print("Loading P-5c data...")
    p5c = load_p5c_data()
    print(f"  {len(p5c)} (li, fy, category) keys")

    # Reconcile P-40 per (li, fy, metric)
    p40_reconciled = {}
    for (li, sec, label, fy), vintage_vals in p40.items():
        if li not in TARGET_LIS or fy not in TARGET_FYS:
            continue
        best_val, best_pb = reconcile_best_vintage(vintage_vals, fy)
        p40_reconciled[(li, fy, label)] = (best_val, best_pb)

    # Write long-form
    long_path = os.path.join(EXTRACTED, "cost_funnel_per_class.csv")
    with open(long_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["LI", "Class", "FY", "Metric Source", "Metric", "Value $M", "Source PB"])
        for li in TARGET_LIS:
            cls = LI_TO_CLASS[li]
            for fy in TARGET_FYS:
                for metric in FUNNEL_P40_ROWS:
                    if (li, fy, metric) in p40_reconciled:
                        val, src = p40_reconciled[(li, fy, metric)]
                        w.writerow([li, cls, fy, "P-40", metric,
                                    f"{val:.3f}", f"PB{src}"])
                for cat in P5C_CATEGORIES:
                    if (li, fy, cat) in p5c:
                        w.writerow([li, cls, fy, "P-5c", cat,
                                    f"{p5c[(li, fy, cat)]:.3f}", ""])
    print(f"Wrote {long_path}")

    # Wide deck-ready summary CSV
    wide_path = os.path.join(EXTRACTED, "cost_funnel_summary.csv")
    with open(wide_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "LI", "Class", "FY",
            "procurement_qty",
            "gross_cost_$M",
            "gross_unit_cost_$M",
            "less_py_ap_$M",
            "plus_cy_ap_$M",
            "net_proc_$M",
            "toa_$M",
            "basic_construction_$M",
            "plan_costs_$M",
            "propulsion_$M",
            "electronics_$M",
            "hme_$M",
            "ordnance_$M",
            "other_cost_$M",
            "change_orders_$M",
            "technology_insertion_$M",
            "total_ship_estimate_$M",
            # Derived:
            "gfe_sum_$M",            # Propulsion + Electronics + Ordnance
            "prime_contract_sum_$M", # Basic Construction + Change Orders
            "basic_construction_pct_of_total", # BC / Total Ship Est
            "gfe_pct_of_total",      # (Propulsion+Electronics+Ordnance) / Total
        ])
        for li in TARGET_LIS:
            cls = LI_TO_CLASS[li]
            for fy in TARGET_FYS:
                def g_p40(metric):
                    rec = p40_reconciled.get((li, fy, metric))
                    return rec[0] if rec else None

                def g_p5c(cat):
                    return p5c.get((li, fy, cat))

                qty = g_p40("Procurement Quantity (Units in Each)")
                gross = g_p40("Gross/Weapon System Cost ($ in Millions)")
                unit = g_p40("Gross/Weapon System Unit Cost ($ in Millions)")
                py_ap = g_p40("Less PY Advance Procurement ($ in Millions)")
                cy_ap = g_p40("Plus CY Advance Procurement ($ in Millions)")
                net_proc = g_p40("Net Procurement (P-1) ($ in Millions)")
                toa = g_p40("Total Obligation Authority ($ in Millions)")

                bc = g_p5c("Basic Construction/Conversion")
                pl = g_p5c("Plan Costs")
                pr = g_p5c("Propulsion Equipment")
                el = g_p5c("Electronics")
                hme = g_p5c("Hull, Mechanical, and Electrical")
                ord_ = g_p5c("Ordnance")
                ot = g_p5c("Other Cost")
                co = g_p5c("Change Orders")
                ti = g_p5c("Technology Insertion")
                tot = g_p5c("Total Ship Estimate")

                gfe_parts = [x for x in (pr, el, ord_) if x is not None]
                gfe_sum = sum(gfe_parts) if gfe_parts else None
                prime_parts = [x for x in (bc, co) if x is not None]
                prime_sum = sum(prime_parts) if prime_parts else None

                bc_pct = (bc / tot) if (bc is not None and tot) else None
                gfe_pct = (gfe_sum / tot) if (gfe_sum is not None and tot) else None

                # Only emit rows that have meaningful data
                if any(x is not None for x in (qty, gross, bc, toa)):
                    def fmt(v, prec=3):
                        return f"{v:.{prec}f}" if v is not None else ""
                    w.writerow([
                        li, cls, fy,
                        fmt(qty, 0) if qty is not None else "",
                        fmt(gross), fmt(unit), fmt(py_ap), fmt(cy_ap),
                        fmt(net_proc), fmt(toa),
                        fmt(bc), fmt(pl), fmt(pr), fmt(el), fmt(hme),
                        fmt(ord_), fmt(ot), fmt(co), fmt(ti), fmt(tot),
                        fmt(gfe_sum), fmt(prime_sum),
                        f"{bc_pct:.4f}" if bc_pct is not None else "",
                        f"{gfe_pct:.4f}" if gfe_pct is not None else "",
                    ])
    print(f"Wrote {wide_path}")


if __name__ == "__main__":
    main()
