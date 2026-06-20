"""contracts_outlook_placeholder - v2.0 slide 6: "Contracts Outlook"
placeholder slide.

A working-deck mockup: standard chrome plus a templated contracts table
(Platform / Contract / Amount / Details / Recompete Date / Current Player /
Budget Alignment) with its budget-alignment legend chips, all sitting UNDER a
full-body gray placeholder box describing the intended exhibit. The table is a
verbatim <a:tbl>; everything else is transcribed verbatim. Source z-order is
preserved by emitting the table first and the shapes (placeholder box last
among them) after it.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide06.xml").read_text(encoding="utf-8")
_TABLES = (_XML / "slide06_tables.xml").read_text(encoding="utf-8")


def _body() -> str:
    return _TABLES + _SHAPES


def render() -> str:
    return slide(_body())
