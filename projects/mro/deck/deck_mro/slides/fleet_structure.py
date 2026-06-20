"""fleet_structure - Marauder-like comp-set by mission-fit tier (v3.3 slide 12).

The tier-roster table is transcribed verbatim (`_chart_xml/slide12_table.xml`); the
mission-fit callout, the exhibit caption, and the footer are transcribed verbatim
(`_chart_xml/slide12.xml`). The analyst "DISCUSS" review-sticky is dropped per the
locked content decisions. Only the chrome is rebuilt from deck_core builders.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip

LAYOUT = "slideLayout4"

_SECTION = "SAM"
_TOPIC = "Fleet Structure"
_TAKEAWAY = ("The Marauder-comparable fleet spans 14 hull programs across three mission-fit tiers "
             "and anchors the SAM vessel universe.")

_XML = Path(__file__).parent / "_chart_xml"
_TABLE = (_XML / "slide12_table.xml").read_text(encoding="utf-8")   # verbatim tier-roster table
_ANNOT = (_XML / "slide12.xml").read_text(encoding="utf-8")         # callout + caption + footer
# Bottom band carries sources only: collapse the transcribed caveat footer to the source line.
_ANNOT = _ANNOT.replace(
    "<a:t>Note: Tier 2 FY2025 total is $0M because LSM, T-LSM, and LCU programs are early in "
    "the procurement cycle and not yet material in obligations. Source: FPDS FY2025 contract "
    "obligations, MSC fleet disposition, USCG Cutter Fleet inventory, Marauder ASV design "
    "envelope. Data as of April 2026.</a:t>",
    "<a:t>Sources: (1) FPDS FY2025 contract obligations; (2) MSC fleet disposition; (3) USCG "
    "Cutter Fleet inventory; (4) Marauder ASV design envelope; data as of April 2026</a:t>",
)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _TABLE + _ANNOT
    )
