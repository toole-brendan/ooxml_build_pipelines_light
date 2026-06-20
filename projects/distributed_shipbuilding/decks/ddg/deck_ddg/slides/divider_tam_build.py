"""divider_tam_build - section divider 2 (TAM Build)."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "TAM Build"
_SUBTITLE = "Two supplier streams build the market, and a single year carries an outsized share"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
