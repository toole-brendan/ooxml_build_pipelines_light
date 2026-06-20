"""_tabs - canonical worksheet tab names (one place to rename a tab).

Tab names are referenced by the sheet module (title banner + SheetEntry) and by any
cross-sheet accessor that quotes the tab in a formula range, so they live here once.
"""
from __future__ import annotations

TAB_RECOMPETE_RADAR = "Recompete Radar"
TAB_CONTRACT_AWARDS = "Contract Awards"
TAB_AWARD_ACTIONS = "Award Actions"
TAB_SUBAWARDS = "Subawards"
TAB_PIPELINE = "Pipeline Events"
