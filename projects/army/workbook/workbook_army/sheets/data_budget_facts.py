"""data_budget_facts - the tidy/long budget funding facts (the funding evidence layer).

One row per (line_item x source_book_fy x exhibit x measure x observed_fy x column_role)
from extracted/budget_funding_facts.csv - the P-40 / R-2 / R-2A funding tables mined from
the FY22-27 PB books. `amount` (in $M, then-year) is the blue source value; identifiers
(line_item_id, observed_fy, source_book_fy, measure, column_role, amount_type) stay exact
strings so the Budget Market / Market Size model sheets can SUMIFS over them. No values are
summed here - the money discipline (never add across amount_type / column_role) lives in
the model sheets. `page` cites the exact PDF page; source_id joins the Source Log.

Promoted accessor: budget_facts_cols(header) -> "'Budget Facts'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_BUDGET_FACTS
from workbook_army.sheets._widths import contract_width

BUDGET_FACTS, budget_facts_cols = make_flat_sheet(
    tab=TAB_BUDGET_FACTS, group="data",
    csv_name="budget_funding_facts", table_name="BudgetFacts",
    banner="§1 - Budget funding facts (tidy/long; P-40 / R-2 / R-2A)",
    intro="Funding facts from the FY22-27 PB books, one row per line x vintage x measure x "
          "year. Never sum across money types ($M, then-year).",
    width_fn=contract_width,
    float_cols=["amount"], int_cols=["page"], input_cols=["amount"],
)
