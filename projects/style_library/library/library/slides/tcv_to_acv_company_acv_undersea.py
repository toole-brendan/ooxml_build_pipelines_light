"""tcv_to_acv_company_acv_undersea — Market sizing Navy (Undersea) deck (20251201), source slide 25.

EXHIBIT — "TCV to ACV Approach · Finding Company ACV": the Navy (Undersea) sibling
of tcv_to_acv_company_acv — same template, Undersea numbers. It shows how Company
TCV converts to Company ACV (annual contract value) via contract-exercise timing.
Top band states the formula — Company TCV ($) × Contract exercise timing (%) =
Company ACV by year ($). The middle is a worked $-example drawn as a styled bar
chart with $-value badges on the bars ($200 … $15) and an output reading
"Company ACV: $85M in Year 1", then $15M / $0M / $0M / $0M for Years 2–5. The
bottom is a native table of per-product exercise timing (Corsair kits / Mirage
kits / Mirage COCO / TREX / LCUE × Initial / In-year / Years 2–5 exercise).

This module exercises all three "hard" converter paths at once: a data-over-
template styled_chart, a native table() reconstruction, and a flattened group.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder()
  • approach steps .... Rectangle 2/7 + Straight Connector 8 (left header block)
  • formula band ...... Rectangle 13/15/16 + "+"/"=" glyphs (Company TCV × timing = ACV)
                        + the dashed bar-to-bar arrows
  • styled chart ...... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the data
                        is the _CHART0_DATA literal, the look is the source template
  • $ badges .......... "Text Placeholder 25" boxes = the $ values on the bars
  • _CATEGORY_TICK_LABELS  manual category-axis labels beneath the chart
  • _DATA_LABELS ......... the three Year 3–5 data labels on the bars
  • ACV cards ......... Rectangle 242/248/80/81/82 = Company ACV by year ($85M … $0M)
  • table ............. per-product exercise-timing table (low-level table/trow/tcell)
  • scope chip ........ "All archetypes" (top-right) + logo + footnote

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=25, connector=9, chart=1, table=1, picture=1,
chrome_builders=2, clusters=2 (covering 12 shapes), frozen_fields=18,
dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, line_break, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_4, BLUE_5, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide25_chart5.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide25_chart5.xlsb").read_bytes()

# data-over-template: these values drive the chart render; the style is the template.
_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [200, 100, 100, 50, 15, 15, 0, 0, 0]},
        {"values": [None, 100, None, 50, 35, None, None, None, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]
IMAGES = [
    {"rId": "rId3", "file": "image6_3071a231.jpeg"},
]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──
PAD = dict(l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960)   # the source's heavier cell padding


def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...).
    Pass **PAD for the source's 60960 padding; omit for the 45720 default."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...).
    Pass **PAD for the source's 60960 padding; omit for the 45720 default. Keeps source tpara()/trun() verbatim."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_H = IN(4.634), IN(0.167)                 # chart column-label row
_VALBADGE_Y, _VALBADGE_W, _VALBADGE_H = IN(4.42), IN(0.115), IN(0.167)  # "0" value badge
_ARROW_W = IN(0.616)   # dashed connector arrow length          [shared x4]
_BADGE_H = IN(0.167)   # $-value badge height                    [shared x6]
_OP_W = IN(0.4)        # "+"/"=" operator-glyph size             [shared x4]
_CARD_Y = IN(2.98)     # Company-ACV-by-year card row y          [shared x5]
_CARD_H = IN(0.385)    # Company-ACV-by-year card height         [shared x5]
_CARD_W = IN(1.218)    # Company-ACV-by-year card width          [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the nine category-axis labels beneath the chart bars.
_CATEGORY_TICK_LABELS = [    # (x, cx, label) x9 — manual category-axis labels beneath the chart bars
    (1.031, 0.314, "SAM"),
    (2.153, 0.844, "Market Share"),
    (3.502, 0.922, "Company TCV"),
    (4.905, 0.891, "Initial exercise"),
    (6.238, 0.998, "In-year exercise"),
    (7.635, 0.974, "Year 2 exercise"),
    (9.023, 0.974, "Year 3 exercise"),
    (10.41, 0.974, "Year 4 exercise"),
    (11.797, 0.974, "Year 5 exercise"),
]

# local_meaning: the Year 3-5 ACV value labels (the '0' badges) riding the bars.
_DATA_LABELS = [    # (x) x3 — Year 3–5 ACV data labels riding the bars
    9.451,
    10.839,
    12.226,
]
# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level layout convention is expressed by repeating the
# same l_ins/r_ins/t_ins/b_ins, anchor, and alignment across the affected cells.
# In tcell()/tcell_rich(), those insets are internal padding and anchor is vertical
# alignment; tcell align or tpara align/mar_l/indent controls horizontal alignment
# and paragraph margins (including hanging bullet indents).

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Explicit zero/tight insets and wrap="none"
# are alignment devices for chart/exhibit labels; omitted values retain the
# primitive defaults intentionally.


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Navy (Undersea)"))
    out.append(title_placeholder("TCV to ACV Approach", "Finding Company ACV"))
    # ── approach-steps header (left) ──
    out.append(text_box(n(), "Rectangle 2", IN(0.425), IN(1.589), IN(2.289), IN(0.701), [paragraph([run("Multiply Company TCV by contract exercise timing to find Company ACV", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 7", IN(0.425), IN(1.229), IN(2.291), IN(0.359), [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Straight Connector 8", IN(0.426), IN(1.586), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))   # 162029 dark navy
    # ── formula band: Company ACV output box, then the dashed bar-to-bar arrows ──
    out.append(text_box(n(), "Rectangle 13", IN(11.46), IN(1.76), IN(1.519), IN(0.359), [paragraph([run("Company ACV by year ($)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color=BLACK, line_width=3175, anchor="ctr"))   # 263746 navy
    out.append(connector(n(), "Straight Connector 118", IN(1.573), IN(2.974), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 132", IN(2.96), IN(3.74), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 139", IN(4.347), IN(3.74), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 41", IN(5.734), IN(4.122), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))   # 162029 dark navy
    out.append(connector(n(), "Straight Connector 153", IN(7.122), IN(4.389), IN(0.615), IN(0), color=DK, width=3175, dashed=True, arrow=True))   # 162029 dark navy
    # ── worked example: styled chart (data-over-template) + $ badges on the bars ──
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.405), y=IN(2.884), cx=IN(12.663), cy=IN(1.71), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.016), IN(3.655), IN(0.344), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("200", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    # ── category-axis labels beneath the chart ──
    # No-wrap, zero insets, centered paragraph alignment, and zero paragraph
    # margins keep each label registered to its plotted category.
    for _x, _cx, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _AXIS_Y, IN(_cx), _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── more $ badges (interleaved with the formula band / ACV cards in paint order) ──
    out.append(text_box(n(), "Text Placeholder 25", IN(2.403), IN(3.273), IN(0.344), _BADGE_H, [paragraph([run("$", size=PT(10), color=BLACK, font=FONT), run("100", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(3.79), IN(4.038), IN(0.344), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("100", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    out.append(text_box(n(), "Text Placeholder 25", IN(5.215), IN(3.847), IN(0.267), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("50", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    out.append(text_box(n(), "Text Placeholder 25", IN(6.602), IN(4.172), IN(0.267), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("35", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # FFFFFF white
    out.append(text_box(n(), "Text Placeholder 25", IN(7.988), IN(4.363), IN(0.267), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("15", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 263746 navy
    # ── Year 3–5 data labels on the bars ──
    # Tight side insets and centered anchoring keep the zero labels within
    # their very narrow source-fit boxes.
    for _x in _DATA_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), _VALBADGE_Y, _VALBADGE_W, _VALBADGE_H, [paragraph([run("0", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 263746 navy
    # ── formula band (cont.): Company TCV × timing = ... ──
    out.append(text_box(n(), "Plus Sign 14", IN(6.575), IN(1.739), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))   # 000000 black
    # ── per-product exercise-timing table ──
    # col_widths fixes product/timing columns and trow(h=...) their row minima.
    # Repeated 60960 insets and anchors encode row/column padding and vertical
    # alignment; tpara align/mar_l/indent controls horizontal text margins.
    # palette — text: FFFFFF white (Year headers) · 000000 black (caption + body);
    #   fills: 263746 navy (Year 1–5 headers); rules: 162029 dark navy + FFFFFF white (banner) · 808080 gray (inner).
    out.append(table(n(), "Table 19", IN(0.495), IN(4.903), IN(12.482), IN(2.1), col_widths=[IN(1.283), IN(2.993), IN(1.368), IN(1.368), IN(1.368), IN(1.368), IN(1.368), IN(1.368)], rows=[
        # ── banner: caption (spans Product+Rationale) | Year 1 (spans 2) | Year 2..5 ──
        trow([
            rcell([tpara([trun("Contract exercise timing by product:", size=PT(10), italic=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], span=2, anchor="b", **PAD, B=edge(WHITE)),
            cell("Year 1", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, span=2, anchor="b", **PAD, R=edge(WHITE), B=edge(DK)),
            cell("Year 2", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(DK)),
            cell("Year 3", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(DK)),
            cell("Year 4", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), R=edge(WHITE), B=edge(DK)),
            cell("Year 5", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", **PAD, L=edge(WHITE), B=edge(DK)),
        ], h=IN(0.3)),
        # ── column headers (Product cell keeps the default 45720 inset) ──
        trow([
            cell("Product", size=PT(10), bold=True, color=BLACK, anchor="b", T=edge(WHITE), B=edge(DK)),
            cell("Rationale", size=PT(10), bold=True, color=BLACK, anchor="b", **PAD, T=edge(WHITE), B=edge(DK)),
            cell("Initial exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("In-Year exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 2 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 3 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 4 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
            cell("Year 5 exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", **PAD, T=edge(DK), B=edge(DK)),
        ], h=IN(0.3)),
        # ── Corsair kits (top rule DK; section rules 808080) ──
        trow([
            cell("Corsair kits", size=PT(10), bold=True, color=BLACK, **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("First tranche / subsequent (in line w/ OT)", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("100% / 50%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("0% / 35%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("0% / 15%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge(DK), B=edge("808080")),
        ], h=IN(0.3)),
        # ── Mirage kits ──
        trow([
            cell("Mirage kits", size=PT(10), bold=True, color=BLACK, **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("In line with Surface Navy Mirage timing", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("50%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("35%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("15%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
        ], h=IN(0.3)),
        # ── Mirage COCO ──
        trow([
            cell("Mirage COCO", size=PT(10), bold=True, color=BLACK, **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("Quarter-long operations", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("100%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
        ], h=IN(0.3)),
        # ── TREX ──
        trow([
            cell("TREX", size=PT(10), bold=True, color=BLACK, **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("Expecting all CLINs exercised up front", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("100%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge("808080")),
        ], h=IN(0.3)),
        # ── LCUE (bottom rule WHITE) ──
        trow([
            cell("LCUE", size=PT(10), bold=True, color=BLACK, **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("Expecting all CLINs exercised up front", size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("100%", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
            rcell([tpara([trun("- -", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], **PAD, T=edge("808080"), B=edge(WHITE)),
        ], h=IN(0.3)),
    ]))
    # ── formula band (cont.) + ACV cards (Year 1/Year 2) — interleaved in paint order ──
    out.append(text_box(n(), "Rectangle 15", IN(3.515), IN(1.76), IN(2.549), IN(0.359), [paragraph([run("Company TCV ($)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_4, line_color=BLACK, line_width=3175, anchor="ctr"))   # 3D5972 dark blue
    out.append(text_box(n(), "Equals 17", IN(10.548), IN(1.739), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 242", IN(4.964), _CARD_Y, IN(2.158), _CARD_H, [paragraph([run("Company ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$85M in Year 1", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))   # 263746 navy
    out.append(text_box(n(), "Rectangle 248", IN(7.519), _CARD_Y, _CARD_W, _CARD_H, [paragraph([run("Year 2 ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$15M", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))   # 263746 navy
    out.append(connector(n(), "Straight Arrow Connector 249", IN(0.495), IN(2.611), IN(12.339), IN(0.002), color="808080", width=12700))   # 808080 gray
    out.append(text_box(n(), "Rectangle 16", IN(7.456), IN(1.76), IN(2.548), IN(0.359), [paragraph([run("Contract exercise timing (%)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=DK, line_color=DK, anchor="ctr"))   # 162029 dark navy
    out.append(text_box(n(), "TextBox 252", IN(6.427), IN(2.125), IN(4.607), IN(0.426), [paragraph([run("Defined as proportion of contract exercised each year ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., 85% in Year 1, 15% in Year 2 for Corsair) ", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 254", IN(0.425), IN(2.253), IN(3.922), IN(0.359), [paragraph([run("Company ACV estimation example ($M):", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 247", IN(6.063), IN(3.524), IN(6.914), IN(1.32), [paragraph([run("For Programs to deliver", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="808080", line_width=19050, dashed_line=True))   # 808080 gray outline
    # ── Year 1 / Subsequent-years timeline arrows + labels ──
    out.append(connector(n(), "Straight Arrow Connector 301", IN(0.54), IN(2.816), IN(6.582), IN(0), color=DK, width=12700, arrow=True))   # 162029 dark navy
    out.append(text_box(n(), "Rectangle 302", IN(3.516), IN(2.701), IN(0.747), IN(0.229), [paragraph([run("Year 1", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    out.append(connector(n(), "Straight Arrow Connector 304", IN(7.519), IN(2.816), IN(5.373), IN(0), color=DK, width=12700, arrow=True))   # 162029 dark navy
    out.append(text_box(n(), "Rectangle 305", IN(9.096), IN(2.701), IN(2.316), IN(0.229), [paragraph([run("Subsequent years", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    # ── scope chip (top-right) + Year 3–5 ACV cards (all $0M) — interleaved in paint order ──
    out.append(text_box(n(), "Rectangle 18", IN(9.121), IN(0.074), IN(2.663), IN(0.5), [paragraph([run("All archetypes", size=PT(12), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=DK, line_width=3175, anchor="ctr"))   # CEDDEC pale blue
    out.append(text_box(n(), "Rectangle 80", IN(8.899), _CARD_Y, _CARD_W, _CARD_H, [paragraph([run("Year 3 ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$0M", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))   # 263746 navy
    out.append(text_box(n(), "Rectangle 81", IN(10.287), _CARD_Y, _CARD_W, _CARD_H, [paragraph([run("Year 4 ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$0M", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))   # 263746 navy
    out.append(text_box(n(), "Rectangle 82", IN(11.674), _CARD_Y, _CARD_W, _CARD_H, [paragraph([run("Year 5 ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$0M", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))   # 263746 navy
    # ── logo (top-right) ──
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 33", IN(9.023), IN(3.959), IN(3.748), IN(0.403), [paragraph([run("May be used if Weapons Procurement contract extends over 5-year period", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=GRAY_1, line_width=19050, anchor="ctr"))   # F2F2F2 off-white
    return "".join(out)


def render() -> str:
    return slide(_body())
