"""data_fpds_primes - the "FPDS Primes" tab (DDG, data group; one module = one sheet).

FPDS prime obligations by vendor group and FY. The former FPDS section of the
composite Suppliers tab, now its own tab. De-capped prime pulls support obligation
sizing and MYP reconstruction; they are NOT a direct SAM bucket-allocation source.
Native table: tbl_ddg_fpds_primes.
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._bind import EXTRACTED
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG FPDS Primes"


def _make_fpds_primes():
    def _f(x) -> float:
        try:
            return float(str(x).replace(",", "").strip())
        except (TypeError, ValueError):
            return 0.0

    _FPDS_SUFFIX = "_obligated_$M"
    _FPDS_ORDER = ["GD-BIW", "HII-Ingalls", "Rolls-Royce", "GE-Propulsion",
                   "LM-Aegis", "Raytheon", "BAE-Guns/VLS", "NG", "GD-MissionSys",
                   "DRS", "L3Harris"]

    def _fpds_load():
        with (EXTRACTED / "fpds_annual_by_prime.csv").open(encoding="utf-8-sig", newline="") as fh:
            rdr = csv.DictReader(fh)
            cols = rdr.fieldnames or []
            raw = list(rdr)
        groups = [c[:-len(_FPDS_SUFFIX)] for c in cols if c.endswith(_FPDS_SUFFIX)]
        ordered = [g for g in _FPDS_ORDER if g in groups] + [g for g in groups if g not in _FPDS_ORDER]
        return ordered, raw

    _FPDS_GROUPS, _FPDS_RAW = _fpds_load()
    _FPDS_HEADERS = ["FY"] + _FPDS_GROUPS
    _NCOLS = max(6, len(_FPDS_HEADERS))

    tables: list[ExcelTable] = []
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Annual obligations (native table + total)
    c.banner("§1 - Annual obligations ($M by FY x vendor group; de-capped)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    fpds_hdr = c.write(_FPDS_HEADERS, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FPDS_GROUPS))
    first_data = c.at()
    for rec in _FPDS_RAW:
        fy = (rec.get("FY") or "").strip()
        vals = [(_f(rec.get(g + _FPDS_SUFFIX)) or None) for g in _FPDS_GROUPS]
        c.write([fy] + vals, styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FPDS_GROUPS), outline_level=1)
    last_data = c.at() - 1
    tables.append(ExcelTable(name="tbl_ddg_fpds_primes",
                             ref=f"B{fpds_hdr}:{col_letter(len(_FPDS_HEADERS))}{last_data}",
                             headers=_FPDS_HEADERS))
    tot = ["Total"] + [f"=SUM({col_letter(2 + i)}{first_data}:{col_letter(2 + i)}{last_data})"
                       for i in range(len(_FPDS_GROUPS))]
    c.total(tot, styles=[S_BOLD] + [S_NUM] * len(_FPDS_GROUPS), n_cols=len(_FPDS_HEADERS))
    c.blank(2)

    # §2 Use in model
    c.banner("§2 - Use in model", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["De-capped prime pulls size obligations and MYP reconstruction; not a direct SAM bucket source."],
            styles=[S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        cols = [8] + [12] * len(_FPDS_GROUPS)
        ws = worksheet(c.rows, cols=cols, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    return SheetEntry(_TAB, _GROUP, render)


FPDS_PRIMES = _make_fpds_primes()
