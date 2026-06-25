"""outsourced_bc_walk - v3 slide 1: the walk from each program's total ship
spend down to outsourced Basic Construction, DDG-51 and Virginia/Columbia side
by side, with a step/rationale ledger on the right.

Ported 1:1 from the v3 working deck (20260605_Defense Demand Drivers New
Construction_v3.pptx) - the v2-built deck re-edited by hand in PowerPoint and
re-exported, so every former module-level patch (the "$" on ~$1.1B, the
separator/callout/caption moves, the two-line "Less: Prime / AP/LLTM" label)
is baked into the source XML and the module is a pure verbatim read.

The two walk charts are REAL native <c:chart> barChart parts, bundled verbatim
via CHARTS and placed by graphic_frame at the source frame coordinates. In v3
chart1 is the SUBMARINE walk ('Chart 70') and chart2 the DDG walk ('Chart 77')
- swapped vs the v2.0 source; the rIds below follow CHARTS order, verified
against slide1.xml.rels. Each ships with its ORIGINAL binary .xlsb workbook
reattached (editable_bundled_chart) so PowerPoint's "Edit Data" works; the
chart XML is otherwise untouched (renders from its cached <c:numCache>
values). Everything else - chrome included - is transcribed verbatim
(`_chart_xml/slide01.xml`); the walk header strip (table 14) and the
step/rationale ledger (table 50) are verbatim tables
(`_chart_xml/slide01_tables.xml`).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide01.xml").read_text(encoding="utf-8")           # chrome + walk overlays
_TABLES = (_XML / "slide01_tables.xml").read_text(encoding="utf-8")    # header strip + ledger
_CHART_SUB = (_XML / "slide01_chart1.xml").read_text(encoding="utf-8")
_CHART_DDG = (_XML / "slide01_chart2.xml").read_text(encoding="utf-8")
_XLSB_SUB = (_XML / "slide01_chart1.xlsb").read_bytes()
_XLSB_DDG = (_XML / "slide01_chart2.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART_SUB, _XLSB_SUB),
          editable_bundled_chart(_CHART_DDG, _XLSB_DDG)]


def _body() -> str:
    sub = graphic_frame(sp_id=371, name="Chart 70", x=4214813, y=1809750,
                        cx=2746375, cy=4330700, rId="rId2")
    ddg = graphic_frame(sp_id=378, name="Chart 77", x=1422400, y=1811338,
                        cx=2746375, cy=4330700, rId="rId3")
    return _TABLES + sub + ddg + _SHAPES


def render() -> str:
    return slide(_body())
