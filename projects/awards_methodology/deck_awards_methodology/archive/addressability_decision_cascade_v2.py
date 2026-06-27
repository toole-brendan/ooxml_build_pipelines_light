"""addressability_decision_cascade — generalized federal-award addressability method.

HAND-BUILT MODULE — Slide 01 method opener for the two worked addressability
examples that follow. The exhibit separates event probability from company
addressability, classifies the award record, walks five gates, and terminates in
four named routes to revenue. A failed gate as prime redirects the opportunity;
it does not automatically eliminate the underlying demand.

LAYOUT / SOURCE-MODULE DNA:
  • chrome ............... breadcrumb() + title_placeholder()
  • framing strip ........ Event probability ≠ Addressability
  • precondition ......... classify the record before applying the gates
  • _GATES ............... five stacked criterion / redirect rows; Access is pivot
  • waypoint ............. ADDRESSABLE MARKET focal stop after Gate 1
  • _ROUTES .............. four posture-tagged route leaves at the payoff
  • portal overlay ....... visibility is a property of the search set, not a gate
  • right rail ........... bold finding, supporting observations, guardrails
  • source line .......... award portals and referenced FAR / DFARS authorities

The content is intentionally conceptual: no program, vehicle, or dollar figures
appear on the slide face. The full access-posture matrix belongs in notes / wiki.
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
    breadcrumb,
    title_placeholder,
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
    FONT,
)

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors ────────────────────────────────────────────────────────────
_MAIN_X, _MAIN_W = IN(0.495), IN(8.95)
_RAIL_X, _RAIL_W = IN(9.66), IN(3.135)

_LABEL_X, _LABEL_W = IN(0.495), IN(1.32)
_READ_X, _READ_W = IN(1.86), IN(4.85)
_VERDICT_X, _VERDICT_W = IN(6.76), IN(2.685)

_ROW_LINE_W = 6350
_MAJOR_LINE_W = 12700


# ── repeated-shape data tables ────────────────────────────────────────────────
_GATES = [
    {
        "y": 2.38,
        "h": 0.53,
        "number": "GATE 1",
        "name": "Demand",
        "read_label": "READ",
        "read": "Obligations on orders and quantity-adding modifications are committed demand; ceilings, TBAOV and unexercised options are capacity.",
        "verdict_label": "FAIL →",
        "verdict": "Track actual orders; do not count capacity as revenue.",
        "label_fill": GRAY_2,
        "read_fill": WHITE,
        "verdict_fill": GRAY_1,
        "label_color": BLACK,
        "read_color": BLACK,
        "verdict_color": BLACK,
    },
    {
        "y": 3.33,
        "h": 0.62,
        "number": "GATE 2 · PIVOT",
        "name": "Access",
        "read_label": "READ",
        "read": "Who may legally compete? Test extent of competition, single- vs. multiple-award structure, and the FAR 16.505 order route.",
        "verdict_label": "PASS →",
        "verdict": "Prime bid.\nFAIL AS PRIME → choose the surviving route.",
        "label_fill": BLUE_3,
        "read_fill": BLACK,
        "verdict_fill": BLACK,
        "label_color": WHITE,
        "read_color": WHITE,
        "verdict_color": WHITE,
    },
    {
        "y": 4.00,
        "h": 0.49,
        "number": "GATE 3",
        "name": "Timing",
        "read_label": "READ",
        "read": "Separate period of performance, ordering-period end and option dates. Is there an upcoming contracting action to target?",
        "verdict_label": "FAIL →",
        "verdict": "Monitor. A bridge delays the follow-on; it does not prove abandonment.",
        "label_fill": GRAY_2,
        "read_fill": WHITE,
        "verdict_fill": GRAY_1,
        "label_color": BLACK,
        "read_color": BLACK,
        "verdict_color": BLACK,
    },
    {
        "y": 4.54,
        "h": 0.49,
        "number": "GATE 4",
        "name": "Ability",
        "read_label": "TEST",
        "read": "Responsibility, past performance, facility clearance, auditable accounting and required subcontract flowdowns.",
        "verdict_label": "FAIL →",
        "verdict": "Qualify, team or subcontract.",
        "label_fill": GRAY_2,
        "read_fill": WHITE,
        "verdict_fill": GRAY_1,
        "label_color": BLACK,
        "read_color": BLACK,
        "verdict_color": BLACK,
    },
    {
        "y": 5.08,
        "h": 0.49,
        "number": "GATE 5",
        "name": "Economics",
        "read_label": "TEST",
        "read": "Contract type and payment risk, financing, data rights, compliance and security burden—does risk-adjusted value fit?",
        "verdict_label": "FAIL →",
        "verdict": "Pass, or pursue a different tier.",
        "label_fill": GRAY_2,
        "read_fill": WHITE,
        "verdict_fill": GRAY_1,
        "label_color": BLACK,
        "read_color": BLACK,
        "verdict_color": BLACK,
    },
]

_ROUTE_W = 2.1625
_ROUTES = [
    {
        "x": 0.495,
        "tag": "OPEN STANDALONE / RECOMPETE",
        "route": "BID THE RECOMPETE",
        "detail": "Compete as prime.",
        "fill": BLUE_1,
        "tag_color": BLACK,
    },
    {
        "x": 2.7575,
        "tag": "MULTIPLE-AWARD IDIQ",
        "route": "ON-RAMP",
        "detail": "Seat at the next pool—or team to a holder. (Slide 03)",
        "fill": BLUE_2,
        "tag_color": BLACK,
    },
    {
        "x": 5.02,
        "tag": "CLOSED PRIME / DIRECTED ACTION",
        "route": "SUBCONTRACT / TEAM",
        "detail": "Closed prime ≠ closed market; enter below the holder. (Slide 02)",
        "fill": BLUE_3,
        "tag_color": WHITE,
    },
    {
        "x": 7.2825,
        "tag": "OT / PROTOTYPE PATH",
        "route": "CONSORTIUM / OT",
        "detail": "Enter early—or the production follow-on closes.",
        "fill": BLUE_4,
        "tag_color": WHITE,
    },
]


# ── helpers ───────────────────────────────────────────────────────────────────
def _gate_label_paragraph(number: str, name: str, color: str) -> list:
    return [
        paragraph(
            [
                run(number, size=PT(7.5), bold=True, color=color, font=FONT),
                line_break(),
                run(name, size=PT(10), bold=True, color=color, font=FONT),
            ],
            align="ctr",
            line_spacing=95000,
        )
    ]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Federal Market Addressability", "Method"))
    out.append(
        title_placeholder(
            "Addressability",
            "A large award isn't an opportunity until it clears five gates — and the gate it fails as prime names the route in.",
        )
    )

    # ── framing strip: the two questions the eye tends to conflate ──
    out.append(
        text_box(
            n(),
            "Event probability",
            IN(0.495),
            IN(1.33),
            IN(4.08),
            IN(0.36),
            [
                paragraph(
                    [
                        run("EVENT PROBABILITY  ", size=PT(8), bold=True, color=BLACK, font=FONT),
                        run("Will the Government buy again?", size=PT(9), italic=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=GRAY_1,
            line_color=DK,
            line_width=_ROW_LINE_W,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Not equal",
            IN(4.64),
            IN(1.33),
            IN(0.56),
            IN(0.36),
            [paragraph([run("≠", size=PT(16), bold=True, color=DK, font=FONT)], align="ctr")],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Addressability",
            IN(5.265),
            IN(1.33),
            IN(4.18),
            IN(0.36),
            [
                paragraph(
                    [
                        run("ADDRESSABILITY  ", size=PT(8), bold=True, color=WHITE, font=FONT),
                        run("Can this company reach, win, and profit?", size=PT(9), italic=True, color=WHITE, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=BLACK,
            line_color=BLACK,
            line_width=_MAJOR_LINE_W,
            anchor="ctr",
        )
    )

    # ── precondition: classify the record before applying the cascade ──
    out.append(
        text_box(
            n(),
            "Precondition label",
            _LABEL_X,
            IN(1.78),
            _LABEL_W,
            IN(0.52),
            [
                paragraph(
                    [
                        run("PRECONDITION", size=PT(7.5), bold=True, color=BLACK, font=FONT),
                        line_break(),
                        run("Classify", size=PT(10), bold=True, color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=95000,
                )
            ],
            fill=GRAY_2,
            line_color=DK,
            line_width=_ROW_LINE_W,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Precondition text",
            _READ_X,
            IN(1.78),
            IN(7.585),
            IN(0.52),
            [
                paragraph(
                    [
                        run("Name the object before gating it: ", size=PT(8.5), bold=True, color=BLACK, font=FONT),
                        run(
                            "standalone contract; IDV + subtype (IDIQ / BPA / BOA / FSS); order; modification / option; qualifying first-tier report; or OT. Object type, contract type and award structure are different dimensions.",
                            size=PT(8.5),
                            color=BLACK,
                            font=FONT,
                        ),
                    ],
                    line_spacing=100000,
                )
            ],
            fill=WHITE,
            line_color=DK,
            line_width=_ROW_LINE_W,
            anchor="ctr",
        )
    )

    # connector into Gate 1
    out.append(
        connector(
            n(),
            "Cascade arrow 0",
            IN(4.97),
            IN(2.30),
            IN(0),
            IN(0.08),
            color=DK,
            width=_MAJOR_LINE_W,
            arrow=True,
        )
    )

    # ── five-gate cascade ──
    for idx, gate in enumerate(_GATES):
        y = IN(gate["y"])
        h = IN(gate["h"])

        out.append(
            text_box(
                n(),
                f"{gate['number']} label",
                _LABEL_X,
                y,
                _LABEL_W,
                h,
                _gate_label_paragraph(gate["number"], gate["name"], gate["label_color"]),
                fill=gate["label_fill"],
                line_color=DK,
                line_width=_MAJOR_LINE_W if idx == 1 else _ROW_LINE_W,
                anchor="ctr",
            )
        )

        out.append(
            text_box(
                n(),
                f"{gate['number']} criterion",
                _READ_X,
                y,
                _READ_W,
                h,
                [
                    paragraph(
                        [
                            run(f"{gate['read_label']}: ", size=PT(8.3), bold=True, color=gate["read_color"], font=FONT),
                            run(gate["read"], size=PT(8.3), color=gate["read_color"], font=FONT),
                        ],
                        line_spacing=100000,
                    )
                ],
                fill=gate["read_fill"],
                line_color=DK,
                line_width=_MAJOR_LINE_W if idx == 1 else _ROW_LINE_W,
                anchor="ctr",
            )
        )

        verdict_runs = [
            run(gate["verdict_label"], size=PT(8.3), bold=True, color=gate["verdict_color"], font=FONT),
            run(" " + gate["verdict"].split("\n")[0], size=PT(8.3), color=gate["verdict_color"], font=FONT),
        ]
        if "\n" in gate["verdict"]:
            verdict_runs.extend(
                [
                    line_break(),
                    run(gate["verdict"].split("\n")[1], size=PT(8.3), bold=True, color=gate["verdict_color"], font=FONT),
                ]
            )

        out.append(
            text_box(
                n(),
                f"{gate['number']} verdict",
                _VERDICT_X,
                y,
                _VERDICT_W,
                h,
                [paragraph(verdict_runs, line_spacing=100000)],
                fill=gate["verdict_fill"],
                line_color=DK,
                line_width=_MAJOR_LINE_W if idx == 1 else _ROW_LINE_W,
                anchor="ctr",
            )
        )

        # Gate 1 flows first into the focal waypoint; the remaining gates stack.
        if idx == 0:
            out.append(
                connector(
                    n(),
                    "Cascade arrow to waypoint",
                    IN(4.97),
                    IN(2.91),
                    IN(0),
                    IN(0.05),
                    color=DK,
                    width=_MAJOR_LINE_W,
                    arrow=True,
                )
            )
        elif idx < len(_GATES) - 1:
            next_y = _GATES[idx + 1]["y"]
            gap = next_y - (gate["y"] + gate["h"])
            out.append(
                connector(
                    n(),
                    f"Cascade arrow {idx}",
                    IN(4.97),
                    IN(gate["y"] + gate["h"]),
                    IN(0),
                    IN(gap),
                    color=BLUE_3 if idx == 1 else DK,
                    width=_MAJOR_LINE_W,
                    arrow=True,
                )
            )

    # ── focal waypoint between demand and access ──
    out.append(
        text_box(
            n(),
            "Addressable market waypoint",
            _MAIN_X,
            IN(2.96),
            _MAIN_W,
            IN(0.32),
            [
                paragraph(
                    [
                        run("ADDRESSABLE MARKET  |  ", size=PT(9), bold=True, color=BLACK, font=FONT),
                        run("Real, in-scope, committed demand—the denominator and first focal stop.", size=PT(8.5), color=BLACK, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=BLUE_2,
            line_color=DK,
            line_width=_MAJOR_LINE_W,
            anchor="ctr",
        )
    )
    out.append(
        connector(
            n(),
            "Waypoint to access",
            IN(4.97),
            IN(3.28),
            IN(0),
            IN(0.05),
            color=BLUE_3,
            width=_MAJOR_LINE_W,
            arrow=True,
        )
    )

    # Gate 5 flows into the route-payoff band.
    out.append(
        connector(
            n(),
            "Cascade arrow to routes",
            IN(4.97),
            IN(5.57),
            IN(0),
            IN(0.05),
            color=BLUE_4,
            width=_MAJOR_LINE_W,
            arrow=True,
        )
    )

    # ── focal payoff: route leaves ──
    out.append(
        text_box(
            n(),
            "Routes to revenue header",
            _MAIN_X,
            IN(5.62),
            _MAIN_W,
            IN(0.27),
            [
                paragraph(
                    [
                        run("ROUTES TO REVENUE  |  ", size=PT(9), bold=True, color=WHITE, font=FONT),
                        run("The surviving access posture names the route—not a binary bid / no-bid answer.", size=PT(8.2), color=WHITE, font=FONT),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=BLUE_4,
            line_color=DK,
            line_width=_MAJOR_LINE_W,
            anchor="ctr",
        )
    )

    # Short arrows make the header read as a branch into four terminal routes.
    for route in _ROUTES:
        _route_center = IN(route["x"] + (_ROUTE_W / 2))
        out.append(
            connector(
                n(),
                "Route branch arrow",
                _route_center,
                IN(5.89),
                IN(0),
                IN(0.07),
                color=BLUE_4,
                width=_ROW_LINE_W,
                arrow=True,
            )
        )

    for route in _ROUTES:
        x = IN(route["x"])
        out.append(
            text_box(
                n(),
                f"{route['route']} posture",
                x,
                IN(5.96),
                IN(_ROUTE_W),
                IN(0.22),
                [
                    paragraph(
                        [run(route["tag"], size=PT(7.1), bold=True, color=route["tag_color"], font=FONT)],
                        align="ctr",
                        line_spacing=100000,
                    )
                ],
                fill=route["fill"],
                line_color=DK,
                line_width=_ROW_LINE_W,
                anchor="ctr",
            )
        )
        out.append(
            text_box(
                n(),
                f"{route['route']} card",
                x,
                IN(6.18),
                IN(_ROUTE_W),
                IN(0.48),
                [
                    paragraph(
                        [
                            run(route["route"], size=PT(8.8), bold=True, color=BLACK, font=FONT),
                            line_break(),
                            run(route["detail"], size=PT(7.4), italic=True, color=BLACK, font=FONT),
                        ],
                        align="ctr",
                        line_spacing=95000,
                    )
                ],
                fill=WHITE,
                line_color=DK,
                line_width=_ROW_LINE_W,
                anchor="ctr",
            )
        )

    # ── portal-visibility overlay: explicitly outside the gate logic ──
    out.append(
        text_box(
            n(),
            "Portal visibility overlay",
            _MAIN_X,
            IN(6.73),
            _MAIN_W,
            IN(0.26),
            [
                paragraph(
                    [
                        run("PORTAL VISIBILITY IS NOT A GATE  |  ", size=PT(7.5), bold=True, color=BLACK, font=FONT),
                        run(
                            "Most addressable awards were found in Contract Awards / USAspending / FPDS—not SAM.gov Contract Opportunities.",
                            size=PT(7.5),
                            color=BLACK,
                            font=FONT,
                        ),
                    ],
                    align="ctr",
                    line_spacing=100000,
                )
            ],
            fill=GRAY_1,
            line_color=DK,
            line_width=_ROW_LINE_W,
            dashed_line=True,
            anchor="ctr",
        )
    )

    # ── right-rail commentary ──
    out.append(
        text_box(
            n(),
            "Right rail header",
            _RAIL_X,
            IN(1.33),
            _RAIL_W,
            IN(0.27),
            [paragraph([run("HOW TO READ THE CASCADE", size=PT(10), bold=True, color=BLACK, font=FONT)])],
            fill=None,
            line_color="none",
            anchor="ctr",
        )
    )
    out.append(
        connector(
            n(),
            "Right rail header rule",
            _RAIL_X,
            IN(1.61),
            _RAIL_W,
            IN(0),
            color=DK,
            width=_MAJOR_LINE_W,
        )
    )
    out.append(
        text_box(
            n(),
            "Finding",
            _RAIL_X,
            IN(1.72),
            _RAIL_W,
            IN(1.04),
            [
                paragraph(
                    [
                        run(
                            "A large award is a posture to classify—not an opportunity. Walk the gates; the gate it fails as prime names the route in.",
                            size=PT(10),
                            bold=True,
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    line_spacing=100000,
                )
            ],
            fill="CEDDEC",
            line_color=DK,
            line_width=_MAJOR_LINE_W,
            anchor="ctr",
        )
    )
    out.append(
        text_box(
            n(),
            "Supporting commentary",
            _RAIL_X,
            IN(2.92),
            _RAIL_W,
            IN(2.95),
            [
                paragraph(
                    [
                        run("Upper gates are hard data", size=PT(8.8), bold=True, color=BLACK, font=FONT),
                        run("—object type, obligations vs. ceiling and extent of competition decide quickly.", size=PT(8.8), color=BLACK, font=FONT),
                    ],
                    bullet=True,
                    mar_l=171450,
                    indent=-171450,
                    line_spacing=100000,
                ),
                paragraph(
                    [
                        run("Timing and ability to perform", size=PT(8.8), bold=True, color=BLACK, font=FONT),
                        run(" are judgment, where the analyst adds value.", size=PT(8.8), color=BLACK, font=FONT),
                    ],
                    bullet=True,
                    mar_l=171450,
                    indent=-171450,
                    line_spacing=100000,
                ),
                paragraph(
                    [
                        run("The decision is route, not bid / no-bid:", size=PT(8.8), bold=True, color=BLACK, font=FONT),
                        run(" prime, on-ramp, team below a holder, or join the innovation path.", size=PT(8.8), color=BLACK, font=FONT),
                    ],
                    bullet=True,
                    mar_l=171450,
                    indent=-171450,
                    line_spacing=100000,
                ),
                paragraph(
                    [
                        run("Closed prime ≠ closed market:", size=PT(8.8), bold=True, color=BLACK, font=FONT),
                        run(" AP / LLTM, EOQ and subcontract demand release below the prime.", size=PT(8.8), color=BLACK, font=FONT),
                    ],
                    bullet=True,
                    mar_l=171450,
                    indent=-171450,
                    line_spacing=100000,
                ),
                paragraph(
                    [
                        run("Award data is evidence, not certainty:", size=PT(8.8), bold=True, color=BLACK, font=FONT),
                        run(" records lag and lower tiers are incomplete.", size=PT(8.8), color=BLACK, font=FONT),
                    ],
                    bullet=True,
                    mar_l=171450,
                    indent=-171450,
                    line_spacing=100000,
                ),
            ],
            fill=None,
            line_color="none",
        )
    )
    out.append(
        text_box(
            n(),
            "Guardrails",
            _RAIL_X,
            IN(6.03),
            _RAIL_W,
            IN(0.96),
            [
                paragraph([run("GUARDRAILS", size=PT(8), bold=True, color=BLACK, font=FONT)], line_spacing=100000),
                paragraph(
                    [
                        run(
                            "IDV ≠ IDIQ · single-award ≠ sole-source · ceiling ≠ demand · option ≠ revenue · modification ≠ new award. Never add a parent ceiling to child-order obligations.",
                            size=PT(7.6),
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    line_spacing=100000,
                ),
            ],
            fill=GRAY_1,
            line_color=DK,
            line_width=_ROW_LINE_W,
        )
    )

    # ── source / authority line ──
    out.append(
        text_box(
            n(),
            "Sources",
            IN(0.495),
            IN(7.08),
            IN(12.3),
            IN(0.30),
            [
                paragraph(
                    [
                        run(
                            "Sources: SAM.gov Contract Awards; USAspending; FPDS; SAM.gov Contract Opportunities. Authorities: FAR 16.5, 17.1–17.2, 9.6, 6.302 / 52.217-8; DFARS 206.001-70, 252.227-7013 / -7014; 15 U.S.C. 638.",
                            size=PT(7),
                            color=BLACK,
                            font=FONT,
                        )
                    ],
                    line_spacing=100000,
                )
            ],
            fill=None,
            line_color="none",
        )
    )

    return "".join(out)


def render() -> str:
    return slide(_body())
