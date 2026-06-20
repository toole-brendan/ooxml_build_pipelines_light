"""tables - GS&O style-guide slide 4: the Tables archetype.

Opex categories driving the US-vs-foreign cost differential (Crew / Insurance /
Repair & Maintenance / Dry-Dock), with an Impact column, a Rationale (Source)
column carrying italicized verbatim quotes, and an Additional Detail column
holding wordmark/source images with drop shadows. A bg2 MSC callout sits at the
bottom. The deck's worked example of bold headers/row-titles, bullet levels,
italicized quotes, and same-size shadowed images.

Faithful 1:1 port (docs/faithful_deck_port_methodology.md). No chart on this
slide. The main table is the verbatim <a:tbl> (`_chart_xml/slide04_tables.xml`);
the four source/wordmark images are verbatim <p:pic> with remapped r:embeds and
shadows preserved (`_chart_xml/slide04_pics.xml`, rId2-rId5); chrome and the MSC
callout are transcribed verbatim (`_chart_xml/slide04.xml`). The 10 purple `JM:`
reviewer callouts are dropped via --keepout (JM_style_notes.md).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide04.xml").read_text(encoding="utf-8")          # chrome + MSC callout
_TABLE = (_XML / "slide04_tables.xml").read_text(encoding="utf-8")    # opex-categories table
_PICS = (_XML / "slide04_pics.xml").read_text(encoding="utf-8")       # 4 wordmark/source images (rId2-5)

IMAGES = [{"rId": "rId2", "file": "image11.png"},
          {"rId": "rId3", "file": "image12.png"},
          {"rId": "rId4", "file": "image13.png"},
          {"rId": "rId5", "file": "image14.png"}]


def _body() -> str:
    return _TABLE + _PICS + _SHAPES


def render() -> str:
    return slide(_body())
