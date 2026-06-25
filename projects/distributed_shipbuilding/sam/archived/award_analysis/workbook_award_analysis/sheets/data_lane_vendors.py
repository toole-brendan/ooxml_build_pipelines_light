"""data_lane_vendors - the "Lane Vendors" leaf sheet.

One row per (PIID, work type, vendor): the record count and $M each supplier
vendor holds in each PIID x Work Type lane, from wb_vendor_lane.csv as the
native table VendorLane. This is the workbook's finest-grain (leaf) supplier
data and the live source behind the derived counts and $ elsewhere: the
Vendors / Repeat % / Shared % formulas and lane $M on Supplier Lanes,
supplier records on By PIID, and Records on By Vendor are all SUMIF(S) /
COUNTIFS over this table. The last two columns are themselves live - COUNTIFS
over the table counting how many PIIDs that row's vendor holds that work type
on, once scoped to the row's program (same-class for virginia / columbia) and
once to its family (Submarines spans both classes; identical for DDG-51,
which is its own family).

Built at import via _make_vendor_lane() into a standalone single-table sheet
(its own title banner, §1 section table, column widths and autofilter).

Promoted accessor (module-level; imported by the sheets that derive from this leaf):
  vl_cols() - absolute column ranges (program / piid / work type / uei /
              records / dollars / program and family PIID footprints) for
              cross-sheet COUNTIFS / SUMIFS.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_INT_INPUT, S_NUM,
    S_NUM_INPUT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import BUCKET_NAME, PROGRAMS, load
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_FAMILY, W_PIID, W_WORKTYPE, W_UEI, W_VENDOR, W_COUNT, W_DOLLAR,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_LANE_VENDORS

_GROUP = "data"
_TAB = TAB_LANE_VENDORS
_BANNER = "§1 - Lane vendors"

_HEADERS = ["Program", "Family", "PIID", "Work Type", "Vendor UEI", "Vendor",
            "Records", "$M (hist)", "PIIDs (WT)", "PIIDs (flt)"]
_NCOLS = len(_HEADERS)
_COLS = [W_PROGRAM, W_FAMILY, W_PIID, W_WORKTYPE, W_UEI,
         W_VENDOR, W_COUNT, W_DOLLAR, W_COUNT, W_COUNT]
_PROG_COL = col_letter(1)                                   # B
_FAM_COL = col_letter(2)                                    # C
_PIID_COL = col_letter(3)                                   # D
_WT_COL = col_letter(4)                                     # E
_UEI_COL = col_letter(5)                                    # F
_REC_COL = col_letter(7)                                    # H
_DOL_COL = col_letter(8)                                    # I
_NP_COL = col_letter(9)                                     # J
_NPF_COL = col_letter(10)                                   # K


def _make_vendor_lane():
    """Build the Lane Vendors leaf sheet: a row-2 title banner + the §1 section
    table. Returns (SheetEntry, vl_cols)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_vendor_lane")
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()

    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS))
    f, l = hdr + 1, hdr + len(rows)

    def _footprint(scope_col: str, r: int) -> str:
        return (f"=COUNTIFS(${scope_col}${f}:${scope_col}${l},{scope_col}{r},"
                f"${_WT_COL}${f}:${_WT_COL}${l},{_WT_COL}{r},"
                f"${_UEI_COL}${f}:${_UEI_COL}${l},{_UEI_COL}{r})")

    def np_formula(r: int) -> str:
        return _footprint(_PROG_COL, r)

    def npf_formula(r: int) -> str:
        return _footprint(_FAM_COL, r)

    last = hdr
    for row in rows:
        last = c.write([row[i["program"]], row[i["family"]], row[i["piid"]],
                        BUCKET_NAME.get(row[i["work_type"]],
                                        row[i["work_type"]]),
                        row[i["vendor_uei"]], row[i["vendor_name"]],
                        row[i["n_records"]], row[i["dollars"]] or 0,
                        np_formula, npf_formula],
                       styles=[S_DEFAULT] * 6 + [S_INT_INPUT, S_NUM_INPUT,
                                                 S_INT, S_INT],
                       outline_level=1)
    assert last == l
    table_ref = f"B{hdr}:{_NPF_COL}{l}"
    c.blank(2)

    for prog, pname in PROGRAMS:
        c.write([f"{pname} total", None, None, None, None, None,
                 f'=SUMIF(${_PROG_COL}${f}:${_PROG_COL}${l},"{prog}",'
                 f'${_REC_COL}${f}:${_REC_COL}${l})',
                 f'=SUMIF(${_PROG_COL}${f}:${_PROG_COL}${l},"{prog}",'
                 f'${_DOL_COL}${f}:${_DOL_COL}${l})', None, None],
                styles=[S_DEFAULT] * 6 + [S_INT, S_NUM, S_DEFAULT, S_DEFAULT])

    def vl_cols() -> dict:
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${l}"
        return {"prog": rng(_PROG_COL), "piid": rng(_PIID_COL),
                "wt": rng(_WT_COL), "uei": rng(_UEI_COL),
                "rec": rng(_REC_COL), "dol": rng(_DOL_COL),
                "np": rng(_NP_COL), "npf": rng(_NPF_COL)}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="VendorLane", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render), vl_cols


(LANE_VENDORS, vl_cols) = _make_vendor_lane()
