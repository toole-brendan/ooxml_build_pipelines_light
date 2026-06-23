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


_DOT = _i(0.18)          # numbered-step circle diameter
_STEP_GAP = _i(0.055)    # clears role-band labels before docking above nodes
_STEP_INSET = _i(0.10)   # consistent circle inset from each target node's left edge
_STEP_VERB_GAP = _i(0.035)
_STEP_VERB_W = _i(0.82)  # wide enough for RESOLVE / VALIDATE without drifting


# Source x role x best-answers x caveat x output reference. Kept at module scope
# (reusable) for a backup/appendix slide; the main slide renders the flow diagram
# as the hero and does NOT draw this table.
_SOURCE_REFERENCE_ROWS = [
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


def _step(
    sp_id: int,
    number: int,
    verb: str,
    x: int,
    y: int,
    *,
    dark: bool = False,
    label_w: int = _STEP_VERB_W,
) -> str:
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
            [paragraph([run(str(number), size=700, bold=True, color=WHITE, font=FONT)],
                       align="ctr", line_spacing=100_000)],
            fill=fill,
            line_color=BLACK,
            anchor="ctr",
            insets=INSETS_NONE,
            prst="ellipse",
        )
        + text_box(
            sp_id + 1,
            f"Verb{number}",
            x + dot + _STEP_VERB_GAP,
            y,
            label_w,
            dot,
            [paragraph(
                [run(verb, size=800, bold=True, color=BLACK, font=FONT)],
                align="l",
                line_spacing=100_000,
            )],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=INSETS_NONE,
            wrap="none",
        )
    )


def _step_above_node(
    sp_id: int,
    number: int,
    verb: str,
    node_x: int,
    node_y: int,
    *,
    inset: int = _STEP_INSET,
    dark: bool = False,
    label_w: int = _STEP_VERB_W,
) -> str:
    """Place a numbered step consistently above the node it describes."""
    return _step(
        sp_id,
        number,
        verb,
        node_x + inset,
        node_y - _DOT - _STEP_GAP,
        dark=dark,
        label_w=label_w,
    )


def _body() -> str:
    parts: list[str] = []

    # Body allocation: operating model (the hero) + the validation rail. The
    # source-role table no longer renders here; it lives at module scope in
    # _SOURCE_REFERENCE_ROWS for a backup/appendix slide.
    flow_h = _i(1.79)
    rail_h = _i(0.58)
    rail_y = BODY_B - rail_h

    # Center the flow block vertically in the region above the rail so dropping the
    # source-role table leaves balanced margins, not one white band in the middle.
    # Every diagram element is offset from flow_y, so this shifts the whole flow.
    flow_y = BODY_Y + ((rail_y - BODY_Y) - flow_h) // 2

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
    # Drop the source row slightly so badges clear the role-band labels.
    # All step circles use the same left inset from their target node, so the
    # numbered circles no longer appear to drift.
    source_y = flow_y + _i(0.405)
    source_h = _i(0.335)
    card_y = flow_y + _i(0.785)
    card_h = _i(0.395)
    source_w = _i(1.12)
    comment_w = _i(1.55)   # comment cards grow into the empty column beside them
    source_x = [BODY_X + _i(v) for v in (2.78, 4.00, 5.22, 6.44)]
    step_verbs = ("ADD", "LINK", "PULL", "RESOLVE")
    for idx, (sx, verb) in enumerate(zip(source_x, step_verbs), start=3):
        parts.append(_step_above_node(20 + (idx - 3) * 2, idx, verb, sx, source_y))

    parts.extend(
        [
            _box(28, "USAspending", source_x[0], source_y, source_w, source_h,
                 "USASPENDING", "FY obligations, TAS",
                 fill=BLUE_2, title_size=750, body_size=650,
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(29, "VehicleFamilies", source_x[1], source_y, source_w, source_h,
                 "VEHICLE FAMILY", "Parent/child orders",
                 fill=BLUE_1, title_size=750, body_size=650,
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(30, "Subawards", source_x[2], source_y, source_w, source_h,
                 "SAM SUBAWARDS", "First-tier suppliers",
                 fill=BLUE_2, title_size=750, body_size=650,
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(31, "EntityManagement", source_x[3], source_y, source_w, source_h,
                 "SAM ENTITY", "UEI / CAGE / NAICS",
                 fill=BLUE_1, title_size=750, body_size=650,
                 insets=(40_000, 18_000, 40_000, 18_000)),
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
    spine_y = flow_y + _i(1.20)
    spine_h = _i(0.34)
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
            _step_above_node(42, 1, "DEFINE", define_x, spine_y),
            _step_above_node(44, 2, "PULL", spine_x, spine_y),
            connector(46, "DefineToSpine", define_x + define_w, spine_y + spine_h // 2,
                      spine_x - (define_x + define_w), 0, width=9_525, arrow=True),
        ]
    )

    # Mandatory validation gate - the single dark focal object.
    gate_x = BODY_X + _i(7.72)
    gate_y = flow_y + _i(0.760)
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
                    paragraph([run("VALIDATION", size=1325, bold=True, color=WHITE, font=FONT)],
                              align="ctr", line_spacing=95_000),
                    paragraph([run("GATE", size=1500, bold=True, color=WHITE, font=FONT)],
                              align="ctr", line_spacing=95_000),
                    paragraph([run("Tag source, vintage, measure, family and confidence",
                                           size=560, color=WHITE, font=FONT)],
                              align="ctr", line_spacing=100_000),
                ],
                fill=BLUE_5,
                line_color=BLACK,
                line_width=19_050,
                anchor="ctr",
                insets=(45_000, 22_000, 45_000, 18_000),
            ),
            _step_above_node(48, 7, "VALIDATE", gate_x, gate_y,
                             inset=_i(0.12), dark=True),
            connector(50, "SpineToGate", spine_x + spine_w, spine_y + spine_h // 2,
                      gate_x - (spine_x + spine_w), 0, width=12_700, arrow=True),
        ]
    )

    # Dashed legacy validation tap below the spine.
    fpds_x = BODY_X + _i(4.72)
    fpds_y = flow_y + _i(1.55)
    fpds_w = _i(2.70)
    fpds_h = _i(0.22)
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
    external_h = _i(0.47)
    parts.extend(
        [
            _box(53, "ExternalProgramEvidence", output_x, external_y, output_w, external_h,
                 "EXTERNAL PROGRAM EVIDENCE",
                 "End-user, low confidence. Payer, buyer and user often differ; place of performance is not proof.",
                 fill=None, title_color=GRAY_4, body_color=GRAY_4,
                 title_size=750, body_size=650, dashed=True,
                 line_color=BLACK, line_width=12_700, align="l", anchor="t",
                 insets=(40_000, 18_000, 40_000, 18_000)),
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
    chip_y = [flow_y + _i(v) for v in (0.69, 1.03, 1.36)]
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
                 fill=BLUE_2, title_size=750, body_size=650, align="l",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(59, "OpportunityOutput", chip_x, chip_y[1], output_w, chip_h,
                 "OPPORTUNITY MAP", "SAM Opportunities, vehicles and incumbents",
                 fill=BLUE_1, title_size=750, body_size=650, align="l",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            _box(60, "EndUserOutput", chip_x, chip_y[2], output_w, chip_h,
                 "END-USER READ", "External evidence, confidence-tagged",
                 fill=GRAY_1, title_size=750, body_size=650, align="l",
                 insets=(40_000, 18_000, 40_000, 18_000)),
            connector(61, "BusToMarket", bus_x, chip_y[0] + chip_h // 2,
                      chip_x - bus_x, 0, width=6_350, arrow=True),
            connector(62, "BusToOpportunity", bus_x, chip_y[1] + chip_h // 2,
                      chip_x - bus_x, 0, width=6_350, arrow=True),
            connector(63, "BusToEndUser", bus_x, chip_y[2] + chip_h // 2,
                      chip_x - bus_x, 0, width=6_350, arrow=True),
        ]
    )

    # (Source-role reference table removed from this slide; the flow is the hero.
    # See _SOURCE_REFERENCE_ROWS at module scope for the backup/appendix slide.)

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
    rail_insets = (_i(0.10), _i(0.045), _i(0.08), _i(0.03))
    parts.append(
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
        )
    )

    # Fewer, non-duplicative rules. The reconcile / roll-vehicle-and-child /
    # tag-source-date-measure rules are already carried by the diagram's comment
    # cards and the validation gate, so they are dropped here.
    rail_rules = [
        "Normalize IDs by source",
        "Validate returned filters before totals",
        "Sum action obligations, not cumulative snapshots",
        "Keep money universes separate",
    ]
    rule_w = (BODY_CX - left_w) // len(rail_rules)
    cursor = BODY_X + left_w
    for idx, rule_copy in enumerate(rail_rules):
        width = BODY_X + BODY_CX - cursor if idx == len(rail_rules) - 1 else rule_w
        parts.append(text_box(
            73 + idx,
            f"ValidationRailRule{idx + 1}",
            cursor,
            rail_y,
            width,
            rail_h,
            [paragraph([run(rule_copy, size=775, bold=(idx in (2, 3)),
                            color=BLACK, font=FONT)], align="ctr", line_spacing=105_000)],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=rail_insets,
        ))
        cursor += width

    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
