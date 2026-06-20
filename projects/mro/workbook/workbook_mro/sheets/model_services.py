"""Services

INTENT
    PSC x hull/vessel SUMIFS cross-tabs that derive the FY2025 services-PSC MRO TAM,
    plus the budget-book reconciliation and prime-landscape blocks. The §1-§3 cross-tabs
    are Python loops over the _crosstab axis constants emitting sumifs_award(...) over
    the ``Awards`` table; structured refs are position-independent so the loop reproduces
    the cross-tab formulas (proven by qa/verify_crosstab; the soffice tie-out backstops).
    §4-§14 are explicit blocks with captured row positions and intra-sheet refs.

    §4 derives the Navy / Coast Guard TAM cells and exposes navy_tam_svc_cell /
    cg_tam_svc_cell (the Reconciliation<->Services cycle nodes - Reconciliation imports
    them lazily in its render). §6/§7 read the Reconciliation budget anchors (MRO_TAS_* /
    OMN_* / USCG_ISVS_*) through that sheet's import-time accessors via the local _ref()
    resolver.

LAYOUT
    row 2 : title
    §1-§3 cross-tabs · §4 TAM (producer) · §5 by work segment · §6/§7 budget
    reconciliation + anchors · §9 coverage · §10 top-10 contractors · §11 HII margin
    · §12 segment share · §13/§14 vessel-type x work-segment ($M / %)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_NUM_INPUT, S_PCT, S_PCT_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION, S_LABEL_INDENT_1,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets._crosstab import (
    PSC_ROWS, VESSEL_TYPES, HULL_PROGRAMS_NAVY, HULL_PROGRAMS_CG, WORK_SEGMENTS,
    sumifs_award, axis_crit,
)
# §6/§7 read the Reconciliation budget anchors via these import-time accessors. Safe at
# module load: the Reconciliation<->Services cycle is broken on Reconciliation's side,
# which imports Services lazily inside its render() - so model_reconciliation fully
# imports without touching this module.
from workbook_mro.sheets.model_reconciliation import mro_tas_cell, omn_cell, uscg_isvs_cell

_GROUP = "model"
_TAB = "Services"
_NCOLS = 32                     # widest section (§2: B..AG); banners span the sheet
_VAL = "FY2025 Obligation"      # the Awards value column for every SUMIFS here
# v4.33 column widths (B onward); the gutter width is prepended by worksheet().
_COLS = [7.0, 38.0] + [12.0] * 14 + [14.0, 14.0] + [12.0] * 10 + [14.0, 14.0]

# §13 vessel categories = the first five (named) vessel types; "Other" is the residual.
_S13_CATS = VESSEL_TYPES[:5]

# Plus-join SUMIFS terms; spacing is value-irrelevant.
def _plus(terms):
    return "+".join(terms)


def _sum_over_pscs(pscs, *extra_crit):
    """(sum of sumifs_award over `pscs` with the shared extra criteria)."""
    return _plus(sumifs_award(_VAL, ("PSC", p), *extra_crit) for p in pscs)


# §10 top-10 contractors: (display name, FPDS Corporate Parent criterion | None).
# None criterion => rank-10 S.C.A. is a hand-keyed INPUT (no FPDS match), not a SUMIFS.
_TOP10 = [
    ("BAE Systems", "BAE Systems"),
    ("General Dynamics", "General Dynamics"),
    ("Huntington Ingalls Industries", "Huntington Ingalls Industries"),
    ("Vigor Marine LLC", "VIGOR MARINE LLC"),
    ("The Charles Stark Draper Laboratory Inc.", "THE CHARLES STARK DRAPER LABORATORY  INC."),
    ("Detyens Shipyards Inc.", "DETYENS SHIPYARDS  INC."),
    ("Epsilon Systems Solutions Inc.", "EPSILON SYSTEMS SOLUTIONS  INC."),
    ("East Coast Repair & Fabrication LLC", "EAST COAST REPAIR & FABRICATION  LLC"),
    ("Lockheed Martin Corporation", "LOCKHEED MARTIN CORPORATION"),
    ("S.C.A. - Shipping Consultants Associated Ltd.", None),
]
_SCA_INPUT = 112.20543451       # rank-10 S.C.A. FY2025 $M (hand-keyed)

# §11 HII margin reference: (entity, FY25 rev $M, FY25 OI $M, OI margin, relevance).
_HII_CONSOL = [
    ("Huntington Ingalls Industries (consolidated)", 12484, 657, 0.05262736302467158,
     "Top-3 Services TAM contractor; blended parent margin"),
    ("General Dynamics (consolidated)", 52550, 5360, 0.1019980970504282,
     "Top-3 Services TAM contractor; blended parent margin"),
    ("BWX Technologies (consolidated)", 3198, 401, 0.1253908692933083,
     "Naval nuclear sole-source supply; not a ship MRO prime"),
]
_HII_PURE = [
    ("HII - Mission Technologies", 3044, 153, 0.05026281208935611,
     "91% service revenue; pure-services benchmark"),
    ("GD - Marine Systems (blended)", 16723, 1177, 0.07038210847336004,
     "Repair sub-line $1,183M FY25 (GD 10-K disclosure)"),
    ("BWXT - Gov Ops (inferred)", 2350, "-", 0.17,
     "~17% margin inferred from consol OI less commercial allocation"),
]

# §12 market share top-3 per segment: segment -> [(display, criterion), x3].
_S12 = [
    ("Depot Ship Repair", ['J998', 'J999'], [
        ("BAE Systems", "BAE Systems"),
        ("General Dynamics", "General Dynamics"),
        ("Huntington Ingalls Industries", "Huntington Ingalls Industries"),
    ]),
    ("Combat Systems Sustainment",
     ['J010', 'J012', 'J013', 'J014', 'J017', 'K010', 'K012', 'K014', 'N010', 'N012', 'N014'], [
        ("The Charles Stark Draper Laboratory Inc.", "THE CHARLES STARK DRAPER LABORATORY  INC."),
        ("Lockheed Martin Corporation", "LOCKHEED MARTIN CORPORATION"),
        ("Leidos Inc.", "LEIDOS  INC."),
    ]),
    ("Hull, Mechanical & Electrical (HM&E)",
     ['J019', 'J020', 'J029', 'J030', 'J035', 'J036', 'J039', 'J041', 'J043', 'J047', 'J048',
      'J049', 'J052', 'J056', 'J091', 'J099', 'K019', 'K020', 'K034', 'K099', 'N019', 'N020',
      'N025', 'N056'], [
        ("Global PCCI (GPC)", "GLOBAL PCCI (GPC)"),
        ("Oceaneering International Inc", "OCEANEERING INTERNATIONAL INC"),
        ("Huntington Ingalls Industries", "Huntington Ingalls Industries"),
    ]),
    ("Electronics & C4ISR Sustainment",
     ['J058', 'J059', 'J061', 'J063', 'J066', 'K058', 'K059'], [
        ("Amentum Services Inc.", "AMENTUM SERVICES  INC."),
        ("L3 Technologies Inc.", "L3 TECHNOLOGIES  INC."),
        ("Science Applications International Corporation",
         "SCIENCE APPLICATIONS INTERNATIONAL CORPORATION"),
    ]),
    ("Port & Technical Services",
     ['H119', 'H120', 'H219', 'H220', 'H319', 'H320', 'H919', 'H920', 'L019', 'L020', 'M1ED',
      'M2AA', 'M2AB', 'M2AC', 'M2AD', 'M2AE', 'M2AF', 'M2BA', 'M2BB', 'M2BZ', 'M2CA'], [
        ("S.C.A. - Shipping Consultants Associated Ltd.", "S.C.A. - SHIPPING CONSULTANTS ASSOCIATED LTD."),
        ("Waypoint LLC", "WAYPOINT LLC"),
        ("Fairlead Boatworks Inc.", "FAIRLEAD BOATWORKS  INC."),
    ]),
]


def _make():
    P: dict[str, int] = {}
    # outline_default=1: every content row collapses under its mark_collapsible banner.
    c = RowCursor(2, outline_default=1)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1-§3 cross-tabs (Python loops over the axis constants). Banner spans the cross-tab's
    # own width (label + axis + total), not the sheet maximum.
    def _crosstab(key, banner_text, axis, mk_crit):
        c.banner(banner_text, n_cols=len(axis) + 3, style=S_TITLE_SECTION,
                 mark_collapsible=True)
        c.blank()
        naxis = len(axis)
        c0 = 3                                   # first data column = D (B=code, C=desc)
        clast = c0 + naxis - 1
        ctot = c0 + naxis
        hdr = ["PSC", "Description"] + list(axis) + ["Total"]
        c.write(hdr, styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * (naxis + 1))
        lo = c.at()
        for code, desc in PSC_ROWS:
            vals = [code, desc]
            for label in axis:
                vals.append("=" + sumifs_award(_VAL, *mk_crit(code, label)))
            vals.append(lambda r: f"=SUM({col_letter(c0)}{r}:{col_letter(clast)}{r})")
            c.write(vals, styles=[S_DEFAULT, S_DEFAULT] + [S_NUM] * (naxis + 1))
        hi = c.at() - 1
        tot_vals = ["Total", None]
        for cc in range(c0, ctot + 1):
            L = col_letter(cc)
            tot_vals.append(f"=SUM({L}{lo}:{L}{hi})")
        c.total(tot_vals, styles=[S_BOLD, S_DEFAULT] + [S_NUM] * (naxis + 1),
                n_cols=len(tot_vals))
        c.blank(2)

    _crosstab("s1", "§1 - U.S. Navy + Coast Guard by vessel type", VESSEL_TYPES,
              lambda code, lab: [("PSC", code), ("Vessel Type", axis_crit(lab))])
    _crosstab("s2", "§2 - U.S. Navy by hull program", HULL_PROGRAMS_NAVY,
              lambda code, lab: [("PSC", code), ("Hull Program", axis_crit(lab)),
                                 ("Service", "Navy")])
    _crosstab("s3", "§3 - U.S. Coast Guard by hull program", HULL_PROGRAMS_CG,
              lambda code, lab: [("PSC", code), ("Hull Program", axis_crit(lab)),
                                 ("Service", "Coast Guard")])

    # §4 FY2025 MRO TAM  (B=Metric, C=$M, D=% of TAM). PRODUCER of the TAM names.
    c.banner("§4 - FY2025 MRO TAM", n_cols=3,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "FY2025 $M", "% of TAM"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    all_pscs = [p for p, _ in PSC_ROWS]
    # Navy / CG / Total are consecutive; the % cells forward-reference the total row,
    # so fix the three row numbers up front (RowCursor resolves callables eagerly).
    P["navy"], P["cg"], P["s4_total"] = c.at(), c.at() + 1, c.at() + 2
    c.write(["U.S. Navy",
             "=(" + _sum_over_pscs(all_pscs, ("Service", "Navy")) + ")/1000000",
             f"=C{P['navy']}/C{P['s4_total']}"],
            styles=[S_DEFAULT, S_NUM, S_PCT])
    c.write(["U.S. Coast Guard",
             "=(" + _sum_over_pscs(all_pscs, ("Service", "Coast Guard")) + ")/1000000",
             f"=C{P['cg']}/C{P['s4_total']}"],
            styles=[S_DEFAULT, S_NUM, S_PCT])
    c.total(["Total Services TAM", f"=C{P['navy']}+C{P['cg']}", "=1"],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=3)
    c.blank(2)

    # legacy-name resolver: ref a figure now that no defined names exist
    # The §4 TAM cells (Navy/CG) are intra-sheet; the §6/§7 budget anchors live on the
    # Reconciliation sheet and are reached through its import-time accessors. Replaces
    # the former bare named-range references (e.g. "=MRO_TAS_OMN_FY25/1000").
    def _ref(name):
        if name == "NAVY_TAM_SVC":
            return f"C{P['navy']}"
        if name == "CG_TAM_SVC":
            return f"C{P['cg']}"
        if name.startswith("MRO_TAS_") and name.endswith("_FY25"):
            return mro_tas_cell(name[len("MRO_TAS_"):-len("_FY25")])
        if name.startswith("OMN_") and name.endswith("_FY25"):
            return omn_cell(name[len("OMN_"):-len("_FY25")])
        if name.startswith("USCG_ISVS_") and name.endswith("_FY25"):
            return uscg_isvs_cell(name[len("USCG_ISVS_"):-len("_FY25")])
        raise ValueError(f"Services: no accessor for legacy name {name!r}")

    # §5 FY2025 MRO TAM by work segment
    c.banner("§5 - FY2025 MRO TAM by work segment",
             n_cols=3, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Segment", "FY2025 $M", "% of TAM"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    seg_rows = []
    for name, pscs in WORK_SEGMENTS:
        r = c.write(
            [name, "=(" + _sum_over_pscs(pscs) + ")/1000000",
             lambda r: f"=C{r}/C{P['s4_total']}"],
            styles=[S_DEFAULT, S_NUM, S_PCT])
        seg_rows.append(r)
    c.total(["Total Services TAM",
             f"=SUM(C{seg_rows[0]}:C{seg_rows[-1]})", "=1"],
            styles=[S_BOLD, S_NUM, S_PCT], n_cols=3)
    c.blank(2)

    # §6 FY2025 MRO budget reconciliation  (B=label, C=$M, D=source, E=% of TAS Total)
    #    Values are BARE NAMES (Reconciliation anchors) - position-independent.
    c.banner("§6 - FY2025 MRO budget reconciliation",
             n_cols=4, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "FY25 $M", "Source", "% of TAS Total"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Services TAM - U.S. Navy", f"=C{P['navy']}", "FPDS Awards (SUMIFS, 65 MRO PSCs)",
             None],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT, S_DEFAULT])
    c.write(["Services TAM - U.S. Coast Guard", f"=C{P['cg']}", "FPDS Awards (SUMIFS, 65 MRO PSCs)",
             None],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT, S_DEFAULT])
    c.total(["Subtotal - FPDS Services TAM (post-exclusion)", f"=C{P['navy']}+C{P['cg']}",
             "FPDS bottom-up", None],
            styles=[S_BOLD, S_NUM, S_BOLD, S_DEFAULT], n_cols=4)
    c.blank()
    c.banner("FY25 MRO-PSC $ by appropriation (TAS-measured)",
             n_cols=4, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    # (label, name, source, pct_denominator_name, note, indent)
    _S6_APPR = [
        ("OMN - Operation & Maintenance, Navy (017-1804)", "MRO_TAS_OMN_FY25", "MRO_TAS_TOTAL_FY25",
         "Primary Navy O&M; dominant in N-series installs, M2 husbanding, L-series tech rep", False),
        ("OPN - Other Procurement, Navy (017-1810)", "MRO_TAS_OPN_FY25", "MRO_TAS_TOTAL_FY25",
         "Modernization procurement; J998/J999 Depot Ship Repair is 70% OPN, not OMN", False),
        ("of which BA-7 Personnel & Command Support Equip (PA 0007)", "MRO_TAS_OPN_BA7_FY25",
         "MRO_TAS_OPN_FY25",
         "Installation + modernization electronics / C4ISR / combat system integration equipment", True),
        ("of which BA-8 Spares & Repair Parts (PA 0008)", "MRO_TAS_OPN_BA8_FY25", "MRO_TAS_OPN_FY25",
         "Spares / consumable repair parts procurement directed at MRO PSC contract actions", True),
        ("of which other BAs (BA-1 Ships Support + Undistributed)", "MRO_TAS_OPN_BAOTHER_FY25",
         "MRO_TAS_OPN_FY25", "BA-1 Ships Support Equipment + undistributed + residual", True),
        ("RDT&E, Defense-Wide (097-0400)", "MRO_TAS_RDTE_DW_FY25", "MRO_TAS_TOTAL_FY25",
         "Trident/SSP/SMDC sustainment on J014, other J-series equipment", False),
        ("Defense-Wide - other (097-* excl. 0400)", "MRO_TAS_DW_OTHER_FY25", "MRO_TAS_TOTAL_FY25",
         "Joint-program O&M + Procurement Defense-Wide + DWCF", False),
        ("Navy - other appropriations (017-* excl. 1804/1810/1611)", "MRO_TAS_NAVY_OTHER_FY25",
         "MRO_TAS_TOTAL_FY25", "APN, WPN, MPN, minor Navy appropriations", False),
        ("SCN - Shipbuilding & Conversion, Navy (017-1611)", "MRO_TAS_SCN_FY25", "MRO_TAS_TOTAL_FY25",
         "PDA/PSA warranty work on newbuild LCS/DDG/LPD; no RCOH spillover", False),
        ("Air Force - O&M + Procurement (057-*)", "MRO_TAS_AIR_FORCE_FY25", "MRO_TAS_TOTAL_FY25",
         "Cross-service AF funding on Navy MRO PSCs (joint K-series mod)", False),
        ("USCG - OE / AC&I (070-*)", "MRO_TAS_USCG_FY25", "MRO_TAS_TOTAL_FY25",
         "Coast Guard cutter sustainment contract flow (includes OE depot work beyond ISVS)", False),
        ("Army - O&M + RDTE (021-*)", "MRO_TAS_ARMY_FY25", "MRO_TAS_TOTAL_FY25",
         "USACE dredge maintenance + cross-service Army RDTE", False),
        ("Other federal agencies (non-DoD, non-USCG)", "MRO_TAS_OTHER_AGENCY_FY25", "MRO_TAS_TOTAL_FY25",
         "Small cross-federal flows", False),
    ]
    for label, name, denom, _note, indent in _S6_APPR:
        c.write([label, f"={_ref(name)}/1000", "Budget Anchors TAS",
                 f"={_ref(name)}/{_ref(denom)}"],
                styles=[S_LABEL_INDENT_1 if indent else S_DEFAULT, S_NUM, S_DEFAULT, S_PCT])
    c.total(["TAS Attribution Total (pre-exclusion MRO-PSC universe)", f"={_ref('MRO_TAS_TOTAL_FY25')}/1000",
             "Budget Anchors SUM", "1.0"],
            styles=[S_BOLD, S_NUM, S_BOLD, S_BOLD], n_cols=4)
    c.blank()
    c.banner("Top-down budget-book context (memo)",
             n_cols=4, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.write(["OMN CE 928 Ship Maintenance By Contract (Ship Ops BA-1 total)",
             f"={_ref('OMN_SHIPOPS_BA1_CONTRACT_FY25')}/1000", "Budget Anchors OMN", None],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT, S_DEFAULT])
    c.write(["OMN BA-1 Ship Ops total (all cost elements)", f"={_ref('OMN_SHIPOPS_BA1_TOTAL_FY25')}/1000",
             "Budget Anchors OMN", None],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT, S_DEFAULT])
    c.write(["USCG ISVS total (PC&I Cutter Sustainment)", f"={_ref('USCG_ISVS_TOTAL_FY25')}/1000",
             "Budget Anchors USCG", None],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT, S_DEFAULT])
    c.blank(2)

    # §7 budget-book anchors  (B=label, C=$M, D=source)
    c.banner("§7 - Budget-book anchors", n_cols=3,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Appropriation / Line Item", "FY25 Enacted $M", "Source"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.banner("FY25 MRO-PSC Appropriation Attribution (TAS-measured)", n_cols=3,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    _S7_TAS = [
        ("OMN - Operation & Maintenance, Navy (017-1804)", "MRO_TAS_OMN_FY25",
         "USAspending /awards/funding/", "Primary Navy O&M; dominant in N-series installs + M2 husbanding + L-series"),
        ("OPN - Other Procurement, Navy (017-1810)", "MRO_TAS_OPN_FY25",
         "USAspending /awards/funding/", "Modernization procurement; 70% of J998/J999 Depot Ship Repair"),
        ("RDT&E, Defense-Wide (097-0400)", "MRO_TAS_RDTE_DW_FY25",
         "USAspending /awards/funding/", "Trident/SSP/SMDC sustainment on J-series equipment"),
        ("Defense-Wide other (097-* excl. 0400)", "MRO_TAS_DW_OTHER_FY25",
         "USAspending /awards/funding/", "Joint-program O&M + Procurement DW"),
        ("Navy other (017-* excl. primary)", "MRO_TAS_NAVY_OTHER_FY25",
         "USAspending /awards/funding/", "APN, WPN, MPN, minor Navy appropriations"),
        ("SCN - Shipbuilding & Conversion, Navy (017-1611)", "MRO_TAS_SCN_FY25",
         "USAspending /awards/funding/", "PDA/PSA warranty on newbuild LCS/DDG/LPD"),
        ("Air Force (057-*)", "MRO_TAS_AIR_FORCE_FY25",
         "USAspending /awards/funding/", "Cross-service AF on Navy MRO PSCs"),
        ("USCG (070-*)", "MRO_TAS_USCG_FY25",
         "USAspending /awards/funding/", "USCG cutter sustainment contract flow"),
        ("Army (021-*)", "MRO_TAS_ARMY_FY25",
         "USAspending /awards/funding/", "USACE dredge + cross-service Army RDTE"),
        ("Other federal agencies", "MRO_TAS_OTHER_AGENCY_FY25",
         "USAspending /awards/funding/", "Small cross-federal flows"),
    ]
    for label, name, src, _desc in _S7_TAS:
        c.write([label, f"={_ref(name)}/1000", src],
                styles=[S_DEFAULT, S_NUM, S_DEFAULT])
    c.write(["TAS Attribution Total", f"={_ref('MRO_TAS_TOTAL_FY25')}/1000", "Budget Anchors SUM formula"],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT])
    c.banner("OMN - Ship Operations BA-1 (Operating Forces)", n_cols=3,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    # (label, name, source, description, indent)
    _S7_OMN = [
        ("1B1B Mission and Other Ship Operations (total)", "OMN_1B1B_TOTAL_FY25",
         "OMN_Book line 619", "Fleet operations, ship movement, crew training", False),
        ("of which CE 928 Ship Maint By Contract", "OMN_1B1B_CONTRACT_FY25",
         "OMN_Book line 4770", "Negligible private-contractor slice within 1B1B", True),
        ("1B2B Ship Operational Support and Training (total)", "OMN_1B2B_TOTAL_FY25",
         "OMN_Book line 620", "Submarine + carrier operational support, pre-planning", False),
        ("of which CE 928 Ship Maint By Contract", "OMN_1B2B_CONTRACT_FY25",
         "OMN_Book line 5255", "Private-contractor slice within 1B2B", True),
        ("1B4B Ship Maintenance (total)", "OMN_1B4B_TOTAL_FY25",
         "OMN_Book line 6714", "All Navy ship depot maintenance O&M,N customer budget", False),
        ("of which CE 928 Ship Maint By Contract", "OMN_1B4B_CONTRACT_FY25",
         "OMN_Book line 6698", "Primary MRO contract bucket - core of Services TAM", True),
        ("1B5B Ship Depot Operations Support (total)", "OMN_1B5B_TOTAL_FY25",
         "OMN_Book line 622", "Depot labor, facilities, LCS single-crew support, SUPSHIP", False),
        ("of which CE 928 Ship Maint By Contract", "OMN_1B5B_CONTRACT_FY25",
         "OMN_Book line 7217", "Depot contract labor / supplies", True),
        ("Ship Ops BA-1 grand total (SUM of 4 SAGs)", "OMN_SHIPOPS_BA1_TOTAL_FY25",
         "Budget Anchors SUM formula", "Top-down Ship Ops funding; includes public-yard via NWCF", False),
        ("CE 928 Ship Maint By Contract - summed across SAGs", "OMN_SHIPOPS_BA1_CONTRACT_FY25",
         "Budget Anchors SUM formula", "Total private-contractor slice across Ship Ops", False),
    ]
    for label, name, src, _desc, indent in _S7_OMN:
        c.write([label, f"={_ref(name)}/1000", src],
                styles=[S_LABEL_INDENT_1 if indent else S_DEFAULT, S_NUM, S_DEFAULT])
    c.banner("USCG PC&I - In-Service Vessel Sustainment", n_cols=3,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    _S7_USCG = [
        ("ISVS total (PPA)", "USCG_ISVS_TOTAL_FY25", "USCG_Justification line 128",
         "Cutter SLEP / MMA umbrella (PC&I capital, not OE)", False),
        ("47-Foot Motor Lifeboat SLEP", "USCG_ISVS_47MLB_FY25", "USCG_Justification line 2378",
         "20-year service-life extension for 47-ft MLB fleet", True),
        ("270-foot WMEC SLEP", "USCG_ISVS_WMEC_FY25", "USCG_Justification",
         "270-ft Famous Class Medium Endurance Cutter SLEP", True),
        ("CGC Healy SLEP", "USCG_ISVS_HEALY_FY25", "USCG_Justification",
         "Medium polar icebreaker SLEP", True),
    ]
    for label, name, src, _desc, indent in _S7_USCG:
        c.write([label, f"={_ref(name)}/1000", src],
                styles=[S_LABEL_INDENT_1 if indent else S_DEFAULT, S_NUM, S_DEFAULT])
    c.banner("NWCF memo", n_cols=3, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.write(["Navy-wide NWCF Budget Authority (memo only)", "~$40,300 ($M equiv)", "NWCF_Book"],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT])
    c.blank(2)

    # §9 work segment coverage  (B=# PSCs, C=segment, D=codes)
    c.banner("§9 - Work segment coverage", n_cols=3,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["# PSCs", "MRO Segment", "PSC Codes"],
            styles=[S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT])
    for name, pscs in WORK_SEGMENTS:
        c.write([len(pscs), name, ", ".join(pscs)],
                styles=[S_NUM_INPUT, S_DEFAULT, S_DEFAULT])
    c.total([sum(len(pscs) for _, pscs in WORK_SEGMENTS), "Total PSCs"],
            styles=[S_NUM_INPUT, S_BOLD], n_cols=3)
    c.blank(2)

    # §10 top-10 contractors  (B=Rank, C=Corporate Parent, D=$M, E=% of TAM, F=Cumulative %)
    c.banner("§10 - FY2025 MRO revenue by contractor, top 10",
             n_cols=5, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Rank", "Corporate Parent", "FY2025 $M", "% of Services TAM", "Cumulative %"],
            styles=[S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    _TAM = f"(C{P['navy']}+C{P['cg']})"
    rank_rows = []
    for i, (display, crit) in enumerate(_TOP10):
        if crit is None:
            money = _SCA_INPUT
            money_style = S_NUM_INPUT
        else:
            money = "=(" + _sum_over_pscs(all_pscs, ("Corporate Parent", crit)) + ")/1000000"
            money_style = S_NUM
        pct = (lambda r: f"=IFERROR(D{r}/{_TAM},0)")
        if i == 0:
            cumul = (lambda r: f"=E{r}")
        else:
            cumul = (lambda r, p=rank_rows[-1]: f"=F{p}+E{r}")
        r = c.write([i + 1, display, money, pct, cumul],
                    styles=[S_DEFAULT, S_DEFAULT, money_style, S_PCT, S_PCT])
        rank_rows.append(r)
    P["top10_sub"] = c.total(
        [None, "Top 10 Subtotal", f"=SUM(D{rank_rows[0]}:D{rank_rows[-1]})",
         lambda r: f"=IFERROR(D{r}/{_TAM},0)", lambda r: f"=E{r}"],
        styles=[S_DEFAULT, S_BOLD, S_NUM, S_PCT, S_PCT], n_cols=5)
    c.write([None, "All Other Contractors", f"={_TAM}-D{P['top10_sub']}",
             lambda r: f"=IFERROR(D{r}/{_TAM},0)"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_PCT])
    c.total([None, "Services TAM", f"={_TAM}", "=1"],
            styles=[S_DEFAULT, S_BOLD, S_NUM, S_PCT], n_cols=5)
    c.blank()
    c.banner("Market Concentration", n_cols=3, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.write([None, "Top 3 share", f"=F{rank_rows[2]}"], styles=[S_DEFAULT, S_DEFAULT, S_PCT])
    c.write([None, "Top 10 share", f"=F{rank_rows[9]}"], styles=[S_DEFAULT, S_DEFAULT, S_PCT])
    c.blank(2)

    # §11 HII Mission Technologies margin reference  (B..F input table)
    c.banner('§11 - HII Mission Technologies margin reference', n_cols=5,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Entity", "FY25 Rev ($M)", "FY25 OI ($M)", "OI Margin", "Relevance to Services TAM"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    for entity, rev, oi, margin, rel in _HII_CONSOL:
        c.write([entity, rev, oi, margin, rel],
                styles=[S_DEFAULT, S_NUM_INPUT, S_NUM_INPUT, S_PCT_INPUT, S_DEFAULT])
    c.banner("Cleanest pure-services sub-segments", n_cols=5, style=S_TITLE_SUBSECTION,
             mark_collapsible=True)
    for entity, rev, oi, margin, rel in _HII_PURE:
        oi_style = S_NUM_INPUT if isinstance(oi, (int, float)) else S_DEFAULT
        c.write([entity, rev, oi, margin, rel],
                styles=[S_DEFAULT, S_NUM_INPUT, oi_style, S_PCT_INPUT, S_DEFAULT])
    c.blank(2)

    # §12 market share by work segment, top 3  (B=Rank, C=Corporate Parent, D=% of Segment)
    c.banner('§12 - FY2025 market share by work segment, top 3', n_cols=3,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Rank", "Corporate Parent", "% of Segment"],
            styles=[S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_CENTER])
    for seg_name, pscs, primes in _S12:
        c.banner(seg_name, n_cols=3, style=S_TITLE_SUBSECTION, mark_collapsible=True)
        denom = _sum_over_pscs(pscs)
        for j, (display, crit) in enumerate(primes):
            num = _sum_over_pscs(pscs, ("Corporate Parent", crit))
            c.write([j + 1, display, f"=IFERROR(({num})/({denom}),0)"],
                    styles=[S_DEFAULT, S_DEFAULT, S_PCT])
    c.blank(2)

    # §13 vessel type x work segment ($M)  (B=label, C..G=5 cats, H=Other, I=Total)
    c.banner("§13 - FY2025 MRO TAM by vessel type x work segment ($M)",
             n_cols=len(_S13_CATS) + 3, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["PSC Group"] + list(_S13_CATS) + ["Other", "Total"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(_S13_CATS) + 2))
    # Single label column (B), so the categories start at column C (index 2):
    # B=label, C..G = 5 cats, H = Other, I = Total.
    _C0 = 2                                 # first data column index (C)
    _ncat = len(_S13_CATS)
    _other_col = _C0 + _ncat                # H
    s13_rows = []
    for name, pscs in WORK_SEGMENTS:
        vals = [name]
        for cat in _S13_CATS:
            vals.append("=(" + _sum_over_pscs(pscs, ("Vessel Type", cat)) + ")/1000000")
        # Other = (all-vessel-type total for these PSCs)/1e6 - (sum of the 5 named cat cells)
        vals.append(lambda r, ps=pscs: "=(" + _sum_over_pscs(ps) + ")/1000000-("
                    + "+".join(f"{col_letter(_C0 + k)}{r}" for k in range(_ncat)) + ")")
        vals.append(lambda r: f"=SUM({col_letter(_C0)}{r}:{col_letter(_other_col)}{r})")
        r = c.write(vals, styles=[S_DEFAULT] + [S_NUM] * (_ncat + 2))
        s13_rows.append(r)
    s13_ncol = _ncat + 2                    # cats + Other + Total
    tot_vals = ["Total"]
    for k in range(s13_ncol):
        L = col_letter(_C0 + k)
        tot_vals.append(f"=SUM({L}{s13_rows[0]}:{L}{s13_rows[-1]})")
    P["s13_total"] = c.total(tot_vals, styles=[S_BOLD] + [S_NUM] * s13_ncol,
                             n_cols=len(tot_vals))
    c.blank(2)

    # §14 vessel type x work segment (%)  (each cell = §13 cell / §13 column total)
    c.banner("§14 - FY2025 MRO TAM by vessel type x work segment (%)",
             n_cols=len(_S13_CATS) + 3, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["PSC Group"] + list(_S13_CATS) + ["Other", "Total"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(_S13_CATS) + 2))
    t = P["s13_total"]
    for name, r13 in zip([n for n, _ in WORK_SEGMENTS], s13_rows):
        vals = [name]
        for k in range(s13_ncol):
            L = col_letter(_C0 + k)
            vals.append(f"=IFERROR({L}{r13}/{L}{t},0)")
        c.write(vals, styles=[S_DEFAULT] + [S_PCT] * s13_ncol)
    # bottom Total row echoes the §13 dollar totals
    bot = ["Total"] + [f"={col_letter(_C0 + k)}{t}" for k in range(s13_ncol)]
    c.total(bot, styles=[S_BOLD] + [S_NUM] * s13_ncol, n_cols=len(bot))

    # accessors (the §4 TAM cells; consumers import these — no defined names)
    def navy_tam_svc_cell(): return f"'{_TAB}'!C{P['navy']}"
    def cg_tam_svc_cell(): return f"'{_TAB}'!C{P['cg']}"

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    accessors = dict(navy_tam_svc_cell=navy_tam_svc_cell, cg_tam_svc_cell=cg_tam_svc_cell)
    return SheetEntry(_TAB, _GROUP, render), accessors


SERVICES, _ACC = _make()

navy_tam_svc_cell = _ACC["navy_tam_svc_cell"]
cg_tam_svc_cell = _ACC["cg_tam_svc_cell"]
