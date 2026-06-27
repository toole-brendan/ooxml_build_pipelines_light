"""outfit_context - the "Outfit Context" tab (data group): SWBS subaward mix.

The HII-Ingalls first-tier subaward spend on the DDG-51 program, distributed by
ship system (SWBS major group), from the SAM award-classification workbook. It is
CONTEXT ONLY - it shows WHY machinery-dense blocks carry more cost (propulsion /
electric / auxiliary dominate purchased content; hull structure is built in-house),
but it is supplier spend, NOT a structural cost weight, and it does not feed the
module allocation.

Values are lifetime, constant FY2026 $M, captured from the SAM workbook's
"DDG SWBS by Ship-System" tab (recalculated 2026-06-25).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_BOLD, S_NOTE, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_NUM_INPUT, S_PCT, S_INT, S_INT_INPUT,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._tabs import TAB_OUTFIT_CONTEXT

_GROUP = "data"
_NCOLS = 4   # B = ship system, C = $M, D = %, E = records

# (SWBS major group, lifetime subaward $M [const FY2026], published records).
# Sorted high -> low so the machinery dominance reads off the page.
_SWBS = [
    ("500 Auxiliary Systems",                1105.6, 1082),
    ("200 Propulsion Plant",                 1093.6,  266),
    ("300 Electric Plant",                    895.8,  422),
    ("U00 No SWBS Evidence",                  684.4, 3708),
    ("600 Outfit & Furnishings",               72.6,  139),
    ("400 Command, Control & Surveillance",    56.3,   88),
    ("100 Hull Structure",                     28.1,  121),
    ("X00 Cross-Cutting",                      10.8,   36),
    ("L00 Legacy / Unmapped",                   8.4,   16),
    ("700 Armament",                            1.7,   13),
]


def _make():
    c = RowCursor(2)
    c.title(TAB_OUTFIT_CONTEXT, _NCOLS)
    c.caption("HII-Ingalls subaward spend by ship system (context only)")
    c.blank(2)

    c.section("§1 - DDG-51 subaward spend by ship system (SWBS), const FY2026 $M", _NCOLS)
    c.blank()
    c.write(["Ship system (SWBS major group)", "Subaward $M", "% of total", "Records"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    start = c.at()
    total_row = start + len(_SWBS)
    for group, dollars, recs in _SWBS:
        c.write([group, dollars, (lambda rr: f"=C{rr}/C{total_row}"), recs],
                styles=[S_BOLD, S_NUM_INPUT, S_PCT, S_INT_INPUT])
    c.total(
        ["All ship systems", f"=SUM(C{start}:C{total_row - 1})",
         f"=C{total_row}/C{total_row}", f"=SUM(E{start}:E{total_row - 1})"],
        styles=[S_BOLD, S_NUM, S_PCT, S_INT], n_cols=_NCOLS)
    c.blank()
    c.write(["Source: SAM award-classification workbook, \"DDG SWBS by Ship-System\" tab "
             "(first-tier HII-Ingalls subawards; recalculated 2026-06-25)."],
            styles=[S_NOTE])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[38, 14, 12, 11],
                       tab_color=group_color(_GROUP), with_gutter=True,
                       show_outline_symbols=False)
        return WorksheetSpec(ws)

    return SheetEntry(TAB_OUTFIT_CONTEXT, _GROUP, render)


OUTFIT_CONTEXT = _make()
