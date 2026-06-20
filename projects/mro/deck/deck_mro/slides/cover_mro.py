"""cover_mro - Cover for the Navy & USCG vessel MRO market-sizing deck (v3.3 slide 1)."""
from __future__ import annotations

from deck_core.primitives import slide, cover_layout

LAYOUT = "slideLayout1"

_TITLE = "Vessel MRO Market Sizing"
_SUBTITLE = "U.S. Navy and U.S. Coast Guard vessel MRO, FY2025 TAM and SAM"
_FOOTER = "April 2026"


def render() -> str:
    """Assemble a text-only cover slide using the locked cover layout."""
    return slide(cover_layout(_TITLE, _SUBTITLE, footer=_FOOTER))
