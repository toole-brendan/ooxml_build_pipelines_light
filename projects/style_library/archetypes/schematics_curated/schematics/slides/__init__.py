"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core.lib.build_pptx reads to wire
slide layouts, native chart parts, and pictures.

Reference corpus of *schematic*-archetype slides ported 1:1 from the source
market-analysis decks. Modules are emitted by the converter at
style_library/_tools/convert_slide.py and may be hand-polished.

Entries are grouped by source deck and kept in source-slide order so the corpus
reads coherently.
"""
from __future__ import annotations

from . import (
    # ── Commercial Strategy Market Analysis (20260325) ──
    ships_act_overview,              # src 11:  SHIPS Act Overview - foreign penalties fund domestic SCF (flow diagram + flag icons)
    value_chain_maritime_transport,  # src 30:  Value Chain (Maritime Transport) - who captures value (3 tables + shapes)
    value_chain_participation,       # src 31:  Value Chain Participation - shipbuilders not vertically integrated (grouped icons)
    addressable_demand,              # src 41:  Addressable Demand - definitions of US-built/flagged oceangoing demand (6 tables)
    ships_act_captive_demand,        # src 60:  SHIPS Act Captive Demand - MSTF supports ~100 more vessels than mandated (styled chart + mandate table)
    approach_unit_economics,         # src 120: Approach (1/2) - determining unit economics
    approach_volume_and_price,       # src 121: Approach (2/2) - annual volume and price per unit
    freight_charges,                 # src 134: Freight Charges - ~70% of westbound charges are vessel-related (styled chart + cost table)
    # ── Market Sizing: Navy (Surface incl MDA) (20251120) ──
    funding_components,              # src 15:  Components - funding inputs/sources/colors of money for Navy (Surface) sizing (flow diagram)
    tcv_approach_usv,                # src 17:  Approach to find TCV - USV-specified
    tcv_approach_manned,             # src 18:  Approach to find TCV - currently manned capabilities
    tcv_to_acv_company_acv,          # src 19:  TCV to ACV Approach - Finding Company ACV (styled chart + table + grouped icons)
    tcv_approach_iamd,               # src 29:  Approach to find TCV - IAMD (OBBBA and SHIELD)
)

SLIDE_RENDERS: list[tuple] = [
    (ships_act_overview, ships_act_overview.render),
    (value_chain_maritime_transport, value_chain_maritime_transport.render),
    (value_chain_participation, value_chain_participation.render),
    (addressable_demand, addressable_demand.render),
    (ships_act_captive_demand, ships_act_captive_demand.render),
    (approach_unit_economics, approach_unit_economics.render),
    (approach_volume_and_price, approach_volume_and_price.render),
    (freight_charges, freight_charges.render),
    # ── Market Sizing: Navy (Surface incl MDA) (20251120) ──
    (funding_components, funding_components.render),
    (tcv_approach_usv, tcv_approach_usv.render),
    (tcv_approach_manned, tcv_approach_manned.render),
    (tcv_to_acv_company_acv, tcv_to_acv_company_acv.render),
    (tcv_approach_iamd, tcv_approach_iamd.render),
]
