"""private_addressable - top-down vs bottom-up convergence (v3.3 slide 11).

No chart or table: two dual-narrative round-rect tile stacks (Bottom-Up / FPDS and
Top-Down / Budget Anchor) with connectors, plus a convergence-result callout. Every
body shape is transcribed verbatim (`_chart_xml/slide11.xml`); only the chrome is
rebuilt from deck_core builders.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip

LAYOUT = "slideLayout4"

_SECTION = "TAM Sizing"
_TOPIC = "Non-Public-NSY"
_TITLE_TOPIC = "Non-Public-NSY Cross-Check"
_TAKEAWAY = ("Non-public-NSY MRO of $9.51B converges within ~6% of the $8.97B reconciled bottom-up "
             "MRO TAM.")

_ANNOT = (Path(__file__).parent / "_chart_xml" / "slide11.xml").read_text(encoding="utf-8")
# Copy-style fix applied at load (durable across a _chart_xml re-extract): strip build-process
# references (internal workbook/Reconciliation-sheet artifacts, the "Phase 2" marker) and
# reformat the transcribed source line to the house convention.
_ANNOT = _ANNOT.replace(
    "Source: workbook_build Non-Public-NSY Bridge sheet; Reconciliation sheet TAS-attributed "
    "appropriation rollup. Captive HII/GDEB complex OH retained inside both numbers (captive "
    "treatment is an addressability filter that belongs in SAM derivation, Phase 2, not the "
    "TAM layer). Data as of April 2026.",
    "Sources: (1) Non-Public-NSY Bridge; (2) TAS-attributed appropriation rollup; data as of "
    "April 2026",
)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _ANNOT
    )
