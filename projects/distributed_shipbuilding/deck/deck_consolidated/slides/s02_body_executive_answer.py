"""s02_body_executive_answer - the deck's one-page answer: a fused supplier
TAM/SAM headline carried by two hero KPI cards, four program/scope support cards,
a compact stacked-vs-comparison column that confirms (does not compete with) the
KPIs, a two-finding commentary rail, and one focal callout.

Layout: a top no-fill qualifier line; two BLUE_5 hero KPI cards (the only 24pt
values on the slide); a four-across support-card row in program/scope hierarchy;
a compact column zone (units caption + 14pt total labels + native stacked column)
on the left with the commentary rail on the right; a full-width BLUE_5 focal
callout strip at the bottom.

The chart is a native stacked column with two categories ("Combined supplier TAM"
stacked submarine + DDG, and "Broad component SAM" as a comparison column). Per
the spec's fit behavior, segment value labels are off and the column totals are
shown as 14pt overlay labels above each column, with a subordinate color key below.
Think-cell look: accent fills, white 0.75pt segment dividers, dark-navy axis, no
native legend/gridlines. (The BLUE_* hero/support cards keep the deck palette; only
the chart fills switch to the chart accent palette.)

Spec: ds_specs/s02_body_executive_answer.txt (SLIDE 02 - EXECUTIVE ANSWER).
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
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    CHART_ACCENT_2, CHART_ACCENT_3, CHART_ACCENT_4,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT, CAP_12PT, BODY_12PT,
    RIBBON_KPI_18PT, ANSWER_KPI_24PT,
)
from deck_core.chart_key import chart_legend

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Executive Summary"
_BREADCRUMB_TOPIC = "Supplier TAM and SAM"
_TOPIC            = "Supplier TAM and SAM"
_TAKEAWAY = ("Combined supplier opportunity is ~$4.2B per year, with ~$3.5B "
             "addressable as broad component SAM.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c Basic Construction and AP/LLTM budget "
            "justification, FY2022–FY2027; (2) DoD place-of-performance award corpus "
            "and parent-prime PIID scope; (3) FFATA/FSRS subaward records and the "
            "operating-entity supplier registry; (4) FY 2026 Mandatory Funding "
            "Allocation Plan, PL 119-21 Sec. 20002")

_QUALIFIER = ("FY2022–FY2027 model-period averages, annualized; constant FY2026 "
              "dollars; includes OBBBA Sec. 20002 mandatory funding.")
_UNITS = ("Combined supplier TAM stacked by program vs broad component SAM, $B per "
          "year; FY2022–FY2027 average, constant FY2026 dollars.")

_EVID_95 = 950   # 9.5pt: commentary supporting-evidence text (spec typography)
_TIGHT = 100_000  # 100% line spacing in the dense KPI/support cards


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_QUAL_Y, _QUAL_H = BODY_Y, 200_000                       # top qualifier line
_HERO_Y, _HERO_H = _QUAL_Y + _QUAL_H + 30_000, 820_000   # two hero KPI cards
_SUP_Y,  _SUP_H  = _HERO_Y + _HERO_H + 40_000, 820_000   # four support cards
_ZONE_Y = _SUP_Y + _SUP_H + 60_000                       # chart + commentary zone

_CALL_H = 440_000
_CALL_Y = BODY_B - _CALL_H                                # focal callout (bottom)
_ZONE_B = _CALL_Y - 110_000

# Support cards: four across the full width.
_SUP_GAP = 180_000
_SUP_W = (BODY_CX - 3 * _SUP_GAP) // 4
_SUP_X = [BODY_X + i * (_SUP_W + _SUP_GAP) for i in range(4)]

# Hero KPI cards: two across, each spanning exactly two support cards below so the
# hero inner edges align with the support-card grid (left hero over support cards
# 0-1, right hero over 2-3). Outer edges already sit at BODY_X / BODY_R.
_HERO_W = 2 * _SUP_W + _SUP_GAP
_HERO_X = [_SUP_X[0], _SUP_X[2]]

# Chart-and-commentary zone: chart (left) + commentary rail (right).
_CHART_W = 6_500_000
_CAP_Y, _CAP_H = _ZONE_Y, 230_000                        # units caption (left)
_TOT_Y, _TOT_H = _CAP_Y + _CAP_H + 30_000, 250_000       # 14pt column totals band
_CHART_Y = _TOT_Y + _TOT_H
_CHART_H = _ZONE_B - _CHART_Y

# Manual color key (replaces the dropped native legend) in a thin band at the
# bottom of the chart footprint; the frame shrinks by _KEY_H to make room.
_KEY_H, _KEY_GAP = 200_000, 20_000
_CHART_CY = _CHART_H - _KEY_H - _KEY_GAP
_KEY_Y = _CHART_Y + _CHART_CY + _KEY_GAP

_COMM_X = BODY_X + _CHART_W + 320_000
_COMM_W = BODY_R - _COMM_X
_COMM_Y, _COMM_H = _ZONE_Y, _ZONE_B - _ZONE_Y

# Approximate column centres inside the chart plot area (left value axis ~0.39in),
# used only to place the two overlay total labels above each column.
_PLOT_L = BODY_X + 360_000
_PLOT_W = _CHART_W - 360_000 - 80_000
_COL1_C = _PLOT_L + _PLOT_W // 4
_COL2_C = _PLOT_L + (3 * _PLOT_W) // 4
_TOT_W = 1_300_000

# Pin the chart's inner plot so each column total sits just above its own bar top
# (per-bar, not a shared band): x/w fractions match the approximate plot above; the
# 10% top margin is headroom for the total labels.
_PLOT_LAYOUT = {"x": 0.055, "y": 0.10, "w": 0.932, "h": 0.80}
_AXIS_MAX = 4.5
_TAM_TOTAL, _SAM_TOTAL = 4.194, 3.541         # TAM stack (sub+DDG); SAM column


# ── Content ──────────────────────────────────────────────────────────────────
# Hero KPI cards: (cap, value, cumulative subline). BLUE_5 / white, the answer.
_HERO = [
    ("COMBINED SUPPLIER TAM", "$4.2B per year", "$25.2B FY2022–FY2027 cumulative"),
    ("COMBINED BROAD COMPONENT SAM", "$3.5B per year",
     "$21.2B FY2022–FY2027 cumulative"),
]

# Support cards: (cap, value | None, subline, fill, fg). Program + scope hierarchy.
_SUPPORT = [
    ("SUBMARINE TAM", "$3.5B per year", "~84% of combined TAM", BLUE_4, WHITE),
    ("DDG TAM", "$659M per year", "Smaller pool, distributed-production proof point",
     BLUE_3, WHITE),
    ("MODULAR ASSEMBLIES", "$408M per year", "Entity-flagged module-assembly work",
     BLUE_1, BLACK),
    ("BROAD INCLUDES MODULAR", None,
     "Seven-bucket envelope, not incremental to modular", BLUE_2, BLACK),
]

# Commentary: (bold 11pt finding, 9.5pt evidence). No label prefixes.
_FINDINGS = [
    ("The pool is submarine-led, while DDG supplies the distributed-production "
     "proof point.",
     "Virginia/Columbia contributes $3.5B of the $4.2B annual TAM; DDG adds "
     "$659M per year and carries the clearest public distributed-production signal."),
    ("Broad SAM is the serviceable envelope, not a capture forecast.",
     "Broad component manufacturing is $3.5B per year across the seven named "
     "buckets; modular assemblies is a narrower $408M entity-flagged cut inside "
     "that envelope."),
]


# ── Chart (native stacked column: TAM stack vs SAM comparison column) ─────────
# Category 1 stacks submarine + DDG to the $4.2B TAM total; category 2 is the
# $3.5B broad-SAM comparison column. Blanks (None) keep each series in its own
# column so SAM reads as a comparison, not a third TAM segment.
_CHART = column_chart(
    mode="stacked",
    categories=["Combined supplier TAM", "Broad component SAM"],
    series=[
        {"name": "Submarine", "values": [3.535, None], "color": CHART_ACCENT_2},  # 1D4D68 (accent2)
        {"name": "DDG", "values": [0.659, None], "color": CHART_ACCENT_3},        # 486D82 (accent3)
        {"name": "Broad component SAM", "values": [None, 3.541],
         "color": CHART_ACCENT_4, "hide_labels": True},                         # 89A2B0 (accent4)
    ],
    title=None,
    show_legend=False,
    value_axis_format='0.0',
    value_axis_min=0, value_axis_max=4.5, value_axis_major_unit=0.5,
    show_gridlines=False,
    seg_line_color=None, axis_line_color="162029",                  # no white dividers (reference look)
    # Submarine/DDG segment values labelled in-bar (plain numbers); the single-
    # segment SAM column hides its label (hide_labels above) so only its overlaid
    # column total shows. Column totals are the 10pt overlay labels above each column.
    show_value_labels=True, value_label_format='0.0',
    value_label_size_pt=9, value_label_bold=False, cat_label_size_pt=8,
    gap_width=90, cat_header="Measure",
    plot_layout=_PLOT_LAYOUT,
)
CHARTS: list[dict] = [_CHART]


# ── Local helpers ────────────────────────────────────────────────────────────
def _hero_card(sp_id: int, x: int, cap: str, value: str, sub: str) -> str:
    return text_box(
        sp_id, "HeroKpi", x, _HERO_Y, _HERO_W, _HERO_H,
        [paragraph([run(cap, size=CAP_12PT, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=120, line_spacing=_TIGHT),
         paragraph([run(value, size=ANSWER_KPI_24PT, bold=True, color=WHITE,
                        font=FONT)], align="ctr", space_after=80, line_spacing=_TIGHT),
         paragraph([run(sub, size=FINEPRINT_8_5PT, italic=True, color=WHITE,
                        font=FONT)], align="ctr", line_spacing=_TIGHT)],
        fill=BLUE_5, line_width=12_700, anchor="ctr",
        insets=(180_000, 40_000, 180_000, 40_000))


def _support_card(sp_id: int, x: int, cap: str, value: str | None, sub: str,
                  fill: str, fg: str) -> str:
    paras = [paragraph([run(cap, size=CAP_12PT, bold=True, color=fg, font=FONT)],
                       align="ctr", space_after=90, line_spacing=_TIGHT)]
    if value:
        paras.append(paragraph(
            [run(value, size=RIBBON_KPI_18PT, bold=True, color=fg, font=FONT)],
            align="ctr", space_after=70, line_spacing=_TIGHT))
        paras.append(paragraph(
            [run(sub, size=FINEPRINT_8_5PT, italic=True, color=fg, font=FONT)],
            align="ctr", line_spacing=_TIGHT))
    else:
        # No KPI value (scope-relationship card): cap over a regular body line.
        paras.append(paragraph(
            [run(sub, size=DENSE_BODY_10PT, color=fg, font=FONT)],
            align="ctr", line_spacing=_TIGHT))
    return text_box(sp_id, "SupportCard", x, _SUP_Y, _SUP_W, _SUP_H, paras,
                    fill=fill, line_width=12_700, anchor="ctr",
                    insets=(90_000, 35_000, 90_000, 35_000))


def _total_box_y(total: float) -> int:
    """Y of the total-label box so its bottom sits ~30k above the bar top for `total`
    (derived from the pinned inner plot)."""
    py = _CHART_Y + int(_CHART_CY * _PLOT_LAYOUT["y"])
    ph = int(_CHART_CY * _PLOT_LAYOUT["h"])
    bar_top = py + int(ph * (1 - total / _AXIS_MAX))
    return bar_top - _TOT_H - 30_000


def _total_label(sp_id: int, x: int, y: int, text: str) -> str:
    return text_box(
        sp_id, "ColumnTotal", x, y, _TOT_W, _TOT_H,
        [paragraph([run(text, size=LABEL_9PT, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)


def _commentary(sp_id: int) -> str:
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
            space_after=90))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 240)))
    return text_box(sp_id, "Commentary", _COMM_X, _COMM_Y, _COMM_W, _COMM_H, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(137_160, 30_000, 100_000, 30_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    qualifier = text_box(
        10, "Qualifier", BODY_X, _QUAL_Y, BODY_CX, _QUAL_H,
        [paragraph([run(_QUALIFIER, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    heroes = "".join(
        _hero_card(20 + i, _HERO_X[i], cap, value, sub)
        for i, (cap, value, sub) in enumerate(_HERO))

    support = "".join(
        _support_card(30 + i, _SUP_X[i], cap, value, sub, fill, fg)
        for i, (cap, value, sub, fill, fg) in enumerate(_SUPPORT))

    caption = text_box(
        40, "UnitsCaption", BODY_X, _CAP_Y, _CHART_W, _CAP_H,
        [paragraph([run(_UNITS, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    totals = (_total_label(41, _COL1_C - _TOT_W // 2, _total_box_y(_TAM_TOTAL), "4.2")
              + _total_label(42, _COL2_C - _TOT_W // 2, _total_box_y(_SAM_TOTAL), "3.5"))

    chart = graphic_frame(sp_id=50, name="ExecutiveTamSamColumn",
                          x=BODY_X, y=_CHART_Y, cx=_CHART_W, cy=_CHART_CY, rId="rId2")

    # Legend low in the chart's bottom band (matching the reference) so it clears the
    # category-axis labels just under the bars; pinned left, 12pt.
    key = chart_legend(
        80, [("Submarine", CHART_ACCENT_2), ("DDG", CHART_ACCENT_3),
             ("Broad component SAM", CHART_ACCENT_4)],
        cy=5_700_000, x=BODY_X)

    commentary = _commentary(60)

    # The bottom focal callout strip was removed in the manual revision; the
    # chart/commentary zone keeps its size and the freed band stays whitespace.
    return (qualifier + heroes + support + caption + totals + chart + key
            + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
