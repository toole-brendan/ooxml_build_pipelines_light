"""data_role_detail - the "Role Detail" leaf sheet.

The workbook's role-grain LEAF data: one row per (program, role, PIID) with
at least one reported subaward record, from wb_role_piid.csv as the native
table RoleDetail - every role, all-roles basis, per-FY $M plus the record
count. By PIID's all-roles record counts and the Checks supplier legs derive
live from this table; only the FY cells and record counts here are hardcoded
(blue inputs), with black live row Totals. The Role column carries the same
display names (ROLE_NAME) the supplier legs filter on, so cross-sheet SUMIFS
criteria match structurally.

Built at import via _make_role_detail() into a standalone single-table sheet
(its own title banner, §1 section table, column widths and autofilter).

Promoted accessors (module-level; imported by By PIID + Checks):
  rd_cols() - absolute column ranges (program / role / piid / per-FY $ /
              records) for cross-sheet SUMIFS.
  role_supplier_total_cell(program)   - supplier full-history $M (SUMIFS over
              this leaf). Relocated here when the rolled-up By Role cut was
              retired; Checks still ties the supplier $M / records leg.
  role_supplier_records_cell(program) - supplier record count (SUMIFS).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DEFAULT, S_INT_INPUT, S_NUM,
    S_NUM_INPUT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    N_VALS, ROLE_NAME, VAL_LABELS, fy_vals, load, row_sum,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_ROLE, W_PIID, W_FY, W_COUNT, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_ROLE_DETAIL

_GROUP = "data"
_TAB = TAB_ROLE_DETAIL
_BANNER = "§1 - Role detail"

_META = ["Program", "Role", "PIID"]
_HEADERS = _META + [f"$ {l}" for l in VAL_LABELS] + ["Records"]
_CENTER_HDRS = {f"$ {l}" for l in VAL_LABELS} | {"Records"}   # center the FY grid + count
_NCOLS = len(_HEADERS)
_COLS = [W_PROGRAM, W_ROLE, W_PIID] + [W_FY] * N_VALS + [W_COUNT]
_PROG_COL = col_letter(1)                                    # B
_ROLE_COL = col_letter(2)                                    # C
_PIID_COL = col_letter(3)                                    # D
_VCOL = [col_letter(1 + len(_META) + j) for j in range(N_VALS)]    # E..T
_REC_COL = col_letter(1 + len(_META) + N_VALS)                     # U


def _make_role_detail():
    """Build the Role Detail leaf sheet: a row-2 title banner + the §1 section
    table. Returns (SheetEntry, rd_cols, role_supplier_total_cell,
    role_supplier_records_cell)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_role_piid")
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()

    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER_HDRS))
    f, l = hdr + 1, hdr + len(rows)
    for row in rows:
        role = row[i["role"]]
        c.write([row[i["program"]], ROLE_NAME.get(role, role),
                 row[i["piid"]]] + fy_vals(i, row)
                + [row_sum(_VCOL[0], _VCOL[-2]), row[i["n_records"]]],
                styles=[S_DEFAULT] * len(_META)
                       + [S_NUM_INPUT] * (N_VALS - 1) + [S_NUM]
                       + [S_INT_INPUT],
                outline_level=1)
    table_ref = f"B{hdr}:{_REC_COL}{l}"

    def rd_cols() -> dict:
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${l}"
        return {"prog": rng(_PROG_COL), "role": rng(_ROLE_COL),
                "piid": rng(_PIID_COL), "rec": rng(_REC_COL),
                "dfy": [rng(col) for col in _VCOL[:-1]],
                "dtot": rng(_VCOL[-1])}

    def role_supplier_total_cell(program: str) -> str:
        R = rd_cols()
        return (f'SUMIFS({R["dtot"]},{R["prog"]},"{program}",'
                f'{R["role"]},"Supplier")')

    def role_supplier_records_cell(program: str) -> str:
        R = rd_cols()
        return (f'SUMIFS({R["rec"]},{R["prog"]},"{program}",'
                f'{R["role"]},"Supplier")')

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="RoleDetail", ref=table_ref, headers=_HEADERS)])

    return (SheetEntry(_TAB, _GROUP, render), rd_cols,
            role_supplier_total_cell, role_supplier_records_cell)


(ROLE_DETAIL, rd_cols, role_supplier_total_cell,
 role_supplier_records_cell) = _make_role_detail()
