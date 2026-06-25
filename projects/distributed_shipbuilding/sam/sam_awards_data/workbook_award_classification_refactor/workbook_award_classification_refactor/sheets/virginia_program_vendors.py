"""virginia_program_vendors - the Virginia-class program-vendor sheet (thin config).

One row per distinct subawardee UEI on the Virginia-class program across all corpus years
(entity-grain); see _program_vendors for the shared column rationale and live-formula design.
This module binds the Virginia-specific program label, transaction leaf, tab, CSV and intro.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._program_vendors import (
    make_program_vendor_sheet,
)
from workbook_award_classification_refactor.sheets._tabs import TAB_VIRGINIA_PROGRAM
from workbook_award_classification_refactor.sheets.virginia_subaward_transactions import (
    virginia_tx_cols,
)

VIRGINIA_PROGRAM_VENDORS, virginia_pv_cols = make_program_vendor_sheet(
    program="Virginia", tab=TAB_VIRGINIA_PROGRAM, tx_cols=virginia_tx_cols,
    csv_name="virginia_program_vendors", table_name="VirginiaProgramVendors",
    banner="§1 - Virginia-class subaward recipients",
    intro="Entity-level Virginia suppliers; reported hull-builder first-tier subawards in "
          "constant FY2026$.",
)
