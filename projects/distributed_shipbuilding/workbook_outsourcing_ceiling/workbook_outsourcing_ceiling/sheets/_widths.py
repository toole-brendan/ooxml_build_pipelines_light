"""_widths - standardized column widths + header-alignment helper.

Local non-sheet helper (like _layout). Centralizes the column-width vocabulary
so every sheet sizes a given column TYPE the same way. Widths are Excel
character units (the `cols=[...]` values passed to worksheet()); the ~1.5-char
gutter is prepended by worksheet(with_gutter=True), so these map to content
columns starting at column B.

header_styles() encodes the workbook's header-alignment rule: every column
header is left-aligned EXCEPT named numeric/center columns. Size to content
(sheet_guide.md "Column widths"); shorten a header rather than widen its column.
"""
from __future__ import annotations

from workbook_core.styles import S_HEADER_LEFT, S_HEADER_CENTER

# Text / label columns
W_LABEL     = 46    # model row label (the first column of a styled-range block)
W_PROGRAM   = 11    # program display name (Virginia / Columbia / DDG-51)
W_CLASS     = 10    # vessel class
W_METRIC    = 34    # measure / parameter label
W_NOTE      = 30    # one-line context / source note (sources tab only)

# Numeric columns
W_VALUE     = 14    # a single value column (a parameter value, a per-program $)
W_DOLLAR    = 12    # $M column
W_PCT       = 11    # percentage column
W_FY        = 7     # a single fiscal-year column (one row per FY in Cost Base)
W_MULT      = 9     # headroom multiple (x)


def header_styles(headers: list[str], center_headers=()) -> list[int]:
    """Header-row styles: S_HEADER_LEFT for every column, S_HEADER_CENTER for
    the headers named in `center_headers` (numeric / FY columns that read better
    centered over their column).
    """
    cs = set(center_headers)
    return [S_HEADER_CENTER if h in cs else S_HEADER_LEFT for h in headers]
