"""value_chain_participation - Commercial Strategy deck, source slide 31.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=7, connector=5, chart=0, table=2, picture=24, chrome_builders=3, clusters=4 (covering 14 shapes), raw_verbatim=0, dropped=2, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, table, trow, tcell, breadcrumb, title_placeholder, prelim_chip,
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


# ── layout anchors (shared coordinates) ──
_LBL_Y, _LBL_W, _LBL_H = IN(1.641), IN(2.1), IN(0.4)
_LBL3_Y, _LBL3_H = IN(1.344), IN(0.236)
_Y1 = IN(2.087)   # shared x4
_H1 = IN(4.9)   # shared x4
_W1 = IN(0.2)   # shared x6

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, fill, label) x3
    (6.465, "447BB2", "Origin Shoreside Logistics"),
    (10.695, "447BB2", "Destination Shoreside Logistics"),
    (8.58, "0E1924", "Maritime Transport"),
]

_LABELS2 = [    # (x, y, cx, cy, line, label) x5
    (6.527, 4.782, 1.876, 0.926, "447BB2", "Terminal Operators"),
    (8.643, 4.782, 1.877, 0.926, "0E1924", "Charter Companies"),
    (8.643, 2.193, 1.877, 0.885, "0E1924", "Pure-play Shipbuilders"),
    (8.643, 3.137, 1.877, 1.586, "0E1924", "Integrated Shipbuilders"),
    (10.807, 4.782, 1.876, 0.926, "447BB2", "Terminal Operators"),
]

_LABELS3 = [    # (x, cx, label) x3
    (0.684, 2.018, "Primarily Maritime Transport Players"),
    (4.646, 1.189, "Integrated Shippers"),
    (2.881, 1.587, "Shoreside Logistics Players"),
]

_CALLOUTS = [    # (x, y, cx, cy, fill, label) x3
    (2.337, 2.32, 1.944, 0.482, WHITE, "Players shown own and operate their own vessels and charter additional ships "),
    (8.778, 3.726, 1.607, 0.169, None, "Entered shipping in ‘24"),
    (8.778, 4.482, 1.607, 0.168, None, "Chartering"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(connector(n(), "Straight Arrow Connector 1032", IN(4.291), _Y1, IN(0), _H1, color="808080", width=3175, dashed=True, flip_h=True))
    out.append(connector(n(), "Straight Arrow Connector 1036", IN(6.404), _Y1, IN(0), _H1, color="808080", width=3175, dashed=True, flip_h=True))
    out.append(connector(n(), "Straight Arrow Connector 1038", IN(8.526), _Y1, IN(0), _H1, color="808080", width=3175, dashed=True, flip_h=True))
    out.append(connector(n(), "Straight Arrow Connector 1040", IN(10.631), _Y1, IN(0), _H1, color="808080", width=3175, dashed=True, flip_h=True))
    out.append(text_box(n(), "Rectangle 41", IN(2.49), IN(6.428), IN(10.305), IN(0.551), [paragraph([run("Shippers / Private Carriers – ", size=PT(10), bold=True, color=BLACK, font=FONT), run("Integrated across value chain steps", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color=BLACK, line_width=19050, dashed_line=True))
    out.append(breadcrumb("Commercial Maritime Value Chain", "Overview"))
    out.append(title_placeholder("Value Chain Participation", "Shipbuilders largely not observed to vertically integrate beyond chartering, whereas large shippers and VOCCs integrate across the value chain."))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 22", IN(0.495), IN(2.193), IN(1.6), IN(4.794), col_widths=[IN(1.6)], rows=[
        trow([tcell("Representative players", size=PT(10), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": {"color": BLACK, "width": 38100}, "T": "none", "B": "none"})], h=IN(4.794)),
    ]))
    for _x, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), _LBL_Y, _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr")], fill=_fill, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    out.append(text_box(n(), "Pfeil: Fünfeck 4", IN(2.235), IN(1.641), IN(2.1), IN(0.4), [paragraph([run("Customer / Shipper Requires Cargo Shipment", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_2, line_color="none", prst="homePlate", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    out.append(text_box(n(), "Pfeil: Chevron 5", IN(4.35), IN(1.641), IN(2.1), IN(0.4), [paragraph([run("Coordination", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_2, line_color="none", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=144000, t_ins=108000, r_ins=144000, b_ins=108000))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 46", IN(0.495), IN(1.641), IN(1.6), IN(0.4), col_widths=[IN(1.6)], rows=[
        trow([tcell("Value Chain Step", size=PT(10), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": {"color": BLACK, "width": 38100}, "T": "none", "B": "none"})], h=IN(0.4)),
    ]))
    for _x, _y, _cx, _cy, _lc, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color=_lc, line_width=19050))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId2", IN(6.871), IN(5.382), IN(1.186), IN(0.273)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 4", "rId3", IN(6.854), IN(5.038), IN(1.221), IN(0.248), src_rect={'t': 39246, 'b': 40454}))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 6", "rId4", IN(4.778), IN(6.709), IN(1.24), IN(0.226)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 14", "rId5", IN(6.825), IN(6.703), IN(0.744), IN(0.237)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId6", IN(2.733), IN(6.712), IN(1.157), IN(0.219)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 4", "rId7", IN(10.197), IN(6.698), IN(1.074), IN(0.248)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 18", "rId8", IN(11.902), IN(6.674), IN(0.661), IN(0.296)))
    # DROPPED <p:pic> ? (no media target or geometry)
    out.append(text_box(n(), "Rectangle 20", IN(0.495), IN(1.361), _W1, _W1, [paragraph([], align="ctr")], fill=None, line_color="0E1924", line_width=19050, anchor="ctr"))
    for _x, _cx, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), _LBL3_Y, IN(_cx), _LBL3_H, [paragraph([run(_t, size=PT(8), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "Rectangle 24", IN(4.457), IN(1.361), _W1, _W1, [paragraph([], align="ctr")], fill=WHITE, line_color=BLACK, line_width=19050, dashed_line=True, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 52", IN(0.532), IN(3.999), IN(4.662), IN(0.746), color=BLACK, width=12700, arrow=True, prst="bentConnector4", rot=5400000, adj={"adj1": "val 47046", "adj2": "val 133516"}))
    out.append(text_box(n(), "Rectangle 9", IN(4.35), IN(5.769), IN(8.445), IN(0.6), [paragraph([run("Vessel Operating Common Carriers", size=PT(10), bold=True, color=BLACK, font=FONT), run(" – ", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), run("Integrated across multiple value chain steps (largely Terminal Ops and/or Coordination)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color="0E1924", line_width=19050))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 6", "rId9", IN(5.554), IN(6.043), IN(1), IN(0.244), src_rect={'t': 1, 'b': 30297}))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 8", "rId10", IN(9.303), IN(6.05), IN(1.5), IN(0.231)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 10", "rId11", IN(11.511), IN(6.027), IN(1.2), IN(0.276)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 16", "rId12", IN(4.464), IN(6.004), IN(0.331), IN(0.321), src_rect={'l': 16902, 't': 18159, 'r': 16883, 'b': 17525}))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 24", "rId13", IN(7.279), IN(5.994), IN(1.3), IN(0.342), src_rect={'l': 1136, 't': 2363, 'r': 1895}))
    for _x, _y, _cx, _cy, _fill, _t in _CALLOUTS:
        out.append(text_box(n(), "Callout", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=_fill, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val 44715", "adj2": "val -24439"}, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 1058", IN(2.691), IN(1.361), _W1, _W1, [paragraph([], align="ctr")], fill=None, line_color="447BB2", line_width=19050, anchor="ctr"))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 20", "rId14", IN(8.693), IN(5.026), IN(1.38), IN(0.273)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 22", "rId15", IN(9.458), IN(5.251), IN(1), IN(0.204)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId16", IN(8.705), IN(5.466), IN(0.884), IN(0.244)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 30", "rId17", IN(9.609), IN(2.812), IN(0.8), IN(0.203)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 16", "rId18", IN(9.559), IN(2.565), IN(0.9), IN(0.103)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 24", "rId19", IN(8.843), IN(2.493), IN(0.5), IN(0.248)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId20", IN(8.693), IN(2.831), IN(0.8), IN(0.201), src_rect={'l': 6989, 't': 38971, 'r': 6559, 'b': 39290}))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 30", "rId21", IN(9.082), IN(3.377), IN(1), IN(0.277)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 4", "rId22", IN(8.78), IN(3.968), IN(1.604), IN(0.205), src_rect={'t': 43928, 'b': 43272}))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 6", "rId23", IN(8.782), IN(4.245), IN(1.6), IN(0.164), src_rect={'t': 44933, 'b': 44796}))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2080", "rId2", IN(11.151), IN(5.382), IN(1.186), IN(0.273)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2081", "rId3", IN(11.134), IN(5.038), IN(1.221), IN(0.248), src_rect={'t': 39246, 'b': 40454}))
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
