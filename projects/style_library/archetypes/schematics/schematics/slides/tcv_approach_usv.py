"""tcv_approach_usv - Commercial Strategy deck, source slide 17.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=15, connector=4, chart=0, table=0, picture=1, chrome_builders=2, clusters=6 (covering 28 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.

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
_SW2_Y, _SW2_W, _SW2_H = IN(2.507), IN(0.4), IN(0.4)
_SW3_W = IN(0.2)
_H1 = IN(0.359)   # shared x6
_W1 = IN(0.4)   # shared x4
_Y1 = IN(1.068)   # shared x4
_H2 = IN(0.2)   # shared x4

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, cx, cy, label) x6
    (0.426, 2.357, 2.101, 0.701, "2. Identify and sum corresponding budget items to find Total Funding"),
    (0.426, 3.121, 2.101, 0.701, "3. Total Funding equals TAM"),
    (0.426, 3.884, 2.101, 0.701, "4. Multiply by unmanned adoption rate to find SAM"),
    (0.426, 1.593, 2.101, 0.701, "1. Identify applicable unmanned platforms"),
    (0.426, 4.648, 2.101, 0.701, "5. Multiply by Saronic market share to find Company TCV"),
    (0.495, 6.642, 12.367, 0.354, "Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)"),
]

_LABELS2 = [    # (x, y, cx, cy, fill, label) x4
    (11.46, 2.528, 1.519, 0.359, BLUE_1, "Total Funding ($)"),
    (11.46, 3.292, 1.519, 0.359, BLUE_2, "TAM ($)"),
    (3.003, 3.292, 2.549, 0.359, BLUE_1, "Total Funding ($)"),
    (3.003, 4.056, 2.549, 0.359, BLUE_2, "TAM ($)"),
]

_LABELS3 = [    # (x, y, cx, cy, fill, label) x7
    (11.46, 4.056, 1.519, 0.359, BLUE_3, "SAM ($)"),
    (11.46, 4.82, 1.519, 0.359, BLUE_4, "Company TCV ($)"),
    (9.106, 2.528, 1.519, 0.359, BLACK, "Cost Elements ($)"),
    (3.003, 4.819, 2.549, 0.359, BLUE_3, "SAM ($)"),
    (8.088, 4.819, 2.548, 0.359, BLACK, "Saronic market share (%)"),
    (3.003, 2.528, 1.519, 0.359, BLACK, "OBBBA items ($)"),
    (10.429, 1.764, 2.549, 0.359, BLACK, "USV Enabling Capabilities"),
]

_LEGEND_SWATCHES = [    # (y) x4
    2.507,
    3.271,
    4.035,
    4.799,
]

_LEGEND_SWATCHES2 = [    # (x) x3
    6.614,
    8.648,
    4.579,
]

_LEGEND_SWATCHES3 = [    # (x, y, cy, fill, line) x4
    (9.078, 1.068, 0.2, "A6A6A6", "A6A6A6"),
    (11.836, 1.068, 0.2, None, GRAY_3),
    (7.764, 1.068, 0.2, BLACK, BLACK),
    (10.773, 1.068, 0.2, GRAY_1, GRAY_1),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(title_placeholder("Approach to find TCV", "USV-specified"))
    for _x, _y, _cx, _cy, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 41", IN(3.003), IN(1.764), IN(2.549), _H1, [paragraph([run("sUSV ", size=PT(9), font=FONT), run("(incl. Corsair- and Mirage-equivalent platforms)", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 42", IN(6.716), IN(1.764), IN(2.549), _H1, [paragraph([run("mUSV", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 53", IN(5.037), IN(2.528), IN(1.519), _H1, [paragraph([run("Programs ($)", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    for _y in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", _SW_X, IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    out.append(text_box(n(), "Plus Sign 59", IN(6.62), IN(4.035), _W1, _W1, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(text_box(n(), "Rectangle 61", IN(8.088), IN(4.056), IN(2.548), _H1, [paragraph([run("Unmanned adoption (%)", size=PT(9), color=WHITE, font=FONT), line_break(), run("Rate: 100% ", size=PT(9), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 63", IN(8.045), IN(-0.882), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 64", IN(8.045), IN(-0.118), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 65", IN(8.045), IN(0.646), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "Plus Sign 66", IN(6.62), IN(4.799), _W1, _W1, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(text_box(n(), "Left Brace 69", IN(7.811), IN(-2.673), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 7206"}, anchor="ctr", rot=16200000))
    out.append(text_box(n(), "Left Brace 70", IN(7.811), IN(-2.673), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=3175, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 68631"}, anchor="ctr", rot=16200000))
    out.append(text_box(n(), "Rectangle 74", IN(7.072), IN(2.528), IN(1.519), _H1, [paragraph([run("Projects ($)", size=PT(9), color=WHITE, font=FONT), run(" 1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    for _x in _LEGEND_SWATCHES2:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SW2_Y, _SW2_W, _SW2_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Rectangle 88", IN(0.425), IN(1.229), IN(2.101), _H1, [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 89", IN(0.426), IN(1.586), IN(2.1), IN(0.002), color=DK, width=12700, flip_h=True))
    for _x, _y, _cy, _fill, _lc in _LEGEND_SWATCHES3:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW3_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 118", IN(9.301), _Y1, IN(1.448), _H2, [paragraph([run("Sized in another campaign", size=PT(8), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 120", IN(12.06), _Y1, IN(0.913), _H2, [paragraph([run("Non-a", size=PT(8), font=FONT), run("ddressable", size=PT(8), color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 122", IN(7.987), _Y1, IN(1.068), _H2, [paragraph([run("Included in sizing", size=PT(8), font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 124", IN(10.996), _Y1, IN(0.817), _H2, [paragraph([run("Future effort", size=PT(8), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "Rectangle 113", IN(9.353), IN(0.137), IN(2.2), IN(0.375), [paragraph([run("Unmanned-specified", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill="99B9D8", line_color=DK, line_width=3175, anchor="ctr"))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
