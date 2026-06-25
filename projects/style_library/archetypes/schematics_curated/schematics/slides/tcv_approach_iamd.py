"""tcv_approach_iamd — Navy market-sizing deck (20251120), source slide 29.

EXHIBIT — "Approach to find TCV · IAMD (OBBBA and SHIELD)": the IAMD-specific
market-sizing build-up (Integrated Air & Missile Defense). Same left→right pattern
as the sibling USV/CMC approach slides — identify relevant OBBBA items → allocate
to domains (Maritime / Space / Ground) → allocate to kill-chain roles → Total
Funding → TAM by year → SAM → Company TCV. Operator glyphs ("+"/"=") and elbow
connectors route the build-up; two dashed boxes flag the domain- and
kill-chain-allocation percentages; a colour legend keys addressability. Header
chip: "Currently manned capabilities – OBBBA / IDIQ approach".

NOTE — the title is a layout placeholder with no explicit geometry, so the
converter kept it as a RAW <p:sp> verbatim (it inherits its position from
slideLayout4, not the source layout). It is the one bit of non-idiomatic residue
here; eyeball its placement.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ........... breadcrumb(); title = the RAW <p:sp> string (see NOTE)
  • _STEP_LABELS ..... approach-steps rail (2-6); step 1 is a standalone box
  • _LIGHT_BOXES ..... dark-text boxes — blue subtotals + grey domain/role boxes
  • _DARK_BOXES ...... white-text boxes — funding items, allocations, platforms
  • _OUTPUT_BOXES .... SAM / Company TCV (blue, DK outline)
  • _EQUALS_SIGNS .... "=" glyphs;  _PLUS_SIGNS = "+" glyphs (both were
                       converter-labelled "LegendSwatch")
  • _LEGEND_CHIPS .... addressability colour chips + caption boxes
  • standalone sp .... dashed allocation-% callout boxes, "+" glyphs, braces
  • connectors ....... elbow routing of the build-up

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=11, connector=6, picture=1, chrome_builders=1,
clusters=7 (covering 44 shapes), raw_verbatim=1 (the title placeholder),
dropped=1 (think-cell OLE frame).
Residue: a breadcrumb-like shape off the house position was kept verbatim.
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


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_STEP_X, _STEP_W, _STEP_H = IN(0.522), IN(2.385), IN(0.701)   # approach-step rail box geometry
_BOX_H = IN(0.359)        # build-up box height (dark boxes)
_EQ_X, _EQ_W, _EQ_H = IN(10.786), IN(0.4), IN(0.4)            # "=" operator column
_PLUS_W, _PLUS_H = IN(0.4), IN(0.4)   # "+" operator glyph size
_CHIP_W = IN(0.2)         # legend colour-chip width
_OP_W = IN(0.4)           # standalone "+" glyph size             [shared x4]
_LEGEND_Y = IN(1.582)     # legend caption row                    [shared x4]
_LEGEND_H = IN(0.2)       # legend caption height                 [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_STEP_LABELS = [    # (y, label) x5 — approach-step rail (steps 2-6; step 1 is standalone)
    (2.614, "2. Allocate to domains to find maritime-specific funding"),
    (4.077, "4. Multiply by FY allocations to find TAM by year"),
    (4.808, "5. Multiply by unmanned adoption rate to find SAM"),
    (5.54, "6. Multiply by Saronic market share to find Company TCV"),
    (3.345, "3. Allocate to kill chain roles to find Total Funding"),
]

_LIGHT_BOXES = [    # (x, y, cx, cy, fill, line, label) x8 — dark text: blue subtotals + grey domain/role boxes
    (11.268, 3.517, 1.867, 0.359, BLUE_1, DK, "Total Funding ($)"),
    (9.236, 2.785, 1.467, 0.359, GRAY_1, GRAY_1, "Space"),
    (7.66, 2.785, 1.467, 0.359, GRAY_1, GRAY_1, "Ground"),
    (11.268, 4.248, 1.867, 0.359, BLUE_2, DK, "TAM ($)"),
    (2.989, 4.248, 2.266, 0.359, BLUE_1, DK, "Total Funding ($)"),
    (2.989, 4.979, 2.266, 0.359, BLUE_2, DK, "TAM ($)"),
    (8.293, 3.516, 1.16, 0.359, GRAY_1, GRAY_1, "Sensors"),
    (9.543, 3.516, 1.16, 0.359, GRAY_1, GRAY_1, "Combat Sys. Integration"),
]

_DARK_BOXES = [    # (x, y, cx, fill, line, label) x13 — white text: funding items, allocations, platforms/effectors
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

_OUTPUT_BOXES = [    # (x, y, cx, cy, fill, label) x3 — SAM / Company TCV outputs (blue, DK outline)
    (11.268, 4.979, 1.867, 0.359, BLUE_3, "SAM ($)"),
    (11.268, 5.711, 1.867, 0.359, BLUE_4, "Company TCV ($)"),
    (2.989, 5.711, 2.266, 0.359, BLUE_3, "SAM ($)"),
]

_EQUALS_SIGNS = [    # (y) x6 — "=" operator glyphs down the right column
    2.765,
    4.227,
    5.69,
    4.959,
    3.496,
    2.033,
]

_PLUS_SIGNS = [    # (x, y) x5 — "+" operator glyphs
    (5.433, 2.765),
    (6.646, 4.959),
    (6.646, 5.69),
    (6.646, 4.227),
    (5.303, 3.496),
]

_LEGEND_CHIPS = [    # (x, y, cy, fill, line) x4 — addressability colour chips
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
    # ── chrome (breadcrumb only; the title is the RAW placeholder below) ──
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    # RAW verbatim (no explicit xfrm (layout placeholder)) — the title; inherits geometry from slideLayout4:
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Title 3\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"title\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr vert=\"horz\" /><a:lstStyle /><a:p><a:pPr marL=\"0\" /><a:r><a:rPr lang=\"en-US\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:rPr><a:t>Approach to find TCV | </a:t></a:r><a:r><a:rPr lang=\"en\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:rPr><a:t>IAMD (OBBBA and SHIELD)</a:t></a:r><a:endParaRPr lang=\"en-US\" dirty=\"0\"><a:solidFill><a:srgbClr val=\"000000\" /></a:solidFill></a:endParaRPr></a:p></p:txBody></p:sp>")
    # step 1 (standalone)
    out.append(text_box(n(), "Rectangle 79", IN(0.522), IN(1.882), IN(2.385), IN(0.701), [paragraph([run("1. Identify relevant OBBBA items ", size=PT(10), color=BLACK, font=FONT), run("(items shown are not exhaustive)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    # ── approach-steps rail (steps 2-6) ──
    for _y, _t in _STEP_LABELS:
        out.append(text_box(n(), "Label", _STEP_X, IN(_y), _STEP_W, _STEP_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    # ── build-up boxes: light fills, dark text ──
    for _x, _y, _cx, _cy, _fill, _lc, _t in _LIGHT_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    # ── build-up boxes: dark fills, white text ──
    for _x, _y, _cx, _fill, _lc, _t in _DARK_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _BOX_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, anchor="ctr"))
    # ── outputs: SAM / Company TCV ──
    for _x, _y, _cx, _cy, _fill, _t in _OUTPUT_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=DK, line_width=3175, anchor="ctr"))
    # ── operator glyphs: "=" column ──
    for _y in _EQUALS_SIGNS:
        out.append(text_box(n(), "LegendSwatch", _EQ_X, IN(_y), _EQ_W, _EQ_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    # ── operator glyphs: "+" ──
    for _x, _y in _PLUS_SIGNS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _PLUS_W, _PLUS_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(connector(n(), "Connector: Elbow 115", IN(7.975), IN(0.022), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 116", IN(7.975), IN(0.754), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    # dashed domain-allocation callout
    out.append(text_box(n(), "Rectangle 121", IN(6.01), IN(2.526), IN(4.741), IN(0.664), [paragraph([run("Domain allocations (%)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=DK, dashed_line=True))
    out.append(text_box(n(), "Plus Sign 131", IN(5.244), IN(2.033), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Plus Sign 132", IN(8.048), IN(2.033), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Rectangle 135", IN(0.522), IN(1.507), IN(2.291), IN(0.359), [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 136", IN(0.523), IN(1.864), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))
    out.append(connector(n(), "Connector: Elbow 137", IN(7.976), IN(-1.441), IN(0.372), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 15352"}))
    # dashed kill-chain-allocation callout
    out.append(text_box(n(), "Rectangle 140", IN(5.751), IN(3.29), IN(5.001), IN(0.616), [paragraph([run("Kill chain role allocations (%)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=DK, dashed_line=True))
    out.append(connector(n(), "Connector: Elbow 145", IN(7.975), IN(-0.71), IN(0.372), IN(8.08), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 32676"}))
    out.append(connector(n(), "Connector: Elbow 160", IN(7.975), IN(1.485), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    # ── legend: addressability colour chips + captions ──
    for _x, _y, _cy, _fill, _lc in _LEGEND_CHIPS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _CHIP_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 11", IN(9.488), _LEGEND_Y, IN(1.448), _LEGEND_H, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 13", IN(12.247), _LEGEND_Y, IN(0.913), _LEGEND_H, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 15", IN(8.174), _LEGEND_Y, IN(1.068), _LEGEND_H, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 17", IN(11.183), _LEGEND_Y, IN(0.817), _LEGEND_H, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    # ── header chip (top-right) + logo ──
    out.append(text_box(n(), "Rectangle 2", IN(9.352), IN(0.137), IN(2.201), IN(0.376), [paragraph([run("Currently manned capabilities – OBBBA / IDIQ approach", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=DK, line_width=3175, anchor="ctr"))
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
