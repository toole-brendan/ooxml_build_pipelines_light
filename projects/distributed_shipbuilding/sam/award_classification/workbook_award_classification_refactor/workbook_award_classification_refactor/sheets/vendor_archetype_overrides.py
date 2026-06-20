"""vendor_archetype_overrides - the hand-researched archetype overrides (leaf input).

One row per researched subawardee UEI x program: the hand-assigned Capability Domain (D)
and Primary Output (P) that take precedence over the NAICS-6 crosswalk default on the
program-vendor sheets. The per-axis research evidence (reasoning + source URLs) folds
into hover Notes on the D / P cells. R is not researched per vendor (it is the internal
axis, defaulted from the crosswalk), so it is not carried here. Built from
extracted/vendor_archetype_overrides.csv (scripts/build_archetype_overrides.py).

Promoted accessor (imported by the program-vendor sheets, Phase 2):
  overrides_cols(header) -> "'Vendor Archetype Overrides'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_ARCHETYPE_OVERRIDES
from workbook_award_classification_refactor.sheets._widths import (
    W_PROGRAM, W_UEI, W_CONF,
)

# Program | Subawardee UEI | Capability Domain (D) | Primary Output (P)
_WIDTHS = [W_PROGRAM, W_UEI, W_CONF, W_CONF]

VENDOR_ARCHETYPE_OVERRIDES, overrides_cols = make_flat_sheet(
    tab=TAB_ARCHETYPE_OVERRIDES, group="data",
    csv_name="vendor_archetype_overrides", table_name="VendorArchetypeOverrides",
    banner="§1 - Hand-researched archetype overrides",
    intro="One row per researched subawardee UEI x program: the hand-assigned Capability Domain and Primary Output that override the NAICS-6 default.",
    widths=_WIDTHS,
    # leaf source values rendered blue: the UEI key + the two override codes.
    input_cols=["Subawardee UEI", "Capability Domain (D)", "Primary Output (P)"],
    # per-axis research evidence folds into hover Notes (dropped from the visible table).
    note_from_verbatim={
        "Capability Domain (D)": "Capability Domain Note",
        "Primary Output (P)": "Primary Output Note",
    },
)
