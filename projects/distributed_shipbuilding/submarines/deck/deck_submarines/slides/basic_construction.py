"""Basic Construction - defend the P-5c Basic Construction denominator before applying the supplier coefficient."""
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
    BODY_R,
    BLUE_2,
    BLUE_4,
    GRAY_1,
    GRAY_4,
    BLACK,
    WHITE,
    FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT,
    CHART_TITLE_10PT,
)
from deck_core.charts import column_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "Market Sizing"
_TOPIC = "Budget Denominator"
_TITLE_TOPIC = "Basic Construction"
_TAKEAWAY = "The FY2022-FY2027 denominator averages ~$9.4B annually"
_SOURCES = "Sources: (1) U.S. Department of the Navy FY2022-FY2027 SCN Justification Books, Exhibit P-5c; (2) CRS RL32418; (3) CRS R41129"
# Columbia zero years are retained as numeric zeroes in the embedded workbook;
# their data-label color is set to WHITE so zero labels do not read on-slide.
_CHART = column_chart(
    mode="stacked",
    categories=["FY22", "FY23", "FY24", "FY25", "FY26", "FY27"],
    # SRT bar palette (docs/chart_conversion_spec.md): Virginia (continuous
    # baseline) hero navy, Columbia slate. label_colors keep zero-year labels
    # invisible against the white plot background.
    series=[
        {
            "name": "Virginia",
            "values": [4.758, 5.095, 9.071, 5.327, 3.137, 8.889],
            "color": "1D4D68",
        },
        {
            "name": "Columbia",
            "values": [0.000, 0.000, 6.356, 0.000, 7.160, 6.854],
            "color": "89A2B0",
            "label_colors": [WHITE, WHITE, BLACK, WHITE, BLACK, BLACK],
        },
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
    gap_width=90,
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
def _note(sp_id: int, name: str, x: int, y: int, cx: int, cy: int, lines: list[str]) -> str:
    paras = [
        paragraph(
            [run(line, size=CONNECTOR_NOTE_8_5PT, italic=True, color=BLACK, font=FONT)],
            align="ctr",
            space_after=35 if idx < len(lines) - 1 else 0,
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
def _commentary_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Total:", "FY2022-FY2027 Basic Construction totals ~$56.6B."),
        ("Average:", "the denominator averages ~$9.4B annually across six years."),
        ("Cadence:", "FY2024 and FY2027 are peak years when both classes contribute."),
        ("Scope:", "BC includes yards, team-build work, purchased material, first-tier subs, and lower-tier flow."),
    ]
    paras = [
        paragraph(
            [run("How to read the denominator", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)],
            space_after=160,
        )
    ]
    for idx, (lead, body) in enumerate(bullets):
        paras.append(
            paragraph(
                [
                    run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=120 if idx < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id,
        "DenominatorCommentaryRail",
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(120_000, 80_000, 90_000, 80_000),
    )
def _unit_note(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    return text_box(
        sp_id,
        "UnitScopeNote",
        x,
        y,
        cx,
        cy,
        [
            paragraph(
                [
                    run("AP-only Columbia years contribute no Basic Construction to this denominator. ", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT),
                    run("Average annual BC is a six-year average, not a smooth run-rate.", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT),
                ]
            )
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _body() -> str:
    chart_x = BODY_X
    chart_y = BODY_Y + 260_000
    chart_w = 8_060_000
    chart_h = 3_330_000
    rail_x = BODY_X + chart_w + 300_000
    rail_w = BODY_R - rail_x
    fy24_label_x = chart_x + 2_570_000
    fy27_label_x = chart_x + 6_230_000
    peak_label_y = chart_y + 80_000
    peak_label_w = 1_650_000
    peak_label_h = 410_000
    return "".join(
        [
            _chart_title(10, chart_x, BODY_Y + 40_000, chart_w, "Basic Construction by fiscal year and class, $B"),
            graphic_frame(sp_id=20, name="BasicConstructionStackedColumnChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2"),
            connector(30, "FY2024PeakLeader", fy24_label_x + peak_label_w // 2, peak_label_y + peak_label_h, 0, 340_000, color=GRAY_4, width=CONNECTOR_HAIRLINE, arrow=False),
            connector(31, "FY2027PeakLeader", fy27_label_x + peak_label_w // 2, peak_label_y + peak_label_h, 0, 330_000, color=GRAY_4, width=CONNECTOR_HAIRLINE, arrow=False),
            _note(40, "FY2024PeakAnnotation", fy24_label_x, peak_label_y, peak_label_w, peak_label_h, ["FY2024 peak", "Virginia and Columbia Basic Construction"]),
            _note(41, "FY2027PeakAnnotation", fy27_label_x, peak_label_y, peak_label_w, peak_label_h, ["FY2027 peak", "Two-boat Virginia plus Columbia"]),
            _commentary_rail(50, rail_x, chart_y + 30_000, rail_w, 3_420_000),
            _unit_note(60, chart_x, chart_y + chart_h + 150_000, chart_w + 120_000, 260_000),
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
