"""strategic_contracts_table — Awards Methodology deck, slide 1 (the payoff exhibit).

EXHIBIT — "Strategic Contracts — Recompete Watch-List": the worked output of the
deck's method. A seven-column table of real defense-maritime contracts grouped by the slide-2
addressability split — the two entry routes named by privity, not internal A/B codes:
  • Direct to Government (win the recompete): vehicles whose ordering clock
    (last date to order) has PASSED or is imminent — winnable as prime or OTA.
  • Through the prime (enter the build): big locked/competed builds entered
    through the supply chain (DDG-51 SWBS subaward lanes + adjacent amphib/auxiliary
    programs).
Columns (8): Route · Platform/Vehicle · Incumbent · Amount · Recompete-or-entry signal ·
Funding (Treasury Account Symbol / color of money) · Budget · Notes. The Budget column is
the budget-outlook read — a colour swatch carrying its own word (green Favorable / grey
Unknown), so it needs no separate legend; it rates each program's budget health and is
DISTINCT from the factual Funding(TAS) column. Notes carries the terse FY27-PB rationale.

CODE MAP (body follows source PAINT ORDER; headers mark roles in place):
  • chrome ............... RAW breadcrumb placeholder + title_placeholder() + prelim_chip()
  • watch-list table ..... native table() — 8 cols, two row-spanned entry-route groups
                           (Direct to Government: 6 rows, Through the prime: 5 rows);
                           Budget column = labelled green/grey swatch; Notes = rationale

DATA PROVENANCE (real data, not the source template's placeholders):
  • Recompete dates / ceilings: SAM.gov Contract Awards (lastDateToOrder,
    completion dates, totalBaseAndAllOptionsValue); obligations from USAspending.
  • Funding / color of money: USAspending File-C Treasury Account Symbol
    (federal_account); SCN 017-1611, OPA 021-2035, RDT&E,N 017-1319, O&M,N, USCG
    PC&I 070-0612. Gravois + Safe Boats report no File-C → funding left blank.
  • DDG-51 SWBS subaward lanes: HHI by SWBS major group recomputed from the
    distributed-shipbuilding subaward transactions via the HII→SWBS crosswalk
    (500 Auxiliary: $947.5M, 90 subs, HHI 683 — open lane; 200 Propulsion: $957.9M,
    29 subs, HHI 1905 — entrenched / team).
  • Budget outlook + Notes: grounded in the FY2027 President's-Budget justification
    books — OPA P-40 watercraft/bridge lines, SCN BA05 (TAO 5025 / TAGOS 5030) + DDG-51
    (LI 2122), O&M,N 1B4B Ship Depot Maintenance, USCG PC&I Vessels. Every row is a
    funded program, so the read is Favorable (funded, flat-to-rising) or Unknown (no
    discrete budget line, or a sharp FY27 budget-year dip) — none Unfavorable. The Notes
    cell is the one-line evidence for each call. Analyst-assigned from the books, not a
    single pulled field.
  • Saronic's own awards are intentionally EXCLUDED (this is Saronic's scan).
Caveats carried by the data: FFATA subaward $ is a floor, not a census; a
non-federal SAM key hides DoD actions < 90 days old; build/recompete windows for
definitive contracts are forecasts, not certain.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun,
    title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── budget-outlook palette + labels (Budget Alignment column = colour swatch + word) ──
# Grounded in the FY2027 President's-Budget books (OPA / SCN / O&M,N / USCG PC&I): every
# row here is a funded program, so the honest read is Favorable (funded, flat-to-rising)
# or Unknown (no discrete budget line, or a sharp FY27 budget-year dip) — NO Unfavorable.
_GREEN, _RED, _GREY = "1B8A57", "A33124", "808080"   # green/Favorable · red/Unfavorable · row-rule grey (all ad-hoc)
_BFILL  = {"F": _GREEN, "U": "BFBFBF", "X": _RED}      # swatch fill (BFBFBF = GRAY_3)
_BLABEL = {"F": "Favorable", "U": "Unknown", "X": "Unfavorable"}
_BTEXT  = {"F": "FFFFFF", "U": "000000", "X": "FFFFFF"}       # label colour on the swatch (FFFFFF = WHITE / 000000 = BLACK)
_ROUTE_FILL = "1F3864"   # dark navy spine for the entry-route row-span column
_RULE = {"color": "808080", "width": 6350}    # 0.5pt grey row separator
_HEAVY = {"color": "000000", "width": 12700}      # 1pt black (header / group boundary)

# ── watch-list data (each tuple drives one table row) ──
# (platform, vehicle/piid, incumbent, amount, recompete-or-entry signal, funding, budget_RAG, note)
# note = the FY27-PB budget rationale for the RAG, ≤ ~5 words (see DATA PROVENANCE).
_ROUTE_A = [
    ("Army watercraft ship-repair", "W56HZV21DL pool", "Bay Ship & Yacht +9", "$416.8M obl", "LDO 2026-01-25 · passed", "OPA 021-2035", "F", "ESP request at series high"),
    ("Army bridge erection boats", "W56HZV19D0093", "Birdon America", "$199M ceil", "LDO 2025-08-12 · passed", "OPA 021-2035", "U", "FY27 trough, recovers later"),
    ("Navy CVN maintenance (PNW)", "N0002419D4310", "Metro Machine (NASSCO)", "$465M ceil", "LDO 2026-03-20 · passed", "O&M,N", "F", "Readiness-protected depot O&M"),
    ("Navy small craft (aluminum)", "N0002417D2209", "Gravois Aluminum Boats", "$118M orders", "LDO 2023-09-30 · portal-dark", "", "U", "No public budget line"),
    ("Navy USV core (R&D vehicle)", "N0002418D6401", "Penn State ARL", "$77M orders", "LDO 2026-09-30 · imminent", "RDT&E,N 017-1319", "F", "Unmanned R&D growth priority"),
    ("Navy patrol boats", "N0002421C2201", "Safe Boats Intl", "$173.9M obl", "Sole-source · ends 2027-12-16", "", "U", "Sole-source; no public line"),
]
_ROUTE_B = [
    ("USCG Offshore Patrol Cutter", "70Z02322C93220001", "Austal (ex-Eastern)", "$3.3B ceil", "Stage-2 build to 2030", "PC&I 070-0612", "U", "FY27 −62%; Stage 3 starts"),
    ("DDG-51 Auxiliary (SWBS 500)", "HII + BIW · locked prime", "90 subs · top 15.9%", "$947.5M subs", "HHI 683 · open lane (FY28-32)", "SCN 017-1611", "F", "Funded to FY31; open lane"),
    ("DDG-51 Propulsion (SWBS 200)", "HII + BIW · locked prime", "GE 34.7%", "$957.9M subs", "HHI 1905 · team / 2nd-source", "SCN 017-1611", "F", "Funded to FY31; entrenched"),
    ("T-AGOS(X) ocean surveillance", "N0002423C2203", "Austal USA", "$3.2B ceil", "Full & open · build to 2033", "SCN 017-1611", "F", "Funded ~1 ship per year"),
    ("T-AO John Lewis fleet oiler", "N0002416C2229", "NASSCO", "$6.0B ceil", "Full & open · build to 2028", "SCN 017-1611", "F", "$2.2B FY27; two ships"),
]

# Layout discipline (gold-standard): the platform NAME and every data cell stay within
# their line budget at the authored column width (name 1 line; signal/funding/notes ≤ 2),
# so the tallest cell (the 2-line platform name+PIID, 0.42") is ≤ the row minimum and the
# table height is deterministic — it cannot balloon past the frame and spill off the slide.
# Verified via deck_core.text_metrics at a conservative width. Σ widths = 12.35.
_COLW = [IN(0.85), IN(2.70), IN(1.95), IN(1.10), IN(2.05), IN(1.40), IN(1.05), IN(1.25)]
_HEADERS = ["Route", "Platform · Vehicle", "Incumbent", "Amount",
            "Recompete / entry", "Funding (TAS)", "Budget", "Notes"]


def _hcell(text):
    return tcell(text, size=PT(11), bold=True, color="000000", align="ctr", anchor="ctr",
                 borders={"T": "none", "B": _HEAVY, "L": "none", "R": "none"})


def _route_cell(line1, line2, span, bottom):
    return tcell_rich([
        tpara([trun(line1, size=PT(12), bold=True, color="FFFFFF", font=FONT)], align="ctr", mar_l=0, indent=0),
        tpara([trun(line2, size=PT(8), color="FFFFFF", font=FONT)], align="ctr", mar_l=0, indent=0),
    ], row_span=span, anchor="ctr", fill=_ROUTE_FILL,
       borders={"T": "none", "B": bottom, "L": "none", "R": {"color": "FFFFFF", "width": 6350}})


def _drow(rec, route_cell, bmode):
    plat, piid, inc, amt, sig, fund, rag, note = rec
    b = {"none": "none", "grey": _RULE, "black": _HEAVY}[bmode]
    edge = {"T": "none", "B": b, "L": "none", "R": "none"}
    cells = []
    if route_cell is not None:
        cells.append(route_cell)
    cells.append(tcell_rich([
        tpara([trun(plat, size=PT(11), bold=True, color="000000", font=FONT)], mar_l=0, indent=0),
        tpara([trun(piid, size=PT(8), italic=True, color=_GREY, font=FONT)], mar_l=0, indent=0),
    ], anchor="ctr", borders=edge))
    cells.append(tcell(inc, size=PT(10), color="000000", align="ctr", anchor="ctr", borders=edge))
    cells.append(tcell(amt, size=PT(10), bold=True, color="000000", align="ctr", anchor="ctr", borders=edge))
    cells.append(tcell(sig, size=PT(9), color="000000", anchor="ctr", borders=edge))
    cells.append(tcell(fund, size=PT(9), color="000000", align="ctr", anchor="ctr", borders=edge))
    # Budget Alignment: colour swatch + word (Favorable green / Unknown grey); no legend.
    cells.append(tcell(_BLABEL[rag], size=PT(8), bold=True, color=_BTEXT[rag], align="ctr",
                       anchor="ctr", fill=_BFILL[rag], borders=edge))
    # Notes: terse FY27-PB budget rationale for the RAG (grey, ≤ 2 lines).
    cells.append(tcell(note, size=PT(8), color=_GREY, anchor="ctr", borders=edge))
    return trow(cells, h=IN(0.45))   # min ≥ the 2-line platform cell (0.42"); rows hold here


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome: breadcrumb placeholder + title + prelim chip ──
    out.append("<p:sp><p:nvSpPr><p:cNvPr id=\"2000\" name=\"Text Placeholder 1\" /><p:cNvSpPr><a:spLocks noGrp=\"1\" /></p:cNvSpPr><p:nvPr><p:ph type=\"body\" sz=\"quarter\" idx=\"10\" /></p:nvPr></p:nvSpPr><p:spPr /><p:txBody><a:bodyPr /><a:lstStyle /><a:p><a:r><a:rPr lang=\"en-US\" b=\"1\" /><a:t>Defense Market Strategy </a:t></a:r><a:r><a:rPr lang=\"en-US\" /><a:t>/ Strategic Contracts</a:t></a:r></a:p></p:txBody></p:sp>")
    out.append(title_placeholder("Strategic Contracts — Recompete Watch-List", "Recompete timing, incumbents, and funding — by entry route."))
    out.append(prelim_chip())
    # ── strategic-contracts watch-list (8 cols; two row-spanned entry-route groups).
    #    Budget Alignment is a labelled colour swatch, so no separate legend is needed. ──
    rows = [trow([_hcell(h) for h in _HEADERS], h=IN(0.32))]
    n_a = len(_ROUTE_A)
    for i, rec in enumerate(_ROUTE_A):
        rc = _route_cell("Direct to Government", "Win the recompete as prime or OTA", n_a, _HEAVY) if i == 0 else None
        rows.append(_drow(rec, rc, "black" if i == n_a - 1 else "grey"))
    n_b = len(_ROUTE_B)
    for i, rec in enumerate(_ROUTE_B):
        rc = _route_cell("Through the prime", "Enter a locked build via the supply chain", n_b, "none") if i == 0 else None
        rows.append(_drow(rec, rc, "none" if i == n_b - 1 else "grey"))
    # cy = header 0.32 + 11 data rows × 0.45 = 5.27"; from y=1.60 the table ends at
    # y≈6.87" — ~0.63" of bottom margin on the 7.5" canvas.
    out.append(table(n(), "Table 44", IN(0.495), IN(1.60), IN(12.35), IN(5.27), col_widths=_COLW, rows=rows))
    return "".join(out)


def render() -> str:
    return slide(_body())
