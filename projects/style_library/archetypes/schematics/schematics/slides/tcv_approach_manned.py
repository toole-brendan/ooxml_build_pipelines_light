"""tcv_approach_manned - Commercial Strategy deck, source slide 18.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=17, connector=11, chart=0, table=0, picture=1, chrome_builders=2, clusters=7 (covering 52 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.

Converter notes:
  - Note/Source line off house position - kept verbatim
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, line_break, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]


# ── layout anchors (shared coordinates) ──
_SW_X, _SW_W, _SW_H = IN(10.843), IN(0.4), IN(0.4)
_SW2_X, _SW2_W, _SW2_H = IN(6.629), IN(0.4), IN(0.4)
_SW3_Y, _SW3_W, _SW3_H = IN(3.927), IN(0.4), IN(0.4)
_Y1 = IN(3.183)   # shared x5
_W1 = IN(1.519)   # shared x7
_H1 = IN(0.359)   # shared x8
_W2 = IN(0.405)   # shared x6
_Y2 = IN(1.068)   # shared x4
_H2 = IN(0.2)   # shared x4

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, cx, cy, label) x8
    (0.426, 1.484, 2.101, 0.701, "1. Identify missions"),
    (0.426, 2.248, 2.101, 0.701, "2. Identify priority kill chain roles"),
    (0.426, 3.776, 2.101, 0.701, "4. Identify and sum corresponding budget items to find Total Funding"),
    (0.426, 4.54, 2.101, 0.701, "5. Allocate platforms and effectors to missions to find TAM"),
    (0.426, 5.304, 2.101, 0.701, "6. Multiply by unmanned adoption rate to find SAM"),
    (0.426, 3.012, 2.101, 0.701, "3. Identify specific platforms / effectors for missions"),
    (0.426, 6.068, 2.101, 0.701, "7. Multiply by Saronic market share to find Company TCV"),
    (0.495, 6.642, 12.367, 0.354, "Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)"),
]

_LABELS2 = [    # (x, y, cx, cy, fill, line, label) x7
    (11.46, 3.947, 1.519, 0.359, BLUE_1, BLACK, "Total Funding ($)"),
    (11.46, 4.711, 1.519, 0.359, BLUE_2, BLACK, "TAM ($)"),
    (10.956, 2.419, 2.022, 0.359, GRAY_1, GRAY_1, "Combat Systems Integration (incl. CEC)"),
    (8.306, 2.419, 2.022, 0.359, GRAY_1, GRAY_1, "Sensors"),
    (3.003, 4.711, 2.549, 0.359, BLUE_1, BLACK, "Total Funding ($)"),
    (3.003, 5.475, 2.549, 0.359, BLUE_2, BLACK, "TAM ($)"),
    (5.656, 2.419, 2.022, 0.359, GRAY_1, GRAY_1, "Effectors"),
]

_LABELS3 = [    # (x, y, cx, cy, fill, line, label) x22
    (11.46, 5.475, 1.519, 0.359, BLUE_3, BLACK, "SAM ($)"),
    (11.46, 6.239, 1.519, 0.359, BLUE_4, BLACK, "Company TCV ($)"),
    (3.003, 2.419, 2.022, 0.359, BLACK, BLACK, "Platforms"),
    (9.768, 3.183, 1.519, 0.359, BLACK, BLACK, "Littoral Combat Ship"),
    (9.106, 3.947, 1.519, 0.359, BLACK, BLACK, "Cost Elements ($)"),
    (8.077, 4.711, 2.548, 0.359, BLACK, BLACK, "Mission allocations by platform and effector (%)"),
    (8.088, 5.475, 2.548, 0.359, BLACK, BLACK, "Unmanned adoption (%)"),
    (3.003, 6.239, 2.549, 0.359, BLUE_3, BLACK, "SAM ($)"),
    (8.088, 6.239, 2.548, 0.359, BLACK, BLACK, "Saronic market share (%)"),
    (3.003, 3.947, 1.519, 0.359, BLACK, BLACK, "OBBBA items ($)"),
    (2.777, 1.371, 1.213, 0.333, BLACK, BLACK, "Anti-Air Warfare (incl. cUAS)"),
    (5.344, 1.371, 1.213, 0.333, BLACK, BLACK, "Anti-Submarine Warfare"),
    (9.196, 1.371, 1.213, 0.333, "A6A6A6", "A6A6A6", "Amphibious Warfare"),
    (6.629, 1.371, 1.212, 0.333, BLACK, BLACK, "Ballistic Missile Defense"),
    (7.912, 1.371, 1.213, 0.333, BLACK, BLACK, "Electronic Warfare (D&D)"),
    (5.344, 1.772, 1.213, 0.333, BLACK, BLACK, "Mine Warfare"),
    (9.196, 1.772, 1.213, 0.333, "A6A6A6", "A6A6A6", "Special Operations"),
    (10.48, 1.772, 1.213, 0.333, "A6A6A6", "A6A6A6", "Sealift"),
    (6.629, 1.774, 1.213, 0.333, BLACK, BLACK, "Strike Warfare"),
    (4.06, 1.772, 1.213, 0.333, BLACK, BLACK, "ISR"),
    (10.48, 1.371, 1.214, 0.333, "A6A6A6", "A6A6A6", "C4"),
    (2.777, 1.778, 1.213, 0.333, BLACK, BLACK, "Electronic Warfare (Other)"),
]

_LEGEND_SWATCHES = [    # (y) x4
    3.927,
    4.691,
    5.454,
    6.218,
]

_LEGEND_SWATCHES2 = [    # (y) x3
    4.691,
    5.454,
    6.218,
]

_LEGEND_SWATCHES3 = [    # (x) x3
    6.614,
    8.648,
    4.579,
]

_VALUE_LABELS = [    # (x, y, cx, cy, fill, line) x5
    (2.667, 1.312, 6.497, 0.859, None, BLACK),
    (9.078, 1.068, 0.2, 0.2, "A6A6A6", "A6A6A6"),
    (11.836, 1.068, 0.2, 0.2, None, GRAY_3),
    (7.764, 1.068, 0.2, 0.2, BLACK, BLACK),
    (10.773, 1.068, 0.2, 0.2, GRAY_1, GRAY_1),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(title_placeholder("Approach to find TCV", "Currently manned capabilities"))
    for _x, _y, _cx, _cy, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _lc, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _lc, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 41", IN(3.003), _Y1, _W1, _H1, [paragraph([run("Ticonderoga", size=PT(9), italic=True, font=FONT), run("-class cruisers", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 42", IN(4.694), _Y1, _W1, _H1, [paragraph([run("Arleigh Burke", size=PT(9), italic=True, font=FONT), run("-class destroyers", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 43", IN(6.385), _Y1, _W1, _H1, [paragraph([run("Zumwalt", size=PT(9), italic=True, font=FONT), run("-class destroyers", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 44", IN(8.077), _Y1, _W1, _H1, [paragraph([run("Constellation-", size=PT(9), italic=True, color=WHITE, font=FONT), run("class frigates", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 46", IN(11.46), _Y1, _W1, _H1, [paragraph([run("Avenger", size=PT(9), bold=True, italic=True, color=WHITE, font=FONT), run("-class MCM ship", size=PT(9), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 47", IN(3.685), IN(2.855), _W2, IN(0.252), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 48", IN(4.531), IN(2.261), _W2, IN(1.44), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 49", IN(5.377), IN(1.415), _W2, IN(3.131), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 50", IN(7.914), IN(-1.122), _W2, IN(8.205), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 51", IN(7.068), IN(-0.276), _W2, IN(6.514), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 52", IN(6.222), IN(0.57), _W2, IN(4.822), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(text_box(n(), "Rectangle 53", IN(5.037), IN(3.947), _W1, _H1, [paragraph([run("Programs ($)", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    for _y in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", _SW_X, IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    for _y in _LEGEND_SWATCHES2:
        out.append(text_box(n(), "LegendSwatch", _SW2_X, IN(_y), _SW2_W, _SW2_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(connector(n(), "Connector: Elbow 63", IN(8.045), IN(0.538), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 64", IN(8.045), IN(1.302), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 65", IN(8.045), IN(2.065), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "Left Brace 69", IN(7.811), IN(-1.253), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 7206"}, anchor="ctr", rot=16200000))
    out.append(text_box(n(), "Left Brace 70", IN(7.811), IN(-1.254), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 68631"}, anchor="ctr", rot=16200000))
    out.append(text_box(n(), "Rectangle 74", IN(7.072), IN(3.947), _W1, _H1, [paragraph([run("Projects ($)", size=PT(9), color=WHITE, font=FONT), run(" 1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    for _x in _LEGEND_SWATCHES3:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SW3_Y, _SW3_W, _SW3_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Rectangle 88", IN(0.425), IN(1.229), IN(2.101), _H1, [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 89", IN(0.426), IN(1.586), IN(2.1), IN(0.002), color=DK, width=12700, flip_h=True))
    out.append(text_box(n(), "Rectangle 97", IN(4.06), IN(1.371), IN(1.213), IN(0.333), [paragraph([run("Anti-Ship ", size=PT(9), color=WHITE, font=FONT), line_break(), run("Warfare", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 98", IN(11.765), IN(1.371), IN(1.213), IN(0.333), [paragraph([run("VBSS", size=PT(9), color=GRAY_3, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=GRAY_3, line_width=3175, anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _lc in _VALUE_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 112", IN(4.84), IN(1.344), IN(0.248), IN(1.902), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "TextBox 118", IN(9.301), _Y2, IN(1.448), _H2, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 120", IN(12.06), _Y2, IN(0.913), _H2, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 122", IN(7.987), _Y2, IN(1.068), _H2, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 124", IN(10.996), _Y2, IN(0.817), _H2, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "Rectangle 4", IN(9.352), IN(0.137), IN(2.201), IN(0.376), [paragraph([run("Currently manned capabilities – primary approach", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=DK, line_width=3175, anchor="ctr"))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
