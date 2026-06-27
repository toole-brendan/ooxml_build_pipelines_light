"""contracts_outlook_placeholder — deck_primary slide 6 (Contracts Outlook · PLACEHOLDER).

EXHIBIT — a working-deck mockup: standard chrome plus a templated contracts table
(Platform · Contract · Amount · Details · Recompete Date · Current Player · Budget
Alignment) with its budget-alignment legend chips, all sitting UNDER a full-body gray
placeholder box describing the intended exhibit.

CODE MAP (body paints back-to-front so the gray box overlays the table):
  • table .......... _TABLES — the templated contracts <a:tbl>, verbatim from
                     _chart_xml/slide06_tables.xml
  • chrome + chips + placeholder box . _SHAPES — breadcrumb / title / budget-alignment
                     legend chips and the gray "intended exhibit" box (last among them),
                     transcribed verbatim from _chart_xml/slide06.xml

Hand-authored PLACEHOLDER from the v2.0 working deck — the intended exhibit is described
in the gray box, not yet realized. Source z-order is preserved by emitting the table
first and the shapes after it. Annotated to the study convention — docstring / comments
only; NO coordinate, value, colour, or paint-order changed, so the render is
byte-identical to the pre-annotation module.

Structure: 1 verbatim table + the verbatim chrome/chips/placeholder layer (no chart).
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
