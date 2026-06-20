"""fr4_body_worktype_by_fy - front-row slide 4 (the manager's P4): outsourced Basic
Construction spend by work type, ANNUAL view - one stacked column per fiscal
year, FY2022-FY2025 (the gated-evidence window, measured vectors only), one
panel per class: Virginia, Columbia, DDG-51. Each column is that class's annual
outsourced BC TAM segmented by the seven work-type buckets plus the hatched
unresolved residual; segment labels are the SHARE of that year's TAM (the
mock's % convention), shown where the segment can hold a 9pt label. Columbia
funds biennially, so FY2024 is its only in-window column (em-dash placeholders
on the empty years).

Three native stacked-column charts (one per panel) with native FY category
labels and value-axis ticks (each panel runs its own $ scale; the per-panel
chips carry the class names, s03/s05 dual-chart precedent). Column totals ($B)
float above each bar; % labels are slide overlays pinned to each chart's inner
plot.

Data: annual constant FY2026 $B, OBBBA Sec. 20002 included (rides Virginia
FY2026 - outside this FY22-25 window); per-FY vectors are the gated yard/GDEB
FY22-25 share evidence applied to each class's own annual TAM (program
workbooks' SAM Build §3-§4 / Worktype by FY), mirrored in
workbook_consolidated z_ChartData_OutsourcedBC §8-§10. Column sums tie to the
s11a annual fills; summed across FY22-25 plus FY26-27 they reproduce the s03b
cumulative pools.
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
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3, CHART_ACCENT_4,
    CHART_ACCENT_5, CHART_ACCENT_6,
    BLACK, WHITE, DK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Executive Summary"
_BREADCRUMB_TOPIC = "Outsourced BC Annual TAM"
_TOPIC            = "Outsourced Basic Construction Spend by Work Type"
_TAKEAWAY = ("Machining leads every DDG-51 year; the submarine mix shifts year "
             "to year with award timing.")
_SOURCES = ("Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and "
            "PB27 FYDP outyears (FY28–FY31); FY26, PL 119-21 Sec. 20002; PB27 SCN, "
            "Columbia P-10 Strategic Outsourcing narrative; OUSD(C) Green Book "
            "Procurement deflators; Navy Shipbuilding Plan; PB27 SCN Exhibit P-10, "
            "LI 2122 (AP/LLTM Ship Construction EOQ); FFATA/FSRS subaward records, "
            "yard-prime construction PIIDs, FY22–FY25 action years (work-type shares)")

_EXHIBIT_HDR = ("Outsourced Basic Construction TAM by Work Type "
                "($B per year, FY22–FY25, FY26 $; segment labels = share of year)")


# ── Chart data (annual constant FY2026 $B; sync z_ChartData_OutsourcedBC §8-§10) ──
_FY_CATS = ["FY2022", "FY2023", "FY2024", "FY2025"]
# (bucket, fill) - stack order base -> top; residual cap hatched.
_BUCKET_FILLS = [
    ("Electrical and power",                  CHART_ACCENT_2),
    ("Piping, valves, and pumps",             CHART_ACCENT_3),
    ("Structural fabrication and pre-outfit", CHART_ACCENT_4),
    ("Machining",                             CHART_ACCENT_5),
    ("Coatings and insulation",               CHART_ACCENT_6),
    ("Castings and forgings",                 CHART_ACCENT_1),
    ("HVAC and ventilation",                  DK),
    ("Residual",                              None),
]
_HATCH = {"prst": "ltUpDiag", "fg": CHART_ACCENT_1, "bg": WHITE}

# Rows follow _BUCKET_FILLS order; columns FY2022-FY2025 ($B).
_VA_WT = [
    [0.368495986, 0.865859642, 0.736346985, 0.035197415],
    [0.272449311, 0.167845438, 0.942754177, 0.547155952],
    [0.513513635, 0.34467773, 0.556551769, 0.492813685],
    [0.108315223, 0.01499292, 0.194228613, 0.113847585],
    [0.076693549, 0.136814098, 0.229244033, 0.115541509],
    [0.046084466, 0.047195813, 0.083546914, 0.235329835],
    [0.003747833, 0.031124026, 0.002703856, 0.016739738],
    [0.39029784, 0.24521617, 0.462048303, 0.290617892],
]
_COL_WT = [
    [0, 0, 0.628862421, 0],
    [0, 0, 0.350632421, 0],
    [0, 0, 0.204411117, 0],
    [0, 0, 0.04539076, 0],
    [0, 0, 0.025676639, 0],
    [0, 0, 0.039021045, 0],
    [0, 0, 0.016820118, 0],
    [0, 0, 0.143458185, 0],
]
_DDG_WT = [
    [0.027222384, 0.056467032, 0.191894256, 0.10630836],
    [0.050574424, 0.087536052, 0.122911364, 0.090768198],
    [0.01663598, 0.043558308, 0.064574503, 0.086383965],
    [0.149893173, 0.407928757, 0.237555688, 0.540793692],
    [0.002434441, 0.003243218, 0.000790084, 0],
    [0, 0, 0.050453501, 0.026375868],
    [0.047756222, 0.255730657, 0.087605799, 0.207467163],
    [0.179848848, 0.37916663, 0.118202324, 0.178292113],
]

_PANELS = [
    {"name": "Virginia", "wt": _VA_WT, "axis_max": 4.0, "axis_major": 1.0},
    {"name": "Columbia", "wt": _COL_WT, "axis_max": 2.0, "axis_major": 0.5},
    {"name": "DDG-51", "wt": _DDG_WT, "axis_max": 2.0, "axis_major": 0.5},
]
for _p in _PANELS:
    _p["totals"] = [sum(_p["wt"][b][k] for b in range(8)) for k in range(4)]

# Ties: column sums = the s11a annual fills (label precision asserted).
_EXP_TOTALS = {"Virginia": [1.780, 1.854, 3.207, 1.847],
               "Columbia": [0.0, 0.0, 1.454, 0.0],
               "DDG-51": [0.474, 1.234, 0.874, 1.236]}
for _p in _PANELS:
    for _k in range(4):
        assert abs(_p["totals"][_k] - _EXP_TOTALS[_p["name"]][_k]) < 0.002, \
            (_p["name"], _k, _p["totals"][_k])


def _panel_chart(panel: dict) -> dict:
    series = []
    for b, (name, fill) in enumerate(_BUCKET_FILLS):
        vals = [panel["wt"][b][k] or None for k in range(4)]
        spec: dict = {"name": name, "values": vals, "hide_labels": True}
        if fill is None:
            spec["pattern"] = _HATCH
        else:
            spec["color"] = fill
        series.append(spec)
    return column_chart(
        mode="stacked",
        categories=_FY_CATS,
        series=series,
        title=None,
        show_legend=False,
        value_axis_format='0.0',
        value_label_format='0.0',
        value_label_size_pt=9,
        value_label_bold=False,
        value_axis_min=0, value_axis_max=panel["axis_max"],
        value_axis_major_unit=panel["axis_major"],
        show_value_axis_labels=True,
        show_gridlines=False,
        seg_line_color=WHITE, seg_line_width=9_525,
        axis_line_color="162029",
        show_cat_labels=True, cat_label_size_pt=10,
        gap_width=70, cat_header="Fiscal year",
        plot_layout=_PLOT_LAYOUT,
    )


_PLOT_LAYOUT = {"x": 0.11, "y": 0.03, "w": 0.86, "h": 0.86}
CHARTS: list[dict] = [_panel_chart(p) for p in _PANELS]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_HDR_H = 220_000
_LEG_Y = BODY_Y + _HDR_H + 90_000              # two legend rows
_LEG_ROW_H = 185_000
_CHIP_Y = _LEG_Y + 2 * _LEG_ROW_H + 70_000     # bordered class chips
_CHIP_W, _CHIP_H = 1_700_000, 230_000
_CHART_Y = _CHIP_Y + _CHIP_H + 60_000
_CHART_H = BODY_B - _CHART_Y

_PANEL_GUT = 250_000
_PANEL_W = (BODY_CX - 2 * _PANEL_GUT) // 3
_PANEL_X = [BODY_X + i * (_PANEL_W + _PANEL_GUT) for i in range(3)]

_SW = 120_000                                   # legend swatch side


def _plot_geom(panel_x: int):
    """(px, py, pw, ph) of a panel chart's pinned inner plot in slide EMU."""
    px = panel_x + int(_PANEL_W * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_H * _PLOT_LAYOUT["y"])
    pw = int(_PANEL_W * _PLOT_LAYOUT["w"])
    ph = int(_CHART_H * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


_GAP_WIDTH = 70


def _bar_centers(px: int, pw: int) -> list[int]:
    return [px + pw * (2 * k + 1) // 8 for k in range(4)]


def _bar_half_w(pw: int) -> int:
    slot = pw / 4
    return int(slot / (1 + _GAP_WIDTH / 100.0) / 2)


# ── Local helpers ────────────────────────────────────────────────────────────
def _exhibit_header() -> str:
    hdr = text_box(
        10, "ExhibitHeader", BODY_X, BODY_Y, BODY_CX, _HDR_H,
        [paragraph([run(_EXHIBIT_HDR, size=DENSE_BODY_10PT, bold=True,
                        color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    rule = connector(11, "ExhibitHeaderRule", BODY_X, BODY_Y + _HDR_H + 20_000,
                     BODY_CX, 0, color=BLACK, width=9_525)
    return hdr + rule


def _hatch_swatch(sp_id: int, x: int, y: int, w: int, h: int) -> str:
    """Legend swatch carrying the residual hatch (text_box is solid-only)."""
    return (f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="KeySwatchHatch"/>'
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
    """Two-row legend grid (4 entries per row) above the panels."""
    col_w = BODY_CX // 4
    parts, sid = [], sp_id0
    for i, (name, fill) in enumerate(_BUCKET_FILLS):
        row, col = divmod(i, 4)
        x = BODY_X + col * col_w
        cy = _LEG_Y + row * _LEG_ROW_H
        sw_y = cy + (_LEG_ROW_H - _SW) // 2
        if fill is None:
            parts.append(_hatch_swatch(sid, x, sw_y, _SW, _SW))
        else:
            parts.append(text_box(
                sid, "KeySwatch", x, sw_y, _SW, _SW,
                [paragraph([run("", size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
                fill=fill, line_color=None, anchor="ctr", insets=INSETS_NONE))
        parts.append(text_box(
            sid + 1, "KeyLabel", x + _SW + 60_000, cy, col_w - _SW - 80_000,
            _LEG_ROW_H,
            [paragraph([run(name, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        sid += 2
    return "".join(parts)


def _panel_chips(sp_id0: int) -> str:
    parts = []
    for i, p in enumerate(_PANELS):
        parts.append(text_box(
            sp_id0 + i, "ClassChip",
            _PANEL_X[i] + (_PANEL_W - _CHIP_W) // 2, _CHIP_Y, _CHIP_W, _CHIP_H,
            [paragraph([run(p["name"], size=DENSE_BODY_10PT, italic=True,
                            color=BLACK, font=FONT)], align="ctr")],
            fill=None, line_color=BLACK, line_width=12_700, anchor="ctr",
            insets=INSETS_NONE))
    return "".join(parts)


def _mids(vals: list[float]) -> list[float]:
    out, cum = [], 0.0
    for v in vals:
        out.append(cum + v / 2)
        cum += v
    return out


def _pct_labels(sp_id0: int) -> str:
    """In-bar % labels (share of that year's TAM) where the segment can hold a
    9pt line; smaller segments stay unlabeled (the legend carries the read)."""
    parts, sid = [], sp_id0
    lbl_w, lbl_h = 460_000, 140_000
    for pi, p in enumerate(_PANELS):
        px, py, pw, ph = _plot_geom(_PANEL_X[pi])
        centers = _bar_centers(px, pw)
        emu_per_b = ph / p["axis_max"]
        for k in range(4):
            total = p["totals"][k]
            if total == 0:
                continue
            col_vals = [p["wt"][b][k] for b in range(8)]
            mids = _mids(col_vals)
            for b in range(8):
                v = col_vals[b]
                if v * emu_per_b < 150_000:
                    continue
                pct = v / total * 100
                y = py + ph - int(mids[b] * emu_per_b)
                fill_hex = _BUCKET_FILLS[b][1]
                dark = fill_hex in (CHART_ACCENT_2, CHART_ACCENT_3, DK)
                parts.append(text_box(
                    sid, "PctLabel", centers[k] - lbl_w // 2, y - lbl_h // 2,
                    lbl_w, lbl_h,
                    [paragraph([run(f"{pct:.0f}%", size=LABEL_9PT,
                                    color=WHITE if dark else BLACK, font=FONT)],
                               align="ctr")],
                    fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
                sid += 1
    return "".join(parts)


def _totals(sp_id0: int) -> str:
    """Float each column's $B total above its bar (9pt bold); em-dash at the
    baseline for Columbia's unfunded years."""
    parts, sid = [], sp_id0
    box_w, box_h, gap = 640_000, 200_000, 22_000
    for pi, p in enumerate(_PANELS):
        px, py, pw, ph = _plot_geom(_PANEL_X[pi])
        centers = _bar_centers(px, pw)
        emu_per_b = ph / p["axis_max"]
        for k in range(4):
            total = p["totals"][k]
            if total == 0:
                parts.append(text_box(
                    sid, "NoFundDash", centers[k] - 110_000,
                    py + ph - 240_000, 220_000, 200_000,
                    [paragraph([run("—", size=LABEL_9PT, color=BLACK, font=FONT)],
                               align="ctr")],
                    fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
            else:
                y_top = py + ph - int(total * emu_per_b)
                parts.append(text_box(
                    sid, "ColTotal", centers[k] - box_w // 2,
                    y_top - gap - box_h, box_w, box_h,
                    [paragraph([run(f"{total:.1f}", size=LABEL_9PT, bold=True,
                                    color=BLACK, font=FONT)], align="ctr")],
                    fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
            sid += 1
    return "".join(parts)


def _col_note(sp_id: int) -> str:
    """Columbia panel note: the class funds biennially, so FY2024 is the only
    full-funding year inside the evidence window."""
    px, py, pw, ph = _plot_geom(_PANEL_X[1])
    return text_box(
        sp_id, "ColNote", px + 30_000, py + 60_000, pw - 60_000, 400_000,
        [paragraph([run("Columbia funds biennially; FY2024 is the only "
                        "full-funding year in the window.",
                        size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    frames = "".join(
        graphic_frame(sp_id=20 + i, name=f"WorktypeByFy{p['name']}",
                      x=_PANEL_X[i], y=_CHART_Y, cx=_PANEL_W, cy=_CHART_H,
                      rId=f"rId{i + 2}")
        for i, p in enumerate(_PANELS))
    return (_exhibit_header() + _legend(30) + _panel_chips(50) + frames
            + _pct_labels(200) + _totals(150) + _col_note(170))


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
