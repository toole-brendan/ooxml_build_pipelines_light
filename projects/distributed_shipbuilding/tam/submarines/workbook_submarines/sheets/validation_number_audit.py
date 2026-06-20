"""validation_number_audit - the "Number Audit" tab (one module = one sheet).

Every registered Figure Register figure tied back to its producer cell: deck value
(the registry's link) vs source value (the producer cell), with a delta and a
pass/fail status. Imports the Figure Register registry + accessors. Produces
fail_count_formula / status_range (consumed by QA Reconciliation + Executive Summary).

Audit basis (kept here, not as cell prose): deck value links to the Figure Register
E column; source value links to the producer cell; status FAILs when the absolute
delta exceeds the tolerance.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT, S_LINK_NUM,
    S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.outputs_figure_register import REGISTRY, value_cell, source_ref, is_pct
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "validation"
_TAB = "Number Audit"
_TOL = 0.01
_BASE = 12                                       # title(2) + blank + §1 at-a-glance(4-9) + 2 blanks
_NA_HEADERS = ["Figure ID", "Slide", "Deck value", "Source value", "Delta", "Status"]


def _build_number_audit(tab: str, base: int):
    c = RowCursor(base)
    c.banner("§2 - Figure tie-out (every registered figure vs its producer cell)", n_cols=6,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    header = c.write(_NA_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER,
                                          S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    first = c.at()
    for fid, slide, _label, ref in REGISTRY:
        pct = is_pct(fid)
        ds = S_LINK_PCT if pct else S_LINK_NUM
        dl = S_PCT if pct else S_NUM
        c.write([fid, slide, f"={value_cell(fid)}", f"={ref}",
                 lambda r: f"=D{r}-E{r}", lambda r: f'=IF(ABS(F{r})<{_TOL},"OK","FAIL")'],
                styles=[S_DEFAULT, S_DEFAULT, ds, ds, dl, S_DEFAULT], outline_level=1)
    last = c.at() - 1

    table = ExcelTable(name="tbl_sub_number_audit",
                       ref=f"B{header}:{col_letter(len(_NA_HEADERS))}{last}", headers=_NA_HEADERS)

    def status_range(): return f"'{tab}'!G{first}:G{last}"
    def fail_count_formula(): return f'COUNTIF({status_range()},"FAIL")'
    return c.rows, c.at(), [table], dict(status_range=status_range, fail_count_formula=fail_count_formula)


# ── Layout pass: tie-out first (promotes fail_count_formula), then at-a-glance ─
_rows, _after, _tables, _acc = _build_number_audit(_TAB, _BASE)
status_range = _acc["status_range"]
fail_count_formula = _acc["fail_count_formula"]


def _render_number_audit() -> WorksheetSpec:
    n_cols = 6
    c = RowCursor(2)
    c.banner("Number Audit", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Figure tie-out", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value", "Target"], styles=S_HEADER_LEFT)
    c.write(["Figures tested", len(REGISTRY), "every Figure Register row"],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT])
    c.write(["FAIL count", f"={fail_count_formula()}", "target 0"], styles=[S_BOLD, S_NUM, S_DEFAULT])
    c.write(["Status", f'=IF({fail_count_formula()}=0,"OK","FAIL")', f"tolerance {_TOL}"],
            styles=[S_BOLD, S_DEFAULT, S_DEFAULT])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)
    c.blank(2)

    # §3 Exceptions
    c.banner("§3 - Exceptions", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Figure ID", "Issue", "Required action"], styles=S_HEADER_LEFT)
    c.write(["None", "No exceptions while FAIL count = 0", "n/a"],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    ws = worksheet(c.rows, cols=[24, 16, 16, 12, 10, 10], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, tables=_tables)


NUMBER_AUDIT = SheetEntry(_TAB, _GROUP, _render_number_audit)
