"""fr1_body_outsourced_bc_walk - front-row slide 1: the walk from each program's total
ship spend down to outsourced Basic Construction (the supplier TAM), DDG-51 and
Virginia/Columbia side by side, with a step/rationale ledger on the right.

Each walk is a NATIVE stacked-bar (horizontal) waterfall: an invisible spacer
series offsets the floating removal bars, a visible series carries the step
magnitudes via per-point fills, and the DDG chart adds a hatched third series
(a:pattFill) for the P-10 Ship Construction EOQ AP/LLTM that rides on top of
the Total Ship Spend and Basic Construction bars. Step labels, dashed
running-total connectors, and the annualized callouts are slide overlays
pinned to each chart's inner plot (plot_layout). Value-axis tick labels are
suppressed (show_value_axis_labels=False) - every bar is annotated directly,
think-cell walk style. Both programs' "Less: Prime AP/LLTM" rows are em-dash
placeholders: the DDG AP/LLTM base is the P-10 EOQ line at coefficient 1.00
(vendor material by classification - none retained by the primes), and the
submarines carry no AP/LLTM stream.

Data: FY2022-FY2027 cumulative, constant FY2026 $B, OBBBA Sec. 20002 mandatory
awards included; supplier coefficients are the announced-POP restates (DDG
25.29% FY23-27 / 22.00% FY22 vintage; Virginia 34% / Columbia 22%)
(workbook_consolidated z_ChartData_OutsourcedBC §1-§2; program workbooks' SCN
Budget / OBBBA Mandatory / Assumptions §3 / TAM Build tabs). Bar labels are
whole numbers (the manager's mock); each walk carries a 1-unit whole-number
rounding artifact at the endpoint (DDG 23 - 16 vs 6; sub 61 - 42 vs 18) -
accepted, matching the established rounding decision.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell, tcell_rich, tpara, trun,
)
from deck_core.charts import bar_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_B, BODY_CX,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3, CHART_ACCENT_4,
    CHART_ACCENT_5,
    BLACK, WHITE, DK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, VALUE_14PT,
)
from deck_core.text_metrics import (
    DEFAULT_CELL_INSET_H, DEFAULT_CELL_INSET_V, DEFAULT_MIN_ROW_H,
    line_height_emu, wrapped_line_count,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Executive Summary"
_BREADCRUMB_TOPIC = "Supplier TAM and SAM"
_TOPIC            = "Outsourced Basic Construction"
_TAKEAWAY = ("Across FY22–FY27, total ship spend narrows to an annualized "
             "~$1.1B of outsourced work for DDG-51 and ~$3.0B for submarines.")
_SOURCES = ("Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and "
            "PB27 FYDP outyears (FY28–FY31); FY26, PL 119-21 Sec. 20002; PB27 SCN, "
            "Columbia P-10 Strategic Outsourcing narrative; OUSD(C) Green Book "
            "Procurement deflators; Navy Shipbuilding Plan; PB27 SCN Exhibit P-10, "
            "LI 2122 (AP/LLTM Ship Construction EOQ); DoD contract award "
            "announcements (announced place-of-performance)")


# ── Walk data (exact floats; whole-number labels render via #,##0) ───────────
# Horizontal stacked bars: spacer[i] is the bar's left offset, visible[i] its
# magnitude, so spacer + visible (+ hatch where present) = the running total at
# step i. Removal bars hang right-aligned under the prior running total;
# subtotal/endpoint bars sit on zero. None = no bar / no label on that row.
#
# DDG component arithmetic (constant FY2026 $B, cumulative FY2022-FY2027):
#   in-year total  36.5921 = 31.1921 P-5c TSE + 5.4000 OBBBA Sec. 20002(17) gross
#   AP/LLTM hatch   1.0423 = P-10 Ship Construction EOQ line, constant FY2026 $
#                            (FY25 41.5 x 1.02 + FY26 1,000.0)
#   GFE step       12.7681 = 10.7593 P-5c GFE + 2.0088 OBBBA non-BC remainder
#   BC base        21.5483 = P-5c BC 18.1571 + OBBBA mandatory BC 3.3912
#   prime BC       16.1689 = BC 21.5483 - BC-stream TAM 5.3794 (announced-POP
#                            coefficients: 25.29% FY23-27, 22.00% FY22 vintage)
#   prime AP/LLTM   none   = EOQ coefficient 1.00 (vendor material by P-10
#                            classification; em-dash row)
#   outsourced BC   6.4217 = BC-stream TAM 5.3794 + AP/LLTM EOQ 1.0423
# Submarine: total 90.2235 = 85.6235 P-5c + 4.6000 OBBBA Sec. 20002(16) gross;
#   GFE 19.1685 = 17.2460 + 1.9225 remainder; BC 60.5655 = 57.8880 + 2.6775
#   OBBBA BC; prime BC 42.4316 = BC - outsourced; outsourced 18.1338 = Virginia
#   BC x 34% + Columbia BC x 22% + OBBBA BC x 34%; no AP/LLTM stream.
_CATS = ["Total Ship Spend", "Less: GFE", "Less: Other non-BC",
         "Basic Construction", "Less: Prime BC", "Less: Prime AP/LLTM",
         "Outsourced BC"]
_N = len(_CATS)

# Per-step fills (mirrored by the rationale ledger): gray subtotals, blue
# removals deepening toward the supplier cut, dark-navy endpoint.
_FILLS = [CHART_ACCENT_1, CHART_ACCENT_5, CHART_ACCENT_4,
          CHART_ACCENT_1, CHART_ACCENT_3, CHART_ACCENT_2, DK]
_HATCH_FG = CHART_ACCENT_1

_DDG = {
    "spacer":  [0.0, 24.866335, 22.590655, 0.0, 6.421730, None, 0.0],
    "visible": [36.592092, 12.768087, 2.275680, 21.548325, 16.168925,
                None, 6.421730],
    "hatch":   [1.042330, None, None, 1.042330, None, None, None],
    "axis_max": 40,
    # Boundary running-total levels for the dashed connectors (edge of bar i
    # and bar i+1): total top, then each new running total going down. The
    # empty Prime AP/LLTM row makes the last connector span rows 4 -> 6.
    "conn_levels": [37.634422, 24.866335, 22.590655, 22.590655, 6.421730],
    "hide_label_points": [],
    "annualized": "~$1.1B",
}
_SUB = {
    "spacer":  [0.0, 71.054967, 60.565463, 0.0, 18.133847, None, 0.0],
    "visible": [90.223472, 19.168505, 10.489504, 60.565463, 42.431616,
                None, 18.133847],
    "hatch":   None,                 # no submarine AP/LLTM stream
    "axis_max": 95,
    "conn_levels": [90.223472, 71.054967, 60.565463, 60.565463, 18.133847],
    "hide_label_points": [],
    "annualized": "~$3.0B",
}
_PANEL_TITLES = ["DDG-51", "Virginia / Columbia-class"]

_EXHIBIT_HDR = ("Walk to Outsourced Basic Construction Spend "
                "($B, cumulative FY22–FY27, FY26 $)")


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Left walk zone (exhibit header, step labels, two chart panels) + right ledger.
# Ledger column split per the manager's draft (narrow step / wide rationale).
_TBL_COL_W = [1_281_269, 3_018_731]
_TBL_W = sum(_TBL_COL_W)
_TBL_GUT = 250_000
_WALK_W = BODY_CX - _TBL_W - _TBL_GUT          # 6_732_362
_TBL_X = BODY_X + _WALK_W + _TBL_GUT           # ledger right edge lands on BODY_R

_LBL_W = 1_480_000                             # shared step-label column
_PANEL_GUT = 120_000
_PANEL_W = (_WALK_W - _LBL_W - _PANEL_GUT) // 2
_DDG_PX = BODY_X + _LBL_W
_SUB_PX = _DDG_PX + _PANEL_W + _PANEL_GUT
_PANELS = [_DDG_PX, _SUB_PX]

_HDR_H = 220_000                               # exhibit header + rule under it
_CHIP_Y = BODY_Y + 300_000                     # bordered program chips
_CHIP_W, _CHIP_H = 1_900_000, 240_000
_MICRO_Y = _CHIP_Y + _CHIP_H + 30_000          # "In-Year" / "AP/LLTM" captions
_MICRO_H = 170_000

_CHART_Y = _MICRO_Y + _MICRO_H + 30_000
_CHART_H = BODY_B - _CHART_Y

# Inner-plot fractions pinned on each chart (plot_layout): no axis tick labels
# or category labels are rendered, so the plot fills nearly the whole frame.
_PLOT_LAYOUT = {"x": 0.012, "y": 0.012, "w": 0.976, "h": 0.970}
_GAP_WIDTH = 50              # % gap between bar rows (thick walk bars)


# ── Chart factory ────────────────────────────────────────────────────────────
def _walk_chart(data: dict) -> dict:
    """One native stacked-bar waterfall: invisible spacer + visible per-point
    series (+ hatched AP/LLTM series on DDG). No native category labels, no
    value-axis tick labels - bars are annotated by native ctr labels and slide
    overlays. Inner plot pinned via plot_layout."""
    series = [
        {"name": "_Base", "values": data["spacer"],
         "no_fill": True, "hide_labels": True},
        {"name": "Walk", "values": data["visible"],
         "data_point_colors": _FILLS,
         "hide_label_points": data["hide_label_points"]},
    ]
    if data["hatch"]:
        series.append({"name": "AP/LLTM", "values": data["hatch"],
                       "pattern": {"prst": "ltUpDiag", "fg": _HATCH_FG,
                                   "bg": WHITE}})
    return bar_chart(
        mode="stacked",
        categories=_CATS,
        series=series,
        title=None,
        show_legend=False,
        value_axis_format='#,##0',
        value_label_format='#,##0',
        value_label_size_pt=9,
        value_label_bold=False,
        value_axis_min=0, value_axis_max=data["axis_max"],
        show_value_axis_labels=False,        # bars are annotated directly
        show_gridlines=False,
        seg_line_color=None,                 # clean borderless walk bars
        axis_line_color="162029",            # dark-navy axis spine
        show_cat_labels=False,               # step labels are slide overlays
        gap_width=_GAP_WIDTH, cat_header="Step",
        plot_layout=_PLOT_LAYOUT,
    )


CHARTS: list[dict] = [_walk_chart(_DDG), _walk_chart(_SUB)]


# ── Plot geometry (mirror of each chart's pinned inner plot) ──────────────────
def _plot_geom(panel_x: int):
    """Return (px, py, pw, ph) of the chart's inner plot rectangle in slide EMU."""
    px = panel_x + int(_PANEL_W * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_H * _PLOT_LAYOUT["y"])
    pw = int(_PANEL_W * _PLOT_LAYOUT["w"])
    ph = int(_CHART_H * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _row_center(py: int, ph: int, i: int) -> int:
    """Bar row i's vertical center (categories run top-to-bottom)."""
    return py + ph * (2 * i + 1) // (2 * _N)


def _bar_half_h(ph: int) -> int:
    # gap_width = gap/bar * 100, so bar = slot / (1 + gap/100); half for edges.
    slot = ph / _N
    return int(slot / (1 + _GAP_WIDTH / 100.0) / 2)


def _x_of(px: int, pw: int, level: float, axis_max: int) -> int:
    return px + int(pw * level / axis_max)


# ── Local helpers ────────────────────────────────────────────────────────────
def _exhibit_header() -> str:
    hdr = text_box(
        10, "ExhibitHeader", BODY_X, BODY_Y, _WALK_W, _HDR_H,
        [paragraph([run(_EXHIBIT_HDR, size=DENSE_BODY_10PT, bold=True,
                        color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    rule = connector(11, "ExhibitHeaderRule", BODY_X, BODY_Y + _HDR_H + 20_000,
                     _WALK_W, 0, color=BLACK, width=9_525)
    return hdr + rule


def _panel_chip(sp_id: int, panel_x: int, label: str) -> str:
    return text_box(
        sp_id, "ProgramChip", panel_x + (_PANEL_W - _CHIP_W) // 2, _CHIP_Y,
        _CHIP_W, _CHIP_H,
        [paragraph([run(label, size=DENSE_BODY_10PT, italic=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=None, line_color=BLACK, line_width=12_700, anchor="ctr",
        insets=INSETS_NONE)


def _micro_caption(sp_id: int, cx: int, text: str) -> str:
    w = 800_000
    return text_box(
        sp_id, "StreamCaption", cx - w // 2, _MICRO_Y, w, _MICRO_H,
        [paragraph([run(text, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)


def _stream_captions() -> str:
    """'In-Year' / 'AP/LLTM' captions over the Total Ship Spend bar's spans."""
    parts = []
    # DDG: in-year span 0..36.59, hatch 36.59..37.63 (of axis 40).
    px, _, pw, _ = _plot_geom(_DDG_PX)
    in_year_cx = _x_of(px, pw, 36.592092 / 2, _DDG["axis_max"])
    hatch_cx = _x_of(px, pw, 37.113257, _DDG["axis_max"])
    parts.append(_micro_caption(22, in_year_cx, "In-Year"))
    parts.append(_micro_caption(23, hatch_cx, "AP/LLTM"))
    # Submarine: in-year only (no AP/LLTM stream).
    px, _, pw, _ = _plot_geom(_SUB_PX)
    parts.append(_micro_caption(24, _x_of(px, pw, 90.223472 / 2,
                                          _SUB["axis_max"]), "In-Year"))
    return "".join(parts)


def _step_labels() -> str:
    """Shared step-label column: one 9pt label per bar row, vertically centered
    on the row (both panels share row geometry, so one column serves both)."""
    _, py, _, ph = _plot_geom(_DDG_PX)
    parts = []
    for i, cat in enumerate(_CATS):
        cy = _row_center(py, ph, i)
        parts.append(text_box(
            30 + i, "StepLabel", BODY_X, cy - 110_000, _LBL_W - 80_000, 220_000,
            [paragraph([run(cat, size=LABEL_9PT, color=BLACK, font=FONT)],
                       align="l")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
    return "".join(parts)


def _walk_overlays(base: int, panel_x: int, data: dict) -> str:
    """Dashed running-total connectors between consecutive bars. The submarine
    walk has no Prime AP/LLTM bar, so its last connector spans the empty row
    (one long rule from the Prime BC bar to the Outsourced BC bar)."""
    px, py, pw, ph = _plot_geom(panel_x)
    axis_max = data["axis_max"]
    half_h = _bar_half_h(ph)
    parts = []
    levels = data["conn_levels"]
    skip_row = data["visible"][5] is None      # empty Prime AP/LLTM row (sub)
    for b, level in enumerate(levels):
        i = b                                  # boundary between rows i, i+1
        j = i + 1
        if skip_row and b == len(levels) - 1:
            i, j = 4, 6                        # span the empty row
        x = _x_of(px, pw, level, axis_max)
        y1 = _row_center(py, ph, i) + half_h
        y2 = _row_center(py, ph, j) - half_h
        parts.append(connector(base + b, "WalkRule", x, y1, 0, y2 - y1,
                               color="162029", width=3_175, dashed=True))
    return "".join(parts)


def _no_ap_dash(sp_id: int, panel_x: int, data: dict) -> str:
    """Em-dash placeholder on a walk's empty Prime AP/LLTM row (both programs:
    the DDG EOQ stream is 100% outsourced by P-10 classification, the
    submarines carry no AP/LLTM stream). Sits at the running-total level."""
    px, py, pw, ph = _plot_geom(panel_x)
    cx = _x_of(px, pw, data["conn_levels"][-1], data["axis_max"])
    w = 220_000
    return text_box(
        sp_id, "NoApDash", cx - w // 2, _row_center(py, ph, 5) - 100_000, w, 200_000,
        [paragraph([run("—", size=LABEL_9PT, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)


def _callout(sp_id: int, panel_x: int, value: str) -> str:
    """Bordered annualized-value callout in the open bottom-right of a panel."""
    _, py, _, ph = _plot_geom(panel_x)
    w, h = 1_150_000, 430_000
    x = panel_x + _PANEL_W - w - 20_000
    y = _row_center(py, ph, 6) - h // 2
    return text_box(
        sp_id, "AnnualizedCallout", x, y, w, h,
        [paragraph([run(value, size=VALUE_14PT, bold=True, color=BLACK,
                        font=FONT)], align="ctr", space_after=20),
         paragraph([run("annualized", size=LABEL_9PT, italic=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=WHITE, line_width=12_700, anchor="ctr", insets=INSETS_NONE)


# ── Step/rationale ledger ─────────────────────────────────────────────────────
# Step-cell fills mirror the bar fills; "Calculation" rows mark the two
# walk subtotals. WHITE text on the dark fills (accent1/3/2, DK). Rationale
# entries are bullet lists (one evidence point per bullet); the two
# "Calculation" strings stay single-line italic.
# Rationale bullets are either a plain string or a list of (text, style) runs
# (style: None / "bu" bold-underline lead-in / "i" italic class name) - the
# manager's run-in lead-in convention ("In-Year Spend:", "AP/LLTM:") with
# italic ship-class names. Copy is sized to keep the table inside BODY_B.
_LED_HEADERS = ["Step", "Rationale"]
_LED_BODY = [
    ("Total Ship Spend",
     [[("In-Year Spend:", "bu"),
       (" FY2022–FY2027 SCN end cost; OBBBA adds two FY2026 DDG-51s ($5.4B) "
        "and a second FY2026 ", None),
       ("Virginia", "i"), (" ($4.6B).", None)],
      [("AP/LLTM:", "bu"),
       (" DDG-51 adds the P-10 EOQ line ($1.0B); submarines carry no separate "
        "AP/LLTM stream.", None)]]),
    ("Less: Government-Furnished Equipment",
     ["Removes GFE (propulsion, electronics, ordnance) the Navy buys directly "
      "and furnishes to Primes, incl. the non-BC remainder of OBBBA awards; "
      "not addressable to outsourced BC players."]),
    ("Less: Other non-BC",
     ["Removes engineering and program costs (plans, change orders, other "
      "non-construction) generally performed by Primes."]),
    ("Basic Construction", "Calculation"),
    ("Less: Prime BC",
     ["Removes construction the Primes perform in their own yards.",
      [("BC spend x the announced outside-yard share from DoD award "
        "place-of-performance data: ~25% DDG-51 (FY22 ships 22%), 34% ", None),
       ("Virginia", "i"), (" / 22% ", None), ("Columbia", "i"), (".", None)]]),
    ("Less: Prime AP/LLTM",
     [[("DDG-51:", "bu"),
       (" the P-10 EOQ base is vendor-purchased material, so Primes retain "
        "none — $0 removed; the full $1.0B flows to Outsourced BC.", None)],
      [("Submarines:", "bu"),
       (" no AP/LLTM stream exists, so there is nothing to remove.", None)]]),
    ("Outsourced BC", "Calculation"),
]
_CALC_ROWS = {4, 7}                  # 1-based row index incl. header
# WHITE step text on CHART_ACCENT_1/3/2 and DK; BLACK on accent5/4.
_STEP_TEXT = [WHITE, BLACK, BLACK, WHITE, WHITE, WHITE, WHITE]

_BULLET_MARL = 142_875               # paragraph() bullet hang (marL/-indent)


_LED_PT = 9.0          # the manager's 9pt ledger text
_LED_SZ = 900


def _bullet_text(b) -> str:
    """Plain text of a bullet spec (str or run list) for wrap estimation."""
    return b if isinstance(b, str) else "".join(t for t, _s in b)


def _ledger_row_heights() -> list[int]:
    """Per-row heights for the bulleted ledger. estimate_row_heights only
    models single-paragraph cells, so the rationale column is sized here:
    each bullet wraps in (column - insets - bullet hang) of width and the
    cell's line count is the sum over bullets."""
    heights = [max(DEFAULT_MIN_ROW_H,
                   line_height_emu(_LED_PT) + 2 * DEFAULT_CELL_INSET_V)]
    step_w = _TBL_COL_W[0] - 2 * DEFAULT_CELL_INSET_H
    rat_w = _TBL_COL_W[1] - 2 * DEFAULT_CELL_INSET_H
    for step, rationale in _LED_BODY:
        lines = wrapped_line_count(step, step_w, size_pt=_LED_PT)
        if isinstance(rationale, str):
            lines = max(lines, wrapped_line_count(rationale, rat_w,
                                                  size_pt=_LED_PT))
        else:
            lines = max(lines, sum(
                wrapped_line_count(_bullet_text(b), rat_w - _BULLET_MARL,
                                   size_pt=_LED_PT)
                for b in rationale))
        heights.append(max(DEFAULT_MIN_ROW_H,
                           lines * line_height_emu(_LED_PT)
                           + 2 * DEFAULT_CELL_INSET_V))
    return heights


_LED_ROW_H = _ledger_row_heights()


def _bullet_para(b) -> dict:
    """Bulleted 9pt paragraph dict for tcell_rich (rationale cells). Accepts a
    plain string or a list of (text, style) runs with style None / "bu"
    (bold underline lead-in) / "i" (italic class name)."""
    if isinstance(b, str):
        runs = [trun(b, size=_LED_SZ, color=BLACK)]
    else:
        runs = [trun(t, size=_LED_SZ, color=BLACK,
                     bold=(s == "bu") or None,
                     underline=(s == "bu") or None,
                     italic=(s == "i") or None)
                for t, s in b]
    return dict(tpara(runs, align="l"),
                bullet=True, bullet_char="•",
                marL=_BULLET_MARL, indent=-_BULLET_MARL)


# Row separators match the manager's vDraft table rules (deck_mini
# slide04_tables.xml): 0.5pt gray horizontal rules only - same weight under
# the header, none under the last row, no verticals.
_LED_RULE = {"color": "808080", "width": 6_350}


def _ledger() -> str:
    rows = []
    entries = [tuple(_LED_HEADERS)] + list(_LED_BODY)
    n = len(entries)
    for ri, (step, rationale) in enumerate(entries):
        hdr = ri == 0
        last = ri == n - 1
        border = {"B": "none"} if last else {"B": dict(_LED_RULE)}
        calc = ri in _CALC_ROWS
        step_cell = tcell(
            step,
            fill=None if hdr else _FILLS[ri - 1],
            color=BLACK if hdr else _STEP_TEXT[ri - 1],
            bold=True, size=_LED_SZ,
            align="l", anchor="ctr", borders=border)
        if isinstance(rationale, str):
            rat_cell = tcell(
                rationale,
                color=BLACK, bold=hdr, italic=(True if calc else None),
                size=_LED_SZ,
                align="l", anchor="ctr", borders=border)
        else:
            rat_cell = tcell_rich([_bullet_para(b) for b in rationale],
                                  anchor="ctr", borders=border)
        rows.append(trow([step_cell, rat_cell], h=_LED_ROW_H[ri]))
    return table(50, "StepRationaleLedger", _TBL_X, BODY_Y, _TBL_W,
                 sum(_LED_ROW_H), col_widths=_TBL_COL_W, rows=rows)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    frames = "".join(
        graphic_frame(sp_id=100 + i, name=f"OutsourcedWalk{i}",
                      x=panel_x, y=_CHART_Y, cx=_PANEL_W, cy=_CHART_H,
                      rId=f"rId{i + 2}")
        for i, panel_x in enumerate(_PANELS))
    chips = "".join(_panel_chip(20 + i, panel_x, _PANEL_TITLES[i])
                    for i, panel_x in enumerate(_PANELS))
    overlays = (_walk_overlays(110, _DDG_PX, _DDG)
                + _walk_overlays(130, _SUB_PX, _SUB)
                + _no_ap_dash(117, _DDG_PX, _DDG) + _no_ap_dash(136, _SUB_PX, _SUB))
    callouts = _callout(60, _DDG_PX, _DDG["annualized"]) \
        + _callout(61, _SUB_PX, _SUB["annualized"])
    return (_exhibit_header() + chips + _stream_captions() + _step_labels()
            + frames + overlays + callouts + _ledger())


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
