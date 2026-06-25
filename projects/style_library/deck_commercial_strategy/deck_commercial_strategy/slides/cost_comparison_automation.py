"""cost_comparison_automation - Commercial Strategy deck, source slide 104.

Auto-converted from the source .pptx by _tools/convert_slide.py.
The native <c:chart> exhibit is a data-over-template styled_chart: the
source chart part is the exact STYLE template and its values live in the
_CHART*_DATA literal (look byte-identical, "Edit Data" still works).
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; the OLE frame + EMF preview dropped.

Converter stats: text_box=9, connector=8, chart=1, table=0, chrome_builders=2, clusters=7 (covering 56 shapes), raw_verbatim=0, dropped=1, frozen_fields=45.

Converter notes:
  - Note/Source line off house position - kept verbatim
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, breadcrumb, title_placeholder,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, BREADCRUMB, PRELIM, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide104_chart59.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide104_chart59.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [11.41, 11.41, 10.84, 11.41, 10.84]},
        {"values": [11.07, 8.3, 5.53, 1.7, 1.59]},
        {"values": [2.12, 2.01, 1.91, 0.14, 0.07]},
        {"values": [0.71, 0.64, 0.6, 0.4, 0.38]},
        {"values": [0.4, 0.4, 0.38, 3.02, 3.2]},
        {"values": [3.55, 3.38, 3.2, 1.78, 1.52]},
        {"values": [1.27, 1.52, 1.46, 0.19, 0.08]},
        {"values": [0.76, 0.57, 0.38, 8.34, 7.9]},
        {"values": [8.78, 9.21, 8.78, 0.03, 0.03]},
        {"values": [0.13, 0.1, 0.08, 3, 2.8]},
        {"values": [0, 2.5, 2.3, None, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates) ──
_LBL_W, _LBL_H = IN(0.229), IN(0.167)
_LBL2_W, _LBL2_H = IN(0.229), IN(0.167)
_LBL3_Y, _LBL3_H = IN(6.484), IN(0.167)
_LBL4_W, _LBL4_H = IN(0.306), IN(0.167)
_LBL5_Y, _LBL5_H = IN(2.332), IN(0.236)
_SW_X, _SW_W, _SW_H = IN(11.344), IN(0.196), IN(0.146)
_LBL6_X, _LBL6_H = IN(11.595), IN(0.167)
_Y1 = IN(2.45)   # shared x5

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, fill, label) x16
    (3.464, 2.997, "89A2B0", "0.1"),
    (3.773, 3.851, "1D4D68", "0.6"),
    (3.773, 4.38, "6F8DB9", "0.6"),
    (5.622, 3.389, "89A2B0", "0.1"),
    (5.931, 4.194, "1D4D68", "0.4"),
    (5.931, 4.689, "6F8DB9", "0.6"),
    (7.781, 3.936, "89A2B0", "0.0"),
    (8.09, 4.693, "1D4D68", "0.2"),
    (8.09, 5.174, "6F8DB9", "0.1"),
    (9.939, 4.062, "89A2B0", "0.0"),
    (10.248, 4.774, "1D4D68", "0.1"),
    (10.248, 5.238, "6F8DB9", "0.1"),
    (1.613, 2.753, "007770", "0.0"),
    (1.304, 2.759, "89A2B0", "0.1"),
    (1.613, 3.585, "1D4D68", "0.8"),
    (1.613, 4.12, "6F8DB9", "0.7"),
]

_LABELS2 = [    # (x, y, fill, label) x4
    (3.464, 4.333, "9DB1CF", "0.4"),
    (5.622, 4.646, "9DB1CF", "0.4"),
    (1.304, 4.069, "9DB1CF", "0.4"),
    (1.304, 3.677, "DFE5EF", "1.3"),
]

_LABELS3 = [    # (x, cx, label) x5
    (3.328, 0.811, "Lower bound"),
    (5.486, 0.811, "Upper bound"),
    (9.804, 0.811, "Upper bound"),
    (1.144, 0.858, "Daniel Inouye"),
    (7.646, 0.811, "Lower bound"),
]

_LABELS4 = [    # (x, y, label) x5
    (3.58, 2.658, "40.0"),
    (5.738, 3.068, "35.5"),
    (7.898, 3.556, "30.0"),
    (10.056, 3.7, "28.4"),
    (1.42, 2.587, "40.2"),
]

_LABELS5 = [    # (x, cx, label) x4
    (2.512, 0.283, "0%"),
    (4.582, 0.458, "-12%"),
    (6.741, 0.458, "-25%"),
    (8.899, 0.458, "-29%"),
]

_LEGEND_SWATCHES = [    # (y, fill) x11
    (3.998, "007770"),
    (4.22, "89A2B0"),
    (4.443, "486D82"),
    (4.665, "1D4D68"),
    (4.887, "DFE5EF"),
    (5.109, "C3CFE1"),
    (5.332, "9DB1CF"),
    (5.554, "6F8DB9"),
    (5.776, "364D6E"),
    (5.998, "C30C3E"),
    (6.22, "79838F"),
]

_LABELS6 = [    # (y, cx, label) x11
    (3.993, 1.144, "Autonomy-Related"),
    (4.215, 0.714, "Other Opex"),
    (4.438, 0.285, "D&A"),
    (4.66, 0.908, "Mgmt & Admin"),
    (4.882, 0.58, "Dry-Dock"),
    (5.104, 0.309, "R&M"),
    (5.326, 0.953, "Lubricating Oils"),
    (5.549, 1.005, "Stores & Spares"),
    (5.771, 0.606, "Insurance"),
    (5.993, 0.325, "Crew"),
    (6.215, 0.269, "Fuel"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(text_box(n(), "Rectangle 663", IN(2.279), IN(2.201), IN(2.918), IN(0.417), [paragraph([run("Vs. Minimally Manned", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr")], fill="CEDDEC", line_color=BLACK))
    out.append(text_box(n(), "Rectangle 683", IN(6.596), IN(2.201), IN(2.918), IN(0.417), [paragraph([run("Vs. Fully Autonomous", size=PT(10), bold=True, italic=True, color=WHITE, font=FONT)], align="ctr")], fill="447BB2", line_color=BLACK))
    # native chart, bundled verbatim + .xlsb ("Edit Data" works)
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.405), y=IN(1.714), cx=IN(10.974), cy=IN(4.97), rId="rId2"))
    out.append(connector(n(), "Straight Connector 182", IN(3.733), _Y1, IN(0), IN(0.167), color=DK, width=12700, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 655", IN(5.891), _Y1, IN(0), IN(0.576), color=DK, width=12700, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 660", IN(8.05), _Y1, IN(0), IN(1.064), color=DK, width=12700, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 188", IN(10.208), _Y1, IN(0), IN(1.208), color=DK, width=12700, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 186", IN(1.573), IN(2.45), IN(0), IN(-0.095), color=DK, width=12700, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 187", IN(1.573), _Y1, IN(8.635), IN(0), color=DK, width=12700, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 674", IN(8.281), IN(5.233), IN(-0.095), IN(0), color=BREADCRUMB, width=6350, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 676", IN(10.439), IN(5.3), IN(-0.095), IN(0), color=BREADCRUMB, width=6350, dashed=True, arrow=True))
    for _x, _y, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    for _x, _y, _fill, _t in _LABELS2:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _LBL2_W, _LBL2_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    for _x, _cx, _t in _LABELS3:
        out.append(text_box(n(), "Label", IN(_x), _LBL3_Y, IN(_cx), _LBL3_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.495), IN(1.677), IN(4.005), IN(0.167), [paragraph([run("Annual Opex & Fuel for 3,600 TEU containership ($M, ", size=PT(10), bold=True, color=BLACK, font=FONT), run("2025 $", size=PT(10), bold=True, color=BLACK, font=FONT), run(")", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    for _x, _y, _t in _LABELS4:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _LBL4_W, _LBL4_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    for _x, _cx, _t in _LABELS5:
        out.append(text_box(n(), "Label", IN(_x), _LBL5_Y, IN(_cx), _LBL5_H, [paragraph([run(_t, size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0)], fill=WHITE, line_color=DK, line_width=9525, prst="ellipse", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(breadcrumb("Impact of Automation on Vessel Costs", "Comparison vs. Conventional Ships"))
    out.append(title_placeholder("Cost Comparison (1/3)", "Minimally manned may see ~0-12% lower costs; Fully autonomous may see ~25-30% lower costs."))
    for _y, _fill in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", _SW_X, IN(_y), _SW_W, _SW_H, [paragraph([], align="ctr")], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _LABELS6:
        out.append(text_box(n(), "Label", _LBL6_X, IN(_y), IN(_cx), _LBL6_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "TextBox 2", IN(3.184), IN(6.674), IN(3.232), IN(0.269), [paragraph([run("Minimally-Manned", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr")], fill="CEDDEC", line_color=BLACK, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "TextBox 4", IN(7.526), IN(6.674), IN(3.233), IN(0.269), [paragraph([run("Fully Autonomous", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr")], fill="447BB2", line_color=BLACK, l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Speech Bubble: Rectangle 56", IN(10.426), IN(2.554), IN(2.604), IN(1.095), [paragraph([run("Upper Bound assumes vertical integration between BuildCo and OpCo; Lower bound represents sales to other customers, with software license benchmarked to Marauder ($2M / year) ", size=PT(10), color=BLACK, font=FONT)], align="ctr")], fill=WHITE, line_color="121415", prst="wedgeRectCallout", geom_adj={"adj1": "val -58149", "adj2": "val -22131"}, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 16", IN(9.471), IN(1.248), IN(3.363), IN(0.45), [paragraph([run("Saronic-Built, US-Flagged, ", size=PT(10), italic=True, color=BLACK, font=FONT), run("Non-Saronic Operated", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT), run("D&A shown for Port Alpha newbuild (hull #10)", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr")], fill=GRAY_1, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 21", IN(8.048), IN(0.173), IN(4.785), IN(0.217), [paragraph([run("Preliminary – values shown are hypotheses to be tested", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr")], fill=PRELIM, line_color="121415", line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 71", IN(0.495), IN(7.01), IN(4.9), IN(0.317), [paragraph([run("Source: Volume, US vs. Foreign Shipbuilding, and US vs. Foreign Opex pages (US D&A and US Opex); Matson pages (fuel expense); Market participant feedback (Potential autonomy impact)", size=PT(8), color=BLACK, font=FONT)]), paragraph([])], fill=None, line_color="none"))
    return "".join(out)


def render() -> str:
    return slide(_body())
