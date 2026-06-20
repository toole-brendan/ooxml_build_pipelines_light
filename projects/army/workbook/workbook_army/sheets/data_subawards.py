"""data_subawards - the raw first-tier FFATA subawards.

One row per first-tier subaward from extracted/contract_subawards.csv (SAM
subcontracts pull, by prime PIID), rendered faithfully. amount_type=subaward - a
SEPARATE money universe from prime obligations; never summed with them. `amount`,
`sub_action_date` and `submitted_date` are blue hardcoded source values;
`fiscal_year` is the derived FY (black); the analyst-bridge `capability_node` column
is kept (blank); everything else is raw text.

Promoted accessor: `subawards_cols(header)` -> "'Subawards'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_SUBAWARDS
from workbook_army.sheets._widths import contract_width

_FLOAT = ["amount"]
_INT = ["fiscal_year"]
_DATE = ["sub_action_date", "submitted_date"]

SUBAWARDS, subawards_cols = make_flat_sheet(
    tab=TAB_SUBAWARDS, group="data",
    csv_name="contract_subawards", table_name="Subawards",
    banner="§1 - First-tier subawards",
    intro="Raw first-tier FFATA subawards (SAM, by prime PIID). amount_type=subaward "
          "- a separate money universe; never summed with prime obligations.",
    width_fn=contract_width,
    float_cols=_FLOAT, int_cols=_INT, date_cols=_DATE,
    input_cols=_FLOAT + _DATE,
)
