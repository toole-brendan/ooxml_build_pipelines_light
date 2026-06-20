"""cover - deck title slide.

Binds to the Saronic Cover layout (slideLayout1) via cover_layout(); exempt from
breadcrumb, Preliminary chip, and Sources (structural slide). Sets only the
words: title (28pt), subtitle (20pt italic), and a Month YYYY date footer.

Spec/house: deck_core/slide_guide.md -> Cover and divider copy.
"""
from __future__ import annotations

from deck_core.primitives import slide, cover_layout

LAYOUT = "slideLayout1"   # Cover layout

_TITLE = "Distributed Shipbuilding Supplier Market"
_SUBTITLE = ("DDG and submarine new-construction component suppliers, "
             "FY2022–FY2027")
_FOOTER = "June 2026"


def render() -> str:
    """Cover composition (no breadcrumb / chip / sources)."""
    return slide(cover_layout(_TITLE, _SUBTITLE, footer=_FOOTER))
