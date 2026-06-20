"""model_by_piid - the "PIID" cut sheet (compact).

One filterable native table: every in-corpus PIID (10 Virginia + 5 Columbia + 24
DDG shipbuilder-directed), with a leading Program column, its scope meta (vessel
class, builder, label), data_status flag, full-history record counts (all roles
and supplier-only) and full-history supplier $M. COMPACT (no 16-FY grid): every
number is DERIVED - Records (all) is black SUMIFS over the Role Detail table by
PIID, Supplier rec is a black SUMIF over the Lane Vendors table, and $M is a black
SUMIFS over the Lane Detail $ Total; the bottom Totals Row is filter-aware
SUBTOTAL. Zero-record PIIDs are KEPT - which PIIDs the data can and cannot speak
to is itself the point of this cut.

Built at import via _make_by_piid() into a standalone single-table sheet (its
own title banner, §1 section table, column widths and autofilter).

Promoted accessors:
  piid_total_cell(program)       - module-level, full-history supplier $M (SUMIFS
                                   over Lane Detail; Checks).
  piid_sup_records_cell(program) - module-level, supplier record count (SUMIFS
                                   over Lane Vendors; Checks).
  piid_section_cols(program)     - section accessor (Class B), the program's
                                   contiguous PIID + Status column sub-ranges
                                   (Summary's coverage formulas).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import PROGRAMS, load
from workbook_award_analysis.sheets.data_lane_vendors import vl_cols
from workbook_award_analysis.sheets.data_lane_detail import ld_cols
from workbook_award_analysis.sheets.data_role_detail import rd_cols
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_CLASS, W_BUILDER, W_LABEL, W_STATUS, W_COUNT, W_DOLLAR,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_PIID

_GROUP = "model"
_TAB = TAB_PIID
_BANNER = "§1 - PIID"

_META = ["Program", "PIID", "Class", "Builder", "Label", "Status",
         "Records (all)", "Supplier rec", "$M"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_PIID, W_CLASS, W_BUILDER, W_LABEL, W_STATUS, W_COUNT,
         W_COUNT, W_DOLLAR]
_PIID_COL = col_letter(2)                               # C
_STATUS_COL = col_letter(6)                             # G
_REC_ALL_COL = col_letter(7)                            # H
_REC_SUP_COL = col_letter(8)                            # I
_DOL_COL = col_letter(9)                                # J ($M)
_LABEL_MAX = 60


def _trim(label) -> str:
    s = str(label or "")
    return s if len(s) <= _LABEL_MAX else s[:_LABEL_MAX - 1] + "…"


def _make_by_piid():
    """Build the PIID cut sheet: a row-2 title banner + the §1 section table.
    Returns (SheetEntry, piid_section_cols); piid_total_cell /
    piid_sup_records_cell are module-level, below."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    section: dict[str, tuple[int, int]] = {}
    i, rows = load("wb_annual_piid")
    V = vl_cols()
    L = ld_cols()
    R = rd_cols()

    def sup_records_f(r: int) -> str:
        return f"=SUMIF({V['piid']},C{r},{V['rec']})"

    def all_records_f(r: int) -> str:
        return f"=SUMIFS({R['rec']},{R['piid']},C{r})"

    def dollar_f(r: int) -> str:
        return f"=SUMIFS({L['dtot']},{L['piid']},C{r})"

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        pfirst = None
        for row in rows:
            if row[i["program"]] != prog:
                continue
            r = c.write([pname, row[i["piid"]], row[i["vessel_class"]],
                         row[i["builder"]], _trim(row[i["label"]]),
                         row[i["data_status"]],
                         all_records_f, sup_records_f, dollar_f],
                        styles=[S_DEFAULT] * 6 + [S_INT, S_INT, S_NUM],
                        outline_level=1)
            pfirst = pfirst if pfirst is not None else r
            last = r
        section[prog] = (pfirst, last)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None, None, None, None, None,
         f"=SUBTOTAL(109,{_REC_ALL_COL}{f}:{_REC_ALL_COL}{last})",
         f"=SUBTOTAL(109,{_REC_SUP_COL}{f}:{_REC_SUP_COL}{last})",
         f"=SUBTOTAL(109,{_DOL_COL}{f}:{_DOL_COL}{last})"],
        styles=[S_BOLD] + [S_DEFAULT] * 5 + [S_INT, S_INT, S_NUM],
        n_cols=_NCOLS)

    def piid_section_cols(program: str) -> dict:
        ff, ll = section[program]
        return {"piid": f"'{_TAB}'!${_PIID_COL}${ff}:${_PIID_COL}${ll}",
                "status": f"'{_TAB}'!${_STATUS_COL}${ff}:${_STATUS_COL}${ll}"}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="MarketPIID", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render), piid_section_cols


# --- module-level Class A accessors (leaf-relative; no own-row dependency) -----

def piid_total_cell(program: str) -> str:
    L = ld_cols()
    return f'SUMIFS({L["dtot"]},{L["prog"]},"{program}")'


def piid_sup_records_cell(program: str) -> str:
    V = vl_cols()
    return f'SUMIFS({V["rec"]},{V["prog"]},"{program}")'


(PIID, piid_section_cols) = _make_by_piid()
