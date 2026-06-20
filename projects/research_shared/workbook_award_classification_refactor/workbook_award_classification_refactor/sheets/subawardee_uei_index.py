"""subawardee_uei_index - the master subawardee-UEI dimension (leaf).

Every distinct subawardee UEI x program seen across the three programs (a UEI active
on two programs appears once per program; the Program column distinguishes), with the
primary NAICS-6 code + title looked up per UEI. NAICS-6 uses the same precedence as
the program-vendor sheets (reference is_primary -> SAM fallback -> title backfill).
The program-vendor sheets XLOOKUP the Subawardee Vendor Name, Primary NAICS-6 and
NAICS-6 Description from here (keyed on Subawardee UEI x Program). Built from
extracted/subawardee_uei_index.csv (scripts/build_uei_dimensions.py).

Promoted accessor (imported by the program-vendor sheets): `uei_index_cols(header)` ->
absolute column range "'Subawardee UEI Index'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_UEI_INDEX
from workbook_award_classification_refactor.sheets._widths import (
    W_UEI, W_PROGRAM, W_VENDOR, W_NAICS, W_NAICS_DESC,
)

# Subawardee UEI | Program | Vendor name | Primary NAICS-6 | NAICS-6 description
_WIDTHS = [W_UEI, W_PROGRAM, W_VENDOR, W_NAICS, W_NAICS_DESC]

SUBAWARDEE_UEI_INDEX, uei_index_cols = make_flat_sheet(
    tab=TAB_UEI_INDEX, group="data",
    csv_name="subawardee_uei_index", table_name="SubawardeeUeiIndex",
    banner="§1 - Subawardee UEI index",
    intro="Per-UEI enrichment - NAICS-6 industry, not carried in the native subaward reports.",
    widths=_WIDTHS,
)
