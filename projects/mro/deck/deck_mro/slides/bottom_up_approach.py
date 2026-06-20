"""bottom_up_approach - FPDS PSC filter funnel to $9.0B (v3.3 slide 4).

The Input -> Filter -> Output grid is transcribed VERBATIM from the source: the
background grid (the "Approach steps" column, the step descriptions, and the
italic Input/Filter/Output headers + rules) is the native `<a:tbl>`
(`_chart_xml/slide04_table.xml`), and the nine labelled boxes + straight arrows +
bent-elbow connectors + footer are the source shapes (`_chart_xml/slide04.xml`).

This replaces an earlier hand-built version that flattened the boxes' `tx1`
lumMod/lumOff fills to a single dark fill (wrong shades) and overflowed two box
captions. Transcribing verbatim restores the exact navy ramp and box sizing.
Connector glue (stCxn/endCxn) is stripped by extract_chart so the elbows render
from their own xfrm. Only the chrome is rebuilt from deck_core builders.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip

LAYOUT = "slideLayout4"

_SECTION = "TAM"
_TOPIC = "Bottom-Up Approach"
_TITLE_TOPIC = "Bottom-Up Methodology"
_TAKEAWAY = ("Filtering FPDS awards to 65 ship-MRO service codes sizes the reconciled FPDS-visible "
             "MRO TAM at $9.0B.")

_XML = Path(__file__).parent / "_chart_xml"
_TABLE = (_XML / "slide04_table.xml").read_text(encoding="utf-8")   # verbatim grid background
_ANNOT = (_XML / "slide04.xml").read_text(encoding="utf-8")         # boxes + arrows + elbows + footer
# Copy-style fixes applied at load (durable across a _chart_xml re-extract): tighten the
# USN/USCG domain slash and reformat the transcribed source line to the house convention.
_TABLE = _TABLE.replace("USN / USCG", "USN/USCG")
_ANNOT = _ANNOT.replace("USN / USCG", "USN/USCG")
_ANNOT = _ANNOT.replace(
    "Source: FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard "
    "(65 ship-MRO PSCs). Data as of April 2026.",
    "Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard "
    "(65 ship-MRO PSCs); data as of April 2026",
)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _TABLE + _ANNOT
    )
