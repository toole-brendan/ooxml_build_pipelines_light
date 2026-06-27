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
  • _GRID_CELLS ... the repeated criteria grid cells, fill = addressability
                        (BLACK table-stakes · 007770 addressable · 969696 non-)
  • _ITEM_DESCRIPTIONS ... the right-column item descriptions / rationale paragraphs
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
# HAND-POLISHED — do not regenerate with convert_slide.py (it will refuse; see logs).
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder,
)
from deck_core.style import IN, PT, BLACK, WHITE, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table kit (local): separates a cell's CONTENT from its MECHANICS (insets,
#    borders, spans). Renders identically to the raw tcell()/tcell_rich() form —
#    the only change is legibility. ──
def edge(color, w=12700):
    """One cell-border edge (default 1pt hairline)."""
    return {"color": color, "width": w}


def bd(L=None, R=None, T=None, B=None):
    """Border dict from only the edges drawn; omitted sides render no-fill (as the source does)."""
    return {k: v for k, v in (("L", L), ("R", R), ("T", T), ("B", B)) if v is not None} or None


def cell(text="", *, fill=None, bold=None, italic=None, color=BLACK, size=PT(10),
         align="l", anchor="ctr", span=1, rowspan=1,
         l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell with span/align/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell(text, fill=fill, bold=bold, italic=italic, color=color, size=size,
                 align=align, anchor=anchor, grid_span=span, row_span=rowspan, font=FONT,
                 l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


def rcell(paras, *, fill=None, anchor="ctr", span=1, rowspan=1,
          l_ins=45720, r_ins=45720, t_ins=45720, b_ins=45720, **edges):
    """tcell_rich with span/anchor/insets defaulted to the engine defaults; borders via L/R/T/B=edge(...)."""
    return tcell_rich(paras, fill=fill, grid_span=span, row_span=rowspan, anchor=anchor,
                      l_ins=l_ins, r_ins=r_ins, t_ins=t_ins, b_ins=b_ins, borders=bd(**edges))


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_CRIT_W, _CRIT_H = IN(2.2), IN(0.5)        # criteria-box geometry
_RATIONALE_X, _RATIONALE_H = IN(4.158), IN(0.5)   # rationale-text column x / height
_ROW_H = IN(0.5)          # tier-row box height                   [shared x4]

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: the six stacked criteria cells of the addressability funnel; the fill encodes
#   addressability (in/out of scope).
_GRID_CELLS = [    # (x, y, fill, label) x6 — repeated criteria grid cells, fill = addressability
    (1.792, 1.746, BLACK, "US-Built"),   # 000000 black
    (1.793, 2.423, BLACK, "US-Flagged"),   # 000000 black
    (1.793, 3.1, "007770", "Commercially Viable"),   # 007770 teal
    (1.793, 3.777, "007770", "Oceangoing"),   # 007770 teal
    (1.793, 5.131, "969696", "Great Lakes Commercial Vessels"),   # 969696 gray
    (1.793, 6.485, "969696", "Other Categories"),   # 969696 gray
]

# local_meaning: the six right-column inclusion/exclusion rationale blurbs, one per criteria
#   row.
_ITEM_DESCRIPTIONS = [    # (y, cx, label) x6 — right-column item descriptions / rationale
    (1.746, 8.677, "Provides Jones Act protection or enables subsidy eligibility under pending legislation and potential expansion of other programs; required for certain export/import provisions"),
    (3.773, 8.677, "Drives national shipbuilding capacity with avg. gross tonnage 15x+ that of offshore vessels"),
    (3.097, 8.677, "Meets capabilities and tonnage required for participation in subsidized programs; priced to achieve revenue targets"),
    (5.799, 8.677, "Small fleet size precludes serial production; low gross tonnage per vessel limits national security utility and pricing"),
    (5.123, 8.677, "Unlikely to drive meaningful demand given small fleet size (~37 vessels) and low retirement rates"),
    (4.448, 8.677, "Large fleet size enables serial production (5+ hulls/yr to achieve max labor efficiencies); viable if owner/operators conduct 1-for-1 replacement of expected retirements"),
]

# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry and trow(h=...) is a minimum row
# height. A row- or column-level convention is expressed by repeating the same
# l_ins/r_ins/t_ins/b_ins and anchor across its cells. In tcell/tcell_rich those
# insets are internal padding and anchor is vertical alignment; tcell align or
# tpara align/mar_l/indent controls horizontal alignment and paragraph margins.

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
    out.append(breadcrumb("US-Built Ship Demand", "Status Quo"))
    out.append(title_placeholder("Addressable Demand", "US-built and flagged oceangoing commercial vessels and high-volume offshore vessels meet desired regulatory and/or serial production requirements."))
    # ── criteria grid cells (colour = addressability) ──
    for _x, _y, _fill, _t in _GRID_CELLS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _CRIT_W, _CRIT_H, [paragraph([run(_t, size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr"))
    # ── tier spine labels + column headers (low-level row-label tables) ──
    # Across these one-cell tables, col_widths is the column-level width and
    # trow(h=...) the row minimum. Repeated cell insets/anchor create a
    # row/column padding convention; tpara alignment and margins place text.
    # palette — text: 007770 teal; rules: 007770 teal (right edge); cell fills: none.
    out.append(table(n(), "Table 20", IN(0.361), IN(3.097), IN(1.264), IN(1.175), col_widths=[IN(1.264)], rows=[
        trow([rcell([tpara([trun("Addressable", size=PT(12), color="007770", font=FONT)]), tpara([trun("Commercial", size=PT(12), color="007770", font=FONT)])], R=edge("007770", 38100))], h=IN(1.175)),
    ]))
    # palette — text: 969696 gray; rules: 969696 gray (right edge); cell fills: none.
    out.append(table(n(), "Table 24", IN(0.362), IN(5.131), IN(1.263), IN(1.854), col_widths=[IN(1.263)], rows=[
        trow([cell("Non-Addressable", size=PT(12), color="969696", R=edge("969696", 38100))], h=IN(1.854)),
    ]))
    # ── right-column item descriptions ──
    for _y, _cx, _t in _ITEM_DESCRIPTIONS:
        out.append(text_box(n(), "Label", _RATIONALE_X, IN(_y), IN(_cx), _RATIONALE_H, [paragraph([run(_t, size=PT(14), color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # ── offshore tier boxes + "Same as above" rationale cells ──
    out.append(text_box(n(), "Rectangle 36", IN(1.793), IN(5.808), IN(2.2), _ROW_H, [paragraph([run("Low Volume Offshore ", size=PT(12), bold=True, color=WHITE, font=FONT), line_break(), run("(ex-PSV and FSV)", size=PT(12), italic=True, color=WHITE, font=FONT), run(" ", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="969696", line_color="none", anchor="ctr"))   # 969696 gray
    # palette — text: 000000 black; rules: 000000 black (header underline); cell fills: none.
    out.append(table(n(), "Table 49", IN(1.792), IN(1.375), IN(2.2), IN(0.3), col_widths=[IN(2.2)], rows=[
        trow([cell("Criteria", size=PT(12), B=edge(BLACK))], h=IN(0)),
    ]))
    # palette — text: 000000 black; rules: 000000 black (header underline); cell fills: none.
    out.append(table(n(), "Table 50", IN(4.158), IN(1.375), IN(8.677), IN(0.3), col_widths=[IN(8.677)], rows=[
        trow([cell("Inclusion / Exclusion Rationale", size=PT(12), B=edge(BLACK))], h=IN(0)),
    ]))
    out.append(text_box(n(), "Rectangle 54", IN(4.158), IN(2.422), IN(8.677), _ROW_H, [paragraph([run("Same as above", size=PT(14), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    out.append(text_box(n(), "Rectangle 23", IN(1.793), IN(4.454), IN(2.2), _ROW_H, [paragraph([run("High Volume Offshore", size=PT(12), bold=True, color=BLACK, font=FONT), line_break(), run("(PSV and FSV)", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="FFC000", line_color="none", anchor="ctr"))   # FFC000 amber
    # palette — text: FFC000 amber; rules: FFC000 amber (right edge); cell fills: none.
    out.append(table(n(), "Table 31", IN(0.362), IN(4.454), IN(1.263), IN(0.5), col_widths=[IN(1.263)], rows=[
        trow([cell("Addressable Offshore", size=PT(12), color="FFC000", R=edge("FFC000", 38100))], h=IN(0.5)),
    ]))
    out.append(text_box(n(), "TextBox 33", IN(4.158), IN(6.485), IN(8.677), _ROW_H, [paragraph([run("Same as above", size=PT(14), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr"))   # 000000 black
    # palette — text: 000000 black; rules: 000000 black (right edge); cell fills: none.
    out.append(table(n(), "Table 39", IN(0.361), IN(1.746), IN(1.264), IN(1.175), col_widths=[IN(1.264)], rows=[
        trow([cell("Table Stakes", size=PT(12), R=edge(BLACK, 38100))], h=IN(1.175)),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
