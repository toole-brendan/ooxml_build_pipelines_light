"""PSC 1905 Classified

INTENT
    One row per PSC 1905 PIID (embedded ship MRO booked under the shipbuilding PSC),
    exposed as the native ``PSC1905Classified`` table. Reconciliation and Output
    SUMIFS against it (filtering on corporate_parent / vessel_supergroup / bucket) so
    the per-vessel and per-parent embedded-MRO rollups stay live at the PIID level.

    Header labels are load-bearing (downstream structured references) - keep them
    stable. Values are raw FY2025 / total obligation DOLLARS (not $M); downstream
    formulas scale to $M. Downstream SUMIFS bucket filters:
        Central MRO = bucket IN {'MRO (strong)', 'MRO (TAS-confirmed)', 'MRO (probable)'}
        Upper MRO   = Central + 'MRO (POP-only)'

    Source CSV: mro/data_and_pipeline/psc1905/build_script_slim/output/
    psc_1905_classified.csv (regenerate via
    ``python -m build_script_slim.psc_1905_classifier`` in the mro tree).

LAYOUT
    row 2   : title
    row 4+  : §1 PSC 1905 PIIDs (native PSC1905Classified table)
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
_TAB = "PSC 1905 Classified"
_TABLE_NAME = "PSC1905Classified"   # stable: downstream SUMIFS reference this name

# (csv_key, display header, content width, is_numeric). Header strings are
# load-bearing (downstream structured references) - keep them stable.
_COLUMNS = [
    ("piid",                   "PIID",                   22, False),
    ("service",                "Service",                 8, False),
    ("recipient_name",         "Recipient",              30, False),
    ("ultimate_parent_name",   "Ultimate Parent",        26, False),
    ("corporate_parent",       "Corporate Parent",       18, False),
    ("vessel_supergroup",      "Vessel Supergroup",      18, False),
    ("vessel_class",           "Vessel Class",           20, False),
    ("hull_program",           "Hull Program",           12, False),
    ("fy2025_obligation",      "FY2025 Obligation",      16, True),
    ("total_obligation",       "Total Obligation",       16, True),
    ("start_date",             "Start Date",             11, False),
    ("end_date",               "End Date",               11, False),
    ("bucket",                 "Bucket",                 22, False),
    ("evidence",               "Evidence",               40, False),
    ("tas_federal_accounts",   "TAS Federal Accounts",   18, False),
    ("description",            "Description",            50, False),
    ("parent_idv_description", "Parent IDV Description", 34, False),
]


def _make_psc_1905_classified():
    def _num(x):
        """Parse a numeric cell; 0/blank -> None so it renders as '-'."""
        try:
            v = float(str(x).replace(",", "").strip())
        except (TypeError, ValueError):
            return None
        return v or None

    def _load():
        with (EXTRACTED / "psc_1905_classified.csv").open(
                encoding="utf-8-sig", newline="") as fh:
            return list(csv.DictReader(fh))

    rows = _load()
    headers = [h for _k, h, _w, _n in _COLUMNS]
    n_cols = len(_COLUMNS)

    c = RowCursor(2)
    c.banner(_TAB, n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Classified PIID table (native, filterable)
    c.banner("§1 - PSC 1905 PIIDs",
             n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr_styles = [S_HEADER_CENTER if is_num else S_HEADER_LEFT
                  for _k, _h, _w, is_num in _COLUMNS]
    hdr = c.write(headers, styles=hdr_styles)
    first_data = c.at()
    for rec in rows:
        vals, styles = [], []
        for key, _h, _w, is_num in _COLUMNS:
            if is_num:
                vals.append(_num(rec.get(key)))
                styles.append(S_NUM_INPUT)
            else:
                vals.append((rec.get(key) or "").strip())
                styles.append(S_DEFAULT)
        c.write(vals, styles=styles, outline_level=1)
    last_data = c.at() - 1

    tables = [ExcelTable(
        name=_TABLE_NAME,
        ref=f"B{hdr}:{col_letter(n_cols)}{last_data}",
        headers=headers,
    )]

    def render() -> WorksheetSpec:
        cols = [w for _k, _h, w, _n in _COLUMNS]
        ws = worksheet(c.rows, cols=cols, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=tables)

    return SheetEntry(_TAB, _GROUP, render)


PSC_1905_CLASSIFIED = _make_psc_1905_classified()
