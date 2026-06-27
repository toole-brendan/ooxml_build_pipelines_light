"""army_watercraft_repair_pool — Strategic Contracts deck (20260624), revised working module.

EXHIBIT — "Army Watercraft Ship-Repair Pool": holder-gated IDIQ access shifts
direct entry to the successor vehicle. A dated on-ramp timeline runs the active
ordering period (74 delivery orders, $416.8M realized) from the 2021-01-27 start
to the common last order date 2026-01-25, then an inferred turnover window where
no successor is visible in the available data as of 2026-06-24. Three regional
sub-pools — CONUS, Japan / Korea, and Forward OCONUS — show obligated value,
ceiling, seats, and delivery orders. An Award Anatomy table summarizes the
instrument, competition, timing trigger, dollars, funding, and route to revenue.

HOUSE-STYLE REVISION:
  • Regional card bodies use one 10-point type size; hierarchy comes from weight,
    italics, and color rather than four competing font sizes.
  • Peer regional headers use one blue fill rather than an arbitrary gradient.
  • The inferred timeline uses neutral gray and a dashed treatment, replacing
    green so color does not collide with addressability / price semantics.
  • The all-caps certainty labels are replaced with one sentence-case key.

CODE MAP (body follows source PAINT ORDER):
  • chrome .................. breadcrumb() + prelim_chip() + title_placeholder()
  • timeline header ......... caption + baseline rule
  • timeline key ............ solid contract data vs. dashed inferred window
  • ordering bands .......... active ordering + open turnover bands and rules
  • timeline milestones ..... start / last-order / inferred-as-of markers
  • regional sub-pools ...... three peer cards with normalized body typography
  • award anatomy ........... native table() (attribute / read / relevance)
  • structural overlay ...... right brace + drop connector tying timeline to cards
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_5, GRAY_1, GRAY_4, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_MARKER_Y, _MARKER_W, _MARKER_H = IN(3.47), IN(0.16), IN(0.16)    # timeline milestone dot [x3]
_DESC_Y, _DESC_W, _DESC_H = IN(4.2), IN(1.2), IN(0.52)            # milestone description box [x3]
_CARD_Y, _CARD_W, _CARD_H = IN(5.159), IN(2.24), IN(1.34)        # sub-pool card frame [x3]
_REGION_Y, _REGION_W, _REGION_H = IN(5.209), IN(2.14), IN(0.3)   # sub-pool region chip [x3]
_LEFT_X = IN(0.495)   # left edge of timeline + sub-pool column [shared x4]
_ROW_H = IN(0.23)   # single-line text-box height [shared x4]
_CAPTION_H = IN(0.2)   # small caption / heading height [shared x4]
_SHARED_EXTENT = IN(0.86)   # milestone-date box width + sub-pool-body box height [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the three timeline markers (ordering-period start / common last
#   order date / inferred as-of point). Solid vs. dashed treatment carries certainty.
_REFERENCE_MARKERS = [    # (x, fill, line) x3 — observed dates + inferred as-of point
    (1.2, BLACK, BLACK),
    (5.15, BLUE_5, BLUE_5),
    (7, GRAY_4, GRAY_4),
]

# local_meaning: the caption under each timeline milestone tick (start / last order /
#   successor).
_REFERENCE_LABELS = [    # (x, label, color, italic) x3 — milestone descriptions
    (0.68, "Ordering period starts", BLACK, False),
    (4.63, "Common last date to order\n(all 14 vehicles)", BLACK, False),
    (6.48, "No successor visible\nin available data", GRAY_4, True),
]

# local_meaning: regional peer cards. Keeping content and geometry in one data table
# ensures the three bodies inherit exactly the same type treatment.
# (frame_x, header_x, region, vehicle, obligated, ceiling, seats, orders)
_SUBPOOLS = [
    (0.495, 0.545, "CONUS", "W56HZV20RL807", "$281.7M", "$529.0M", "6", "40"),
    (2.885, 2.935, "Japan / Korea", "W56HZV20RL806", "$123.2M", "$216.0M", "3", "18"),
    (5.275, 5.325, "Forward OCONUS", "W56HZV20RL805", "$11.9M", "$186.0M", "5", "16"),
]

# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome: breadcrumb · prelim chip · title ──
    out.append(breadcrumb("Strategic Contracts", "Vehicle-Gated Access"))
    out.append(prelim_chip())
    out.append(title_placeholder("Army Watercraft Ship-Repair Pool", "Holder-gated IDIQ access shifts direct entry to the successor vehicle."))
    # ── timeline: header caption + baseline rule ──
    out.append(text_box(n(), "Timeline Header", _LEFT_X, IN(1.515), IN(7.02), _ROW_H, [paragraph([run("Dated on-ramp: contract data may indicate recompete opportunity", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="b", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    out.append(connector(n(), "Timeline Header Rule", _LEFT_X, IN(1.742), IN(7.02), IN(0), color=BLACK, width=12700))
    # ── timeline key: line style, not semantic green, carries certainty ──
    out.append(text_box(n(), "Timeline Key", IN(4.05), IN(1.95), IN(3.02), _CAPTION_H, [paragraph([run("Solid: contract data  |  Dashed: inferred", size=PT(8), italic=True, color=GRAY_4, font=FONT)], align="r", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    # ── ordering-period & open-turnover bands (+ their baseline rules) ──
    out.append(text_box(n(), "Order Activity Band", IN(1.275), IN(2.22), IN(3.95), IN(0.78), [paragraph([run("Active Ordering Period", size=PT(12), bold=True, color=BLACK, font=FONT), line_break(), run("74 delivery orders  |  $416.8M realized", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=DK, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # GRAY_1
    out.append(text_box(n(), "Open Turnover Band", IN(5.225), IN(2.22), IN(1.85), IN(0.78), [paragraph([run("Open Turnover", size=PT(12), bold=True, color=BLACK, font=FONT), line_break(), run("No visible successor", size=PT(10), italic=True, color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=GRAY_4, dashed_line=True, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(connector(n(), "Ordering Period Rule", IN(1.2), IN(3.55), IN(3.95), IN(0), color=BLACK, width=19050))
    out.append(connector(n(), "Turnover Window Rule", IN(5.15), IN(3.55), IN(1.85), IN(0), color=GRAY_4, width=19050, dashed=True, arrow=True))
    # ── timeline milestones: ticks · marker dots · dates · descriptions (interleaved paint order) ──
    out.append(connector(n(), "Milestone Tick", IN(1.28), IN(3.12), IN(0), IN(0.82), color=BLACK, width=12700))
    for _x, _fill, _lc in _REFERENCE_MARKERS:
        out.append(text_box(n(), "Timeline Marker", IN(_x), _MARKER_Y, _MARKER_W, _MARKER_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, prst="ellipse", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Milestone Date", IN(0.85), IN(3.98), _SHARED_EXTENT, _ROW_H, [paragraph([run("2021-01-27", size=PT(9), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    for _x, _t, _color, _italic in _REFERENCE_LABELS:
        out.append(text_box(n(), "Milestone Description", IN(_x), _DESC_Y, _DESC_W, _DESC_H, [paragraph([run(_t, size=PT(9), italic=_italic or None, color=_color, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(connector(n(), "Milestone Tick", IN(5.23), IN(3.12), IN(0), IN(0.82), color=BLUE_5, width=12700))
    out.append(text_box(n(), "Milestone Date", IN(4.8), IN(3.98), _SHARED_EXTENT, _ROW_H, [paragraph([run("2026-01-25", size=PT(9), bold=True, color=BLUE_5, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(connector(n(), "Milestone Tick", IN(7.08), IN(3.12), IN(0), IN(0.82), color=GRAY_4, width=12700))
    out.append(text_box(n(), "Milestone Date", IN(6.65), IN(3.98), _SHARED_EXTENT, _ROW_H, [paragraph([run("2026-06-24", size=PT(9), bold=True, color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    # ── regional sub-pools: caption · card frames · region chips · bodies ──
    out.append(text_box(n(), "Subpool Caption", _LEFT_X, IN(4.919), IN(7.02), _CAPTION_H, [paragraph([run("Three regional sub-pools", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="b", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    # Frames first, then headers, then bodies, preserving the source paint stack.
    for _frame_x, *_rest in _SUBPOOLS:
        out.append(text_box(n(), "Subpool Card Frame", IN(_frame_x), _CARD_Y, _CARD_W, _CARD_H, [paragraph([], line_spacing=100000)], fill=WHITE, line_color=DK, line_width=6350, l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    for _frame_x, _header_x, _region, *_rest in _SUBPOOLS:
        out.append(text_box(n(), "Subpool Region Header", IN(_header_x), _REGION_Y, _REGION_W, _REGION_H, [paragraph([run(_region, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    for _frame_x, _header_x, _region, _vehicle, _obligated, _ceiling, _seats, _orders in _SUBPOOLS:
        out.append(text_box(n(), "Subpool Body", IN(_frame_x), IN(5.579), _CARD_W, _SHARED_EXTENT, [paragraph([run(_vehicle, size=PT(10), color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000), paragraph([run(_obligated, size=PT(10), bold=True, color=BLACK, font=FONT), run(" obligated", size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run(f"{_ceiling} ceiling", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run(_seats, size=PT(10), bold=True, color=BLACK, font=FONT), run(" seats  ·  ", size=PT(10), color=GRAY_4, font=FONT), run(_orders, size=PT(10), bold=True, color=BLACK, font=FONT), run(" orders", size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── award anatomy: title + native table ──
    out.append(text_box(n(), "Award Anatomy Title", IN(7.735), IN(1.515), IN(5.09), _CAPTION_H, [paragraph([run("Award Anatomy", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    # Table layout: col_widths fix the three columns (attribute / read / relevance)
    # and trow(h=...) each row minimum; the 162029 header row anchors the cells while the
    # body rows repeat the white-fill / grey-rule border convention.
    # Rule/text palette: header fill 162029 (DK) + WHITE text; body text 000000 (BLACK); rules 000000 (BLACK) header · 808080 (rule-gray, ad-hoc ~GRAY_4) inner.
    out.append(table(n(), "Award Anatomy Table", IN(7.735), IN(1.75), IN(5.09), IN(4.15), col_widths=[IN(1.12), IN(2.1), IN(1.87)], rows=[
        trow([tcell("Attribute", size=PT(10), bold=True, color="FFFFFF", align="ctr", fill="162029", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}}), tcell("Army watercraft read", size=PT(10), bold=True, color="FFFFFF", align="ctr", fill="162029", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}}), tcell("Relevance", size=PT(10), bold=True, color="FFFFFF", align="ctr", fill="162029", borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}})], h=IN(0.3)),   # DK
        trow([tcell("Instrument / award structure", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Multiple-award IDIQ / IDC for non-nuclear ship repair", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Direct access is limited to vehicle holders during the ordering period", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),   # WHITE
        trow([tcell("Competition / holder set", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Full-and-open parent competition; 14 holder vehicles across 10 vendors", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("New entrants compete for a seat at the successor pool or on-ramp", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),   # WHITE
        trow([tcell("Timing trigger", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Last date to order: January 25, 2026", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Dates the entry window more precisely than a generic recompete estimate", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),   # WHITE
        trow([tcell("Obligated amount", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("$416.8M across 74 delivery orders", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Measures realized demand; this is the summable dollar measure", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),   # WHITE
        trow([tcell("Ceiling / potential value", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("$529.0M, $216.0M, and $186.0M regional ceilings shared within each sub-pool", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Shows capacity without overstating revenue", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),   # WHITE
        trow([tcell("TAS / appropriation", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("021-2020 O&M, Army; 021-2035 Other Procurement, Army", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Confirms sustainment / procurement funding context", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.4)),   # WHITE
        trow([tcell("Route to revenue", size=PT(9), bold=True, color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Direct to Government at successor holder selection; incumbent-chain route in the interim", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Bid the successor pool; subcontract or team with current holders before award", size=PT(9), color="000000", fill="FFFFFF", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.7)),   # WHITE
    ]))
    # ── structural overlay: timeline-to-cards brace + drop connector ──
    out.append(text_box(n(), "Right Brace 4", IN(3.779), IN(1.116), IN(0.48), IN(7.2), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=DK, prst="rightBrace", geom_adj={"adj1": "val 6721", "adj2": "val 39391"}, anchor="ctr", rot=16200000))   # DK
    out.append(connector(n(), "Straight Connector 9", IN(3.25), IN(3), IN(0.005), IN(1.476), color=BLACK, width=12700))
    return "".join(out)


def render() -> str:
    return slide(_body())
