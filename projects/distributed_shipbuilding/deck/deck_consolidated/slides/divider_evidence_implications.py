"""divider_evidence_implications - section divider before the evidence and
implications slides (Supplier Visibility, Where to Play, Entry Wedge).

Binds to the Saronic Section Divider layout (slideLayout2) via
section_divider_layout(); exempt from breadcrumb, Preliminary chip, and Sources.
The subtitle previews the answer qualitatively (no numbers, no terminal period).

Spec/house: deck_core/slide_guide.md -> Cover and divider copy.
"""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"   # Section Divider layout

_SECTION = "Evidence and Implications"
_SUBTITLE = "Assessing opportunities and the current supplier landscape"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
