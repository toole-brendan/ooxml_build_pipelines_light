"""model_source_concentration - the "Source Diversification" indicator sheet.

Indicator 3 = a lane historically held by ONE supplier where a credible second
source has recently entered (incumbent still present = a split, not a swap). One
filterable native table with a leading Program column: one row per (program, PIID
x work-type) lane, sorted by recent supplier $. The single->multi move reads off
the data - Active vendors steps from 1 (prior) to >= 2 (recent) while the
incumbent stays active and Top-1 share falls.

Active vendor counts and Top-1 concentration shares are DERIVED LIVE - COUNTIFS /
SUMIFS / MAXIFS over the Lane Vendors x FY leaf, split into prior and recent
windows (the LIVE Assumptions recent-FY cutoff drives the split at the leaf). The
identity signals Excel cannot derive - the second-source entry FY, the incumbent
and whether it is still active - are a live XLOOKUP of the Lane Signals leaf
(keyed on PIID|Work Type), so nothing is hardcoded on this calculation tab. The
bottom Totals Row (prior/recent $) is filter-aware SUBTOTAL.

Built at import via _make_source_concentration() into a standalone single-table
sheet (its own title banner, §1 section table, column widths and autofilter).

Promoted accessor (module-level; imported by Summary):
  sc_emerging_count(program) - count of emerging-competition lanes (prior
                               single-source -> recent multi-source, incumbent
                               still active), for Summary's findings block.
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
from workbook_award_analysis.sheets.data_lane_signals import ls_cols
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DOLLAR, W_PCT, W_STATUS,
    W_VENDOR, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_SOURCE_DIVERSIFICATION
from workbook_award_analysis.sheets._yn import S_CENTER

_GROUP = "model"
_TAB = TAB_SOURCE_DIVERSIFICATION
_BANNER = "§1 - Source diversification"

_META = ["Program", "PIID", "Work Type", "Vendors prior", "Vendors recent",
         "Prior $M", "Recent $M", "Top-1 prior", "Top-1 recent",
         "2nd-source FY", "Incumbent", "Incumbent active"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_COUNT, W_DOLLAR, W_DOLLAR,
         W_PCT, W_PCT, W_STATUS, W_VENDOR, W_STATUS]
_PIID = col_letter(2)     # C
_WT = col_letter(3)       # D
_PRIOR = col_letter(6)    # G  Prior $M
_RECENT = col_letter(7)   # H  Recent $M


def _make_source_concentration():
    """Build the Source diversification screen sheet: a row-2 title banner + the
    §1 section table. Returns (SheetEntry, sc_emerging_count)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    L = lvf_cols()
    LS = ls_cols()
    i, rows = load("wb_lane_signals")

    def crit(r):
        return f'{L["piid"]},{_PIID}{r},{L["wt"]},{_WT}{r}'

    vprior_f = lambda r: f'=COUNTIFS({crit(r)},{L["rec_prior"]},">0")'
    vrecent_f = lambda r: f'=COUNTIFS({crit(r)},{L["rec_recent"]},">0")'
    prior_d_f = lambda r: f'=SUMIFS({L["dol_prior"]},{crit(r)})'
    recent_d_f = lambda r: f'=SUMIFS({L["dol_recent"]},{crit(r)})'
    top1_prior_f = lambda r: (f'=IF({_PRIOR}{r}=0,0,'
                              f'_xlfn.MAXIFS({L["dol_prior"]},{crit(r)})/{_PRIOR}{r})')
    top1_recent_f = lambda r: (f'=IF({_RECENT}{r}=0,0,'
                               f'_xlfn.MAXIFS({L["dol_recent"]},{crit(r)})/{_RECENT}{r})')
    # identity signals Excel can't derive (second-source entry FY, incumbent +
    # whether it is still active) - live XLOOKUP of the Lane Signals leaf, keyed
    # on PIID|Work Type, so no hardcoded cells sit on this calculation tab.
    def _look(col: str):
        return lambda r: (f'=_xlfn.XLOOKUP({_PIID}{r}&"|"&{_WT}{r},'
                          f'{LS["key"]},{LS[col]},"")')
    secondfy_f = _look("secondfy")
    incumbent_f = _look("incumbent")
    incactive_f = _look("incactive")

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
                 vprior_f, vrecent_f, prior_d_f, recent_d_f,
                 top1_prior_f, top1_recent_f,
                 secondfy_f, incumbent_f, incactive_f],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT, S_INT, S_NUM,
                        S_NUM, S_PCT, S_PCT, S_DEFAULT, S_DEFAULT, S_CENTER],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None, None, None, None,
         f"=SUBTOTAL(109,{_PRIOR}{f}:{_PRIOR}{last})",
         f"=SUBTOTAL(109,{_RECENT}{f}:{_RECENT}{last})",
         None, None, None, None, None],
        styles=[S_BOLD] + [S_DEFAULT] * 4 + [S_NUM, S_NUM] + [S_DEFAULT] * 5,
        n_cols=_NCOLS)
    c.blank(2)
    c.write(["Criteria: prior single-source; recent multi-source; incumbent "
             "active; FY26 partial."],
            styles=[S_DEFAULT])

    def sc_emerging_count(program: str) -> str:
        # Emerging competition = a prior single-source lane (Vendors prior (E) = 1)
        # now recently multi-source (Vendors recent (F) >= 2) where the incumbent
        # is still active (Incumbent active (M) = "Y") - a split, not a swap.
        # All three conditions are the table's stated criteria; keyed by Program
        # (B, display name) over the table body.
        def rng(col: str) -> str:
            return f"'{_TAB}'!${col}${f}:${col}${last}"
        return (f'COUNTIFS({rng(col_letter(1))},"{program_label(program)}",'
                f'{rng(col_letter(4))},1,{rng(col_letter(5))},">=2",'
                f'{rng(col_letter(12))},"Y")')

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="SourceConcentration", ref=table_ref,
                       headers=_META)])

    return SheetEntry(_TAB, _GROUP, render), sc_emerging_count


(SOURCE_DIVERSIFICATION, sc_emerging_count) = _make_source_concentration()
