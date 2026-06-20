"""data_fydp_outyears - the "FYDP Outyears" tab (DDG, data group; one module = one sheet).

PB2027 P-40 Resource Summary for DDG-51 (LI 2122): the FYDP grid FY2025-FY2031.
FY2028-FY2031 are the budget-request outyears the Outlook sheet projects implied
Outsourced BC against; FY2025-FY2027 are carried so the exhibit ties to the SCN
Budget tab (FY 2027 Total = P-5c Total Ship Estimate). Outyear dollars are the
PB2027 request, not appropriation - refresh at PB2028.

Promoted accessors:
  fydp_gross_then_cell(li, fy)   §1 then-year Gross/Weapon System Cost cell
  fydp_gross_cell(li, fy)        §2 constant-FY2026 gross cell (Outlook reads this)
  fydp_qty_cell(li, fy)          §1 procurement-quantity cell
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.lib import EXTRACTED
from workbook_ddg.sheets.data_deflators import deflator_factor_cell
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "FYDP Outyears"
_LI = 2122
_FY_COLUMNS = [2025, 2026, 2027, 2028, 2029, 2030, 2031]
_FY_COL_INDEX = {fy: 2 + i for i, fy in enumerate(_FY_COLUMNS)}   # C..I
_NCOLS = 1 + len(_FY_COLUMNS)
# CSV column per FY; FY2027 uses the Total column (Base + OOC), which is the
# value that ties to the P-5c Total Ship Estimate.
_CSV_COL = {2025: "FY 2025", 2026: "FY 2026", 2027: "FY 2027 Total",
            2028: "FY 2028", 2029: "FY 2029", 2030: "FY 2030", 2031: "FY 2031"}


def _fy_col(fy: int) -> str:
    return col_letter(_FY_COL_INDEX[fy])


def _apnum(x):
    s = (str(x) if x is not None else "").strip().replace(",", "")
    if s in ("", "-"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _load(li: int) -> dict:
    out = {}
    with (EXTRACTED / "scn_li_resource_summary.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            if (r.get("LI") or "").strip() != str(li):
                continue
            out[(r.get("Row Label") or "").strip()] = r
    return out


def _make_fydp_outyears():
    rs = _load(_LI)
    p1_line = (next(iter(rs.values()), {}).get("P-1 Line") or "").strip()

    def _vals(row_label: str) -> list:
        rec = rs.get(row_label, {})
        return [_apnum(rec.get(_CSV_COL[fy])) for fy in _FY_COLUMNS]

    P: dict = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Source exhibit + then-year FYDP grid
    c.banner("§1 - Source exhibit (P-40 Resource Summary, PB2027)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for field, value in [
        ("Exhibit", "PB 2027 Navy, Exhibit P-40 (1611N Shipbuilding and Conversion, Navy)"),
        ("Program", f"DDG-51 Arleigh Burke (LI {_LI}), P-1 line {p1_line}"),
        ("Vintage", "PB2027 (April 2026); FY2028-FY2031 are the budget request, not appropriation"),
        ("Columns", "FY2027 = FY 2027 Total (Base + OOC); FY2028-FY2031 = FYDP outyears"),
        ("Refresh", "At PB2028: re-tie FY2027 gross to SCN Budget and re-base the outyears"),
    ]:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    P["gross_then"] = c.write(
        ["Gross / Weapon System Cost, then-year $M"] + _vals("Gross/Weapon System Cost ($ in Millions)"),
        styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    P["qty"] = c.write(
        ["Procurement quantity (ships)"] + _vals("Procurement Quantity (Units in Each)"),
        styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    c.write(["Net Procurement (P-1), then-year $M (memo)"] + _vals("Net Procurement (P-1) ($ in Millions)"),
            styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    c.write(["Total Obligation Authority, then-year $M (memo)"] + _vals("Total Obligation Authority ($ in Millions)"),
            styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    c.blank(2)

    # §2 Constant FY2026 $ (then-year x Green Book Procurement deflator; the
    # FY2030-FY2031 factors are extrapolated - see the Deflators tab).
    c.banner("§2 - Constant FY2026 $M (then-year x deflator)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    P["gross_const"] = c.write(
        ["Gross / Weapon System Cost, constant FY2026 $M"]
        + [f"={_fy_col(fy)}{P['gross_then']}*{deflator_factor_cell(fy)}" for fy in _FY_COLUMNS],
        styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 12, 12, 12, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def _check(li: int, fy: int) -> None:
        if li != _LI:
            raise ValueError(f"Unknown LI {li!r}; DDG program is {_LI}")
        if fy not in _FY_COL_INDEX:
            raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")

    def fydp_gross_then_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['gross_then']}"

    def fydp_gross_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['gross_const']}"

    def fydp_qty_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['qty']}"

    return SheetEntry(_TAB, _GROUP, render), fydp_gross_then_cell, fydp_gross_cell, fydp_qty_cell


(FYDP_OUTYEARS, fydp_gross_then_cell, fydp_gross_cell, fydp_qty_cell) = _make_fydp_outyears()
