"""Sheet registry - tab order and grouping for the 9-tab workbook.

Tab order = the order of SHEETS below. Each entry is a tables.SheetEntry with a
group (workbook_core.groups); the blocks keep each group contiguous and in
groups.SHEET_GROUPS order: summary -> inputs -> model -> data -> validation ->
sources. package_workbook() asserts that invariant at build time.

Shared NON-sheet helpers (imported by the sheet modules; NOT registered):
  - _layout : RowCursor over the workbook_core primitives
  - _widths : column widths + header-alignment helper
"""
from __future__ import annotations

from . import (
    # summary
    summary_overview,
    # inputs (the single edit surface)
    inputs_assumptions,
    # model (ceiling -> bridge -> headroom)
    model_ceiling,
    model_bridge,
    model_headroom,
    # data (the P-5c cost base everything links to)
    data_cost_base,
    # validation
    validation_sensitivity,
    validation_tie_outs,
    # sources
    sources_source_index,
)


SHEETS: list = [
    # --- Summary ---
    summary_overview.OVERVIEW,
    # --- Inputs ---
    inputs_assumptions.ASSUMPTIONS,
    # --- Model ---
    model_ceiling.CEILING_MODEL,
    model_bridge.CONVERSION_BRIDGE,
    model_headroom.HEADROOM,
    # --- Data ---
    data_cost_base.COST_BASE,
    # --- Validation ---
    validation_sensitivity.SENSITIVITY,
    validation_tie_outs.TIE_OUTS,
    # --- Sources ---
    sources_source_index.SOURCES,
]
