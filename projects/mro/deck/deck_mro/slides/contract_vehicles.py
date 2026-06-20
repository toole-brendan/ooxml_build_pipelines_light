"""contract_vehicles - contract vehicles & qualifications (v3.3 slide 15).

The five-vehicle qualifications table is transcribed verbatim
(`_chart_xml/slide15_table.xml`); the qualification-paths callout, the exhibit
caption, and the footer are transcribed verbatim (`_chart_xml/slide15.xml`). The
analyst "DISCUSS" review-sticky is dropped per the locked content decisions. Only
the chrome is rebuilt from deck_core builders.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip

LAYOUT = "slideLayout4"

_SECTION = "SAM"
_TOPIC = "Contract Vehicles"
_TITLE_TOPIC = "Contract Vehicles & Qualifications"
_TAKEAWAY = ("MSRA and MAC-MO carry ~84% of Navy depot MRO, with Coast Guard cutter repair on a "
             "separate USCG track.")

_XML = Path(__file__).parent / "_chart_xml"
_TABLE = (_XML / "slide15_table.xml").read_text(encoding="utf-8")   # verbatim vehicles table
_ANNOT = (_XML / "slide15.xml").read_text(encoding="utf-8")         # callout + caption + footer
# Copy-style fix applied at load (durable across a _chart_xml re-extract): restructure the
# transcribed em-dashes and the "+" separator (no em dashes / lazy separators in rendered copy).
_ANNOT = _ANNOT.replace("OASIS+ — not gates", "OASIS+; not gates")
_TABLE = _TABLE.replace("technical services — not depot repair",
                        "technical services; not depot repair")
_TABLE = _TABLE.replace("Separate gate — not Navy MSRA", "Separate gate, not Navy MSRA")
_TABLE = _TABLE.replace("certification + qualified Dockmaster",
                        "certification and qualified Dockmaster")
# Tighten domain-pair slashes and reformat the transcribed source line (the body already
# uses (1)/(2) for content points, so the source list stays unnumbered to avoid a clash).
_ANNOT = _ANNOT.replace("SAM / UEI registration:", "SAM/UEI registration:")
# Bottom band carries sources only: collapse the qualification-paths commentary footer to the
# source line (its headline already lives in the title).
_ANNOT = _ANNOT.replace(
    "<a:t>(1) ~84% of FY2025 Navy depot obligations ($4.1B of $4.9B) awarded to MSRA-holders "
    "under MAC-MO regional pools, priced as FFP delivery orders. Remaining ~16%: Trade IDIQ "
    "carve-outs, FDNF pierside (foreign MSRAs), SeaPort-NxG overflow, direct-award small "
    "services. (2) Coast Guard cutter MRO runs on a separate USCG / SFLC track; drydock work "
    "requires Std Spec 8634 facility certification. Source: FPDS FY2025 obligations; DFARS "
    "217.71 (Master Agreements); GAO MAC-MO references; CNRMC MSRA instruction (2025); USCG "
    "Std Spec 8634. Data as of April 2026.</a:t>",
    "<a:t>Sources: FPDS FY2025 obligations; DFARS 217.71 (Master Agreements); GAO MAC-MO "
    "references; CNRMC MSRA instruction (2025); USCG Std Spec 8634; data as of April 2026</a:t>",
)
_TABLE = _TABLE.replace("Typical POP / ceiling", "Typical POP/ceiling")
_TABLE = _TABLE.replace("USCG / SFLC", "USCG/SFLC")
_TABLE = _TABLE.replace("LTA / BPA", "LTA/BPA")


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _TABLE + _ANNOT
    )
