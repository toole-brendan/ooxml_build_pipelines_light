"""Contracts award-data sourcing - convert source methodology into one validated operating model."""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
    run,
    paragraph,
    text_box,
    house_table,
    connector,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_CY,
    BODY_B,
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    GRAY_4,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_MICRO_CAP,
    INSETS_MESSAGE,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
    BADGE_16PT,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

_SECTION = "Market Sizing"
_TOPIC = "Award Data Sourcing"               # title topic
_BREADCRUMB_TOPIC = "Sources and Validation"   # breadcrumb second half
_TAKEAWAY = (
    "SAM Contract Awards anchors the pull; funding and subaward layers enrich it, "
    "and validation precedes any total."
)
_SOURCES = (
    "Sources: SAM.gov Contract Awards API; USAspending; SAM Acquisition Subaward Reporting; "
    "SAM Entity Management and Opportunities; President's Budget P-1 / R-1; external program "
    "and operational reporting; FPDS Atom (legacy validation, slated to retire FY2026) | "
    "As of 2026-06-22"
)

_EMU = 914_400


def _i(value: float) -> int:
    return int(round(value * _EMU))


_DOT = _i(0.18)        # numbered-step circle diameter
_STEP_GAP = _i(0.04)   # uniform clearance between each step circle and the node directly below it


def _box(
    sp_id: int,
    name: str,
    x: int,
    y: int,
    cx: int,
    cy: int,
    title: str,
    body: str = "",
    *,
    fill: str | None,
    title_color: str = BLACK,
    body_color: str = BLACK,
    title_size: int = LABEL_9PT,
    body_size: int = FINEPRINT_8_5PT,
    dashed: bool = False,
    line_color: str | None = None,
    line_width: int = 12_700,
    align: str = "ctr",
    anchor: str = "ctr",
    insets=INSETS_MICRO_CAP,
) -> str:
    paras = [
        paragraph(
            [run(title, size=title_size, bold=True, color=title_color, font=FONT)],
            align=align,
            line_spacing=100_000,
        )
    ]
    if body:
        paras.append(
            paragraph(
                [run(body, size=body_size, color=body_color, font=FONT)],
                align=align,
                line_spacing=100_000,
            )
        )
    resolved_line = line_color if line_color is not None else (BLACK if fill not in (None, "none") else None)
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        paras,
        fill=fill,
        line_color=resolved_line,
        line_width=line_width,
        dashed_line=dashed,
        anchor=anchor,
        insets=insets,
    )


def _step(sp_id: int, number: int, verb: str, x: int, y: int, *, dark: bool = False) -> str:
    dot = _DOT
    fill = BLUE_5 if dark else BLUE_3
    return (
        text_box(
            sp_id,
            f"Step{number}",
            x,
            y,
            dot,
            dot,
            [paragraph([run(str(number), size=700, bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100_000)],
            fill=fill,
            line_color=BLACK,
            anchor="ctr",
            insets=INSETS_NONE,
            prst="ellipse",
        )
        + text_box(
            sp_id + 1,
            f"Verb{number}",
            x + dot + _i(0.035),
            y,
            _i(0.58),
            dot,
            [paragraph([run(verb, size=800, bold=True, color=BLACK, font=FONT)])],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=INSETS_NONE,
            wrap="none",
        )
    )


def _body() -> str:
    parts: list[str] = []

    # Body allocation: operating model, source-role legend, validation rail.
    flow_y = BODY_Y
    flow_h = _i(1.79)
    gap = _i(0.04)

    rows = [
        ["Source", "Role in workflow", "Best answers", "Caveat / rule", "Slide output"],
        [
            "President's Budget / justification (P-1, R-1)",
            "Forward funding",
            "Funded by account, PE/BLI, color of money?",
            "Budget lines do not map to NAICS/PSC or vendors",
            "Funded-demand spine",
        ],
        [
            "SAM Contract Awards API",
            "Prime and vehicle pull",
            "Awards/IDVs; parent-child structure; ceilings?",
            "Do not double-count vehicle and child orders; tag coverage",
            "Vehicle, incumbent and capacity map",
        ],
        [
            "USAspending",
            "Budget bridge",
            "Transaction FY obligations; funding TAS?",
            "Reconcile to procurement record; fields differ",
            "TAS bridge and FY view",
        ],
        [
            "SAM Subaward Reporting",
            "First-tier layer",
            "Which reported suppliers sit under a prime?",
            "Lagged/incomplete; separate from prime obligations",
            "Supplier and workshare map",
        ],
        [
            "SAM enrichment sources",
            "Resolve and pipeline",
            "UEI/CAGE/NAICS; what is posted pre-award?",
            "Registration/posting does not prove program relevance or award",
            "Vendor segments and watchlist",
        ],
        [
            "FPDS Atom feed",
            "Legacy validation",
            "What does the older action feed show?",
            "Not the future base; retiring FY2026",
            "Lineage validation",
        ],
        [
            "External program evidence",
            "End-user attribution",
            "Who requires, tests, or fields the capability?",
            "Cite and confidence-tag; place of performance is not proof",
            "End-user map",
        ],
    ]
    col_w = [_i(1.92), _i(1.55), _i(3.00), _i(3.25)]
    col_w.append(BODY_CX - sum(col_w))
    row_h = estimate_row_heights(
        rows,
        col_w,
        size_pt=8.75,
        header_size_pt=8.75,
        min_row_h=_i(0.235),
    )
    table_h = sum(row_h)
    table_y = flow_y + flow_h + gap
    rail_y = table_y + table_h + gap
    rail_h = BODY_B - rail_y

    # Role bands sit behind the entire flow and ramp toward the validation gate.
    pull_w = _i(2.65)
    enrich_w = _i(5.00)
    validate_w = _i(1.55)
    parts.extend(
        [
            text_box(10, "PullBand", BODY_X, flow_y, pull_w, flow_h,
                     [paragraph([])], fill=GRAY_1, line_color="none", insets=INSETS_NONE),
            text_box(11, "EnrichBand", BODY_X + pull_w, flow_y, enrich_w, flow_h,
                     [paragraph([])], fill=BLUE_1, line_color="none", insets=INSETS_NONE),
            text_box(12, "ValidateBand", BODY_X + pull_w + enrich_w, flow_y, validate_w, flow_h,
                     [paragraph([])], fill=BLUE_2, line_color="none", insets=INSETS_NONE),
        ]
    )
    role_y = flow_y + _i(0.01)
    role_h = _i(0.14)
    parts.extend(
        [
            text_box(13, "PullLabel", BODY_X + _i(0.08), role_y, _i(0.65), role_h,
                     [paragraph([run("PULL", size=800, bold=True, color=BLACK, font=FONT)])],
                     fill=None, line_color=None, insets=INSETS_NONE, wrap="none"),
            text_box(14, "EnrichLabel", BODY_X + pull_w + _i(0.08), role_y, _i(0.75), role_h,
                     [paragraph([run("ENRICH", size=800, bold=True, color=BLACK, font=FONT)])],
                     fill=None, line_color=None, insets=INSETS_NONE, wrap="none"),
            text_box(15, "ValidateLabel", BODY_X + pull_w + enrich_w + _i(0.08), role_y,
                     _i(0.88), role_h,
                     [paragraph([run("VALIDATE", size=800, bold=True, color=BLACK, font=FONT)])],
                     fill=None, line_color=None, insets=INSETS_NONE, wrap="none"),
            text_box(16, "OutputsLabel", BODY_X + pull_w + enrich_w + validate_w + _i(0.43),
                     role_y, _i(0.75), role_h,
                     [paragraph([run("OUTPUTS", size=800, bold=True, color=BLACK, font=FONT)])],
                     fill=None, line_color=None, insets=INSETS_NONE, wrap="none"),
        ]
    )

    # Commentary 1: establish the structural spine and subordinate the legacy feed.
    note_x = BODY_X + _i(0.12)
    note_y = flow_y + _i(0.19)
    note_w = _i(2.38)
    note_h = _i(0.74)
    parts.append(
        text_box(
            17,
            "ModernBaseNote",
            note_x,
            note_y,
            note_w,
            note_h,
            [
                paragraph(
                    [run("The modern base pull is SAM Contract Awards, not the FPDS Atom feed.",
                         size=900, bold=True, color=BLACK, font=FONT)],
                    line_spacing=102_000,
                ),
                paragraph(
                    [run("FPDS remains useful for legacy lineage and per-action validation; the "
                         "workflow does not depend on a feed slated to retire in FY2026.",
                         size=750, color=BLACK, font=FONT)],
                    line_spacing=100_000,
                ),
            ],
            fill=None,
            line_color=None,
            anchor="t",
            insets=(0, 0, _i(0.04), 0),
        )
    )

    # Enrichment tributaries and numbered verbs.
    # Lower the source row by _STEP_GAP and shrink its height to hold the bottom edge
    # fixed (0.69) - this opens the step-circle gap without disturbing the cards/spine below.
    source_y = flow_y + _i(0.345)
    source_h = _i(0.345)
    card_y = flow_y + _i(0.73)
    card_h = _i(0.41)
    source_w = _i(1.12)
    comment_w = _i(1.55)   # comment cards grow into the empty column beside them
    source_x = [BODY_X + _i(v) for v in (2.78, 4.00, 5.22, 6.44)]
    step_verbs = ("ADD", "LINK", "PULL", "RESOLVE")
    for idx, (sx, verb) in enumerate(zip(source_x, step_verbs), start=3):
        parts.append(_step(20 + (idx - 3) * 2, idx, verb, sx, source_y - _DOT - _STEP_GAP))

    parts.extend(
        [
            _box(28, "USAspending", source_x[0], source_y, source_w, source_h,
                 "USASPENDING", "FY obligations, TAS",
                 fill=BLUE_2, body_size=725, insets=(40_000, 18_000, 40_000, 18_000)),
            _box(29, "VehicleFamilies", source_x[1], source_y, source_w, source_h,
                 "VEHICLE FAMILY", "Parent/child orders",
                 fill=BLUE_1, body_size=725, insets=(40_000, 18_000, 40_000, 18_000)),
            _box(30, "Subawards", source_x[2], source_y, source_w, source_h,
                 "SAM SUBAWARDS", "First-tier suppliers",
                 fill=BLUE_2, body_size=725, insets=(40_000, 18_000, 40_000, 18_000)),
            _box(31, "EntityManagement", source_x[3], source_y, source_w, source_h,
                 "SAM ENTITY", "UEI / CAGE / NAICS",
                 fill=BLUE_1, body_size=725, insets=(40_000, 18_000, 40_000, 18_000)),
            _box(32, "USAspendingComment", source_x[0], card_y, comment_w, card_h,
                 "BUDGET BRIDGE", "FY obligations and TAS; reconcile to SAM.",
                 fill=BLUE_1, title_size=775, body_size=625, align="l", anchor="t",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(33, "SubawardComment", source_x[2], card_y, comment_w, card_h,
                 "DIFFERENT QUESTION", "Lagged first-tier only; never add to primes.",
                 fill=GRAY_2, title_size=675, body_size=600, align="l", anchor="t",
                 insets=(40_000, 18_000, 40_000, 18_000)),
        ]
    )

    # Tributaries dock directly onto the upper edge of the prime/vehicle spine.
    spine_y = flow_y + _i(1.18)
    spine_h = _i(0.36)
    spine_top = spine_y
    parts.extend(
        [
            connector(34, "USABoxToCard", source_x[0] + source_w // 2,
                      source_y + source_h, 0, card_y - (source_y + source_h),
                      width=6_350),
            connector(35, "USACardToSpine", source_x[0] + source_w // 2,
                      card_y + card_h, 0, spine_top - (card_y + card_h),
                      width=6_350, arrow=True),
            connector(36, "VehicleToSpine", source_x[1] + source_w // 2,
                      source_y + source_h, 0, spine_top - (source_y + source_h),
                      width=6_350, arrow=True),
            connector(37, "SubawardBoxToCard", source_x[2] + source_w // 2,
                      source_y + source_h, 0, card_y - (source_y + source_h),
                      width=6_350),
            connector(38, "SubawardCardToSpine", source_x[2] + source_w // 2,
                      card_y + card_h, 0, spine_top - (card_y + card_h),
                      width=6_350, arrow=True),
            connector(39, "EntityToSpine", source_x[3] + source_w // 2,
                      source_y + source_h, 0, spine_top - (source_y + source_h),
                      width=6_350, arrow=True),
        ]
    )

    # Define and pull the dominant structural spine.
    define_x = BODY_X + _i(0.10)
    define_w = _i(1.18)
    spine_x = BODY_X + _i(1.52)
    spine_w = _i(5.78)
    parts.extend(
        [
            _box(40, "DefineMarketSpine", define_x, spine_y, define_w, spine_h,
                 "PRESIDENT'S BUDGET", "PE/BLI and money color",
                 fill=GRAY_1, title_size=750, body_size=650,
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(41, "SAMContractAwardsSpine", spine_x, spine_y, spine_w, spine_h,
                 "SAM CONTRACT AWARDS", "Primes, IDVs, orders/calls and ceiling",
                 fill=BLUE_3, title_color=WHITE, body_color=WHITE,
                 title_size=LABEL_9PT, body_size=775),
            _step(42, 1, "DEFINE", define_x + _i(0.02), spine_y - _DOT - _STEP_GAP),
            _step(44, 2, "PULL", spine_x + _i(0.02), spine_y - _DOT - _STEP_GAP),
            connector(46, "DefineToSpine", define_x + define_w, spine_y + spine_h // 2,
                      spine_x - (define_x + define_w), 0, width=9_525, arrow=True),
        ]
    )

    # Mandatory validation gate - the single dark focal object.
    gate_x = BODY_X + _i(7.72)
    gate_y = flow_y + _i(0.74)
    gate_w = _i(1.48)
    gate_h = _i(0.96)
    parts.extend(
        [
            text_box(
                47,
                "ValidationGate",
                gate_x,
                gate_y,
                gate_w,
                gate_h,
                [
                    paragraph([run("VALIDATION", size=1400, bold=True, color=WHITE, font=FONT)],
                              align="ctr", line_spacing=95_000),
                    paragraph([run("GATE", size=BADGE_16PT, bold=True, color=WHITE, font=FONT)],
                              align="ctr", line_spacing=95_000),
                    paragraph([run("Tag source, vintage, measure, family and confidence",
                                           size=625, color=WHITE, font=FONT)],
                              align="ctr", line_spacing=100_000),
                ],
                fill=BLUE_5,
                line_color=BLACK,
                line_width=19_050,
                anchor="ctr",
                insets=(45_000, 22_000, 45_000, 18_000),
            ),
            _step(48, 7, "VALIDATE", gate_x + _i(0.14), gate_y - _DOT - _STEP_GAP, dark=True),
            connector(50, "SpineToGate", spine_x + spine_w, spine_y + spine_h // 2,
                      gate_x - (spine_x + spine_w), 0, width=12_700, arrow=True),
        ]
    )

    # Dashed legacy validation tap below the spine.
    fpds_x = BODY_X + _i(4.72)
    fpds_y = flow_y + _i(1.54)
    fpds_w = _i(2.70)
    fpds_h = _i(0.24)
    parts.extend(
        [
            _box(51, "FPDSLegacy", fpds_x, fpds_y, fpds_w, fpds_h,
                 "FPDS ATOM | legacy lineage and validation; retiring FY2026",
                 fill=None, title_color=GRAY_4, title_size=650,
                 dashed=True, line_color=BLACK, line_width=12_700,
                 body_size=650, align="ctr", insets=(35_000, 8_000, 35_000, 8_000)),
            connector(52, "FPDSToGate", fpds_x + fpds_w,
                      fpds_y + fpds_h // 2,
                      gate_x - (fpds_x + fpds_w), 0,
                      width=6_350, dashed=True, arrow=True),
        ]
    )

    # Off-platform evidence also enters the validation gate before any output.
    output_x = BODY_X + _i(9.62)
    output_w = BODY_X + BODY_CX - output_x - _i(0.08)
    external_y = flow_y + _i(0.17)
    external_h = _i(0.44)
    parts.extend(
        [
            _box(53, "ExternalProgramEvidence", output_x, external_y, output_w, external_h,
                 "EXTERNAL PROGRAM EVIDENCE",
                 "End-user, low confidence. Payer, buyer and user often differ; place of performance is not proof.",
                 fill=None, title_color=GRAY_4, body_color=GRAY_4,
                 title_size=775, body_size=650, dashed=True,
                 line_color=BLACK, line_width=12_700, align="l", anchor="t"),
            connector(54, "ExternalEvidenceLeft", output_x,
                      external_y + external_h // 2,
                      (gate_x + gate_w // 2) - output_x, 0,
                      width=6_350, dashed=True),
            connector(55, "ExternalEvidenceDown", gate_x + gate_w // 2,
                      external_y + external_h // 2,
                      0, gate_y - (external_y + external_h // 2),
                      width=6_350, dashed=True, arrow=True),
        ]
    )

    # Outputs fan out from the validation gate through one bus.
    chip_h = _i(0.30)
    chip_y = [flow_y + _i(v) for v in (0.64, 0.98, 1.32)]
    bus_x = BODY_X + _i(9.38)
    chip_x = output_x
    parts.extend(
        [
            connector(56, "GateToOutputBus", gate_x + gate_w,
                      gate_y + gate_h // 2,
                      bus_x - (gate_x + gate_w), 0,
                      width=9_525),
            connector(57, "OutputBus", bus_x, chip_y[0] + chip_h // 2,
                      0, (chip_y[-1] + chip_h // 2) - (chip_y[0] + chip_h // 2),
                      width=9_525),
            _box(58, "MarketOutput", chip_x, chip_y[0], output_w, chip_h,
                 "MARKET SIZE", "Funded-demand spine",
                 fill=BLUE_2, title_size=800, body_size=675, align="l",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(59, "OpportunityOutput", chip_x, chip_y[1], output_w, chip_h,
                 "OPPORTUNITY MAP", "SAM Opportunities, vehicles and incumbents",
                 fill=BLUE_1, title_size=800, body_size=650, align="l",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(60, "EndUserOutput", chip_x, chip_y[2], output_w, chip_h,
                 "END-USER READ", "External evidence, confidence-tagged",
                 fill=GRAY_1, title_size=800, body_size=675, align="l",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            connector(61, "BusToMarket", bus_x, chip_y[0] + chip_h // 2,
                      chip_x - bus_x, 0, width=6_350, arrow=True),
            connector(62, "BusToOpportunity", bus_x, chip_y[1] + chip_h // 2,
                      chip_x - bus_x, 0, width=6_350, arrow=True),
            connector(63, "BusToEndUser", bus_x, chip_y[2] + chip_h // 2,
                      chip_x - bus_x, 0, width=6_350, arrow=True),
        ]
    )

    # Full-width source-role legend. The caveat column reads as caution; the
    # output column reads as payoff. Source cells match the diagram's role colors.
    source_fills = {
        (1, 0): GRAY_1,
        (2, 0): BLUE_3,
        (3, 0): BLUE_2,
        (4, 0): BLUE_2,
        (5, 0): BLUE_1,
        (6, 0): GRAY_2,
        (7, 0): GRAY_1,
    }
    for ri in range(1, len(rows)):
        source_fills[(ri, 3)] = GRAY_1
        source_fills[(ri, 4)] = BLUE_1
    source_text = {(2, 0): WHITE}
    payoff_bold = {(ri, 4): True for ri in range(1, len(rows))}
    parts.append(
        house_table(
            70,
            "SourceRoleLegend",
            BODY_X,
            table_y,
            col_w,
            rows,
            row_h=row_h,
            table_skin="rule",
            aligns=["l", "l", "l", "l", "l"],
            anchor="ctr",
            size=875,  # 8.75pt density exception; visually reads as the 9pt table tier.
            cell_fills=source_fills,
            cell_text_colors=source_text,
            cell_bold=payoff_bold,
        )
    )

    # Validation and limits rail: high contrast, but lighter than the gate.
    parts.append(
        text_box(
            71,
            "ValidationRailBackground",
            BODY_X,
            rail_y,
            BODY_CX,
            rail_h,
            [paragraph([])],
            fill=BLUE_2,
            line_color=BLACK,
            line_width=12_700,
            insets=INSETS_NONE,
        )
    )
    left_w = _i(3.15)
    mid_w = _i(4.55)
    right_w = BODY_CX - left_w - mid_w
    rail_insets = (_i(0.10), _i(0.045), _i(0.08), _i(0.03))
    parts.extend(
        [
            text_box(
                72,
                "ValidationRailFinding",
                BODY_X,
                rail_y,
                left_w,
                rail_h,
                [
                    paragraph([run("VALIDATION IS THE METHOD.", size=950, bold=True,
                                   color=BLACK, font=FONT)], line_spacing=100_000),
                    paragraph([run("Most errors come from mixed money universes or double counting. "
                                   "Award data names the buyer, not the user.",
                                   size=750, color=BLACK, font=FONT)], line_spacing=100_000),
                ],
                fill=None,
                line_color=None,
                anchor="ctr",
                insets=rail_insets,
            ),
            text_box(
                73,
                "ValidationRailRulesA",
                BODY_X + left_w,
                rail_y,
                mid_w,
                rail_h,
                [paragraph([run(
                    "Normalize IDs by source | Validate returned filters | Sum action obligations, "
                    "not cumulative totals | Keep money universes separate",
                    size=775, color=BLACK, font=FONT)], line_spacing=105_000)],
                fill=None,
                line_color=None,
                anchor="ctr",
                insets=rail_insets,
            ),
            text_box(
                74,
                "ValidationRailRulesB",
                BODY_X + left_w + mid_w,
                rail_y,
                right_w,
                rail_h,
                [paragraph([run(
                    "Roll the vehicle and child orders into one family | Reconcile SAM and USAspending | "
                    "Tag source, date, measure, coverage and confidence",
                    size=775, color=BLACK, font=FONT)], line_spacing=105_000)],
                fill=None,
                line_color=None,
                anchor="ctr",
                insets=rail_insets,
            ),
        ]
    )

    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
