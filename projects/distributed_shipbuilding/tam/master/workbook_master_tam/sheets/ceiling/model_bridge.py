"""model_bridge - the "Conversion Bridge" tab (model group).

Resolves the hours != dollars problem. The Navy's ~50% is a LABOR-HOUR share;
the model is in dollars. The dollar outsourced share is:

    outsourced $ = h*L*BC + p*M*BC ,   M = 1 - L

i.e. the prime-yard labor that relocates (h*L) plus the pass-through material
that rides with outsourced packages (p*M). Three pass-through cases per class -
labor-only (p=0, ~h*L of BC), the active p from Assumptions, and material-
inclusive (p=1) - show why 50% of hours maps to ~25% of BC dollars labor-only
and rises toward the ceiling as outsourced packages carry their own material.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ceiling._layout import RowCursor
from workbook_master_tam.sheets.ceiling.inputs_assumptions import (
    core_h_cell, labor_share_cell, passthrough_cell,
)
from workbook_master_tam.sheets.ceiling.model_ceiling import bc_base_cell

_GROUP = "model"
_TAB = "Conversion Bridge"

NAMES = ["Virginia", "Columbia", "DDG-51"]
_CCOLS = ["C", "D", "E"]
_NCOLS = 5


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Hours-to-dollars bridge (outsourced share of BC)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(["Measure"] + NAMES + ["Portfolio"],
                  styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 4)
    bc, L, h, p, M, lo, act, hi, dol = (hdr + i for i in range(1, 10))
    _pp = passthrough_cell()

    c.write(["BC base (cumulative FY22-27, $M)"]
            + [f"={bc_base_cell(n)}" for n in NAMES] + [f"=SUM(C{bc}:E{bc})"],
            styles=[S_DEFAULT] + [S_LINK_NUM] * 3 + [S_NUM], outline_level=1)
    c.write(["L - shipyard labor share of BC"]
            + [f"={labor_share_cell(n)}" for n in NAMES] + [None],
            styles=[S_DEFAULT] + [S_LINK_PCT] * 3 + [S_DEFAULT], outline_level=1)
    c.write(["h - outsourceable labor-hour share"]
            + [f"={core_h_cell(n)}" for n in NAMES] + [None],
            styles=[S_DEFAULT] + [S_LINK_PCT] * 3 + [S_DEFAULT], outline_level=1)
    c.write(["p - pass-through material (active)", f"={_pp}", None, None, None],
            styles=[S_DEFAULT, S_LINK_PCT, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Material share M = 1 - L"]
            + [f"=1-{col}{L}" for col in _CCOLS] + [None],
            styles=[S_DEFAULT] + [S_PCT] * 3 + [S_DEFAULT], outline_level=1)
    c.write(["Outsourced share, labor-only (p=0) = h x L"]
            + [f"={col}{h}*{col}{L}" for col in _CCOLS]
            + [f"=IF(F{bc}=0,0,SUMPRODUCT(C{lo}:E{lo},C{bc}:E{bc})/F{bc})"],
            styles=[S_DEFAULT] + [S_PCT] * 4, outline_level=1)
    c.write(["Outsourced share, active p = hL + pM"]
            + [f"={col}{h}*{col}{L}+{_pp}*{col}{M}" for col in _CCOLS]
            + [f"=IF(F{bc}=0,0,F{dol}/F{bc})"],
            styles=[S_BOLD] + [S_PCT] * 4, outline_level=1)
    c.write(["Outsourced share, material-incl (p=1) = hL + M"]
            + [f"={col}{h}*{col}{L}+{col}{M}" for col in _CCOLS]
            + [f"=IF(F{bc}=0,0,SUMPRODUCT(C{hi}:E{hi},C{bc}:E{bc})/F{bc})"],
            styles=[S_DEFAULT] + [S_PCT] * 4, outline_level=1)
    c.write(["Outsourced $M (active p)"]
            + [f"={col}{act}*{col}{bc}" for col in _CCOLS]
            + [f"=SUM(C{dol}:E{dol})"],
            styles=[S_BOLD] + [S_NUM] * 4, outline_level=1)

    rows_at = dict(act=act, hi=hi)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[48, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render), rows_at


CONVERSION_BRIDGE, _R = _make()
_NAME_COL = {"Virginia": "C", "Columbia": "D", "DDG-51": "E", "Portfolio": "F"}


# active-p (selected p=0.5) and material-inclusive (p=1) outsourced-share cells,
# consumed by Summary (active case beside the ceiling) and Tie-Outs (p=1 == ceiling).
def active_share_cell(name): return f"'{_TAB}'!{_NAME_COL[name]}{_R['act']}"
def material_incl_share_cell(name): return f"'{_TAB}'!{_NAME_COL[name]}{_R['hi']}"
