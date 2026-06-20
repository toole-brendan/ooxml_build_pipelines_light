"""_tabs - canonical worksheet (tab) names, in one place.

Local non-sheet helper (like _layout / _cuts / _widths). Tab names are
load-bearing: the packager rejects duplicates rather than renaming, and a native
table sits on a named sheet. Centralizing the names here means a rename happens in
exactly one place.

Tab structure (group-contiguous, canonical guide -> model -> data order):
  [guide] Taxonomy · Methodology
  [model] DDG Program Vendors · Virginia Program Vendors · Columbia Program Vendors
  [data]  DDG/Virginia/Columbia Subaward Transactions (the fact spine; each row
          carries its own domestic/foreign flag + country) ·
          Subawardee UEI Index · Subawardee Parents
"""
from __future__ import annotations

TAB_TAXONOMY         = "Taxonomy"
TAB_METHODOLOGY      = "Methodology"
TAB_NAICS_MAP        = "NAICS-6 Archetype Map"
TAB_DDG_PROGRAM      = "DDG Program Vendors"
TAB_VIRGINIA_PROGRAM = "Virginia Program Vendors"
TAB_COLUMBIA_PROGRAM = "Columbia Program Vendors"
# raw transaction fact sheets (one row per subaward report id)
TAB_DDG_TX           = "DDG Subaward Transactions"
TAB_VIRGINIA_TX      = "Virginia Subaward Transactions"
TAB_COLUMBIA_TX      = "Columbia Subaward Transactions"
# UEI-dimension sheets (one row per UEI x program)
TAB_UEI_INDEX        = "Subawardee UEI Index"
TAB_PARENTS          = "Subawardee Parents"
# archetype crosswalk (NAICS-6 default) + the hand-researched (Program, UEI) overrides
TAB_ARCHETYPE_OVERRIDES = "Vendor Archetype Overrides"

# All <= 31 chars (Excel sheet-name limit); the packager re-asserts this.
assert all(len(n) <= 31 for n in (
    TAB_TAXONOMY, TAB_METHODOLOGY, TAB_NAICS_MAP,
    TAB_DDG_PROGRAM, TAB_VIRGINIA_PROGRAM, TAB_COLUMBIA_PROGRAM,
    TAB_DDG_TX, TAB_VIRGINIA_TX, TAB_COLUMBIA_TX,
    TAB_UEI_INDEX, TAB_PARENTS, TAB_ARCHETYPE_OVERRIDES,
))
