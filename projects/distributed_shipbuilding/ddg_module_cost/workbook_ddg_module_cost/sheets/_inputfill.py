"""_inputfill - pale-yellow input-cell fill for THIS workbook (scoped, per-build).

The ICAEW Financial Modelling Code (Layout - "Make inputs easy to find") says to
distinguish input cells "using a defined cell fill colour and/or a cell border,
not just a defined font colour". workbook_core marks hardcoded inputs by blue FONT
only (S_*_INPUT, no fill). Register pale-yellow filled clones of the input styles
ONCE by appending a fill + cellXfs entries to workbook_core.styles at build time,
IN THIS PROCESS ONLY - the same per-build scoping trick _factor.py / _italic.py
use. The append is fully additive: existing FILLS / CELL_XFS indices (and every
S_* constant) are unchanged - xfs reference fills by id, so a new trailing fill
perturbs nothing.

Scope: the editable knobs on the Assumptions tab (anchor FY, structural counts,
module weights). Raw transcribed source values on the data tabs keep blue-font-
only styling.

Exports S_NUM_INPUT_FILL / S_PCT_INPUT_FILL / S_INT_INPUT_FILL (blue input font on a
pale-yellow fill, otherwise identical to S_NUM_INPUT / S_PCT_INPUT / S_INT_INPUT),
plus S_YEAR_INPUT_FILL (General format - a fiscal year with no thousands separator).
"""
from __future__ import annotations

import workbook_core.styles as _styles

# Idempotent registration (guards against a double-import via different paths).
if not getattr(_styles, "_inputfill_registered", None):
    _C_INPUT_FILL = "FFF2CC"   # pale yellow - the editable-input marker
    _fill = len(_styles.FILLS)
    _styles.FILLS.append(
        f'<fill><patternFill patternType="solid">'
        f'<fgColor rgb="FF{_C_INPUT_FILL}"/></patternFill></fill>'
    )
    _num = len(_styles.CELL_XFS)
    _styles.CELL_XFS.append(
        f'<xf numFmtId="164" fontId="3" fillId="{_fill}" borderId="0" xfId="0" '
        'applyNumberFormat="1" applyFont="1" applyFill="1"/>'
    )
    _pct = len(_styles.CELL_XFS)
    _styles.CELL_XFS.append(
        f'<xf numFmtId="165" fontId="6" fillId="{_fill}" borderId="0" xfId="0" '
        'applyNumberFormat="1" applyFont="1" applyFill="1"/>'
    )
    _int = len(_styles.CELL_XFS)
    _styles.CELL_XFS.append(
        f'<xf numFmtId="168" fontId="3" fillId="{_fill}" borderId="0" xfId="0" '
        'applyNumberFormat="1" applyFont="1" applyFill="1"/>'
    )
    # Year (General format, numFmtId 0): a 4-digit fiscal year with NO thousands
    # separator (2025, not 2,025) - blue input font on the pale-yellow fill.
    _year = len(_styles.CELL_XFS)
    _styles.CELL_XFS.append(
        f'<xf numFmtId="0" fontId="3" fillId="{_fill}" borderId="0" xfId="0" '
        'applyFont="1" applyFill="1"/>'
    )
    _styles._inputfill_registered = (_num, _pct, _int, _year)

(S_NUM_INPUT_FILL, S_PCT_INPUT_FILL, S_INT_INPUT_FILL,
 S_YEAR_INPUT_FILL) = _styles._inputfill_registered
