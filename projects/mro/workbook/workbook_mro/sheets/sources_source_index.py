"""Source Index

INTENT
    Dataset inventory + model lineage for the MRO workbook. Native table
    tbl_mro_source_index. Row counts for the three extracted CSVs are computed live at
    build time so the index never drifts from the data tabs.

    Accessor: dataset_row_cell (internal hygiene).

LAYOUT
    row 2 : title
    §1 extracted datasets (native table) · §2 consumers by model area
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.lib import EXTRACTED
from workbook_mro.sheets._layout import RowCursor

_GROUP = "sources"
_TAB = "Source Index"
_NCOLS = 5


def _count_rows(csv_name: str) -> str:
    """Live data-row count of an extracted CSV (header excluded), comma-formatted."""
    with (EXTRACTED / csv_name).open(encoding="utf-8-sig", newline="") as fh:
        n = sum(1 for _ in csv.reader(fh)) - 1
    return f"{max(n, 0):,}"


def _make_source_lineage():
    _SI_HEADERS = ["Dataset (extracted/)", "Rows", "Key fields", "Consumed by (tab)",
                   "Vintage"]
    _LINEAGE = [
        ("awards.csv", _count_rows("awards.csv"),
         "Service, PSC, FY2025 obligation, canonical office, vessel type, Is MRO",
         "Services / TAM Bridge / Verification / Output", "FY2025"),
        ("j998_j999.csv", _count_rows("j998_j999.csv"),
         "PSC J998/J999, RMC, availability type, contractor tier, vessel category",
         "Depot Ship Repair / Output", "FY2025"),
        ("psc_1905_classified.csv", _count_rows("psc_1905_classified.csv"),
         "PIID, ultimate parent, vessel supergroup, MRO bucket, TAS accounts",
         "Reconciliation / TAM Atoms / Verification / Output", "FY2025"),
        ("v433/*.json (extracted v4.33 grid)", "n/a",
         "Per-sheet cell/formula grid - the tie-out oracle",
         "qa/tie_out.py (provenance only)", "v4.33"),
        ("v433/_defined_names.json", "88",
         "Named-range -> A1 target map (the bridge anchors)",
         "qa/tie_out.py name gate", "v4.33"),
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
    table = ExcelTable(name="tbl_mro_source_index",
                       ref=f"B{si_hdr}:{col_letter(_NCOLS)}{si_last}", headers=_SI_HEADERS)
    c.blank(2)

    # §2 Consumers by model area
    c.banner("§2 - Consumers by model area", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    roll, nxt = build_table(
        c.at(), headers=["Model area", "Primary datasets", "", "", ""],
        data_rows=[
            ["Services-MRO TAM", "awards.csv (65 MRO PSCs)", "", "", ""],
            ["Depot ship repair", "j998_j999.csv", "", "", ""],
            ["Embedded / reconciliation", "psc_1905_classified.csv", "", "", ""],
            ["Top-down anchors", "v433 OP-5 / MSC / SCN / OPN / USCG budget lines", "", "", ""],
            ["Tie-out", "v433/*.json, v433/_defined_names.json", "", "", ""],
        ],
        header_style=S_HEADER_LEFT, col_styles=S_DEFAULT, start_col=1, outline_level=1)
    c.feed(roll, nxt)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[34, 8, 40, 34, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=[table])

    def dataset_row_cell(dataset: str) -> str:
        return f"'{_TAB}'!B{DS_ROW[dataset]}"

    return SheetEntry(_TAB, _GROUP, render), dataset_row_cell


(SOURCE_INDEX, dataset_row_cell) = _make_source_lineage()
