"""_cuts - shared access to the extracted CSV(s).

Local non-sheet helper (like _layout / _widths). The data is written into
extracted/<name>.csv by ``build_extracted.py`` (re-run only if the upstream TAM
SCN-budget slice changes).

Reads every cell as a RAW STRING so identifiers keep their exact form; each sheet
module then casts only the columns it knows are numeric via as_int / as_float, and
routes everything else through cell() so a blank stays a real empty cell (None)
rather than the literal "".
"""
from __future__ import annotations

import csv

from workbook_ddg_module_cost.lib import EXTRACTED


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


def load_rows(name: str) -> list[dict[str, str]]:
    """List of {header: cell} dicts (DictReader-style), raw strings."""
    headers, rows = load_table(name)
    return [dict(zip(headers, r)) for r in rows]


def as_int(s):
    """'' / None -> None; '5' -> 5 (count / FY columns)."""
    s = (s or "").strip()
    return int(s) if s else None


def as_float(s):
    """'' / None -> None; '2001.391' -> 2001.391 ($M columns)."""
    s = (s or "").strip()
    return float(s.replace(",", "")) if s else None


def cell(s):
    """Raw text cell -> the string, or None for blank (so a styled empty cell
    renders blank, not the literal empty string)."""
    s = s if s is not None else ""
    return s if s != "" else None
