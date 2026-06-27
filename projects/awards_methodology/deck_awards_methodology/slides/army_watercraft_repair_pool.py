"""army_watercraft_repair_pool — Strategic Contracts deck (20260624), source slide 3.

EXHIBIT — "Army Watercraft Ship-Repair Pool": holder-gated IDIQ access shifts
direct entry to the successor vehicle. A dated on-ramp timeline runs the active
ordering period (74 delivery orders, $416.8M realized) from the 2021-01-27 start
to the common last order date 2026-01-25, then an open-turnover window where no
successor is yet visible in the data (inferred 2026-06-24). Three regional
sub-pools — CONUS, Japan/Korea, Forward OCONUS — break out obligated-of-ceiling,
seats, and orders, while an Award Anatomy table reads the instrument, competition,
timing trigger, dollars, funding, and route to revenue. Marker colour keys
DATE-CERTAIN events apart from INFERRED ones.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome .................. breadcrumb() + prelim_chip() + title_placeholder()
  • timeline header ......... "Dated on-ramp…" caption + baseline rule connector
  • timeline legend ......... DATE-CERTAIN vs INFERRED labels keying marker colour
  • ordering bands .......... "Active Ordering Period" + "Open Turnover" bands and
                             their ordering-period / turnover baseline rules
  • _MILESTONE_MARKERS ...... three coloured tick dots on the rule (start /
                             last-order / successor); painted interleaved with…
  • _MILESTONE_DESCRIPTIONS . the caption under each tick, plus the standalone
                             "Milestone Tick" connectors and "Milestone Date" boxes
  • _SUBPOOL_CARDS .......... three white sub-pool card frames under the
                             "Three regional sub-pools" caption
  • _SUBPOOL_REGIONS ........ coloured region header chips (CONUS / Japan-Korea /
                             Forward OCONUS) on the cards
  • sub-pool bodies ......... per-pool vehicle id · obligated-of-ceiling · seats·orders
  • award anatomy ........... title + native table() (attribute / read / relevance)
  • structural overlay ...... right-brace + drop connector tying timeline to cards

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=14, connector=7, table=1, chrome_builders=3, clusters=4
(covering 12 shapes), dropped=1 (think-cell OLE frame).
Residue: a title-like shape sits off the house title position, kept verbatim at
its source coordinates.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates; values unchanged from the raw port) ──
_MARKER_Y, _MARKER_W, _MARKER_H = IN(3.47), IN(0.16), IN(0.16)    # timeline milestone dot [x3]
_DESC_Y, _DESC_W, _DESC_H = IN(4.2), IN(1.2), IN(0.52)            # milestone description box [x3]
_CARD_Y, _CARD_W, _CARD_H = IN(5.159), IN(2.24), IN(1.34)        # sub-pool card frame [x3]
_REGION_Y, _REGION_W, _REGION_H = IN(5.209), IN(2.14), IN(0.3)   # sub-pool region chip [x3]
_LEFT_X = IN(0.495)   # left edge of timeline + sub-pool column [shared x4]
_ROW_H = IN(0.23)   # single-line text-box height [shared x4]
_CAPTION_H = IN(0.2)   # small caption / heading height [shared x4]
_SHARED_EXTENT = IN(0.86)   # milestone-date box width + sub-pool-body box height [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
_MILESTONE_MARKERS = [    # (x, fill, line) x3 — coloured tick dots on the timeline rule (start / last-order / successor)
    (1.2, BLACK, BLACK),
    (5.15, "223E59", "223E59"),
    (7, "007770", "007770"),
]

_MILESTONE_DESCRIPTIONS = [    # (x, label) x3 — caption under each milestone tick
    (0.68, "Ordering period starts"),
    (4.63, "Common last date to order\n(all 14 vehicles)"),
    (6.48, "No successor visible\nin available data"),
]

_SUBPOOL_CARDS = [    # (x) x3 — white card frame per regional sub-pool
    0.495,
    2.885,
    5.275,
]

_SUBPOOL_REGIONS = [    # (x, fill, label) x3 — coloured region header chip per card
    (0.545, "223E59", "CONUS"),
    (2.935, "447BB2", "Japan / Korea"),
    (5.325, "6F8DB9", "Forward OCONUS"),
]

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
    out.append(text_box(n(), "Timeline Header", _LEFT_X, IN(1.515), IN(7.02), _ROW_H, [paragraph([run("Dated on-ramp: contract data may indicate recompete opportunity", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="b", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(connector(n(), "Timeline Header Rule", _LEFT_X, IN(1.742), IN(7.02), IN(0), color=BLACK, width=12700))
    # ── timeline legend: date-certain vs inferred markers ──
    out.append(text_box(n(), "Date Certainty Label", IN(4.274), IN(1.95), IN(1.9), _CAPTION_H, [paragraph([run("DATE-CERTAIN", size=PT(8), bold=True, color="223E59", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Inference Label", IN(6.666), IN(1.95), IN(0.8), _CAPTION_H, [paragraph([run("INFERRED", size=PT(8), bold=True, color="007770", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── ordering-period & open-turnover bands (+ their baseline rules) ──
    out.append(text_box(n(), "Order Activity Band", IN(1.275), IN(2.22), IN(3.95), IN(0.78), [paragraph([run("Active Ordering Period", size=PT(12), bold=True, color=BLACK, font=FONT), line_break(), run("74 delivery orders  |  $416.8M realized", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color=DK, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Open Turnover Band", IN(5.225), IN(2.22), IN(1.85), IN(0.78), [paragraph([run("Open Turnover", size=PT(12), bold=True, color="007770", font=FONT), line_break(), run("S", size=PT(10), italic=True, color=BLACK, font=FONT), run("uccessor not seen", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="DCEFE8", line_color="007770", dashed_line=True, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(connector(n(), "Ordering Period Rule", IN(1.2), IN(3.55), IN(3.95), IN(0), color=BLACK, width=19050))
    out.append(connector(n(), "Turnover Window Rule", IN(5.15), IN(3.55), IN(1.85), IN(0), color="007770", width=19050, dashed=True, arrow=True))
    # ── timeline milestones: ticks · marker dots · dates · descriptions (interleaved paint order) ──
    out.append(connector(n(), "Milestone Tick", IN(1.28), IN(3.12), IN(0), IN(0.82), color=BLACK, width=12700))
    for _x, _fill, _lc in _MILESTONE_MARKERS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _MARKER_Y, _MARKER_W, _MARKER_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, prst="ellipse", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Milestone Date", IN(0.85), IN(3.98), _SHARED_EXTENT, _ROW_H, [paragraph([run("2021-01-27", size=PT(9), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    for _x, _t in _MILESTONE_DESCRIPTIONS:
        out.append(text_box(n(), "Label", IN(_x), _DESC_Y, _DESC_W, _DESC_H, [paragraph([run(_t, size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(connector(n(), "Milestone Tick", IN(5.23), IN(3.12), IN(0), IN(0.82), color="223E59", width=12700))
    out.append(text_box(n(), "Milestone Date", IN(4.8), IN(3.98), _SHARED_EXTENT, _ROW_H, [paragraph([run("2026-01-25", size=PT(9), bold=True, color="223E59", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    out.append(connector(n(), "Milestone Tick", IN(7.08), IN(3.12), IN(0), IN(0.82), color="007770", width=12700))
    out.append(text_box(n(), "Milestone Date", IN(6.65), IN(3.98), _SHARED_EXTENT, _ROW_H, [paragraph([run("2026-06-24", size=PT(9), bold=True, color="007770", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))
    # ── regional sub-pools: caption · card frames · region chips · bodies ──
    out.append(text_box(n(), "Subpool Caption", _LEFT_X, IN(4.919), IN(7.02), _CAPTION_H, [paragraph([run("Three regional sub-pools", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="b", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for _x in _SUBPOOL_CARDS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _CARD_Y, _CARD_W, _CARD_H, [paragraph([], line_spacing=100000)], fill=WHITE, line_color=DK, line_width=6350, l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    for _x, _fill, _t in _SUBPOOL_REGIONS:
        out.append(text_box(n(), "Label", IN(_x), _REGION_Y, _REGION_W, _REGION_H, [paragraph([run(_t, size=PT(10.5), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Subpool Body", _LEFT_X, IN(5.579), IN(2.24), _SHARED_EXTENT, [paragraph([run("W56HZV20RL807", size=PT(8), color="808080", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("$281.7M", size=PT(13), bold=True, color=BLACK, font=FONT), run(" obligated", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("of $529.0M ceiling (shared)", size=PT(8.5), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("6 seats", size=PT(9.5), bold=True, color=BLACK, font=FONT), run("  ·  ", size=PT(9.5), color="808080", font=FONT), run("40 orders", size=PT(9.5), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Subpool Body", IN(2.885), IN(5.579), IN(2.24), _SHARED_EXTENT, [paragraph([run("W56HZV20RL806", size=PT(8), color="808080", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("$123.2M", size=PT(13), bold=True, color=BLACK, font=FONT), run(" obligated", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("of $216.0M ceiling (shared)", size=PT(8.5), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("3 seats", size=PT(9.5), bold=True, color=BLACK, font=FONT), run("  ·  ", size=PT(9.5), color="808080", font=FONT), run("18 orders", size=PT(9.5), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Subpool Body", IN(5.275), IN(5.579), IN(2.24), _SHARED_EXTENT, [paragraph([run("W56HZV20RL805", size=PT(8), color="808080", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("$11.9M", size=PT(13), bold=True, color=BLACK, font=FONT), run(" obligated", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("of $186.0M ceiling (shared)", size=PT(8.5), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("5 seats", size=PT(9.5), bold=True, color=BLACK, font=FONT), run("  ·  ", size=PT(9.5), color="808080", font=FONT), run("16 orders", size=PT(9.5), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── award anatomy: title + native table ──
    out.append(text_box(n(), "Award Anatomy Title", IN(7.735), IN(1.515), IN(5.09), _CAPTION_H, [paragraph([run("Award Anatomy", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Award Anatomy Table", IN(7.735), IN(1.75), IN(5.09), IN(4.15), col_widths=[IN(1.12), IN(2.1), IN(1.87)], rows=[
        trow([tcell("Attribute", size=PT(10), bold=True, color=WHITE, align="ctr", fill=DK, borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Army watercraft read", size=PT(10), bold=True, color=WHITE, align="ctr", fill=DK, borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Relevance", size=PT(10), bold=True, color=WHITE, align="ctr", fill=DK, borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.3)),
        trow([tcell("Instrument / award structure", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Multiple-award IDIQ / IDC for non-nuclear ship repair", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Direct access is limited to vehicle holders during the ordering period", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),
        trow([tcell("Competition / holder set", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Full-and-open parent competition; 14 holder vehicles across 10 vendors", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("New entrants compete for a seat at the successor pool or on-ramp", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),
        trow([tcell("Timing trigger", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Last date to order: January 25, 2026", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Dates the entry window more precisely than a generic recompete estimate", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),
        trow([tcell("Obligated amount", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("$416.8M across 74 delivery orders", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Measures realized demand; this is the summable dollar measure", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),
        trow([tcell("Ceiling / potential value", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("$529.0M, $216.0M, and $186.0M regional ceilings shared within each sub-pool", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Shows capacity without overstating revenue", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.55)),
        trow([tcell("TAS / appropriation", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("021-2020 O&M, Army; 021-2035 Other Procurement, Army", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Confirms sustainment / procurement funding context", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.4)),
        trow([tcell("Route to revenue", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Direct to Government at successor holder selection; incumbent-chain route in the interim", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Bid the successor pool; subcontract or team with current holders before award", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.7)),
    ]))
    # ── structural overlay: timeline-to-cards brace + drop connector ──
    out.append(text_box(n(), "Right Brace 4", IN(3.779), IN(1.116), IN(0.48), IN(7.2), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=DK, prst="rightBrace", geom_adj={"adj1": "val 6721", "adj2": "val 39391"}, anchor="ctr", rot=16200000))
    out.append(connector(n(), "Straight Connector 9", IN(3.25), IN(3), IN(0.005), IN(1.476), color=BLACK, width=12700))
    return "".join(out)


def render() -> str:
    return slide(_body())
