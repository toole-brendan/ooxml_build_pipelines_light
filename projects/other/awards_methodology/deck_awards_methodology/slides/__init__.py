"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Current set: the contracts methodology trio - award-data sourcing, the
obligated-vs-unobligated value distinction, and the recompete-timing schematic.
The prior methodology / alternative-versions modules are retained under
``deck_awards_methodology/archive/`` (not registered, not built).

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_awards_methodology/slides/<name>.py.
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order.
"""
from __future__ import annotations

from . import (
    contracts_recompete_timing,          # 01  recompete-clock swim-lane schematic
    contracts_obligated_vs_unobligated,  # 02  contract-value snapshots vs additive action obligations
    contracts_award_data_sourcing,       # 03  source methodology -> one validated operating model
)

SLIDE_RENDERS: list[tuple] = [
    (contracts_recompete_timing, contracts_recompete_timing.render),
    (contracts_obligated_vs_unobligated, contracts_obligated_vs_unobligated.render),
    (contracts_award_data_sourcing, contracts_award_data_sourcing.render),
]
