"""bridge_charts_2 - GS&O style-guide slide 2: the Bridge Charts archetype (2/2).

Annual opex for MR product tankers ($M '25E): a stacked-column build to the
US-flagged proxy with the foreign-flagged gap (left, chart2) beside a
company-comps column set (OSG / Hafnia / Scorpio / Torm, right, chart3), with
circled data rows (avg fleet age / capacity / US-flagged proportion), dashed
content separators, and the four operator logos under the comps. The deck's
worked example of circled data rows, segment-value labels, and logo parity.

Faithful 1:1 port (docs/faithful_deck_port_methodology.md). Both column sets are
real native <c:chart> parts (chart2 -> Worksheet1.xlsb, chart3 -> Worksheet2.xlsb),
bundled verbatim via CHARTS and reattached editable, placed by graphic_frame at
the source frame coords (chart2 -> rId2, chart3 -> rId3). The circled data rows,
dashed separators, axis/segment labels, and all chrome are transcribed verbatim
(`_chart_xml/slide02.xml`); the four operator logos are verbatim <p:pic> with
remapped r:embeds (`_chart_xml/slide02_pics.xml`, rId4-rId7). The 10 purple `JM:`
reviewer callouts are dropped via --keepout (JM_style_notes.md).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide02.xml").read_text(encoding="utf-8")          # chrome + circled rows + dashed seps + labels
_PICS = (_XML / "slide02_pics.xml").read_text(encoding="utf-8")       # OSG / Hafnia / Scorpio / Torm logos (rId4-7)
_CHART_GAP = (_XML / "slide02_chart2.xml").read_text(encoding="utf-8")
_CHART_COMPS = (_XML / "slide02_chart3.xml").read_text(encoding="utf-8")
_XLSB_GAP = (_XML / "slide02_chart2.xlsb").read_bytes()
_XLSB_COMPS = (_XML / "slide02_chart3.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART_GAP, _XLSB_GAP),
          editable_bundled_chart(_CHART_COMPS, _XLSB_COMPS)]
IMAGES = [{"rId": "rId4", "file": "image7.jpeg"},
          {"rId": "rId5", "file": "image8.jpeg"},
          {"rId": "rId6", "file": "image9.jpeg"},
          {"rId": "rId7", "file": "image10.png"}]


def _body() -> str:
    gap = graphic_frame(sp_id=308, name="Chart 7", x=369888, y=1687513,
                        cx=6729412, cy=2792412, rId="rId2")
    comps = graphic_frame(sp_id=317, name="Chart 16", x=7251700, y=1687513,
                          cx=4565650, cy=2792412, rId="rId3")
    return gap + comps + _PICS + _SHAPES


def render() -> str:
    return slide(_body())
