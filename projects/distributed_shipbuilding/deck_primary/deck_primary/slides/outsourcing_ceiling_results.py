"""outsourcing_ceiling_results - the results companion to the Outsourcing Ceiling
methodology slides. Where the method slides prove the estimate is defensible, this
slide proves the implication is large: by program, how far today's off-yard floor
sits below the structural ceiling, with the selected p=50% working case in between.

Pattern A: a native clustered column chart (left) carrying the quantitative answer,
a right-side by-program headroom table (floor -> ceiling and the headroom multiple,
the one figure not on the chart), and a three-card KPI strip under the chart sizing
the dollars. The chart is generated natively via column_chart() -
so it travels with an embedded, editable worksheet - and is styled to match this
deck's own charts (see slides/_chart_xml/slide05_chart5.xml): a dark-navy 162029
0.75pt axis spine on both axes, the value scale shown in %, no gridlines, and no
per-bar outline. It uses an alternative blue ramp (lighter -> darker = floor ->
selected -> ceiling) distinct from the methodology slide so the pair reads as two
exhibits, not a duplicate. Headroom multiples live in the commentary, not on the
chart; dollars sit in the KPI strip, not on the chart axis, because the workbook's
answer is the share and the multiple.

Chrome + sources shared with the sibling ceiling slides (sources stay external).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide, breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, trow, tcell,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.chart_key import chart_legend
from deck_core.style import (
    BODY_X, BODY_R, BLACK, WHITE, FONT, GRAY_1, GRAY_5,
    CHART_TITLE_10PT, CAP_12PT, FINEPRINT_8_5PT, DENSE_BODY_10PT,
    RIBBON_KPI_18PT, INSETS_CARD, INSETS_NONE,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

# ── Chrome text (shared with the sibling ceiling slides) ─────────────────────
_SECTION = "Executive Summary"
_TOPIC_LABEL = "Supplier TAM and SAM"
_TOPIC = "Outsourcing Ceiling Results"
_TAKEAWAY = ("The structural ceiling is ~76% of Basic Construction, leaving ~3x "
             "headroom over today.")
_SOURCES = (
    "Sources: Defense News, \"Defense firms outsource sub, carrier construction "
    "amid labor woes\" (M. Eckstein, Oct 2022); O'Rourke (CRS), State of U.S. "
    "Shipbuilding, House Armed Services Committee testimony (Mar 2025), "
    "cross-checked against the CBO Shipbuilding Composite Index (Apr 2024); "
    "DoD FMR 7000.14-R Vol 2B Ch 4, Exhibit P-5 ship cost element categories "
    "(Nov 2017); DoD contract award announcements (announced place-of-performance): "
    "Virginia Block V (2019), Columbia Build I (2020), DDG-51 FY23–27 multiyear "
    "(2023) | Note: dollar figures are constant FY2026 $."
)
_SOURCES_Y = 6_085_448
_BOTTOM = 6_023_400

# ── Native clustered column chart: share of BC, by program ───────────────────
# Alternative blue ramp (cooler than the methodology slide's BLUE_* tokens):
# light = current floor, mid = selected case, dark = structural ceiling.
_C_FLOOR, _C_SELECTED, _C_CEILING = "89A2B0", "486D82", "1D4D68"

_CATEGORIES = ["Virginia", "Columbia", "DDG-51", "Portfolio"]

# Styled to match this deck's own charts (see _chart_xml/slide05_chart5.xml):
# both axes carry a dark-navy 162029 0.75pt spine, the value scale shows in %,
# no gridlines, no per-bar outline (bars abut, as in slide05), quiet 10pt %
# data labels, and a bottom legend keying the three reads. Native column_chart,
# so the data travels in an embedded editable worksheet; bars carry the alt
# floor -> selected -> ceiling ramp.
_CHART = column_chart(
    mode="clustered",
    categories=_CATEGORIES,
    series=[
        {"name": "Current floor", "values": [0.34, 0.22, 0.13, 0.26],
         "color": _C_FLOOR},
        {"name": "Selected case", "values": [0.50, 0.50, 0.52, 0.51],
         "color": _C_SELECTED},
        {"name": "Structural ceiling", "values": [0.75, 0.75, 0.80, 0.76],
         "color": _C_CEILING},
    ],
    show_legend=False,
    value_axis_format="0%",
    value_label_format="0%",
    value_axis_min=0.0,
    value_axis_max=1.0,
    value_axis_major_unit=0.25,
    show_value_axis_labels=True,
    show_gridlines=False,
    seg_line_color=None,
    axis_line_color="162029",
    axis_line_width=9525,
    show_value_labels=True,
    value_label_size_pt=10,
    value_label_bold=False,
    cat_label_size_pt=10,
    gap_width=80,
    cat_header="Program",
)
CHARTS = [_CHART]

# ── Two-zone layout: chart left, commentary rail right, KPI strip under chart ─
_CHART_X = BODY_X
_CHART_W = 7_400_000
_RAIL_X = _CHART_X + _CHART_W + 160_000
_RAIL_CX = BODY_R - _RAIL_X

_UNITS_Y, _UNITS_H = 1_410_000, 220_000
_CHART_Y, _CHART_H = 1_650_000, 2_700_000
_LEGEND_CY = 4_500_000          # legend chips sit below the chart, above the KPIs


def _units() -> str:
    return text_box(
        10, "UnitsCaption", _CHART_X, _UNITS_Y, _CHART_W, _UNITS_H,
        [paragraph([run("Share of Basic Construction; Portfolio is FY22–27 "
                        "BC-weighted", size=CHART_TITLE_10PT, italic=True,
                        color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _chart() -> str:
    return graphic_frame(sp_id=11, name="CeilingResultsChart", x=_CHART_X,
                         y=_CHART_Y, cx=_CHART_W, cy=_CHART_H, rId="rId2")


def _legend() -> str:
    # Legend chips matching this deck's own charts: a 179388x133350 swatch + a
    # 10pt label per entry (see _chart_xml/slide05.xml work-type key). Replaces
    # the native chart legend, which the deck's charts don't use.
    return chart_legend(
        12,
        [("Current floor", _C_FLOOR),
         ("Selected case", _C_SELECTED),
         ("Structural ceiling", _C_CEILING)],
        cy=_LEGEND_CY, x_center=_CHART_X + _CHART_W // 2,
        label_size=DENSE_BODY_10PT)


# ── KPI strip: portfolio dollars at each read ────────────────────────────────
# Card fills match the chart bar colors (GS&O style: match boxes to chart bars),
# so each read keeps one identity across the chart, legend, and KPI strip.
# (fill, text color, label caps, value, subline)
_KPIS = [
    (_C_FLOOR, BLACK, "CURRENT FLOOR", "$19.1B", "POP-based off-yard work"),
    (_C_SELECTED, WHITE, "SELECTED CASE", "$37.5B", "p=50% working read"),
    (_C_CEILING, WHITE, "STRUCTURAL CEILING", "$56.4B", "p=100% upper bound"),
]
_KPI_GAP = 150_000
_KPI_W = (_CHART_W - 2 * _KPI_GAP) // 3
_KPI_Y, _KPI_H = 4_720_000, 1_020_000
assert _KPI_Y + _KPI_H <= _BOTTOM, "KPI strip runs past the body bottom edge"


def _kpis() -> str:
    parts = []
    for i, (fill, txt, label, value, sub) in enumerate(_KPIS):
        x = _CHART_X + i * (_KPI_W + _KPI_GAP)
        parts.append(text_box(
            20 + i, f"Kpi{i + 1}", x, _KPI_Y, _KPI_W, _KPI_H,
            [paragraph([run(label, size=CAP_12PT, bold=True, color=txt,
                            font=FONT)], align="ctr", space_after=120),
             paragraph([run(value, size=RIBBON_KPI_18PT, bold=True, color=txt,
                            font=FONT)], align="ctr", space_after=120),
             paragraph([run(sub, size=FINEPRINT_8_5PT, italic=True, color=txt,
                            font=FONT)], align="ctr")],
            fill=fill, anchor="ctr", insets=INSETS_CARD))
    return "".join(parts)


# ── Right rail: a by-program headroom table (replaces prose commentary) ──────
# House "rule" skin mirroring slide 7's by-program table: bold header + 1.5pt
# rule, ½pt gray row rules, a 1pt rule + GRAY_1 fill setting off the Portfolio
# rollup. The Headroom column is bold - the additive payload, since the
# multiples aren't on the chart (a light borrow from the gso_JM "impact" column).
# A caption above says what the table shows; a quiet italic note below (the
# gso_JM bottom-callout idiom) recovers the working-case and widest-gap reads.
_RAIL_CAP_Y = 1_650_000
_RAIL_TBL_Y = 2_240_000

_TBL_HEADER = ["Program", "Floor → ceiling", "Headroom"]
_TBL_ROWS = [
    ["Virginia", "34% → 75%", "2.2x"],
    ["Columbia", "22% → 75%", "3.4x"],
    ["DDG-51", "13% → 80%", "6.1x"],
    ["Portfolio", "26% → 76%", "3.0x"],
]
_TBL_ALL = [_TBL_HEADER] + _TBL_ROWS
_TBL_COL_W = [1_000_000, 1_500_000, _RAIL_CX - 2_500_000]   # sum = _RAIL_CX
assert sum(_TBL_COL_W) == _RAIL_CX, "rail table columns must sum to the rail width"
_TBL_ALIGNS = ["l", "ctr", "ctr"]
_TBL_SZ = DENSE_BODY_10PT
_TBL_HEADROOM_CI = 2
_TBL_ROW_H = estimate_row_heights(_TBL_ALL, _TBL_COL_W, size_pt=_TBL_SZ / 100.0)
_TBL_CY = sum(_TBL_ROW_H)
_PORTFOLIO_RI = len(_TBL_ALL) - 1

_RULE_HEADER = {"color": BLACK, "width": 19_050}     # 1.5pt under the header
_RULE_BODY = {"color": GRAY_5, "width": 6_350}       # ½pt between body rows
_RULE_TOTAL = {"color": BLACK, "width": 12_700}      # 1pt above the rollup

_RAIL_NOTE_Y = _RAIL_TBL_Y + _TBL_CY + 200_000
assert _RAIL_NOTE_Y + 700_000 <= _SOURCES_Y, "rail note runs into the sources band"


def _rail_caption() -> str:
    return text_box(
        30, "RailCaption", _RAIL_X, _RAIL_CAP_Y, _RAIL_CX, 480_000,
        [paragraph([run("By program: ", size=DENSE_BODY_10PT, bold=True,
                        color=BLACK, font=FONT),
                    run("current place-of-performance floor, the structural "
                        "ceiling, and the headroom between them.",
                        size=DENSE_BODY_10PT, color=BLACK, font=FONT)])],
        fill=None, anchor="t", insets=INSETS_NONE)


def _row_border(ri: int) -> dict:
    if ri == 0:
        return {"B": _RULE_HEADER}
    if ri == _PORTFOLIO_RI:
        return {"B": "none"}
    if ri == _PORTFOLIO_RI - 1:
        return {"B": _RULE_TOTAL}
    return {"B": _RULE_BODY}


def _rail_table() -> str:
    rows = []
    for ri, row in enumerate(_TBL_ALL):
        hdr = ri == 0
        total = ri == _PORTFOLIO_RI
        border = _row_border(ri)
        cells = [
            tcell(text, size=_TBL_SZ, align=_TBL_ALIGNS[ci],
                  bold=(hdr or total or ci == 0 or ci == _TBL_HEADROOM_CI),
                  fill=(GRAY_1 if total else None),
                  anchor="ctr", borders=border)
            for ci, text in enumerate(row)
        ]
        rows.append(trow(cells, h=_TBL_ROW_H[ri]))
    return table(31, "HeadroomByProgram", _RAIL_X, _RAIL_TBL_Y, _RAIL_CX,
                 _TBL_CY, col_widths=_TBL_COL_W, rows=rows)


def _rail_note() -> str:
    return text_box(
        32, "RailNote", _RAIL_X, _RAIL_NOTE_Y, _RAIL_CX, 700_000,
        [paragraph([run("The selected p=50% working case is already ~half the "
                        "build (50–52% by program); DDG-51's ~6.1x is the widest "
                        "gap, off the lowest current floor.",
                        size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, anchor="t", insets=INSETS_NONE)


def _body() -> str:
    return (_units() + _chart() + _legend() + _kpis()
            + _rail_caption() + _rail_table() + _rail_note())


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC_LABEL)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES, y=_SOURCES_Y)
    )
