#!/usr/bin/env python3
"""config - central tunables + classification rules for the Army contracts analytics.

CANONICAL for the data/aggregate side (this is where contract_families.csv, the
customer segment, watercraft relevance, the materiality floor and the lineage windows
are COMPUTED). The workbook mirrors only the few display constants it needs for its
no-canonical-CSV fallback, with a sync note - see
workbook_army/sheets/config.py.

Keeping these in one place is the fix for the reviews' finding that materiality / lineage
windows / scope sets were scattered as private constants inside model_recompete_radar.py.
"""
from __future__ import annotations

# ---- materiality + as-of -------------------------------------------------
AS_OF = "2026-06-20"                 # model as-of (data snapshot); editable in-sheet
MIN_OBLIG = 1_000_000.0              # radar/calendar materiality floor (selected measure)
FAMILY_PULL_FLOOR = 250_000.0        # SAM CA hydration pull floor (sub-floor lineage buffer)

# ---- lineage temporal windows (predecessor -> successor chaining) ---------
GAP_CAP_DAYS = 913                   # 30 mo: max forward gap pred-end -> succ-start
OVERLAP_DAYS = 548                   # 18 mo: max overlap (successor IDV starts pre-option-end)

# ---- notice planning lead -------------------------------------------------
NOTICE_LEAD_DAYS = 90               # notice-by = decision date - this (solicitation lead)
CAPTURE_LEAD_DAYS = 540             # 18 mo: capture-start = decision - this (BD/teaming lead;
                                    # the 90-day notice lead is far too late to BEGIN capture
                                    # of a complex autonomous-vessel acquisition)

# ---- effective-decision-date rules + anomaly thresholds -------------------
# The vehicle recompete date is a CLASSIFIED date (build_families): IDV ordering-period end
# for vehicles, contract PoP end for standalones, agreement-specific for BOA/BPA - NOT the
# conflated MAX(child task-order ends). These flag implausible inputs.
DATE_HORIZON_YEARS = 15             # effective decision date beyond As-of + this -> anomaly
CEILING_ANOMALY = 5e10             # ceiling > $50B -> anomaly (a data error, not a real ceiling)
CHILD_LAG_ANOMALY_DAYS = 1825      # 5 yr: child order ends this long after the vehicle end ->
                                    # anomaly (the Birdon W56HZV19D0093 ordering-end-vs-2030 case)

# ---- multiple-award cohort detection (requirement -> co-awarded vehicles) -
# Vehicles sharing office + PoP-start + ordering-end + PSC under one MULTIPLE-AWARD
# requirement are ONE cohort (count once), not N independent recompetes.
COHORT_START_WINDOW_DAYS = 365     # bucket width for pop_start_date co-clustering
COHORT_ORDEND_WINDOW_DAYS = 365    # bucket width for ordering_period_end co-clustering

# ---- watercraft relevance scope (deterministic, documented) --------------
WC_PSC = {"1905", "1915", "1925", "1930", "1935", "1940", "1945", "1990", "2090"}
WC_NAICS = {"336611", "336612"}
WC_PRIMES = ["VIGOR", "BIRDON", "BAY SHIP", "COLONNA", "CONRAD",
             "EASTERN SHIPBUILDING", "THOMA-SEA", "METAL TRADES"]
WC_DESC = ["SHIP BUILD", "SHIP REPAIR", "BOAT", "VESSEL", "WATERCRAFT", "DREDG",
           "BARGE", "LANDING CRAFT", "TUG", "PONTOON", "LIGHTER", "MARINE"]

# ---- coverage reconciliation thresholds ----------------------------------
# action coverage = reconstructed action sum / award-reported obligation.
COVERAGE_COMPLETE_LO = 0.95         # within [lo, hi] of award-reported -> "complete"
COVERAGE_COMPLETE_HI = 1.05

# ---- customer segments (Army vs USACE vs MRO vs peripheral) --------------
# Ordered (first match wins); evaluated by mapping_rules.customer_segment().
SEG_USACE = "USACE floating plant / civil works"
SEG_ARMY_OPS = "Army operational watercraft & bridging"
SEG_ARMY_LOG = "Army logistics / prepositioned / floating"
SEG_ARMY_RDTE = "Army experimentation / autonomy / sensors / RDT&E"
SEG_MRO = "Maintenance, repair & vessel support"
SEG_PERIPHERAL = "Peripheral / excluded maritime"

# ---- Saronic tier (review #5: Saronic-first default view) -----------------
# A pure re-grouping of customer_segment so the radar/calendar sort Army operational
# watercraft + autonomy/RDT&E FIRST (Core), then MRO/logistics (Adjacent), with USACE /
# peripheral last (Peripheral) - opt-in via the table AutoFilter, not excluded.
SARONIC_TIER_CORE = "Core (Army ops + autonomy/RDT&E)"
SARONIC_TIER_ADJACENT = "Adjacent (MRO + logistics)"
SARONIC_TIER_PERIPHERAL = "Peripheral (USACE + excluded)"
SARONIC_TIER_BY_SEGMENT = {
    SEG_ARMY_OPS:   SARONIC_TIER_CORE,
    SEG_ARMY_RDTE:  SARONIC_TIER_CORE,
    SEG_MRO:        SARONIC_TIER_ADJACENT,
    SEG_ARMY_LOG:   SARONIC_TIER_ADJACENT,
    SEG_USACE:      SARONIC_TIER_PERIPHERAL,
    SEG_PERIPHERAL: SARONIC_TIER_PERIPHERAL,
}
SARONIC_TIER_RANK = {SARONIC_TIER_CORE: 0, SARONIC_TIER_ADJACENT: 1,
                     SARONIC_TIER_PERIPHERAL: 2}
