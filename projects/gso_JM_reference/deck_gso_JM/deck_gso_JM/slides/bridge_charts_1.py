"""bridge_charts_1 - GS&O style-guide slide 1: the Bridge Charts archetype (1/2).

Newbuild price-reduction levers: a stacked-bar bridge (US Today -> repricing ->
ITC -> US post-ITC, $M '25E for a 3,600 TEU containership) on the left, paired
with the cost-category lever table (Cost Category / Reduction vs. US today /
Rationale / Drivers[BuildCo|Policy]) on the right, with on-bar callouts and an
8pt Note/Source line. This is the deck's worked example of a content-dense page
where objects intentionally break the title L/R alignment.

Faithful 1:1 port (docs/faithful_deck_port_methodology.md). The bridge is a real
native <c:chart> (chart1 -> Worksheet.xlsb), bundled verbatim via CHARTS and
reattached editable, placed by graphic_frame at the source frame coords.
Everything else - chrome, the on-bar value/category callouts, the connectors -
is transcribed verbatim (`_chart_xml/slide01.xml`); the lever table is the
verbatim <a:tbl> (`_chart_xml/slide01_tables.xml`); the US-flag wordmark is the
verbatim <p:pic> with its r:embed remapped (`_chart_xml/slide01_pics.xml`). The
14 purple `JM:` reviewer callouts are dropped via --keepout (JM_style_notes.md).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide01.xml").read_text(encoding="utf-8")          # chrome + on-bar callouts + connectors
_TABLE = (_XML / "slide01_tables.xml").read_text(encoding="utf-8")    # cost-category lever table
_PICS = (_XML / "slide01_pics.xml").read_text(encoding="utf-8")       # US-flag wordmark (rId3)
_CHART = (_XML / "slide01_chart1.xml").read_text(encoding="utf-8")
_XLSB = (_XML / "slide01_chart1.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART, _XLSB)]
IMAGES = [{"rId": "rId3", "file": "image6.png"}]


def _body() -> str:
    chart = graphic_frame(sp_id=308, name="Chart 7", x=1595438, y=1362075,
                          cx=3138487, cy=4216400, rId="rId2")
    # chart under the transcribed overlays so the on-bar labels paint on top
    return _TABLE + chart + _PICS + _SHAPES


def render() -> str:
    return slide(_body())
