"""data_pipeline_events - the raw pre-award pipeline notices.

One row per SAM Opportunities notice from extracted/contract_pipeline_events.csv -
the forward signal (sources-sought / RFIs / solicitations) before an award posts on
USAspending. Rendered faithfully: `posted_date` and `response_deadline` are blue
hardcoded source dates; `fiscal_year` is the derived FY (black); the analyst-bridge
`capability_node` column is kept (blank); everything else is raw text. No money.

Scope: Army + USACE watercraft notices posted in the trailing ~12 months (the
`active` Stage-5 pull). Rows are sorted soonest-deadline-first by the aggregate, so the
live opportunities sit at the top.

Two DERIVED columns are appended (live, not stored): `Open?` and `Days to deadline`,
both keyed off the Timing & Incumbent Screen As-of cell (_tabs.AS_OF_CELL) - so the leaf
re-clocks open/closed with the same single edit that drives the radar's expiry math.

Promoted accessor: `pipeline_cols(header)` -> "'Pipeline Events'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_core.primitives import col_letter
from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._cuts import load_table
from workbook_army.sheets._tabs import TAB_PIPELINE, AS_OF_CELL
from workbook_army.sheets._widths import contract_width

_INT = ["fiscal_year", "n_notices"]
_DATE = ["first_posted_date", "posted_date", "response_deadline"]

# response_deadline's in-sheet column letter (gutter-offset, +1) - the derived columns
# compare this cell to the As-of date. Computed from the CSV header order so it tracks
# any column reordering; the derived columns are appended AFTER it, so its index holds.
_PH, _ = load_table("contract_pipeline_events")
_DL = col_letter(_PH.index("response_deadline") + 1)

# "Open?" = response deadline still in the future vs the As-of date; "" deadline -> n/a
# (award notices / sources-sought carry no deadline). "Days to deadline" = signed days.
_open_fn = lambda r: (f'=IF(${_DL}{r}="","n/a",'
                      f'IF(${_DL}{r}>={AS_OF_CELL},"OPEN","closed"))')
_days_fn = lambda r: f'=IF(${_DL}{r}="","",${_DL}{r}-{AS_OF_CELL})'

PIPELINE_EVENTS, pipeline_cols = make_flat_sheet(
    tab=TAB_PIPELINE, group="data",
    csv_name="contract_pipeline_events", table_name="PipelineEvents",
    banner="§1 - Pre-award pipeline (one row per solicitation lifecycle)",
    intro="Army + USACE watercraft SAM Opportunities, COLLAPSED to one row per "
          "solicitation lifecycle (n_notices = amendments + award notice folded in; raw "
          "per-notice records are kept in _opportunities_index.json). first_posted_date / "
          "posted_date bracket the lifecycle; notice_type is the current stage. Sorted "
          "soonest-deadline first; Open? and Days to deadline are LIVE vs the Timing & "
          "Incumbent Screen As-of date. customer_segment splits Army watercraft from USACE.",
    width_fn=contract_width,
    int_cols=_INT, date_cols=_DATE,
    input_cols=_DATE,
    derived_cols=[("Open?", None, _open_fn),
                  ("Days to deadline", "int", _days_fn)],
)
