"""recompete_onramp — Recompete Radar deck, "Recompete On-Ramp" (companion to the
DDG-51 MYP cadence slide).

EXHIBIT — "Recompete On-Ramp": an expiring multiple-award IDIQ pool is a dated,
winnable recompete — its ordering-period end is recorded on each award years
ahead, and the route in is an open on-ramp (bid the next pool, or sub to a holder),
not a closed re-up. Worked example: the U.S. Army's watercraft non-nuclear
ship-repair pool (TACOM, W56HZV21DL).

The HERO (left ~58%) is one grouped table: 14 holder vehicles in 3 regional tiers
(CONUS / Japan-Korea / forward), each a multiple-award sub-pool with its own SHARED
ceiling, holder PIID, delivery-order count, and realized $ — footed to 10 distinct
vendors · 74 orders · $416.8M. The right rail (~38%) carries three stacked cards:
  • answer card (dark) — "THE WINDOW IS OPEN NOW": ordering period closed 2026-01-25,
    no successor pool visible -> the recompete is the live opportunity.
  • "STRUCTURE & AUTHORITY" — the native SAM Contract Awards fields (multiple-award
    IDC, full & open, FAR 16.505 fair opportunity, last date to order, office, work).
  • "MIND THE SHARED CEILING" — the IDV holds $0; money lives on the delivery orders;
    tier ceilings are shared across holders, never summed.
A house Sources/Note line closes it out.

CODE MAP (built top-down; sections mark roles):
  • chrome ........ breadcrumb() + title_placeholder() + prelim_chip() (house builders)
  • hero table .... sub-head text_box + table()/trow()/tcell() driven by _TIERS;
                    BLUE_5 column header, BLUE_2 tier bands, BLUE_1 total row
  • right rail .... answer card (text_box, BLUE_5) + two cap-bar/body card pairs
                    (_CARD cap bars over light bodies) for structure + shared-ceiling
  • sources ....... house sources_line() (Source + Note, lifted above content)

Hand-authored against deck_core (primitives + style tokens); Arial + the BLUE_*/
GRAY_* ramp throughout, geometry inside the BODY box.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
)
from deck_core.style import (
    IN, PT, FONT, BLACK, WHITE, DK,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5, GRAY_1, GRAY_2, GRAY_4, BODY_R,
)

LAYOUT = "slideLayout4"
CHARTS: list = []


# ── layout anchors ─────────────────────────────────────────────────────────
_BODY_X   = IN(0.495)              # flush with chrome left edge
_BODY_TOP = IN(1.46)              # just above the BODY box top; clears the title

# Left hero table column.
_TBL_X = _BODY_X
_TBL_W = IN(7.20)
# 4 grid columns: Holder | Award vehicle (PIID) | Orders | Realized $.
_COL_HOLDER, _COL_PIID, _COL_ORD, _COL_REAL = IN(2.85), IN(2.10), IN(0.95), IN(1.30)
_COL_WIDTHS = [_COL_HOLDER, _COL_PIID, _COL_ORD, _COL_REAL]

# Right rail column.
_RAIL_X = IN(7.97)
_RAIL_W = BODY_R - _RAIL_X        # -> right edge flush with chrome (≈4.84in)

# Shared rule colors / weights.
_RULE_HEAVY = {"color": DK, "width": 12700}     # 1pt  header underline / total top
_RULE_LIGHT = {"color": GRAY_2, "width": 6350}  # 0.5pt inter-row hairline


# ── hero-table data — 14 holder vehicles in 3 regional tiers ────────────────
# Each tier band line shows the SHARED ceiling next to that tier's realized total,
# so "$186M ceiling vs $11.9M realized" reads at a glance (capacity, not spend).
# (holder, PIID, orders, realized)
_TIERS = [
    ("CONUS  ·  ceiling $529M shared  ·  6 holders  ·  40 orders  ·  $281.7M realized", [
        ("Bay Ship & Yacht",          "W56HZV21DL002", "5",  "$145.4M"),
        ("Metal Trades",              "W56HZV21DL010", "18", "$58.9M"),
        ("Colonna's Ship Yard",       "W56HZV21DL003", "6",  "$52.9M"),
        ("Lyon Shipyard",             "W56HZV21DL008", "3",  "$11.9M"),
        ("Murtech",                   "W56HZV21DL011", "6",  "$10.5M"),
        ("Yank Marine",               "W56HZV21DL015", "2",  "$2.1M"),
    ]),
    ("Japan / Korea  ·  ceiling $216M shared  ·  3 holders  ·  18 orders  ·  $123.2M realized", [
        ("Yokohama Engineering",      "W56HZV21DL024", "15", "$114.5M"),
        ("Sunjin Entech",             "W56HZV21DL023", "1",  "$7.0M"),
        ("Sumitomo Heavy Industries", "W56HZV21DL022", "2",  "$1.7M"),
    ]),
    ("Forward  ·  ceiling $186M shared  ·  5 holders  ·  16 orders  ·  $11.9M realized", [
        ("HII Fleet Support Group",   "W56HZV21DL031", "6",  "$2.7M"),
        ("Metal Trades",              "W56HZV21DL034", "7",  "$2.6M"),
        ("Yokohama Engineering",      "W56HZV21DL038", "1",  "$6.0M"),
        ("Sumitomo Heavy Industries", "W56HZV21DL036", "1",  "$0.4M"),
        ("Lyon Shipyard",             "W56HZV21DL033", "1",  "$0.2M"),
    ]),
]

# Right-rail structure card — native SAM Contract Awards fields, one per line.
_STRUCT_ROWS = [
    ("Vehicle", "Multiple-award IDC (IDIQ) — holds $0 itself"),
    ("Competition", "Full & open"),
    ("Orders", "FAR 16.505 fair opportunity — on every order"),
    ("Ordering period", "Ends (last date to order) 2026-01-25 · opened 2021-01-27"),
    ("Office", "Army TACOM (W56HZV)"),
    ("Work", "Non-nuclear ship repair · NAICS 336611 · PSC J998 / J999 / J019"),
]


# ── small builders ──────────────────────────────────────────────────────────
def _cap_bar(n, x, y, w, text, *, fill=BLUE_4):
    """A dark cap strip over a rail card: Arial 11pt bold, ALL CAPS, white."""
    return text_box(n, "CardCap", x, y, w, IN(0.26),
                    [paragraph([run(text, size=PT(11), bold=True, color=WHITE, font=FONT)],
                               align="l", line_spacing=100000)],
                    fill=fill, line_color=fill, anchor="ctr",
                    l_ins=91440, t_ins=20000, r_ins=45720, b_ins=20000)


def _hero_table(n):
    rows = []
    # Column header (BLUE_5, white bold) with a 1pt underline.
    rows.append(trow([
        tcell("Holder", fill=BLUE_5, size=PT(9), bold=True, color=WHITE, align="l",
              anchor="ctr", t_ins=24000, b_ins=24000, borders={"B": _RULE_HEAVY}),
        tcell("Award vehicle (PIID)", fill=BLUE_5, size=PT(9), bold=True, color=WHITE,
              align="l", anchor="ctr", t_ins=24000, b_ins=24000, borders={"B": _RULE_HEAVY}),
        tcell("Orders", fill=BLUE_5, size=PT(9), bold=True, color=WHITE, align="ctr",
              anchor="ctr", t_ins=24000, b_ins=24000, borders={"B": _RULE_HEAVY}),
        tcell("Realized $", fill=BLUE_5, size=PT(9), bold=True, color=WHITE, align="r",
              anchor="ctr", t_ins=24000, b_ins=24000, borders={"B": _RULE_HEAVY}),
    ], h=IN(0.27)))

    for band_label, holder_rows in _TIERS:
        # Tier band — spans all 4 columns (BLUE_2), shared-ceiling vs realized line.
        rows.append(trow([
            tcell(band_label, fill=BLUE_2, size=PT(9), bold=True, color=BLACK, align="l",
                  grid_span=4, anchor="ctr", l_ins=82000, t_ins=18000, b_ins=18000,
                  borders={"B": {"color": WHITE, "width": 6350}}),
        ], h=IN(0.225)))
        for holder, piid, orders, realized in holder_rows:
            rows.append(trow([
                tcell(holder, size=PT(9), color=BLACK, align="l", anchor="ctr",
                      t_ins=18000, b_ins=18000, borders={"B": _RULE_LIGHT}),
                tcell(piid, size=PT(8), color=GRAY_4, align="l", anchor="ctr",
                      t_ins=18000, b_ins=18000, borders={"B": _RULE_LIGHT}),
                tcell(orders, size=PT(9), color=BLACK, align="ctr", anchor="ctr",
                      t_ins=18000, b_ins=18000, borders={"B": _RULE_LIGHT}),
                tcell(realized, size=PT(9), color=BLACK, align="r", anchor="ctr",
                      t_ins=18000, b_ins=18000, borders={"B": _RULE_LIGHT}),
            ], h=IN(0.205)))

    # Pool total — 10 distinct vendors · 74 · $416.8M (BLUE_1, bold, 1pt top rule).
    rows.append(trow([
        tcell("Pool total — 10 distinct vendors", fill=BLUE_1, size=PT(9), bold=True,
              color=BLACK, align="l", grid_span=2, anchor="ctr",
              t_ins=22000, b_ins=22000, borders={"T": _RULE_HEAVY}),
        tcell("74", fill=BLUE_1, size=PT(9), bold=True, color=BLACK, align="ctr",
              anchor="ctr", t_ins=22000, b_ins=22000, borders={"T": _RULE_HEAVY}),
        tcell("$416.8M", fill=BLUE_1, size=PT(9), bold=True, color=BLACK, align="r",
              anchor="ctr", t_ins=22000, b_ins=22000, borders={"T": _RULE_HEAVY}),
    ], h=IN(0.27)))

    return table(n, "PoolTable", _TBL_X, IN(1.78), _TBL_W, IN(4.1),
                 col_widths=_COL_WIDTHS, rows=rows, first_row=False, first_col=False)


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Recompete Radar", "Multiple-Award On-Ramp"))
    out.append(title_placeholder(
        "Recompete On-Ramp",
        "An expiring multiple-award pool is a dated, winnable recompete — bid the next "
        "pool or sub to a holder, not a closed re-up"))
    out.append(prelim_chip())

    # ── hero table (left) — sub-head + the grouped pool ──
    out.append(text_box(n(), "TableSubhead", _TBL_X, _BODY_TOP, _TBL_W, IN(0.28),
                        [paragraph([
                            run("The pool — 14 holder vehicles in 3 regional tiers    ",
                                size=PT(11), bold=True, color=DK, font=FONT),
                            run("Army TACOM  ·  IDIQ W56HZV21DL  ·  full & open",
                                size=PT(9), italic=True, color=GRAY_4, font=FONT),
                        ], align="l", line_spacing=100000)],
                        fill=None, line_color="none", anchor="b",
                        l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(_hero_table(n()))

    # ── right rail ──
    # Answer card (dark) — the live-window punchline.
    out.append(text_box(n(), "AnswerCard", _RAIL_X, _BODY_TOP, _RAIL_W, IN(1.22),
        [
            paragraph([run("THE WINDOW IS OPEN NOW", size=PT(12.5), bold=True,
                           color=WHITE, font=FONT)], align="l",
                      line_spacing=100000, space_after=400),
            paragraph([
                run("Ordering period closed ", size=PT(10), color=WHITE, font=FONT),
                run("2026-01-25", size=PT(10), bold=True, color=WHITE, font=FONT),
                run(" and ", size=PT(10), color=WHITE, font=FONT),
                run("no successor pool is visible", size=PT(10), bold=True, color=WHITE, font=FONT),
                run(" (Army extract through 2026-06-20) — the recompete is the live "
                    "opportunity.", size=PT(10), color=WHITE, font=FONT),
            ], align="l", line_spacing=104000, space_after=300),
            paragraph([
                run("Route in:", size=PT(10), bold=True, color=WHITE, font=FONT),
                run(" bid the next pool, or subcontract to a current holder.",
                    size=PT(10), color=WHITE, font=FONT),
            ], align="l", line_spacing=104000),
        ],
        fill=BLUE_5, line_color=BLUE_5, anchor="t",
        l_ins=120000, t_ins=70000, r_ins=120000, b_ins=70000))

    # Card 2 — structure & authority (cap bar + body table of native fields).
    _c2_cap_y = IN(2.86)
    out.append(_cap_bar(n(), _RAIL_X, _c2_cap_y, _RAIL_W,
                        "STRUCTURE & AUTHORITY  (SAM CONTRACT AWARDS)"))
    _c2_body_y = _c2_cap_y + IN(0.26)
    _attr_w = IN(1.28)
    struct_rows = []
    for k, v in _STRUCT_ROWS:
        struct_rows.append(trow([
            tcell(k, size=PT(8.5), bold=True, color=DK, align="l", anchor="t",
                  t_ins=14000, b_ins=14000, l_ins=10000),
            tcell_rich([tpara([trun(v, size=PT(8.5), color=BLACK, font=FONT)],
                              align="l", line_spacing=102000)],
                       anchor="t", t_ins=14000, b_ins=14000, l_ins=20000),
        ], h=IN(0.2)))
    out.append(table(n(), "StructTable", _RAIL_X, _c2_body_y, _RAIL_W, IN(1.26),
                     col_widths=[_attr_w, _RAIL_W - _attr_w], rows=struct_rows,
                     first_row=False, first_col=False))

    # Card 3 — read the order layer / mind the shared ceiling.
    _c3_cap_y = IN(4.58)
    out.append(_cap_bar(n(), _RAIL_X, _c3_cap_y, _RAIL_W,
                        "MIND THE SHARED CEILING", fill=BLUE_4))
    _c3_body_y = _c3_cap_y + IN(0.26)
    out.append(text_box(n(), "CeilingBody", _RAIL_X, _c3_body_y, _RAIL_W, IN(1.02),
        [
            paragraph([
                run("Read the order layer.", size=PT(9), bold=True, color=DK, font=FONT),
                run(" The IDV holds ", size=PT(9), color=BLACK, font=FONT),
                run("$0", size=PT(9), bold=True, color=BLACK, font=FONT),
                run(" — money and appropriations live on the delivery orders "
                    "($416.8M realized across 74 orders; O&M, Army and Other "
                    "Procurement, Army).", size=PT(9), color=BLACK, font=FONT),
            ], align="l", line_spacing=104000, space_after=400),
            paragraph([
                run("Ceilings are shared.", size=PT(9), bold=True, color=DK, font=FONT),
                run(" $529M / $216M / $186M are per-tier ", size=PT(9), color=BLACK, font=FONT),
                run("pool capacity, shared across holders", size=PT(9), bold=True,
                    color=BLACK, font=FONT),
                run(" — never summed.", size=PT(9), color=BLACK, font=FONT),
            ], align="l", line_spacing=104000),
        ],
        fill=GRAY_1, line_color=GRAY_2, line_width=6350, anchor="t",
        l_ins=110000, t_ins=60000, r_ins=110000, b_ins=60000))

    # ── house sources / note ──
    out.append(sources_line(
        "Sources: SAM.gov Contract Awards — by PIID (vehicle type, last date to order, "
        "shared ceiling, solicitation, office, competition) and by awardee UEI (successor "
        "check); USAspending /awards (IDV confirmation). Delivery-order dollars, FY profile, "
        "and TAS from the Army contracts extract (USAspending-lineage). Route per FAR Subpart "
        "16.5 / 16.505.  |  Note: tier ceilings are shared across holders and are never summed "
        "— realized obligation ($416.8M) is the only summable measure. The successor recompete "
        "is inferred (none seen as of this pull); a DoD award signed in the last ~90 days may be "
        "hidden on a non-federal SAM key — confirm before acting. As of 2026-06-24.",
        y=IN(6.42)))
    return "".join(out)


def render() -> str:
    return slide(_body())
