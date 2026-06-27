"""recompete_onramp — Recompete Radar, slide 03.

EXHIBIT — "Recompete On-Ramp": the Army TACOM watercraft non-nuclear
ship-repair multiple-award IDIQ is a dated, observable recompete. Four lifecycle
cards show the 2021 award, realized ordering activity, the common 2026-01-25 last
date to order, and the absence of a visible successor as of 2026-06-24. A
three-gate strip converts those facts into the "open turnover" conclusion.

The right rail summarizes the 14 holder vehicles across three regional pools,
showing realized delivery-order obligations separately from shared tier ceilings.
The bottom action strip gives the two entry routes: bid onto the successor pool
or subcontract to a current holder. A caveat preserves the distinction between a
date-certain ordering-period end and an inferred successor status.

CODE MAP:
  • chrome ............. breadcrumb() + title_placeholder() + prelim_chip()
  • _TIMELINE .......... four lifecycle cards connected left-to-right
  • _GATES ............. closed period / open structure / no successor → turnover
  • companion callout .. bridge to slide 02's closed-prime supply-chain route
  • pool table ......... three regional tiers + total, realized vs. shared ceiling
  • _AUTHORITY_CHIPS ... Full & Open / Multiple Award / FAR 16.505
  • takeaway banner .... the live on-ramp conclusion
  • _ENTRY_ROUTES ...... bid / subcontract / read the order layer
  • footnote ........... successor caveat, source, and as-of date

Designed as a native-shape module: no external images or chart templates.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    connector,
    line_break,
    table,
    trow,
    tcell,
    tcell_rich,
    tpara,
    trun,
    tbreak,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.style import (
    IN,
    PT,
    BLACK,
    WHITE,
    DK,
    GRAY_1,
    GRAY_2,
    FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors ───────────────────────────────────────────────────────────
_TIMELINE_Y = IN(1.76)
_TIMELINE_H = IN(1.18)
_GATE_Y = IN(3.29)
_GATE_H = IN(0.79)
_RIGHT_X = IN(7.80)
_RIGHT_W = IN(5.03)
_ROUTE_Y = IN(5.72)
_ROUTE_H = IN(0.72)


# ── repeated-shape data tables ───────────────────────────────────────────────
# (x, width, fill, text colour, date, headline, detail)
_TIMELINE = [
    (0.55, 1.35, "CEDDEC", BLACK, "JAN. 2021", "POOL AWARDED", "14 vehicles\n10 vendors"),
    (2.21, 1.45, "99B9D8", BLACK, "2021–2026", "ORDERING ACTIVITY", "74 orders\n$416.8M realized"),
    (3.97, 1.55, "447BB2", WHITE, "JAN. 25, 2026", "LAST DATE TO ORDER", "Ordering period closes"),
    (5.83, 1.72, "007770", WHITE, "AS OF JUN. 24, 2026", "NO SUCCESSOR VISIBLE", "OPEN TURNOVER"),
]

# (x, width, fill, text colour, headline, detail)
_GATES = [
    (0.55, 1.65, GRAY_2, BLACK, "PERIOD CLOSED", "Last date to order\nJan. 25, 2026"),
    (2.53, 1.65, GRAY_2, BLACK, "ROUTE IS OPEN", "Full & open\nMultiple award"),
    (4.51, 1.65, GRAY_2, BLACK, "NO SUCCESSOR VISIBLE", "Current award data\nthrough Jun. 24"),
    (6.49, 1.06, "007770", WHITE, "OPEN", "TURNOVER"),
]

# (x, width, fill, text colour, headline, detail)
_AUTHORITY_CHIPS = [
    (7.80, 1.58, "223E59", WHITE, "FULL & OPEN", "competition"),
    (9.49, 1.58, "447BB2", WHITE, "MULTIPLE AWARD", "holder pool"),
    (11.18, 1.65, "99B9D8", BLACK, "FAR 16.505", "fair opportunity"),
]

# (x, width, fill, text colour, kicker, body)
_ENTRY_ROUTES = [
    (0.50, 3.55, "447BB2", WHITE, "PRIMARY ROUTE", "Bid onto the successor multiple-award pool"),
    (4.18, 3.55, "99B9D8", BLACK, "ALTERNATE ROUTE", "Subcontract to a current holder"),
    (7.86, 4.97, GRAY_2, BLACK, "READ THE ORDER LAYER", "IDV = $0; obligations and TAS sit on 74 delivery orders"),
]


def _rich_card(
    n: int,
    name: str,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    color: str,
    kicker: str,
    headline: str,
    detail: str,
    *,
    line_color: str = BLACK,
    kicker_size: int = 9,
    headline_size: int = 10,
    detail_size: int = 9,
) -> str:
    """Build a three-level card using one centred paragraph."""
    runs = []
    if kicker:
        runs.extend([
            run(kicker, size=PT(kicker_size), bold=True, color=color, font=FONT),
            line_break(),
        ])
    runs.extend([
        run(headline, size=PT(headline_size), bold=True, color=color, font=FONT),
        line_break(),
    ])
    detail_lines = detail.split("\n")
    for idx, line in enumerate(detail_lines):
        runs.append(run(line, size=PT(detail_size), color=color, font=FONT))
        if idx < len(detail_lines) - 1:
            runs.append(line_break())
    return text_box(
        n,
        name,
        IN(x),
        IN(y),
        IN(w),
        IN(h),
        [paragraph(runs, align="ctr", line_spacing=100000)],
        fill=fill,
        line_color=line_color,
        line_width=3175,
        anchor="ctr",
        l_ins=55000,
        r_ins=55000,
        t_ins=40000,
        b_ins=40000,
    )


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Recompete Radar", "Army Ship Repair"))
    out.append(
        title_placeholder(
            "Recompete On-Ramp",
            "Army TACOM's ship-repair pool expired Jan. 25, 2026; no successor is visible, creating an open path to the next multiple-award pool.",
        )
    )
    out.append(prelim_chip())

    # ── section headers ──
    out.append(
        text_box(
            n(),
            "TimelineHeader",
            IN(0.55),
            IN(1.42),
            IN(7.00),
            IN(0.23),
            [paragraph([run("A dated opportunity visible years ahead", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="b",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        )
    )
    out.append(
        text_box(
            n(),
            "PoolHeader",
            _RIGHT_X,
            IN(1.42),
            _RIGHT_W,
            IN(0.23),
            [paragraph([run("Pool structure | 14 vehicles / 10 distinct vendors", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="b",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        )
    )

    # ── timeline connectors, painted before the cards ──
    for x, width in [(1.93, 0.25), (3.69, 0.25), (5.55, 0.25)]:
        out.append(
            connector(
                n(),
                "TimelineArrow",
                IN(x),
                IN(2.35),
                IN(width),
                IN(0),
                color=DK,
                width=12700,
                arrow=True,
            )
        )

    # ── lifecycle cards ──
    for x, width, fill, color, date, headline, detail in _TIMELINE:
        out.append(
            _rich_card(
                n(),
                "LifecycleCard",
                x,
                1.76,
                width,
                1.18,
                fill,
                color,
                date,
                headline,
                detail,
                kicker_size=9,
                headline_size=10,
                detail_size=9,
            )
        )

    # ── turnover-gate connectors ──
    for x, width in [(2.23, 0.27), (4.21, 0.27), (6.19, 0.27)]:
        out.append(
            connector(
                n(),
                "GateArrow",
                IN(x),
                IN(3.685),
                IN(width),
                IN(0),
                color=DK,
                width=12700,
                arrow=True,
            )
        )

    # ── turnover gates ──
    for x, width, fill, color, headline, detail in _GATES:
        out.append(
            _rich_card(
                n(),
                "TurnoverGate",
                x,
                3.29,
                width,
                0.79,
                fill,
                color,
                "",
                headline,
                detail,
                line_color=DK,
                kicker_size=1,
                headline_size=9,
                detail_size=8,
            )
        )

    # ── companion-to-slide-02 bridge ──
    out.append(
        text_box(
            n(),
            "CompanionLogic",
            IN(0.55),
            IN(4.28),
            IN(7.00),
            IN(0.71),
            [
                paragraph(
                    [
                        run("Companion to slide 02: ", size=PT(9), bold=True, color=BLACK, font=FONT),
                        run("DDG-51 = supply the closed prime; ", size=PT(9), color=BLACK, font=FONT),
                        run("TACOM = bid into an open holder pool.", size=PT(9), bold=True, color=BLACK, font=FONT),
                        line_break(),
                        run("At recompete, bid the pool—or subcontract to an incumbent.", size=PT(9), italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill="DFE7EB",
            line_color=DK,
            line_width=3175,
            anchor="ctr",
        )
    )

    # ── regional-pool summary table ──
    out.append(
        table(
            n(),
            "PoolSummary",
            _RIGHT_X,
            IN(1.72),
            _RIGHT_W,
            IN(2.30),
            col_widths=[IN(1.55), IN(0.75), IN(1.20), IN(1.53)],
            rows=[
                trow(
                    [
                        tcell("Regional pool", size=PT(9), bold=True, color=WHITE, align="ctr", fill="223E59", borders={"B": {"color": BLACK, "width": 12700}}),
                        tcell("Seats", size=PT(9), bold=True, color=WHITE, align="ctr", fill="223E59", borders={"B": {"color": BLACK, "width": 12700}}),
                        tcell("Realized", size=PT(9), bold=True, color=WHITE, align="ctr", fill="223E59", borders={"B": {"color": BLACK, "width": 12700}}),
                        tcell("Shared ceiling", size=PT(9), bold=True, color=WHITE, align="ctr", fill="223E59", borders={"B": {"color": BLACK, "width": 12700}}),
                    ],
                    h=IN(0.38),
                ),
                trow(
                    [
                        tcell("CONUS", size=PT(10), bold=True, color=BLACK, fill="CEDDEC", borders={"T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}),
                        tcell("6", size=PT(11), bold=True, color=BLACK, align="ctr", borders={"T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}),
                        tcell("$281.7M", size=PT(11), bold=True, color=BLACK, align="ctr", borders={"T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}),
                        tcell("$529M", size=PT(11), color=BLACK, align="ctr", borders={"T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}),
                    ],
                    h=IN(0.46),
                ),
                trow(
                    [
                        tcell("Japan / Korea", size=PT(10), bold=True, color=BLACK, fill="99B9D8", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                        tcell("3", size=PT(11), bold=True, color=BLACK, align="ctr", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                        tcell("$123.2M", size=PT(11), bold=True, color=BLACK, align="ctr", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                        tcell("$216M", size=PT(11), color=BLACK, align="ctr", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                    ],
                    h=IN(0.46),
                ),
                trow(
                    [
                        tcell("Forward", size=PT(10), bold=True, color=WHITE, fill="447BB2", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                        tcell("5", size=PT(11), bold=True, color=BLACK, align="ctr", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                        tcell("$11.9M", size=PT(11), bold=True, color=BLACK, align="ctr", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                        tcell("$186M", size=PT(11), color=BLACK, align="ctr", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}),
                    ],
                    h=IN(0.46),
                ),
                trow(
                    [
                        tcell("POOL TOTAL", size=PT(10), bold=True, color=BLACK, fill="DFE7EB", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": BLACK, "width": 12700}}),
                        tcell_rich(
                            [tpara([trun("14 seats", size=PT(9), bold=True, color=BLACK, font=FONT), tbreak(), trun("10 vendors", size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)],
                            fill="DFE7EB",
                            borders={"T": {"color": "808080", "width": 6350}, "B": {"color": BLACK, "width": 12700}},
                        ),
                        tcell("$416.8M", size=PT(13), bold=True, color="007770", align="ctr", fill="DFE7EB", borders={"T": {"color": "808080", "width": 6350}, "B": {"color": BLACK, "width": 12700}}),
                        tcell_rich(
                            [tpara([trun("Do not sum", size=PT(9), bold=True, color=BLACK, font=FONT), tbreak(), trun("shared by tier", size=PT(8), italic=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)],
                            fill="DFE7EB",
                            borders={"T": {"color": "808080", "width": 6350}, "B": {"color": BLACK, "width": 12700}},
                        ),
                    ],
                    h=IN(0.54),
                ),
            ],
        )
    )

    # ── structure / authority chips ──
    for x, width, fill, color, headline, detail in _AUTHORITY_CHIPS:
        out.append(
            _rich_card(
                n(),
                "AuthorityChip",
                x,
                4.16,
                width,
                0.38,
                fill,
                color,
                "",
                headline,
                detail,
                line_color=BLACK,
                kicker_size=1,
                headline_size=9,
                detail_size=8,
            )
        )

    # ── order-layer clarification ──
    out.append(
        text_box(
            n(),
            "OrderLayer",
            _RIGHT_X,
            IN(4.65),
            _RIGHT_W,
            IN(0.40),
            [
                paragraph(
                    [
                        run("Read the order layer: ", size=PT(9), bold=True, color=BLACK, font=FONT),
                        run("IDV = $0; obligations + TAS sit on child orders. ", size=PT(9), color=BLACK, font=FONT),
                        run("Shared ceilings are capacity, not spend.", size=PT(9), italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=GRAY_1,
            line_color=DK,
            line_width=3175,
            anchor="ctr",
        )
    )

    # ── live-opportunity takeaway ──
    out.append(
        text_box(
            n(),
            "TakeawayBanner",
            IN(0.50),
            IN(5.18),
            IN(12.33),
            IN(0.42),
            [paragraph([run("The on-ramp is live: the pool is expired, open by design, and not yet visibly replaced.", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
            fill="223E59",
            line_color="none",
            anchor="ctr",
        )
    )

    # ── entry routes ──
    for x, width, fill, color, kicker, body in _ENTRY_ROUTES:
        out.append(
            _rich_card(
                n(),
                "EntryRoute",
                x,
                5.72,
                width,
                0.72,
                fill,
                color,
                "",
                kicker,
                body,
                line_color=DK,
                kicker_size=1,
                headline_size=9,
                detail_size=10,
            )
        )

    # ── caveat + sources ──
    out.append(
        text_box(
            n(),
            "SourceNote",
            IN(0.50),
            IN(6.58),
            IN(12.33),
            IN(0.40),
            [
                paragraph(
                    [
                        run("Caveat: ", size=PT(8), bold=True, color=BLACK, font=FONT),
                        run("the 2026-01-25 ordering-period end is date-certain; successor status is inferred. A recently signed DoD award may remain unrevealed for ~90 days—confirm before acting.", size=PT(8), color=BLACK, font=FONT),
                        line_break(),
                        run("Source: SAM Contract Awards; Army contracts extract (USAspending lineage). As of 2026-06-24.", size=PT(8), color=BLACK, font=FONT),
                    ],
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        )
    )

    return "".join(out)


def render() -> str:
    return slide(_body())
