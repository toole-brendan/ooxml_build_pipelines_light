"""FFATA limitations - frame visible first-tier subawards as a floor and evidence layer."""
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
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_B,
    BLUE_1,
    GRAY_1,
    GRAY_2,
    GRAY_5,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    INSETS_CARD,
    INSETS_MESSAGE,
    LABEL_9PT,
    FINEPRINT_8_5PT,
    DENSE_BODY_10PT,
    CHART_TITLE_10PT,
    MESSAGE_11PT,
    VALUE_14PT,
)
from deck_core.text_metrics import estimate_row_heights
LAYOUT = "slideLayout4"
_SECTION = "Appendix"
_TOPIC = "Visibility Gap"
_TAKEAWAY = "Visible first-tier subawards are a floor, not a full market read"
_SOURCES = "Sources: FAR 52.204-10; SAM.gov Acquisition Subaward Reporting Public API; GAO-25-106286"
_BREADCRUMB_TOPIC = "FFATA Limitations"
_TABLE_W = 7_300_000
_RIGHT_X = BODY_X + _TABLE_W + 350_000
_RIGHT_W = BODY_X + BODY_CX - _RIGHT_X
_CAUTION_Y = BODY_Y + 50_000
_TABLE_Y = BODY_Y + 470_000
_ROWS = [
    ["Public-data element", "What it captures", "What remains unseen", "Implication"],
    ["FFATA-reported first-tier subawards", "Direct prime-to-sub subcontracts above threshold", "Lower-tier suppliers and sub-threshold actions", "Evidence layer, not TAM denominator"],
    ["SAM.gov published and deleted records", "FSRS records through SAM.gov API", "Reporting lag and late corrections", "Public access path for FFATA evidence"],
    ["Yard-prime PIID filings", "Visible supplier names and descriptions", "Direct material bookings and standing agreements", "Supports supplier landscape and bucket classification"],
    ["Vendor and description fields", "Bucket evidence for SAM classification", "Incomplete NAICS and UEI resolution", "Use with residual and caveat logic"],
    ["SAM.gov Entity Management enrichment", "Entity names and identifiers", "Parent cleanup and name variants", "Supports supplier aggregation, not perfect parentage"],
    ["USAspending cross-validation", "Secondary public cross-check", "Truncation and timing differences", "QA support only"],
]
_COL_W = [1_790_000, 1_820_000, 1_970_000, 1_720_000]
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.0, header_size_pt=9.0)
_TABLE_H = sum(_ROW_H)
_RANGE_TITLE_Y = _TABLE_Y
_RANGE_CARD_Y = _RANGE_TITLE_Y + 260_000
_RANGE_H = 5 * 500_000 + 4 * 60_000
_LIMITS_Y = min(max(_TABLE_Y + _TABLE_H, _RANGE_CARD_Y + _RANGE_H) + 130_000, BODY_B - 790_000)
# Chart-side evidence ledger -> rule skin (the range chips carry the numbers).
# Only the two encoded columns keep a fill: "what remains unseen" muted GRAY_1,
# "implication" BLUE_1. (Old dark header dropped; first column auto-bolds.)
_CELL_FILLS = {}
for _ri in range(1, len(_ROWS)):
    _CELL_FILLS[(_ri, 2)] = GRAY_1
    _CELL_FILLS[(_ri, 3)] = BLUE_1
def _evidence_table() -> str:
    return house_table(
        20,
        "FFATAEvidenceLedger",
        BODY_X,
        _TABLE_Y,
        _COL_W,
        _ROWS,
        row_h=_ROW_H,
        table_skin="rule",
        aligns=["l", "l", "l", "l"],
        size=LABEL_9PT,
        cell_fills=_CELL_FILLS,
    )
def _range_chip(sp_id: int, y: int, label: str, value: str, *, fill: str, color: str = BLACK) -> str:
    return text_box(
        sp_id,
        "RangeCueValue",
        _RIGHT_X,
        y,
        _RIGHT_W,
        500_000,
        [
            paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=color, font=FONT)], align="l"),
            paragraph([run(value, size=VALUE_14PT, bold=True, color=color, font=FONT)], align="r"),
        ],
        fill=fill,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _range_cue() -> str:
    y = _RANGE_CARD_Y
    return (
        text_box(
            50,
            "RangeCueTitle",
            _RIGHT_X,
            _RANGE_TITLE_Y,
            _RIGHT_W,
            170_000,
            [paragraph([run("Cumulative yard-side view", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
            fill=None,
            line_color=None,
            anchor="t",
            insets=INSETS_NONE,
        )
        + _range_chip(51, y, "FFATA-visible yard-side flow", "~$2.73B cumulative", fill=GRAY_5, color=WHITE)
        + _range_chip(52, y + 560_000, "Estimated outsourcing low", "~$11.31B cumulative", fill=GRAY_1)
        + _range_chip(53, y + 1_120_000, "Estimated outsourcing midpoint", "~$13.57B cumulative", fill=GRAY_2)
        + _range_chip(54, y + 1_680_000, "Estimated outsourcing high", "~$16.16B cumulative", fill=GRAY_1)
        + _range_chip(55, y + 2_240_000, "Visible share at midpoint", "20.1%", fill=BLUE_1)
    )
def _limitations_rail() -> str:
    return text_box(
        80,
        "LimitationsCommentary",
        BODY_X,
        _LIMITS_Y,
        BODY_CX,
        760_000,
        [
            paragraph(
                [run("Coverage: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("Direct material purchases can be booked outside subcontract reporting.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=90,
            ),
            paragraph(
                [run("Tiering: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("A sub's sub is not reportable.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=90,
            ),
            paragraph(
                [run("Reporting: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("The FY23-27 BIW master shows a major reporting gap.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
                space_after=90,
            ),
            paragraph(
                [run("Timing: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT), run("Recent years are still affected by reporting lag.", size=LABEL_9PT, color=BLACK, font=FONT)],
                bullet=True,
            ),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_MESSAGE,
    )
def _body() -> str:
    caution = text_box(
        10,
        "MainCaution",
        BODY_X,
        _CAUTION_Y,
        BODY_CX,
        300_000,
        [
            paragraph(
                [
                    run("FFATA is the observable floor. ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("It supports supplier names, bucket evidence, and concentration, but not the full market denominator.", size=LABEL_9PT, color=BLACK, font=FONT),
                ]
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
    return caution + _evidence_table() + _range_cue() + _limitations_rail()
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
