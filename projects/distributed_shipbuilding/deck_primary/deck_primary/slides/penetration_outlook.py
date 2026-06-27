"""penetration_outlook — deck_primary slide 4 (Penetration Rate Outlook · PLACEHOLDER).

EXHIBIT — a placeholder slide: standard chrome plus a full-body gray placeholder box
describing the intended exhibit (a per-class penetration line chart with forecast /
ceiling overlays and a commentary column). The realized line-chart build was a draft
that was never green-lit, so only the placeholder ships — matching the slide 6
contracts-outlook placeholder treatment.

CODE MAP:
  • chrome + placeholder box . _SHAPES — breadcrumb / title / Preliminary chip plus the
                               gray "intended exhibit" box, transcribed verbatim from
                               _chart_xml/slide04.xml

Hand-authored PLACEHOLDER from the v2.0 working deck — the intended exhibit is described
in the gray box, not yet realized. Annotated to the study convention — docstring /
comments only; NO coordinate, value, colour, or paint-order changed, so the render is
byte-identical to the pre-annotation module.

Structure: one verbatim-XML layer (no chart, no table).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide04.xml").read_text(encoding="utf-8")


def _body() -> str:
    return _SHAPES


def render() -> str:
    return slide(_body())
