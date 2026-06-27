"""recompete_cadence_supply_chain_entry — Recompete cadence → supply-chain entry (deck slide 6).

EXHIBIT — "Recompete Cadence → Supply-Chain Entry": the DDG-51 prime award is a
closed HII / Bath Iron Works duopoly, but its five-year multi-year-procurement
cadence creates a visible, recurring first-tier sourcing wave. The slide combines:

  • a route-to-market strip (closed prime → fixed cadence → open supplier layer),
  • a 2013 / 2018 / 2023 / ~2028 cadence and supplier-wave visual,
  • a supplier-base summary and system-concentration entry table,
  • a bottom action banner and an honest FFATA reporting caveat.

The layout follows the project-course pattern used by
``status_quo_outlook_oceangoing`` (left visual + right decision table + takeaway),
with timeline devices adapted from ``production_outlook_colocated`` and the
route-to-market strip adapted from ``tcv_to_acv_company_acv``.

This is a native-shape module: no chart template or external media is required.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    connector,
    table,
    trow,
    tcell,
    tcell_rich,
    tpara,
    trun,
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
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_4,
    GRAY_1,
    GRAY_2,
    GRAY_3,
    FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []

# ── palette additions used only on this slide ──
_TEAL = "007770"
_TEAL_LIGHT = "DDEFE7"
_FORECAST_FILL = "EDF3F8"
_BLUE_LINE = "447BB2"
_RULE = "808080"

# ── layout anchors ──
_LEFT_X, _LEFT_W = IN(0.495), IN(7.72)
_RIGHT_X, _RIGHT_W = IN(8.55), IN(4.245)
_CARD_Y, _CARD_H = IN(1.42), IN(0.62)
_TIMELINE_Y = IN(2.79)
_BAR_BASE_Y = IN(5.02)
_BAR_W = IN(1.34)
_FOOT_Y = IN(6.635)

# ── repeated-shape data ──
_ROUTE_CARDS = [
    # (x, width, fill, line, text colour, headline, detail)
    (0.495, 2.08, BLACK, BLACK, WHITE, "Closed prime", "HII + BIW only"),
    (2.84, 2.44, BLUE_1, DK, BLACK, "Five-year cadence", "2013 · 2018 · 2023 · ~2028"),
    (5.55, 2.665, BLUE_3, DK, WHITE, "Open supplier layer", "~$1B+ first-tier wave / block"),
]

_AWARD_NODES = [
    # (x, award year, block label, forecast?) — x aligns with supplier-wave centre
    (1.36, "2013", "FY13–17 MYP", False),
    (3.32, "2018", "FY18–22 MYP", False),
    (5.28, "2023", "FY23–27 MYP", False),
    (7.24, "~2028", "FY28–32 MYP", True),
]

_SUPPLIER_WAVES = [
    # (x, y, h, fill, line, dashed, text colour, amount, suppliers / status)
    (0.69, 4.03, 0.99, BLUE_1, DK, False, BLACK, "$0.94B", "320 suppliers"),
    (2.65, 3.66, 1.36, BLUE_2, DK, False, BLACK, "$1.33B", "344 suppliers"),
    (4.61, 3.84, 1.18, BLUE_3, DK, False, WHITE, "$1.14B*", "89 suppliers*"),
    (6.57, 3.97, 1.05, WHITE, _BLUE_LINE, True, BLACK, "~$1B+", "2028–31 window"),
]

_FACT_CARDS = [
    # (x, fill, text colour, big number, caption)
    (8.55, BLUE_2, BLACK, "$3.47B", "reported first-tier $"),
    (9.995, GRAY_1, BLACK, "521", "distinct suppliers"),
    (11.44, BLUE_4, WHITE, "266", "recurring suppliers"),
]


def _none_borders() -> dict:
    return {"L": "none", "R": "none", "T": "none", "B": "none"}


def _row_borders(top: str | dict, bottom: str | dict) -> dict:
    return {"L": "none", "R": "none", "T": top, "B": bottom}


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Recompete On-Ramps", "Supply the prime"))
    out.append(
        title_placeholder(
            "Recompete Cadence → Supply-Chain Entry",
            "DDG-51's closed prime re-awards every ~5 years, creating a predictable ~$1B+ supplier wave—the next opens ~2028–31.",
        )
    )
    out.append(
        text_box(
            n(),
            "Path chip",
            IN(9.90),
            IN(0.122),
            IN(1.15),
            IN(0.317),
            [paragraph([run("Path 1 of 2", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)],
            fill="CEDDEC",
            line_color=DK,
            line_width=3175,
            anchor="ctr",
        )
    )
    out.append(prelim_chip())

    # ── route-to-market strip ──
    for _x, _w, _fill, _line, _tc, _head, _detail in _ROUTE_CARDS:
        out.append(
            text_box(
                n(),
                "Route card",
                IN(_x),
                _CARD_Y,
                IN(_w),
                _CARD_H,
                [
                    paragraph([run(_head, size=PT(11), bold=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000),
                    paragraph([run(_detail, size=PT(9), color=_tc, font=FONT)], align="ctr", line_spacing=100000),
                ],
                fill=_fill,
                line_color=_line,
                line_width=3175,
                anchor="ctr",
            )
        )
    out.append(connector(n(), "Route arrow 1", IN(2.59), IN(1.73), IN(0.22), IN(0), color=DK, width=12700, arrow=True))
    out.append(connector(n(), "Route arrow 2", IN(5.30), IN(1.73), IN(0.22), IN(0), color=DK, width=12700, arrow=True))

    # ── left panel: cadence and first-tier sourcing waves ──
    out.append(
        text_box(
            n(),
            "Cadence heading",
            _LEFT_X,
            IN(2.20),
            _LEFT_W,
            IN(0.24),
            [paragraph([run("Five-year prime cadence dates the supplier sourcing wave", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="b",
        )
    )
    out.append(
        text_box(
            n(),
            "Forecast window",
            IN(6.39),
            IN(2.48),
            IN(1.82),
            IN(2.55),
            [paragraph([], line_spacing=100000)],
            fill=_FORECAST_FILL,
            line_color="none",
            anchor="t",
        )
    )
    out.append(connector(n(), "Cadence line", IN(0.92), _TIMELINE_Y, IN(6.98), IN(0), color=DK, width=12700, arrow=True))

    for _x, _year, _block, _forecast in _AWARD_NODES:
        out.append(
            text_box(
                n(),
                "Award year",
                IN(_x - 0.31),
                IN(2.48),
                IN(0.62),
                IN(0.22),
                [paragraph([run(_year, size=PT(10), bold=True, color=_BLUE_LINE if _forecast else BLACK, font=FONT)], align="ctr", line_spacing=100000)],
                fill=None,
                line_color="none",
                anchor="ctr",
            )
        )
        out.append(
            text_box(
                n(),
                "Award node",
                IN(_x - 0.09),
                IN(2.70),
                IN(0.18),
                IN(0.18),
                [paragraph([], align="ctr", line_spacing=100000)],
                fill=WHITE if _forecast else DK,
                line_color=_BLUE_LINE if _forecast else DK,
                line_width=12700,
                prst="ellipse",
                anchor="ctr",
            )
        )
        out.append(
            text_box(
                n(),
                "Block label",
                IN(_x - 0.58),
                IN(2.93),
                IN(1.16),
                IN(0.31),
                [paragraph([run(_block, size=PT(9), bold=True, color=_BLUE_LINE if _forecast else BLACK, font=FONT)], align="ctr", line_spacing=100000)],
                fill=None,
                line_color="none",
                anchor="ctr",
            )
        )

    # light leaders connect each award date to the supplier wave it triggers
    for (_x, _year, _block, _forecast), (_bar_x, _bar_y, _bar_h, _fill, _line, _dash, _tc, _amount, _supplier_text) in zip(_AWARD_NODES, _SUPPLIER_WAVES):
        out.append(
            connector(
                n(),
                "Award-to-wave leader",
                IN(_x),
                IN(3.24),
                IN(0),
                IN(_bar_y - 3.24),
                color=_BLUE_LINE if _forecast else GRAY_3,
                width=3175,
                dashed=True,
            )
        )

    # FORECAST label — a band-fill chip in the clear gap below the block labels,
    # painted after the leaders so it cleanly interrupts the dashed forecast leader
    # (instead of colliding with the ~2028 award-year label at the top of the band).
    out.append(
        text_box(
            n(),
            "Forecast label",
            IN(6.39),
            IN(3.45),
            IN(1.82),
            IN(0.22),
            [paragraph([run("FORECAST", size=PT(8), bold=True, color=_BLUE_LINE, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_FORECAST_FILL,
            line_color="none",
            anchor="ctr",
        )
    )

    # bars are proportional enough to communicate relative magnitude without implying precision
    for _x, _y, _h, _fill, _line, _dash, _tc, _amount, _supplier_text in _SUPPLIER_WAVES:
        out.append(
            text_box(
                n(),
                "Supplier wave",
                IN(_x),
                IN(_y),
                _BAR_W,
                IN(_h),
                [
                    paragraph([run(_amount, size=PT(12), bold=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000),
                    paragraph([run(_supplier_text, size=PT(9), color=_tc, font=FONT)], align="ctr", line_spacing=100000),
                ],
                fill=_fill,
                line_color=_line,
                line_width=6350,
                dashed_line=_dash,
                anchor="ctr",
            )
        )
    out.append(connector(n(), "Supplier-wave baseline", IN(0.58), _BAR_BASE_Y, IN(7.46), IN(0), color=DK, width=6350))
    out.append(
        text_box(
            n(),
            "Wave label",
            IN(0.60),
            IN(5.08),
            IN(4.4),
            IN(0.20),
            [paragraph([run("First-tier subaward $ by named MYP block (total reported $3.47B)", size=PT(9), italic=True, color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="t",
        )
    )
    out.append(
        text_box(
            n(),
            "Lag callout",
            IN(0.62),
            IN(5.38),
            IN(7.36),
            IN(0.47),
            [
                paragraph(
                    [
                        run("Front-loaded after the prime award: ", size=PT(10), bold=True, color=BLACK, font=FONT),
                        run("26%", size=PT(10), bold=True, color=_BLUE_LINE, font=FONT),
                        run(" lands in year 0; ", size=PT(10), color=BLACK, font=FONT),
                        run("~80%", size=PT(10), bold=True, color=_BLUE_LINE, font=FONT),
                        run(" within four years.", size=PT(10), color=BLACK, font=FONT),
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

    # ── divider between evidence and decision rail ──
    out.append(connector(n(), "Panel divider", IN(8.37), IN(1.38), IN(0), IN(4.53), color=GRAY_3, width=6350))

    # ── right rail: supplier-base facts and where-to-enter table ──
    for _x, _fill, _tc, _big, _cap in _FACT_CARDS:
        out.append(
            text_box(
                n(),
                "Fact card",
                IN(_x),
                _CARD_Y,
                IN(1.355),
                _CARD_H,
                [
                    paragraph([run(_big, size=PT(13), bold=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000),
                    paragraph([run(_cap, size=PT(8), color=_tc, font=FONT)], align="ctr", line_spacing=100000),
                ],
                fill=_fill,
                line_color=DK if _fill != GRAY_1 else GRAY_3,
                line_width=3175,
                anchor="ctr",
            )
        )

    out.append(
        text_box(
            n(),
            "Entry heading",
            _RIGHT_X,
            IN(2.22),
            _RIGHT_W,
            IN(0.25),
            [paragraph([run("Where to enter: big + fragmented wins", size=PT(11), bold=True, color=BLACK, font=FONT)], line_spacing=100000)],
            fill=None,
            line_color="none",
            anchor="b",
        )
    )

    thin_top = {"color": _RULE, "width": 6350}
    thin_bottom = {"color": _RULE, "width": 6350}
    white_top = {"color": WHITE, "width": 12700}
    out.append(
        table(
            n(),
            "System concentration table",
            _RIGHT_X,
            IN(2.52),
            _RIGHT_W,
            IN(2.15),
            col_widths=[IN(1.28), IN(0.61), IN(0.72), IN(1.635)],
            rows=[
                trow(
                    [
                        tcell("Ship system", size=PT(9), bold=True, color=WHITE, align="ctr", fill=DK, borders=_none_borders()),
                        tcell("$M", size=PT(9), bold=True, color=WHITE, align="ctr", fill=DK, borders=_none_borders()),
                        tcell("HHI", size=PT(9), bold=True, color=WHITE, align="ctr", fill=DK, borders=_none_borders()),
                        tcell("Route", size=PT(9), bold=True, color=WHITE, align="ctr", fill=DK, borders=_none_borders()),
                    ],
                    h=IN(0.35),
                ),
                trow(
                    [
                        tcell("Auxiliary", size=PT(9), bold=True, color=BLACK, fill=_TEAL_LIGHT, borders=_row_borders(white_top, thin_bottom)),
                        tcell("948", size=PT(9), color=BLACK, align="ctr", fill=_TEAL_LIGHT, borders=_row_borders(white_top, thin_bottom)),
                        tcell("683", size=PT(9), color=BLACK, align="ctr", fill=_TEAL_LIGHT, borders=_row_borders(white_top, thin_bottom)),
                        tcell_rich(
                            [
                                tpara([trun("ENTER", size=PT(9), bold=True, color=_TEAL, font=FONT)], align="ctr", mar_l=0, indent=0),
                                tpara([trun("no supplier >16%", size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0),
                            ],
                            fill=_TEAL_LIGHT,
                            borders=_row_borders(white_top, thin_bottom),
                        ),
                    ],
                    h=IN(0.57),
                ),
                trow(
                    [
                        tcell("Propulsion", size=PT(9), bold=True, color=BLACK, fill=GRAY_1, borders=_row_borders(thin_top, thin_bottom)),
                        tcell("958", size=PT(9), color=BLACK, align="ctr", fill=GRAY_1, borders=_row_borders(thin_top, thin_bottom)),
                        tcell("1,905", size=PT(9), color=BLACK, align="ctr", fill=GRAY_1, borders=_row_borders(thin_top, thin_bottom)),
                        tcell_rich(
                            [
                                tpara([trun("TEAM", size=PT(9), bold=True, color=DK, font=FONT)], align="ctr", mar_l=0, indent=0),
                                tpara([trun("GE 35%", size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0),
                            ],
                            fill=GRAY_1,
                            borders=_row_borders(thin_top, thin_bottom),
                        ),
                    ],
                    h=IN(0.57),
                ),
                trow(
                    [
                        tcell("Electric", size=PT(9), bold=True, color=BLACK, fill=GRAY_2, borders=_row_borders(thin_top, "none")),
                        tcell("751", size=PT(9), color=BLACK, align="ctr", fill=GRAY_2, borders=_row_borders(thin_top, "none")),
                        tcell("2,106", size=PT(9), color=BLACK, align="ctr", fill=GRAY_2, borders=_row_borders(thin_top, "none")),
                        tcell_rich(
                            [
                                tpara([trun("TEAM", size=PT(9), bold=True, color=DK, font=FONT)], align="ctr", mar_l=0, indent=0),
                                tpara([trun("Rolls-Royce 43%", size=PT(8), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0),
                            ],
                            fill=GRAY_2,
                            borders=_row_borders(thin_top, "none"),
                        ),
                    ],
                    h=IN(0.57),
                ),
            ],
        )
    )

    out.append(
        text_box(
            n(),
            "Concentration read",
            _RIGHT_X,
            IN(4.91),
            _RIGHT_W,
            IN(0.89),
            [
                paragraph([run("Entry read", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000),
                paragraph(
                    [
                        run("Auxiliary", size=PT(9), bold=True, color=_TEAL, font=FONT),
                        run(" is fragmented (HHI 683, no supplier >16%); propulsion and electric are concentrated (HHI 1,900+, one supplier above a third each).", size=PT(9), color=BLACK, font=FONT),
                    ],
                    line_spacing=100000,
                ),
            ],
            fill=GRAY_1,
            line_color="none",
            anchor="ctr",
        )
    )

    # ── bottom takeaway and caveat ──
    out.append(
        text_box(
            n(),
            "Action banner",
            IN(0.495),
            IN(6.05),
            IN(12.30),
            IN(0.45),
            [
                paragraph(
                    [
                        run("ACTION: ", size=PT(11), bold=True, color=_TEAL, font=FONT),
                        run("begin qualification before 2028; target auxiliary systems directly and partner into propulsion / electric.", size=PT(11), bold=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill="CEDDEC",
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Caveat and source",
            IN(0.495),
            _FOOT_Y,
            IN(12.30),
            IN(0.36),
            [
                paragraph(
                    [
                        run("Note: ", size=PT(8), bold=True, color=BLACK, font=FONT),
                        run("FFATA is first-tier only, lags 6–18 months, and materially under-reports BIW; totals are a floor. *FY23–27 is still reporting (incomplete). The 2028–31 window is a demand-surge forecast, not a bid deadline. ", size=PT(8), color=BLACK, font=FONT),
                        run("Source: ", size=PT(8), bold=True, color=BLACK, font=FONT),
                        run("SAM.gov Contract Awards / Subaward Reporting; USAspending; DDG-51 research extract. As of 2026-06-24.", size=PT(8), color=BLACK, font=FONT),
                    ],
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
            anchor="t",
        )
    )

    return "".join(out)


def render() -> str:
    return slide(_body())
