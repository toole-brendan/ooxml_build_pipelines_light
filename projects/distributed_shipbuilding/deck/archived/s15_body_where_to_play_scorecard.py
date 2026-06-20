"""s15_body_where_to_play_scorecard - a full-width diligence-order scorecard: rank the
seven entry lanes by modeled value plus qualitative diligence filters (program relevance,
strategic fit, qualification burden, evidence confidence) and a one-line priority read.
It is a where-to-look-first screen, not a scored model and not a sales forecast.

Layout (primary full-width table, no chart): one dark-header house_table under the title
(eight columns, seven lanes in diligence-priority order) and a two-column no-fill
commentary block below. Per the current spec there is no separate focal strip - the
first finding now folds in the former focal line ("where to look first, not what an
entrant will win") - and the space freed at the bottom is intentional breathing room,
not a gap to backfill.

Only the Lane and Priority-read cells of the two lead lanes (modular assemblies, broad
component manufacturing) take a light E2E9EF emphasis fill; the qualitative rating cells
stay unfilled so color never implies a modeled score (no traffic-light heatmap).

Spec: ds_specs/s15_body_where_to_play_scorecard.txt (SLIDE 15 - WHERE-TO-PLAY SCORECARD).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_B, BODY_CX,
    BLUE_1,
    BLACK, FONT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Implications"
_BREADCRUMB_TOPIC = "Where to Play"
_TOPIC            = "Where to Play"
_TAKEAWAY = ("Start diligence with modular assemblies and broad component "
             "manufacturing, then triage the rest by qualification burden and "
             "openness.")
_SOURCES = ("Sources: (1) modeled scenario SAM, FY2022–FY2027; (2) FFATA/FSRS "
            "supplier-visibility evidence and qualification-burden assessment; "
            "(3) DDG and submarine program implications analysis")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Scorecard table ──────────────────────────────────────────────────────────
# Eight columns: Lane and Priority read widest; Combined value medium; the five
# qualitative columns are narrow equal-width scan columns. Sum = BODY_CX.
_COL_W = [2_150_000, 1_280_000, 820_000, 820_000, 820_000, 820_000, 820_000,
          3_752_362]

_ROWS = [
    ["LANE", "COMBINED VALUE ($/YR)", "DDG RELEVANCE", "SUBMARINE RELEVANCE",
     "STRATEGIC FIT", "QUALIFICATION BURDEN", "EVIDENCE CONFIDENCE", "PRIORITY READ"],
    ["Modular assemblies", "$381M per year", "High", "Medium", "High", "Medium",
     "Medium", "Start here; validate open work and qualification path"],
    ["Broad component manufacturing", "$3.28B per year", "High", "High", "Medium",
     "Mixed", "High", "Useful envelope, too broad without bucket-level triage"],
    ["Structural fabrication and pre-outfit", "$590M per year", "High", "High",
     "High", "Medium", "Medium", "Closest physical fit to distributed structural work"],
    ["Electrical and power", "$1.26B per year", "Medium", "High", "Medium", "High",
     "Medium", "Largest bucket, but likely incumbent- and qualification-heavy"],
    ["Piping and HM&E", "$2.35B HM&E scenario", "Medium", "High", "Medium", "High",
     "Medium", "Attractive, but product-by-product qualification matters"],
    ["Machining, castings, and forgings", "$485M per year", "Medium", "Medium",
     "Medium", "Medium", "Low", "Smaller dollars, but potential bottleneck areas"],
    ["Coatings, insulation, and HVAC", "$285M per year", "Low", "Medium", "Low",
     "Medium", "Low", "Module-attach or specialized materials work"],
]

# Lane left, Combined value left, the five ratings centered (scan columns),
# Priority read left.
_ALIGNS = ["l", "l", "ctr", "ctr", "ctr", "ctr", "ctr", "l"]

# Bold the Combined-value column (house_table already bolds the Lane column + header).
_CELL_BOLD = {(r, 1): True for r in range(1, len(_ROWS))}

# Priority emphasis: light E2E9EF in the Lane + Priority-read cells of the two lead
# lanes (rows 1 and 2). Rating cells stay unfilled - no modeled-score color.
_CELL_FILLS = {(1, 0): BLUE_1, (1, 7): BLUE_1, (2, 0): BLUE_1, (2, 7): BLUE_1}

# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Table under the title; two-column commentary below. With no focal strip, the table
# (the slide's primary object) is grown past its content-fit minimum to occupy the
# main content area so the page fills evenly instead of leaving a large bottom gap.
_TABLE_Y       = BODY_Y
_COMM_H        = 900_000
_COMM_GAP_V    = 220_000                          # table -> commentary
_BOTTOM_MARGIN = 40_000

# Natural content-fit row heights, then scaled up to the target table height.
_NAT_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=8.5)
_TABLE_CY_TARGET = (BODY_B - _BOTTOM_MARGIN - _COMM_H - _COMM_GAP_V) - _TABLE_Y
_EXTRA = max(0, _TABLE_CY_TARGET - sum(_NAT_ROW_H))
_ADD   = _EXTRA // len(_NAT_ROW_H)
_ROW_H = [h + _ADD for h in _NAT_ROW_H]
_ROW_H[0] += _EXTRA - _ADD * len(_NAT_ROW_H)     # rounding remainder onto the header
_TABLE_CY = sum(_ROW_H)

_COMM_GAP = 280_000
_COMM_W   = (BODY_CX - _COMM_GAP) // 2           # 5_501_181
_COMM_X   = [BODY_X, BODY_X + _COMM_W + _COMM_GAP]
_COMM_Y   = _TABLE_Y + _TABLE_CY + _COMM_GAP_V


# ── Content ──────────────────────────────────────────────────────────────────
_FINDINGS = [
    ("The scorecard orders diligence, not expected wins.",
     "The table points to where to look first; the decision still depends on fit, "
     "qualification path, incumbent lock-up, and whether work can move to a new "
     "site."),
    ("Modular leads because it best matches the entry thesis.",
     "The modular cut is only $381M, but it is most aligned with distributed build; "
     "broad component manufacturing remains the sizing envelope to triage by "
     "bucket."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _commentary(sp_id: int, x: int, finding: str, evidence: str) -> str:
    return text_box(
        sp_id, "Commentary", x, _COMM_Y, _COMM_W, _COMM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=90),
         paragraph([run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t", insets=(40_000, 30_000, 40_000, 30_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    table_xml = house_table(
        10, "WhereToPlayScorecard", BODY_X, _TABLE_Y, _COL_W, _ROWS,
        row_h=_ROW_H, table_skin="dark", aligns=_ALIGNS, size=850,   # 8.5pt
        cell_fills=_CELL_FILLS, cell_bold=_CELL_BOLD)

    commentary = "".join(
        _commentary(20 + i, _COMM_X[i], finding, evidence)
        for i, (finding, evidence) in enumerate(_FINDINGS))

    return table_xml + commentary


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
