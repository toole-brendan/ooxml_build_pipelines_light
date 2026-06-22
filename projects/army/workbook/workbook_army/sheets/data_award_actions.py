"""data_award_actions - the raw per-modification obligation actions (THE sum-able table).

One row per contract modification from extracted/contract_award_actions.csv, rendered
faithfully. Every row carries amount_type=obligation, so this is the ONE table whose
`amount` column sums correctly (FPDS per-mod obligatedAmount wins; USAspending
transactions fill awards FPDS did not return - the `source_system` column flags which).
`amount` and `action_date` are blue hardcoded source values; `fiscal_year` is the
derived FY (black); everything else is raw text.

Promoted accessor (imported by the future recompete radar): `actions_cols(header)` ->
absolute column range "'Award Actions'!$X$first:$X$last" - the leaf the radar's
per-family / per-PIID obligation roll-ups (SUMIFS over `amount`) key on.
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_AWARD_ACTIONS
from workbook_army.sheets._widths import contract_width

_FLOAT = ["amount"]
_INT = ["fiscal_year"]
_DATE = ["action_date"]

AWARD_ACTIONS, actions_cols = make_flat_sheet(
    tab=TAB_AWARD_ACTIONS, group="data",
    csv_name="contract_award_actions", table_name="AwardActions",
    banner="§1 - Award modifications (per-mod obligations)",
    intro="Sum-able obligations, one row per modification (amount_type=obligation). Sum the "
          "Amount column for lifetime totals.",
    width_fn=contract_width,
    float_cols=_FLOAT, int_cols=_INT, date_cols=_DATE,
    input_cols=_FLOAT + _DATE,
)
