"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Current set: six slides auto-converted by
``projects/style_library/_tools/convert_slide.py`` (mechanical first pass) --
the four "Strategic Contracts" slides from
``20260624_Strategic Contracts_vPreliminary.pptx`` (01-04), plus two slides
lifted from ``20260626_US Defense_Market Strategy_Kickoff Materials...`` (the
example strategic-contracts page = source slide 10, and the award-data-sourcing
workflow = source slide 33). The prior recompete-cadence / addressability
working modules were retired to ``deck_awards_methodology/archive/`` (not
registered, not built).

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
    strategic_contracts_table,         # 01  Example Strategic Contracts Page (US Defense deck, slide 10)
    contract_addressability,           # 02  Defining Contract Addressability (market-access framework)
    ddg51_supplier_opportunity,        # 03  DDG-51 Supplier Opportunity (MYP cadence + system tables)
    army_watercraft_repair_pool,       # 04  Army Watercraft Ship-Repair Pool (vehicle-gated on-ramp)
    award_data_sourcing,               # 05  Award Data Sourcing (pull/enrich/validate; US Defense deck, slide 33)
    award_data_reference,              # 06  Award Data Reference (prime/subaward field methodology)
)

SLIDE_RENDERS: list[tuple] = [
    (strategic_contracts_table, strategic_contracts_table.render),
    (contract_addressability, contract_addressability.render),
    (ddg51_supplier_opportunity, ddg51_supplier_opportunity.render),
    (army_watercraft_repair_pool, army_watercraft_repair_pool.render),
    (award_data_sourcing, award_data_sourcing.render),
    (award_data_reference, award_data_reference.render),
]
