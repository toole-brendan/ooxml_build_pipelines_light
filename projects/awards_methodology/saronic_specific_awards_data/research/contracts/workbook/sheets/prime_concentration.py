"""Prime Concentration — top prime recipients by market tier.

Mechanism 2 (vehicle-gated market): the top recipients in each tier, with the
obligated dollars ($M) and each prime's share of the tier. The Summary reads the
top-5 share off this tab. Source: extracted/prime_concentration.csv
(analyze_market_structure.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "tier",      "show": "Tier",         "type": "text", "w": 16},
    {"csv": "prime",     "show": "Prime",        "type": "text", "w": 42},
    {"csv": "dollars",   "show": "Obligated $M", "type": "num",  "w": 14, "scale": 1e-6},
    {"csv": "share_pct", "show": "Tier Share %", "type": "num",  "w": 12},
]

PRIME_CONCENTRATION, conc_cols = flat_sheet(
    tab="Prime Concentration", csv_name="prime_concentration",
    table_name="PrimeConcentration",
    banner="§1 - Prime concentration by market tier (top recipients)",
    intro=("Top recipients per tier; obligated in $M and tier share in percent. Sorted "
           "by share within tier."),
    columns=_COLUMNS,
)
