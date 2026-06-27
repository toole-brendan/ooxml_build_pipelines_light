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
  • _STEP_RAIL_LABELS  approach-steps rail (2-6); step 1 is a standalone box
  • _FLOW_NODES ...... calculation/build-up nodes in light/dark/output style buckets
  • _OPERATOR_GLYPHS . grouped "+"/"=" math glyph positions
  • _LEGEND_KEYS ..... addressability colour chips; captions remain standalone
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
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
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
_CHIP_W = IN(0.2)         # legend colour-chip width
_OP_W = IN(0.4)           # standalone "+" glyph size             [shared x4]
_LEGEND_Y = IN(1.582)     # legend caption row                    [shared x4]
_LEGEND_H = IN(0.2)       # legend caption height                 [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the five approach-step rail cards (steps 2-6; step 1 is standalone).
_STEP_RAIL_LABELS = [    # (y, label) x5 — approach-step rail (steps 2-6; step 1 is standalone)
    (2.614, "2. Allocate to domains to find maritime-specific funding"),
    (4.077, "4. Multiply by FY allocations to find TAM by year"),
    (4.808, "5. Multiply by unmanned adoption rate to find SAM"),
    (5.54, "6. Multiply by Saronic market share to find Company TCV"),
    (3.345, "3. Allocate to kill chain roles to find Total Funding"),
]

# local_meaning: the twenty-four IAMD calculation/build-up nodes (subtotals, domain/role boxes,
#   funding items, platforms/effectors, SAM/TCV outputs); fill/line/line_width/text_color are per-
#   row fields.
_FLOW_NODES = [    # (x, y, cx, cy, fill, line, line_width, text_color, label) x24
    (11.268, 3.517, 1.867, 0.359, BLUE_1, DK, 3175, BLACK, "Total Funding ($)"),   # E2E9EF pale blue
    (9.236, 2.785, 1.467, 0.359, GRAY_1, GRAY_1, 3175, BLACK, "Space"),   # F2F2F2 off-white
    (7.66, 2.785, 1.467, 0.359, GRAY_1, GRAY_1, 3175, BLACK, "Ground"),   # F2F2F2 off-white
    (11.268, 4.248, 1.867, 0.359, BLUE_2, DK, 3175, BLACK, "TAM ($)"),   # B6C8D8 light blue
    (2.989, 4.248, 2.266, 0.359, BLUE_1, DK, 3175, BLACK, "Total Funding ($)"),   # E2E9EF pale blue
    (2.989, 4.979, 2.266, 0.359, BLUE_2, DK, 3175, BLACK, "TAM ($)"),   # B6C8D8 light blue
    (8.293, 3.516, 1.16, 0.359, GRAY_1, GRAY_1, 3175, BLACK, "Sensors"),   # F2F2F2 off-white
    (9.543, 3.516, 1.16, 0.359, GRAY_1, GRAY_1, 3175, BLACK, "Combat Sys. Integration"),   # F2F2F2 off-white
    (6.083, 2.785, 1.467, 0.359, BLACK, BLACK, 12700, WHITE, "Maritime"),   # 000000 black
    (8.436, 4.248, 2.267, 0.359, BLACK, BLACK, 12700, WHITE, "FY allocations (%)"),   # 000000 black
    (8.437, 4.979, 2.266, 0.359, BLACK, BLACK, 12700, WHITE, "Unmanned adoption (%)"),   # 000000 black
    (8.437, 5.711, 2.266, 0.359, BLACK, BLACK, 12700, WHITE, "Saronic market share (%)"),   # 000000 black
    (11.268, 2.785, 1.867, 0.359, BLACK, BLACK, 12700, WHITE, "Maritime-specific funding ($)"),   # 000000 black
    (2.989, 2.785, 2.267, 0.359, BLACK, BLACK, 12700, WHITE, "Relevant OBBBA items ($) "),   # 000000 black
    (2.989, 2.054, 2.106, 0.359, BLACK, BLACK, 12700, WHITE, "Hypersonic test bed program ($)"),   # 000000 black
    (8.597, 2.054, 2.106, 0.359, BLACK, BLACK, 12700, WHITE, "Hypersonic defense systems ($)"),   # 000000 black
    (5.793, 2.054, 2.106, 0.359, BLACK, BLACK, 12700, WHITE, "Military missile defense capabilities ($)"),   # 000000 black
    (11.268, 2.054, 1.867, 0.359, DK, DK, 12700, WHITE, "Relevant OBBBA items ($) "),   # 162029 dark navy
    (5.793, 3.516, 1.16, 0.359, BLACK, BLACK, 12700, WHITE, "Platforms"),   # 000000 black
    (2.988, 3.516, 2.266, 0.359, BLACK, BLACK, 12700, WHITE, "Maritime-specific funding ($)"),   # 000000 black
    (7.043, 3.516, 1.16, 0.359, BLACK, BLACK, 12700, WHITE, "Effectors"),   # 000000 black
    (11.268, 4.979, 1.867, 0.359, BLUE_3, DK, 3175, WHITE, "SAM ($)"),   # 6E91B1 blue
    (11.268, 5.711, 1.867, 0.359, BLUE_4, DK, 3175, WHITE, "Company TCV ($)"),   # 3D5972 dark blue
    (2.989, 5.711, 2.266, 0.359, BLUE_3, DK, 3175, WHITE, "SAM ($)"),   # 6E91B1 blue
]

# local_meaning: the eleven '=' and '+' operator glyphs; preset and rotation are per-row fields.
_OPERATOR_GLYPHS = [    # (x, y, cx, cy, preset, rotation) x11
    (10.786, 2.765, 0.4, 0.4, "mathEqual", 0),
    (10.786, 4.227, 0.4, 0.4, "mathEqual", 0),
    (10.786, 5.69, 0.4, 0.4, "mathEqual", 0),
    (10.786, 4.959, 0.4, 0.4, "mathEqual", 0),
    (10.786, 3.496, 0.4, 0.4, "mathEqual", 0),
    (10.786, 2.033, 0.4, 0.4, "mathEqual", 0),
    (5.433, 2.765, 0.4, 0.4, "mathPlus", 2572505),
    (6.646, 4.959, 0.4, 0.4, "mathPlus", 2572505),
    (6.646, 5.69, 0.4, 0.4, "mathPlus", 2572505),
    (6.646, 4.227, 0.4, 0.4, "mathPlus", 2572505),
    (5.303, 3.496, 0.4, 0.4, "mathPlus", 2572505),
]

# local_meaning: the four addressability colour chips.
_LEGEND_KEYS = [    # (x, y, cy, fill, line) x4 — addressability colour chips
    (9.265, 1.582, 0.2, "A6A6A6", "A6A6A6"),   # A6A6A6 mid-gray
    (12.023, 1.582, 0.2, None, GRAY_3),   # BFBFBF silver-gray outline
    (7.951, 1.582, 0.2, BLACK, BLACK),   # 000000 black
    (10.96, 1.582, 0.2, GRAY_1, GRAY_1),   # F2F2F2 off-white
]

# ── text layout commentary ──
# text_box(): anchor controls vertical alignment inside the shape; paragraph(..., align=...)
# controls horizontal alignment. l_ins/t_ins/r_ins/b_ins are the internal padding;
# when omitted, the primitive defaults are intentional. paragraph mar_l/indent are
# used only when a text-bearing shape needs a hanging bullet/label margin.

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
    out.append(text_box(n(), "Rectangle 79", IN(0.522), IN(1.882), IN(2.385), IN(0.701), [paragraph([run("1. Identify relevant OBBBA items ", size=PT(10), color=BLACK, font=FONT), run("(items shown are not exhaustive)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── approach-steps rail (steps 2-6) ──
    for _y, _t in _STEP_RAIL_LABELS:
        out.append(text_box(n(), "Label", _STEP_X, IN(_y), _STEP_W, _STEP_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── flow nodes — calculation/build-up boxes; rendering details are row data ──
    # anchor/align center the labels; the primitive-default insets are intentional.
    for _x, _y, _cx, _cy, _fill, _lc, _lw, _txt, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=_txt, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=_lw, anchor="ctr"))
    # ── operator glyphs — preset and rotation are carried by each row ──
    for _x, _y, _cx, _cy, _prst, _rot in _OPERATOR_GLYPHS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst=_prst, anchor="ctr", rot=_rot))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 115", IN(7.975), IN(0.022), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 116", IN(7.975), IN(0.754), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    # dashed domain-allocation callout
    out.append(text_box(n(), "Rectangle 121", IN(6.01), IN(2.526), IN(4.741), IN(0.664), [paragraph([run("Domain allocations (%)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=DK, dashed_line=True))   # 162029 dark navy outline
    out.append(text_box(n(), "Plus Sign 131", IN(5.244), IN(2.033), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Plus Sign 132", IN(8.048), IN(2.033), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Rectangle 135", IN(0.522), IN(1.507), IN(2.291), IN(0.359), [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Straight Connector 136", IN(0.523), IN(1.864), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))   # 162029 dark navy
    out.append(connector(n(), "Connector: Elbow 137", IN(7.976), IN(-1.441), IN(0.372), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 15352"}))   # 000000 black
    # dashed kill-chain-allocation callout
    out.append(text_box(n(), "Rectangle 140", IN(5.751), IN(3.29), IN(5.001), IN(0.616), [paragraph([run("Kill chain role allocations (%)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color=DK, dashed_line=True))   # 162029 dark navy outline
    out.append(connector(n(), "Connector: Elbow 145", IN(7.975), IN(-0.71), IN(0.372), IN(8.08), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 32676"}))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 160", IN(7.975), IN(1.485), IN(0.373), IN(8.079), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    # ── legend: addressability colour chips + captions ──
    for _x, _y, _cy, _fill, _lc in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _CHIP_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 11", IN(9.488), _LEGEND_Y, IN(1.448), _LEGEND_H, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 13", IN(12.247), _LEGEND_Y, IN(0.913), _LEGEND_H, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 15", IN(8.174), _LEGEND_Y, IN(1.068), _LEGEND_H, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 17", IN(11.183), _LEGEND_Y, IN(0.817), _LEGEND_H, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── header chip (top-right) + logo ──
    out.append(text_box(n(), "Rectangle 2", IN(9.352), IN(0.137), IN(2.201), IN(0.376), [paragraph([run("Currently manned capabilities – OBBBA / IDIQ approach", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=DK, line_width=3175, anchor="ctr"))   # 447BB2 blue
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
