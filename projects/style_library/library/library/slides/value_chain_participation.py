"""value_chain_participation — Commercial Strategy market-analysis deck (20260325), source slide 31.

EXHIBIT — "Value Chain Participation": shipbuilders are largely not observed to
vertically integrate beyond chartering, whereas large shippers and VOCCs integrate
across the value chain. A value-chain matrix — a "Value Chain Step" header row of
chevrons (Customer requires shipment → Coordination → Shoreside Logistics →
Maritime Transport → Destination Logistics) over a "Representative players" row
whose cells hold ~24 company logos. Player-archetype boxes (Terminal Operators,
Charter Companies, Pure-play / Integrated Shipbuilders) and dashed integration-span
boxes (Shippers/Private Carriers, VOCCs) show who spans which steps; small group
labels and wedge callouts annotate. Preliminary chip top-right.

This is the most picture-dense module in the set (24 logo pics + 2 row-label
tables) — a worked example of wiring many IMAGES entries to picture() calls.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ........... breadcrumb() + title_placeholder() + prelim_chip()
  • _STAGE_HEADERS ..... value-chain stage-header chevrons
  • _GRID_CELLS ........ repeated player/archetype matrix cells
  • _GROUP_CAPTIONS .... small italic grouped-region captions
  • _CALLOUTS .......... wedgeRectCallout annotations
  • tables ........... 2 single-cell row-label tables ("Value Chain Step",
                       "Representative players")
  • pictures ......... ~24 company logos in the matrix cells (rId2-rId23; rId2/
                       rId3 reused for the two repeated columns); ONE <p:pic> was
                       dropped (no media target or geometry)
  • markers / dividers small square outline boxes (_MARK_W) + 4 dashed step rules

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=7, connector=5, chart=0, table=2, picture=24, custom_geometry=0, chrome_builders=3, clusters=4 (covering 14 shapes), raw_verbatim=0, dropped=2, frozen_fields=0.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_2, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image13_672efe4b.png"},
    {"rId": "rId3", "file": "image14_1bf4c99e.png"},
    {"rId": "rId4", "file": "image15_25624857.png"},
    {"rId": "rId5", "file": "image16_da5f3708.png"},
    {"rId": "rId6", "file": "image17_f373f1da.png"},
    {"rId": "rId7", "file": "image18_ddebb15f.png"},
    {"rId": "rId8", "file": "image19_84003496.png"},
    {"rId": "rId9", "file": "image21_0bacf462.png"},
    {"rId": "rId10", "file": "image22_9fb945dc.png"},
    {"rId": "rId11", "file": "image23_03c42e94.png"},
    {"rId": "rId12", "file": "image24_2778926d.png"},
    {"rId": "rId13", "file": "image25_bd50af1e.png"},
    {"rId": "rId14", "file": "image26_8d2caa7b.png"},
    {"rId": "rId15", "file": "image27_768e13fd.png"},
    {"rId": "rId16", "file": "image28_9cbe8d79.png"},
    {"rId": "rId17", "file": "image29_4d22badb.png"},
    {"rId": "rId18", "file": "image30_ee91678f.png"},
    {"rId": "rId19", "file": "image31_98d329b1.png"},
    {"rId": "rId20", "file": "image32_251526d6.png"},
    {"rId": "rId21", "file": "image33_f545c301.png"},
    {"rId": "rId22", "file": "image34_75574897.jpeg"},
    {"rId": "rId23", "file": "image35_b95a7460.jpeg"},
]


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
_CHEV_Y, _CHEV_W, _CHEV_H = IN(1.641), IN(2.1), IN(0.4)   # step-chevron geometry
_GROUP_Y, _GROUP_H = IN(1.344), IN(0.236)                 # group-label row
_DIV_Y = IN(2.087)        # dashed step-divider y                 [shared x4]
_DIV_H = IN(4.9)          # dashed step-divider height            [shared x4]
_MARK_W = IN(0.2)         # small square group-marker size        [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the three value-chain stage-header chevrons across the top.
_STAGE_HEADERS = [    # (x, fill, label) x3 — value-chain stage-header chevrons
    (6.465, "447BB2", "Origin Shoreside Logistics"),   # 447BB2 blue
    (10.695, "447BB2", "Destination Shoreside Logistics"),   # 447BB2 blue
    (8.58, "0E1924", "Maritime Transport"),   # 0E1924 near-black navy
]

# local_meaning: the five player x archetype matrix cells marking which players participate at
#   each stage (mostly not shipbuilders).
_GRID_CELLS = [    # (x, y, cx, cy, line, label) x5 — player/archetype matrix cells
    (6.527, 4.782, 1.876, 0.926, "447BB2", "Terminal Operators"),
    (8.643, 4.782, 1.877, 0.926, "0E1924", "Charter Companies"),
    (8.643, 2.193, 1.877, 0.885, "0E1924", "Pure-play Shipbuilders"),
    (8.643, 3.137, 1.877, 1.586, "0E1924", "Integrated Shipbuilders"),
    (10.807, 4.782, 1.876, 0.926, "447BB2", "Terminal Operators"),
]

# local_meaning: the three small italic captions labeling grouped regions of the matrix.
_GROUP_CAPTIONS = [    # (x, cx, label) x3 — small italic grouped-region captions
    (0.684, 2.018, "Primarily Maritime Transport Players"),
    (4.646, 1.189, "Integrated Shippers"),
    (2.881, 1.587, "Shoreside Logistics Players"),
]

# local_meaning: the three wedge callouts annotating the participation gaps.
_CALLOUTS = [    # (x, y, cx, cy, fill, label) x3 — wedge callouts
    (2.337, 2.32, 1.944, 0.482, WHITE, "Players shown own and operate their own vessels and charter additional ships "),   # FFFFFF white
    (8.778, 3.726, 1.607, 0.169, None, "Entered shipping in ‘24"),   # 000000 black
    (8.778, 4.482, 1.607, 0.168, None, "Chartering"),   # 000000 black
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
    # ── dashed step dividers + bottom integration-span box, then chrome ──
    out.append(connector(n(), "Straight Arrow Connector 1032", IN(4.291), _DIV_Y, IN(0), _DIV_H, color="808080", width=3175, dashed=True, flip_h=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 1036", IN(6.404), _DIV_Y, IN(0), _DIV_H, color="808080", width=3175, dashed=True, flip_h=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 1038", IN(8.526), _DIV_Y, IN(0), _DIV_H, color="808080", width=3175, dashed=True, flip_h=True))   # 808080 gray
    out.append(connector(n(), "Straight Arrow Connector 1040", IN(10.631), _DIV_Y, IN(0), _DIV_H, color="808080", width=3175, dashed=True, flip_h=True))   # 808080 gray
    out.append(text_box(n(), "Rectangle 41", IN(2.49), IN(6.428), IN(10.305), IN(0.551), [paragraph([run("Shippers / Private Carriers – ", size=PT(10), bold=True, color=BLACK, font=FONT), run("Integrated across value chain steps", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=BLACK, line_width=19050, dashed_line=True))   # FFFFFF white
    out.append(breadcrumb("Commercial Maritime Value Chain", "Overview"))
    out.append(title_placeholder("Value Chain Participation", "Shipbuilders largely not observed to vertically integrate beyond chartering, whereas large shippers and VOCCs integrate across the value chain."))
    # ── row-label table: Representative players ──
    # One column and one row define the band; cell padding/anchor own the
    # internal placement, while tpara mar_l/indent own paragraph margins.
    # palette — text: 000000 black (label); fills: FFFFFF white; rules: 000000 black (right edge).
    out.append(table(n(), "Table 22", IN(0.495), IN(2.193), IN(1.6), IN(4.794), col_widths=[IN(1.6)], rows=[
        trow([rcell([tpara([trun("Representative players", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, R=edge(BLACK, 38100))], h=IN(4.794)),
    ]))
    # ── value-chain stage headers ──
    # Explicit four-side padding plus centered anchor/alignment keeps text
    # clear of the chevron head and vertically balanced.
    for _x, _fill, _t in _STAGE_HEADERS:
        out.append(text_box(n(), "Label", IN(_x), _CHEV_Y, _CHEV_W, _CHEV_H, [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    out.append(text_box(n(), "Pfeil: Fünfeck 4", IN(2.235), IN(1.641), IN(2.1), IN(0.4), [paragraph([run("Customer / Shipper Requires Cargo Shipment", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color="none", prst="homePlate", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))   # D9D9D9 light gray
    out.append(text_box(n(), "Pfeil: Chevron 5", IN(4.35), IN(1.641), IN(2.1), IN(0.4), [paragraph([run("Coordination", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_2, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))   # D9D9D9 light gray
    # ── row-label table: Value Chain Step ──
    # Repeats the same one-cell padding/alignment contract as the row spine.
    # palette — text: 000000 black (label); fills: FFFFFF white; rules: 000000 black (right edge).
    out.append(table(n(), "Table 46", IN(0.495), IN(1.641), IN(1.6), IN(0.4), col_widths=[IN(1.6)], rows=[
        trow([rcell([tpara([trun("Value Chain Step", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=WHITE, R=edge(BLACK, 38100))], h=IN(0.4)),
    ]))
    # ── grid cells: player/archetype regions ──
    # Paragraphs are horizontally centered; omitted anchor/insets deliberately
    # retain primitive defaults for these larger outlined regions.
    for _x, _y, _cx, _cy, _lc, _t in _GRID_CELLS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=_lc, line_width=19050))   # FFFFFF white
    # ── company logos in the matrix cells (interleaved with markers/labels in paint order) ──
    out.append(picture(n(), "Picture 2", "rId2", IN(6.871), IN(5.382), IN(1.186), IN(0.273)))
    out.append(picture(n(), "Picture 4", "rId3", IN(6.854), IN(5.038), IN(1.221), IN(0.248), src_rect={'t': 39246, 'b': 40454}))
    out.append(picture(n(), "Picture 6", "rId4", IN(4.778), IN(6.709), IN(1.24), IN(0.226)))
    out.append(picture(n(), "Picture 14", "rId5", IN(6.825), IN(6.703), IN(0.744), IN(0.237)))
    out.append(picture(n(), "Picture 2", "rId6", IN(2.733), IN(6.712), IN(1.157), IN(0.219)))
    out.append(picture(n(), "Picture 4", "rId7", IN(10.197), IN(6.698), IN(1.074), IN(0.248)))
    out.append(picture(n(), "Picture 18", "rId8", IN(11.902), IN(6.674), IN(0.661), IN(0.296)))
    # DROPPED <p:pic> ? (no media target or geometry)
    out.append(text_box(n(), "Rectangle 20", IN(0.495), IN(1.361), _MARK_W, _MARK_W, [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="0E1924", line_width=19050, anchor="ctr"))   # 0E1924 near-black navy outline
    # ── group captions — centered vertically, no-wrap, default horizontal padding ──
    for _x, _cx, _t in _GROUP_CAPTIONS:
        out.append(text_box(n(), "Label", IN(_x), _GROUP_Y, IN(_cx), _GROUP_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))   # 000000 black
    out.append(text_box(n(), "Rectangle 24", IN(4.457), IN(1.361), _MARK_W, _MARK_W, [paragraph([], align="ctr", line_spacing=100000)], fill=WHITE, line_color=BLACK, line_width=19050, dashed_line=True, anchor="ctr"))   # FFFFFF white
    out.append(connector(n(), "Connector: Elbow 52", IN(0.532), IN(3.999), IN(4.662), IN(0.746), color=BLACK, width=12700, arrow=True, prst="bentConnector4", rot=5400000, adj={"adj1": "val 47046", "adj2": "val 133516"}))   # 000000 black
    out.append(text_box(n(), "Rectangle 9", IN(4.35), IN(5.769), IN(8.445), IN(0.6), [paragraph([run("Vessel Operating Common Carriers", size=PT(10), bold=True, color=BLACK, font=FONT), run(" – ", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), run("Integrated across multiple value chain steps (largely Terminal Ops and/or Coordination)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="0E1924", line_width=19050))   # FFFFFF white
    out.append(picture(n(), "Picture 6", "rId9", IN(5.554), IN(6.043), IN(1), IN(0.244), src_rect={'t': 1, 'b': 30297}))
    out.append(picture(n(), "Picture 8", "rId10", IN(9.303), IN(6.05), IN(1.5), IN(0.231)))
    out.append(picture(n(), "Picture 10", "rId11", IN(11.511), IN(6.027), IN(1.2), IN(0.276)))
    out.append(picture(n(), "Picture 16", "rId12", IN(4.464), IN(6.004), IN(0.331), IN(0.321), src_rect={'l': 16902, 't': 18159, 'r': 16883, 'b': 17525}))
    out.append(picture(n(), "Picture 24", "rId13", IN(7.279), IN(5.994), IN(1.3), IN(0.342), src_rect={'l': 1136, 't': 2363, 'r': 1895}))
    # ── callouts — centered both ways; pointer geometry is independent of text padding ──
    for _x, _y, _cx, _cy, _fill, _t in _CALLOUTS:
        out.append(text_box(n(), "Callout", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val 44715", "adj2": "val -24439"}, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 1058", IN(2.691), IN(1.361), _MARK_W, _MARK_W, [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="447BB2", line_width=19050, anchor="ctr"))   # 447BB2 blue outline
    # ── more logos ──
    out.append(picture(n(), "Picture 20", "rId14", IN(8.693), IN(5.026), IN(1.38), IN(0.273)))
    out.append(picture(n(), "Picture 22", "rId15", IN(9.458), IN(5.251), IN(1), IN(0.204)))
    out.append(picture(n(), "Picture 2", "rId16", IN(8.705), IN(5.466), IN(0.884), IN(0.244)))
    out.append(picture(n(), "Picture 30", "rId17", IN(9.609), IN(2.812), IN(0.8), IN(0.203)))
    out.append(picture(n(), "Picture 16", "rId18", IN(9.559), IN(2.565), IN(0.9), IN(0.103)))
    out.append(picture(n(), "Picture 24", "rId19", IN(8.843), IN(2.493), IN(0.5), IN(0.248)))
    out.append(picture(n(), "Picture 2", "rId20", IN(8.693), IN(2.831), IN(0.8), IN(0.201), src_rect={'l': 6989, 't': 38971, 'r': 6559, 'b': 39290}))
    out.append(picture(n(), "Picture 30", "rId21", IN(9.082), IN(3.377), IN(1), IN(0.277)))
    out.append(picture(n(), "Picture 4", "rId22", IN(8.78), IN(3.968), IN(1.604), IN(0.205), src_rect={'t': 43928, 'b': 43272}))
    out.append(picture(n(), "Picture 6", "rId23", IN(8.782), IN(4.245), IN(1.6), IN(0.164), src_rect={'t': 44933, 'b': 44796}))
    out.append(picture(n(), "Picture 2080", "rId2", IN(11.151), IN(5.382), IN(1.186), IN(0.273)))
    out.append(picture(n(), "Picture 2081", "rId3", IN(11.134), IN(5.038), IN(1.221), IN(0.248), src_rect={'t': 39246, 'b': 40454}))
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
