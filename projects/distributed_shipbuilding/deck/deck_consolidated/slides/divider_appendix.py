"""divider_appendix - section divider before the appendix (Definitions, the
methodology deep-dives, Method Deltas, Bucket Crosswalk).

Binds to the Saronic Section Divider layout (slideLayout2) via
section_divider_layout(); exempt from breadcrumb, Preliminary chip, and Sources.
No subtitle (an appendix has no governing thought to preview).

Spec/house: deck_core/slide_guide.md -> Cover and divider copy.
"""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"   # Section Divider layout

_SECTION = "Appendix"


def render() -> str:
    return slide(section_divider_layout(_SECTION))
