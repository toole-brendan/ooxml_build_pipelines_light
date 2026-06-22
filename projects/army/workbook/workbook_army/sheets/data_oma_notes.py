"""data_oma_notes - O&M watercraft EVIDENCE notes (NOT a funding profile).

O&M has no discrete watercraft line item; watercraft sustainment lives bundled inside OP-5
Subactivity Groups. So this is an evidence table, not a time series: each row is a SAG
context + a (bundled) amount + narrative + relevance flag. amount_is_watercraft_discrete=N
means the dollars are NOT watercraft-only - DO NOT sum amount_k. The one watercraft-specific
signal is the FY27 Composite Watercraft Company stand-up (relevance=direct).

Promoted accessor: oma_cols(header) -> "'O&M Watercraft Notes'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_army.sheets._flat import make_flat_sheet
from workbook_army.sheets._tabs import TAB_OMA_NOTES
from workbook_army.sheets._widths import contract_width

OMA_NOTES, oma_cols = make_flat_sheet(
    tab=TAB_OMA_NOTES, group="data",
    csv_name="budget_oma_watercraft_notes", table_name="OmaWatercraftNotes",
    banner="§1 - O&M evidence",
    intro="Watercraft O&M is bundled in OP-5 SAGs - context only, never summed. FY27 "
          "Composite Watercraft Company is the force-structure signal.",
    width_fn=contract_width,
    float_cols=["amount_k"], int_cols=["page"], input_cols=["amount_k"],
)
