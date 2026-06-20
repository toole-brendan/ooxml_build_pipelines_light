"""sib_exclusion - Show material SIB capacity-development pass-throughs and why they stay outside component TAM and SAM."""
from __future__ import annotations

from deck_core.charts import waterfall_chart, graphic_frame
from deck_core.primitives import (
    slide,
    breadcrumb,
    title_placeholder,
    prelim_chip,
    sources_line,
    run,
    paragraph,
    text_box,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_R,
    BODY_B,
    GRAY_1,
    GRAY_2,
    GRAY_3,
    GRAY_4,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_MESSAGE,
    FINEPRINT_8_5PT,
    CHART_TITLE_10PT,
    MESSAGE_11PT,
    DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"

_SECTION = "Market Sizing"
_BREADCRUMB_TOPIC = "SIB Exclusion"
_TITLE_TOPIC = "SIB Exclusion"
_TAKEAWAY = "Capacity-development pass-throughs are material but outside component TAM"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) GAO-25-106286"

GAP = 91_440
NOTE_H = 455_000
TITLE_H = 150_000
CHART_TITLE_GAP = 220_000

# Additive exclusion waterfall (decision: waterfall over table): the three
# capacity-development pass-throughs build to the total excluded (~$4,252M).
# SRT bar palette (docs/chart_conversion_spec.md); excluded steps stay gray (not
# hero TAM) and the total pillar is neutral - the point is these are NOT TAM.
_CHART = waterfall_chart(
    steps=[
        {"label": "BlueForge", "value": 4173.3, "kind": "start"},
        {"label": "TMG", "value": 77.0, "kind": "delta"},
        {"label": "IALR", "value": 1.5, "kind": "delta"},
        {"label": "Total excluded", "value": None, "kind": "end"},
    ],
    title=None,
    value_axis_format='"$"#,##0"M"',
    increase_color="A1A1A1",
    decrease_color="A1A1A1",
    total_color="79838F",
    show_value_labels=True,
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    cat_label_size_pt=9,
    cat_header="SIB pass-through",
)
CHARTS = [_CHART]


def _chart_title(text: str, x: int, y: int, cx: int, *, sp_id: int = 10) -> str:
    return text_box(
        sp_id,
        "ChartTitle",
        x,
        y,
        cx,
        TITLE_H,
        [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )


def _treatment_card(x: int, y: int, w: int) -> str:
    return text_box(
        30,
        "TreatmentCard",
        x,
        y,
        w,
        1_430_000,
        [
            paragraph(
                [
                    run("Exclude from component TAM and SAM. ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(
                        "These dollars fund supplier development, workforce, capacity expansion, qualification, and infrastructure rather than current components delivered into a hull.",
                        size=DENSE_BODY_10PT,
                        color=BLACK,
                        font=FONT,
                    ),
                ]
            )
        ],
        fill=GRAY_2,
        line_color=BLACK,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )


def _total_readout(y: int, w: int) -> str:
    return text_box(
        40,
        "ExcludedTotalReadout",
        BODY_X,
        y,
        w,
        330_000,
        [
            paragraph(
                [
                    run("Total excluded SIB pass-throughs: ", size=MESSAGE_11PT, color=BLACK, font=FONT),
                    run("~$4,252M", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                ]
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )


def _terminology_note() -> str:
    return text_box(
        50,
        "TerminologyNote",
        BODY_X,
        BODY_B - NOTE_H,
        BODY_CX,
        NOTE_H,
        [
            paragraph(
                [
                    run(
                        "Deck standardizes on SIB (Submarine Industrial Base); earlier source files may use MIB (Maritime Industrial Base).",
                        size=FINEPRINT_8_5PT,
                        italic=True,
                        color=BLACK,
                        font=FONT,
                    )
                ]
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )


def _body() -> str:
    chart_w = int(BODY_CX * 0.62)
    chart_x = BODY_X
    chart_y = BODY_Y + CHART_TITLE_GAP
    chart_h = 2_280_000
    treatment_x = chart_x + chart_w + GAP
    treatment_w = BODY_R - treatment_x
    total_y = chart_y + chart_h + 140_000
    return (
        _chart_title("SIB capacity-development pass-throughs (excluded from component TAM and SAM)", chart_x, BODY_Y, chart_w)
        + graphic_frame(sp_id=20, name="SIBExclusionChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2")
        + _treatment_card(treatment_x, chart_y, treatment_w)
        + _total_readout(total_y, chart_w)
        + _terminology_note()
    )


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
