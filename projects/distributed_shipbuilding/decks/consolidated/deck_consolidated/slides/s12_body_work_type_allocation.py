"""s12_body_work_type_allocation - rank the seven physical work-type buckets of the
combined supplier pool, stacked by program, and keep the $653M unresolved residual
visible but separate from the named-bucket ranking.

Pattern A: a native ranked stacked column (left) with full bucket names on the axis,
a no-fill commentary box (right), and a units caption above. The former dark focal
strip is gone: per the current spec the slide closes on a no-fill italic transition
line with a thin right-pointing rule that bridges to the where-to-play view, and the
space that frees at the bottom is intentional breathing room, not a gap to backfill.

Named buckets are stacked by program (submarine accent2 1D4D68 base, DDG accent1 79838F
gray upper); the per-program splits are the fused workbook values (z_ChartData DDG section
6 + submarine section 5) and sum to the combined bucket totals to the dollar
(1353/710/633/375/206/162/102). The residual is a single separated accent3 486D82 column
outside the named-bucket group.

Spec: ds_specs/s12_body_work_type_allocation.txt (SLIDE 12 - WORK-TYPE TAXONOMY).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    CHART_ACCENT_1, CHART_ACCENT_2, CHART_ACCENT_3,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, BODY_12PT,
)
from deck_core.chart_key import chart_legend

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Sizing"
_BREADCRUMB_TOPIC = "Work-Type Mix"
_TOPIC            = "Work-Type Mix"
_TAKEAWAY = ("Electrical power, piping, and structural fabrication lead the combined "
             "pool; a $653M residual stays separate.")
_SOURCES = ("Sources: (1) FFATA/FSRS subaward records and the operating-entity "
            "supplier registry, FY2017–FY2026; (2) Navy SCN and P-5c Basic "
            "Construction and AP/LLTM budget justification, FY2022–FY2027; "
            "(3) parent-prime PIID program-scope attribution")

_UNITS = ("Combined average annual TAM by work type, $M; stacked by program. "
          "Residual shown separate. Constant FY2026 dollars.")

_EVID_95  = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)
_TRANS_95 = 950   # 9.5pt: transition line (italic)


# ── Chart (native ranked stacked column) ─────────────────────────────────────
# Seven named buckets in descending combined order, each stacked submarine (base,
# accent2 1D4D68) + DDG (upper, accent1 79838F gray). Residual is a third series present
# only in the last slot, so it renders as one separate accent3 486D82 column outside the
# named-bucket ranking. Colors match the think-cell reference (chart5): a consistent
# program palette across the deck — submarine navy, DDG gray on both this slide and Annual
# Cadence (s11) — with the residual on its own mid-slate. Plus white 0.75pt dividers,
# dark-navy axis, 8pt labels, no native legend/gridlines (a manual key below).
_CATEGORIES = [
    "Electrical and power",
    "Piping, valves, and pumps",
    "Structural fabrication and pre-outfit",
    "Machining",
    "Coatings and insulation",
    "Castings and forgings",
    "HVAC and ventilation",
    "Residual",
]
_SUB = [1315, 675, 597, 116, 189, 151, 61, None]   # submarine base (sums verified)
_DDG = [38, 35, 36, 259, 17, 11, 41, None]          # DDG upper
_RES = [None, None, None, None, None, None, None, 653]
# DDG caps too thin to hold an in-bar label: suppress the native label and overlay
# a colored chip instead (think-cell look). Every bucket except Machining (225, the
# only DDG cap with room) gets a chip.
_DDG_CHIP_PTS = [0, 1, 2, 4, 5, 6]

# Inner-plot fractions (pinned via plot_layout on the chart) reused to float each
# bucket's stack total just above its bar — a native stacked column can't carry a
# total data label, so the totals are overlaid as text (think-cell look).
_PLOT_LAYOUT = {"x": 0.06, "y": 0.085, "w": 0.93, "h": 0.78}
_AXIS_MAX = 1500
_BUCKET_TOTALS = [(s or 0) + (d or 0) + (r or 0)
                  for s, d, r in zip(_SUB, _DDG, _RES)]   # 1353/710/.../102/653
_BUCKET_TOTAL_LABELS = [f"{t:,}" for t in _BUCKET_TOTALS]

_CHART = column_chart(
    mode="stacked",
    categories=_CATEGORIES,
    series=[
        {"name": "Submarine", "values": _SUB, "color": CHART_ACCENT_2},  # 1D4D68 base (accent2)
        {"name": "DDG", "values": _DDG, "color": CHART_ACCENT_1,         # 79838F gray upper (accent1)
         "hide_label_points": _DDG_CHIP_PTS},
        {"name": "Residual", "values": _RES, "color": CHART_ACCENT_3},   # 486D82 separate (accent3)
    ],
    title=None,
    show_legend=False,
    value_axis_format='#,##0',
    value_axis_min=0, value_axis_max=1500, value_axis_major_unit=100,
    show_gridlines=False,
    seg_line_color=None, axis_line_color="162029",                  # no white dividers (reference look)
    show_value_labels=True, value_label_format='#,##0',
    value_label_size_pt=9, value_label_bold=False, cat_label_size_pt=8,
    gap_width=60, cat_header="Work type",
    # Inner plot pinned so the per-bucket stack-total overlays (below) land just
    # above each bar top; the top margin is headroom for the tallest total label.
    plot_layout=_PLOT_LAYOUT,
)
CHARTS: list[dict] = [_CHART]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_CAP_Y, _CAP_H = BODY_Y, 300_000                # units caption (8.5pt italic)
_CHART_Y = _CAP_Y + _CAP_H + 70_000             # 1_741_600

_TRANS_H = 360_000                              # forward bridge line
_TRANS_Y = BODY_B - _TRANS_H                    # 5_510_000
_CHART_H = (_TRANS_Y - 240_000) - _CHART_Y      # 3_528_400  (breathing room above bridge)

# Manual color key (replaces the dropped native legend) below the chart; the
# frame shrinks by _KEY_H so the key sits inside the old chart footprint.
_KEY_H, _KEY_GAP = 210_000, 20_000
_CHART_CY = _CHART_H - _KEY_H - _KEY_GAP
_KEY_Y = _CHART_Y + _CHART_CY + _KEY_GAP

_CHART_W = 7_050_000                            # ~7.7in (Pattern A)
_GAP_CC  = 280_000
_COMM_X  = BODY_X + _CHART_W + _GAP_CC          # 7_783_079
_COMM_W  = BODY_R - _COMM_X                     # 3_952_362 (~4.32in)
_COMM_Y  = _CHART_Y
_COMM_H  = _CHART_H
_COMM_INSETS = (137_160, 30_000, 137_160, 30_000)


# ── Content ──────────────────────────────────────────────────────────────────
_FINDINGS = [
    ("Three buckets dominate the named supplier pool.",
     "Electrical power, piping, and structural fabrication total ~$2.7B of the "
     "$4.2B TAM, led by $1,353M of electrical and power work."),
    ("Entity-resolved classification shifts the mix, not the TAM headline.",
     "Machining rises to $375M once VLS launcher-cell machining and LM2500 "
     "propulsion machinery are assigned to physical work type; combat electronics "
     "leave the supplier base."),
    ("Residual remains visible outside named-bucket SAM.",
     "$653M of supplier dollars lacks recoverable bucket evidence, so it stays in "
     "TAM while remaining outside broad SAM."),
]

_TRANS_TEXT = ("The component pool is not one thing; entry, qualification, and "
               "incumbent dynamics differ sharply by work type.")


# ── Local helpers ────────────────────────────────────────────────────────────
def _units_caption(sp_id: int) -> str:
    return text_box(
        sp_id, "UnitsCaption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(_UNITS, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _commentary(sp_id: int) -> str:
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=90))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 260)))
    return text_box(sp_id, "Commentary", _COMM_X, _COMM_Y, _COMM_W, _COMM_H,
                    paras, fill=None, line_color=None, anchor="t",
                    insets=_COMM_INSETS)


def _transition(sp_id: int) -> str:
    """No-fill italic forward bridge + a thin right-pointing rule (not a dark strip)."""
    text = text_box(
        sp_id, "TransitionLine", BODY_X, _TRANS_Y, 9_200_000, _TRANS_H,
        [paragraph([run(_TRANS_TEXT, size=_TRANS_95, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    rule = connector(
        sp_id + 1, "BridgeRule", 9_750_000, _TRANS_Y + _TRANS_H // 2,
        BODY_R - 9_750_000, 0, color=BLACK, width=9_525, arrow=True)
    return text + rule


def _plot_geom():
    """(px, py, pw, ph) of the chart's pinned inner plot in slide EMU, so the
    stack-total and chip overlays land on the rendered bars."""
    px = BODY_X + int(_CHART_W * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_CY * _PLOT_LAYOUT["y"])
    pw = int(_CHART_W * _PLOT_LAYOUT["w"])
    ph = int(_CHART_CY * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _bar_center(px: int, pw: int, i: int) -> int:
    return px + pw * (2 * i + 1) // (2 * len(_BUCKET_TOTALS))


def _stack_totals(sp_id0: int) -> str:
    """Float each bucket's stack total just above its bar; positions derive from the
    pinned inner plot (_PLOT_LAYOUT) so each label tracks its own bar top."""
    px, py, pw, ph = _plot_geom()
    box_w, box_h, gap = 760_000, 210_000, 22_000
    parts = []
    for i, (total, label) in enumerate(zip(_BUCKET_TOTALS, _BUCKET_TOTAL_LABELS)):
        y_top = py + int(ph * (1 - total / _AXIS_MAX))
        parts.append(text_box(
            sp_id0 + i, "StackTotal", _bar_center(px, pw, i) - box_w // 2,
            y_top - gap - box_h, box_w, box_h,
            [paragraph([run(label, size=LABEL_9PT, color=BLACK,
                            font=FONT)], align="ctr")],
            fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
    return "".join(parts)


def _chips(sp_id0: int) -> str:
    """Overlay a small gray DDG chip for each cap too thin for an in-bar label (those
    in _DDG_CHIP_PTS, whose native label is suppressed). Filled with the DDG accent so
    it stays tied to its segment color (white label); snug around the 9pt number."""
    px, py, pw, ph = _plot_geom()
    cw, ch, overlap = 215_000, 112_000, 10_000
    parts = []
    for k, i in enumerate(_DDG_CHIP_PTS):
        top = _SUB[i] + _DDG[i]                            # bar top (sub + DDG cap)
        y_top = py + int(ph * (1 - top / _AXIS_MAX)) - overlap
        parts.append(text_box(
            sp_id0 + k, "SegChip", _bar_center(px, pw, i) - cw // 2, y_top, cw, ch,
            [paragraph([run(f"{_DDG[i]:,}", size=LABEL_9PT, color=WHITE,
                            font=FONT)], align="ctr")],
            fill=CHART_ACCENT_1, line_color="none", anchor="ctr", insets=INSETS_NONE))
    return "".join(parts)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = _units_caption(10)
    chart = graphic_frame(sp_id=20, name="WorkTypeRankedStackedColumn",
                          x=BODY_X, y=_CHART_Y, cx=_CHART_W, cy=_CHART_CY,
                          rId="rId2")
    totals = _stack_totals(60)
    chips = _chips(70)
    commentary = _commentary(30)
    transition = _transition(40)
    # Legend at the top of the chart (reference places it over the short right-side
    # bars), centered on the chart's mid-x; 12pt with rectangular swatches.
    legend = chart_legend(
        50, [("Submarine", CHART_ACCENT_2), ("DDG", CHART_ACCENT_1),
             ("Residual", CHART_ACCENT_3)],
        cy=_CHART_Y + 150_000, x_center=BODY_X + _CHART_W // 2)
    return caption + chart + totals + chips + legend + commentary + transition


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
