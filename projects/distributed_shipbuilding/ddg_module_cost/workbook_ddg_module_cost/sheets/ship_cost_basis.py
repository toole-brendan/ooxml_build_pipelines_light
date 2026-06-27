"""ship_cost_basis - the "Ship Cost Basis" data tab.

The DDG-51 (LI 2122) P-5c cost-category slice, mirrored from the Master TAM
workbook's extracted/scn_budget.csv (then-year $M), with the Green Book deflator
applied to constant FY2026 $M and divided by the per-FY procurement quantity to a
PER-SHIP figure. The per-ship Basic Construction line is the numerator the rest of
the workbook allocates down the structural hierarchy.

Cost structure (verified from the TAM slice): for DDG-51,
    Total = Basic + Plans + HM&E + Other + Change Orders + GFE,  GFE = Electronics + Ordnance.
So Basic Construction is a standalone shipbuilder line; GFE (government-furnished
Aegis/SPY electronics + VLS/ordnance) is separate and never inside Basic.

Promoted accessors:
  per_ship_bc_cell(fy)   -> 'Ship Cost Basis'!<col><row>  per-ship Basic Construction,
                            const FY2026 $M (only FY2025 / FY2027 carry a quantity)
  per_ship_bc_range()    -> the per-ship BC row range C..H (for INDEX/MATCH by FY)
  fy_axis_range()        -> the numeric-FY row range C..H (the MATCH lookup axis)
  per_ship_total_cell(fy)-> per-ship Total Ship Estimate, const FY2026 $M (context)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NOTE, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_NUM_INPUT, S_INT, S_INT_INPUT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._cuts import load_rows, as_float, as_int
from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._factor import S_FACTOR
from workbook_ddg_module_cost.sheets._tabs import TAB_SHIP_COST_BASIS
from workbook_ddg_module_cost.sheets import _widths as W

_GROUP = "data"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(_FY)}     # C..H
_C0, _CN = _FY_COL[_FY[0]], _FY_COL[_FY[-1]]                      # C, H
_NCOLS = 1 + len(_FY)                                            # label + 6 FY
_HDR_FY = [S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY)

# §1 cost-category rows (CSV column key -> display label), outermost-first.
_CATS = [
    ("basic",         "Basic Construction (TAM base)"),
    ("plans",         "Plans"),
    ("hme",           "Hull, Mechanical & Electrical (HM&E)"),
    ("electronics",   "Electronics (GFE)"),
    ("ordnance",      "Ordnance (GFE)"),
    ("other_cost",    "Other Cost"),
    ("gfe",           "GFE Sum (= Electronics + Ordnance)"),
    ("change_orders", "Change Orders"),
    ("total",         "Total Ship Estimate"),
]


def _make():
    raw = load_rows("ddg_ship_cost")
    data: dict[int, dict] = {}
    for r in raw:
        fy = int(r["fy"])
        data[fy] = {k: as_float(r.get(k)) for k, _ in _CATS}
        data[fy]["qty"] = as_int(r.get("qty"))
        data[fy]["deflator_factor"] = as_float(r.get("deflator_factor"))

    P: dict = {}
    c = RowCursor(2)
    c.title(TAB_SHIP_COST_BASIS, _NCOLS)
    c.caption("DDG-51 (LI 2122) P-5c cost slice, mirrored from the Master TAM workbook")
    c.blank(2)

    # §1 then-year categories ---------------------------------------------------------
    c.section("§1 - P-5c cost categories, then-year $M", _NCOLS)
    c.blank()
    c.write(["Cost category"] + [f"FY{fy}" for fy in _FY], styles=_HDR_FY)
    cat_row: dict[str, int] = {}
    for key, label in _CATS:
        vals = [label] + [data.get(fy, {}).get(key) for fy in _FY]
        cat_row[key] = c.write(vals, styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY))
    c.write(["GFE = Electronics + Ordnance (government-furnished combat systems; "
             "installed late / pier-side, not part of a structural block)"],
            styles=[S_NOTE])
    c.blank(2)

    # §2 constant FY2026 $ and per-ship ----------------------------------------------
    c.section("§2 - Constant FY2026 $M and per ship", _NCOLS)
    c.blank()
    c.write(["Line"] + [f"FY{fy}" for fy in _FY], styles=_HDR_FY)

    # numeric FY axis (the MATCH lookup row). General format (S_DEFAULT) so the
    # years render 2022..2027 with NO thousands separator.
    P["fy_axis"] = c.write(["Fiscal year (FY)"] + list(_FY),
                           styles=[S_BOLD] + [S_DEFAULT] * len(_FY))
    # Green Book factor (then-year -> constant FY2026), two decimals
    P["factor"] = c.write(
        ["Constant-FY2026 factor (Green Book)"]
        + [data.get(fy, {}).get("deflator_factor") for fy in _FY],
        styles=[S_DEFAULT] + [S_FACTOR] * len(_FY))
    # constant-FY2026 Basic Construction = then * factor
    P["const_basic"] = c.write(
        ["Basic Construction, const FY2026 $M"]
        + [f"={_FY_COL[fy]}{cat_row['basic']}*{_FY_COL[fy]}{P['factor']}" for fy in _FY],
        styles=[S_DEFAULT] + [S_NUM] * len(_FY))
    # constant-FY2026 Total Ship Estimate = then * factor (context)
    P["const_total"] = c.write(
        ["Total Ship Estimate, const FY2026 $M"]
        + [f"={_FY_COL[fy]}{cat_row['total']}*{_FY_COL[fy]}{P['factor']}" for fy in _FY],
        styles=[S_DEFAULT] + [S_NUM] * len(_FY))
    # procurement quantity (ships) - blank where there is no buy
    P["qty"] = c.write(
        ["Procurement quantity (ships)"]
        + [data.get(fy, {}).get("qty") for fy in _FY],
        styles=[S_DEFAULT] + [S_INT_INPUT] * len(_FY))

    def _per_ship(const_row):
        """Per-ship row: const / qty only where a quantity exists (else blank)."""
        out = []
        for fy in _FY:
            if data.get(fy, {}).get("qty"):
                out.append(f"={_FY_COL[fy]}{const_row}/{_FY_COL[fy]}{P['qty']}")
            else:
                out.append(None)
        return out

    P["per_ship_bc"] = c.total(
        ["Per-ship Basic Construction, const FY2026 $M"] + _per_ship(P["const_basic"]),
        styles=[S_BOLD] + [S_NUM] * len(_FY), n_cols=_NCOLS)
    P["per_ship_total"] = c.write(
        ["Per-ship Total Ship Estimate, const FY2026 $M"] + _per_ship(P["const_total"]),
        styles=[S_DEFAULT] + [S_NUM] * len(_FY))
    c.write(["Per-ship figures exist only for FY2025 (3-ship buy) and FY2027 "
             "(1-ship buy); other years have no procurement quantity."],
            styles=[S_NOTE])
    c.blank(2)

    # §3 source ----------------------------------------------------------------------
    c.section("§3 - Source", _NCOLS)
    c.blank()
    c.write(["Series", "Source"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    c.write(["P-5c cost categories",
             "Master TAM workbook, extracted/scn_budget.csv (DDG-51 LI 2122, "
             "PB exhibits); GFE = Electronics + Ordnance"],
            styles=[S_BOLD, S_DEFAULT])
    c.write(["Quantities",
             "Master TAM workbook, extracted/fydp_outyears.csv (PB2027 P-40)"],
            styles=[S_BOLD, S_DEFAULT])
    c.write(["Deflator",
             "Master TAM workbook, extracted/deflators.csv (Green Book Procurement "
             "TOA; FY2025=100, rebased FY2026=1.000)"],
            styles=[S_BOLD, S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[W.W_LABEL_WIDE] + [W.W_DOLLAR] * len(_FY),
                       tab_color=group_color(_GROUP), with_gutter=True,
                       show_outline_symbols=False)
        return WorksheetSpec(ws)

    def per_ship_bc_cell(fy: int) -> str:
        if not data.get(fy, {}).get("qty"):
            raise ValueError(f"FY{fy} has no per-ship Basic Construction (no quantity)")
        return f"'{TAB_SHIP_COST_BASIS}'!{_FY_COL[fy]}{P['per_ship_bc']}"

    def per_ship_total_cell(fy: int) -> str:
        if not data.get(fy, {}).get("qty"):
            raise ValueError(f"FY{fy} has no per-ship total (no quantity)")
        return f"'{TAB_SHIP_COST_BASIS}'!{_FY_COL[fy]}{P['per_ship_total']}"

    def per_ship_bc_range() -> str:
        return f"'{TAB_SHIP_COST_BASIS}'!{_C0}{P['per_ship_bc']}:{_CN}{P['per_ship_bc']}"

    def fy_axis_range() -> str:
        return f"'{TAB_SHIP_COST_BASIS}'!{_C0}{P['fy_axis']}:{_CN}{P['fy_axis']}"

    return (SheetEntry(TAB_SHIP_COST_BASIS, _GROUP, render),
            dict(per_ship_bc_cell=per_ship_bc_cell,
                 per_ship_total_cell=per_ship_total_cell,
                 per_ship_bc_range=per_ship_bc_range,
                 fy_axis_range=fy_axis_range))


(SHIP_COST_BASIS, _A) = _make()
per_ship_bc_cell = _A["per_ship_bc_cell"]
per_ship_total_cell = _A["per_ship_total_cell"]
per_ship_bc_range = _A["per_ship_bc_range"]
fy_axis_range = _A["fy_axis_range"]
