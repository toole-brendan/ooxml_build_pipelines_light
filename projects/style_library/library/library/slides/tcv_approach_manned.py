"""tcv_approach_manned — Navy market-sizing deck (20251120), source slide 18.

EXHIBIT — "Approach to find TCV · Currently manned capabilities (CMC)": the CMC
market-sizing build-up. A 7-step approach rail on the left; the body maps mission
areas (Anti-Air Warfare, ASW, …) and ship classes (Ticonderoga, Arleigh Burke,
Zumwalt, Constellation, Avenger) onto platforms/effectors, then rolls
Programs/Projects/Cost-Elements up through Total Funding → TAM → SAM → Company TCV
(blue-gradient summary stack on the right, repeated as a worked middle chain).
Operator glyphs ("+"/"="), elbow connectors and brace groupings route it; a colour
legend keys addressability. Header chip: "Currently manned capabilities – primary
approach". This is the densest schematic in the set (52 shapes collapsed to 7
loops).

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder()
  • _STEP_RAIL_LABELS  left approach-steps rail (1-7)
  • _ANNOTATION_BOXES  off-house footnote / note row
  • _FLOW_NODES ...... calculation/build-up nodes; fill, outline, and text contrast
                        are row fields
  • _GRID_CELLS ...... mission-area grid chips pulled out of the old style cluster
  • _OPERATOR_GLYPHS . grouped "+"/"=" math glyphs; source cNvPr names are kept
                        verbatim even when they say "LegendSwatch"
  • _GRID_FRAME ...... single mission-grid outline box
  • _LEGEND_KEYS ..... addressability colour chips
  • standalone sp ..... ship-class boxes, Programs/Projects, brace groupings
  • connectors ........ elbow routing from missions/ships down to the build-up

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=17, connector=11, picture=1, chrome_builders=2,
clusters=7 (covering 52 shapes), dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
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
_EQ_X, _EQ_W, _EQ_H = IN(10.843), IN(0.4), IN(0.4)          # "=" operator column
_PLUS_X, _PLUS_W, _PLUS_H = IN(6.629), IN(0.4), IN(0.4)     # "+" operator column
_PLUSROW_Y, _PLUSROW_W, _PLUSROW_H = IN(3.927), IN(0.4), IN(0.4)  # "+" operator row
_SHIP_Y = IN(3.183)       # ship-class row y                     [shared x5]
_BOX_W = IN(1.519)        # build-up box width                   [shared x7]
_BOX_H = IN(0.359)        # build-up box height                  [shared x8]
_ELBOW_W = IN(0.405)      # elbow-connector width                [shared x6]
_LEGEND_Y = IN(1.068)     # legend caption row                   [shared x4]
_LEGEND_H = IN(0.2)       # legend caption height                [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the seven approach-step rail cards.
_STEP_RAIL_LABELS = [    # (x, y, cx, cy, label) x7 — approach-step rail
    (0.426, 1.484, 2.101, 0.701, "1. Identify missions"),
    (0.426, 2.248, 2.101, 0.701, "2. Identify priority kill chain roles"),
    (0.426, 3.776, 2.101, 0.701, "4. Identify and sum corresponding budget items to find Total Funding"),
    (0.426, 4.54, 2.101, 0.701, "5. Allocate platforms and effectors to missions to find TAM"),
    (0.426, 5.304, 2.101, 0.701, "6. Multiply by unmanned adoption rate to find SAM"),
    (0.426, 3.012, 2.101, 0.701, "3. Identify specific platforms / effectors for missions"),
    (0.426, 6.068, 2.101, 0.701, "7. Multiply by Saronic market share to find Company TCV"),
]

# local_meaning: the off-house footnote/note row.
_ANNOTATION_BOXES = [    # (x, y, cx, cy, label) x1 — off-house footnote / note row
    (0.495, 6.642, 12.367, 0.354, "Note: (1) Programs and Projects included where relevant (e.g., no Cost Elements or Cost Elements in FY26 PBR account for small fraction of total Program/Project funds)"),
]

# local_meaning: the seventeen TCV calculation/build-up nodes (blue subtotals, grey role boxes,
#   SAM/TCV/platform/input boxes); fill/line/text_color are per-row fields.
_FLOW_NODES = [    # (x, y, cx, cy, fill, line, text_color, label) x17 — calculation/build-up nodes; style is row data
    (11.46, 3.947, 1.519, 0.359, BLUE_1, BLACK, BLACK, "Total Funding ($)"),   # E2E9EF pale blue
    (11.46, 4.711, 1.519, 0.359, BLUE_2, BLACK, BLACK, "TAM ($)"),   # B6C8D8 light blue
    (10.956, 2.419, 2.022, 0.359, GRAY_1, GRAY_1, BLACK, "Combat Systems Integration (incl. CEC)"),   # F2F2F2 off-white
    (8.306, 2.419, 2.022, 0.359, GRAY_1, GRAY_1, BLACK, "Sensors"),   # F2F2F2 off-white
    (3.003, 4.711, 2.549, 0.359, BLUE_1, BLACK, BLACK, "Total Funding ($)"),   # E2E9EF pale blue
    (3.003, 5.475, 2.549, 0.359, BLUE_2, BLACK, BLACK, "TAM ($)"),   # B6C8D8 light blue
    (5.656, 2.419, 2.022, 0.359, GRAY_1, GRAY_1, BLACK, "Effectors"),   # F2F2F2 off-white
    (11.46, 5.475, 1.519, 0.359, BLUE_3, BLACK, WHITE, "SAM ($)"),   # 6E91B1 blue
    (11.46, 6.239, 1.519, 0.359, BLUE_4, BLACK, WHITE, "Company TCV ($)"),   # 3D5972 dark blue
    (3.003, 2.419, 2.022, 0.359, BLACK, BLACK, WHITE, "Platforms"),   # 000000 black
    (9.768, 3.183, 1.519, 0.359, BLACK, BLACK, WHITE, "Littoral Combat Ship"),   # 000000 black
    (9.106, 3.947, 1.519, 0.359, BLACK, BLACK, WHITE, "Cost Elements ($)"),   # 000000 black
    (8.077, 4.711, 2.548, 0.359, BLACK, BLACK, WHITE, "Mission allocations by platform and effector (%)"),   # 000000 black
    (8.088, 5.475, 2.548, 0.359, BLACK, BLACK, WHITE, "Unmanned adoption (%)"),   # 000000 black
    (3.003, 6.239, 2.549, 0.359, BLUE_3, BLACK, WHITE, "SAM ($)"),   # 6E91B1 blue
    (8.088, 6.239, 2.548, 0.359, BLACK, BLACK, WHITE, "Saronic market share (%)"),   # 000000 black
    (3.003, 3.947, 1.519, 0.359, BLACK, BLACK, WHITE, "OBBBA items ($)"),   # 000000 black
]

# local_meaning: the twelve mission-area grid cells.
_GRID_CELLS = [    # (x, y, cx, cy, fill, line, text_color, label) x12 — mission-area grid cells
    (2.777, 1.371, 1.213, 0.333, BLACK, BLACK, WHITE, "Anti-Air Warfare (incl. cUAS)"),   # 000000 black
    (5.344, 1.371, 1.213, 0.333, BLACK, BLACK, WHITE, "Anti-Submarine Warfare"),   # 000000 black
    (9.196, 1.371, 1.213, 0.333, "A6A6A6", "A6A6A6", WHITE, "Amphibious Warfare"),   # A6A6A6 mid-gray
    (6.629, 1.371, 1.212, 0.333, BLACK, BLACK, WHITE, "Ballistic Missile Defense"),   # 000000 black
    (7.912, 1.371, 1.213, 0.333, BLACK, BLACK, WHITE, "Electronic Warfare (D&D)"),   # 000000 black
    (5.344, 1.772, 1.213, 0.333, BLACK, BLACK, WHITE, "Mine Warfare"),   # 000000 black
    (9.196, 1.772, 1.213, 0.333, "A6A6A6", "A6A6A6", WHITE, "Special Operations"),   # A6A6A6 mid-gray
    (10.48, 1.772, 1.213, 0.333, "A6A6A6", "A6A6A6", WHITE, "Sealift"),   # A6A6A6 mid-gray
    (6.629, 1.774, 1.213, 0.333, BLACK, BLACK, WHITE, "Strike Warfare"),   # 000000 black
    (4.06, 1.772, 1.213, 0.333, BLACK, BLACK, WHITE, "ISR"),   # 000000 black
    (10.48, 1.371, 1.214, 0.333, "A6A6A6", "A6A6A6", WHITE, "C4"),   # A6A6A6 mid-gray
    (2.777, 1.778, 1.213, 0.333, BLACK, BLACK, WHITE, "Electronic Warfare (Other)"),   # 000000 black
]

# local_meaning: the '=' and '+' operator glyphs (column and row '+' runs).
_OPERATOR_GLYPHS = {
    "equals_column": [    # (y) x4 — "=" operator glyphs down the right column
        3.927,
        4.691,
        5.454,
        6.218,
    ],
    "plus_column": [    # (y) x3 — "+" operator glyphs stacked in a column
        4.691,
        5.454,
        6.218,
    ],
    "plus_row": [    # (x) x3 — "+" operator glyphs across a row
        6.614,
        8.648,
        4.579,
    ],
}

_GRID_FRAME = (2.667, 1.312, 6.497, 0.859, None, BLACK)  # mission-grid outline box

# local_meaning: the four addressability colour chips.
_LEGEND_KEYS = [    # (x, y, cx, cy, fill, line) x4 — addressability colour chips
    (9.078, 1.068, 0.2, 0.2, "A6A6A6", "A6A6A6"),   # A6A6A6 mid-gray
    (11.836, 1.068, 0.2, 0.2, None, GRAY_3),   # BFBFBF silver-gray outline
    (7.764, 1.068, 0.2, 0.2, BLACK, BLACK),   # 000000 black
    (10.773, 1.068, 0.2, 0.2, GRAY_1, GRAY_1),   # F2F2F2 off-white
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
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(title_placeholder("Approach to find TCV", "Currently manned capabilities"))
    # ── approach-steps rail (left), then the off-house footnote ──
    # Shape text: anchor="ctr" vertically centers the label; paragraph default align
    # is left for the rail; text_box internal padding uses primitive defaults.
    for _x, _y, _cx, _cy, _t in _STEP_RAIL_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    for _x, _y, _cx, _cy, _t in _ANNOTATION_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── flow nodes: calculation/build-up boxes; fill, outline, and text contrast are row fields ──
    # Shape text: centered vertically (anchor="ctr") and horizontally (align="ctr");
    # internal padding uses primitive defaults because these nodes are compact but single-line.
    for _x, _y, _cx, _cy, _fill, _lc, _txt, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=_txt, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    # ── grid cells: mission-area chips from the old dark style cluster ──
    for _x, _y, _cx, _cy, _fill, _lc, _txt, _t in _GRID_CELLS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(9), color=_txt, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    # ── ship classes (standalone) ──
    out.append(text_box(n(), "Rectangle 41", IN(3.003), _SHIP_Y, _BOX_W, _BOX_H, [paragraph([run("Ticonderoga", size=PT(9), italic=True, font=FONT), run("-class cruisers", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 42", IN(4.694), _SHIP_Y, _BOX_W, _BOX_H, [paragraph([run("Arleigh Burke", size=PT(9), italic=True, font=FONT), run("-class destroyers", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 43", IN(6.385), _SHIP_Y, _BOX_W, _BOX_H, [paragraph([run("Zumwalt", size=PT(9), italic=True, font=FONT), run("-class destroyers", size=PT(9), font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 44", IN(8.077), _SHIP_Y, _BOX_W, _BOX_H, [paragraph([run("Constellation-", size=PT(9), italic=True, color=WHITE, font=FONT), run("class frigates", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 46", IN(11.46), _SHIP_Y, _BOX_W, _BOX_H, [paragraph([run("Avenger", size=PT(9), bold=True, italic=True, color=WHITE, font=FONT), run("-class MCM ship", size=PT(9), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    # ── elbow connectors: missions/ships → platforms ──
    out.append(connector(n(), "Connector: Elbow 47", IN(3.685), IN(2.855), _ELBOW_W, IN(0.252), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 48", IN(4.531), IN(2.261), _ELBOW_W, IN(1.44), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 49", IN(5.377), IN(1.415), _ELBOW_W, IN(3.131), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 50", IN(7.914), IN(-1.122), _ELBOW_W, IN(8.205), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 51", IN(7.068), IN(-0.276), _ELBOW_W, IN(6.514), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 52", IN(6.222), IN(0.57), _ELBOW_W, IN(4.822), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(text_box(n(), "Rectangle 53", IN(5.037), IN(3.947), _BOX_W, _BOX_H, [paragraph([run("Programs ($)", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    # ── operator glyphs: "=" column ──
    for _y in _OPERATOR_GLYPHS["equals_column"]:
        out.append(text_box(n(), "LegendSwatch", _EQ_X, IN(_y), _EQ_W, _EQ_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))   # 000000 black
    # ── operator glyphs: "+" column ──
    for _y in _OPERATOR_GLYPHS["plus_column"]:
        out.append(text_box(n(), "LegendSwatch", _PLUS_X, IN(_y), _PLUS_W, _PLUS_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 63", IN(8.045), IN(0.538), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 64", IN(8.045), IN(1.302), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 65", IN(8.045), IN(2.065), IN(0.405), IN(7.942), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Left Brace 69", IN(7.811), IN(-1.253), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 7206"}, anchor="ctr", rot=16200000))   # 000000 black outline
    out.append(text_box(n(), "Left Brace 70", IN(7.811), IN(-1.254), IN(0.359), IN(9.975), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="leftBrace", geom_adj={"adj1": "val 8333", "adj2": "val 68631"}, anchor="ctr", rot=16200000))   # 000000 black outline
    out.append(text_box(n(), "Rectangle 74", IN(7.072), IN(3.947), _BOX_W, _BOX_H, [paragraph([run("Projects ($)", size=PT(9), color=WHITE, font=FONT), run(" 1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    # ── operator glyphs: "+" row ──
    for _x in _OPERATOR_GLYPHS["plus_row"]:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _PLUSROW_Y, _PLUSROW_W, _PLUSROW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=5400000))   # 000000 black
    out.append(text_box(n(), "Rectangle 88", IN(0.425), IN(1.229), IN(2.101), _BOX_H, [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Straight Connector 89", IN(0.426), IN(1.586), IN(2.1), IN(0.002), color=DK, width=12700, flip_h=True))   # 162029 dark navy
    out.append(text_box(n(), "Rectangle 97", IN(4.06), IN(1.371), IN(1.213), IN(0.333), [paragraph([run("Anti-Ship ", size=PT(9), color=WHITE, font=FONT), line_break(), run("Warfare", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 98", IN(11.765), IN(1.371), IN(1.213), IN(0.333), [paragraph([run("VBSS", size=PT(9), color=GRAY_3, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=GRAY_3, line_width=3175, anchor="ctr"))   # BFBFBF silver-gray outline
    # ── grid frame, then addressability legend keys ──
    _x, _y, _cx, _cy, _fill, _lc = _GRID_FRAME
    out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))   # 000000 black outline
    for _x, _y, _cx, _cy, _fill, _lc in _LEGEND_KEYS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 112", IN(4.84), IN(1.344), IN(0.248), IN(1.902), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    # ── legend captions ──
    out.append(text_box(n(), "TextBox 118", IN(9.301), _LEGEND_Y, IN(1.448), _LEGEND_H, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 120", IN(12.06), _LEGEND_Y, IN(0.913), _LEGEND_H, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 122", IN(7.987), _LEGEND_Y, IN(1.068), _LEGEND_H, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 124", IN(10.996), _LEGEND_Y, IN(0.817), _LEGEND_H, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    # ── header chip (top-right) + logo ──
    out.append(text_box(n(), "Rectangle 4", IN(9.352), IN(0.137), IN(2.201), IN(0.376), [paragraph([run("Currently manned capabilities – primary approach", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=DK, line_width=3175, anchor="ctr"))   # 447BB2 blue
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
