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
  • _EQUALS_SIGNS .... "=" glyphs (mathEqual)
  • _PLUS_SIGNS ...... "+" glyphs (mathPlus);  _TIMES_SIGNS = "×" (mathMultiply);
                       plus a standalone "÷" (mathDivide). All were converter-
                       labelled "LegendSwatch"; they are calc operators
  • _INPUT_BOXES ..... volume/price input boxes down the two tracks
  • _PRICE_BOXES ..... green price-formula boxes
  • _AXIS_LABELS ..... the Volume / Price / Proportions track labels
  • _LEGEND_CHIPS .... the colour-key chips
  • tables ........... "Total Container Volume" / "Container Price" header bands
  • callouts ......... Preliminary speech bubbles + dashed "repeat" frames

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=12, connector=6, table=2, chrome_builders=2,
clusters=7 (covering 41 shapes), dropped=1 (think-cell OLE frame).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, PRELIM, BLUE_3, BLUE_5, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


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
_EQUALS_SIGNS = [    # (x, y) x7 — "=" operator glyphs
    (1.645, 4.981),
    (5.064, 2.933),
    (8.464, 2.933),
    (6.764, 4.981),
    (6.764, 6.347),
    (1.645, 3.615),
    (1.645, 6.347),
]

_PLUS_SIGNS = [    # (x, y) x4 — "+" operator glyphs
    (6.764, 3.26),
    (11.345, 4.298),
    (11.345, 4.981),
    (6.764, 5.664),
]

_INPUT_BOXES = [    # (x, y, fill, label) x10 — volume/price input boxes
    (0.495, 2.566, GRAY_1, "Annual voyage count (#)"),
    (0.495, 3.249, GRAY_1, "Vessel capacity (#)"),
    (0.495, 4.615, None, "Vessel utilization (%)"),
    (0.495, 5.297, GRAY_1, "Annual container volume (#) "),
    (7.314, 2.566, None, "FEU proportion of cargo type (%)"),
    (3.914, 2.566, None, "TEU proportion of cargo type (%)"),
    (5.614, 4.615, None, "Cargo type proportion of total volume (%)"),
    (0.495, 3.932, GRAY_1, "Annual vessel capacity (#)"),
    (0.495, 5.98, GRAY_1, "Annual voyage count (#)"),
    (0.495, 6.663, GRAY_1, "Avg. container volume per voyage (#)"),
]

_TIMES_SIGNS = [    # (x, y) x6 — "×" operator glyphs
    (1.645, 2.933),
    (8.464, 2.25),
    (5.064, 2.25),
    (8.338, 5.322),
    (6.764, 4.298),
    (1.645, 4.298),
]

_PRICE_BOXES = [    # (x, y, cx, label) x8 — green price-formula boxes
    (10.195, 3.932, 2.6, "Fuel surcharge ($ / TEU)"),
    (3.914, 1.883, 2.6, "Avg. TEU basic ocean rate within cargo type ($ / TEU)"),
    (7.314, 1.883, 2.6, "Avg. FEU container rate within cargo type, normalized to TEU ($ / TEU)"),
    (10.195, 4.615, 2.6, "Wharfage / Other Fees ($ / TEU)"),
    (7.314, 3.249, 2.6, "Mix-weighted FEU basic ocean rate, normalized to TEU ($ / TEU)"),
    (8.762, 5.297, 1.228, "Surcharge (%)"),
    (5.614, 5.297, 2.6, "Volume-weighted avg. basic ocean rate ($ / TEU)"),
    (5.614, 5.98, 2.6, "Ancillary charges ($ / TEU)"),
]

_AXIS_LABELS = [    # (x, cx, label) x3 — track-axis labels
    (1.727, 0.752, "Volume (#)"),
    (0.709, 0.626, "Price ($)"),
    (2.895, 0.984, "Proportions (%)"),
]

_LEGEND_CHIPS = [    # (x, fill) x3 — colour-key chips
    (0.486, "2E7D32"),
    (1.504, GRAY_1),
    (2.671, None),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Approach (2/2)", "To find annual volume and price per unit of cargo ($ / TEU)."))
    # ── operator glyphs: "=" ──
    for _x, _y in _EQUALS_SIGNS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _EQ_W, _EQ_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color="none", prst="mathEqual", anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 52", IN(7.597), IN(2.915), IN(0.333), IN(1.7), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "Rectangle 77", IN(5.614), IN(3.932), _BOX_W, _BOX_H, [paragraph([run("Mix-weighted avg. basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    # ── operator glyphs: "+" ──
    for _x, _y in _PLUS_SIGNS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _PLUS_W, _PLUS_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=WHITE, prst="mathPlus", anchor="ctr", rot=5400000))
    # ── volume/price input boxes ──
    for _x, _y, _fill, _t in _INPUT_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _INPUT_W, _INPUT_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 19", IN(0.495), IN(1.883), _BOX_W, _BOX_H, [paragraph([run("Vessel (e.g., Maunawili)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, anchor="ctr"))
    # ── track header bands (low-level tables) ──
    out.append(table(n(), "Table 39", IN(0.495), IN(1.464), IN(3.1), IN(0.3), col_widths=[IN(3.1)], rows=[
        trow([tcell("Total Container Volume ", size=PT(10), bold=True, color=BLACK, l_ins=37785, r_ins=37785, borders={"L": "none", "R": "none", "T": {"color": WHITE, "width": 12700}, "B": {"color": DK, "width": 12700}})], h=IN(0.3)),
    ]))
    out.append(table(n(), "Table 40", IN(3.795), IN(1.464), IN(9), IN(0.3), col_widths=[IN(9)], rows=[
        trow([tcell("Container Price", size=PT(10), bold=True, color=BLACK, l_ins=37785, r_ins=37785, borders={"L": "none", "R": "none", "T": {"color": WHITE, "width": 12700}, "B": {"color": DK, "width": 12700}})], h=IN(0.3)),
    ]))
    # ── operator glyphs: "×" ──
    for _x, _y in _TIMES_SIGNS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _MULT_W, _MULT_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=WHITE, prst="mathMultiply", anchor="ctr"))
    # ── green price-formula boxes ──
    for _x, _y, _cx, _t in _PRICE_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _PRICE_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 71", IN(10.195), IN(5.297), _BOX_W, _BOX_H, [paragraph([run("Terminal Handling / Stevedoring", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 72", IN(3.914), IN(6.663), IN(6), _BOX_H, [paragraph([run("Total weighted avg. container price", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 73", IN(3.914), IN(3.249), _BOX_W, _BOX_H, [paragraph([run("Mix-weighted TEU basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 92", IN(5.897), IN(2.915), IN(0.333), IN(1.7), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 97", IN(9.989), IN(4.107), IN(0.206), IN(1.365), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))
    out.append(text_box(n(), "Rectangle 118", IN(3.795), IN(1.828), IN(6.194), IN(3.174), [paragraph([], line_spacing=100000), paragraph([run("Repeat across ", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), line_break(), run("cargo types", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b"))
    # ── Preliminary callouts ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 105", IN(10.164), IN(2.481), IN(2.632), IN(0.738), [paragraph([run("Finding mix-weighted rate required as TEU generally have higher basic ocean and terminal handling / stevedoring charges vs. normalized FEU", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -59942", "adj2": "val 53401"}, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 136", IN(9.601), IN(4.26), IN(0.508), IN(3.282), color=BLACK, width=12700, arrow=True, prst="bentConnector2", rot=5400000))
    out.append(text_box(n(), "Speech Bubble: Rectangle 139", IN(11.645), IN(5.814), IN(1.336), IN(0.626), [paragraph([run("Also weighted by TEU/FEU mix and cargo composition ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val 5870", "adj2": "val -74249"}, anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 143", IN(1.795), IN(2.233), IN(0), IN(0.333), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Speech Bubble: Rectangle 158", IN(3.127), IN(5.092), IN(1.521), IN(1.238), [paragraph([run("Matson does not publish utilization metrics; thus, utilization is solved for using published & forecast annual and quarterly container volume, westbound / eastbound cargo proportions, and cargo type proportions", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -55587", "adj2": "val -66064"}, anchor="ctr"))
    # ── standalone "÷" glyph ──
    out.append(text_box(n(), "Division Sign 159", IN(1.645), IN(5.664), IN(0.3), IN(0.3), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color="none", prst="mathDivide", anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 169", IN(0.495), IN(2.741), IN(0.014), IN(3.414), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=10800000, adj={"adj1": "val 1800000"}))
    out.append(text_box(n(), "TextBox 172", IN(7.593), IN(1.164), IN(5.473), IN(0.234), [paragraph([run("Repeat across all routes and vessels", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "TextBox 173", IN(7.593), IN(1.478), IN(5.473), IN(0.234), [paragraph([run("To find volume and price for dry cargo TEUs, refrigerated TEUs, and automobiles", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_3, line_color=BLACK, anchor="ctr"))
    # ── track-axis labels + legend key ──
    for _x, _cx, _t in _AXIS_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _AXIS_Y, IN(_cx), _AXIS_H, [paragraph([run(_t, size=PT(8), color=DK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", wrap="none"))
    for _x, _fill in _LEGEND_CHIPS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _KEY_Y, _KEY_W, _KEY_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    return "".join(out)


def render() -> str:
    return slide(_body())
