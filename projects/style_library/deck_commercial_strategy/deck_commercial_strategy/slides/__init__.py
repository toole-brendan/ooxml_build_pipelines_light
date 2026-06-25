"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str), ``CHARTS`` (list[dict]), and
``IMAGES`` (list[dict]) attributes that deck_core.lib.build_pptx reads to wire
slide layouts, native chart parts, and pictures.

Reference corpus ported 1:1 from the Commercial Strategy Market Analysis deck.
Modules are emitted by _tools/convert_slide.py and may be hand-polished after.

  src 59 | ships_act_volume_by_type | SHIPS Act Volume by Type (stacked-column native chart + overlays)
"""
from __future__ import annotations

from . import (
    research_scope,              # src 3:   Research scope - objectives x focus-area framework (diagram)
    project_calendar,            # src 4:   Project Calendar - timeline table + numbered milestones
    ships_act_volume_by_type,    # src 59:  SHIPS Act Volume by Type (stacked-column native chart)
    cost_comparison_automation,  # src 104: Cost Comparison (1/3) - automation vs conventional
)

SLIDE_RENDERS: list[tuple] = [
    (research_scope, research_scope.render),
    (project_calendar, project_calendar.render),
    (ships_act_volume_by_type, ships_act_volume_by_type.render),
    (cost_comparison_automation, cost_comparison_automation.render),
]
