"""fr2_body_worktype_by_program - front-row slide 2: outsourced Basic
Construction spend re-cut to one stacked column per program / submarine class
(DDG-51, Virginia, Columbia), segmented by the seven work-type buckets with
each column's unresolved residual riding the stack as a hatched cap, and the
M4 classifier methodology condensed into a right-side ledger (so the slide
self-contains the method instead of pointing at the appendix).

The chart is a NATIVE stacked column: eight series (seven solid buckets + the
a:pattFill residual), white think-cell dividers, no native legend or value-axis
labels. The plot is pinned right-of-center (plot_layout) so the chart zone's
left strip holds a vertical color key and the DDG leader-label ladder. Labels
are mixed in-bar / leader by segment height: DDG ladders its four thin
segments left of its bar; Virginia leader-labels its three thin segments
(machining, castings, HVAC) into the Virginia-Columbia gap; Columbia hangs its
five thin top segments on an even-pitch ladder right of its bar. Column totals
float above each bar; positions derive from the pinned inner plot, s03/s12
style.

Data: FY2022-FY2027 cumulative, constant FY2026 $B, OBBBA Sec. 20002 mandatory
awards included; the 2026-06-10 restates applied (announced-POP class-vintage
coefficients; gated FY22-25 per-class per-FY work-type vectors). Per-bucket
values are the program workbooks' SAM Build allocations (annual TAM x per-FY
modeled share; DDG §3b, submarines §4a/§4b per class), mirrored in
workbook_consolidated z_ChartData_OutsourcedBC §3. Each column sums to its
supplier TAM; DDG = the s03 walk endpoint (6.4217), Virginia + Columbia
(13.6268 + 4.5071) = the submarine endpoint (18.1338). Bar labels are $B to
one decimal; small rounding artifacts vs the totals are accepted (s03
precedent).
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
    BODY_X, BODY_Y, BODY_B, BODY_CX,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3, CHART_ACCENT_4,
    CHART_ACCENT_5, CHART_ACCENT_6,
    BLUE_1, GRAY_1, GRAY_2,
    BLACK, WHITE, DK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Executive Summary"
_BREADCRUMB_TOPIC = "Supplier TAM and SAM"
_TOPIC            = "Outsourced Basic Construction Spend by Work Type"
_TAKEAWAY = ("Electrical power leads the ~$18.1B submarine pool; machining "
             "leads the ~$6.4B DDG-51 pool.")
_SOURCES = ("Sources: Navy SCN P-5c / P-40 budget justification, FY22–FY27, and "
            "PB27 FYDP outyears (FY28–FY31); FY26, PL 119-21 Sec. 20002; PB27 SCN, "
            "Columbia P-10 Strategic Outsourcing narrative; OUSD(C) Green Book "
            "Procurement deflators; Navy Shipbuilding Plan; PB27 SCN Exhibit P-10, "
            "LI 2122 (AP/LLTM Ship Construction EOQ); FFATA/FSRS subaward records, "
            "yard-prime construction PIIDs, FY22–FY25 action years (work-type shares)")

_EXHIBIT_HDR = ("Outsourced Basic Construction Spend by Work Type "
                "($B, cumulative FY22–FY27, FY26 $)")

_EVID_95 = 950   # 9.5pt: methodology findings under the ledger


# ── Chart data (cumulative FY2022-FY2027 constant FY2026 $B, exact floats) ───
# (bucket, DDG-51, Virginia, Columbia, fill) - stack order base -> top; the
# residual cap is hatched (no solid fill). Values = z_ChartData_OutsourcedBC §3
# = SAM Build allocations (per class for the submarines).
_BUCKETS = [
    ("Electrical and power",                  0.687840132, 3.579611972, 2.015264257, CHART_ACCENT_2),
    ("Piping, valves, and pumps",             0.603915665, 2.79263306,  0.918962976, CHART_ACCENT_3),
    ("Structural fabrication and pre-outfit", 0.37146878,  2.925105325, 0.691126691, CHART_ACCENT_4),
    ("Machining",                             2.260781875, 0.6001458,   0.10813464,  CHART_ACCENT_5),
    ("Coatings and insulation",               0.009666927, 0.894591879, 0.06840629,  CHART_ACCENT_6),
    ("Castings and forgings",                 0.146559104, 0.607109542, 0.178717817, CHART_ACCENT_1),
    ("HVAC and ventilation",                  0.984150038, 0.104599769, 0.086917623, DK),
    ("Residual",                              1.357347159, 2.122962685, 0.439556207, None),
]
_HATCH = {"prst": "ltUpDiag", "fg": CHART_ACCENT_1, "bg": WHITE}

_DDG_VALS = [b[1] for b in _BUCKETS]
_VA_VALS = [b[2] for b in _BUCKETS]
_COL_VALS = [b[3] for b in _BUCKETS]
_DDG_TOTAL = sum(_DDG_VALS)            # 6.4217 (ties to the s03 walk endpoint)
_VA_TOTAL = sum(_VA_VALS)              # 13.6268
_COL_TOTAL = sum(_COL_VALS)            # 4.5071 (Va + Col = the sub endpoint)

# Segments too thin for an in-bar 9pt label (< ~0.64 $B at the 0-15 axis), per
# column: DDG ladders left, Virginia leader-labels into the Va-Col gap,
# Columbia ladders right.
_DDG_THIN = [1, 2, 4, 5]               # piping, structural, coatings, castings
_VA_THIN = [3, 5, 6]                   # machining, castings, HVAC
_COL_THIN = [3, 4, 5, 6, 7]            # machining .. residual

_AXIS_MAX = 15
_GAP_WIDTH = 65          # % gap between columns (fat think-cell bars)


def _series() -> list[dict]:
    out = []
    for i, (name, d, v, cl, fill) in enumerate(_BUCKETS):
        spec: dict = {"name": name, "values": [d, v, cl]}
        if fill is None:
            spec["pattern"] = _HATCH
        else:
            spec["color"] = fill
        hide = [j for j, thin in enumerate([_DDG_THIN, _VA_THIN, _COL_THIN])
                if i in thin]
        if len(hide) == 3:
            spec["hide_labels"] = True
        elif hide:
            spec["hide_label_points"] = hide
        out.append(spec)
    return out


_PLOT_LAYOUT = {"x": 0.30, "y": 0.05, "w": 0.60, "h": 0.84}

_CHART = column_chart(
    mode="stacked",
    categories=["DDG-51", "Virginia", "Columbia"],
    series=_series(),
    title=None,
    show_legend=False,
    value_axis_format='0.0',
    value_label_format='0.0',
    value_label_size_pt=9,
    value_label_bold=False,
    value_axis_min=0, value_axis_max=_AXIS_MAX,
    show_value_axis_labels=False,        # every segment is annotated directly
    show_gridlines=False,
    seg_line_color=WHITE, seg_line_width=9_525,   # think-cell dividers
    axis_line_color="162029",
    show_cat_labels=True, cat_label_size_pt=10,
    gap_width=_GAP_WIDTH, cat_header="Program",
    # Plot pinned right-of-center: the left strip inside the chart zone carries
    # the vertical color key and the DDG leader-label ladder; the right margin
    # holds the Columbia ladder.
    plot_layout=_PLOT_LAYOUT,
)
CHARTS: list[dict] = [_CHART]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Left chart zone (exhibit header, key, ladder, chart) + right methodology ledger.
_TBL_COL_W = [1_350_000, 2_850_000]
_TBL_W = sum(_TBL_COL_W)
_TBL_GUT = 250_000
_CHART_ZONE_W = BODY_CX - _TBL_W - _TBL_GUT     # 6_832_362
_TBL_X = BODY_X + _CHART_ZONE_W + _TBL_GUT      # ledger right edge lands on BODY_R

_HDR_H = 220_000                                # exhibit header + rule under it
_CHART_Y = BODY_Y + _HDR_H + 80_000             # 1_671_600
_CHART_H = BODY_B - _CHART_Y                    # 4_198_400


def _plot_geom():
    """(px, py, pw, ph) of the chart's pinned inner plot in slide EMU."""
    px = BODY_X + int(_CHART_ZONE_W * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_H * _PLOT_LAYOUT["y"])
    pw = int(_CHART_ZONE_W * _PLOT_LAYOUT["w"])
    ph = int(_CHART_H * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _bar_geom():
    """Per-column (center_x, bar_width): three category slots across the plot."""
    px, _, pw, _ = _plot_geom()
    slot = pw // 3
    bar_w = int(slot / (1 + _GAP_WIDTH / 100.0))
    return [px + slot // 2 + slot * i for i in range(3)], bar_w


def _y_of(level: float) -> int:
    """Slide y of a $B level on the pinned plot."""
    _, py, _, ph = _plot_geom()
    return py + ph - int(ph * level / _AXIS_MAX)


def _mids(vals: list[float]) -> list[float]:
    """Running-stack segment midpoints ($B) for one column."""
    out, cum = [], 0.0
    for v in vals:
        out.append(cum + v / 2)
        cum += v
    return out


# ── Local helpers ────────────────────────────────────────────────────────────
def _zone_header(sp_id: int, x: int, w: int, text: str) -> str:
    """Bold 10pt zone header with a thin rule under it (s03 exhibit idiom)."""
    hdr = text_box(
        sp_id, "ZoneHeader", x, BODY_Y, w, _HDR_H,
        [paragraph([run(text, size=DENSE_BODY_10PT, bold=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    rule = connector(sp_id + 1, "ZoneHeaderRule", x, BODY_Y + _HDR_H + 20_000,
                     w, 0, color=BLACK, width=9_525)
    return hdr + rule


def _hatch_swatch(sp_id: int, x: int, y: int, w: int, h: int) -> str:
    """Key swatch carrying the chart's residual hatch. text_box() fills are
    solid-only, so this is a hand-built <p:sp> with the same a:pattFill."""
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


_KEY_Y0 = 1_960_000        # key top; the strip above the short DDG bar is open
_KEY_PITCH = 170_000
_SW = 120_000              # swatch side


def _key(sp_id0: int) -> str:
    """Vertical 8-entry color key in the chart zone's left strip, listed in the
    bucket (z_ChartData_OutsourcedBC §3) order; the residual swatch carries the
    hatch."""
    parts = []
    for i, (name, _d, _v, _cl, fill) in enumerate(_BUCKETS):
        cy = _KEY_Y0 + i * _KEY_PITCH
        sw_y = cy + (150_000 - _SW) // 2
        if fill is None:
            parts.append(_hatch_swatch(sp_id0 + 2 * i, BODY_X, sw_y, _SW, _SW))
        else:
            parts.append(text_box(
                sp_id0 + 2 * i, "KeySwatch", BODY_X, sw_y, _SW, _SW,
                [paragraph([run("", size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
                fill=fill, line_color=None, anchor="ctr", insets=INSETS_NONE))
        parts.append(text_box(
            sp_id0 + 2 * i + 1, "KeyLabel", BODY_X + _SW + 60_000, cy,
            2_450_000, 150_000,
            [paragraph([run(name, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
    return "".join(parts)


# DDG leader ladder: the four thin DDG values on an even pitch up from the plot
# bottom, left of the DDG bar. Strict per-segment y collapses (piping/structural
# centers sit close), so labels take the ladder and a two-piece elbow leader
# walks each one back to its true segment center; the thin indices ascend the
# stack and the ladder ascends with them, so leaders cannot cross.
_LADDER_PITCH = 160_000
_LBL_W, _LBL_H = 420_000, 150_000
_GAP_LBL_W = 360_000     # narrower labels for the Virginia gap leaders


def _ddg_ladder(lbl_id0: int, ln_id0: int) -> str:
    centers, bar_w = _bar_geom()
    bar_left = centers[0] - bar_w // 2
    _, py, _, ph = _plot_geom()
    plot_bottom = py + ph
    lbl_right = bar_left - 320_000
    mids = _mids(_DDG_VALS)
    parts = []
    for k, i in enumerate(_DDG_THIN):
        y_seg = _y_of(mids[i])
        y_lab = plot_bottom - _LADDER_PITCH * k - 80_000
        parts.append(text_box(
            lbl_id0 + k, "DdgLadderLabel", lbl_right - _LBL_W, y_lab - _LBL_H // 2,
            _LBL_W, _LBL_H,
            [paragraph([run(f"{_DDG_VALS[i]:.1f}", size=LABEL_9PT, color=BLACK,
                            font=FONT)], align="r")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        parts.append(connector(ln_id0 + 2 * k, "DdgLeaderTick",
                               bar_left - 60_000, y_seg, 60_000, 0,
                               color="162029", width=6_350))
        parts.append(connector(ln_id0 + 2 * k + 1, "DdgLeaderElbow",
                               lbl_right + 12_000, y_lab,
                               (bar_left - 60_000) - (lbl_right + 12_000),
                               y_seg - y_lab,
                               color="162029", width=6_350))
    return "".join(parts)


def _va_leaders(lbl_id0: int, ln_id0: int) -> str:
    """Virginia's three thin segments, leader-labeled into the Virginia-Columbia
    gap; castings and HVAC centers sit closer than a 9pt line, so those two
    spread to a 150k minimum pitch about their mean."""
    centers, bar_w = _bar_geom()
    bar_right = centers[1] + bar_w // 2
    lbl_left = bar_right + 100_000
    mids = _mids(_VA_VALS)
    y_true = {i: _y_of(mids[i]) for i in _VA_THIN}
    y_lab = dict(y_true)
    if abs(y_true[5] - y_true[6]) < 150_000:
        mean = (y_true[5] + y_true[6]) // 2
        y_lab[5], y_lab[6] = mean + 75_000, mean - 75_000
    parts = []
    for k, i in enumerate(_VA_THIN):
        parts.append(text_box(
            lbl_id0 + k, "VaLeaderLabel", lbl_left, y_lab[i] - _LBL_H // 2,
            _GAP_LBL_W, _LBL_H,
            [paragraph([run(f"{_VA_VALS[i]:.1f}", size=LABEL_9PT, color=BLACK,
                            font=FONT)], align="l")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        parts.append(connector(ln_id0 + 2 * k, "VaLeaderTick",
                               bar_right, y_true[i], 60_000, 0,
                               color="162029", width=6_350))
        parts.append(connector(ln_id0 + 2 * k + 1, "VaLeaderElbow",
                               bar_right + 60_000, y_true[i],
                               (lbl_left - 12_000) - (bar_right + 60_000),
                               y_lab[i] - y_true[i],
                               color="162029", width=6_350))
    return "".join(parts)


def _col_ladder(lbl_id0: int, ln_id0: int) -> str:
    """Columbia's five thin top segments (machining .. residual) on an
    even-pitch ladder right of its bar: their true centers span only ~0.6 $B,
    so labels descend from the highest (residual) at ladder pitch with elbow
    leaders back to the true centers. Mid order is monotonic, so no crossing."""
    centers, bar_w = _bar_geom()
    bar_right = centers[2] + bar_w // 2
    lbl_left = bar_right + 320_000
    mids = _mids(_COL_VALS)
    order = sorted(_COL_THIN, key=lambda i: mids[i], reverse=True)
    y_top_lab = _y_of(mids[order[0]])
    parts = []
    for k, i in enumerate(order):
        y_seg = _y_of(mids[i])
        y_lab = y_top_lab + _LADDER_PITCH * k
        parts.append(text_box(
            lbl_id0 + k, "ColLadderLabel", lbl_left, y_lab - _LBL_H // 2,
            _LBL_W, _LBL_H,
            [paragraph([run(f"{_COL_VALS[i]:.1f}", size=LABEL_9PT, color=BLACK,
                            font=FONT)], align="l")],
            fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE))
        parts.append(connector(ln_id0 + 2 * k, "ColLeaderTick",
                               bar_right, y_seg, 60_000, 0,
                               color="162029", width=6_350))
        parts.append(connector(ln_id0 + 2 * k + 1, "ColLeaderElbow",
                               bar_right + 60_000, y_seg,
                               (lbl_left - 12_000) - (bar_right + 60_000),
                               y_lab - y_seg,
                               color="162029", width=6_350))
    return "".join(parts)


def _stack_totals(sp_id0: int) -> str:
    """Float each column's total just above its bar top (9pt bold reads apart
    from the regular-weight segment labels by position and weight)."""
    centers, _ = _bar_geom()
    box_w, box_h, gap = 760_000, 210_000, 22_000
    parts = []
    for i, total in enumerate([_DDG_TOTAL, _VA_TOTAL, _COL_TOTAL]):
        y_top = _y_of(total)
        parts.append(text_box(
            sp_id0 + i, "StackTotal", centers[i] - box_w // 2,
            y_top - gap - box_h, box_w, box_h,
            [paragraph([run(f"{total:.1f}", size=LABEL_9PT, bold=True,
                            color=BLACK, font=FONT)], align="ctr")],
            fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
    return "".join(parts)


# ── Methodology ledger (condensed M4 classifier, right panel) ────────────────
# The appendix classification ledger (appendix_sam_classification_field_audit)
# compressed to Stage | Rule applied; row fills mirror the appendix highlights
# (entity / output rows blue, role filter and residual gray).
_LED_HEADERS = ["Stage", "Rule applied"]
_LED_BODY = [
    ("1. Award pull",
     "Pull FFATA/FSRS subawards; collect visible supplier evidence (mix, not TAM)."),
    ("2. PIID gate",
     "Gate to yard construction PIIDs per program (BIW / Ingalls; GDEB); GFE "
     "chains drop out."),
    ("3. Entity resolution",
     "Resolve the operating entity paid (UEI), not the parent brand."),
    ("4. Role filter",
     "Drop non-supplier / non-component roles from the addressable base."),
    ("5. Work-type assign",
     "First clean match wins one work-type home (vendor registry, NAICS-4)."),
    ("6. Residual discipline",
     "Keep unresolved dollars in the addressable base; residual dilutes named shares."),
    ("7. Share output",
     "Bucket dollars over the addressable base set the modeled work-type and "
     "residual shares, per class and per FY; feeds the allocation step."),
]
# No row fills - the manager's draft strips the blue/gray stage tints.
_LED_ROW_FILL: dict[int, str] = {}

_LED_ROWS_TEXT = [_LED_HEADERS] + [[s, r] for s, r in _LED_BODY]
_LED_ROW_H = estimate_row_heights(_LED_ROWS_TEXT, _TBL_COL_W,
                                  size_pt=9.0, header_size_pt=9.0,
                                  min_row_h=274_320)

_FINDINGS = [
    # No evidence bullet on the first finding: stages 2-4 of the ledger above
    # already carry the gate / UEI / role-filter detail.
    ("The classifier is entity-first and role-first.",
     None),
    ("Share window: FY2022–FY2025 yard subawards, per class.",
     None),
    ("Residual is unclassified award spend.",
     "Unresolved dollars stay in TAM but outside SAM: the hatched cap on each "
     "column's stack."),
]


def _ledger(sp_id: int) -> str:
    rows = []
    n = len(_LED_ROWS_TEXT)
    for ri, (stage, rule) in enumerate([tuple(_LED_HEADERS)] + list(_LED_BODY)):
        hdr = ri == 0
        last = ri == n - 1
        if hdr:
            border = {"B": {"color": BLACK, "width": 19_050}}
        elif not last:
            border = {"B": {"color": BLACK, "width": 12_700}}
        else:
            border = {"B": "none"}
        fill = None if hdr else _LED_ROW_FILL.get(ri)
        rows.append(trow([
            tcell(stage, fill=fill, color=BLACK, bold=True,
                  size=950 if hdr else 850, align="l", anchor="ctr",
                  borders=border),
            tcell(rule, fill=fill, color=BLACK, bold=hdr,
                  size=950 if hdr else 850, align="l", anchor="ctr",
                  borders=border),
        ], h=_LED_ROW_H[ri]))
    return table(sp_id, "ClassifierLedger", _TBL_X, _CHART_Y, _TBL_W,
                 sum(_LED_ROW_H), col_widths=_TBL_COL_W, rows=rows)


def _findings(sp_id: int) -> str:
    y = _CHART_Y + sum(_LED_ROW_H) + 280_000
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=(0 if last else 180) if evidence is None else 90))
        if evidence is not None:
            paras.append(paragraph(
                [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
                bullet=True, space_after=(0 if last else 180)))
    return text_box(sp_id, "MethodFindings", _TBL_X, y, _TBL_W, BODY_B - y,
                    paras, fill=None, line_color=None, anchor="t",
                    insets=INSETS_NONE)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    headers = (_zone_header(10, BODY_X, _CHART_ZONE_W, _EXHIBIT_HDR)
               + _zone_header(12, _TBL_X, _TBL_W, "Methodology"))
    chart = graphic_frame(sp_id=20, name="WorkTypeByProgramStackedColumn",
                          x=BODY_X, y=_CHART_Y, cx=_CHART_ZONE_W, cy=_CHART_H,
                          rId="rId2")
    key = _key(30)
    ladder = _ddg_ladder(50, 60)
    va = _va_leaders(85, 90)
    col = _col_ladder(140, 150)
    totals = _stack_totals(80)
    return (headers + chart + key + ladder + va + col + totals
            + _ledger(110) + _findings(120))


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
