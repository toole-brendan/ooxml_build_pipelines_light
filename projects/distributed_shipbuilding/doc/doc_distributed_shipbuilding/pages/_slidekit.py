"""Shared canvas drawing helpers for the distributed-shipbuilding slide mocks.

PRIVATE (underscore) module - NOT a page; pages/__init__.py never registers it.
The two slide-mock page modules (lane_evidence, priority_board) wireframe real
16:9 slides entirely in the DrawingML canvas layer (docx_core.wireframes canvas /
CanvasBox / CanvasLine). The generic, reusable pieces of that work live here so
both slides share one implementation; slide-specific composites (the method rail's
stage content, the program answer cards) stay in the page modules.

Helpers (all return lists of CanvasBox / CanvasLine in canvas inches, origin
top-left, mapping 1:1 into the slide region):
  stage_rail   - a row of labelled stage cards joined by thin arrows (method rail)
  stacked_hbar - 100% stacked horizontal bars with an "x of y" end label
  ranked_hbar  - single-series ranked horizontal bars, linear, per-bar color
  rule_table   - horizontal-rule table (no vertical grid), per-cell fills

Pure builders (the build never lints or scores them), exactly like
docx_core.wireframes itself.
"""
from __future__ import annotations

from docx_core.wireframes import CanvasBox, CanvasLine
from docx_core.style import BLACK, BLUE_5


# ---------------------------------------------------------------------------
# Method rail - a row of stage cards joined by arrows
# ---------------------------------------------------------------------------

def stage_rail(x0, y0, w, h, stages, *, gap=0.34, title_pt=11, sub_pt=8.5):
    """A horizontal method rail: N equal stage cards, each a filled sharp-rect with
    an ALL-CAPS title over italic sublines, joined left-to-right by thin black
    arrows. `stages` is a list of (title, [sublines], fill, text_color,
    border_pt) - so a caller controls the blue ramp and which card carries the one
    heavy border. Returns CanvasBox (cards + text) + CanvasLine (arrows)."""
    out = []
    n = len(stages)
    card_w = (w - gap * (n - 1)) / n
    for i, (title, subs, fill, tcol, border_pt) in enumerate(stages):
        cx = x0 + i * (card_w + gap)
        out.append(CanvasBox(cx, y0, card_w, h, fill=fill, line=BLACK,
                             line_pt=border_pt, name=title))
        out.append(CanvasBox(cx + 0.07, y0 + 0.07, card_w - 0.14, 0.30,
                             text=title, fill="none", line="none", align="left",
                             text_size_pt=title_pt, text_color=tcol))
        out.append(CanvasBox(cx + 0.07, y0 + 0.40, card_w - 0.14, h - 0.46,
                             text="\n".join(subs), fill="none", line="none",
                             align="left", text_size_pt=sub_pt, text_color=tcol))
        if i < n - 1:
            ay = y0 + h / 2
            out.append(CanvasLine(cx + card_w + 0.03, ay, gap - 0.06, 0.0,
                                  color=BLACK, line_pt=1.0, arrow=True))
    return out


# ---------------------------------------------------------------------------
# 100% stacked horizontal bars (coverage shares)
# ---------------------------------------------------------------------------

def stacked_hbar(x0, y0, w, rows, *, name_w=1.3, bar_h=0.30, gap=0.12,
                 max_bar=3.0, end_w=0.95, label_pt=9, seg_pt=9):
    """One 100%-stacked horizontal bar per row. `rows` is a list of (name,
    segments, end_label) where segments is [(value, fill, text_color), ...] - each
    segment width is value/total of the fixed max_bar, with its value printed
    inside. A right-aligned name label sits left of the bar and the absolute
    "x of y" end_label past its right end. Returns CanvasBox children."""
    out = []
    bx = x0 + name_w
    y = y0
    for name, segments, end_label in rows:
        total = sum(v for v, _f, _c in segments)
        out.append(CanvasBox(x0, y, name_w - 0.08, bar_h, text=name, fill="none",
                             line="none", align="right", text_size_pt=label_pt,
                             text_color=BLUE_5))
        cur = bx
        for value, fill, tcolor in segments:
            sw = (value / total) * max_bar
            out.append(CanvasBox(cur, y, sw, bar_h, text=str(value), fill=fill,
                                 line=BLACK, line_pt=0.75, text_color=tcolor,
                                 align="center", text_size_pt=seg_pt))
            cur += sw
        out.append(CanvasBox(cur + 0.08, y, end_w, bar_h, text=end_label,
                             fill="none", line="none", align="left",
                             text_size_pt=label_pt, text_color=BLACK))
        y += bar_h + gap
    return out


# ---------------------------------------------------------------------------
# Ranked horizontal bars (single series, linear, per-bar color)
# ---------------------------------------------------------------------------

def ranked_hbar(x0, y0, w, rows, *, name_w=3.6, bar_h=0.18, gap=0.06,
                max_bar=7.4, value_w=0.95, label_pt=8.5):
    """Single-series ranked horizontal bars, LINEAR scale (so dollar weight reads),
    one color per bar. `rows` is a list of (label, value, fill, value_label) in
    rank order; bar length is value/max scaled to max_bar, with the label left of
    the bar and value_label at its right end. Returns CanvasBox children."""
    out = []
    maxv = max(v for _l, v, _f, _vl in rows)
    bx = x0 + name_w
    y = y0
    for label, value, fill, value_label in rows:
        blen = max(0.15, (value / maxv) * max_bar)
        out.append(CanvasBox(x0, y, name_w - 0.08, bar_h, text=label, fill="none",
                             line="none", align="left", text_size_pt=label_pt,
                             text_color=BLUE_5))
        out.append(CanvasBox(bx, y, blen, bar_h, fill=fill, line=BLACK,
                             line_pt=0.75, name=label))
        out.append(CanvasBox(bx + blen + 0.06, y, value_w, bar_h, text=value_label,
                             fill="none", line="none", align="left",
                             text_size_pt=label_pt))
        y += bar_h + gap
    return out


# ---------------------------------------------------------------------------
# Horizontal-rule table (no vertical grid)
# ---------------------------------------------------------------------------

def _cell_props(cell, *, default_pt, default_color=BLACK):
    """Normalize a table cell - a plain str or {text,fill,color,align,pt} dict -
    to a (text, fill, color, align, pt) tuple."""
    if isinstance(cell, dict):
        return (cell.get("text", ""), cell.get("fill", "none"),
                cell.get("color", default_color), cell.get("align", "left"),
                cell.get("pt", default_pt))
    return (cell, "none", default_color, "left", default_pt)


def rule_table(x0, y0, w, headers, rows, col_w, *, header_h=0.30, row_h=0.40,
               body_pt=8.0, header_pt=9.0):
    """A table drawn purely in the canvas: horizontal rules only, no vertical grid.

    Each header / cell is a plain str or a {text,fill,color,align,pt} dict; pass
    the same fill across a row to band it. The header gets a 1.5pt rule beneath,
    every body row a 1pt rule. All cell fills are emitted first, then every rule,
    so the rules always read over the bands. col_w must sum to w. Returns
    CanvasBox (cells) + CanvasLine (rules)."""
    cells = []
    rules = []
    cx = x0
    for i, hcell in enumerate(headers):
        text, fill, _color, align, _pt = _cell_props(
            hcell, default_pt=header_pt, default_color=BLUE_5)
        cells.append(CanvasBox(cx, y0, col_w[i], header_h, text=text, fill=fill,
                               line="none", align=align, text_size_pt=header_pt,
                               text_color=BLUE_5))
        cx += col_w[i]
    yr = y0 + header_h
    rules.append(CanvasLine(x0, yr, w, 0.0, color=BLACK, line_pt=1.5,
                            arrow=False))
    y = yr
    for row in rows:
        cx = x0
        for i, cell in enumerate(row):
            text, fill, color, align, pt = _cell_props(cell, default_pt=body_pt)
            cells.append(CanvasBox(cx, y, col_w[i], row_h, text=text, fill=fill,
                                   line="none", align=align, text_size_pt=pt,
                                   text_color=color))
            cx += col_w[i]
        y += row_h
        rules.append(CanvasLine(x0, y, w, 0.0, color=BLACK, line_pt=1.0,
                                arrow=False))
    return cells + rules
