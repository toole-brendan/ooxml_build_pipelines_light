"""virginia_subaward_transactions - the COMPLETE raw Virginia-class subaward pull.

One row per deduped published subaward record (subAwardReportId) on the Virginia
class, carrying every field on the raw FSRS `published` object (50 leaf columns;
see ddg_subaward_transactions / scripts/build_program_transactions.py for the
schema). Fact spine behind the Virginia Program Vendors roll-up (Subaward $M /
Actions / First / Last / Domestic-or-Foreign are live formulas over this table,
keyed on Subawardee UEI). NO SAM enrichment here (NAICS-6 lives on the Subawardee
UEI Index).

Promoted accessor (imported by virginia_program_vendors): `virginia_tx_cols(header)`.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._fiscal import (
    TX_EXTRA_COLS, TX_FED_FY, TX_FACTOR, TX_REAL, tx_fy_formulas,
)
from workbook_award_classification_refactor.sheets._tabs import TAB_VIRGINIA_TX
from workbook_award_classification_refactor.sheets._widths import (
    W_UEI, W_VENDOR, W_REPORTID, W_UUID, W_SUBNUM, W_DATE, W_AMOUNT, W_TEXT,
    W_STREET2, W_CITY, W_CD, W_CODE, W_STATE, W_CC, W_COUNTRY, W_ZIP, W_BIZCODE,
    W_PAY, W_PIID, W_CONTRACTKEY, W_REFIDV, W_AWARDTYPE, W_TCV, W_NAICS,
    W_NAICS_DESC, W_ORGCODE, W_NAME, W_TEXT_WIDE,
)

# 50 columns, in build_program_transactions.COLUMNS order (UEI = column B).
_WIDTHS = [
    W_UEI, W_VENDOR, W_VENDOR, W_UEI, W_VENDOR,
    W_REPORTID, W_UUID, W_SUBNUM, W_DATE, W_DATE, W_AMOUNT, W_TEXT,
    W_VENDOR, W_STREET2, W_CITY, W_CD, W_CODE, W_STATE, W_CC, W_COUNTRY, W_ZIP,
    W_BIZCODE, W_TEXT, W_PAY, W_VENDOR,
    W_PIID, W_CONTRACTKEY, W_CODE, W_PIID, W_REFIDV, W_AWARDTYPE, W_TCV, W_DATE,
    W_UEI, W_VENDOR, W_TEXT_WIDE, W_NAICS, W_NAICS_DESC,
    W_ORGCODE, W_NAME, W_ORGCODE, W_NAME, W_ORGCODE, W_NAME,
    W_ORGCODE, W_NAME, W_ORGCODE, W_NAME, W_ORGCODE, W_NAME,
    W_CD, W_CD, W_AMOUNT,               # Federal FY | Deflator Factor | Subaward $ FY2026$
]
assert len(_WIDTHS) == 53, len(_WIDTHS)

_DATE_COLS = ["Subaward Date", "Submitted Date", "Base Award Date Signed"]
_FLOAT_COLS = ["Subaward Amount $", "Total Contract Value $"]
# Transaction-grain constant-FY2026$ columns (sheet-only; see _fiscal / _flat.extra_cols).
_FY_FORMULAS = tx_fy_formulas(
    "virginia_subaward_transactions", date_header="Subaward Date",
    amount_header="Subaward Amount $", extra_cols=TX_EXTRA_COLS)

VIRGINIA_SUBAWARD_TX, virginia_tx_cols = make_flat_sheet(
    tab=TAB_VIRGINIA_TX, group="data",
    csv_name="virginia_subaward_transactions", table_name="VirginiaSubawardTx",
    banner="§1 - Virginia-class subaward transactions",
    intro="Deduplicated Virginia first-tier subaward reports; nominal and constant FY2026$.",
    widths=_WIDTHS,
    int_cols=[TX_FED_FY], float_cols=_FLOAT_COLS + [TX_FACTOR, TX_REAL],
    date_cols=_DATE_COLS, input_cols=_FLOAT_COLS + _DATE_COLS,
    formula_cols=_FY_FORMULAS, extra_cols=TX_EXTRA_COLS,
)
