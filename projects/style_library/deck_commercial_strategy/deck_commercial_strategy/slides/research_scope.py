"""research_scope - Commercial Strategy deck, source slide 3.

Auto-converted from the source .pptx by _tools/convert_slide.py. The native
<c:chart> exhibit is bundled verbatim with its .xlsb (byte-exact, still "Edit
Data"-editable); shapes are deck_core primitives at the source EMU coordinates.
Standard chrome uses the house builders; repeated shape clusters are data tables
+ loops; think-cell <a:fld> labels are frozen; the OLE frame + EMF preview dropped.

Converter stats: text_box=5, connector=9, chart=0, chrome_builders=2, clusters=6 (covering 32 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder,
)
from deck_core.charts import graphic_frame, editable_bundled_chart
from deck_core.style import IN, PT, BLACK, WHITE, BLUE_1, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_LBL_W, _LBL_H = IN(4.751), IN(0.45)
_LBL2_H = IN(0.45)
_LBL4_Y, _LBL4_H = IN(1.182), IN(0.294)
_LBL5_X, _LBL5_W = IN(3.349), IN(2.977)
_VAL_X, _VAL_W, _VAL_H = IN(6.381), IN(0.3), IN(0.3)
_Y1 = IN(1.475)   # shared x4
_X1 = IN(3.348)   # shared x4
_W1 = IN(8.139)   # shared x5

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, fill, label) x4
    (6.736, 1.516, None, "Define the end-to-end (E2E) commercial maritime value chain, including current revenue potential and profitability "),
    (6.736, 2.071, GRAY_1, "Assess demand for US-built ships under current and expected industrial policy (i.e., Jones Act status quo, SHIPS Act, other US-built markets)"),
    (6.736, 2.627, GRAY_3, "Compare US shipbuilding costs vs. PRC / ROK / Japan under current and expected industrial policy"),
    (6.736, 3.738, "C4DFEF", "Compare US-flagged vs. foreign-flagged vessel costs under current and expected industrial policy"),
]

_LABELS2 = [    # (x, y, cx, fill, label) x6
    (6.736, 5.96, 4.751, "0F2634", "Project OpCo financials given potential industrial policy and automation impact"),
    (6.736, 4.294, 4.751, "89C0DE", "Determine impact of automation on vessel opex and fuel costs"),
    (6.736, 4.849, 4.751, "4EA0CE", "Identify most attractive entry points in existing US-flagged market based on unit economics, incumbent fleet, competition, and our capabilities"),
    (6.736, 6.516, 4.751, BLACK, "Project ComboCo financials under different demand, subsidy, and automation scenarios"),
    (6.736, 3.182, 4.751, "808080", "Project ShipbuilderCo financials given US-built ship demand and shipyard subsidy scenarios"),
    (6.736, 5.405, 4.751, "163A4E", "Identify and assess attractiveness of alternative service models unlocked by automation (i.e., substitute ocean for trucking/rail)"),
]

_LABELS3 = [    # (x, y, cx, cy, label) x3
    (10.817, 5.064, 2.228, 0.627, "Carriers"),
    (11.252, 2.339, 2.23, 1.498, "Shipbuilders"),
    (12.216, 4.955, 1.006, 0.793, "Terminal Ops & Coordination"),
]

_LABELS4 = [    # (x, cx, fill, label) x4
    (11.618, 1.6, WHITE, "Value Chain Steps"),
    (6.382, 5.105, None, "Focus Areas"),
    (3.348, 2.903, None, "Key Questions for Saronic"),
    (0.217, 3, None, "Objectives"),
]

_LABELS5 = [    # (y, cy, label) x5
    (3.737, 1.006, "How do US-flagged vessel economics compare to foreign-flagged today, and how do industrial policy and automation change the gap?"),
    (1.516, 0.401, "How do economics of integrated players compare to pure-play entities today?"),
    (5.96, 0.45, "What do these findings imply for OpCo (Saronic as owner/operator) financials?"),
    (6.516, 0.45, "What do these findings imply for ComboCo financials?"),
    (4.849, 1.006, "Where is most attractive to enter in existing US-flagged trades and/or in new markets unlocked by automation?"),
]

_VALUE_LABELS = [    # (y, label) x10
    (1.566, "1"),
    (2.146, "2"),
    (2.702, "3"),
    (3.257, "4"),
    (3.813, "5"),
    (4.369, "6"),
    (4.924, "7"),
    (6.035, "9"),
    (6.591, "10"),
    (5.48, "8"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(text_box(n(), "Rectangle 73", IN(0.216), IN(1.537), IN(1.452), IN(5.429), [paragraph([run("Determine where Saronic should play", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=BLUE_1, line_color=BLACK, anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    out.append(breadcrumb("Commercial Strategy", "Research Overview"))
    for _x, _y, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)])], fill=_fill, line_color=BLACK, anchor="ctr"))
    for _x, _y, _cx, _fill, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL2_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)])], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(title_placeholder("Research scope", "Two objectives are supported by ten research focus areas."))
    for _x, _y, _cx, _cy, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color=BLACK, anchor="ctr", rot=5400000))
    for _x, _cx, _fill, _t in _LABELS4:
        out.append(text_box(n(), "Label", IN(_x), _LBL4_Y, IN(_cx), _LBL4_H, [paragraph([run(_t, size=PT(11), bold=True, color=BLACK, font=FONT)])], fill=_fill, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 33", IN(6.383), _Y1, IN(5.104), IN(-0.002), color=BLACK, width=12700))
    out.append(connector(n(), "Straight Arrow Connector 44", IN(3.349), _Y1, IN(2.903), IN(-0.002), color=BLACK, width=12700))
    for _y, _cy, _t in _LABELS5:
        out.append(text_box(n(), "Label", _LBL5_X, IN(_y), _LBL5_W, IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    out.append(connector(n(), "Straight Arrow Connector 64", IN(0.216), _Y1, IN(3), IN(-0.002), color=BLACK, width=12700))
    out.append(text_box(n(), "Rectangle 65", IN(1.764), IN(2.392), IN(1.452), IN(4.574), [paragraph([run("Understand how Saronic will win", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=BLUE_1, line_color=BLACK, anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    for _y, _t in _VALUE_LABELS:
        out.append(text_box(n(), "ValueLabel", _VAL_X, IN(_y), _VAL_W, _VAL_H, [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color=BLACK, prst="ellipse", anchor="ctr", l_ins=0, r_ins=0))
    out.append(connector(n(), "Straight Arrow Connector 7", IN(11.618), _Y1, IN(1.498), IN(-0.002), color=BLACK, width=12700))
    out.append(connector(n(), "Straight Connector 6", _X1, IN(2.018), _W1, IN(0), color=BLACK, width=6350))
    out.append(text_box(n(), "Rectangle 51", IN(7.66), IN(0.125), IN(2.902), IN(0.452), [paragraph([], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    out.append(connector(n(), "Straight Connector 55", _X1, IN(4.796), _W1, IN(0), color=BLACK, width=6350))
    out.append(connector(n(), "Straight Connector 57", _X1, IN(6.463), _W1, IN(0), color=BLACK, width=6350))
    out.append(text_box(n(), "Rectangle 61", IN(3.349), IN(2.069), IN(2.978), IN(1.563), [paragraph([run("What is the addressable demand for US-built ships and what does it imply for Port Alpha’s orderbook?", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr"), paragraph([], align="ctr"), paragraph([run("What are the impacts on US newbuild prices vs. those of major international shipbuilders?", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr"), paragraph([], align="ctr"), paragraph([run("How do these findings impact our shipyard financial outlook (Port Alpha)?", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    out.append(connector(n(), "Straight Connector 67", _X1, IN(5.908), _W1, IN(0), color=BLACK, width=6350))
    out.append(connector(n(), "Straight Connector 68", IN(3.444), IN(3.685), _W1, IN(0), color=BLACK, width=6350))
    out.append(text_box(n(), "Rectangle 69", IN(3.312), IN(2.581), IN(2.901), IN(0.528), [paragraph([], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    return "".join(out)


def render() -> str:
    return slide(_body())
