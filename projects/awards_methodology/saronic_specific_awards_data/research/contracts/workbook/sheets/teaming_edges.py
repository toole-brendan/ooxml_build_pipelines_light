"""Teaming Edges — first-tier prime-to-subcontractor subaward edges (SAM/FSRS).

Mechanism 3: one row per reported first-tier subaward, mapping who an integrator
subs work out to. A reported floor, not a census (FFATA lags; some primes file
nothing). Sub amount in $M (raw dollars scaled). Source:
extracted/subaward_edges.csv (build_teaming_map.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "prime_piid",    "show": "Prime PIID",  "type": "text", "w": 16},
    {"csv": "prime",         "show": "Prime",       "type": "text", "w": 28},
    {"csv": "prime_uei",     "show": "Prime UEI",   "type": "text", "w": 13},
    {"csv": "sub_key",       "show": "Sub Key",     "type": "text", "w": 13},
    {"csv": "sub_name",      "show": "Subcontractor", "type": "text", "w": 30},
    {"csv": "sub_uei",       "show": "Sub UEI",     "type": "text", "w": 13},
    {"csv": "sub_amount",    "show": "Sub $M",      "type": "num",  "w": 11, "scale": 1e-6},
    {"csv": "sub_date",      "show": "Sub Date",    "type": "text", "w": 12},
    {"csv": "capability",    "show": "Capability",  "type": "text", "w": 18},
    {"csv": "report_lag_mo", "show": "Lag (mo)",    "type": "num",  "w": 9},
    {"csv": "description",   "show": "Description",  "type": "text", "w": 30},
]

TEAMING_EDGES, teaming_cols = flat_sheet(
    tab="Teaming Edges", csv_name="subaward_edges", table_name="TeamingEdges",
    banner="§1 - First-tier subaward edges, prime to subcontractor (SAM/FSRS)",
    intro=("One row per reported first-tier subaward; sub amount in $M. A reported "
           "floor, not a census."),
    columns=_COLUMNS,
)
