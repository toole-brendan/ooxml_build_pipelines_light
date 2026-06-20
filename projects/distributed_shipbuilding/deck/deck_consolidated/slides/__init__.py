"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Deck structure:
  Cover -> front-row Outsourced BC story (walk, annual TAM outlook, work type)
  -> [Market Landscape divider] -> executive answer + market slides
  -> [Sizing the Opportunity divider] -> sizing slides
  -> [Evidence and Implications divider] -> evidence/implications slides
  -> [Appendix divider] -> methodology roadmap + four methodology deep-dives.

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_consolidated/slides/<name>.py.
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order.
"""
from __future__ import annotations

# Cover + section dividers (structural slides).
from . import cover
from . import divider_market_landscape
from . import divider_sizing_opportunity
from . import divider_evidence_implications
from . import divider_appendix

# Front-row Outsourced BC story (fr1-fr4, deck order after the cover).
from . import fr1_body_outsourced_bc_walk
from . import fr2_body_worktype_by_program
from . import fr3_body_outsourced_bc_annual_tam
from . import fr4_body_worktype_by_fy

# Body slides.
from . import s02_body_executive_answer
from . import s04_body_ecosystem_map
from . import s05_body_scope_cost_funnel
from . import s06_body_demand_backdrop
from . import s08_body_methodology_process_rail
from . import s09_body_tam_bridge_ap_lltm
from . import s10_body_supplier_share_evidence
from . import s11_body_annual_cadence
from . import s12_body_work_type_allocation
from . import s13_body_sam_scenario_menu
from . import s14_body_supplier_visibility

# Appendix: methodology roadmap + the four methodology deep-dive pages. (The
# older definitions / deltas / crosswalk and m1-m3 pages are retired to
# deck/archived/ and intentionally excluded from the build. The Where-to-Play
# scorecard and Entry-Wedge thesis slides are likewise retired to deck/archived/.)
from . import appendix_methodology_roadmap
from . import appendix_tam_budget_base_scope_gates
from . import appendix_supplier_share_pop_conversion
from . import appendix_sam_classification_field_audit
from . import appendix_sam_allocation_scenario_views

SLIDE_RENDERS: list[tuple] = [
    # Cover + the front-row Outsourced BC story (the manager's four slides,
    # vDraft order: walk -> work type -> annual TAM -> work type by FY).
    (cover, cover.render),
    # fr1: the walk from total ship spend to outsourced BC, with the ledger.
    (fr1_body_outsourced_bc_walk, fr1_body_outsourced_bc_walk.render),
    # fr2: work type by program/class (cumulative) + classifier panel.
    (fr2_body_worktype_by_program, fr2_body_worktype_by_program.render),
    # fr3: annual TAM in clustered per-class columns with denominator outlines,
    # penetration strips and the FY2028-FY2031 implied outlook (s11 stays).
    (fr3_body_outsourced_bc_annual_tam, fr3_body_outsourced_bc_annual_tam.render),
    # fr4: work type by FY, per class, FY2022-FY2025.
    (fr4_body_worktype_by_fy, fr4_body_worktype_by_fy.render),
    # Market Landscape.
    (divider_market_landscape, divider_market_landscape.render),
    # One-page answer (Supplier TAM and SAM) - first slide after the divider.
    (s02_body_executive_answer, s02_body_executive_answer.render),
    (s04_body_ecosystem_map, s04_body_ecosystem_map.render),
    (s05_body_scope_cost_funnel, s05_body_scope_cost_funnel.render),
    (s06_body_demand_backdrop, s06_body_demand_backdrop.render),
    # Sizing the Opportunity.
    (divider_sizing_opportunity, divider_sizing_opportunity.render),
    (s08_body_methodology_process_rail, s08_body_methodology_process_rail.render),
    (s09_body_tam_bridge_ap_lltm, s09_body_tam_bridge_ap_lltm.render),
    (s10_body_supplier_share_evidence, s10_body_supplier_share_evidence.render),
    (s11_body_annual_cadence, s11_body_annual_cadence.render),
    (s12_body_work_type_allocation, s12_body_work_type_allocation.render),
    (s13_body_sam_scenario_menu, s13_body_sam_scenario_menu.render),
    # Evidence and Implications.
    (divider_evidence_implications, divider_evidence_implications.render),
    (s14_body_supplier_visibility, s14_body_supplier_visibility.render),
    # Appendix.
    (divider_appendix, divider_appendix.render),
    # Methodology roadmap - the reader's map for the appendix.
    (appendix_methodology_roadmap, appendix_methodology_roadmap.render),
    # TAM budget base + scope gates - the denominator proof.
    (appendix_tam_budget_base_scope_gates, appendix_tam_budget_base_scope_gates.render),
    # Supplier-share / POP conversion - budget bases -> fixed supplier TAM pool.
    (appendix_supplier_share_pop_conversion, appendix_supplier_share_pop_conversion.render),
    # SAM classification field audit - award evidence -> auditable work-type shares.
    (appendix_sam_classification_field_audit, appendix_sam_classification_field_audit.render),
    # SAM allocation + scenario views - the final allocation board.
    (appendix_sam_allocation_scenario_views, appendix_sam_allocation_scenario_views.render),
]
