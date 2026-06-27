"""addressability_decision_cascade — Federal Award Addressability deck, method opener (slide 01).

EXHIBIT — "Addressability": the generalized decision cascade that teaches the reader
to read *any* federal award and answer one question — is there reachable revenue
here, and by what route? A left-hand vertical cascade walks five gates top-to-bottom
(Demand × Access × Timing × Ability to perform × Economics), each muted gate box
paired with an italic pass/redirect verdict in the middle column. Two focal accent
bands break the stack: the ADDRESSABLE MARKET waypoint (after Gate 1) and the
full-width ROUTE LEAVES row (after Gate 5) — the focal pair — with the Access gate
rendered as the mid-blue pivot that turns between them. The four route leaves
(Bid the recompete · On-ramp · Subcontract/teaming · Consortium/OT) each carry the
posture that leads to them; the Subcontract and Consortium leaves fold in the two
reframes (closed prime ≠ closed market; enter early). A right-rail finding panel
states the lesson and its supports; a dashed portal-visibility band sits apart
beneath the leaves (a property of the set, not a gate).

This is a generalized method slide — no dataset figures on the face; postures are
named in real terms (e.g., "a multiple-award IDIQ on FAR 16.505 fair opportunity")
rather than as specific programs or dollars.

CODE MAP (body follows paint order; headers mark roles in place):
  • chrome ........... breadcrumb() + title_placeholder() (the event-probability vs.
                       addressability one-liner leads the right-rail panel)
  • right-rail ....... single-cell table() — bold finding + bulleted supports
                       (tcell_rich()/tpara()/trun(); light DFE7EB panel)
  • ADDRESSABLE band . focal accent box (223E59 / white) — the first focal stop
  • _GATES ........... the cascade — precondition + five gate boxes (muted white,
                       Access = 447BB2 pivot) each emitting its Zone-B verdict → loop
  • cascade arrow .... straight down-arrow from the gate stack into the route leaves
  • _ROUTE_LEAVES .... the four route-to-revenue boxes (focal pair, 223E59 / white),
                       posture + folded-in reframes → loop
  • portal overlay ... dashed band set apart beneath the leaves (not in the cascade)
  • sources .......... sources_line() footnote (authorities)

Authored from the slide spec (slide_01_addressability_funnel.md) in the house module
idiom — chrome builders, stacked accent boxes, loop-driven repeated shapes — rather
than auto-converted from a source deck.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, connector, table, trow, tcell_rich, tpara, trun, breadcrumb, title_placeholder, sources_line,
)
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_GATE_X, _GATE_W = IN(0.495), IN(4.35)     # cascade gate-box column (Zone A)
_VERD_X, _VERD_W = IN(5.0), IN(3.95)       # pass/redirect verdict column (Zone B)
_ROW_H = IN(0.44)                          # gate / verdict row height        [shared x6]
_BAND_X, _BAND_W = IN(0.495), IN(8.455)    # focal band span (Zone A + Zone B)
_RAIL_X, _RAIL_W = IN(9.12), IN(3.66)      # right-rail finding panel (Zone C)
_LEAF_Y, _LEAF_W, _LEAF_H = IN(5.54), IN(2.985), IN(0.96)   # route-leaf geometry [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_GATES = [    # (y, fill, line, line_w, txt, name, criterion, verdict) x6 — precondition + five gates; Access = pivot
    (1.54, GRAY_3, "808080", 12700, BLACK,
     "Precondition · Classify the record",
     "Name the object: IDV ≠ IDIQ; contract type ≠ award structure",
     "Mislabel the record and every gate below is wrong."),
    (2.04, WHITE, "808080", 12700, BLACK,
     "Gate 1 · Demand, not capacity",
     "Obligated orders & quantity-adds = demand; ceiling / options = capacity",
     "Fail → a ceiling, empty BPA/BOA, or unexercised option is not yet revenue — track for actual orders."),
    (3.06, "447BB2", "223E59", 28575, WHITE,
     "Gate 2 · Access — the pivot",
     "extentCompeted · single- vs. multiple-award · FAR 16.505 fair opportunity",
     "Fail as prime → multiple-/single-award or sole-source redirects off-prime; pass → open recompete, be prime."),
    (3.56, WHITE, "808080", 12700, BLACK,
     "Gate 3 · Timing",
     "Period of performance · ordering-period end · option dates · bridges",
     "Fail → an option exercise (FAR 17.207) or a vehicle mid-ordering-period: monitor, don't act."),
    (4.06, WHITE, "808080", 12700, BLACK,
     "Gate 4 · Ability to perform",
     "Responsibility · past performance · FCL · CAS / DCAA · flowdowns",
     "Fail → not yet qualified: qualify, team, or subcontract."),
    (4.56, WHITE, "808080", 12700, BLACK,
     "Gate 5 · Economics",
     "Contract type & payment risk · financing · data rights · compliance burden",
     "Fail → economics don't fit: pass, or pursue a different tier."),
]

_ROUTE_LEAVES = [    # (x, title, posture, reframe-lead, reframe-rest) x4 — the two reframes fold into leaves 3 & 4
    (0.495, "Bid the recompete",
     "Open standalone / full-and-open recompete — compete as prime.",
     "", ""),
    (3.6, "On-ramp",
     "Multiple-award IDIQ — seat as a holder when the pool re-competes.",
     "Worked on ", "slide 03."),
    (6.705, "Subcontract / teaming",
     "Closed prime · single-award · sole-source — FAR 9.6 CTA or prime-sub.",
     "Closed prime ≠ closed market: ", "MYP / block buys release AP/LLTM & EOQ below the prime (slide 02)."),
    (9.81, "Consortium / OT",
     "Innovation pathway — enter at the prototype / consortium stage.",
     "Enter early: ", "OT prototype → production follow-on; SBIR/STTR Phase III sole-source."),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome ──
    out.append(breadcrumb("Award Addressability", "Generalized Decision Cascade"))
    out.append(title_placeholder("Addressability", "A large award isn't an opportunity until it clears five gates — and the gate it fails as prime names the route in."))
    # ── right-rail finding panel — event-vs-addressability lead, bold finding, bulleted supports ──
    out.append(table(n(), "Right Rail", _RAIL_X, IN(1.54), _RAIL_W, IN(3.46), col_widths=[_RAIL_W], rows=[
        trow([tcell_rich([
            tpara([trun("Event probability ", size=PT(9), italic=True, color=BLACK, font=FONT), trun("(will the Government buy this again?) is not ", size=PT(9), italic=True, color=BLACK, font=FONT), trun("addressability ", size=PT(9), italic=True, color=BLACK, font=FONT), trun("(can this company reach and win the action?).", size=PT(9), italic=True, color=BLACK, font=FONT)], mar_l=0, indent=0),
            tpara([trun("A large award is not an opportunity — it is a posture to classify. Walk the gates; the gate it fails as prime names the route in.", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0),
            tpara([]),
            tpara([trun("Upper gates are hard data — object type, obligations vs. ceiling, extent of competition — and decide quickly; the lower gates (timing, ability) are judgment.", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("The decision is route, not bid/no-bid: bid the recompete, on-ramp, subcontract/team, or join the consortium/OT.", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("A closed prime is not a closed market — multiyear and block buys release demand below the prime (AP/LLTM, EOQ, first-tier subs).", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("Single-award ≠ sole-source; an IDV is not necessarily an IDIQ; an unexercised option is not guaranteed revenue.", size=PT(9), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
        ], fill="DFE7EB", l_ins=82296, r_ins=82296, t_ins=54864, b_ins=54864, borders={"L": {"color": "808080", "width": 6350}, "R": {"color": "808080", "width": 6350}, "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(3.46)),
    ]))
    # ── cascade: precondition + five gate boxes (Zone A) each with its pass/redirect verdict (Zone B) ──
    for _y, _fill, _lc, _lw, _tc, _name, _crit, _verd in _GATES:
        out.append(text_box(n(), "Gate", _GATE_X, IN(_y), _GATE_W, _ROW_H, [paragraph([run(_name, size=PT(10), bold=True, color=_tc, font=FONT), line_break(), run(_crit, size=PT(9), color=_tc, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color=_lc, line_width=_lw, anchor="ctr", l_ins=45720, t_ins=9144, r_ins=45720, b_ins=9144))
        out.append(text_box(n(), "Verdict", _VERD_X, IN(_y), _VERD_W, _ROW_H, [paragraph([run(_verd, size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    # ── ADDRESSABLE MARKET waypoint — first focal stop (interrupts the stack after Gate 1) ──
    out.append(text_box(n(), "Addressable Market", _BAND_X, IN(2.54), _BAND_W, IN(0.46), [paragraph([run("ADDRESSABLE MARKET", size=PT(11), bold=True, color=WHITE, font=FONT), run("   —   real, in-scope, committed demand (the denominator, and the first focal stop)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="223E59", line_color="none", anchor="ctr"))
    # ── cascade arrow into the route leaves (the payoff transition) ──
    out.append(connector(n(), "Straight Arrow Connector 1", IN(2.67), IN(5.0), IN(0), IN(0.28), color="223E59", width=19050, arrow=True))
    # ── ROUTE LEAVES header + four boxes (full width) — second focal stop ──
    out.append(text_box(n(), "Route Header", IN(0.495), IN(5.28), IN(12.3), IN(0.22), [paragraph([run("Route to revenue", size=PT(11), bold=True, color="223E59", font=FONT), run("   —   what survives the gates is named by route (the second focal stop)", size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    for _x, _title, _posture, _tlead, _trest in _ROUTE_LEAVES:
        _runs = [run(_title, size=PT(10), bold=True, color=WHITE, font=FONT), line_break(), run(_posture, size=PT(8), color=WHITE, font=FONT)]
        if _tlead:
            _runs += [line_break(), run(_tlead, size=PT(8), bold=True, italic=True, color="FFC000", font=FONT), run(_trest, size=PT(8), italic=True, color=WHITE, font=FONT)]
        out.append(text_box(n(), "Leaf", IN(_x), _LEAF_Y, _LEAF_W, _LEAF_H, [paragraph(_runs, align="ctr", line_spacing=100000)], fill="223E59", line_color="none", anchor="ctr", l_ins=45720, t_ins=9144, r_ins=45720, b_ins=9144))
    # ── portal-visibility overlay (a property of the set, not a gate — set apart, dashed) ──
    out.append(text_box(n(), "Portal Overlay", IN(0.495), IN(6.6), IN(12.3), IN(0.34), [paragraph([run("Portal visibility (a property of the set, not a gate):   ", size=PT(9), bold=True, italic=True, color=GRAY_1, font=FONT), run("most addressable awards were never advertised on SAM.gov Contract Opportunities — award-data analysis runs on Contract Awards, USAspending, and FPDS.", size=PT(9), italic=True, color=GRAY_1, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="808080", line_width=12700, dashed_line=True, anchor="ctr"))
    # ── sources ──
    out.append(sources_line("Source: SAM.gov Contract Awards; USAspending; FPDS; SAM.gov Contract Opportunities | Authorities: FAR Subpart 16.5 (multiple-award / fair opportunity); FAR 17.1 (multiyear); FAR 17.2 (options); FAR 9.6 (teaming); FAR 6.302 / 52.217-8 (sole-source bridge / extension of services); DFARS 206.001-70 (OT prototype → production follow-on); DFARS 252.227-7013 / -7014 (data rights); 15 U.S.C. 638 (SBIR/STTR Phase III)"))
    return "".join(out)


def render() -> str:
    return slide(_body())
