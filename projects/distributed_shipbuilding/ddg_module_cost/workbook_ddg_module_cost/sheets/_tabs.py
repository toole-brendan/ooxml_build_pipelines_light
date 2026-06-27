"""_tabs - canonical worksheet (tab) names, in one place.

Local non-sheet helper (like _layout / _cuts / _widths). Tab names are
load-bearing: formulas/accessors reference a sheet by value and the packager
rejects duplicates rather than renaming. Centralizing the names here means a
rename happens in exactly one place.

Tab structure (group-contiguous, canonical summary -> guide -> inputs -> data order):
  [summary]  Module Cost
  [guide]    Structural Hierarchy
  [inputs]   Assumptions
  [data]     Ship Cost Basis · Outfit Context
"""
from __future__ import annotations

TAB_MODULE_COST       = "Module Cost"
TAB_STRUCTURAL_HIER   = "Structural Hierarchy"
TAB_ASSUMPTIONS       = "Assumptions"
TAB_SHIP_COST_BASIS   = "Ship Cost Basis"
TAB_OUTFIT_CONTEXT    = "Outfit Context"

# All <= 31 chars (Excel sheet-name limit); the packager re-asserts this.
assert all(len(n) <= 31 for n in (
    TAB_MODULE_COST, TAB_STRUCTURAL_HIER, TAB_ASSUMPTIONS,
    TAB_SHIP_COST_BASIS, TAB_OUTFIT_CONTEXT,
))
