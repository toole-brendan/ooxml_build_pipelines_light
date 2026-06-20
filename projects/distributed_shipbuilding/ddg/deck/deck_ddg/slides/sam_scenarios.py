"""sam_scenarios - Build the ranked SAM scenario exhibit and inclusion matrix."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    GRAY_1,
    BLACK, FONT, INSETS_NONE,
    CHART_TITLE_10PT, FINEPRINT_8_5PT, LABEL_9PT,
)

# Sea Range Telemetry chart-bar palette (raw hex, per docs/chart_conversion_spec.md):
# hero navy + descending blue ramp for ranked columns.
_SRT_RAMP = ["1D4D68", "486D82", "89A2B0", "AFC2CC", "D8E3EB"]

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "SAM Scenarios"
_TAKEAWAY = "Broad component manufacturing represents ~$327M per year of serviceable market"
_SOURCES = "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) FAR 52.204-10; (3) U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122"

GAP = 91_440
TITLE_H = 160_000
TITLE_GAP = 70_000
NOTE_H = 370_000

_CATEGORIES = [
    "Broad components",
    "Metal components",
    "Electrical/power",
    "Modular assy",
    "HM&E",
]
_VALUES = [327.3, 169.7, 131.8, 104.3, 88.5]

_CHART = column_chart(
    mode="ranked",
    categories=_CATEGORIES,
    series=[{"name": "Average annual SAM", "values": _VALUES,
             "data_point_colors": _SRT_RAMP}],
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

_ROWS = [
    ["Bucket",      "Metal", "HM&E", "Elec", "Modular", "Broad"],
    ["Structural",  "Yes",   "No",   "No",   "Yes",     "Yes"],
    ["Machining",   "Yes",   "Yes",  "No",   "No",      "Yes"],
    ["Castings",    "Yes",   "No",   "No",   "No",      "Yes"],
    ["Piping",      "No",    "Yes",  "No",   "No",      "Yes"],
    ["Electrical",  "No",    "No",   "Yes",  "No",      "Yes"],
    ["HVAC",        "No",    "Yes",  "No",   "No",      "Yes"],
    ["Coatings",    "No",    "No",   "No",   "Yes",     "Yes"],
]


def _chart_title(text: str, x: int, y: int, cx: int, *, sp_id: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_H,
                    [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
                    fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _ratio_widths(total: int, ratios: list[float]) -> list[int]:
    s = sum(ratios)
    widths = [int(total * r / s) for r in ratios[:-1]]
    widths.append(total - sum(widths))
    return widths


def _body() -> str:
    chart_w = int(BODY_CX * 0.62)
    chart_x = BODY_X
    title_y = BODY_Y
    frame_y = BODY_Y + TITLE_H + TITLE_GAP
    note_y = BODY_B - NOTE_H
    frame_h = note_y - frame_y - 80_000

    matrix_x = chart_x + chart_w + GAP
    matrix_w = BODY_X + BODY_CX - matrix_x
    matrix_col_w = _ratio_widths(matrix_w, [3.4, 1.0, 1.0, 1.0, 1.0, 1.0])
    matrix_row_h = estimate_row_heights(_ROWS, matrix_col_w, size_pt=9.0, header_size_pt=9.0)

    yes_bold = {
        (1, 1): True, (1, 4): True, (1, 5): True,
        (2, 1): True, (2, 2): True, (2, 5): True,
        (3, 1): True, (3, 5): True,
        (4, 2): True, (4, 5): True,
        (5, 3): True, (5, 5): True,
        (6, 2): True, (6, 5): True,
        (7, 4): True, (7, 5): True,
    }

    title = _chart_title("SAM scenarios, average annual FY22-27", chart_x, title_y, chart_w, sp_id=20)
    chart = graphic_frame(sp_id=21, name="SAMScenarioChart", x=chart_x, y=frame_y,
                          cx=chart_w, cy=frame_h, rId="rId2")
    matrix = house_table(22, "ScenarioInclusionMatrix", matrix_x, frame_y, matrix_col_w, _ROWS,
                         row_h=matrix_row_h, table_skin="rule", size=900,
                         aligns=["l", "ctr", "ctr", "ctr", "ctr", "ctr"],
                         cell_bold=yes_bold)
    note = text_box(23, "SizingNote", BODY_X, note_y, BODY_CX, NOTE_H,
                    [paragraph([run("Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture.",
                                    size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="l")],
                    fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    return title + chart + matrix + note


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("SAM Scenarios", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
