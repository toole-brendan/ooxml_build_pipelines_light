"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

Scaffold status: seeded with a single placeholder body slide (overview) so the
pipeline builds a valid .pptx on first run. Replace it with real content modules.

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_army/slides/<name>.py.
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order.
"""
from __future__ import annotations

from . import (
    overview,                        # 01 placeholder body slide (replace)
)

SLIDE_RENDERS: list[tuple] = [
    (overview, overview.render),
]
