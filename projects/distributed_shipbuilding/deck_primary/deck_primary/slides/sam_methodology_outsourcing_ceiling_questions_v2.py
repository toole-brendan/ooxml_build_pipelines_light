"""sam_methodology_outsourcing_ceiling_questions_v2 - concise discussion table for validating the outsourcing-ceiling methodology.

INTENT: Provide a high-level question matrix that pressure-tests the ceiling / headroom
logic in discussion without exposing workbook-specific variables, formulas, or cell mechanics.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb,
    prelim_chip,
    title_placeholder,
    house_table,
)
from deck_core.style import (
    BODY_X,
    BODY_Y,
    BODY_CX,
    BODY_CY,
    DENSE_BODY_10PT,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers the page

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION = "SAM Methodology"
_TOPIC = "Outsourcing Ceiling"
_TAKEAWAY = "Discussion questions test whether the ceiling logic reflects shipbuilding reality."


_ROWS = [
    ["Question area", "Question to discuss", "Model implication"],
    [
        "Overall frame",
        "Is an upper-bound ceiling a fair way to frame the question, separate from current outsourcing?",
        "Confirms the output is an upside boundary, not a current-state estimate.",
    ],
    [
        "Addressable base",
        "Does Basic Construction capture the controllable build work, or does it exclude important supplier opportunities?",
        "Validates the denominator before comparing classes or sizing headroom.",
    ],
    [
        "Current baseline",
        "How reliable is place-of-performance as a floor for work already distributed away from the prime yard?",
        "Calibrates the starting point for the headroom comparison.",
    ],
    [
        "Yard-bound core",
        "What work truly cannot leave the yard because of integration, nuclear controls, alignment, test, certification, or yard know-how?",
        "Sets the irreducible core that limits the ceiling.",
    ],
    [
        "Movable work",
        "Which build tasks can practically move outside the yard, and which are only theoretically movable?",
        "Tests whether distributed labor is realistic capacity relief.",
    ],
    [
        "Package economics",
        "When work moves outside the yard, does material usually move with the package, or mainly labor / fabrication?",
        "Translates movable work into supplier-dollar opportunity.",
    ],
    [
        "Program differences",
        "Where should Virginia, Columbia, and DDG-51 be treated differently: yard, class, block maturity, GFE mix, or supplier base?",
        "Determines whether one model shape can travel across programs.",
    ],
    [
        "Constraints + readout",
        "What most limits more outsourcing, and should the gap to the ceiling read as opportunity, capacity headroom, or a screen?",
        "Frames feasibility caveats and the external wording.",
    ],
]


def _body() -> str:
    """Build a single native, default-rule table, vertically centered in BODY.

    House-table defaults: 10pt cells (DENSE_BODY_10PT) and rows sized to CONTENT via
    estimate_row_heights — not a forced even BODY_CY division — so the grid reads
    even and the text fills the row instead of floating in an over-tall band. Cells
    top-anchor so the three columns of each row align on their first line.
    """
    col_w = [
        2_080_000,
        6_660_000,
        BODY_CX - 2_080_000 - 6_660_000,
    ]
    row_h = estimate_row_heights(_ROWS, col_w, size_pt=DENSE_BODY_10PT / 100.0)
    # Center the snug table in BODY (the source strip is gone, so balance the slack).
    y = BODY_Y + max(0, BODY_CY - sum(row_h)) // 2

    return house_table(
        10,
        "sam_methodology_outsourcing_ceiling_questions",
        BODY_X,
        y,
        col_w,
        _ROWS,
        row_h=row_h,
        table_skin="rule",  # default posture: no header/body fills, horizontal rules only.
        aligns=["l", "l", "l"],
        anchor="t",
        size=DENSE_BODY_10PT,
    )


def render() -> str:
    """Assemble chrome + body into one <p:sld>, in locked paint order."""
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
    )
