"""data_lane_vendor_fy - the "Lane Vendor FY" leaf sheet.

The jump-ball LEAF: one row per (program, PIID, work type, vendor) carrying
the supplier's $M and record count BY subaward FY, the vendor's first/last
award in the lane, and a capability tag (vendor-side SAM NAICS - finer than
the seven work-type buckets, so a reviewer can see whether a multi-vendor
lane holds vendors that overlap on the same component or spread across
non-competing ones), from wb_vendor_lane_fy.csv as the native table
LaneVendorFY. Only the per-FY cells and the two dates are blue inputs; the
$M / Records totals and the prior/recent window sums are live row formulas.

The indicator tabs (Periodic Sourcing / Concentration / Source diversification)
derives every vendor count and concentration share LIVE (COUNTIFS / MAXIFS /
SUMIFS) from this table, keyed on each row's PIID + Work Type; this is the one
place those vendor x FY values are hardcoded.

Built at import via _make_lane_vendor_fy() into a standalone single-table sheet
(its own title banner, §1 section table, column widths and autofilter).

Promoted accessors (module-level; imported by the Indicators screens + Checks):
  lvf_cols() - absolute column ranges (program / piid / work type / vendor /
               capability + the live $ Recent / $ Prior / Rec Recent /
               Rec Prior / First / Last columns) for the Indicators tab.
  lvf_total_cell / lvf_records_total_cell(program) - the per-program SUMIF
               total cells (Checks direct-link legs).
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
    BUCKET_NAME, FY_KEYS, FY_LABELS, PROGRAMS, date_serial, load,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_FAMILY, W_PIID, W_WORKTYPE, W_UEI, W_VENDOR, W_CAPABILITY,
    W_NAICS4, W_DATE, W_COUNT, W_DOLLAR, W_FY, W_FY_N, header_styles,
)
from workbook_award_analysis.sheets.summary_inputs import input_recent_fy_cell
from workbook_award_analysis.sheets._tabs import TAB_LANE_VENDOR_FY

_GROUP = "data"
_TAB = TAB_LANE_VENDOR_FY
_BANNER = "§1 - Lane vendor FY"

# Inline FY array constant aligned to the 15 $ / N FY cells (le_fy12 -> 2012,
# fy2013 -> 2013, ... fy2026 -> 2026). The recent/prior window masks compare it
# against the Assumptions recent-FY cutoff cell; commas keep it horizontal so it
# aligns element-wise with the in-row FY range inside SUMPRODUCT.
_FY_ARR = "{" + ",".join(str(y) for y in range(2012, 2027)) + "}"

_DATE_HDRS = {"First Award", "Last Award"}

_NFY = len(FY_KEYS)               # 15 FY columns (no Total)

_META = ["Program", "Family", "PIID", "Work Type", "Vendor UEI", "Vendor",
         "Capability", "NAICS4", "First Award", "Last Award", "Records",
         "$M", "$ Prior", "$ Recent", "Rec Prior", "Rec Recent"]
_HEADERS = _META + [f"$ {l}" for l in FY_LABELS] + [f"N {l}" for l in FY_LABELS]
_CENTER_HDRS = ({f"$ {l}" for l in FY_LABELS}          # center both FY grids
                | {f"N {l}" for l in FY_LABELS})
_NCOLS = len(_HEADERS)
_NMETA = len(_META)
_COLS = ([W_PROGRAM, W_FAMILY, W_PIID, W_WORKTYPE, W_UEI,
          W_VENDOR, W_CAPABILITY, W_NAICS4, W_DATE, W_DATE,
          W_COUNT, W_DOLLAR, W_DOLLAR, W_DOLLAR, W_COUNT,
          W_COUNT] + [W_FY] * _NFY + [W_FY_N] * _NFY)
# content index i -> column letter (gutter shifts content to start at column B)
def _C(i: int) -> str:
    return col_letter(1 + i)
_PROG_COL, _PIID_COL, _WT_COL = _C(0), _C(2), _C(3)
_UEI_COL, _VEND_COL, _CAP_COL = _C(4), _C(5), _C(6)
_FA_COL, _LA_COL = _C(8), _C(9)
_REC_TOT_COL, _DOL_TOT_COL = _C(10), _C(11)            # L, M
_DOL_PRIOR_COL, _DOL_RECENT_COL = _C(12), _C(13)       # N, O
_REC_PRIOR_COL, _REC_RECENT_COL = _C(14), _C(15)       # P, Q
_DCOL = [_C(_NMETA + j) for j in range(_NFY)]        # 15 $ FY cols
_NCOL = [_C(_NMETA + _NFY + j) for j in range(_NFY)]   # 15 N FY cols


def _make_lane_vendor_fy():
    """Build the Lane Vendor FY leaf sheet: a row-2 title banner + the §1 section
    table. Returns (SheetEntry, lvf_cols, lvf_total_cell, lvf_records_total_cell)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_vendor_lane_fy")
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()

    hdr = c.write(_HEADERS,
                  styles=header_styles(_HEADERS, _DATE_HDRS, center_headers=_CENTER_HDRS))
    f, l = hdr + 1, hdr + len(rows)

    # live row formulas (callables resolved by RowCursor against the row).
    # $M / records totals are full-history SUMs; the prior/recent window sums
    # are SUMPRODUCT masks over the FY array vs the LIVE Assumptions recent-FY cutoff
    # (recent = FY >= cutoff; prior = FY < cutoff). At the default cutoff (2022)
    # this reproduces the fixed last-5 / first-10 split exactly, and the
    # Indicators screens inherit the window automatically.
    cut = input_recent_fy_cell()
    rec_tot = lambda r: f"=SUM({_NCOL[0]}{r}:{_NCOL[-1]}{r})"
    dol_tot = lambda r: f"=SUM({_DCOL[0]}{r}:{_DCOL[-1]}{r})"
    dol_recent = lambda r: (f"=SUMPRODUCT(({_FY_ARR}>={cut})*"
                            f"({_DCOL[0]}{r}:{_DCOL[-1]}{r}))")
    dol_prior = lambda r: (f"=SUMPRODUCT(({_FY_ARR}<{cut})*"
                           f"({_DCOL[0]}{r}:{_DCOL[-1]}{r}))")
    rec_recent = lambda r: (f"=SUMPRODUCT(({_FY_ARR}>={cut})*"
                            f"({_NCOL[0]}{r}:{_NCOL[-1]}{r}))")
    rec_prior = lambda r: (f"=SUMPRODUCT(({_FY_ARR}<{cut})*"
                           f"({_NCOL[0]}{r}:{_NCOL[-1]}{r}))")

    for row in rows:
        dvals = [row[i[f"d_{k}"]] if row[i[f"d_{k}"]] is not None else 0
                 for k in FY_KEYS]
        nvals = [row[i[f"n_{k}"]] if row[i[f"n_{k}"]] is not None else 0
                 for k in FY_KEYS]
        c.write([row[i["program"]], row[i["family"]], row[i["piid"]],
                 BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                 row[i["vendor_uei"]], row[i["vendor_name"]],
                 row[i["capability"]], row[i["naics4"]],
                 date_serial(row[i["first_award"]]),
                 date_serial(row[i["last_award"]]),
                 rec_tot, dol_tot, dol_prior, dol_recent, rec_prior, rec_recent]
                + dvals + nvals,
                styles=[S_DEFAULT] * 8 + [S_DATE_INPUT] * 2
                       + [S_INT, S_NUM, S_NUM, S_NUM, S_INT, S_INT]
                       + [S_NUM_INPUT] * _NFY + [S_INT_INPUT] * _NFY,
                outline_level=1)
    table_ref = f"B{hdr}:{_NCOL[-1]}{l}"
    c.blank(2)

    # per-program SUMIF totals (full history) - give Checks a leg proving the
    # leaf ties to every other supplier cut.
    prog_total: dict[str, int] = {}
    for prog, pname in PROGRAMS:
        prog_total[prog] = c.write(
            [f"{pname} supplier total ($M / records, full history)", None,
             None, None, None, None, None, None, None, None,
             f'=SUMIF(${_PROG_COL}${f}:${_PROG_COL}${l},"{prog}",'
             f'${_REC_TOT_COL}${f}:${_REC_TOT_COL}${l})',
             f'=SUMIF(${_PROG_COL}${f}:${_PROG_COL}${l},"{prog}",'
             f'${_DOL_TOT_COL}${f}:${_DOL_TOT_COL}${l})'],
            styles=[S_DEFAULT] * 10 + [S_INT, S_NUM])

    def lvf_cols() -> dict:
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${l}"
        return {"prog": rng(_PROG_COL), "piid": rng(_PIID_COL),
                "wt": rng(_WT_COL), "uei": rng(_UEI_COL),
                "vendor": rng(_VEND_COL), "cap": rng(_CAP_COL),
                "dol_prior": rng(_DOL_PRIOR_COL),
                "dol_recent": rng(_DOL_RECENT_COL),
                "rec_prior": rng(_REC_PRIOR_COL),
                "rec_recent": rng(_REC_RECENT_COL),
                "first": rng(_FA_COL), "last": rng(_LA_COL)}

    def lvf_total_cell(program: str) -> str:
        return f"'{_TAB}'!{_DOL_TOT_COL}{prog_total[program]}"

    def lvf_records_total_cell(program: str) -> str:
        return f"'{_TAB}'!{_REC_TOT_COL}{prog_total[program]}"

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="LaneVendorFY", ref=table_ref, headers=_HEADERS)])

    return (SheetEntry(_TAB, _GROUP, render), lvf_cols, lvf_total_cell,
            lvf_records_total_cell)


(LANE_VENDOR_FY, lvf_cols, lvf_total_cell,
 lvf_records_total_cell) = _make_lane_vendor_fy()
