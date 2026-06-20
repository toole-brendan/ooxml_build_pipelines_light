"""columbia_subaward_transactions - the COMPLETE raw Columbia-class subaward pull.

One row per deduped published subaward record (subAwardReportId) on the Columbia
class, carrying every field on the raw FSRS `published` object (50 leaf columns;
see ddg_subaward_transactions / scripts/build_program_transactions.py for the
schema). Fact spine behind the Columbia Program Vendors roll-up (Subaward $M /
Actions / First / Last / Domestic-or-Foreign are live formulas over this table,
keyed on Subawardee UEI). NO SAM enrichment here (NAICS-6 lives on the Subawardee
UEI Index).

Promoted accessor (imported by columbia_program_vendors): `columbia_tx_cols(header)`.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_COLUMBIA_TX
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
]
assert len(_WIDTHS) == 50, len(_WIDTHS)

_DATE_COLS = ["Subaward Date", "Submitted Date", "Base Award Date Signed"]
_FLOAT_COLS = ["Subaward Amount $", "Total Contract Value $"]

COLUMBIA_SUBAWARD_TX, columbia_tx_cols = make_flat_sheet(
    tab=TAB_COLUMBIA_TX, group="data",
    csv_name="columbia_subaward_transactions", table_name="ColumbiaSubawardTx",
    banner="§1 - Columbia-class subaward transactions",
    intro="The raw Columbia-class subaward pull, CY2016-2025 - one row per deduped FSRS published report; nominal dollars, with MIB/BlueForge UEIs already removed upstream.",
    widths=_WIDTHS,
    float_cols=_FLOAT_COLS, date_cols=_DATE_COLS,
    input_cols=_FLOAT_COLS + _DATE_COLS,
)
