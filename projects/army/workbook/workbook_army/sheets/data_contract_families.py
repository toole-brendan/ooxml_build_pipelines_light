"""data_contract_families - the canonical per-family fact table (one row per vehicle).

The build-time canonical produced by aggregate_contracts.py: every watercraft/contract
FAMILY with its reconciled obligation measures (award-reported vs reconstructed actions +
coverage), the SAM third-lens total, hydrated vehicle dates, customer segment, and the
single selected measure that drives the materiality floor. Rendered as a faithful leaf (loaded
canonical values -> blue) so the Overview + QA sheets can COUNTIFS / SUMIFS over it live.
The Timing & Incumbent Screen shows the same numbers as live formulas; this is the register.

Promoted accessor: families_cols(header) -> "'Contract Families'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_CONTRACT_FAMILIES
from workbook_army.sheets._widths import contract_width

_FLOAT = ["award_reported_obligation", "reconstructed_action_sum", "sam_family_obligated",
          "selected_measure", "ceiling_value"]
_PCT = ["coverage_ratio"]              # a 0-1 ratio -> render as percent (85.0%), not 0.85
_INT = ["n_awards", "n_task_orders", "action_count", "cohort_size"]
# effective_decision_date / latest_task_order_end are CLASSIFIED dates (the vehicle
# recompete + the child follow-on lens, split from the old conflated PoP end by
# aggregate_contracts.py) - rendered blue as loaded register values, like the other dates.
_DATE = ["first_action_date", "last_action_date", "pop_start_date",
         "pop_current_end_date", "pop_potential_end_date", "ordering_period_end",
         "effective_decision_date", "latest_task_order_end"]

CONTRACT_FAMILIES, families_cols = make_flat_sheet(
    tab=TAB_CONTRACT_FAMILIES, group="data",
    csv_name="contract_families", table_name="ContractFamilies",
    banner="§1 - Canonical contract families (reconciled)",
    intro="One row per contract family: reconciled obligations, classified recompete "
          "timing, cohort and segment. Historical obligations, not TAM/SAM.",
    width_fn=contract_width,
    float_cols=_FLOAT, int_cols=_INT, date_cols=_DATE, pct_cols=_PCT,
    input_cols=_FLOAT + _PCT + _INT + _DATE,
)
