"""ships_act_overview — Commercial Strategy market-analysis deck (20260325), source slide 11.

EXHIBIT — "SHIPS Act Overview": foreign penalties fund the domestic Strategic
Commercial Fleet (SCF). A bottom-to-top money-flow diagram — foreign vessel
owners/operators pay penalties (regular tonnage taxes, cargo fees) into the
Maritime Security Trust Fund ($20B cap, FY26-FY35), which disburses capital &
operating subsidies to US shipbuilders and US-built/US-flagged owners to build out
the SCF (250 foreign-trade-only ships, permanently Jones-Act-ineligible). Three
left-column tier bands (US Shipbuilders / US-Built-Flagged Owners / Foreign
Owners) group the rows; flag icons mark operator tiers; elbow connectors route the
flows; a speech bubble notes US-crew requirements.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ......... title_placeholder() + breadcrumb() (a background Rectangle
                     203 paints first, before the chrome)
  • _FLOW_NODES .... connected boxes; fill and text contrast are row fields
  • _GROUP_HEADERS . the 3 tall left-column tier bands
  • money bands .... Maritime Security Trust Fund / Cargo Fees / tonnage-tax boxes
                     (the _BAND_H rectangles)
  • _EDGE_LABELS .... small italic verbs riding the arrows (Sells / Buys / Pays / …)
  • icons .......... flag/marker pictures (rId2 once, rId3 reused ×3)
  • connectors ..... elbow + straight-arrow money-flow routing
  • callout ........ US-crew-requirement speech bubble

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=10, connector=15, picture=4, chrome_builders=2,
clusters=4 (covering 19 shapes), dropped=1 (think-cell OLE frame).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
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


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_FLOW_NODE_H = IN(0.321)  # connected flow-node box height
_TIER_X, _TIER_W, _TIER_H = IN(1.161), IN(1.5), IN(1.2)   # left-column tier-band geometry
_BAND_H = IN(0.321)       # money-band box height                 [shared x4]
_ELBOW_W = IN(0.565)      # elbow/arrow connector width            [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the eight money-flow boxes of the SHIPS Act funding diagram (foreign penalties
#   -> Strategic Fund -> domestic shipbuilding); the text_color row field carries the source
#   light/dark styling (black-text vs white-text nodes).
_FLOW_NODES = [    # (x, y, cx, fill, text_color, label) x8 — connected boxes; style is row data
    (8.792, 6.652, 2, GRAY_1, BLACK, "Other foreign ship operators"),   # F2F2F2 off-white
    (7.831, 4.321, 2.46, "6DCF9E", BLACK, "Operating Subsidies"),   # 6DCF9E mint green
    (6.847, 6.652, 1.9, GRAY_2, BLACK, "25-49% of orderbook at PRC"),   # D9D9D9 light gray
    (4.795, 6.652, 1.9, GRAY_3, BLACK, "50% of orderbook / fleet from PRC"),   # BFBFBF silver-gray
    (5.288, 4.321, 2.46, "3D9970", WHITE, "Capital Subsidies"),   # 3D9970 green
    (2.744, 2.87, 2.462, "447BB2", WHITE, "US Built Ships"),   # 447BB2 blue
    (2.744, 5.765, 6.002, "C00000", WHITE, "Penalties"),   # C00000 dark red
    (2.744, 6.652, 1.9, "A6A6A6", WHITE, "PRC owned/operated"),   # A6A6A6 mid-gray
]

# local_meaning: the three tall left-column tier bands labeling the flow rows (funding source /
#   mechanism / destination).
_GROUP_HEADERS = [    # (y, fill, label) x3 — tall left-column tier bands
    (1.418, "223E59", "US Shipbuilders"),   # 223E59 navy
    (2.87, "447BB2", "US-Built, US-Flagged Vessel Owners / Operators"),   # 447BB2 blue
    (5.773, "808080", "Foreign Vessel Owners / Operators"),   # 808080 gray
]

# local_meaning: the eight small italic verbs riding the connector arrows (the action on each
#   money-flow edge).
_EDGE_LABELS = [    # (x, y, cx, cy, label) x8 — small italic verbs riding the arrows
    (2.975, 1.927, 0.605, 0.181, "Sells"),
    (5.287, 3.887, 5.003, 0.182, "Paid to US vessel owner / operators for each ship in SCF"),
    (6.56, 4.963, 2.46, 0.182, "Disburses"),
    (6.287, 2.787, 1.444, 0.198, "Placed into service "),
    (2.054, 2.65, 0.605, 0.181, "Buys"),
    (5.438, 6.284, 0.615, 0.182, "Pays"),
    (9.484, 6.284, 0.615, 0.182, "Pays"),
    (11.479, 6.278, 0.615, 0.182, "Pays"),
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
    # ── background band, then chrome (note: title precedes breadcrumb in paint order) ──
    out.append(text_box(n(), "Rectangle 203", IN(2.713), IN(6.539), IN(8.123), IN(0.496), [paragraph([], align="ctr", line_spacing=100000)], fill="DFE7EB", line_color=BLACK, anchor="ctr"))   # DFE7EB pale blue
    out.append(title_placeholder("SHIPS Act Overview", "Foreign penalties fund domestic Strategic Commercial Fleet (SCF) build-out."))
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    # ── flow nodes — connected boxes; fill and text contrast come from each row ──
    # Shape text is centered vertically/horizontally; default insets are retained.
    for _x, _y, _cx, _fill, _txt, _t in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _FLOW_NODE_H, [paragraph([run(_t, size=PT(10), bold=True, color=_txt, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    # ── money band: regular tonnage taxes ──
    out.append(text_box(n(), "Rectangle 20", IN(8.791), IN(5.765), IN(2), _BAND_H, [paragraph([run("Regular Tonnage Taxes ", size=PT(10), bold=True, color=BLACK, font=FONT), line_break(), run("(Subject to exemptions)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="FFC000", line_color=BLACK, anchor="ctr"))   # FFC000 amber
    # ── left-column tier bands ──
    for _y, _fill, _t in _GROUP_HEADERS:
        out.append(text_box(n(), "Label", _TIER_X, IN(_y), _TIER_W, _TIER_H, [paragraph([run(_t, size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=BLACK, anchor="ctr"))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 4", "rId2", IN(0.287), IN(6.173), IN(0.6), IN(0.4)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(0.207), IN(1.818), IN(0.76), IN(0.4)))
    out.append(text_box(n(), "Rectangle 37", IN(1.161), IN(4.321), IN(1.5), IN(1.2), [paragraph([run("US Government", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="99B9D8", line_color=BLACK, anchor="ctr"))   # 99B9D8 light blue
    # ── money band: Maritime Security Trust Fund ──
    out.append(text_box(n(), "Rectangle 39", IN(2.744), IN(5.2), IN(10.092), _BAND_H, [paragraph([run("Maritime Security Trust Fund ", size=PT(10), bold=True, color=WHITE, font=FONT), run("($20B cap, appropriations specified from FY26-FY35)", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="1B4332", line_color=BLACK, anchor="ctr"))   # 1B4332 dark green
    out.append(connector(n(), "Connector: Elbow 43", IN(4.437), IN(5.344), _ELBOW_W, IN(2.051), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, flip_v=True, rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 44", IN(6.488), IN(5.344), _ELBOW_W, IN(2.051), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 50", IN(6.646), IN(4.621), IN(0.244), IN(2.045), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, flip_v=True, rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 54", IN(8.669), IN(4.643), IN(0.244), IN(2.001), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))   # 000000 black
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(0.207), IN(3.27), IN(0.76), IN(0.4)))
    # <p:pic> image (bytes copied into slides/images/, wired via IMAGES)
    out.append(picture(n(), "Picture 2", "rId3", IN(0.207), IN(4.721), IN(0.76), IN(0.4)))
    out.append(connector(n(), "Connector: Elbow 65", IN(8.147), IN(4.286), IN(0.558), IN(1.271), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_h=True, flip_v=True, rot=5400000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 69", IN(6.875), IN(4.285), IN(0.558), IN(1.272), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 72", IN(2.661), IN(2.018), IN(1.314), IN(0.852), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 86", IN(4.681), IN(2.485), IN(1.131), IN(2.543), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 89", IN(5.953), IN(1.213), IN(1.131), IN(5.086), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))   # 000000 black
    # ── SCF target box ──
    out.append(text_box(n(), "Rectangle 121", IN(8.747), IN(2.334), IN(4.088), IN(0.819), [paragraph([run("Strategic Commercial Fleet (SCF)", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("(250 commercial ships for foreign trade only; ", size=PT(10), italic=True, color=WHITE, font=FONT), run("permanently ineligible for coastwise trade i.e., Jones Act", size=PT(10), bold=True, italic=True, color=WHITE, font=FONT), run(")", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="0E1924", line_color=BLACK, anchor="ctr"))   # 0E1924 near-black navy
    # ── edge labels riding the arrows ──
    for _x, _y, _cx, _cy, _t in _EDGE_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    out.append(connector(n(), "Connector: Elbow 137", IN(5.206), IN(2.744), IN(3.541), IN(0.286), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 147", IN(1.911), IN(2.618), IN(0), IN(0.252), color=BLACK, width=12700, arrow=True, flip_v=True))   # 000000 black
    out.append(text_box(n(), "Rectangle 167", IN(9.754), IN(1.418), IN(3.08), IN(0.595), [paragraph([run("Vessel and Shipyard Investment Tax Credits (40% and 25%, respectively) from Building Ships in America Act not shown", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, anchor="ctr"))   # 000000 black outline
    out.append(connector(n(), "Straight Arrow Connector 189", IN(5.745), IN(6.087), IN(0), _ELBOW_W, color=BLACK, width=12700, arrow=True, flip_v=True))   # 000000 black
    out.append(connector(n(), "Straight Arrow Connector 193", IN(9.791), IN(6.087), IN(0), _ELBOW_W, color=BLACK, width=12700, arrow=True, flip_h=True, flip_v=True))   # 000000 black
    # ── money band: cargo fees (SHIPS Act "Plus") ──
    out.append(text_box(n(), "Rectangle 196", IN(10.836), IN(5.765), IN(2), _BAND_H, [paragraph([run("Cargo Fees ($0.01+ / kg)", size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run("SHIPS Act “Plus” only", size=PT(10), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="FB6B3C", line_color=BLACK, anchor="ctr"))   # FB6B3C orange
    out.append(connector(n(), "Connector: Elbow 204", IN(10.836), IN(6.087), IN(1), IN(0.7), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_v=True))   # 000000 black
    out.append(connector(n(), "Connector: Elbow 208", IN(9.691), IN(3.62), IN(0.244), IN(4.046), color=BLACK, width=12700, arrow=True, prst="bentConnector3", flip_v=True, rot=16200000))   # 000000 black
    out.append(text_box(n(), "Rectangle 211", IN(0.174), IN(6.652), IN(0.827), _BAND_H, [paragraph([run("+ ROW", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 8", IN(0.139), IN(1.12), IN(3.08), IN(0.245), [paragraph([run("Chart reads from bottom to top", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── callout: US-crew requirement ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 1", IN(4.61), IN(2.173), IN(1.958), IN(0.51), [paragraph([run("US crew required to participate in SCF; SHIPS Act states vessels will be crewed IAW ", size=PT(8), italic=True, color=BLACK, font=FONT), run("46 USC 8103", size=PT(8), italic=True, color=BLACK, font=FONT), run(" ", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, prst="wedgeRectCallout", geom_adj={"adj1": "val 41650", "adj2": "val 74944"}, anchor="ctr"))   # 000000 black outline
    return "".join(out)


def render() -> str:
    return slide(_body())
