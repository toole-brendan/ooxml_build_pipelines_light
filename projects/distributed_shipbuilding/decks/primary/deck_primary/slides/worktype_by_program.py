"""worktype_by_program - v3 slide 2: outsourced BC spend by work type, the
~$18.1B submarine pool vs the ~$6.4B DDG-51 pool, with the methodology ledger
on the right.

Ported 1:1 from the v3 working deck (20260605_Defense Demand Drivers New
Construction_v3.pptx) - the v2-built deck re-edited by hand in PowerPoint and
re-exported, so the former module-level patches (the replaced PIID/action-year
MethodFindings note, the FY22-FY27 title window, the ledger's FY26-27 share
disclosure) are baked into the source XML and the module is a pure verbatim
read.

The stacked-column chart is a REAL native <c:chart> part (chart3.xml), bundled
verbatim and placed at the source frame coordinates ('Chart 51'), with its
ORIGINAL binary .xlsb workbook reattached (editable_bundled_chart) so "Edit
Data" works. The methodology ledger (table 6) and the two caption strips
(tables 53, 54) are verbatim tables; every other shape (chrome, legend
swatches, axis/label overlays) is transcribed verbatim.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide
from deck_core.charts import graphic_frame, editable_bundled_chart

LAYOUT = "slideLayout4"

_XML = Path(__file__).parent / "_chart_xml"
_SHAPES = (_XML / "slide02.xml").read_text(encoding="utf-8")           # chrome + legend + overlays
_TABLES = (_XML / "slide02_tables.xml").read_text(encoding="utf-8")    # ledger + caption strips
_CHART = (_XML / "slide02_chart3.xml").read_text(encoding="utf-8")
_XLSB = (_XML / "slide02_chart3.xlsb").read_bytes()

CHARTS = [editable_bundled_chart(_CHART, _XLSB)]


def _body() -> str:
    chart = graphic_frame(sp_id=352, name="Chart 51", x=349250, y=1665288,
                          cx=4341813, cy=4376737, rId="rId2")
    return _TABLES + chart + _SHAPES


def render() -> str:
    return slide(_body())
