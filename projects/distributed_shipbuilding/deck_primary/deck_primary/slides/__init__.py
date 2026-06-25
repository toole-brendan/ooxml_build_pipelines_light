"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes
that deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Slides 1-3 are ported 1:1 from the v3 working deck (20260605_Defense Demand
Drivers New Construction_v3.pptx - the v2 build re-edited by hand in
PowerPoint and re-exported); slides 4-6 from the v2.0 deck as placeholder
slides (the intended exhibit described in a gray placeholder box, not yet
realized). Slide 7 is the new-built outsourcing-ceiling sizing slide; slides 8-10
are the outsourcing-ceiling set built to compare side by side - two alternative
methodology treatments (8 = flow + ledger + rail; 9 = the method bridge:
flow spine + p-reads + ledger + guardrails) and a results exhibit (10).
"""
from __future__ import annotations

from . import (
    outsourced_bc_walk,               # v3 1: total ship spend -> outsourced BC walk
    worktype_by_program,              # v3 2: work-type split, submarine vs DDG pools
    # v3 3 superseded: the verbatim port and the chart_ref/layers/data staging twins are kept on disk
    # but unregistered; outsourced_bc_annual_tam_ref is the flattened, self-contained reference that replaces them.
    outsourced_bc_annual_tam_ref,     # v3 3: annual TAM - self-contained native-chart reference (chart mirror + 8 named layers + data-driven penetration)
    penetration_outlook,              # v2.0 4: penetration rate outlook (placeholder)
    worktype_by_fy,                   # v2.0 5: work-type FY stacked bars per class
    contracts_outlook_placeholder,    # v2.0 6: placeholder - contracts outlook table
    outsourcing_ceiling_method,       # 7 (new): how the outsourcing ceiling (the pool) is sized
    outsourcing_ceiling_method_v2,    # 8 (new): alt methodology treatment (flow + ledger + rail)
    outsourcing_ceiling_method_v3,    # 9 (new): method bridge (flow spine + p-reads + ledger + guardrails)
    outsourcing_ceiling_results,      # 10 (new): results exhibit (clustered columns + KPI strip)
    supplier_lane_method_part1,       # 11 (new): supplier-lane method part 1 - build the lane, concentration-first split
    supplier_lane_method_part2,       # 12 (new): supplier-lane method part 2 - track interpretation (maintained / diversifying / periodic / continuous)
    sam_methodology_outsourcing_ceiling_questions_v2,  # 13 (new): outsourcing-ceiling methodology discussion-questions table
    data_reference,                   # 14 (new): plain methodology backup - PIID scope, work-type taxonomy, native award fields
)

SLIDE_RENDERS: list[tuple] = [
    (outsourced_bc_walk, outsourced_bc_walk.render),
    (worktype_by_program, worktype_by_program.render),
    (outsourced_bc_annual_tam_ref, outsourced_bc_annual_tam_ref.render),
    (penetration_outlook, penetration_outlook.render),
    (worktype_by_fy, worktype_by_fy.render),
    (contracts_outlook_placeholder, contracts_outlook_placeholder.render),
    (outsourcing_ceiling_method, outsourcing_ceiling_method.render),
    (outsourcing_ceiling_method_v2, outsourcing_ceiling_method_v2.render),
    (outsourcing_ceiling_method_v3, outsourcing_ceiling_method_v3.render),
    (outsourcing_ceiling_results, outsourcing_ceiling_results.render),
    (supplier_lane_method_part1, supplier_lane_method_part1.render),
    (supplier_lane_method_part2, supplier_lane_method_part2.render),
    (sam_methodology_outsourcing_ceiling_questions_v2, sam_methodology_outsourcing_ceiling_questions_v2.render),
    (data_reference, data_reference.render),
]
