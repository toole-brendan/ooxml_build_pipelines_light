"""model_ceiling - the "Ceiling Model" tab (model group).

The structural ceiling, per class, as a share of Basic Construction:
    core    = L x (1 - h)     (irreducible prime-yard work: final assembly,
                               integration, reactor install, alignment, test)
    ceiling = 1 - core        (everything in principle outsourceable)
applied to the cumulative FY22-27 BC base. L and h link from Assumptions; BC
links from Cost Base. Every headline is a live formula; only the Assumptions
inputs are blue. Portfolio column rolls the three classes up by dollars.

Promotes core_pct_cell / ceiling_pct_cell / core_dollar_cell /
ceiling_dollar_cell / bc_base_cell (name in Virginia/Columbia/DDG-51/Portfolio),
consumed by Bridge, Headroom, Overview, Sensitivity and Tie-Outs.
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
    core_h_cell, labor_share_cell,
)
from workbook_outsourcing_ceiling.sheets.data_cost_base import bc_cumulative_cell

_GROUP = "model"
_TAB = "Ceiling Model"

NAMES = ["Virginia", "Columbia", "DDG-51"]
_CCOLS = ["C", "D", "E"]
_NAME_COL = {"Virginia": "C", "Columbia": "D", "DDG-51": "E", "Portfolio": "F"}
_NCOLS = 5   # Measure + 3 classes + Portfolio


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Outsourcing ceiling (share of Basic Construction)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(["Measure"] + NAMES + ["Portfolio"],
                  styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 4)
    bc, L, h, core, ceil, cdol, kdol = (hdr + i for i in range(1, 8))

    c.write(["BC base (cumulative FY22-27, $M)"]
            + [f"={bc_cumulative_cell(n)}" for n in NAMES]
            + [f"=SUM(C{bc}:E{bc})"],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 3 + [S_NUM], outline_level=1)
    c.write(["L - shipyard labor share of BC"]
            + [f"={labor_share_cell(n)}" for n in NAMES] + [None],
            styles=[S_DEFAULT] + [S_LINK_PCT] * 3 + [S_DEFAULT], outline_level=1)
    c.write(["h - outsourceable labor-hour share"]
            + [f"={core_h_cell(n)}" for n in NAMES] + [None],
            styles=[S_DEFAULT] + [S_LINK_PCT] * 3 + [S_DEFAULT], outline_level=1)
    c.write(["Core % = L x (1 - h)"]
            + [f"={col}{L}*(1-{col}{h})" for col in _CCOLS]
            + [f"=IF(F{bc}=0,0,F{cdol}/F{bc})"],
            styles=[S_BOLD] + [S_PCT] * 4, outline_level=1)
    c.write(["Ceiling % = 1 - core"]
            + [f"=1-{col}{core}" for col in _CCOLS] + [f"=1-F{core}"],
            styles=[S_BOLD] + [S_PCT] * 4, outline_level=1)
    c.write(["Core $M (never-outsourced)"]
            + [f"={col}{core}*{col}{bc}" for col in _CCOLS]
            + [f"=SUM(C{cdol}:E{cdol})"],
            styles=[S_DEFAULT] + [S_NUM] * 4, outline_level=1)
    c.write(["Ceiling $M (outsourceable)"]
            + [f"={col}{ceil}*{col}{bc}" for col in _CCOLS]
            + [f"=SUM(C{kdol}:E{kdol})"],
            styles=[S_BOLD] + [S_NUM] * 4, outline_level=1)

    rows_at = dict(bc=bc, core=core, ceil=ceil, cdol=cdol, kdol=kdol)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[40, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render), rows_at


CEILING_MODEL, _R = _make()


def _col(name: str) -> str:
    if name not in _NAME_COL:
        raise ValueError(f"unknown name {name!r}; expected one of {list(_NAME_COL)}")
    return _NAME_COL[name]


def bc_base_cell(name): return f"'{_TAB}'!{_col(name)}{_R['bc']}"
def bc_base_range(): return f"'{_TAB}'!C{_R['bc']}:E{_R['bc']}"   # 3-class BC row, for portfolio rollups
def core_pct_cell(name): return f"'{_TAB}'!{_col(name)}{_R['core']}"
def ceiling_pct_cell(name): return f"'{_TAB}'!{_col(name)}{_R['ceil']}"
def core_dollar_cell(name): return f"'{_TAB}'!{_col(name)}{_R['cdol']}"
def ceiling_dollar_cell(name): return f"'{_TAB}'!{_col(name)}{_R['kdol']}"
