"""model_wave_cadence - the "Wave Cadence" indicator sheet.

The lane-level read on the award-wave rhythm that the Periodic Sourcing screen
rests on - kept on its OWN tab (cadence quality is a different grain of claim than
the periodic-sourcing screen). One row per (program, PIID x work-type) lane,
sorted by award-wave count, answering:
  - how often do waves recur?      Award waves, Median gap, Gap IQR / CV.
  - are the waves discrete or continuous (does a cadence even apply)?  Longest /
    Median wave span, Span/median gap, Active months %, and the live Sourcing
    mode / Cadence applicable / Cadence confidence verdicts. 90-day single-
    linkage chains a continuously-active lane into one multi-year "wave", so a
    long span (not the gap) is the tell - those lanes read Continuous sourcing
    and are screened on Continuous Sourcing instead of carrying a cadence.
  - are the same vendors / dollar splits recurring (Q2)?  Vendor retention
    (vendors carried wave-to-wave), Allocation similarity (cosine of the dollar-
    share vectors), Top-vendor stable (share of waves with the same top vendor).
  - is the rhythm robust to the clustering window?  Window-stable (does the wave
    count hold at 60 / 90 / 120 days - precomputed, since the workbook can't
    re-cluster live).
  - what is a lane's recurrence tied to (Q3, low confidence)?  Capability
    coherence (do the waves share one capability) feeds a descriptive
    Prod-cycle confidence token (text tokens deferred; see the compute script).

The dispersion / composition / shape signals (median, IQR, cosine, durations
across waves can't be Excel formulas) are blue leaf values from
wb_lane_signals.csv - the documented exception to "aggregations live". The live
derivations are Next expected (Last award + median gap, blank for single-wave
lanes), Span/median gap, and the Sourcing mode / Cadence applicable / Cadence
confidence verdicts (same classifier as Periodic Sourcing, over the blue shape cells
+ the Assumptions §2b knobs).

Built at import via _make_wave_cadence() into a standalone single-table sheet.
No Summary accessor - this is a descriptive companion to Periodic Sourcing.
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
from workbook_award_analysis.sheets._cuts import BUCKET_NAME, PROGRAMS, load
from workbook_award_analysis.sheets.data_lane_signals import ls_cols
from workbook_award_analysis.sheets.data_wave_pairs import wp_cols
from workbook_award_analysis.sheets.summary_inputs import (
    input_periodic_maxdur_cell, input_ratio_cap_cell, input_strong_minwaves_cell,
    input_strong_cvcap_cell,
)
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DATE, W_PCT, W_STATUS, W_RATIO,
    W_DAYS, W_MODE, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_WAVE_CADENCE
from workbook_award_analysis.sheets._yn import S_CENTER

_GROUP = "model"
_TAB = TAB_WAVE_CADENCE
_BANNER = "§1 - Wave cadence"

_META = ["Program", "PIID", "Work Type", "Award waves", "Median gap (days)",
         "Gap IQR (days)", "Gap CV", "Longest span", "Median span",
         "Median quiet gap", "Span/median gap", "Active months %",
         "Cadence applicable", "Sourcing mode", "Cadence confidence",
         "Last award", "Next expected", "Vendor retention",
         "Allocation similarity", "Top-vendor stable", "Capability coherence",
         "Window-stable", "Prod-cycle confidence"]
_NCOLS = len(_META)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_COUNT, W_DAYS, W_DAYS, W_RATIO, W_DAYS,
         W_DAYS, W_DAYS, W_RATIO, W_PCT, W_STATUS, W_MODE, W_STATUS, W_DATE,
         W_DATE, W_PCT, W_PCT, W_PCT, W_PCT, W_STATUS, W_STATUS]
_PIID = col_letter(2)      # C  PIID (Lane Signals / Wave Pairs join key)
_WT = col_letter(3)        # D  Work Type
_WAVES = col_letter(4)     # E  Award waves
_GAP = col_letter(5)       # F  Median gap
_CV = col_letter(7)        # H  Gap CV
_SPAN = col_letter(8)      # I  Longest span
_RATIO = col_letter(11)    # L  Span/median gap
_CADAPPL = col_letter(13)  # N  Cadence applicable
_LAST = col_letter(16)     # Q  Last award
_DATE_HDRS = {"Last award", "Next expected"}


def _make_wave_cadence():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_lane_signals")
    LS = ls_cols()
    WP = wp_cols()
    pmax = input_periodic_maxdur_cell()
    ratiocap = input_ratio_cap_cell()
    strongn = input_strong_minwaves_cell()
    cvcap = input_strong_cvcap_cell()

    # every shape / composition cell is LIVE off the data leaves, so no hardcoded
    # values sit on this calculation tab. Numeric cadence / shape signals are a
    # SUMIFS into the Lane Signals leaf (a lane is unique by PIID + Work Type, so
    # the sum returns the single value); IQR / CV are blank for <3-wave lanes (no
    # dispersion), matching the leaf. Vendor retention / Allocation similarity are
    # AVERAGEIFS over the Wave Pair Metrics leaf (the lane-level roll-up of the
    # per-pair composition - Python owns the cosine, the workbook owns the mean);
    # Window-stable / Prod-cycle confidence are an XLOOKUP of the leaf verdict.
    def crit(r):                              # join into Lane Signals (one row/lane)
        return f'{LS["piid"]},{_PIID}{r},{LS["wt"]},{_WT}{r}'

    def critWP(r):                            # join into Wave Pairs (many rows/lane)
        return f'{WP["piid"]},{_PIID}{r},{WP["wt"]},{_WT}{r}'

    waves_f = lambda r: f'=SUMIFS({LS["waves"]},{crit(r)})'
    gap_f = lambda r: f'=SUMIFS({LS["gap"]},{crit(r)})'
    iqr_f = lambda r: f'=IF({_WAVES}{r}<3,"",SUMIFS({LS["iqr"]},{crit(r)}))'
    cv_f = lambda r: f'=IF({_WAVES}{r}<3,"",SUMIFS({LS["cv"]},{crit(r)}))'
    span_f = lambda r: f'=SUMIFS({LS["span"]},{crit(r)})'
    mspan_f = lambda r: f'=SUMIFS({LS["mspan"]},{crit(r)})'
    qgap_f = lambda r: f'=SUMIFS({LS["qgap"]},{crit(r)})'
    amonths_f = lambda r: f'=SUMIFS({LS["amonths"]},{crit(r)})'
    last_f = lambda r: f'=SUMIFS({LS["last"]},{crit(r)})'
    retention_f = lambda r: f'=IFERROR(AVERAGEIFS({WP["retention"]},{critWP(r)}),"")'
    alloc_f = lambda r: f'=IFERROR(AVERAGEIFS({WP["alloc"]},{critWP(r)}),"")'
    topstable_f = lambda r: f'=SUMIFS({LS["topstable"]},{crit(r)})'
    capcoh_f = lambda r: f'=SUMIFS({LS["capcoh"]},{crit(r)})'
    wstable_f = lambda r: (f'=_xlfn.XLOOKUP({_PIID}{r}&"|"&{_WT}{r},'
                           f'{LS["key"]},{LS["wstable"]},"")')
    prodconf_f = lambda r: (f'=_xlfn.XLOOKUP({_PIID}{r}&"|"&{_WT}{r},'
                            f'{LS["key"]},{LS["confidence"]},"")')

    # span/median gap, cadence-applicability + sourcing-mode verdicts (live; same
    # classifier as Periodic Sourcing). Next expected = last award + median wave gap;
    # blank for single-wave lanes (median gap = 0).
    ratio_f = lambda r: f'=IF({_GAP}{r}=0,"",{_SPAN}{r}/{_GAP}{r})'
    cadappl_f = lambda r: (
        f'=IF(AND({_WAVES}{r}>=2,{_SPAN}{r}<={pmax},{_RATIO}{r}<>"",'
        f'{_RATIO}{r}<={ratiocap}),"Y","N")')
    mode_f = lambda r: (
        f'=IF(OR({_SPAN}{r}>{pmax},AND({_RATIO}{r}<>"",{_RATIO}{r}>{ratiocap})),'
        f'"Continuous sourcing",'
        f'IF({_WAVES}{r}<2,"Sparse / one-off",'
        f'IF({_WAVES}{r}>={strongn},"Periodic sourcing","Weak periodic")))')
    conf_f = lambda r: (
        f'=IF({_CADAPPL}{r}<>"Y","n/a",'
        f'IF(AND({_WAVES}{r}>={strongn},{_RATIO}{r}<=1,{_CV}{r}<>"",'
        f'{_CV}{r}<={cvcap}),"High",'
        f'IF({_WAVES}{r}>={strongn},"Medium","Weak")))')
    next_f = lambda r: f'=IF({_GAP}{r}=0,"",{_LAST}{r}+{_GAP}{r})'

    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META, _DATE_HDRS))
    f = hdr + 1
    last = hdr
    for prog, pname in PROGRAMS:
        prows = sorted((row for row in rows if row[i["program"]] == prog),
                       key=lambda row: (-(row[i["n_waves"]] or 0), row[i["piid"]]))
        for row in prows:
            last = c.write(
                [pname, row[i["piid"]],
                 BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
                 waves_f, gap_f, iqr_f, cv_f, span_f, mspan_f, qgap_f, ratio_f,
                 amonths_f, cadappl_f, mode_f, conf_f, last_f, next_f,
                 retention_f, alloc_f, topstable_f, capcoh_f,
                 wstable_f, prodconf_f],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT,
                        S_INT, S_INT, S_NUM, S_INT,
                        S_INT, S_INT, S_NUM, S_PCT, S_CENTER,
                        S_DEFAULT, S_DEFAULT, S_DATE, S_DATE, S_PCT,
                        S_PCT, S_PCT, S_PCT, S_CENTER,
                        S_DEFAULT],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total", None, None,
         f"=SUBTOTAL(109,{_WAVES}{f}:{_WAVES}{last})"] + [None] * 19,
        styles=[S_BOLD] + [S_DEFAULT] * 2 + [S_INT] + [S_DEFAULT] * 19,
        n_cols=_NCOLS)
    c.blank(2)
    c.write(["Cadence / composition / shape signals are precomputed (median, IQR, "
             "durations and cross-wave cosine can't be live formulas) and read "
             "LIVE off the Lane Signals / Wave Pair Metrics leaves - nothing is "
             "hardcoded here. Sourcing mode and Cadence applicable read the same "
             "§2b knobs as Periodic Sourcing. Window-stable tests the wave count "
             "at 60 / 90 / 120 days. FY26 partial."],
            styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="WaveCadence", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render)


WAVE_CADENCE = _make_wave_cadence()
