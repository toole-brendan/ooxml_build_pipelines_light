"""cover_market_sizing - Cover for the DDG-51 supplier-market sizing deck."""
from __future__ import annotations

from deck_core.primitives import slide, cover_layout

LAYOUT = "slideLayout1"

_TITLE = "DDG-51 Supplier Market Sizing"
_SUBTITLE = ("TAM and SAM for the DDG-51 new-construction supplier base, "
             "average annual FY2022–FY2027")
_FOOTER = "June 2026"


def render() -> str:
    """Assemble a text-only cover slide using the locked cover layout."""
    return slide(cover_layout(_TITLE, _SUBTITLE, footer=_FOOTER))
