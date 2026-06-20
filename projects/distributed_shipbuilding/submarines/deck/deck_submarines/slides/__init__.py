"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

This is the REAL deck registry. It holds the cover, all four section dividers,
the promoted body slides (S02-S18), and the trimmed appendix (A1, A3-A6). The SAM/Supplier
section (S12-S16: work_type_taxonomy, bucket_tam, sam_scenarios,
visible_suppliers, sib_exclusion) was built from the deck's slide_specs/ and is
now wired in behind Divider 3. See the project's docs/specs/deck_spec.txt.

Order follows the deck_spec narrative spine:
    Cover (S01)
    Divider 1 - Market and Scope
      S02 Market Primer / S03 Sizing Boundary / S04 Executive Summary
    Divider 2 - TAM Build
      S05 Demand Backdrop / S06 Methodology / S07 Basic Construction /
      S08 TAM Bridge / S09 Annual Cadence / S10 Coefficient Evidence /
      S11 AP/LLTM
    Divider 3 - SAM and Supplier Landscape
      S12 Work-Type Taxonomy / S13 Bucket TAM / S14 SAM Scenarios /
      S15 Visible Suppliers / S16 SIB Exclusion
    Divider 4 - Interpretation
      S17 Data Limits / S18 Implications
    Appendix (breadcrumb-flagged, no divider), in deck_spec sec.5 order:
      A1 Definitions and Scope / A3 AP/LLTM Detail /
      A4 Coefficient Sensitivity / A5 SAM Bucket Crosswalk /
      A6 Top 25 Visible Suppliers
      (A2 Model Map and Figure Register, A7 Data Limitations and Unseen Layer,
      A8 SIB Exclusion Detail, and A9 QA Reconciliation were removed from the
      professional deck; A8's detail is folded into S16 SIB Exclusion.)

Each entry is a (module, module.render) tuple; deck_core.lib.build_pptx reads each
module's optional LAYOUT and CHARTS attributes to wire layouts and chart parts.
"""
from __future__ import annotations

from . import (
    cover_market_sizing_assessment,   # cover (slideLayout1)
    divider_market_scope,
    market_primer,
    sizing_boundary,
    executive_summary,
    divider_tam_build,
    demand_backdrop,
    methodology,
    basic_construction,
    tam_bridge,
    annual_cadence,
    coefficient_evidence,
    ap_and_lltm,
    divider_sam_supplier,
    work_type_taxonomy,
    bucket_tam,
    sam_scenarios,
    visible_suppliers,
    sib_exclusion,
    divider_interpretation,
    data_limits,
    implications,
    # Appendix (deck_spec sec.5 order; A2, A7, A8, A9 removed from the professional deck)
    appendix_definitions_and_scope,
    appendix_ap_and_lltm_detail,
    appendix_coefficient_sensitivity,
    appendix_sam_bucket_crosswalk,
    appendix_top_25_visible_suppliers,
)

SLIDE_RENDERS: list[tuple] = [
    (cover_market_sizing_assessment, cover_market_sizing_assessment.render),
    (divider_market_scope, divider_market_scope.render),
    (market_primer, market_primer.render),
    (sizing_boundary, sizing_boundary.render),
    (executive_summary, executive_summary.render),
    (divider_tam_build, divider_tam_build.render),
    (demand_backdrop, demand_backdrop.render),
    (methodology, methodology.render),
    (basic_construction, basic_construction.render),
    (tam_bridge, tam_bridge.render),
    (annual_cadence, annual_cadence.render),
    (coefficient_evidence, coefficient_evidence.render),
    (ap_and_lltm, ap_and_lltm.render),
    # Divider 3 - SAM and Supplier Landscape, then S12-S16
    (divider_sam_supplier, divider_sam_supplier.render),
    (work_type_taxonomy, work_type_taxonomy.render),    # S12
    (bucket_tam, bucket_tam.render),                    # S13
    (sam_scenarios, sam_scenarios.render),              # S14
    (visible_suppliers, visible_suppliers.render),      # S15
    (sib_exclusion, sib_exclusion.render),              # S16
    (divider_interpretation, divider_interpretation.render),
    (data_limits, data_limits.render),
    (implications, implications.render),
    # Appendix (A2 Model Map, A7 Data Limitations, A8 SIB Exclusion Detail, A9 QA Reconciliation removed)
    (appendix_definitions_and_scope, appendix_definitions_and_scope.render),                  # A1
    (appendix_ap_and_lltm_detail, appendix_ap_and_lltm_detail.render),                        # A3
    (appendix_coefficient_sensitivity, appendix_coefficient_sensitivity.render),              # A4
    (appendix_sam_bucket_crosswalk, appendix_sam_bucket_crosswalk.render),                    # A5
    (appendix_top_25_visible_suppliers, appendix_top_25_visible_suppliers.render),            # A6
]
