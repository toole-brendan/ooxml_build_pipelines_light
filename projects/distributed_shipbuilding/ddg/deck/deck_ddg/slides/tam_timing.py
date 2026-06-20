"""TAM timing - native stacked column chart showing annual supplier TAM lumpiness."""
from __future__ import annotations
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLUE_2, BLUE_4, GRAY_1,
    BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, CHART_TITLE_10PT,
    VALUE_14PT,
)
from deck_core.charts import column_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Timing"
_TAKEAWAY = "Annual supplier TAM is lumpy, with the FY26 spike driven by AP/LLTM"
_SOURCES = "Sources: U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; DoW DDG-51 contract announcements, July 2022-May 2026; SAM.gov Acquisition Subaward Reporting Public API"
_SIZING_NOTE = "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
_CHART = column_chart(
    mode="stacked",
    categories=["FY22", "FY23", "FY24", "FY25", "FY26", "FY27"],
    # SRT bar palette (docs/chart_conversion_spec.md): AP/LLTM is the FY26 spike
    # driver (the story), so it gets hero navy; BC stream is mid blue context.
    series=[
        {"name": "BC stream", "values": [245.9, 571.9, 416.9, 580.7, 35.5, 341.2], "color": "486D82"},
        {"name": "AP/LLTM stream", "values": [None, None, None, 56.6, 1190.0, None], "color": "1D4D68"},
    ],
    title=None,
    show_legend=True,
    legend_pos="b",
    value_axis_format='"$"#,##0"M"',
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    show_value_labels=True,
    value_label_format='"$"#,##0"M"',
    value_label_size_pt=9,
    cat_label_size_pt=9,
    gap_width=80,
    cat_header="Fiscal year",
)
CHARTS: list[dict] = [_CHART]
def _chart_title(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ChartTitle", x, y, cx, 150_000,
        [paragraph([run("Supplier TAM by fiscal year and stream", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _kpi_callout(sp_id: int, x: int, y: int, cx: int, lead: str, value: str, qualifier: str) -> str:
    return text_box(
        sp_id, "NoFillKPICallout", x, y, cx, 560_000,
        [
            paragraph([run(lead, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], space_after=35),
            paragraph([run(value, size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], space_after=30),
            paragraph([run(qualifier, size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)]),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _fy26_label(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "FY26DirectLabel", x, y, cx, 520_000,
        [
            paragraph([run("FY26 peak", size=LABEL_9PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=25),
            paragraph([run("~$1.23B", size=VALUE_14PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=20),
            paragraph([run("mostly AP/LLTM", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=None,
        line_color=None,
        anchor="ctr",
        insets=INSETS_NONE,
    )
def _sizing_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "SizingNote", x, y, cx, 190_000,
        [paragraph([run(_SIZING_NOTE, size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _body() -> str:
    title_y = BODY_Y + 50_000
    callout_y = BODY_Y + 250_000
    chart_y = BODY_Y + 800_000
    chart_h = 3_210_000
    sizing_y = BODY_B - 220_000
    callout_w = 2_790_000
    callout_gap = 260_000
    callout2_x = BODY_X + BODY_CX - callout_w
    callout1_x = callout2_x - callout_gap - callout_w
    fy26_x = BODY_X + int(BODY_CX * 0.705)
    fy26_y = chart_y + 230_000
    return (
        _chart_title(10, BODY_X, title_y, BODY_CX)
        + _kpi_callout(20, callout1_x, callout_y, callout_w, "Average annual convention", "~$573M per year", "useful for market sizing, not a smooth run-rate")
        + _kpi_callout(21, callout2_x, callout_y, callout_w, "FY26 is not the run-rate", "~$1.23B", "driven by AP/LLTM")
        + graphic_frame(sp_id=30, name="TAMTimingStackedColumn", x=BODY_X, y=chart_y, cx=BODY_CX, cy=chart_h, rId="rId2")
        + _fy26_label(40, fy26_x, fy26_y, 1_360_000)
        + _sizing_note(50, BODY_X, sizing_y, BODY_CX)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("TAM Timing", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
