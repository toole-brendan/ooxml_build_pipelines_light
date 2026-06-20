"""data_lane_detail - the "Lane Detail" leaf sheet.

The workbook's lane-grain LEAF data: one row per (program, PIID, work type)
supplier lane from wb_piid_worktype.csv, carrying the per-FY $M (d_ columns)
and per-FY record counts (n_ columns) side by side as the native table
LaneDetail, plus lane identity (program / family / PIID / builder / work
type) and the lane's first/last award dates (real date cells, blue).
Everything aggregated by work type, PIID, or builder elsewhere in the
workbook (By Work Type grids, By PIID $ grid, By Vessel builder detail, the
Supplier Lanes count grid) derives live from this table; only the FY cells
and dates here are hardcoded (blue inputs), with black live row Totals per
block.

Built at import via _make_lane_detail() into a standalone single-table sheet
(its own title banner, §1 section table, column widths and autofilter).

Promoted accessors (module-level; imported by the sheets that derive from this leaf):
  ld_cols()         - absolute column ranges (program / piid / builder /
                      work type + per-FY $ and count column ranges) for
                      cross-sheet SUMIFS.
  ld_date_refs(idx) - the (First Award, Last Award) cell refs of the idx-th
                      lane row (CSV order) - Supplier Lanes links these.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DATE_INPUT, S_DEFAULT, S_INT,
    S_INT_INPUT, S_NUM, S_NUM_INPUT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, FY_KEYS, N_VALS, VAL_LABELS, date_serial, load, row_sum,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_FAMILY, W_PIID, W_BUILDER, W_WORKTYPE, W_DATE, W_FY, W_FY_N,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_LANE_DETAIL

_GROUP = "data"
_TAB = TAB_LANE_DETAIL
_BANNER = "§1 - Lane detail"

_DATE_HDRS = {"First Award", "Last Award"}

_META = ["Program", "Family", "PIID", "Builder", "Work Type",
         "First Award", "Last Award"]
_HEADERS = (_META + [f"$ {l}" for l in VAL_LABELS]
            + [f"N {l}" for l in VAL_LABELS])
_CENTER_HDRS = ({f"$ {l}" for l in VAL_LABELS}         # center both FY grids
                | {f"N {l}" for l in VAL_LABELS})
_NCOLS = len(_HEADERS)
_COLS = ([W_PROGRAM, W_FAMILY, W_PIID, W_BUILDER, W_WORKTYPE, W_DATE, W_DATE]
         + [W_FY] * N_VALS + [W_FY_N] * N_VALS)
_PROG_COL = col_letter(1)                                    # B
_PIID_COL = col_letter(3)                                    # D
_BLDR_COL = col_letter(4)                                    # E
_WT_COL = col_letter(5)                                      # F
_FA_COL = col_letter(6)                                      # G
_LA_COL = col_letter(7)                                      # H
_DCOL = [col_letter(1 + len(_META) + j) for j in range(N_VALS)]    # I..X
_NCOL = [col_letter(1 + len(_META) + N_VALS + j)
         for j in range(N_VALS)]                                   # Y..AN
_FAMILY = {"virginia": "Submarines", "columbia": "Submarines",
           "ddg": "DDG-51"}


def _make_lane_detail():
    """Build the Lane Detail leaf sheet: a row-2 title banner + the §1 section
    table. Returns (SheetEntry, ld_cols, ld_date_refs)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_piid_worktype")
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()

    hdr = c.write(_HEADERS,
                  styles=header_styles(_HEADERS, _DATE_HDRS, center_headers=_CENTER_HDRS))
    f, l = hdr + 1, hdr + len(rows)
    for row in rows:
        prog = row[i["program"]]
        c.write([prog, _FAMILY[prog], row[i["piid"]], row[i["builder"]],
                 BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                 date_serial(row[i["first_award"]]),
                 date_serial(row[i["last_award"]])]
                + [row[i[f"d_{k}"]] if row[i[f"d_{k}"]] is not None else 0
                   for k in FY_KEYS]
                + [row_sum(_DCOL[0], _DCOL[-2])]
                + [row[i[f"n_{k}"]] if row[i[f"n_{k}"]] is not None else 0
                   for k in FY_KEYS]
                + [row_sum(_NCOL[0], _NCOL[-2])],
                styles=[S_DEFAULT] * 5 + [S_DATE_INPUT] * 2
                       + [S_NUM_INPUT] * (N_VALS - 1) + [S_NUM]
                       + [S_INT_INPUT] * (N_VALS - 1) + [S_INT],
                outline_level=1)
    table_ref = f"B{hdr}:{_NCOL[-1]}{l}"

    def ld_cols() -> dict:
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${l}"
        return {"prog": rng(_PROG_COL), "piid": rng(_PIID_COL),
                "builder": rng(_BLDR_COL), "wt": rng(_WT_COL),
                "dfy": [rng(col) for col in _DCOL[:-1]],
                "nfy": [rng(col) for col in _NCOL[:-1]],
                "dtot": rng(_DCOL[-1]), "ntot": rng(_NCOL[-1])}

    def ld_date_refs(idx: int) -> tuple[str, str]:
        r = f + idx
        return f"'{_TAB}'!{_FA_COL}{r}", f"'{_TAB}'!{_LA_COL}{r}"

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="LaneDetail", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render), ld_cols, ld_date_refs


(LANE_DETAIL, ld_cols, ld_date_refs) = _make_lane_detail()
