"""divider_tam_build - section divider 2."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "TAM Build"
_SUBTITLE = "The headline rests on one deliberately strict coefficient, even where the evidence would support more"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
