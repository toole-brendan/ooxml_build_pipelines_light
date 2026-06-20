"""Work-type allocation - ranked bar chart with no-fill interpretation rail."""
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
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_R,
    BODY_B,
    BLUE_1,
    BLUE_3,
    BLUE_4,
    BLUE_5,
    GRAY_1,
    GRAY_3,
    BLACK,
    FONT,
    INSETS_NONE,
    CHART_TITLE_10PT,
    FINEPRINT_8_5PT,
    LABEL_9PT,
    DENSE_BODY_10PT,
)
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Work-Type Allocation"
_TAKEAWAY = "Residual ambiguity remains material, while electrical and structural work are the largest named buckets"
_SOURCES = "Sources: SAM.gov Acquisition Subaward Reporting Public API; FAR 52.204-10; U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122"
# SRT bar palette (docs/chart_conversion_spec.md): residual stays gray
# (evidence ambiguity, de-emphasized); the top named bucket is hero navy and the
# rest walk the blue ramp down to a light-gray tail.
_CHART = column_chart(
    mode="ranked",
    categories=[
        "Unbucketed",
        "Electrical/power",
        "Structural",
        "Machining",
        "Piping/valves",
        "HVAC",
        "Coatings",
        "Castings",
    ],
    series=[
        {
            "name": "Average annual TAM",
            "values": [245.8, 131.8, 101.4, 65.6, 13.0, 9.9, 2.8, 2.7],
            "data_point_colors": ["A1A1A1", "1D4D68", "486D82", "89A2B0", "AFC2CC", "D8E3EB", "BEBEBE", "BEBEBE"],
        }
    ],
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
    cat_header="Work type",
)
CHARTS: list[dict] = [_CHART]
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
def _interpretation_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Residual ambiguity:", "largest line item at ~$246M per year and 42.9% of TAM."),
        ("Largest named lanes:", "electrical and power and structural fabrication are the biggest targetable buckets."),
        ("Core metal lane:", "machining adds a third material named bucket behind electrical and structural."),
        ("Read:", "residual is evidence ambiguity, not a target wedge or zero market."),
    ]
    paras = [paragraph([run("How to read the allocation", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)], space_after=150)]
    for i, (lead, body) in enumerate(bullets):
        paras.append(
            paragraph(
                [
                    run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
                    run(body, size=LABEL_9PT, color=BLACK, font=FONT),
                ],
                bullet=True,
                space_after=140 if i < len(bullets) - 1 else 0,
            )
        )
    return text_box(
        sp_id,
        "InterpretationRail",
        x,
        y,
        cx,
        cy,
        paras,
        fill=None,
        line_color=None,
        anchor="t",
        insets=(70_000, 30_000, 40_000, 30_000),
    )
def _sizing_note(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id,
        "SizingNote",
        x,
        y,
        cx,
        250_000,
        [paragraph([run("Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture.", size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _body() -> str:
    chart_x = BODY_X + 60_000
    chart_w = 7_610_000
    rail_x = chart_x + chart_w + 380_000
    rail_w = BODY_R - rail_x - 70_000
    title_y = BODY_Y + 55_000
    chart_y = title_y + 230_000
    chart_h = 3_760_000
    note_y = BODY_B - 270_000
    return (
        _chart_title(10, chart_x, title_y, chart_w, "Portfolio TAM allocation by work type")
        + graphic_frame(sp_id=20, name="WorkTypeAllocationChart", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2")
        + _interpretation_rail(30, rail_x, chart_y + 260_000, rail_w, 2_620_000)
        + _sizing_note(40, BODY_X, note_y, BODY_CX)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Work-Type Allocation", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
