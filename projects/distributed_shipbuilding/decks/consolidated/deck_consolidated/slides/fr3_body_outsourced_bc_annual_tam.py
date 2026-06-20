"""fr3_body_outsourced_bc_annual_tam - front-row slide 3: Outsourced Basic
Construction (Annual TAM)
with the FY2028-FY2031 outlook, in the manager's clustered format: per FY,
THREE columns (Virginia, Columbia, DDG-51) whose FILLED portion is that class's
outsourced BC TAM and whose no-fill OUTLINED extension above is the rest of its
total ship spend (the penetration denominator) - dashed outline for the two
submarine classes, dotted for DDG. Columbia funds biennially, so FY22/23/25
carry no Columbia column. FY28-31 estimate clusters carry per-class implied-low
fills with a hatched range cap to each class's high bound and a dashed frame
per cluster - no denominator outlines (the FYDP gross is quoted in the
commentary instead).

One native stacked column drives the cluster: categories are [Va, Col, DDG,
spacer] quadruplets per FY (native category labels off; FY labels, the legend,
value labels, penetration ovals, the band rule and the commentary table are
slide overlays pinned to the inner plot). The outline series use the deck_core
per-series `line` option (no_fill + dash/sysDot outline).

Banding: Historical = FY2022-FY2026 (enacted, incl. OBBBA), Forecasted =
FY2027-FY2031 (PB2027 request + FYDP outlook); one dashed vertical at the
FY26|FY27 boundary runs from the plot top through the strips and the
commentary, with boxed band labels at the plot top.

Numbers sync: consolidated z_ChartData_OutsourcedBC §4 (fills + remainders +
ranges), §6-§7 (penetration), §5 (FY22-25 average). FY28-31 = each class's
PB2027 FYDP gross x its penetration assumption; low = class FY22-25 average,
high = low x 1.30 (stated outsourcing-intent uplift); constant FY2026 $.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3, CHART_ACCENT_4,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, BODY_12PT,
)
from deck_core.text_metrics import avg_char_width_emu

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Executive Summary"
_BREADCRUMB_TOPIC = "Outsourced BC Annual TAM"
_TOPIC            = "Outsourced Basic Construction Annual TAM"
_TAKEAWAY = ("After averaging $3.5B through FY2025, demand peaks at $5.5B in "
             "FY2024 and FY2026 and is expected to hold $4.3–5.7B a year "
             "through FY2031.")
_SOURCES = ("Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and "
            "PB27 FYDP outyears (FY28–FY31); FY26, PL 119-21 Sec. 20002; PB27 SCN, "
            "Columbia P-10 Strategic Outsourcing narrative; OUSD(C) Green Book "
            "Procurement deflators; Navy Shipbuilding Plan; PB27 SCN Exhibit P-10, "
            "LI 2122 (AP/LLTM Ship Construction EOQ). FY28–31 = PB27 FYDP gross × "
            "penetration per class; low = FY22–25 average, high = low × 1.30 "
            "(stated outsourcing intent); constant FY26 $.")

_UNITS = ("Outsourced Basic Construction TAM by fiscal year and class (Virginia, "
          "Columbia, DDG-51), $B, constant FY2026 dollars: filled = outsourced, "
          "outlined = rest of that class's total ship spend. FY2022–FY2027 incl. "
          "OBBBA Sec. 20002; FY2028–FY2031 estimated (hatched range, dashed frames).")


# ── Data (sync: workbook_consolidated z_chart_data_outsourced_bc §4-§7) ──────
_N_FY = 10
_N_ACT = 6                                       # FY2022..FY2027 actuals
_FY_LABELS = [f"FY{fy}" for fy in range(2022, 2032)]

# Filled (outsourced) values, $B. Columbia FY22/23/25 are genuinely zero (P-5c
# full funding lands biennially). FY28-31 = per-class implied LOW.
_VA_FILL  = [1.780, 1.854, 3.207, 1.847, 1.977, 2.962, 2.551, 2.457, 2.209, 2.246]
_COL_FILL = [0.0,   0.0,   1.454, 0.0,   1.575, 1.478, 1.273, 1.274, 1.257, 1.259]
_DDG_FILL = [0.474, 1.234, 0.874, 1.236, 1.929, 0.674, 0.552, 0.566, 0.870, 0.896]
# Denominator remainders (class total ship spend - outsourced), FY22-27 only.
_VA_REM  = [5.828, 5.904, 8.625, 7.843, 8.012, 8.246]
_COL_REM = [0.0,   0.0,   9.662, 0.0,   9.169, 8.799]
_DDG_REM = [4.006, 7.272, 4.838, 6.780, 3.777, 3.498]
_VA_DEN  = [f + r for f, r in zip(_VA_FILL[:6], _VA_REM)]
_COL_DEN = [f + r for f, r in zip(_COL_FILL[:6], _COL_REM)]
_DDG_DEN = [f + r for f, r in zip(_DDG_FILL[:6], _DDG_REM)]
# Range caps (high - low) on the estimate years, per class.
_VA_EST_HI  = [3.317, 3.194, 2.872, 2.919]
_COL_EST_HI = [1.655, 1.656, 1.634, 1.637]
_DDG_EST_HI = [0.718, 0.735, 1.131, 1.165]
_VA_RANGE  = [h - l for h, l in zip(_VA_EST_HI, _VA_FILL[6:])]
_COL_RANGE = [h - l for h, l in zip(_COL_EST_HI, _COL_FILL[6:])]
_DDG_RANGE = [h - l for h, l in zip(_DDG_EST_HI, _DDG_FILL[6:])]

_AVG_FY22_25 = 3.49                              # combined, $B (§5)

# Penetration strips (outsourced / class total ship spend, §6-§7 + Outlook §2).
_VA_PEN_LABELS  = ["23%", "24%", "27%", "19%", "20%", "26%"]
_COL_PEN_LABELS = [None, None, "13%", None, "15%", "14%"]
_DDG_PEN_LABELS = ["11%", "15%", "15%", "15%", "34%", "16%"]
_VA_PEN_RANGE  = "24–31% (assumed)"      # FY22-25 class avg / x1.30 intent
_COL_PEN_RANGE = "13–17% (assumed)"
_DDG_PEN_RANGE = "14–19% (assumed)"

assert len(_VA_FILL) == len(_COL_FILL) == len(_DDG_FILL) == _N_FY
assert len(_VA_REM) == len(_COL_REM) == len(_DDG_REM) == _N_ACT
assert all(r > 0 for r in _VA_RANGE + _COL_RANGE + _DDG_RANGE)

_AXIS_MAX = 13.0
assert max(_VA_DEN + _COL_DEN + _DDG_DEN) <= _AXIS_MAX - 1.0, \
    "raise _AXIS_MAX: denominator totals need headroom"


# ── Cluster layout: categories are [Va, Col, DDG, spacer] per FY ─────────────
_NS = 4 * _N_FY - 1            # 39 slots; no trailing spacer
_VA_SLOT  = [4 * k for k in range(_N_FY)]
_COL_SLOT = [4 * k + 1 for k in range(_N_FY)]
_DDG_SLOT = [4 * k + 2 for k in range(_N_FY)]


def _slots(pairs: dict[int, float | None]) -> list:
    """Expand {slot: value} into the 39-slot series value list."""
    return [pairs.get(i) for i in range(_NS)]


_HATCH = {"prst": "ltUpDiag", "fg": CHART_ACCENT_3, "bg": WHITE}
_OUTLINE_W = 9_525

_SERIES = [
    {"name": "Virginia",
     "values": _slots({_VA_SLOT[k]: _VA_FILL[k] for k in range(_N_FY)}),
     "color": CHART_ACCENT_2, "hide_labels": True},
    {"name": "Columbia",
     "values": _slots({_COL_SLOT[k]: (_COL_FILL[k] or None) for k in range(_N_FY)}),
     "color": CHART_ACCENT_4, "hide_labels": True},
    {"name": "DDG",
     "values": _slots({_DDG_SLOT[k]: _DDG_FILL[k] for k in range(_N_FY)}),
     "color": CHART_ACCENT_1, "hide_labels": True},
    {"name": "Va remainder",
     "values": _slots({_VA_SLOT[k]: _VA_REM[k] for k in range(_N_ACT)}),
     "no_fill": True, "hide_labels": True,
     "line": {"color": "162029", "width": _OUTLINE_W, "dash": "dash"}},
    {"name": "Col remainder",
     "values": _slots({_COL_SLOT[k]: (_COL_REM[k] or None) for k in range(_N_ACT)}),
     "no_fill": True, "hide_labels": True,
     "line": {"color": "162029", "width": _OUTLINE_W, "dash": "dash"}},
    {"name": "DDG remainder",
     "values": _slots({_DDG_SLOT[k]: _DDG_REM[k] for k in range(_N_ACT)}),
     "no_fill": True, "hide_labels": True,
     "line": {"color": "162029", "width": _OUTLINE_W, "dash": "sysDot"}},
    {"name": "Range to high",
     "values": _slots({**{_VA_SLOT[_N_ACT + j]: _VA_RANGE[j] for j in range(4)},
                       **{_COL_SLOT[_N_ACT + j]: _COL_RANGE[j] for j in range(4)},
                       **{_DDG_SLOT[_N_ACT + j]: _DDG_RANGE[j] for j in range(4)}}),
     "pattern": _HATCH, "hide_labels": True},
]

_PLOT_LAYOUT = {"x": 0.045, "y": 0.10, "w": 0.945, "h": 0.84}
_GAP_WIDTH = 30
_CHART = column_chart(
    mode="stacked",
    categories=[""] * _NS,
    series=_SERIES,
    title=None,
    show_legend=False,
    value_axis_format='#,##0',
    value_axis_min=0, value_axis_max=int(_AXIS_MAX), value_axis_major_unit=2,
    show_gridlines=False,
    seg_line_color=None, axis_line_color="162029",
    show_value_labels=False,
    value_label_format='0.0', value_label_size_pt=9, value_label_bold=False,
    show_cat_labels=False,
    gap_width=_GAP_WIDTH, cat_header="Slot",
    plot_layout=_PLOT_LAYOUT,
)
CHARTS: list[dict] = [_CHART]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_CAP_Y, _CAP_H = BODY_Y, 280_000               # units caption (8.5pt italic)
_KEY_Y, _KEY_H = 1_700_000, 200_000            # legend band (above the plot)
_CHART_Y = 1_700_000
_CHART_CY = 2_460_000                          # frame bottom 4_160_000
_FYLBL_Y = 4_030_000                           # FY labels (below plot, in frame)
_STRIP_H = 175_000                             # penetration oval height
_STRIP_Y = [4_185_000, 4_420_000, 4_655_000]   # Virginia, Columbia, DDG rows
_COMM_Y = 4_900_000
_COMM_H = BODY_B - _COMM_Y
_COMM_ROW_H = [390_000, 300_000, _COMM_H - 690_000]


def _plot_geom():
    """(px, py, pw, ph) of the chart's pinned inner plot in slide EMU."""
    px = BODY_X + int(BODY_CX * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_CY * _PLOT_LAYOUT["y"])
    pw = int(BODY_CX * _PLOT_LAYOUT["w"])
    ph = int(_CHART_CY * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _slot_center(px: int, pw: int, i: int) -> int:
    return px + pw * (2 * i + 1) // (2 * _NS)


def _cluster_center(px: int, pw: int, k: int) -> int:
    """The FY cluster's center = the middle (Columbia) column's center."""
    return _slot_center(px, pw, 4 * k + 1)


def _bar_half_w(pw: int) -> int:
    slot = pw / _NS
    return int(slot / (1 + _GAP_WIDTH / 100.0) / 2)


def _y_of(py: int, ph: int, level: float) -> int:
    return py + int(ph * (1 - level / _AXIS_MAX))


def _band_boundary_x(px: int, pw: int) -> int:
    """Historical | Forecasted boundary: the spacer slot center after FY2026."""
    return _slot_center(px, pw, 4 * 4 + 3)


# ── Content: commentary table (Submarines / DDG-51 / Penetration %) ──────────
_COMM_ROWS = [
    ("Submarines",
     "Columbia funds biennially (FY24/26 in window). Virginia outsources ~24%, "
     "Columbia ~13%.",
     "FYDP gross holds ~$19–21B a year (1 Columbia + 2 Virginias from 2028); "
     "capacity requires “strategically outsourcing workload to qualified "
     "suppliers” (PB27 SCN, Columbia P-10)."),
    ("DDG-51",
     "Outsourced 11–15%; FY2026 reads 34% on the OBBBA two-ship add plus EOQ "
     "AP/LLTM.",
     "FYDP gross $3.9–6.3B a year (two-ship buys FY30–31); upper bound reflects "
     "stated intent to grow outsourced manhours ~30%."),
    ("Penetration %",
     "Measured per FY and per class: outsourced BC TAM / total ship spend "
     "(constant FY2026 $).",
     "Lower bound = FY22–25 class average; upper bound = lower x 1.30 (stated "
     "outsourcing intent)."),
]
_COMM_LBL_W = 1_280_000


# ── Local helpers ────────────────────────────────────────────────────────────
def _units_caption(sp_id: int) -> str:
    return text_box(
        sp_id, "UnitsCaption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(_UNITS, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _hatch_swatch(sp_id: int, x: int, y: int, w: int, h: int) -> str:
    """Legend swatch carrying the chart's range hatch (text_box is solid-only)."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="LegendSwatchHatch"/>'
            '<p:cNvSpPr/><p:nvPr/></p:nvSpPr>'
            f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
            f'<a:pattFill prst="{_HATCH["prst"]}">'
            f'<a:fgClr><a:srgbClr val="{_HATCH["fg"]}"/></a:fgClr>'
            f'<a:bgClr><a:srgbClr val="{_HATCH["bg"]}"/></a:bgClr></a:pattFill>'
            '<a:ln w="6350"><a:solidFill><a:srgbClr val="BFBFBF"/></a:solidFill></a:ln>'
            '</p:spPr>'
            '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="en-US"/></a:p>'
            '</p:txBody></p:sp>')


def _legend(sp_id0: int) -> str:
    """Five-entry legend in the key band: three class fills, the dashed
    total-spend outline, and the hatched range cap."""
    sw_w, sw_h = 179_388, 133_350
    gap_sw, gap_entry, label_pad = 60_000, 200_000, 44_000
    char_w = avg_char_width_emu(BODY_12PT / 100.0) * 1.25
    cy = _KEY_Y + _KEY_H // 2
    px, _py, _pw, _ph = _plot_geom()
    entries = [("Virginia", CHART_ACCENT_2, None),
               ("Columbia", CHART_ACCENT_4, None),
               ("DDG-51", CHART_ACCENT_1, None),
               ("Total spend", WHITE, "dashed"),
               ("Range to high", None, "hatch")]
    parts, cx, sid = [], px, sp_id0
    for label, fill, kind in entries:
        if kind == "hatch":
            parts.append(_hatch_swatch(sid, cx, cy - sw_h // 2, sw_w, sw_h))
        else:
            parts.append(text_box(
                sid, "LegendSwatch", cx, cy - sw_h // 2, sw_w, sw_h,
                [paragraph([])],
                fill=fill, line_color="162029" if kind == "dashed" else None,
                line_width=9_525, dashed_line=(kind == "dashed"),
                anchor="ctr", insets=INSETS_NONE))
        lw = int(len(label) * char_w) + label_pad
        parts.append(text_box(
            sid + 1, "LegendLabel", cx + sw_w + gap_sw, cy - sw_h, lw, sw_h * 2,
            [paragraph([run(label, size=BODY_12PT, color=BLACK, font=FONT)])],
            fill=None, line_color=None, anchor="ctr", wrap="none", insets=INSETS_NONE))
        cx += sw_w + gap_sw + lw + gap_entry
        sid += 2
    return "".join(parts)


def _fy_labels(sp_id0: int) -> str:
    """FY labels under the plot, centered on each cluster."""
    px, _py, pw, _ph = _plot_geom()
    parts = []
    for k, lab in enumerate(_FY_LABELS):
        parts.append(text_box(
            sp_id0 + k, "FyLabel", _cluster_center(px, pw, k) - 350_000, _FYLBL_Y,
            700_000, 150_000,
            [paragraph([run(lab, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
                       align="ctr")],
            fill=None, line_color=None, anchor="t", insets=INSETS_NONE))
    return "".join(parts)


def _value_labels(sp_id0: int) -> str:
    """Per-column value annotations: the filled (outsourced) value just above
    the fill boundary inside the outline box; the remainder value just under
    the outline top; the denominator total bold above the outline. Estimate
    clusters read 'lo-hi' above each hatch cap instead. Columbia's empty years
    render nothing (the strip row carries the gap)."""
    px, py, pw, ph = _plot_geom()
    lbl_w, lbl_h = 560_000, 150_000
    tot_h, tot_gap = 200_000, 20_000
    parts, sid = [], sp_id0
    for k in range(_N_ACT):
        for slot, fill_v, rem_v, den_v in (
                (_VA_SLOT[k], _VA_FILL[k], _VA_REM[k], _VA_DEN[k]),
                (_COL_SLOT[k], _COL_FILL[k], _COL_REM[k], _COL_DEN[k]),
                (_DDG_SLOT[k], _DDG_FILL[k], _DDG_REM[k], _DDG_DEN[k])):
            if den_v == 0:
                sid += 3
                continue
            cx = _slot_center(px, pw, slot)
            y_fill = _y_of(py, ph, fill_v)
            y_den = _y_of(py, ph, den_v)
            parts.append(text_box(
                sid, "FillLabel", cx - lbl_w // 2, y_fill - lbl_h - 8_000,
                lbl_w, lbl_h,
                [paragraph([run(f"{fill_v:.1f}", size=LABEL_9PT, color=BLACK,
                                font=FONT)], align="ctr")],
                fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
            parts.append(text_box(
                sid + 1, "RemLabel", cx - lbl_w // 2, y_den + 14_000, lbl_w, lbl_h,
                [paragraph([run(f"{rem_v:.1f}", size=LABEL_9PT, color=BLACK,
                                font=FONT)], align="ctr")],
                fill=None, line_color=None, anchor="t", insets=INSETS_NONE))
            parts.append(text_box(
                sid + 2, "DenTotal", cx - lbl_w // 2, y_den - tot_gap - tot_h,
                lbl_w, tot_h,
                [paragraph([run(f"{den_v:.1f}", size=LABEL_9PT, bold=True,
                                color=BLACK, font=FONT)], align="ctr")],
                fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
            sid += 3
    # Estimate clusters: 'lo-hi' above each class's hatch cap.
    for j in range(4):
        k = _N_ACT + j
        for slot, lo, hi in ((_VA_SLOT[k], _VA_FILL[k], _VA_EST_HI[j]),
                             (_COL_SLOT[k], _COL_FILL[k], _COL_EST_HI[j]),
                             (_DDG_SLOT[k], _DDG_FILL[k], _DDG_EST_HI[j])):
            cx = _slot_center(px, pw, slot)
            y_top = _y_of(py, ph, hi)
            parts.append(text_box(
                sid, "EstLabel", cx - lbl_w // 2, y_top - lbl_h - 14_000,
                lbl_w, lbl_h,
                [paragraph([run(f"{lo:.1f}–{hi:.1f}", size=FINEPRINT_8_5PT,
                                color=BLACK, font=FONT)], align="ctr")],
                fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
            sid += 1
    return "".join(parts)


def _band_rule_and_labels(sp_id0: int) -> str:
    """One dashed vertical at the FY26|FY27 boundary (plot top -> commentary
    bottom) + boxed 'Historical' / 'Forecasted' band labels at the plot top."""
    px, py, pw, _ph = _plot_geom()
    bx = _band_boundary_x(px, pw)
    parts = [connector(sp_id0, "BandRule", bx, py, 0, BODY_B - py,
                       color="162029", width=3_175, dashed=True)]
    box_w, box_h = 1_150_000, 200_000
    for i, (lab, cx) in enumerate((("Historical", (px + bx) // 2),
                                   ("Forecasted", (bx + px + pw) // 2))):
        parts.append(text_box(
            sp_id0 + 1 + i, "BandLabel", cx - box_w // 2, py + 26_000, box_w, box_h,
            [paragraph([run(lab, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                            font=FONT)], align="ctr")],
            fill=WHITE, line_color=BLACK, line_width=9_525, anchor="ctr",
            insets=INSETS_NONE))
    return "".join(parts)


def _avg_line(sp_id: int) -> str:
    """Dashed FY22-25 combined-average reference line + label."""
    px, py, pw, ph = _plot_geom()
    y = _y_of(py, ph, _AVG_FY22_25)
    line = connector(sp_id, "AvgLine", px, y, pw, 0,
                     color="162029", width=9_525, dashed=True)
    lbl = text_box(
        sp_id + 1, "AvgLabel", px + 40_000, y - 200_000, 2_100_000, 180_000,
        [paragraph([run(f"FY22–25 avg (combined): {_AVG_FY22_25:.1f}",
                        size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    return line + lbl


def _est_frames(sp_id0: int) -> str:
    """Dashed-outline frame around each FY28-31 estimate cluster (hi top ->
    baseline, spanning the three class columns)."""
    px, py, pw, ph = _plot_geom()
    half_w = _bar_half_w(pw)
    pad = 26_000
    base_y = py + ph
    parts = []
    for j in range(4):
        k = _N_ACT + j
        hi = max(_VA_EST_HI[j], _COL_EST_HI[j], _DDG_EST_HI[j])
        y_top = _y_of(py, ph, hi) - pad
        x0 = _slot_center(px, pw, _VA_SLOT[k]) - half_w - pad
        x1 = _slot_center(px, pw, _DDG_SLOT[k]) + half_w + pad
        parts.append(text_box(
            sp_id0 + j, "EstFrame", x0, y_top, x1 - x0, base_y - y_top + pad,
            [paragraph([])],
            fill=None, line_color="162029", line_width=9_525, dashed_line=True,
            anchor="ctr", insets=INSETS_NONE))
    return "".join(parts)


def _pen_strips(sp_id0: int) -> str:
    """Three penetration rows under the chart (Virginia, Columbia, DDG-51):
    right-aligned single-line row label, one black-outlined oval per funded FY
    centered on its cluster, and a spanning 'assumed' pill across the outlook
    years. Columbia's unfunded years carry no oval."""
    px, _py, pw, _ph = _plot_geom()
    oval_w = 520_000
    lbl_w = 1_430_000 - BODY_X
    rows = [("Virginia %", _VA_PEN_LABELS, _VA_PEN_RANGE, _STRIP_Y[0]),
            ("Columbia %", _COL_PEN_LABELS, _COL_PEN_RANGE, _STRIP_Y[1]),
            ("DDG-51 %", _DDG_PEN_LABELS, _DDG_PEN_RANGE, _STRIP_Y[2])]
    parts, sid = [], sp_id0
    for label, labels, rng, y in rows:
        cy = y + _STRIP_H // 2
        parts.append(text_box(
            sid, "StripLabel", BODY_X, cy - 110_000, lbl_w, 220_000,
            [paragraph([run(label, size=DENSE_BODY_10PT, bold=True, italic=True,
                            color=BLACK, font=FONT)], align="r")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        sid += 1
        for k, lab in enumerate(labels):
            if lab is None:
                continue
            parts.append(text_box(
                sid + k, "PenOval", _cluster_center(px, pw, k) - oval_w // 2, y,
                oval_w, _STRIP_H,
                [paragraph([run(lab, size=FINEPRINT_8_5PT, italic=True,
                                color=BLACK, font=FONT)], align="ctr")],
                fill=WHITE, line_color=BLACK, line_width=12_700,
                prst="ellipse", anchor="ctr", insets=INSETS_NONE))
        sid += len(labels)
        ox = _cluster_center(px, pw, _N_ACT) - 380_000
        parts.append(text_box(
            sid, "PenPillRange", ox, y, px + pw - 60_000 - ox, _STRIP_H,
            [paragraph([run(rng, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                            font=FONT)], align="ctr")],
            fill=WHITE, line_color=BLACK, line_width=12_700,
            prst="roundRect", geom_adj={"adj": 50_000},
            anchor="ctr", insets=INSETS_NONE))
        sid += 1
    return "".join(parts)


def _commentary(sp_id: int) -> str:
    """Three-row commentary table (Submarines / DDG-51 / Penetration %), the
    content split Historical | Forecasted at the band boundary."""
    px, _py, pw, _ph = _plot_geom()
    bx = _band_boundary_x(px, pw)
    col_w = [_COMM_LBL_W, bx - BODY_X - _COMM_LBL_W, BODY_R - bx]
    rows = []
    for ri, (label, hist, fcst) in enumerate(_COMM_ROWS):
        last = ri == len(_COMM_ROWS) - 1
        border = {"B": "none"} if last else {"B": {"color": BLACK, "width": 9_525}}
        rows.append(trow([
            tcell(label, color=BLACK, bold=True, size=900, align="l",
                  anchor="ctr", borders=border),
            tcell(hist, color=BLACK, size=850, align="l", anchor="ctr",
                  borders=border),
            tcell(fcst, color=BLACK, size=850, align="l", anchor="ctr",
                  borders=border),
        ], h=_COMM_ROW_H[ri]))
    return table(sp_id, "BandCommentary", BODY_X, _COMM_Y, sum(col_w),
                 _COMM_H, col_widths=col_w, rows=rows)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = _units_caption(10)
    chart = graphic_frame(sp_id=20, name="OutsourcedBCAnnualTAMCluster",
                          x=BODY_X, y=_CHART_Y, cx=BODY_CX, cy=_CHART_CY, rId="rId2")
    legend = _legend(50)
    fy = _fy_labels(160)
    labels = _value_labels(200)
    band = _band_rule_and_labels(80)
    avg = _avg_line(84)
    frames = _est_frames(86)
    strips = _pen_strips(90)
    commentary = _commentary(30)
    return (caption + chart + legend + fy + labels + band + avg + frames
            + strips + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
