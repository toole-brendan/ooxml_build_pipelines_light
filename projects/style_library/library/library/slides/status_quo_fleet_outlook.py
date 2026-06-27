"""status_quo_fleet_outlook — Commercial Strategy Market Analysis deck (20260325), source slide 43.

EXHIBIT — "Status Quo Fleet Outlook": after the current orderbook delivers, the
US-flagged/US-built fleet is projected to shrink. A vertical styled column chart
spans the years 2026–2050 (x-axis) against a net gross-tonnage scale (y-axis,
−350…350 K GT through zero); each year's column carries an on-bar value label —
positive early-year additions (32 / 206 / 244 / 265) give way to net retirements
(−10 … −312). Two callouts frame the read: "Bar totals indicate net gross tonnage
added (removed) each year" and "‘31-’50 avg. retirements: ~144K GT p.a."; a dashed
trend connector runs across the retirement years. The title states the fleet is
expected to shrink by ~144K GT p.a. ’31-’50 (<2% of the 10M GT target). A four-row
legend keys Commercial (teal) vs. Offshore (amber) × Retirements / Orderbook.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ................ breadcrumb() + title_placeholder() + prelim_chip()
  • "Years with orderbook data" box .. grey side note left of the chart
  • styled chart ......... graphic_frame(rId2) → CHARTS[0] = styled_chart(...);
                           the data is _CHART0_DATA (3 series × 25 years), the
                           look is the source chart template
  • _VALUE_TICK_LABELS  value-axis gross-tonnage labels (−350 … 350) → loop
  • _CATEGORY_TICK_LABELS  category-axis year labels (2026 … 2050) → loop
  • _DATA_LABELS ........ on-bar values in retirement/orderbook paint-order buckets
  • chart title .......... "Implied Retirements vs. Orderbook…" placeholder
  • _LEGEND_KEYS ......... 4 colour chips (teal Commercial / amber Offshore)
  • _LEGEND_LABELS ....... the 4 legend captions → loop
  • callouts ............. two wedgeRectCallout speech bubbles (net-tonnage note ·
                           ‘31-’50 avg. retirements) + dashed trend connector
  • footnote ............. Note/Source line (service-life assumptions · Clarksons)
  • scenario chip ........ "(1) Status Quo Scenario" (top-right)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=6, connector=1, chart=1, chrome_builders=3, clusters=6
(covering 73 shapes), frozen_fields=69, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide43_chart25.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide43_chart25.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [48049, 96098, 222000, 285000, 285000, -8415, -22359, -31669, -15549, -13908, -14256, -29826, -23429, -25050, -33881, -11820, -31534, -45321, -103450, -58863, -35032, -16215, -18412, -7328, -1634]},
        {"values": [-12518, -949, -16350, -24688, -18715, -1904, -61988, -91245, -61540, None, -85099, -85098, -86641, -196080, -230065, -196080, -87726, -221687, -208874, -216895, -55958, -59960, -29242, -62318, -151354]},
        {"values": [-196731, -62895, None, -16771, -1495, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_YTICK_H = IN(0.167)                         # y-axis tick-label height        [x15]
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.134), IN(0.319), IN(0.167)   # x-axis year row [x25]
_DATA_LABEL_H = IN(0.167)                    # on-bar data-label height [x25]
_SWATCH_X, _SWATCH_W, _SWATCH_H = IN(10.156), IN(0.196), IN(0.146)  # legend chip [x4]
_LEGEND_LBL_X, _LEGEND_LBL_H = IN(10.408), IN(0.167)               # legend caption [x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the fifteen gross-tonnage value-axis ticks (thousands GT).
_VALUE_TICK_LABELS = [    # (x, y, cx, label) x15 — value-axis gross-tonnage tick labels (K GT)
    (0.538, 6.003, 0.276, "-350"),
    (0.538, 5.72, 0.276, "-300"),
    (0.538, 5.436, 0.276, "-250"),
    (0.538, 5.153, 0.276, "-200"),
    (0.538, 4.868, 0.276, "-150"),
    (0.538, 4.585, 0.276, "-100"),
    (0.615, 4.3, 0.2, "-50"),
    (0.738, 4.017, 0.076, "0"),
    (0.661, 3.733, 0.153, "50"),
    (0.585, 3.45, 0.229, "100"),
    (0.585, 3.165, 0.229, "150"),
    (0.585, 2.882, 0.229, "200"),
    (0.585, 2.597, 0.229, "250"),
    (0.585, 2.314, 0.229, "300"),
    (0.585, 2.03, 0.229, "350"),
]

# local_meaning: the twenty-five year ticks along the category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x25 — category-axis year labels
    (1.012, "2026"),
    (1.446, "2027"),
    (1.882, "2028"),
    (2.318, "2029"),
    (2.753, "2030"),
    (3.188, "2031"),
    (3.623, "2032"),
    (4.059, "2033"),
    (4.493, "2034"),
    (4.929, "2035"),
    (5.365, "2036"),
    (5.8, "2037"),
    (6.234, "2038"),
    (6.67, "2039"),
    (7.106, "2040"),
    (7.542, "2041"),
    (7.976, "2042"),
    (8.411, "2043"),
    (8.847, "2044"),
    (9.281, "2045"),
    (9.717, "2046"),
    (10.153, "2047"),
    (10.589, "2048"),
    (11.023, "2049"),
    (11.458, "2050"),
]

# local_meaning: the net gross-tonnage printed on each bar; the 21 net-negative (retirement)
#   years and the 4 early net-positive (orderbook) years are placed differently via the per-row
#   anchor/shape_name field.
_DATA_LABELS = [    # (shape_name, x, y, cx, anchor, label) x25 — on-bar values
    ("Label", 1.016, 5.316, 0.314, "t", "-161"),
    ("Label", 3.229, 4.186, 0.238, "t", "-10"),
    ("Label", 3.665, 4.606, 0.238, "t", "-84"),
    ("Label", 4.062, 4.825, 0.314, "t", "-123"),
    ("Label", 4.535, 4.566, 0.238, "t", "-77"),
    ("Label", 5.406, 4.691, 0.238, "t", "-99"),
    ("Label", 5.804, 4.78, 0.314, "t", "-115"),
    ("Label", 6.238, 4.752, 0.314, "t", "-110"),
    ("Label", 6.674, 5.384, 0.314, "t", "-221"),
    ("Label", 7.109, 5.627, 0.314, "t", "-264"),
    ("Label", 7.545, 5.307, 0.314, "t", "-208"),
    ("Label", 7.979, 4.804, 0.314, "t", "-119"),
    ("Label", 4.97, 4.207, 0.238, "t", "-14"),
    ("Label", 8.851, 5.901, 0.314, "t", "-312"),
    ("Label", 9.285, 5.693, 0.314, "t", "-276"),
    ("Label", 9.759, 4.644, 0.238, "t", "-91"),
    ("Label", 10.194, 4.561, 0.238, "t", "-76"),
    ("Label", 10.63, 4.398, 0.238, "t", "-48"),
    ("Label", 11.064, 4.523, 0.238, "t", "-70"),
    ("Label", 11.462, 4.997, 0.314, "t", "-153"),
    ("Label", 8.415, 5.644, 0.314, "t", "-267"),
    ("ValueLabel", 1.51, 3.359, 0.191, "b", "32"),
    ("ValueLabel", 1.908, 2.646, 0.267, "b", "206"),
    ("ValueLabel", 2.344, 2.288, 0.267, "b", "244"),
    ("ValueLabel", 2.78, 2.288, 0.267, "b", "265"),
]

# local_meaning: the four legend colour chips: teal Commercial vs amber Offshore.
_LEGEND_KEYS = [    # (y, fill) x4 — colour chips: teal Commercial / amber Offshore
    (2.174, "007770"),   # 007770 teal
    (2.396, "007770"),   # 007770 teal
    (2.618, "FFC000"),   # FFC000 amber
    (2.84, "FFC000"),    # FFC000 amber
]

# local_meaning: the four legend captions crossing Retirements/Orderbook with
#   Commercial/Offshore.
_LEGEND_LABELS = [    # (y, cx, label) x4 — legend captions (Retirements / Orderbook × Commercial / Offshore)
    (2.168, 2.332, "Addressable Commercial Retirements"),
    (2.391, 2.238, "Addressable Commercial Orderbook"),
    (2.613, 2.12, "Addressable Offshore Retirements"),
    (2.835, 2.026, "Addressable Offshore Orderbook"),
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
    # ── side note (left of the chart) — which years carry orderbook data ──
    out.append(text_box(n(), "Rectangle 995", IN(0.95), IN(2.104), IN(2.182), IN(4.196), [paragraph([run("Years with ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("orderbook ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("data", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=GRAY_1, line_color="none"))   # F2F2F2 off-white
    # ── styled chart (data-over-template), bundled verbatim + .xlsb ("Edit Data" works) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.865), y=IN(2.023), cx=IN(11.062), cy=IN(4.155), rId="rId2"))
    # ── value-axis gross-tonnage tick labels ──
    for _x, _y, _cx, _t in _VALUE_TICK_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _YTICK_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── category-axis year labels ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── on-bar data labels — row-level anchor preserves negative/positive placement ──
    # Insets are the source 17,463 EMU left/right and zero top/bottom; paragraph
    # margins are zero so the centered label sits flush within that padded box.
    for _name, _x, _y, _cx, _anchor, _t in _DATA_LABELS:
        out.append(text_box(n(), _name, IN(_x), IN(_y), IN(_cx), _DATA_LABEL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor=_anchor, wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chart title ──
    out.append(text_box(n(), "Text Placeholder 25", IN(0.585), IN(1.752), IN(8.285), IN(0.167), [paragraph([run("Implied Retirements vs. Orderbook of US-Flagged, US-Built Vessels (K GT, High and Partial Autonomy Fit Vessel Archetypes) ", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("Status Quo Fleet Outlook", "Following completion of orderbook deliveries, fleet is expected to shrink by ~144K GT p.a. ’31-’50 (<2% of 10M GT target)."))
    # ── legend: colour chips + captions ──
    for _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", _SWATCH_X, IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", _LEGEND_LBL_X, IN(_y), IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── callouts — net-tonnage note + dashed trend connector + ‘31-’50 avg. retirements ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 960", IN(10.306), IN(1.705), IN(2.488), IN(0.425), [paragraph([run("Bar totals indicate net gross tonnage added (removed) each year", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=WHITE, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val -19106", "adj2": "val -3267"}, anchor="ctr"))   # FFFFFF white
    out.append(connector(n(), "Straight Arrow Connector 1045", IN(3.196), IN(4.898), IN(8.7), IN(0), color=BLACK, width=12700, dashed=True))   # 000000 black
    out.append(text_box(n(), "Speech Bubble: Rectangle 1050", IN(11.806), IN(4.632), IN(1.2), IN(0.522), [paragraph([run("‘31-’50 avg. retirements: ", size=PT(10), italic=True, color=BLACK, font=FONT), run("~144K GT p.a.", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", prst="wedgeRectCallout", geom_adj={"adj1": "val -19106", "adj2": "val -3267"}, anchor="ctr"))   # 000000 black
    # ── footnote — kept verbatim (sits off the house Source position) ──
    out.append(text_box(n(), "Rectangle 48", IN(0.495), IN(6.679), IN(12.367), IN(0.319), [paragraph([run("Note: Service life assumptions – 40 years for Bulk, Container, General Cargo, and RORO, 35 years for Tankers, 30 years for PSVs, and 25 years for Crew/FSVs ", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: Clarksons (US fleet size and GT data)", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    out.append(prelim_chip())
    # ── scenario chip (top-right) ──
    out.append(text_box(n(), "Rectangle 2", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))   # CEDDEC pale blue
    return "".join(out)


def render() -> str:
    return slide(_body())
