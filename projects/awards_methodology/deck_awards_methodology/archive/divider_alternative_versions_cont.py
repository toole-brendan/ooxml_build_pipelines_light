"""Section divider - Alternative versions (cont.)."""
from __future__ import annotations

from deck_core.primitives import slide, section_divider_layout

LAYOUT = "slideLayout2"   # section divider layout


def render() -> str:
    """Section divider slide for the continued Alternative versions section."""
    return slide(section_divider_layout("Alternative versions (cont.)"))
