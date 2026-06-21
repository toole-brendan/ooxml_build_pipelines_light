"""sources_source_index - the "Source Index" tab (one module = one sheet).

The data / budget / methodology source inventory, as three native tables, plus a
short refresh-control block. Leaf module (static content + table names unchanged
from the former source_sheets).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "sources"
_TAB = "Sub Source Index"

_SI_HEADERS = ["Source", "Retrieved", "Location"]
_SI_DATA_SOURCES = [
    ["dod_announcement_pop.csv", "2026-05", "extracted/ (DoD/DoW announcements)"],
    ["dod_action_pop_by_worktype.csv", "2026-05", "extracted/"],
    ["entity_naics_lookup.csv", "2026-05", "extracted/ (USAspending + SAM.gov)"],
    ["nc_records_long.csv", "2026-05", "extracted/ (FFATA subawards)"],
    ["subaward_top_recipients.csv", "2026-05", "extracted/"],
    ["nc_geo_by_state.csv / nc_geo_by_country.csv", "2026-05", "extracted/"],
    ["nc_scope_summary.json", "2026-05", "extracted/"],
]
_SI_BUDGET_SOURCES = [
    ["SCN P-5c (Basic Construction)", "FY22-FY27 PB", "budget_books/SCN_Book_FY{22..27}"],
    ["SCN P-10 (Advance Procurement)", "FY22-FY27 PB", "budget_books/SCN_Book_FY{22..27}"],
    ["SCN per-FY actual TOA", "FY22-FY27", "extracted/scn_per_fy_actual_toa.csv"],
    ["FY 2026 Mandatory Funding Allocation Plan (OBBBA, Sec. 20002)", "2026-02-18",
     "docs/obbba_funding_allocation_narrative_20260218.txt"],
    ["SCN P-40 Resource Summary (FYDP outyears FY28-31)", "PB2027 (2026-04)",
     "extracted/scn_li_resource_summary.csv"],
]
_SI_DOC_SOURCES = [
    ["METHODOLOGY (POP / subaward / budget)", "2026-05", "docs/distributed_shipbuilding_implementation_plan.md"],
    ["Implementation plan", "2026-05-29", "docs/distributed_shipbuilding_implementation_plan.md"],
    ["BPMI reconciliation", "2026-05-29", "docs/distributed_shipbuilding_sub_phase3_BPMI_reconciliation.md"],
    ["deck_specs.md", "2026-05", "docs/distributed_shipbuilding_deck_specs.md"],
]


def _render_source_index() -> WorksheetSpec:
    n_cols = 3
    table_specs: list[tuple[str, int, int]] = []
    c = RowCursor(2)
    c.banner("Source Index", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()

    def _sub(sec, title, data, table_name):
        c.banner(f"§{sec} - {title}", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        header_row = c.at()
        blk, nxt = build_table(header_row, headers=_SI_HEADERS, data_rows=data,
                               header_style=S_HEADER_LEFT, col_styles=S_DEFAULT,
                               start_col=1, outline_level=1)
        c.feed(blk, nxt)
        table_specs.append((table_name, header_row, nxt - 1))
        c.blank(2)

    _sub(1, "Data sources (extracted)", _SI_DATA_SOURCES, "tbl_sub_source_index_data")
    _sub(2, "Budget exhibits (SCN P-5c / P-10 / TOA)", _SI_BUDGET_SOURCES, "tbl_sub_source_index_budget")
    _sub(3, "Methodology + reference docs", _SI_DOC_SOURCES, "tbl_sub_source_index_docs")

    # §4 Refresh control
    c.banner("§4 - Refresh control", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Area", "Last refreshed", "Source path"], styles=S_HEADER_LEFT)
    for rec in [
        ["POP corpus", "2026-05", "extracted/dod_announcement_pop.csv"],
        ["Subaward vendors", "2026-05", "extracted/entity_naics_lookup.csv"],
        ["Budget exhibits", "FY22-27 PB", "budget_books/"],
        ["OBBBA mandatory allocation plan", "2026-02-18", "docs/obbba_funding_allocation_narrative_20260218.txt"],
        ["FYDP outyears (P-40 gross)", "PB2027 (2026-04)",
         "extracted/scn_li_resource_summary.csv - refresh at PB2028; re-tie Va FY26 = 5,389.109"],
    ]:
        c.write(rec, styles=S_DEFAULT, outline_level=1)

    ws = worksheet(c.rows, cols=[38, 16, 40], tab_color=group_color(_GROUP), with_gutter=True)
    tables = [ExcelTable(name=nm, ref=f"B{hdr}:{col_letter(len(_SI_HEADERS))}{last}", headers=_SI_HEADERS)
              for nm, hdr, last in table_specs]
    return WorksheetSpec(ws, tables=tables)


SOURCE_INDEX = SheetEntry(_TAB, _GROUP, _render_source_index)
