"""model_continuous_sourcing - the "Continuous Sourcing" indicator sheet.

The companion to Periodic Sourcing for the lanes that are NOT wave-like. 90-day
single-linkage chains a continuously-active lane (awards every few weeks for
years) into one multi-year "wave", so a next-wave DATE is meaningless there - but
the lane is still a contestable, already-split supplier stream. This screen keeps
those lanes visible as ALWAYS-ON openings and reads them on activity +
contestability instead of cadence:
  - is it actively buying now?       Last 180-day / 365-day $M + records,
                                     Days since last award.
  - is the work already split?       Active vendors, Top-1 / Others' share.
  - is the base moving?              Prior top-1, Top-1 trend (recent - prior),
                                     Vendor adds (365d).
  - why isn't it wave-like?          Award waves, Longest span, Span/cadence
                                     ratio, Sourcing mode (the live verdict).

One row per (program, PIID x work-type) lane (the same universe as Periodic Sourcing
and Wave Cadence), sorted by recent supplier $. NOTHING is hardcoded on this
calculation tab: the contestability cells (recent $, active vendors, top-1) are
LIVE COUNTIFS / SUMIFS / MAXIFS over the Lane Vendor FY leaf; the wave-shape cells
(award waves, cadence, longest span, prior top-1, vendor adds, capability
coherence) are LIVE SUMIFS into the Lane Signals leaf; the trailing-window
activity cells (last 180/365-day $ + records, days-since) are LIVE SUMIFS /
COUNTIFS / MAXIFS over the raw Award Events leaf, anchored on the Assumptions
as-of date (re-pointing the as-of re-reads the windows - no as-built snapshot);
and Sourcing mode + the Active continuous opening flag are LIVE formulas over
those cells + the Assumptions §2b knobs.

  Active continuous opening = shared (eligible) AND Sourcing mode = "Continuous
      sourcing" AND Recent $M >= materiality AND last-365d $ >= the active floor
      AND (last-365d records >= the min OR last award within the active lookback)
      - the current-activity gate that separates an opening from a quiet lane.

Built at import via _make_continuous_sourcing() into a standalone single-table
sheet.

Promoted accessors (module-level; imported by Summary):
  cont_opening_count(program) - lanes flagged as an Active continuous opening
                                (the headline, current-activity gated).
  cont_lane_count(program)    - the broader structural continuous multi-source
                                lane count (no activity gate; Summary diagnostic).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_NUM, S_PCT,
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
from workbook_award_analysis.sheets.data_award_events import ae_cols
from workbook_award_analysis.sheets.summary_inputs import (
    input_multisource_cell, input_conc_threshold_cell, input_asof_cell,
    input_periodic_maxdur_cell, input_ratio_cap_cell, input_strong_minwaves_cell,
    input_alwayson_materiality_cell, input_active_lookback_cell,
    input_active_minrec_cell, input_active_mindollar_cell,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DOLLAR, W_PCT, W_RATIO, W_DAYS,
    W_MODE, W_STATUS, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_CONTINUOUS_SOURCING
from workbook_award_analysis.sheets._yn import S_CENTER

_GROUP = "model"
_TAB = TAB_CONTINUOUS_SOURCING
_BANNER = "§1 - Continuous sourcing"

_META = ["Program", "PIID", "Work Type", "Recent $M", "Active vendors",
         "Top-1 share", "Others' share", "Prior top-1", "Top-1 trend",
         "Award waves", "Award-wave cadence", "Longest span",
         "Span/cadence ratio", "Last 180d $M", "Last 180d rec", "Last 365d $M",
         "Last 365d rec", "Days since", "Vendor adds 365d",
         "Capability coherence", "Sourcing mode", "Active continuous opening"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_DOLLAR, W_COUNT, W_PCT, W_PCT, W_PCT,
         W_PCT, W_COUNT, W_DAYS, W_DAYS, W_RATIO, W_DOLLAR, W_COUNT, W_DOLLAR,
         W_COUNT, W_DAYS, W_COUNT, W_PCT, W_MODE, W_STATUS]
# within-row column letters (gutter mode: content i -> column 1+i)
_PIID = col_letter(2)     # C
_WT = col_letter(3)       # D
_RECENT = col_letter(4)   # E  Recent $M
_ACTIVE = col_letter(5)   # F  Active vendors
_TOP1 = col_letter(6)     # G  Top-1 share
_PRIOR1 = col_letter(8)   # I  Prior top-1
_WAVES = col_letter(10)   # K  Award waves
_GAP = col_letter(11)     # L  Award-wave cadence
_SPAN = col_letter(12)    # M  Longest span
_RATIO = col_letter(13)   # N  Span/cadence ratio
_D365 = col_letter(16)    # Q  Last 365d $M
_N365 = col_letter(17)    # R  Last 365d rec
_DAYSSINCE = col_letter(18)  # S  Days since
_MODE = col_letter(21)    # V  Sourcing mode
_ALWAYSON = col_letter(22)  # W  Active continuous opening


def _make_continuous_sourcing():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    L = lvf_cols()
    LS = ls_cols()
    AE = ae_cols()
    i, rows = load("wb_lane_signals")
    multimin = input_multisource_cell()
    conccut = input_conc_threshold_cell()
    asof = input_asof_cell()
    pmax = input_periodic_maxdur_cell()
    ratiocap = input_ratio_cap_cell()
    strongn = input_strong_minwaves_cell()
    mater = input_alwayson_materiality_cell()
    actlook = input_active_lookback_cell()
    actrec = input_active_minrec_cell()
    actdol = input_active_mindollar_cell()

    def crit(r):                              # recent-window contestability (LVF)
        return f'{L["piid"]},{_PIID}{r},{L["wt"]},{_WT}{r}'

    def critLS(r):                            # wave-shape signals (Lane Signals)
        return f'{LS["piid"]},{_PIID}{r},{LS["wt"]},{_WT}{r}'

    def critAE(r):                            # raw award stream (Award Events)
        return f'{AE["piid"]},{_PIID}{r},{AE["wt"]},{_WT}{r}'

    recent_f = lambda r: f'=SUMIFS({L["dol_recent"]},{crit(r)})'
    active_f = lambda r: f'=COUNTIFS({crit(r)},{L["rec_recent"]},">0")'
    top1_f = lambda r: (f'=IF({_RECENT}{r}=0,0,'
                        f'_xlfn.MAXIFS({L["dol_recent"]},{crit(r)})/{_RECENT}{r})')
    others_f = lambda r: f'=IF({_RECENT}{r}=0,0,1-{_TOP1}{r})'
    trend_f = lambda r: f'={_TOP1}{r}-{_PRIOR1}{r}'
    # wave-shape cells: live SUMIFS into the Lane Signals leaf (no hardcoded cells).
    prior1_f = lambda r: f'=SUMIFS({LS["prior1"]},{critLS(r)})'
    waves_f = lambda r: f'=SUMIFS({LS["waves"]},{critLS(r)})'
    gap_f = lambda r: f'=SUMIFS({LS["gap"]},{critLS(r)})'
    span_f = lambda r: f'=SUMIFS({LS["span"]},{critLS(r)})'
    vadds_f = lambda r: f'=SUMIFS({LS["vadds"]},{critLS(r)})'
    capcoh_f = lambda r: f'=SUMIFS({LS["capcoh"]},{critLS(r)})'
    # trailing-window activity: LIVE over the raw Award Events leaf, anchored on
    # the Assumptions as-of date (re-pointing the as-of re-reads the windows) -
    # the old as-built snapshot cells are gone.
    d180_f = lambda r: (f'=SUMIFS({AE["dol"]},{critAE(r)},{AE["date"]},'
                        f'">="&({asof}-180),{AE["date"]},"<="&{asof})')
    n180_f = lambda r: (f'=COUNTIFS({critAE(r)},{AE["date"]},'
                        f'">="&({asof}-180),{AE["date"]},"<="&{asof})')
    d365_f = lambda r: (f'=SUMIFS({AE["dol"]},{critAE(r)},{AE["date"]},'
                        f'">="&({asof}-365),{AE["date"]},"<="&{asof})')
    n365_f = lambda r: (f'=COUNTIFS({critAE(r)},{AE["date"]},'
                        f'">="&({asof}-365),{AE["date"]},"<="&{asof})')
    days_since_f = lambda r: (f'=IF(COUNTIFS({critAE(r)})=0,"",'
                              f'{asof}-_xlfn.MAXIFS({AE["date"]},{critAE(r)}))')
    ratio_f = lambda r: f'=IF({_GAP}{r}=0,"",{_SPAN}{r}/{_GAP}{r})'
    mode_f = lambda r: (
        f'=IF(OR({_SPAN}{r}>{pmax},AND({_RATIO}{r}<>"",{_RATIO}{r}>{ratiocap})),'
        f'"Continuous sourcing",'
        f'IF({_WAVES}{r}<2,"Sparse / one-off",'
        f'IF({_WAVES}{r}>={strongn},"Periodic sourcing","Weak periodic")))')
    # active continuous opening = a shared (eligible), continuous, material lane
    # that is STILL buying at the as-of date: net last-365d $ >= the active floor
    # AND (recent records OR a recent last award within the lookback). The last
    # clause is what drops a structurally-continuous lane that has gone quiet.
    alwayson_f = lambda r: (
        f'=IF(AND({_ACTIVE}{r}>={multimin},{_TOP1}{r}<={conccut},'
        f'{_MODE}{r}="Continuous sourcing",{_RECENT}{r}>={mater},'
        f'{_D365}{r}>={actdol},'
        f'OR({_N365}{r}>={actrec},{_DAYSSINCE}{r}<={actlook})),"Y","N")')

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
                 recent_f, active_f, top1_f, others_f,
                 prior1_f, trend_f,
                 waves_f, gap_f, span_f, ratio_f,
                 d180_f, n180_f, d365_f, n365_f, days_since_f, vadds_f,
                 capcoh_f, mode_f, alwayson_f],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM, S_INT, S_PCT,
                        S_PCT, S_PCT, S_PCT, S_INT, S_INT,
                        S_INT, S_NUM, S_NUM, S_INT, S_NUM,
                        S_INT, S_INT, S_INT, S_PCT,
                        S_DEFAULT, S_CENTER],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None, None,
         f"=SUBTOTAL(109,{_RECENT}{f}:{_RECENT}{last})"] + [None] * 18,
        styles=[S_BOLD] + [S_DEFAULT] * 2 + [S_NUM] + [S_DEFAULT] * 18,
        n_cols=_NCOLS)
    c.blank(2)
    c.write(["Active continuous opening = a shared (active vendors ≥ Assumptions "
             "min AND Top-1 share ≤ cutoff), continuous, material (Recent $M ≥ "
             "always-on materiality) lane that is STILL buying at the as-of date "
             "(last-365d $ ≥ active floor AND last-365d records ≥ min OR last "
             "award within the active lookback). Structurally-continuous lanes "
             "that have gone quiet stay visible above but are not flagged. These "
             "are contestable supplier streams, not dated periodic buys - timing "
             "is not forecast. FY26 partial."],
            styles=[S_DEFAULT])

    def _rng(c2: str) -> str:
        return f"'{_TAB}'!${c2}${f}:${c2}${last}"

    def cont_opening_count(program: str) -> str:
        # ACTIVE continuous opening = the Always-on flag (gated on current
        # activity) - the headline.
        return (f'COUNTIFS({_rng(col_letter(1))},"{program_label(program)}",'
                f'{_rng(_ALWAYSON)},"Y")')

    def cont_lane_count(program: str) -> str:
        # STRUCTURAL continuous multi-source lane = shared (eligible), continuous,
        # material - regardless of whether it is still buying now. The broad
        # universe the active-now gate narrows; kept as a Summary diagnostic.
        return (f'COUNTIFS({_rng(col_letter(1))},"{program_label(program)}",'
                f'{_rng(_MODE)},"Continuous sourcing",'
                f'{_rng(_ACTIVE)},">="&{multimin},'
                f'{_rng(_TOP1)},"<="&{conccut},'
                f'{_rng(_RECENT)},">="&{mater})')

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="ContinuousSourcing", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render), cont_opening_count, cont_lane_count


(CONTINUOUS_SOURCING, cont_opening_count,
 cont_lane_count) = _make_continuous_sourcing()
