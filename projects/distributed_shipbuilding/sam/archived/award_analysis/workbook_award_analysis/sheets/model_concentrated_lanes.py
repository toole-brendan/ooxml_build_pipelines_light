"""model_concentrated_lanes - the "Concentration" indicator sheet.

Indicator 2, the level read = a lane where ONE vendor holds most of the recent
supplier $ - contestable on its own, whether or not it is yet splitting (the
"in motion" subset lives on Source diversification). One filterable native table
with a leading Program column: one row per (program, PIID x work-type) lane,
sorted by recent supplier $ (materiality first, as the sibling indicator
sections). The screen is top-1 vendor share >= the LIVE Assumptions concentration
cutoff of recent supplier $; filter Top-1 share to that cut and the material
concentrated lanes lead. Read off the data, not labelled.

Active vendors, Recent $M and Top-1 share are DERIVED LIVE - COUNTIFS / SUMIFS /
MAXIFS over the Lane Vendors x FY leaf on the recent window, keyed on each row's
own PIID + Work Type cells. Only the identity Excel cannot derive - the current
top vendor's name - is a leaf value (text) from wb_lane_signals.csv. Lanes with
no recent $ fall to Top-1 share 0 and sort to the bottom. The bottom Totals Row
(recent $) is filter-aware SUBTOTAL.

Built at import via _make_concentrated_lanes() into a standalone single-table
sheet (its own title banner, §1 section table, column widths and autofilter).

Promoted accessor (module-level; imported by Summary):
  cl_concentrated_count(program) - count of lanes at/above the LIVE concentration
                                   cutoff, for Summary's findings block.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_NUM, S_PCT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, PROGRAMS, load, program_label,
)
from workbook_award_analysis.sheets.data_lane_vendor_fy import lvf_cols
from workbook_award_analysis.sheets.summary_inputs import input_conc_threshold_cell
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DOLLAR, W_PCT, W_VENDOR,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_CONCENTRATION

_GROUP = "model"
_TAB = TAB_CONCENTRATION
_BANNER = "§1 - Concentration"

_META = ["Program", "PIID", "Work Type", "Active vendors", "Recent $M",
         "Top-1 share", "Top vendor (recent)"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DOLLAR, W_PCT, W_VENDOR]
_PIID = col_letter(2)     # C
_WT = col_letter(3)       # D
_RECENT = col_letter(5)   # F  Recent $M
_TOP1 = col_letter(6)     # G  Top-1 share


def _make_concentrated_lanes():
    """Build the Concentration screen sheet: a row-2 title banner + the §1
    section table. Returns (SheetEntry, cl_concentrated_count)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    L = lvf_cols()
    i, rows = load("wb_lane_signals")

    def crit(r):
        return f'{L["piid"]},{_PIID}{r},{L["wt"]},{_WT}{r}'

    active_f = lambda r: f'=COUNTIFS({crit(r)},{L["rec_recent"]},">0")'
    recent_f = lambda r: f'=SUMIFS({L["dol_recent"]},{crit(r)})'
    top1_f = lambda r: (f'=IF({_RECENT}{r}=0,0,'
                        f'_xlfn.MAXIFS({L["dol_recent"]},{crit(r)})/{_RECENT}{r})')

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        prows = sorted((row for row in rows if row[i["program"]] == prog),
                       key=lambda row: -(row[i["dollars_recent"]] or 0))
        for row in prows:
            last = c.write(
                [pname, row[i["piid"]],
                 BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                 active_f, recent_f, top1_f,
                 row[i["recent_top1_name"]] or ""],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT, S_NUM, S_PCT,
                        S_DEFAULT],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None, None, None,
         f"=SUBTOTAL(109,{_RECENT}{f}:{_RECENT}{last})", None, None],
        styles=[S_BOLD] + [S_DEFAULT] * 3 + [S_NUM] + [S_DEFAULT] * 2,
        n_cols=_NCOLS)
    c.blank(2)
    c.write(["Criteria: top-1 share ≥ Assumptions cutoff; FY26 partial."],
            styles=[S_DEFAULT])

    def cl_concentrated_count(program: str) -> str:
        # Concentrated = top-1 share (G) >= the LIVE Assumptions concentration cutoff,
        # keyed by Program (B) over the table body. Zero-recent-$ lanes read
        # Top-1 share 0 and drop out of the comparison.
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${last}"
        return (f'COUNTIFS({rng(col_letter(1))},"{program_label(program)}",'
                f'{rng(_TOP1)},">="&{input_conc_threshold_cell()})')

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="ConcentratedLanes", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render), cl_concentrated_count


(CONCENTRATION, cl_concentrated_count) = _make_concentrated_lanes()
