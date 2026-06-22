"""data_source_clocks - per-source data-through dates + reporting lag (Data Freshness).

From extracted/source_clocks.csv (written by aggregate_contracts.py). The data are NOT
equally current: the SAM Contract Awards API is REVEALED-only (DoD awards signed < 90 days
are excluded), USAspending lags ~1-2 weeks, FFATA subawards 6-18 months, the budget corpus
is the FY22-27 vintage. Surfacing each clock keeps the model honest about what it can/can't
see. Referenced by the Overview + QA sheets.

Promoted accessor: source_clocks_cols(header) -> "'Data Freshness'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_DATA_FRESHNESS
from workbook_army.sheets._widths import contract_width

DATA_FRESHNESS, source_clocks_cols = make_flat_sheet(
    tab=TAB_DATA_FRESHNESS, group="validation",
    csv_name="source_clocks", table_name="DataFreshness",
    banner="§1 - Source data-through dates + reporting lag",
    intro="What each source can and cannot see. The EDITABLE model clock is the Timing & "
          "Incumbent Screen $C$6 (live-linked on Overview); the data_snapshot row below is "
          "the fixed pull date, and every other row is a data-through date with its known lag.",
    width_fn=contract_width,
)
