"""docx_core.units - WordprocessingML measurement conversions.

Word geometry is not one unit. Page size, margins, indents and table widths are
in twips (1/1440 inch, a.k.a. dxa); font size is in half-points; line spacing
with lineRule="auto" is in 240ths of a line. These tiny converters are the one
place those factors live, so rhythm.py / sections.py / styles.py never inline a
magic 20 or 1440.

Pure functions, no dependency on the rest of docx_core (cheap, cycle-free).
"""
from __future__ import annotations


def twips_from_pt(pt: float) -> int:
    """Twips from points: 20 twips per point (w:spacing before/after, w:sz*10…)."""
    return int(round(pt * 20))


def twips_from_in(inches: float) -> int:
    """Twips (dxa) from inches: 1440 twips per inch (w:pgSz, w:pgMar, w:ind…)."""
    return int(round(inches * 1440))


def line_auto(multiplier: float) -> int:
    """w:spacing w:line for lineRule="auto": 240 = single, 276 = 1.15, 360 = 1.5."""
    return int(round(multiplier * 240))


# English Metric Units: the unit DrawingML geometry uses (wp:extent, a:off/a:ext,
# a:ln widths). 914_400 per inch, 12_700 per point. The wireframe layer converts
# inches/points to EMU through these.
EMU_PER_IN = 914_400
EMU_PER_PT = 12_700


def emu_from_in(inches: float) -> int:
    """EMU from inches (DrawingML geometry): 914_400 per inch."""
    return int(round(inches * EMU_PER_IN))


def emu_from_pt(pt: float) -> int:
    """EMU from points (line widths, font-derived sizes): 12_700 per point."""
    return int(round(pt * EMU_PER_PT))
