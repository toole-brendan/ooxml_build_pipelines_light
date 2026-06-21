"""sources_references - the "References" tab (DDG, sources group; one module = one sheet).

Source / citation registry. Two native tables: tbl_ddg_references_primary (primary
sources & data pulls) and tbl_ddg_references_citations (policy & industry citations).
A source table (the context-note exception), so it keeps short context notes.

Promoted accessor (internal hygiene):
  source_ref_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "sources"
_TAB = "DDG References"
_NCOLS = 6


def _make_references():
    _REF_HEADERS = ["Source ID", "Document / dataset", "Type", "Date",
                    "Location / reference", "Context note"]
    _PRIMARY = [
        ("SRC-01", "DDG-51 SCN budget justification books FY2022-FY2027",
         "Budget exhibit (P-5c/P-10/P-40)", "2021-2026", "budget_books/SCN_Book_FY22..27",
         "Basic Construction, AP/EOQ, cost categories for LI 2122. P-5c categories reconciled "
         "across all six PB vintages (most-recent settled per FY); pre-FY24 HM&E backfilled."),
        ("SRC-02", "SCN cost categories per FY (LI 2122)",
         "Extracted CSV", "FY22-27 PB", "extracted/scn_li_cost_categories.csv (9)",
         "Total ship -> Basic Construction, multi-vintage reconciled. Feeds TAM Build + slide-05 portfolio funnel."),
        ("SRC-03", "SCN production schedule (hull -> yard -> FY)",
         "Extracted CSV", "FY27 PB", "extracted/scn_li_production_schedule.csv (31)",
         "DDG 126-156 -> BIW or Ingalls. Drives per-yard BC allocation."),
        ("SRC-04", "DoD/DoW daily contract announcements + POP",
         "Press releases (>=$7.5M)", "CY2022-2026", "extracted/dod_announcement_pop.csv (860)",
         "POP % by action; 152 TAM-relevant. MYP master $ redacted here."),
        ("SRC-05", "DoD announcement POP rollup by work-type",
         "Extracted CSV", "CY2022-2026", "extracted/dod_action_pop_by_worktype.csv (36)",
         "Dollar-weighted POP shares by program x work-type."),
        ("SRC-06", "FPDS de-capped prime pulls (BIW + Rolls-Royce)",
         "FPDS Atom feed (raw JSON)", "2017-2026", "fpds_raw_v2/ (BIW 30,236 / RR 3,562)",
         "Recovers vendor slugs past the FPDS cap. Prime-obligation sizing."),
        ("SRC-07", "FPDS prime obligations annual by vendor group",
         "Extracted CSV", "FY2017-2026", "extracted/fpds_annual_by_prime.csv (10)",
         "Two-yard compare; reads fpds_raw/ + fpds_raw_v2/."),
        ("SRC-08", "SAM.gov FSRS first-tier subawards (new construction)",
         "Extracted CSV", "FY2017-2026", "extracted/nc_records_long.csv (22,867)",
         "Canonical subaward source. Signed subaward records + sub_entity_uei for registry-led entity classification."),
        ("SRC-09", "Subaward annual by PIID (yard-grouped)",
         "Extracted CSV", "FY2017-2026", "extracted/nc_annual_by_piid.csv",
         "Per-FY subaward by PIID/yard. FFATA ~15% floor of true flow."),
        ("SRC-10", "Cleaned lifetime vendors + NAICS enrichment",
         "Extracted CSV", "2026", "nc_lifetime_vendors.csv (1,555) / entity_naics_lookup.csv (151)",
         "Vendor concentration + sector. ~35% NAICS lookup-fail."),
        ("SRC-11", "In-scope PIID set + discovered PIIDs",
         "JSON / CSV", "2026", "nc_scope_summary.json / _discovered_piids.csv (118)",
         "Scope arbiter. IVECO, DDG-1000, WPN/OPN, Thales ESSM removed."),
        ("SRC-12", "Cost-funnel decomposition (BC base)",
         "Extracted CSV", "FY27 PB", "extracted/cost_funnel_summary.csv (13)",
         "Total ship cost -> Basic Construction base. Yard-side band archived."),
        ("SRC-13", "HII Ingalls segment + GD Marine Systems financials",
         "SEC EDGAR (10-K/10-Q)", "FY2019-2025", "edgar_research/",
         "Segment-revenue triangulation of the hidden yard-side (archived)."),
        ("SRC-14", "Executive earnings-call commentary on outsourcing",
         "Extracted CSV", "FY2019-2026", "extracted/exec_quotes_outsourcing.csv (241)",
         "Direction-of-travel signal (HII/GD/LM/RTX). Not dollar sizing."),
        ("SRC-15", "FY 2026 Mandatory Funding Allocation Plan (OBBBA)",
         "DoD allocation plan (narrative)", "a/o 2026-02-18", "extracted/obbba_ddg_mandatory.csv (36)",
         "Sec. 20002(17): $5,400.0M FY2026, two DDG-51 (BC + GFE, current MYP, award Q2 FY2026). "
         "All Sec. 20002 lines transcribed; only line 17 enters the model."),
    ]
    _CITATIONS = [
        ("CITE-01", "MYP master totals - BIW 2305 (~$6.40B), Ingalls 2307 (~$8.18B)",
         "Trade press (USNI / Defense Daily)", "2023", "USNI/Defense Daily + FPDS",
         "Reconstructs the ~$14.58B redacted master dollars; POP as announced. Outside-yards 87% -> ~42%."),
        ("CITE-02", "Navy DDG-51 Arleigh Burke-class destroyer program",
         "CRS report (RL32109)", "latest", "crsreports.congress.gov",
         "Program scope, multi-year procurement, two-yard structure."),
        ("CITE-03", "GAO shipbuilding / Navy industrial-base assessments",
         "GAO reports", "latest", "gao.gov", "Cost/schedule + supplier-base anchors."),
        ("CITE-04", "Navy 30-Year Shipbuilding Plan",
         "Navy report", "latest", "budget_books/30_Year_Shipbuilding_Plan",
         "Build-rate / distributed-shipbuilding direction."),
        ("CITE-05", "Methodology + model spec (internal)",
         "Internal doc", "2026-05-28", "METHODOLOGY.md / WORKBOOK_SPEC.md",
         "Four-denominator framing, MYP guardrail, scope-exclusion list."),
        ("CITE-06", "PL 119-21 Title II (One Big Beautiful Bill Act), Sec. 20002",
         "Public law", "2025-07-04", "congress.gov / PL 119-21",
         "Mandatory (reconciliation) shipbuilding appropriation; obligation availability "
         "through 2029-09-30."),
        ("CITE-07", "OSD National Defense Budget Estimates FY2025 (Green Book), Tables 5-3/5-4",
         "OSD Comptroller", "FY2025 ed.", "fy25_Green_Book.pdf pp. 57-59",
         "Procurement TOA deflators through FY2029 (rebased to FY2026); FY2030-FY2031 "
         "extrapolated at 2.1%/yr (Table 5-3 steady-state purchases inflation)."),
        ("CITE-08", "PB2027 P-40 FYDP outyears (FY2028-FY2031), LI 2122",
         "SCN justification book (P-40)", "April 2026", "budget_books/SCN_Book_FY27",
         "Gross/Weapon System Cost request basis for the Outlook outyear projection; "
         "request, not appropriation - refresh at PB2028."),
        ("CITE-09", "Exhibit P-10 Advance Procurement Requirements Analysis, LI 2122",
         "SCN justification book (P-10)", "April 2026",
         "budget_books/SCN_Book_FY27 (Vol 1 p.243); FY25 split also PB2026 (p.235)",
         "AP/LLTM stream basis: FY26 $1,750.0M = Ship Construction EOQ $1,000.0M + "
         "congressional adds $450.0M shipyard infrastructure + $300.0M wage enhancements "
         "(excluded); FY25 $83.224M = EOQ $41.5M + NMT terminal GFE (excluded)."),
        ("CITE-10", "FY18-22 MYP master awards - BIW 18-2305 ($3,904.7M), Ingalls 18-2307 ($5,104.7M)",
         "DoD announcement (2018-09-27)", "2018-09-27",
         "defense.gov article 1647166 (Wayback 20180928083950); research_primary_sources/"
         "dod_announcement_pop/2018-09-27_dod-contracts_1647166.txt",
         "Announced $ and POP: BIW 61% Bath / 39% outside; Ingalls 91% Pascagoula / 9% "
         "outside. Basis for the FY2022-vintage BC coefficient (22.0%); predates the "
         "POP-corpus window, so not a corpus row."),
    ]

    SRC_ROW: dict[str, int] = {}
    tables: list[ExcelTable] = []
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Primary sources (native table)
    c.banner("§1 - Primary sources & data pulls", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    p_hdr = c.write(_REF_HEADERS, styles=S_HEADER_LEFT)
    for rec in _PRIMARY:
        SRC_ROW[rec[0]] = c.write(list(rec), styles=[S_DEFAULT] * len(_REF_HEADERS), outline_level=1)
    tables.append(ExcelTable(name="tbl_ddg_references_primary",
                             ref=f"B{p_hdr}:{col_letter(_NCOLS)}{c.at() - 1}", headers=_REF_HEADERS))
    c.blank(2)

    # §2 Policy & industry citations (native table)
    c.banner("§2 - Policy & industry citations", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c_hdr = c.write(_REF_HEADERS, styles=S_HEADER_LEFT)
    for rec in _CITATIONS:
        SRC_ROW[rec[0]] = c.write(list(rec), styles=[S_DEFAULT] * len(_REF_HEADERS), outline_level=1)
    tables.append(ExcelTable(name="tbl_ddg_references_citations",
                             ref=f"B{c_hdr}:{col_letter(_NCOLS)}{c.at() - 1}", headers=_REF_HEADERS))

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[14, 36, 24, 12, 26, 40],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    def source_ref_cell(src_id: str) -> str:
        return f"'{_TAB}'!C{SRC_ROW[src_id]}"

    return SheetEntry(_TAB, _GROUP, render), source_ref_cell


(REFERENCES, source_ref_cell) = _make_references()
