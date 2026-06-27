"""structural_hierarchy - the "Structural Hierarchy" tab (guide group).

HII's modular build hierarchy for the DDG-51, with the verbatim source quote, the
level ratios, and an explicit flag that the quote's "210 units" figure belongs to
the LPD (San Antonio-class), NOT the DDG. The live counts (4 / 21 / 72) are the
editable inputs on Assumptions; this tab links them and explains them.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NOTE, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_INT, S_LINK_INT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._italic import S_ITALIC
from workbook_ddg_module_cost.sheets._tabs import TAB_STRUCTURAL_HIER
from workbook_ddg_module_cost.sheets import assumptions as A

_GROUP = "guide"
_NCOLS = 3   # B = level/label, C = count/value, D = description/note

_QUOTE = [
    "Ingalls Shipbuilding uses modular construction techniques pioneered by the shipyard "
    "in the 1970s and refined over the years to maximize shipyard throughput.",
    "During the construction of a DDG 51 destroyer, 72 structural assemblies (units) are "
    "integrated, forming 21 grand blocks.",
    "These grand blocks are integrated, creating the ship's hull modules 1, 2 and 3.",
    "The deckhouse is landed (module 4), piping systems installed, cable routed, equipment "
    "connected and systems readied for test.",
    "The ship is moved to a drydock and launched in a 12-hour time period. Final outfitting "
    "and test is completed pier side.",
]


def _make():
    c = RowCursor(2)
    c.title(TAB_STRUCTURAL_HIER, _NCOLS)
    c.caption("HII (Ingalls) modular build hierarchy: ship -> modules -> grand blocks -> units")
    c.blank(2)

    # §1 the hierarchy ----------------------------------------------------------------
    c.section("§1 - The modular build hierarchy", _NCOLS)
    c.blank()
    c.write(["Level", "Count", "Description"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["Ship (per hull)", 1, "One complete DDG-51 (Arleigh Burke-class) hull."],
            styles=[S_BOLD, S_INT, S_DEFAULT])
    c.write(["Hull modules 1-3", 3,
             "Forward / midship / aft hull; each integrated from grand blocks."],
            styles=[S_DEFAULT, S_INT, S_DEFAULT])
    c.write(["Deckhouse (module 4)", 1, "Landed onto the hull after modules 1-3."],
            styles=[S_DEFAULT, S_INT, S_DEFAULT])
    c.write(["Modules (total)", f"={A.count_cell('modules')}",
             "Hull modules 1-3 + deckhouse (module 4)."],
            styles=[S_BOLD, S_LINK_INT, S_DEFAULT])
    c.write(["Grand blocks", f"={A.count_cell('blocks')}",
             "Integrated to create the hull modules."],
            styles=[S_BOLD, S_LINK_INT, S_DEFAULT])
    c.write(["Structural units (assemblies)", f"={A.count_cell('units')}",
             "Base assemblies: CAM-cut plate, bent pipe; extensively pre-outfitted."],
            styles=[S_BOLD, S_LINK_INT, S_DEFAULT])
    c.write(["Counts (4 / 21 / 72) are the editable inputs on the Assumptions tab."],
            styles=[S_NOTE])
    c.blank(2)

    # §2 ratios -----------------------------------------------------------------------
    c.section("§2 - Level ratios (live)", _NCOLS)
    c.blank()
    c.write(["Ratio", "Value", "Note"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["Units per grand block",
             f"={A.count_cell('units')}/{A.count_cell('blocks')}", "72 / 21"],
            styles=[S_DEFAULT, S_NUM, S_NOTE])
    c.write(["Grand blocks per module",
             f"={A.count_cell('blocks')}/{A.count_cell('modules')}", "21 / 4"],
            styles=[S_DEFAULT, S_NUM, S_NOTE])
    c.write(["Units per module",
             f"={A.count_cell('units')}/{A.count_cell('modules')}", "72 / 4"],
            styles=[S_DEFAULT, S_NUM, S_NOTE])
    c.blank(2)

    # §3 source quote -----------------------------------------------------------------
    c.section("§3 - HII source (verbatim)", _NCOLS)
    c.blank()
    for line in _QUOTE:
        c.write([line], styles=[S_ITALIC])
    c.write(["Source: HII / Ingalls Shipbuilding, Arleigh Burke-class capability page "
             "(web.archive.org capture 2026-04-02)."],
            styles=[S_NOTE])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[30, 11, 78],
                       tab_color=group_color(_GROUP), with_gutter=True,
                       show_outline_symbols=False)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_STRUCTURAL_HIER, _GROUP, render)


STRUCTURAL_HIERARCHY = _make()
