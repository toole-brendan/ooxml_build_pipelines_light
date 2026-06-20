"""MYP correction - back up the redacted master reconstruction and corrected outside-yards share."""
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
    BLUE_5,
    GRAY_2,
    GRAY_3,
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
_TOPIC = "MYP Correction"
_TAKEAWAY = "The $14.58B redacted masters drive the outside-yards correction"
_SOURCES = (
    "Sources: DoW contract announcements, Aug. 1, Aug. 11, and Sept. 6, 2023; "
    "USNI News, Navy Reveals Contract Costs of Latest 10-Hull Destroyer Deal, Sept. 6, 2023; "
    "NAVSEA, Navy Awards DDG 51 FY23-27 Multiyear Procurement Contracts, Aug. 1, 2023"
)
_BREADCRUMB_TOPIC = "MYP Correction"
_TABLE_W = 7_600_000
_RIGHT_X = BODY_X + _TABLE_W + 270_000
_RIGHT_W = BODY_X + BODY_CX - _RIGHT_X
_TABLE_Y = BODY_Y + 190_000
_ROWS = [
    ["Item", "$M", "POP treatment", "Use in model", "Note"],
    ["BIW FY23-27 MYP master", "6,400", "Bath 69% plus supplier sites", "Reconstructed from public reporting and POP paragraph", "Yard-heavy master"],
    ["Ingalls FY23-27 MYP master", "8,180", "Pascagoula 77% to 79%", "Reconstructed from public reporting and POP paragraph", "Yard-heavy master"],
    ["Combined masters", "14,580", "yard-heavy", "67.2% of gated corpus", "Too large to omit"],
    ["Gated corpus with masters", "21,712", "all gated", "denominator for correction", "Corpus used for corrected POP"],
    ["Corrected outside-yards", "n.a.", "32.8%", "other-US plus foreign", "Use forward"],
    ["Disclosed artifact", "n.a.", "73.6%", "guardrail only", "Do not headline"],
]
_COL_W = [2_150_000, 1_000_000, 1_600_000, 1_800_000, 1_050_000]
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.0, header_size_pt=9.0)
_TABLE_H = sum(_ROW_H)
_SENS_Y = min(_TABLE_Y + _TABLE_H + 135_000, BODY_B - 1_300_000)
_GUARD_Y = min(_SENS_Y + 610_000, BODY_B - 680_000)
# Supporting reconstruction table -> rule skin (the comparison bars carry the
# headline). Emphasis rows kept via cell maps: "Combined masters" (3) and
# "Corrected outside-yards" (5) BLUE_1 + bold; "Disclosed artifact" (6) muted
# GRAY_2. (Old dark header dropped; first column auto-bolds.)
def _reconstruction_cell_maps():
    cell_fills: dict[tuple[int, int], str] = {}
    cell_bold: dict[tuple[int, int], bool] = {}
    for ri in (3, 5):
        for ci in range(len(_COL_W)):
            cell_fills[(ri, ci)] = BLUE_1
            cell_bold[(ri, ci)] = True
    for ci in range(len(_COL_W)):
        cell_fills[(6, ci)] = GRAY_2
    return cell_fills, cell_bold
def _reconstruction_table() -> str:
    cell_fills, cell_bold = _reconstruction_cell_maps()
    return house_table(
        20,
        "MYPReconstructionTable",
        BODY_X,
        _TABLE_Y,
        _COL_W,
        _ROWS,
        row_h=_ROW_H,
        table_skin="rule",
        aligns=["l", "r", "l", "l", "l"],
        size=LABEL_9PT,
        cell_fills=cell_fills,
        cell_bold=cell_bold,
    )
def _comparison_bar(sp_id: int, x: int, y: int, cx: int, label: str, value: str, *, fill: str, color: str, line_w: int) -> str:
    return text_box(
        sp_id,
        "OutsideYardsBar",
        x,
        y,
        cx,
        560_000,
        [
            paragraph([run(label, size=LABEL_9PT, bold=True, color=color, font=FONT)], align="l"),
            paragraph([run(value, size=VALUE_14PT, bold=True, color=color, font=FONT)], align="r"),
        ],
        fill=fill,
        line_width=line_w,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _bar_comparison() -> str:
    x, w = _RIGHT_X, _RIGHT_W
    title = text_box(
        60,
        "ComparisonTitle",
        x,
        BODY_Y + 190_000,
        w,
        155_000,
        [paragraph([run("Outside-yards share", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
    max_w = w - 290_000
    corrected_w = int(max_w * 32.8 / 73.6)
    bars = (
        _comparison_bar(61, x, BODY_Y + 560_000, max_w, "Disclosed artifact", "73.6%", fill=GRAY_3, color=BLACK, line_w=12_700)
        + _comparison_bar(62, x, BODY_Y + 1_480_000, corrected_w, "MYP-corrected", "32.8%", fill=BLUE_5, color=WHITE, line_w=19_050)
        + text_box(
            63,
            "CorrectedUseForwardLabel",
            x + corrected_w + 90_000,
            BODY_Y + 1_590_000,
            w - corrected_w - 90_000,
            280_000,
            [paragraph([run("use forward", size=LABEL_9PT, italic=True, color=BLACK, font=FONT)])],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=INSETS_NONE,
        )
    )
    return title + bars
def _sensitivity_strip() -> str:
    return text_box(
        80,
        "SensitivityMiniRow",
        BODY_X,
        _SENS_Y,
        BODY_CX,
        500_000,
        [
            paragraph(
                [
                    run("Portfolio TAM: ", size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT),
                    run("~$3.44B corrected versus ~$2.13B disclosed-only; MYP reconstruction uplift is ~$1.31B.", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                ],
                align="ctr",
            )
        ],
        fill=BLUE_1,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )
def _guardrail_note() -> str:
    return text_box(
        90,
        "GuardrailCommentary",
        BODY_X,
        _GUARD_Y,
        BODY_CX,
        650_000,
        [
            paragraph(
                [
                    run("Guardrail: ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(
                        "Corrected distribution is BIW 29.0%, Ingalls 33.6%, Other-US 31.5%, Foreign 1.3%, and Unparsed 4.5%. The applied BC supplier coefficient is lower because it is measured on the non-GFE BC corpus, not the all-gated corpus.",
                        size=LABEL_9PT,
                        color=BLACK,
                        font=FONT,
                    ),
                ]
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _body() -> str:
    return _reconstruction_table() + _bar_comparison() + _sensitivity_strip() + _guardrail_note()
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
