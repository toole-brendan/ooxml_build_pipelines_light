"""model_headroom - the "Headroom" tab (model group).

The POP-lead comparison: how far today's outsourcing sits below the structural
ceiling, per class. Current off-team work (announced POP) -> ceiling -> headroom
multiple. The FFATA-visible subaward total is the observed hard floor; the
make/buy mid band is shown as a reference footnote (it overstates contestable
headroom because much bought-out material is sole-source-locked). Portfolio
column rolls up by dollars.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_outsourcing_ceiling.sheets._layout import RowCursor
from workbook_outsourcing_ceiling.sheets.inputs_assumptions import (
    pop_current_cell, makebuy_cell,
)
from workbook_outsourcing_ceiling.sheets.model_ceiling import (
    bc_base_cell, ceiling_pct_cell, ceiling_dollar_cell,
)
from workbook_outsourcing_ceiling.sheets.data_cost_base import ffata_cumulative_cell

_GROUP = "model"
_TAB = "Headroom"

NAMES = ["Virginia", "Columbia", "DDG-51"]
_CCOLS = ["C", "D", "E"]
_NCOLS = 5


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Headroom over current outsourcing (POP frame; $M, x)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(["Measure"] + NAMES + ["Portfolio"],
                  styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 4)
    bc, cur, ceil, hr, curd, ceild, ffat, mb = (hdr + i for i in range(1, 9))

    c.write(["BC base (cumulative FY22-27, $M)"]
            + [f"={bc_base_cell(n)}" for n in NAMES] + [f"=SUM(C{bc}:E{bc})"],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 3 + [S_NUM], outline_level=1)
    c.write(["Current off-team work (POP)"]
            + [f"={pop_current_cell(n)}" for n in NAMES]
            + [f"=IF(F{bc}=0,0,F{curd}/F{bc})"],
            styles=[S_DEFAULT] + [S_LINK_PCT] * 3 + [S_PCT], outline_level=1)
    c.write(["Ceiling %"]
            + [f"={ceiling_pct_cell(n)}" for n in NAMES]
            + [f"=IF(F{bc}=0,0,F{ceild}/F{bc})"],
            styles=[S_DEFAULT] + [S_LINK_PCT] * 3 + [S_PCT], outline_level=1)
    c.write(["Headroom x = ceiling / current"]
            + [f"=IF({col}{cur}=0,0,{col}{ceil}/{col}{cur})" for col in _CCOLS]
            + [f"=IF(F{cur}=0,0,F{ceil}/F{cur})"],
            styles=[S_BOLD] + [S_NUM] * 4, outline_level=1)
    c.write(["Current outsourced $M = POP x BC"]
            + [f"={col}{cur}*{col}{bc}" for col in _CCOLS]
            + [f"=SUM(C{curd}:E{curd})"],
            styles=[S_DEFAULT] + [S_NUM] * 4, outline_level=1)
    c.write(["Ceiling $M (outsourceable)"]
            + [f"={ceiling_dollar_cell(n)}" for n in NAMES]
            + [f"=SUM(C{ceild}:E{ceild})"],
            styles=[S_BOLD] + [S_LINK_NUM] * 3 + [S_NUM], outline_level=1)
    c.write(["FFATA-visible subawards $M (observed floor)"]
            + [f"={ffata_cumulative_cell(n)}" for n in NAMES]
            + [f"=SUM(C{ffat}:E{ffat})"],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 3 + [S_NUM], outline_level=1)
    c.write(["Make/buy reference $M (mid band, footnote)"]
            + [f"={makebuy_cell('mid')}*{col}{bc}" for col in _CCOLS]
            + [f"=SUM(C{mb}:E{mb})"],
            styles=[S_DEFAULT] + [S_NUM] * 4, outline_level=1)

    rows_at = dict(cur=cur, ceil=ceil, hr=hr)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render), rows_at


HEADROOM, _R = _make()
_NAME_COL = {"Virginia": "C", "Columbia": "D", "DDG-51": "E", "Portfolio": "F"}


def headroom_mult_cell(name): return f"'{_TAB}'!{_NAME_COL[name]}{_R['hr']}"
