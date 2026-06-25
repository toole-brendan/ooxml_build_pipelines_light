"""approach_volume_and_price - Commercial Strategy deck, source slide 121.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=12, connector=6, chart=0, table=2, picture=0, chrome_builders=2, clusters=7 (covering 41 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
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


# ── layout anchors (shared coordinates) ──
_SW_W, _SW_H = IN(0.3), IN(0.3)
_SW2_W, _SW2_H = IN(0.3), IN(0.3)
_LBL_W, _LBL_H = IN(2.6), IN(0.35)
_SW3_W, _SW3_H = IN(0.3), IN(0.3)
_LBL2_H = IN(0.35)
_LBL3_Y, _LBL3_H = IN(1.163), IN(0.236)
_SW4_Y, _SW4_W, _SW4_H = IN(1.163), IN(0.231), IN(0.234)
_W1 = IN(2.6)   # shared x4
_H1 = IN(0.35)   # shared x5

# ── repeated-shape data tables (each drives a loop in _body) ──
_LEGEND_SWATCHES = [    # (x, y) x7
    (1.645, 4.981),
    (5.064, 2.933),
    (8.464, 2.933),
    (6.764, 4.981),
    (6.764, 6.347),
    (1.645, 3.615),
    (1.645, 6.347),
]

_LEGEND_SWATCHES2 = [    # (x, y) x4
    (6.764, 3.26),
    (11.345, 4.298),
    (11.345, 4.981),
    (6.764, 5.664),
]

_LABELS = [    # (x, y, fill, label) x10
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

_LEGEND_SWATCHES3 = [    # (x, y) x6
    (1.645, 2.933),
    (8.464, 2.25),
    (5.064, 2.25),
    (8.338, 5.322),
    (6.764, 4.298),
    (1.645, 4.298),
]

_LABELS2 = [    # (x, y, cx, label) x8
    (10.195, 3.932, 2.6, "Fuel surcharge ($ / TEU)"),
    (3.914, 1.883, 2.6, "Avg. TEU basic ocean rate within cargo type ($ / TEU)"),
    (7.314, 1.883, 2.6, "Avg. FEU container rate within cargo type, normalized to TEU ($ / TEU)"),
    (10.195, 4.615, 2.6, "Wharfage / Other Fees ($ / TEU)"),
    (7.314, 3.249, 2.6, "Mix-weighted FEU basic ocean rate, normalized to TEU ($ / TEU)"),
    (8.762, 5.297, 1.228, "Surcharge (%)"),
    (5.614, 5.297, 2.6, "Volume-weighted avg. basic ocean rate ($ / TEU)"),
    (5.614, 5.98, 2.6, "Ancillary charges ($ / TEU)"),
]

_LABELS3 = [    # (x, cx, label) x3
    (1.727, 0.752, "Volume (#)"),
    (0.709, 0.626, "Price ($)"),
    (2.895, 0.984, "Proportions (%)"),
]

_LEGEND_SWATCHES4 = [    # (x, fill) x3
    (0.486, "2E7D32"),
    (1.504, GRAY_1),
    (2.671, None),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Carrier Entry Point Attractiveness", "Matson Test Case"))
    out.append(title_placeholder("Approach (2/2)", "To find annual volume and price per unit of cargo ($ / TEU)."))
    for _x, _y in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color="none", prst="mathEqual", anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 52", IN(7.597), IN(2.915), IN(0.333), IN(1.7), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "Rectangle 77", IN(5.614), IN(3.932), _W1, _H1, [paragraph([run("Mix-weighted avg. basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    for _x, _y in _LEGEND_SWATCHES2:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW2_W, _SW2_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=WHITE, prst="mathPlus", anchor="ctr", rot=5400000))
    for _x, _y, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 19", IN(0.495), IN(1.883), _W1, _H1, [paragraph([run("Vessel (e.g., Maunawili)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, anchor="ctr"))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 39", IN(0.495), IN(1.464), IN(3.1), IN(0.3), col_widths=[IN(3.1)], rows=[
        trow([tcell("Total Container Volume ", size=PT(10), bold=True, color=BLACK, l_ins=37785, r_ins=37785, borders={"L": "none", "R": "none", "T": {"color": WHITE, "width": 12700}, "B": {"color": DK, "width": 12700}})], h=IN(0.3)),
    ]))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 40", IN(3.795), IN(1.464), IN(9), IN(0.3), col_widths=[IN(9)], rows=[
        trow([tcell("Container Price", size=PT(10), bold=True, color=BLACK, l_ins=37785, r_ins=37785, borders={"L": "none", "R": "none", "T": {"color": WHITE, "width": 12700}, "B": {"color": DK, "width": 12700}})], h=IN(0.3)),
    ]))
    for _x, _y in _LEGEND_SWATCHES3:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW3_W, _SW3_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=WHITE, prst="mathMultiply", anchor="ctr"))
    for _x, _y, _cx, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL2_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 71", IN(10.195), IN(5.297), _W1, _H1, [paragraph([run("Terminal Handling / Stevedoring", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 72", IN(3.914), IN(6.663), IN(6), _H1, [paragraph([run("Total weighted avg. container price", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 73", IN(3.914), IN(3.249), _W1, _H1, [paragraph([run("Mix-weighted TEU basic ocean rate ", size=PT(10), color=WHITE, font=FONT), line_break(), run("($ / TEU)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="2E7D32", line_color=BLACK, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 92", IN(5.897), IN(2.915), IN(0.333), IN(1.7), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 97", IN(9.989), IN(4.107), IN(0.206), IN(1.365), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))
    out.append(text_box(n(), "Rectangle 118", IN(3.795), IN(1.828), IN(6.194), IN(3.174), [paragraph([], line_spacing=100000), paragraph([run("Repeat across ", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), line_break(), run("cargo types", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=BLACK, dashed_line=True, anchor="b"))
    out.append(text_box(n(), "Speech Bubble: Rectangle 105", IN(10.164), IN(2.481), IN(2.632), IN(0.738), [paragraph([run("Finding mix-weighted rate required as TEU generally have higher basic ocean and terminal handling / stevedoring charges vs. normalized FEU", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -59942", "adj2": "val 53401"}, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 136", IN(9.601), IN(4.26), IN(0.508), IN(3.282), color=BLACK, width=12700, arrow=True, prst="bentConnector2", rot=5400000))
    out.append(text_box(n(), "Speech Bubble: Rectangle 139", IN(11.645), IN(5.814), IN(1.336), IN(0.626), [paragraph([run("Also weighted by TEU/FEU mix and cargo composition ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val 5870", "adj2": "val -74249"}, anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 143", IN(1.795), IN(2.233), IN(0), IN(0.333), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Speech Bubble: Rectangle 158", IN(3.127), IN(5.092), IN(1.521), IN(1.238), [paragraph([run("Matson does not publish utilization metrics; thus, utilization is solved for using published & forecast annual and quarterly container volume, westbound / eastbound cargo proportions, and cargo type proportions", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=PRELIM, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val -55587", "adj2": "val -66064"}, anchor="ctr"))
    out.append(text_box(n(), "Division Sign 159", IN(1.645), IN(5.664), IN(0.3), IN(0.3), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color="none", prst="mathDivide", anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 169", IN(0.495), IN(2.741), IN(0.014), IN(3.414), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=10800000, adj={"adj1": "val 1800000"}))
    out.append(text_box(n(), "TextBox 172", IN(7.593), IN(1.164), IN(5.473), IN(0.234), [paragraph([run("Repeat across all routes and vessels", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "TextBox 173", IN(7.593), IN(1.478), IN(5.473), IN(0.234), [paragraph([run("To find volume and price for dry cargo TEUs, refrigerated TEUs, and automobiles", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_3, line_color=BLACK, anchor="ctr"))
    for _x, _cx, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), _LBL3_Y, IN(_cx), _LBL3_H, [paragraph([run(_t, size=PT(8), color=DK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", wrap="none"))
    for _x, _fill in _LEGEND_SWATCHES4:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SW4_Y, _SW4_W, _SW4_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    return "".join(out)


def render() -> str:
    return slide(_body())
