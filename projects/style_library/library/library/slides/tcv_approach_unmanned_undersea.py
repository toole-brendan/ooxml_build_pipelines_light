"""tcv_approach_unmanned_undersea — Market sizing Navy (Undersea) deck (20251201), source slide 15.

EXHIBIT — "Approach to find TCV · Unmanned-specified": a left-to-right TCV build-up
diagram (boxes + operator glyphs + connectors, no chart). A left spine lists the
five approach steps (1 Identify applicable unmanned platforms → 2 sum budget items
to Total Funding → 3 Total Funding = TAM → 4 × unmanned adoption = SAM → 5 ×
Saronic market share = Company TCV). The flow itself reads across the slide: UUV
platform inputs (S/M · Large/XL · Wave-powered UUV · Core Technologies) feed
OBBBA-item / Programs / Projects / Cost-Element budget boxes that sum (via "=" /
"+" glyphs and elbow + brace connectors) into blue Total Funding and TAM boxes,
then into SAM and Company TCV outputs. A top-right addressability legend
(Included in sizing · Sized in another campaign · Future effort · Non-addressable)
and an "Unmanned-specified" scope chip frame the exhibit; a footnote closes it.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place — groups
interleave):
  • chrome ............ breadcrumb() + title_placeholder() (house builders)
  • _STEP_RAIL_LABELS  left-spine approach steps 1–5 → loop
  • _ANNOTATION_BOXES  off-house footnote / note row
  • _FLOW_NODES ...... calculation/build-up boxes; fill, outline, and text contrast
                       are row fields
  • _OPERATOR_GLYPHS . grouped "+"/"=" math glyphs; source cNvPr names are kept
                       verbatim even when they say "LegendSwatch"; two standalone
                       "+" signs + the elbow/brace connectors interleave nearby
  • Programs/Projects . standalone black budget boxes with footnote-marker runs
  • spine header ..... "Approach steps" label + its underline rule
  • _LEGEND_KEYS .... the 4 addressability colour chips → loop; their caption
                       text boxes are standalone and follow immediately
  • scope chip + logo  "Unmanned-specified" chip (top-right) + picture() (IMAGES rId2)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=12, connector=4, picture=1, chrome_builders=2,
clusters=6 (covering 32 shapes), dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_1, BLUE_2, BLUE_3, BLUE_4, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image6_3071a231.jpeg"},
]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_EQ_X, _EQ_W, _EQ_H = IN(10.843), IN(0.4), IN(0.4)     # "=" glyph column x / size
_PLUS_Y, _PLUS_W, _PLUS_H = IN(2.507), IN(0.4), IN(0.4)  # row-2 "+" glyph y / size
_SWATCH_W = IN(0.2)       # legend colour-chip width
_PLUS_SZ = IN(0.4)        # standalone "+" glyph size              [shared x4]
_LEGEND_Y = IN(1.068)     # legend row (chips + captions)          [shared x4]
_LEGEND_H = IN(0.2)       # legend row height                      [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the five left-spine approach steps.
_STEP_RAIL_LABELS = [    # (x, y, cx, cy, label) x5 — left-spine approach steps
    (0.425, 2.357, 2.101, 0.701, "2. Identify and sum corresponding budget items to find Total Funding"),
    (0.425, 3.121, 2.101, 0.701, "3. Total Funding equals TAM"),
    (0.425, 3.884, 2.101, 0.701, "4. Multiply by unmanned adoption rate to find SAM"),
    (0.425, 1.593, 2.101, 0.701, "1. Identify applicable unmanned platforms"),
    (0.425, 4.648, 2.101, 0.701, "5. Multiply by Saronic market share to find Company TCV"),
]

# local_meaning: the off-house footnote/note row.
_ANNOTATION_BOXES = [    # (x, y, cx, cy, label) x1 — off-house footnote / note row
    (0.495, 6.642, 12.367, 0.354, "Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)"),
]

# local_meaning: the fifteen UUV calculation/build-up nodes (running totals plus UUV inputs,
#   budget items, factors, SAM/TCV outputs); fill/line/text_color are per-row fields.
_FLOW_NODES = [    # (x, y, cx, cy, fill, line, text_color, label) x15 — calculation / build-up nodes; style is row data
    (11.46, 2.528, 1.519, 0.359, BLUE_1, BLACK, BLACK, "Total Funding ($)"),   # E2E9EF pale blue
    (11.46, 3.292, 1.519, 0.359, BLUE_2, BLACK, BLACK, "TAM ($)"),   # B6C8D8 light blue
    (3.003, 3.292, 2.549, 0.359, BLUE_1, BLACK, BLACK, "Total Funding ($)"),   # E2E9EF pale blue
    (3.003, 4.056, 2.549, 0.359, BLUE_2, BLACK, BLACK, "TAM ($)"),   # B6C8D8 light blue
    (11.46, 4.056, 1.519, 0.359, BLUE_3, BLACK, WHITE, "SAM ($)"),   # 6E91B1 blue
    (11.46, 4.82, 1.519, 0.359, BLUE_4, BLACK, WHITE, "Company TCV ($)"),   # 3D5972 dark blue
    (3.003, 1.764, 1.519, 0.359, BLACK, "A6A6A6", WHITE, "S/M UUV"),   # 000000 black
    (5.821, 1.764, 1.519, 0.359, BLACK, BLACK, WHITE, "Large / XL UUV"),   # 000000 black
    (9.106, 2.528, 1.519, 0.359, BLACK, BLACK, WHITE, "Cost Elements ($)"),   # 000000 black
    (8.088, 4.056, 2.548, 0.359, BLACK, BLACK, WHITE, "Unmanned adoption (%) - 100% "),   # 000000 black
    (3.003, 4.819, 2.549, 0.359, BLUE_3, BLACK, WHITE, "SAM ($)"),   # 6E91B1 blue
    (8.088, 4.819, 2.548, 0.359, BLACK, BLACK, WHITE, "Saronic market share (%)"),   # 000000 black
    (3.003, 2.528, 1.519, 0.359, BLACK, BLACK, WHITE, "OBBBA items ($)"),   # 000000 black
    (8.64, 1.764, 1.519, 0.359, BLACK, BLACK, WHITE, "Wave-powered UUV"),   # 000000 black
    (11.459, 1.764, 1.519, 0.359, BLACK, BLACK, WHITE, "Core Technologies"),   # 000000 black
]

# local_meaning: the '=' x4 and '+' x3 operator glyphs.
_OPERATOR_GLYPHS = {
    "equals_column": [    # (y) x4 — "=" operator glyphs in the right column
        2.507,
        3.271,
        4.035,
        4.799,
    ],
    "plus_row": [    # (x) x3 — row-2 "+" operator glyphs
        6.614,
        8.648,
        4.579,
    ],
}

# local_meaning: the four addressability colour chips.
_LEGEND_KEYS = [    # (x, y, cy, fill, line) x4 — addressability colour chips
    (9.078, 1.068, 0.2, "A6A6A6", "A6A6A6"),   # A6A6A6 mid-gray
    (11.836, 1.068, 0.2, None, GRAY_3),   # BFBFBF silver-gray outline
    (7.764, 1.068, 0.2, BLACK, BLACK),   # 000000 black
    (10.773, 1.068, 0.2, GRAY_1, GRAY_1),   # F2F2F2 off-white
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
    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Navy (Undersea)"))
    out.append(title_placeholder("Approach to find TCV", "Unmanned-specified"))
    # ── left-spine approach steps 1–5, then the off-house footnote ──
    # Shape text: anchor="ctr" vertically centers the label; paragraph default align
    # is left for the rail; text_box internal padding uses primitive defaults.
    for _x, _y, _cx, _cy, _t in _STEP_RAIL_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    for _x, _y, _cx, _cy, _t in _ANNOTATION_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── flow nodes: calculation/build-up boxes; fill, outline, and text contrast are row fields ──
    # Shape text: centered vertically (anchor="ctr") and horizontally (align="ctr");
    # internal padding uses primitive defaults because the nodes are compact but single-line.
    for _x, _y, _cx, _cy, _fill, _lc, _txt, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=_txt, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 53", IN(5.037), IN(2.528), IN(1.519), IN(0.359), [paragraph([run("Programs ($)", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    # ── operator glyphs + flow connectors (interleave with boxes in paint order) ──
    for _y in _OPERATOR_GLYPHS["equals_column"]:
        out.append(text_box(n(), "LegendSwatch", _EQ_X, IN(_y), _EQ_W, _EQ_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Plus Sign 59", IN(6.629), IN(4.035), _PLUS_SZ, _PLUS_SZ, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 63", IN(8.045), IN(-0.882), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 64", IN(8.045), IN(-0.118), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 65", IN(8.045), IN(0.646), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Plus Sign 66", IN(6.629), IN(4.799), _PLUS_SZ, _PLUS_SZ, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))   # 000000 black
    out.append(text_box(n(), "Left Brace 69", IN(7.811), IN(-2.673), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 7206"}, anchor="ctr", rot=16200000))   # 000000 black outline
    out.append(text_box(n(), "Left Brace 70", IN(7.811), IN(-2.673), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=3175, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 68631"}, anchor="ctr", rot=16200000))   # 000000 black outline
    out.append(text_box(n(), "Rectangle 74", IN(7.072), IN(2.528), IN(1.519), IN(0.359), [paragraph([run("Projects ($)", size=PT(9), color=WHITE, font=FONT), run(" 1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    for _x in _OPERATOR_GLYPHS["plus_row"]:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _PLUS_Y, _PLUS_W, _PLUS_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))   # 000000 black
    # ── "Approach steps" spine header + its underline rule ──
    out.append(text_box(n(), "Rectangle 88", IN(0.425), IN(1.229), IN(2.101), IN(0.359), [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Straight Connector 89", IN(0.426), IN(1.586), IN(2.1), IN(0.002), color=DK, width=12700, flip_h=True))   # 162029 dark navy
    # ── addressability legend (top-right): colour chips, then their captions ──
    for _x, _y, _cy, _fill, _lc in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SWATCH_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 118", IN(9.301), _LEGEND_Y, IN(1.448), _LEGEND_H, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 120", IN(12.06), _LEGEND_Y, IN(0.913), _LEGEND_H, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 122", IN(7.987), _LEGEND_Y, IN(1.068), _LEGEND_H, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 124", IN(10.996), _LEGEND_Y, IN(0.817), _LEGEND_H, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── scope chip (top-right) + logo ──
    out.append(text_box(n(), "Rectangle 113", IN(9.121), IN(0.074), IN(2.663), IN(0.5), [paragraph([run("Unmanned-specified", size=PT(12), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill="99B9D8", line_color=DK, line_width=3175, anchor="ctr"))   # 99B9D8 light blue
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
