"""divider_sizing_opportunity - section divider before the sizing slides (Sizing
Chain, TAM Bridge, Supplier Share, Annual Cadence, Work-Type Mix, SAM Scenarios).

Binds to the Saronic Section Divider layout (slideLayout2) via
section_divider_layout(); exempt from breadcrumb, Preliminary chip, and Sources.
The subtitle previews the answer qualitatively (no numbers, no terminal period).

Spec/house: deck_core/slide_guide.md -> Cover and divider copy.
"""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"   # Section Divider layout

_SECTION = "Sizing the Opportunity"
_SUBTITLE = "A budget-led TAM with an allocation-led SAM"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
