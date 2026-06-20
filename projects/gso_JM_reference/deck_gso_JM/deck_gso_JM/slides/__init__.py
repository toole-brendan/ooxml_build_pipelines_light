"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core.lib.build_pptx reads to wire
slide layouts, native chart parts, and pictures.

Faithful 1:1 port of the 5-slide GS&O "Strategy Materials Style Guide" deck
(20260615_GS&O_Strategy Materials Style Guide.pptx). Each slide is a worked
example of one exhibit archetype; the floating ``JM:`` reviewer directives in
the source are dropped from the render (captured verbatim in
../../JM_style_notes.md). Built per docs/faithful_deck_port_methodology.md.

  src 1 | bridge_charts_1   | Bridge Charts (1/2): newbuild price-reduction levers
  src 2 | bridge_charts_2   | Bridge Charts (2/2): MR product-tanker opex comps
  src 3 | bar_charts        | Bar Charts: SCF legally-mandated demand
  src 4 | tables            | Tables: opex categories driving cost differential
  src 5 | flow_charts_graph | Flow Charts: SCF subsidy / penalty flow (hybrid semantic-graph + pinned connectors)
"""
from __future__ import annotations

from . import (
    bridge_charts_1,       # src 1: Bridge Charts (1/2) - newbuild price-reduction levers
    bridge_charts_2,       # src 2: Bridge Charts (2/2) - MR product-tanker opex comps
    bar_charts,            # src 3: Bar Charts - SCF legally-mandated demand
    tables,                # src 4: Tables - opex categories driving cost differential
    flow_charts_graph,     # src 5: Flow Charts - hybrid semantic graph (src/dst) + pinned PowerPoint connectors
)

# SLIDE_RENDERS is the source of truth for order and progress (methodology
# Sec. 11); deck order matches the source 1:1.

SLIDE_RENDERS: list[tuple] = [
    (bridge_charts_1, bridge_charts_1.render),
    (bridge_charts_2, bridge_charts_2.render),
    (bar_charts, bar_charts.render),
    (tables, tables.render),
    (flow_charts_graph, flow_charts_graph.render),
]
