"""divider_other_2 - section divider ("Other 2")."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "Other 2"


def render() -> str:
    return slide(section_divider_layout(_SECTION))
