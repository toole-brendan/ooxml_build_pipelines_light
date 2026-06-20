"""_cuts - shared access to the per-sheet raw CSV extracts.

Local non-sheet helper (like _layout / _widths). The classification workbook's
sheet content was extracted verbatim from the manual workbook into
extracted/<stem>.csv by extract_classification_cuts.py (re-run only if the manual
source changes).

Unlike the engine's numeric-coercing load_extracted_csv, this reads every cell as
a RAW STRING so identifiers keep their exact form (Work-type ID "01", CAGE "90099",
UEIs, NAICS codes). Each sheet module then casts only the columns it knows are
numeric, via as_int / as_float, and routes everything else through cell() so a
blank stays a real empty cell (None) rather than the literal "".
"""
from __future__ import annotations

import csv
from datetime import date

from workbook_award_classification_refactor.lib import EXTRACTED

_EPOCH = date(1899, 12, 30)          # Excel date serial day 0


def load_grid(name: str) -> list[list[str]]:
    """Full row-major grid of extracted/<name>.csv as raw strings ('' for blank)."""
    with (EXTRACTED / f"{name}.csv").open(encoding="utf-8", newline="") as fh:
        return [list(r) for r in csv.reader(fh)]


def load_table(name: str) -> tuple[list[str], list[list[str]]]:
    """(headers, data_rows) for a flat-table CSV: row 0 is the header row."""
    grid = load_grid(name)
    if not grid:
        return [], []
    return grid[0], grid[1:]


def as_int(s):
    """'' / None -> None; '5' -> 5 (rank / count columns)."""
    s = (s or "").strip()
    return int(s) if s else None


def as_float(s):
    """'' / None -> None; '2001.391' -> 2001.391 ($M columns)."""
    s = (s or "").strip()
    return float(s) if s else None


def cell(s):
    """Raw text cell -> the string, or None for blank (so a styled empty cell
    renders blank, not the literal empty string)."""
    s = s if s is not None else ""
    return s if s != "" else None


def date_serial(s):
    """ISO date text -> Excel date serial (None for blank). Date cells are
    written as real serials (S_DATE_INPUT / S_DATE) so MINIFS/MAXIFS can
    aggregate them. Copied from workbook_award_analysis/sheets/_cuts.py."""
    if not s:
        return None
    y, m, d = (int(p) for p in str(s)[:10].split("-"))
    return (date(y, m, d) - _EPOCH).days
