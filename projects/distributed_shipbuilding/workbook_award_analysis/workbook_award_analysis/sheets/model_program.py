"""model_program - the "Program" cut sheet (the headline trend).

The one section of Market Views that KEEPS the ≤FY12 -> FY26 grid: three rows
(Virginia / Columbia / DDG-51), supplier $M by subaward FY, fully DERIVED - black
per-FY SUMIFS over the Lane Detail leaf by program (via wt_total_fy_refs), with a
live row Total and a filter-aware SUBTOTAL Totals Row. Only three rows, so the FY
grid stays readable; the finer by-dimension cuts below are compact (no FY grid).

Built at import via _make_program() into a standalone single-table sheet (its
own title banner, §1 section table, column widths and autofilter).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    N_VALS, PROGRAMS, VAL_LABELS, row_sum,
)
from workbook_award_analysis.sheets.model_by_worktype import wt_total_fy_refs
from workbook_award_analysis.sheets._widths import W_PROGRAM, W_FY, header_styles
from workbook_award_analysis.sheets._tabs import TAB_PROGRAM

_GROUP = "model"
_TAB = TAB_PROGRAM
_BANNER = "§1 - Program"

_HEADERS = ["Program"] + VAL_LABELS
_CENTER_HDRS = set(VAL_LABELS)                          # center the FY grid
_NCOLS = len(_HEADERS)                                  # 1 + 16 = 17
_COLS = [W_PROGRAM] + [W_FY] * N_VALS
_VCOL = [col_letter(2 + j) for j in range(N_VALS)]      # C..R (16 value cols)


def _make_program():
    """Build the Program FY-trend cut sheet: a row-2 title banner + the §1
    section table. Returns the SheetEntry."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER_HDRS))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        last = c.write(
            [pname] + [f"={ref}" for ref in wt_total_fy_refs(prog)]
            + [row_sum(_VCOL[0], _VCOL[-2])],
            styles=[S_DEFAULT] + [S_NUM] * N_VALS,
            outline_level=1)
    table_ref = f"B{hdr}:{_VCOL[-1]}{last}"
    c.total(
        ["Total"] + [f"=SUBTOTAL(109,{col}{f}:{col}{last})" for col in _VCOL],
        styles=[S_BOLD] + [S_NUM] * N_VALS, n_cols=_NCOLS)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="ProgramFY", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


PROGRAM = _make_program()
