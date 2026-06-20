"""ddg_subaward_transactions - the COMPLETE raw DDG-51 subaward transaction pull.

One row per deduped published subaward record (subAwardReportId) on the DDG-51
program, carrying every field on the raw FSRS `published` object (50 leaf columns;
see scripts/build_program_transactions.py for the schema). This is the finest-grain
fact spine behind the DDG Program Vendors roll-up: the vendor sheet's Subaward $M /
Actions / First / Last / Domestic-or-Foreign are live SUMIFS / COUNTIFS / MINIFS /
MAXIFS / IF over THIS table, keyed on Subawardee UEI. Subaward Amount $, Total
Contract Value $, and the three dates are blue hardcoded source values; everything
else is raw text. NO SAM enrichment lives here - the subawardee's NAICS-6 is an
entity attribute on the Subawardee UEI Index.

Promoted accessor (imported by ddg_program_vendors): `ddg_tx_cols(header)` ->
absolute column range "'DDG Subaward Transactions'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_DDG_TX
from workbook_award_classification_refactor.sheets._widths import (
    W_UEI, W_VENDOR, W_REPORTID, W_UUID, W_SUBNUM, W_DATE, W_AMOUNT, W_TEXT,
    W_STREET2, W_CITY, W_CD, W_CODE, W_STATE, W_CC, W_COUNTRY, W_ZIP, W_BIZCODE,
    W_PAY, W_PIID, W_CONTRACTKEY, W_REFIDV, W_AWARDTYPE, W_TCV, W_NAICS,
    W_NAICS_DESC, W_ORGCODE, W_NAME, W_TEXT_WIDE,
)

# 50 columns, in build_program_transactions.COLUMNS order (UEI = column B).
_WIDTHS = [
    W_UEI, W_VENDOR, W_VENDOR, W_UEI, W_VENDOR,                 # subawardee entity
    W_REPORTID, W_UUID, W_SUBNUM, W_DATE, W_DATE, W_AMOUNT, W_TEXT,   # the subaward
    W_VENDOR, W_STREET2, W_CITY, W_CD, W_CODE, W_STATE, W_CC, W_COUNTRY, W_ZIP,  # address
    W_BIZCODE, W_TEXT, W_PAY, W_VENDOR,                          # business types / exec comp
    W_PIID, W_CONTRACTKEY, W_CODE, W_PIID, W_REFIDV, W_AWARDTYPE, W_TCV, W_DATE,  # prime ctx
    W_UEI, W_VENDOR, W_TEXT_WIDE, W_NAICS, W_NAICS_DESC,         # prime entity / naics
    W_ORGCODE, W_NAME, W_ORGCODE, W_NAME, W_ORGCODE, W_NAME,     # funding org
    W_ORGCODE, W_NAME, W_ORGCODE, W_NAME, W_ORGCODE, W_NAME,     # contracting org
]
assert len(_WIDTHS) == 50, len(_WIDTHS)

_DATE_COLS = ["Subaward Date", "Submitted Date", "Base Award Date Signed"]
_FLOAT_COLS = ["Subaward Amount $", "Total Contract Value $"]

DDG_SUBAWARD_TX, ddg_tx_cols = make_flat_sheet(
    tab=TAB_DDG_TX, group="data",
    csv_name="ddg_subaward_transactions", table_name="DdgSubawardTx",
    banner="§1 - DDG-51 subaward transactions",
    intro="The raw DDG-51 subaward pull, CY2013-2026 - one row per deduped FSRS published report; nominal dollars, with GFE primes and MIB/BlueForge UEIs already removed upstream.",
    widths=_WIDTHS,
    float_cols=_FLOAT_COLS, date_cols=_DATE_COLS,
    input_cols=_FLOAT_COLS + _DATE_COLS,
)
