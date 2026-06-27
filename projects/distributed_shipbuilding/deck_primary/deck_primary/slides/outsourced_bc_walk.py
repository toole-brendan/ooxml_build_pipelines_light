"""outsourced_bc_walk — deck_primary slide 1 (Total Ship Spend → outsourced BC walk).

EXHIBIT — the walk from each program's total ship spend down to outsourced Basic
Construction, DDG-51 and Virginia/Columbia side by side as two vertical waterfall
charts, with a step/rationale ledger down the right. A header strip captions the
two walks; the ledger explains each deduction (e.g. the two-line "Less: Prime /
AP/LLTM" step).

CODE MAP (body paints back-to-front: tables → charts → overlay shapes):
  • tables ......... _TABLES — header strip (table 14) + step/rationale ledger
                     (table 50), verbatim <a:tbl> from _chart_xml/slide01_tables.xml
  • charts ......... CHARTS — two native <c:chart> barChart walks bundled verbatim via
                     editable_bundled_chart; placed by graphic_frame() (submarine
                     'Chart 70' → rId2, DDG 'Chart 77' → rId3; note v3 swaps
                     chart1=SUB / chart2=DDG vs the v2.0 source)
  • chrome+overlay . _SHAPES — breadcrumb / title / callouts / captions, transcribed
                     verbatim from _chart_xml/slide01.xml

Hand-authored 1:1 port of the v3 working deck (20260605 Defense Demand Drivers New
Construction), source slide 1: the charts are native parts bundled untouched (each
with its original .xlsb so "Edit Data" works, rendering from its cached
<c:numCache>); chrome, overlays and both tables are verbatim-XML transcriptions.
Annotated to the study convention — docstring / comments only; NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the pre-annotation
module.

Structure: 2 native charts (editable_bundled_chart) + 2 verbatim tables + the
verbatim chrome/overlay layer.
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
