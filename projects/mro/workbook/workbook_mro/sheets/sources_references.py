"""References

INTENT
    Source / citation registry. Two native tables: tbl_mro_references_primary (primary
    sources & data pulls) and tbl_mro_references_citations (policy & industry
    citations). A source table - the context-note exception - so it keeps a short
    context note per row.

    Accessor: source_ref_cell (internal hygiene).

LAYOUT
    row 2 : title
    §1 primary sources & data pulls (SRC-01..10) · §2 policy & industry citations
    (CITE-01..05)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor

_GROUP = "sources"
_TAB = "References"
_NCOLS = 6


def _make_references():
    _REF_HEADERS = ["Source ID", "Document / dataset", "Type", "Date",
                    "Location / reference", "Context note"]
    _PRIMARY = [
        ("SRC-01", "FPDS unified services-MRO award master",
         "Extracted CSV", "FY2025", "extracted/awards.csv",
         "65 J/K/N/M/H/L MRO PSCs; canonical-office + vessel-type tagged with an Is MRO "
         "flag. The bottom-up TAM universe (Services / Verification / TAM Bridge SUMIFS)."),
        ("SRC-02", "FPDS J998/J999 depot ship-repair task orders",
         "Extracted CSV", "FY2025", "extracted/j998_j999.csv",
         "Classified by RMC, availability type, contractor tier and vessel category. "
         "Drives the Depot Ship Repair cross-tabs."),
        ("SRC-03", "PSC 1905 classified PIIDs (embedded ship MRO)",
         "Extracted CSV", "FY2025", "extracted/psc_1905_classified.csv",
         "Ship MRO booked under the shipbuilding PSC 1905; bucketed strong / TAS-confirmed "
         "/ probable. Feeds the reconciled-TAM embedded slice + captive-OH deduction."),
        ("SRC-04", "OP-5 Navy O&M budget justification (Table IV)",
         "Budget exhibit", "FY24-26 PB", "OMN_Book / OP-5 Table IV",
         "1B4B ship-maintenance availability categories with the private vs public-NSY "
         "split. The Navy top-down anchor (OP-5 Navy Top-Down sheet)."),
        ("SRC-05", "MSC operations & maintenance (M&R)",
         "Budget exhibit", "FY25-26 PB", "OMN_Book line 4467",
         "MSC vessel M&R; FY25 executes out of 1B1B and transfers to 1B4B in FY26."),
        ("SRC-06", "SCN shipbuilding budget - CVN RCOH (LI 2086)",
         "Budget exhibit", "FY25 PB", "SCN_Book LI 2086",
         "CVN refueling complex overhaul; multi-year incremental TOA. The embedded-MRO "
         "bridge component."),
        ("SRC-07", "OPN BA1 budget - ship maintenance (LI 1000)",
         "Budget exhibit", "FY25 enacted", "OPN_BA1_Book line 21287 (P-5) / 21193 (P-40)",
         "Private contracted CONUS surface + submarine maintenance at CPF / FFC; FY25 "
         "$2,392.190M. Distinct 1810N appropriation (PL 116-93); parallel to OMN 1B4B."),
        ("SRC-08", "WPN procurement P-40 exhibits",
         "Budget exhibit", "FY25 PB", "WPN_Book P-40",
         "Missile / torpedo / weapons procurement. Shipboard combat-systems installation "
         "is not isolable from procurement; only a plan-estimate plug enters the model."),
        ("SRC-09", "USCG In-Service Vessel Sustainment (ISVS)",
         "Budget exhibit", "FY25 PB", "USCG PC&I / O&S budget",
         "Cutter sustainment floor ($120M FY25). No OP-5 Table IV equivalent; USCG cutter "
         "MRO mostly embedded in O&S Surface/Air/Shore Ops."),
        ("SRC-10", "HII Mission Technologies segment financials",
         "SEC EDGAR (10-K/10-Q)", "FY2024-2025", "edgar_research/",
         "Segment revenue / operating income / service-mix triangulation for the captive "
         "SUPSHIP yard side (HII_MT_* anchors on Reconciliation)."),
    ]
    _CITATIONS = [
        ("CITE-01", "Consolidated Appropriations Act, 2020 (PL 116-93)",
         "Statute", "2020", "congress.gov",
         "Established the 1810N OPN appropriation for private contracted ship maintenance "
         "at CPF / FFC - the basis for the no-double-count vs OMN 1B4B."),
        ("CITE-02", "NAVSEA regional maintenance center (RMC) structure",
         "Navy org reference", "latest", "navsea.navy.mil",
         "SWRMC / MARMC / SERMC / NW RMC / Pearl Harbor RMC / SRF-JRMC / FDRMC canonical "
         "buyers; the contracting-office alias rollup."),
        ("CITE-03", "GAO Navy ship-maintenance & depot reports",
         "GAO reports", "latest", "gao.gov",
         "Maintenance backlog, private-vs-public depot capacity, schedule context."),
        ("CITE-04", "FPDS-NG Product/Service Code (PSC) manual",
         "Reference", "latest", "fpds.gov / PSC selection tool",
         "Definitions for the 65 services-MRO PSCs (J/K/N/M/H/L) and the PSC 1905 "
         "shipbuilding code."),
        ("CITE-05", "Methodology + workbook spec (internal)",
         "Internal doc", "2026", "METHODOLOGY.md / WORKBOOK_SPEC.md",
         "Two-universe TAM/SAM framing, scope-exclusion list, the no-double-count "
         "appropriation discipline."),
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
    tables.append(ExcelTable(name="tbl_mro_references_primary",
                             ref=f"B{p_hdr}:{col_letter(_NCOLS)}{c.at() - 1}", headers=_REF_HEADERS))
    c.blank(2)

    # §2 Policy & industry citations (native table)
    c.banner("§2 - Policy & industry citations", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c_hdr = c.write(_REF_HEADERS, styles=S_HEADER_LEFT)
    for rec in _CITATIONS:
        SRC_ROW[rec[0]] = c.write(list(rec), styles=[S_DEFAULT] * len(_REF_HEADERS), outline_level=1)
    tables.append(ExcelTable(name="tbl_mro_references_citations",
                             ref=f"B{c_hdr}:{col_letter(_NCOLS)}{c.at() - 1}", headers=_REF_HEADERS))

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[12, 38, 26, 14, 30, 44],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    def source_ref_cell(src_id: str) -> str:
        return f"'{_TAB}'!C{SRC_ROW[src_id]}"

    return SheetEntry(_TAB, _GROUP, render), source_ref_cell


(REFERENCES, source_ref_cell) = _make_references()
