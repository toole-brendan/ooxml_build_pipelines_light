"""columbia_program_vendors - the Columbia-class program-vendor sheet (thin config).

One row per distinct subawardee UEI on the Columbia-class program across all corpus years
(entity-grain); see _program_vendors for the shared column rationale and live-formula design.
This module binds the Columbia-specific program label, transaction leaf, tab, CSV and intro.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._program_vendors import (
    make_program_vendor_sheet,
)
from workbook_award_classification_refactor.sheets._tabs import TAB_COLUMBIA_PROGRAM
from workbook_award_classification_refactor.sheets.columbia_subaward_transactions import (
    columbia_tx_cols,
)

COLUMBIA_PROGRAM_VENDORS, columbia_pv_cols = make_program_vendor_sheet(
    program="Columbia", tab=TAB_COLUMBIA_PROGRAM, tx_cols=columbia_tx_cols,
    csv_name="columbia_program_vendors", table_name="ColumbiaProgramVendors",
    banner="§1 - Columbia-class subaward recipients",
    intro="Entity-level Columbia suppliers; reported hull-builder first-tier subawards in "
          "constant FY2026$.",
)
