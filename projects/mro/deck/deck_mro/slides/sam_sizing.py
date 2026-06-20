"""sam_sizing - TAM -> SAM sizing (v3.3 slide 14).

This slide sits on the "Blank" layout (slideLayout5), so its breadcrumb / title /
Preliminary chrome are authored as ordinary shapes rather than layout placeholders
-- everything except the analyst "DISCUSS" sticky is therefore transcribed verbatim
(`_chart_xml/slide14.xml` = chrome + the TAM->SAM funnel tiles / arrows / labels;
`_chart_xml/slide14_table.xml` = the Note/Detail table). The DISCUSS sticky is
dropped per the locked content decisions.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide

LAYOUT = "slideLayout5"

_XML = Path(__file__).parent / "_chart_xml"
_ANNOT = (_XML / "slide14.xml").read_text(encoding="utf-8")          # chrome + funnel shapes
# Copy-style fix applied at load (durable across a _chart_xml re-extract): drop the "Note:"
# self-label and the "per Definitions slide" cross-reference, restructure the em-dash, tighten
# the J998/J999 slash, and reformat the source line to the house "Sources: (1) …" convention.
_ANNOT = _ANNOT.replace(
    "<a:t>Note: SAM = Serviceable Addressable Market per Definitions slide — depot ship repair "
    "spend (PSCs J998 / J999) on Marauder-like hulls. Source: FPDS FY2025 contract obligations. "
    "Data as of April 2026.</a:t>",
    "<a:t>Sources: (1) FPDS FY2025 contract obligations; data as of April 2026</a:t>",
)
# Title heading: no casual abbreviations ("comp-set") and no trailing fragment.
_ANNOT = _ANNOT.replace(
    "Intersecting the Marauder-like fleet with depot ship repair lands SAM at ",
    "Intersecting the Marauder-comparable fleet with depot ship repair sizes SAM at ")
_ANNOT = _ANNOT.replace("<a:t>% of TAM and 82% of Marauder-like comp-set MRO</a:t>",
                        "<a:t>% of TAM.</a:t>")
_TABLE = (_XML / "slide14_table.xml").read_text(encoding="utf-8")    # verbatim Note/Detail table


def render() -> str:
    return slide(_ANNOT + _TABLE)
