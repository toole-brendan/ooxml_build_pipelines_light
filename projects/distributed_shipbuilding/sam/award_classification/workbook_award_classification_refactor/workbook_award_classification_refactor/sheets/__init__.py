"""Sheet registry - the tab order and grouping for the workbook.

ONE module per rendered sheet (one file = one tab). Tab order = the order of SHEETS
below. Each module exposes a single tables.SheetEntry and declares its group (see
workbook_core.groups); the blocks below keep each group contiguous and in
groups.SHEET_GROUPS canonical order. package_workbook() asserts that at build time.

Reader-first layers (answer -> scope -> levers -> model -> evidence):
  - summary : the reader-facing answer pages - Executive Summary, the Domain
              Concentration "where to play" cut, and the Market Bridge estimate.
  - guide   : scope & method - Taxonomy and Methodology.
  - inputs  : the editable classification levers - the NAICS-6 archetype crosswalk
              and the hand-researched (Program, UEI) overrides.
  - model   : the derived cuts - the three program-vendor roll-ups (live SUMIFS /
              COUNTIFS / MINIFS / MAXIFS over the transaction leaves + a single
              Supplier Master match-row) plus the per-subsystem SWBS roll-up.
  - data    : the source evidence - the Supplier Master dimension, the SWBS crosswalk,
              the deflators, the prime awards, the HII co-build narrative, and the three
              raw subaward-transaction fact spines.

Shared NON-sheet helpers (imported by the sheet modules; NOT registered here):
  - _layout / _tabs / _widths / _cuts / _flat / _fiscal / _program_vendors / _taxonomy
  - _integrity : the build-stopping (Program x UEI) universe guard (called from lib.build)
"""
from __future__ import annotations

from . import (
    # summary (reader-facing answer pages)
    executive_summary,
    domain_concentration,
    parent_concentration,
    subaward_activity,
    market_bridge,
    # guide (scope & method)
    taxonomy,
    guide_methodology,
    # inputs (editable classification levers)
    naics6_archetype_map,
    vendor_archetype_overrides,
    # model (derived program-vendor roll-ups + per-subsystem SWBS roll-up)
    ddg_program_vendors,
    ddg_swbs_rollup,
    virginia_program_vendors,
    columbia_program_vendors,
    # data (source evidence: dimension + crosswalk + deflators + primes + co-build + raw transaction spines)
    supplier_master,
    hii_swbs_crosswalk,
    deflators,
    prime_awards,
    hii_co_build,
    ddg_subaward_transactions,
    virginia_subaward_transactions,
    columbia_subaward_transactions,
)


SHEETS: list = [
    # --- Summary (the answer pages) ---
    executive_summary.EXECUTIVE_SUMMARY,
    domain_concentration.DOMAIN_CONCENTRATION,
    parent_concentration.PARENT_CONCENTRATION,
    subaward_activity.SUBAWARD_ACTIVITY,
    market_bridge.MARKET_BRIDGE,
    # --- Guide (scope & method) ---
    taxonomy.TAXONOMY,
    guide_methodology.METHODOLOGY,
    # --- Inputs (editable classification levers) ---
    naics6_archetype_map.NAICS_ARCHETYPE_MAP,
    vendor_archetype_overrides.VENDOR_ARCHETYPE_OVERRIDES,
    # --- Model (derived program-vendor roll-ups + per-subsystem SWBS roll-up) ---
    ddg_program_vendors.DDG_PROGRAM_VENDORS,
    ddg_swbs_rollup.DDG_SWBS_ROLLUP,
    virginia_program_vendors.VIRGINIA_PROGRAM_VENDORS,
    columbia_program_vendors.COLUMBIA_PROGRAM_VENDORS,
    # --- Data (source evidence: dimension + crosswalk + deflators + primes + co-build + raw fact spines) ---
    supplier_master.SUPPLIER_MASTER,
    hii_swbs_crosswalk.HII_SWBS_CROSSWALK,
    deflators.DEFLATORS,
    prime_awards.PRIME_AWARDS,
    hii_co_build.HII_CO_BUILD,
    ddg_subaward_transactions.DDG_SUBAWARD_TX,
    virginia_subaward_transactions.VIRGINIA_SUBAWARD_TX,
    columbia_subaward_transactions.COLUMBIA_SUBAWARD_TX,
]
