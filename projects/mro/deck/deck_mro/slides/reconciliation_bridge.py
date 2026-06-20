"""reconciliation_bridge - top-down vs bottom-up reconciliation (v3.3 slide 10).

No chart on this slide: the bridge is the wide `bridge_components` table plus seven
numbered oval row-markers in the left margin. The table is transcribed verbatim
(`_chart_xml/slide10_table.xml`), and the ovals + footer are transcribed verbatim
(`_chart_xml/slide10.xml`); only the chrome is rebuilt from deck_core builders.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip

LAYOUT = "slideLayout4"

_SECTION = "TAM Sizing"
_TOPIC = "Reconciliation"
_TITLE_TOPIC = "Reconciliation Bridge"
_TAKEAWAY = ("Public Naval Shipyard labor of $7.49B is the structural FPDS-invisible gap between "
             "the $17.0B top-down and $9.0B bottom-up MRO.")

_XML = Path(__file__).parent / "_chart_xml"
_TABLE = (_XML / "slide10_table.xml").read_text(encoding="utf-8")   # verbatim bridge table
# Copy-style fix at load (durable across a _chart_xml re-extract): strip the internal
# "plan section" reference and the "NEW"/"source-pinned" status tells from two bridge cells.
_TABLE = _TABLE.replace(
    "Primary recon test (plan section 6.5). FY2025 PB26 forecast vs FPDS actual obligations",
    "Primary reconciliation test: FY2025 PB26 forecast vs FPDS actual obligations",
)
_TABLE = _TABLE.replace(
    "NEW source-pinned. Modernization side of avails, separate appropriation from OMN",
    "Modernization side of avails, separate appropriation from OMN",
)
_ANNOT = (_XML / "slide10.xml").read_text(encoding="utf-8")         # numbered ovals + footer
# Copy-style fix applied at load (durable across a _chart_xml re-extract): strip build-process
# references (internal workbook/plan artifacts, "source-pinned") and reformat the source line.
_ANNOT = _ANNOT.replace(
    "Source: workbook_build TAM Bridge sheet (corrected 2026-04-27); plan section 2.3 "
    "dual-narrative reconciliation. Top-down components fully source-pinned to budget-book "
    "line items after OPN LI 1000 substitution. WPN combat-systems sustainment intentionally "
    "excluded from top-down (no Table-IV-equivalent exists in WPN P-40 exhibits); FPDS captures "
    "the WPN flow on combat-system PSCs (J012, J014, K010, K012) within Narrative A. Data as of "
    "April 2026.",
    "Sources: (1) PB26 budget-book line items; (2) FPDS FY2025 contract obligations; data as of "
    "April 2026",
)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _TABLE + _ANNOT
    )
