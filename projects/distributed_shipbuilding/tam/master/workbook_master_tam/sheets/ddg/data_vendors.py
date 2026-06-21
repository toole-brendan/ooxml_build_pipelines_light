"""data_vendors - the "Vendors" tab (DDG, data group; one module = one sheet).

Top subaward recipients by lifetime $. The former Vendors section of the composite
Suppliers tab, now its own tab. Reader / evidence support; it does not drive the
core model. Native table: tbl_ddg_top_vendors.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, build_table, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import EXTRACTED
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG Vendors"
_NCOLS = 6


def _make_vendors():
    def _f(x) -> float:
        try:
            return float(str(x).replace(",", "").strip())
        except (TypeError, ValueError):
            return 0.0

    _TV_TOP_N = 60
    _TV_HEADERS = ["#", "Vendor", "Foreign", "$M lifetime", "Records", "PIIDs"]

    def _tv_load():
        out = []
        with (EXTRACTED / "nc_lifetime_vendors.csv").open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                out.append({"rank": (r.get("rank") or "").strip(), "vendor": (r.get("vendor") or "").strip(),
                            "foreign": (r.get("foreign") or "").strip(), "amt": _f(r.get("amount_M_lifetime")),
                            "records": (r.get("records") or "").strip(), "piids": (r.get("piid_count") or "").strip()})
        out.sort(key=lambda r: r["amt"], reverse=True)
        return out

    _TV = _tv_load()
    _shown = min(len(_TV), _TV_TOP_N)
    tables: list[ExcelTable] = []
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Top vendors (native table)
    c.banner(f"§1 - Top {_TV_TOP_N} vendors by lifetime $ (FFATA-visible)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    tv_hdr = c.at()
    tv_rows = [[str(i), r["vendor"], r["foreign"], r["amt"], r["records"], r["piids"]]
               for i, r in enumerate(_TV[:_TV_TOP_N], start=1)]
    vblk, vnxt = build_table(tv_hdr, headers=_TV_HEADERS, data_rows=tv_rows,
                             header_style=S_HEADER_LEFT,
                             col_styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM_INPUT, S_DEFAULT, S_DEFAULT],
                             start_col=1, outline_level=1)
    c.feed(vblk, vnxt)
    tables.append(ExcelTable(name="tbl_ddg_top_vendors",
                             ref=f"B{tv_hdr}:{col_letter(len(_TV_HEADERS))}{tv_hdr + _shown}",
                             headers=_TV_HEADERS))
    c.blank(2)

    # §2 Concentration (formula-driven over the table $ column, col E)
    c.banner("§2 - Concentration (of the shown top vendors)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Group", "$M lifetime", "% of shown total", ""],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    tv_first = tv_hdr + 1
    r0 = c.at()
    shown_row = r0 + 2
    for idx, n in enumerate((10, 25, _shown)):
        dollar = f"=SUM(E{tv_first}:E{tv_first + n - 1})"
        c.write([f"Top {n}", dollar, f"=C{r0 + idx}/C{shown_row}", ""],
                styles=[S_DEFAULT, S_NUM, S_PCT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[6, 40, 10, 14, 11, 11],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    return SheetEntry(_TAB, _GROUP, render)


VENDORS = _make_vendors()
