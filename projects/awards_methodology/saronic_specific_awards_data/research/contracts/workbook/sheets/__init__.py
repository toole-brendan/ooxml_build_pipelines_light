"""Sheet registry — tab order for the Saronic awards mini-workbook.

Reader-first: the answer page (Summary) first, then the four raw-pull data tabs it
computes off, then the Phase-2 backtest (validation). Three groups — summary (purple),
data (burgundy), validation (gray) — kept contiguous and in groups.SHEET_GROUPS order,
which package_workbook() asserts.
"""
from __future__ import annotations

from . import (summary, ot_layer, recompete_radar, teaming_edges, prime_concentration,
               market_tiers, portal_notices, award_opp_match,
               backtest_events, pop_timeline)

SHEETS = [
    summary.SUMMARY,                          # summary
    ot_layer.OT_LAYER,                        # data
    recompete_radar.RECOMPETE_RADAR,          # data
    teaming_edges.TEAMING_EDGES,              # data
    prime_concentration.PRIME_CONCENTRATION,  # data
    market_tiers.MARKET_TIERS,                # data
    portal_notices.PORTAL_NOTICES,            # data
    award_opp_match.AWARD_OPP_MATCH,          # data
    backtest_events.BACKTEST_EVENTS,          # validation
    pop_timeline.POP_TIMELINE,                # validation
]
