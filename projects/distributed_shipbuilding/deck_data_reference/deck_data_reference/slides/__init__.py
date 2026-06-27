"""Slide registry - ONE module per rendered slide (one file = one <p:sld>).

Slide order = the order of SLIDE_RENDERS below. Each entry is a
(module, render_fn) tuple, where render_fn() -> a complete <p:sld> XML string
and the module may carry ``LAYOUT`` (str) and ``CHARTS`` (list[dict]) attributes
that deck_core.lib.build_pptx reads to wire slide layouts and native chart parts.

This deck is a single slide: the plain methodology backup (PIID scope, the
Capability-Domain / Primary-Output classification archetypes, native award
fields), lifted from the deck_primary pipeline.
"""
from __future__ import annotations

from . import (
    data_reference,   # 1: plain methodology backup - PIID scope, classification archetypes, native award fields
)

SLIDE_RENDERS: list[tuple] = [
    (data_reference, data_reference.render),
]
