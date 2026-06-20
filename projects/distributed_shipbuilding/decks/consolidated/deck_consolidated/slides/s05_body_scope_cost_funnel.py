"""s05_body_scope_cost_funnel - show why total ship cost is not the supplier TAM
denominator: two small-multiple waterfalls bridge each program's total ship
estimate down to its non-GFE Basic Construction base, on independent vertical
scales.

Pattern B: a full-width dual-waterfall exhibit (both programs on the same
FY2022-FY2027 cumulative portfolio basis) and three no-fill InterpBox cards below.
Each waterfall is a NATIVE stacked-column chart (matching the think-cell reference
chart2/chart3): an invisible spacer series lifts the floating removal bars, and a
single visible series carries the bar fills via per-point colors - accent5 AFC2CC
total-ship-estimate start, accent4 89A2B0 removals, accent2 1D4D68 Basic
Construction endpoint. The chart owns the bars and the left value axis (0-30 / 0-90,
dark-navy axis line, no gridlines); category labels, the four value labels (totals
above the full bars, removals centered inside their floating segment), and the black
running-total connector rules are slide overlays pinned to the chart's inner plot
(plot_layout), exactly as the reference builds them.

Spec: ds_specs/s05_body_scope_cost_funnel.txt (SLIDE 05 - SCOPE AND COST FUNNEL MAP).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_B, BODY_CX,
    CHART_ACCENT_2, CHART_ACCENT_4, CHART_ACCENT_5,
    BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Definition"
_BREADCRUMB_TOPIC = "Scope and Cost Funnel"
_TOPIC            = "Scope and Cost Funnel"
_TAKEAWAY = ("Sizing starts at new-construction budget lines and narrows to "
             "non-GFE Basic Construction, not total ship cost.")
_SOURCES = ("Sources: (1) DDG and submarine SCN/P-5c cost-funnel data, FY2022–FY2027; "
            "(2) Navy P-5c GFE and Basic Construction breakouts; (3) program TAM "
            "bridge inputs; (4) FY 2026 Mandatory Funding Allocation Plan, PL 119-21 "
            "Sec. 20002")


# ── Waterfall data (exact float values; matches reference chart2/chart3) ──────
# Each funnel is a stacked column: a no-fill spacer lifts the floating removal bars,
# a visible series carries the bar heights. spacer[i] + visible[i] == the bar top
# (running total) at category i. Per-point fills: accent5 start, accent4 removals,
# accent2 Basic Construction. `labels` are the rounded magnitudes; `kinds` drive
# label placement (start/end float above the full bar; decrease centers in-segment).
_CATS = ["Total ship estimate", "Less GFE / directed equipment",
         "Less other non-BC", "Basic Construction"]
_KINDS = ["start", "decrease", "decrease", "end"]
_FILLS = [CHART_ACCENT_5, CHART_ACCENT_4, CHART_ACCENT_4, CHART_ACCENT_2]

_DDG = {
    "spacer":  [0.0, 20.432805, 18.157125, 0.0],
    "visible": [31.192092, 10.759287, 2.275680, 18.157125],
    "labels":  ["31", "11", "2", "18"],
    "axis_max": 35, "axis_major": 5,
}
_SUB = {
    "spacer":  [0.0, 68.377484, 57.887981, 0.0],
    "visible": [85.623472, 17.245988, 10.489504, 57.887981],
    "labels":  ["86", "17", "10", "58"],
    "axis_max": 90, "axis_major": 10,
}

# Per-funnel title: italic caption carrying the units (no separate shared caption).
_TITLES = [
    "DDG-51, FY2022–FY2027 portfolio cumulative, constant FY2026 $B",
    "Submarines, FY2022–FY2027 portfolio cumulative, constant FY2026 $B",
]

# InterpBox cards: (9pt bold title, 9pt bulleted body) - the common Pattern B format.
_CARDS = [
    ("Basic Construction is the included denominator.",
     "The sizing base is $18.2B of DDG's $31.2B FY2022–FY2027 estimate and $57.9B "
     "of the submarine portfolio's $85.6B. This base funds yard labor, team-build "
     "work, purchased material, and first- and lower-tier supplier flow."),
    ("GFE, other budget categories, and yard self-perform leave the boundary.",
     "GFE leaves first — DDG electronics and ordnance ($10.8B); submarine government-"
     "furnished propulsion, electronics, and ordnance ($17.2B). Then other non-BC "
     "categories — plans, change orders, HM&E, and other, plus Virginia technology "
     "insertion on the submarine side ($2.3B DDG, $10.5B sub). "
     "Yard self-perform within Basic Construction is removed later, at the supplier step."),
    ("Top-of-funnel context and first-tier filings are evidence, not numerator.",
     "Total ship estimate and TOA frame the denominator; FFATA/FSRS subawards are a "
     "visible floor behind the supplier coefficient. Do not add AP/LLTM on top of "
     "the BC base inside this funnel; the DDG-only filtered AP/LLTM stream is handled "
     "separately, and the OBBBA Sec. 20002 mandatory awards are additive to these "
     "P-5c funnels, entering at the TAM bridge."),
]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_CAP_Y = BODY_Y                                       # top of the per-funnel titles

_CARDS_H = 1_400_000
_CARDS_Y = BODY_B - _CARDS_H                           # three InterpBox cards (bottom)
_EXH_B = _CARDS_Y - 130_000

# Two half-width small multiples.
_WGUT = 400_000
_HALF_W = (BODY_CX - _WGUT) // 2
_DDG_HX = BODY_X
_SUB_HX = BODY_X + _HALF_W + _WGUT
_HALVES = [_DDG_HX, _SUB_HX]

# Per-funnel italic title line at the top of each half.
_PHDR_W, _PHDR_H = 3_900_000, 300_000
_PHDR_Y = _CAP_Y

# Native-chart frame (bars + value axis) sits under the title, above the cards.
_CHART_Y = _PHDR_Y + _PHDR_H + 40_000
_CHART_H = _EXH_B - _CHART_Y

# Inner-plot fractions pinned on each chart (plot_layout) so the overlay value
# labels, connector rules, and category labels track the rendered bars. x leaves
# room for the value-axis tick labels; the bottom margin (1 - y - h) holds the
# two-line category labels.
_PLOT_LAYOUT = {"x": 0.05, "y": 0.13, "w": 0.93, "h": 0.69}
_N = 4                       # categories per funnel
_GAP_WIDTH = 80              # % gap between columns (matches reference gapWidth=80)

# Three InterpBox cards across the full width.
_ICARD_GAP = 200_000
_ICARD_W = (BODY_CX - 2 * _ICARD_GAP) // 3
_ICARD_X = [BODY_X + i * (_ICARD_W + _ICARD_GAP) for i in range(3)]

_CAT_LNSPC = 102_000         # tight line spacing for wrapped 9pt category labels


# ── Chart factory ────────────────────────────────────────────────────────────
def _funnel_chart(data: dict) -> dict:
    """One native stacked-column waterfall: invisible spacer + visible per-point
    series, left value axis, dark-navy axis line, no gridlines, no native value or
    category labels (those are slide overlays). Inner plot pinned via plot_layout."""
    return column_chart(
        mode="stacked",
        categories=_CATS,
        series=[
            {"name": "_Base", "values": data["spacer"],
             "no_fill": True, "hide_labels": True},
            {"name": "Funnel", "values": data["visible"],
             "data_point_colors": _FILLS},
        ],
        title=None,
        show_legend=False,
        value_axis_format='#,##0',
        value_axis_min=0, value_axis_max=data["axis_max"],
        value_axis_major_unit=data["axis_major"],
        show_gridlines=False,
        seg_line_color=None,                 # clean borderless funnel bars
        axis_line_color="162029",            # dark-navy value + category axis spine
        show_value_labels=False,             # value labels are overlays (below)
        show_cat_labels=False,               # category labels are overlays (below)
        gap_width=_GAP_WIDTH, cat_header="Step",
        plot_layout=_PLOT_LAYOUT,
    )


CHARTS: list[dict] = [_funnel_chart(_DDG), _funnel_chart(_SUB)]


# ── Plot geometry (mirror of each chart's pinned inner plot) ──────────────────
def _plot_geom(half_x: int):
    """Return (px, py, pw, ph) of the chart's inner plot rectangle in slide EMU,
    derived from the pinned plot_layout so overlays land on the rendered bars."""
    px = half_x + int(_HALF_W * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_H * _PLOT_LAYOUT["y"])
    pw = int(_HALF_W * _PLOT_LAYOUT["w"])
    ph = int(_CHART_H * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _bar_center(px: int, pw: int, i: int) -> int:
    return px + pw * (2 * i + 1) // (2 * _N)


def _bar_half_w(pw: int) -> int:
    # gap_width = gap/bar * 100, so bar = slot / (1 + gap/100); half-width for edges.
    slot = pw / _N
    return int(slot / (1 + _GAP_WIDTH / 100.0) / 2)


def _y_of(py: int, ph: int, level: float, axis_max: int) -> int:
    return py + int(ph * (1 - level / axis_max))


# ── Local helpers ────────────────────────────────────────────────────────────
def _title(sp_id: int, half_x: int, text: str) -> str:
    return text_box(
        sp_id, "FunnelTitle", half_x + (_HALF_W - _PHDR_W) // 2, _PHDR_Y,
        _PHDR_W, _PHDR_H,
        [paragraph([run(text, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)], align="l")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)


def _funnel_overlays(base: int, half_x: int, data: dict) -> str:
    """Overlay the four value labels (start/end float above the full bar; removals
    center inside their floating segment), three black running-total connector
    rules, and the four category labels — all pinned to the chart's inner plot."""
    px, py, pw, ph = _plot_geom(half_x)
    axis_max = data["axis_max"]
    spacer, visible, labels = data["spacer"], data["visible"], data["labels"]
    tops = [spacer[i] + visible[i] for i in range(_N)]   # running total at each bar
    half_w = _bar_half_w(pw)
    base_y = py + ph                                     # baseline (value == 0)

    parts = []

    # Connector rules: thin dark-navy dashed lines at each shared running-total level,
    # from one bar's edge to the next bar's edge (the think-cell reference look; drawn
    # first so the bars/labels sit on top).
    for i in range(_N - 1):
        level = tops[i + 1]                              # shared edge of bars i, i+1
        y = _y_of(py, ph, level, axis_max)
        x1 = _bar_center(px, pw, i) + half_w
        x2 = _bar_center(px, pw, i + 1) - half_w
        parts.append(connector(base + 40 + i, "WfRule", x1, y, x2 - x1, 0,
                               color="162029", width=3_175, dashed=True))

    # Value labels.
    box_w, box_h, gap = 760_000, 240_000, 24_000
    for i in range(_N):
        cx = _bar_center(px, pw, i)
        if _KINDS[i] in ("start", "end"):                # float above the full bar
            y_top = _y_of(py, ph, tops[i], axis_max) - gap - box_h
            anchor = "b"
        else:                                            # center in the floating segment
            mid = spacer[i] + visible[i] / 2.0
            y_top = _y_of(py, ph, mid, axis_max) - box_h // 2
            anchor = "ctr"
        parts.append(text_box(
            base + 10 + i, "WfValue", cx - box_w // 2, y_top, box_w, box_h,
            [paragraph([run(labels[i], size=LABEL_9PT, color=BLACK,
                            font=FONT)], align="ctr")],
            fill=None, line_color=None, anchor=anchor, insets=INSETS_NONE))

    # Category labels below the baseline.
    cat_w = pw // _N
    for i in range(_N):
        cx = _bar_center(px, pw, i)
        parts.append(text_box(
            base + 20 + i, "WfCat", cx - cat_w // 2, base_y + 30_000,
            cat_w, _CHART_Y + _CHART_H - (base_y + 30_000),
            [paragraph([run(_CATS[i], size=LABEL_9PT, color=BLACK, font=FONT)],
                       align="ctr", line_spacing=_CAT_LNSPC)],
            fill=None, line_color=None, anchor="t", insets=INSETS_NONE))

    return "".join(parts)


def _interp_card(sp_id: int, x: int, title: str, body: str) -> str:
    return text_box(
        sp_id, "InterpBox", x, _CARDS_Y, _ICARD_W, _CARDS_H,
        [paragraph([run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   space_after=100),
         paragraph([run(body, size=LABEL_9PT, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t",
        insets=(60_000, 40_000, 60_000, 40_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    titles = "".join(_title(20 + i, half_x, _TITLES[i])
                     for i, half_x in enumerate(_HALVES))

    # Two native chart frames (rId2 = DDG, rId3 = submarine) + their overlays.
    frames = "".join(
        graphic_frame(sp_id=100 + i, name=f"ScopeFunnel{i}",
                      x=half_x, y=_CHART_Y, cx=_HALF_W, cy=_CHART_H,
                      rId=f"rId{i + 2}")
        for i, half_x in enumerate(_HALVES))
    overlays = _funnel_overlays(100, _DDG_HX, _DDG) \
        + _funnel_overlays(200, _SUB_HX, _SUB)

    cards = "".join(_interp_card(30 + i, _ICARD_X[i], title, body)
                    for i, (title, body) in enumerate(_CARDS))

    return titles + frames + overlays + cards


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
