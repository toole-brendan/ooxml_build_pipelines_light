"""overview - SCAFFOLD PLACEHOLDER: proves the deck pipeline emits a valid slide.

This is the seed module from the new-project scaffold. It renders chrome only
(breadcrumb + title + sources line) so ``build_deck.py`` produces a valid 1-slide
.pptx immediately. Replace it with real content modules per deck_core/slide_guide.md:
copy deck_core/slide_base_template.py to a new slides/<name>.py, build _body(),
and register it in slides/__init__.py.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers

# ── chrome text ──────────────────────────────────────────────────────────────
_SECTION  = "U.S. Army"
_TOPIC    = "Market Mapping"
_TAKEAWAY = "scaffold placeholder - replace with the first content slide."
_SOURCES  = "Sources: (1) ...; (2) ...; (3) ..."


def _body() -> str:
    return ""   # chrome-only until you build the body


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
