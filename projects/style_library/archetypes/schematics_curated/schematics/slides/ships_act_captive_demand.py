"""ships_act_captive_demand — Commercial Strategy market-analysis deck (20260325), source slide 60.

EXHIBIT — "SHIPS Act Captive Demand": the Maritime Security Trust Fund (MSTF) can
support ~100 more vessels (~200 total) than the SHIPS Act's legally-mandated
demand. Left: a styled stacked-bar chart comparing the MSTF-supported Strategic
Commercial Fleet vs. legally-mandated demand by vessel type (Container, LNG,
Crude / Product Tanker, Bulk, Ro-Ro, Other). Right: a mandate table mapping each
SHIPS Act provision (bill section) to its vessel type, cargo-% ramp, and US-built /
US-flagged requirement. A "(2) SHIPS Act Scenario" tag and an Opex/D&A-differential
caveat box annotate.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............. title_placeholder() + breadcrumb() + prelim_chip()
  • styled chart ....... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the
                         data (7 vessel-type series × 2 bars) is _CHART0_DATA
  • table ............. SHIPS Act provision → mandate table (low-level table())
  • _BAR_VALUE_MARKERS . small "1" value labels on thin bar segments
  • _LEGEND_SWATCHES ... vessel-type colour chips;  _VESSEL_LABELS = their names
  • connectors ........ dashed leader lines from labels to bar segments
  • _pattern_swatch ... inline primitive for the ltDnDiag legend swatch — a
                        pattern fill base text_box can't express (helper below)
  • annotations ....... scenario tag, caveat box, "Port Alpha production modeled"

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=12, connector=5, chart=1, table=1, chrome_builders=3,
clusters=3 (covering 16 shapes), raw_verbatim=1 (the pattern-fill swatch, lifted
into the inline _pattern_swatch helper below), dropped=1 (think-cell OLE frame),
frozen_fields=14.
Residue: the Note/Source line sits off the house position, kept verbatim.
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


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_MARK_W, _MARK_H = IN(0.115), IN(0.167)        # on-bar value-marker size
_SWATCH_W, _SWATCH_H = IN(0.196), IN(0.146)    # legend colour-chip size
_VLBL_X, _VLBL_H = IN(4.139), IN(0.167)        # vessel-label column x / height
_TXT_H = IN(0.167)        # chart-title / axis-label height        [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_BAR_VALUE_MARKERS = [    # (x, y, fill) x3 — small "1" markers on thin bar segments
    (2.309, 2.21, "4C6C9C"),
    (4.583, 3.997, BLACK),
    (3.951, 4.016, "4C6C9C"),
]

_LEGEND_SWATCHES = [    # (x, y, fill) x6 — vessel-type colour chips
    (3.887, 2.149, "969696"),
    (3.887, 2.372, BLACK),
    (3.887, 2.594, "4C6C9C"),
    (3.887, 2.816, "1D4D68"),
    (3.887, 3.038, "C0C0C0"),
    (3.887, 3.26, "007770"),
]

_VESSEL_LABELS = [    # (y, cx, label) x7 — vessel-type legend names
    (1.922, 0.345, "Other"),
    (2.144, 0.401, "Ro-Ro"),
    (2.366, 0.269, "Bulk"),
    (2.589, 0.944, "Product Tanker"),
    (2.811, 0.845, "Crude Tanker"),
    (3.033, 0.285, "LNG"),
    (3.255, 0.599, "Container"),
]

def _pattern_swatch(sp_id, name, x, y, cx, cy, *, prst, fg="tx1", bg="bg1"):
    """Inline primitive: a rect with a *pattern* fill (deck_core.text_box has no
    pattern_fill= option). Returns the same <p:sp> the converter dumped as RAW,
    reproduced byte-for-byte from params. Raw EMU coords + an explicit id (the raw
    shape used id 2000, outside the n() range) keep the render unchanged."""
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{sp_id}" name="{name}" /><p:cNvSpPr /><p:nvPr /></p:nvSpPr>'
        f'<p:spPr bwMode="auto"><a:xfrm><a:off x="{x}" y="{y}" /><a:ext cx="{cx}" cy="{cy}" /></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst /></a:prstGeom>'
        f'<a:pattFill prst="{prst}"><a:fgClr><a:schemeClr val="{fg}" /></a:fgClr><a:bgClr><a:schemeClr val="{bg}" /></a:bgClr></a:pattFill>'
        f'<a:ln w="19050" cap="flat" cmpd="sng" algn="ctr"><a:noFill /><a:prstDash val="solid" /><a:miter lim="800000" /><a:headEnd type="none" w="med" len="med" /><a:tailEnd type="none" w="med" len="med" /></a:ln>'
        f'<a:effectLst /></p:spPr>'
        f'<p:style><a:lnRef idx="2"><a:schemeClr val="accent1"><a:shade val="15000" /></a:schemeClr></a:lnRef><a:fillRef idx="1"><a:schemeClr val="accent1" /></a:fillRef><a:effectRef idx="0"><a:schemeClr val="accent1" /></a:effectRef><a:fontRef idx="minor"><a:schemeClr val="lt1" /></a:fontRef></p:style>'
        f'<p:txBody><a:bodyPr rtlCol="0" anchor="ctr" /><a:lstStyle /><a:p><a:pPr algn="ctr" /><a:endParaRPr lang="en-US" /></a:p></p:txBody>'
        f'</p:sp>'
    )


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome (title precedes the Note line + breadcrumb in paint order) ──
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
    # ── styled chart (data-over-template) → CHARTS[0] ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.429), y=IN(1.62), cx=IN(5.123), cy=IN(4.674), rId="rId2"))
    out.append(connector(n(), "Straight Connector 74", IN(2.599), IN(2.274), IN(0.101), IN(0.069), color=BREADCRUMB, width=6350, dashed=True, arrow=True, flip_h=True, flip_v=True))
    out.append(connector(n(), "Straight Connector 75", IN(2.599), IN(2.177), IN(0.101), IN(0.069), color=BREADCRUMB, width=6350, dashed=True, arrow=True, flip_h=True))
    out.append(text_box(n(), "Text Placeholder 25", IN(0.542), IN(1.505), IN(4.384), _TXT_H, [paragraph([run("SCF Supported by MSTF vs. Legally Mandated Demand (# vessels)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    # ── on-bar value markers ──
    for _x, _y, _fill in _BAR_VALUE_MARKERS:
        out.append(text_box(n(), "ValueLabel", IN(_x), IN(_y), _MARK_W, _MARK_H, [paragraph([run("1", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.215), IN(6.094), IN(1.667), IN(0.333), [paragraph([run("Strategic Commercial Fleet (supported by MSTF)", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(3.493), IN(6.094), IN(1.663), _TXT_H, [paragraph([run("Legally Mandated Demand", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.915), IN(2.033), IN(0.267), _TXT_H, [paragraph([run("201", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(4.191), IN(3.83), IN(0.267), _TXT_H, [paragraph([run("104", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    # pattern-fill legend swatch — inline primitive (text_box has no pattern_fill=)
    out.append(_pattern_swatch(2000, "Rectangle 109", 3554413, 1762125, 179388, 133350, prst="ltDnDiag"))
    # ── legend: vessel-type colour chips + names ──
    for _x, _y, _fill in _LEGEND_SWATCHES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), IN(_y), _SWATCH_W, _SWATCH_H, [paragraph([], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    for _y, _cx, _t in _VESSEL_LABELS:
        out.append(text_box(n(), "Label", _VLBL_X, IN(_y), IN(_cx), _VLBL_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
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
