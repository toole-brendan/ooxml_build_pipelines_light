"""recompete_on_ramp — Recompete Radar, slide 03.

EXHIBIT — "Recompete On-Ramp": an expiring multiple-award IDIQ is a dated,
winnable recompete. The worked example is the Army TACOM non-nuclear watercraft
ship-repair pool: all 14 holder vehicles share a recorded last date to order of
2026-01-25; 74 delivery orders have obligated $416.8M; and no successor pool is
visible as of the 2026-06-24 pull.

The slide is intentionally timeline-led rather than KPI-card-led. Left: a dated
ordering-period timeline that separates the date-certain contract expiration from
the inferred open-turnover window. Right: a compact evidence/implication table
showing why the entry route is open (multiple award, full and open, FAR 16.505).
Bottom: one regional-tier table that keeps realized obligations separate from the
three shared ceilings. A full-width takeaway banner links the exhibit back to the
companion "supply the prime" slide.

CODE MAP:
  • chrome .............. breadcrumb() + title_placeholder() + route chip
  • timeline ............ activity band, dated milestones, solid/dashed rules,
                          and an inferred open-turnover window
  • evidence table ...... recorded field/fact → implication for entry
  • regional table ...... CONUS / Japan-Korea / Forward pool footprint
  • takeaway + footnote . action-oriented conclusion and honest caveats/sources

This is a hand-built module following the project's slideLayout4 primitives.
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
    breadcrumb,
    title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_2, GRAY_3, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── palette (house-compatible additions) ──
_NAVY = "223E59"
_BLUE = "447BB2"
_BLUE_LIGHT = "CEDDEC"
_GREEN = "007770"
_GREEN_LIGHT = "DCEFE8"

# ── layout anchors ──
_LEFT_X, _LEFT_W = IN(0.495), IN(7.22)
_RIGHT_X, _RIGHT_W = IN(7.94), IN(4.855)
_TOP_Y = IN(1.42)
_SECTION_TITLE_H = IN(0.23)
_FOOTNOTE_Y = IN(6.69)

# ── dated timeline milestones: (x, fill, date, description) ──
_TIMELINE_MILESTONES = [
    (1.20, BLACK, "2021-01-27", "Ordering period starts"),
    (5.15, _NAVY, "2026-01-25", "Common last date to order\n(all 14 vehicles)"),
    (7.00, _GREEN, "2026-06-24", "No successor visible\nin available data"),
]

# ── evidence rows: (recorded field / fact, implication) ──
_EVIDENCE_ROWS = [
    ("lastDateToOrder = 2026-01-25", "Turnover date was visible years ahead"),
    ("Multiple award; full and open", "Bid for a seat on the follow-on pool"),
    ("FAR 16.505 fair opportunity", "Task orders compete among qualified holders"),
    ("14 vehicles / 10 vendors", "Entry is broader than a closed prime re-up"),
    ("$0 on IDVs; $416.8M on orders", "Read spend and appropriations at child-order level"),
    ("No successor pool visible", "Open turnover is live, but inferred"),
]

# ── regional pool footprint: (tier, fill, vehicles, orders, realized, ceiling) ──
_REGIONAL_ROWS = [
    ("CONUS", _NAVY, "6", "40", "$281.7M", "$529M shared"),
    ("Japan / Korea", _BLUE, "3", "18", "$123.2M", "$216M shared"),
    ("Forward", "6F8DB9", "5", "16", "$11.9M", "$186M shared"),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Recompete Radar", "Army Watercraft Ship Repair"))
    out.append(
        title_placeholder(
            "Recompete On-Ramp",
            "The Army's multiple-award ship-repair pool expired Jan. 25, 2026; no successor is visible, creating an open path to become a holder.",
        )
    )
    out.append(
        text_box(
            n(),
            "Route Chip",
            IN(10.52),
            IN(0.17),
            IN(2.26),
            IN(0.23),
            [paragraph([run("SLIDE 03  |  BECOME A HOLDER", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_NAVY,
            line_color=_NAVY,
            anchor="ctr",
        )
    )

    # ── section headers and divider ──
    out.append(
        text_box(
            n(),
            "Timeline Header",
            _LEFT_X,
            _TOP_Y,
            _LEFT_W,
            _SECTION_TITLE_H,
            [paragraph([run("Dated on-ramp: the contract records the turnover years ahead", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="b",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        )
    )
    out.append(connector(n(), "Timeline Header Rule", _LEFT_X, IN(1.69), _LEFT_W, IN(0), color=BLACK, width=12700))
    out.append(
        text_box(
            n(),
            "Evidence Header",
            _RIGHT_X,
            _TOP_Y,
            _RIGHT_W,
            _SECTION_TITLE_H,
            [paragraph([run("Why the route is open", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="b",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        )
    )
    out.append(connector(n(), "Evidence Header Rule", _RIGHT_X, IN(1.69), _RIGHT_W, IN(0), color=BLACK, width=12700))
    out.append(connector(n(), "Panel Divider", IN(7.82), IN(1.48), IN(0), IN(2.98), color=GRAY_3, width=6350))

    # ── timeline: activity band + open-turnover band ──
    out.append(
        text_box(
            n(),
            "Order Activity Band",
            IN(1.20),
            IN(2.05),
            IN(3.95),
            IN(0.56),
            [
                paragraph(
                    [
                        run("ACTIVE ORDERING PERIOD", size=PT(9), bold=True, color=BLACK, font=FONT),
                        line_break(),
                        run("74 delivery orders  |  $416.8M realized", size=PT(12), bold=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=GRAY_1,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Open Turnover Band",
            IN(5.15),
            IN(2.05),
            IN(1.85),
            IN(0.56),
            [
                paragraph(
                    [
                        run("OPEN TURNOVER", size=PT(9), bold=True, color=_GREEN, font=FONT),
                        line_break(),
                        run("successor not seen", size=PT(11), bold=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=_GREEN_LIGHT,
            line_color=_GREEN,
            line_width=12700,
            dashed_line=True,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Date Certainty Label",
            IN(4.20),
            IN(1.78),
            IN(1.90),
            IN(0.20),
            [paragraph([run("DATE-CERTAIN", size=PT(8), bold=True, color=_NAVY, font=FONT)], align="ctr", line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Inference Label",
            IN(5.62),
            IN(1.78),
            IN(1.56),
            IN(0.20),
            [paragraph([run("INFERRED", size=PT(8), bold=True, color=_GREEN, font=FONT)], align="r", line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )

    # solid ordering-period rule, then dashed post-expiration rule
    out.append(connector(n(), "Ordering Period Rule", IN(1.20), IN(3.02), IN(3.95), IN(0), color=BLACK, width=19050))
    out.append(connector(n(), "Turnover Window Rule", IN(5.15), IN(3.02), IN(1.85), IN(0), color=_GREEN, width=19050, dashed=True, arrow=True))

    # milestone markers, date labels, descriptions, and vertical ticks
    for _x, _fill, _date, _desc in _TIMELINE_MILESTONES:
        out.append(connector(n(), "Milestone Tick", IN(_x + 0.08), IN(2.67), IN(0), IN(0.70), color=_fill, width=12700))
        out.append(
            text_box(
                n(),
                "Milestone Marker",
                IN(_x),
                IN(2.94),
                IN(0.16),
                IN(0.16),
                [paragraph([], align="ctr", line_spacing=100000)],
                fill=_fill,
                line_color=_fill,
                prst="ellipse",
                anchor="ctr",
            )
        )
        out.append(
            text_box(
                n(),
                "Milestone Date",
                IN(_x - 0.35),
                IN(3.34),
                IN(0.86),
                IN(0.23),
                [paragraph([run(_date, size=PT(9), bold=True, color=_fill, font=FONT)], align="ctr", line_spacing=100000)],
                fill=None,
                line_color="none",
                anchor="ctr",
                l_ins=0,
                r_ins=0,
            )
        )
        out.append(
            text_box(
                n(),
                "Milestone Description",
                IN(_x - 0.52),
                IN(3.58),
                IN(1.20),
                IN(0.52),
                [paragraph([run(_desc, size=PT(9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
                fill=None,
                line_color="none",
                anchor="t",
                l_ins=0,
                r_ins=0,
                t_ins=0,
                b_ins=0,
            )
        )

    out.append(
        text_box(
            n(),
            "Timeline Read",
            IN(1.18),
            IN(4.15),
            IN(6.10),
            IN(0.26),
            [
                paragraph(
                    [
                        run("Read-through: ", size=PT(9), bold=True, color=BLACK, font=FONT),
                        run("the expiration is recorded; the live opportunity follows from the successor check.", size=PT(9), italic=True, color=BLACK, font=FONT),
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

    # ── evidence → implication table ──
    evidence_rows = [
        trow(
            [
                tcell("Recorded field / fact", size=PT(9), bold=True, color=BLACK, fill=GRAY_2, borders={"L": "none", "R": {"color": WHITE, "width": 12700}, "T": "none", "B": {"color": BLACK, "width": 12700}}),
                tcell("Implication for entry", size=PT(9), bold=True, color=BLACK, fill=GRAY_2, borders={"L": {"color": WHITE, "width": 12700}, "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}),
            ],
            h=IN(0.31),
        )
    ]
    for _fact, _implication in _EVIDENCE_ROWS:
        evidence_rows.append(
            trow(
                [
                    tcell(_fact, size=PT(8.5), bold=True, color=BLACK, borders={"L": "none", "R": {"color": GRAY_3, "width": 6350}, "T": {"color": GRAY_3, "width": 6350}, "B": {"color": GRAY_3, "width": 6350}}),
                    tcell(_implication, size=PT(8.5), color=BLACK, borders={"L": {"color": GRAY_3, "width": 6350}, "R": "none", "T": {"color": GRAY_3, "width": 6350}, "B": {"color": GRAY_3, "width": 6350}}),
                ],
                h=IN(0.36),
            )
        )
    out.append(
        table(
            n(),
            "Evidence Table",
            _RIGHT_X,
            IN(1.79),
            _RIGHT_W,
            IN(2.47),
            col_widths=[IN(2.20), IN(2.655)],
            rows=evidence_rows,
        )
    )
    out.append(
        text_box(
            n(),
            "Entry Action",
            _RIGHT_X,
            IN(4.29),
            _RIGHT_W,
            IN(0.31),
            [
                paragraph(
                    [
                        run("FOLLOW-ON PATH: ", size=PT(9), bold=True, color=_NAVY, font=FONT),
                        run("bid onto the next pool—or subcontract to a current holder.", size=PT(9), bold=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=_BLUE_LIGHT,
            line_color="none",
            anchor="ctr",
        )
    )

    # ── regional tier heading and pool-total read ──
    out.append(
        text_box(
            n(),
            "Regional Header",
            IN(0.495),
            IN(4.66),
            IN(3.45),
            IN(0.22),
            [paragraph([run("Three regional tiers", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)],
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
            "Pool Total Read",
            IN(4.05),
            IN(4.66),
            IN(8.745),
            IN(0.22),
            [
                paragraph(
                    [
                        run("Pool total: ", size=PT(9), bold=True, color=BLACK, font=FONT),
                        run("14 vehicles · 10 vendors · 74 orders · $416.8M realized  |  ceilings are shared, not spend", size=PT(9), italic=True, color=BLACK, font=FONT),
                    ],
                    align="r",
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
            anchor="b",
            l_ins=0,
            r_ins=0,
            t_ins=0,
            b_ins=0,
        )
    )
    out.append(connector(n(), "Regional Header Rule", IN(0.495), IN(4.91), IN(12.30), IN(0), color=BLACK, width=12700))

    regional_rows = [
        trow(
            [
                tcell("Regional tier", size=PT(9), bold=True, color=BLACK, fill=GRAY_2, borders={"L": "none", "R": {"color": WHITE, "width": 12700}, "T": "none", "B": {"color": BLACK, "width": 12700}}),
                tcell("Holder vehicles", size=PT(9), bold=True, color=BLACK, align="ctr", fill=GRAY_2, borders={"L": {"color": WHITE, "width": 12700}, "R": {"color": WHITE, "width": 12700}, "T": "none", "B": {"color": BLACK, "width": 12700}}),
                tcell("Orders", size=PT(9), bold=True, color=BLACK, align="ctr", fill=GRAY_2, borders={"L": {"color": WHITE, "width": 12700}, "R": {"color": WHITE, "width": 12700}, "T": "none", "B": {"color": BLACK, "width": 12700}}),
                tcell("Realized obligation", size=PT(9), bold=True, color=BLACK, align="ctr", fill=GRAY_2, borders={"L": {"color": WHITE, "width": 12700}, "R": {"color": WHITE, "width": 12700}, "T": "none", "B": {"color": BLACK, "width": 12700}}),
                tcell("Shared tier ceiling", size=PT(9), bold=True, color=BLACK, align="ctr", fill=GRAY_2, borders={"L": {"color": WHITE, "width": 12700}, "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}),
            ],
            h=IN(0.30),
        )
    ]
    for _tier, _fill, _vehicles, _orders, _realized, _ceiling in _REGIONAL_ROWS:
        regional_rows.append(
            trow(
                [
                    tcell(_tier, size=PT(10), bold=True, color=WHITE, fill=_fill, borders={"L": "none", "R": {"color": WHITE, "width": 12700}, "T": {"color": WHITE, "width": 6350}, "B": {"color": WHITE, "width": 6350}}),
                    tcell(_vehicles, size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": {"color": WHITE, "width": 12700}, "R": {"color": GRAY_3, "width": 6350}, "T": {"color": GRAY_3, "width": 6350}, "B": {"color": GRAY_3, "width": 6350}}),
                    tcell(_orders, size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": {"color": GRAY_3, "width": 6350}, "R": {"color": GRAY_3, "width": 6350}, "T": {"color": GRAY_3, "width": 6350}, "B": {"color": GRAY_3, "width": 6350}}),
                    tcell(_realized, size=PT(11), bold=True, color=BLACK, align="ctr", borders={"L": {"color": GRAY_3, "width": 6350}, "R": {"color": GRAY_3, "width": 6350}, "T": {"color": GRAY_3, "width": 6350}, "B": {"color": GRAY_3, "width": 6350}}),
                    tcell(_ceiling, size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": {"color": GRAY_3, "width": 6350}, "R": "none", "T": {"color": GRAY_3, "width": 6350}, "B": {"color": GRAY_3, "width": 6350}}),
                ],
                h=IN(0.31),
            )
        )
    out.append(
        table(
            n(),
            "Regional Tier Table",
            IN(0.495),
            IN(4.95),
            IN(12.30),
            IN(1.23),
            col_widths=[IN(3.00), IN(1.65), IN(1.25), IN(3.00), IN(3.40)],
            rows=regional_rows,
        )
    )

    # ── takeaway banner ──
    out.append(
        text_box(
            n(),
            "Takeaway Banner",
            IN(0.495),
            IN(6.22),
            IN(12.30),
            IN(0.43),
            [
                paragraph(
                    [
                        run("ORDERING PERIOD CLOSED + NO SUCCESSOR VISIBLE  →  ", size=PT(11), bold=True, color=_NAVY, font=FONT),
                        run("the follow-on pool is a live holder on-ramp, not a closed prime re-up.", size=PT(11), bold=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=_BLUE_LIGHT,
            line_color="none",
            anchor="ctr",
        )
    )

    # ── honest caveats + sources ──
    out.append(
        text_box(
            n(),
            "Footnote",
            IN(0.495),
            _FOOTNOTE_Y,
            IN(12.30),
            IN(0.30),
            [
                paragraph(
                    [
                        run("Note: ", size=PT(7.5), bold=True, color=BLACK, font=FONT),
                        run("The 2026-01-25 last date to order is recorded; the successor opportunity is inferred. A DoD award signed in the last ~90 days may be unrevealed on a non-federal SAM key. Tier ceilings are shared across holders and must not be summed; realized order obligations are the summable measure. ", size=PT(7.5), color=BLACK, font=FONT),
                        run("Source: SAM Contract Awards; Army contracts extract (USAspending lineage); FAR 16.505. Army extract through 2026-06-20; successor check / pull as of 2026-06-24.", size=PT(7.5), italic=True, color=BLACK, font=FONT),
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
