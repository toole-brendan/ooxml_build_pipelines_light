"""Reconciliation

INTENT
    Budget Authority vs FPDS Awards: deck-evidence anchors (§1) + the FY2025
    appropriation-attribution / budget-anchor table (§2).
    The §1 anchors (PSC1905_MRO_* / RECONCILED_MRO_TAM / PUBLIC_SHIPYARD_NWCF /
    HII_MT_*, value column) and the §2 anchors (MRO_TAS_* / OMN_* / SCN_* / USCG_ISVS_*,
    FY25 Enacted column) are exposed as closure accessors that every consumer imports;
    qa/name_map maps each legacy v4.33 name to its accessor for the tie-out.

    Cycle break: Reconciliation's RECONCILED_MRO_TAM pulls the Services TAM producers
    while Services §6/§7 pull these budget anchors. Broken on this side - Services
    imports these accessors at module load, and the single RECONCILED_MRO_TAM back-link
    to Services is a DEFERRED row whose formula is spliced in at render() behind a lazy
    import - so there is no model_reconciliation <-> model_services import cycle.

LAYOUT
    row 2 : title
    §1 deck-evidence anchors (B:D - Anchor / Line / Value $M, value col D)
    §2 budget-anchor table (B:H), led by the wide Line Item description so it shares column B
       with §1's Anchor (no empty column): Line Item / Appropriation / Line / FY24 $K (E) /
       FY25 Enacted $K (F) / FY26 $K (G) / Source (H), appropriation sub-bands as collapsible
       subsection banners
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, banner_row, write_row
from workbook_core.styles import (
    S_DEFAULT, S_NUM, S_NUM_INPUT, S_LABEL_INDENT_1,
    S_HEADER_LEFT, S_HEADER_CENTER,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor

_GROUP = "model"
_TAB = "Reconciliation"
# §1 lives in B:D (Anchor / Line / Value). §2 leads with the wide Line Item description so it
# shares the wide column B with §1's Anchor - no empty column, and §1's numeric Value column (D)
# stays narrow (the one-column-doing-two-jobs bug is solved by aligning the wide columns, not by
# offsetting §2). Banner/section widths are local per section.
_NCOLS = 7                      # B..H (the §2 budget-anchor table is the widest section)
_S1_NCOLS = 3                   # §1 spans B:D
# Column widths B..H: B = wide label (Anchor / Line Item), C = code/name, D = value/line,
# E/F/G = FY24/FY25/FY26 $K, H = Source. The 70-wide Description prose column was dropped earlier.
_COLS = [48.0, 24.0, 14.0, 16.0, 16.0, 16.0, 32.0]

# §1 deck-evidence anchors before the deferred RECONCILED_MRO_TAM row.
# (label, defined-name, value $M, deck slide, source/note)
_ANCHORS_BEFORE = [
    ("PSC 1905 embedded MRO (total)", "PSC1905_MRO_EMBEDDED", 1904, "S20 Scope Reconciliation",
     "Classifier-locked Central from workbook_build.psc_1905_classifier across 201 PSC 1905 PIIDs. "
     "Tier 0: USAspending /awards/funding/ TAS (OMN/OPN/RDTE funding on a PSC 1905 award is a "
     "definitive MRO signal - O&M dollars cannot fund new construction). Tier 1-5: strong/soft MRO "
     "keywords + POP length + newbuild hull override. Central = strong + TAS-confirmed + probable. "
     "Bounds: $1,553M / $1,904M / $2,057M."),
    ("PSC 1905 embedded MRO - Submarines", "PSC1905_MRO_SUBS", 1255, "S20 Scope Reconciliation",
     "Embedded MRO within PSC 1905 attributed to submarine hulls (dominated by Electric Boat SSN "
     "Seam Split Repairs $831M + USS Boise SSN-764 Engineered Overhaul $424M)."),
    ("PSC 1905 embedded MRO - Aircraft Carriers", "PSC1905_MRO_CARRIERS", 337, "S20 Scope Reconciliation",
     "Embedded MRO within PSC 1905 attributed to aircraft carriers (CVN-68 class inactivation + "
     "CVN-69 Eisenhower FY25 PIA + CVN-74/75 Refueling Complex Overhaul support)."),
    ("PSC 1905 embedded MRO - Surface Combatants", "PSC1905_MRO_SURFCOMBS", 119, "S09 TAM Composition",
     "Embedded MRO within PSC 1905 attributed to surface combatants (DDG 1000 BYMP, DDG "
     "modernization and cross-class support work)."),
    ("PSC 1905 embedded MRO - Unclassified vessels", "PSC1905_MRO_UNCL", 193, "S09 TAM Composition",
     "Embedded MRO within PSC 1905 that could not be attributed to a specific vessel supergroup "
     "(general SUPSHIP support, labor support, cross-class mods)."),
    ("PSC 1905 embedded MRO - SSN", "PSC1905_MRO_SSN", 1255, "S09 TAM Composition",
     "Embedded MRO attributed to SSN (Virginia-class attack subs). Electric Boat SHT Seam Split "
     "Repairs + USS Boise SSN-764 Engineered Overhaul."),
    ("PSC 1905 embedded MRO - CVN", "PSC1905_MRO_CVN", 337, "S09 TAM Composition",
     "Embedded MRO attributed to CVN (Nimitz/Ford-class carriers). CVN-68 inactivation + USS "
     "Eisenhower FY25 PIA + CVN-74/75 RCOH support at HII Newport News."),
    ("PSC 1905 embedded MRO - DDG", "PSC1905_MRO_DDG", 77, "S09 TAM Composition",
     "Embedded MRO attributed to DDG (Arleigh Burke destroyers). DDG modernization / availability "
     "support routed through the shipbuilding PSC."),
    ("PSC 1905 embedded MRO - LCS", "PSC1905_MRO_LCS", 41, "S09 TAM Composition",
     "Embedded MRO attributed to LCS (Littoral Combat Ship). Sustainment task orders routed "
     "through PSC 1905."),
    ("PSC 1905 embedded MRO - Tier 0 TAS-confirmed subset", "PSC1905_MRO_TIER0", 235,
     "S20 Scope Reconciliation",
     "Subset of embedded MRO that received OMN / OPN / RDT&E funding on PSC 1905 awards (definitive "
     "MRO signal via USAspending /awards/funding/ TAS pull). Appropriation attribution for this "
     "subset is known; the remainder imputes to SCN 017-1611."),
    ("PSC 1905 embedded MRO - General Dynamics", "PSC1905_MRO_GD", 965, "S17 Prime Landscape TAM",
     "Per-parent rollup of embedded PSC 1905 MRO (Central basis). GD share driven by Electric Boat "
     "SHT Seam Split Repairs + New England Maintenance + Nuclear Regional Maintenance Dept work."),
    ("PSC 1905 embedded MRO - Huntington Ingalls Industries", "PSC1905_MRO_HII", 872,
     "S17 Prime Landscape TAM",
     "Per-parent rollup of embedded PSC 1905 MRO (Central basis). HII share driven by HII Newport "
     "News USS Boise EOH, CVN 68 inactivation, USS Eisenhower FY25 PIA."),
    ("PSC 1905 embedded MRO - BAE Systems", "PSC1905_MRO_BAE", 48, "S17 Prime Landscape TAM",
     "Per-parent rollup of embedded PSC 1905 MRO (Central basis). BAE exposure in PSC 1905 is "
     "small; dominant BAE MRO share comes from J998 / J999 services-PSC work (captured in Awards)."),
    ("PSC 1905 embedded MRO - Other primes", "PSC1905_MRO_OTHER_PRIMES", 20, "S17 Prime Landscape TAM",
     "Per-parent rollup residual (Lockheed Martin, Mills Marine, PCSI, Jered, etc.). Small; used to "
     "keep Slide 15 Prime Landscape rollup reconciled with PSC1905_MRO_EMBEDDED total."),
]
# The deferred RECONCILED_MRO_TAM row (formula pulls Services TAM via lazy import at render).
_RECON_LABEL = "Reconciled FPDS-visible MRO TAM"
# §1 anchors after the deferred row.
_ANCHORS_AFTER = [
    ("Public naval shipyard NWCF", "PUBLIC_SHIPYARD_NWCF", 7500, "S20 Scope Reconciliation",
     "FY25 OMN 1B4B Ship Depot Maintenance total minus \"Ship Maintenance By Contract\" cost "
     "element; approximates public-yard labor reimbursed through NWCF. $12-15B all-in including "
     "mission funding customer orders."),
    ("HII Mission Technologies FY25 revenue", "HII_MT_FY25_REV", 3044,
     "S17 / S18 HII Mission Technologies", "FY2025 10-K segment revenue."),
    ("HII Mission Technologies FY25 OI", "HII_MT_FY25_OI", 153,
     "S18 HII Mission Technologies Financials",
     "FY2025 10-K segment operating income (~5.0% margin on $3.04B)."),
    ("HII Mission Technologies FY25 service revenue mix", "HII_MT_FY25_SVC_MIX_PCT", 91,
     "S17 HII Mission Technologies Overview",
     "Services share of segment revenue (%); cleanest pure-services public comp in the "
     "Navy MRO comp set."),
]

# §2 BudgetAnchors table rows (the v4.33 grid, baked in as static literals).
# Each entry: ("sec", text) | ("row", v433r, appr, line, lineitem, fy24, fy25, fy26, src, desc, name)
#           | ("frow", v433r, appr, line, lineitem, [rows_to_sum], src, desc, name)
# The `desc` field is retained as in-source provenance but is NO LONGER rendered as a
# sheet column - the per-row Description column was dropped so the calc grid stays
# compact (source/citation prose lives in sources_references / guide_methodology).
_S2 = [
    ("sec", "FY2025 MRO-PSC Appropriation Attribution - measured via Treasury TAS (bottom-up)"),
    ("row", 28, "OMN", "TAS OMN", "OMN - Operation & Maintenance, Navy (017-1804)", None, 2761054,
     None, "USAspending /awards/funding/ + PSC imputation",
     "Primary Navy operating funds on MRO PSCs; funds N-series installs, M2 husbanding, L-series "
     "tech rep (all OMN-dominant buckets)", "MRO_TAS_OMN_FY25"),
    ("row", 29, "OPN", "TAS OPN", "OPN - Other Procurement, Navy (017-1810)", None, 2587836, None,
     "USAspending /awards/funding/ + PSC imputation",
     "Modernization procurement; J998/J999 Depot Ship Repair is 70% OPN - DSRAs/DPIAs funded as "
     "mod installs, not O&M contract maintenance", "MRO_TAS_OPN_FY25"),
    ("row", 30, "OPN", "TAS OPN BA-7", "  of which BA-7 Personnel & Command Support Equip (PA 0007)",
     None, 1591498, None, "USAspending /awards/funding/ PA split (classify_opn_pa_split)",
     "Installation + modernization electronics / C4ISR / combat system integration equipment",
     "MRO_TAS_OPN_BA7_FY25"),
    ("row", 31, "OPN", "TAS OPN BA-8", "  of which BA-8 Spares & Repair Parts (PA 0008)", None,
     824996, None, "USAspending /awards/funding/ PA split (classify_opn_pa_split)",
     "Spares / consumable repair parts procurement directed at MRO PSC contract actions",
     "MRO_TAS_OPN_BA8_FY25"),
    ("row", 32, "OPN", "TAS OPN Other",
     "  of which other BAs (BA-1 Ships Support + Undistributed + other)", None, 171342, None,
     "USAspending /awards/funding/ PA split (classify_opn_pa_split)",
     "BA-1 Ships Support Equipment + undistributed + pre-FY21 optional rows + residual",
     "MRO_TAS_OPN_BAOTHER_FY25"),
    ("row", 33, "RDT&E DW", "TAS RDTE-DW", "RDT&E, Defense-Wide (097-0400)", None, 780443, None,
     "USAspending /awards/funding/ + PSC imputation",
     "Strategic Systems Programs - Draper MK7 Trident sustainment ($318M), other SMDC/SSP work; "
     "31% of J-series Equip Maint bucket", "MRO_TAS_RDTE_DW_FY25"),
    ("row", 34, "Defense-Wide", "TAS DW other", "Defense-Wide - other (097-* excl. 0400)", None,
     311924, None, "USAspending /awards/funding/ + PSC imputation",
     "Joint-program O&M + Procurement Defense-Wide + DWCF", "MRO_TAS_DW_OTHER_FY25"),
    ("row", 35, "Navy misc", "TAS Navy other",
     "Navy - other appropriations (017-* excl. 1804/1810/1611)", None, 298533, None,
     "USAspending /awards/funding/ + PSC imputation",
     "APN, WPN, MPN, and other small Navy appropriations that land on MRO PSCs",
     "MRO_TAS_NAVY_OTHER_FY25"),
    ("row", 36, "SCN", "TAS SCN", "SCN - Shipbuilding & Conversion, Navy (017-1611)", None, 40064,
     None, "USAspending /awards/funding/ + PSC imputation",
     "PDA/PSA warranty work on newbuild LCS/DDG/LPD; minimal RCOH spillover (most RCOH stays on "
     "PSC 1905)", "MRO_TAS_SCN_FY25"),
    ("row", 37, "Air Force", "TAS Air Force", "Air Force - O&M + Procurement (057-*)", None, 164294,
     None, "USAspending /awards/funding/ + PSC imputation",
     "Cross-service Air Force funding on Navy MRO PSCs (joint-program K-series mod work)",
     "MRO_TAS_AIR_FORCE_FY25"),
    ("row", 38, "USCG", "TAS USCG", "USCG - OE / AC&I (070-*)", None, 320102, None,
     "USAspending /awards/funding/ + PSC imputation",
     "Coast Guard cutter sustainment contract flow; larger than USCG ISVS alone ($120M) because it "
     "includes routine OE depot work", "MRO_TAS_USCG_FY25"),
    ("row", 39, "Army", "TAS Army", "Army - O&M + RDTE (021-*)", None, 128814, None,
     "USAspending /awards/funding/ + PSC imputation",
     "USACE dredge maintenance + cross-service Army RDTE", "MRO_TAS_ARMY_FY25"),
    ("row", 40, "Other agency", "TAS Other agency", "Other federal agencies (non-DoD, non-USCG)",
     None, 12921, None, "USAspending /awards/funding/ + PSC imputation", "Small cross-federal flows",
     "MRO_TAS_OTHER_AGENCY_FY25"),
    ("frow", 41, "Total", "TAS Total", "MRO-PSC FY25 Total (sum of appropriation rows)",
     [28, 29, 33, 34, 35, 36, 37, 38, 39, 40], "SUM of 10 appropriation rows above",
     "Pre-exclusion MRO-PSC universe; Services sheet TAM is ~$339M smaller (shore-base exclusions "
     "applied there but not in TAS rollup)", "MRO_TAS_TOTAL_FY25"),
    ("sec", "OMN BA-1 Operating Forces - Ship Operations appropriation"),
    ("row", 43, "OMN", "1B1B", "Mission and Other Ship Operations (SAG total)", 7460169, 7258014,
     5350073, "OMN_Book line 619",
     "Fleet operations, ship movement, crew training (MSC M&R transfers to 1B4B in FY26)",
     "OMN_1B1B_TOTAL_FY25"),
    ("row", 44, "OMN", "1B1B-928", "  of which CE 928 Ship Maintenance By Contract", 2663, 1746, 20,
     "OMN_Book line 4770", "Private-contractor slice within 1B1B (negligible)", "OMN_1B1B_CONTRACT_FY25"),
    ("row", 45, "OMN", "1B2B", "Ship Operational Support and Training (SAG total)", 1372331, 1536668,
     1719580, "OMN_Book line 620",
     "Pre-planning, engineering, submarine + carrier operational support", "OMN_1B2B_TOTAL_FY25"),
    ("row", 46, "OMN", "1B2B-928", "  of which CE 928 Ship Maintenance By Contract", 28630, 24621,
     8562, "OMN_Book line 5255", "Private-contractor slice within 1B2B", "OMN_1B2B_CONTRACT_FY25"),
    ("row", 47, "OMN", "1B4B", "Ship Maintenance (SAG total)", 11502495, 11763594, 13803188,
     "OMN_Book line 6714", "All Navy ship depot maintenance O&M,N customer budget", "OMN_1B4B_TOTAL_FY25"),
    ("row", 48, "OMN", "1B4B-928", "  of which CE 928 Ship Maintenance By Contract", 1769659, 2228255,
     3971574, "OMN_Book line 6698", "Private-contractor slice within 1B4B (primary MRO contract bucket)",
     "OMN_1B4B_CONTRACT_FY25"),
    ("row", 49, "OMN", "1B5B", "Ship Depot Operations Support (SAG total)", 2714238, 2671812, 2760878,
     "OMN_Book line 622", "Depot labor, facilities, LCS single-crew support, SUPSHIP", "OMN_1B5B_TOTAL_FY25"),
    ("row", 50, "OMN", "1B5B-928", "  of which CE 928 Ship Maintenance By Contract", 119929, 141550,
     186695, "OMN_Book line 7217", "Private-contractor slice within 1B5B", "OMN_1B5B_CONTRACT_FY25"),
    ("frow", 51, "OMN", "BA-1 total", "Ship Operations BA-1 grand total (SUM of 4 SAG totals)",
     [43, 45, 47, 49], "Sum of 4 SAGs above",
     "Top-down Ship Ops funding across all 4 SAGs (incl. public-yard labor cross-charged via NWCF "
     "rates)", "OMN_SHIPOPS_BA1_TOTAL_FY25"),
    ("frow", 52, "OMN", "BA-1 928", "CE 928 Ship Maintenance By Contract - summed across SAGs",
     [44, 46, 48, 50], "Sum of 4 CE 928 rows above",
     "Total private-contractor slice across all 4 Ship Ops SAGs", "OMN_SHIPOPS_BA1_CONTRACT_FY25"),
    ("sec", "SCN Capital Ships - 1611N Detail, Exhibit P-1"),
    ("row", 54, "SCN", "LI 1045 SFF", "Columbia Class - Subsequent Full Funding (construction)", 0,
     3364835, 3928828, "SCN_Book line 227",
     "Base construction authority for SSBN Columbia (Electric Boat + HII NNS)", None),
    ("row", 55, "SCN", "LI 1045 AP", "Columbia Class - Advance Procurement (CY)", 0, 6215939, 5065766,
     "SCN_Book line 231", "Concurrent AP for future Columbia hulls", None),
    ("frow", 56, "SCN", "LI 1045", "Columbia Class - BA-01 rollup (SFF + AP)", [54, 55],
     "SCN_Book line 270 (BA-01 program total)",
     "Program-level BA-01 authority = construction + concurrent AP", "SCN_COLUMBIA_FY25"),
    ("row", 57, "SCN", "LI 2013", "Virginia Class Submarine (parent aggregate)", 7298145, 9599908,
     816705, "SCN_Book parent aggregate line 310+SFF+CPY",
     "SSN Block V/VI construction + SFF + Completion PY adjustments", "SCN_VIRGINIA_FY25"),
    ("row", 58, "SCN", "LI 2086", "CVN Refueling Overhauls (net FY execution)", 42422, 1480314,
     1779011, "SCN_Book lines 357-362 (net of AP/SFF)",
     "Single-year RCOH execution authority (CVN-74 Stennis); not standing multi-ship program total",
     "SCN_CVN_RCOH_FY25"),
    ("row", 59, "SCN", "LI 2001", "Carrier Replacement Program - CVN-80 (parent)", 1729021, 1359124,
     1046700, "SCN_Book lines 280-281 (SFF + Completion PY)",
     "CVN-80 USS Enterprise construction (HII Newport News)", "SCN_CVN_REPL_FY25"),
    ("row", 60, "SCN", "LI 2004", "CVN-81", 800492, 674930, 1622935, "SCN_Book line 307 (SFF for FY 2020)",
     "CVN-81 USS Doris Miller construction (HII Newport News)", "SCN_CVN81_FY25"),
    ("sec", "USCG Cutter Sustainment - PC&I In-Service Vessel Sustainment"),
    ("row", 62, "USCG PC&I", "ISVS total", "In-Service Vessel Sustainment (PPA total)", 120000, 120000,
     152000, "USCG_Justification line 128 / 2133",
     "Coast Guard cutter SLEP / MMA umbrella line (PC&I capital, not OE)", "USCG_ISVS_TOTAL_FY25"),
    ("row", 63, "USCG PC&I", "ISVS 47MLB", "  47-Foot Motor Lifeboat SLEP", 43000, 43000, 45000,
     "USCG_Justification line 2378", "20-year service-life extension for 47-ft motor lifeboat fleet",
     "USCG_ISVS_47MLB_FY25"),
    ("row", 64, "USCG PC&I", "ISVS WMEC", "  270-foot Medium Endurance Cutter (WMEC) SLEP", 46200,
     46200, 76000, "USCG_Justification", "270-ft Famous Class cutter SLEP production", "USCG_ISVS_WMEC_FY25"),
    ("row", 65, "USCG PC&I", "ISVS Healy", "  CGC Healy SLEP", 13000, 13000, 11000, "USCG_Justification",
     "Medium polar icebreaker SLEP (detail design + procurement)", "USCG_ISVS_HEALY_FY25"),
    ("sec", "NWCF Memo - Navy Working Capital Fund"),
    ("row", 67, "NWCF", "NWCF", "Navy-wide NWCF Budget Authority (memo)", None, None, 40300000,
     "NWCF_Book",
     "Navy-wide revolving fund; no clean public-shipyard-only line published. Public-yard workload "
     "is cross-charged into OMN via NWCF customer rates.", None),
]

_S2_HEADERS = ["Line Item", "Appropriation", "Line", "FY24 Actuals $K", "FY25 Enacted $K",
               "FY26 Request $K", "Source"]


def _build_body():
    name_cell: dict[str, int] = {}        # defined name -> native row of its value cell
    name_col: dict[str, str] = {}         # defined name -> value column ("D" for §1, "F" for §2)
    # Start at row 4: _render() emits the sheet title banner at row 2 and leaves row 3
    # blank, so the body's first section banner must begin at row 4 (else the §1 banner
    # collides with the title on row 2 - the historical duplicate-<row r="2"> bug).
    c = RowCursor(4)

    # §1 deck evidence anchors (value in col D)
    s1_banner_row = c.banner("§1 - Deck evidence anchors (values in $M unless noted)",
                             n_cols=_S1_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    assert s1_banner_row == 4, (
        f"Reconciliation §1 banner landed at row {s1_banner_row}, expected 4 "
        f"(title row 2 + blank row 3 are emitted in _render); body must start at RowCursor(4)")
    c.blank()
    c.write(["Anchor", "Line", "Value ($M)"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER])
    for label, name, value, _slide, _note in _ANCHORS_BEFORE:
        r = c.write([label, name, value],
                    styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT],
                    outline_level=1)
        name_cell[name], name_col[name] = r, "D"

    # deferred RECONCILED_MRO_TAM row (formula spliced at render behind a lazy import)
    rows_before = list(c.rows)
    recon_row = c.at()
    name_cell["RECONCILED_MRO_TAM"], name_col["RECONCILED_MRO_TAM"] = recon_row, "D"
    c.blank()                              # reserve the deferred row
    c.rows = []                            # subsequent rows belong to the 'after' bucket

    for label, name, value, _slide, _note in _ANCHORS_AFTER:
        r = c.write([label, name, value],
                    styles=[S_DEFAULT, S_DEFAULT, S_NUM_INPUT],
                    outline_level=1)
        name_cell[name], name_col[name] = r, "D"
    c.blank(2)

    # §2 budget-anchor table (collapsible; Line Item leads in col B; FY25 Enacted = col F).
    # A plain styled range (not a native ExcelTable) so the appropriation sub-bands can be
    # full-width collapsible subsection banners.
    c.banner("§2 - FY2025 appropriation attribution & budget anchors", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(_S2_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_LEFT,
                                 S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER,
                                 S_HEADER_LEFT])
    pos: dict[int, int] = {}               # v433 row -> native row
    # Line Item leads at col B, so the amount columns are E/F/G:
    # FY24 Actuals = E, FY25 Enacted = F, FY26 Request = G.
    _FY24, _FY25, _FY26 = "E", "F", "G"
    for entry in _S2:
        if entry[0] == "sec":
            c.banner(entry[1], n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
            continue
        if entry[0] == "row":
            _, v433r, appr, line, li, fy24, fy25, fy26, src, _desc, name = entry
            # Leading-space "of which..." sub-bands are components of the SAG/total above
            # them: carry the hierarchy in the indent style (on the Line Item column), not in
            # fake whitespace.
            li_style = S_LABEL_INDENT_1 if li.startswith(" ") else S_DEFAULT
            r = c.write([li.lstrip(), appr, line, fy24, fy25, fy26, src],
                        styles=[li_style, S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_NUM_INPUT,
                                S_NUM_INPUT, S_DEFAULT],
                        outline_level=1)
        else:  # frow
            _, v433r, appr, line, li, src_rows, src, _desc, name = entry
            f24 = "=" + "+".join(f"{_FY24}{pos[rr]}" for rr in src_rows)
            f25 = "=" + "+".join(f"{_FY25}{pos[rr]}" for rr in src_rows)
            f26 = "=" + "+".join(f"{_FY26}{pos[rr]}" for rr in src_rows)
            r = c.write([li, appr, line, f24, f25, f26, src],
                        styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM, S_NUM, S_NUM,
                                S_DEFAULT],
                        outline_level=1)
        pos[v433r] = r
        if name:
            name_cell[name], name_col[name] = r, _FY25     # FY25 Enacted cell (col F)

    return rows_before, recon_row, list(c.rows), name_cell, name_col


_rows_before, _RECON_ROW, _rows_after, _NAME_CELL, _NAME_COL = _build_body()


# accessors (load-bearing; consumed by Services §6/§7 [bare name today], OP-5, Output)

def _cell(name): return f"'{_TAB}'!{_NAME_COL[name]}{_NAME_CELL[name]}"
def _c1(name): return _cell(name)
def _c2(name): return _cell(name)


def reconciled_mro_tam_cell(): return _c1("RECONCILED_MRO_TAM")
def public_shipyard_nwcf_cell(): return _c1("PUBLIC_SHIPYARD_NWCF")
def hii_mt_rev_cell(): return _c1("HII_MT_FY25_REV")
def hii_mt_oi_cell(): return _c1("HII_MT_FY25_OI")
def hii_mt_svc_mix_cell(): return _c1("HII_MT_FY25_SVC_MIX_PCT")


def psc1905_mro_cell(bucket):
    name = f"PSC1905_MRO_{bucket}"
    if name not in _NAME_CELL:
        raise ValueError(f"PSC1905 MRO: unknown bucket {bucket!r}")
    return _c1(name)


def mro_tas_cell(key):
    name = f"MRO_TAS_{key}_FY25"
    if name not in _NAME_CELL:
        raise ValueError(f"MRO TAS: unknown key {key!r}")
    return _c2(name)


def omn_cell(key):
    name = f"OMN_{key}_FY25"
    if name not in _NAME_CELL:
        raise ValueError(f"OMN: unknown key {key!r}")
    return _c2(name)


def scn_cell(key):
    name = f"SCN_{key}_FY25"
    if name not in _NAME_CELL:
        raise ValueError(f"SCN: unknown key {key!r}")
    return _c2(name)


def uscg_isvs_cell(key):
    name = f"USCG_ISVS_{key}_FY25"
    if name not in _NAME_CELL:
        raise ValueError(f"USCG ISVS: unknown key {key!r}")
    return _c2(name)


def _render() -> WorksheetSpec:
    # Lazy import breaks the (future) Reconciliation <-> Services cycle: the only
    # back-link to Services is RECONCILED_MRO_TAM, spliced in here.
    from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell
    recon = write_row(
        _RECON_ROW,
        [_RECON_LABEL, "RECONCILED_MRO_TAM",
         f"={navy_tam_svc_cell()}+{cg_tam_svc_cell()}+D{_NAME_CELL['PSC1905_MRO_EMBEDDED']}"],
        styles=[S_DEFAULT, S_DEFAULT, S_NUM],
        start_col=1, outline_level=1)
    title = banner_row(2, _TAB, n_cols=_NCOLS, style=S_TITLE_SHEET, with_gutter=True)
    rows = [title] + _rows_before + [recon] + _rows_after
    ws = worksheet(rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


RECONCILIATION = SheetEntry(_TAB, _GROUP, _render)
