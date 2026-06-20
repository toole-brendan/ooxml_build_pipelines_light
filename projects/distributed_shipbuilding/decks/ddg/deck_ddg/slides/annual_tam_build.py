"""Annual TAM build - native editable waterfall bridge plus compact cumulative tie-out."""
from __future__ import annotations
# Implementation note: waterfall_chart uses the shared native stacked-column
# workaround; external labels and the bridge ledger carry the signed values.
from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4,
    BLACK, FONT,
    INSETS_NONE, INSETS_CARD, INSETS_CHIP,
    FINEPRINT_8_5PT, LABEL_9PT, CHART_TITLE_10PT,
    MESSAGE_11PT, CAP_12PT, VALUE_14PT,
)
from deck_core.charts import waterfall_chart, graphic_frame
LAYOUT = "slideLayout4"
_SECTION = "DDG-51 Supplier TAM"
_TOPIC = "TAM Build"
_TAKEAWAY = "The corrected model yields ~$573M per year of supplier TAM"
_SOURCES = "Sources: U.S. Navy FY2022-FY2027 SCN Justification Books, LI 2122; DoW DDG-51 contract announcements, July 2022-May 2026; SAM.gov Acquisition Subaward Reporting Public API"
_SIZING_NOTE = "Nominal $M per year; average annual FY22-27 unless noted. FY22-27 cumulative values shown in parentheses. Excludes SOM and capture."
_CHART = waterfall_chart(
    steps=[
        {"label": "BC base", "value": 2911.8, "kind": "start"},
        {"label": "Less non-supplier", "value": -2546.5, "kind": "delta"},
        {"label": "BC stream", "value": None, "kind": "subtotal"},
        {"label": "AP/LLTM", "value": 207.8, "kind": "delta"},
        {"label": "Portfolio TAM", "value": None, "kind": "end"},
    ],
    title=None,
    value_axis_format='"$"#,##0"M"',
    # SRT bar palette (docs/chart_conversion_spec.md).
    increase_color="486D82",
    decrease_color="A1A1A1",
    total_color="1D4D68",
    show_value_labels=False,
    show_gridlines=True,
    major_gridline_color=GRAY_1,
    major_gridline_width=3_175,
    cat_label_size_pt=9,
    cat_header="Step",
)
CHARTS: list[dict] = [_CHART]
def _chart_title(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "ChartTitle", x, y, cx, 150_000,
        [paragraph([run("Average annual supplier TAM build, FY22-27", size=CHART_TITLE_10PT, italic=True, color=BLACK, font=FONT)])],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _waterfall_label(sp_id: int, x: int, y: int, cx: int, title: str, value: str) -> str:
    return text_box(
        sp_id, "WaterfallStepLabel", x, y, cx, 430_000,
        [
            paragraph([run(title, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=30),
            paragraph([run(value, size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=None,
        line_color=None,
        anchor="t",
        insets=INSETS_NONE,
    )
def _label_strip(sp_id: int, x: int, y: int, cx: int) -> str:
    labels = [
        ("BC base", "~$2,912M per year"),
        ("Less non-supplier", "~-$2,546M per year"),
        ("BC stream", "~$365M per year"),
        ("Add AP/LLTM", "~$208M per year"),
        ("Portfolio TAM", "~$573M per year"),
    ]
    gap = 55_000
    item_w = (cx - (len(labels) - 1) * gap) // len(labels)
    return "".join(
        _waterfall_label(sp_id + i, x + i * (item_w + gap), y, item_w, title, value)
        for i, (title, value) in enumerate(labels)
    )
def _bridge_header(sp_id: int, x: int, y: int, cx: int) -> str:
    return text_box(
        sp_id, "BridgeHeader", x, y, cx, 360_000,
        [paragraph([run("CUMULATIVE BRIDGE, FY22-27", size=CAP_12PT, bold=True, color=BLACK, font=FONT)], align="ctr")],
        fill=GRAY_1,
        anchor="ctr",
        insets=INSETS_CARD,
    )
def _bridge_row(sp_id: int, x: int, y: int, cx: int, label: str, value: str, *, focal: bool = False) -> str:
    label_w = int(cx * 0.63)
    value_w = cx - label_w
    value_size = VALUE_14PT if focal else MESSAGE_11PT
    return (
        text_box(
            sp_id, "BridgeRowLabel", x, y, label_w, 320_000,
            [paragraph([run(label, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)])],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=INSETS_NONE,
        )
        + text_box(
            sp_id + 1, "BridgeRowValue", x + label_w, y, value_w, 320_000,
            [paragraph([run(value, size=value_size, bold=True, color=BLACK, font=FONT)], align="r")],
            fill=None,
            line_color=None,
            anchor="ctr",
            insets=INSETS_NONE,
        )
    )
def _coefficient_chip(sp_id: int, x: int, y: int, cx: int, label: str, value: str, *, fill: str) -> str:
    return text_box(
        sp_id, "CoefficientChip", x, y, cx, 430_000,
        [
            paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT)], align="ctr", space_after=35),
            paragraph([run(value, size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)], align="ctr"),
        ],
        fill=fill,
        anchor="ctr",
        insets=INSETS_CHIP,
    )
def _bridge_block(sp_id: int, x: int, y: int, cx: int) -> str:
    header_h = 360_000
    row_h = 340_000
    rows = [
        ("BC base", "~$17.47B", False),
        ("Removed non-supplier", "~$15.28B", False),
        ("BC stream", "~$2.19B", False),
        ("AP/LLTM stream", "~$1.25B", False),
        ("Portfolio TAM", "~$3.44B", True),
    ]
    parts = [_bridge_header(sp_id, x, y, cx)]
    row_start = y + header_h + 70_000
    for i, (label, value, focal) in enumerate(rows):
        yy = row_start + i * row_h
        parts.append(connector(sp_id + 20 + i, f"BridgeRowRule{i}", x, yy - 25_000, cx, 0, color=GRAY_4, width=6_350))
        parts.append(_bridge_row(sp_id + 2 + i * 2, x, yy, cx, label, value, focal=focal))
    chip_gap = 90_000
    chip_y = row_start + len(rows) * row_h + 110_000
    chip_w = (cx - chip_gap) // 2
    parts.append(_coefficient_chip(sp_id + 40, x, chip_y, chip_w, "BC coefficient", "12.5%", fill=BLUE_1))
    parts.append(_coefficient_chip(sp_id + 41, x + chip_w + chip_gap, chip_y, chip_w, "AP coefficient", "85.0%", fill=GRAY_2))
    return "".join(parts)
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
    chart_x = BODY_X
    chart_w = 7_330_000
    bridge_x = BODY_X + 7_720_000
    bridge_w = BODY_R - bridge_x
    title_y = BODY_Y + 50_000
    chart_y = BODY_Y + 350_000
    chart_h = 2_900_000
    label_y = chart_y + chart_h + 70_000
    bridge_y = chart_y
    sizing_y = BODY_B - 220_000
    return (
        _chart_title(10, chart_x, title_y, chart_w)
        + graphic_frame(sp_id=20, name="AnnualTAMBuildWaterfall", x=chart_x, y=chart_y, cx=chart_w, cy=chart_h, rId="rId2")
        + _label_strip(30, chart_x, label_y, chart_w)
        + _bridge_block(60, bridge_x, bridge_y, bridge_w)
        + _sizing_note(120, BODY_X, sizing_y, BODY_CX)
    )
def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder("Annual TAM Build", _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
