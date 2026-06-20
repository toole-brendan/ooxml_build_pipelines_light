"""divider_market_landscape - section divider before the market-landscape slides
(Supplier Layer, Scope and Cost Funnel, Demand Signals).

Binds to the Saronic Section Divider layout (slideLayout2) via
section_divider_layout(); exempt from breadcrumb, Preliminary chip, and Sources.
The subtitle previews the answer qualitatively (no numbers, no terminal period).

Spec/house: deck_core/slide_guide.md -> Cover and divider copy.
"""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"   # Section Divider layout

_SECTION = "Market Landscape"
_SUBTITLE = ("The opportunity is the component layer yards buy out, and demand is "
             "funded")


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
