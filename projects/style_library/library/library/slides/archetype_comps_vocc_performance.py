"""archetype_comps_vocc_performance — Commercial Strategy Market Analysis deck (20260325), source slide 33.

EXHIBIT — "Archetype Comps (2/3)": VOCC (commercial maritime) performance for
2020-2024, used to compare margin behaviour across the value-chain archetypes.
The left two-thirds is a styled EBIT-margin (%) chart with year ticks 2020-2024
on the x-axis and an "EBIT Margin (%)" y-axis title; a bubble keyed "$10B
(Revenue)" sets bubble scale. Below the plot, a legend keys five archetypes by
colour — Shipbuilders (red) · Owner/Operator · Charter Companies · Terminal
Operators (Integrated) · Terminal Operators (Standalone, hatched). The right
rail is a "Revenue and EBIT margin drivers" panel: per-archetype ’21-’22 vs.
’23-’24 commentary (freight rates spiked post-COVID, then normalized; charter
earnings stayed propped up by leases locked in ’21-’22). A footnote lists the
constituent companies behind each archetype.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder() + prelim_chip()
  • styled chart ...... graphic_frame(rId2) → CHARTS[0] = styled_chart(...);
                        bundled verbatim with its .xlsb ("Edit Data" works)
  • _CATEGORY_TICK_LABELS ....... x-axis year tick labels 2020-2024 (loop)
  • y-axis title ...... standalone "EBIT Margin (%)" box (interleaves)
  • _LEGEND_KEYS .. 4 archetype colour-chip ellipses + the $10B-revenue ring
                        (one ellipse style; loop). The 5th Standalone chip is a
                        standalone pct50-hatched "Oval 2027" that interleaves
  • _LEGEND_LABELS .... legend captions — 5 archetype names + "$10B (Revenue)"
  • narrative rail .... "Rectangle 2220" margin-driver commentary block, titled
                        by the single-cell native table() "Table 2221"
  • footnote .......... "Rectangle 4" Source/Note line (kept verbatim)

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated. (Here
_CHART0_DATA holds seven empty series, so the chart renders straight from the
bundled template + .xlsb.)

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=4, chart=1, table=1, chrome_builders=3,
clusters=3 (covering 16 shapes), frozen_fields=5, dropped=1 (think-cell OLE frame).
Residue: the Note/Source line sits off the house position, kept verbatim.
"""
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide33_chart18.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide33_chart18.xlsb").read_bytes()

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


# ── table kit (local): separates a rich cell's CONTENT from its MECHANICS (insets,
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
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_W, _AXIS_H = IN(6.736), IN(0.306), IN(0.167)   # year-axis label row [shared x5]
_LEGEND_LBL_H = IN(0.167)   # legend caption height                                  [shared x6]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the five year ticks along the chart's category axis.
_CATEGORY_TICK_LABELS = [    # (x, label) x5 — category tick labels along the chart's x-axis
    (2.13, "2020"),
    (3.589, "2021"),
    (5.045, "2022"),
    (6.502, "2023"),
    (7.96, "2024"),
]

# heterogeneous by meaning, homogeneous by visual: 4 archetype colour chips share
# one ellipse style with the 5th entry, the (fill-less) "$10B (Revenue)" bubble ring.
# local_meaning: the legend marks: the archetype ellipse chips plus the revenue-bubble ring.
_LEGEND_KEYS = [    # (x, y, cx, cy, fill) x5 — legend ellipse chips (+ revenue ring)
    (7.148, 5.583, 0.146, 0.146, "C30C3E"),   # C30C3E crimson — Shipbuilders
    (7.148, 5.806, 0.146, 0.146, "364D6E"),   # 364D6E dark blue — Owner/Operator
    (7.148, 6.028, 0.146, 0.146, "27AE60"),   # 27AE60 green — Charter Companies
    (7.148, 6.25, 0.146, 0.146, "6F8DB9"),    # 6F8DB9 blue — Terminal Operators (Integrated)
    (7.066, 5.139, 0.326, 0.326, None),       # 162029 dark navy outline — "$10B (Revenue)" bubble ring
]

# local_meaning: the six legend captions: archetype names plus the revenue-bubble caption.
_LEGEND_LABELS = [    # (x, y, cx, label) x6 — legend captions (+ the revenue-bubble caption)
    (7.375, 5.578, 0.76, "Shipbuilders"),
    (7.375, 5.8, 2.139, "Owner/Operator (Carrier Segment)"),
    (7.375, 6.023, 1.2, "Charter Companies"),
    (7.375, 6.245, 1.944, "Terminal Operators (Integrated)"),
    (7.375, 6.467, 2.021, "Terminal Operators (Standalone)"),
    (7.45, 5.224, 1.005, "$10B (Revenue)"),
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
    # ── chrome ──
    out.append(breadcrumb("Commercial Maritime Value Chain", "Performance"))
    out.append(title_placeholder("Archetype Comps (2/3)", "VOCC performance ’21-’22 driven by historically high freight rates; charter companies benefitted through ’24 from leases locked in ’21-’22."))
    # ── styled chart, bundled verbatim + .xlsb ("Edit Data" works) → CHARTS[0] ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.373), y=IN(1.696), cx=IN(9.286), cy=IN(5.2), rId="rId2"))
    # ── x-axis year ticks + y-axis title ("EBIT Margin (%)") ──
    for _x, _t in _CATEGORY_TICK_LABELS:
        out.append(text_box(n(), "YearLabel", IN(_x), _AXIS_Y, _AXIS_W, _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    out.append(text_box(n(), "Text Placeholder 25", IN(0.533), IN(1.505), IN(1.064), IN(0.167), [paragraph([run("EBIT Margin (%)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── legend — 4 archetype colour chips + the standalone $10B-revenue ring (loop) ──
    for _x, _y, _cx, _cy, _fill in _LEGEND_KEYS:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color=DK, line_width=3175, prst="ellipse", anchor="ctr"))
    # standalone hatched chip — Terminal Operators (Standalone), pct50 pattern fill
    out.append(text_box(n(), "Oval 2027", IN(7.148), IN(6.472), IN(0.146), IN(0.146), [paragraph([], align="ctr", line_spacing=100000)], fill=None, line_color=DK, pattern_fill={"prst": "pct50", "fg": "scheme:tx1", "bg": "scheme:bg1"}, line_width=3175, prst="ellipse", anchor="ctr"))   # 162029 dark navy outline
    # ── legend captions — 5 archetype names + the "$10B (Revenue)" caption (loop) ──
    for _x, _y, _cx, _t in _LEGEND_LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LEGEND_LBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))   # 000000 black
    # ── right-rail narrative — per-archetype ’21-’22 / ’23-’24 margin-driver commentary ──
    out.append(text_box(n(), "Rectangle 2220", IN(9.66), IN(1.866), IN(3.136), IN(4.87), [paragraph([run("Shipbuilders ", size=PT(10), bold=True, color=BLACK, font=FONT), run("(relating to Commercial market)", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("’21-’22:", size=PT(10), bold=True, color=BLACK, font=FONT), run(" While orders recovered from ’20, earnings remained pressured by input materials and labor cost growth.", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("’23-’24:", size=PT(10), bold=True, color=BLACK, font=FONT), run(" Improvement driven by performance against orderbook contracts and rising new build prices", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Owner/Operators", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("’21-’22: ", size=PT(10), bold=True, color=BLACK, font=FONT), run("Freight rates reached historic highs driven by post-COVID pent-up demand and shift toward goods consumption, while port congestion and operational disruptions constrained effective vessel supply amid below-trend capacity additions.", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("’23-’24:", size=PT(10), bold=True, color=BLACK, font=FONT), run(" Freight rates normalized as consumer demand softened under inflationary pressure, coinciding with acceleration in new vessel deliveries that expanded global fleet capacity.", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Charter Companies", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("’21-’22:", size=PT(10), bold=True, color=BLACK, font=FONT), run(" Charter rates surged alongside freight rates as operators sought to secure tonnage in supply-constrained market.", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("’23-’24:", size=PT(10), bold=True, color=BLACK, font=FONT), run(" Earnings remained supported by multi-year charter contracts signed at peak market conditions ’21-’22, partially insulating results from lower charter rates.", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True), paragraph([run("Terminal Operators", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000), paragraph([run("Relatively more stable margins given ability to pass on costs to operators.", size=PT(10), color=BLACK, font=FONT)], mar_l=171450, indent=-171450, line_spacing=100000, bullet=True)], fill=None, line_color="none"))   # 000000 black
    # ── narrative header band — single-cell native table titling the right rail ──
    # (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    # palette — text: 000000 black (title); rules: FFFFFF white (top) · 000000 black (bottom); cell fills: none.
    out.append(table(n(), "Table 2221", IN(9.66), IN(1.563), IN(3.135), IN(0.3), col_widths=[IN(3.135)], rows=[
        trow([
            rcell([tpara([trun("Revenue and EBIT margin drivers", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0)], l_ins=41564, r_ins=41564, T=edge(WHITE), B=edge(BLACK)),
        ], h=IN(0.3)),
    ]))
    # ── footnote — Source/Note line, kept verbatim (sits off the house Source position) ──
    out.append(text_box(n(), "Rectangle 4", IN(0.495), IN(7.081), IN(5.102), IN(0.349), [paragraph([run("Source: Company filings |   ", size=PT(7), color=BLACK, font=FONT), run("Shipbuilders:", size=PT(7), bold=True, color="C30C3E", font=FONT), run(" Austal, Hanwha Ocea, Fincantieri, HD Hyundai KSOE, Samsung Heavy. ", size=PT(7), color=BLACK, font=FONT), run("Owner/Operator", size=PT(7), bold=True, color="364D6E", font=FONT), run(": Matson OT segment, ZIM, Hapag Lloyd, Maersk Ocean segment. ", size=PT(7), color=BLACK, font=FONT), run("Charter Companies", size=PT(7), bold=True, color="27AE60", font=FONT), run(": Danaos, ", size=PT(7), color=BLACK, font=FONT), run("Costamare", size=PT(7), color=BLACK, font=FONT), run(", Seaspan. ", size=PT(7), color=BLACK, font=FONT), run("Terminal Operators (Integrated)", size=PT(7), bold=True, color="6F8DB9", font=FONT), run(": Maersk Terminals.         ", size=PT(7), color=BLACK, font=FONT), run("Terminal Operators (Standalone)", size=PT(7), bold=True, color="8A8F93", font=FONT), run(": Hutchison Ports, ICTS. Note: Segment margins not burdened by corporate", size=PT(7), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── chrome (cont.) ──
    out.append(prelim_chip())
    return "".join(out)


def render() -> str:
    return slide(_body())
