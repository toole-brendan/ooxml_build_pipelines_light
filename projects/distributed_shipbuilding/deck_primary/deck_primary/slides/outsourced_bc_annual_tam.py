"""outsourced_bc_annual_tam - v3 slide 3: annual outsourced-BC TAM FY22-FY31,
pre/post-OBBBA, with per-class penetration strips (DDG-51 / Virginia /
Columbia) and a band-commentary table along the bottom.

Ported 1:1 from the v3 working deck (20260605_Defense Demand Drivers New
Construction_v3.pptx) - the v2-built deck re-edited by hand in PowerPoint
(with think-cell) and re-exported. The whole former patch layer (the hilo/ramp
chart derivation, strip-row remaps, legend re-layout, pill stretches, n/a
ovals, footnotes, manager flags) is superseded: whatever of it the user kept
is baked into the v3 XML, and the chart is v3's own chart4.xml - so the module
is a pure verbatim read again. The retired hilo/ramp generator is archived at
_qa/archive_pre_v3/make_chart4_hilo.py.

The chart is a REAL native <c:chart> part (chart4.xml), bundled verbatim and
placed at the source frame coordinates ('Chart 36'), with its ORIGINAL binary
.xlsb workbook reattached (editable_bundled_chart) so "Edit Data" works. The
band commentary (table 52) is a verbatim table; the dense annotation layer
(penetration strips, ovals, pills, forecast box, legend, chrome) is
transcribed verbatim (`_chart_xml/slide03.xml`).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide03.xml").read_text(encoding="utf-8")           # chrome + annotation layer
_TABLES = (_XML / "slide03_tables.xml").read_text(encoding="utf-8")    # band commentary
_CHART = (_XML / "slide03_chart4.xml").read_text(encoding="utf-8")
_XLSB = (_XML / "slide03_chart4.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART, _XLSB)]


def _body() -> str:
    chart = graphic_frame(sp_id=337, name="Chart 36", x=646113, y=1574800,
                          cx=11126787, cy=2470150, rId="rId2")
    return _TABLES + chart + _SHAPES


def render() -> str:
    return slide(_body())
