"""data_fydp_outyears - the "FYDP Outyears" tab (submarines, data group; one module = one sheet).

PB2027 P-40 Resource Summary for Virginia (LI 2013) and Columbia (LI 1045): the
FYDP grid FY2025-FY2031. FY2028-FY2031 are the budget-request outyears the Outlook
sheet projects implied Outsourced BC against; FY2025-FY2027 are carried so the
exhibit ties to the SCN Budget tab (FY 2027 Total = P-5c Total Ship Estimate;
Virginia FY2026 = the $5,389.1M one-boat value the TAM Build tripwire pins).
Outyear dollars are the PB2027 request, not appropriation - refresh at PB2028.

Promoted accessors:
  fydp_gross_then_cell(li, fy)    §1 then-year Gross/Weapon System Cost cell
  fydp_gross_cell(li, fy)         §2 constant-FY2026 gross cell, per class
  fydp_qty_cell(li, fy)           §1 procurement-quantity cell
  fydp_portfolio_gross_cell(fy)   §2 constant-FY2026 portfolio (Va + Col) cell
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._bind import EXTRACTED
from workbook_master_tam.sheets.submarines.data_deflators import deflator_factor_cell
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "data"
_TAB = "Sub FYDP Outyears"
_LIS = (2013, 1045)
_LI_LABEL = {2013: "Virginia (LI 2013)", 1045: "Columbia (LI 1045)"}
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


def _load() -> dict:
    out = {li: {} for li in _LIS}
    with (EXTRACTED / "scn_li_resource_summary.csv").open(encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh):
            li = (r.get("LI") or "").strip()
            if not li.isdigit() or int(li) not in out:
                continue
            out[int(li)][(r.get("Row Label") or "").strip()] = r
    return out


def _make_fydp_outyears():
    rs = _load()

    def _vals(li: int, row_label: str) -> list:
        rec = rs[li].get(row_label, {})
        return [_apnum(rec.get(_CSV_COL[fy])) for fy in _FY_COLUMNS]

    P: dict = {"gross_then": {}, "qty": {}, "gross_const": {}}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Source exhibit + then-year FYDP grids, one block per class
    c.banner("§1 - Source exhibit (P-40 Resource Summary, PB2027)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for field, value in [
        ("Exhibit", "PB 2027 Navy, Exhibit P-40 (1611N Shipbuilding and Conversion, Navy)"),
        ("Programs", "Virginia class (LI 2013) and Columbia class (LI 1045)"),
        ("Vintage", "PB2027 (April 2026); FY2028-FY2031 are the budget request, not appropriation"),
        ("Columns", "FY2027 = FY 2027 Total (Base + OOC); FY2028-FY2031 = FYDP outyears"),
        ("Refresh", "At PB2028: re-tie FY2027 gross to SCN Budget and re-base the outyears"),
    ]:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    for n, li in enumerate(_LIS, start=1):
        c.banner(f"§1{'ab'[n - 1]} - {_LI_LABEL[li]}, then-year $M", n_cols=_NCOLS,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Metric"] + list(_FY_COLUMNS),
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
        P["gross_then"][li] = c.write(
            ["Gross / Weapon System Cost, then-year $M"]
            + _vals(li, "Gross/Weapon System Cost ($ in Millions)"),
            styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
        P["qty"][li] = c.write(
            ["Procurement quantity (ships)"] + _vals(li, "Procurement Quantity (Units in Each)"),
            styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
        c.write(["Net Procurement (P-1), then-year $M (memo)"]
                + _vals(li, "Net Procurement (P-1) ($ in Millions)"),
                styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
        c.write(["Total Obligation Authority, then-year $M (memo)"]
                + _vals(li, "Total Obligation Authority ($ in Millions)"),
                styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
        c.blank()
    c.blank()

    # §2 Constant FY2026 $ (then-year x Green Book Procurement deflator; the
    # FY2030-FY2031 factors are extrapolated - see the Deflators tab).
    c.banner("§2 - Constant FY2026 $M (then-year x deflator)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    for li in _LIS:
        P["gross_const"][li] = c.write(
            [_LI_LABEL[li]]
            + [f"={_fy_col(fy)}{P['gross_then'][li]}*{deflator_factor_cell(fy)}"
               for fy in _FY_COLUMNS],
            styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)
    g13, g10 = P["gross_const"][2013], P["gross_const"][1045]
    P["portfolio_const"] = c.total(
        ["Portfolio (Va + Col), constant FY2026 $M"]
        + [f"=N({_fy_col(fy)}{g13})+N({_fy_col(fy)}{g10})" for fy in _FY_COLUMNS],
        styles=[S_BOLD] + [S_NUM] * len(_FY_COLUMNS), n_cols=_NCOLS)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 12, 12, 12, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def _check(li: int, fy: int) -> None:
        if li not in _LIS:
            raise ValueError(f"Unknown LI {li!r}; expected 2013 or 1045")
        if fy not in _FY_COL_INDEX:
            raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")

    def fydp_gross_then_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['gross_then'][li]}"

    def fydp_gross_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['gross_const'][li]}"

    def fydp_qty_cell(li: int, fy: int) -> str:
        _check(li, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['qty'][li]}"

    def fydp_portfolio_gross_cell(fy: int) -> str:
        _check(2013, fy)
        return f"'{_TAB}'!{_fy_col(fy)}{P['portfolio_const']}"

    return (SheetEntry(_TAB, _GROUP, render), fydp_gross_then_cell, fydp_gross_cell,
            fydp_qty_cell, fydp_portfolio_gross_cell)


(FYDP_OUTYEARS, fydp_gross_then_cell, fydp_gross_cell, fydp_qty_cell,
 fydp_portfolio_gross_cell) = _make_fydp_outyears()
