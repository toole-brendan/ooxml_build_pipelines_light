"""Market Tiers — the discovery universe of in-scope sea-service awards, by tier.

The fact spine behind the market sizing: one row per discovered in-scope award, with
the tier that splits the addressable craft market (USV / small craft / other small)
from the excluded capital-ship tier (broad_maritime). The Summary's tier sizing and
the addressable $11.5B are SUMIF/COUNTIF off this tab. Award amount in $M. Source:
extracted/market_tiers.csv (pull_usaspending_discovery.py).
"""
from __future__ import annotations

from ..helpers import flat_sheet

_COLUMNS = [
    {"csv": "piid",          "show": "PIID",         "type": "text", "w": 18},
    {"csv": "tier",          "show": "Tier",         "type": "text", "w": 16},
    {"csv": "award_amount",  "show": "Award $M",     "type": "num",  "w": 14, "scale": 1e-6},
    {"csv": "recipient",     "show": "Recipient",    "type": "text", "w": 38},
    {"csv": "matched_axes",  "show": "Matched Axes", "type": "text", "w": 24},
]

MARKET_TIERS, tiers_cols = flat_sheet(
    tab="Market Tiers", csv_name="market_tiers", table_name="MarketTiers",
    banner="§1 - In-scope sea-service awards by market tier (discovery universe)",
    intro=("One row per discovered in-scope award; award amount in $M. Tier splits the "
           "addressable craft market from the excluded capital-ship tier (broad_maritime)."),
    columns=_COLUMNS,
)
