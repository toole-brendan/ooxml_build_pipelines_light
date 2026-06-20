"""_yn - centered Y/N flag style for THIS workbook (scoped, per-build).

The Y/N flag columns render centered. workbook_core ships no center-aligned data
cell style, so we register one ONCE by appending to workbook_core.styles.CELL_XFS
at build time, IN THIS PROCESS ONLY - the same scoping trick lib.py uses for the
tab colors. build_styles_xml() reads CELL_XFS at build time, so appending here (at
sheet import, before packaging) is enough; no workbook_core source change, and
every other pipeline builds in its own process with unchanged style tables.

Exports S_CENTER (a center-aligned clone of S_DEFAULT - the Y/N value style).

NB: these Y/N columns are computed screening FLAGS (read-only formula / leaf
outputs), not editable toggles. Green/red conditional formatting was deliberately
NOT applied - it would impose a good/bad polarity the descriptive flags don't
carry (e.g. "Concentrated" = Y is the flagged condition, not "good").
"""
from __future__ import annotations

import workbook_core.styles as _styles

# Idempotent registration (guards against a double-import via different paths).
if not getattr(_styles, "_yn_registered", None):
    # Center-aligned clone of S_DEFAULT (id 0): same numFmt/font/fill/border,
    # centered both ways, no wrap (workbook standard).
    _s_center = len(_styles.CELL_XFS)
    _styles.CELL_XFS.append(
        '<xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0" '
        'applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>'
    )
    _styles._yn_registered = _s_center

S_CENTER = _styles._yn_registered
