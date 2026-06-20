"""Sheet registry - ONE module per rendered sheet (one file = one tab).

Tab order = the order of SHEETS below. Each sheet module exposes a single
tables.SheetEntry (or a module with render()); each declares its group (see
workbook_core.groups), and the blocks below keep each group contiguous and in
groups.SHEET_GROUPS order (summary -> guide -> inputs -> model -> data ->
outputs -> validation -> sources -> chartdata). package_workbook() asserts that
invariant at build time.

Module files are named ``<group>_<tab-slug>.py`` (the spec files in
workbook/sheet_specs/ match 1:1).

This pipeline is freshly scaffolded: SHEETS is EMPTY. Until at least one sheet
module is registered, ``python build_workbook.py`` raises a helpful SystemExit
(see workbook_sea_range_telemetry/lib.py build()).

Shared NON-sheet helper already in place (imported by the sheet modules that
need it; NOT registered here):
  - _layout    : RowCursor - a local row cursor over the workbook_core primitives

To add a sheet:
  1. Copy workbook_core/sheet_base_template.py to
     workbook_sea_range_telemetry/sheets/<group>_<slug>.py (group in groups.SHEET_GROUPS).
  2. Fill the metadata + INTENT/LAYOUT, build the rows, and expose a single
     tables.SheetEntry (or a module-level render()).
  3. Import the module below and place its entry in its group's block in SHEETS,
     keeping each group contiguous and in groups.SHEET_GROUPS order.
"""
from __future__ import annotations

SHEETS: list = []
