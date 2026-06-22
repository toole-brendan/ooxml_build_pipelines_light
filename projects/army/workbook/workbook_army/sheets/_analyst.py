"""_analyst - read the durable analyst tables (system of record OUTSIDE the xlsx).

The analyst judgment columns on the model sheets (recompete Window / Confidence /
Pursuit access / program / capability_node / Notes, and the bridge tables) must SURVIVE
a rebuild - a workbook regenerated from the CSVs would otherwise wipe them. So they live
in version-controlled CSVs under workbook/analyst/ keyed by a stable id (family_key,
opportunity_id, row_hash, ...), and the build merges them back onto the rendered rows as
BLUE inputs. This module is the read side; aggregate_contracts.py seeds the schemas.
"""
from __future__ import annotations

import csv
from pathlib import Path

ANALYST_DIR = Path(__file__).resolve().parents[2] / "analyst"


def load_analyst_table(name: str, key_col: str) -> dict:
    """workbook/analyst/<name>.csv -> {key_col value: row dict}. Empty if absent."""
    path = ANALYST_DIR / f"{name}.csv"
    if not path.exists():
        return {}
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            k = (r.get(key_col) or "").strip()
            if k:
                out[k] = r
    return out


def value(table: dict, key: str, col: str):
    """A single analyst cell, or None (so the renderer leaves an empty blue input)."""
    row = table.get((key or "").strip())
    if not row:
        return None
    v = (row.get(col) or "").strip()
    return v or None
