"""vessel_taxonomy - the full Navy + USCG hull taxonomy table (v3.3 slide 5).

The wide taxonomy table is transcribed VERBATIM as its native `<a:tbl>`
(`_chart_xml/slide05_table.xml`) -- exact column widths, per-row heights, per-cell
category fills, and the in-cell rotated "Definition" / "Classifications" labels --
rather than re-authored cell-by-cell. The MSC speech-bubble note, the italic
exhibit label, and the (de-hyperlinked) source line are transcribed verbatim
(`_chart_xml/slide05.xml`). Only the chrome is rebuilt from deck_core builders.

This replaces an earlier hand-built version whose row heights / rotated-label
overlays did not match the source.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip

LAYOUT = "slideLayout4"

_SECTION = "TAM"
_TOPIC = "Vessel Taxonomy"
_TAKEAWAY = "MRO TAM scope covers every SECNAV and USCG hull category."

_XML = Path(__file__).parent / "_chart_xml"
_TABLE = (_XML / "slide05_table.xml").read_text(encoding="utf-8")   # verbatim taxonomy table
_ANNOT = (_XML / "slide05.xml").read_text(encoding="utf-8")         # MSC bubble + exhibit label + source
# Copy-style fix at load (durable across a _chart_xml re-extract): number the de-hyperlinked
# source citations under the house "Sources: (1) …" convention.
_ANNOT = _ANNOT.replace("<a:t>Source: </a:t>", "<a:t>Sources: (1) </a:t>")
_ANNOT = _ANNOT.replace("<a:t>Coast Guard Cutter Fleet</a:t>",
                        "<a:t>(2) Coast Guard Cutter Fleet</a:t>")
_ANNOT = _ANNOT.replace("<a:t>Boats of the United States Coast Guard (2024)</a:t>",
                        "<a:t>(3) Boats of the United States Coast Guard (2024)</a:t>")


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _TABLE + _ANNOT
    )
