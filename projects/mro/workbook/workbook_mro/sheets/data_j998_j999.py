"""J998 J999 Data

INTENT
    FY2025 classified J998/J999 depot ship-repair task orders (one row per task order).
    Exposed as the native ``J998J999Data`` table; Depot Ship Repair and Output
    SUMIFS / COUNTIFS against it. Values are extracted to CSV.

    Header labels are load-bearing (downstream structured references) - keep them
    stable. PSC / NAICS stay TEXT so SUMIFS criteria match; dollar / count columns
    are numeric.

LAYOUT
    row 2   : title
    row 4+  : §1 FY2025 J998/J999 task orders (native J998J999Data table)
"""
from __future__ import annotations

import csv

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.lib import EXTRACTED
from workbook_mro.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "J998 J999 Data"
_TABLE_NAME = "J998J999Data"   # stable: downstream SUMIFS / COUNTIFS reference this name
_CSV = "j998_j999.csv"

# (csv_key, display header, content width, is_numeric). csv_key == header. Numeric:
# FY2025 Obligation, Total Obligation, FY2025 Actions, Mod Count.
_COLUMNS = [
    ("Service",            "Service",             9, False),
    ("PIID",               "PIID",               22, False),
    ("PSC",                "PSC",                 8, False),
    ("PSC Description",    "PSC Description",     30, False),
    ("Recipient",          "Recipient",          30, False),
    ("Ultimate Parent",    "Ultimate Parent",    26, False),
    ("Corporate Parent",   "Corporate Parent",   20, False),
    ("FY2025 Obligation",  "FY2025 Obligation",  15, True),
    ("Total Obligation",   "Total Obligation",   15, True),
    ("FY2025 Actions",     "FY2025 Actions",     12, True),
    ("Mod Count",          "Mod Count",          10, True),
    ("Hull Program",       "Hull Program",       12, False),
    ("Vessel Class",       "Vessel Class",       20, False),
    ("Vessel Category",    "Vessel Category",    18, False),
    ("Vessel Type",        "Vessel Type",        18, False),
    ("Matched Ship Name",  "Matched Ship Name",  20, False),
    ("Hull Number",        "Hull Number",        11, False),
    ("Availability Type",  "Availability Type",  18, False),
    ("Availability Group", "Availability Group", 18, False),
    ("RMC",                "RMC",                12, False),
    ("Contractor Tier",    "Contractor Tier",    16, False),
    ("IDV Scope Type",     "IDV Scope Type",     16, False),
    ("IDV Scope Group",    "IDV Scope Group",    16, False),
    ("NAICS",              "NAICS",              10, False),
    ("Contracting Office", "Contracting Office", 22, False),
    ("POP State",          "POP State",           9, False),
    ("Start Date",         "Start Date",         11, False),
    ("End Date",           "End Date",           11, False),
]


def _num(x):
    """Parse a numeric cell; blank/garbage -> None (renders '-', sums as 0)."""
    s = str(x).replace(",", "").strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _make_j998_j999():
    with (EXTRACTED / _CSV).open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    headers = [h for _k, h, _w, _n in _COLUMNS]
    n_cols = len(_COLUMNS)

    c = RowCursor(2)
    c.banner(_TAB, n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()

    # §1 - the native, filterable task-order table
    c.banner("§1 - FY2025 J998/J999 task orders",
             n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr_styles = [S_HEADER_CENTER if is_num else S_HEADER_LEFT
                  for _k, _h, _w, is_num in _COLUMNS]
    hdr = c.write(headers, styles=hdr_styles)
    for rec in rows:
        vals, styles = [], []
        for key, _h, _w, is_num in _COLUMNS:
            if is_num:
                vals.append(_num(rec.get(key)))
                styles.append(S_NUM_INPUT)
            else:
                vals.append((rec.get(key) or "").strip() or None)
                styles.append(S_DEFAULT)
        c.write(vals, styles=styles, outline_level=1)
    last = c.at() - 1

    tables = [ExcelTable(name=_TABLE_NAME,
                         ref=f"B{hdr}:{col_letter(n_cols)}{last}", headers=headers)]

    def render() -> WorksheetSpec:
        cols = [w for _k, _h, w, _n in _COLUMNS]
        ws = worksheet(c.rows, cols=cols, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    return SheetEntry(_TAB, _GROUP, render)


J998_J999 = _make_j998_j999()
