"""hii_co_build - the HII-Newport News co-build workshare that the subaward data can't see.

The first-order honesty layer for the submarine programs. The build runs under a Navy-
directed teaming arrangement with GDEB as sole prime; the HII-Newport News co-build
workshare flows through GDEB and is almost entirely absent from the FFATA/FSRS subaward
universe the program-vendor and Domain Concentration sheets are computed over. This sheet
quantifies that missing mass from primary issuer disclosures (HII announcements + SEC),
clearly labelled as non-transactional, so a reader never mistakes "share of reported
subcontracted scope" for "share of total boat construction."

Static reference memo (no live formulas - these are cited disclosures, not corpus roll-
ups). `guide` group. Sources are listed in §6.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_TITLE_SHEET, S_TITLE_SECTION, S_NUM,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_award_classification_refactor.sheets._layout import RowCursor
from workbook_award_classification_refactor.sheets._italic import S_ITALIC
from workbook_award_classification_refactor.sheets._tabs import TAB_HII_CO_BUILD

_GROUP = "data"
_NCOLS = 6
_COLS = [24, 12, 12, 14, 18, 38]

INTRO = ("Issuer-disclosed HII-Newport News co-build workshare excluded from reported "
         "subaward totals.")

# --- §1 two-tier framing -------------------------------------------------------------
TIER = [
    "The boat splits into two reporting tiers, and only one is in the subaward data:",
    "Subcontractable tier - GDEB first-tier subawards to the supplier base. This is the "
    "FFATA/FSRS data; the Domain Concentration sheet is the supplier-base view of it.",
    "Co-build tier - the GDEB / HII Newport News workshare under the Navy-directed teaming "
    "arrangement. It is allocated by the co-build structure, not won as a subaward, so it is "
    "almost entirely absent from FFATA and is quantified below from issuer disclosures.",
]

# --- §2 what the subaward data captures for HII --------------------------------------
VISIBLE = [
    "What the subaward universe contains for HII-NNS on these programs (this workbook):",
    "Virginia: about $98M - EB purchase orders to Huntington Ingalls Inc (UEI WMXDDH6HJNA5, "
    "about $98.1M on the Block V/VI master + VPM primes) plus Newport News Nuclear (UEI "
    "CR39JL3216G7, about $0.3M). Columbia: $0.00.",
    "So HII's reported subaward footprint is about $98M against a co-build workshare in the "
    "tens of billions - roughly 0.1-0.2% of the real workshare. It is netted out on the Market "
    "Bridge co-build scenario; the rest is the gap quantified below.",
]

# --- §3 issuer-disclosed subcontract ledger: (program, announced, action$M, cumulative$M, basis, scope)
LEDGER_HDR = ["Program", "Announced", "Action $M", "Cumulative $M", "Amount basis", "Scope"]
LEDGER = [
    ("Columbia",        "Dec 2017", None,   468.0,  "Ceiling",                 "Integrated product & process development (ceiling; not necessarily funded)"),
    ("Columbia",        "Nov 2018", 197.0,  None,   "Incremental modification", "Long-lead material + advance construction"),
    ("Columbia",        "Nov 2020", 2200.0, None,   "Incremental modification", "Design support + modules, first two boats (about $2.2B)"),
    ("Columbia",        "Apr 2023", 567.6,  None,   "Incremental modification", "Build II LLTM + advance construction"),
    ("Virginia Blk V",  "Apr 2019", 727.4,  1040.0, "Incremental modification", "AP mod; brings AP contract to $1.04B"),
    ("Virginia Blk V",  "Mar 2021", None,   9800.0, "Cumulative disclosed value", "Option exercised; total NN contract value $9.8B"),
    ("Virginia Blk V",  "May 2023", 305.2,  10200.0,"Cumulative disclosed value", "Mod; updated overall value $10.2B (strongest public Virginia figure)"),
]
# The non-additivity warning lives in a Note on the Cumulative $M header (below), not as a
# visible all-caps paragraph.
CUM_NOTE = ("Not additive down the column: amounts are basis-typed, and a cumulative value "
            "already contains the prior incremental mods. Build a program total row by row "
            "with lineage. The strongest single public figure is the HII-NNS Block V contract "
            "value of about $10.2B as of 2023-05-24 (a disclosed cumulative value); prefer it "
            "over the looser CRS percentage for Virginia headlines.")

# --- §4 CRS workshare cross-check ----------------------------------------------------
CRS = [
    "CRS / prime-announcement workshare (order-of-magnitude cross-check on the disclosed figures):",
    "Virginia: about 50% co-builder (CRS RL32418); the Block V prime announcement allocates "
    "about 25% place-of-performance to Newport News. Columbia: about 22-23% (CRS R41129); the "
    "2017 design award shows 12.7% NN place-of-performance.",
    "Applied to EB's multi-billion Virginia/Columbia construction prime base, this implies an "
    "HII co-build workshare in the tens of billions - consistent with the $10.2B Block V "
    "disclosure above. This is a derived estimate; label each figure by basis and never mix "
    "CRS percentages with disclosed dollars.",
]

# --- §5 public bound -----------------------------------------------------------------
BOUND = [
    "Public hard bound (HII SEC 10-K / earnings): HII Newport News segment revenue is about "
    "$6.0B/yr (2023; about $1.5B in Q2-2023), submarine + carrier combined. HII does not "
    "separately break out submarine revenue in the 10-K, so this caps - does not pinpoint - "
    "HII submarine work. Even so it dwarfs the about-$98M reported subaward footprint, "
    "corroborating the scale of the reporting gap.",
]

# --- §6 sources ----------------------------------------------------------------------
SOURCES = [
    "CRS (C. O'Rourke): RL32418 Virginia-Class Submarine Program; R41129 Columbia-Class.",
    "DoD/DoW contract announcements: N00024-20-C-2120 (Lead Yard Support, Virginia); 2019-12-02 "
    "Block V (N00024-17-C-2100, GDEB prime / HII major subcontractor, about 25% NN place-of-"
    "performance); 2017-09-21 Columbia design (N00024-17-C-2117, 12.7% NN place-of-performance).",
    "HII issuer disclosures (hii.com newsroom) + SEC 10-K (EDGAR CIK 1501585); GD Electric Boat releases.",
    "Mechanism: FAR 52.204-10 (FFATA first-tier subcontract reporting). HII characterises these "
    "as EB subcontract modifications, so the absence is a reporting / data-treatment gap, not a "
    "clean teaming carve-out and not proof that no reportable subcontract existed.",
]


def _para(c, lines, lead_style=S_BOLD):
    for i, ln in enumerate(lines):
        c.write([ln], styles=[lead_style if i == 0 else S_DEFAULT], outline_level=1)


def _make_hii_co_build():
    def render() -> WorksheetSpec:
        c = RowCursor(2)
        c.banner(TAB_HII_CO_BUILD, n_cols=_NCOLS, style=S_TITLE_SHEET)
        c.write([INTRO], styles=[S_ITALIC])
        c.blank(2)

        c.banner("§1 - Two reporting tiers", n_cols=_NCOLS, style=S_TITLE_SECTION,
                 mark_collapsible=True)
        _para(c, TIER)
        c.blank(2)

        c.banner("§2 - What the subaward data captures for HII",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        _para(c, VISIBLE)
        c.blank(2)

        c.banner("§3 - Issuer-disclosed subcontract ledger",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        hdr = c.write(LEDGER_HDR, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 5)
        for prog, dt, act, cum, basis, scope in LEDGER:
            c.write([prog, dt, act, cum, basis, scope],
                    styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_NUM, S_DEFAULT, S_DEFAULT],
                    outline_level=1)
        c.write(["Amounts are basis-typed; cumulative values already include the prior "
                 "incremental mods, so the column is not additive (see the note on Cumulative $M)."],
                styles=[S_ITALIC], outline_level=1)
        c.blank(2)

        c.banner("§4 - CRS / announcement workshare cross-check",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        _para(c, CRS)
        c.blank(2)

        c.banner("§5 - Public bound (SEC 10-K segment)",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        _para(c, BOUND, lead_style=S_DEFAULT)
        c.blank(2)

        c.banner("§6 - Sources", n_cols=_NCOLS, style=S_TITLE_SECTION,
                 mark_collapsible=True)
        _para(c, SOURCES, lead_style=S_DEFAULT)

        # Non-additivity warning as a hover Note on the Cumulative $M header (col E).
        notes = [ExcelNote(f"E{hdr}", CUM_NOTE)]
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, show_outline_symbols=True)
        return WorksheetSpec(ws, notes=notes)

    return SheetEntry(TAB_HII_CO_BUILD, _GROUP, render)


HII_CO_BUILD = _make_hii_co_build()
