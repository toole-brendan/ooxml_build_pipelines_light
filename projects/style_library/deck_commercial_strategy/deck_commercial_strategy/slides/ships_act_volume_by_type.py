"""ships_act_volume_by_type - Commercial Strategy deck, source slide 59.

Auto-converted from the source .pptx by _tools/convert_slide.py.
The native <c:chart> exhibit is a data-over-template styled_chart: the
source chart part is the exact STYLE template and its values live in the
_CHART*_DATA literal (look byte-identical, "Edit Data" still works).
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; the OLE frame + EMF preview dropped.

Converter stats: text_box=8, connector=1, chart=1, table=0, chrome_builders=3, clusters=5 (covering 64 shapes), raw_verbatim=1, dropped=1, frozen_fields=55.

Converter notes:
  - Note/Source line off house position - kept verbatim
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide59_chart42.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide59_chart42.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [1, 2, 2, 5, 8, 16, 21, 15, 12, 7, 5, 3, 5, 3, 5, 3, 2, 4, 3, 4, 2, 2, 2, 2, 5]},
        {"values": [None, None, None, 2, 4, 8, 11, 6, 5, 3, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, None, 1, 2]},
        {"values": [None, None, None, 5, 2, 4, 5, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, None, None, None, 1, 2]},
        {"values": [None, None, None, None, 1, 2, 3, 2, 1, None, 1, None, 1, 1, 1, None, 1, 2, None, None, None, None, None, None, 2]},
        {"values": [None, None, None, None, 5, None, 2, 2, 1, None, None, None, None, None, 1, None, None, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, 1, 5, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
        {"values": [None, None, None, None, None, None, 7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
        {"values": [3, 8, 1, 0, 1, 5, 4, 5, 11, 4, 7, 7, 10, 5, 9, 0, 7, 0, 5, 0, 6, 0, 7, 0, 0]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.094), IN(0.167), IN(0.306)
_VAL_H = IN(0.167)
_SW_X, _SW_W, _SW_H = IN(9.806), IN(0.196), IN(0.146)
_LBL_X, _LBL_H = IN(10.057), IN(0.167)

# ── repeated-shape data tables (each drives a loop in _body) ──
_AXIS_YEARS = [    # (x, label) x25
    (1.064, "2026"),
    (1.54, "2027"),
    (2.016, "2028"),
    (2.49, "2029"),
    (2.965, "2030"),
    (3.441, "2031"),
    (3.917, "2032"),
    (4.392, "2033"),
    (4.866, "2034"),
    (5.342, "2035"),
    (5.818, "2036"),
    (6.293, "2037"),
    (6.769, "2038"),
    (7.243, "2039"),
    (7.719, "2040"),
    (8.194, "2041"),
    (8.67, "2042"),
    (9.146, "2043"),
    (9.62, "2044"),
    (10.095, "2045"),
    (10.571, "2046"),
    (11.047, "2047"),
    (11.523, "2048"),
    (11.997, "2049"),
    (12.472, "2050"),
]

_VALUE_LABELS = [    # (x, y, cx, label) x22
    (1.09, 5.783, 0.115, "1"),
    (2.477, 5.016, 0.191, "12"),
    (2.953, 4.458, 0.191, "20"),
    (3.429, 3.762, 0.191, "30"),
    (3.905, 2.368, 0.191, "50"),
    (4.38, 3.554, 0.191, "33"),
    (4.854, 4.319, 0.191, "22"),
    (5.33, 5.087, 0.191, "11"),
    (5.844, 5.295, 0.115, "8"),
    (6.319, 5.503, 0.115, "5"),
    (7.269, 5.434, 0.115, "6"),
    (7.707, 5.156, 0.191, "10"),
    (8.22, 5.503, 0.115, "5"),
    (8.696, 5.434, 0.115, "6"),
    (9.172, 5.295, 0.115, "8"),
    (6.795, 5.295, 0.115, "8"),
    (10.083, 5.156, 0.191, "10"),
    (10.597, 5.644, 0.115, "3"),
    (11.073, 5.644, 0.115, "3"),
    (12.023, 5.573, 0.115, "4"),
    (12.46, 5.087, 0.191, "11"),
    (9.646, 5.226, 0.115, "9"),
]

_LEGEND_SWATCHES = [    # (y, fill) x6
    (2.375, "808080"),
    (2.597, "4C6C9C"),
    (2.819, "969696"),
    (3.042, "C0C0C0"),
    (3.264, "364D6E"),
    (3.486, "007770"),
]

_LABELS = [    # (y, cx, label) x8
    (1.925, 2.682, "Incremental Vessels to Fill Captive Demand"),
    (2.148, 0.345, "Other"),
    (2.37, 0.269, "Bulk"),
    (2.592, 0.944, "Product Tanker"),
    (2.814, 0.401, "Ro-Ro"),
    (3.036, 0.285, "LNG"),
    (3.259, 0.845, "Crude Tanker"),
    (3.481, 0.599, "Container"),
]

_CALLOUTS = [    # (x, y, cx, cy, label, tail) x3
    (5.465, 4, 2.813, 0.588, "Decline driven by MSTF prioritizing payments to existing ships in fleet, reducing available balance for new adds ", {"adj1": "val -62515", "adj2": "val 22663"}),
    (9.029, 4.489, 3.417, 0.432, "Captive demand volatility driven by mandated import / export proportions that increase every 1-3 years", {"adj1": "val 11502", "adj2": "val 163585"}),
    (1.533, 3.679, 1.587, 0.588, "Ramp enabled by shipyard capacity coming online", {"adj1": "val 65129", "adj2": "val -21653"}),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(text_box(n(), "Rectangle 657", IN(2.344), IN(1.87), IN(3.788), IN(4.172), [paragraph([run("Demand enables serial production of containerships ", size=PT(10), italic=True, color=BLACK, font=FONT), run("(5-21 ships / year)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_1, line_color="none"))
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.505), y=IN(1.62), cx=IN(12.38), cy=IN(4.674), rId="rId2"))
    for _x, _t in _AXIS_YEARS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for _x, _y, _cx, _t in _VALUE_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), _VAL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.618), IN(1.505), IN(4.908), IN(0.167), [paragraph([run("Additions to US-Built, Oceangoing Commercial Fleet by Type (# deliveries)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    out.append(title_placeholder("SHIPS Act Volume by Type", "Only containerships provide sufficient volume to sustain extended serial production."))
    out.append(connector(n(), "Straight Connector 70", IN(9.826), IN(2.003), IN(0.155), IN(0), color="C30C3E", width=38100, dashed=True, arrow=True))
    # RAW verbatim (pattFill):
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Rectangle 402\" /><p:cNvSpPr /><p:nvPr /></p:nvSpPr><p:spPr bwMode=\"auto\"><a:xfrm><a:off x=\"8966200\" y=\"1968500\" /><a:ext cx=\"179388\" cy=\"133350\" /></a:xfrm><a:prstGeom prst=\"rect\"><a:avLst /></a:prstGeom><a:pattFill prst=\"ltDnDiag\"><a:fgClr><a:schemeClr val=\"tx1\" /></a:fgClr><a:bgClr><a:schemeClr val=\"bg1\" /></a:bgClr></a:pattFill><a:ln w=\"19050\" cap=\"flat\" cmpd=\"sng\" algn=\"ctr\"><a:noFill /><a:prstDash val=\"solid\" /><a:miter lim=\"800000\" /><a:headEnd type=\"none\" w=\"med\" len=\"med\" /><a:tailEnd type=\"none\" w=\"med\" len=\"med\" /></a:ln><a:effectLst /></p:spPr><p:style><a:lnRef idx=\"2\"><a:schemeClr val=\"accent1\"><a:shade val=\"15000\" /></a:schemeClr></a:lnRef><a:fillRef idx=\"1\"><a:schemeClr val=\"accent1\" /></a:fillRef><a:effectRef idx=\"0\"><a:schemeClr val=\"accent1\" /></a:effectRef><a:fontRef idx=\"minor\"><a:schemeClr val=\"lt1\" /></a:fontRef></p:style><p:txBody><a:bodyPr rtlCol=\"0\" anchor=\"ctr\" /><a:lstStyle /><a:p><a:pPr algn=\"ctr\" /><a:endParaRPr lang=\"en-US\" /></a:p></p:txBody></p:sp>")
    for _y, _fill in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", _SW_X, IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr")], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _LABELS:
        out.append(text_box(n(), "Label", _LBL_X, IN(_y), IN(_cx), _LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Rectangle 444", IN(0.495), IN(6.687), IN(12.367), IN(0.311), [paragraph([run("Note: ", size=PT(8), color=BLACK, font=FONT), run("Product and Crude Tankers assumed to be LR1/Aframax size; Containerships assumed to have 3-8K TEU capacity; “Other” category includes the following vessel types: Chemical & Oil, Bulk Chemical, General Cargo, Refrigerated Fish, Heavy Lift, and Cable-Laying / Repair Ships | ", size=PT(8), color=BLACK, font=FONT), run("Source: See SHIPS Act and SHIPS Act “Plus” Volume pages", size=PT(8), color=BLACK, font=FONT)])], fill=None, line_color="none"))
    out.append(text_box(n(), "Rectangle 660", IN(9.756), IN(3.233), IN(1.3), IN(0.434), [paragraph([], align="ctr")], fill=None, line_color="FB6B3C", line_width=19050, anchor="b"))
    out.append(text_box(n(), "Rectangle 661", IN(9.756), IN(2.549), IN(1.3), IN(0.227), [paragraph([], align="ctr")], fill=None, line_color="FB6B3C", line_width=19050, anchor="b"))
    for _x, _y, _cx, _cy, _t, _ga in _CALLOUTS:
        out.append(text_box(n(), "Callout", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color="121415", prst="wedgeRectCallout", geom_adj=_ga, anchor="ctr"))
    out.append(prelim_chip())
    out.append(text_box(n(), "Rectangle 96", IN(8.069), IN(0.173), IN(2.977), IN(0.218), [paragraph([run("(2) SHIPS Act Scenario", size=PT(12), bold=True, font=FONT)], align="ctr")], fill="447BB2", line_color=BLACK, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 6", IN(9.92), IN(1.554), IN(0.1), IN(0.234), [paragraph([], align="ctr")], fill=None, line_color="FB6B3C", line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "TextBox 7", IN(9.976), IN(1.554), IN(2.101), IN(0.234), [paragraph([run("Port Alpha production modeled", size=PT(10), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr", wrap="none"))
    return "".join(out)


def render() -> str:
    return slide(_body())
