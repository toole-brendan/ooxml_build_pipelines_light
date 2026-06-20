"""divider_market_scope - section divider 1."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "Market and Scope"
_SUBTITLE = "The addressable opportunity is a narrow layer inside a much larger procurement ecosystem"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
