"""award_data_reference — Strategic Contracts deck (20260624), source slide 4.

EXHIBIT — "Award Data Reference": the right award-data fields separate real
demand, access, timing, and supplier opportunity. Two side-by-side reference
tables list the fields that matter — a prime-award table (left) grouping fields
into identity/linkage, classification, competition/access, money, timing and
scope/organization/funding, and a subaward table (right) grouping the FFATA
report into report identity, dollars/dates, supplier identity, work description,
prime linkage and prime context — each row pairing the actual FPDS/USAspending
nomenclature with why it matters for entry. A full-width source-orientation strip
along the bottom keys each layer to its feeds (prime: SAM.gov Contract Awards /
USAspending / FPDS; subaward: SAM.gov Subaward Reporting / FFATA / USAspending
subawards).

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............... breadcrumb() + prelim_chip() + title_placeholder()
  • prime awards ......... "Prime Award Fields Banner" text_box + table(
                          "Prime Award Fields") — six prime field groups
  • subawards ........... "Subaward Fields Banner" text_box + table(
                          "Subaward Fields") — six subaward field groups
  • source orientation .. table("Source Orientation Strip") — full-width
                          two-row footer keying each layer to its data sources

Auto-converted by _tools/convert_slide.py, then hand-annotated for study: names
and comments made semantic, body grouped into sections — NO coordinate, value,
colour, or paint-order changed, so the render is byte-identical to the raw port.

Converter stats: text_box=2, table=3, chrome_builders=3, dropped=1 (think-cell
OLE frame).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


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
    out.append(breadcrumb("Strategic Contracts", "Award Data Methodology"))
    out.append(prelim_chip())
    out.append(title_placeholder("Award Data Reference", "The right fields separate real demand, access, timing, and supplier opportunity."))
    # ── prime awards: banner + field-reference table ──
    out.append(text_box(n(), "Prime Award Fields Banner", IN(0.495), IN(1.384), IN(6.025), IN(0.32), [paragraph([run("Prime awards — fields that determine direct access and timing", size=PT(10), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="1D4D68", line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # CHART_ACCENT_2 (charts-only)
    # Table layout: col_widths fix the three field-reference columns (group /
    # nomenclature / why-it-matters) and trow(h=...) sets each group-row minimum.
    # Every cell repeats t_ins/b_ins=27432 padding; the header row carries the
    # bottom rule and the body rows alternate fill.
    # Rule/text palette: text 000000 (BLACK), group labels 162029 (DK); rules 000000 (BLACK) header · 808080 (rule-gray, ad-hoc ~GRAY_4) inner.
    out.append(table(n(), "Prime Award Fields", IN(0.495), IN(1.725), IN(6.025), IN(4.535), col_widths=[IN(1.42), IN(2.53), IN(2.075)], rows=[
        trow([tcell("Data field group", size=PT(9), bold=True, color="000000", fill="F4F6F7", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}}), tcell("Actual data field nomenclature", size=PT(9), bold=True, color="000000", fill="F4F6F7", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}}), tcell("Why it matters", size=PT(9), bold=True, color="000000", fill="F4F6F7", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}})], h=IN(0.289)),   # near-white (ad-hoc, ~GRAY_1)
        trow([tcell("Identity and linkage", size=PT(9.5), bold=True, color="162029", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("PIID; referenced IDV PIID; modification number; UEI; ultimate-parent UEI; USAspending generated internal ID", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Links the award family, holder, parent vehicle, modifications and detail calls", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.708)),   # WHITE
        trow([tcell("Classification", size=PT(9.5), bold=True, color="162029", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("award or IDV type; single- / multiple-award IDC; type of IDC; contract pricing type", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Determines whether the direct route is open, holder-gated, single-award, OT, delivery order, FSS, BPA, BOA or definitive contract", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.86)),   # near-white (ad-hoc)
        trow([tcell("Competition and access", size=PT(9.5), bold=True, color="162029", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("extent competed; fair opportunity; set-aside; number of offers; solicitation ID", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Identifies who can compete and whether a new entrant must wait for a pool, on-ramp or recompete", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.708)),   # WHITE
        trow([tcell("Money", size=PT(9.5), bold=True, color="162029", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("per-action obligation; cumulative obligation; base and all-options value / ceiling", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Separates committed spend from capacity; prevents summing cumulative fields or shared ceilings", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.708)),   # near-white (ad-hoc)
        trow([tcell("Timing", size=PT(9.5), bold=True, color="162029", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("date signed; start date; current completion; ultimate completion; last date to order", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Dates the entry window, especially for IDVs and successor vehicles", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.555)),   # WHITE
        trow([tcell("Scope, organization and funding", size=PT(9.5), bold=True, color="162029", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("PSC; NAICS; requirement description; contracting office; TAS / federal account; business-size / socioeconomic data", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Connects the award to the market, buyer, mission, appropriation and eligibility constraints", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.708)),   # near-white (ad-hoc)
    ]))
    # ── subawards: banner + field-reference table ──
    out.append(text_box(n(), "Subaward Fields Banner", IN(6.77), IN(1.391), IN(6.025), IN(0.32), [paragraph([run("Subawards — fields that identify the visible supplier layer", size=PT(10), bold=True, color="FFFFFF", font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color="none", anchor="ctr", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))   # blue (ad-hoc, ~BLUE_3)
    # Table layout: the same three-column field-reference contract as the prime
    # table; the repeated cell t_ins/b_ins padding and per-row fill/border
    # convention place the grouped subaward rows.
    # Rule/text palette: text 000000 (BLACK), group labels 162029 (DK); rules 000000 (BLACK) header · 808080 (rule-gray, ad-hoc ~GRAY_4) inner.
    out.append(table(n(), "Subaward Fields", IN(6.77), IN(1.725), IN(6.025), IN(3.743), col_widths=[IN(1.42), IN(2.53), IN(2.075)], rows=[
        trow([tcell("Data field group", size=PT(9), bold=True, color="000000", fill="F4F6F7", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}}), tcell("Actual data field nomenclature", size=PT(9), bold=True, color="000000", fill="F4F6F7", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}}), tcell("Why it matters", size=PT(9), bold=True, color="000000", fill="F4F6F7", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": "none", "B": {"color": "000000", "width": 12700}})], h=IN(0.287)),   # near-white (ad-hoc, ~GRAY_1)
        trow([tcell("Report identity", size=PT(9.5), bold=True, color="162029", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("subaward report ID; subaward number", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}}), tcell("Provides the report-level key; SAM FFATA report ID does not require deduplication", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "000000", "width": 12700}, "B": {"color": "808080", "width": 6350}})], h=IN(0.551)),   # WHITE
        trow([tcell("Dollars and dates", size=PT(9.5), bold=True, color="162029", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("subaward amount; subaward date; submitted date", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Measures reported first-tier demand and reporting lag; submitted date is the lag field", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.702)),   # near-white (ad-hoc)
        trow([tcell("Supplier identity", size=PT(9.5), bold=True, color="162029", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("subawardee UEI; subawardee legal name; parent UEI; parent legal name; business type", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Enables supplier rollup, recurrence, concentration and eligibility analysis", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.551)),   # WHITE
        trow([tcell("Work description", size=PT(9.5), bold=True, color="162029", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("subaward description; description of requirement", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Shows what the supplier is being paid to provide", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.399)),   # near-white (ad-hoc)
        trow([tcell("Prime linkage", size=PT(9.5), bold=True, color="162029", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("prime PIID; referenced IDV PIID; prime contract key; prime award type", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}}), tcell("Connects the supplier report to the prime award, block or vehicle", size=PT(9), color="000000", fill="FFFFFF", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": {"color": "808080", "width": 6350}})], h=IN(0.551)),   # WHITE
        trow([tcell("Prime context", size=PT(9.5), bold=True, color="162029", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("prime UEI; prime name; prime NAICS; contracting office; funding office; total contract value", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"}), tcell("Shows who buys from the supplier, what market the prime sits in, and the scale of the underlying award", size=PT(9), color="000000", fill="FBFCFD", t_ins=27432, b_ins=27432, borders={"L": "none", "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.702)),   # near-white (ad-hoc)
    ]))
    # ── source orientation strip (full-width source-key footer) ──
    # Table layout: a full-width two-column footer; the left label cell row-spans
    # both rows (row_span=2) while tcell_rich/tpara/trun set the mixed-weight
    # source captions in the right column.
    # Rule/text palette: text 162029 (DK) / 000000 (BLACK), WHITE cell separators, 808080 (rule-gray, ad-hoc ~GRAY_4) bottom rule.
    out.append(table(n(), "Source Orientation Strip", IN(0.495), IN(6.405), IN(12.339), IN(0.6), col_widths=[IN(1.655), IN(10.683)], rows=[
        trow([tcell("Source orientation", size=PT(9), bold=True, color="FFFFFF", align="ctr", fill="1D4D68", row_span=2, t_ins=27432, b_ins=27432, borders={"L": "none", "R": {"color": "FFFFFF", "width": 6350}, "T": "none", "B": "none"}), tcell_rich([tpara([trun("Prime awards: ", size=PT(8.5), bold=True, color="162029", font=FONT), trun("SAM.gov Contract Awards; USAspending; FPDS", size=PT(8.5), color="000000", font=FONT), trun(" — classify access, competition, money, timing, scope, organization and appropriation", size=PT(8.5), italic=True, color="000000", font=FONT)])], fill="EAF2F8", t_ins=27432, b_ins=27432, borders={"L": {"color": "FFFFFF", "width": 6350}, "R": "none", "T": "none", "B": {"color": "808080", "width": 6350}})], h=IN(0.3)),   # CHART_ACCENT_2 (charts-only), pale-blue (ad-hoc)
        trow([tcell_rich([tpara([trun("Subawards: ", size=PT(8.5), bold=True, color="162029", font=FONT), trun("SAM.gov Subaward Reporting / FFATA; USAspending subawards", size=PT(8.5), color="000000", font=FONT), trun(" — identify first-tier suppliers, reported dollars, reporting lag and prime linkage", size=PT(8.5), italic=True, color="000000", font=FONT)])], fill="EAF2F8", t_ins=27432, b_ins=27432, borders={"L": {"color": "FFFFFF", "width": 6350}, "R": "none", "T": {"color": "808080", "width": 6350}, "B": "none"})], h=IN(0.3)),   # pale-blue (ad-hoc)
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
