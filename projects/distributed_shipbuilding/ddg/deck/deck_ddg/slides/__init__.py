"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_ddg/slides/<name>.py.
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order.
"""
from __future__ import annotations

from . import (
    cover_market_sizing,             # cover (slideLayout1)
    divider_market_and_scope,        # section divider (slideLayout2)
    market_primer,
    executive_summary,
    scope,
    divider_tam_build,               # section divider (slideLayout2)
    cost_funnel,
    myp_redaction,
    tam_methodology,
    annual_tam_build,
    tam_timing,
    divider_sam_work_types,          # section divider (slideLayout2)
    sam_taxonomy,
    work_type_allocation,
    sam_scenarios,
    supplier_landscape,
    ffata_visibility_gap,
    market_direction,
    implications,
    # Appendix
    appendix_definitions_scope,
    appendix_tam_calculation,
    appendix_myp_correction,
    appendix_ap_lltm_sensitivity,
    appendix_ffata_limitations,
    appendix_bucket_rules_supplier_evidence,
)

SLIDE_RENDERS: list[tuple] = [
    (cover_market_sizing, cover_market_sizing.render),
    # Section 1 - Market and Scope
    (divider_market_and_scope, divider_market_and_scope.render),
    (market_primer, market_primer.render),
    (executive_summary, executive_summary.render),
    (scope, scope.render),
    # Section 2 - TAM Build
    (divider_tam_build, divider_tam_build.render),
    (cost_funnel, cost_funnel.render),
    (myp_redaction, myp_redaction.render),
    (tam_methodology, tam_methodology.render),
    (annual_tam_build, annual_tam_build.render),
    (tam_timing, tam_timing.render),
    # Section 3 - SAM and Work Types
    (divider_sam_work_types, divider_sam_work_types.render),
    (sam_taxonomy, sam_taxonomy.render),
    (work_type_allocation, work_type_allocation.render),
    (sam_scenarios, sam_scenarios.render),
    (supplier_landscape, supplier_landscape.render),
    (ffata_visibility_gap, ffata_visibility_gap.render),
    (market_direction, market_direction.render),
    (implications, implications.render),
    # Appendix
    (appendix_definitions_scope, appendix_definitions_scope.render),
    (appendix_tam_calculation, appendix_tam_calculation.render),
    (appendix_myp_correction, appendix_myp_correction.render),
    (appendix_ap_lltm_sensitivity, appendix_ap_lltm_sensitivity.render),
    (appendix_ffata_limitations, appendix_ffata_limitations.render),
    (appendix_bucket_rules_supplier_evidence, appendix_bucket_rules_supplier_evidence.render),
]
