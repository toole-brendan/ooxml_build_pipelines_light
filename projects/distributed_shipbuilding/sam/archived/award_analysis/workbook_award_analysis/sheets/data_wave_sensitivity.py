"""data_wave_sensitivity - the "Wave Sensitivity" sheet (now fully LIVE).

One row per (lane x clustering window): how many award waves the lane has, and
the typical gap between them, when the clustering window is 45 / 60 / 90 / 120 /
180 days. Nothing here is precomputed any more - the values are live formulas
over the Event Dates leaf, which assigns wave starts live from the raw award
dates. Change a sensitivity window on Assumptions and the counts re-cluster.

  Window (days)              link to the live Assumptions sensitivity window.
  Award waves                = SUMIFS(Event Dates[Wave start @W], lane) - the
                               count of wave starts at that window (exactly the
                               build_waves clustering result, but computed live).
  Median between-wave gap    = MEDIAN of the prior gaps at this lane's wave
                               starts (a single-cell array formula); blank for a
                               one-wave lane (no between-wave gap).

This answers the standing question "where do the award-wave / gap numbers come
from?": from the raw award dates, via formulas - no compute script. The only
hardcoded inputs in the wave pipeline are the award dates on Event Dates.

A reviewer can filter one lane and read how its wave count holds (or collapses)
as the window widens - the Lane Signals "Window-stable" verdict is the live
60/90/120 comparison of these same counts.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, ArrayF
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_LINK_INT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import BUCKET_NAME, PROGRAMS, load
from workbook_award_analysis.sheets.data_event_dates import ed_cols
from workbook_award_analysis.sheets.summary_inputs import input_sens_window_cell
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_DAYS, W_COUNT, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_WAVE_SENSITIVITY

_GROUP = "data"
_TAB = TAB_WAVE_SENSITIVITY
_BANNER = "§1 - Wave sensitivity"
_WINDOWS = [45, 60, 90, 120, 180]

_HEADERS = ["Program", "PIID", "Work Type", "Window (days)", "Award waves",
            "Median between-wave gap (days)"]
_NCOLS = len(_HEADERS)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_DAYS, W_COUNT, W_DAYS]
_CENTER_HDRS = {"Window (days)", "Award waves",
                "Median between-wave gap (days)"}
_PIID, _WT = col_letter(2), col_letter(3)    # C, D


def _make_wave_sensitivity():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_lane_signals")            # lane roster only (132 lanes)
    porder = {p: n for n, (p, _) in enumerate(PROGRAMS)}
    lanes = sorted(((row[i["program"]], row[i["piid"]], row[i["work_type"]])
                    for row in rows),
                   key=lambda k: (porder.get(k[0], 9), k[1], k[2]))
    E = ed_cols()

    def waves_f(w):
        return lambda r: f'=SUMIFS({E[f"start{w}"]},{E["piid"]},{_PIID}{r},{E["wt"]},{_WT}{r})'

    def gap_f(w):
        # median of the prior gaps at this lane's wave starts (a wave start that
        # is not the lane's first date carries the between-wave gap; the first
        # date's gap is blank and drops out). Single-cell array formula.
        return lambda r: ArrayF(
            f'=IFERROR(MEDIAN(IF(({E["piid"]}={_PIID}{r})*({E["wt"]}={_WT}{r})*'
            f'({E[f"start{w}"]}=1),{E["gap"]})),"")')
    win_f = {w: input_sens_window_cell(w) for w in _WINDOWS}

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS,
                                                 center_headers=_CENTER_HDRS))
    f = hdr + 1
    last = hdr
    for prog, piid, wt in lanes:
        wt_disp = BUCKET_NAME.get(wt, wt)
        pname = dict(PROGRAMS).get(prog, prog)
        for w in _WINDOWS:
            last = c.write(
                [pname, piid, wt_disp, f"={win_f[w]}", waves_f(w), gap_f(w)],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_LINK_INT, S_INT,
                        S_INT],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.blank(2)
    c.write(["Live from Event Dates: Award waves = SUMIFS(Wave start @window, "
             "lane); the between-wave gap median is a single-cell array formula "
             "over the same wave starts. Change a window on Assumptions §3b to "
             "re-cluster. FY26 partial."],
            styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="WaveSensitivity", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render)


WAVE_SENSITIVITY = _make_wave_sensitivity()
