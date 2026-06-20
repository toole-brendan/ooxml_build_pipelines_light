"""divider_sam_supplier - section divider 3."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "SAM and Supplier Landscape"
_SUBTITLE = "The serviceable slice is a menu of work types, and the visible suppliers are a concentrated floor"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
