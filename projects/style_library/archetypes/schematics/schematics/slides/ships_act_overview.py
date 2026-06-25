"""ships_act_overview - Commercial Strategy deck, source slide 11.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=10, connector=15, chart=0, table=0, picture=4, chrome_builders=2, clusters=4 (covering 19 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, line_break, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, GRAY_2, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []
IMAGES = [
    {"rId": "rId2", "file": "image6_9f2e24d3.png"},
    {"rId": "rId3", "file": "image7_f6006d1c.png"},
]


# ── layout anchors (shared coordinates) ──
_LBL_H = IN(0.321)
_LBL2_H = IN(0.321)
_LBL3_X, _LBL3_W, _LBL3_H = IN(1.161), IN(1.5), IN(1.2)
_H1 = IN(0.321)   # shared x4
_W1 = IN(0.565)   # shared x4

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, cx, fill, label) x4
    (8.792, 6.652, 2, GRAY_1, "Other foreign ship operators"),
    (7.831, 4.321, 2.46, "6DCF9E", "Operating Subsidies"),
    (6.847, 6.652, 1.9, GRAY_2, "25-49% of orderbook at PRC"),
    (4.795, 6.652, 1.9, GRAY_3, "50% of orderbook / fleet from PRC"),
]

_LABELS2 = [    # (x, y, cx, fill, label) x4
    (5.288, 4.321, 2.46, "3D9970", "Capital Subsidies"),
    (2.744, 2.87, 2.462, "447BB2", "US Built Ships"),
    (2.744, 5.765, 6.002, "C00000", "Penalties"),
    (2.744, 6.652, 1.9, "A6A6A6", "PRC owned/operated"),
]

_LABELS3 = [    # (y, fill, label) x3
    (1.418, "223E59", "US Shipbuilders"),
    (2.87, "447BB2", "US-Built, US-Flagged Vessel Owners / Operators"),
    (5.773, "808080", "Foreign Vessel Owners / Operators"),
]

_LABELS4 = [    # (x, y, cx, cy, label) x8
    (2.975, 1.927, 0.605, 0.181, "Sells"),
    (5.287, 3.887, 5.003, 0.182, "Paid to US vessel owner / operators for each ship in SCF"),
    (6.56, 4.963, 2.46, 0.182, "Disburses"),
    (6.287, 2.787, 1.444, 0.198, "Placed into service "),
    (2.054, 2.65, 0.605, 0.181, "Buys"),
    (5.438, 6.284, 0.615, 0.182, "Pays"),
    (9.484, 6.284, 0.615, 0.182, "Pays"),
    (11.479, 6.278, 0.615, 0.182, "Pays"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(text_box(n(), "Rectangle 203", IN(2.713), IN(6.539), IN(8.123), IN(0.496), [paragraph([], align="ctr")], fill="DFE7EB", line_color=BLACK, anchor="ctr"))
    out.append(title_placeholder("SHIPS Act Overview", "Foreign penalties fund domestic Strategic Commercial Fleet (SCF) build-out."))
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    for _x, _y, _cx, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL_H, [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=_fill, line_color=BLACK, anchor="ctr"))
    for _x, _y, _cx, _fill, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL2_H, [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr")], fill=_fill, line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 20", IN(8.791), IN(5.765), IN(2), _H1, [paragraph([run("Regular Tonnage Taxes ", size=PT(10), bold=True, color=BLACK, font=FONT), line_break(), run("(Subject to exemptions)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill="FFC000", line_color=BLACK, anchor="ctr"))
    for _y, _fill, _t in _LABELS3:
        out.append(text_box(n(), "Label", _LBL3_X, IN(_y), _LBL3_W, _LBL3_H, [paragraph([run(_t, size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill=_fill, line_color=BLACK, anchor="ctr"))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 4", "rId2", IN(0.287), IN(6.173), IN(0.6), IN(0.4)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(0.207), IN(1.818), IN(0.76), IN(0.4)))
    out.append(text_box(n(), "Rectangle 37", IN(1.161), IN(4.321), IN(1.5), IN(1.2), [paragraph([run("US Government", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr")], fill="99B9D8", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 39", IN(2.744), IN(5.2), IN(10.092), _H1, [paragraph([run("Maritime Security Trust Fund ", size=PT(10), bold=True, color=WHITE, font=FONT), run("($20B cap, appropriations specified from FY26-FY35)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr")], fill="1B4332", line_color=BLACK, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 43", IN(4.437), IN(5.344), _W1, IN(2.051), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, flip_v=True, rot=5400000))
    out.append(connector(n(), "Connector: Elbow 44", IN(6.488), IN(5.344), _W1, IN(2.051), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 50", IN(6.646), IN(4.621), IN(0.244), IN(2.045), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, flip_v=True, rot=5400000))
    out.append(connector(n(), "Connector: Elbow 54", IN(8.669), IN(4.643), IN(0.244), IN(2.001), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(0.207), IN(3.27), IN(0.76), IN(0.4)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(0.207), IN(4.721), IN(0.76), IN(0.4)))
    out.append(connector(n(), "Connector: Elbow 65", IN(8.147), IN(4.286), IN(0.558), IN(1.271), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, flip_v=True, rot=5400000))
    out.append(connector(n(), "Connector: Elbow 69", IN(6.875), IN(4.285), IN(0.558), IN(1.272), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 72", IN(2.661), IN(2.018), IN(1.314), IN(0.852), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Connector: Elbow 86", IN(4.681), IN(2.485), IN(1.131), IN(2.543), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 89", IN(5.953), IN(1.213), IN(1.131), IN(5.086), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))
    out.append(text_box(n(), "Rectangle 121", IN(8.747), IN(2.334), IN(4.088), IN(0.819), [paragraph([run("Strategic Commercial Fleet (SCF)", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("(250 commercial ships for foreign trade only; ", size=PT(10), italic=True, color=WHITE, font=FONT), run("permanently ineligible for coastwise trade i.e., Jones Act", size=PT(10), bold=True, italic=True, color=WHITE, font=FONT), run(")", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr")], fill="0E1924", line_color=BLACK, anchor="ctr"))
    for _x, _y, _cx, _cy, _t in _LABELS4:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 137", IN(5.206), IN(2.744), IN(3.541), IN(0.286), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))
    out.append(connector(n(), "Straight Arrow Connector 147", IN(1.911), IN(2.618), IN(0), IN(0.252), color=BLACK, width=12700, arrow=True, flip_v=True))
    out.append(text_box(n(), "Rectangle 167", IN(9.754), IN(1.418), IN(3.08), IN(0.595), [paragraph([run("Vessel and Shipyard Investment Tax Credits (40% and 25%, respectively) from Building Ships in America Act not shown", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color=BLACK, anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 189", IN(5.745), IN(6.087), IN(0), _W1, color=BLACK, width=12700, arrow=True, flip_v=True))
    out.append(connector(n(), "Straight Arrow Connector 193", IN(9.791), IN(6.087), IN(0), _W1, color=BLACK, width=12700, arrow=True, flip_h=True, flip_v=True))
    out.append(text_box(n(), "Rectangle 196", IN(10.836), IN(5.765), IN(2), _H1, [paragraph([run("Cargo Fees ($0.01+ / kg)", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("SHIPS Act “Plus” only", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr")], fill="FB6B3C", line_color=BLACK, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 204", IN(10.836), IN(6.087), IN(1), IN(0.7), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_v=True))
    out.append(connector(n(), "Connector: Elbow 208", IN(9.691), IN(3.62), IN(0.244), IN(4.046), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))
    out.append(text_box(n(), "Rectangle 211", IN(0.174), IN(6.652), IN(0.827), _H1, [paragraph([run("+ ROW", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 8", IN(0.139), IN(1.12), IN(3.08), IN(0.245), [paragraph([run("Chart reads from bottom to top", size=PT(10), italic=True, color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Speech Bubble: Rectangle 1", IN(4.61), IN(2.173), IN(1.958), IN(0.51), [paragraph([run("US crew required to participate in SCF; SHIPS Act states vessels will be crewed IAW ", size=PT(8), italic=True, color=BLACK, font=FONT), run("46 USC 8103", size=PT(8), italic=True, color=BLACK, font=FONT), run(" ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=None, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val 41650", "adj2": "val 74944"}, anchor="ctr"))
    return "".join(out)


def render() -> str:
    return slide(_body())
