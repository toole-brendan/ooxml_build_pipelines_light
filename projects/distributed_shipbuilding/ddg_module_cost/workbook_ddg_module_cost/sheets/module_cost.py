"""module_cost - the "Module Cost" answer tab (summary group).

The headline: the per-ship Basic-Construction anchor (from Assumptions) divided
down HII's modular build hierarchy.

  §1 Even split        - ship cost / count at each level (ship -> module -> grand
                         block -> unit). The honest first-order average.
  §2 Module breakout   - the 4 modules carry the per-ship cost in proportion to
                         their relative weights (Assumptions §3); equal weights
                         reduce this to the even split, and the column ties back
                         to the per-ship Basic Construction.
  §3 Sensitivity       - the FY2027 single-ship buy (a higher per-ship rate) as a
                         reference band against the FY2025 multi-ship headline.

Every figure is a live formula into Assumptions / Ship Cost Basis - no hardcoded
results.

Promoted accessor:
  alloc_total_cell()  -> the summed module-breakout cell (Checks ties it to the
                         per-ship Basic Construction numerator)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NOTE, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_INT, S_LINK_NUM, S_LINK_INT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._tabs import TAB_MODULE_COST
from workbook_ddg_module_cost.sheets import assumptions as A
from workbook_ddg_module_cost.sheets.ship_cost_basis import per_ship_bc_cell

_GROUP = "summary"
_NCOLS = 3   # content columns (gutter mode): B = label, C = count/weight, D = $M


def _make():
    num = A.numerator_cell()
    P: dict = {}
    c = RowCursor(2)
    c.title(TAB_MODULE_COST, _NCOLS)
    c.caption("Per-ship Basic Construction allocated down the HII modular build hierarchy")
    c.blank(2)

    # §1 Even split -------------------------------------------------------------------
    c.section("§1 - Cost per structural level (even split, const FY2026 $M)", _NCOLS)
    c.blank()
    c.write(["Level", "Count", "Avg per item ($M)"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    P["ship"] = c.write(["Ship (per hull)", 1, f"={num}"],
                        styles=[S_BOLD, S_INT, S_LINK_NUM])
    P["module"] = c.write(
        ["Hull module", f"={A.count_cell('modules')}",
         f"={num}/{A.count_cell('modules')}"],
        styles=[S_DEFAULT, S_LINK_INT, S_NUM])
    P["block"] = c.write(
        ["Grand block", f"={A.count_cell('blocks')}",
         f"={num}/{A.count_cell('blocks')}"],
        styles=[S_DEFAULT, S_LINK_INT, S_NUM])
    P["unit"] = c.write(
        ["Structural unit", f"={A.count_cell('units')}",
         f"={num}/{A.count_cell('units')}"],
        styles=[S_DEFAULT, S_LINK_INT, S_NUM])
    c.blank(2)

    # §2 Module breakout (weighted) ---------------------------------------------------
    c.section("§2 - Module breakout (weighted, const FY2026 $M)", _NCOLS)
    c.blank()
    c.write(["Module", "Relative weight", "Allocated ($M)"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    wtot = A.weight_total_cell()
    alloc_rows: list[int] = []
    for label, wcell in A.weight_cells():
        r = c.write([label, f"={wcell}", f"={num}*{wcell}/{wtot}"],
                    styles=[S_DEFAULT, S_LINK_NUM, S_NUM])
        alloc_rows.append(r)
    a0, a1 = alloc_rows[0], alloc_rows[-1]
    P["alloc_total"] = c.total(
        ["All modules", f"={wtot}", f"=SUM(D{a0}:D{a1})"],
        styles=[S_BOLD, S_LINK_NUM, S_NUM], n_cols=_NCOLS)
    c.write(["Allocated total ties to per-ship Basic Construction; equal weights "
             "reduce this to the even split (/4)."],
            styles=[S_NOTE])
    c.blank(2)

    # §3 Sensitivity: single-ship FY2027 ---------------------------------------------
    c.section("§3 - Sensitivity: FY2027 single-ship buy", _NCOLS)
    c.blank()
    c.write(["Line", "Count", "Value ($M)"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    c.write(["Per-ship Basic Construction, FY2027 (1-ship)", None,
             f"={per_ship_bc_cell(2027)}"],
            styles=[S_DEFAULT, S_DEFAULT, S_LINK_NUM])
    c.write(["  per structural unit (/72)", f"={A.count_cell('units')}",
             f"={per_ship_bc_cell(2027)}/{A.count_cell('units')}"],
            styles=[S_DEFAULT, S_LINK_INT, S_NUM])
    c.write(["Single-ship buys carry rate + nonrecurring loading; the FY2025 "
             "multi-ship rate is the headline."],
            styles=[S_NOTE])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[42, 15, 16],
                       tab_color=group_color(_GROUP), with_gutter=True,
                       show_outline_symbols=False)
        return WorksheetSpec(ws)

    def alloc_total_cell() -> str:
        return f"'{TAB_MODULE_COST}'!D{P['alloc_total']}"

    return SheetEntry(TAB_MODULE_COST, _GROUP, render), alloc_total_cell


(MODULE_COST, alloc_total_cell) = _make()
