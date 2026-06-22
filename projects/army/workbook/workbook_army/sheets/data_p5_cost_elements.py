"""data_p5_cost_elements - the P-5 sub-line cost elements (child-grain budget evidence).

One row per P-5 cost element (LCU SLEP, MIBS, HCCC, PM/CLS, ...) from
extracted/budget_p5_cost_elements.csv - the budget-native decomposition of each P-1 line.
A cost element is FAITHFUL evidence, NOT an analyst work package: the commercial
decomposition lives in the analyst layer (work_packages.csv), keyed off these. unit_cost_k
/ qty_each / total_cost_m are blue source values; is_subtotal flags rollup rows (never sum
a subtotal with its components). raw_context is folded into a hover note for audit.

Promoted accessor: p5_cols(header) -> "'P-5 Cost Elements'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_P5_COST
from workbook_army.sheets._widths import contract_width

P5_COST_ELEMENTS, p5_cols = make_flat_sheet(
    tab=TAB_P5_COST, group="data",
    csv_name="budget_p5_cost_elements", table_name="P5CostElements",
    banner="§1 - P-5 cost elements (sub-line; child-grain evidence)",
    intro="P-5 cost-element decomposition per P-1 line ($M). Subtotal rows are rollups - "
          "never sum a subtotal with its components.",
    width_fn=contract_width,
    float_cols=["unit_cost_k", "qty_each", "total_cost_m"], int_cols=["page"],
    input_cols=["unit_cost_k", "qty_each", "total_cost_m"],
    note_from_verbatim={"cost_element": "raw_context"},
)
