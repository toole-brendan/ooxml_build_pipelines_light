"""fleet_overview — Commercial Strategy Market Analysis deck (20260325), source slide 42.

EXHIBIT — "US-Flagged, US-Built Fleet Overview": the entire US-flagged and
US-built fleet (~6.6M gross tons) is less than a single year's capacity target
(10M GT), and only ~3.9M GT of it is addressable. A horizontal styled bar chart
(left) breaks the fleet into six segments by gross tonnage; to its right, three
stacked "big-number" cards (10M target · ~6.6M current · ~3.9M addressable) make
the shortfall explicit, with a right-column comparison annotation. A colour
legend keys the six segments by addressability.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • styled chart ......... graphic_frame(rId2) → CHARTS[0] = styled_chart(...);
                           the data is _CHART0_DATA (6 segment gross-tonnages),
                           the look is the source chart template
  • chart title .......... "…Fleet Composition by Gross Tonnage" placeholder
  • _CATEGORY_TICK_LABELS . manual category-axis labels left of the bars (Total /
                           Commercial / Great Lakes / …)
  • _DATA_LABELS ........ GT-in-millions labels attached to the bars (6.6 / 3.3 …)
  • chrome ............... breadcrumb() + title_placeholder() + prelim_chip()
  • big-number cards ..... Rectangle 1143/1144/1145 = 10M / ~6.6M / ~3.9M cards
  • _ANNOTATION_BOXES ... right-column commentary boxes (Annual target · current vs.
                           addressable GT · "rebuild the fleet 1.5x/yr" note)
  • legend ............... frame + "Addressability" title + _LEGEND_KEYS marks
                           + _LEGEND_LABELS captions
  • scenario chip ........ "(1) Status Quo Scenario" (top-right)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=8, chart=1, chrome_builders=3, clusters=5 (covering
26 shapes), frozen_fields=17, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide42_chart24.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide42_chart24.xlsb").read_bytes()

# data-over-template: these values drive the chart render; the style is the template.
_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [6628515, 3347252, 739991, 625304, 334461, 1581507]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_SEGMENT_LBL_H = IN(0.167)                       # segment category-label height [x6]
_BARVAL_W, _BARVAL_H = IN(0.229), IN(0.167)      # bar value-label box           [x6]
_COMPARE_LBL_H = IN(1)                           # comparison-callout height     [x4]
_SWATCH_X, _SWATCH_W, _SWATCH_H = IN(5.632), IN(0.196), IN(0.146)  # legend chip [x5]
_LEGEND_LBL_X, _LEGEND_LBL_H = IN(5.884), IN(0.167)               # legend caption [x5]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the six vessel-segment category labels down the left of the chart bars.
_CATEGORY_TICK_LABELS = [    # (x, y, cx, label) x6 — manual category-axis labels
    (1.887, 2.295, 0.307, "Total"),
    (0.648, 2.955, 1.547, "Addressable Commercial"),
    (0.663, 3.616, 1.531, "Great Lakes Commercial"),
    (0.859, 4.276, 1.335, "Addressable Offshore"),
    (0.559, 4.936, 1.635, "Non-Addressable Offshore"),
    (1.189, 5.597, 1.005, "Other Segments"),
]

# local_meaning: the gross-tonnage (millions GT) value printed on each of the six bars.
_DATA_LABELS = [    # (x, y, label) x6 — values attached to plotted bars
    (7.514, 2.295, "6.6"),
    (4.941, 2.955, "3.3"),
    (2.896, 3.616, "0.7"),
    (2.806, 4.276, "0.6"),
    (2.578, 4.936, "0.3"),
    (3.556, 5.597, "1.6"),
]

# local_meaning: the four right-column commentary boxes (tail-less callouts) comparing fleet
#   segments.
_ANNOTATION_BOXES = [    # (x, y, cx, fill, label) x4 — commentary boxes without pointer tails
    (9.504, 1.764, 3.292, None, "Annual target"),   # 000000 black
    (9.504, 2.939, 3.292, None, "Current US-flagged, US-built fleet gross tonnage"),   # 000000 black
    (9.504, 4.113, 3.292, None, "Addressable Commercial and Offshore gross tonnage"),   # 000000 black
    (8.038, 5.288, 4.757, "CEDDEC", "Reaching throughput target requires rebuilding the entire fleet 1.5x every year"),   # CEDDEC pale blue
]

# local_meaning: the five legend colour chips keying the bar fills by addressability.
_LEGEND_KEYS = [    # (y, fill) x5 — visual category keys
    (4.905, "007770"),   # 007770 teal
    (5.127, "FFC000"),   # FFC000 amber
    (5.349, "969696"),   # 969696 gray
    (5.571, "969696"),   # 969696 gray
    (5.793, "969696"),   # 969696 gray
]

# local_meaning: the five legend captions for the addressability colour keys.
_LEGEND_LABELS = [    # (y, cx, label) x5 — legend captions
    (4.899, 1.547, "Addressable Commercial"),
    (5.122, 1.335, "Addressable Offshore"),
    (5.344, 1.531, "Great Lakes Commercial"),
    (5.566, 1.635, "Non-Addressable Offshore"),
    (5.788, 1.005, "Other Segments"),
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
    # ── styled chart (data-over-template) + its title ──
    # Shape text: the title is bottom-anchored, no-wrap, and zero-inset to align
    # tightly with the chart frame.
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(2.198), y=IN(1.958), cx=IN(5.378), cy=IN(4.142), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(2.283), IN(1.766), IN(4.997), IN(0.167), [paragraph([run("US-Flagged, US-Built Fleet Composition by Gross Tonnage (GT in millions)", size=PT(10), bold=True, color=BLACK, font=FONT), run("1", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── category-axis labels (left of the bars) ──
    for _x, _y, _cx, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _SEGMENT_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="r", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── data labels (GT in millions) ──
    # Shape text: vertically centered with tight 17,463-EMU side padding; paragraph
    # margins are zero so the figures sit consistently against bar ends.
    for _x, _y, _t in _DATA_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _BARVAL_W, _BARVAL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))   # 000000 black
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("US-Flagged, US-Built Fleet Overview", "Entire US-flagged and US-built fleet (~6.6M GT) is less than 1 year’s capacity target (10M GT); addressable fleet is ~3.9M GT."))
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 125", IN(0.495), IN(6.665), IN(12.367), IN(0.332), [paragraph([run("Note: (1) As of January 2026; Addressable Commercial defined as oceangoing vessels", size=PT(8), color=BLACK, font=FONT), line_break(), run("Source: Clarksons (US fleet size and GT data)", size=PT(8), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none"))   # 000000 black
    # ── big-number cards: 10M target · ~6.6M current · ~3.9M addressable ──
    # Shape text: cards use anchor="ctr" and centered paragraphs; default internal
    # padding is retained to keep the two-line number/unit blocks balanced.
    out.append(text_box(n(), "Rectangle 1143", IN(8.038), IN(1.764), IN(1.466), IN(1), [paragraph([run("10M", size=PT(28), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Gross tons", size=PT(16), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="none", anchor="ctr"))   # F2F2F2 off-white
    out.append(text_box(n(), "Rectangle 1144", IN(8.038), IN(2.939), IN(1.466), IN(1), [paragraph([run("~6.6M", size=PT(28), bold=True, color="C00000", font=FONT), line_break(), run("Gross tons", size=PT(16), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="none", anchor="ctr"))   # F2F2F2 off-white
    out.append(text_box(n(), "Rectangle 1145", IN(8.038), IN(4.113), IN(1.466), IN(1), [paragraph([run("~3.9M", size=PT(28), bold=True, color="C00000", font=FONT), line_break(), run("Gross tons", size=PT(16), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="none", anchor="ctr"))   # F2F2F2 off-white
    # ── annotation boxes in the comparison column ──
    for _x, _y, _cx, _fill, _t in _ANNOTATION_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _COMPARE_LBL_H, [paragraph([run(_t, size=PT(16), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    # ── legend: frame + title + visual keys + captions ──
    # Keys have empty centered text bodies. Caption boxes are vertically centered,
    # no-wrap, and zero-inset with zero paragraph margins.
    out.append(text_box(n(), "Rectangle 1163", IN(5.51), IN(4.752), IN(2.104), IN(1.278), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color="121415", anchor="ctr"))   # 121415 near-black outline
    out.append(text_box(n(), "Rectangle 1164", IN(5.997), IN(4.665), IN(1.13), IN(0.175), [paragraph([run("Addressability", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))   # FFFFFF white
    for _y, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", _SWATCH_X, IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", _LEGEND_LBL_X, IN(_y), IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── scenario chip (top-right) ──
    out.append(text_box(n(), "Rectangle 123", IN(8.069), IN(0.174), IN(2.977), IN(0.217), [paragraph([run("(1) Status Quo Scenario", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=BLACK, anchor="ctr"))   # CEDDEC pale blue
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
