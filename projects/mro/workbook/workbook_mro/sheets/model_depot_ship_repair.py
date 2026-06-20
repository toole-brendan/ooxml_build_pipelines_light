"""Depot Ship Repair - J998/J999 non-nuclear ship-repair deep dive (availability /
RMC / contractor-tier / hull cross-tabs over the J998J999Data table).

Every $ / count cell is a live SUMIFS / COUNTIFS over ``J998J999Data`` via the
_crosstab.sumifs_j / countifs_j builders (structured refs, position-independent); intra-
sheet ratios / subtotals reference captured row positions. The 12 sections cover the
availability / RMC / contractor-tier / hull cross-tabs. (A "Top 15 Parent IDV Vehicles"
cut is omitted - J998J999Data carries no IDV-PIID dimension to compute it.)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER,
    S_NUM, S_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets._crosstab import sumifs_j, countifs_j

_GROUP = "model"
_TAB = "Depot Ship Repair"
_NCOLS = 20                     # B..U (the §4 group x hull matrix is the widest)
_COLS = [34, 28, 20] + [13] * 17

_OBL = "FY2025 Obligation"

# dimension axes (transcribed once from the v4.33 grid)
# §2 condensed / §8 / §10 column axis (11 availability groups).
_AVAIL_GROUPS_11 = [
    "Drydocked Availability", "Pierside Availability", "Continuous Maintenance (CMAV)",
    "MSC Availability", "USCG / FDNF Pierside", "Emergent & Voyage Repair",
    "Inspection/Survey", "Shipyard Production Labor", "Support Infrastructure",
    "Other / Sub-availability", "Out of Scope (FMS)",
]
# §4 row axis (9 availability groups - no Shipyard Production Labor / Out of Scope).
_AVAIL_GROUPS_9 = [
    "Drydocked Availability", "Pierside Availability", "Continuous Maintenance (CMAV)",
    "MSC Availability", "USCG / FDNF Pierside", "Emergent & Voyage Repair",
    "Inspection/Survey", "Support Infrastructure", "Other / Sub-availability",
]
# §3 availability types (27).
_AVAIL_TYPES = [
    "DSRA", "DPIA", "EDSRA", "DMP", "Drydock (other)", "SRA", "PIA/CIA", "PSA", "PMAV",
    "CNO Availability", "Maintenance Availability (unspec)", "CMAV",
    "Regular Overhaul (MSC)", "Mid-Term Availability (MSC)", "Selected Interim Avail (MSC)",
    "CAT A/B Work (MSC)", "DOS Period (MSC)", "Deactivation Availability (MSC)",
    "Dockside Repair", "Lay Berth Repair", "Emergent", "Voyage Repair", "Inspection/Survey",
    "Shipyard Production Labor", "Floating Support Infra", "FMS (Out of Scope)", "Other",
]
# §5 vessel categories (8).
_VESSEL_CATS = [
    "Surface Combatants", "Amphibious Warfare Ships", "Aircraft Carriers",
    "Combat Logistics & MSC", "Submarines", "USCG Cutters", "Mine Warfare",
    "Other / Unclassified",
]
# §4 hull programs (18 columns).
_HULL_PROGRAMS = [
    "DDG", "LPD", "T-AO", "LCS", "LHA", "CVN", "LHD", "LSD", "T-AKE", "AS", "T-EPF",
    "T-AH", "CG", "SSN", "WMEC", "WMSL", "WPC", "WLB",
]
# §9 / §10 / §11 contractor tiers (5).
_TIERS = ["Tier 1 - CONUS Complex Repair Prime", "Tier 2 - Regional Repair",
          "Tier 3 - Technical Services", "Tier 4 - FDNF Foreign Yard", "Other"]
# §6 / §7 regional maintenance centers: (rmc, geography, lead-prime display, lead crit).
# Corporate-parent criteria preserved EXACTLY (incl. load-bearing double-spaces).
_RMC = [
    ("SWRMC", "Pacific / San Diego", "BAE Systems", "BAE Systems"),
    ("MARMC", "Atlantic / Norfolk", "General Dynamics", "General Dynamics"),
    ("SERMC", "Southeast / Mayport", "BAE Systems", "BAE Systems"),
    ("NW RMC / Puget Sound", "Pacific NW / Bremerton", "Huntington Ingalls Industries",
     "Huntington Ingalls Industries"),
    ("Pearl Harbor RMC", "Hawaii", "Pacific Shipyards International LLC",
     "PACIFIC SHIPYARDS INTERNATIONAL  LLC"),
    ("SRF-JRMC Yokosuka", "WESTPAC / Japan", "Sumitomo Heavy Industries Ltd",
     "SUMITOMO HEAVY INDUSTRIES  LTD"),
    ("FDRMC Naples", "EU / Mediterranean", "Navantia S.A. S.M.E.", "NAVANTIA  S.A.  S.M.E."),
    ("FLC Bahrain", "Arabian Gulf", "Arab Shipbuilding & Repair Yard Co. (Asry)",
     "ARAB SHIPBUILDING & REPAIR YARD CO. (ASRY)"),
    ("Military Sealift Cmd", "MSC HQ (non-regional)", "Detyens Shipyards Inc.",
     "DETYENS SHIPYARDS  INC."),
    ("NAVSEA HQ", "DC / HQ", "Vigor Marine LLC", "VIGOR MARINE LLC"),
    ("Portsmouth NSY", "Portsmouth NSY", "Mills Marine & Ship Repair LLC",
     "MILLS MARINE & SHIP REPAIR LLC"),
    ("Norfolk NSY", "Norfolk NSY", "Qed Systems Inc.", "QED SYSTEMS  INC."),
    ("NUWC", "NUWC (Newport)", "Amentum Services Inc.", "AMENTUM SERVICES  INC."),
    ("Army/USACE", "Army Watercraft", "Vigor Marine LLC", "VIGOR MARINE LLC"),
    ("USCG SFLC", "USCG - Baltimore", "Jag Industrial Services Inc",
     "JAG INDUSTRIAL SERVICES  INC"),
    ("Other", "Other / Unclassified", "Bay Ship & Yacht Co.", "BAY SHIP & YACHT CO."),
]
# §11 top contractors per tier: (display, corporate-parent criterion).
_TIER_CONTRACTORS = [
    ("Tier 1 - CONUS Complex Repair Prime", [
        ("BAE Systems", "BAE Systems"),
        ("General Dynamics", "General Dynamics"),
        ("Huntington Ingalls Industries", "Huntington Ingalls Industries"),
        ("Vigor Marine LLC", "VIGOR MARINE LLC"),
        ("Detyens Shipyards Inc.", "DETYENS SHIPYARDS  INC."),
    ]),
    ("Tier 2 - Regional Repair", [
        ("East Coast Repair & Fabrication LLC", "EAST COAST REPAIR & FABRICATION  LLC"),
        ("Pacific Shipyards International LLC", "PACIFIC SHIPYARDS INTERNATIONAL  LLC"),
        ("Alabama Shipyard LLC", "ALABAMA SHIPYARD LLC"),
        ("Bay Ship & Yacht Co.", "BAY SHIP & YACHT CO."),
        ("Bayonne Drydock & Repair Corp.", "BAYONNE DRYDOCK & REPAIR CORP."),
    ]),
    ("Tier 3 - Technical Services", [
        ("Epsilon Systems Solutions Inc.", "EPSILON SYSTEMS SOLUTIONS  INC."),
        ("Amentum Services Inc.", "AMENTUM SERVICES  INC."),
        ("Southcoast Welding & Manufacturing LLC.", "SOUTHCOAST WELDING & MANUFACTURING  LLC."),
        ("Man Energy Solutions Middle East L.L.C", "MAN ENERGY SOLUTIONS MIDDLE EAST L.L.C"),
        ("Man Energy Solutions Singapore Pte. Ltd.", "MAN ENERGY SOLUTIONS SINGAPORE PTE. LTD."),
    ]),
    ("Tier 4 - FDNF Foreign Yard", [
        ("Sumitomo Heavy Industries Ltd", "SUMITOMO HEAVY INDUSTRIES  LTD"),
        ("Navantia S.A. S.M.E.", "NAVANTIA  S.A.  S.M.E."),
        ("Hanwha Ocean Co. Ltd.", "HANWHA OCEAN CO.  LTD."),
        ("Cabras Marine Corporation", "CABRAS MARINE CORPORATION"),
        ("Unithai Shipyard & Engineering Limited - Branch",
         "UNITHAI SHIPYARD & ENGINEERING LIMITED - BRANCH"),
    ]),
    ("Other", [
        ("Colonna's Ship Yard Incorporated", "COLONNA'S SHIP YARD  INCORPORATED"),
        ("Austal USA LLC", "AUSTAL USA  LLC"),
        ("American Maritime Holdings Inc.", "AMERICAN MARITIME HOLDINGS  INC."),
        ("Jag Alaska Inc.", "JAG ALASKA INC."),
        ("Delphinus Engineering Inc.", "DELPHINUS ENGINEERING  INC."),
    ]),
]
# §12 top 15 task orders: (piid, ship, hull, availability type, rmc, recipient).
_TASK_ORDERS = [
    ("N0002425C4411", "USS GREEN BAY (LPD-20)", "LPD", "DSRA", "SWRMC",
     "BAE Systems San Diego Ship Repair Inc."),
    ("N0002425C4404", "USS AMERICA (LHA-6)", "LHA", "DSRA", "SWRMC",
     "General Dynamics Corporation"),
    ("N0002425C4415", "-", None, "DSRA", "SWRMC",
     "BAE Systems San Diego Ship Repair Inc."),
    ("N4523A25F0302", "CVN-76", "CVN", "DPIA", "NW RMC / Puget Sound", "Metro Machine Corp"),
    ("N0002425C4402", "USS KIDD (DDG-100)", "DDG", "DMP", "NW RMC / Puget Sound",
     "Vigor Marine LLC"),
    ("N0002425C4400", "-", None, "DSRA", "MARMC", "General Dynamics Corporation"),
    ("N0002425C4412", "USS LABOON (DDG-58)", "DDG", "DSRA", "MARMC",
     "BAE Systems Norfolk Ship Repair Inc."),
    ("N0002424C4423", "USS HALSEY (DDG-97)", "DDG", "DMP", "SWRMC",
     "BAE Systems San Diego Ship Repair Inc."),
    ("N0002425C4427", "USS PORTER (DDG-78)", "DDG", "EDSRA", "MARMC",
     "General Dynamics Corporation"),
    ("N0002425C4421", "DDG-68", "DDG", "DSRA", "SERMC",
     "BAE Systems Jacksonville Ship Repair LLC"),
    ("N0002425C4431", "LPD-21", "LPD", "SRA", "MARMC",
     "Marine Hydraulics International LLC"),
    ("N0002425C4430", "USS WASP (LHD-1)", "LHD", "DSRA", "MARMC",
     "BAE Systems Norfolk Ship Repair Inc."),
    ("N0002425C4422", "USS HARPERS FERRY (LSD-49)", "LSD", "SRA", "SWRMC",
     "General Dynamics Corporation"),
    ("N0002425C4429", "USS RUSSELL (DDG-59)", "DDG", "DSRA", "SWRMC",
     "Continental Maritime of San Diego LLC"),
    ("N0002425C4409", "USS GABRIELLE GIFFORDS (LCS-10)", "LCS", "DSRA", "SWRMC",
     "Vigor Marine LLC"),
]


def _fy(*crit):
    return f"={sumifs_j(_OBL, *crit)}/1000000"


def _cnt(*crit):
    return f"={countifs_j(*crit)}"


def _make():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    def _section(title, n_cols):
        # Banner spans the section's own content width, not the sheet maximum (_NCOLS=20,
        # set by the §4 group x hull matrix) - so narrow sections don't fill across to U.
        c.banner(title, n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()

    # §1 FY2025 TAM - J998/J999 non-nuclear ship repair
    _section("§1 - FY2025 TAM - J998/J999 non-nuclear ship repair", 7)
    c.write(["Bucket", "PSC Scope", "FY25 $M", "% of Total", "# Awards", "# Mods",
             "Avg $M/Award"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * 5, outline_level=1)
    r6 = c.at()
    r7, r8 = r6 + 1, r6 + 2          # gross total at r8 (referenced by % cells)
    c.write(["J998 - East of 108th meridian", "Atlantic, Gulf, EU FDNF",
             _fy(("PSC", "J998")), f"=IFERROR(D{r6}/D{r8},0)", _cnt(("PSC", "J998")),
             f'={sumifs_j("Mod Count", ("PSC", "J998"))}', f"=IFERROR(D{r6}/F{r6},0)"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_NUM, S_NUM], outline_level=1)
    c.write(["J999 - West of 108th meridian", "Pacific, WESTPAC FDNF",
             _fy(("PSC", "J999")), f"=IFERROR(D{r7}/D{r8},0)", _cnt(("PSC", "J999")),
             f'={sumifs_j("Mod Count", ("PSC", "J999"))}', f"=IFERROR(D{r7}/F{r7},0)"],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_NUM, S_NUM], outline_level=1)
    c.total(["Total J998+J999 (gross)", None, f"=SUM(D{r6}:D{r7})", 1,
             f"=SUM(F{r6}:F{r7})", f"=SUM(G{r6}:G{r7})", f"=IFERROR(D{r8}/F{r8},0)"],
            styles=[S_BOLD, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_NUM, S_NUM], n_cols=7,
            outline_level=1)
    r9 = c.at()
    c.write(["Less: FMS (foreign navy, out of scope)", None,
             f'=-{sumifs_j(_OBL, ("Availability Group", "Out of Scope (FMS)"))}/1000000',
             f"=IFERROR(D{r9}/D{r8},0)",
             _cnt(("Availability Group", "Out of Scope (FMS)")), None, None],
            styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_DEFAULT, S_DEFAULT],
            outline_level=1)
    r10 = c.at()
    c.total(["FY25 In-Scope TAM (US Navy + USCG)", None, f"=D{r8}+D{r9}",
             f"=IFERROR(D{r10}/D{r8},0)", f"=F{r8}-F{r9}", None, None],
            styles=[S_BOLD, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_DEFAULT, S_DEFAULT],
            n_cols=7, outline_level=1)
    c.blank(2)

    # generic "dim breakdown" sections (§2/§3/§5/§9)
    def _dim_section(title, label_hdr, dim, items):
        _section(title, 5)
        c.write([label_hdr, "FY25 $M", "% of Total", "# Awards", "Avg $M/Award"],
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * 4, outline_level=1)
        first = c.at()
        total = first + len(items)
        for i, v in enumerate(items):
            r = first + i
            c.write([v, _fy((dim, v)), f"=IFERROR(C{r}/C{total},0)", _cnt((dim, v)),
                     f"=IFERROR(C{r}/E{r},0)"],
                    styles=[S_DEFAULT, S_NUM, S_PCT, S_NUM, S_NUM], outline_level=1)
        c.total(["Total", f"=SUM(C{first}:C{total - 1})", 1,
                 f"=SUM(E{first}:E{total - 1})", f"=IFERROR(C{total}/E{total},0)"],
                styles=[S_BOLD, S_NUM, S_PCT, S_NUM, S_NUM], n_cols=5,
                outline_level=1)
        c.blank(2)

    _dim_section("§2 - FY2025 TAM by availability group (condensed)",
                 "Availability Group", "Availability Group", _AVAIL_GROUPS_11)
    _dim_section("§3 - FY2025 TAM by availability type (detail)",
                 "Availability Type", "Availability Type", _AVAIL_TYPES)

    # §4 group x hull matrix
    def _matrix_section(title, row_hdr, row_dim, row_items, col_dim, col_items):
        ncol = len(col_items)
        _section(title, ncol + 2)                            # row label + cols + total
        lo, hi = col_letter(2), col_letter(1 + ncol)        # data cols (C .. )
        c.write([row_hdr] + col_items + ["Total"],
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (ncol + 1), outline_level=1)
        first = c.at()
        last = first + len(row_items) - 1
        for i, rv in enumerate(row_items):
            r = first + i
            cells = [rv] + [_fy((row_dim, rv), (col_dim, cv)) for cv in col_items] + \
                    [f"=SUM({lo}{r}:{hi}{r})"]
            c.write(cells, styles=[S_DEFAULT] + [S_NUM] * (ncol + 1), outline_level=1)
        trow = c.at()
        totals = [f"=SUM({col_letter(2 + j)}{first}:{col_letter(2 + j)}{last})"
                  for j in range(ncol)]
        c.total(["Total"] + totals + [f"=SUM({lo}{trow}:{hi}{trow})"],
                styles=[S_BOLD] + [S_NUM] * (ncol + 1), n_cols=ncol + 2,
                outline_level=1)
        c.blank(2)

    _matrix_section("§4 - FY2025 $M - availability group x hull program",
                    "Availability Group", "Availability Group", _AVAIL_GROUPS_9,
                    "Hull Program", _HULL_PROGRAMS)

    _dim_section("§5 - FY2025 TAM by vessel category (deck-facing rollup)",
                 "Vessel Category", "Vessel Category", _VESSEL_CATS)

    # §6 TAM by RMC (with geography)
    _section("§6 - FY2025 TAM by regional maintenance center", 6)
    c.write(["RMC", "Geography", "FY25 $M", "% of Total", "# Awards", "Avg $M/Award"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * 4, outline_level=1)
    first6 = c.at()
    total6 = first6 + len(_RMC)
    for i, (rmc, geo, _ld, _lc) in enumerate(_RMC):
        r = first6 + i
        c.write([rmc, geo, _fy(("RMC", rmc)), f"=IFERROR(D{r}/D{total6},0)",
                 _cnt(("RMC", rmc)), f"=IFERROR(D{r}/F{r},0)"],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_NUM], outline_level=1)
    c.total(["Total", None, f"=SUM(D{first6}:D{total6 - 1})", 1,
             f"=SUM(F{first6}:F{total6 - 1})", f"=IFERROR(D{total6}/F{total6},0)"],
            styles=[S_BOLD, S_DEFAULT, S_NUM, S_PCT, S_NUM, S_NUM], n_cols=6,
            outline_level=1)
    c.blank(2)

    # §7 lead prime per RMC
    _section("§7 - Lead prime per RMC (FY2025, $M)", 6)
    c.write(["RMC", "Geography", "RMC FY25 $M", "Lead Consolidated Parent", "Lead $M",
             "% of RMC"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT,
                    S_HEADER_CENTER, S_HEADER_CENTER], outline_level=1)
    for rmc, geo, lead, crit in _RMC:
        r = c.at()
        c.write([rmc, geo, _fy(("RMC", rmc)), lead,
                 _fy(("RMC", rmc), ("Corporate Parent", crit)), f"=IFERROR(F{r}/D{r},0)"],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_DEFAULT, S_NUM, S_PCT],
                outline_level=1)
    c.blank(2)

    _matrix_section("§8 - FY2025 $M - RMC x availability group",
                    "Regional Maintenance Center", "RMC", [r[0] for r in _RMC],
                    "Availability Group", _AVAIL_GROUPS_11)

    _dim_section("§9 - FY2025 TAM by contractor tier", "Contractor Tier",
                 "Contractor Tier", _TIERS)

    _matrix_section("§10 - FY2025 $M - contractor tier x availability group",
                    "Contractor Tier", "Contractor Tier", _TIERS,
                    "Availability Group", _AVAIL_GROUPS_11)

    # §11 top contractors within each tier
    _section("§11 - Top contractors within each tier (FY2025, $M)", 5)
    c.write(["Tier", "Consolidated Parent", "FY25 $M", "% of Tier", "# Awards"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * 3, outline_level=1)
    for tier, contractors in _TIER_CONTRACTORS:
        c.banner(tier, n_cols=5, style=S_TITLE_SUBSECTION, mark_collapsible=True)
        tier_total = f"{sumifs_j(_OBL, ('Contractor Tier', tier))}/1000000"
        for disp, crit in contractors:
            r = c.at()
            c.write([None, disp, _fy(("Contractor Tier", tier), ("Corporate Parent", crit)),
                     f"=IFERROR(D{r}/({tier_total}),0)",
                     _cnt(("Contractor Tier", tier), ("Corporate Parent", crit))],
                    styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_PCT, S_NUM], outline_level=1)
    c.blank(2)

    # §12 top 15 task orders
    _section("§12 - Top 15 task orders by FY25 obligation", 9)
    c.write(["Rank", "PIID", "Ship", "Hull Program", "Availability Type", "RMC",
             "Recipient", "FY25 $M", "# Mods"],
            styles=[S_HEADER_CENTER] + [S_HEADER_LEFT] * 6 + [S_HEADER_CENTER] * 2,
            outline_level=1)
    for i, (piid, ship, hull, avail, rmc, recip) in enumerate(_TASK_ORDERS, 1):
        c.write([i, piid, ship, hull, avail, rmc, recip,
                 _fy(("PIID", piid)), f'={sumifs_j("Mod Count", ("PIID", piid))}'],
                styles=[S_DEFAULT] * 7 + [S_NUM, S_NUM], outline_level=1)
    c.blank(2)
    # (v4.33 §13 "Top 15 Parent IDV Vehicles" was a header-only stub - never populated,
    #  and J998J999Data has no IDV-PIID dimension to compute it - so it is omitted.)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


DEPOT_SHIP_REPAIR = _make()
