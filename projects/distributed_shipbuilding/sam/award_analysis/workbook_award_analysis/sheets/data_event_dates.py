"""data_event_dates - the "Event Dates" live wave-assignment helper sheet.

The bridge that lets the workbook re-cluster award waves LIVE from raw award
dates - so wave counts, cadence and sensitivity are formulas, not precomputed
CSV values. One row per (lane, DISTINCT award date), projected from the raw
Award Events leaf (the award dates are the only hardcoded inputs here - they are
extracted fields). Everything else is a live formula:

  Prior gap (days)  = this date - the previous award date IN THE SAME LANE.
  Wave start @W     = 1 when this date opens a new wave at clustering window W,
                      i.e. it is the lane's first date OR its prior gap > W.
                      One flag column per Assumptions sensitivity window
                      (45 / 60 / 90 / 120 / 180), each reading its window cell
                      live, so changing a window re-clusters that column.

n_waves at window W for a lane is then just SUMIFS(Wave start @W, lane) - the
count of wave starts - which reproduces the build_waves() clustering exactly
(a new wave begins when the gap to the prior date exceeds the window).

IMPORTANT - rows are build-ordered by (lane, date) and the live cells reference
the row DIRECTLY ABOVE (an O(n) running calculation; the workbook holds 11k+
event dates, so a self-joining COUNTIFS per row would be O(n^2) and far too slow
on every recalc). The sheet is therefore NOT a sortable native table - re-sorting
it would break the running gap/flag formulas. It is a read-mostly helper leaf;
the screens read it with absolute-range SUMIFS / MEDIAN, which are sort-proof.

Promoted accessor (module-level; imported by Wave Sensitivity + Lane Signals):
  ed_cols() - absolute column ranges (lane key parts, award date, prior gap, and
              the five Wave start @W flag columns) for the live roll-ups.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DATE_INPUT, S_DEFAULT, S_INT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, PROGRAMS, date_serial, load,
)
from workbook_award_analysis.sheets.summary_inputs import input_sens_window_cell
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_LABEL, W_DATE, W_DAYS, W_COUNT,
    header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_EVENT_DATES

_GROUP = "data"
_TAB = TAB_EVENT_DATES
_BANNER = "§1 - Event dates (live wave assignment)"

_WINDOWS = [45, 60, 90, 120, 180]
_HEADERS = (["Program", "PIID", "Work Type", "Lane key", "Award date",
             "Prior gap"] + [f"Wave start @{w}" for w in _WINDOWS])
_NCOLS = len(_HEADERS)
_COLS = ([W_PROGRAM, W_PIID, W_WORKTYPE, W_LABEL, W_DATE, W_DAYS]
         + [W_COUNT] * len(_WINDOWS))
_DATE_HDRS = {"Award date"}

def _C(i: int) -> str:
    return col_letter(1 + i)
_LANE_COL, _DATE_COL = _C(3), _C(4)          # E lane key, F award date
_GAP_COL = _C(5)                             # G prior gap
_START_COL = {w: _C(6 + n) for n, w in enumerate(_WINDOWS)}   # H..L


def _make_event_dates():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_award_events")
    porder = {p: n for n, (p, _) in enumerate(PROGRAMS)}
    # distinct (lane, date), build-ordered by lane then date so the row ABOVE is
    # the prior award date in the lane (the running calculation depends on it).
    seen = {}
    for row in rows:
        key = (row[i["program"]], row[i["piid"]], row[i["work_type"]],
               row[i["award_date"]])
        seen[key] = True
    keys = sorted(seen, key=lambda k: (porder.get(k[0], 9), k[1], k[2], k[3]))

    wref = {w: input_sens_window_cell(w) for w in _WINDOWS}

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, _DATE_HDRS))
    f = hdr + 1

    # live running formulas (reference the row directly above). The first data
    # row's "above" is the header text, so the lane-key comparison is unequal and
    # the row reads as a lane start (flag 1, blank gap) - correct.
    def gap_f(r):
        return (f'=IF({_LANE_COL}{r}<>{_LANE_COL}{r-1},"",'
                f'{_DATE_COL}{r}-{_DATE_COL}{r-1})')

    def start_f(w):
        wc = wref[w]
        return lambda r: (f'=IF({_LANE_COL}{r}<>{_LANE_COL}{r-1},1,'
                          f'IF({_DATE_COL}{r}-{_DATE_COL}{r-1}>{wc},1,0))')
    starts = {w: start_f(w) for w in _WINDOWS}

    for prog, piid, wt, d in keys:
        wt_disp = BUCKET_NAME.get(wt, wt)
        c.write(
            [prog, piid, wt_disp, f"{piid}|{wt_disp}", date_serial(d), gap_f]
            + [starts[w] for w in _WINDOWS],
            styles=([S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DATE_INPUT,
                     S_INT] + [S_INT] * len(_WINDOWS)),
            outline_level=1)
    last = hdr + len(keys)
    c.blank(2)
    c.write(["Build-ordered by lane then award date; the prior-gap and wave-start "
             "flags read the row directly above. Do not re-sort this sheet. "
             "n_waves at a window = SUMIFS(Wave start @window, lane)."],
            styles=[S_DEFAULT])

    def _abs(col: str) -> str:
        return f"'{_TAB}'!${col}${f}:${col}${last}"

    def ed_cols() -> dict:
        d = {"piid": _abs(_C(1)), "wt": _abs(_C(2)), "lane": _abs(_LANE_COL),
             "date": _abs(_DATE_COL), "gap": _abs(_GAP_COL)}
        for w in _WINDOWS:
            d[f"start{w}"] = _abs(_START_COL[w])
        return d

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws)        # NOT a native table (running formulas)

    return SheetEntry(_TAB, _GROUP, render), ed_cols


(EVENT_DATES, ed_cols) = _make_event_dates()
