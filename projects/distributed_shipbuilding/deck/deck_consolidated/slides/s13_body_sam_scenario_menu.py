"""s13_body_sam_scenario_menu - present the SAM scenarios as overlapping inclusion
cuts of one TAM, not additive markets: the broad-component envelope ($3.5B) and four
nested cuts (HM&E, electrical, metal, modular) sized against it.

Pattern A: a native single-series clustered column (left) - the five scenario columns
step through the BLUE theme accents in index order (accent2..accent6, the think-cell
color progression; the gray accent1 is reserved for 1-v-1 charts): broad first as
accent2, then the four cuts in accent3..accent6 - a no-fill commentary box (right), a
subordinate no-fill scenario-composition legend under the chart, a units caption above,
and a filled do-not-sum caveat strip pinned to the bottom (the caveat carries the
non-summable message). Think-cell look: white 0.75pt column outlines, dark-navy axis,
8pt labels, no gridlines.

The scenarios are non-summable cuts of one TAM, so the columns are clustered (each
independent), never stacked on one another. Each value is the combined scenario SAM, $B.

Spec: ds_specs/s13_body_sam_scenario_menu.txt (SLIDE 13 - SAM SCENARIO MENU).
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
    CHART_ACCENT_2, CHART_ACCENT_3, CHART_ACCENT_4, CHART_ACCENT_5, CHART_ACCENT_6,
    GRAY_4, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, MESSAGE_11PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Sizing"
_BREADCRUMB_TOPIC = "SAM Scenarios"
_TOPIC            = "SAM Scenarios"
_TAKEAWAY = ("Broad component manufacturing is the $3.5B envelope; HM&E is the "
             "largest cut at $2.5B and modular is the smallest at $408M.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c Basic Construction and AP/LLTM budget "
            "justification, FY2022–FY2027; (2) FFATA/FSRS subaward records and the "
            "operating-entity supplier registry; (3) DDG and submarine SAM scenario "
            "inclusion-cut definitions")

_UNITS = ("Average annual scenario SAM, $B, FY2022–FY2027; constant FY2026 dollars. "
          "Each scenario is an inclusion cut of one TAM, not additive.")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Chart (native single-series clustered column) ────────────────────────────
# One column per scenario, broad first. Combined scenario SAM, $B. Think-cell color
# progression: the five columns step through the BLUE accents in index order
# (accent2 broad -> accent3..accent6 cuts; gray accent1 reserved for 1-v-1 charts).
# Labels above the columns (outEnd), BLACK, 8pt. Clustered, not stacked: the cuts are
# overlapping, non-summable slices of one TAM (the do-not-sum caveat strip carries that
# message, not a uniform cut color).
_SCENARIOS = [
    ("Broad mfg (envelope)", 3.54,  CHART_ACCENT_2),   # 1D4D68 (accent2)
    ("HM&E",                 2.54,  CHART_ACCENT_3),    # 486D82 (accent3)
    ("Electrical/power",     1.35,  CHART_ACCENT_4),    # 89A2B0 (accent4)
    ("Metal components",     1.17,  CHART_ACCENT_5),    # AFC2CC (accent5)
    ("Modular assy",         0.408, CHART_ACCENT_6),    # D8E3EB (accent6)
]

_CHART = column_chart(
    mode="clustered",                          # one series, 5 independent columns
    categories=[s[0] for s in _SCENARIOS],
    series=[{
        "name": "Average annual scenario SAM",
        "values": [s[1] for s in _SCENARIOS],
        "data_point_colors": [s[2] for s in _SCENARIOS],
    }],
    title=None,
    show_legend=False,
    value_axis_format='0.0',
    value_axis_min=0, value_axis_max=4, value_axis_major_unit=0.5,
    show_gridlines=False,
    seg_line_color=None, axis_line_color="162029",                  # no bar borders (reference look)
    show_value_labels=True, value_label_format='0.0',
    value_label_size_pt=9, value_label_bold=False, cat_label_size_pt=8,
    gap_width=64, cat_header="Scenario",
)
CHARTS: list[dict] = [_CHART]


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_CAP_Y, _CAP_H = BODY_Y, 300_000               # units caption (8.5pt italic)

_CAVEAT_H = 520_000
_CAVEAT_Y = BODY_B - _CAVEAT_H                  # 5_350_000

_LEGEND_H = 540_000
_LEGEND_Y = _CAVEAT_Y - 60_000 - _LEGEND_H      # 4_750_000

_CHART_Y = _CAP_Y + _CAP_H + 70_000             # 1_741_600
_CHART_W = 6_950_000                            # ~7.6in (Pattern A)
_CHART_H = _LEGEND_Y - 80_000 - _CHART_Y        # 2_928_400

_GAP_CC = 280_000
_COMM_X = BODY_X + _CHART_W + _GAP_CC           # 7_683_079
_COMM_W = BODY_R - _COMM_X                       # 4_052_362 (~4.43in)
_COMM_Y = _CHART_Y
_COMM_H = (_CAVEAT_Y - 70_000) - _COMM_Y         # 3_538_400
_COMM_INSETS = (137_160, 30_000, 137_160, 30_000)


# ── Content ──────────────────────────────────────────────────────────────────
_FINDINGS = [
    ("Broad is the serviceable envelope, not another market.",
     "Broad component manufacturing is $3.5B per year, equal to $4.2B of TAM less "
     "the $653M residual; every other scenario is a cut of that envelope."),
    ("HM&E is the largest overlapping cut.",
     "HM&E reaches $2.5B because it includes electrical power, machining, "
     "piping/valves/pumps, and HVAC; electrical alone is $1.4B and metal is $1.2B."),
    ("Modular is smaller but most aligned with distributed build.",
     "The $408M modular cut is entity-flagged module-assembly work, not a "
     "structural-and-coatings union."),
]

# Scenario-composition legend: scenario name bold before each "=", definition regular;
# GRAY_4 semicolon separators between entries (no plus signs as prose separators).
_COMPOSITION = [
    ("Broad", " = all seven buckets"),
    ("HM&E", " = machining, piping/valves/pumps, electrical/power, and HVAC"),
    ("Electrical", " = electrical/power only"),
    ("Metal", " = structural/pre-outfit, machining, and castings/forgings"),
    ("Modular", " = entity-flagged module-assembly work, not a bucket union"),
]

_CAVEAT_LEAD = "Note: "
_CAVEAT_BODY = "Scenarios are overlapping cuts of one TAM."


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


def _composition_legend(sp_id: int) -> str:
    """Subordinate no-fill legend/chip row: bold scenario name, regular definition,
    GRAY_4 semicolon separators between entries."""
    runs = [run("Scenario composition  ", size=FINEPRINT_8_5PT, bold=True,
                italic=True, color=BLACK, font=FONT)]
    for i, (name, definition) in enumerate(_COMPOSITION):
        if i:
            runs.append(run(";   ", size=FINEPRINT_8_5PT, color=GRAY_4, font=FONT))
        runs.append(run(name, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT))
        runs.append(run(definition, size=FINEPRINT_8_5PT, color=BLACK, font=FONT))
    return text_box(
        sp_id, "ScenarioCompositionLegend", BODY_X, _LEGEND_Y, _CHART_W, _LEGEND_H,
        [paragraph(runs, line_spacing=110_000)],
        fill=None, line_color=None, anchor="t",
        insets=(40_000, 30_000, 40_000, 30_000))


def _caveat_strip(sp_id: int) -> str:
    # Small right-column note (was a full-width bottom strip): the do-not-sum point
    # is now a quiet footnote under the commentary, not a focal band.
    return text_box(
        sp_id, "DoNotSumCaveat", _COMM_X, _CAVEAT_Y, _COMM_W, _CAVEAT_H,
        [paragraph([
            run(_CAVEAT_LEAD, size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run(_CAVEAT_BODY, size=1000, color=WHITE, font=FONT)],   # 1000 = 10pt
            align="ctr")],
        fill=GRAY_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = _units_caption(10)
    chart = graphic_frame(sp_id=20, name="SamScenarioClusteredColumn",
                          x=BODY_X, y=_CHART_Y, cx=_CHART_W, cy=_CHART_H, rId="rId2")
    commentary = _commentary(30)
    legend = _composition_legend(40)
    caveat = _caveat_strip(50)
    return caption + chart + commentary + legend + caveat


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
