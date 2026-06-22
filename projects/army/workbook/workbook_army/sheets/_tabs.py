"""_tabs - canonical worksheet tab names (one place to rename a tab).

Tab names are referenced by the sheet module (title banner + SheetEntry) and by any
cross-sheet accessor that quotes the tab in a formula range, so they live here once.
"""
from __future__ import annotations

# Renamed per the market-mapping review: the radar is a contract/incumbent SCREEN (not yet
# an opportunity forecast); the calendar is a RESEARCH QUEUE (timing flags to chase, not a
# decision-grade BD pipeline). The constant names follow the rename so a grep for the new
# identity finds every reference.
TAB_TIMING_SCREEN = "Timing & Incumbent Screen"   # <=31 chars (Excel tab limit)
TAB_TIMING_DETAIL = "Timing Detail"               # the moved provenance columns
TAB_RECOMPETE_REVIEWS = "Recompete Reviews"       # inputs-group per-family analyst judgment
TAB_RESEARCH_QUEUE = "Recompete Research Queue"
TAB_NOTICE_LINKS = "Notice Links"
TAB_BUDGET_MARKET = "Budget Market"
TAB_MARKET_SIZE = "Market Size"
TAB_MARKET_ASSUMPTIONS = "Market Assumptions"   # inputs-group editable knobs (the % levers)
TAB_CONTRACT_AWARDS = "Contract Awards"
TAB_AWARD_ACTIONS = "Award Actions"
TAB_SUBAWARDS = "Subawards"
TAB_PIPELINE = "Pipeline Events"
TAB_BUDGET_FACTS = "Budget Facts"
TAB_P5_COST = "P-5 Cost Elements"
TAB_OMA_NOTES = "O&M Watercraft Notes"
TAB_CONTRACT_FAMILIES = "Contract Families"
TAB_SOURCE_LOG = "Source Log"
TAB_OVERVIEW = "Overview"
TAB_SCOPE = "Scope & Assumptions"
TAB_CUSTOMER_MAP = "Customer Map"
TAB_QA = "QA & Reconciliation"
TAB_DATA_FRESHNESS = "Data Freshness"

# The editable As-of date cell on the Timing & Incumbent Screen (column C of its as-of row).
# Both the screen's own expiry clock AND the Pipeline Events "Open?" / days-to-deadline
# columns key off this one cell, so the whole book re-clocks from a single edit. The
# screen asserts its rendered row matches AS_OF_ROW so this address can't silently drift.
AS_OF_ROW = 6
AS_OF_CELL = f"'{TAB_TIMING_SCREEN}'!$C${AS_OF_ROW}"
