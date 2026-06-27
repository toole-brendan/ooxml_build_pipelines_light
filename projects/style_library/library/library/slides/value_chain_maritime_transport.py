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
  • _STAGE_HEADERS ...... value-chain stage-header chevrons
  • _FLOW_NODES ......... archetype nodes; fill and text contrast are row fields
  • _ITEM_DESCRIPTIONS .. long descriptions paired with stages/archetype nodes
  • _EDGE_LABELS ........ small italic labels placed on relationship paths
  • _METRIC_LABELS ...... compact "$ TBD | EBIT margin %" readouts (+ four
                           standalone readouts); see residue note below
  • _LEGEND_KEYS ........ visual colour keys
  • tables ............. 3 single-cell tables (Value Chain Step / Revenue|EBIT
                         margin header / Archetypes spine)
  • connectors ......... owned- vs chartered-vessel value-flow arrows

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=15, connector=9, table=3, chrome_builders=3,
clusters=6 (covering 31 shapes), dropped=1 (think-cell OLE frame).
Residue: 9 "$ TBD | %" metric readouts look title-like (they contain " | ") but sit
off the house title position, so each was kept verbatim as a plain text_box.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, tcell_rich, tpara, trun, tbreak, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, BLUE_1, GRAY_1, GRAY_2, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell_rich() form — the only
#    change is legibility. ──
def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_CHEV_Y, _CHEV_W, _CHEV_H = IN(1.695), IN(2.1), IN(0.4)   # stage-header chevron geometry
_FLOW_NODE_W = IN(2)       # archetype flow-node width
_ITEM_DESCRIPTION_W = IN(1.9)  # paired description width
_SWATCH_Y, _SWATCH_W, _SWATCH_H = IN(1.406), IN(0.2), IN(0.2)   # legend-key geometry
_METRIC_W = IN(1.576)     # "$ TBD | %" metric-label width        [shared x4]
_METRIC_H = IN(0.225)     # "$ TBD | %" metric-label height       [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the three value-chain stage-header chevrons spanning the slide (the maritime-
#   transport stages).
_STAGE_HEADERS = [    # (x, fill, label) x3 — value-chain stage-header chevrons
    (6.465, "447BB2", "Origin Shoreside Logistics"),   # 447BB2 blue
    (10.695, "447BB2", "Destination Shoreside Logistics"),   # 447BB2 blue
    (8.58, "0E1924", "Maritime Transport"),   # 0E1924 near-black navy
]

# local_meaning: the seven vessel-archetype nodes laid under the stages; the fill/text_color row
#   field marks the 4 in-scope archetypes (dark fill, white text) vs the 3 other archetypes (grey
#   fill, black text).
_FLOW_NODES = [    # (x, y, cy, fill, text_color, label) x7 — archetype nodes; style is row data
    (3.662, 6.246, 0.401, "0E1924", WHITE, "Shipbuilders"),   # 0E1924 near-black navy
    (5.088, 3.938, 0.4, "0E1924", WHITE, "Vessel Operating Common Carriers"),   # 0E1924 near-black navy
    (10.795, 3.938, 0.4, "0E1924", WHITE, "Private Carriers"),   # 0E1924 near-black navy
    (9.368, 6.246, 0.401, "0E1924", WHITE, "Charter Companies"),   # 0E1924 near-black navy
    (2.235, 3.938, 0.4, GRAY_2, BLACK, "Non-Vessel Operating Common Carriers"),   # D9D9D9 light gray
    (6.515, 6.246, 0.401, GRAY_2, BLACK, "MRO"),   # D9D9D9 light gray
    (7.942, 3.938, 0.4, GRAY_2, BLACK, "Tramp Carriers"),   # D9D9D9 light gray
]


# local_meaning: the nine description blurbs paired with the stages/archetypes (what each
#   participant does).
_ITEM_DESCRIPTIONS = [    # (x, y, cy, label) x9 — descriptions paired with stages/archetypes
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

# local_meaning: the four small italic flow annotations between nodes (relationships along the
#   chain).
_EDGE_LABELS = [    # (x, y, cx, cy, label) x4 — small italic relationship labels
    (4.268, 3.836, 0.788, 0.267, "NVOCC leases space"),
    (4.268, 4.191, 0.788, 0.269, "VOCC provides space"),
    (6.745, 3.259, 1.535, 0.183, "Terminal Operators shown"),
    (10.997, 3.259, 1.535, 0.183, "Terminal Operators shown"),
]

# local_meaning: the five '$ TBD | %' value-capture labels showing the margin/share captured at
#   each stage (the 'shipbuilders capture least' point).
_METRIC_LABELS = [    # (x, y, cx, cy, fill, label) x5 — "$ TBD | %" value-capture metric labels
    (6.727, 6.689, 1.576, 0.226, WHITE, "$ TBD |  %TBD"),   # FFFFFF white
    (4.611, 3.042, 1.575, 0.225, WHITE, "$ TBD |  %TBD"),   # FFFFFF white
    (6.727, 3.042, 1.576, 0.225, WHITE, "$ TBD |  30-54%"),   # FFFFFF white
    (10.956, 3.042, 1.576, 0.225, WHITE, "$ TBD |  30-54%"),   # FFFFFF white
    (8.153, 4.973, 1.575, 0.225, None, "$ TBD |  %TBD"),   # 000000 black
]

# local_meaning: the three legend colour chips keying the archetype fills.
_LEGEND_KEYS = [    # (x, fill) x3 — visual colour keys
    (0.495, "0E1924"),   # 0E1924 near-black navy
    (4.017, GRAY_2),   # D9D9D9 light gray
    (2.48, "447BB2"),   # 447BB2 blue
]
# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level layout convention is expressed by repeating the
# same l_ins/r_ins/t_ins/b_ins, anchor, and alignment across the affected cells.
# In tcell()/tcell_rich(), those insets are internal padding and anchor is vertical
# alignment; tcell align or tpara align/mar_l/indent controls horizontal alignment
# and paragraph margins (including hanging bullet indents).

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Explicit zero/tight insets and wrap="none"
# are alignment devices for chart/exhibit labels; omitted values retain the
# primitive defaults intentionally.


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── value-flow legend boxes (owned vs chartered) ──
    out.append(text_box(n(), "Rectangle 213", IN(4.948), IN(3.457), IN(7.959), IN(1.85), [paragraph([run("Cargo moved by one or more of the following maritime transport archetypes", size=PT(8), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=GRAY_1, line_color=BLACK))   # F2F2F2 off-white
    out.append(connector(n(), "Connector: Elbow 135", IN(3.235), IN(3.154), IN(1.376), IN(0.783), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_v=True, rot=10800000))   # 000000 black
    out.append(text_box(n(), "Rectangle 177", IN(9.145), IN(5.962), IN(2.461), IN(1), [paragraph([run("Value flow for chartered vessels", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK))   # 000000 black outline
    out.append(text_box(n(), "Rectangle 138", IN(3.6), IN(5.962), IN(4.975), IN(1), [paragraph([run("Value flow for owned vessels", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_1, line_color="808080"))   # E2E9EF pale blue
    out.append(text_box(n(), "Rectangle 73", IN(5.088), IN(4.948), IN(4.853), IN(0.275), [paragraph([], align="r", line_spacing=100000)], fill=None, line_color=BLACK, line_width=6350, dashed_line=True))   # 000000 black outline
    # ── value-chain stage headers ──
    # Chevron labels use explicit four-side padding and centered vertical/horizontal
    # alignment so the text clears the arrow head consistently.
    for _x, _fill, _t in _STAGE_HEADERS:
        out.append(text_box(n(), "Label", IN(_x), _CHEV_Y, _CHEV_W, _CHEV_H, [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    # ── chrome ──
    out.append(breadcrumb("Commercial Maritime Value Chain", "Overview"))
    out.append(title_placeholder("Value Chain (Maritime Transport)", "Shipbuilders capture the least value (2-6% EBIT margins); margin expansion likely requires vertical integration."))
    # ── archetype flow nodes ──
    # Nodes share centered anchoring/alignment and fixed left/right padding; fill
    # and readable text contrast remain row data rather than cluster taxonomy.
    for _x, _y, _cy, _fill, _txt, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _FLOW_NODE_W, IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=_txt, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(connector(n(), "Connector: Elbow 23", IN(10.41), IN(2.553), IN(0.604), IN(2.165), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000, adj={"adj1": "val 65164"}))   # 000000 black
    out.append(text_box(n(), "Pfeil: Fünfeck 4", IN(2.235), IN(1.695), IN(2.1), IN(0.4), [paragraph([run("Customer / Shipper Requires Cargo Shipment", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color="none", prst="homePlate", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))   # D9D9D9 light gray
    out.append(text_box(n(), "Pfeil: Chevron 5", IN(4.35), IN(1.695), IN(2.1), IN(0.4), [paragraph([run("Coordination", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))   # D9D9D9 light gray
    # ── row-label / header tables ──
    # Each is a one-column grid. col_widths fixes the column; the single trow height
    # fixes/minimizes the band. Cell anchor/insets govern vertical placement and
    # padding, while tpara align/mar_l/indent governs horizontal text margins.
    # palette — text: 000000 black (label); fills: FFFFFF white; rules: 000000 black (right edge).
    out.append(table(n(), "Table 111", IN(0.495), IN(1.695), IN(1.6), IN(1.638), col_widths=[IN(1.6)], rows=[
        trow([rcell([tpara([trun("Value Chain Step", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), tbreak()], mar_l=0, indent=0)], fill=WHITE, R=edge(BLACK, 38100))], h=IN(1.638)),
    ]))
    # palette — text: 000000 black (header); fills: none; rules: none.
    out.append(table(n(), "Table 112", IN(9.579), IN(1.191), IN(3.215), IN(0.5), col_widths=[IN(3.215)], rows=[
        trow([rcell([tpara([trun("Revenue | ", size=PT(8), bold=True, color=BLACK, font=FONT), trun("EBIT margin %", size=PT(8), bold=True, italic=True, color=BLACK, font=FONT), tbreak(), trun("(Revenue = total value chain rev. indexed to $100; EBIT margins for 2024)", size=PT(8), italic=True, color=BLACK, font=FONT)], align="r", mar_l=0, indent=0)])], h=IN(0)),
    ]))
    # palette — text: 000000 black (label); fills: FFFFFF white; rules: 000000 black (right edge).
    out.append(table(n(), "Table 124", IN(0.495), IN(3.457), IN(1.6), IN(3.505), col_widths=[IN(1.6)], rows=[
        trow([rcell([tpara([trun("Archetypes", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, R=edge(BLACK, 38100))], h=IN(3.505)),
    ]))
    out.append(connector(n(), "Connector: Elbow 176", IN(7.557), IN(1.865), IN(0.604), IN(3.541), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 65164"}))   # 000000 black
    # ── item descriptions ──
    # Zero left/right shape insets let centered paragraphs use the full narrow box.
    for _x, _y, _cy, _t in _ITEM_DESCRIPTIONS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _ITEM_DESCRIPTION_W, IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", l_ins=0, r_ins=0))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 63", IN(8.984), IN(3.291), IN(0.604), IN(0.688), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000, adj={"adj1": "val 65251"}))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 66", IN(4.235), IN(4.138), IN(0.853), IN(0), color=BLACK, width=12700, arrow=True))   # 000000 black
    # ── edge labels — centered, zero left/right padding on relationship paths ──
    for _x, _y, _cx, _cy, _t in _EDGE_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))   # 000000 black
    # ── value-capture metric labels (title-like; kept verbatim — see docstring residue) ──
    out.append(text_box(n(), "Rectangle 127", IN(8.842), IN(3.042), _METRIC_W, _METRIC_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("2 - 42%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))   # 000000 black
    out.append(text_box(n(), "Rectangle 187", IN(3.873), IN(6.69), _METRIC_W, _METRIC_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("2-6%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))   # FFFFFF white
    for _x, _y, _cx, _cy, _fill, _t in _METRIC_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))
    out.append(text_box(n(), "Rectangle 189", IN(9.579), IN(6.69), _METRIC_W, _METRIC_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("22-53%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))   # 000000 black
    out.append(text_box(n(), "TextBox 132", IN(6.756), IN(4.945), IN(1.665), IN(0.276), [paragraph([run("Revenue shown assumes one archetype moves goods", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 181", IN(9.324), IN(4.91), IN(0.655), IN(1.448), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, rot=16200000))   # 000000 black
    out.append(text_box(n(), "Rectangle 142", IN(5.3), IN(4.973), _METRIC_W, _METRIC_H, [paragraph([run("$ TBD | ", size=PT(12), bold=True, color=BLACK, font=FONT), run("13-42%", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, r_ins=91440))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 216", IN(7.18), IN(4.214), IN(0.655), IN(2.84), color=BLACK, width=12700, arrow=True, prst="bentConnector3", rot=5400000))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 231", IN(8.575), IN(6.462), IN(0.571), IN(0), color=BLACK, width=12700, arrow=True, flip_h=True))   # 000000 black
    out.append(text_box(n(), "Rectangle 4", IN(10.144), IN(5.647), IN(2.461), IN(0.267), [paragraph([run("Amount dependent on charter type ", size=PT(8), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., time or voyage) ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, r_ins=0))   # 000000 black
    # ── legend keys + captions; keys have empty centered text bodies ──
    for _x, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _SWATCH_Y, _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "TextBox 107", IN(0.707), IN(1.321), IN(1.76), IN(0.37), [paragraph([run("Maritime Transport archetypes ", size=PT(8), color=BLACK, font=FONT), line_break(), run("considered in analysis", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 109", IN(4.229), IN(1.388), IN(0.817), IN(0.236), [paragraph([run("Future effort", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "TextBox 113", IN(2.693), IN(1.321), IN(1.312), IN(0.37), [paragraph([run("Other steps ", size=PT(8), color=BLACK, font=FONT), line_break(), run("considered in analysis", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 9", IN(10.367), IN(3.532), IN(0), IN(1.7), color="808080", width=19050, dashed=True))   # 808080 gray
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
