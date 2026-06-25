"""model_rebuy_timing - the "Periodic Sourcing" indicator sheet.

Indicator 1 = an existing MULTI-SOURCE lane the prime already splits across
several suppliers, surfaced - WHEN its buying is genuinely periodic - with an
estimated next sourcing WINDOW. One filterable native table with a leading Program
column: one row per (program, PIID x work-type) lane, sorted by recent supplier
$ so material multi-source lanes sit on top. (Tab renamed from "Re-buy Timing":
now that continuous lanes are split off, only periodic, cadence-applicable lanes
are timed here; "re-buy" stays in the methodology narrative.)

Two gates, both EXPLICIT and live:

  Shared-lane eligible = Active vendors (recent) >= the Assumptions multi-source
                       minimum AND Top-1 share <= the Assumptions concentration
                       cutoff (a materially shared lane, not a concentrated one).
  Cadence applicable = the lane's award waves are DISCRETE: >= 2 waves, longest
                       wave span <= the Assumptions periodic-max duration, and
                       span/cadence ratio <= the Assumptions cap. 90-day single-
                       linkage chains a CONTINUOUSLY-active lane into one multi-
                       year "wave", so a long wave span (not the gap count) is
                       the tell; those lanes are routed to Continuous Sourcing
                       instead of carrying a spurious next-wave date.
  Forecast window due = cadence applicable AND the forecast WINDOW overlaps the
                       Assumptions horizon of the as-of date.
  Periodic opening due = eligible AND forecast window due  <- the headline opening.

The forecast is a WINDOW, not a point: a periodic buy is an interval, not a day.
  Forecast start = Last award + Median quiet gap   (next lull, then buy)
  Forecast end   = Forecast start + Median wave span
Both blank unless cadence applicable. The naive point-date measure (Last award +
cadence, in horizon, no gate) is kept as a single Ungated timing signal column for
the secondary Summary diagnostic - it is what the gate strips out.

NOTHING is hardcoded on this calculation tab. Every count and share is DERIVED
LIVE - COUNTIFS / SUMIFS / MAXIFS over the Lane Vendor FY leaf, keyed on each
row's PIID + Work Type, on the recent window. The wave-shape cells (Award-wave
cadence = median wave-anchor gap, Award waves, Gap CV, Longest/Median wave span,
Median quiet gap) are LIVE SUMIFS into the Lane Signals data leaf (the wave table
can't be re-clustered live, but its outputs live in a data sheet, not as blue
cells here). Sourcing mode / Cadence applicable / Cadence confidence are LIVE
formulas over those cells + the Assumptions §2b knobs, so the periodic/continuous
split is adjustable in-book. The bottom Totals Row (recent $) is filter-aware
SUBTOTAL.

Built at import via _make_rebuy_timing() into a standalone single-table sheet.

Promoted accessors (module-level; imported by Summary):
  rb_due_count(program)        - lanes Periodic opening due (eligible AND cadence-
                                 applicable AND window-due) - the strict headline.
  rb_timing_due_count(program) - lanes flagged by the naive Ungated timing signal
                                 (point date in horizon, no gate), for the
                                 secondary diagnostic row.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DATE, S_DEFAULT, S_INT, S_NUM, S_PCT,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, PROGRAMS, load, program_label,
)
from workbook_award_analysis.sheets.data_lane_vendor_fy import lvf_cols
from workbook_award_analysis.sheets.data_lane_signals import ls_cols
from workbook_award_analysis.sheets.summary_inputs import (
    input_asof_cell, input_horizon_cell, input_multisource_cell,
    input_conc_threshold_cell, input_periodic_maxdur_cell, input_ratio_cap_cell,
    input_strong_minwaves_cell, input_strong_cvcap_cell,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DOLLAR, W_PCT, W_DATE, W_STATUS,
    W_RATIO, W_DAYS, W_MODE, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_REBUY_TIMING
from workbook_award_analysis.sheets._yn import S_CENTER

_GROUP = "model"
_TAB = TAB_REBUY_TIMING
_BANNER = "§1 - Periodic sourcing"

_META = ["Program", "PIID", "Work Type", "Active vendors", "Recent $M",
         "Top-1 share", "Others' share", "Last award", "Award-wave cadence",
         "Award waves", "Gap CV", "Longest span", "Median span",
         "Median quiet gap", "Span/cadence ratio", "Sourcing mode",
         "Cadence applicable", "Cadence confidence", "Shared-lane eligible",
         "Forecast start", "Forecast end", "Forecast window due",
         "Periodic opening due", "Ungated timing signal"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DOLLAR, W_PCT, W_PCT,
         W_DATE, W_DAYS, W_COUNT, W_RATIO, W_DAYS, W_DAYS, W_DAYS, W_RATIO,
         W_MODE, W_STATUS, W_STATUS, W_STATUS, W_DATE, W_DATE, W_STATUS,
         W_STATUS, W_STATUS]
# within-row column letters (gutter mode: content i -> column 1+i)
_PIID = col_letter(2)      # C
_WT = col_letter(3)        # D
_ACTIVE = col_letter(4)    # E  Active vendors
_RECENT = col_letter(5)    # F  Recent $M
_TOP1 = col_letter(6)      # G  Top-1 share
_LAST = col_letter(8)      # I  Last award
_GAP = col_letter(9)       # J  Award-wave cadence (median wave gap)
_WAVES = col_letter(10)    # K  Award waves
_CV = col_letter(11)       # L  Gap CV
_SPAN = col_letter(12)     # M  Longest wave span
_MSPAN = col_letter(13)    # N  Median wave span
_QGAP = col_letter(14)     # O  Median quiet gap
_RATIO = col_letter(15)    # P  Span/cadence ratio
_MODE = col_letter(16)     # Q  Sourcing mode
_CADAPPL = col_letter(17)  # R  Cadence applicable
_CONF = col_letter(18)     # S  Cadence confidence
_ELIG = col_letter(19)     # T  Shared-lane eligible
_FSTART = col_letter(20)   # U  Forecast start
_FEND = col_letter(21)     # V  Forecast end
_TIMING = col_letter(22)   # W  Forecast window due
_DUE = col_letter(23)      # X  Periodic opening due
_DATEONLY = col_letter(24) # Y  Ungated timing signal (diagnostic)
_DATE_HDRS = {"Last award", "Forecast start", "Forecast end"}


def _make_rebuy_timing():
    """Build the Periodic sourcing screen sheet: a row-2 title banner + the §1
    section table. Returns (SheetEntry, rb_due_count, rb_timing_due_count)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    L = lvf_cols()
    LS = ls_cols()
    i, rows = load("wb_lane_signals")
    multimin = input_multisource_cell()
    conccut = input_conc_threshold_cell()
    asof = input_asof_cell()
    horizon = input_horizon_cell()
    pmax = input_periodic_maxdur_cell()
    ratiocap = input_ratio_cap_cell()
    strongn = input_strong_minwaves_cell()
    cvcap = input_strong_cvcap_cell()

    def crit(r):
        return f'{L["piid"]},{_PIID}{r},{L["wt"]},{_WT}{r}'

    active_f = lambda r: f'=COUNTIFS({crit(r)},{L["rec_recent"]},">0")'
    recent_f = lambda r: f'=SUMIFS({L["dol_recent"]},{crit(r)})'
    top1_f = lambda r: (f'=IF({_RECENT}{r}=0,0,'
                        f'_xlfn.MAXIFS({L["dol_recent"]},{crit(r)})/{_RECENT}{r})')
    others_f = lambda r: f'=IF({_RECENT}{r}=0,0,1-{_TOP1}{r})'
    last_f = lambda r: f'=_xlfn.MAXIFS({L["last"]},{crit(r)})'
    # wave-shape cells: live SUMIFS over the Lane Signals leaf (a lane is unique
    # by PIID + Work Type, so the sum returns that lane's single value) - no
    # hardcoded shape cells on this calculation screen. Gap CV is blank for
    # <3-wave lanes (no dispersion to measure), matching the leaf.
    def critLS(r):
        return f'{LS["piid"]},{_PIID}{r},{LS["wt"]},{_WT}{r}'

    gap_f = lambda r: f'=SUMIFS({LS["gap"]},{critLS(r)})'
    waves_f = lambda r: f'=SUMIFS({LS["waves"]},{critLS(r)})'
    cv_f = lambda r: f'=IF({_WAVES}{r}<3,"",SUMIFS({LS["cv"]},{critLS(r)}))'
    span_f = lambda r: f'=SUMIFS({LS["span"]},{critLS(r)})'
    mspan_f = lambda r: f'=SUMIFS({LS["mspan"]},{critLS(r)})'
    qgap_f = lambda r: f'=SUMIFS({LS["qgap"]},{critLS(r)})'
    # span / cadence ratio: a "wave" that lasts longer than the cadence is not a
    # discrete event. Blank for single-wave lanes (cadence = 0).
    ratio_f = lambda r: f'=IF({_GAP}{r}=0,"",{_SPAN}{r}/{_GAP}{r})'
    # sourcing mode (live classification over the blue shape cells + §2b knobs;
    # wave-shape only, so the same formula reads identically on Continuous
    # Sourcing and Wave Cadence). Continuity is tested FIRST: a lane active for
    # years with no 90-day gap is ONE long wave - continuous, not "sparse".
    mode_f = lambda r: (
        f'=IF(OR({_SPAN}{r}>{pmax},AND({_RATIO}{r}<>"",{_RATIO}{r}>{ratiocap})),'
        f'"Continuous sourcing",'
        f'IF({_WAVES}{r}<2,"Sparse / one-off",'
        f'IF({_WAVES}{r}>={strongn},"Periodic sourcing","Weak periodic")))')
    cadappl_f = lambda r: (
        f'=IF(AND({_WAVES}{r}>=2,{_SPAN}{r}<={pmax},{_RATIO}{r}<>"",'
        f'{_RATIO}{r}<={ratiocap}),"Y","N")')
    conf_f = lambda r: (
        f'=IF({_CADAPPL}{r}<>"Y","n/a",'
        f'IF(AND({_WAVES}{r}>={strongn},{_RATIO}{r}<=1,{_CV}{r}<>"",'
        f'{_CV}{r}<={cvcap}),"High",'
        f'IF({_WAVES}{r}>={strongn},"Medium","Weak")))')
    elig_f = lambda r: (f'=IF(AND({_ACTIVE}{r}>={multimin},'
                        f'{_TOP1}{r}<={conccut}),"Y","N")')
    # forecast WINDOW (only when cadence applicable): next lull, then a wave.
    fstart_f = lambda r: f'=IF({_CADAPPL}{r}<>"Y","",{_LAST}{r}+{_QGAP}{r})'
    fend_f = lambda r: f'=IF({_CADAPPL}{r}<>"Y","",{_FSTART}{r}+{_MSPAN}{r})'
    timing_f = lambda r: (
        f'=IF(AND({_CADAPPL}{r}="Y",{_FEND}{r}>={asof},'
        f'{_FSTART}{r}<=EDATE({asof},{horizon})),"Y","N")')
    due_f = lambda r: f'=IF(AND({_ELIG}{r}="Y",{_TIMING}{r}="Y"),"Y","N")'
    # naive point-date-in-horizon (no gate) - the measure the gate strips out;
    # surfaced only for the secondary "Ungated timing signal (date only)" row.
    dateonly_f = lambda r: (
        f'=IF(AND({_GAP}{r}>0,{_LAST}{r}+{_GAP}{r}>={asof},'
        f'{_LAST}{r}+{_GAP}{r}<=EDATE({asof},{horizon})),"Y","N")')

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META, _DATE_HDRS))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        prows = sorted((row for row in rows if row[i["program"]] == prog),
                       key=lambda row: -(row[i["dollars_recent"]] or 0))
        for row in prows:
            last = c.write(
                [pname, row[i["piid"]],
                 BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                 active_f, recent_f, top1_f, others_f, last_f,
                 gap_f, waves_f, cv_f, span_f, mspan_f, qgap_f,
                 ratio_f, mode_f, cadappl_f, conf_f, elig_f,
                 fstart_f, fend_f, timing_f, due_f, dateonly_f],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT, S_NUM, S_PCT,
                        S_PCT, S_DATE, S_INT, S_INT, S_NUM,
                        S_INT, S_INT, S_INT, S_NUM, S_DEFAULT,
                        S_CENTER, S_DEFAULT, S_CENTER, S_DATE, S_DATE,
                        S_CENTER, S_CENTER, S_CENTER],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None, None, None,
         f"=SUBTOTAL(109,{_RECENT}{f}:{_RECENT}{last})"] + [None] * 19,
        styles=[S_BOLD] + [S_DEFAULT] * 3 + [S_NUM] + [S_DEFAULT] * 19,
        n_cols=_NCOLS)
    c.blank(2)
    c.write(["Criteria: Shared-lane eligible = active vendors ≥ Assumptions min "
             "AND Top-1 share ≤ cutoff. Cadence applicable = ≥2 discrete waves "
             "(longest span ≤ periodic-max, span/cadence ratio ≤ cap); "
             "continuously-active lanes read Continuous sourcing and are screened "
             "on Continuous Sourcing instead. Periodic opening due = eligible AND "
             "the forecast window overlaps the horizon. Ungated timing signal is "
             "the naive point-date test (no gate), shown for contrast. FY26 "
             "partial."],
            styles=[S_DEFAULT])

    def _due_count(program: str, col: str) -> str:
        def rng(c2: str) -> str:
            return f"'{_TAB}'!${c2}${f}:${c2}${last}"
        return (f'COUNTIFS({rng(col_letter(1))},"{program_label(program)}",'
                f'{rng(col)},"Y")')

    def rb_due_count(program: str) -> str:
        # Strict periodic: lanes Periodic opening due (eligible AND cadence-
        # applicable AND window-due) for this program - the headline opening.
        return _due_count(program, _DUE)

    def rb_timing_due_count(program: str) -> str:
        # Broad diagnostic: lanes flagged by the naive Ungated timing signal
        # (point date in horizon, no eligibility / cadence gate).
        return _due_count(program, _DATEONLY)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="PeriodicSourcing", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render), rb_due_count, rb_timing_due_count


(REBUY_TIMING, rb_due_count, rb_timing_due_count) = _make_rebuy_timing()
