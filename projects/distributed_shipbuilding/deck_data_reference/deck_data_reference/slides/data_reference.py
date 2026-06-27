"""data_reference — deck_data_reference slide 1 (Award Analysis / Data Reference).

Lifted verbatim from the deck_primary pipeline (where it was slide 8) into this
standalone single-slide deck; the exhibit body below is unchanged.

EXHIBIT — "Data Reference": a fill-free methodology-backup exhibit — horizontal
rules only (no cell fills), keyed to the hull-builder new-construction subaward
pull:
  1. In-scope PIIDs — the hull-builder new-construction contract scope, one row per
     platform (SSN · Virginia, SSBN · Columbia, DDG · DDG-51).
  2. Classification archetypes — the two published axes the analysis assigns per
     vendor: Capability Domain (D0–D11, what technical ship area the vendor
     supports) and Primary Output (P0–P6, what physically leaves the vendor),
     shown side by side with a one-line "what it covers" for each archetype.
  3. Award field sample — four raw FSRS / SAM.gov first-tier subaward records
     showing the NATIVE pull fields (PIID · subawardee · UEI · date · $M ·
     NAICS-4 · report id); Capability Domain / Primary Output are classified
     downstream from the vendor, not part of the pull.
A sources line closes it out.

CODE MAP (body follows source PAINT ORDER; the section headers mark roles in place):
  • chrome ......... breadcrumb() + prelim_chip() + title_placeholder() (house builders)
  • in-scope PIIDs . table() "data_ref_piids" — 4 rows × 2 cols
  • domain axis .... table() "data_ref_domains" — 13 rows × 3 cols (left)
  • output axis .... table() "data_ref_outputs" — 8 rows × 3 cols (right)
  • award sample ... table() "data_ref_award_fields" — 5 rows × 7 cols
  • sources ........ one text_box() (kept verbatim — sits off the house Source position)

Data refresh (2026-06-26): re-pointed to the updated SAM classification workbook
(workbook_award_classification_refactor). The seven NAICS-4 work-type buckets are
retired in favour of the two published archetype axes (D / P); the in-scope PIID
set is narrowed to the hull-builder-only scope (GDEB subs; GD-BIW + HII-Ingalls
DDG-51), which leaves Columbia a single in-scope construction PIID; and the award
sample's one out-of-scope row (Scot Forge under the Columbia design PIID) is
swapped for the same vendor's in-scope record under N0002417C2117. The taxonomy
vocabulary is quoted from the workbook's _taxonomy.py (DOMAINS / OUTPUTS), with the
"what it covers" column condensed for the slide. Table primitives unchanged
(general table()/trow()/tcell()); this is a content/data edit, so the render is NOT
byte-identical to the prior build.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, table, trow, tcell, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, DK, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── classification vocabulary (quoted from the SAM workbook's _taxonomy.py;
#    the "what it covers" text is condensed for the slide) ──
# Capability Domain (D) — the technical ship area the vendor supports.
DOMAINS: list[tuple[str, str, str]] = [
    ("D1",  "Hull, Structures & Marine Fabrication",                    "Hull, decks, weldments, foundations"),
    ("D2",  "Propulsion & Power-Transmission Machinery",                "Turbines, gears, shafting, propulsors"),
    ("D3",  "Electrical Power — Generation, Conversion & Distribution", "Generators, switchboards, switchgear"),
    ("D4",  "Fluid, Pressure & Piping Systems",                         "Valves, pumps, manifolds, piping"),
    ("D5",  "Thermal, HVAC & Life-Support",                             "Chillers, HVAC, heat exchangers"),
    ("D6",  "Mission, Combat & Communications Systems",                 "Sonar, radar, fire-control, ordnance"),
    ("D7",  "Electronic Components, Interconnect & Cable",              "Penetrators, connectors, cable, harnesses"),
    ("D8",  "Mechanical Handling & Deck Machinery",                     "Davits, cranes, hoists, handling gear"),
    ("D9",  "Specialty Materials & Precision Processes",               "Forging, casting, machining, composites"),
    ("D10", "Interiors, Habitability & Outfitting",                     "Furniture, berthing outfit, insulation"),
    ("D11", "Services & Non-Material Support",                          "Engineering, repair, logistics, software"),
    ("D0",  "Unresolved / Insufficient Evidence",                      "No single domain defensible; thin evidence"),
]
# Primary Output (P) — what physically leaves the vendor.
OUTPUTS: list[tuple[str, str, str]] = [
    ("P1", "Materials, Stock & Bulk Inputs",          "Plate, bar, forgings, castings"),
    ("P2", "Finished Parts & Fabricated Components",   "Machined parts, fittings, pipe spools"),
    ("P3", "Functional Equipment & Machinery",         "Engines, pumps, valves, switchboards"),
    ("P4", "Integrated Systems & Configured Shipsets", "Sonar shipsets, drive packages"),
    ("P5", "Outfitted Structures & Ship Modules",      "Hull units, outfitted modules"),
    ("P6", "Services & Technical Work Products",        "Engineering, test, install, repair"),
    ("P0", "Unresolved / Attribution-Only",            "No defensible output; attribution-only"),
]

# In-scope hull-builder new-construction PIIDs (prime_contract_scope.csv, include=Y).
PIID_ROWS: list[tuple[str, str]] = [
    ("SSN · Virginia",
     "N0002409C2104, N0002410C2118, N0002412C2115, N0002416C2111, N0002417C2100, N0002424C2110"),
    ("SSBN · Columbia",
     "N0002417C2117"),
    ("DDG · DDG-51",
     "N0002402C2303, N0002402C2304, N0002403C2306, N0002409C2302, N0002411C2305, N0002411C2307, "
     "N0002411C2309, N0002413C2305, N0002413C2307, N0002418C2305, N0002418C2307, N0002423C2305, "
     "N0002423C2307"),
]

# Award field sample — raw FSRS records (native pull fields). Row 3 uses Scot Forge's
# IN-SCOPE Columbia record under N0002417C2117 (was the out-of-scope N0002413C2128).
AWARD_SAMPLE: list[tuple[str, ...]] = [
    ("N0002412C2115", "BAKER SHEET METAL CORPORATION", "RYRLL49HWN65", "2016-02-03", "0.085", "3323", "20692413"),
    ("N0002412C2115", "ARNOLD MAGNETICS CORPORATION",  "RK6GKSXPC8W7", "2016-02-03", "0.134", "3359", "20692322"),
    ("N0002417C2117", "SCOT FORGE COMPANY",            "N1PJDANWUJ61", "2022-10-28", "0.081", "3321", "20960134"),
    ("N0002411C2307", "WESTLAND TECHNOLOGIES, INC.",   "HMBSX7Z72UK4", "2013-05-09", "0.106", "3262", "20684452"),
]


# ── table-cell layout commentary ──
# Each table(): col_widths is column-level geometry; trow(h=...) is a MINIMUM row
# height (LibreOffice grows a wrapped row past it — see the
# house-table-row-height-is-a-minimum note). Cells are the plain tcell() helper
# with no fills (the "rule" skin); per-cell borders={"B": ...} draw the
# horizontal rules — 19050 EMU (1.5pt) under each header row, 12700 (1pt) between
# body rows, "none" on each block's last row. The two archetype tables sit side by
# side (D left, P right) because the axes are independent; the longer Capability
# Domain table governs the block height.

_NB = {"L": "none", "R": "none", "T": "none"}   # no side / top rules


def _hb():    # header bottom rule (1.5pt)
    return {**_NB, "B": {"color": BLACK, "width": 19050}}


def _bb(last: bool):   # body bottom rule (1pt), "none" on the block's last row
    return {**_NB, "B": "none"} if last else {**_NB, "B": {"color": BLACK, "width": 12700}}


def _tax_rows(items: list[tuple[str, str, str]], axis_header: str) -> list:
    """Build a code / archetype / what-it-covers table body for one axis."""
    rows = [trow([
        tcell("", size=PT(8), bold=True, color=BLACK, anchor="t", borders=_hb()),
        tcell(axis_header, size=PT(8), bold=True, color=BLACK, anchor="t", borders=_hb()),
        tcell("What it covers", size=PT(8), bold=True, color=BLACK, anchor="t", borders=_hb()),
    ], h=IN(0.2))]
    for i, (code, name, covers) in enumerate(items):
        b = _bb(i == len(items) - 1)
        rows.append(trow([
            tcell(code, size=PT(8), bold=True, color=BLACK, anchor="t", borders=b),
            tcell(name, size=PT(8), bold=True, color=BLACK, anchor="t", borders=b),
            tcell(covers, size=PT(8), color=BLACK, anchor="t", borders=b),
        ], h=IN(0.17)))
    return rows


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome ──
    out.append(breadcrumb("Award Analysis", "Data Reference"))
    out.append(prelim_chip())
    out.append(title_placeholder("Data Reference", "Scope PIIDs, the Capability-Domain and Primary-Output archetypes, and the native subaward fields the analysis reads."))
    # ── in-scope PIIDs — hull-builder new-construction contract scope, one row per platform ──
    piid_rows = [trow([
        tcell("Platform", size=PT(8), bold=True, color=BLACK, anchor="t", borders=_hb()),
        tcell("Hull-builder new-construction contract PIIDs", size=PT(8), bold=True, color=BLACK, anchor="t", borders=_hb()),
    ], h=IN(0.233))]
    for i, (plat, piids) in enumerate(PIID_ROWS):
        b = _bb(i == len(PIID_ROWS) - 1)
        piid_rows.append(trow([
            tcell(plat, size=PT(8), bold=True, color=BLACK, anchor="t", borders=b),
            tcell(piids, size=PT(8), color=BLACK, anchor="t", borders=b),
        ], h=IN(0.233)))
    out.append(table(n(), "data_ref_piids", IN(0.495), IN(1.4), IN(12.339), IN(1.0),
                     col_widths=[IN(1.64), IN(10.698)], rows=piid_rows))
    # ── classification archetypes — two published axes, side by side (D left, P right) ──
    out.append(table(n(), "data_ref_domains", IN(0.495), IN(2.55), IN(6.0), IN(2.6),
                     col_widths=[IN(0.4), IN(2.8), IN(2.8)],
                     rows=_tax_rows(DOMAINS, "Capability Domain (D)")))
    out.append(table(n(), "data_ref_outputs", IN(6.834), IN(2.55), IN(6.0), IN(1.6),
                     col_widths=[IN(0.4), IN(2.8), IN(2.8)],
                     rows=_tax_rows(OUTPUTS, "Primary Output (P)")))
    # ── award field sample — raw FSRS subaward records (native pull fields) ──
    aw_cols = [IN(1.64), IN(3.336), IN(1.64), IN(1.367), IN(0.93), IN(1.094), IN(2.332)]
    aw_hdr = [("PIID", "t"), ("Subawardee", "t"), ("Subawardee UEI", "t"), ("Award date", "ctr"),
              ("$M", "r"), ("NAICS-4", "ctr"), ("Report ID", "t")]
    aw_rows = [trow([tcell(t, size=PT(8), bold=True, color=BLACK, align=a, anchor="t", borders=_hb())
                     for (t, a) in aw_hdr], h=IN(0.233))]
    aligns = ["t", "t", "t", "ctr", "r", "ctr", "t"]
    for i, rec in enumerate(AWARD_SAMPLE):
        b = _bb(i == len(AWARD_SAMPLE) - 1)
        cells = []
        for j, val in enumerate(rec):
            cells.append(tcell(val, size=PT(8), bold=(j == 0), color=BLACK, align=aligns[j], anchor="t", borders=b))
        aw_rows.append(trow(cells, h=IN(0.233)))
    out.append(table(n(), "data_ref_award_fields", IN(0.495), IN(5.3), IN(12.339), IN(1.167),
                     col_widths=aw_cols, rows=aw_rows))
    # ── sources (kept verbatim — sits off the house Source position) ──
    out.append(text_box(n(), "Sources", IN(0.495), IN(6.75), IN(12.339), IN(0.7), [paragraph([run("FSRS / SAM.gov first-tier subaward pull, hull-builder new-construction PIIDs (GDEB submarines; GD-BIW + HII-Ingalls DDG-51). Design-engineering, ship-alteration, planning-yard and GFE-prime contracts are out of scope — leaving Columbia one in-scope construction PIID. Capability Domain and Primary Output are classified downstream from the vendor, not the award text.", size=PT(8), color=DK, font=FONT)], line_spacing=100000)], fill=None, line_color="none", l_ins=91440, t_ins=45720, r_ins=91440, b_ins=45720))
    return "".join(out)


def render() -> str:
    return slide(_body())
