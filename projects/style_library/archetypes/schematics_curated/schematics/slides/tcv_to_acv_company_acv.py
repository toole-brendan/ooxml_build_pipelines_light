"""tcv_to_acv_company_acv — Navy market-sizing deck (20251120), source slide 19.

EXHIBIT — "TCV to ACV Approach · Finding Company ACV": how Company TCV converts to
Company ACV (annual contract value) via contract-exercise timing. Top band states
the formula — Company TCV × Contract exercise timing (%) = Company ACV by year.
Middle is a worked $-example (presumed Marauder timing) drawn as a styled bar
chart spanning Year 1 / Year 2, with $-value badges sitting on the bars. Bottom is
a native table of per-product exercise timing (Corsair / Mirage / Marauder ×
Initial / In-year / Next-year).

This module exercises all three "hard" converter paths at once: a data-over-
template styled_chart, a native table() reconstruction, and a flattened group.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ......... breadcrumb() + title_placeholder()
  • formula band ... Rectangle 13/15/16 + "+"/"=" glyphs (Company TCV × timing = ACV)
  • _AXIS_LABELS ... the column labels under the chart (SAM … Next-year exercise)
  • styled chart ... graphic_frame(rId2) → CHARTS[0] = styled_chart(...); the data
                     is the _CHART0_DATA literal, the look is the source template
  • $ badges ....... "Text Placeholder 25" boxes = the $ values on the bars
  • table .......... per-product exercise-timing table (low-level table/trow/tcell)
  • scope chip ..... "All archetypes" (top-right) + logo

styled_chart caveat: editing _CHART0_DATA re-renders the chart, but PowerPoint's
"Edit Data" pane still shows the source workbook until it is regenerated.

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=21, connector=9, chart=1, table=1, picture=1,
chrome_builders=2, clusters=1 (covering 6 shapes), frozen_fields=12,
dropped=1 (think-cell OLE frame).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, picture, line_break, table, trow, tcell, breadcrumb, title_placeholder,
)
from deck_core.charts import graphic_frame, styled_chart
from deck_core.style import IN, PT, BLACK, WHITE, DK, BLUE_4, BLUE_5, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
_CHART0_TPL = (_SRC / "slide19_chart3.xml").read_text(encoding="utf-8")
_XLSB0 = (_SRC / "slide19_chart3.xlsb").read_bytes()

# data-over-template: these values drive the chart render; the style is the template.
_CHART0_DATA = {
    "categories": None,
    "series": [
        {"values": [400, 200, 200, 190, 100, 100]},
        {"values": [None, 200, None, 10, 90, None]},
    ],
}

CHARTS = [styled_chart(_CHART0_TPL, _CHART0_DATA, _XLSB0)]
IMAGES = [
    {"rId": "rId3", "file": "image8_3071a231.jpeg"},
]


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_AXIS_Y, _AXIS_H = IN(5.002), IN(0.167)   # chart column-label row
_BOX_H = IN(0.359)        # formula-band box height                [shared x4]
_ARROW_W = IN(0.924)      # dashed connector arrow length          [shared x5]
_BADGE_W = IN(0.344)      # $-value badge width                    [shared x4]
_BADGE_H = IN(0.167)      # $-value badge height                   [shared x6]
_OP_W = IN(0.4)           # "+"/"=" operator-glyph size            [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_AXIS_LABELS = [    # (x, cx, label) x6 — column labels beneath the chart bars
    (1.378, 0.314, "SAM"),
    (3.193, 0.844, "Market Share"),
    (5.236, 0.922, "Company TCV"),
    (7.332, 0.891, "Initial exercise"),
    (9.358, 0.998, "In-year exercise"),
    (11.354, 1.168, "Next-year exercise"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome ──
    out.append(breadcrumb("Market Sizing", "Navy (Surface incl. MDA)"))
    out.append(title_placeholder("TCV to ACV Approach", "Finding Company ACV"))
    # ── approach-steps header (left) ──
    out.append(text_box(n(), "Rectangle 2", IN(0.425), IN(1.589), IN(2.289), IN(0.701), [paragraph([run("Multiply Company TCV by contract exercise timing to find Company ACV", size=PT(10), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 7", IN(0.425), IN(1.229), IN(2.291), _BOX_H, [paragraph([run("Approach steps", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Connector 8", IN(0.426), IN(1.586), IN(2.289), IN(0.002), color=DK, width=12700, flip_h=True))
    # ── formula band: Company ACV output box, then the dashed bar-to-bar arrows ──
    out.append(text_box(n(), "Rectangle 13", IN(11.46), IN(1.76), IN(1.519), IN(0.359), [paragraph([run("Company ACV by year ($)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(connector(n(), "Straight Connector 118", IN(2.113), IN(3.089), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 132", IN(4.194), IN(4.023), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 139", IN(6.274), IN(4.023), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 147", IN(8.354), IN(4.068), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))
    out.append(connector(n(), "Straight Connector 153", IN(10.436), IN(4.488), _ARROW_W, IN(0), color=DK, width=3175, dashed=True, arrow=True))
    # ── worked example: styled chart (data-over-template) + $ badges on the bars ──
    out.append(graphic_frame(sp_id=n(), name="Chart", x=IN(0.405), y=IN(2.998), cx=IN(12.663), cy=IN(2.047), rId="rId2"))
    out.append(text_box(n(), "Text Placeholder 25", IN(1.363), IN(3.938), _BADGE_W, _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("400", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    # ── chart column labels ──
    for _x, _cx, _t in _AXIS_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _AXIS_Y, IN(_cx), _AXIS_H, [paragraph([run(_t, size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    # ── more $ badges (interleaved with the formula-band boxes in paint order) ──
    out.append(text_box(n(), "Text Placeholder 25", IN(3.443), IN(3.472), _BADGE_W, _BADGE_H, [paragraph([run("$", size=PT(10), color=BLACK, font=FONT), run("200", size=PT(10), color=BLACK, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(5.524), IN(4.405), _BADGE_W, _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("200", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(7.642), IN(3.962), IN(0.267), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("10", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(9.722), IN(4.194), IN(0.267), _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("90", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    out.append(text_box(n(), "Text Placeholder 25", IN(11.766), IN(4.637), _BADGE_W, _BADGE_H, [paragraph([run("$", size=PT(10), color=WHITE, font=FONT), run("100", size=PT(10), color=WHITE, font=FONT)], align="ctr", mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=17463, t_ins=0, r_ins=17463, b_ins=0))
    # ── formula band (cont.): Company TCV × timing = ... ──
    out.append(text_box(n(), "Plus Sign 14", IN(6.575), IN(1.739), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathPlus", anchor="ctr", rot=2572505))
    out.append(text_box(n(), "Rectangle 15", IN(3.515), IN(1.76), IN(2.549), _BOX_H, [paragraph([run("Company TCV ($)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_4, line_color=BLACK, line_width=3175, anchor="ctr"))
    out.append(text_box(n(), "Equals 17", IN(10.548), IN(1.739), _OP_W, _OP_W, [paragraph([], align="ctr", line_spacing=100000)], fill=BLACK, line_color=BLACK, prst="mathEqual", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 242", IN(7.198), IN(3.083), IN(3.238), IN(0.512), [paragraph([run("Company ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$100M in Year 1", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 247", IN(9.167), IN(3.781), IN(3.479), IN(1.435), [paragraph([run("For Programs to deliver", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="808080", line_width=19050, dashed_line=True))
    out.append(text_box(n(), "Rectangle 248", IN(11.192), IN(3.083), IN(1.474), IN(0.512), [paragraph([run("Company ACV: ", size=PT(10), color=WHITE, font=FONT), line_break(), run("$100M in Year 2", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=BLUE_5, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 249", IN(0.495), IN(2.734), IN(12.339), IN(0.002), color="808080", width=12700))
    out.append(text_box(n(), "Rectangle 16", IN(7.456), IN(1.76), IN(2.548), _BOX_H, [paragraph([run("Contract exercise timing (%)", size=PT(10), color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=DK, line_color=DK, anchor="ctr"))
    out.append(text_box(n(), "TextBox 252", IN(6.427), IN(2.125), IN(4.607), IN(0.426), [paragraph([run("Defined as proportion of contract exercised each year ", size=PT(10), italic=True, color=BLACK, font=FONT), line_break(), run("(e.g., 50% in Year 1, 50% in Year 2 for Marauder) ", size=PT(10), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 254", IN(0.425), IN(2.377), IN(5.099), _BOX_H, [paragraph([run("Company ACV estimation example ($M, presumed Marauder exercise timing):", size=PT(10), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 301", IN(0.54), IN(2.885), IN(10.239), IN(0), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Rectangle 302", IN(5.078), IN(2.774), IN(1.162), IN(0.222), [paragraph([run("Year 1", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 304", IN(10.844), IN(2.885), IN(2.134), IN(0), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Rectangle 305", IN(11.47), IN(2.774), IN(0.92), IN(0.222), [paragraph([run("Year 2", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="none", anchor="ctr"))
    # ── per-product exercise-timing table (low-level table()/trow()/tcell(); merges via grid_span/row_span) ──
    out.append(table(n(), "Table 19", IN(0.495), IN(5.318), IN(12.482), IN(1.667), col_widths=[IN(0.851), IN(5.847), IN(1.812), IN(1.812), IN(2.16)], rows=[
        trow([tcell("Contract exercise timing by product:", size=PT(10), italic=True, color=DK, grid_span=2, anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"L": "none", "R": "none", "T": "none", "B": {"color": WHITE, "width": 12700}}), tcell("Year 1", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, grid_span=2, anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"L": "none", "R": {"color": WHITE, "width": 12700}, "T": "none", "B": {"color": DK, "width": 12700}}), tcell("Year 2", size=PT(10), bold=True, color=WHITE, align="ctr", fill=BLUE_5, anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"L": {"color": WHITE, "width": 12700}, "R": "none", "T": "none", "B": {"color": DK, "width": 12700}})], h=IN(0)),
        trow([tcell("Product", size=PT(10), bold=True, color=BLACK, anchor="b", borders={"T": {"color": WHITE, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("Rationale", size=PT(10), bold=True, color=BLACK, anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": WHITE, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("Initial exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("In-Year exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}}), tcell("Next-year exercise", size=PT(10), bold=True, color=BLACK, align="ctr", anchor="b", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 12700}})], h=IN(0)),
        trow([tcell("Corsair", size=PT(10), bold=True, color=BLACK, l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 6350}}), tcell("In line with Production OT", size=PT(10), color=BLACK, l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 6350}}), tcell("50%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 6350}}), tcell("35%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 6350}}), tcell("15%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 12700}, "B": {"color": DK, "width": 6350}})], h=IN(0)),
        trow([tcell("Mirage", size=PT(10), bold=True, color=BLACK, l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": DK, "width": 6350}}), tcell("Assumes similar timing as Corsair Production OT because Mirage falls under sUSV funding", size=PT(10), color=BLACK, l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": DK, "width": 6350}}), tcell("50%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": DK, "width": 6350}}), tcell("35%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": DK, "width": 6350}}), tcell("15%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": DK, "width": 6350}})], h=IN(0)),
        trow([tcell("Marauder", size=PT(10), bold=True, color=BLACK, l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": WHITE, "width": 12700}}), tcell("Based on estimated MASC contract exercise: MASC procured in 10-vessel block buys with each vessel a separate CLIN and CLINs are exercised evenly across 24-month period", size=PT(10), color=BLACK, l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": WHITE, "width": 12700}}), tcell("5%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": WHITE, "width": 12700}}), tcell("45%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": WHITE, "width": 12700}}), tcell("50%", size=PT(10), italic=True, color=BLACK, align="ctr", l_ins=60960, r_ins=60960, t_ins=60960, b_ins=60960, borders={"T": {"color": DK, "width": 6350}, "B": {"color": WHITE, "width": 12700}})], h=IN(0)),
    ]))
    # ── scope chip (top-right) + logo ──
    out.append(text_box(n(), "Rectangle 4", IN(9.353), IN(0.137), IN(2.2), IN(0.375), [paragraph([run("All archetypes", size=PT(10), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=DK, line_width=3175, anchor="ctr"))
    out.append(picture(n(), "Picture 2", "rId3", IN(12.373), IN(0.048), IN(0.922), IN(0.922)))
    return "".join(out)


def render() -> str:
    return slide(_body())
