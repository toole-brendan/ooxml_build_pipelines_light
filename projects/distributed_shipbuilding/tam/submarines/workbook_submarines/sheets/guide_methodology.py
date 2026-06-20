"""guide_methodology - the "Methodology" tab (one module = one sheet).

The analytical method sheet (successor to the former README_Methodology, without
the cover / tab-map / version-history front matter): definitions, the formula
framework, the market-sizing flow, the scope boundary, exclusion rules, the bucket
taxonomy, and the classification precedence. The bucket vocabulary + classify() live
in taxonomy.py; this sheet renders them and shows a few live figures (coefficients,
gated/GFE corpus, SIB exclusion) via cross-sheet links. Pure consumer (no accessors).
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
from workbook_submarines.sheets.taxonomy import BUCKETS, UNBUCKETED, NAICS4_BUCKET
from workbook_submarines.sheets.model_tam_build import (
    va_bc_supplier_coeff_cell, col_bc_supplier_coeff_cell, ap_lltm_supplier_coeff_cell,
)
from workbook_submarines.sheets.validation_pop_source_audit import gated_dollar_cell, gfe_excluded_dollar_cell
from workbook_submarines.sheets.validation_sib_excluded import sib_total_cell
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "guide"
_TAB = "Methodology"


def _render_methodology_scope() -> WorksheetSpec:
    n_cols = 4
    c = RowCursor(2)
    c.banner("Methodology", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()

    # §1 Definitions
    c.banner("§1 - Definitions", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Term", "Definition", "Treatment"], styles=S_HEADER_LEFT)
    _dn = {}
    for term, defn, treat in [
        ("TAM", "non-GFE/SIB new-construction supplier opportunity", "BC base x coeff + AP/LLTM base x coeff"),
        ("SAM", "portion of TAM in targeted work-type buckets", "scenario menu"),
        ("BC", "Basic Construction (P-5c, GFE-free)", "the headline TAM stream"),
        ("AP/LLTM", "advance procurement / long-lead material", "reference stream; additive base = 0"),
        ("OBBBA mandatory", "Sec. 20002 mandatory new-construction funding", "gross x BC share x BC coeff; FY26 BA (spillover lever to FY27)"),
        ("GFE", "government-furnished equipment / weapons", "excluded from TAM"),
        ("SIB", "submarine industrial base / capacity grants", "excluded from SAM"),
        ("POP", "place of performance", "drives the supplier coefficient"),
        ("Supplier coefficient", "$-weighted supplier+foreign POP share", "applied to each stream base"),
        ("Worktype share gate", "per-class bucket shares measured on GDEB-PIID subawards, FY2022-25 window", "non-GDEB prime records excluded"),
        ("Distributed-production view", "work away from the final-assembly yard", "appendix context only"),
    ]:
        _dn[term] = c.write([term, defn, treat], styles=[S_BOLD, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Formula framework
    c.banner("§2 - Formula framework", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - TAM framework", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["TAM = BC base x class-vintage BC supplier coefficient + AP/LLTM base x AP/LLTM supplier coefficient"], styles=[S_DEFAULT])
    c.write(["Applied: per-class BC base x its funding construction master's announced-POP coefficient + $0 AP/LLTM base x AP/LLTM reference coeff"], styles=[S_DEFAULT])
    c.write(["Coefficient (live)", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Virginia BC coefficient (Block V announced POP)", f"={va_bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    c.write(["Columbia BC coefficient (Build I announced POP)", f"={col_bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    c.write(["AP/LLTM reference coefficient", f"={ap_lltm_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    c.blank()
    c.banner("§2b - SAM framework", n_cols=n_cols, style=S_TITLE_SUBSECTION)
    c.blank()
    c.write(["SAM scenario = SUMPRODUCT(bucket TAM, scenario inclusion flag)"], styles=[S_DEFAULT])
    c.write(["Bucket shares are per-class per-FY vectors measured on gated evidence: GDEB construction/LLTM PIIDs only (BPMI / LM / BAE / RR prime records excluded), Virginia and Columbia separately, FY2022-FY2025 reporting years -> Worktype by FY."], styles=[S_DEFAULT])
    c.write(["Each class's annual TAM is allocated at its own FY's vector; FY2026-27 use the FY22-25 window vector (no usable subaward reporting yet)."], styles=[S_DEFAULT])
    c.blank()
    c.banner("§2c - Penetration & outyear outlook", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Penetration = Outsourced BC TAM (all streams) / total ship spend (Va + Col Total Ship Estimate + OBBBA gross), constant FY2026 $, measured per class."], styles=[S_DEFAULT])
    c.write(["Window averages are ratios of sums; implied FY28-31 Outsourced BC = each class's PB2027 FYDP gross x its penetration assumption, low = class FY22-25 average, high = low x (1 + stated outsourcing-intent uplift, Assumptions §9); portfolio = Virginia + Columbia."], styles=[S_DEFAULT])
    c.write(["FYDP outyears are the PB2027 request, not appropriation; FY2030-FY2031 deflators are extrapolated (Deflators tab)."], styles=[S_DEFAULT])
    c.blank(2)
    c.banner("§2d - Evidence basis by fiscal year", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["FY", "Dollar basis", "Outsourced % basis"], styles=S_HEADER_LEFT)
    for fy, dollars, pct in [
        ("2022-2025", "Settled actuals (PB >= FY+2 vintage rule)",
         "Class-vintage announced POP of the funding construction masters: Virginia 34% (Block V, 2019-12-02 bulletin), Columbia 22% (Build I, 2020-11-05 bulletin)"),
        ("2026", "Enacted: PB2027 P-5c + OBBBA PL 119-21 Sec. 20002(16) mandatory",
         "Same class coefficients (OBBBA boat is a Virginia -> 34%); the OBBBA BC share (observed Virginia FY26 P-5c ratio, ~58.2%) is the one assumption layer"),
        ("2027", "PB2027 request - not yet appropriated",
         "Same class coefficients; OBBBA FY27 execution spillover defaults to 0 - estimate until appropriation"),
        ("2028-2031", "PB2027 FYDP request (Outlook only; outside TAM)",
         "Penetration assumption, not announcement POP - styled as an estimate"),
    ]:
        c.write([fy, dollars, pct], styles=S_DEFAULT, outline_level=1)
    c.write(["Announced POP is the contract-level planned distribution ('Work will be performed in...'), not realized per-FY actuals."], styles=[S_DEFAULT])
    c.write(["The pooled 2022-2026 corpus coefficient (35.0%) is retained on TAM Build §3a as a reference; Block VI construction is unawarded, so the Virginia row restates on its announcement."], styles=[S_DEFAULT])
    c.write(["The AP/LLTM additive base is 0 (P-10 supplier LLTM already sits inside P-5c BC); no AP coefficient is applied."], styles=[S_DEFAULT])
    c.blank(2)

    # §3 Market-sizing flow
    c.banner("§3 - Market-sizing flow", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "Input", "Method", "Output tab"], styles=S_HEADER_LEFT)
    for step, inp, method, tab in [
        ("Budget base", "SCN P-5c + P-10", "extract per class/FY", "SCN Annual / LLTM AP"),
        ("Add OBBBA mandatory BC (Sec. 20002(16))", "mandatory allocation plan", "gross x BC share", "OBBBA Mandatory"),
        ("Remove GFE / non-addressable / dup AP", "budget base", "exclusion rules", "TAM Build"),
        ("Apply POP supplier coefficient", "in-scope base", "POP $-weighted share", "TAM Build"),
        ("Portfolio TAM", "BC + AP/LLTM + OBBBA streams", "base x coefficient", "TAM Build"),
        ("Gate work-type share evidence", "FFATA subawards", "GDEB PIIDs, per class, FY22-25 window", "Worktype by FY"),
        ("Allocate TAM into buckets", "annual class TAM", "x per-class per-FY modeled share", "SAM Build"),
        ("Apply target scenario flags", "bucket TAM", "SUMPRODUCT with flags", "SAM Build"),
        ("SAM scenario output", "scenario selection", "scenario menu", "SAM Build"),
        ("Penetration & outyear outlook", "TAM + ship spend + PB2027 FYDP gross", "TAM / spend; FYDP x penetration range", "Outlook"),
    ]:
        c.write([step, inp, method, tab], styles=S_DEFAULT, outline_level=1)
    c.blank(2)

    # §4 Scope boundary
    c.banner("§4 - Scope boundary", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§4a - In TAM", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in ["Basic Construction, non-GFE", "Supplier-addressable component procurement",
                "Work away from prime / co-prime / GFE sites", "Eligible AP/LLTM/EOQ only if additive",
                "OBBBA mandatory BC share (Sec. 20002(16): one FY2026 Virginia boat)"]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§4b - Out of TAM", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in ["GFE / weapons / sensors / ordnance", "SIB / industrial-base capacity grants",
                "Sustainment / depot / design-only work", "Prime / co-prime final-assembly yard work",
                "AP/LLTM already inside BC",
                "OBBBA capacity / workforce / repair / nuclear lines (memo on OBBBA Mandatory)"]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §5 Exclusion rules
    c.banner("§5 - Exclusion rules", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Exclusion category", "Treatment", "Rationale", "Evidence tab"], styles=S_HEADER_LEFT)
    for cat, treat, why, tab in [
        ("Mission systems", "exclude", "combat/electronics (sonar, EW, fire-control) - different market", "Entity Master"),
        ("GFE", "exclude", "Navy-furnished equipment / weapons", "SCN Annual"),
        ("SIB", "exclude", "capacity grants, not construction", "SIB Excluded"),
        ("OBBBA capacity lines", "exclude", "capacity / workforce grants, not construction", "OBBBA Mandatory"),
        ("BPMI / naval nuclear", "exclude", "GFE reactor line; out of BC corpus", "Sensitivity"),
        ("Prime yard", "exclude", "final-assembly work, not addressable", "POP Location Parse"),
        ("Co-prime yard", "exclude", "co-prime site work, not addressable", "POP Location Parse"),
        ("Foreign / FMS", "exclude", "foreign supplier / FMS, not US yard-side", "Entity Master"),
        ("Holding / IT / services", "exclude", "holding co (5511), IT resellers, eng services", "Entity Master"),
        ("Design-only", "exclude", "lead-yard design (Plan Costs)", "LLTM AP"),
        ("AP/LLTM already in BC", "exclude", "supplier LLTM booked inside BC", "LLTM AP"),
        ("Service / non-component", "exclude", "service NAICS, not manufacturing", "Entity Master"),
    ]:
        c.write([cat, treat, why, tab], styles=S_DEFAULT, outline_level=1)
    c.blank()
    c.banner("§5a - Effect on the corpus (live)", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Gated TAM corpus", f"={gated_dollar_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["less: GFE / excluded scope", f"={gfe_excluded_dollar_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["SIB exclusion (subaward-level)", f"={sib_total_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.blank(2)

    # §6 Bucket taxonomy
    c.banner("§6 - Bucket taxonomy", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket key", "Display name", "Definition", "Typical evidence"], styles=S_HEADER_LEFT)
    for k, name, defn in BUCKETS:
        c.write([k, name, defn, "Worktype Evidence"], styles=S_DEFAULT, outline_level=1)
    c.write([UNBUCKETED, "Unbucketed / ambiguous", "parent-unknown or no clean NAICS", "Worktype Evidence"],
            styles=S_DEFAULT, outline_level=1)
    c.blank()
    c.banner("§6a - Governing signal: operating-entity resolution (registry)", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Step", "Method"], styles=S_HEADER_LEFT)
    for step, method in [
        ("Key", "each subaward's sub_entity_uei = the operating entity that received the dollars"),
        ("Resolve", "SAM Entity API -> operating-entity legal name + primary NAICS"),
        ("Adjudicate", "evidence registry assigns role + bucket per entity (signed dollars)"),
        ("Why", "Northrop Sunnyvale turbine generators -> electrical (real ship power), not the brand"),
    ]:
        c.write([step, method], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()
    c.banner("§6b - NAICS-4 -> bucket crosswalk (fallback for entities not in the registry)", n_cols=n_cols, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["NAICS-4", "Bucket"], styles=[S_HEADER_CENTER, S_HEADER_LEFT])
    for code in sorted(NAICS4_BUCKET):
        c.write([code, NAICS4_BUCKET[code]], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §7 Classification precedence
    c.banner("§7 - Classification precedence (first match wins)", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Priority", "Rule", "Result", "Example"],
            styles=[S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_LEFT])
    for pri, rule, result, ex in [
        ("1", "Evidence registry (operating-entity UEI)", "role + bucket per registry", "DRS Naval Power -> electrical"),
        ("2", "Prime / co-prime name", "role=prime/co_prime", "Electric Boat, HII-NNS"),
        ("3", "GFE / SIB name", "role=gfe_sib", "Lockheed, BlueForge"),
        ("4", "Vendor-name override", "bucket per override", "Circor->piping"),
        ("5", "NAICS-4 crosswalk (no 3364/3344)", "role=supplier, bucket per NAICS", "3329->piping"),
        ("6", "Service / non-component NAICS", "role=service", "5416 mgmt, 5413 eng"),
        ("7", "Holding (NAICS 5511)", "role=holding (excluded)", "parent-only holding co"),
        ("8", "Foreign-flagged, no NAICS", "role=foreign_fms (excluded)", "foreign supplier / FMS"),
        ("9", "Residual", "role=supplier, bucket=unbucketed", "blank-NAICS, not in registry"),
    ]:
        c.write([pri, rule, result, ex], styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)

    # Native Excel Notes: one concise hover per definition, on the LAST column of the
    # §1 table (D, Treatment). The single home for the model's recurring caveats - other
    # sheets carry the durable evidence in real cells, not notes.
    notes = [
        ExcelNote(f"D{_dn['TAM']}",
                  "Opportunity ceiling, not a forecast: per-class BC base x its funding "
                  "construction master's announced-POP coefficient (Virginia 34.0% Block V, "
                  "Columbia 22.0% Build I)."),
        ExcelNote(f"D{_dn['SAM']}",
                  "Scenario cuts of TAM. Buckets overlap, so shares exceed 100% and must "
                  "not be summed."),
        ExcelNote(f"D{_dn['AP/LLTM']}",
                  "Held at $0: supplier LLTM already sits inside Basic Construction, so adding "
                  "the ~$44.7B P-10 gross would double-count. Reference only."),
        ExcelNote(f"D{_dn['SIB']}",
                  "~$4,252M of SIB capacity / workforce / R&D pass-throughs (mostly BlueForge) - "
                  "future capacity, not component manufacture. Role, not size, decides. "
                  "(SIB = MIB in earlier files.)"),
        ExcelNote(f"D{_dn['OBBBA mandatory']}",
                  "PL 119-21 Title II, Sec. 20002 (FY 2026 Mandatory Funding Allocation Plan): "
                  "$29.2B shipbuilding, all FY2026 budget authority. Only item 16 (second FY26 "
                  "Virginia boat, $4.6B) is new-construction procurement and feeds TAM; capacity / "
                  "workforce lines are memo-excluded like SIB. FY27 receives dollars only via the "
                  "spillover control."),
    ]
    ws = worksheet(c.rows, cols=[24, 42, 38, 22], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws, notes=notes)


METHODOLOGY = SheetEntry(_TAB, _GROUP, _render_methodology_scope)
