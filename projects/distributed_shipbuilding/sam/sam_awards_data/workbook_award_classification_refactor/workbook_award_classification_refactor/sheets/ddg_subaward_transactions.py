"""ddg_subaward_transactions - the COMPLETE raw DDG-51 subaward pull, SWBS-tagged.

One row per deduped published subaward record (subAwardReportId) on the DDG-51 program,
carrying every field on the raw FSRS `published` object (50 leaf columns; see
scripts/build_program_transactions.py) PLUS the Ship Work Breakdown Structure (SWBS) tag
(5 columns appended by scripts/tag_ddg_transactions_swbs.py). This is the finest-grain
fact spine behind BOTH roll-ups: the program-vendor sheets key on Subawardee UEI, and the
DDG SWBS by Ship-System roll-up keys on the SWBS Subsystem resolved here.

The SWBS tag: `HII Work-Item Code` + `Builder` are hardcoded leaves (joined / derived by the
tagger). The crosswalk MATCH is done ONCE per row in a sheet-only `SWBS Match Row` helper
(appended after the CSV columns); `SWBS Subsystem`, `SWBS`, `SWBS basis` are LIVE formulas that
INDEX that matched row (Builder-gated, so GD-BIW rows - which carry no SWBS - read blank / n/a
and HII rows with an unmapped code land in U00). One MATCH instead of three over ~6.4k rows.

Promoted accessor (imported by the program-vendor + SWBS roll-up sheets): `ddg_tx_cols`.
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import (
    make_flat_sheet, swbs_match_row, swbs_from_row, flat_header_letters,
)
from workbook_award_classification_refactor.sheets._fiscal import (
    TX_EXTRA_COLS, TX_FED_FY, TX_FACTOR, TX_REAL, tx_fy_formulas,
)
from workbook_award_classification_refactor.sheets._tabs import TAB_DDG_TX
from workbook_award_classification_refactor.sheets.hii_swbs_crosswalk import (
    swbs_xwalk_cols,
)
from workbook_award_classification_refactor.sheets._widths import (
    W_UEI, W_VENDOR, W_REPORTID, W_UUID, W_SUBNUM, W_DATE, W_AMOUNT, W_TEXT,
    W_STREET2, W_CITY, W_CD, W_CODE, W_STATE, W_CC, W_COUNTRY, W_ZIP, W_BIZCODE,
    W_PAY, W_PIID, W_CONTRACTKEY, W_REFIDV, W_AWARDTYPE, W_TCV, W_NAICS,
    W_NAICS_DESC, W_ORGCODE, W_NAME, W_TEXT_WIDE, W_SUPTYPE,
)

# 55 columns = 50 raw (build_program_transactions.COLUMNS order, UEI = column B) + 5 SWBS.
_WIDTHS = [
    W_UEI, W_VENDOR, W_VENDOR, W_UEI, W_VENDOR,                 # subawardee entity
    W_REPORTID, W_UUID, W_SUBNUM, W_DATE, W_DATE, W_AMOUNT, W_TEXT,   # the subaward
    W_VENDOR, W_STREET2, W_CITY, W_CD, W_CODE, W_STATE, W_CC, W_COUNTRY, W_ZIP,  # address
    W_BIZCODE, W_TEXT, W_PAY, W_VENDOR,                          # business types / exec comp
    W_PIID, W_CONTRACTKEY, W_CODE, W_PIID, W_REFIDV, W_AWARDTYPE, W_TCV, W_DATE,  # prime ctx
    W_UEI, W_VENDOR, W_TEXT_WIDE, W_NAICS, W_NAICS_DESC,         # prime entity / naics
    W_ORGCODE, W_NAME, W_ORGCODE, W_NAME, W_ORGCODE, W_NAME,     # funding org
    W_ORGCODE, W_NAME, W_ORGCODE, W_NAME, W_ORGCODE, W_NAME,     # contracting org
    W_CODE, W_SUPTYPE, W_CODE, W_TEXT_WIDE, W_TEXT,            # SWBS: code | builder | subsystem | SWBS | basis
    W_CD,                                                     # SWBS Match Row (sheet-only helper)
    W_CD, W_CD, W_AMOUNT,              # Federal FY | Deflator Factor | Subaward $ FY2026$
]
assert len(_WIDTHS) == 59, len(_WIDTHS)

_DATE_COLS = ["Subaward Date", "Submitted Date", "Base Award Date Signed"]
_FLOAT_COLS = ["Subaward Amount $", "Total Contract Value $"]

# SWBS tag: MATCH the row's HII work-item code into the crosswalk ONCE (the SWBS Match Row
# helper, a sheet-only column appended after the CSV), gated on Builder; the three SWBS outputs
# then INDEX that matched row. Builder / code / match-row column letters are resolved by NAME
# (flat_header_letters) so no column letter is hardcoded in this module.
_SWBS_EXTRA = ["SWBS Match Row"]
_EXTRA = _SWBS_EXTRA + TX_EXTRA_COLS            # SWBS helper + Federal FY / factor / FY2026$
_L = flat_header_letters("ddg_subaward_transactions", extra_cols=_EXTRA)
_XW_CODE = swbs_xwalk_cols("HII Work-Item Code")
_XW_SUBSYS = swbs_xwalk_cols("SWBS Subsystem")
_XW_SWBS = swbs_xwalk_cols("SWBS")
_XW_BASIS = swbs_xwalk_cols("SWBS basis")


def _bld(r):  return f"${_L['Builder']}{r}"
def _code(r): return f"${_L['HII Work-Item Code']}{r}"
def _mrow(r): return f"${_L['SWBS Match Row']}{r}"


_FORMULAS = {
    "SWBS Match Row": lambda r: swbs_match_row(_bld(r), _code(r), _XW_CODE),
    "SWBS Subsystem": lambda r: swbs_from_row(_bld(r), _mrow(r), _XW_SUBSYS,
                                              na="", unmapped="U00"),
    "SWBS":           lambda r: swbs_from_row(_bld(r), _mrow(r), _XW_SWBS,
                                              na="n/a (non-HII-Ingalls)",
                                              unmapped="U00 No SWBS Evidence"),
    "SWBS basis":     lambda r: swbs_from_row(_bld(r), _mrow(r), _XW_BASIS,
                                              na="-", unmapped="U - no SWBS evidence"),
}
_FORMULAS.update(tx_fy_formulas(
    "ddg_subaward_transactions", date_header="Subaward Date",
    amount_header="Subaward Amount $", extra_cols=_EXTRA))

DDG_SUBAWARD_TX, ddg_tx_cols = make_flat_sheet(
    tab=TAB_DDG_TX, group="data",
    csv_name="ddg_subaward_transactions", table_name="DdgSubawardTx",
    banner="§1 - DDG-51 subaward transactions",
    intro="Deduplicated DDG-51 first-tier subaward reports; nominal and constant FY2026$.",
    widths=_WIDTHS,
    int_cols=_SWBS_EXTRA + [TX_FED_FY], float_cols=_FLOAT_COLS + [TX_FACTOR, TX_REAL],
    date_cols=_DATE_COLS, input_cols=_FLOAT_COLS + _DATE_COLS,
    formula_cols=_FORMULAS, extra_cols=_EXTRA,
    # the once-per-row crosswalk match index is a formula helper, not reader content.
    hidden_headers=_SWBS_EXTRA,
)

# Guard: the pre-build letter resolver must agree with the sheet make_flat_sheet actually built,
# so the same-sheet SWBS + FY formulas reference the real columns.
_GUARD_COLS = ("Builder", "HII Work-Item Code", "SWBS Match Row", TX_FED_FY, TX_FACTOR, TX_REAL)
assert all(f"!${_L[h]}$" in ddg_tx_cols(h) for h in _GUARD_COLS), {
    h: (_L[h], ddg_tx_cols(h)) for h in _GUARD_COLS}
