"""divider_other - section divider ("Other")."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "Other"


def render() -> str:
    return slide(section_divider_layout(_SECTION))
