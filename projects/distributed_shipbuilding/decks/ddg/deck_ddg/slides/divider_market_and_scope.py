"""divider_market_and_scope - section divider 1 (Market and Scope)."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "Market and Scope"
_SUBTITLE = "The supplier-addressable market is a narrow slice of total DDG-51 spend"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
