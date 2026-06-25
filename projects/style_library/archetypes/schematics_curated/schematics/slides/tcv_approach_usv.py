"""tcv_approach_usv — Navy market-sizing deck (20251120), source slide 17.

EXHIBIT — "Approach to find TCV · USV-specified": a left→right market-sizing
build-up for unmanned (USV) funding, ending at Saronic's Company TCV. A numbered
"Approach steps" rail down the left (1 identify platforms … 5 multiply by market
share); the body works the calculation as a detailed middle chain plus a compact
right-hand summary stack (Total Funding → TAM → SAM → Company TCV, blue gradient
BLUE_1→BLUE_4), wired by "+"/"=" operator glyphs and elbow connectors. Top-right
carries an "Unmanned-specified" scope chip and a colour legend keyed to
addressability.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ........... breadcrumb() + title_placeholder()
  • _STEP_LABELS ..... the left approach-steps rail (+ the footnote Note row)
  • _LIGHT_BOXES ..... build-up boxes with dark text on light-blue fills
  • _DARK_BOXES ...... build-up boxes with white text on dark fills
  • _EQUALS_SIGNS .... "=" operator glyphs (mathEqual) — the converter labelled
                       these "LegendSwatch"; they are calc operators, not legend
  • _PLUS_SIGNS ...... "+" operator glyphs (mathPlus)
  • _LEGEND_CHIPS .... the real addressability colour legend + caption boxes
  • standalone sp .... platform inputs (sUSV/mUSV), Programs/Projects/Cost
                       Elements, adoption-rate box, grouping braces
  • connectors ....... elbow routing of the build-up

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=15, connector=4, picture=1, chrome_builders=2,
clusters=6 (covering 28 shapes), dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim (it is
the last row of _STEP_LABELS).
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


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_EQ_X, _EQ_W, _EQ_H = IN(10.843), IN(0.4), IN(0.4)     # "=" operator column (right)
_PLUS_Y, _PLUS_W, _PLUS_H = IN(2.507), IN(0.4), IN(0.4)  # "+" operator row
_CHIP_W = IN(0.2)         # legend colour-chip width
_BOX_H = IN(0.359)        # build-up box height                   [shared x6]
_OP_W = IN(0.4)           # operator-glyph size                   [shared x4]
_LEGEND_Y = IN(1.068)     # legend caption row                    [shared x4]
_LEGEND_H = IN(0.2)       # legend caption height                 [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_STEP_LABELS = [    # (x, y, cx, cy, label) x6 — approach-step rail (1-5) + footnote Note
    (0.426, 2.357, 2.101, 0.701, "2. Identify and sum corresponding budget items to find Total Funding"),
    (0.426, 3.121, 2.101, 0.701, "3. Total Funding equals TAM"),
    (0.426, 3.884, 2.101, 0.701, "4. Multiply by unmanned adoption rate to find SAM"),
    (0.426, 1.593, 2.101, 0.701, "1. Identify applicable unmanned platforms"),
    (0.426, 4.648, 2.101, 0.701, "5. Multiply by Saronic market share to find Company TCV"),
    (0.495, 6.642, 12.367, 0.354, "Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)"),
]

_LIGHT_BOXES = [    # (x, y, cx, cy, fill, label) x4 — build-up boxes, dark text on light-blue fills
    (11.46, 2.528, 1.519, 0.359, BLUE_1, "Total Funding ($)"),
    (11.46, 3.292, 1.519, 0.359, BLUE_2, "TAM ($)"),
    (3.003, 3.292, 2.549, 0.359, BLUE_1, "Total Funding ($)"),
    (3.003, 4.056, 2.549, 0.359, BLUE_2, "TAM ($)"),
]

_DARK_BOXES = [    # (x, y, cx, cy, fill, label) x7 — build-up boxes, white text on dark fills
    (11.46, 4.056, 1.519, 0.359, BLUE_3, "SAM ($)"),
    (11.46, 4.82, 1.519, 0.359, BLUE_4, "Company TCV ($)"),
    (9.106, 2.528, 1.519, 0.359, BLACK, "Cost Elements ($)"),
    (3.003, 4.819, 2.549, 0.359, BLUE_3, "SAM ($)"),
    (8.088, 4.819, 2.548, 0.359, BLACK, "Saronic market share (%)"),
    (3.003, 2.528, 1.519, 0.359, BLACK, "OBBBA items ($)"),
    (10.429, 1.764, 2.549, 0.359, BLACK, "USV Enabling Capabilities"),
]

_EQUALS_SIGNS = [    # (y) x4 — "=" operator glyphs down the right column
    2.507,
    3.271,
    4.035,
    4.799,
]

_PLUS_SIGNS = [    # (x) x3 — "+" operator glyphs across the middle row
    6.614,
    8.648,
    4.579,
]

_LEGEND_CHIPS = [    # (x, y, cy, fill, line) x4 — addressability colour chips
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
    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(title_placeholder("Approach to find TCV", "USV-specified"))
    # ── approach-steps rail (left) + footnote ──
    for _x, _y, _cx, _cy, _t in _STEP_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    # ── build-up boxes: light fills, dark text (Total Funding / TAM stages) ──
    for _x, _y, _cx, _cy, _fill, _t in _LIGHT_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    # ── build-up boxes: dark fills, white text (SAM / Company TCV / input items) ──
    for _x, _y, _cx, _cy, _fill, _t in _DARK_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    # ── platform inputs + funding-item boxes (standalone) ──
    out.append(text_box(n(), "Rectangle 41", IN(3.003), IN(1.764), IN(2.549), _BOX_H, [paragraph([run("sUSV ", size=PT(9), font=FONT), run("(incl. Corsair- and Mirage-equivalent platforms)", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 42", IN(6.716), IN(1.764), IN(2.549), _BOX_H, [paragraph([run("mUSV", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 53", IN(5.037), IN(2.528), IN(1.519), _BOX_H, [paragraph([run("Programs ($)", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    # ── operator glyphs: "=" column ──
    for _y in _EQUALS_SIGNS:
        out.append(text_box(n(), "LegendSwatch", _EQ_X, IN(_y), _EQ_W, _EQ_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    out.append(text_box(n(), "Plus Sign 59", IN(6.62), IN(4.035), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(text_box(n(), "Rectangle 61", IN(8.088), IN(4.056), IN(2.548), _BOX_H, [paragraph([run("Unmanned adoption (%)", size=PT(9), color=WHITE, font=FONT), line_break(), run("Rate: 100% ", size=PT(9), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 63", IN(8.045), IN(-0.882), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 64", IN(8.045), IN(-0.118), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Connector: Elbow 65", IN(8.045), IN(0.646), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(text_box(n(), "Plus Sign 66", IN(6.62), IN(4.799), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(text_box(n(), "Left Brace 69", IN(7.811), IN(-2.673), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 7206"}, anchor="ctr", rot=16200000))
    out.append(text_box(n(), "Left Brace 70", IN(7.811), IN(-2.673), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=3175, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 68631"}, anchor="ctr", rot=16200000))
    out.append(text_box(n(), "Rectangle 74", IN(7.072), IN(2.528), IN(1.519), _BOX_H, [paragraph([run("Projects ($)", size=PT(9), color=WHITE, font=FONT), run(" 1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    # ── operator glyphs: "+" row (diagonal mathPlus) ──
    for _x in _PLUS_SIGNS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _PLUS_Y, _PLUS_W, _PLUS_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))
    out.append(text_box(n(), "Rectangle 88", IN(0.425), IN(1.229), IN(2.101), _BOX_H, [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 89", IN(0.426), IN(1.586), IN(2.1), IN(0.002), color=DK, width=12700, flip_h=True))
    # ── legend: addressability colour chips + captions ──
    for _x, _y, _cy, _fill, _lc in _LEGEND_CHIPS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _CHIP_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 118", IN(9.301), _LEGEND_Y, IN(1.448), _LEGEND_H, [paragraph([run("Sized in another campaign", size=PT(8), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 120", IN(12.06), _LEGEND_Y, IN(0.913), _LEGEND_H, [paragraph([run("Non-a", size=PT(8), font=FONT), run("ddressable", size=PT(8), color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 122", IN(7.987), _LEGEND_Y, IN(1.068), _LEGEND_H, [paragraph([run("Included in sizing", size=PT(8), font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 124", IN(10.996), _LEGEND_Y, IN(0.817), _LEGEND_H, [paragraph([run("Future effort", size=PT(8), font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    # ── scope chip (top-right) + logo ──
    out.append(text_box(n(), "Rectangle 113", IN(9.353), IN(0.137), IN(2.2), IN(0.375), [paragraph([run("Unmanned-specified", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill="99B9D8", line_color=DK, line_width=3175, anchor="ctr"))
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
