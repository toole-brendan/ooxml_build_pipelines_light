"""Sheet registry - the tab order and grouping for the workbook.

ONE module per rendered sheet (one file = one tab). Tab order = the order of
SHEETS below. Each module exposes a single tables.SheetEntry; each declares its
group (see workbook_core.groups), and the blocks below keep each group contiguous
and in groups.SHEET_GROUPS order. This workbook uses guide -> model -> data;
package_workbook() asserts that invariant at build time.

Three layers:
  - guide : the classification legend (Taxonomy) + method (Methodology).
  - model : the three program-vendor sheets - entity-grain derived cuts whose
            Subaward $M / Actions / First / Last columns are LIVE SUMIFS / COUNTIFS /
            MINIFS / MAXIFS over the transaction leaf below.
  - data  : the raw source pulls - one subaward-transaction fact sheet per program
            (the formula spine; it also carries each transaction's domestic/foreign
            flag + country) plus two per-UEI dimension sheets (NAICS index, parents).

Shared NON-sheet helpers (imported by the sheet modules; NOT registered here):
  - _layout   : RowCursor - a local row cursor over the workbook_core primitives
  - _tabs     : canonical tab names (one place to rename a worksheet)
  - _widths   : column widths + header alignment
  - _cuts     : raw-string access to the extracted per-sheet CSVs (+ date_serial)
  - _flat     : shared single-table sheet builder for the flat tabs
  - _taxonomy : the finalized 3-axis classification vocabulary (constants)
"""
from __future__ import annotations

from . import (
    # guide (the classification legend + method + NAICS-6 crosswalk)
    taxonomy,
    guide_methodology,
    naics6_archetype_map,
    # model (refactored program-vendor sheets - live roll-ups over the tx leaf)
    ddg_program_vendors,
    virginia_program_vendors,
    columbia_program_vendors,
    # data (raw transaction fact sheets - the roll-up spine)
    ddg_subaward_transactions,
    virginia_subaward_transactions,
    columbia_subaward_transactions,
    # data (per-UEI dimension sheets + the hand-researched archetype overrides)
    subawardee_uei_index,
    subawardee_parents,
    vendor_archetype_overrides,
)


SHEETS: list = [
    # --- Guide ---
    taxonomy.TAXONOMY,
    guide_methodology.METHODOLOGY,
    naics6_archetype_map.NAICS_ARCHETYPE_MAP,
    # --- Model (derived program-vendor roll-ups) ---
    ddg_program_vendors.DDG_PROGRAM_VENDORS,
    virginia_program_vendors.VIRGINIA_PROGRAM_VENDORS,
    columbia_program_vendors.COLUMBIA_PROGRAM_VENDORS,
    # --- Data (raw transaction fact spine) ---
    ddg_subaward_transactions.DDG_SUBAWARD_TX,
    virginia_subaward_transactions.VIRGINIA_SUBAWARD_TX,
    columbia_subaward_transactions.COLUMBIA_SUBAWARD_TX,
    # --- Data (per-UEI dimensions + archetype overrides) ---
    subawardee_uei_index.SUBAWARDEE_UEI_INDEX,
    subawardee_parents.SUBAWARDEE_PARENTS,
    vendor_archetype_overrides.VENDOR_ARCHETYPE_OVERRIDES,
]
