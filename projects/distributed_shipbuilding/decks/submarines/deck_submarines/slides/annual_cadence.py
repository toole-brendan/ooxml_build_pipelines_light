"""Annual Cadence - show lumpy annual TAM and broad SAM output by fiscal year."""
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
    connector,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BLUE_2,
    BLUE_5,
    GRAY_1,
    GRAY_3,
    GRAY_4,
    BLACK,
    FONT,
    INSETS_NONE,
    INSETS_MESSAGE,
    CHART_TITLE_10PT,
    CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT,
    MESSAGE_11PT,
    FINEPRINT_8_5PT,
)
from deck_core.charts import column_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "Annual Cadence"
_TITLE_TOPIC = "Annual Cadence"
_TAKEAWAY = "TAM and broad SAM are lumpy, with FY2024 and FY2027 peaks"
_SOURCES = "Sources: (1) U.S. Department of the Navy SCN Justification Books, Exhibit P-5c; (2) U.S. DoD daily Contracts announcements; (3) SAM.gov FFATA, FSRS, and Entity Management records"
_CHART = column_chart(
    mode="clustered",
    categories=["FY22", "FY23", "FY24", "FY25", "FY26", "FY27"],
    # SRT bar palette (docs/chart_conversion_spec.md): Broad SAM (the addressable
    # subset, the decision-relevant metric) is hero navy; TAM is neutral context.
    series=[
        {"name": "TAM", "values": [1.667, 1.785, 5.403, 1.866, 3.606, 5.514], "color": "79838F"},
        {"name": "Broad SAM", "values": [1.414, 1.514, 4.584, 1.583, 3.060, 4.678], "color": "1D4D68"},
    ],
    title=None,
    show_legend=True,
    legend_pos="b",
    value_axis_format='"$"0.0"B"',
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    show_value_labels=True,
    value_label_format='"$"0.0"B"',
    value_label_size_pt=9,
    cat_label_size_pt=9,
    gap_width=110,
    cat_header="FY",
)
CHARTS = [_CHART]
CONNECTOR_HAIRLINE = 9_525
def _chart_title(sp_id: int, x: int, y: int, cx: int, text: str) -> str:
    return text_box(
        sp_id,
        "ChartTitle",
        x,
        y,
        cx,
        150_000,
        [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _peak_note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, lines: list[str]) -> str:
    paras = [
        paragraph(
            [run(line, size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)],
            align="ctr",
            space_after=30 if idx < len(lines) - 1 else 0,
        )
        for idx, line in enumerate(lines)
    ]
    return text_box(
        sp_id,
        name,
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _guardrail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "AverageAnnualGuardrail",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("Scope note: ", size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT),
                    run("Average annual TAM is ~$3.3B and broad SAM is ~$2.8B, but actual annual flow follows procurement cadence.", size=DENSE_BODY_10PT, color=BLACK, font=FONT),
                ],
                align="ctr",
                space_after=35,
            ),
            paragraph(
                [run("Peaks are procurement-cadence effects, not commercial-style market volatility.", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)],
                align="ctr",
            ),
        ],
        fill=GRAY_1,
        line_color=GRAY_3,
        anchor="ctr",
        insets=INSETS_MESSAGE,
    )
def _body() -> str:
    chart_x = BODY_X
    chart_title_y = BODY_Y + 35_000
    chart_y = BODY_Y + 240_000
    chart_h = 3_430_000
    guardrail_y = BODY_Y + 3_930_000
    guardrail_h = 430_000
    fy24_x = BODY_X + 3_470_000
    fy27_x = BODY_X + 8_720_000
    label_y = chart_y + 75_000
    label_w = 1_900_000
    label_h = 430_000
    return "".join(
        [
            _chart_title(10, chart_x, chart_title_y, BODY_CX, "Annual TAM and broad SAM by fiscal year, $B"),
            graphic_frame(sp_id=20, name="AnnualTAMAndBroadSAMClusteredColumnChart", x=chart_x, y=chart_y, cx=BODY_CX, cy=chart_h, rId="rId2"),
            connector(30, "FY2024CadencePeakLeader", fy24_x + label_w // 2, label_y + label_h, 0, 350_000, color=GRAY_4, width=CONNECTOR_HAIRLINE, arrow=False),
            connector(31, "FY2027CadencePeakLeader", fy27_x + label_w // 2, label_y + label_h, 0, 350_000, color=GRAY_4, width=CONNECTOR_HAIRLINE, arrow=False),
            _peak_note(40, "FY2024CadencePeakAnnotation", fy24_x, label_y, label_w, label_h, ["FY2024 peak", "Both classes contribute Basic Construction"]),
            _peak_note(41, "FY2027CadencePeakAnnotation", fy27_x, label_y, label_w, label_h, ["FY2027 peak", "Two-boat Virginia plus Columbia"]),
            _guardrail(50, BODY_X, guardrail_y, BODY_CX, guardrail_h),
        ]
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
