"""_tabs - canonical worksheet (tab) names, in one place.

Local non-sheet helper (like _layout / _cuts / _widths / _taxonomy). Tab names
are load-bearing: cross-sheet formulas reference a sheet by its exact name (the
``*_cols`` / ``*_total_cell`` accessors embed ``'<tab>'!`` in formula strings),
and the packager rejects duplicates rather than renaming. Centralizing the names
here means a rename happens in exactly one place and every accessor that embeds
it follows automatically.

Naming rule (sheet_guide.md "Human workbook standard"): tab names read like
analyst-built worksheet names - short, no ``§`` (the ``§N - …`` convention is for
SECTION banners inside a sheet, not the tab). Each consolidated tab opens with a
title banner equal to its tab name, then ``§N - short noun phrase`` sections.

The tab structure (group-contiguous, canonical
summary -> inputs -> model -> data -> validation -> sources order). The former
Indicators / Market Views / Detail Tables coordinator tabs are now split one tab
per section so every table owns its own column widths and autofilter:
  Executive Summary · Assumptions ·
  [model] Supplier Lanes · Periodic Sourcing · Wave Cadence · Continuous Sourcing ·
          Concentration · Source Diversification · Program · Work Type ·
          Vessel & Builder · PIID · Vendor ·
  [data]  Lane Detail · Lane Vendors · Lane Vendor FY · Award Waves ·
          Wave Vendors · Role Detail · Prime Awards ·
  Checks (hidden) · Sources
"""
from __future__ import annotations

TAB_SUMMARY        = "Executive Summary"  # was "Summary" / "Overview"
TAB_INPUTS         = "Assumptions"      # was "Inputs"
TAB_SUPPLIER_LANES = "Supplier Lanes"   # was "PIID x Work Type"

# model: the periodic-sourcing screen + its wave-cadence companion, then the 2
# other indicator screens, now one tab each. "Periodic Sourcing" (not "Re-buy
# Timing"): only periodic, cadence-applicable lanes get a dated forecast here -
# continuous lanes are routed to Continuous Sourcing. ("Re-buy" stays in the
# methodology narrative; FSRS subaward data observes reported awards, not a
# formal prime solicitation/competition, so neither is a "recompete".)
TAB_REBUY_TIMING           = "Periodic Sourcing"
TAB_WAVE_CADENCE           = "Wave Cadence"
TAB_CONTINUOUS_SOURCING    = "Continuous Sourcing"
TAB_CONCENTRATION          = "Concentration"
TAB_SOURCE_DIVERSIFICATION = "Source Diversification"

# model: the 5 former Market Views cuts, now one tab each ("&" not "/" - the
# slash is illegal in a sheet name)
TAB_PROGRAM        = "Program"
TAB_WORK_TYPE      = "Work Type"
TAB_VESSEL_BUILDER = "Vessel & Builder"
TAB_PIID           = "PIID"
TAB_VENDOR         = "Vendor"

# data: the leaf tables, one tab each (incl. the award-wave leaves + the four
# computed-signal leaves that let the model tabs stay formula-only: the per-lane
# signal table, the raw award-event stream, the per-wave-pair composition, and
# the long-form window sensitivity)
TAB_LANE_DETAIL      = "Lane Detail"
TAB_LANE_VENDORS     = "Lane Vendors"
TAB_LANE_VENDOR_FY   = "Lane Vendor FY"
TAB_AWARD_WAVES      = "Award Waves"
TAB_WAVE_VENDORS     = "Wave Vendors"
TAB_ROLE_DETAIL      = "Role Detail"
TAB_PRIME_AWARDS     = "Prime Awards"
TAB_AWARD_EVENTS     = "Award Events"
TAB_EVENT_DATES      = "Event Dates"
TAB_LANE_SIGNALS     = "Lane Signals"
TAB_WAVE_PAIRS       = "Wave Pair Metrics"
TAB_WAVE_SENSITIVITY = "Wave Sensitivity"

TAB_CHECKS         = "Checks"           # was "Tie-Outs" (stays hidden)
TAB_SOURCES        = "Sources"          # new

# All <= 31 chars (Excel sheet-name limit); the packager re-asserts this.
assert all(len(n) <= 31 for n in (
    TAB_SUMMARY, TAB_INPUTS, TAB_SUPPLIER_LANES,
    TAB_REBUY_TIMING, TAB_WAVE_CADENCE, TAB_CONTINUOUS_SOURCING,
    TAB_CONCENTRATION, TAB_SOURCE_DIVERSIFICATION,
    TAB_PROGRAM, TAB_WORK_TYPE, TAB_VESSEL_BUILDER, TAB_PIID, TAB_VENDOR,
    TAB_LANE_DETAIL, TAB_LANE_VENDORS, TAB_LANE_VENDOR_FY, TAB_AWARD_WAVES,
    TAB_WAVE_VENDORS, TAB_ROLE_DETAIL, TAB_PRIME_AWARDS,
    TAB_AWARD_EVENTS, TAB_EVENT_DATES, TAB_LANE_SIGNALS, TAB_WAVE_PAIRS,
    TAB_WAVE_SENSITIVITY, TAB_CHECKS, TAB_SOURCES,
))
