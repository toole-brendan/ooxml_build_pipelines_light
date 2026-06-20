"""penetration_outlook - v2.0 slide 4: "Penetration Rate Outlook" placeholder.

Reverted to the v2.0 working-deck placeholder: standard chrome plus a
full-body gray placeholder box describing the intended exhibit (a per-class
penetration line chart with forecast/ceiling overlays and a commentary
column). The realized line-chart build was a draft that was never
green-lighted, so this slide carries only the placeholder, transcribed
verbatim from slide04.xml - matching the slide 6 contracts-outlook placeholder
treatment.
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
