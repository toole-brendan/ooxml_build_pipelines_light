"""subawardee_parents - the subawardee parent-enrichment dimension (leaf).

One row per subawardee UEI x program: the dollar-modal *standardized* Parent UEI and
its paired (dollar-modal) parent vendor name as reported in the corpus, plus the raw
"; "-joined set of every parent UEI seen for that subawardee (multi-valued, kept for
transparency). The program-vendor sheets XLOOKUP the standardized Parent UEI +
Parent Vendor Name from here (keyed on Subawardee UEI x Program). Pure source
reference. Built from extracted/subawardee_parents.csv (scripts/build_uei_dimensions.py).

Promoted accessor (imported by the program-vendor sheets): `parents_cols(header)` ->
absolute column range "'Subawardee Parents'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_PARENTS
from workbook_award_classification_refactor.sheets._widths import (
    W_UEI, W_PROGRAM, W_VENDOR, W_TEXT,
)

# Subawardee UEI | Program | Vendor name | Parent UEI (standardized) | Parent vendor
# name | Parent UEI(s) (raw set)
_WIDTHS = [W_UEI, W_PROGRAM, W_VENDOR, W_UEI, W_VENDOR, W_TEXT]

SUBAWARDEE_PARENTS, parents_cols = make_flat_sheet(
    tab=TAB_PARENTS, group="data",
    csv_name="subawardee_parents", table_name="SubawardeeParents",
    banner="§1 - Subawardee parents",
    intro="Per-UEI enrichment - parent ownership, not carried in the native subaward reports.",
    widths=_WIDTHS,
)
