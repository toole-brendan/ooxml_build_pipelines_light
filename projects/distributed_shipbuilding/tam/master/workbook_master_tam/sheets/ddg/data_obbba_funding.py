"""data_obbba_funding - the "OBBBA Mandatory" tab (DDG, data group; one module = one sheet).

OBBBA (PL 119-21, Title II) Sec. 20002(17) mandatory funding for DDG-51 new
construction: $5,400.0M in FY2026 procuring two DDG-51 destroyers (DDG 147 / DDG 149)
under the current MYP. The award covers basic construction AND GFE with no source
breakout, so §2 bridges the gross award to a BC-addressable base via the editable
BC-share knob (Assumptions). TAM Build adds the BC base to its BC stream; the GFE
remainder stays out of TAM per the standing GFE exclusion. Additive to the P-5c
base (the FY27 PB P-1 carries zero FY2026 discretionary quantity).

Promoted accessors:
  obbba_gross_cell(li, fy)      §1b constant-FY2026 gross award cell
  obbba_bc_base_cell(li, fy)    §2 BC-addressable base cell (feeds TAM Build)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import load_extracted_csv
from workbook_master_tam.sheets.submarines.data_deflators import deflator_factor_cell
from workbook_master_tam.sheets.ddg.inputs_assumptions import obbba_bc_share_cell
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG OBBBA Mandatory"
_NCOLS = 7
_LI = 2122
_FY_COLUMNS = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL_INDEX = {fy: 2 + i for i, fy in enumerate(_FY_COLUMNS)}   # C..H


def _fy_col(fy: int) -> str:
    return col_letter(_FY_COL_INDEX[fy])


def _make_obbba_funding():
    headers, data = load_extracted_csv("obbba_ddg_mandatory")
    idx = {h: i for i, h in enumerate(headers)}
    rows = [{h: r[idx[h]] for h in headers} for r in data]
    ddg = next(r for r in rows if r["included"] == 1)
    _amt = {fy: (ddg["fy2026_$M"] if fy == 2026 else 0) for fy in _FY_COLUMNS}

    P: dict = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Source line
    c.banner("§1 - Source line (OBBBA Sec. 20002, line 17)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for field, value in [
        ("Authority", "PL 119-21 Title II (OBBBA), Sec. 20002 Shipbuilding, line 17"),
        ("Title", str(ddg["item"])),
        ("Program", "DDG-51 Arleigh Burke (LI 2122) - DDG 147 / DDG 149"),
        ("Funding type", "Mandatory appropriation (reconciliation)"),
        ("Scope", "Basic construction and government furnished equipment (no source breakout)"),
        ("Award timing", "Starting Q2 FY2026, under the current MYP contract"),
        ("Obligation availability", "Through 2029-09-30"),
        ("Booking basis", "Budget-year (all in FY2026)"),
    ]:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    P["then"] = c.write(["Sec. 20002(17) award, then-year $M"]
                        + [_amt[fy] for fy in _FY_COLUMNS],
                        styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    c.blank(2)

    # §1b Constant FY2026 $ (then-year x Green Book Procurement deflator; FY2026
    # factor is 1.00, kept so the row stays unit-consistent with SCN Budget §1b).
    c.banner("§1b - Constant FY2026 $M (then-year x deflator)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    P["const"] = c.write(
        ["Sec. 20002(17) award, constant FY2026 $M"]
        + [f"={_fy_col(fy)}{P['then']}*{deflator_factor_cell(fy)}" for fy in _FY_COLUMNS],
        styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)
    c.blank(2)

    # §2 BC/GFE bridge - the award funds BC + GFE as one number; only the BC share
    # is supplier-addressable, so the Assumptions BC-share knob splits it.
    c.banner("§2 - BC/GFE bridge", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    bc_vals = ["OBBBA BC base ($M, constant FY2026)"]
    for fy in _FY_COLUMNS:
        col = _fy_col(fy)
        bc_vals.append(f'=IF({col}{P["const"]}=0,"",{col}{P["const"]}*{obbba_bc_share_cell()})')
    P["bc_base"] = c.write(bc_vals, styles=[S_BOLD] + [S_NUM] * len(_FY_COLUMNS), outline_level=1)
    gfe_vals = ["GFE / non-BC remainder ($M; excluded from TAM)"]
    for fy in _FY_COLUMNS:
        col = _fy_col(fy)
        gfe_vals.append(f'=IF({col}{P["const"]}=0,"",{col}{P["const"]}-N({col}{P["bc_base"]}))')
    c.write(gfe_vals, styles=[S_DEFAULT] + [S_NUM] * len(_FY_COLUMNS), outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[44, 12, 12, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def _check(li: int, fy: int) -> None:
        if li != _LI:
            raise ValueError(f"Unknown LI {li!r}; DDG program is {_LI}")
        if fy not in _FY_COL_INDEX:
            raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")

    def obbba_gross_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['const']}"

    def obbba_bc_base_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['bc_base']}"

    return SheetEntry(_TAB, _GROUP, render), obbba_gross_cell, obbba_bc_base_cell


(OBBBA_FUNDING, obbba_gross_cell, obbba_bc_base_cell) = _make_obbba_funding()
