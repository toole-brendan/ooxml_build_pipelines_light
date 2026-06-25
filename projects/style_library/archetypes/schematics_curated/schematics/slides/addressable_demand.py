"""addressable_demand — Commercial Strategy market-analysis deck (20260325), source slide 41.

EXHIBIT — "Addressable Demand": US-built and flagged oceangoing commercial vessels
and high-volume offshore vessels meet the desired regulatory and/or serial-
production requirements. A criteria × rationale definitional table — a left
"Criteria" column of stacked, colour-coded tier boxes (Table Stakes: US-Built /
US-Flagged · Addressable Commercial: Commercially Viable / Oceangoing · Addressable
Offshore: High- / Low-Volume · Non-Addressable: Great Lakes / Other) set against a
right "Inclusion / Exclusion Rationale" column of explanatory text.

A pure table-and-box archetype: no chart, no connectors — just low-level table()
row/header labels, the criteria boxes, and the rationale text.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder()
  • _CRITERIA_BOXES ... the stacked criteria boxes, fill = addressability
                        (BLACK table-stakes · 007770 addressable · 969696 non-)
  • _RATIONALE_TEXT ... the right-column inclusion/exclusion rationale paragraphs
  • tables ........... 6 single-cell row-label tables — the column headers
                        (Criteria / Inclusion-Exclusion Rationale) and the tier
                        spine labels (Table Stakes / Addressable Commercial /
                        Addressable Offshore / Non-Addressable)
  • standalone boxes . High- / Low-Volume Offshore boxes + "Same as above" cells

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=4, table=6, chrome_builders=2, clusters=2 (covering 12
shapes), dropped=1 (think-cell OLE frame).
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


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_CRIT_W, _CRIT_H = IN(2.2), IN(0.5)        # criteria-box geometry
_RATIONALE_X, _RATIONALE_H = IN(4.158), IN(0.5)   # rationale-text column x / height
_ROW_H = IN(0.5)          # tier-row box height                   [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
_CRITERIA_BOXES = [    # (x, y, fill, label) x6 — stacked criteria boxes, fill = addressability
    (1.792, 1.746, BLACK, "US-Built"),
    (1.793, 2.423, BLACK, "US-Flagged"),
    (1.793, 3.1, "007770", "Commercially Viable"),
    (1.793, 3.777, "007770", "Oceangoing"),
    (1.793, 5.131, "969696", "Great Lakes Commercial Vessels"),
    (1.793, 6.485, "969696", "Other Categories"),
]

_RATIONALE_TEXT = [    # (y, cx, label) x6 — right-column inclusion/exclusion rationale
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
    # ── chrome ──
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("Addressable Demand", "US-built and flagged oceangoing commercial vessels and high-volume offshore vessels meet desired regulatory and/or serial production requirements."))
    # ── criteria boxes (colour = addressability) ──
    for _x, _y, _fill, _t in _CRITERIA_BOXES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _CRIT_W, _CRIT_H, [paragraph([run(_t, size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill=_fill, line_color="none", anchor="ctr"))
    # ── tier spine labels + column headers (low-level row-label tables) ──
    out.append(table(n(), "Table 20", IN(0.361), IN(3.097), IN(1.264), IN(1.175), col_widths=[IN(1.264)], rows=[
        trow([tcell_rich([tpara([trun("Addressable", size=PT(12), color="007770", font=FONT)]), tpara([trun("Commercial", size=PT(12), color="007770", font=FONT)])], borders={"R": {"color": "007770", "width": 38100}, "T": "none", "B": "none"})], h=IN(1.175)),
    ]))
    out.append(table(n(), "Table 24", IN(0.362), IN(5.131), IN(1.263), IN(1.854), col_widths=[IN(1.263)], rows=[
        trow([tcell("Non-Addressable", size=PT(12), color="969696", borders={"R": {"color": "969696", "width": 38100}, "T": "none", "B": "none"})], h=IN(1.854)),
    ]))
    # ── right-column rationale text ──
    for _y, _cx, _t in _RATIONALE_TEXT:
        out.append(text_box(n(), "Label", _RATIONALE_X, IN(_y), IN(_cx), _RATIONALE_H, [paragraph([run(_t, size=PT(14), color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    # ── offshore tier boxes + "Same as above" rationale cells ──
    out.append(text_box(n(), "Rectangle 36", IN(1.793), IN(5.808), IN(2.2), _ROW_H, [paragraph([run("Low Volume Offshore ", size=PT(12), bold=True, color=WHITE, font=FONT), line_break(), run("(ex-PSV and FSV)", size=PT(12), italic=True, color=WHITE, font=FONT), run(" ", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr")], fill="969696", line_color="none", anchor="ctr"))
    out.append(table(n(), "Table 49", IN(1.792), IN(1.375), IN(2.2), IN(0.3), col_widths=[IN(2.2)], rows=[
        trow([tcell("Criteria", size=PT(12), color=BLACK, borders={"R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0)),
    ]))
    out.append(table(n(), "Table 50", IN(4.158), IN(1.375), IN(8.677), IN(0.3), col_widths=[IN(8.677)], rows=[
        trow([tcell("Inclusion / Exclusion Rationale", size=PT(12), color=BLACK, borders={"R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0)),
    ]))
    out.append(text_box(n(), "Rectangle 54", IN(4.158), IN(2.422), IN(8.677), _ROW_H, [paragraph([run("Same as above", size=PT(14), italic=True, color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    out.append(text_box(n(), "Rectangle 23", IN(1.793), IN(4.454), IN(2.2), _ROW_H, [paragraph([run("High Volume Offshore", size=PT(12), bold=True, color=BLACK, font=FONT), line_break(), run("(PSV and FSV)", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr")], fill="FFC000", line_color="none", anchor="ctr"))
    out.append(table(n(), "Table 31", IN(0.362), IN(4.454), IN(1.263), IN(0.5), col_widths=[IN(1.263)], rows=[
        trow([tcell("Addressable Offshore", size=PT(12), color="FFC000", borders={"R": {"color": "FFC000", "width": 38100}, "T": "none", "B": "none"})], h=IN(0.5)),
    ]))
    out.append(text_box(n(), "TextBox 33", IN(4.158), IN(6.485), IN(8.677), _ROW_H, [paragraph([run("Same as above", size=PT(14), italic=True, color=BLACK, font=FONT)])], fill=None, line_color="none", anchor="ctr"))
    out.append(table(n(), "Table 39", IN(0.361), IN(1.746), IN(1.264), IN(1.175), col_widths=[IN(1.264)], rows=[
        trow([tcell("Table Stakes", size=PT(12), color=BLACK, borders={"R": {"color": BLACK, "width": 38100}, "T": "none", "B": "none"})], h=IN(1.175)),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
