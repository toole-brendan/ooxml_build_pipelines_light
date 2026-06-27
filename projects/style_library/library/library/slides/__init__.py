"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core.lib.build_pptx reads to wire
slide layouts, native chart parts, and pictures.

Curated, hand-polished reference corpus of *schematic*-archetype slides ported
1:1 from the source market-analysis decks. The raw converter output lives in the
sibling ``archetypes/schematics/`` (staging) deck; these modules are the frozen,
hand-annotated study copies. Do NOT point the converter's ``--out`` here.

Entries are grouped by source deck and kept in source-slide order (mirroring the
staging registry) so the two decks align slide-for-slide and the corpus reads
coherently.
"""
from __future__ import annotations

from . import (
    # ── Commercial Strategy Market Analysis (20260325) ──
    overview,                        # src 2:   Overview (2 summary tables + logo)
    key_terms_glossary,              # src 5:   For Reference | Key Terms Glossary (3 tables)
    key_findings_demand_build_economics,  # src 8:   Key Findings (1/3) - demand, build cost, vessel economics (table)
    key_findings_financial_outlook,  # src 9:   Key Findings (2/3) - ComboCo financial outlook (table)
    key_findings_what_must_be_true,  # src 10:  Key Findings (3/3) - what must be true to succeed (table)
    ships_act_overview,              # src 11:  SHIPS Act Overview - foreign penalties fund domestic SCF (flow diagram + flag icons)
    value_chain_maritime_transport,  # src 30:  Value Chain (Maritime Transport) - who captures value (3 tables + shapes)
    value_chain_participation,       # src 31:  Value Chain Participation - shipbuilders not vertically integrated (grouped icons)
    archetype_comps_newbuild_prices,  # src 32:  Archetype Comps (1/3) - improvement from rising new-build prices (chart)
    archetype_comps_vocc_performance,  # src 33:  Archetype Comps (2/3) - VOCC performance '21-'22 (chart + table)
    archetype_comps_shipbuilder_margins,  # src 34:  Archetype Comps (3/3) - shipbuilder margin profile across geographies (5 charts, dense)
    addressable_demand,              # src 41:  Addressable Demand - definitions of US-built/flagged oceangoing demand (6 tables)
    fleet_overview,                  # src 42:  US-Flagged, US-Built Fleet Overview (chart)
    status_quo_fleet_outlook,        # src 43:  Status Quo Fleet Outlook - fleet after orderbook deliveries (chart)
    status_quo_outlook_oceangoing,   # src 44:  Status Quo Outlook (Oceangoing Commercial) (chart + table)
    status_quo_outlook_offshore_1,   # src 45:  Status Quo Outlook (Addressable Offshore 1/2) (chart + table)
    status_quo_outlook_offshore_2,   # src 46:  Status Quo Outlook (Addressable Offshore 2/2) (chart)
    ships_act_volume,                # src 51:  SHIPS Act Volume - bill-specified subsidy funding (chart + connectors)
    ships_act_plus_volume,           # src 52:  SHIPS Act "Plus" Volume - demand declines after mid-2030s (chart + connectors)
    us_delivery_capacity,            # src 53:  US Delivery Capacity - expansion driven by Saronic (chart + table)
    ships_act_captive_demand,        # src 60:  SHIPS Act Captive Demand - MSTF supports ~100 more vessels than mandated (styled chart + mandate table)
    assumptions_income_statement_1,  # src 77:  Assumptions & Methodology - Income Statement (1/2) (table)
    assumptions_income_statement_2,  # src 78:  Assumptions & Methodology - Income Statement (2/2) (table)
    approach_unit_economics,         # src 120: Approach (1/2) - determining unit economics
    approach_volume_and_price,       # src 121: Approach (2/2) - annual volume and price per unit
    freight_charges,                 # src 134: Freight Charges - ~70% of westbound charges are vessel-related (styled chart + cost table)
    coordination_archetypes,         # src 166: Coordination Archetypes - entities in the Coordination step (table)
    key_inputs,                      # src 167: Key Inputs (table)
    # ── Market Sizing: Navy (Surface incl MDA) (20251120) ──
    funding_components,              # src 15:  Components - funding inputs/sources/colors of money for Navy (Surface) sizing (flow diagram)
    definitions_market_levels,       # src 16:  Definitions - market broken into five levels (table + nested-circles image)
    tcv_approach_usv,                # src 17:  Approach to find TCV - USV-specified
    tcv_approach_manned,             # src 18:  Approach to find TCV - currently manned capabilities
    tcv_to_acv_company_acv,          # src 19:  TCV to ACV Approach - Finding Company ACV (styled chart + table + grouped icons)
    tcv_approach_iamd,               # src 29:  Approach to find TCV - IAMD (OBBBA and SHIELD)
    # ── Market Sizing: Navy (Undersea) (20251201) ──
    tcv_approach_unmanned_undersea,  # src 15:  Approach to find TCV - Unmanned-specified (flow diagram)
    tcv_approach_manned_undersea,    # src 16:  Approach to find TCV - currently manned capabilities (flow diagram)
    tcv_to_acv_company_acv_undersea,  # src 25:  TCV to ACV Approach - Finding Company ACV (chart + table + grouped icons)
    # ── Market Sizing: Golden Dome (20260116) ──
    comparison_vs_ddgs,              # src 8:   Comparison vs. DDGs - GD MR procurement cost vs four Arleigh Burkes (chart + 2 tables)
    production_outlook_colocated,    # src 11:  Production Outlook - co-located sensors and interceptors (chart)
    production_outlook_separate,     # src 12:  Production Outlook - separate platforms (chart)
)

SLIDE_RENDERS: list[tuple] = [
    # ── Commercial Strategy Market Analysis (20260325) ──
    (overview, overview.render),
    (key_terms_glossary, key_terms_glossary.render),
    (key_findings_demand_build_economics, key_findings_demand_build_economics.render),
    (key_findings_financial_outlook, key_findings_financial_outlook.render),
    (key_findings_what_must_be_true, key_findings_what_must_be_true.render),
    (ships_act_overview, ships_act_overview.render),
    (value_chain_maritime_transport, value_chain_maritime_transport.render),
    (value_chain_participation, value_chain_participation.render),
    (archetype_comps_newbuild_prices, archetype_comps_newbuild_prices.render),
    (archetype_comps_vocc_performance, archetype_comps_vocc_performance.render),
    (archetype_comps_shipbuilder_margins, archetype_comps_shipbuilder_margins.render),
    (addressable_demand, addressable_demand.render),
    (fleet_overview, fleet_overview.render),
    (status_quo_fleet_outlook, status_quo_fleet_outlook.render),
    (status_quo_outlook_oceangoing, status_quo_outlook_oceangoing.render),
    (status_quo_outlook_offshore_1, status_quo_outlook_offshore_1.render),
    (status_quo_outlook_offshore_2, status_quo_outlook_offshore_2.render),
    (ships_act_volume, ships_act_volume.render),
    (ships_act_plus_volume, ships_act_plus_volume.render),
    (us_delivery_capacity, us_delivery_capacity.render),
    (ships_act_captive_demand, ships_act_captive_demand.render),
    (assumptions_income_statement_1, assumptions_income_statement_1.render),
    (assumptions_income_statement_2, assumptions_income_statement_2.render),
    (approach_unit_economics, approach_unit_economics.render),
    (approach_volume_and_price, approach_volume_and_price.render),
    (freight_charges, freight_charges.render),
    (coordination_archetypes, coordination_archetypes.render),
    (key_inputs, key_inputs.render),
    # ── Market Sizing: Navy (Surface incl MDA) (20251120) ──
    (funding_components, funding_components.render),
    (definitions_market_levels, definitions_market_levels.render),
    (tcv_approach_usv, tcv_approach_usv.render),
    (tcv_approach_manned, tcv_approach_manned.render),
    (tcv_to_acv_company_acv, tcv_to_acv_company_acv.render),
    (tcv_approach_iamd, tcv_approach_iamd.render),
    # ── Market Sizing: Navy (Undersea) (20251201) ──
    (tcv_approach_unmanned_undersea, tcv_approach_unmanned_undersea.render),
    (tcv_approach_manned_undersea, tcv_approach_manned_undersea.render),
    (tcv_to_acv_company_acv_undersea, tcv_to_acv_company_acv_undersea.render),
    # ── Market Sizing: Golden Dome (20260116) ──
    (comparison_vs_ddgs, comparison_vs_ddgs.render),
    (production_outlook_colocated, production_outlook_colocated.render),
    (production_outlook_separate, production_outlook_separate.render),
]
