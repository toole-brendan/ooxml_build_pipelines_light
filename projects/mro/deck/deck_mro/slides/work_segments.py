"""work_segments - MRO work-segment split (v3.3 slide 6).

The left-side stacked bar is a NATIVE column_chart (single stacked column, six
work-segment segments shown as % share) styled to the think-cell look; it
replaces the earlier static-shape transcription of the source exhibit. The
right-side Work Segment / Coverage table, the chart caption, the column total,
and the footer note are deck_core primitives.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip,
    run, paragraph, text_box, house_table,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    DK, BLACK, FONT, INSETS_NONE, FINEPRINT_8_5PT, SOURCES_8PT,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
    CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6,
)

LAYOUT = "slideLayout4"

_SECTION = "TAM"
_TOPIC = "Work Segments"
_TITLE_TOPIC = "MRO Work Segments"
_TAKEAWAY = ("Depot ship repair and nuclear and complex overhauls captured ~75% of FY2025 MRO TAM.")

_CHART_CAPTION = "FY2025 reconciled FPDS-visible MRO TAM by work segment ($M)"
_FOOTER = ("Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; data as "
           "of April 2026")

_TBL_X, _TBL_Y = 7004304, 1417320
_COL_W = [1691640, 2542032]
_RH = [182880, 603504, 603504, 603504, 603504, 603504, 603504]
_ROWS = [
    ["Work Segment", "Coverage"],
    ["Depot Ship Repair",
     "Whole-ship maintenance availabilities at Pacific and Atlantic Regional Maintenance Centers; "
     "MAC-MO IDIQ task orders"],
    ["Nuclear & Complex Overhauls",
     "PSC 1905 embedded MRO: engineered overhauls, refueling and complex overhauls (RCOH), and "
     "inactivations at SUPSHIP yards (Newport News, GDEB); separate from J998/J999 depot repair"],
    ["Hull, Mechanical & Electrical (HM&E)",
     "Propulsion accessories, pumps, valves, piping, HVAC, diesel engines, and ship structural systems"],
    ["Combat Systems Sustainment",
     "Weapons, fire control, VLS, and guided missiles (including Trident II on Ohio-class SSBNs); "
     "aircraft launch and arresting gear"],
    ["Electronics & C4ISR Sustainment",
     "Afloat C4ISR: radar, sonar, radio and network systems, navigation, alarms, and electrical "
     "signal equipment"],
    ["Port & Technical Services",
     "Quality control, testing, and inspection; OEM technical representation; husbanding (fuel, "
     "transport, port visits); shipyard operations support"],
]

# Native stacked-column reproduction of the v3.3 think-cell exhibit. Single fat
# column; the six segments stack bottom->top in the source's accent order (note
# the deliberate accent5/accent6 swap on the top two). Values are the % shares the
# source labels show; the theme accent hexes equal deck_core CHART_ACCENT_*, so the
# fills are pixel-faithful. Segment names populate only the (hidden) embedded data.
_SEG = [  # (series name, fill, % share, force white in-bar label) — bottom->top
    ("Depot Ship Repair",                    CHART_ACCENT_1, 53, True),
    ("Nuclear & Complex Overhauls",          CHART_ACCENT_2, 21, True),
    ("Hull, Mechanical & Electrical (HM&E)", CHART_ACCENT_3, 10, True),
    ("Combat Systems Sustainment",           CHART_ACCENT_4,  7, True),   # accent4
    ("Port & Technical Services",            CHART_ACCENT_6,  5, False),  # accent6 (swap)
    ("Electronics & C4ISR Sustainment",      CHART_ACCENT_5,  4, False),  # accent5 (swap)
]
_CHART = column_chart(
    mode="stacked",
    categories=["Total FY2025 MRO TAM"],
    series=[{"name": n, "values": [p], "color": c,
             **({"label_color": "FFFFFF"} if w else {})} for (n, c, p, w) in _SEG],
    value_axis_format='0"%"', value_label_format='0"%"',
    value_axis_min=0, value_axis_max=100, value_axis_major_unit=5,
    seg_line_color="FFFFFF", seg_line_width=9525, axis_line_color="162029",
    show_gridlines=False, show_legend=False,
    value_label_size_pt=8, cat_label_size_pt=8,
    gap_width=0, cat_header="Work segment",
    # Inner plot pinned to the source bar region within the graphic_frame below,
    # so the single column lands at the exact x/width of the transcribed exhibit.
    plot_layout={"x": 0.0833, "y": 0.0138, "w": 0.9155, "h": 0.9491},
)
CHARTS: list[dict] = [_CHART]

# Vertical color key, transcribed from the source exhibit (the native chart has no
# legend). Each entry: (fill, label, swatch_y, label_y); swatch x=4495800, label
# x=4689475. Order top->bottom mirrors the source (Port -> Depot).
_LEG = [
    (CHART_ACCENT_6, "Port & Technical Services",            1776413, 1771650),
    (CHART_ACCENT_5, "Electronics & C4ISR Sustainment",      1949450, 1944688),
    (CHART_ACCENT_4, "Combat Systems Sustainment",           2122488, 2117725),
    (CHART_ACCENT_3, "Hull, Mechanical & Electrical (HM&E)", 2295525, 2290763),
    (CHART_ACCENT_2, "Nuclear & Complex Overhauls",          2468563, 2463800),
    (CHART_ACCENT_1, "Depot Ship Repair",                    2641600, 2636838),
]


def _legend() -> str:
    parts = []
    sid = 50
    for fillc, label, sy, ly in _LEG:
        parts.append(text_box(
            sid, "LegendSwatch", 4495800, sy, 142875, 106362, [paragraph([])],
            fill=fillc, line_color="FFFFFF", line_width=9525, insets=INSETS_NONE))
        parts.append(text_box(
            sid + 1, "LegendLabel", 4689475, ly, 1750000, 122238,
            [paragraph([run(label, size=SOURCES_8PT, color=BLACK, font=FONT)], align="l")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        sid += 2
    return "".join(parts)


def _body() -> str:
    caption = text_box(
        10, "ChartCaption", 403013, 1298363, 3622253, 275434,
        [paragraph([run(_CHART_CAPTION, size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
    tbl = house_table(
        20, "WorkSegmentTable", _TBL_X, _TBL_Y, _COL_W, _ROWS,
        row_h=_RH, table_skin="rule", aligns=["l", "l"], size=900,
    )
    footer = text_box(
        30, "FooterNote", 457200, 6037783, 11308384, 502920,
        [paragraph([run(_FOOTER, size=SOURCES_8PT, color=DK, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
    # Native chart placed in the static exhibit's footprint (rId2 = this slide's
    # first chart). The catAx renders the "Total FY2025 MRO TAM" label; only the
    # column total can't be a native stacked-chart element, so keep it as overlay.
    chart = graphic_frame(
        sp_id=40, name="WorkSegmentStackedColumn",
        x=465138, y=1660000, cx=3946525, cy=4180000, rId="rId2",
    )
    total = text_box(
        45, "ChartTotal", 2387600, 1574800, 427038, 122238,
        [paragraph([run("$8,971M", size=SOURCES_8PT, color=BLACK, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE,
    )
    return caption + tbl + footer + chart + total + _legend()


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
    )
