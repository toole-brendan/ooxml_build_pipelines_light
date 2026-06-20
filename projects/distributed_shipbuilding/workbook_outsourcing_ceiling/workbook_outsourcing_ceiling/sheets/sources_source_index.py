"""sources_source_index - the "Sources" tab (sources group).

Provenance + methodology, in one place:
  §1 Anchors        - the verified citations behind each parameter (native
                      table from wb_anchors.csv). Each Source cell carries its
                      raw URL as a hover note, so the URL stays one hover away
                      without a wide, clipping URL column.
  §2 Sourced vs assumed - which parameters are verified, derived, or analyst
                      assumptions (the honest ledger).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry, ExcelTable
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_outsourcing_ceiling.lib import load_extracted_csv
from workbook_outsourcing_ceiling.sheets._layout import RowCursor

_GROUP = "sources"
_TAB = "Sources"

_T_HEADERS = ["Parameter", "Value", "Basis", "Source", "ID"]
_NCOLS = 5   # B..F  (raw URL lives in a hover note on the Source cell, not a column)

_LEDGER = [
    ["h - outsourceable labor-hour share", "Verified", "Rucker / Defense News 2022 (A1)"],
    ["L - shipyard labor share of BC", "Verified + judgment",
     "40% of total cost (CRS/CBO A2/A3), rebased to BC (see Assumptions)"],
    ["core = L x (1 - h)", "Derived", "identity"],
    ["ceiling = 1 - core", "Derived", "identity"],
    ["p - pass-through material", "Assumption", "scenario input; sizes supplier-package value"],
    ["DDG-51 h / L", "Assumption", "non-nuclear contrast, not Rucker"],
    ["Current off-team POP %", "Sourced + derived", "announced POP A5/A6; DDG-51 13% blended (A7)"],
]


def _make():
    headers, rows = load_extracted_csv("wb_anchors")
    ix = {h: i for i, h in enumerate(headers)}

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 anchors (native table)
    c.banner("§1 - Anchors (verified citations)", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_T_HEADERS, styles=[S_HEADER_LEFT] * _NCOLS)
    last = hdr
    url_notes = []
    for r in rows:
        last = c.write([r[ix["parameter"]], r[ix["value"]], r[ix["basis"]],
                        r[ix["source_title"]], r[ix["anchor_id"]]],
                       styles=[S_DEFAULT] * _NCOLS, outline_level=1)
        url = (r[ix["source_url"]] or "").strip()
        if url:
            # Raw URL as a compact hover note on the Source cell (col E); auto-fit
            # dims so the box stays small (just the link), not a wide URL column.
            url_notes.append(ExcelNote(f"E{last}", url))
    table = ExcelTable(name="Anchors",
                       ref=f"B{hdr}:{col_letter(_NCOLS)}{last}",
                       headers=_T_HEADERS)
    c.blank(2)

    # §2 sourced vs assumed ledger
    c.banner("§2 - Sourced vs assumed", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Parameter", "Status", "Note"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_LEFT])
    for param, status, note in _LEDGER:
        c.write([param, status, note], styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT],
                outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[44, 10, 34, 80, 6],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=[table], notes=url_notes)

    return SheetEntry(_TAB, _GROUP, render)


SOURCES = _make()
