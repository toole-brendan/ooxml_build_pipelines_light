"""contract_addressability — Strategic Contracts deck (20260624), source slide 1.

EXHIBIT — "Defining Contract Addressability": award structure, not raw demand,
determines whether market entry is direct, gated, or incumbent-led. The slide
reads left→right across three zones — 1. Observed market, 2. Contract landscape,
3. Route to revenue — joined by a branching connector trunk. Zone 1 separates
committed demand from mere capacity and pins the funding context; zone 2 screens
the contract record on three questions (Is demand real? · Who has access? · When
can a company enter?), with a dashed secondary-diligence card on ability-to-perform
and economics. An ACCESS pivot tag splits the trunk into Route A (Direct to
Government) and Route B (Through the incumbent performance chain).

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............... breadcrumb() + prelim_chip() + title_placeholder()
  • zone headers ......... "1. Observed market" homePlate + "2. Contract
                           landscape" / "3. Route to revenue" chevrons — gray,
                           darkening left→right (D9D9D9 → BFBFBF → 7F7F7F); on the
                           equal-column grid
  • _GROUP_CAPTIONS ...... italic one-liner under each zone header
  • observed-market cards  ObservedMarketCard ×3 (committed demand · capacity,
                           not revenue · funding context) — zone-1 column
  • contract screens ..... ContractScreen ×3 (is demand real? · who has access? ·
                           when can a company enter?); the pivotal "who has
                           access?" screen is the deep-blue (263746) emphasis card
  • pivot + diligence .... "ACCESS" pivot tag (3D5972 hinge) + dashed
                           secondary-diligence card
  • trunk connectors ..... 5 connectors forming the branching trunk (observed →
                           landscape, then access → direct / incumbent)
  • route cards + chips .. RouteCard ×2 (Direct to Government / incumbent chain)
                           + Route A / Route B chips — zone-3 column; the blue
                           "gatedness" gradient now rides the chips 6E91B1 (direct)
                           → 263746 (incumbent), with E2E9EF / F2F2F2 card fills

Auto-converted by _tools/convert_slide.py, then hand-annotated for study AND
hand-tuned. Two deliberate post-conversion edits (so the render is NO LONGER
byte-identical to the raw port):
  • Layout — the three zones were equalized onto a uniform column grid
    (_LM · _COLW · gutters _G1/_G2): zone 1 widened (was 2.93"), zones 2–3
    narrowed (were 4.28"/4.34") so all three share one _COLW. Every Y position
    and row height is unchanged, so nothing reflows vertically.
  • Colour — recoloured off the source's ad-hoc navy/blue/amber onto the house
    blue+gray ramps: gray zone headers darkening left→right (D9D9D9 → BFBFBF →
    7F7F7F); the pivotal "Who has access?" screen + the ACCESS hinge in deep blue
    (no black card, no orange badge); a 6E91B1→263746 "gatedness" gradient on the
    route chips. Every filled shape carries the house 1pt black border (the AUTO
    default) — including the chevrons; the dashed secondary-diligence card keeps
    its dash but is now black 1pt. The Preliminary chip is exempt (its own builder).

Converter stats: text_box=15, connector=5, chrome_builders=3, clusters=1
(covering 3 shapes), dropped=1 (think-cell OLE frame).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors: equal three-column grid (the hand-tuned layout edit) ──
_LM   = 0.495   # left margin = column-1 left edge (house left margin)
_COLW = 3.85    # equal column width — every zone shares this (was 2.93 / 4.28 / 4.34)
_G1   = 0.30    # gutter 1 (observed → landscape): a single right-arrow connector
_G2   = 0.45    # gutter 2 (landscape → route): the branching ACCESS trunk lives here
_C1_X = _LM                       # 0.495  zone-1 (observed market) column left edge
_C2_X = _LM + _COLW + _G1         # 4.645  zone-2 (contract landscape) column left edge
_C3_X = _C2_X + _COLW + _G2       # 8.945  zone-3 (route to revenue) column left edge
_C1_R = _C1_X + _COLW             # 4.345  zone-1 right edge (gutter-1 starts here)
_C2_R = _C2_X + _COLW             # 8.495  zone-2 right edge (gutter-2 starts here)
_TRUNK_X = _C2_R + _G2 / 2        # 8.720  branch trunk, mid gutter-2

_CAPTION_Y, _CAPTION_H = IN(1.955), IN(0.17)   # zone-caption row top + height [x3]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the three italic one-liner captions under the zone headers (observed market /
#   contract landscape / route to revenue).
_GROUP_CAPTIONS = [    # (x, cx, label) x3 — italic caption under each zone header
    (_C1_X, _COLW, "Demand exists before access is determined"),
    (_C2_X, _COLW, "Award record separates market size from market access"),
    (_C3_X, _COLW, "Access posture determines the practical route in"),
]

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
    # ── chrome (breadcrumb · prelim chip · title) ──
    out.append(breadcrumb("Strategic Contracts", "Market Access Framework"))
    out.append(prelim_chip())
    out.append(title_placeholder("Defining Contract Addressability", "Award structure determines whether entry is direct, gated, or incumbent-led."))
    # ── zone headers: 1 observed market · 2 contract landscape · 3 route to revenue (neutral D9D9D9) ──
    out.append(text_box(n(), "ZoneHeader", IN(_C1_X), IN(1.57), IN(_COLW), IN(0.36), [paragraph([run("1. Observed market", size=PT(10), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="D9D9D9", prst="homePlate", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # GRAY_2
    out.append(text_box(n(), "ZoneHeader", IN(_C2_X), IN(1.57), IN(_COLW), IN(0.36), [paragraph([run("2. Contract landscape", size=PT(10), bold=True, color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill="BFBFBF", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # GRAY_3
    out.append(text_box(n(), "ZoneHeader", IN(_C3_X), IN(1.57), IN(_COLW), IN(0.36), [paragraph([run("3. Route to revenue", size=PT(10), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="7F7F7F", prst="chevron", geom_adj={"adj": "val 24929"}, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # GRAY_4
    # ── zone captions (italic one-liner under each header) ──
    for _x, _cx, _t in _GROUP_CAPTIONS:
        out.append(text_box(n(), "Label", IN(_x), _CAPTION_Y, IN(_cx), _CAPTION_H, [paragraph([run(_t, size=PT(9), italic=True, color="000000", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # BLACK
    # ── zone 1 · observed-market cards (committed demand · capacity · funding) ──
    out.append(text_box(n(), "ObservedMarketCard", IN(_C1_X), IN(2.395), IN(_COLW), IN(0.66), [paragraph([run("Committed demand", size=PT(10), bold=True, color="000000", font=FONT)], line_spacing=90000), paragraph([run("Obligations on orders; quantity-adding modifications; recurring funding", size=PT(9), color="000000", font=FONT)], line_spacing=85000)], fill="FFFFFF", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # WHITE
    out.append(text_box(n(), "ObservedMarketCard", IN(_C1_X), IN(3.195), IN(_COLW), IN(0.66), [paragraph([run("Capacity, not revenue", size=PT(10), bold=True, color="000000", font=FONT)], line_spacing=90000), paragraph([run("Ceilings; potential value; unexercised options", size=PT(9), color="000000", font=FONT)], line_spacing=85000)], fill="E2E9EF", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # BLUE_1
    out.append(text_box(n(), "ObservedMarketCard", IN(_C1_X), IN(3.995), IN(_COLW), IN(0.66), [paragraph([run("Funding context", size=PT(10), bold=True, color="000000", font=FONT)], line_spacing=90000), paragraph([run("TAS / appropriation; customer; mission", size=PT(9), color="000000", font=FONT)], line_spacing=85000)], fill="FFFFFF", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # WHITE
    # ── zone 2 · contract-screen cards (real? · access? · timing?); "who has access?" = 263746 emphasis ──
    out.append(text_box(n(), "ContractScreen", IN(_C2_X), IN(2.345), IN(_COLW), IN(0.72), [paragraph([run("Is demand real?", size=PT(10), bold=True, color="000000", font=FONT)], line_spacing=88000), paragraph([run("Evidence: obligations, orders, quantity additions, recurring funding", size=PT(9), color="000000", font=FONT)], line_spacing=82000), paragraph([run("Implication: size the realized market", size=PT(9), italic=True, color="000000", font=FONT)], line_spacing=82000)], fill="FFFFFF", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # WHITE
    out.append(text_box(n(), "ContractScreen", IN(_C2_X), IN(3.185), IN(_COLW), IN(1.13), [paragraph([run("Who has access?", size=PT(10), bold=True, color="FFFFFF", font=FONT)], line_spacing=88000), paragraph([], line_spacing=82000), paragraph([run("Evidence: extent competed; single- / multiple-award structure; set-aside; holder roster", size=PT(9), color="FFFFFF", font=FONT)], line_spacing=82000), paragraph([], line_spacing=82000), paragraph([run("Implication: direct access versus incumbent-chain route", size=PT(9), italic=True, color="FFFFFF", font=FONT)], line_spacing=82000)], fill="263746", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # BLUE_5
    out.append(text_box(n(), "ContractScreen", IN(_C2_X), IN(4.435), IN(_COLW), IN(0.78), [paragraph([run("When can a company enter?", size=PT(10), bold=True, color="000000", font=FONT)], line_spacing=88000), paragraph([run("Evidence: last date to order; ultimate completion; option dates; bridges; MYP cadence", size=PT(9), color="000000", font=FONT)], line_spacing=82000), paragraph([run("Implication: pursue now, position, or monitor", size=PT(9), italic=True, color="000000", font=FONT)], line_spacing=82000)], fill="FFFFFF", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # WHITE
    # ── access pivot tag (3D5972 hinge) + secondary-diligence card ──
    out.append(text_box(n(), "Access pivot tag", IN(7.415), IN(3.29), IN(0.86), IN(0.255), [paragraph([run("ACCESS", size=PT(9), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="3D5972", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))   # BLUE_4
    out.append(text_box(n(), "Secondary diligence", IN(_C2_X), IN(5.405), IN(_COLW), IN(0.69), [paragraph([run("Secondary diligence: ability to perform + economics", size=PT(10), bold=True, color="000000", font=FONT)], line_spacing=90000), paragraph([run("Technical scope; clearance; accounting system; past performance; pricing type; IP / data rights; compliance burden; concentration", size=PT(9), color="000000", font=FONT)], line_spacing=82000)], fill="F2F2F2", dashed_line=True, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # GRAY_1
    # ── branching-trunk connectors (direct vs incumbent), routed through the gutters ──
    out.append(connector(n(), "Observed to landscape", IN(_C1_R), IN(3.505), IN(_G1), IN(0), color="000000", width=12700, arrow=True))   # BLACK
    out.append(connector(n(), "Access to branch trunk", IN(_C2_R), IN(3.725), IN(_G2 / 2), IN(0), color="000000", width=12700))   # BLACK
    out.append(connector(n(), "Branch trunk", IN(_TRUNK_X), IN(3.085), IN(0), IN(2.22), color="000000", width=12700))   # BLACK
    out.append(connector(n(), "Branch to direct", IN(_TRUNK_X), IN(3.085), IN(_G2 / 2), IN(0), color="000000", width=12700, arrow=True))   # BLACK
    out.append(connector(n(), "Branch to incumbent", IN(_TRUNK_X), IN(5.305), IN(_G2 / 2), IN(0), color="000000", width=12700, arrow=True))   # BLACK
    # ── zone 3 · route cards + route chips (blue gatedness gradient: direct=6E91B1, incumbent=263746) ──
    out.append(text_box(n(), "RouteCard", IN(_C3_X), IN(2.385), IN(_COLW), IN(1.72), [paragraph([run("Direct to Government", size=PT(12), bold=True, color="000000", font=FONT)], line_spacing=90000), paragraph([run("Bid an open recompete; become a holder on an on-ramp, new pool, or vehicle recompete; enter early through OT / SBIR / BAA / CSO before the production pathway is committed.", size=PT(10), color="000000", font=FONT)], line_spacing=84000)], fill="E2E9EF", anchor="ctr", l_ins=121920, t_ins=73152, r_ins=121920, b_ins=73152))   # BLUE_1
    out.append(text_box(n(), "RouteCard", IN(_C3_X), IN(4.425), IN(_COLW), IN(1.72), [paragraph([run("Through the incumbent performance chain", size=PT(12), bold=True, color="000000", font=FONT)], line_spacing=90000), paragraph([run("Team or subcontract to a current holder; supply a closed prime or upper-tier supplier; license / integrate a separable capability; build past performance for a later direct entry.", size=PT(10), color="000000", font=FONT)], line_spacing=84000)], fill="F2F2F2", anchor="ctr", l_ins=121920, t_ins=73152, r_ins=121920, b_ins=73152))   # GRAY_1
    out.append(text_box(n(), "RouteChipA", IN(_C3_X + 0.16), IN(2.535), IN(0.68), IN(0.25), [paragraph([run("Route A", size=PT(9), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="6E91B1", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))   # BLUE_3
    out.append(text_box(n(), "RouteChipB", IN(_C3_X + 0.16), IN(4.575), IN(0.68), IN(0.25), [paragraph([run("Route B", size=PT(9), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="263746", anchor="ctr", l_ins=0, t_ins=45720, r_ins=0, b_ins=45720))   # BLUE_5
    return "".join(out)


def render() -> str:
    return slide(_body())
