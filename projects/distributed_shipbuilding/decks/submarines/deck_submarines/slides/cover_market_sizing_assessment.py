"""cover_market_sizing_assessment - Cover for the U.S. submarine supplier-market sizing deck."""
from __future__ import annotations

from deck_core.primitives import slide, cover_layout

LAYOUT = "slideLayout1"

_TITLE = "Submarine Supplier Market Sizing"
_SUBTITLE = ("TAM and SAM for the U.S. submarine new-construction supplier base, "
             "average annual FY2022–FY2027")
_FOOTER = "June 2026"


def render() -> str:
    """Assemble a text-only cover slide using the locked cover layout."""
    return slide(cover_layout(_TITLE, _SUBTITLE, footer=_FOOTER))
