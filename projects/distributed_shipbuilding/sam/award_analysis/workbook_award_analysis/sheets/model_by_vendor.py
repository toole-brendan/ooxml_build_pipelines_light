"""model_by_vendor - the "Vendor" cut sheet (compact).

The full supplier vendor roster (all three programs, every vendor key with at
least one supplier record) as one filterable native table: identity, modal work
type, cut profile, first/last award dates (real date cells, so Summary's
MINIFS/MAXIFS span formulas aggregate them), record count and full-history $M.
COMPACT (no 16-FY grid): both Records and $M are DERIVED - black SUMIFS over the
Lane Vendors leaf by (program, vendor UEI). A vendor active on both submarine
classes appears once per class program; its Cut Profile reads "both". Per-program
SUMIF totals sit under the table (the Checks link targets).

Built at import via _make_by_vendor() into a standalone single-table sheet (its
own title banner, §1 section table, column widths and autofilter).

Promoted accessors (bound to this sheet's rows; imported by Summary / Checks):
  vendor_total_cell(program)         - full-history supplier $M total cell (Checks).
  vendor_records_total_cell(program) - full-history record total cell (Checks).
  bv_cols()                          - program / cut profile / first / last award /
                                       $M column ranges (Summary's corpus-shape and
                                       top-vendor-share formulas).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DATE_INPUT, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, PROGRAMS, date_serial, load,
)
from workbook_award_analysis.sheets.data_lane_vendors import vl_cols
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_UEI, W_VENDOR, W_WORKTYPE, W_STATUS, W_DATE, W_COUNT, W_DOLLAR,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_VENDOR

_GROUP = "model"
_TAB = TAB_VENDOR
_BANNER = "§1 - Vendor"

_DATE_HDRS = {"First Award", "Last Award"}

_META = ["Program", "Vendor UEI", "Vendor", "Work Type", "Cut Profile",
         "First Award", "Last Award", "Records", "$M"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_UEI, W_VENDOR, W_WORKTYPE, W_STATUS, W_DATE, W_DATE,
         W_COUNT, W_DOLLAR]
_PROG_COL = col_letter(1)                               # B
_PROFILE_COL = col_letter(5)                            # F (Cut Profile)
_FA_COL = col_letter(6)                                 # G (First Award)
_LA_COL = col_letter(7)                                 # H (Last Award)
_REC_COL = col_letter(8)                                # I (Records)
_TOT_COL = col_letter(9)                                # J ($M)


def _make_by_vendor():
    """Build the Vendor roster cut sheet: a row-2 title banner + the §1 section
    table. Returns (SheetEntry, vendor_total_cell, vendor_records_total_cell,
    bv_cols)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_vendor_fy")
    V = vl_cols()

    def records_f(r: int) -> str:
        return f"=SUMIFS({V['rec']},{V['prog']},B{r},{V['uei']},C{r})"

    def dollar_f(r: int) -> str:
        return f"=SUMIFS({V['dol']},{V['prog']},B{r},{V['uei']},C{r})"

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META, _DATE_HDRS))
    first = last = None
    for row in rows:
        r = c.write([row[i["program"]], row[i["vendor_uei"]],
                     row[i["vendor_name"]],
                     BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                     row[i["cut_profile"]],
                     date_serial(row[i["first_award"]]),
                     date_serial(row[i["last_award"]]),
                     records_f, dollar_f],
                    styles=[S_DEFAULT] * 5 + [S_DATE_INPUT] * 2 + [S_INT, S_NUM],
                    outline_level=1)
        first = first if first is not None else r
        last = r
    table_ref = f"B{hdr}:{_TOT_COL}{last}"
    c.blank(2)

    vendor_total: dict[str, int] = {}
    for prog, pname in PROGRAMS:
        vendor_total[prog] = c.write(
            [f"{pname} supplier total ($M, full history)", None, None, None,
             None, None, None,
             f'=SUMIF(${_PROG_COL}${first}:${_PROG_COL}${last},"{prog}",'
             f'${_REC_COL}${first}:${_REC_COL}${last})',
             f'=SUMIF(${_PROG_COL}${first}:${_PROG_COL}${last},"{prog}",'
             f'${_TOT_COL}${first}:${_TOT_COL}${last})'],
            styles=[S_DEFAULT] * 7 + [S_INT, S_NUM])

    def vendor_total_cell(program: str) -> str:
        return f"'{_TAB}'!{_TOT_COL}{vendor_total[program]}"

    def vendor_records_total_cell(program: str) -> str:
        return f"'{_TAB}'!{_REC_COL}{vendor_total[program]}"

    def bv_cols() -> dict:
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${first}:${col}${last}"
        return {"prog": rng(_PROG_COL), "profile": rng(_PROFILE_COL),
                "first": rng(_FA_COL), "last": rng(_LA_COL),
                "tot": rng(_TOT_COL)}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="MarketVendor", ref=table_ref, headers=_META)])

    return (SheetEntry(_TAB, _GROUP, render), vendor_total_cell,
            vendor_records_total_cell, bv_cols)


(VENDOR, vendor_total_cell, vendor_records_total_cell,
 bv_cols) = _make_by_vendor()
