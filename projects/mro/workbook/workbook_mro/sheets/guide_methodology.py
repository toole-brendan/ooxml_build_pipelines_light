"""Methodology

INTENT
    Analytical method tab: definitions, the formula framework (two-universe TAM/SAM
    model), the market-sizing flow, the scope boundary, exclusion rules, and the
    appropriation map (no-double-count across 1804N OMN / 1810N OPN / SCN / WPN / MSC /
    USCG). Table-first; a few headline figures link in live via the Reconciliation /
    Services accessors.

LAYOUT
    row 2 : title
    §1 definitions · §2 formula framework · §3 market-sizing flow · §4 scope boundary
    · §5 exclusion rules · §6 appropriation map
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_LINK_NUM,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets.model_reconciliation import (
    reconciled_mro_tam_cell, psc1905_mro_cell,
)
from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell

_GROUP = "guide"
_TAB = "Methodology"
_NCOLS = 3


def _sc(s: str) -> str:
    """Sentence-case a prose value: capitalize a lowercase first letter, leaving codes,
    acronyms (FPDS/OP-5/PSC), and digit-leading strings untouched."""
    return s[:1].upper() + s[1:] if s and s[0].islower() else s


def _render_methodology() -> WorksheetSpec:
    # outline_default=1: every content row (definitions, framework lines, tables) collapses
    # under its section/sub-section banner.
    c = RowCursor(2, outline_default=1)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Definitions
    c.banner("§1 - Definitions", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Term", "Definition"], styles=S_HEADER_LEFT)
    for term, defn in [
        ("MRO", "vessel maintenance, repair, and overhaul (depot + intermediate)"),
        ("Services-MRO TAM", "FPDS-visible MRO over the 65 J/K/N/M/H/L services PSCs"),
        ("Embedded MRO", "ship MRO booked under shipbuilding PSC 1905 (complex overhaul / RCOH)"),
        ("Reconciled MRO TAM", "services-MRO (Navy+USCG) + embedded PSC 1905 MRO (the one TAM)"),
        ("Budget-anchored MRO funding pot", "the top-down appropriation pot (OP-5 1B4B + MSC + SCN + OPN + USCG, incl. Public NSY); WPN is a memo, not in the pot"),
        ("Bottom-up universe", "FPDS award data summed over the 65 MRO PSCs"),
        ("Captive (SUPSHIP) MRO", "PSC 1905 MRO at HII / Electric Boat / GD / Fluor yards"),
        ("Non-public-NSY funding", "budget pot less Public NSY (~$9.5B): a funding cross-check vs the Reconciled MRO TAM, NOT a separate TAM"),
        ("Broad Addressable", "Reconciled MRO TAM less captive SUPSHIP OH and FMS (~$7.1B): the private-contestable SAM base (a SAM rung, not a TAM)"),
        ("Public NSY", "the four naval shipyards (intramural federal workforce)"),
        ("FMS", "foreign military sales work"),
        ("TAM atom", "one mutually-exclusive slice of TAM (a source award / PIID row), tagged on every SAM axis; SUM(atoms) = Reconciled TAM"),
        ("SAM", "a scenario-selected SUBSET of TAM atoms (within-axis OR, across-axis AND) - a menu of overlapping options, NOT a second TAM and NOT to be summed"),
        ("Addressability", "a scope-class flag on each atom (Addressable / Captive SUPSHIP / FMS), not a separate TAM"),
        ("Target hull set", "the marauder-like 14-hull comp-set (auxiliary / patrol / logistics); the Target Hull Set Depot MRO scenario"),
        ("SOM", "share a competitor could realistically win"),
    ]:
        c.write([term, _sc(defn)], styles=[S_BOLD, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Formula framework
    c.banner("§2 - Formula framework", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - TAM framework", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Reconciled MRO TAM = Navy services-MRO + USCG services-MRO + embedded PSC 1905 MRO"], styles=[S_DEFAULT])
    c.blank()                              # generated spacer: keeps row numbers deterministic
    c.write(["Component (live)", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Navy + USCG services-MRO (65 PSCs)", f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}"],
            styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.write(["Embedded PSC 1905 MRO", f"={psc1905_mro_cell('EMBEDDED')}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["Reconciled FPDS-visible MRO TAM", f"={reconciled_mro_tam_cell()}"],
            styles=[S_BOLD, S_LINK_NUM], outline_level=1)
    c.blank()
    c.banner("§2b - The two-universe model", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Universe", "Built from", "Sizes"], styles=S_HEADER_LEFT)
    for u, src, sizes in [
        ("Top-down (budget pot)", "OP-5 1B4B avail categories + MSC + SCN CVN RCOH + OPN LI 1000 + USCG ISVS",
         "the appropriated maintenance budget (~$17B incl. public NSY)"),
        ("Bottom-up (award data)", "FPDS obligations summed over the 65 MRO PSCs (+ embedded PSC 1905)",
         "the contractor-visible market (~$9B)"),
    ]:
        c.write([u, _sc(src), _sc(sizes)], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§2c - Non-public-NSY bridge & Broad Addressable", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Non-public-NSY funding cross-check = Budget-anchored MRO funding pot - Public NSY  (~$9.5B; a funding-side check vs the $9.0B Reconciled MRO TAM, ~6% apart). NOT a TAM."], styles=[S_DEFAULT])
    c.write(["Broad Addressable (SAM entry) = Reconciled MRO TAM - captive SUPSHIP complex OH - FMS  (~$7.1B private-contestable base; computed on the TAM atoms / SAM Build, NOT subtracted from TAM here)."], styles=[S_DEFAULT])
    c.blank()
    c.banner("§2d - SAM scenario engine", n_cols=_NCOLS, style=S_TITLE_SUBSECTION,
             mark_collapsible=True)
    c.blank()
    for line in [
        "SAM = a scenario-selected subset of the TAM atoms (Scenarios matrix -> SAM Build); one headline TAM, not a second one.",
        "Each atom carries one bucket per axis: work segment, hull, buyer/RMC, contractor tier, IDV scope, scope class, service.",
        "Inclusion: within an axis OR (multiple buckets flagged 1), across axes AND (an atom must clear every axis).",
        "Scenario SAMs are a MENU of overlapping options - do NOT sum them (overlaps can exceed TAM).",
        "Addressability is a scope-class flag on each atom (Addressable / Captive / FMS), NOT a separate TAM.",
    ]:
        c.write([line], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 Market-sizing flow
    c.banner("§3 - Market-sizing flow", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "Input", "Method"], styles=S_HEADER_LEFT)
    for step, inp, method, _tab in [
        ("Tag MRO awards", "FPDS award master", "65-PSC filter + Is MRO flag", "Awards"),
        ("Sum services-MRO TAM", "tagged awards", "SUMIFS by PSC x service", "Services"),
        ("Add embedded MRO", "PSC 1905 classified", "bucket SUMIFS (complex OH / RCOH)", "PSC 1905 Classified"),
        ("Reconcile vs top-down", "OP-5 / MSC / SCN / OPN / USCG", "appropriation roll-up", "Reconciliation / TAM Bridge"),
        ("Non-public-NSY cross-check & Broad Addressable", "budget pot / TAM", "pot - Public NSY (~$9.5B); TAM - captive - FMS (~$7.1B)", "Non-Public-NSY Bridge"),
        ("Cut into work segments", "services-MRO TAM", "work-segment partition of the 65 PSCs", "Services / Output"),
        ("Build TAM atoms", "Awards + J998J999 + PSC 1905", "one tagged atom per source row; SUM = Reconciled TAM", "TAM Atoms"),
        ("Select a SAM scenario", "TAM atoms + Scenarios matrix", "SUMPRODUCT(atom $, scenario flags); a menu - not summed", "Scenarios / SAM Build"),
    ]:
        c.write([step, _sc(inp), _sc(method)], styles=S_DEFAULT, outline_level=1)
    c.blank(2)

    # §4 Scope boundary
    c.banner("§4 - Scope boundary", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§4a - In scope", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in ["Depot & intermediate ship maintenance, repair & overhaul (the 65 MRO PSCs)",
                "Private-yard and RMC-contracted availabilities (OH / SRA / PIA / DSRA / CM)",
                "Embedded ship MRO booked under PSC 1905 (complex overhaul, CVN RCOH)",
                "Husbanding & port services tied to vessel availabilities"]:
        c.write([_sc(txt)], styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§4b - Out of scope", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in ["Public NSY intramural labor (federal civilian workforce, not contracted)",
                "New construction / shipbuilding (except the embedded-MRO PSC 1905 slice)",
                "GFE weapons / combat-systems procurement (WPN missile/torpedo lines)",
                "Foreign Military Sales (FMS) work",
                "O&S operating costs not tied to a maintenance availability"]:
        c.write([_sc(txt)], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 Exclusion rules
    c.banner("§5 - Exclusion rules", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Exclusion category", "Rationale", "Evidence tab"], styles=S_HEADER_LEFT)
    for cat, why, tab in [
        ("Public NSY labor", "intramural federal workforce, invisible to FPDS", "TAM Bridge"),
        ("Captive SUPSHIP OH", "HII/EB/GD/Fluor complex OH not competable; excluded at the SAM addressability rung (Broad Addressable)", "SAM Build"),
        ("GFE / WPN weapons", "combat-systems procurement, not ship depot work", "Reconciliation"),
        ("FMS", "foreign sales; excluded at the SAM addressability rung (Broad Addressable)", "SAM Build"),
        ("New construction (non-1905)", "shipbuilding, not MRO", "Awards"),
        ("Double-count OMN vs OPN", "1804N OMN and 1810N OPN are parallel streams - count once", "Reconciliation"),
    ]:
        c.write([cat, _sc(why), tab], styles=S_DEFAULT, outline_level=1)
    c.blank(2)

    # §6 Appropriation map (no double-count)
    c.banner("§6 - Appropriation map", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Appropriation", "Scope", "MRO treatment"], styles=S_HEADER_LEFT)
    for appn, scope, treat in [
        ("OMN 1804N (SAG 1B4B)", "Navy ship operations & maintenance", "primary private-yard ship-maintenance pot (OP-5 Table IV)"),
        ("OPN 1810N (LI 1000)", "private contracted CONUS surface/sub maintenance at CPF/FFC", "PARALLEL to 1B4B (PL 116-93); counted once, not double-counted"),
        ("SCN (LI 2086)", "CVN refueling complex overhaul (RCOH)", "multi-year incremental; the embedded-MRO bridge component"),
        ("WPN", "missile / torpedo / weapons procurement", "out of scope except the ~$500M combat-systems plug (Assumptions §2)"),
        ("MSC (OMN)", "Military Sealift Command M&R", "FY25 executes 1B1B, transfers to 1B4B in FY26"),
        ("USCG (PC&I / O&S)", "Coast Guard cutter sustainment (ISVS)", "no OP-5 equivalent; bottom-up FPDS is the better anchor"),
    ]:
        c.write([appn, _sc(scope), _sc(treat)], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)

    ws = worksheet(c.rows, cols=[26, 46, 40], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


METHODOLOGY = SheetEntry(_TAB, _GROUP, _render_methodology)
