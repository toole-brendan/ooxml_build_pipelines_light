"""data_pipeline_events - the raw pre-award pipeline notices.

One row per SAM Opportunities notice from extracted/contract_pipeline_events.csv -
the forward signal (sources-sought / RFIs / solicitations) before an award posts on
USAspending. Rendered faithfully: `posted_date` and `response_deadline` are blue
hardcoded source dates; `fiscal_year` is the derived FY (black); the analyst-bridge
`capability_node` column is kept (blank); everything else is raw text. No money.

NOTE: Stage 5 (Opportunities) was only smoke-run, so this is a partial set (4
notices), not the full pipeline - the sparse tab is expected, not "no pipeline."

Promoted accessor: `pipeline_cols(header)` -> "'Pipeline Events'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_PIPELINE
from workbook_army.sheets._widths import contract_width

_INT = ["fiscal_year"]
_DATE = ["posted_date", "response_deadline"]

PIPELINE_EVENTS, pipeline_cols = make_flat_sheet(
    tab=TAB_PIPELINE, group="data",
    csv_name="contract_pipeline_events", table_name="PipelineEvents",
    banner="§1 - Pre-award pipeline notices",
    intro="Raw SAM Opportunities notices (pre-award forward signal). Stage 5 was "
          "smoke-run only - this is a PARTIAL set, not the full pipeline.",
    width_fn=contract_width,
    int_cols=_INT, date_cols=_DATE,
    input_cols=_DATE,
)
