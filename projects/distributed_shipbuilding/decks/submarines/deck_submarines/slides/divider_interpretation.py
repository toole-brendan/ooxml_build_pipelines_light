"""divider_interpretation - section divider 4."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "Interpretation"
_SUBTITLE = "What the data shows is a visible floor, not the full supplier layer"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
