"""s18_appendix_definitions_terminology - the fused glossary and boundary guardrail: a
plain-language term, its meaning, what the model uses it for, and the guardrail that keeps
it from drifting, for every sizing, evidence, and shipbuilding-vocabulary term in the deck.

Layout (full-width reference table, no chart, no commentary): one full-width glossary
house_table under the title is the entire page - a reference matrix, complete on its own,
with the title carrying the finding. The space the matrix leaves below it is intentional
breathing room.

This is a reference matrix, not an argument exhibit, so it uses the rule skin (unfilled
header carried by a heavy dark bottom-rule, differentiating it from the dark-header
scorecard and audit tables) with horizontal rules only. Light gray (F2F2F2) shades the
Guardrail column as a quiet reference cue; light blue-gray (E2E9EF) shades the Term cell
only of the misread-prevention vocabulary rows (Electrical, Mission systems, Modular,
Structural unit, Module, Block, Mission module) so the row itself is never banded.

Term rows stay in the spec order and read as three bands - core sizing terms, evidence and
scope terms, shipbuilding-vocabulary terms - without a colored section row.

Note: house_table renders one cell font size per table; this uses 8.5pt throughout (the
Term column is bold via the house first-column rule), which keeps the dense 17-row matrix
inside the body box rather than splitting the Term column to a separate 9pt size.

Spec: ds_specs/s18_appendix_definitions_terminology.txt (SLIDE 18 - APPENDIX A1).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    house_table,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y,
    BLUE_1, GRAY_1,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Definitions"
_TOPIC            = "Definitions and Terminology"
_TAKEAWAY = ("Plain-language terms keep the model boundary and shipbuilding "
             "vocabulary consistent.")
_SOURCES = ("Sources: (1) DDG and submarine appendix definitions and model-boundary "
            "scope; (2) FFATA/FSRS subaward records and the operating-entity supplier "
            "registry; (3) HII and Navy shipbuilding terminology references")


# ── Glossary table ───────────────────────────────────────────────────────────
# Four columns: Term (scan column, wide enough for long shipbuilding terms);
# Plain-English meaning (widest); Used for (medium); Guardrail (medium-wide,
# fragmentary). Rows stay in spec order across three reading bands.
_COL_W = [2_950_000, 3_600_000, 2_300_000, 2_432_362]   # sum 11_282_362

_ROWS = [
    ["TERM", "PLAIN-ENGLISH MEANING", "USED FOR", "GUARDRAIL"],
    # -- core sizing terms --
    ["TAM", "Supplier opportunity inside selected new-construction boundary",
     "Headline, shown annualized", "Not total ship cost"],
    ["SAM", "Scenario cut of TAM by work-type bucket", "Serviceable sizing",
     "Scenarios overlap; do not add"],
    ["Basic Construction", "P-5c construction budget base",
     "Budget base for supplier share", "Not total ship cost"],
    ["AP/LLTM", "Advance procurement and long-lead-time material",
     "Additive for DDG after filtering; reference-only for submarine",
     "Additive only where the boundary allows"],
    ["Supplier share", "Share of a budget base estimated as supplier work",
     "Converts budget base to TAM", "Applied value, not broader POP evidence"],
    # -- evidence and scope terms --
    ["FFATA/FSRS", "First-tier subaward reporting",
     "Supplier names and work-type evidence", "Names and evidence, not full supplier flow"],
    ["POP", "Place-of-performance evidence", "Where work is performed",
     "Evidence and sensitivity, not applied share"],
    ["GFE/GFP", "Government-furnished equipment and property", "Excluded scope",
     "Outside modeled component opportunity"],
    ["SIB", "Submarine industrial-base capacity funding", "Context",
     "Not current component delivery"],
    # -- shipbuilding-vocabulary terms --
    ["Electrical (work-type bucket)", "Ship power, distribution, and generation",
     "Largest physical bucket", "Not combat or mission electronics"],
    ["Mission systems", "Combat and electronics systems",
     "Excluded before bucket assignment", "Different market, not GFE"],
    ["Modular (scenario)", "Entity-flagged module-assembly work",
     "Distributed-build SAM cut", "Not a structural-and-coatings bucket union"],
    ["Structural unit; outfitted unit; DDG unit",
     "HII language for partner-built DDG sections", "DDG physical sections",
     "Default DDG term, not module"],
    ["Module", "Submarine structural-section language", "Submarine physical sections",
     "Rare in DDG; not the DDG default"],
    ["Block", "Virginia procurement tranche", "Procurement grouping",
     "Not a physical section"],
    ["Grand block", "Eastern and USNI language", "Outside HII default vocabulary",
     "Not HII default"],
    ["Mission module", "LCS swappable-payload language", "LCS payloads",
     "Avoid for DDG and submarine structural work"],
]

# Glossary reads as a four-column lookup; every column left-aligned.
_ALIGNS = ["l", "l", "l", "l"]

# Column cue: light gray (F2F2F2) down the Guardrail column. Misread-prevention rows
# take a light blue-gray (E2E9EF) fill in the Term cell ONLY (never across the row):
# Electrical, Mission systems, Modular, Structural unit, Module, Block, Mission module.
_MISREAD_TERM_ROWS = {10, 11, 12, 13, 14, 15, 17}
_CELL_FILLS: dict[tuple[int, int], str] = {}
for _r in range(1, len(_ROWS)):
    _CELL_FILLS[(_r, 3)] = GRAY_1                 # Guardrail column cue
for _r in _MISREAD_TERM_ROWS:
    _CELL_FILLS[(_r, 0)] = BLUE_1                 # Term-cell misread cue


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_TABLE_X = BODY_X
_TABLE_Y = BODY_Y
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=8.5, min_row_h=200_000)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    return house_table(
        10, "DefinitionsGlossary", _TABLE_X, _TABLE_Y, _COL_W, _ROWS,
        row_h=_ROW_H, table_skin="rule", aligns=_ALIGNS, size=850,   # 8.5pt
        cell_fills=_CELL_FILLS)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
