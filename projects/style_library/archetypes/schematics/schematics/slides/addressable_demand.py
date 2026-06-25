"""addressable_demand - Commercial Strategy deck, source slide 41.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=4, connector=0, chart=0, table=6, picture=0, chrome_builders=2, clusters=2 (covering 12 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_LBL_W, _LBL_H = IN(2.2), IN(0.5)
_LBL2_X, _LBL2_H = IN(4.158), IN(0.5)
_H1 = IN(0.5)   # shared x4

# ── repeated-shape data tables (each drives a loop in _body) ──
_LABELS = [    # (x, y, fill, label) x6
    (1.792, 1.746, BLACK, "US-Built"),
    (1.793, 2.423, BLACK, "US-Flagged"),
    (1.793, 3.1, "007770", "Commercially Viable"),
    (1.793, 3.777, "007770", "Oceangoing"),
    (1.793, 5.131, "969696", "Great Lakes Commercial Vessels"),
    (1.793, 6.485, "969696", "Other Categories"),
]

_LABELS2 = [    # (y, cx, label) x6
    (1.746, 8.677, "Provides Jones Act protection or enables subsidy eligibility under pending legislation and potential expansion of other programs; required for certain export/import provisions"),
    (3.773, 8.677, "Drives national shipbuilding capacity with avg. gross tonnage 15x+ that of offshore vessels"),
    (3.097, 8.677, "Meets capabilities and tonnage required for participation in subsidized programs; priced to achieve revenue targets"),
    (5.799, 8.677, "Small fleet size precludes serial production; low gross tonnage per vessel limits national security utility and pricing"),
    (5.123, 8.677, "Unlikely to drive meaningful demand given small fleet size (~37 vessels) and low retirement rates"),
    (4.448, 8.677, "Large fleet size enables serial production (5+ hulls/yr to achieve max labor efficiencies); viable if owner/operators conduct 1-for-1 replacement of expected retirements"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("Addressable Demand", "US-built and flagged oceangoing commercial vessels and high-volume offshore vessels meet desired regulatory and/or serial production requirements."))
    for _x, _y, _fill, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _LBL_W, _LBL_H, [paragraph([run(_t, size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill=_fill, line_color="none", anchor="ctr"))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 20", IN(0.361), IN(3.097), IN(1.264), IN(1.175), col_widths=[IN(1.264)], rows=[
        trow([tcell_rich([tpara([trun("Addressable", size=PT(12), color="007770", font=FONT)]), tpara([trun("Commercial", size=PT(12), color="007770", font=FONT)])], borders={"R": {"color": "007770", "width": 38100}, "T": "none", "B": "none"})], h=IN(1.175)),
    ]))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 24", IN(0.362), IN(5.131), IN(1.263), IN(1.854), col_widths=[IN(1.263)], rows=[
        trow([tcell("Non-Addressable", size=PT(12), color="969696", borders={"R": {"color": "969696", "width": 38100}, "T": "none", "B": "none"})], h=IN(1.854)),
    ]))
    for _y, _cx, _t in _LABELS2:
        out.append(text_box(n(), "Label", _LBL2_X, IN(_y), IN(_cx), _LBL2_H, [paragraph([run(_t, size=PT(14), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 36", IN(1.793), IN(5.808), IN(2.2), _H1, [paragraph([run("Low Volume Offshore ", size=PT(12), bold=True, color=WHITE, font=FONT), line_break(), run("(ex-PSV and FSV)", size=PT(12), italic=True, color=WHITE, font=FONT), run(" ", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill="969696", line_color="none", anchor="ctr"))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 49", IN(1.792), IN(1.375), IN(2.2), IN(0.3), col_widths=[IN(2.2)], rows=[
        trow([tcell("Criteria", size=PT(12), color=BLACK, borders={"R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0)),
    ]))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 50", IN(4.158), IN(1.375), IN(8.677), IN(0.3), col_widths=[IN(8.677)], rows=[
        trow([tcell("Inclusion / Exclusion Rationale", size=PT(12), color=BLACK, borders={"R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0)),
    ]))
    out.append(text_box(n(), "Rectangle 54", IN(4.158), IN(2.422), IN(8.677), _H1, [paragraph([run("Same as above", size=PT(14), italic=True, color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 23", IN(1.793), IN(4.454), IN(2.2), _H1, [paragraph([run("High Volume Offshore", size=PT(12), bold=True, color=BLACK, font=FONT), line_break(), run("(PSV and FSV)", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr")], fill="FFC000", line_color="none", anchor="ctr"))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 31", IN(0.362), IN(4.454), IN(1.263), IN(0.5), col_widths=[IN(1.263)], rows=[
        trow([tcell("Addressable Offshore", size=PT(12), color="FFC000", borders={"R": {"color": "FFC000", "width": 38100}, "T": "none", "B": "none"})], h=IN(0.5)),
    ]))
    out.append(text_box(n(), "TextBox 33", IN(4.158), IN(6.485), IN(8.677), _H1, [paragraph([run("Same as above", size=PT(14), italic=True, color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Table 39", IN(0.361), IN(1.746), IN(1.264), IN(1.175), col_widths=[IN(1.264)], rows=[
        trow([tcell("Table Stakes", size=PT(12), color=BLACK, borders={"R": {"color": BLACK, "width": 38100}, "T": "none", "B": "none"})], h=IN(1.175)),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
