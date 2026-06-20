"""s11_body_annual_cadence - show that the $4.2B average annual TAM is a sizing
convention while actual supplier demand is lumpy, peaking in submarine-driven
FY2024 and in FY2026, where OBBBA mandatory funding and DDG AP/LLTM coincide.

Pattern B: full-width native stacked column (combined supplier TAM by fiscal year,
stacked DDG + submarine), a no-fill units caption above, and three InterpBox cards
below. The per-program split is the live workbook data (DDG z_ChartData section 5
BC + AP/LLTM streams; submarine annual-cadence TAM), and the stacked totals
reproduce the spec's combined FY totals exactly.

Spec: ds_specs/s11_body_annual_cadence.txt (SLIDE 11 - ANNUAL CADENCE).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    CHART_ACCENT_1, CHART_ACCENT_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, BODY_12PT,
)
from deck_core.chart_key import chart_legend

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Sizing"
_BREADCRUMB_TOPIC = "Annual Cadence"
_TOPIC            = "Annual Cadence"
_TAKEAWAY = ("Average annual TAM is a sizing convention; actual supplier demand is "
             "lumpy and peaks in FY2024 and in OBBBA-boosted FY2026.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c Basic Construction and AP/LLTM budget "
            "justification, FY2022–FY2027; (2) Virginia and Columbia annual "
            "procurement profiles; (3) DoD contract announcements and FFATA/FSRS "
            "subaward records; (4) FY 2026 Mandatory Funding Allocation Plan, "
            "PL 119-21 Sec. 20002")

_UNITS = ("Combined supplier TAM by fiscal year, $B; stacked by program. Constant "
          "FY2026 dollars, FY2022–FY2027; incl. OBBBA Sec. 20002 mandatory funding.")


# ── Chart (native stacked column) ────────────────────────────────────────────
# Per-program supplier TAM by FY ($B). DDG = BC stream + AP/LLTM (z_ChartData §5);
# submarine = annual-cadence TAM. DDG + submarine == the combined FY totals
# (2.1 / 2.5 / 6.1 / 2.6 / 6.2 / 5.7). This is a 1-v-1 (two-series) chart, so it
# uses the gray accent1 + blue accent2 pair. Stacking order follows the think-cell
# reference: submarine (accent2, dark navy) is the BASE/lower segment and DDG (accent1,
# gray) is the UPPER cap — the program-driving submarine block reads from the baseline
# up. The centered legend below keeps its DDG-then-Submarine reading order regardless of
# the bottom-up stack order. No segment dividers (reference look), dark-navy axis, 10pt
# regular labels, no native legend/gridlines (a centered legend sits below).
# The inner-plot fractions (pinned via plot_layout on the chart) are reused below to
# float each FY stack total just above its bar — a native stacked column can't carry
# a total data label, so the totals are overlaid as text (think-cell look).
_PLOT_LAYOUT = {"x": 0.075, "y": 0.085, "w": 0.915, "h": 0.78}
_AXIS_MAX = 7.0
_CATEGORIES = ["FY2022", "FY2023", "FY2024", "FY2025", "FY2026", "FY2027"]
_SUB_VALS = [1.833, 1.910, 5.619, 1.903, 4.544, 5.403]            # submarine (base)
_DDG_VALS = [0.271, 0.612, 0.434, 0.650, 1.651, 0.334]            # DDG (upper cap)
# DDG caps too thin to hold an in-bar label: suppress the native label and overlay
# a colored chip instead (think-cell look). FY2022 and FY2027 are too thin.
_DDG_CHIP_PTS = [0, 5]
_FY_TOTALS = [s + d for s, d in zip(_SUB_VALS, _DDG_VALS)]         # DDG + submarine per FY
_FY_TOTAL_LABELS = ["2.1", "2.5", "6.1", "2.6", "6.2", "5.7"]
_CHART = column_chart(
    mode="stacked",
    categories=_CATEGORIES,
    series=[
        {"name": "Submarine", "values": _SUB_VALS,
         "color": CHART_ACCENT_2},                                  # 1D4D68 (accent2, base)
        {"name": "DDG", "values": _DDG_VALS,
         "color": CHART_ACCENT_1,                                   # 79838F (accent1, upper cap)
         "hide_label_points": _DDG_CHIP_PTS},
    ],
    title=None,
    show_legend=False,
    value_axis_format='0.0',
    value_axis_min=0, value_axis_max=7, value_axis_major_unit=1,
    show_gridlines=False,
    seg_line_color=None, axis_line_color="162029",                  # no white dividers (reference look)
    show_value_labels=True, value_label_format='0.0',
    value_label_size_pt=9, value_label_bold=False, cat_label_size_pt=8,
    gap_width=90, cat_header="Fiscal year",
    # Inner plot pinned so the per-FY stack-total overlays (below) land just above
    # each bar top; the top margin is the headroom the tallest total needs.
    plot_layout=_PLOT_LAYOUT,
)
CHARTS: list[dict] = [_CHART]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_CAP_Y, _CAP_H = BODY_Y, 300_000               # units caption (8.5pt italic)
_CHART_Y = _CAP_Y + _CAP_H + 70_000            # 1_741_600
_CARDS_H = 1_180_000
_CARDS_Y = BODY_B - _CARDS_H                    # 4_690_000
_CHART_H = _CARDS_Y - 150_000 - _CHART_Y       # 2_798_400 (bottom 4_540_000)

# Manual color key (replaces the dropped native legend) in a thin band at the
# bottom of the old chart footprint; the frame shrinks by _KEY_H to make room.
_KEY_H, _KEY_GAP = 210_000, 20_000
_CHART_CY = _CHART_H - _KEY_H - _KEY_GAP
_KEY_Y = _CHART_Y + _CHART_CY + _KEY_GAP

# Three InterpBox cards across the full width.
_CARD_GAP = 200_000
_CARD_W   = (BODY_CX - 2 * _CARD_GAP) // 3      # 3_627_454
_CARD_X   = [BODY_X + i * (_CARD_W + _CARD_GAP) for i in range(3)]


# ── Content ──────────────────────────────────────────────────────────────────
_CARDS = [
    ("Submarine procurement drives the cadence baseline.",
     "FY2024 reaches $6.1B and FY2027 $5.7B when Virginia and Columbia Basic "
     "Construction fund together."),
    ("FY2026 is the OBBBA and long-lead spike.",
     "The combined year reaches $6.2B: OBBBA mandatory funding adds two DDG-51s "
     "and a second Virginia boat, while DDG AP/LLTM long-lead peaks at ~$1.2B in "
     "the same year."),
    ("The $4.2B average is a sizing convention.",
     "The six-year average smooths a path from $2.1B in FY2022 to $6.2B in "
     "FY2026; the annual shape reflects procurement cadence, not a steady run-rate."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _units_caption(sp_id: int) -> str:
    return text_box(
        sp_id, "UnitsCaption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(_UNITS, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _interp_card(sp_id: int, x: int, title: str, body: str) -> str:
    """No-fill InterpBox: bold 9pt mini-title over a bulleted 9pt body, so the
    hierarchy reads through bold + bullet rather than a larger parent font."""
    return text_box(
        sp_id, "InterpBox", x, _CARDS_Y, _CARD_W, _CARDS_H,
        [paragraph([run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   space_after=100),
         paragraph([run(body, size=LABEL_9PT, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t", insets=(70_000, 40_000, 70_000, 40_000))


# ── Local helpers (cont.) ────────────────────────────────────────────────────
def _plot_geom():
    """(px, py, pw, ph) of the chart's pinned inner plot in slide EMU, so the
    stack-total and chip overlays land on the rendered bars."""
    px = BODY_X + int(BODY_CX * _PLOT_LAYOUT["x"])
    py = _CHART_Y + int(_CHART_CY * _PLOT_LAYOUT["y"])
    pw = int(BODY_CX * _PLOT_LAYOUT["w"])
    ph = int(_CHART_CY * _PLOT_LAYOUT["h"])
    return px, py, pw, ph


def _bar_center(px: int, pw: int, i: int) -> int:
    return px + pw * (2 * i + 1) // (2 * len(_CATEGORIES))


def _stack_totals(sp_id0: int) -> str:
    """Float each FY stack total just above its bar. A native stacked column can't
    carry a total data label, so overlay them; positions derive from the pinned
    inner plot (_PLOT_LAYOUT) so each label tracks its own bar top."""
    px, py, pw, ph = _plot_geom()
    box_w, box_h, gap = 760_000, 230_000, 26_000
    parts = []
    for i, (total, label) in enumerate(zip(_FY_TOTALS, _FY_TOTAL_LABELS)):
        y_top = py + int(ph * (1 - total / _AXIS_MAX))
        parts.append(text_box(
            sp_id0 + i, "StackTotal", _bar_center(px, pw, i) - box_w // 2,
            y_top - gap - box_h, box_w, box_h,
            [paragraph([run(label, size=LABEL_9PT, color=BLACK,
                            font=FONT)], align="ctr")],
            fill=None, line_color=None, anchor="b", insets=INSETS_NONE))
    return "".join(parts)


def _chips(sp_id0: int) -> str:
    """Overlay a small colored chip for each DDG cap too thin for an in-bar label
    (those in _DDG_CHIP_PTS, whose native label is suppressed). The chip is filled
    with the DDG accent so it stays tied to its segment color (white label on it),
    snug around the 9pt number and sitting at the bar top."""
    px, py, pw, ph = _plot_geom()
    cw, ch, overlap = 215_000, 112_000, 10_000
    parts = []
    for k, i in enumerate(_DDG_CHIP_PTS):
        top = _SUB_VALS[i] + _DDG_VALS[i]                  # bar top (running total)
        y_top = py + int(ph * (1 - top / _AXIS_MAX)) - overlap
        parts.append(text_box(
            sp_id0 + k, "SegChip", _bar_center(px, pw, i) - cw // 2, y_top, cw, ch,
            [paragraph([run(f"{_DDG_VALS[i]:.1f}", size=LABEL_9PT, color=WHITE,
                            font=FONT)], align="ctr")],
            fill=CHART_ACCENT_1, line_color="none", anchor="ctr", insets=INSETS_NONE))
    return "".join(parts)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = _units_caption(10)
    chart = graphic_frame(sp_id=20, name="AnnualCadenceStackedColumn",
                          x=BODY_X, y=_CHART_Y, cx=BODY_CX, cy=_CHART_CY, rId="rId2")
    totals = _stack_totals(60)
    chips = _chips(70)
    legend = chart_legend(
        50, [("DDG", CHART_ACCENT_1), ("Submarine", CHART_ACCENT_2)],
        cy=_KEY_Y + _KEY_H // 2, x_center=BODY_X + BODY_CX // 2)
    cards = "".join(
        _interp_card(30 + i, _CARD_X[i], title, body)
        for i, (title, body) in enumerate(_CARDS))
    return caption + chart + totals + chips + legend + cards


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
