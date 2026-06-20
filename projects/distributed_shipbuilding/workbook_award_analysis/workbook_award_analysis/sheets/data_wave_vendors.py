"""data_wave_vendors - the "Wave Vendors" sheet, now LIVE via dynamic-array spills.

One row per (lane, award wave, vendor), derived live from the raw Award Events
leaf - no precomputed rows. Column B spills the distinct wave-vendor keys
(=SORT(UNIQUE(AwardEvents[Wave-vendor key]))); identity fields are parsed from the
key and the metrics (net $ / gross+ $ / records / first+last date / wave share)
are SUMIFS / COUNTIFS / MINIFS / MAXIFS / XLOOKUP over Award Events keyed on that
spill. Wave share is on the positive-gross basis (vendor gross / wave gross),
matching the old definition. Requires Excel 365 + xl/metadata.xml.

Promoted accessors (module-level):
  wv_cols()  - the ANCHORARRAY spill references (wave key / vendor / uei / gross /
               net) so Award Waves can roll up vendor composition live.
  wv_total_cell / wv_records_total_cell(program) - per-program tie-out cells.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, SpillF
from workbook_core.styles import (
    S_BOLD, S_DATE, S_DEFAULT, S_INT, S_NUM, S_PCT, S_TITLE_SECTION,
    S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import PROGRAMS
from workbook_award_analysis.sheets.data_award_events import ae_cols
from workbook_award_analysis.sheets._widths import (
    W_LABEL, W_PROGRAM, W_PIID, W_WORKTYPE, W_WAVE_SEQ, W_UEI, W_VENDOR,
    W_CAPABILITY, W_DOLLAR, W_COUNT, W_DATE, W_PCT, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_WAVE_VENDORS

_GROUP = "data"
_TAB = TAB_WAVE_VENDORS
_BANNER = "§1 - Wave vendors (live spill)"

_HEADERS = ["WV key", "Wave key", "Program", "PIID", "Work Type", "Wave",
            "Vendor UEI", "Vendor", "Capability", "Wave $M", "Wave $M (gross+)",
            "Records", "First in wave", "Last in wave", "Wave share"]
_NCOLS = len(_HEADERS)
_COLS = [W_LABEL, W_LABEL, W_PROGRAM, W_PIID, W_WORKTYPE, W_WAVE_SEQ, W_UEI,
         W_VENDOR, W_CAPABILITY, W_DOLLAR, W_DOLLAR, W_COUNT, W_DATE, W_DATE,
         W_PCT]
_DATE_HDRS = {"First in wave", "Last in wave"}

def _C(i: int) -> str:
    return col_letter(1 + i)
_ANCHOR = 10
_KEY, _WK, _PROG, _NET, _GROSS = _C(0), _C(1), _C(2), _C(9), _C(10)  # B,C,D,K,L


def _aa(col: str) -> str:
    return f"_xlfn.ANCHORARRAY({col}{_ANCHOR})"


def _make_wave_vendors():
    AE = ae_cols()
    wv, wave_k, dol, pos = AE["wvkey"], AE["wavekey"], AE["dol"], AE["pos"]
    date, uei, vendor, cap = AE["date"], AE["uei"], AE["vendor"], AE["cap"]

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)            # row 2
    c.blank()                                                    # row 3
    rnet = c.write(["Wave-vendor $ / records by program (tie-out)"]
                   + [f'=SUMIFS({_aa(_NET)},{_aa(_PROG)},"{p}")' for p, _ in PROGRAMS]
                   + [None] * (_NCOLS - 1 - len(PROGRAMS)),
                   styles=[S_BOLD] + [S_NUM] * len(PROGRAMS)
                          + [S_DEFAULT] * (_NCOLS - 1 - len(PROGRAMS)))   # row 4
    rrec = c.write([None]
                   + [f'=SUMIFS({_aa(_C(11))},{_aa(_PROG)},"{p}")' for p, _ in PROGRAMS]
                   + [None] * (_NCOLS - 1 - len(PROGRAMS)),
                   styles=[S_DEFAULT] + [S_INT] * len(PROGRAMS)
                          + [S_DEFAULT] * (_NCOLS - 1 - len(PROGRAMS)))   # row 5
    tot_net = {p: (rnet, _C(1 + n)) for n, (p, _) in enumerate(PROGRAMS)}
    tot_rec = {p: (rrec, _C(1 + n)) for n, (p, _) in enumerate(PROGRAMS)}
    c.blank()                                                    # row 6
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)                              # row 7
    c.blank()                                                    # row 8
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, _DATE_HDRS))  # row 9
    assert hdr + 1 == _ANCHOR

    S = SpillF
    aB, aC, aL = _aa(_KEY), _aa(_WK), _aa(_GROSS)
    row = [
        S(f'=_xlfn._xlws.SORT(_xlfn.UNIQUE({wv}))'),                       # WV key
        S(f'=_xlfn.TEXTBEFORE({aB},"|",4)'),                              # Wave key
        S(f'=_xlfn.TEXTBEFORE({aB},"|",1)'),                              # Program
        S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({aB},"|",1),"|",1)'),        # PIID
        S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({aB},"|",2),"|",1)'),        # Work Type
        S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({aB},"|",3),"|",1)+0'),      # Wave
        S(f'=_xlfn.TEXTAFTER({aB},"|",4)'),                               # Vendor UEI
        S(f'=_xlfn.XLOOKUP({aB},{wv},{vendor})'),                         # Vendor
        S(f'=_xlfn.XLOOKUP({aB},{wv},{cap})'),                            # Capability
        S(f'=SUMIFS({dol},{wv},{aB})'),                                   # net $
        S(f'=SUMIFS({pos},{wv},{aB})'),                                   # gross+ $
        S(f'=COUNTIFS({wv},{aB})'),                                       # records
        S(f'=_xlfn.MINIFS({date},{wv},{aB})'),                            # first
        S(f'=_xlfn.MAXIFS({date},{wv},{aB})'),                            # last
        S(f'=IF(SUMIFS({pos},{wave_k},{aC})<=0,0,{aL}/SUMIFS({pos},{wave_k},{aC}))'),  # share
    ]
    styles = [S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT,
              S_DEFAULT, S_DEFAULT, S_DEFAULT, S_NUM, S_NUM, S_INT, S_DATE,
              S_DATE, S_PCT]
    c.write(row, styles=styles)

    def wv_cols() -> dict:
        a = lambda col: f"_xlfn.ANCHORARRAY('{_TAB}'!{col}{_ANCHOR})"
        return {"wavekey": a(_WK), "vendor": a(_C(7)), "uei": a(_C(6)),
                "gross": a(_GROSS), "net": a(_NET)}

    def wv_total_cell(program: str) -> str:
        r, col = tot_net[program]
        return f"'{_TAB}'!{col}{r}"

    def wv_records_total_cell(program: str) -> str:
        r, col = tot_rec[program]
        return f"'{_TAB}'!{col}{r}"

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws)        # spill sheet: NOT a native table

    return (SheetEntry(_TAB, _GROUP, render), wv_cols, wv_total_cell,
            wv_records_total_cell)


(WAVE_VENDORS, wv_cols, wv_total_cell,
 wv_records_total_cell) = _make_wave_vendors()
