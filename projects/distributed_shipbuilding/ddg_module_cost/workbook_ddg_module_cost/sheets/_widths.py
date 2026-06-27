"""_widths - standardized column widths + header-alignment helper.

Local non-sheet helper (like _layout / _cuts). Centralizes the column-width
vocabulary so every sheet sizes a given column TYPE the same way. Widths are Excel
character units (the `cols=[...]` values passed to worksheet()); the ~1.5-char
gutter is prepended by worksheet(with_gutter=True), so these map to content
columns starting at column B.
"""
from __future__ import annotations

from workbook_core.styles import S_HEADER_LEFT, S_HEADER_CENTER

# Labels / prose
W_LABEL      = 46    # leading metric / measure / control label column
W_LABEL_WIDE = 52    # wider label column
W_TEXT       = 46    # general prose
W_TEXT_WIDE  = 70    # long prose (definitions, notes, the HII quote)

# Numeric
W_FY         = 12    # a per-fiscal-year value column
W_DOLLAR     = 14    # $M figure column
W_PCT        = 12    # percentage column
W_VALUE      = 15    # single "Value" column
W_COUNT      = 11    # integer count (modules / blocks / units)


def fy_cols(label_w: int = W_LABEL, n_fy: int = 6, fy_w: int = W_FY) -> list[int]:
    """[label, fy, fy, ...] width list for an FY-grid sheet (label + n_fy years)."""
    return [label_w] + [fy_w] * n_fy


def header_styles(headers: list[str], center_headers=()) -> list[int]:
    """Header-row styles: left-align text headers; center any columns named in
    `center_headers`."""
    centered = set(center_headers)
    return [S_HEADER_CENTER if h in centered else S_HEADER_LEFT for h in headers]
