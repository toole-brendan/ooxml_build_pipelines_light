"""divider_sam_work_types - section divider 3 (SAM and Work Types)."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"

_SECTION = "SAM and Work Types"
_SUBTITLE = "The serviceable market is a menu of work types, not a single capture number"


def render() -> str:
    return slide(section_divider_layout(_SECTION, _SUBTITLE))
