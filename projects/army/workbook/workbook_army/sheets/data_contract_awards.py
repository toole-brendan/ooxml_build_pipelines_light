"""data_contract_awards - the raw Army + USACE prime-award register.

One row per in-scope PIID from extracted/contract_awards.csv (the Stage-1/2 discovery
+ USAspending award-detail pull), rendered faithfully: every source field is a column,
including the always-blank analyst-bridge columns (program / capability_node) and the
provenance columns (source_system / source_id / extract_run_id / row_hash). The dollar
columns and the period-of-performance dates are blue hardcoded source values;
everything else is raw text with identifiers (PIID, UEI, NAICS / PSC codes) kept as
exact strings.

Money discipline: obligation_amount, current_value and ceiling_value are three DISTINCT
amount concepts - never summed across. The sum-able obligation stream lives on Award
Actions (one row per mod).

Promoted accessor (imported by the future recompete radar): `awards_cols(header)` ->
absolute column range "'Contract Awards'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_CONTRACT_AWARDS
from workbook_army.sheets._widths import contract_width

_FLOAT = ["obligation_amount", "current_value", "ceiling_value", "total_outlay",
          "total_subaward_amount"]
_INT = ["subaward_count", "number_of_offers"]
_DATE = ["date_signed", "pop_start_date", "pop_current_end_date",
         "pop_potential_end_date", "first_action_date", "last_action_date"]

CONTRACT_AWARDS, awards_cols = make_flat_sheet(
    tab=TAB_CONTRACT_AWARDS, group="data",
    csv_name="contract_awards", table_name="ContractAwards",
    banner="§1 - Prime contract awards",
    intro="Raw Army + USACE prime-award register - one row per in-scope PIID. "
          "Obligation, Current value and Ceiling are three DISTINCT money columns; "
          "never summed across (the sum-able obligation stream is on Award Actions).",
    width_fn=contract_width,
    float_cols=_FLOAT, int_cols=_INT, date_cols=_DATE,
    input_cols=_FLOAT + _INT + _DATE,
)
