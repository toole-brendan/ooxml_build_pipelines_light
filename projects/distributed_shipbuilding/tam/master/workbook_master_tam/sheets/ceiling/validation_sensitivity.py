"""validation_sensitivity - the "Sensitivity" tab (validation group).

The answer is a bracket, so the parameters get swept. §1 is a two-way grid of
ceiling % = 1 - L*(1 - h) over plausible L (down) and h (across). §2 sweeps the
bridge pass-through p at the live Virginia central case (outsourced share of BC
= hL + p*M), showing the labor-only -> material-inclusive span. The axis values
are blue scan inputs; the grid bodies are live formulas.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_PCT, S_PCT_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ceiling._layout import RowCursor
from workbook_master_tam.sheets.ceiling.inputs_assumptions import (
    core_h_cell, labor_share_cell,
)

_GROUP = "validation"
_TAB = "Ceiling Sensitivity"

_H_AXIS = [0.30, 0.40, 0.50, 0.60, 0.70]
_L_AXIS = [0.35, 0.40, 0.45, 0.50, 0.55, 0.60]
_P_AXIS = [0.00, 0.25, 0.50, 0.75, 1.00]
_NCOLS = 1 + len(_H_AXIS)            # label + 5 axis cols (B..G)
_AXIS_COLS = [col_letter(2 + i) for i in range(len(_H_AXIS))]   # C..G


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - ceiling % = 1 - L*(1-h), L down / h across
    c.banner("§1 - Ceiling % sensitivity (L down, h across)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hrow = c.write(["L \\ h"] + _H_AXIS,
                   styles=[S_HEADER_LEFT] + [S_PCT_INPUT] * len(_H_AXIS))
    for Lval in _L_AXIS:
        c.write(
            [Lval] + [(lambda rr, col=cc: f"=1-$B{rr}*(1-{col}${hrow})")
                      for cc in _AXIS_COLS],
            styles=[S_PCT_INPUT] + [S_PCT] * len(_H_AXIS), outline_level=1)
    c.blank(2)

    # §2 - bridge pass-through sweep at the live Virginia central case
    c.banner("§2 - Outsourced share vs pass-through p (Virginia params)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    prow = c.write(["Outsourced share \\ p"] + _P_AXIS,
                   styles=[S_HEADER_LEFT] + [S_PCT_INPUT] * len(_P_AXIS))
    _hL = f"{labor_share_cell('Virginia')}*{core_h_cell('Virginia')}"
    _M = f"(1-{labor_share_cell('Virginia')})"
    c.write(["hL + p*M (share of BC)"]
            + [(lambda rr, col=cc: f"=({_hL})+{col}${prow}*{_M}")
               for cc in _AXIS_COLS],
            styles=[S_BOLD] + [S_PCT] * len(_P_AXIS), outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[20] + [10] * len(_H_AXIS),
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


SENSITIVITY = _make()
