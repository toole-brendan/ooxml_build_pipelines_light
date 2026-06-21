"""data_cost_base - the "Cost Base" tab (data group, one native table).

The descriptive P-5c budget substrate the whole model rests on: one row per
(program, fiscal year) with a boat funded, FY22-27, unioned across the submarine
and DDG cost funnels by build_ceiling_base.py. The genuine budget lines (Basic
Construction, GFE, Total Ship Estimate) are blue leaf inputs; Plans+Other is the
live residual (Total - BC - GFE) and BC % is the live ratio, so every row ties
BC + GFE + Plans+Other = Total.

Promotes the load-bearing $ accessors the model tabs link to:
  bc_cumulative_cell / gfe_cumulative_cell / total_cumulative_cell /
  ffata_cumulative_cell  - a per-program SUMIF over the table body.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NUM, S_NUM_INPUT, S_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry, ExcelTable
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ceiling._bind import load_extracted_csv
from workbook_master_tam.sheets.ceiling._layout import RowCursor
from workbook_master_tam.sheets.ceiling._widths import header_styles

_GROUP = "data"
_TAB = "Cost Base"

PROGRAMS = ["Virginia", "Columbia", "DDG-51"]

_HEADERS = ["Program", "FY", "BC", "GFE", "Total", "Plans+Other", "BC %", "FFATA"]
# Content columns B..I (0-indexed): B=1 Program, C=2 FY, D=3 BC, E=4 GFE,
# F=5 Total, G=6 Plans+Other, H=7 BC %, I=8 FFATA.
_COL = {h: col_letter(1 + i) for i, h in enumerate(_HEADERS)}   # "BC" -> "D", etc.
_NCOLS = len(_HEADERS)


def _make_cost_base():
    headers, rows = load_extracted_csv("wb_cost_base")
    ix = {h: i for i, h in enumerate(headers)}

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - P-5c cost base ($M then-year, FY22-27)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, {"FY"}))

    first = last = None
    for row in rows:
        prog = row[ix["program"]]
        fy = row[ix["fy"]]
        bc = row[ix["bc_$M"]]
        gfe = row[ix["gfe_$M"]]
        total = row[ix["total_ship_$M"]]
        ffata = row[ix["ffata_visible_$M"]]
        r = c.write(
            [prog, fy, bc, gfe, total,
             lambda rr: f"=F{rr}-D{rr}-E{rr}",            # Plans+Other = Total-BC-GFE
             lambda rr: f"=IF(F{rr}=0,0,D{rr}/F{rr})",    # BC %
             ffata],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_NUM_INPUT, S_NUM_INPUT,
                    S_NUM, S_PCT, S_NUM_INPUT], outline_level=1)
        first = first if first is not None else r
        last = r

    # Filter-aware Totals Row, one row BELOW the table ref (outside it).
    def _sub(letter):
        return f"=SUBTOTAL(109,{letter}{first}:{letter}{last})"
    c.total(
        ["Portfolio (FY22-27)", "", _sub("D"), _sub("E"), _sub("F"),
         _sub("G"), lambda rr: f"=IF(F{rr}=0,0,D{rr}/F{rr})", _sub("I")],
        styles=[S_BOLD, S_DEFAULT, S_NUM, S_NUM, S_NUM, S_NUM, S_PCT, S_NUM],
        n_cols=_NCOLS)

    table = ExcelTable(name="CostBase", ref=f"B{hdr}:{_COL['FFATA']}{last}",
                       headers=_HEADERS)

    # ---- accessors (per-program SUMIF over the table body; return fragments) ----
    def _cum(letter, program):
        b = _COL["Program"]
        return (f'SUMIF(\'{_TAB}\'!${b}${first}:${b}${last},"{program}",'
                f'\'{_TAB}\'!${letter}${first}:${letter}${last})')

    def bc_cumulative_cell(program): return _cum(_COL["BC"], program)
    def gfe_cumulative_cell(program): return _cum(_COL["GFE"], program)
    def total_cumulative_cell(program): return _cum(_COL["Total"], program)
    def ffata_cumulative_cell(program): return _cum(_COL["FFATA"], program)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[11, 7, 11, 11, 12, 13, 10, 11],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=[table])

    acc = dict(bc_cumulative_cell=bc_cumulative_cell,
               gfe_cumulative_cell=gfe_cumulative_cell,
               total_cumulative_cell=total_cumulative_cell,
               ffata_cumulative_cell=ffata_cumulative_cell)
    return SheetEntry(_TAB, _GROUP, render), acc


COST_BASE, _ACC = _make_cost_base()
bc_cumulative_cell = _ACC["bc_cumulative_cell"]
gfe_cumulative_cell = _ACC["gfe_cumulative_cell"]
total_cumulative_cell = _ACC["total_cumulative_cell"]
ffata_cumulative_cell = _ACC["ffata_cumulative_cell"]
