"""value_chain_maritime_transport — Commercial Strategy market-analysis deck (20260325), source slide 30.

EXHIBIT — "Value Chain (Maritime Transport)": shipbuilders capture the least value
(2-6% EBIT margins); margin expansion likely requires vertical integration. A
value-chain matrix across steps (Customer requires shipment → Coordination →
Origin Shoreside Logistics → Maritime Transport → Destination Shoreside Logistics),
with rows = maritime-transport archetypes (NVOCCs, VOCCs, Tramp Carriers, Private
Carriers, Charter Companies, Shipbuilders, MRO), each with a description and a
"$ TBD | EBIT margin %" value-capture label. Connectors trace owned- vs chartered-
vessel value flows; a Revenue|EBIT-margin legend and a swatch key annotate.
Preliminary chip top-right.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............. breadcrumb() + title_placeholder() + prelim_chip()
  • _STEP_CHEVRONS ..... value-chain step header chevrons
  • _ARCH_DARK / _GREY . archetype boxes (dark 0E1924 = in-scope, grey = other)
  • _ARCH_DESCRIPTIONS . the long per-archetype description paragraphs
  • _FLOW_NOTES ........ small italic flow annotations (NVOCC leases space, …)
  • _MARGIN_LABELS ..... the "$ TBD | EBIT margin %" value-capture labels (+ four
                         standalone ones); see residue note below
  • _LEGEND_SWATCHES ... colour key
  • tables ............. 3 single-cell tables (Value Chain Step / Revenue|EBIT
                         margin header / Archetypes spine)
  • connectors ......... owned- vs chartered-vessel value-flow arrows

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=15, connector=9, table=3, chrome_builders=3,
clusters=7 (covering 31 shapes), dropped=1 (think-cell OLE frame).
Residue: 9 "$ TBD | %" margin labels look title-like (they contain " | ") but sit
off the house title position, so each was kept verbatim as a plain text_box.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, tcell_rich, tpara, trun, tbreak, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, BLUE_1, GRAY_1, GRAY_2, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_CHEV_Y, _CHEV_W, _CHEV_H = IN(1.695), IN(2.1), IN(0.4)   # step-chevron geometry
_ARCH_DK_W = IN(2)        # dark archetype-box width
_ARCH_GREY_W = IN(2)      # grey archetype-box width
_DESC_W = IN(1.9)         # archetype-description text width
_SWATCH_Y, _SWATCH_W, _SWATCH_H = IN(1.406), IN(0.2), IN(0.2)   # legend-swatch geometry
_MARGIN_W = IN(1.576)     # "$ TBD | %" margin-label width        [shared x4]
_MARGIN_H = IN(0.225)     # "$ TBD | %" margin-label height       [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_STEP_CHEVRONS = [    # (x, fill, label) x3 — value-chain step header chevrons
    (6.465, "447BB2", "Origin Shoreside Logistics"),
    (10.695, "447BB2", "Destination Shoreside Logistics"),
    (8.58, "0E1924", "Maritime Transport"),
]

_ARCH_DARK = [    # (x, y, cy, label) x4 — in-scope archetype boxes (dark fill, white text)
    (3.662, 6.246, 0.401, "Shipbuilders"),
    (5.088, 3.938, 0.4, "Vessel Operating Common Carriers"),
    (10.795, 3.938, 0.4, "Private Carriers"),
    (9.368, 6.246, 0.401, "Charter Companies"),
]

_ARCH_GREY = [    # (x, y, cy, label) x3 — other archetype boxes (grey fill, black text)
    (2.235, 3.938, 0.4, "Non-Vessel Operating Common Carriers"),
    (6.515, 6.246, 0.401, "MRO"),
    (7.942, 3.938, 0.4, "Tramp Carriers"),
]

_ARCH_DESCRIPTIONS = [    # (x, y, cy, label) x9 — per-archetype / per-step description text
    (2.335, 2.094, 0.9, "Initiation of transportation process by owner of goods (e.g., retailer, commodity trader, or manufacturer)"),
    (4.45, 2.094, 0.9, "Arrangement of transport modes, storage, and compliance by coordinating entities (e.g., BCOs, freight forwarders)"),
    (6.565, 2.094, 0.9, "Movement of cargo from originating site onto ocean vessel; includes various transport modes, terminal ops, and export customs clearance"),
    (8.68, 2.094, 0.9, "Transport of cargo across ocean between ports of loading and discharge by common or private carriers on owned or chartered vessels"),
    (10.795, 2.094, 0.9, "Movement of cargo from ocean vessel to destination site; includes various transport modes, terminal ops, and import customs clearance "),
    (2.285, 4.343, 1.219, "Books space on operator vessels and resells to shippers without owning ships; NVOCC are a Coordination players that act like carriers by assuming legal liability for cargo"),
    (5.138, 4.343, 0.6, "Own/lease and operate vessels on fixed schedules for public use"),
    (10.845, 4.343, 0.6, "Shippers who own/lease and operate an internal fleet to move their own cargo"),
    (7.992, 4.343, 0.6, "Own/lease and operate vessels on demand for public use (no fixed schedule)"),
]

_FLOW_NOTES = [    # (x, y, cx, cy, label) x4 — small italic flow annotations
    (4.268, 3.836, 0.788, 0.267, "NVOCC leases space"),
    (4.268, 4.191, 0.788, 0.269, "VOCC provides space"),
    (6.745, 3.259, 1.535, 0.183, "Terminal Operators shown"),
    (10.997, 3.259, 1.535, 0.183, "Terminal Operators shown"),
]

_MARGIN_LABELS = [    # (x, y, cx, cy, fill, label) x5 — "$ TBD | %" value-capture labels
    (6.727, 6.689, 1.576, 0.226, WHITE, "$ TBD |  %TBD"),
    (4.611, 3.042, 1.575, 0.225, WHITE, "$ TBD |  %TBD"),
    (6.727, 3.042, 1.576, 0.225, WHITE, "$ TBD |  30-54%"),
    (10.956, 3.042, 1.576, 0.225, WHITE, "$ TBD |  30-54%"),
    (8.153, 4.973, 1.575, 0.225, None, "$ TBD |  %TBD"),
]

_LEGEND_SWATCHES = [    # (x, fill) x3 — colour key
    (0.495, "0E1924"),
    (4.017, GRAY_2),
    (2.48, "447BB2"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── value-flow legend boxes (owned vs chartered) ──
    out.append(text_box(n(), "Rectangle 213", IN(4.948), IN(3.457), IN(7.959), IN(1.85), [paragraph([run("Cargo moved by one or more of the following maritime transport archetypes", size=PT(8), italic=True, color=BLACK, font=FONT)])], fill=GRAY_1, line_color=BLACK))
    out.append(connector(n(), "Connector: Elbow 135", IN(3.235), IN(3.154), IN(1.376), IN(0.783), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_v=True, rot=10800000))
    out.append(text_box(n(), "Rectangle 177", IN(9.145), IN(5.962), IN(2.461), IN(1), [paragraph([run("Value flow for chartered vessels", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color=BLACK))
    out.append(text_box(n(), "Rectangle 138", IN(3.6), IN(5.962), IN(4.975), IN(1), [paragraph([run("Value flow for owned vessels", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=BLUE_1, line_color="808080"))
    out.append(text_box(n(), "Rectangle 73", IN(5.088), IN(4.948), IN(4.853), IN(0.275), [paragraph([], align="r")], fill=None, line_color=BLACK, line_width=6350, dashed_line=True))
    # ── value-chain step chevrons ──
    for _x, _fill, _t in _STEP_CHEVRONS:
        out.append(text_box(n(), "Label", IN(_x), _CHEV_Y, _CHEV_W, _CHEV_H, [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr")], fill=_fill, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    # ── chrome ──
    out.append(breadcrumb("Commercial Maritime Value Chain", "Overview"))
    out.append(title_placeholder("Value Chain (Maritime Transport)", "Shipbuilders capture the least value (2-6% EBIT margins); margin expansion likely requires vertical integration."))
    # ── archetype boxes: in-scope (dark) then other (grey) ──
    for _x, _y, _cy, _t in _ARCH_DARK:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _ARCH_DK_W, IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr")], fill="0E1924", line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    for _x, _y, _cy, _t in _ARCH_GREY:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _ARCH_GREY_W, IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_2, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(connector(n(), "Connector: Elbow 23", IN(10.41), IN(2.553), IN(0.604), IN(2.165), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000, adj={"adj1": "val 65164"}))
    out.append(text_box(n(), "Pfeil: Fünfeck 4", IN(2.235), IN(1.695), IN(2.1), IN(0.4), [paragraph([run("Customer / Shipper Requires Cargo Shipment", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_2, line_color="none", prst="homePlate", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    out.append(text_box(n(), "Pfeil: Chevron 5", IN(4.35), IN(1.695), IN(2.1), IN(0.4), [paragraph([run("Coordination", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_2, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    # ── row-label / header tables ──
    out.append(table(n(), "Table 111", IN(0.495), IN(1.695), IN(1.6), IN(1.638), col_widths=[IN(1.6)], rows=[
        trow([tcell_rich([tpara([trun("Value Chain Step", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), tbreak()])], fill=WHITE, borders={"L": "none", "R": {"color": BLACK, "width": 38100}, "T": "none", "B": "none"})], h=IN(1.638)),
    ]))
    out.append(table(n(), "Table 112", IN(9.579), IN(1.191), IN(3.215), IN(0.5), col_widths=[IN(3.215)], rows=[
        trow([tcell_rich([tpara([trun("Revenue | ", size=PT(8), bold=True, color=BLACK, font=FONT), trun("EBIT margin %", size=PT(8), bold=True, italic=True, color=BLACK, font=FONT), tbreak(), trun("(Revenue = total value chain rev. indexed to $100; EBIT margins for 2024)", size=PT(8), italic=True, color=BLACK, font=FONT)], align="r")], borders={"L": "none", "R": "none", "T": "none", "B": "none"})], h=IN(0)),
    ]))
    out.append(table(n(), "Table 124", IN(0.495), IN(3.457), IN(1.6), IN(3.505), col_widths=[IN(1.6)], rows=[
        trow([tcell("Archetypes", size=PT(10), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": {"color": BLACK, "width": 38100}, "T": "none", "B": "none"})], h=IN(3.505)),
    ]))
    out.append(connector(n(), "Connector: Elbow 176", IN(7.557), IN(1.865), IN(0.604), IN(3.541), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 65164"}))
    # ── per-archetype descriptions ──
    for _x, _y, _cy, _t in _ARCH_DESCRIPTIONS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _DESC_W, IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", l_ins=0, r_ins=0))
    out.append(connector(n(), "Connector: Elbow 63", IN(8.984), IN(3.291), IN(0.604), IN(0.688), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 65251"}))
    out.append(connector(n(), "Straight Arrow Connector 66", IN(4.235), IN(4.138), IN(0.853), IN(0), color=BLACK, width=12700, arrow=True))
    # ── small flow notes ──
    for _x, _y, _cx, _cy, _t in _FLOW_NOTES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))
    # ── value-capture margin labels (title-like; kept verbatim — see docstring residue) ──
    out.append(text_box(n(), "Rectangle 127", IN(8.842), IN(3.042), _MARGIN_W, _MARGIN_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("2 - 42%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(text_box(n(), "Rectangle 187", IN(3.873), IN(6.69), _MARGIN_W, _MARGIN_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("2-6%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    for _x, _y, _cx, _cy, _fill, _t in _MARGIN_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=_fill, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(text_box(n(), "Rectangle 189", IN(9.579), IN(6.69), _MARGIN_W, _MARGIN_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("22-53%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(text_box(n(), "TextBox 132", IN(6.756), IN(4.945), IN(1.665), IN(0.276), [paragraph([run("Revenue shown assumes one archetype moves goods", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 181", IN(9.324), IN(4.91), IN(0.655), IN(1.448), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))
    out.append(text_box(n(), "Rectangle 142", IN(5.3), IN(4.973), _MARGIN_W, _MARGIN_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("13-42%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(connector(n(), "Connector: Elbow 216", IN(7.18), IN(4.214), IN(0.655), IN(2.84), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))
    out.append(connector(n(), "Straight Arrow Connector 231", IN(8.575), IN(6.462), IN(0.571), IN(0), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(text_box(n(), "Rectangle 4", IN(10.144), IN(5.647), IN(2.461), IN(0.267), [paragraph([run("Amount dependent on charter type ", size=PT(8), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., time or voyage) ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))
    # ── legend swatches + captions ──
    for _x, _fill in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SWATCH_Y, _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr")], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 107", IN(0.707), IN(1.321), IN(1.76), IN(0.37), [paragraph([run("Maritime Transport archetypes ", size=PT(8), color=BLACK, font=FONT), line_break(), run("considered in analysis", size=PT(8), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 109", IN(4.229), IN(1.388), IN(0.817), IN(0.236), [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "TextBox 113", IN(2.693), IN(1.321), IN(1.312), IN(0.37), [paragraph([run("Other steps ", size=PT(8), color=BLACK, font=FONT), line_break(), run("considered in analysis", size=PT(8), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(connector(n(), "Straight Arrow Connector 9", IN(10.367), IN(3.532), IN(0), IN(1.7), color="808080", width=19050, dashed=True))
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
