"""validation_tie_outs - the "Tie-Outs" tab (validation group, hidden).

The reconciliation oracle: the model's identities and sanity bounds, per class,
each an OK/FAIL formula that links the producing cells (so a check can't pass
while the calc is broken). Identities: core $ + ceiling $ = BC $, and
core % + ceiling % = 1. Sanity: ceiling % >= current POP %, and ceiling $ >=
the observed FFATA-visible floor.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ceiling._layout import RowCursor
from workbook_master_tam.sheets.ceiling.inputs_assumptions import pop_current_cell, pop_range
from workbook_master_tam.sheets.ceiling.model_ceiling import (
    bc_base_cell, bc_base_range, core_pct_cell, ceiling_pct_cell,
    core_dollar_cell, ceiling_dollar_cell,
)
from workbook_master_tam.sheets.ceiling.model_bridge import material_incl_share_cell
from workbook_master_tam.sheets.ceiling.data_cost_base import ffata_cumulative_cell

_GROUP = "validation"
_TAB = "Tie-Outs"
CLASSES = ["Virginia", "Columbia", "DDG-51"]
NAMES = CLASSES + ["Portfolio"]
_NCOLS = 1 + len(NAMES)


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Identity + sanity checks", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check"] + NAMES, styles=[S_HEADER_LEFT] * _NCOLS)

    first = last = None

    def row(label, f):
        nonlocal first, last
        r = c.write([label] + [f(n) for n in NAMES],
                    styles=[S_DEFAULT] * _NCOLS, outline_level=1)
        first = first if first is not None else r
        last = r

    row("Core $ + Ceiling $ = BC $",
        lambda n: f'=IF(ABS(({core_dollar_cell(n)}+{ceiling_dollar_cell(n)})'
                  f'-{bc_base_cell(n)})<0.5,"OK","FAIL")')
    row("Core % + Ceiling % = 1",
        lambda n: f'=IF(ABS(({core_pct_cell(n)}+{ceiling_pct_cell(n)})-1)'
                  f'<0.001,"OK","FAIL")')
    def _pop_floor(n):
        # Portfolio POP% is dollar-weighted (SUMPRODUCT of per-class POP x BC over
        # total BC); per class it is the announced input.
        pop = (f"SUMPRODUCT({pop_range()},{bc_base_range()})/{bc_base_cell('Portfolio')}"
               if n == "Portfolio" else pop_current_cell(n))
        return f'=IF({ceiling_pct_cell(n)}>=({pop}),"OK","FAIL")'
    row("Ceiling % >= current POP %", _pop_floor)

    def _ffata_floor(n):
        ff = ("+".join(ffata_cumulative_cell(p) for p in CLASSES)
              if n == "Portfolio" else ffata_cumulative_cell(n))
        return f'=IF({ceiling_dollar_cell(n)}>=({ff}),"OK","FAIL")'
    row("Ceiling $ >= FFATA-visible $ (floor)", _ffata_floor)
    row("Ceiling % = Bridge p=1 case",
        lambda n: f'=IF(ABS({ceiling_pct_cell(n)}-{material_incl_share_cell(n)})'
                  f'<0.001,"OK","FAIL")')
    c.blank()
    c.write(["All-OK gate"]
            + [f'=IF(COUNTIF({col}{first}:{col}{last},"FAIL")=0,"OK","FAIL")'
               for col in ("C", "D", "E", "F")],
            styles=[S_BOLD] + [S_DEFAULT] * len(NAMES))

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[40, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render, hidden=True)


TIE_OUTS = _make()
