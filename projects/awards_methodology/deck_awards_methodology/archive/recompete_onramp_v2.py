"""recompete_onramp — Recompete Radar deck, "Recompete On-Ramp" (slide 03).

EXHIBIT — "Recompete On-Ramp": companion to the recompete-cadence slide. Where that
slide shows the *supply-the-prime* route (a closed prime whose supply chain is open),
this one shows the *become-a-holder* route — bidding onto an expiring multiple-award
IDIQ pool. The point: an expiring pool is a dated, winnable recompete (its last date
to order is recorded on every award years ahead) and the way in is an open on-ramp,
not a closed re-up. Worked example: the U.S. Army's TACOM watercraft ship-repair pool.

The slide is a left "Key takeaways" rail (four condensed points) paired with the
centrepiece exhibit — the pool roster: 14 holder vehicles seated by one full-and-open
competition into three regional tiers (CONUS · Japan/Korea · Forward), each tier a
multiple-award group with its own *shared* ceiling, under a common last date to order
of 2026-01-25. Realized $ = sum of each holder's delivery orders; the pool-total row
closes the table (10 distinct vendors · 74 orders · $416.8M). An authority caption
strip sits above the table and an order-layer note (shared ceilings never summed; the
IDVs hold $0) below it; a caveats/provenance Source line closes the page.

CODE MAP (body follows paint order; section headers mark roles in place):
  • chrome ......... breadcrumb() + title_placeholder()
  • takeaways rail . "KEY TAKEAWAYS" header + accent rule + 4 numbered text_box()es
                     (driven by _TAKEAWAYS / _TAKEAWAY_Y, looped)
  • caption strip .. vehicle/authority one-liner (two lines via line_break())
  • pool table ..... one table() — header row + 3 tier-band rows + 14 holder rows +
                     pool-total row, built from _POOL_TIERS via the _band_row /
                     _data_row helpers (low-level trow()/tcell()/tcell_rich())
  • order-layer note . shared-ceiling / IDV-$0 / appropriation caption under the table
  • sources_line ... caveats (date-certain vs. inferred; 90-day rule) + provenance

Hand-authored from the slide-03 spec on deck_core primitives (no converter pass);
no chart or image dependencies, so CHARTS is empty and there is no _src payload.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, sources_line,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_1, BLUE_5, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── shared cell metrics (kept uniform so the dense roster reads cleanly) ──
_PAD_X = 54864     # l/r cell inset  (~0.057in)            [shared across the table]
_HDR_TB = 36576    # header top/bottom inset (~0.040in)
_BAND_TB = 18288   # tier-band top/bottom inset (~0.020in)
_ROW_TB = 13716    # data-row top/bottom inset (~0.015in)  — compact, 14 rows deep
_TOT_TB = 27432    # pool-total top/bottom inset (~0.030in)
_HAIRLINE = {"L": "none", "R": "none", "T": "none", "B": {"color": "808080", "width": 6350}}
_NOBORDER = {"L": "none", "R": "none", "T": "none", "B": "none"}
_TOPRULE = {"L": "none", "R": "none", "T": {"color": DK, "width": 12700}, "B": "none"}

# ── takeaways rail (each tuple → one positioned text_box; lead is bold, body regular) ──
_TAKEAWAYS = [    # (lead, body) x4 — condensed from the spec's five key takeaways
    ("A dated recompete you can see coming.",
     "The Army watercraft ship-repair IDIQ (W56HZV21DL, TACOM) seated 14 holder vehicles "
     "under a single last date to order — 2026-01-25 — recorded on each award years ahead."),
    ("An on-ramp, not a duopoly.",
     "Competed full-and-open; task orders run on FAR 16.505 fair opportunity across 10 "
     "distinct vendors. At recompete you bid onto the next pool or subcontract to a holder "
     "— unlike the DDG line, which re-ups to the same two yards."),
    ("A real, recurring channel.",
     "74 delivery orders and $416.8M obligated through the pool to date; ship repair "
     "re-competes on a cycle, so a follow-on pool is expected."),
    ("The window is open now.",
     "The ordering period closed 2026-01-25 and no successor pool is visible in the data "
     "— the recompete is the live opportunity."),
]
_TAKEAWAY_Y = [2.06, 3.22, 4.50, 5.46]   # top of each takeaway box (rail, top-anchored)

# ── pool roster — 14 holder vehicles in 3 regional tiers (each tier its own SHARED ceiling) ──
_POOL_TIERS = [    # (tier label w/ shared ceiling, solicitation, [(holder, piid, orders, realized, psc)])
    ("CONUS — $529M shared ceiling (6 holders)", "W56HZV20RL807", [
        ("Bay Ship & Yacht",          "W56HZV21DL002",  5, "$145.4M", "J999"),
        ("Metal Trades",              "W56HZV21DL010", 18,  "$58.9M", "J998"),
        ("Colonna’s Ship Yard",  "W56HZV21DL003",  6,  "$52.9M", "J998"),
        ("Lyon Shipyard",             "W56HZV21DL008",  3,  "$11.9M", "J998"),
        ("Murtech",                   "W56HZV21DL011",  6,  "$10.5M", "J998"),
        ("Yank Marine",               "W56HZV21DL015",  2,   "$2.1M", "J019"),
    ]),
    ("Japan / Korea — $216M shared ceiling (3 holders)", "W56HZV20RL806", [
        ("Yokohama Engineering",      "W56HZV21DL024", 15, "$114.5M", "J999"),
        ("Sunjin Entech",             "W56HZV21DL023",  1,   "$7.0M", "J998"),
        ("Sumitomo Heavy Industries", "W56HZV21DL022",  2,   "$1.7M", "J019"),
    ]),
    ("Forward — $186M shared ceiling (5 holders)", "W56HZV20RL805", [
        ("HII Fleet Support Group",   "W56HZV21DL031",  6,   "$2.7M", "J999"),
        ("Metal Trades",              "W56HZV21DL034",  7,   "$2.6M", "J019"),
        ("Yokohama Engineering",      "W56HZV21DL038",  1,   "$6.0M", "J019"),
        ("Sumitomo Heavy Industries", "W56HZV21DL036",  1,   "$0.4M", "J019"),
        ("Lyon Shipyard",             "W56HZV21DL033",  1,   "$0.2M", "J999"),
    ]),
]


def _hdr_cell(text: str, align: str = "l"):
    """Dark-fill (BLUE_5) header cell, white bold."""
    return tcell(text, size=PT(11), bold=True, color=WHITE, align=align, fill=BLUE_5, anchor="ctr",
                 l_ins=_PAD_X, r_ins=_PAD_X, t_ins=_HDR_TB, b_ins=_HDR_TB, borders=_NOBORDER)


def _band_row(label: str, sol: str):
    """Full-width tier band (BLUE_1) — bold label + lighter solicitation tag."""
    return trow([tcell_rich([tpara([
        trun(label, size=PT(11), bold=True, color=DK, font=FONT),
        trun("      solicitation " + sol, size=PT(9), italic=True, color="595959", font=FONT),
    ], mar_l=0, indent=0)], grid_span=5, fill=BLUE_1, anchor="ctr",
        l_ins=_PAD_X, r_ins=_PAD_X, t_ins=_BAND_TB, b_ins=_BAND_TB, borders=_NOBORDER)], h=IN(0))


def _data_cell(text: str, align: str = "l"):
    return tcell(text, size=PT(11), color=BLACK, align=align, anchor="ctr",
                 l_ins=_PAD_X, r_ins=_PAD_X, t_ins=_ROW_TB, b_ins=_ROW_TB, borders=_HAIRLINE)


def _data_row(holder: str, piid: str, orders: int, realized: str, psc: str):
    return trow([
        _data_cell(holder),
        _data_cell(piid),
        _data_cell(str(orders), align="ctr"),
        _data_cell(realized, align="r"),
        _data_cell(psc, align="ctr"),
    ], h=IN(0))


def _total_cell(text: str, align: str = "l", grid_span: int = 1):
    return tcell(text, size=PT(11), bold=True, color=BLACK, align=align, grid_span=grid_span,
                 fill=GRAY_1, anchor="ctr", l_ins=_PAD_X, r_ins=_PAD_X, t_ins=_TOT_TB, b_ins=_TOT_TB,
                 borders=_TOPRULE)


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome ──
    out.append(breadcrumb("Recompete Radar", "On-Ramp"))
    out.append(title_placeholder(
        "Recompete On-Ramp",
        "An expiring multiple-award IDIQ pool is a dated, winnable recompete — the way in is an "
        "open on-ramp (bid onto the next pool), not a closed re-up. Worked example: the U.S. Army’s "
        "TACOM watercraft ship-repair pool."))
    # ── takeaways rail — header, accent rule, then 4 numbered points ──
    out.append(text_box(n(), "Takeaways Header", IN(0.495), IN(1.60), IN(3.20), IN(0.30), [paragraph([run("KEY TAKEAWAYS", size=PT(11), bold=True, color=DK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b"))
    out.append(text_box(n(), "Accent Rule", IN(0.495), IN(1.94), IN(3.00), IN(0.022), [paragraph([], line_spacing=100000)], fill=DK, line_color="none"))
    for _i, ((_lead, _body_t), _y) in enumerate(zip(_TAKEAWAYS, _TAKEAWAY_Y), start=1):
        out.append(text_box(n(), "Takeaway", IN(0.495), IN(_y), IN(3.45), IN(1.10), [paragraph([
            run(f"{_i}   ", size=PT(11), bold=True, color=DK, font=FONT),
            run(_lead + "  ", size=PT(11), bold=True, color=BLACK, font=FONT),
            run(_body_t, size=PT(11), color=BLACK, font=FONT),
        ], mar_l=137160, indent=-137160, line_spacing=103000)], fill=None, line_color="none"))
    # ── authority caption strip (above the table) ──
    out.append(text_box(n(), "Authority Strip", IN(4.15), IN(1.56), IN(8.70), IN(0.46), [paragraph([
        run("Vehicle  ", size=PT(10), bold=True, color=DK, font=FONT),
        run("Multiple-award IDC · full & open competition · FAR 16.505 fair opportunity on every order", size=PT(10), color=BLACK, font=FONT),
        line_break(),
        run("Ordering period 2021-01-27 → 2026-01-25 (last date to order) · Army TACOM (W56HZV) · non-nuclear ship repair · NAICS 336611", size=PT(10), color=BLACK, font=FONT),
    ], mar_l=0, indent=0, line_spacing=104000)], fill=None, line_color="none", anchor="t"))
    # ── pool table — header + 3 tier bands + 14 holder rows + pool total ──
    _rows = [trow([
        _hdr_cell("Holder"), _hdr_cell("Vehicle (PIID)"), _hdr_cell("Orders", "ctr"),
        _hdr_cell("Realized $", "r"), _hdr_cell("PSC", "ctr"),
    ], h=IN(0))]
    for _label, _sol, _holders in _POOL_TIERS:
        _rows.append(_band_row(_label, _sol))
        for _h, _piid, _o, _rz, _psc in _holders:
            _rows.append(_data_row(_h, _piid, _o, _rz, _psc))
    _rows.append(trow([
        _total_cell("Pool total — 10 distinct vendors", align="l", grid_span=2),
        _total_cell("74", align="ctr"),
        _total_cell("$416.8M", align="r"),
        _total_cell("", align="ctr"),
    ], h=IN(0)))
    out.append(table(n(), "Pool Roster", IN(4.15), IN(2.08), IN(8.70), IN(3.62),
                     col_widths=[IN(3.20), IN(2.00), IN(0.90), IN(1.60), IN(1.00)], rows=_rows))
    # ── order-layer note (below the table) — shared ceilings never summed; IDV holds $0 ──
    out.append(text_box(n(), "Order-Layer Note", IN(4.15), IN(5.80), IN(8.70), IN(0.78), [paragraph([
        run("Read the order layer. ", size=PT(9), bold=True, italic=True, color=DK, font=FONT),
        run("Realized $ = sum of each holder’s delivery orders. Tier ceilings ($529M / $216M / $186M) are "
            "shared pool capacity — never summed across holders. The multiple-award IDVs themselves report "
            "$0 obligated; the money and appropriations (O&M, Army 021-2020; Other Procurement, Army 021-2035) "
            "sit on the child delivery orders.", size=PT(9), color=BLACK, font=FONT),
    ], mar_l=0, indent=0, line_spacing=104000)], fill=None, line_color="none", anchor="t"))
    # ── caveats + provenance footnote ──
    out.append(sources_line(
        "Note: Last date to order (2026-01-25) is date-certain and recorded on each award; the successor pool is "
        "inferred — none seen as of this pull. A DoD award signed in the last ~90 days can be hidden on a "
        "non-federal SAM key — confirm before treating the window as open. Tier ceilings are shared across "
        "holders and never summed; realized obligation ($416.8M across 74 orders) is the only summable measure.   |   "
        "Source: SAM.gov Contract Awards (by PIID and by awardee UEI); USAspending /awards; Army contracts extract "
        "(USAspending-lineage); route per FAR Subpart 16.5 / 16.505. As of 2026-06-24."))
    return "".join(out)


def render() -> str:
    return slide(_body())
