"""_tabs - canonical worksheet tab names (one place to rename a tab).

Tab names are referenced by the sheet module (title banner + SheetEntry) and by any
cross-sheet accessor that quotes the tab in a formula range, so they live here once.
"""
from __future__ import annotations

TAB_RECOMPETE_RADAR = "Recompete Radar"
TAB_RECOMPETE_CALENDAR = "Recompete Calendar"
TAB_CONTRACT_AWARDS = "Contract Awards"
TAB_AWARD_ACTIONS = "Award Actions"
TAB_SUBAWARDS = "Subawards"
TAB_PIPELINE = "Pipeline Events"

# The editable As-of date cell on the Recompete Radar (column C of its as-of row).
# Both the radar's own expiry clock AND the Pipeline Events "Open?" / days-to-deadline
# columns key off this one cell, so the whole book re-clocks from a single edit. The
# radar asserts its rendered row matches AS_OF_ROW so this address can't silently drift.
AS_OF_ROW = 6
AS_OF_CELL = f"'{TAB_RECOMPETE_RADAR}'!$C${AS_OF_ROW}"
