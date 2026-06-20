"""Overview - SCAFFOLD PLACEHOLDER: proves the workbook pipeline emits a valid sheet.

This is the seed module from the new-project scaffold. It renders a single title
banner so ``build_workbook.py`` produces a valid 1-sheet .xlsx immediately.
Replace it with real sheet modules per workbook_core/sheet_guide.md: copy
workbook_core/sheet_base_template.py to a new sheets/<name>.py, build
_build_rows(), and register its SheetEntry in sheets/__init__.py.

INTENT
    Placeholder summary tab; carries nothing the model depends on.

LAYOUT
    row 2 : title banner
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, banner_row
from workbook_core.styles import S_TITLE_SHEET
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

_GROUP = "summary"
_TAB = "Overview"
_COLS = [52, 14, 22]            # content widths, col B onward (gutter is auto)
_WITH_GUTTER = True


def _render() -> WorksheetSpec:
    rows: list[str] = []
    rows.append(banner_row(2, _TAB, n_cols=len(_COLS),
                           style=S_TITLE_SHEET, with_gutter=_WITH_GUTTER))
    ws = worksheet(
        rows,
        cols=_COLS,
        tab_color=group_color(_GROUP),
        with_gutter=_WITH_GUTTER,
    )
    return WorksheetSpec(ws)


OVERVIEW = SheetEntry(_TAB, _GROUP, _render)
