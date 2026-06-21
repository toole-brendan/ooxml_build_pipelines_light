"""sources_source_index - the "Source Index" tab (DDG, sources group; one module = one sheet).

Dataset inventory + model lineage. Native table: tbl_ddg_source_index.

Promoted accessor (internal hygiene):
  dataset_row_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "sources"
_TAB = "DDG Source Index"
_NCOLS = 5


def _make_source_lineage():
    _SI_HEADERS = ["Dataset (extracted/)", "Rows", "Key fields", "Consumed by (tab)",
                   "Retrieval"]
    _LINEAGE = [
        ("scn_li_cost_categories.csv", "9", "LI, cost category, FY values",
         "SCN Budget", "FY22-27 PB (reconciled)"),
        ("scn_li_production_schedule.csv", "31", "ship, shipbuilder, FY, award/start/delivery",
         "Production Schedule", "FY27 PB"),
        ("scn_li_resource_summary.csv", "21", "row label, prior/FY/to-complete/total",
         "AP Bridge / TAM Build / FYDP Outyears / Outlook", "FY27 PB"),
        ("dod_announcement_pop.csv", "860", "piid, amount, prime, pop_*_pct, work_type, gate",
         "POP Corpus", "CY22-26"),
        ("dod_action_pop_by_worktype.csv", "36", "program, work_type, n, $, pop_*_pct_w",
         "POP Corpus", "CY22-26"),
        ("nc_records_long.csv", "22,867", "piid, fy, subAwardAmount, sub_name, description",
         "SAM Build / Entities", "FY17-26"),
        ("nc_annual_by_piid.csv", "16", "FY x PIID ($M + count)",
         "SAM Build", "FY17-26"),
        ("nc_annual_by_vendor.csv", "4,323", "fy, uei, vendor, amount_M",
         "Vendors", "FY17-26"),
        ("nc_lifetime_vendors.csv", "1,555", "rank, uei, vendor, amount_M_lifetime, piids",
         "Vendors / Entities / Locations", "2026"),
        ("entity_naics_lookup.csv", "151", "uei, vendor, primary_naics, naics_4digit, country",
         "Entities", "2026"),
        ("fpds_annual_by_prime.csv", "10", "FY x vendor-group ($M + piid_count)",
         "FPDS Primes", "FY17-26"),
        ("fpds_raw_v2/ (BIW, Rolls-Royce JSON)", "33,798", "obligatedAmount, piid, dates",
         "FPDS Primes / TAM Build", "2026"),
        ("nc_scope_summary.json + _discovered_piids.csv", "397 / 118", "piid, group, class, label",
         "Scope Exclusions", "2026"),
        ("cost_funnel_summary.csv", "13 / 106", "LI, FY, basic_construction_$M, band",
         "SCN Budget", "FY27 PB"),
        ("obbba_ddg_mandatory.csv", "36", "section, line, item, fy2026_$M, included, category",
         "OBBBA Mandatory / TAM Build", "Mandatory Funding Allocation Plan a/o 2026-02-18"),
        ("sam_subaward_annual_by_prime.csv", "16", "FY x PIID ($M + count)",
         "SAM Build", "FY17-26"),
        ("exec_quotes_outsourcing.csv", "241", "company, fy, speaker, matched_phrase",
         "References", "FY19-26"),
        ("edgar_research/ (HII, GD filings)", "n/a", "segment revenue, backlog",
         "References", "FY19-25"),
    ]

    DS_ROW: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Extracted datasets (native table)
    c.banner("§1 - Extracted datasets and their consuming tabs", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    si_hdr = c.write(_SI_HEADERS, styles=S_HEADER_LEFT)
    for rec in _LINEAGE:
        DS_ROW[rec[0]] = c.write(list(rec), styles=[S_DEFAULT] * len(_SI_HEADERS), outline_level=1)
    si_last = c.at() - 1
    table = ExcelTable(name="tbl_ddg_source_index",
                       ref=f"B{si_hdr}:{col_letter(_NCOLS)}{si_last}", headers=_SI_HEADERS)
    c.blank(2)

    # §2 Consumers by model area
    c.banner("§2 - Consumers by model area", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    roll, nxt = build_table(
        c.at(), headers=["Model area", "Primary datasets", "", "", ""],
        data_rows=[
            ["Budget", "scn_li_cost_categories, scn_li_resource_summary, cost_funnel_summary, obbba_ddg_mandatory", "", "", ""],
            ["POP", "dod_announcement_pop, dod_action_pop_by_worktype", "", "", ""],
            ["Suppliers", "entity_naics_lookup, nc_lifetime_vendors, fpds_annual_by_prime, fpds_raw_v2", "", "", ""],
            ["SAM", "nc_records_long, nc_annual_by_piid, sam_subaward_annual_by_prime", "", "", ""],
            ["Validation", "nc_scope_summary, _discovered_piids", "", "", ""],
            ["References", "exec_quotes_outsourcing, edgar_research", "", "", ""],
        ],
        header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(roll, nxt)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[36, 10, 32, 26, 14],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=[table])

    def dataset_row_cell(dataset: str) -> str:
        return f"'{_TAB}'!B{DS_ROW[dataset]}"

    return SheetEntry(_TAB, _GROUP, render), dataset_row_cell


(SOURCE_INDEX, dataset_row_cell) = _make_source_lineage()
