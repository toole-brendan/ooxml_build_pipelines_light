"""supplier_landscape - Build the ranked visible first-tier supplier landscape slide."""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.charts import bar_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, GRAY_1,
    BLACK, FONT, INSETS_NONE, INSETS_MESSAGE,
    CHART_TITLE_10PT, FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"

_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "Supplier Landscape"
_TAKEAWAY = "Visible supplier flow is concentrated among specialized defense manufacturers"
_SOURCES = "Sources: (1) SAM.gov Acquisition Subaward Reporting Public API; (2) SAM.gov Entity Management API; (3) FAR 52.204-10"

GAP = 91_440
TITLE_H = 160_000
TITLE_GAP = 70_000
NOTE_H = 370_000

_CATEGORIES = [
    "Leonardo SpA",
    "Arctic Slope Regional Corp",
    "Major Tool and Machine",
    "General Dynamics Corp",
    "General Electric Co",
    "Rolls-Royce Holdings plc",
    "Northrop Grumman Corp",
    "Johnson Controls Navy Systems",
    "Advanced Sciences and Technologies",
    "CAES Systems LLC",
]
_VALUES = [1810.3, 987.4, 816.1, 372.0, 335.6, 257.2, 249.3, 178.2, 174.0, 169.2]

_CHART = bar_chart(
    mode="ranked",
    categories=_CATEGORIES,
    series=[{"name": "Lifetime visible flow", "values": _VALUES,
             # SRT bar palette (docs/chart_conversion_spec.md): top supplier hero
             # navy, blue ramp down, neutral gray-blue tail. Kept horizontal -
             # 10 long supplier names do not fit a vertical column axis.
             "data_point_colors": ["1D4D68", "486D82", "486D82", "89A2B0", "89A2B0", "AFC2CC", "AFC2CC", "79838F", "79838F", "79838F"]}],
    title=None,
    show_legend=False,
    value_axis_format='"$"#,##0"M"',
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    show_value_labels=True,
    value_label_format='"$"#,##0"M"',
    value_label_size_pt=9,
    cat_label_size_pt=9,
    gap_width=40,
    cat_header="Supplier parent",
)
CHARTS = [_CHART]


def _chart_title(text: str, x: int, y: int, cx: int, *, sp_id: int) -> str:
    return text_box(sp_id, "ChartTitle", x, y, cx, TITLE_H,
                    [paragraph([run(text, size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
                    fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _caveat_rail(sp_id: int, x: int, y: int, cx: int, cy: int) -> str:
    bullets = [
        ("Visible only:", "first-tier FFATA flow, not the full true market."),
        ("Mixed roles:", "some parent names blend product, service, and prime-related activity."),
        ("Aggregate parents:", "clean duplicate name variants; avoid bucket-split rows."),
    ]
    paras = [paragraph([run("Caveats", size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)], space_after=170)]
    for i, (lead, body) in enumerate(bullets):
        paras.append(paragraph([
            run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run(body, size=LABEL_9PT, color=BLACK, font=FONT),
        ], bullet=True, space_after=120 if i < len(bullets) - 1 else 0))
    return text_box(sp_id, "CaveatRail", x, y, cx, cy, paras, fill=None, line_color=None,
                    anchor="t", insets=INSETS_MESSAGE)


def _body() -> str:
    chart_w = int(BODY_CX * 0.68)
    chart_x = BODY_X
    title_y = BODY_Y
    frame_y = BODY_Y + TITLE_H + TITLE_GAP
    note_y = BODY_B - NOTE_H
    frame_h = note_y - frame_y - 80_000
    rail_x = chart_x + chart_w + GAP
    rail_w = BODY_X + BODY_CX - rail_x

    title = _chart_title("Top visible first-tier suppliers by lifetime flow, $M", chart_x, title_y, chart_w, sp_id=20)
    chart = graphic_frame(sp_id=21, name="SupplierLandscapeChart", x=chart_x, y=frame_y,
                          cx=chart_w, cy=frame_h, rId="rId2")
    rail = _caveat_rail(22, rail_x, frame_y, rail_w, 1_650_000)
    note = text_box(23, "VisibleFloorNote", BODY_X, note_y, chart_w, NOTE_H,
                    [paragraph([run("Lifetime visible first-tier subaward flow per parent vendor; a floor, not the full supplier base. Names only, no logos.",
                                    size=FINEPRINT_8_5PT, color=BLACK, font=FONT)], align="l")],
                    fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    return title + chart + rail + note


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Supplier Landscape", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
