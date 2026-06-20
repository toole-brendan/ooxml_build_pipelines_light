"""Awards

INTENT
    FY2025 unified FPDS services-MRO award master (one row per PIID x hull, with the
    FY25 apportionment helper columns) - the bottom-up TAM universe. Exposed as the
    native ``Awards`` table; Services, TAM Bridge, Verification, and Output SUMIFS
    against it. Values are extracted to CSV.

    Header labels are load-bearing (downstream structured references) - keep them
    stable. Code-like columns (PSC, NAICS, ZIP, PIID, CAGE) stay TEXT so SUMIFS
    criteria such as "1905" / a PSC code match; dollar / count / apportionment columns
    are numeric so SUMIFS can sum them.

LAYOUT
    row 2   : title
    row 4+  : §1 FY2025 services-MRO awards (native Awards table)
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
_TAB = "Awards"
_TABLE_NAME = "Awards"   # stable: downstream SUMIFS reference this name
_CSV = "awards.csv"

# (csv_key, display header, content width, is_numeric). csv_key == header (the CSV
# columns already carry the load-bearing display labels). Numeric: FY2025 Obligation,
# FY2025 Actions, # Hulls, Offers, Ceiling, Total Obligation, FY25 Apport M1-M4.
_COLUMNS = [
    ("Service",                "Service",                 9, False),
    ("PIID",                   "PIID",                   22, False),
    ("Recipient",              "Recipient",              30, False),
    ("Ultimate Parent",        "Ultimate Parent",        26, False),
    ("Corporate Parent",       "Corporate Parent",       20, False),
    ("FY2025 Obligation",      "FY2025 Obligation",      15, True),
    ("FY2025 Actions",         "FY2025 Actions",         12, True),
    ("Hull Program",           "Hull Program",           12, False),
    ("Vessel Class",           "Vessel Class",           20, False),
    ("Vessel Type",            "Vessel Type",            18, False),
    ("Hull Source",            "Hull Source",            14, False),
    ("Matched Ship Name",      "Matched Ship Name",      20, False),
    ("Hull Number",            "Hull Number",            11, False),
    ("All Hulls Detected",     "All Hulls Detected",     18, False),
    ("# Hulls",                "# Hulls",                 9, True),
    ("Proper Names Detected",  "Proper Names Detected",  20, False),
    ("Residual Row",           "Residual Row",           12, False),
    ("Parent IDV PIID",        "Parent IDV PIID",        20, False),
    ("Parent IDV Description", "Parent IDV Description",  34, False),
    ("PSC",                    "PSC",                     8, False),
    ("PSC Description",        "PSC Description",         30, False),
    ("Prod/Svc",               "Prod/Svc",                9, False),
    ("NAICS",                  "NAICS",                  10, False),
    ("GFE",                    "GFE",                     8, False),
    ("DoD Program",            "DoD Program",            16, False),
    ("Pricing Type",           "Pricing Type",           16, False),
    ("Competition",            "Competition",            16, False),
    ("Offers",                 "Offers",                  9, True),
    ("Ceiling",                "Ceiling",                14, True),
    ("Total Obligation",       "Total Obligation",       15, True),
    ("CAGE",                   "CAGE",                   10, False),
    ("POP State",              "POP State",               9, False),
    ("POP ZIP",                "POP ZIP",                10, False),
    ("Contracting Office",     "Contracting Office",     22, False),
    ("Description",            "Description",            50, False),
    ("Source Collections",     "Source Collections",     18, False),
    ("Start Date",             "Start Date",             11, False),
    ("End Date",               "End Date",               11, False),
    ("Sub Plan",               "Sub Plan",               10, False),
    ("Canonical Office",       "Canonical Office",       18, False),
    ("Is MRO",                 "Is MRO",                  8, False),
    ("FY25 Apport M1",         "FY25 Apport M1",         13, True),
    ("FY25 Apport M2",         "FY25 Apport M2",         13, True),
    ("FY25 Apport M3",         "FY25 Apport M3",         13, True),
    ("FY25 Apport M4",         "FY25 Apport M4",         13, True),
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


def _make_awards():
    with (EXTRACTED / _CSV).open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    headers = [h for _k, h, _w, _n in _COLUMNS]
    n_cols = len(_COLUMNS)

    c = RowCursor(2)
    c.banner(_TAB, n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()

    # §1 - the native, filterable awards table
    c.banner("§1 - FY2025 services-MRO awards",
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


AWARDS = _make_awards()
