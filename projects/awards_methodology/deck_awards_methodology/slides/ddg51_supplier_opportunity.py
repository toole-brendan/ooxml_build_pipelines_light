"""ddg51_supplier_opportunity — Strategic Contracts deck (20260624), source slide 2.

EXHIBIT — "DDG-51 Supplier Opportunity": prime access to the DDG-51 program is
effectively committed — Huntington Ingalls and Bath Iron Works are the established
primes — but each multi-year procurement (MYP) block opens a predictable, datable
supplier entry window. A top band of five MYP cadence cards (FY13-17 … FY28-32
plus a Chain total) reports each block's award date, prime obligations, first-tier
subaward dollars, and supplier count. Below, a cumulative spend axis stacks
"Award yr / +1 / +2 / +3 / +4" segments against years-after-award, with
cumulative-share labels (cum. 26% … 79%) and a callout that ≈80% of first-tier
dollars land within four years. Two native tables read the opportunity by ship
system (the System Concentration table over SWBS systems) and by award structure
(the Award Anatomy table), arguing the route to revenue is to qualify through the
incumbent chain before the FY28-32 sourcing wave.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ................ breadcrumb() + prelim_chip() + title_placeholder()
                           (painted first, ahead of the data)
  • _SECTION_BANNERS ...... numbered dark-navy banners (1·2·3) + the "Award Anatomy"
                           banner over the right-hand table ("Label" shapes)
  • _CAPTION_NOTES ........ italic basis/scope captions sitting under the banners
  • _MYP_CARD_BASES ....... the five cadence-card background rectangles ("LegendSwatch")
  • _MYP_CARD_HEADERS ..... FY-block header chips (FY13-17 … FY28-32 · Chain total)
  • MYP Card Body ......... five per-block detail boxes (award date · prime $ ·
                           first-tier $ · supplier count)
  • cumulative spend axis . "Spend Axis" caption + five "Spend Segment" bars +
                           _CUMULATIVE_LABELS (cum. % labels) — the labels loop is
                           painted between the first and remaining Spend Segments
  • spend callout ......... "≈80% within four years" box
  • System Concentration .. table: SWBS systems × reported $ / supplier structure / entry read
  • Award Anatomy ......... table: award attributes × DDG-51 read / relevance
  • reporting caveat ...... "Reporting Caveat" FFATA-floor note

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=13, table=2, chrome_builders=3, clusters=5 (covering
22 shapes), dropped=1 (think-cell OLE frame).
Residue: a title-like shape sits off the house position; the converter kept it
verbatim rather than re-homing it to the house title slot.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, line_break, table, trow, tcell, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates; value unchanged from the raw port) ──
_BANNER_H = IN(0.238)                              # numbered section-banner height   [x4]
_CAPTION_W = IN(8.1)                               # section caption-note width       [x3]
_CARD_BASE_Y, _CARD_BASE_W, _CARD_BASE_H = IN(2.012), IN(1.405), IN(0.962)        # MYP card base box     [x5]
_CARD_HEADER_Y, _CARD_HEADER_W, _CARD_HEADER_H = IN(2.012), IN(1.405), IN(0.231)  # MYP card header strip [x5]
_CUM_LABEL_Y, _CUM_LABEL_H = IN(4.051), IN(0.16)   # cumulative-label box             [x5]
_CARD_BODY_Y = IN(2.277)   # MYP card body box, shared y      [x5]
_CARD_BODY_W = IN(1.315)   # MYP card body box, shared width  [x5]
_CARD_BODY_H = IN(0.647)   # MYP card body box, shared height [x5]
_SPEND_SEG_Y = IN(3.621)   # spend-segment bar, shared y      [x5]
_SPEND_SEG_H = IN(0.4)     # spend-segment bar, shared height [x5]

# ── repeated-shape data tables (each drives a loop in _body) ──
_SECTION_BANNERS = [    # (x, y, cx, label) x4 — numbered dark-navy section banners (1·2·3) + "Award Anatomy"
    (0.495, 1.592, 8.1, "1. Multiyear procurement cadence — the supplier market is datable"),
    (0.495, 3.177, 8.1, "2. Award-to-supplier spend timing — first-tier dollars are front-loaded"),
    (0.495, 4.604, 8.1, "3. Where to compete or position — entry tactic varies by ship system"),
    (8.765, 1.592, 4.03, "Award Anatomy"),
]

_CAPTION_NOTES = [    # (x, y, cy, label) x3 — italic basis/scope captions under the sections
    (0.495, 1.845, 0.135, "Prime obligations shown as HII / BIW; first-tier values are reported FFATA / SAM subawards"),
    (0.452, 4.308, 0.16, "Basis: mature FY13-17 and FY18-22 blocks"),
    (0.495, 6.616, 0.24, "SWBS mapping covers 81% of reported dollars; unmapped / non-Ingalls, including BIW, is $674.0M (19.5%)."),
]

_MYP_CARD_BASES = [    # (x, fill) x5 — MYP cadence-card background rectangles (shape name "LegendSwatch")
    (0.689, WHITE),
    (2.219, WHITE),
    (3.749, WHITE),
    (5.279, "CEDDEC"),
    (6.809, "DFE7EB"),
]

_MYP_CARD_HEADERS = [    # (x, fill, label) x5 — FY-block header chips (FY13-17 … FY28-32 · Chain total)
    (0.689, "364D6E", "FY13-17"),
    (2.219, "4C6C9C", "FY18-22"),
    (3.749, "447BB2", "FY23-27"),
    (5.279, "007770", "FY28-32"),
    (6.809, "0E1924", "Chain total"),
]

_CUMULATIVE_LABELS = [    # (x, cx, label) x5 — cumulative-share labels under the spend bars
    (0.565, 2.24, "cum. 26%"),
    (2.805, 1.378, "cum. 42%"),
    (4.183, 1.292, "cum. 58%"),
    (5.476, 0.948, "cum. 69%"),
    (6.423, 0.862, "cum. 79%"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    # ── chrome: breadcrumb · prelim chip · title ──
    out.append(breadcrumb("Strategic Contracts", "Incumbent-Chain Opportunities"))
    out.append(prelim_chip())
    out.append(title_placeholder("DDG-51 Supplier Opportunity", "Prime access is committed, but each MYP block creates a predictable supplier entry window."))
    # ── numbered section banners (dark-navy headers) ──
    for _x, _y, _cx, _t in _SECTION_BANNERS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _BANNER_H, [paragraph([run(_t, size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="0E1924", line_color="none", anchor="ctr", l_ins=91440, t_ins=18288, r_ins=91440, b_ins=18288))
    # ── section caption notes (italic basis lines) ──
    for _x, _y, _cy, _t in _CAPTION_NOTES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), _CAPTION_W, IN(_cy), [paragraph([run(_t, size=PT(8.5), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    # ── MYP cadence cards: base rectangles ──
    for _x, _fill in _MYP_CARD_BASES:
        out.append(text_box(n(), "LegendSwatch", IN(_x), _CARD_BASE_Y, _CARD_BASE_W, _CARD_BASE_H, [paragraph([], line_spacing=100000)], fill=_fill, line_color=DK, line_width=6350, l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── MYP cadence cards: FY-block header chips ──
    for _x, _fill, _t in _MYP_CARD_HEADERS:
        out.append(text_box(n(), "Label", IN(_x), _CARD_HEADER_Y, _CARD_HEADER_W, _CARD_HEADER_H, [paragraph([run(_t, size=PT(9), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── MYP cadence cards: per-block body detail ──
    out.append(text_box(n(), "MYP Card Body", IN(0.734), _CARD_BODY_Y, _CARD_BODY_W, _CARD_BODY_H, [paragraph([run("Awarded 2013-06-03", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$3.35B / $4.93B", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$942.3M first-tier", size=PT(9), bold=True, color=BLACK, font=FONT), line_break(), run("320 suppliers", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "MYP Card Body", IN(2.264), _CARD_BODY_Y, _CARD_BODY_W, _CARD_BODY_H, [paragraph([run("Awarded 2018-09-27", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$6.83B / $5.34B", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$1,327.2M first-tier", size=PT(9), bold=True, color=BLACK, font=FONT), line_break(), run("344 suppliers", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "MYP Card Body", IN(3.794), _CARD_BODY_Y, _CARD_BODY_W, _CARD_BODY_H, [paragraph([run("Awarded 2023-08-01", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$6.95B / $5.03B", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$1,144.6M first-tier", size=PT(9), bold=True, color=BLACK, font=FONT), line_break(), run("89 suppliers", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "MYP Card Body", IN(5.324), _CARD_BODY_Y, _CARD_BODY_W, _CARD_BODY_H, [paragraph([run("Expected ~2028", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("not yet awarded", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("next sourcing cycle", size=PT(9), bold=True, color=BLACK, font=FONT), line_break(), run("2028-31 window", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "MYP Card Body", IN(6.854), _CARD_BODY_Y, _CARD_BODY_W, _CARD_BODY_H, [paragraph([run("incl. FY11 buy", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("prime layer shown above", size=PT(8.5), color=BLACK, font=FONT), line_break(), run("$3,465.8M first-tier", size=PT(9), bold=True, color=BLACK, font=FONT), line_break(), run("521 suppliers", size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    # ── cumulative spend axis: caption · stacked segments · cum. labels (interleaved) ──
    out.append(text_box(n(), "Spend Axis", IN(0.565), IN(3.465), IN(6.63), IN(0.14), [paragraph([run("Share of reported first-tier subaward dollars by years after prime award", size=PT(8.5), italic=True, color=BLACK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    out.append(text_box(n(), "Spend Segment", IN(0.565), _SPEND_SEG_Y, IN(2.24), _SPEND_SEG_H, [paragraph([run("Award yr", size=PT(8.5), bold=True, color=WHITE, font=FONT), line_break(), run("26%", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="364D6E", line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    for _x, _cx, _t in _CUMULATIVE_LABELS:
        out.append(text_box(n(), "Label", IN(_x), _CUM_LABEL_Y, IN(_cx), _CUM_LABEL_H, [paragraph([run(_t, size=PT(8.5), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=91440, t_ins=0, r_ins=91440, b_ins=0))
    out.append(text_box(n(), "Spend Segment", IN(2.805), _SPEND_SEG_Y, IN(1.378), _SPEND_SEG_H, [paragraph([run("+1", size=PT(8.5), bold=True, color=WHITE, font=FONT), line_break(), run("16%", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="4C6C9C", line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Spend Segment", IN(4.183), _SPEND_SEG_Y, IN(1.292), _SPEND_SEG_H, [paragraph([run("+2", size=PT(8.5), bold=True, color=WHITE, font=FONT), line_break(), run("15%", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Spend Segment", IN(5.476), _SPEND_SEG_Y, IN(0.948), _SPEND_SEG_H, [paragraph([run("+3", size=PT(8.5), bold=True, color=WHITE, font=FONT), line_break(), run("11%", size=PT(10), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="6F8DB9", line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    out.append(text_box(n(), "Spend Segment", IN(6.423), _SPEND_SEG_Y, IN(0.862), _SPEND_SEG_H, [paragraph([run("+4", size=PT(8.5), bold=True, color=BLACK, font=FONT), line_break(), run("10%", size=PT(10), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill="CEDDEC", line_color=WHITE, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── spend callout (≈80% within four years) ──
    out.append(text_box(n(), "Spend Callout", IN(7.345), IN(3.513), IN(1.3), IN(0.7), [paragraph([run("≈80%", size=PT(16), bold=True, color="007770", font=FONT)], align="ctr", line_spacing=100000), paragraph([run("within four years", size=PT(9), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color="007770", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    # ── System Concentration table (SWBS systems × entry read) ──
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "System Concentration Table", IN(0.495), IN(4.961), IN(8.1), IN(1.6), col_widths=[IN(1.42), IN(1), IN(2.13), IN(3.55)], rows=[
        trow([tcell("Ship system", size=PT(9), bold=True, color=BLACK, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Reported dollars", size=PT(9), bold=True, color=BLACK, align="ctr", anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Supplier structure", size=PT(9), bold=True, color=BLACK, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Entry read", size=PT(9), bold=True, color=BLACK, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.4)),
        trow([tcell("Auxiliary systems", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("$947.5M", size=PT(9), bold=True, color=BLACK, align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("90 suppliers; top vendor 15.9%", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Fragmented work where another qualified supplier can compete", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.4)),
        trow([tcell("Electric plant", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("$750.8M", size=PT(9), bold=True, color=BLACK, align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("24 suppliers; Rolls-Royce 42.6%", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Second-source qualification or teaming around supplier risk", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.4)),
        trow([tcell("Propulsion plant", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("$957.9M", size=PT(9), bold=True, color=BLACK, align="ctr", fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("29 suppliers; General Electric 34.7%", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Incumbent-led work to monitor for second-source or partner openings", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.4)),
    ]))
    # ── Award Anatomy table (award attributes × DDG-51 read) ──
    # native table (low-level table()/trow()/tcell(); merges via grid_span/row_span)
    out.append(table(n(), "Award Anatomy Table", IN(8.765), IN(1.892), IN(4.03), IN(4.4), col_widths=[IN(1.02), IN(1.49), IN(1.52)], rows=[
        trow([tcell("Attribute", size=PT(9), bold=True, color=BLACK, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("DDG-51 read", size=PT(9), bold=True, color=BLACK, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Relevance", size=PT(9), bold=True, color=BLACK, anchor="b", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.3)),
        trow([tcell("Instrument / award structure", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Definitive MYP production contracts; dual-source prime structure", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Direct prime access is effectively committed for the block", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": BLACK, "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.5)),
        trow([tcell("Competition / holder set", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Huntington Ingalls and Bath Iron Works are established primes", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("New entry is through qualification, teaming, or upper-tier integration", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.5)),
        trow([tcell("Timing trigger", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("MYP awards in 2013, 2018, 2023; FY28-32 expected ~2028", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Dates the next supplier sourcing wave", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.5)),
        trow([tcell("Obligated amount", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Prime obligations by shipyard; $3.47B reported first-tier subawards", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Measures the scale of the visible supplier layer", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.5)),
        trow([tcell("Ceiling / potential value", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("N/A — definitive MYP, not an IDIQ", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Avoids forcing an IDV ceiling metric", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.5)),
        trow([tcell("TAS / appropriation", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Shipbuilding and Conversion, Navy, 017-1611", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Confirms shipbuilding procurement funding context", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.5)),
        trow([tcell("Route to revenue", size=PT(9), bold=True, color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Through the incumbent performance chain", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Qualify before FY28-32 supplier demand is sourced", size=PT(9), color=BLACK, fill=WHITE, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.5)),
    ]))
    # ── reporting caveat (FFATA floor) ──
    out.append(text_box(n(), "Reporting Caveat", IN(8.765), IN(6.351), IN(4.03), IN(0.498), [paragraph([run("Reporting caveat: ", size=PT(9), bold=True, color=BLACK, font=FONT), run("FFATA first-tier reporting is a floor. It lags 6–18 months and under-reports some prime supply chains.", size=PT(9), color=BLACK, font=FONT)], line_spacing=100000)], fill="DFE7EB", line_color=DK, line_width=6350, anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    return "".join(out)


def render() -> str:
    return slide(_body())
