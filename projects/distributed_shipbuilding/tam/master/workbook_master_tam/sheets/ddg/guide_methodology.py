"""guide_methodology - the "Methodology" tab (DDG, guide group; one module = one sheet).

The analytical method sheet, structured to match the submarine Methodology tab:
definitions, the formula framework, the market-sizing flow, the scope boundary,
exclusion rules, the bucket taxonomy, and the classification precedence. Table-first,
minimal prose; a few live figures (coefficients, gated/GFE corpus) come in via
cross-sheet links. DDG-specific additions vs the submarine sheet: the MYP-correction
sub-section (§2c) and the named-contaminants table (§5b).

The bucket vocabulary + classify() live in the ``_taxonomy`` leaf (not here); this
module renders them. Pure consumer (no accessors).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_LINK_NUM, S_LINK_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg.model_tam_build import (
    bc_supplier_coeff_cell, ap_lltm_supplier_coeff_cell,
)
from workbook_master_tam.sheets.ddg.validation_pop_source_audit import (
    gated_dollar_cell, gfe_excluded_dollar_cell,
)
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "guide"
_TAB = "DDG Methodology"
_NCOLS = 4


def _render_methodology() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Definitions
    c.banner("§1 - Definitions", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Term", "Definition", "Treatment"], styles=S_HEADER_LEFT)
    _dn = {}
    for term, defn, treat in [
        ("TAM", "non-GFE, non-MIB new-construction supplier opportunity", "BC base x coeff + AP/LLTM base x coeff"),
        ("BC", "Basic Construction (P-5c)", "the headline TAM stream"),
        ("AP/LLTM/EOQ", "advance procurement / long-lead material / EOQ", "additive stream, supplier-addressable portion"),
        ("GFE", "government-furnished equipment / weapons", "excluded from TAM"),
        ("MIB", "maritime industrial base / capacity", "excluded"),
        ("POP", "place of performance", "drives the supplier coefficient"),
        ("Supplier coefficient", "$-weighted supplier+foreign POP share", "applied to each stream base"),
        ("MYP correction", "redacted MYP masters folded back at reconstructed POP", "corrects the BC coefficient"),
    ]:
        _dn[term] = c.write([term, defn, treat], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Formula framework
    c.banner("§2 - Formula framework", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - TAM framework", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["TAM = BC base x BC supplier coefficient + AP/LLTM base x AP/LLTM supplier coefficient"], styles=[S_DEFAULT])
    c.write(["Both streams contribute; the BC coefficient is MYP-corrected (see §2c)."], styles=[S_DEFAULT])
    c.write(["Coefficient (live)", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Applied BC supplier coefficient", f"={bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    c.write(["AP/LLTM supplier coefficient", f"={ap_lltm_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    c.blank()
    c.banner("§2b - MYP correction", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["BC coefficient is measured on the non-GFE BC corpus, with the two $-redacted MYP masters folded back at their announced POP ($ reconstructed from FPDS + trade press)."], styles=[S_DEFAULT])
    c.write(["POP figure", "Meaning"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for fig, mean in [
        ("~87% disclosed outside-yards", "redaction artifact; the $-redacted masters drop out of the denominator"),
        ("~42% MYP-corrected outside-yards", "the 0.42 anchor, with the masters folded back"),
        ("25.3% applied BC coefficient (FY23-27)", "over the non-GFE BC corpus - the value actually used"),
        ("22.0% FY2022-vintage BC coefficient", "FY18-22 masters' announced POP (2018-09-27 bulletin); applied to FY2022 only"),
    ]:
        c.write([fig, mean], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§2c - Penetration & outyear outlook", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Penetration = Outsourced BC TAM (both streams) / total ship spend (P-5c Total Ship Estimate + OBBBA gross), constant FY2026 $."], styles=[S_DEFAULT])
    c.write(["Window averages are ratios of sums; implied FY28-31 Outsourced BC = PB2027 FYDP gross x penetration, low = FY22-25 average, high = low x (1 + stated outsourcing-intent uplift, Assumptions §7)."], styles=[S_DEFAULT])
    c.write(["FYDP outyears are the PB2027 request, not appropriation; FY2030-FY2031 deflators are extrapolated (Deflators tab)."], styles=[S_DEFAULT])
    c.blank(2)
    c.banner("§2d - Evidence basis by fiscal year", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["FY", "Dollar basis", "Outsourced % basis"], styles=S_HEADER_LEFT)
    for fy, dollars, pct in [
        ("2022", "Settled actuals (PB >= FY+2 vintage rule)",
         "Announced POP of the FY18-22 MYP masters funding the FY22 ships (22.0%; CITE-10)"),
        ("2023-2025", "Settled actuals",
         "Announced POP of the FY23-27 MYP masters funding those ships (25.3% corpus coefficient; CITE-01)"),
        ("2026", "Enacted: PB2027 P-5c + OBBBA PL 119-21 mandatory",
         "Same 25.3% (FY26 ships are options under the FY23-27 masters); the OBBBA BC/GFE split (62.8%) is the one assumption layer"),
        ("2027", "PB2027 request - not yet appropriated",
         "Same 25.3% (the Ingalls master covers the FY27 ship); estimate until appropriation"),
        ("2028-2031", "PB2027 FYDP request (Outlook only; outside TAM)",
         "Penetration assumption, not announcement POP - styled as an estimate"),
    ]:
        c.write([fy, dollars, pct], styles=S_DEFAULT, outline_level=1)
    c.write(["Announced POP is the contract-level planned distribution ('Work will be performed in...'), not realized per-FY actuals."], styles=[S_DEFAULT])
    c.write(["The AP/LLTM stream (FY25-26 only) is budget-exhibit classification (P-10 Ship Construction EOQ, CITE-09), not announcement POP."], styles=[S_DEFAULT])
    c.blank(2)

    # §3 Market-sizing flow
    c.banner("§3 - Market-sizing flow", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "Input", "Method", "Output tab"], styles=S_HEADER_LEFT)
    for step, inp, method, tab in [
        ("Budget base", "SCN P-5c + P-10", "extract per class/FY", "SCN Budget / AP Bridge"),
        ("Add OBBBA mandatory BC (Sec. 20002(17))", "mandatory allocation plan", "gross x BC share", "OBBBA Mandatory"),
        ("Remove GFE / non-addressable / dup AP", "budget base", "exclusion rules", "TAM Build"),
        ("Apply POP supplier coefficient", "in-scope base", "POP $-weighted share", "TAM Build"),
        ("Portfolio TAM", "BC + AP/LLTM streams", "base x coefficient", "TAM Build"),
        ("Penetration & outyear outlook", "TAM + ship spend + PB2027 FYDP gross", "TAM / spend; FYDP x penetration range", "Outlook"),
    ]:
        c.write([step, inp, method, tab], styles=S_DEFAULT, outline_level=1)
    c.blank(2)

    # §4 Scope boundary
    c.banner("§4 - Scope boundary", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§4a - In TAM", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in ["Basic Construction, non-GFE",
                "Supplier-addressable component work, per award description",
                "Work away from prime / co-prime / GFE sites",
                "Eligible AP / LLTM / EOQ (additive only)",
                "OBBBA mandatory BC share (Sec. 20002(17): two FY2026 ships, DDG 147/149)"]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§4b - Out of TAM", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in ["GFE / Aegis / SPY-6 / VLS / weapons / ordnance",
                "MIB / industrial-base capacity (incl. the other OBBBA Sec. 20002 lines)",
                "Sustainment / depot / design-only work",
                "Prime / co-prime final-assembly yard work (BIW, Ingalls)",
                "AP/LLTM already inside BC"]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§4c - Mandatory (OBBBA) funding treatment", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in [
        "OBBBA Sec. 20002(17): $5.4B FY2026 mandatory funding for two DDG-51 destroyers "
        "(DDG 147/149) under the current MYP; the FY27 PB P-1 carries zero FY2026 "
        "discretionary quantity.",
        "The award covers basic construction and GFE with no breakout; the BC portion uses "
        "the P-5c BC/GFE cost structure (Assumptions knob) and the GFE share is excluded "
        "from TAM.",
        "Booked in FY2026 on budget-year basis (awards from Q2 FY2026; obligation authority "
        "through 2029-09-30); FY2027 is discretionary-only.",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 Exclusion rules
    c.banner("§5 - Exclusion rules", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Exclusion category", "Treatment", "Rationale", "Evidence tab"], styles=S_HEADER_LEFT)
    for cat, treat, why, tab in [
        ("Mission systems", "exclude", "combat/electronics (VLS launch-control, radar, EW) - different market", "Entity Master"),
        ("GFE", "exclude", "Navy-directed equipment / weapons", "SCN Budget"),
        ("MIB", "exclude", "industrial-base capacity, not construction", "Scope Exclusions"),
        ("Prime yard", "exclude", "BIW final-assembly work, not addressable", "POP Corpus"),
        ("Co-prime yard", "exclude", "Ingalls site work, not addressable", "POP Corpus"),
        ("Foreign / FMS", "exclude", "foreign supplier / FMS, not US yard-side", "Entity Master"),
        ("Holding / IT / services", "exclude", "holding co (5511), IT resellers, eng services", "Entity Master"),
        ("Sustainment / depot", "exclude", "in-service, not new construction", "Scope Exclusions"),
        ("Design-only", "exclude", "engineering only, no hardware", "POP Corpus"),
        ("AP/LLTM already in BC", "exclude", "booked inside BC; no double-count", "AP Bridge"),
        ("Service / non-component", "exclude", "service NAICS, not manufacturing", "Entity Master"),
    ]:
        c.write([cat, treat, why, tab], styles=S_DEFAULT, outline_level=1)
    c.blank()
    c.banner("§5a - Effect on the corpus (live)", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Gated TAM corpus", f"={gated_dollar_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["less: GFE / excluded scope", f"={gfe_excluded_dollar_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.blank()
    c.banner("§5b - Named contaminants", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Item", "Identifier", "Why excluded"], styles=S_HEADER_LEFT)
    for item, ident, why in [
        ("IVECO Mk110 gun", "M6785416C0006", "Marine Corps gun, not DDG (~$707M dropped)"),
        ("DDG-1000 / Zumwalt", "LI 2119", "out of class; closed, OPN modernization only"),
        ("Thales ESSM", "N0002415C5420", "NATO cost-share on a Raytheon PIID; WPN-funded (~$4.2B dropped)"),
        ("WPN/OPN weapons", "SM / ESSM / Tomahawk / CIWS", "different appropriation, not SCN"),
    ]:
        c.write([item, ident, why], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # Native Excel Notes: one concise hover per definition, on the LAST column of the §1
    # table (D, Treatment) - the single home for the model's recurring caveats. Other
    # sheets carry the durable evidence in real cells, not notes.
    notes = [
        ExcelNote(f"D{_dn['TAM']}",
                  "Opportunity ceiling, not a forecast: non-GFE, non-MIB new-construction "
                  "supplier $ away from BIW / Ingalls / GFE sites. ~$1,070M/yr (BC ~$897M + "
                  "AP/LLTM ~$174M)."),
        ExcelNote(f"D{_dn['AP/LLTM/EOQ']}",
                  "Additive stream: the P-10 'Ship Construction EOQ' line (FY25 $41.5M + "
                  "FY26 $1,000.0M then-year; PB2027 P-10, LI 2122) at a 1.00 supplier "
                  "coefficient (EOQ = procurements of material items) = ~$1.04B "
                  "(~$174M/yr). Congressional adds (shipyard infrastructure, wages) and "
                  "terminal GFE excluded at the line level; haircuts on Sensitivity."),
        ExcelNote(f"D{_dn['MYP correction']}",
                  "Applied BC coefficient = 25.3% over the non-GFE BC corpus. Keep distinct: "
                  "~87% disclosed (an artifact - $-redacted MYP masters drop out), ~42% "
                  "MYP-corrected outside-yards, 25.3% applied."),
    ]
    ws = worksheet(c.rows, cols=[24, 44, 40, 22], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, notes=notes)


METHODOLOGY = SheetEntry(_TAB, _GROUP, _render_methodology)
