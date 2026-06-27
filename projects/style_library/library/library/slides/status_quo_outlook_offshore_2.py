"""status_quo_outlook_offshore_2 — Commercial Strategy Market Analysis deck (20260325), source slide 46.

EXHIBIT — "Status Quo Outlook (Addressable Offshore 2/2)": a dual-axis time
series (1986–2025) testing whether crude prices drive US offshore-vessel
demand. A styled combo chart overlays US-built & flagged FSV / PSV fleet
additions (# vessels, columns, right axis) against inflation-adjusted WTI and
Brent crude spot prices (2025 $ / barrel, two lines, left axis). Peak fleet-add
years carry value labels (11 / 33 / 23); a left-hand legend keys the three
series (FSV/PSV Adds · WTI Spot Price · Brent Spot Price) with matching swatch +
dashed arrows. A blue callout reports the moderate positive correlation (WTI
r = 0.48, Brent r = 0.46), and a tall grey note flags "No FSV / PSV additions".
Subtitle: favorable upstream capex outlook is contingent on elevated crude, yet
the recent spike did NOT produce fleet adds.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • styled chart ......... graphic_frame(rId2) → CHARTS[0] = styled_chart(...);
                           the data is _CHART0_DATA (3 series: fleet adds + WTI +
                           Brent), the look is the source chart template
  • chart titles ......... two "Text Placeholder 25" axis-title boxes (fleet-adds
                           title right · WTI/Brent crude-price title left)
  • _CATEGORY_TICK_LABELS .......... x-axis year tick labels under the chart (1986 … 2025)
  • _DATA_LABELS ... fleet-add count callouts riding the tallest columns
  • chrome ............... breadcrumb() + title_placeholder() + prelim_chip()
  • legend swatch+rules .. Rectangle 927 colour chip + the two dashed arrow
                           connectors (WTI gold · Brent teal) keying the series
  • _LEGEND_LABELS ....... the three legend captions left of the chart
  • footnote ............. Note/Source line (PCE inflation basis · data sources)
  • scenario chip ........ "(1) Status Quo Scenario" (top-right)
  • correlation callout .. blue box reporting WTI/Brent correlation coefficients

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=7, connector=2, chart=1, chrome_builders=3,
clusters=3 (covering 15 shapes), frozen_fields=15, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide46_chart28.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide46_chart28.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [None, None, None, None, 2, 1, 1, None, 1, 2, 4, 7, 14, 15, 11, 5, 11, 17, 8, 12, 9, 18, 18, 16, 16, 7, 13, 18, 33, 23, 11, 6, 5, 3, 1, 2, None, None, None, None]},
        {"values": [37.29, 46.15, 36.94, 43.53, 52.09, 44.26, 41.19, 35.99, 32.9, 34.52, 40.57, 37.15, 25.79, 34.09, 52.23, 43.79, 43.55, 50.64, 66, 87.53, 99.28, 106.01, 141.87, 88.42, 111.45, 129.76, 126.27, 129.84, 121.76, 63.47, 55.9, 64.48, 81.13, 69.88, 47.49, 79.35, 103.75, 81.71, 78.65, 65.39]},
        {"values": [None, 44.54, 34.49, 40.41, 50.45, 41.17, 38.66, 33.21, 30.34, 31.88, 37.86, 34.45, 22.82, 31.55, 49.27, 41.23, 41.57, 47.01, 60.83, 84.33, 97.94, 106.16, 137.98, 88.12, 111.63, 152.16, 149.87, 143.86, 129.34, 68.25, 56.36, 68.7, 88.73, 78.84, 50.88, 82.53, 110.34, 86.88, 82.64, 69.14]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.236), IN(0.319), IN(0.167)   # year-tick label box [x9]
_PEAKVAL_W, _PEAKVAL_H = IN(0.191), IN(0.167)                 # fleet-add value-label box [x3]
_SERIES_LBL_X, _SERIES_LBL_H = IN(1.33), IN(0.167)            # legend-caption box anchor [x3]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the nine year ticks along the category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x9
    (0.889, "1986"),
    (2.052, "1990"),
    (3.505, "1995"),
    (4.96, "2000"),
    (6.413, "2005"),
    (7.868, "2010"),
    (9.321, "2015"),
    (10.776, "2020"),
    (12.229, "2025"),
]

# local_meaning: the fleet-add counts printed on the three tallest columns.
_DATA_LABELS = [    # (x, y, label) x3 — fleet-add counts on the tallest columns
    (5.606, 5.097, "11"),
    (9.095, 3.304, "33"),
    (9.385, 4.12, "23"),
]

# local_meaning: the three legend captions to the left of the chart.
_LEGEND_LABELS = [    # (y, cx, label) x3 — legend captions left of the chart
    (2.168, 0.936, "FSV/PSV Adds"),
    (2.391, 1.608, "WTI Spot Price ($ / barrel)"),
    (2.613, 1.682, "Brent Spot Price ($ / barrel)"),
]

# ── text layout commentary ──
# text_box(): anchor controls vertical alignment inside the shape; paragraph(..., align=...)
# controls horizontal alignment. l_ins/t_ins/r_ins/b_ins are the internal padding;
# when omitted, the primitive defaults are intentional. paragraph mar_l/indent are
# used only when a text-bearing shape needs a hanging bullet/label margin.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── "No FSV / PSV additions" note (tall grey panel, right edge) ──
    out.append(text_box(n(), "Rectangle 1140", IN(11.389), IN(2.097), IN(1.153), IN(4.092), [paragraph([run("No FSV / PSV additions", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=GRAY_1, line_color="none"))   # F2F2F2 off-white
    # ── styled chart (data-over-template, bundled verbatim + .xlsb so "Edit Data" works) + its two axis titles ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.42), y=IN(1.866), cx=IN(12.521), cy=IN(4.569), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(9.075), IN(1.752), IN(3.753), IN(0.167), [paragraph([run("US-Built & Flagged FSV / PSV Fleet Additions (# Vessels)", size=PT(10), bold=True, color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(0.533), IN(1.752), IN(5.212), IN(0.167), [paragraph([run("West Texas Intermediate (WTI) and Brent Crude Spot Prices (2025 $ per barrel)", size=PT(10), bold=True, color=BLACK, font=FONT), run("1", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── x-axis year tick labels (1986 … 2025) ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── fleet-add value labels on the peak columns (11 / 33 / 23) ──
    for _x, _y, _t in _DATA_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), _PEAKVAL_W, _PEAKVAL_H, [paragraph([run(_t, size=PT(10), font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("Status Quo Outlook (Addressable Offshore 2/2)", "Favorable upstream capex outlook likely contingent upon crude prices remaining elevated, though recent spike did not result in fleet adds."))
    # ── legend swatch + dashed series rules (Rectangle 927 chip · WTI gold arrow · Brent teal arrow) ──
    out.append(text_box(n(), "Rectangle 927", IN(1.078), IN(2.174), IN(0.196), IN(0.146), [paragraph([], align="ctr", line_spacing=100000)], fill="364D6E", line_color="none", anchor="ctr"))   # 364D6E dark blue
    out.append(connector(n(), "Straight Connector 871", IN(1.094), IN(2.469), IN(0.165), IN(0), color="FFC000", width=28575, dashed=True, arrow=True))   # FFC000 amber
    out.append(connector(n(), "Straight Connector 1069", IN(1.094), IN(2.691), IN(0.165), IN(0), color="007770", width=28575, dashed=True, arrow=True))   # 007770 teal
    # ── legend captions (left of the chart) ──
    for _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", _SERIES_LBL_X, IN(_y), IN(_cx), _SERIES_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 701", IN(0.495), IN(6.692), IN(12.367), IN(0.306), [paragraph([run("Note: (1) Historical WTI and Brent spot prices inflated to 2025 $ using US Personal Consumption Expenditures (PCE) index", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: Clarksons (US fleet adds); ", size=PT(8), color=BLACK, font=FONT), run("EIA (WTI Spot)", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("EIA (Brent Spot)", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("FRED (PCE)", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    out.append(prelim_chip())
    # ── scenario chip (top-right) ──
    out.append(text_box(n(), "Rectangle 2", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))   # CEDDEC pale blue
    # ── correlation callout (blue box: WTI r = 0.48 · Brent r = 0.46) ──
    out.append(text_box(n(), "Rectangle 1098", IN(1.031), IN(3.069), IN(3.823), IN(0.994), [paragraph([run("Moderate positive correlation", size=PT(10), bold=True, color=BLACK, font=FONT), run(" ", size=PT(10), bold=True, color=BLACK, font=FONT), run("between crude prices (inflation adjusted) and FSV & PSV fleet additions:", size=PT(10), color=BLACK, font=FONT), line_break(), line_break(), run("WTI correlation coefficient (r) = 0.48 ", size=PT(10), bold=True, color=BLACK, font=FONT), line_break(), run("Brent correlation coefficient (r) = 0.46 ", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color="none", anchor="ctr"))   # CEDDEC pale blue
    return "".join(out)


def render() -> str:
    return slide(_body())
