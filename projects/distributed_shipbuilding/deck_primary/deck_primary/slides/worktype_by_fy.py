"""worktype_by_fy - v2.0 slide 5: outsourced BC work-type mix by FY, full-width
stacked bars grouped DDG-51 / Virginia-class / Columbia-class with a shared
legend.

The chart is a REAL native <c:chart> part (chart5.xml), bundled verbatim and
placed at the source frame coordinates, with its ORIGINAL binary .xlsb workbook
reattached (editable_bundled_chart) so "Edit Data" works. Everything else
(chrome, legend, axis/label overlays) is transcribed verbatim.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide05.xml").read_text(encoding="utf-8")
_CHART = (_XML / "slide05_chart5.xml").read_text(encoding="utf-8")
_XLSB = (_XML / "slide05_chart5.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART, _XLSB)]


def _body() -> str:
    chart = graphic_frame(sp_id=843, name="Chart 542", x=349250, y=2216150,
                          cx=11296650, cy=3341688, rId="rId2")
    return chart + _SHAPES


def render() -> str:
    return slide(_body())
