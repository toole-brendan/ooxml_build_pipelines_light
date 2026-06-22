"""config - workbook-side display constants for the recompete model sheets.

The DATA/aggregate side is canonical for materiality + classification rules (see
research/contracts/scripts/config.py): contract_families.csv ships the per-family
selected measure, coverage, segment and hydrated dates pre-computed. This module holds
only what the workbook needs at render time, plus a small MIRROR of the watercraft scope
sets used by load_families' fallback path (when contract_families.csv is absent).

  >> If you change the watercraft sets here, change scripts/config.py too (and vice
     versa). They are deliberately small + static to keep drift risk low.
"""
from __future__ import annotations

# As-of default (editable in-sheet; re-clocks every expiry/tenure column).
AS_OF = "2026-06-20"

# Materiality floor (selected measure) + lineage windows - used by the fallback path
# and by any build-time sort/split; the canonical CSV already applies the floor.
MIN_OBLIG = 1_000_000.0
GAP_CAP_DAYS = 913
OVERLAP_DAYS = 548

# Notice planning lead: notice-by = decision date - this many days.
NOTICE_LEAD_DAYS = 90
# Capture lead: capture-start = decision date - this many days (18 mo). MIRROR of
# scripts/config.py CAPTURE_LEAD_DAYS - needed workbook-side for the live Capture-start
# formula on the Research Queue. The 90-day notice lead is far too late to BEGIN capture
# of a complex autonomous-vessel acquisition. >> keep in sync with scripts/config.py.
CAPTURE_LEAD_DAYS = 540

# Saronic-first tier ordering for the timing screens. The full tier LABELS + segment map
# live canonically in scripts/config.py (emitted onto contract_families.saronic_tier); the
# screens only need the rank to sort, keyed on the label's first word (Core/Adjacent/
# Peripheral) so it survives the parenthetical without re-mirroring the whole label.
SARONIC_TIER_RANK = {"Core": 0, "Adjacent": 1, "Peripheral": 2}

# Watercraft scope sets - MIRROR of scripts/config.py (fallback relevance only).
WC_PSC = {"1905", "1915", "1925", "1930", "1935", "1940", "1945", "1990", "2090"}
WC_NAICS = {"336611", "336612"}
WC_PRIMES = ["VIGOR", "BIRDON", "BAY SHIP", "COLONNA", "CONRAD",
             "EASTERN SHIPBUILDING", "THOMA-SEA", "METAL TRADES"]
WC_DESC = ["SHIP BUILD", "SHIP REPAIR", "BOAT", "VESSEL", "WATERCRAFT", "DREDG",
           "BARGE", "LANDING CRAFT", "TUG", "PONTOON", "LIGHTER", "MARINE"]
