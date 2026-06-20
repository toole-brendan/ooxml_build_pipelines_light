"""data_award_events - the "Award Events" raw leaf sheet.

The atomic supplier-award stream: one row per reported FSRS supplier subaward
record (program, PIID, work type, vendor, award date, FY, net $M, report id,
capability), from wb_award_events.csv as the native table AwardEvents. This is
the finest grain in the workbook - the raw records the award waves are clustered
from - so every wave, lane and program total can be traced back to the events
that produced it.

It exists so the Continuous Sourcing screen can compute its trailing-window
activity (last 180 / 365-day $ + records, days-since-last-award) with LIVE
formulas keyed on the Assumptions as-of date, instead of carrying a hardcoded
as-built snapshot: a SUMIFS over the award-date column replaces the old blue
cells, so re-pointing the as-of date re-reads the windows. Every value here is a
blue leaf input (raw record fields Excel cannot derive); the rollups live on the
screens that read it.

Built at import via _make_award_events() into a standalone single-table sheet.

Promoted accessors (module-level):
  ae_cols() - absolute column ranges (program / piid / work type / $ / date)
              for the Continuous Sourcing trailing-window SUMIFS / MAXIFS.
  ae_total_cell / ae_records_total_cell(program) - per-program SUMIF / COUNTIF
              totals (the Checks reconciliation legs; net $ basis).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_DATE_INPUT, S_DEFAULT, S_INT, S_INT_INPUT, S_NUM, S_NUM_INPUT,
    S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import (
    BUCKET_NAME, PROGRAMS, date_serial, load,
)
from workbook_award_analysis.sheets.data_event_dates import ed_cols
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_FAMILY, W_PIID, W_WORKTYPE, W_UEI, W_VENDOR, W_DATE, W_FY_N,
    W_DOLLAR, W_REPORT, W_NAICS4, W_CAPABILITY, W_COUNT, W_LABEL, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_AWARD_EVENTS

_GROUP = "data"
_TAB = TAB_AWARD_EVENTS
_BANNER = "§1 - Award events"

# The last three columns are LIVE: Wave is the 90-day wave number the record falls
# in (count of Event Dates wave-starts in the lane up to this date - so the wave
# tables can be derived live); Wave key concatenates lane + wave for the live
# Award Waves / Wave Vendors spills; Positive $M floors $ at 0 for gross shares.
_HEADERS = ["Program", "Family", "PIID", "Work Type", "Vendor UEI", "Vendor",
            "Award date", "FY", "$M", "Report ID", "NAICS4", "Capability",
            "Wave", "Wave key", "Positive $M", "Wave-vendor key"]
_NCOLS = len(_HEADERS)
_COLS = [W_PROGRAM, W_FAMILY, W_PIID, W_WORKTYPE, W_UEI, W_VENDOR, W_DATE,
         W_FY_N, W_DOLLAR, W_REPORT, W_NAICS4, W_CAPABILITY, W_COUNT, W_LABEL,
         W_DOLLAR, W_LABEL]
_DATE_HDRS = {"Award date"}

def _C(i: int) -> str:
    return col_letter(1 + i)
_PROG_COL, _PIID_COL, _WT_COL = _C(0), _C(2), _C(3)
_UEI_COL, _DATE_COL, _DOL_COL = _C(4), _C(6), _C(8)
_WAVE_COL, _KEY_COL, _POS_COL, _WVKEY_COL = _C(12), _C(13), _C(14), _C(15)
_REC_TOTAL_COL = _C(11)                      # M - per-program COUNTIF lands here


def _make_award_events():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    i, rows = load("wb_award_events")
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, _DATE_HDRS))
    f, l = hdr + 1, hdr + len(rows)
    ED = ed_cols()

    def _abs(col: str) -> str:
        return f"'{_TAB}'!${col}${f}:${col}${l}"

    # Wave @90 = count of Event Dates wave-starts in this lane up to this award
    # date (every record in a wave gets the same number); Wave key + Positive $M
    # are simple cell concatenation / floor. All live, sort-safe.
    wave_f = lambda r: (f'=SUMIFS({ED["start90"]},{ED["piid"]},{_PIID_COL}{r},'
                        f'{ED["wt"]},{_WT_COL}{r},{ED["date"]},"<="&{_DATE_COL}{r})')
    key_f = lambda r: (f'={_PROG_COL}{r}&"|"&{_PIID_COL}{r}&"|"&{_WT_COL}{r}'
                       f'&"|"&{_WAVE_COL}{r}')
    pos_f = lambda r: f'=MAX({_DOL_COL}{r},0)'
    wvkey_f = lambda r: f'={_KEY_COL}{r}&"|"&{_UEI_COL}{r}'

    for row in rows:
        c.write(
            [row[i["program"]], row[i["family"]], row[i["piid"]],
             BUCKET_NAME.get(row[i["work_type"]], row[i["work_type"]]),
             row[i["vendor_uei"]], row[i["vendor_name"]],
             date_serial(row[i["award_date"]]), row[i["fy"]],
             row[i["dollar_m"]] or 0, row[i["report_id"]],
             row[i["naics4"]], row[i["capability"]],
             wave_f, key_f, pos_f, wvkey_f],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT,
                    S_DEFAULT, S_DATE_INPUT, S_INT_INPUT, S_NUM_INPUT,
                    S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT, S_DEFAULT, S_NUM,
                    S_DEFAULT],
            outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{l}"
    c.blank(2)

    # per-program SUMIF $ / COUNTIF records totals - the Checks reconciliation
    # legs (every supplier record lands here, so this ties to every other cut).
    prog_total: dict[str, int] = {}
    for prog, pname in PROGRAMS:
        prog_total[prog] = c.write(
            [f"{pname} supplier total ($M / records, full history)"]
            + [None] * 7
            + [f'=SUMIF(${_PROG_COL}${f}:${_PROG_COL}${l},"{prog}",'
               f'${_DOL_COL}${f}:${_DOL_COL}${l})', None, None,
               f'=COUNTIF(${_PROG_COL}${f}:${_PROG_COL}${l},"{prog}")'],
            styles=[S_DEFAULT] * 8 + [S_NUM, S_DEFAULT, S_DEFAULT, S_INT])

    def ae_cols() -> dict:
        return {"prog": _abs(_PROG_COL), "piid": _abs(_PIID_COL),
                "wt": _abs(_WT_COL), "uei": _abs(_UEI_COL),
                "vendor": _abs(_C(5)), "cap": _abs(_C(11)),
                "dol": _abs(_DOL_COL), "date": _abs(_DATE_COL),
                "wave": _abs(_WAVE_COL), "wavekey": _abs(_KEY_COL),
                "pos": _abs(_POS_COL), "wvkey": _abs(_WVKEY_COL)}

    def ae_total_cell(program: str) -> str:
        return f"'{_TAB}'!{_DOL_COL}{prog_total[program]}"

    def ae_records_total_cell(program: str) -> str:
        return f"'{_TAB}'!{_REC_TOTAL_COL}{prog_total[program]}"

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="AwardEvents", ref=table_ref, headers=_HEADERS)])

    return (SheetEntry(_TAB, _GROUP, render), ae_cols, ae_total_cell,
            ae_records_total_cell)


(AWARD_EVENTS, ae_cols, ae_total_cell,
 ae_records_total_cell) = _make_award_events()
