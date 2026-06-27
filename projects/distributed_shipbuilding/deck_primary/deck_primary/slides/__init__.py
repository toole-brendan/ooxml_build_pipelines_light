"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes
that deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Slides 1-3 are ported 1:1 from the v3 working deck (20260605_Defense Demand
Drivers New Construction_v3.pptx - the v2 build re-edited by hand in
PowerPoint and re-exported); slides 4-6 from the v2.0 deck as placeholder
slides (the intended exhibit described in a gray placeholder box, not yet
realized). Slide 7 is the SAM outsourcing-ceiling methodology
discussion-questions table; slide 8 is the plain methodology backup (PIID
scope, work-type taxonomy, native award fields).

Archived (moved to ../archived/, out of the build): the outsourcing-ceiling
method/results set (former slides 7-10: outsourcing_ceiling_method, _v2, _v3
and outsourcing_ceiling_results) and the supplier-lane method pair (former
slides 11-12: supplier_lane_method_part1/part2) with their shared
_lane_method_kit helper.
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
    sam_methodology_outsourcing_ceiling_questions_v2,  # 7: outsourcing-ceiling methodology discussion-questions table
    data_reference,                   # 8: plain methodology backup - PIID scope, work-type taxonomy, native award fields
)

SLIDE_RENDERS: list[tuple] = [
    (outsourced_bc_walk, outsourced_bc_walk.render),
    (worktype_by_program, worktype_by_program.render),
    (outsourced_bc_annual_tam_ref, outsourced_bc_annual_tam_ref.render),
    (penetration_outlook, penetration_outlook.render),
    (worktype_by_fy, worktype_by_fy.render),
    (contracts_outlook_placeholder, contracts_outlook_placeholder.render),
    (sam_methodology_outsourcing_ceiling_questions_v2, sam_methodology_outsourcing_ceiling_questions_v2.render),
    (data_reference, data_reference.render),
]
