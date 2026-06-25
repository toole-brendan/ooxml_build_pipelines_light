"""data_award_waves - the "Award Waves" sheet, now LIVE via dynamic-array spills.

One row per (program, PIID, work type, award WAVE), DERIVED LIVE from the raw
Award Events leaf - no precomputed wave rows. The whole table spills from a single
anchor row: column B spills the distinct wave keys
(=SORT(UNIQUE(AwardEvents[Wave key]))), and every other column is a dynamic-array
formula over that spill - the identity fields parsed from the key, and the
roll-ups (start / end / span / anchor / records / $ / gross+ $ / wave type) as
MINIFS / MAXIFS / SUMIFS / COUNTIFS and a BYROW median over Award Events keyed on
the wave key. Changing the clustering window on Assumptions re-derives the waves
(the Award Events "Wave" column re-clusters), and this sheet re-spills.

Requires Excel 365 (the spill engine) and the package's xl/metadata.xml marker.
Vendor composition (per-wave vendor list, $, share) lives on the Wave Vendors
spill (its own grain); it is not duplicated here. Deferred on this sheet (not
load-bearing for the model): modal capability, prior-wave gap, prime-base offset.

Promoted accessors (module-level; imported by Checks):
  aw_total_cell / aw_records_total_cell(program) - per-program $ / record totals
      (live SUMIFS over the spilled columns; the reconciliation legs).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, SpillF
from workbook_core.styles import (
    S_BOLD, S_DATE, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import PROGRAMS
from workbook_award_analysis.sheets.data_award_events import ae_cols
from workbook_award_analysis.sheets.summary_inputs import input_periodic_maxdur_cell
from workbook_award_analysis.sheets._widths import (
    W_PROGRAM, W_PIID, W_WORKTYPE, W_WAVE_SEQ, W_DATE, W_COUNT, W_DOLLAR,
    W_MODE, W_LABEL, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_AWARD_WAVES

_GROUP = "data"
_TAB = TAB_AWARD_WAVES
_BANNER = "§1 - Award waves (live spill)"
_CONTINUOUS_SPAN = 730

_HEADERS = ["Wave key", "Program", "PIID", "Work Type", "Wave", "Wave start",
            "Wave end", "Span (days)", "Wave anchor", "Records", "Wave $M",
            "Wave $M (gross+)", "Wave type", "Prior gap (days)"]
_NCOLS = len(_HEADERS)
_COLS = [W_LABEL, W_PROGRAM, W_PIID, W_WORKTYPE, W_WAVE_SEQ, W_DATE, W_DATE,
         W_COUNT, W_DATE, W_COUNT, W_DOLLAR, W_DOLLAR, W_MODE, W_COUNT]
_DATE_HDRS = {"Wave start", "Wave end", "Wave anchor"}

# content index i -> column letter (gutter: B is content 0)
def _C(i: int) -> str:
    return col_letter(1 + i)
# anchor row is fixed by the preamble below (title,blank,net,rec,blank,banner,
# blank,header,anchor) => row 10.
_ANCHOR = 10
_KEY, _PROG, _NET, _REC = _C(0), _C(1), _C(10), _C(9)   # B, C, L, K


def _aa(col: str) -> str:                    # the spill (#) operator
    return f"_xlfn.ANCHORARRAY({col}{_ANCHOR})"


def _make_award_waves():
    AE = ae_cols()
    pmax = input_periodic_maxdur_cell()
    key, date, dol, pos = AE["wavekey"], AE["date"], AE["dol"], AE["pos"]

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)            # row 2
    c.blank()                                                    # row 3
    # per-program tie-out totals (live SUMIFS over the spilled columns below)
    prog_total_net, prog_total_rec = {}, {}
    rnet = c.write(["Wave $ / records by program (tie-out)"]
                   + [f'=SUMIFS({_aa(_NET)},{_aa(_PROG)},"{p}")' for p, _ in PROGRAMS]
                   + [None] * (_NCOLS - 1 - len(PROGRAMS)),
                   styles=[S_BOLD] + [S_NUM] * len(PROGRAMS)
                          + [S_DEFAULT] * (_NCOLS - 1 - len(PROGRAMS)))   # row 4
    rrec = c.write([None]
                   + [f'=SUMIFS({_aa(_REC)},{_aa(_PROG)},"{p}")' for p, _ in PROGRAMS]
                   + [None] * (_NCOLS - 1 - len(PROGRAMS)),
                   styles=[S_DEFAULT] + [S_INT] * len(PROGRAMS)
                          + [S_DEFAULT] * (_NCOLS - 1 - len(PROGRAMS)))   # row 5
    for n, (p, _) in enumerate(PROGRAMS):
        prog_total_net[p] = (rnet, _C(1 + n))
        prog_total_rec[p] = (rrec, _C(1 + n))
    c.blank()                                                    # row 6
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)                              # row 7
    c.blank()                                                    # row 8
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, _DATE_HDRS))  # row 9
    assert hdr + 1 == _ANCHOR, f"anchor row drift: {hdr+1} != {_ANCHOR}"

    # the anchor row: column B spills the distinct wave keys; every other column
    # is a dynamic-array formula over that spill (SpillF -> cm dynamic marker).
    S = SpillF
    row = [
        S(f'=_xlfn._xlws.SORT(_xlfn.UNIQUE({key}))'),                       # Wave key
        S(f'=_xlfn.TEXTBEFORE({_aa(_KEY)},"|")'),                           # Program
        S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({_aa(_KEY)},"|"),"|")'),      # PIID
        S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({_aa(_KEY)},"|",2),"|")'),    # Work Type
        S(f'=_xlfn.TEXTAFTER({_aa(_KEY)},"|",3)+0'),                        # Wave
        S(f'=_xlfn.MINIFS({date},{key},{_aa(_KEY)})'),                      # start
        S(f'=_xlfn.MAXIFS({date},{key},{_aa(_KEY)})'),                      # end
        S(f'={_aa(_C(6))}-{_aa(_C(5))}'),                                   # span
        S(f'=_xlfn.BYROW({_aa(_KEY)},_xlfn.LAMBDA(_xlpm.wkey,'
          f'MEDIAN(IF({key}=_xlpm.wkey,{date}))))'),                        # anchor
        S(f'=COUNTIFS({key},{_aa(_KEY)})'),                                 # records
        S(f'=SUMIFS({dol},{key},{_aa(_KEY)})'),                            # net $
        S(f'=SUMIFS({pos},{key},{_aa(_KEY)})'),                            # gross+ $
        S(f'=IF({_aa(_C(10))}<=0,"Correction-only",'
          f'IF({_aa(_C(7))}>{_CONTINUOUS_SPAN},"Continuous episode",'
          f'IF({_aa(_C(7))}>{pmax},"Extended episode","Clean wave")))'),    # wave type
        # prior gap = this wave anchor - the prior wave's anchor (same lane,
        # wave-1), looked up in this sheet's own spill; blank for wave 1.
        S(f'=IFERROR(IF({_aa(_C(4))}=1,"",{_aa(_C(8))}-_xlfn.XLOOKUP('
          f'{_aa(_C(1))}&"|"&{_aa(_C(2))}&"|"&{_aa(_C(3))}&"|"&({_aa(_C(4))}-1),'
          f'{_aa(_C(0))},{_aa(_C(8))})),"")'),                               # prior gap
    ]
    styles = [S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT, S_DATE,
              S_DATE, S_INT, S_DATE, S_INT, S_NUM, S_NUM, S_DEFAULT, S_INT]
    c.write(row, styles=styles)

    def aw_total_cell(program: str) -> str:
        r, col = prog_total_net[program]
        return f"'{_TAB}'!{col}{r}"

    def aw_records_total_cell(program: str) -> str:
        r, col = prog_total_rec[program]
        return f"'{_TAB}'!{col}{r}"

    def aw_cols() -> dict:
        a = lambda col: f"_xlfn.ANCHORARRAY('{_TAB}'!{col}{_ANCHOR})"
        return {"piid": a(_C(2)), "wt": a(_C(3)), "span": a(_C(7)),
                "anchor": a(_C(8)), "priorgap": a(_C(13))}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws)        # spill sheet: NOT a native table

    return (SheetEntry(_TAB, _GROUP, render), aw_cols, aw_total_cell,
            aw_records_total_cell)


(AWARD_WAVES, aw_cols, aw_total_cell,
 aw_records_total_cell) = _make_award_waves()
