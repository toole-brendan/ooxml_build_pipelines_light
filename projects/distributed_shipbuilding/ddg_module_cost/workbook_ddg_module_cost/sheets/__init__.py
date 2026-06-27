"""Sheet registry - the tab order and grouping for the ddg_module_cost workbook.

ONE module per rendered sheet (one file = one tab). Tab order = the order of
SHEETS below. Each module exposes a single tables.SheetEntry declaring its group
(see workbook_core.groups); the packager keeps each group contiguous and in
groups.SHEET_GROUPS order (summary -> guide -> inputs -> data -> validation).

Layers:
  - summary : the answer page (Module Cost: the cascade).
  - guide   : the build hierarchy (Structural Hierarchy).
  - inputs  : the single edit surface (Assumptions: anchor FY, counts, weights).
  - data    : the cost basis (Ship Cost Basis) + supplier context (Outfit Context).

Dependency (import) order is leaves -> answer and self-enforced by Python imports:
  ship_cost_basis -> assumptions -> module_cost.

Shared NON-sheet helpers (imported by the sheet modules; NOT registered here):
  _layout · _tabs · _widths · _cuts · _italic · _factor · _inputfill.
"""
from __future__ import annotations

from . import (
    # summary
    module_cost,
    # guide
    structural_hierarchy,
    # inputs
    assumptions,
    # data
    ship_cost_basis,
    outfit_context,
)


SHEETS: list = [
    # --- Summary ---
    module_cost.MODULE_COST,
    # --- Guide ---
    structural_hierarchy.STRUCTURAL_HIERARCHY,
    # --- Inputs ---
    assumptions.ASSUMPTIONS,
    # --- Data ---
    ship_cost_basis.SHIP_COST_BASIS,
    outfit_context.OUTFIT_CONTEXT,
]
