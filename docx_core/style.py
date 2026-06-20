"""docx_core.style - design tokens for the Word build pipeline.

Single source of truth for the style-y values that are pure data: the body font,
the palette (blue / gray ramps, kept in step with deck_core so a cross-pipeline
spec reads consistently), and one Word-specific helper - hp(), the points ->
half-points converter Word uses for w:sz.

Pure data plus one tiny helper; no dependency on the rest of docx_core, so
importing it is cheap and safe. The human-facing color + type rules live in
docx_core/doc_guide.md; this module is the machine-readable mirror.

Note the split (mirrors deck_core): pure tokens live here, the pt/in/line
conversions live in docx_core/units.py, and the actual WordprocessingML for the
styles is emitted by docx_core/styles.py.
"""
from __future__ import annotations


# ---------------------------------------------------------------------------
# 1. Font
# ---------------------------------------------------------------------------
# Arial throughout - the deck/workbook house font (not Word's Calibri default),
# so a Word report and the slides/sheets it documents share one typeface.
FONT = "Arial"

# Monospace face for ASCII wireframes / code blocks (fixed-width sketches).
MONO = "Courier New"


# ---------------------------------------------------------------------------
# 2. Palette
# ---------------------------------------------------------------------------
# 6-char hex, no leading '#'. Word color attrs (w:color, fills, borders) take the
# bare RRGGBB form (unlike SpreadsheetML's "FF"+hex). Ramps mirror deck_core.

BLACK = "000000"
WHITE = "FFFFFF"

# Blue ramp: lightest (BLUE_1) to darkest (BLUE_5). Use for fills / hierarchy.
BLUE_1 = "E2E9EF"
BLUE_2 = "B6C8D8"
BLUE_3 = "6E91B1"
BLUE_4 = "3D5972"
BLUE_5 = "263746"

# Gray ramp: lightest (GRAY_1) to darkest (GRAY_5).
GRAY_1 = "F2F2F2"
GRAY_2 = "D9D9D9"
GRAY_3 = "BFBFBF"
GRAY_4 = "7F7F7F"
GRAY_5 = "646464"

# Hyperlink blue (Word's Office "Hyperlink" character-style color) - used by the
# R_LINK character style only.
LINK_BLUE = "0563C1"


# ---------------------------------------------------------------------------
# 3. Type scale (points)
# ---------------------------------------------------------------------------
# Word-readable report sizes (larger than the dense deck/workbook scale). The
# actual half-point values are computed via hp() where the styles are built.

BODY_PT = 11.0
SMALL_PT = 9.0          # captions, source notes, footnotes
H1_PT = 16.0
H2_PT = 13.0
H3_PT = 11.5
TITLE_PT = 26.0         # cover / report title

# Structured-block sizes (generic card / field / register blocks).
BLOCK_HEADING_PT = 13.0  # a structured-block heading
COMPACT_BODY_PT = 10.5   # compact body copy under a label

# Monospace sizes (ASCII wireframes / code blocks).
CODE_PT = 9.0
CODE_SMALL_PT = 8.0


def hp(pt: float) -> int:
    """Half-points from points: Word's w:sz / w:szCs unit. hp(11) -> 22."""
    return int(round(pt * 2))
