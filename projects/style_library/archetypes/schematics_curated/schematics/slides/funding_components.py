"""funding_components — Navy market-sizing deck (20251120), source slide 15.

EXHIBIT — "Components": a mission-area × funding-structure matrix that lays out
what the Navy (Surface incl. MDA) market-sizing model treats as in- or out-of-
scope. Left spine carries three rotated −90° row-group labels (Funding Inputs ·
Budget Data Sources · Color of Money). The body is a grid of mission-area boxes
colour-coded by addressability — BLACK = sized in this campaign, A6A6A6 grey =
sized in another campaign, white-outline = non-addressable — sitting under three
funding-type headers (Unmanned-specified · Currently-manned-capabilities · Kill-
chain roles). A legend strip (top-right) and a footnote row close it out.

CODE MAP (the body follows the source's PAINT ORDER, so groups interleave; the
section headers below mark roles in place rather than re-ordering the shapes):
  • chrome ............ breadcrumb() + title_placeholder() (house builders)
  • _BANNER_LABELS .... full-width budget-row banners + black mission labels that
                        share one black-fill PT9 style → one loop
  • _LEGEND_SWATCHES .. the 4 legend colour chips → loop; their caption text
                        boxes are standalone and interleave further down
  • _GREY_LABELS ...... grey kill-chain-role boxes (Sensors/Effectors/CSI) + O&M
  • _ROW_GROUP_LABELS . the 3 rotated spine labels → loop
  • mission grid ...... standalone Rectangle text_box()s, one per mission area,
                        each ending in a superscript footnote run
  • connectors ........ dashed row dividers + vertical spine rules
  • callout ........... one wedgeRectCallout speech bubble (sUSV note)
  • logo .............. picture() top-right (IMAGES rId2)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments were made semantic and the body grouped into sections — NO
coordinate, value, colour, or paint-order was changed, so the render is
byte-identical to the raw port.

Converter stats: text_box=21, connector=6, picture=1, chrome_builders=2,
clusters=4 (covering 25 shapes), dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, line_break, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image8_3071a231.jpeg"},
]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_BANNER_H = IN(0.333)     # row-banner box height
_SWATCH_W = IN(0.2)       # legend colour-chip width
_GREY_H = IN(0.333)       # grey kill-chain box height
_LEGEND_Y = IN(1.563)     # legend row (chips + captions)        [shared x4]
_LEGEND_H = IN(0.2)       # legend row height                    [shared x4]
_MISSION_W = IN(1.213)    # mission-area box width               [shared x9]
_MISSION_H = IN(0.333)    # mission-area box height              [shared x14]
_GRID_Y2 = IN(2.758)      # mission grid, 2nd row                [shared x4]
_GRID_Y3 = IN(3.19)       # mission grid, 3rd row                [shared x4]
_HDR_Y = IN(1.889)        # funding-type header row              [shared x5]

# ── repeated-shape data tables (each drives a loop in _body) ──
_BANNER_LABELS = [    # (x, y, cx, label) x14 — budget-row banners + black mission labels
    (0.604, 4.093, 12.229, "FY26 PBR & Congressional Committee markups"),
    (0.604, 4.528, 12.229, "OBBBA & Congressional Committee intent"),
    (9.599, 4.963, 3.222, "SHIELD IDIQ"),
    (2.641, 2.323, 1.213, "Anti-Air Warfare (incl. cUAS)"),
    (8.208, 2.323, 1.213, "Electronic Warfare (D&D)"),
    (9.599, 2.323, 1.213, "IAMD (OBBBA)"),
    (0.902, 2.323, 1.212, "sUSV"),
    (0.902, 2.758, 1.212, "mUSV"),
    (11.046, 2.323, 1.767, "Platforms"),
    (9.599, 2.758, 1.213, "IAMD (SHIELD)"),
    (0.604, 5.399, 12.229, "Procurement"),
    (0.604, 5.834, 12.229, "RDT&E"),
    (2.641, 2.758, 1.213, "Electronic Warfare (Other)"),
    (0.902, 3.19, 1.212, "USV Enabling Capabilities"),
]

_LEGEND_SWATCHES = [    # (x, y, cy, fill, line) x4 — addressability colour chips
    (8.929, 1.563, 0.2, "A6A6A6", "A6A6A6"),
    (11.687, 1.563, 0.2, None, GRAY_3),
    (7.614, 1.563, 0.2, BLACK, BLACK),
    (10.623, 1.563, 0.2, GRAY_1, GRAY_1),
]

_GREY_LABELS = [    # (x, y, cx, label) x4 — kill-chain-role boxes + O&M row
    (11.046, 3.19, 1.768, "Sensors"),
    (11.045, 3.622, 1.768, "Combat Systems Integration (incl. CEC)"),
    (11.045, 2.758, 1.768, "Effectors"),
    (0.604, 6.269, 12.229, "O&M"),
]

_ROW_GROUP_LABELS = [    # (x, y, cx, cy, label) x3 — rotated −90° spine labels
    (-0.781, 2.659, 2.147, 0.563, "Funding Inputs"),
    (-0.308, 5.714, 1.2, 0.562, "Color of Money"),
    (-0.308, 4.412, 1.2, 0.562, "Budget Data Sources"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(title_placeholder("Components", "The following funding inputs, sources, and colors of money are considered for sizing the Navy (Surface) market"))
    # ── row banners — full-width budget rows + black mission labels (one shared black-fill style) ──
    for _x, _y, _cx, _t in _BANNER_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _BANNER_H, [paragraph([run(_t, size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    # ── legend — 4 colour chips; the caption text boxes interleave below in paint order ──
    for _x, _y, _cy, _fill, _lc in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SWATCH_W, IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 13", IN(9.152), _LEGEND_Y, IN(1.448), _LEGEND_H, [paragraph([run("Sized in another campaign", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 15", IN(11.91), _LEGEND_Y, IN(0.913), _LEGEND_H, [paragraph([run("Non-addressable", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    # ── mission grid — one box per mission area; fill = addressability (BLACK sized here · A6A6A6 another campaign · white-outline non-addressable); trailing run = footnote marker ──
    out.append(text_box(n(), "Rectangle 17", IN(5.424), IN(2.323), _MISSION_W, _MISSION_H, [paragraph([run("Anti-Submarine Warfare", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 18", IN(8.208), _GRID_Y2, _MISSION_W, _MISSION_H, [paragraph([run("Amphibious Warfare", size=PT(9), color=WHITE, font=FONT), run("3", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="A6A6A6", line_color="A6A6A6", line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 19", IN(6.817), IN(2.323), IN(1.212), _MISSION_H, [paragraph([run("Ballistic Missile Defense", size=PT(9), color=WHITE, font=FONT), run("2", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 22", IN(4.033), _GRID_Y3, _MISSION_W, _MISSION_H, [paragraph([run("Special Operations", size=PT(9), color=WHITE, font=FONT), run("5", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="A6A6A6", line_color="A6A6A6", line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 21", IN(5.424), _GRID_Y2, _MISSION_W, _MISSION_H, [paragraph([run("Mine Warfare", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 24", IN(5.424), _GRID_Y3, _MISSION_W, _MISSION_H, [paragraph([run("Sealift", size=PT(9), color=WHITE, font=FONT), run("3", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="A6A6A6", line_color="A6A6A6", line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 25", IN(4.033), IN(2.323), _MISSION_W, _MISSION_H, [paragraph([run("Anti-Surface Ship Warfare", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 27", IN(6.816), _GRID_Y3, _MISSION_W, _MISSION_H, [paragraph([run("VBSS", size=PT(9), color=GRAY_3, font=FONT), run("6", size=PT(9), color=GRAY_3, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=GRAY_3, line_width=3175, anchor="ctr"))
    # funding-type header (interleaves with the grid in paint order)
    out.append(text_box(n(), "Rectangle 28", IN(0.604), _HDR_Y, IN(1.807), _MISSION_H, [paragraph([run("Unmanned-specified funding (USV)", size=PT(11), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="99B9D8", line_color=DK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 29", IN(6.816), _GRID_Y2, _MISSION_W, _MISSION_H, [paragraph([run("Strike Warfare", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 31", IN(2.485), _HDR_Y, IN(8.468), _MISSION_H, [paragraph([run("Currently manned capabilities (CMC) funding ", size=PT(11), color=WHITE, font=FONT), line_break(), run("Surface missions", size=PT(11), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=DK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 32", IN(11.026), _HDR_Y, IN(1.807), _MISSION_H, [paragraph([run("Kill chain roles", size=PT(11), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="0E1924", line_color=DK, line_width=3175, anchor="ctr"))
    # ── grey boxes — kill-chain roles (Sensors/Effectors/CSI) + O&M row ──
    for _x, _y, _cx, _t in _GREY_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _GREY_H, [paragraph([run(_t, size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=GRAY_1, line_width=3175, anchor="ctr"))
    # ── row-group spine labels (rotated −90°) ──
    for _x, _y, _cx, _cy, _t in _ROW_GROUP_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(11), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", rot=16200000))
    # ── structure — dashed row dividers + vertical spine rules (two more grid boxes + the footnote interleave here) ──
    out.append(connector(n(), "Straight Connector 42", IN(0.515), _HDR_Y, IN(0), IN(2.1), color=DK, width=12700))
    out.append(connector(n(), "Straight Connector 44", IN(0.486), IN(4.041), IN(12.267), IN(0), color="88AABD", width=3175, dashed=True, flip_h=True))
    out.append(connector(n(), "Straight Connector 46", IN(0.512), IN(5.394), IN(0.002), IN(1.2), color=DK, width=12700))
    out.append(connector(n(), "Straight Connector 47", IN(0.486), IN(5.342), IN(12.267), IN(0), color="88AABD", width=3175, dashed=True, flip_h=True))
    out.append(text_box(n(), "Rectangle 6", IN(4.033), _GRID_Y2, _MISSION_W, _MISSION_H, [paragraph([run("ISR", size=PT(9), color=WHITE, font=FONT), run("1", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 52", IN(2.641), _GRID_Y3, IN(1.214), _MISSION_H, [paragraph([run("C4", size=PT(9), color=WHITE, font=FONT), run("4", size=PT(9), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="A6A6A6", line_color="A6A6A6", line_width=3175, anchor="ctr"))
    # footnotes — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 57", IN(0.495), IN(6.642), IN(12.367), IN(0.354), [paragraph([run("Note: (1) Only addressable by Surface materiel; (2) Current BMD mission; (3) Sized in USMC Campaign, with Sealift pertaining to Contested Logistics; (4) Undersea portion sized in Navy (Undersea) Campaign; (5) Sized in SOCOM Campaign; (6) Requires manned presence to fulfill mission", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 60", IN(0.512), IN(4.093), IN(0.002), IN(1.2), color=DK, width=12700))
    out.append(connector(n(), "Straight Connector 61", IN(10.989), _HDR_Y, IN(0), IN(2.066), color="88AABD", width=3175, dashed=True, flip_v=True))
    # legend captions (cont.)
    out.append(text_box(n(), "TextBox 2056", IN(7.837), _LEGEND_Y, IN(1.068), _LEGEND_H, [paragraph([run("Included in sizing", size=PT(8), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 2058", IN(10.846), _LEGEND_Y, IN(0.817), _LEGEND_H, [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "Rectangle 2064", IN(9.459), IN(2.249), IN(1.493), IN(1.706), [paragraph([run("Sizing approach different vs. other CMC", size=PT(9), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=DK, line_width=3175, anchor="b"))
    # ── callout — sUSV capabilities ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 8", IN(0.551), IN(3.574), IN(2.785), IN(0.407), [paragraph([run("sUSV expected to deliver counter-UAS, Deception & Decoy, and ISR capabilities", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val -48497", "adj2": "val -3486"}))
    # ── logo (top-right) ──
    out.append(picture(n(), "Picture 2", "rId2", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
