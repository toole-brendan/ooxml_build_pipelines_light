"""Sheet registry - the tab order and grouping for the workbook.

ONE module per rendered sheet (one file = one tab). Tab order = the order of
SHEETS below. Each module exposes a single tables.SheetEntry; each declares its
group (see workbook_core.groups), and the blocks below keep each group
contiguous and in groups.SHEET_GROUPS order. This workbook uses
summary -> inputs -> model -> data -> validation -> sources (model before data,
per groups.SHEET_GROUPS). package_workbook() asserts that invariant at build
time.

Each model/data module builds at import via a ``_make_*()`` that writes the
row-2 title banner + its §1 section table and returns ``(SheetEntry, *accessors)``
(or just the SheetEntry); the cross-sheet accessors consumed by Summary / Checks
are module-level names imported straight from the owning sheet module.

Shared NON-sheet helpers (imported by the sheet modules; NOT registered here):
  - _layout    : RowCursor - a local row cursor over the workbook_core primitives
  - _tabs      : canonical tab names (one place to rename a worksheet)
  - _taxonomy  : work-type bucket vocabulary (copy-from the consolidated workbook)
  - _cuts      : shared access to the wb_*.csv data-cut extracts
  - _widths    : column widths + header alignment (one ruler per single-table tab)
"""
from __future__ import annotations

from . import (
    # summary
    summary_overview,
    # inputs (the live control surface + displayed taxonomy reference)
    summary_inputs,
    # model (Supplier Lanes + re-buy/wave-cadence + 2 indicator + 5 market views)
    model_piid_worktype,
    model_rebuy_timing,
    model_wave_cadence,
    model_continuous_sourcing,
    model_concentrated_lanes,
    model_source_concentration,
    model_program,
    model_by_worktype,
    model_by_vessel,
    model_by_piid,
    model_by_vendor,
    # data (the leaf tables everything derives from; the last four are the
    # computed-signal leaves that keep the model tabs formula-only)
    data_lane_detail,
    data_lane_vendors,
    data_lane_vendor_fy,
    data_award_waves,
    data_wave_vendors,
    data_role_detail,
    data_prime_awards,
    data_award_events,
    data_event_dates,
    data_lane_signals,
    data_wave_pairs,
    data_wave_sensitivity,
    # validation
    validation_tie_outs,
    # sources (authored provenance / pull log)
    summary_sources,
)


SHEETS: list = [
    # --- Summary ---
    summary_overview.OVERVIEW,
    # --- Assumptions (live control surface) ---
    summary_inputs.INPUTS,
    # --- Model (Supplier Lanes + re-buy/wave-cadence + 2 indicator + 5 views) ---
    model_piid_worktype.PIID_WORKTYPE,             # Supplier Lanes
    model_rebuy_timing.REBUY_TIMING,               # Periodic Sourcing
    model_wave_cadence.WAVE_CADENCE,               # Wave Cadence
    model_continuous_sourcing.CONTINUOUS_SOURCING,  # Continuous Sourcing
    model_concentrated_lanes.CONCENTRATION,        # Concentration
    model_source_concentration.SOURCE_DIVERSIFICATION,  # Source Diversification
    model_program.PROGRAM,                         # Program
    model_by_worktype.WORK_TYPE,                   # Work Type
    model_by_vessel.VESSEL_BUILDER,                # Vessel & Builder
    model_by_piid.PIID,                            # PIID
    model_by_vendor.VENDOR,                        # Vendor
    # --- Data (the leaf tables everything derives from) ---
    data_lane_detail.LANE_DETAIL,                 # Lane Detail
    data_lane_vendors.LANE_VENDORS,                # Lane Vendors
    data_lane_vendor_fy.LANE_VENDOR_FY,           # Lane Vendor FY
    data_award_waves.AWARD_WAVES,                 # Award Waves
    data_wave_vendors.WAVE_VENDORS,               # Wave Vendors
    data_role_detail.ROLE_DETAIL,                 # Role Detail
    data_prime_awards.PRIME_AWARDS,             # Prime Awards
    data_award_events.AWARD_EVENTS,               # Award Events
    data_event_dates.EVENT_DATES,                 # Event Dates (live wave assign)
    data_lane_signals.LANE_SIGNALS,               # Lane Signals
    data_wave_pairs.WAVE_PAIRS,                   # Wave Pair Metrics
    data_wave_sensitivity.WAVE_SENSITIVITY,       # Wave Sensitivity
    # --- Validation (built hidden - unhide via the sheet menu) ---
    validation_tie_outs.TIE_OUTS,
    # --- Sources (authored provenance / pull log) ---
    summary_sources.SOURCES,
]
