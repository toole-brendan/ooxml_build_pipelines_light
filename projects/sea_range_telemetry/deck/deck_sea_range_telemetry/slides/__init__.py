"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string and
the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes that
deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

These four appendix methodology slides set the modeling boundary, the evidence
base, and the TAM / SAM build logic for the sea-range telemetry market sizing.

To add a slide:
  1. Copy deck_core/slide_base_template.py to deck_sea_range_telemetry/slides/<name>.py.
  2. Fill the chrome constants + build _body(); add a module-level
     CHARTS = [...] (from deck_core.charts) if the slide has a native chart.
  3. Import the module here and append (<name>, <name>.render) to SLIDE_RENDERS,
     in slide order. Name files for their role: cover_* (slideLayout1),
     divider_* (slideLayout2), appendix_*, or a plain descriptive body name.
"""
from __future__ import annotations

from . import s01_appendix_scope_evidence_boundary
from . import s02_appendix_evidence_base
from . import s03_appendix_tam_build
from . import s04_appendix_sam_build
# alternative_v1 methodology sequence (renders after the existing four).
from . import s05_appendix_methodology_roadmap
from . import s06_appendix_evidence_streams
from . import s07_appendix_tam_build
from . import s08_appendix_sam_build

SLIDE_RENDERS: list[tuple] = [
    (s01_appendix_scope_evidence_boundary, s01_appendix_scope_evidence_boundary.render),
    (s02_appendix_evidence_base, s02_appendix_evidence_base.render),
    (s03_appendix_tam_build, s03_appendix_tam_build.render),
    (s04_appendix_sam_build, s04_appendix_sam_build.render),
    (s05_appendix_methodology_roadmap, s05_appendix_methodology_roadmap.render),
    (s06_appendix_evidence_streams, s06_appendix_evidence_streams.render),
    (s07_appendix_tam_build, s07_appendix_tam_build.render),
    (s08_appendix_sam_build, s08_appendix_sam_build.render),
]
