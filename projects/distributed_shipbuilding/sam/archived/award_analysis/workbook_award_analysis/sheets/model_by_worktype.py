"""model_by_worktype - the "Work Type" cut sheet (compact).

One filterable native table: supplier subaward $M and record counts by work-type
bucket, per program, with a leading Program column. COMPACT (no 16-FY grid): the
two figures are fully DERIVED - black SUMIFS over the Lane Detail leaf's $ Total
and record-count Total columns, keyed on the program key and each row's own
bucket cell. The bottom filter-aware Totals Row uses SUBTOTAL.
wb_annual_worktype.csv is read only for the bucket roster and its descending
full-history dollar order.

Built at import via _make_by_worktype() into a standalone single-table sheet
(its own title banner, §1 section table, column widths and autofilter).

Promoted accessors (module-level, leaf-relative = independent of this sheet's
own rows; imported by Program / Summary / Checks):
  wt_total_cell(program)         - full-history supplier $M (SUMIFS over Lane
                                   Detail).
  wt_records_total_cell(program) - full-history record count.
  wt_total_fy_refs(program)      - 15 per-FY supplier-$ SUMIFS fragments (the
                                   §1 Program FY grid consumes these).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import BUCKET_NAME, PROGRAMS, load
from workbook_award_analysis.sheets.data_lane_detail import ld_cols
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_WORKTYPE, W_DOLLAR, W_COUNT, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_WORK_TYPE

_GROUP = "model"
_TAB = TAB_WORK_TYPE
_BANNER = "§1 - Work type"

_META = ["Program", "Work type", "$M", "Records"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_WORKTYPE, W_DOLLAR, W_COUNT]
_DOL_COL = col_letter(3)                # D  ($M)
_REC_COL = col_letter(4)                # E  (Records)
_WT_COL = col_letter(2)                 # C  (each row's bucket cell)


def _lane_sumifs(rng: str, prog_rng: str, prog: str, wt_rng: str):
    """One derived cell: the program's lane $ / counts for this row's bucket."""
    return lambda r: f'=SUMIFS({rng},{prog_rng},"{prog}",{wt_rng},$C{r})'


def _make_by_worktype():
    """Build the Work type cut sheet: a row-2 title banner + the §1 section
    table. Returns the SheetEntry (its accessors are module-level, below)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_annual_worktype")
    L = ld_cols()
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        for row in rows:
            if row[i["program"]] != prog:
                continue
            bucket = BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]])
            last = c.write(
                [pname, bucket,
                 _lane_sumifs(L["dtot"], L["prog"], prog, L["wt"]),
                 _lane_sumifs(L["ntot"], L["prog"], prog, L["wt"])],
                styles=[S_DEFAULT, S_DEFAULT, S_NUM, S_INT],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None,
         f"=SUBTOTAL(109,{_DOL_COL}{f}:{_DOL_COL}{last})",
         f"=SUBTOTAL(109,{_REC_COL}{f}:{_REC_COL}{last})"],
        styles=[S_BOLD, S_DEFAULT, S_NUM, S_INT], n_cols=_NCOLS)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="MarketWorkType", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render)


# --- module-level Class A accessors (leaf-relative; no own-row dependency) ----

def wt_total_cell(program: str) -> str:
    L = ld_cols()
    return f'SUMIFS({L["dtot"]},{L["prog"]},"{program}")'


def wt_records_total_cell(program: str) -> str:
    L = ld_cols()
    return f'SUMIFS({L["ntot"]},{L["prog"]},"{program}")'


def wt_total_fy_refs(program: str) -> list[str]:
    L = ld_cols()
    return [f'SUMIFS({rng},{L["prog"]},"{program}")' for rng in L["dfy"]]


WORK_TYPE = _make_by_worktype()
