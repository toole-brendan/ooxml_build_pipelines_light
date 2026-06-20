"""sam_scenarios - Rank overlapping SAM scenarios and make the no-SOM guardrail explicit."""
from __future__ import annotations

from deck_core.charts import column_chart, graphic_frame
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
    BLUE_1,
    BLUE_2,
    BLUE_3,
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_2,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_MESSAGE,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
    CHART_TITLE_10PT,
    MESSAGE_11PT,
)

LAYOUT = "slideLayout4"

_SECTION = "Market Sizing"
_BREADCRUMB_TOPIC = "SAM Scenarios"
_TITLE_TOPIC = "SAM Scenarios"
_TAKEAWAY = "Broad component manufacturing is the largest scenario at ~$2.8B per year"
_SOURCES = "Sources: (1) SAM.gov FFATA/FSRS records; (2) SAM.gov Entity Management API; (3) U.S. Department of the Navy SCN Justification Books"

GAP = 91_440
NOTE_H = 360_000
TITLE_H = 150_000
CHART_TITLE_GAP = 220_000

_CATEGORIES = [
    "Broad components",
    "Electrical/power",
    "Metal components",
    "Modular assy",
    "HM&E",
]
_VALUES = [2805.5, 1257.1, 865.4, 726.0, 679.6]
# SRT bar palette (docs/chart_conversion_spec.md): hero navy + descending blue ramp.
_COLORS = ["1D4D68", "486D82", "89A2B0", "AFC2CC", "D8E3EB"]

_CHART = column_chart(
    mode="ranked",
    categories=_CATEGORIES,
    series=[{"name": "Average annual SAM", "values": _VALUES, "data_point_colors": _COLORS}],
    title=None,
    show_legend=False,
    value_axis_format='"$"#,##0"M"',
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    show_value_labels=True,
    value_label_format='"$"#,##0"M"',
    value_label_size_pt=10,
    cat_label_size_pt=9,
    gap_width=80,
    cat_header="Scenario",
)
CHARTS = [_CHART]

_RAIL_BULLETS: list[tuple[str, str]] = [
    ("Broad:", "all seven buckets, residual excluded - the envelope."),
    ("Electrical:", "the electrical and power bucket alone."),
    ("Metal:", "structural fabrication, machining, and castings and forgings."),
    ("Modular:", "structural fabrication and pre-outfit, with coatings and insulation."),
    ("HM&E:", "piping, valves, pumps, HVAC, and machining (machining also sits in metal)."),
]


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


def _commentary_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    paras = [
        paragraph(
            [run("How to read the scenarios", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)],
            space_after=160,
        )
    ]
    for i, (lead, body) in enumerate(_RAIL_BULLETS):
        paras.append(
            paragraph(
                [
                    run(f"{lead} ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120 if i < len(_RAIL_BULLETS) - 1 else 0,
            )
        )
    return text_box(
        sp_id,
        "ScenarioCommentaryRail",
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(137_160, 80_000, 137_160, 80_000),
    )


def _guardrail(y: int) -> str:
    return text_box(
        40,
        "GuardrailStrip",
        BODY_X,
        y,
        BODY_CX,
        640_000,
        [
            paragraph(
                [
                    run("Scenario SAM only. ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run(
                        "No SOM, share capture, win probability, qualification success, or pricing haircut is modeled.",
                        size=MESSAGE_11PT,
                        color=BLACK,
                        font=FONT,
                    ),
                ],
                align="ctr",
            )
        ],
        fill=GRAY_2,
        line_color=BLACK,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )


def _note() -> str:
    return text_box(
        50,
        "OverlapNote",
        BODY_X,
        BODY_B - NOTE_H,
        BODY_CX,
        NOTE_H,
        [
            paragraph(
                [
                    run(
                        "Scenarios are overlapping cuts of one TAM; do not sum across them. Values are average annual FY2022-FY2027; cumulative shown for context.",
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
    rail_x = chart_x + chart_w + GAP
    rail_w = BODY_R - rail_x
    guardrail_y = BODY_Y + 3_330_000
    chart_h = guardrail_y - chart_y - 120_000
    return (
        _chart_title("SAM scenarios, average annual FY2022-FY2027", chart_x, BODY_Y, chart_w)
        + graphic_frame(sp_id=20, name="SAMScenarioChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2")
        + _commentary_rail(30, rail_x, chart_y, rail_w, chart_h)
        + _guardrail(guardrail_y)
        + _note()
    )


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
