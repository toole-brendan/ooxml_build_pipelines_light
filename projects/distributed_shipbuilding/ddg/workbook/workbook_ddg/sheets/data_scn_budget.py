"""data_scn_budget - the "SCN Budget" tab (DDG, data group; one module = one sheet).

Raw + derived SCN P-5c cost-category support for Basic Construction. The former SCN
section of the composite Budget tab, now its own tab. Basic Construction is the
value consumed by TAM Build (its BC stream base).

Promoted accessors:
  scn_cell(li, fy, metric)          per-FY P-5c cost-category cell (§1/§2)
  portfolio_scn_cell(metric)        FY2022-FY2027 cumulative cost-funnel cell (§3)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.lib import load_extracted_csv
from workbook_ddg.sheets.data_deflators import deflator_factor_cell
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "SCN Budget"
_NCOLS = 7
_LI = 2122
_FY_COLUMNS = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL_INDEX = {fy: 2 + i for i, fy in enumerate(_FY_COLUMNS)}


def _fy_col(fy: int) -> str:
    return col_letter(_FY_COL_INDEX[fy])


def _make_scn_budget():
    def _scn_load():
        headers, data = load_extracted_csv("cost_funnel_summary")
        idx = {h: i for i, h in enumerate(headers)}
        cols = {"total": "total_ship_estimate_$M", "plans": "plan_costs_$M",
                "electronics": "electronics_$M", "ordnance": "ordnance_$M",
                "hme": "hme_$M", "other_cost": "other_cost_$M",
                "gfe": "gfe_elec_ord_$M", "change_orders": "change_orders_$M",
                "basic": "basic_construction_$M"}
        out = {}
        for r in data:
            li, fy = r[idx["LI"]], r[idx["FY"]]
            if li != _LI or fy not in _FY_COL_INDEX:
                continue
            out[fy] = {k: r[idx[c]] for k, c in cols.items()}
        return out

    _SCN = _scn_load()
    P: dict = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Cost categories
    c.banner("§1 - Cost categories (DDG-51 LI 2122, $M per FY)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))

    def _cat(label, key):
        return c.write([label] + [_SCN.get(fy, {}).get(key) for fy in _FY_COLUMNS],
                       styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)

    P["total"] = _cat("Total Ship Estimate", "total")
    P["plans"] = _cat("Plans Costs", "plans")
    P["electronics"] = _cat("Electronics", "electronics")
    P["ordnance"] = _cat("Ordnance", "ordnance")
    P["hme"] = _cat("Hull, Mechanical, Electrical (HM&E; missing pre-FY24)", "hme")
    P["other_cost"] = _cat("Other Cost", "other_cost")
    P["gfe"] = _cat("GFE Sum (Electronics + Ordnance)", "gfe")
    P["change_orders"] = _cat("Change Orders", "change_orders")
    P["basic"] = _cat("Basic Construction (BC base -> TAM Build)", "basic")
    c.write(["FY2026 is discretionary-only; the two FY2026 ships (DDG 147/149) are funded "
             "via OBBBA Sec. 20002(17) (see OBBBA Mandatory tab)."],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §1b Constant FY2026 $ (then-year x Green Book Procurement deflator). This block,
    # not §1, is the constant-dollar source the model and this sheet's §2/§3 read; §1
    # stays as the blue then-year provenance. All P-5c categories are deflated at the
    # one Procurement factor (GFE included as an approximation - GFE is removed before
    # TAM, so it is not load-bearing) so the cost funnel stays internally consistent.
    c.banner("§1b - Constant FY2026 $M (then-year x deflator)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    Pc: dict = {}

    def _cat_const(label, key):
        vals = [label] + [f"={_fy_col(fy)}{P[key]}*{deflator_factor_cell(fy)}"
                          for fy in _FY_COLUMNS]
        Pc[key] = c.write(vals, styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS),
                          outline_level=1)

    _cat_const("Total Ship Estimate", "total")
    _cat_const("Plans Costs", "plans")
    _cat_const("Electronics", "electronics")
    _cat_const("Ordnance", "ordnance")
    _cat_const("Hull, Mechanical, Electrical (HM&E)", "hme")
    _cat_const("Other Cost", "other_cost")
    _cat_const("GFE Sum (Electronics + Ordnance)", "gfe")
    _cat_const("Change Orders", "change_orders")
    _cat_const("Basic Construction (BC base -> TAM Build)", "basic")
    c.blank(2)

    # §2 Derived ratios
    c.banner("§2 - Derived ratios", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Ratio"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    r_total = Pc["total"]                                    # constant-$ rows (§1b)
    for label, num_key, pkey in [("BC % of Total", "basic", "bc_pct"),
                                 ("GFE % of Total", "gfe", "gfe_pct")]:
        num_r = Pc[num_key]
        vals = [label] + [f'=IF({_fy_col(fy)}{r_total}=0,"",{_fy_col(fy)}{num_r}/{_fy_col(fy)}{r_total})'
                          for fy in _FY_COLUMNS]
        P[pkey] = c.write(vals, styles=[S_BOLD] + [S_PCT] * len(_FY_COLUMNS), outline_level=1)
    c.blank(2)

    # §3 Portfolio cost funnel (FY2022-FY2027 cumulative) - the standardized slide-05
    # funnel base. Live SUMs of the §1 annual rows, so the workbook (not the deck) is
    # the source of truth for the cumulative Total -> GFE -> other -> Basic Construction
    # narrowing. "other non-BC" is the residual Total - GFE - Basic Construction.
    c.banner("§3 - Portfolio cost funnel (FY2022-FY2027 cumulative, $M)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "FY2022-FY2027"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _c0, _cN = _fy_col(_FY_COLUMNS[0]), _fy_col(_FY_COLUMNS[-1])   # C..H (FY22..FY27)
    _vc = _c0                                                      # portfolio value column

    def _fy_sum(pkey):
        return f"SUM({_c0}{Pc[pkey]}:{_cN}{Pc[pkey]})"     # sum the constant-$ rows (§1b)

    P["portfolio_total"] = c.write(
        ["Total ship estimate", f"={_fy_sum('total')}"],
        styles=[S_BOLD, S_NUM], outline_level=1)
    P["portfolio_gfe"] = c.write(
        ["Less GFE / directed equipment", f"={_fy_sum('gfe')}"],
        styles=[S_DEFAULT, S_NUM], outline_level=1)
    P["portfolio_other_non_bc"] = c.write(
        ["Less other non-BC categories",
         f"={_vc}{P['portfolio_total']}-{_vc}{P['portfolio_gfe']}-{_fy_sum('basic')}"],
        styles=[S_DEFAULT, S_NUM], outline_level=1)
    P["portfolio_basic"] = c.write(
        ["Basic Construction base", f"={_fy_sum('basic')}"],
        styles=[S_BOLD, S_NUM], outline_level=1)
    P["portfolio_bc_pct"] = c.write(
        ["BC % of Total",
         f'=IF({_vc}{P["portfolio_total"]}=0,"",{_vc}{P["portfolio_basic"]}/{_vc}{P["portfolio_total"]})'],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    P["portfolio_gfe_pct"] = c.write(
        ["GFE % of Total",
         f'=IF({_vc}{P["portfolio_total"]}=0,"",{_vc}{P["portfolio_gfe"]}/{_vc}{P["portfolio_total"]})'],
        styles=[S_DEFAULT, S_PCT], outline_level=1)

    # Dollar metrics resolve to the constant-FY2026 rows (§1b); ratio metrics stay on
    # the §2 rows (a ratio of same-FY dollars is deflator-invariant).
    scn_metric_row = {
        "total": Pc["total"], "plans": Pc["plans"], "electronics": Pc["electronics"],
        "ordnance": Pc["ordnance"], "hme": Pc["hme"], "other_cost": Pc["other_cost"],
        "gfe": Pc["gfe"], "change_orders": Pc["change_orders"], "basic": Pc["basic"],
        "bc_pct": P["bc_pct"], "gfe_pct": P["gfe_pct"],
    }
    portfolio_metric_row = {
        "total": P["portfolio_total"], "gfe": P["portfolio_gfe"],
        "other_non_bc": P["portfolio_other_non_bc"], "basic": P["portfolio_basic"],
        "bc_pct": P["portfolio_bc_pct"], "gfe_pct": P["portfolio_gfe_pct"],
    }

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[44, 12, 12, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def scn_cell(li: int, fy: int, metric: str) -> str:
        if li != _LI:
            raise ValueError(f"Unknown LI {li!r}; DDG program is {_LI}")
        if fy not in _FY_COL_INDEX:
            raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")
        if metric not in scn_metric_row:
            raise ValueError(f"Unknown metric {metric!r}")
        return f"'{_TAB}'!{_fy_col(fy)}{scn_metric_row[metric]}"

    def portfolio_scn_cell(metric: str) -> str:
        """FY2022-FY2027 cumulative cost-funnel cell (§3). metric in
        total | gfe | other_non_bc | basic | bc_pct | gfe_pct."""
        if metric not in portfolio_metric_row:
            raise ValueError(f"Unknown portfolio metric {metric!r}")
        return f"'{_TAB}'!{_vc}{portfolio_metric_row[metric]}"

    return SheetEntry(_TAB, _GROUP, render), scn_cell, portfolio_scn_cell


(SCN_BUDGET, scn_cell, portfolio_scn_cell) = _make_scn_budget()
