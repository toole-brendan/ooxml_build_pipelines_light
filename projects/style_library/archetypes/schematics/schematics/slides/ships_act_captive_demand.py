"""ships_act_captive_demand - Commercial Strategy deck, source slide 60.

Auto-converted from the source .pptx by _tools/convert_slide.py.
The native <c:chart> exhibit is a data-over-template styled_chart: the
source chart part is the exact STYLE template and its values live in the
_CHART*_DATA literal (look byte-identical, "Edit Data" still works).
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=12, connector=5, chart=1, table=1, picture=0, chrome_builders=3, clusters=3 (covering 16 shapes), raw_verbatim=1, dropped=1, frozen_fields=14.

Converter notes:
  - Note/Source line off house position - kept verbatim
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, table, trow, tcell, tcell_rich, tpara, trun, tbreak, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, BREADCRUMB, GRAY_2, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide60_chart43.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide60_chart43.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [124, 46]},
        {"values": [46, 41]},
        {"values": [18, 15]},
        {"values": [9, 1]},
        {"values": [1, 1]},
        {"values": [1, None]},
        {"values": [2, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates) ──
_VAL_W, _VAL_H = IN(0.115), IN(0.167)
_SW_W, _SW_H = IN(0.196), IN(0.146)
_LBL_X, _LBL_H = IN(4.139), IN(0.167)
_H1 = IN(0.167)   # shared x4

# ── repeated-shape data tables (each drives a loop in _body) ──
_VALUE_LABELS = [    # (x, y, fill) x3
    (2.309, 2.21, "4C6C9C"),
    (4.583, 3.997, BLACK),
    (3.951, 4.016, "4C6C9C"),
]

_LEGEND_SWATCHES = [    # (x, y, fill) x6
    (3.887, 2.149, "969696"),
    (3.887, 2.372, BLACK),
    (3.887, 2.594, "4C6C9C"),
    (3.887, 2.816, "1D4D68"),
    (3.887, 3.038, "C0C0C0"),
    (3.887, 3.26, "007770"),
]

_LABELS = [    # (y, cx, label) x7
    (1.922, 0.345, "Other"),
    (2.144, 0.401, "Ro-Ro"),
    (2.366, 0.269, "Bulk"),
    (2.589, 0.944, "Product Tanker"),
    (2.811, 0.845, "Crude Tanker"),
    (3.033, 0.285, "LNG"),
    (3.255, 0.599, "Container"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(title_placeholder("SHIPS Act Captive Demand", "MSTF can support ~100 more vessels than legally mandated demand for SHIPS Act."))
    out.append(text_box(n(), "Rectangle 4", IN(0.495), IN(6.675), IN(12.367), IN(0.322), [paragraph([run("Note: Captive demand considers current cargo volumes, growth rates, and annual vessel capacity (driven by number of trips / year, cargo capacity, and utilization)", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: S&P Panjiva; Clarksons; ", size=PT(8), color=BLACK, font=FONT), run("SHIPS Act text", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA AEO LNG Export Table", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA AEO Crude Export Table", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA Crude Tanker Descriptions", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("GAO Report on Government Preference Cargo", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 10", IN(5.703), IN(1.483), IN(7.089), IN(4.007), col_widths=[IN(2.808), IN(1.799), IN(1.241), IN(1.241)], rows=[
        trow([tcell("Legally mandated demand from SHIPS Act Provisions", size=PT(10), bold=True, color=BLACK, align="ctr", fill=GRAY_2, grid_span=4, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": "none"})], h=IN(0)),
        trow([tcell_rich([tpara([trun("Provision ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("(Bill Section)", size=PT(10), italic=True, color=BLACK, font=FONT), tbreak(), trun("Vessel Type Impacted", size=PT(10), color=BLACK, font=FONT)])], anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell_rich([tpara([trun("% of Cargo", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("(Start – ramp end)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("US-Built", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("US-Flagged", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0)),
        trow([tcell_rich([tpara([trun("Crude Exports from the US", size=PT(10), bold=True, color=WHITE, font=FONT)]), tpara([trun("SEC. 420", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Crude Tankers", size=PT(10), color=WHITE, font=FONT)])], fill="1D4D68", borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell_rich([tpara([trun("3% to 10%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2027-2040", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.661)),
        trow([tcell_rich([tpara([trun("LNG Exports from the US", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("SEC. 420", size=PT(10), italic=True, color=BLACK, font=FONT), tbreak(), trun("LNG Ships", size=PT(10), color=BLACK, font=FONT)])], fill="C0C0C0", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell_rich([tpara([trun("2% to 15%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2027-2047", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.661)),
        trow([tcell_rich([tpara([trun("China Imports to the US", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 415", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships", size=PT(10), color=WHITE, font=FONT)])], fill="007770", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell_rich([tpara([trun("1% to 10%", size=PT(10), bold=True, color=BLACK, font=FONT), tbreak(), trun("2031-2040", size=PT(10), italic=True, color=BLACK, font=FONT), trun(" ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.661)),
        trow([tcell_rich([tpara([trun("US Government Cargo Preference", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 411", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships & Bulk", size=PT(10), color=WHITE, font=FONT)])], fill="007770", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell_rich([tpara([trun("50% to 100%", size=PT(10), bold=True, color=BLACK, font=FONT), trun(" ", size=PT(10), color=BLACK, font=FONT), tbreak(), trun("180 days after bill passage", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=WHITE, row_span=2, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("No", size=PT(12), bold=True, color="C00000", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.661)),
        trow([tcell_rich([tpara([trun("USDA Program Exports", size=PT(10), bold=True, color=WHITE, font=FONT), tbreak(), trun("SEC. 418", size=PT(10), italic=True, color=WHITE, font=FONT), tbreak(), trun("Containerships", size=PT(10), color=WHITE, font=FONT)])], fill="007770", borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("No", size=PT(12), bold=True, color="C00000", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Yes", size=PT(12), bold=True, color="007770", align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.661)),
    ]))
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.429), y=IN(1.62), cx=IN(5.123), cy=IN(4.674), rId="rId2"))
    out.append(connector(n(), "Straight Connector 74", IN(2.599), IN(2.274), IN(0.101), IN(0.069), color=BREADCRUMB, width=6350, dashed=True, arrow=True, flip_h=True, flip_v=True))
    out.append(connector(n(), "Straight Connector 75", IN(2.599), IN(2.177), IN(0.101), IN(0.069), color=BREADCRUMB, width=6350, dashed=True, arrow=True, flip_h=True))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.542), IN(1.505), IN(4.384), _H1, [paragraph([run("SCF Supported by MSTF vs. Legally Mandated Demand (# vessels)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for _x, _y, _fill in _VALUE_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), _VAL_W, _VAL_H, [paragraph([run("1", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.215), IN(6.094), IN(1.667), IN(0.333), [paragraph([run("Strategic Commercial Fleet (supported by MSTF)", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(3.493), IN(6.094), IN(1.663), _H1, [paragraph([run("Legally Mandated Demand", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.915), IN(2.033), IN(0.267), _H1, [paragraph([run("201", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(4.191), IN(3.83), IN(0.267), _H1, [paragraph([run("104", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    # RAW verbatim (pattFill):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Rectangle 109\" /><p:cNvSpPr /><p:nvPr /></p:nvSpPr><p:spPr bwMode=\"auto\"><a:xfrm><a:off x=\"3554413\" y=\"1762125\" /><a:ext cx=\"179388\" cy=\"133350\" /></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst /></a:prstGeom><a:pattFill prst=\"ltDnDiag\"><a:fgClr><a:schemeClr val=\"tx1\" /></a:fgClr><a:bgClr><a:schemeClr val=\"bg1\" /></a:bgClr></a:pattFill><a:ln w=\"19050\" cap=\"flat\" cmpd=\"sng\" algn=\"ctr\"><a:noFill /><a:prstDash val=\"solid\" /><a:miter lim=\"800000\" /><a:headEnd type=\"none\" w=\"med\" len=\"med\" /><a:tailEnd type=\"none\" w=\"med\" len=\"med\" /></a:ln><a:effectLst /></p:spPr><p:style><a:lnRef idx=\"2\"><a:schemeClr val=\"accent1\"><a:shade val=\"15000\" /></a:schemeClr></a:lnRef><a:fillRef idx=\"1\"><a:schemeClr val=\"accent1\" /></a:fillRef><a:effectRef idx=\"0\"><a:schemeClr val=\"accent1\" /></a:effectRef><a:fontRef idx=\"minor\"><a:schemeClr val=\"lt1\" /></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol=\"0\" anchor=\"ctr\" /><a:lstStyle /><a:p><a:pPr algn=\"ctr\" /><a:endParaRPr lang=\"en-US\" /></a:p></p:txBody></p:sp>")
    for _x, _y, _fill in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _LABELS:
        out.append(text_box(n(), "Label", _LBL_X, IN(_y), IN(_cx), _LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Rectangle 329", IN(5.703), IN(5.56), IN(7.089), IN(0.867), [paragraph([run("Reaching ~200 vessels assumes owners accept Opex and D&A differential of operating US-built and flagged vessels vs. foreign-built and flagged", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))
    out.append(prelim_chip())
    out.append(text_box(n(), "Rectangle 336", IN(8.069), IN(0.173), IN(2.977), IN(0.218), [paragraph([run("(2) SHIPS Act Scenario", size=PT(12), bold=True, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=BLACK, anchor="ctr"))
    out.append(connector(n(), "Straight Connector 351", IN(4.958), IN(2.188), IN(0.745), IN(1.927), color="808080", width=6350, dashed=True, flip_v=True))
    out.append(connector(n(), "Straight Connector 355", IN(4.958), IN(2.854), IN(0.745), IN(1.536), color="808080", width=6350, dashed=True, flip_v=True))
    out.append(connector(n(), "Straight Connector 358", IN(4.958), IN(3.487), IN(0.745), IN(1.683), color="808080", width=6350, dashed=True, flip_v=True))
    out.append(text_box(n(), "Rectangle 53", IN(10.635), IN(1.191), IN(0.1), IN(0.234), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "TextBox 54", IN(10.691), IN(1.191), IN(2.101), IN(0.234), [paragraph([run("Port Alpha production modeled", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none"))
    out.append(text_box(n(), "Rectangle 55", IN(3.835), IN(2.569), IN(1.3), IN(0.426), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="b"))
    out.append(text_box(n(), "Rectangle 56", IN(3.835), IN(3.236), IN(1.3), IN(0.207), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="FB6B3C", line_width=19050, anchor="b"))
    return "".join(out)


def render() -> str:
    return slide(_body())
