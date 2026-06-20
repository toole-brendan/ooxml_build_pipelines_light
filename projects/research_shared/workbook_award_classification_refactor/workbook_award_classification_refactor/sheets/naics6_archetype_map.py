"""naics6_archetype_map - the NAICS-6 -> archetype crosswalk (leaf reference).

One row per observed subawardee NAICS-6 industry code, giving the DEFAULT 3-axis
archetype - Capability Domain (D), Operating Role (R, internal), Primary Output (P) -
used to tag a program-vendor row when that UEI has no hand-researched override. R is the
internal validation axis (carried here, not published per-vendor). Resolution / Review /
R-P Lattice / High-Integration Gate are the QA flags; the per-axis rationale and any
caveat fold into hover Notes on the D / R / P / Resolution cells. Built from
extracted/naics6_archetype_map.csv.

Promoted accessor (imported by the program-vendor sheets, Phase 2):
  naics_map_cols(header) -> "'NAICS-6 Archetype Map'!$X$first:$X$last".
"""
from __future__ import annotations

from workbook_award_classification_refactor.sheets._flat import make_flat_sheet
from workbook_award_classification_refactor.sheets._tabs import TAB_NAICS_MAP
from workbook_award_classification_refactor.sheets._widths import (
    W_NAICS, W_NAICS_DESC, W_CONF, W_CODE, W_DOMFOR,
)

# NAICS-6 | Title | D | R(internal) | P | Resolution | Review | R-P Lattice | Gate
_WIDTHS = [W_NAICS, W_NAICS_DESC, W_CONF, W_CONF, W_CONF, W_CONF, W_CODE,
           W_DOMFOR, W_DOMFOR]

NAICS_ARCHETYPE_MAP, naics_map_cols = make_flat_sheet(
    tab=TAB_NAICS_MAP, group="guide",
    csv_name="naics6_archetype_map", table_name="Naics6ArchetypeMap",
    banner="§1 - NAICS-6 to archetype crosswalk",
    intro="One row per observed NAICS-6: the default Capability Domain, Operating Role (internal) and Primary Output used when a vendor has no research override.",
    widths=_WIDTHS,
    # leaf source values rendered blue: the lookup key + the three classification codes.
    input_cols=["NAICS-6", "Capability Domain (D)",
                "Operating Role (R, internal)", "Primary Output (P)"],
    # per-axis rationale + caveat fold into hover Notes (dropped from the visible table).
    note_from_verbatim={
        "Capability Domain (D)": "D Rationale",
        "Operating Role (R, internal)": "R Rationale",
        "Primary Output (P)": "P Rationale",
        "Resolution": "Notes / Caveats",
    },
)
