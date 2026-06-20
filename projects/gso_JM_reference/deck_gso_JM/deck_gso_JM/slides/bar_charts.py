"""bar_charts - GS&O style-guide slide 3: the Bar Charts archetype.

A stacked single-column native chart (SCF supported by legally-mandated demand,
# vessels) with a manual left legend and on-bar range labels, paired with the
"Legally Mandated Demand from SHIPS Act Provisions" table on the right and a
bg2-filled focal callout beneath it; standard eyebrow / title / Preliminary
chip chrome and an 8pt Note/Source line.

Faithful 1:1 port (docs/faithful_deck_port_methodology.md). The stacked column
is a real native <c:chart> (chart4 -> Worksheet3.xlsb), bundled verbatim via
CHARTS (caches intact, externalData stripped) and reattached editable, placed by
graphic_frame at the source frame coords. Everything else - chrome, the manual
legend swatches + labels, the on-bar range labels, the leader connectors, and
the focal callout - is transcribed verbatim (`_chart_xml/slide03.xml`); the
SHIPS Act table is the verbatim <a:tbl> (`_chart_xml/slide03_tables.xml`). The
three purple `JM:` reviewer callouts (src ids 3, 7, 9) are dropped via --keepout
(captured in JM_style_notes.md).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide03.xml").read_text(encoding="utf-8")          # chrome + legend + labels + callout
_TABLE = (_XML / "slide03_tables.xml").read_text(encoding="utf-8")    # SHIPS Act provisions table
_CHART = (_XML / "slide03_chart4.xml").read_text(encoding="utf-8")
_XLSB = (_XML / "slide03_chart4.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART, _XLSB)]


def _body() -> str:
    chart = graphic_frame(sp_id=329, name="Chart 28", x=392113, y=1550988,
                          cx=4684712, cy=4133850, rId="rId2")
    # chart under the transcribed overlays so the manual labels/legend paint on top
    return _TABLE + chart + _SHAPES


def render() -> str:
    return slide(_body())
