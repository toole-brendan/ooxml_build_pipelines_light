"""us_delivery_capacity — Commercial Strategy Market Analysis deck (20260325), source slide 53.

EXHIBIT — "US Delivery Capacity": US-built oceangoing commercial delivery capacity
ramps from ~1 to ~166 potential deliveries/yr through 2050, expansion largely
driven by Saronic. A styled stacked-area chart spans the years 2026-2050 (x-axis
labels) with per-year capacity totals riding the bars (12 · 20 · 30 … 166); seven
colour swatches key the contributing shipyards (GD NASSCO · Tampa Ship · Bollinger
· New Entrant · Hanwha 2nd Yard · Hanwha Philly · Saronic). A right-hand "Inputs &
Assumptions" panel narrates the Total / Saronic / Competitor capacity build-ups,
and a bottom strip of ellipse badges summarises Total US GT, oceangoing commercial
GT, and the % attributable to Port Alpha at five snapshot years.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • styled chart ....... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                         data is _CHART0_DATA (7 shipyard series), the look is the
                         source chart template
  • _CATEGORY_TICK_LABELS ........ category-axis labels 2026…2050 → loop
  • _DATA_LABELS .. per-year capacity totals riding the bars (12…166) → loop
  • chart title ........ "US-Built Oceangoing Commercial Delivery Capacity…" box
  • _LEGEND_KEYS ... the 7 shipyard colour chips → loop
  • _LEGEND_LABELS ... the shipyard caption text beside each chip → loop
  • chrome ............. breadcrumb() + title_placeholder()
  • footnote ........... Note/Source row (Rectangle 17)
  • inputs panel ....... "Total Delivery Capacity" assumptions block (Rectangle 244)
                         + "Inputs & Assumptions" header table()
  • summary strip ...... row labels (Total US GT / oceangoing commercial GT / % to
                         Port Alpha) + _SUMMARY_BADGES ellipses (1.1M…75%) → loop
  • callouts ........... three wedgeRectCallout / rectangle notes (non-oceangoing
                         GT · implied-from-orderbook · Saronic ramp)
  • scope chip ......... "All Scenarios" (top-right) + prelim_chip()

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=10, chart=1, table=1, chrome_builders=3, clusters=5
(covering 76 shapes), frozen_fields=54, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide53_chart32.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide53_chart32.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [1, 2, 2, 7, 14, 23, 40, 56, 85, 97, 111, 110, 110, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125]},
        {"values": [None, None, None, 5, 6, 6, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 20, 20, 20, 20, 20]},
        {"values": [None, None, None, None, None, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5]},
        {"values": [None, None, None, None, None, None, 1, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]},
        {"values": [None, None, None, None, None, None, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]},
        {"values": [None, None, None, None, None, None, 1, 2, 2, 3, 3, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]},
        {"values": [None, None, None, None, None, None, None, None, 1, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell_rich() form — the only
#    change is legibility. ──
def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...).
    Pass l_ins/r_ins explicitly for non-default padding (e.g. 41564); omit for the 45720 default."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(5.042), IN(0.167), IN(0.306)        # x-axis year-label row [x25]
_VALUE_LBL_H = IN(0.167)                                           # bar value-label height [x22]
_SWATCH_X, _SWATCH_W, _SWATCH_H = IN(0.967), IN(0.196), IN(0.146)  # legend chip [x7]
_SHIPYARD_LBL_H = IN(0.167)                                        # shipyard caption height [x7]
_BADGE_W, _BADGE_H = IN(0.602), IN(0.256)                          # summary-strip ellipse [x15]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the twenty-five year ticks along the category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x25
    (0.997, "2026"),
    (1.335, "2027"),
    (1.674, "2028"),
    (2.012, "2029"),
    (2.351, "2030"),
    (2.689, "2031"),
    (3.026, "2032"),
    (3.365, "2033"),
    (3.703, "2034"),
    (4.042, "2035"),
    (4.38, "2036"),
    (4.719, "2037"),
    (5.057, "2038"),
    (5.396, "2039"),
    (5.734, "2040"),
    (6.073, "2041"),
    (6.411, "2042"),
    (6.75, "2043"),
    (7.087, "2044"),
    (7.425, "2045"),
    (7.764, "2046"),
    (8.102, "2047"),
    (8.441, "2048"),
    (8.78, "2049"),
    (9.118, "2050"),
]

# local_meaning: the per-year delivery-capacity totals riding the bars.
_DATA_LABELS = [    # (x, y, cx, label) x22 — per-year capacity totals riding the bars
    (2, 4.592, 0.191, "12"),
    (2.339, 4.453, 0.191, "20"),
    (2.677, 4.28, 0.191, "30"),
    (3.014, 3.931, 0.191, "50"),
    (3.352, 3.601, 0.191, "69"),
    (3.653, 3.01, 0.267, "103"),
    (3.991, 2.767, 0.267, "117"),
    (4.33, 2.49, 0.267, "133"),
    (4.668, 2.418, 0.267, "137"),
    (5.007, 2.384, 0.267, "139"),
    (5.684, 2.019, 0.267, "160"),
    (6.023, 2.002, 0.267, "161"),
    (6.361, 1.984, 0.267, "162"),
    (6.7, 1.95, 0.267, "164"),
    (7.036, 1.932, 0.267, "165"),
    (5.345, 2.089, 0.267, "156"),
    (7.714, 1.915, 0.267, "166"),
    (8.052, 1.915, 0.267, "166"),
    (8.391, 1.915, 0.267, "166"),
    (8.729, 1.915, 0.267, "166"),
    (9.068, 1.915, 0.267, "166"),
    (7.375, 1.915, 0.267, "166"),
]

# local_meaning: the seven shipyard colour chips.
_LEGEND_KEYS = [    # (y, fill) x7
    (1.927, "808080"),   # 808080 gray
    (2.149, "C3CFE1"),   # C3CFE1 light blue
    (2.372, "9DB1CF"),   # 9DB1CF light blue
    (2.594, "6F8DB9"),   # 6F8DB9 blue
    (2.816, "4C6C9C"),   # 4C6C9C blue
    (3.038, "364D6E"),   # 364D6E dark blue
    (3.26, "007770"),   # 007770 teal
]

# local_meaning: the seven shipyard captions beside the legend chips.
_LEGEND_LABELS = [    # (x, y, cx, label) x7 — shipyard captions beside the legend chips
    (1.219, 1.922, 1.194, "GD NASSCO (SHI)"),
    (1.219, 2.144, 1.356, "Tampa Ship (HD HHI)"),
    (1.219, 2.366, 0.576, "Bollinger "),
    (1.219, 2.589, 1.944, "New Entrant (e.g., HD Hyundai)"),
    (1.219, 2.811, 1.104, "Hanwha 2nd Yard"),
    (1.219, 3.033, 0.877, "Hanwha Philly"),
    (1.219, 3.255, 0.469, "Saronic"),
]

# local_meaning: the fifteen bottom-strip badges: GT totals (top/mid rows) plus % to Port Alpha
#   (bottom row).
_SUMMARY_BADGES = [    # (x, y, label) x15 — bottom-strip ellipses: GT totals (top/mid rows) + % to Port Alpha (bottom row)
    (2.128, 5.889, "1.1M"),
    (3.824, 5.889, "6.0M"),
    (5.517, 5.889, "8.1M"),
    (7.208, 5.889, "8.4M"),
    (8.9, 5.889, "8.4M"),
    (2.128, 5.492, "1.0M"),
    (3.824, 5.492, "5.9M"),
    (5.517, 5.492, "8.0M"),
    (7.208, 5.492, "8.3M"),
    (8.9, 5.492, "8.3M"),
    (2.128, 6.285, "70%"),
    (3.824, 6.285, "83%"),
    (5.517, 6.285, "78%"),
    (7.208, 6.285, "75%"),
    (8.9, 6.285, "75%"),
]

# ── table-cell layout commentary ──
# table(): col_widths are column-level sizing and trow(h=...) is a minimum row
# height. Each tcell/tcell_rich owns internal padding via l_ins/r_ins/t_ins/b_ins
# and vertical alignment via anchor=...; horizontal alignment and paragraph
# margins live in tcell(..., align=...) or tpara(..., align=..., mar_l=..., indent=...).

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
    # ── styled chart (data-over-template), bundled verbatim + .xlsb ("Edit Data" works) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.429), y=IN(1.62), cx=IN(9.033), cy=IN(3.622), rId="rId2"))
    # ── category-axis labels (2026…2050) ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── per-year capacity totals riding the bars ──
    for _x, _y, _cx, _t in _DATA_LABELS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), IN(_cx), _VALUE_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chart title ──
    out.append(text_box(n(), "Text Placeholder 25", IN(0.542), IN(1.505), IN(5.773), IN(0.167), [paragraph([run("US-Built Oceangoing Commercial Delivery Capacity by Shipyard  (# potential deliveries)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── legend: 7 shipyard colour chips, then their captions ──
    for _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", _SWATCH_X, IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _x, _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _SHIPYARD_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "With SHIPS Act"))
    out.append(title_placeholder("US Delivery Capacity", "Expansion largely driven by Saronic; Competitor growth enabled by ownership / partnerships with major ROK shipbuilders and completion of USN/USCG activity."))
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 17", IN(0.495), IN(6.675), IN(12.367), IN(0.322), [paragraph([run("Note: (1) Assumes avg. 50K GT per newbuild (~13K higher than current fleet avg.); 10M GT target may be achieved with 140-160 deliveries / year with 60K-70K GT per newbuild ", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: Saronic IP (Jan ’26); ", size=PT(8), color=BLACK, font=FONT), run("Hanwha Philly", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("Breaking Defense (Hanwha 2", size=PT(8), color=BLACK, font=FONT), run("nd", size=PT(8), color=BLACK, font=FONT), run(" Yard)", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("Conrad Shipyard", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("HD Hyundai (Tampa Ship)", size=PT(8), color=BLACK, font=FONT), run("; ", size=PT(8), color=BLACK, font=FONT), run("GD NASSCO", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    # ── inputs panel (right): "Total Delivery Capacity" assumptions block ──
    out.append(text_box(n(), "Rectangle 244", IN(9.439), IN(1.742), IN(3.674), IN(4.365), [paragraph([run("Total Delivery Capacity", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("US ramps to 8.3M GT by early 2050s based on Investor Presentation target (Jan ’26) ", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Avg. GT stays ~50K / ship, in line with recent US built containerships; ~10K above 10-yr. avg. for commercially viable, ocean ships", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Saronic Capacity", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Port Alpha ramps from 7 deliveries in 2029 to 125 delivery capacity by late ’30s to align with IP assertion of achieving 10M GT of US capacity", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Competitor Capacities", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Hanwha Philly achieves 10 deliveries/yr. by mid-2030s and 20 deliveries/yr. by mid-2040s, in line with stated goals", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Hanwha purchase 2", size=PT(10), color=BLACK, font=FONT), run("nd", size=PT(10), color=BLACK, font=FONT), run(" yard in the US, ramping to 5 deliveries/yr. by mid-2040s", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("HD Hyundai potentially enters US market, purchasing a Gulf Coast yard, ramping production through 2030s", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Tampa Ship begins producing commercial vessels in early 2030s, enabled by HD HII partnership", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Bollinger begins producing commercial vessels in early-to-mid 2030s after completion of USCG vessels", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("GD NASSCO begins delivering commercial vessels after completion of Navy T-AO in early-to-mid 2030s", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)], fill=None, line_color="none"))   # 000000 black
    # "Inputs & Assumptions" header bar — native table()/trow()/tcell_rich()
    # palette — text: 000000 black (header); fills: none; rules: FFFFFF white (top) · 000000 black (bottom).
    out.append(table(n(), "Table 245", IN(9.439), IN(1.431), IN(3.674), IN(0.3), col_widths=[IN(3.674)], rows=[
        trow([rcell([tpara([trun("Inputs & Assumptions ", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], l_ins=41564, r_ins=41564, T=edge(WHITE), B=edge(BLACK))], h=IN(0.3)),
    ]))
    # ── summary strip (bottom): row labels + ellipse badges interleave in paint order ──
    out.append(text_box(n(), "Rectangle 394", IN(0.113), IN(5.846), IN(2), IN(0.34), [paragraph([run("Total US GT ", size=PT(10), bold=True, color=BLACK, font=FONT), run("(incl. non-ocean/commercial)", size=PT(10), italic=True, color=BLACK, font=FONT), run(":", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    for _x, _y, _t in _SUMMARY_BADGES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _BADGE_W, _BADGE_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=6350, prst="ellipse", anchor="ctr", l_ins=0, r_ins=0))   # 000000 black outline
    out.append(text_box(n(), "Rectangle 390", IN(0.113), IN(5.45), IN(2), IN(0.34), [paragraph([run("Oceangoing commercial GT", size=PT(10), bold=True, color=BLACK, font=FONT), run("1", size=PT(10), bold=True, color=BLACK, font=FONT), run(":", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 413", IN(0.113), IN(6.243), IN(2), IN(0.34), [paragraph([run("% oceangoing commercial attributable to Port Alpha:", size=PT(10), bold=True, italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── callouts ──
    out.append(text_box(n(), "Speech Bubble: Rectangle 423", IN(9.99), IN(5.889), IN(2.797), IN(1.04), [paragraph([run("Est. ~100K GT for naval, USCG, offshore, and other vessels remains relatively stable through forecast; implied amount based on current orderbook for non-oceangoing commercial and assumed defense/national security production", size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="121415", prst="wedgeRectCallout", geom_adj={"adj1": "val -62578", "adj2": "val -35925"}, anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "Speech Bubble: Rectangle 83", IN(0.965), IN(3.546), IN(1.712), IN(0.699), [paragraph([run("Implied delivery capacity based on orderbook; excludes idle / underutilized yards", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="121415", prst="wedgeRectCallout", geom_adj={"adj1": "val -21817", "adj2": "val 120159"}, anchor="ctr"))   # FFFFFF white
    out.append(text_box(n(), "Rectangle 88", IN(5.224), IN(4.28), IN(3.993), IN(0.628), [paragraph([run("Saronic capacity assumes Port Alpha ramps from 7 delivery capacity in 2029 to 125 deliveries by late 2030s to align with IP assertion of achieving 10M GT of US shipbuilding capacity ", size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=BLACK, anchor="ctr"))   # FFFFFF white
    # ── scope chip (top-right) ──
    out.append(text_box(n(), "Rectangle 91", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("All Scenarios", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, anchor="ctr"))   # 000000 black outline
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
