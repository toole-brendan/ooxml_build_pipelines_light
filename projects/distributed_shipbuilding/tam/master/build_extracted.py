"""build_extracted.py - reshape raw source exhibits into clean combined-by-type CSVs.

Reads the handful of raw source CSVs under ``source_data/{submarines,ddg}/`` (copied
verbatim from the upstream research corpora) and writes the five clean, COMBINED CSVs
the workbook's data tabs load from ``extracted/``:

    scn_budget.csv          P-5c cost categories, then-year $M, all three programs
    place_of_performance.csv  gated DoD-announcement POP corpus, unified schema
    obbba.csv               OBBBA Sec. 20002 mandatory awards (Va (16), DDG (17))
    fydp_outyears.csv       PB2027 P-40 Resource Summary FY2025-FY2031
    deflators.csv           Green Book Procurement deflator (from workbook_core)

Re-run only if a source exhibit changes. The transforms here mirror the original
per-program data modules exactly, so the rebuilt workbook ties out to master/.
Run:  python3 build_extracted.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
sys.path.insert(0, str(_HERE.parents[4]))   # repo root, for workbook_core

from workbook_core import deflators as _d   # noqa: E402

SRC = _HERE.parent / "source_data"
OUT = _HERE.parent / "extracted"
OUT.mkdir(exist_ok=True)

_FY_BUDGET = [2022, 2023, 2024, 2025, 2026, 2027]


def _read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _num(x):
    """Then-year cell -> trimmed numeric string, or '' for blank/dash."""
    s = (str(x) if x is not None else "").strip().replace(",", "")
    if s in ("", "-"):
        return ""
    try:
        return repr(float(s)) if "." in s or "e" in s.lower() else str(int(s))
    except ValueError:
        return ""


def _write(name: str, header: list[str], rows: list[list]) -> None:
    with (OUT / f"{name}.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {name}.csv  ({len(rows)} rows)")


# ---------------------------------------------------------------------------
# 1. scn_budget.csv  (combined P-5c cost categories, then-year $M)
# ---------------------------------------------------------------------------
_SCN_METRICS = ["total", "plans", "propulsion", "electronics", "hme", "ordnance",
                "other_cost", "technology_insertion", "gfe", "change_orders", "basic"]


def build_scn_budget() -> None:
    rows = []

    # Submarines: cost_funnel_with_subawards.csv, LI 2013 (Virginia) / 1045 (Columbia)
    sub_map = {
        "total": "total_ship_estimate_$M", "plans": "plan_costs_$M",
        "propulsion": "propulsion_$M", "electronics": "electronics_$M",
        "hme": "hme_$M", "ordnance": "ordnance_$M", "other_cost": "other_cost_$M",
        "technology_insertion": "technology_insertion_$M", "gfe": "gfe_sum_$M",
        "change_orders": "change_orders_$M", "basic": "basic_construction_$M",
    }
    sub_prog = {2013: "Virginia", 1045: "Columbia"}
    src = {(int(r["LI"]), int(r["FY"])): r
           for r in _read(SRC / "submarines/cost_funnel_with_subawards.csv")
           if r.get("LI", "").strip().isdigit() and r.get("FY", "").strip().isdigit()}
    for li in (2013, 1045):
        for fy in _FY_BUDGET:
            r = src.get((li, fy), {})
            rows.append([sub_prog[li], li, fy]
                        + [_num(r.get(sub_map[m])) for m in _SCN_METRICS])

    # DDG-51: cost_funnel_summary.csv, LI 2122 (no propulsion / tech-insertion lines)
    ddg_map = {
        "total": "total_ship_estimate_$M", "plans": "plan_costs_$M",
        "propulsion": None, "electronics": "electronics_$M", "hme": "hme_$M",
        "ordnance": "ordnance_$M", "other_cost": "other_cost_$M",
        "technology_insertion": None, "gfe": "gfe_elec_ord_$M",
        "change_orders": "change_orders_$M", "basic": "basic_construction_$M",
    }
    dsrc = {int(r["FY"]): r for r in _read(SRC / "ddg/cost_funnel_summary.csv")
            if r.get("LI", "").strip() == "2122" and r.get("FY", "").strip().isdigit()}
    for fy in _FY_BUDGET:
        r = dsrc.get(fy, {})
        rows.append(["DDG-51", 2122, fy]
                    + [_num(r.get(ddg_map[m])) if ddg_map[m] else "" for m in _SCN_METRICS])

    _write("scn_budget", ["program", "li", "fy"] + _SCN_METRICS, rows)


# ---------------------------------------------------------------------------
# 2. place_of_performance.csv  (gated DoD-announcement POP corpus, unified)
# ---------------------------------------------------------------------------
_GATE_TRUE = {"yes", "y", "true", "1"}
# Unified schema. GFE-excluded rows are dropped (they never enter a coefficient), so
# every row is a gated, confirmed, BC-eligible, class-attributable announcement.
# master: 1 = an announced construction-master row. vintage: 1 = a DDG FY18-22 master
# (feeds the DDG FY2022-vintage coefficient only). source = the DoD-announcement URL/cite.
_POP_HEADER = ["program", "action_date", "piid", "prime", "work_type", "stream",
               "master", "vintage", "dollar_m", "prime_pct", "coprime_pct",
               "other_us_pct", "foreign_pct", "source"]

# Announced construction masters - the authoritative DoD contract-award announcements.
# (program, date, piid, prime, $M, prime%, coprime%, other_us%, foreign%, vintage, source)
_MASTERS = [
    ("Virginia", "2019-12-02", "N00024-17-C-2100", "General Dynamics Electric Boat",
     22209.893, 41, 25, 33, 1, 0,
     "DoD Contracts 2019-12-02 (defense.gov Article 2030017); Block V, 9 boats FY19-23"),
    ("Columbia", "2020-11-05", "N00024-17-C-2117", "General Dynamics Electric Boat",
     9473.511, 53, 25, 22, 0, 0,
     "DoD Contracts 2020-11-05 (defense.gov Article 2406922); Build I, SSBN 826/827"),
    ("DDG-51", "(MYP master)", "N00024-23-C-2305", "Bath Iron Works",
     6400.0, 69, 0, 31, 0, 0,
     "DDG FY23-27 MYP; POP per award bulletin, $ reconstructed from FPDS + trade press"),
    ("DDG-51", "(MYP master)", "N00024-23-C-2307", "Huntington Ingalls Industries",
     8180.0, 0, 77, 23, 0, 0,
     "DDG FY23-27 MYP; POP per award bulletin, $ reconstructed from FPDS + trade press"),
    ("DDG-51", "2018-09-27", "N00024-18-C-2305", "Bath Iron Works",
     3904.736, 61, 0, 39, 0, 1,
     "DoD Contracts 2018-09-27 (defense.gov Article 1647166); FY18-22 MYP"),
    ("DDG-51", "2018-09-27", "N00024-18-C-2307", "Huntington Ingalls Industries",
     5104.669, 0, 91, 9, 0, 1,
     "DoD Contracts 2018-09-27 (defense.gov Article 1647166); FY18-22 MYP"),
]


def _f(x) -> float:
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def _pct(x) -> str:
    return repr(_f(x) / 100.0)


def _master_row(m) -> list:
    prog, date, piid, prime, dol, p, cp, ous, frn, vintage, source = m
    return [prog, date, piid, prime, "construction", "BC", 1, vintage, repr(dol),
            repr(p / 100), repr(cp / 100), repr(ous / 100), repr(frn / 100), source]


def build_place_of_performance() -> None:
    _AP_LLTM_WT = {"lltm_early_mfg", "advance_procurement"}
    # GFE programs (dropped): submarine BPMI nuclear + GFE electronics/components; DDG ddg_gfe_*
    _SUB_GFE = {"sub_gfe_electronics", "sub_gfe_components", "bpmi_nuclear"}
    _SUB_CLASS = {"va": "Virginia", "col": "Columbia"}

    # --- Submarine gated, non-GFE rows (cleanly Virginia / Columbia) ---
    sub = []
    for r in _read(SRC / "submarines/dod_announcement_pop.csv"):
        if (r.get("is_sub_new_construction_tam") or "").strip().lower() not in _GATE_TRUE:
            continue
        if (r.get("program_refined") or "").strip() in _SUB_GFE:
            continue                                   # 2a: drop GFE-excluded rows
        cls = _SUB_CLASS.get((r.get("program_primary") or "").strip())
        if cls is None:
            continue                                   # only class-attributable rows remain
        wt = (r.get("work_type_primary") or "").strip()
        stream = "AP_LLTM" if wt in _AP_LLTM_WT else "BC"
        sub.append({
            "prog": cls, "dollar_m": _f(r.get("amount_usd")) / 1e6,
            "row": [cls, (r.get("action_date") or "").strip(),
                    (r.get("piid") or "").strip() or "-", (r.get("prime") or "").strip() or "-",
                    wt, stream, 0, 0, repr(_f(r.get("amount_usd")) / 1e6),
                    _pct(r.get("pop_eb_site_pct")), _pct(r.get("pop_hii_site_pct")),
                    _pct(r.get("pop_other_us_pct")), _pct(r.get("pop_foreign_pct")),
                    (r.get("source_url") or "").strip()],
        })

    # --- DDG-51 gated, non-GFE rows ---
    ddg = []
    for r in _read(SRC / "ddg/dod_announcement_pop.csv"):
        if (r.get("is_ddg_new_construction_tam") or "").strip().lower() not in _GATE_TRUE:
            continue
        if (r.get("program_refined") or "").strip().startswith("ddg_gfe_"):
            continue                                   # 2a: drop GFE-excluded rows
        ddg.append({
            "dollar_m": _f(r.get("amount_usd")) / 1e6,
            "row": ["DDG-51", (r.get("action_date") or "").strip(),
                    (r.get("piid") or "").strip() or "-", (r.get("prime") or "").strip() or "-",
                    (r.get("work_type_primary") or "").strip(), "BC", 0, 0,
                    repr(_f(r.get("amount_usd")) / 1e6),
                    _pct(r.get("pop_biw_site_pct")), _pct(r.get("pop_ingalls_site_pct")),
                    _pct(r.get("pop_other_us_pct")), _pct(r.get("pop_foreign_pct")),
                    (r.get("source_url") or "").strip()],
        })

    va = sorted([d for d in sub if d["prog"] == "Virginia"], key=lambda d: -d["dollar_m"])
    col = sorted([d for d in sub if d["prog"] == "Columbia"], key=lambda d: -d["dollar_m"])
    ddg.sort(key=lambda d: -d["dollar_m"])

    rows = [_master_row(_MASTERS[0])]                                 # Block V
    rows += [d["row"] for d in va]
    rows.append(_master_row(_MASTERS[1]))                            # Build I
    rows += [d["row"] for d in col]
    rows += [_master_row(_MASTERS[2]), _master_row(_MASTERS[3])]     # DDG current masters
    rows += [d["row"] for d in ddg]
    rows += [_master_row(_MASTERS[4]), _master_row(_MASTERS[5])]     # DDG FY18-22 masters

    _write("place_of_performance", _POP_HEADER, rows)


# ---------------------------------------------------------------------------
# 3. obbba.csv  (OBBBA Sec. 20002 mandatory new-construction awards)
# ---------------------------------------------------------------------------
def build_obbba() -> None:
    rows = [
        ["Virginia", 2013, "20002(16)", 2026, "4600.0",
         "Second FY2026 Virginia-class submarine; full ship procurement (no cost-category breakout)"],
    ]
    ddg = next((r for r in _read(SRC / "ddg/obbba_ddg_mandatory.csv")
                if (r.get("included") or "").strip() == "1"), None)
    if ddg is None:
        raise SystemExit("obbba_ddg_mandatory.csv: no included==1 row found")
    rows.append(["DDG-51", 2122, "20002(17)", 2026, _num(ddg["fy2026_$M"]),
                 "Two DDG-51 (DDG 147/149) under current MYP; covers BC + GFE (no breakout)"])
    _write("obbba", ["program", "li", "section", "fy", "gross_then_$M", "scope_note"], rows)


# ---------------------------------------------------------------------------
# 4. fydp_outyears.csv  (PB2027 P-40 Resource Summary FY2025-FY2031)
# ---------------------------------------------------------------------------
_FYDP_FY = [2025, 2026, 2027, 2028, 2029, 2030, 2031]
_FYDP_CSV_COL = {2025: "FY 2025", 2026: "FY 2026", 2027: "FY 2027 Total",
                 2028: "FY 2028", 2029: "FY 2029", 2030: "FY 2030", 2031: "FY 2031"}
_FYDP_ROWS = {
    "gross_then_$M": "Gross/Weapon System Cost ($ in Millions)",
    "qty": "Procurement Quantity (Units in Each)",
    "net_proc_$M": "Net Procurement (P-1) ($ in Millions)",
    "toa_$M": "Total Obligation Authority ($ in Millions)",
}


def _load_resource_summary(path: Path, li: int) -> dict:
    out = {}
    for r in _read(path):
        if (r.get("LI") or "").strip() != str(li):
            continue
        out[(r.get("Row Label") or "").strip()] = r
    return out


def build_fydp() -> None:
    rows = []
    for prog, li, path in [
        ("Virginia", 2013, SRC / "submarines/scn_li_resource_summary.csv"),
        ("Columbia", 1045, SRC / "submarines/scn_li_resource_summary.csv"),
        ("DDG-51", 2122, SRC / "ddg/scn_li_resource_summary.csv"),
    ]:
        rs = _load_resource_summary(path, li)
        for fy in _FYDP_FY:
            vals = []
            for key in ("gross_then_$M", "qty", "net_proc_$M", "toa_$M"):
                rec = rs.get(_FYDP_ROWS[key], {})
                vals.append(_num(rec.get(_FYDP_CSV_COL[fy])))
            rows.append([prog, li, fy] + vals)
    _write("fydp_outyears",
           ["program", "li", "fy", "gross_then_$M", "qty", "net_proc_$M", "toa_$M"], rows)


# ---------------------------------------------------------------------------
# 5. deflators.csv  (Green Book Procurement deflator, from workbook_core)
# ---------------------------------------------------------------------------
def build_deflators() -> None:
    rows = []
    for fy in _d.FY_RANGE:
        basis = "Extrapolated @ 2.1%/yr" if fy in _d.EXTRAPOLATED_FYS else "Green Book Table 5-4"
        rows.append([fy, f"{_d.raw_index(fy):.2f}", f"{_d.factor(fy):.2f}", basis])
    _write("deflators", ["fy", "procurement_index_fy2025_100",
                         "factor_const_fy2026", "basis"], rows)


# ---------------------------------------------------------------------------
# 6. ap_lltm.csv  (DDG-51 P-10 Ship Construction EOQ + CY AP gross, then-year $M)
# ---------------------------------------------------------------------------
# The DDG-only advance-procurement (P-10) line is SOURCE DATA, so it lives in the
# extracted pipeline (consumed on the SCN Budget tab), not hardcoded on Assumptions.
# Only the AP supplier COEFFICIENT remains a behavioral knob on Assumptions.
_AP_LLTM = {  # fy: (Ship Construction EOQ then-year, CY AP gross then-year [P-1 memo])
    2022: (0, 0), 2023: (0, 0), 2024: (0, 0),
    2025: (41.5, 83.224), 2026: (1000.0, 1750.0), 2027: (0, 0),
}


def build_ap_lltm() -> None:
    rows = [["DDG-51", 2122, fy, eoq, cy] for fy, (eoq, cy) in sorted(_AP_LLTM.items())]
    _write("ap_lltm", ["program", "li", "fy", "eoq_then_$M", "cy_gross_then_$M"], rows)


def main() -> int:
    print("build_extracted: reshaping source_data/ -> extracted/")
    build_scn_budget()
    build_place_of_performance()
    build_obbba()
    build_fydp()
    build_deflators()
    build_ap_lltm()
    print("done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
