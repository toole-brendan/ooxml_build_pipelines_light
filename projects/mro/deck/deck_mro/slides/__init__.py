"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Porting status: building the 15 slides of the v3.3 deck 1:1 (see the project plan).
The registry is filled slide-by-slide; the vertical slice starts with the cover.

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_mro/slides/<name>.py.
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order.
"""
from __future__ import annotations

from . import (
    cover_mro,                       # 01 cover (slideLayout1)
    overview,                        # 02 context + objectives
    definitions,                     # 03 five sizing levels
    bottom_up_approach,              # 04 FPDS PSC filter funnel -> $9.0B
    vessel_taxonomy,                 # 05 Navy + USCG hull taxonomy table
    work_segments,                   # 06 work-segment split (chart blank) + coverage table
    tam_composition,                 # 07 segment x hull composition (Mekko blank) + commentary
    topdown_detail,                  # 08 top-down budget rollup table + static stacked bar
    topdown_funnel,                  # 09 budget -> non-public-NSY funding funnel (native chart)
    reconciliation_bridge,           # 10 top-down vs bottom-up bridge table + oval markers
    private_addressable,             # 11 non-public-NSY cross-check tiles + callout
    fleet_structure,                 # 12 Marauder-like comp-set tier-roster table
    fleet_mro,                       # 13 Marauder-like fleet MRO static Marimekko
    sam_sizing,                      # 14 TAM -> SAM sizing (Blank layout)
    contract_vehicles,               # 15 contract vehicles & qualifications table
)

SLIDE_RENDERS: list[tuple] = [
    (cover_mro, cover_mro.render),
    (overview, overview.render),
    (definitions, definitions.render),
    (bottom_up_approach, bottom_up_approach.render),
    (vessel_taxonomy, vessel_taxonomy.render),
    (work_segments, work_segments.render),
    (tam_composition, tam_composition.render),
    (topdown_detail, topdown_detail.render),
    (topdown_funnel, topdown_funnel.render),
    (reconciliation_bridge, reconciliation_bridge.render),
    (private_addressable, private_addressable.render),
    (fleet_structure, fleet_structure.render),
    (fleet_mro, fleet_mro.render),
    (sam_sizing, sam_sizing.render),
    (contract_vehicles, contract_vehicles.render),
]
