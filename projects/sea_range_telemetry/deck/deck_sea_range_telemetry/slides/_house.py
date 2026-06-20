"""Shared slide helper: an honest-height native table for the alternative_v1
methodology slides (s05-s08).

Why this exists: deck_core.house_table renders its cells at 115% line spacing, so
its real rendered height runs ~15% taller than text_metrics.estimate_row_heights
predicts (see memory: house_table row-height gotcha). These methodology pages pack
a table into a tightly budgeted zone with a caveat / guardrail strip directly
below, so an under-estimated frame height would let the table grow into the strip.

dark_table() rebuilds the house posture on the low-level table() engine with cells
pinned to 100% line spacing, so sum(row_h) from estimate_row_heights matches the
render exactly. It keeps the house table contract: a dark BLUE_5 header with white
all-caps text, bold first column, cascading horizontal rules only (1.5pt under the
header, 1pt under each body row but the last), and palette cell fills.

This is NOT a slide module — it carries no render(); the registry never imports it.
The slide modules import dark_table from it.
"""
from __future__ import annotations

from deck_core.primitives import table, trow, tcell_rich, trun
from deck_core.style import BLUE_5, WHITE, BLACK, FONT


def _cell(text, *, align, fill, bold, size, color, borders):
    """One table cell at 100% line spacing (honest height vs estimate_row_heights)."""
    return tcell_rich(
        [{"align": align,
          "runs": [trun(text, size=size, bold=bold, color=color, font=FONT)],
          "line_spacing": 100_000}],
        fill=fill, anchor="ctr", borders=borders)


def dark_table(sp_id, name, x, y, col_w, rows, row_h, *, aligns,
               size=800, header_size=850, cell_fills=None, cell_bold=None,
               cell_color=None):
    """Honest-height native table with the house dark-header posture.

    rows[0] is the header (BLUE_5 fill, white all-caps). Body rows get a bold first
    column; pass cell_bold / cell_color / cell_fills as {(row, col): value} for
    per-cell overrides (e.g. bold value columns, shaded total rows). row_h is the
    per-row EMU list from estimate_row_heights(...); the frame cy = sum(row_h)
    matches the render because every cell is pinned to 100% line spacing.
    """
    cell_fills = cell_fills or {}
    cell_bold = cell_bold or {}
    cell_color = cell_color or {}
    ncol = len(col_w)
    n = len(rows)

    header_borders = {"B": {"color": BLACK, "width": 19_050}}
    built = [trow([
        _cell(rows[0][c].upper(), align=aligns[c], fill=BLUE_5, bold=True,
              size=header_size, color=WHITE, borders=header_borders)
        for c in range(ncol)
    ], h=row_h[0])]

    for ri in range(1, n):
        last = ri == n - 1
        bb = {"B": "none"} if last else {"B": {"color": BLACK, "width": 12_700}}
        cells = [
            _cell(rows[ri][ci], align=aligns[ci], fill=cell_fills.get((ri, ci)),
                  bold=(ci == 0 or cell_bold.get((ri, ci), False)),
                  size=size, color=cell_color.get((ri, ci), BLACK), borders=bb)
            for ci in range(ncol)
        ]
        built.append(trow(cells, h=row_h[ri]))

    return table(sp_id, name, x, y, sum(col_w), sum(row_h),
                 col_widths=col_w, rows=built)
