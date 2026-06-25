"""_widths - standardized column widths + header-alignment helper.

Local non-sheet helper (like _layout / _cuts / _taxonomy). Centralizes the
column-width vocabulary so every sheet sizes a given column TYPE the same way
instead of hand-picking a number per sheet - the workbook reads as one ruled
system. Widths are Excel character units (the `cols=[...]` values passed to
worksheet()); the ~1.5-char gutter is prepended by worksheet(with_gutter=True),
so these map to content columns starting at column B.

Sizing rule (see sheet_guide.md "Column widths"): size to the column's content,
not padded wide. Where a header is longer than its type's width, SHORTEN the
header (house style) rather than widen - the FY columns stay compact (their
headers are <=5 chars) so the 15-16 FY-column grids don't bloat.

header_styles() encodes the workbook's header-alignment rule: every column
header is left-aligned EXCEPT real date columns and dense FY/numeric columns
(passed as center_headers), which are centered. (Numbers and dates still
right-align in the data rows via their number formats; this is only the header
cell.)
"""
from __future__ import annotations

from workbook_core.styles import S_HEADER_LEFT, S_HEADER_CENTER

# ---------------------------------------------------------------------------
# Column widths by semantic type (Excel character units)
# ---------------------------------------------------------------------------

# Text / label columns
W_PROGRAM    = 12    # program display name (Virginia / Columbia / DDG-51)
W_FAMILY     = 12    # family (Submarines / DDG-51)
W_CLASS      = 12    # vessel class
W_BUILDER    = 14    # builder / shipbuilder
W_PIID       = 18    # PIID identifier
W_ROLE       = 24    # role display name (longest: "GFE / SIB pass-through")
W_WORKTYPE   = 30    # work-type bucket display name (long edge cases clip)
W_LABEL      = 40    # PIID label / block label
W_VENDOR     = 34    # vendor name (long edge-case names clip)
W_UEI        = 14    # vendor UEI
W_REPORT     = 22    # FSRS report id (Award Events leaf)
W_CAPABILITY = 28    # SAM capability (vendor-side NAICS description)
W_NAICS4     = 8     # 4-digit NAICS
W_STATUS     = 15    # status / flag / FY-entered text
W_WAVE_SEQ   = 7     # award-wave sequence number (1, 2, 3, ...)
W_MODE       = 19    # sourcing-mode label ("Continuous sourcing" is the longest)

# Numeric columns
W_FY         = 10    # $ per-FY columns and the $ Total column
W_FY_N       = 8     # record-count per-FY columns and the N Total column
W_COUNT      = 14    # record / vendor count columns
W_DOLLAR     = 13    # single $ summary columns ($M, prior/recent $)
W_PCT        = 14    # percentage columns
W_DATE       = 13    # award dates (yyyy-mm-dd)
W_RATIO      = 9     # unitless ratio / coefficient (span/cadence, gap-CV)
W_DAYS       = 11    # day-count columns (wave span, quiet gap, days-since)


# ---------------------------------------------------------------------------
# Header alignment
# ---------------------------------------------------------------------------

def header_styles(headers: list[str], date_headers=(), center_headers=()) -> list[int]:
    """Header-row styles: left-align text headers; center the date columns named
    in `date_headers` plus any FY / numeric columns named in `center_headers`.

    Pass the same header strings used in the header write_row and the subset
    that are date columns and/or dense FY-grid columns, e.g.
        c.write(_HEADERS, styles=header_styles(_HEADERS, {"First Award", "Last Award"}))
        c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=set(VAL_LABELS)))
    """
    centered = set(date_headers) | set(center_headers)
    return [S_HEADER_CENTER if h in centered else S_HEADER_LEFT for h in headers]
