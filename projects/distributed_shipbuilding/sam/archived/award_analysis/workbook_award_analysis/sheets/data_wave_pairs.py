"""data_wave_pairs - the "Wave Pair Metrics" sheet, now LIVE via dynamic spills.

One row per consecutive award-wave PAIR (prior wave -> current wave) in a lane,
derived live from the raw Award Events leaf - the cosine allocation-similarity
that used to be a Python computation is now an in-workbook formula. Column B
spills the distinct "current" wave keys with wave >= 2 (each one pairs with its
wave-1 predecessor); the metrics are BYROW+LAMBDA over Award Events:

  Vendor retention      = share of the current wave's vendors that were also in
                          the prior wave.
  Allocation similarity = cosine of the two waves' positive-$ vendor vectors over
                          the union of their vendors (SUMPRODUCT / SUMSQ).

All over STABLE Award Events ranges (no cross-sheet spill references). Requires
Excel 365 + the package's xl/metadata.xml marker. LET/LAMBDA local names carry the
_xlpm. prefix; SORT/FILTER use _xlfn._xlws, everything else _xlfn.

Promoted accessor (module-level; imported by Lane Signals):
  wp_cols() - ANCHORARRAY spill refs (PIID / Work Type / retention / allocation)
              for the lane-level AVERAGEIFS roll-ups.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet, SpillF
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_PCT, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets.data_award_events import ae_cols
from workbook_award_analysis.sheets._widths import (
    W_LABEL, W_PROGRAM, W_PIID, W_WORKTYPE, W_WAVE_SEQ, W_PCT, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_WAVE_PAIRS

_GROUP = "data"
_TAB = TAB_WAVE_PAIRS
_BANNER = "§1 - Wave pair metrics (live spill)"

_HEADERS = ["Pair key", "Program", "PIID", "Work Type", "Prior wave", "Wave",
            "Vendor retention", "Allocation similarity"]
_NCOLS = len(_HEADERS)
_COLS = [W_LABEL, W_PROGRAM, W_PIID, W_WORKTYPE, W_WAVE_SEQ, W_WAVE_SEQ, W_PCT,
         W_PCT]

def _C(i: int) -> str:
    return col_letter(1 + i)
_ANCHOR = 7
_KEY = _C(0)                                 # B
# prior wave key for a current key ck (lane | wave-1):
_PK = ('_xlfn.TEXTBEFORE(_xlpm.ck,"|",3)&"|"&(_xlfn.TEXTAFTER(_xlpm.ck,"|",3)+0-1)')


def _aa(col: str) -> str:
    return f"_xlfn.ANCHORARRAY({col}{_ANCHOR})"


def _make_wave_pairs():
    AE = ae_cols()
    wk, uei, pos = AE["wavekey"], AE["uei"], AE["pos"]
    aB = _aa(_KEY)

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)            # row 2
    c.blank()                                                    # row 3
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)                              # row 4
    c.blank()                                                    # row 5
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS))      # row 6
    assert hdr + 1 == _ANCHOR

    S = SpillF
    # anchor: distinct current-wave keys with wave >= 2 (the pairs)
    key_f = S(f'=_xlfn.LET(_xlpm.u,_xlfn.UNIQUE({wk}),'
              f'_xlfn._xlws.SORT(_xlfn._xlws.FILTER(_xlpm.u,'
              f'(_xlfn.TEXTAFTER(_xlpm.u,"|",3)+0)>=2)))')
    prog_f = S(f'=_xlfn.TEXTBEFORE({aB},"|",1)')
    piid_f = S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({aB},"|",1),"|",1)')
    wt_f = S(f'=_xlfn.TEXTBEFORE(_xlfn.TEXTAFTER({aB},"|",2),"|",1)')
    pwave_f = S(f'=_xlfn.TEXTAFTER({aB},"|",3)+0-1')
    wave_f = S(f'=_xlfn.TEXTAFTER({aB},"|",3)+0')
    # vendor retention: |cur ∩ pri| / |cur|
    ret_f = S(f'=_xlfn.BYROW({aB},_xlfn.LAMBDA(_xlpm.ck,_xlfn.LET('
              f'_xlpm.pk,{_PK},'
              f'_xlpm.cur,_xlfn.UNIQUE(_xlfn._xlws.FILTER({uei},{wk}=_xlpm.ck)),'
              f'_xlpm.pri,_xlfn.UNIQUE(_xlfn._xlws.FILTER({uei},{wk}=_xlpm.pk)),'
              f'SUM(--ISNUMBER(MATCH(_xlpm.cur,_xlpm.pri,0)))/ROWS(_xlpm.cur))))')
    # allocation similarity: cosine of the positive-$ vendor vectors over the union
    cos_f = S(f'=_xlfn.BYROW({aB},_xlfn.LAMBDA(_xlpm.ck,_xlfn.LET('
              f'_xlpm.pk,{_PK},'
              f'_xlpm.U,_xlfn.UNIQUE(_xlfn._xlws.FILTER({uei},'
              f'ISNUMBER(MATCH({wk},_xlfn.VSTACK(_xlpm.ck,_xlpm.pk),0)))),'
              f'_xlpm.dc,_xlfn.MAP(_xlpm.U,_xlfn.LAMBDA(_xlpm.u,'
              f'SUMIFS({pos},{wk},_xlpm.ck,{uei},_xlpm.u))),'
              f'_xlpm.dp,_xlfn.MAP(_xlpm.U,_xlfn.LAMBDA(_xlpm.u,'
              f'SUMIFS({pos},{wk},_xlpm.pk,{uei},_xlpm.u))),'
              f'IFERROR(SUMPRODUCT(_xlpm.dc,_xlpm.dp)/'
              f'(SQRT(SUMSQ(_xlpm.dc))*SQRT(SUMSQ(_xlpm.dp))),""))))')
    c.write([key_f, prog_f, piid_f, wt_f, pwave_f, wave_f, ret_f, cos_f],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_INT, S_INT,
                    S_PCT, S_PCT])

    def wp_cols() -> dict:
        a = lambda col: f"_xlfn.ANCHORARRAY('{_TAB}'!{col}{_ANCHOR})"
        return {"piid": a(_C(2)), "wt": a(_C(3)),
                "retention": a(_C(6)), "alloc": a(_C(7))}

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws)        # spill sheet: NOT a native table

    return SheetEntry(_TAB, _GROUP, render), wp_cols


(WAVE_PAIRS, wp_cols) = _make_wave_pairs()
