"""data_source_log - the cited-source register (the methodology's Source Log).

One row per cited budget book from extracted/source_log.csv: id, title, FY, appropriation,
exhibits, sha256, pages, local paths, access date. The source URL is folded into a hover
note on the title (one link per line). This is the provenance backbone every budget fact's
source_id joins back to. (Contract-source clocks live in the QA layer / source_clocks.csv.)

Promoted accessor: source_log_cols(header) -> "'Source Log'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_SOURCE_LOG
from workbook_army.sheets._widths import contract_width

SOURCE_LOG, source_log_cols = make_flat_sheet(
    tab=TAB_SOURCE_LOG, group="sources",
    csv_name="source_log", table_name="SourceLog",
    banner="§1 - Cited source log (budget books)",
    intro="The cited FY22-27 budget books behind the funding facts - source_id joins each "
          "budget fact to its book. Source URL is in the title cell note.",
    width_fn=contract_width,
    int_cols=["pdf_pages"],
    note_from={"title": "url"},
)
