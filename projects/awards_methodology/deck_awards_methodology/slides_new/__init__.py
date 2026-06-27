"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Current set (14 slides): two polished openers converted by
``projects/style_library/_tools/convert_slide.py`` from
``Awards_Analysis_Market_Timing_vPrelim`` (slides 1-2:
contract_addressability_gate, the recompete-actionability decision gate, shown
alongside an alt version contract_addressability_gate_updated, and
recompete_timing_window, the award-type recompete window / color-of-money cap),
then an "Other" section divider (slideLayout2), then three modules converted from
``20260626_US Defense_Market Strategy_Kickoff Materials...`` (slides 32-34:
Contract Addressability / Recompete Timing / Recompete Timing and Outlook),
then an "Other 2" section divider (slideLayout2), then the six original Strategic
Contracts / Awards Methodology modules. Superseded module versions are kept in
``slides_new/archived/``; the earlier polished-replacement openers
(contract_addressability_framework_updated, recompete_qualification_filter,
recompete_qualification_filter_updated, recompete_window_updated,
recompete_timing_updated, recompete_window_simplified) were moved to
``deck_awards_methodology/archive/`` (not registered, not built).

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_awards_methodology/slides/<name>.py
     (or convert one with _tools/convert_slide.py).
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order.
"""
from __future__ import annotations

from . import (
    # — converted from Awards_Analysis_Market_Timing_vPrelim (20260626), slides 1-2 —
    contract_addressability_gate,       # 01  Contract Addressability (recompete-actionability decision gate)
    contract_addressability_gate_updated,  # 02  Contract Addressability (alt decision-gate version)
    recompete_timing_window,            # 03  Recompete Timing (award-type window / color-of-money cap)
    divider_other,                      # 04  "Other" section divider (slideLayout2)
    # — converted from US Defense Market Strategy Kickoff (20260626), slides 32-34 —
    contract_addressability_framework,  # 05  Contract Addressability (market-access framework)
    recompete_timing,                   # 06  Recompete Timing
    recompete_timing_outlook,           # 07  Recompete Timing and Outlook
    divider_other_2,                    # 08  "Other 2" section divider (slideLayout2)
    # — original Strategic Contracts / Awards Methodology modules —
    strategic_contracts_table,          # 09  Example Strategic Contracts Page
    contract_addressability,            # 10  Defining Contract Addressability (market-access framework)
    ddg51_supplier_opportunity,         # 11  DDG-51 Supplier Opportunity (MYP cadence + system tables)
    army_watercraft_repair_pool,        # 12  Army Watercraft Ship-Repair Pool (vehicle-gated on-ramp)
    award_data_sourcing,                # 13  Award Data Sourcing (pull/enrich/validate)
    award_data_reference,               # 14  Award Data Reference (prime/subaward field methodology)
)

SLIDE_RENDERS: list[tuple] = [
    (contract_addressability_gate, contract_addressability_gate.render),
    (contract_addressability_gate_updated, contract_addressability_gate_updated.render),
    (recompete_timing_window, recompete_timing_window.render),
    (divider_other, divider_other.render),
    (contract_addressability_framework, contract_addressability_framework.render),
    (recompete_timing, recompete_timing.render),
    (recompete_timing_outlook, recompete_timing_outlook.render),
    (divider_other_2, divider_other_2.render),
    (strategic_contracts_table, strategic_contracts_table.render),
    (contract_addressability, contract_addressability.render),
    (ddg51_supplier_opportunity, ddg51_supplier_opportunity.render),
    (army_watercraft_repair_pool, army_watercraft_repair_pool.render),
    (award_data_sourcing, award_data_sourcing.render),
    (award_data_reference, award_data_reference.render),
]
