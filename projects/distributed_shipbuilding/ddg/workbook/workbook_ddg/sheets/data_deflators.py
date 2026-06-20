"""data_deflators - the "Deflators" tab (DDG, data group; one module = one sheet).

Renders the shared DoD price-deflator index (workbook_core.deflators) as auditable
work: the Green Book Procurement TOA series (blue inputs, FY2025=100) and the rebased
constant-FY2026 factor. The factor is shown to two decimals and is the value the budget
sheets multiply by, so the displayed factor reconciles with the constant-$ rows.

Promoted accessor:
  deflator_factor_cell(fy)  -> 'Deflators'!<factor-col><row>  (a live cell the budget
                               sheets multiply by, not a baked constant)
"""
from __future__ import annotations

from workbook_core import deflators as _d
from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "Deflators"
_NCOLS = 4
# content columns under the gutter: B=FY, C=raw index, D=factor, E=basis
_FY_COL, _RAW_COL, _FAC_COL, _BASIS_COL = (col_letter(i) for i in (1, 2, 3, 4))


def _make_deflators():
    fac_row: dict = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    c.banner("§1 - DoD price deflators (Green Book Procurement TOA, rebased FY2026)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["FY", "Procurement deflator (FY2025=100)", "Factor to constant FY2026 $",
             "Basis"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])

    # Factor is written to two decimals (e.g. 1.10). It is text, so the budget sheets'
    # `then-year * factor` coerces it back to a number - meaning the displayed factor is
    # exactly the multiplier used, and the constant rows reconcile to it. FY2026 = 1.00.
    for fy in _d.FY_RANGE:
        basis = ("Extrapolated @ 2.1%/yr" if fy in _d.EXTRAPOLATED_FYS
                 else "Green Book Table 5-4")
        fac_row[fy] = c.write(
            [f"FY{fy}", _d.raw_index(fy), f"{_d.factor(fy):.2f}", basis],
            styles=[S_BOLD, S_NUM_INPUT, S_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    c.banner("§2 - Sources", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Series", "Source"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    c.write(["Green Book Procurement TOA", _d.GREEN_BOOK_CITE],
            styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.write(["FY2030-FY2031 outyears", _d.GREEN_BOOK_EXTRAP_CITE],
            styles=[S_BOLD, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[10, 44, 30, 28],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def deflator_factor_cell(fy: int) -> str:
        if fy not in fac_row:
            raise ValueError(f"FY {fy!r} outside {_d.FY_RANGE!r}")
        return f"'{_TAB}'!{_FAC_COL}{fac_row[fy]}"

    return SheetEntry(_TAB, _GROUP, render), deflator_factor_cell


(DEFLATORS, deflator_factor_cell) = _make_deflators()
