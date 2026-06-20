"""topdown_funnel - top-down budget -> non-public-NSY funding funnel (v3.3 slide 9).

Unlike the think-cell stacked-bar slides, slide 9's funnel is a NATIVE pptx chart
(`<c:barChart>` stacked columns in chart1.xml) plus two connector "neck" lines and
three stage labels. So it is reproduced as a real native chart part: chart1.xml is
bundled VERBATIM via CHARTS (its <c:externalData> link to the embedded workbook
stripped so it renders self-contained from its cached values), placed by
graphic_frame(). The funnel-neck connectors, the three stage labels, the
commentary rail, the caption, and the footer are transcribed verbatim from the
source (frozen via _qa/extract_chart.py -> _chart_xml/slide09.xml). Only the
breadcrumb / Preliminary / title chrome is rebuilt from deck_core builders.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import slide, breadcrumb, title_placeholder, prelim_chip
from deck_core.charts import graphic_frame

LAYOUT = "slideLayout4"

_SECTION = "TAM Sizing"
_TOPIC = "Top-Down Funnel"
_TAKEAWAY = ("Removing the $7.49B Public NSY labor floor from the $17.0B budget leaves $9.5B of "
             "non-public-NSY MRO, near the $9.0B bottom-up TAM.")

_XML = Path(__file__).parent / "_chart_xml"
# Native stacked-column funnel chart, bundled verbatim (externalData stripped).
_CHART1 = (_XML / "slide09_chart1.xml").read_text(encoding="utf-8")
# Funnel-neck connectors + stage labels + commentary rail + caption + footer.
_ANNOT = (_XML / "slide09.xml").read_text(encoding="utf-8")
# Copy-style fix applied at load (durable across a _chart_xml re-extract): reformat the
# transcribed source line to the house convention and drop the "source-pinned" process note.
_ANNOT = _ANNOT.replace(
    "Source: PB26 OMN OP-5 Exhibit 1B4B Ship Maintenance (p.157, MSC p.129); PB26 OPN BA-1 "
    "P-40 LI 1000 (p.521); PB26 SCN P-40 LI 2086 CVN RCOH (p.175); PB26 USCG Justification "
    "ISVS PC and I (p.6). Public NSY ($7.49B) reflects federal civilian workforce at the four "
    "public yards, FPDS-invisible by construction. Each anchor source-pinned to a specific "
    "budget-book PDF page. Data as of April 2026.",
    "Sources: (1) PB26 OMN OP-5 Exhibit 1B4B Ship Maintenance (p.157, MSC p.129); (2) PB26 OPN "
    "BA-1 P-40 LI 1000 (p.521); (3) PB26 SCN P-40 LI 2086 CVN RCOH (p.175); (4) PB26 USCG "
    "Justification ISVS PC and I (p.6); data as of April 2026",
)

CHARTS = [{"chart_xml": _CHART1}]


def _body() -> str:
    frame = graphic_frame(
        sp_id=100, name="Chart 49", x=354013, y=1646238, cx=6018212, cy=3881437,
        rId="rId2",
    )
    return frame + _ANNOT


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
    )
