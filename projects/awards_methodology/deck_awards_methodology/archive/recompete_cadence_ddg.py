"""recompete_cadence_ddg — Recompete-cadence research, source spec slide 02.

EXHIBIT — "Recompete Cadence -> Supply-Chain Entry": the DDG-51 prime is a closed
two-yard duopoly you cannot win, but it re-buys on a fixed ~5-year multi-year
cadence and each block flows ~$1B+ to a visible first-tier supplier base. The
cadence is the timing engine; the addressable move is to supply the next block's
sourcing wave, positioned years ahead. The slide is a two-column composition: a
left "Key takeaways" rail carries the argument, while the right column stacks three
big-number cards (scale / recurrence / timing) over two evidence tables — the
multi-year procurement cadence (with the FY28-32 buy highlighted as the next event)
and the where-to-enter concentration read by ship system (HHI). An honest source
line flags that first-tier (FFATA) reporting is a floor, not a census.

CODE MAP (body follows paint order; headers mark roles in place):
  • chrome ............ breadcrumb() + title_placeholder() (house builders)
  • takeaways rail .... left table() — "Key takeaways" header + one bulleted body
                        cell (tcell_rich/tpara/trun, bold lead-ins per bullet)
  • _SUMMARY_CARDS .... three big-number cards (scale / recurrence / timing) -> loop
  • cadence table ..... right table() — Block / Awarded / Prime obligated (HII / BIW)
                        / Next event; the FY28-32 row is highlight-filled as "next"
  • hhi table ......... right table() — Ship system / $M / Suppliers / HHI / Read;
                        the auxiliary "open lane" row is highlight-filled
  • sources_line ...... house Source/Note footnote (the floor-not-census caveat)

Hand-authored from the slide-02 spec (slide_02_recompete_radar.md) on the deck_core
primitives, following the house paint-order + in-place section-header conventions
(no converter provenance — this slide was composed, not ported).
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, tcell_rich, tpara, trun, breadcrumb, title_placeholder, sources_line,
)
from deck_core.style import IN, PT, BLACK, DK, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []

# ── shared rule styles (cell borders; value unchanged across the slide) ──
_RULE_DK = {"color": DK, "width": 12700}        # 1.0pt header / section rule
_RULE_GREY = {"color": "808080", "width": 6350}  # 0.5pt inter-row separator
_HILITE = "CEDDEC"   # light-blue highlight fill — the "next event" / "open lane" rows
_NAVY = "1D4D68"     # big-number accent

# ── layout anchors (shared coordinates) ──
_RAIL_X, _RAIL_W = IN(0.49), IN(4.62)            # left takeaways rail
_COL_X, _COL_W = IN(5.33), IN(7.5)               # right evidence column
_CARD_Y, _CARD_W, _CARD_H = IN(1.62), IN(2.38), IN(0.95)  # big-number card box [x3]

# ── repeated-shape data table (drives the card loop in _body) ──
_SUMMARY_CARDS = [    # (x, big, small) x3 — scale / recurrence / timing
    (5.33, "$3.47B", "first-tier subawards · 521 suppliers"),
    (7.89, "~$1B+", "re-opens with each ~5-yr block"),
    (10.45, "~2028", "next buy (FY28-32) → window ’28–’31"),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome ──
    out.append(breadcrumb("Recompete Cadence", "DDG-51 Supply-Chain Entry"))
    out.append(title_placeholder("Recompete Cadence → Supply-Chain Entry", "The DDG-51 prime is a closed two-yard duopoly you can’t win — but it re-buys on a ~5-year cadence, and each block flows ~$1B+ to a first-tier supplier base; the next wave (FY28-32, ~2028) opens a dated supplier window ~2028–2031."))
    # ── takeaways rail (left) — "Key takeaways" header + one bulleted body cell ──
    out.append(table(n(), "Key takeaways", _RAIL_X, IN(1.62), _RAIL_W, IN(4.85), col_widths=[_RAIL_W], rows=[
        trow([tcell("Key takeaways", size=PT(13), bold=True, color=BLACK, borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK})], h=IN(0)),
        trow([tcell_rich([
            tpara([trun("The cadence is the timing engine. ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("DDG-51 is bought as sequential ~5-year multi-year procurements — FY13-17 → FY18-22 → FY23-27 — so the next block (FY28-32) is due ~2028, readable in the award record today.", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("The prime is closed; the supply chain is the opening. ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("You can’t win the prime (it re-ups to Huntington Ingalls + Bath Iron Works), but each block sub-contracts ~$1B+ to first-tier suppliers — $3.47B across 521 suppliers over the chain.", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("The cadence makes the opportunity datable. ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("~26% of subaward dollars land in the award year and ~80% within four years, so the FY28-32 buy opens a dated supplier window ~2028–2031 — position ahead of the surge, not after it.", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("Concentration is system-specific — that’s the where-to-enter signal. ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("Overall supplier HHI is just 354, but auxiliary systems ($948M, no supplier >16%) is the open lane; propulsion and electric are big but entrenched (GE 35%, Rolls-Royce 43%) — teaming targets.", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
            tpara([trun("Read it honestly. ", size=PT(10), bold=True, color=BLACK, font=FONT), trun("First-tier (FFATA) reporting is a floor, not a census — Bath Iron Works files <5% of HII on the same block, so its chain is dark — and the timing is a demand-surge forecast, not a bid deadline.", size=PT(10), color=BLACK, font=FONT)], bullet=True, mar_l=171450, indent=-171450),
        ], borders={"L": "none", "R": "none", "T": _RULE_DK, "B": "none"})], h=IN(0)),
    ]))
    # ── big-number cards (scale / recurrence / timing) ──
    for _x, _big, _small in _SUMMARY_CARDS:
        out.append(text_box(n(), "Card", IN(_x), _CARD_Y, _CARD_W, _CARD_H, [
            paragraph([run(_big, size=PT(22), bold=True, color=_NAVY, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run(_small, size=PT(10), color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
        ], fill=GRAY_1, line_color="none", anchor="ctr"))
    # ── cadence table (right) — the timing engine ──
    out.append(text_box(n(), "CadenceCaption", _COL_X, IN(2.68), _COL_W, IN(0.2), [paragraph([run("The timing engine — DDG-51 is re-bought every ~5 years, dual-sourced HII + BIW", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(table(n(), "Cadence", _COL_X, IN(2.9), _COL_W, IN(1.4), col_widths=[IN(1.25), IN(1.55), IN(2.85), IN(1.85)], rows=[
        trow([tcell("Block", size=PT(10), bold=True, color=BLACK, borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("Awarded", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("Prime obligated to date (HII / BIW)", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("Next event", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK})], h=IN(0)),
        trow([tcell("FY13-17 MYP", size=PT(10), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell("2013-06-03", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell("$3.35B / $4.93B", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell("—", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("FY18-22 MYP", size=PT(10), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("2018-09-27", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("$6.83B / $5.34B", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("—", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("FY23-27 MYP", size=PT(10), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("2023-08-01", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("$6.95B / $5.03B", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("—", size=PT(10), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("FY28-32 MYP", size=PT(10), bold=True, color=BLACK, fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("~2028 (forecast)", size=PT(10), bold=True, color=BLACK, align="ctr", fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("not yet awarded", size=PT(10), bold=True, italic=True, color=BLACK, align="ctr", fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("next sourcing wave", size=PT(10), bold=True, color=BLACK, align="ctr", fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"})], h=IN(0)),
    ]))
    # ── hhi table (right) — where to enter (reported first-tier $) ──
    out.append(text_box(n(), "HhiCaption", _COL_X, IN(4.62), _COL_W, IN(0.2), [paragraph([run("Where to enter — reported first-tier $ concentration by ship system (HHI)", size=PT(10), bold=True, color=BLACK, font=FONT)], mar_l=0, indent=0, line_spacing=100000)], fill=None, line_color="none", anchor="b", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(table(n(), "HHI", _COL_X, IN(4.84), _COL_W, IN(1.6), col_widths=[IN(2.25), IN(0.62), IN(0.95), IN(0.72), IN(2.96)], rows=[
        trow([tcell("Ship system", size=PT(10), bold=True, color=BLACK, borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("$M", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("Suppliers", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("HHI", size=PT(10), bold=True, color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK}), tcell("Read", size=PT(10), bold=True, color=BLACK, borders={"L": "none", "R": "none", "T": "none", "B": _RULE_DK})], h=IN(0)),
        trow([tcell("Auxiliary systems", size=PT(9), color=BLACK, fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell("948", size=PT(9), color=BLACK, align="ctr", fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell("90", size=PT(9), color=BLACK, align="ctr", fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell("683", size=PT(9), color=BLACK, align="ctr", fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY}), tcell_rich([tpara([trun("Open lane", size=PT(9), bold=True, color=BLACK, font=FONT), trun(" — no supplier >16%", size=PT(9), color=BLACK, font=FONT)], mar_l=0, indent=0)], fill=_HILITE, borders={"L": "none", "R": "none", "T": _RULE_DK, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("Propulsion plant", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("958", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("29", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("1,905", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("Entrenched (GE 35%) — team", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("Electric plant", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("751", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("24", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("2,106", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("Entrenched (Rolls-Royce 43%) — team", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("Command, control & surv.", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("48", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("7", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("2,188", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY}), tcell("Concentrated, small", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": _RULE_GREY})], h=IN(0)),
        trow([tcell("Armament", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("2", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("2", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("6,561", size=PT(9), color=BLACK, align="ctr", borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"}), tcell("Locked (Lake Shore 78%)", size=PT(9), color=BLACK, borders={"L": "none", "R": "none", "T": _RULE_GREY, "B": "none"})], h=IN(0)),
    ]))
    # ── house Source/Note footnote ──
    out.append(sources_line("Note: First-tier (FFATA) subawards are first-tier only, lag 6–18 months, and are under-reported (Bath Iron Works ≪ Huntington Ingalls — BIW files <5% of HII on the same block), so every subaward total is a floor and the HHI / where-to-enter read is on reported dollars; the supplier “recompete” is a forecastable demand surge on the prime’s ~5-year cadence, not a date-certain ordering-period end; subaward dollars mapped to ship work-breakdown system (SWBS) via the program-workbook crosswalk (81% of dollars map) | Source: SAM.gov Contract Awards + USAspending (prime cadence, dollars, dates; multiyear basis 10 U.S.C. 3501 / FAR Subpart 17.1); SAM.gov Subaward Reporting (FFATA) for the first-tier supplier base, corroborated against the Distributed Shipbuilding extract. As of 2026-06-24"))
    return "".join(out)


def render() -> str:
    return slide(_body())
