"""data_lane_signals - the "Lane Signals" per-lane signal sheet.

One row per (program, PIID x work-type) lane. MOST columns are now LIVE formulas
derived in the workbook from the raw leaves / spills: wave cadence + dispersion
(award waves, median wave gap, gap IQR / CV from Event Dates + the Award Waves
prior-gap spill), wave shape (longest / median span, median quiet gap), cross-wave
composition (vendor retention, allocation similarity from the Wave Pairs spill),
prior top-1 (Lane Vendor FY), last award (Award Events) and window-stable (Event
Dates 60/90/120 compare).

A RESIDUAL set stays as precomputed blue leaf inputs from wb_lane_signals.csv -
the signals Excel cannot (yet) derive live: active-months %, top-vendor stability,
capability coherence, second-source entry FY, incumbent + whether it is still
active, vendor adds 365d, and prod-cycle confidence. These residuals are baked at
the extract's as-built 90-day wave basis, so unlike the live columns they do NOT
re-evaluate when the Assumptions clustering window changes (a note row on the
sheet flags this). Loaded as the native table LaneSignals.

This sheet exists so the per-lane signals live in ONE auditable DATA leaf instead
of as hardcoded blue cells scattered across the model/"calculation" tabs. The
Periodic Sourcing / Wave Cadence / Continuous Sourcing / Source Diversification
screens read every one of these LIVE - SUMIFS on the numeric columns (a lane is
unique by PIID + Work Type, so the sum returns the single value) and XLOOKUP on
the text columns, keyed on each row's PIID + Work Type (the "Lane key" column is
the PIID|Work-Type concatenation those XLOOKUPs match on).

Built at import via _make_lane_signals() into a standalone single-table sheet.

Promoted accessor (module-level; imported by the four model screens):
  ls_cols() - absolute column ranges (the PIID / Work Type criteria columns, the
              Lane key, and every signal column) for the screens' live formulas.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, ArrayF
from workbook_core.styles import (
    S_DATE, S_DATE_INPUT, S_DEFAULT, S_INT, S_INT_INPUT, S_NUM, S_NUM_INPUT,
    S_PCT, S_PCT_INPUT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, PROGRAMS, date_serial, load,
)
from workbook_award_analysis.sheets.data_event_dates import ed_cols
from workbook_award_analysis.sheets.data_wave_pairs import wp_cols
from workbook_award_analysis.sheets.data_award_events import ae_cols
from workbook_award_analysis.sheets.data_award_waves import aw_cols
from workbook_award_analysis.sheets.data_lane_vendor_fy import lvf_cols
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_LABEL, W_COUNT, W_DAYS, W_RATIO, W_PCT,
    W_STATUS, W_VENDOR, W_DATE, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_LANE_SIGNALS
from workbook_award_analysis.sheets._yn import S_CENTER

_GROUP = "data"
_TAB = TAB_LANE_SIGNALS
_BANNER = "§1 - Lane signals"

# leaf shows the same display labels the screens render, so the screens' XLOOKUPs
# are pass-throughs (no re-casing live). Y/N toggles (centered + green/red CF on
# the screens and here); a blank Incumbent active means "no incumbent" (kept blank,
# not "N"), so the map deliberately has no entry for "".
_YN = {"yes": "Y", "no": "N"}
_CONF = {"high": "High", "medium": "Medium", "low": "Low",
         "not-supportable": "Not-supportable", "n/a": "n/a"}

_HEADERS = ["Program", "PIID", "Work Type", "Lane key", "Award waves",
            "Median wave gap", "Gap IQR", "Gap CV", "Longest span",
            "Median span", "Median quiet gap", "Active months %",
            "Vendor retention", "Allocation similarity", "Top-vendor stable",
            "Capability coherence", "Prior top-1", "2nd-source FY", "Incumbent",
            "Incumbent active", "Vendor adds 365d", "Last award",
            "Window-stable", "Prod-cycle confidence"]
_NCOLS = len(_HEADERS)
_COLS = [W_PROGRAM, W_PIID, W_WORKTYPE, W_LABEL, W_COUNT, W_DAYS, W_DAYS,
         W_RATIO, W_DAYS, W_DAYS, W_DAYS, W_PCT, W_PCT, W_PCT, W_PCT, W_PCT,
         W_PCT, W_STATUS, W_VENDOR, W_STATUS, W_COUNT, W_DATE, W_STATUS,
         W_STATUS]
_DATE_HDRS = {"Last award"}

def _C(i: int) -> str:
    return col_letter(1 + i)


def _fy_label(v):
    return f"FY{int(v) % 100}" if v not in (None, "") else ""


def _make_lane_signals():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_lane_signals")
    E = ed_cols()
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, _DATE_HDRS))
    f, l = hdr + 1, hdr + len(rows)

    def _abs(col: str) -> str:
        return f"'{_TAB}'!${col}${f}:${col}${l}"

    WP, AE, L, AW = wp_cols(), ae_cols(), lvf_cols(), aw_cols()
    P, D = _C(1), _C(2)                       # this row's PIID / Work Type cells
    _lanematch = lambda r: f'({AW["piid"]}={P}{r})*({AW["wt"]}={D}{r})'

    # window-stable is now LIVE: the wave count holds across 60 / 90 / 120-day
    # clustering (counted from Event Dates), keyed on this row's PIID + Work Type.
    def wstable_f(r):
        def n(w):
            return (f'SUMIFS({E[f"start{w}"]},{E["piid"]},{P}{r},'
                    f'{E["wt"]},{D}{r})')
        return f'=IF(AND({n(60)}={n(90)},{n(90)}={n(120)}),"Y","N")'

    # --- live signals over the spill / leaf sheets (proven patterns) ---
    # award waves = wave-start count at the production window (Event Dates).
    awards_f = lambda r: (f'=SUMIFS({E["start90"]},{E["piid"]},{P}{r},'
                          f'{E["wt"]},{D}{r})')
    # median quiet gap = median between-wave gap (Event Dates prior gaps at wave
    # starts; the lane's first date drops out as blank).
    quiet_f = lambda r: ArrayF(
        f'=IFERROR(MEDIAN(IF(({E["piid"]}={P}{r})*({E["wt"]}={D}{r})*'
        f'({E["start90"]}=1),{E["gap"]})),"")')
    # vendor retention / allocation similarity = lane average over Wave Pairs.
    ret_f = lambda r: (f'=IFERROR(AVERAGEIFS({WP["retention"]},{WP["piid"]},{P}{r},'
                       f'{WP["wt"]},{D}{r}),"")')
    alloc_f = lambda r: (f'=IFERROR(AVERAGEIFS({WP["alloc"]},{WP["piid"]},{P}{r},'
                         f'{WP["wt"]},{D}{r}),"")')
    # prior top-1 share = top vendor share in the prior window (Lane Vendor FY).
    prior1_f = lambda r: (
        f'=IF(SUMIFS({L["dol_prior"]},{L["piid"]},{P}{r},{L["wt"]},{D}{r})=0,0,'
        f'_xlfn.MAXIFS({L["dol_prior"]},{L["piid"]},{P}{r},{L["wt"]},{D}{r})/'
        f'SUMIFS({L["dol_prior"]},{L["piid"]},{P}{r},{L["wt"]},{D}{r}))')
    # last award = latest award date in the lane (Award Events).
    last_f = lambda r: (f'=_xlfn.MAXIFS({AE["date"]},{AE["piid"]},{P}{r},'
                        f'{AE["wt"]},{D}{r})')
    # --- cadence dispersion: live over the Award Waves prior-gap / span spill ---
    longest_f = lambda r: (f'=_xlfn.MAXIFS({AW["span"]},{AW["piid"]},{P}{r},'
                           f'{AW["wt"]},{D}{r})')
    mgap_f = lambda r: ArrayF(
        f'=IFERROR(MEDIAN(IF({_lanematch(r)}*({AW["priorgap"]}<>""),'
        f'{AW["priorgap"]})),"")')
    mspan_f = lambda r: ArrayF(
        f'=IFERROR(MEDIAN(IF({_lanematch(r)},{AW["span"]})),"")')
    iqr_f = lambda r: ArrayF(
        f'=IFERROR(_xlfn.LET(_xlpm.g,_xlfn._xlws.FILTER({AW["priorgap"]},'
        f'{_lanematch(r)}*({AW["priorgap"]}<>"")),'
        f'QUARTILE(_xlpm.g,3)-QUARTILE(_xlpm.g,1)),"")')
    cv_f = lambda r: ArrayF(
        f'=IFERROR(_xlfn.LET(_xlpm.g,_xlfn._xlws.FILTER({AW["priorgap"]},'
        f'{_lanematch(r)}*({AW["priorgap"]}<>"")),'
        f'STDEV(_xlpm.g)/AVERAGE(_xlpm.g)),"")')

    for prog, _pname in PROGRAMS:
        prows = sorted((row for row in rows if row[i["program"]] == prog),
                       key=lambda row: (row[i["piid"]], row[i["work_type"]]))
        for row in prows:
            wt_disp = BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]])
            c.write(
                [row[i["program"]], row[i["piid"]], wt_disp,
                 f'{row[i["piid"]]}|{wt_disp}',
                 awards_f, mgap_f,
                 iqr_f, cv_f,
                 longest_f,
                 mspan_f,
                 quiet_f,
                 row[i["active_months_frac"]], ret_f, alloc_f,
                 row[i["top_vendor_stable_frac"]], row[i["capability_coherence"]],
                 prior1_f,
                 _fy_label(row[i["second_source_entry_fy"]]),
                 row[i["incumbent_name"]] or "",
                 _YN.get((row[i["incumbent_still_active"]] or "").lower(), ""),
                 row[i["vendor_adds_last365"]] or 0,
                 last_f,
                 wstable_f,
                 _CONF.get(row[i["prodcycle_confidence"]],
                           row[i["prodcycle_confidence"]])],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT,
                        S_INT, S_INT, S_NUM, S_INT,
                        S_INT, S_INT, S_PCT_INPUT, S_PCT, S_PCT,
                        S_PCT_INPUT, S_PCT_INPUT, S_PCT, S_DEFAULT, S_DEFAULT,
                        S_CENTER, S_INT_INPUT, S_DATE, S_CENTER, S_DEFAULT],
                outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{l}"

    c.blank()
    c.write(["Residual fields (blue inputs) - Active months %, Top-vendor stable, "
             "Capability coherence, 2nd-source FY, Incumbent, Incumbent active, "
             "Vendor adds 365d, Prod-cycle confidence - are precomputed in the "
             "extract at the as-built 90-day wave basis. Unlike the live cadence / "
             "composition columns, they do NOT re-evaluate when the Assumptions "
             "clustering window changes."],
            styles=[S_DEFAULT])

    def ls_cols() -> dict:
        keys = ["prog", "piid", "wt", "key", "waves", "gap", "iqr", "cv",
                "span", "mspan", "qgap", "amonths", "retention", "alloc",
                "topstable", "capcoh", "prior1", "secondfy", "incumbent",
                "incactive", "vadds", "last", "wstable", "confidence"]
        return {k: _abs(_C(n)) for n, k in enumerate(keys)}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="LaneSignals", ref=table_ref, headers=_HEADERS)])

    return SheetEntry(_TAB, _GROUP, render), ls_cols


(LANE_SIGNALS, ls_cols) = _make_lane_signals()
