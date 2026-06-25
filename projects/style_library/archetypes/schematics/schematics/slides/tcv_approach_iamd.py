"""tcv_approach_iamd - Commercial Strategy deck, source slide 29.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=11, connector=6, chart=0, table=0, picture=1, chrome_builders=1, clusters=7 (covering 44 shapes), raw_verbatim=1, dropped=1, frozen_fields=0.

Converter notes:
  - breadcrumb-like shape off house position - kept verbatim
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, breadcrumb,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]


# ── layout anchors (shared coordinates) ──
_LBL_X, _LBL_W, _LBL_H = IN(0.522), IN(2.385), IN(0.701)
_LBL3_H = IN(0.359)
_SW_X, _SW_W, _SW_H = IN(10.786), IN(0.4), IN(0.4)
_SW2_W, _SW2_H = IN(0.4), IN(0.4)
_SW3_W = IN(0.2)
_W1 = IN(0.4)   # shared x4
_Y1 = IN(1.582)   # shared x4
_H1 = IN(0.2)   # shared x4

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (y, label) x5
    (2.614, "2. Allocate to domains to find maritime-specific funding"),
    (4.077, "4. Multiply by FY allocations to find TAM by year"),
    (4.808, "5. Multiply by unmanned adoption rate to find SAM"),
    (5.54, "6. Multiply by Saronic market share to find Company TCV"),
    (3.345, "3. Allocate to kill chain roles to find Total Funding"),
]

_LABELS2 = [    # (x, y, cx, cy, fill, line, label) x8
    (11.268, 3.517, 1.867, 0.359, BLUE_1, DK, "Total Funding ($)"),
    (9.236, 2.785, 1.467, 0.359, GRAY_1, GRAY_1, "Space"),
    (7.66, 2.785, 1.467, 0.359, GRAY_1, GRAY_1, "Ground"),
    (11.268, 4.248, 1.867, 0.359, BLUE_2, DK, "TAM ($)"),
    (2.989, 4.248, 2.266, 0.359, BLUE_1, DK, "Total Funding ($)"),
    (2.989, 4.979, 2.266, 0.359, BLUE_2, DK, "TAM ($)"),
    (8.293, 3.516, 1.16, 0.359, GRAY_1, GRAY_1, "Sensors"),
    (9.543, 3.516, 1.16, 0.359, GRAY_1, GRAY_1, "Combat Sys. Integration"),
]

_LABELS3 = [    # (x, y, cx, fill, line, label) x13
    (6.083, 2.785, 1.467, BLACK, BLACK, "Maritime"),
    (8.436, 4.248, 2.267, BLACK, BLACK, "FY allocations (%)"),
    (8.437, 4.979, 2.266, BLACK, BLACK, "Unmanned adoption (%)"),
    (8.437, 5.711, 2.266, BLACK, BLACK, "Saronic market share (%)"),
    (11.268, 2.785, 1.867, BLACK, BLACK, "Maritime-specific funding ($)"),
    (2.989, 2.785, 2.267, BLACK, BLACK, "Relevant OBBBA items ($) "),
    (2.989, 2.054, 2.106, BLACK, BLACK, "Hypersonic test bed program ($)"),
    (8.597, 2.054, 2.106, BLACK, BLACK, "Hypersonic defense systems ($)"),
    (5.793, 2.054, 2.106, BLACK, BLACK, "Military missile defense capabilities ($)"),
    (11.268, 2.054, 1.867, DK, DK, "Relevant OBBBA items ($) "),
    (5.793, 3.516, 1.16, BLACK, BLACK, "Platforms"),
    (2.988, 3.516, 2.266, BLACK, BLACK, "Maritime-specific funding ($)"),
    (7.043, 3.516, 1.16, BLACK, BLACK, "Effectors"),
]

_LABELS4 = [    # (x, y, cx, cy, fill, label) x3
    (11.268, 4.979, 1.867, 0.359, BLUE_3, "SAM ($)"),
    (11.268, 5.711, 1.867, 0.359, BLUE_4, "Company TCV ($)"),
    (2.989, 5.711, 2.266, 0.359, BLUE_3, "SAM ($)"),
]

_LEGEND_SWATCHES = [    # (y) x6
    2.765,
    4.227,
    5.69,
    4.959,
    3.496,
    2.033,
]

_LEGEND_SWATCHES2 = [    # (x, y) x5
    (5.433, 2.765),
    (6.646, 4.959),
    (6.646, 5.69),
    (6.646, 4.227),
    (5.303, 3.496),
]

_LEGEND_SWATCHES3 = [    # (x, y, cy, fill, line) x4
    (9.265, 1.582, 0.2, "A6A6A6", "A6A6A6"),
    (12.023, 1.582, 0.2, None, GRAY_3),
    (7.951, 1.582, 0.2, BLACK, BLACK),
    (10.96, 1.582, 0.2, GRAY_1, GRAY_1),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    # RAW verbatim (no explicit xfrm (layout placeholder)):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Title 3\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"title\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr vert=\"horz\" /><a:lstStyle /><a:p><a:pPr marL=\"0\" /><a:r><a:rPr lang=\"en-US\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:rPr><a:t>Approach to find TCV | </a:t></a:r><a:r><a:rPr lang=\"en\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:rPr><a:t>IAMD (OBBBA and SHIELD)</a:t></a:r><a:endParaRPr lang=\"en-US\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:endParaRPr></a:p></p:txBody></p:sp>")
    out.append(text_box(n(), "Rectangle 79", IN(0.522), IN(1.882), IN(2.385), IN(0.701), [paragraph([run("1. Identify relevant OBBBA items ", size=PT(10), color=BLACK, font=FONT), run("(items shown are not exhaustive)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    for _y, _t in _LABELS:
        out.append(text_box(n(), "Label", _LBL_X, IN(_y), _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _lc, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    for _x, _y, _cx, _fill, _lc, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL3_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _t in _LABELS4:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=DK, line_width=3175, anchor="ctr"))
    for _y in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", _SW_X, IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    for _x, _y in _LEGEND_SWATCHES2:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW2_W, _SW2_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(connector(n(), "Connector: Elbow 115", IN(7.975), IN(0.022), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 116", IN(7.975), IN(0.754), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "Rectangle 121", IN(6.01), IN(2.526), IN(4.741), IN(0.664), [paragraph([run("Domain allocations (%)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=DK, dashed_line=True))
    out.append(text_box(n(), "Plus Sign 131", IN(5.244), IN(2.033), _W1, _W1, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Plus Sign 132", IN(8.048), IN(2.033), _W1, _W1, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Rectangle 135", IN(0.522), IN(1.507), IN(2.291), IN(0.359), [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 136", IN(0.523), IN(1.864), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))
    out.append(connector(n(), "Connector: Elbow 137", IN(7.976), IN(-1.441), IN(0.372), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 15352"}))
    out.append(text_box(n(), "Rectangle 140", IN(5.751), IN(3.29), IN(5.001), IN(0.616), [paragraph([run("Kill chain role allocations (%)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=DK, dashed_line=True))
    out.append(connector(n(), "Connector: Elbow 145", IN(7.975), IN(-0.71), IN(0.372), IN(8.08), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 32676"}))
    out.append(connector(n(), "Connector: Elbow 160", IN(7.975), IN(1.485), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    for _x, _y, _cy, _fill, _lc in _LEGEND_SWATCHES3:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW3_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 11", IN(9.488), _Y1, IN(1.448), _H1, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 13", IN(12.247), _Y1, IN(0.913), _H1, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 15", IN(8.174), _Y1, IN(1.068), _H1, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 17", IN(11.183), _Y1, IN(0.817), _H1, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "Rectangle 2", IN(9.352), IN(0.137), IN(2.201), IN(0.376), [paragraph([run("Currently manned capabilities – OBBBA / IDIQ approach", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=DK, line_width=3175, anchor="ctr"))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
