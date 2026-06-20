"""validation_number_audit - the "Number Audit" tab (DDG, validation group; one module = one sheet).

Ties every deck figure back to its source cell. Each deck value must equal its
producer; the fail count gates the deck. §2 is a native no-format table.

Promoted accessors:
  fail_count_formula, fail_count_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets.outputs_figure_register import REGISTRY, value_cell, source_ref
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "validation"
_TAB = "Number Audit"
_NCOLS = 6
_Q = '"'
_TOL = 0.01
_REG_LEN = len(REGISTRY)
_FAIL_ROW = 7                    # §1 "Figures failing tie-out" value cell
_NA_HEADER = 13                  # §2 native-table header row
_NA_FIRST = _NA_HEADER + 1
_NA_LAST = _NA_FIRST + _REG_LEN - 1
_HEADERS = ["Figure ID", "Slide", "Deck value", "Source value", "Delta", "Status"]


def fail_count_formula():
    return f'COUNTIF(\'{_TAB}\'!G{_NA_FIRST}:G{_NA_LAST},{_Q}FAIL{_Q})'


def fail_count_cell():
    return f"'{_TAB}'!C{_FAIL_ROW}"


def _render_figure_audit() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Tie-out status
    c.banner("§1 - Tie-out status", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    fail_row = c.write(["Figures failing tie-out", f"={fail_count_formula()}"],
                       styles=[S_BOLD, S_NUM], outline_level=1)
    assert fail_row == _FAIL_ROW, f"fail row at {fail_row}, expected {_FAIL_ROW}"
    c.write(["Status", f'=IF({fail_count_formula()}=0,{_Q}OK{_Q},{_Q}FAIL{_Q})'],
            styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Figure tie-out (native table; each deck value must equal its producer)
    c.banner("§2 - Figure tie-out (deck value vs source cell)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    header_row = c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER,
                                           S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    assert header_row == _NA_HEADER, f"na header at {header_row}, expected {_NA_HEADER}"
    for fid, slide, _label, ref, pct in REGISTRY:
        link = S_LINK_PCT if pct else S_LINK_NUM
        delta = S_PCT if pct else S_NUM
        r = c.at()
        c.write([fid, slide, f"={value_cell(fid)}", f"={ref}", f"=D{r}-E{r}",
                 f'=IF(ABS(F{r})<{_TOL},{_Q}OK{_Q},{_Q}FAIL{_Q})'],
                styles=[S_DEFAULT, S_DEFAULT, link, link, delta, S_DEFAULT], outline_level=1)
    table = ExcelTable(name="tbl_ddg_figure_audit",
                       ref=f"B{header_row}:{col_letter(len(_HEADERS))}{_NA_LAST}",
                       headers=_HEADERS)
    ws = worksheet(c.rows, cols=[12, 7, 16, 16, 12, 10],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, tables=[table])


NUMBER_AUDIT = SheetEntry(_TAB, _GROUP, _render_figure_audit)
