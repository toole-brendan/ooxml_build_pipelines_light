"""archetype_comps_newbuild_prices — Commercial Strategy Market Analysis deck (20260325), source slide 32.

EXHIBIT — "Archetype Comps (1/3)": the first of three archetype-comparison slides,
making the point that despite improvement from rising new-build prices and
increased orders, shipbuilders only reached low-to-mid-single-digit EBIT margins
by '24. The exhibit is a styled line chart of EBIT Margin (%) over 2020–2024
(year labels run along the bottom; a rotated "EBIT Margin (%)" y-axis title sits
top-left). A bottom-right legend keys five value-chain archetypes to coloured
markers — Shipbuilders (C30C3E) · Owner/Operator Carrier (364D6E) · Charter
Companies (27AE60) · Terminal Operators Integrated (6F8DB9) · Terminal Operators
Standalone (a pct50-hatched marker) — plus a "$10B (Revenue)" bubble key. A
single Source/Note footnote (company filings, with the per-archetype constituents)
closes it out.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............... breadcrumb() + title_placeholder() + prelim_chip()
  • styled chart ........ graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                          data is _CHART0_DATA (all series empty — see Residue),
                          the look is the source chart template
  • _CATEGORY_TICK_LABELS ......... category-axis year labels under the chart (2020 … 2024) → loop
  • y-axis title ........ "Text Placeholder 25" = the "EBIT Margin (%)" caption
  • _LEGEND_KEYS ..... 4 coloured ellipse keys + the larger "$10B (Revenue)"
                          bubble outline (fill=None) → loop (heterogeneous: it
                          groups the ellipse markers by shared prst, not meaning)
  • hatched marker ...... "Oval 2027" = the pct50 pattern-fill legend chip for
                          Terminal Operators (Standalone), standalone (its own
                          pattern_fill arg keeps it out of the loop)
  • _LEGEND_LABELS ...... legend captions for the five archetypes + "$10B
                          (Revenue)" key → loop
  • footnote ............ "Rectangle 2116" = Source/Note line (kept verbatim)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=3, chart=1, chrome_builders=3, clusters=3 (covering
16 shapes), frozen_fields=5, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim; the
styled_chart's _CHART0_DATA series are all empty (the source chart carries its
own cached values via the bundled template + .xlsb).
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, DK, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide32_chart17.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide32_chart17.xlsb").read_bytes()

_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": []},
        {"values": []},
        {"values": []},
        {"values": []},
        {"values": []},
        {"values": []},
        {"values": []},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.736), IN(0.306), IN(0.167)   # x-axis year-label row box [shared x5]
_LEGEND_LBL_H = IN(0.167)                                     # legend caption height     [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the five year ticks beneath the chart's category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x5 — category-axis year labels under the chart
    (2.674, "2020"),
    (4.672, "2021"),
    (6.672, "2022"),
    (8.672, "2023"),
    (10.67, "2024"),
]

# local_meaning: the legend marks: four coloured archetype ellipse chips plus the hollow '$10B
#   (Revenue)' bubble outline (fill=None).
_LEGEND_KEYS = [    # (x, y, cx, cy, fill) x5 — 4 coloured ellipse chips + the "$10B (Revenue)" bubble outline (fill=None)
    (10.373, 5.583, 0.146, 0.146, "C30C3E"),   # C30C3E crimson
    (10.373, 5.806, 0.146, 0.146, "364D6E"),   # 364D6E dark blue
    (10.373, 6.028, 0.146, 0.146, "27AE60"),   # 27AE60 green
    (10.373, 6.25, 0.146, 0.146, "6F8DB9"),   # 6F8DB9 blue
    (10.283, 5.139, 0.326, 0.326, None),   # 162029 dark navy outline
]

# local_meaning: the six legend captions: the four archetype names plus the '$10B (Revenue)'
#   bubble key.
_LEGEND_LABELS = [    # (x, y, cx, label) x6 — archetype captions + "$10B (Revenue)" key
    (10.601, 5.578, 0.76, "Shipbuilders"),
    (10.601, 5.8, 2.139, "Owner/Operator (Carrier Segment)"),
    (10.601, 6.023, 1.2, "Charter Companies"),
    (10.601, 6.245, 1.944, "Terminal Operators (Integrated)"),
    (10.601, 6.467, 2.021, "Terminal Operators (Standalone)"),
    (10.667, 5.224, 1.005, "$10B (Revenue)"),
]

# ── text layout commentary ──
# text_box(): l_ins/t_ins/r_ins/b_ins are internal padding and anchor is vertical
# alignment. paragraph(..., align=...) is horizontal alignment; mar_l/indent are
# paragraph margins or hanging indents. Omitted values intentionally retain the
# primitive defaults, so layout behavior stays visible at each call site.

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Commercial Maritime Value Chain", "Performance"))
    out.append(title_placeholder("Archetype Comps (1/3)", "Despite seeing improvement from rising new build prices and increased orders, shipbuilders only achieved low-to-mid-single digit EBIT margins by ‘24."))
    # ── styled chart (data-over-template), bundled verbatim + .xlsb ("Edit Data" works) ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.373), y=IN(1.696), cx=IN(12.54), cy=IN(5.2), rId="rId2"))
    # ── category-axis year labels (under the chart) ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── y-axis title ──
    out.append(text_box(n(), "Text Placeholder 25", IN(0.533), IN(1.505), IN(1.064), IN(0.167), [paragraph([run("EBIT Margin (%)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── legend markers — 4 coloured ellipse chips + the "$10B (Revenue)" bubble outline ──
    for _x, _y, _cx, _cy, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=DK, line_width=3175, prst="ellipse", anchor="ctr"))
    # hatched legend marker — Terminal Operators (Standalone), pct50 pattern fill (standalone, not in the loop)
    out.append(text_box(n(), "Oval 2027", IN(10.373), IN(6.472), IN(0.146), IN(0.146), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=DK, pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"}, line_width=3175, prst="ellipse", anchor="ctr"))   # 162029 dark navy outline
    # ── legend captions (archetypes + "$10B (Revenue)" key) ──
    for _x, _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # footnote — kept verbatim (sits off the house Source position)
    out.append(text_box(n(), "Rectangle 2116", IN(0.495), IN(7.081), IN(5.102), IN(0.349), [paragraph([run("Source: Company filings |   ", size=PT(7), color=BLACK, font=FONT), run("Shipbuilders:", size=PT(7), bold=True, color="C30C3E", font=FONT), run(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. ", size=PT(7), color=BLACK, font=FONT), run("Owner/Operator", size=PT(7), bold=True, color="364D6E", font=FONT), run(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. ", size=PT(7), color=BLACK, font=FONT), run("Charter Companies", size=PT(7), bold=True, color="27AE60", font=FONT), run(": Danaos, Costamare, Seaspan. ", size=PT(7), color=BLACK, font=FONT), run("Terminal Operators (Integrated)", size=PT(7), bold=True, color="6F8DB9", font=FONT), run(": Maersk Terminals.         ", size=PT(7), color=BLACK, font=FONT), run("Terminal Operators (Standalone)", size=PT(7), bold=True, color="8A8F93", font=FONT), run(": Hutchison Ports, ICTS. Note: Segment margins not burdened by corporate", size=PT(7), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
