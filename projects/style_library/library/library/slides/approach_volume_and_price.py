"""approach_volume_and_price — Commercial Strategy market-analysis deck (20260325), source slide 121.

EXHIBIT — "Approach (2/2)": how to find annual volume and price per unit of cargo
($ / TEU). A two-track build-up wired together by operator glyphs (= + × ÷): a
Volume track and a Price track roll up — via mix-weighted basic-ocean-rate and
surcharge calculations, repeated across cargo types and routes — into a total
weighted-average container price ($ / TEU). Input boxes feed green price-formula
boxes; dashed "repeat across cargo types" frames and Preliminary speech-bubble
callouts annotate the method.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ........... breadcrumb() + title_placeholder()
  • _OPERATOR_GLYPHS  "=" / "+" / "×" calculation glyphs in paint-order buckets;
                       the standalone "÷" remains an individual shape
  • _FLOW_NODES ..... input and price-formula calculation nodes
  • _TRACK_LABELS ... the Volume / Price / Proportions track labels
  • _LEGEND_KEYS .... the colour-key chips
  • tables ........... "Total Container Volume" / "Container Price" header bands
  • callouts ......... Preliminary speech bubbles + dashed "repeat" frames

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=12, connector=6, chart=0, table=2, picture=0, custom_geometry=0, chrome_builders=2, clusters=7 (covering 41 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, PRELIM, BLUE_3, BLUE_5, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell_rich() form — the only
#    change is legibility. ──
def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...).
    Pass l_ins/r_ins explicitly for non-default padding (e.g. 37785); omit for the 45720 default."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_EQ_W, _EQ_H = IN(0.3), IN(0.3)        # "=" glyph size
_PLUS_W, _PLUS_H = IN(0.3), IN(0.3)    # "+" glyph size
_INPUT_W, _INPUT_H = IN(2.6), IN(0.35)  # input-box geometry
_MULT_W, _MULT_H = IN(0.3), IN(0.3)    # "×" glyph size
_PRICE_H = IN(0.35)       # price-box height
_AXIS_Y, _AXIS_H = IN(1.163), IN(0.236)   # track-axis label row
_KEY_Y, _KEY_W, _KEY_H = IN(1.163), IN(0.231), IN(0.234)   # legend-key chip geometry
_BOX_W = IN(2.6)          # green formula-box width                [shared x4]
_BOX_H = IN(0.35)         # green formula-box height               [shared x5]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the formula operators: '=' x7, '+' x4, 'x' x6; the glyph is a per-row field.
_OPERATOR_GLYPHS = {
    # Buckets preserve the original equals / plus / multiply paint positions;
    # preset geometry and rotation stay in the emitting loops.
    "equals": [
        (1.645, 4.981),
        (5.064, 2.933),
        (8.464, 2.933),
        (6.764, 4.981),
        (6.764, 6.347),
        (1.645, 3.615),
        (1.645, 6.347),
    ],
    "plus": [
        (6.764, 3.26),
        (11.345, 4.298),
        (11.345, 4.981),
        (6.764, 5.664),
    ],
    "multiply": [
        (1.645, 2.933),
        (8.464, 2.25),
        (5.064, 2.25),
        (8.338, 5.322),
        (6.764, 4.298),
        (1.645, 4.298),
    ],
}

# local_meaning: the formula build-up boxes: volume/price input boxes plus green price-formula
#   boxes; fill is a per-row field.
_FLOW_NODES = {
    # Fill and text contrast remain rendering data; both buckets are calculation nodes.
    "inputs": [
        (0.495, 2.566, GRAY_1, "Annual voyage count (#)"),    # F2F2F2 off-white
        (0.495, 3.249, GRAY_1, "Vessel capacity (#)"),    # F2F2F2 off-white
        (0.495, 4.615, None, "Vessel utilization (%)"),    # 000000 black outline
        (0.495, 5.297, GRAY_1, "Annual container volume (#) "),    # F2F2F2 off-white
        (7.314, 2.566, None, "FEU proportion of cargo type (%)"),    # 000000 black outline
        (3.914, 2.566, None, "TEU proportion of cargo type (%)"),    # 000000 black outline
        (5.614, 4.615, None, "Cargo type proportion of total volume (%)"),    # 000000 black outline
        (0.495, 3.932, GRAY_1, "Annual vessel capacity (#)"),    # F2F2F2 off-white
        (0.495, 5.98, GRAY_1, "Annual voyage count (#)"),    # F2F2F2 off-white
        (0.495, 6.663, GRAY_1, "Avg. container volume per voyage (#)"),    # F2F2F2 off-white
    ],
    "price_formulas": [
        (10.195, 3.932, 2.6, "Fuel surcharge ($ / TEU)"),
        (3.914, 1.883, 2.6, "Avg. TEU basic ocean rate within cargo type ($ / TEU)"),
        (7.314, 1.883, 2.6, "Avg. FEU container rate within cargo type, normalized to TEU ($ / TEU)"),
        (10.195, 4.615, 2.6, "Wharfage / Other Fees ($ / TEU)"),
        (7.314, 3.249, 2.6, "Mix-weighted FEU basic ocean rate, normalized to TEU ($ / TEU)"),
        (8.762, 5.297, 1.228, "Surcharge (%)"),
        (5.614, 5.297, 2.6, "Volume-weighted avg. basic ocean rate ($ / TEU)"),
        (5.614, 5.98, 2.6, "Ancillary charges ($ / TEU)"),
    ],
}

# local_meaning: the three parallel-track axis labels (Volume / Price / Proportions).
_TRACK_LABELS = [    # (x, cx, label) x3 — parallel Volume / Price / Proportions tracks
    (1.727, 0.752, "Volume (#)"),
    (0.709, 0.626, "Price ($)"),
    (2.895, 0.984, "Proportions (%)"),
]

# local_meaning: the three colour-key chips.
_LEGEND_KEYS = [    # (x, fill) x3 — colour-key chips
    (0.486, "2E7D32"),    # 2E7D32 green
    (1.504, GRAY_1),    # F2F2F2 off-white
    (2.671, None),    # 000000 black outline
]

# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Approach (2/2)", "To find annual volume and price per unit of cargo ($ / TEU)."))
    # ── operator glyphs: "=" ──
    for _x, _y in _OPERATOR_GLYPHS["equals"]:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _EQ_W, _EQ_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color="none", prst="mathEqual", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 52", IN(7.597), IN(2.915), IN(0.333), IN(1.7), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Rectangle 77", IN(5.614), IN(3.932), _BOX_W, _BOX_H, [paragraph([run("Mix-weighted avg. basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))   # 2E7D32 green
    # ── operator glyphs: "+" ──
    for _x, _y in _OPERATOR_GLYPHS["plus"]:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _PLUS_W, _PLUS_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=WHITE, prst="mathPlus", anchor="ctr", rot=5400000))   # 000000 black
    # ── flow nodes: volume/price inputs ──
    for _x, _y, _fill, _t in _FLOW_NODES["inputs"]:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _INPUT_W, _INPUT_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 19", IN(0.495), IN(1.883), _BOX_W, _BOX_H, [paragraph([run("Vessel (e.g., Maunawili)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, anchor="ctr"))   # 000000 black
    # ── track header bands (low-level tables) ──
    # Each one-column table carries its width at col_widths; the single row
    # supplies the minimum height. Cell l/r insets are explicit, anchor keeps
    # vertical centering, and tpara mar_l/indent makes the text margin zero.
    # palette — text: 000000 black; rules: FFFFFF white (top) · 162029 dark navy (bottom); cell fills: none.
    out.append(table(n(), "Table 39", IN(0.495), IN(1.464), IN(3.1), IN(0.3), col_widths=[IN(3.1)], rows=[
        trow([rcell([tpara([trun("Total Container Volume ", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], l_ins=37785, r_ins=37785, T=edge(WHITE), B=edge(DK))], h=IN(0.3)),
    ]))
    # palette — text: 000000 black; rules: FFFFFF white (top) · 162029 dark navy (bottom); cell fills: none.
    out.append(table(n(), "Table 40", IN(3.795), IN(1.464), IN(9), IN(0.3), col_widths=[IN(9)], rows=[
        trow([rcell([tpara([trun("Container Price", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], l_ins=37785, r_ins=37785, T=edge(WHITE), B=edge(DK))], h=IN(0.3)),
    ]))
    # ── operator glyphs: "×" ──
    for _x, _y in _OPERATOR_GLYPHS["multiply"]:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _MULT_W, _MULT_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=WHITE, prst="mathMultiply", anchor="ctr"))   # 000000 black
    # ── flow nodes: green price formulas ──
    for _x, _y, _cx, _t in _FLOW_NODES["price_formulas"]:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _PRICE_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))   # 2E7D32 green
    out.append(text_box(n(), "Rectangle 71", IN(10.195), IN(5.297), _BOX_W, _BOX_H, [paragraph([run("Terminal Handling / Stevedoring", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))   # 2E7D32 green
    out.append(text_box(n(), "Rectangle 72", IN(3.914), IN(6.663), IN(6), _BOX_H, [paragraph([run("Total weighted avg. container price", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))   # 2E7D32 green
    out.append(text_box(n(), "Rectangle 73", IN(3.914), IN(3.249), _BOX_W, _BOX_H, [paragraph([run("Mix-weighted TEU basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))   # 2E7D32 green
    out.append(connector(n(), "Connector: Elbow 92", IN(5.897), IN(2.915), IN(0.333), IN(1.7), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 97", IN(9.989), IN(4.107), IN(0.206), IN(1.365), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))   # 000000 black
    out.append(text_box(n(), "Rectangle 118", IN(3.795), IN(1.828), IN(6.194), IN(3.174), [paragraph([], line_spacing=100000), paragraph([run("Repeat across ", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), line_break(), run("cargo types", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b"))   # 000000 black outline
    # ── Preliminary callouts ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 105", IN(10.164), IN(2.481), IN(2.632), IN(0.738), [paragraph([run("Finding mix-weighted rate required as TEU generally have higher basic ocean and terminal handling / stevedoring charges vs. normalized FEU", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -59942", "adj2": "val 53401"}, anchor="ctr"))   # FFFFCC pale yellow
    out.append(connector(n(), "Connector: Elbow 136", IN(9.601), IN(4.26), IN(0.508), IN(3.282), color=BLACK, width=12700, arrow=True, prst="bentConnector2", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Speech Bubble: Rectangle 139", IN(11.645), IN(5.814), IN(1.336), IN(0.626), [paragraph([run("Also weighted by TEU/FEU mix and cargo composition ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val 5870", "adj2": "val -74249"}, anchor="ctr"))   # FFFFCC pale yellow
    out.append(connector(n(), "Straight Arrow Connector 143", IN(1.795), IN(2.233), IN(0), IN(0.333), color=BLACK, width=12700, arrow=True))   # 000000 black
    out.append(text_box(n(), "Speech Bubble: Rectangle 158", IN(3.127), IN(5.092), IN(1.521), IN(1.238), [paragraph([run("Matson does not publish utilization metrics; thus, utilization is solved for using published & forecast annual and quarterly container volume, westbound / eastbound cargo proportions, and cargo type proportions", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -55587", "adj2": "val -66064"}, anchor="ctr"))   # FFFFCC pale yellow
    # ── standalone "÷" glyph ──
    out.append(text_box(n(), "Division Sign 159", IN(1.645), IN(5.664), IN(0.3), IN(0.3), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color="none", prst="mathDivide", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 169", IN(0.495), IN(2.741), IN(0.014), IN(3.414), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=10800000, adj={"adj1": "val 1800000"}))   # 000000 black
    out.append(text_box(n(), "TextBox 172", IN(7.593), IN(1.164), IN(5.473), IN(0.234), [paragraph([run("Repeat across all routes and vessels", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color=BLACK, anchor="ctr"))   # 263746 navy
    out.append(text_box(n(), "TextBox 173", IN(7.593), IN(1.478), IN(5.473), IN(0.234), [paragraph([run("To find volume and price for dry cargo TEUs, refrigerated TEUs, and automobiles", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_3, line_color=BLACK, anchor="ctr"))   # 6E91B1 blue
    # ── track labels + legend keys ──
    for _x, _cx, _t in _TRACK_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _AXIS_Y, IN(_cx), _AXIS_H, [paragraph([run(_t, size=PT(8), color=DK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", wrap="none"))   # 162029 dark navy
    for _x, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _KEY_Y, _KEY_W, _KEY_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    return "".join(out)


def render() -> str:
    return slide(_body())
