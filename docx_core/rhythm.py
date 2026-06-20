"""docx_core.rhythm - the margins + line/paragraph spacing layer.

Vertical rhythm is a first-class concern, not an ad hoc argument on every
paragraph. This is the DOCX analog of the workbook's row-spacing rhythm and the
deck's body box: pure presets (no OOXML plumbing beyond the two tiny serializers)
that styles.py attaches to paragraph styles and sections.py attaches to page
setup.

  - ParaRhythm  -> the <w:spacing> on a paragraph style (before/after/line).
  - PageMargins -> the <w:pgMar> inside a section's <w:sectPr>.

Authors almost never touch this directly; they pick a named paragraph style (the
rhythm rides on it) or a section preset. Imports only docx_core.units.
"""
from __future__ import annotations

from dataclasses import dataclass

from docx_core.units import twips_from_pt, twips_from_in, line_auto


# ---------------------------------------------------------------------------
# Paragraph rhythm
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ParaRhythm:
    """Spacing for a paragraph style. before/after are in points (converted to
    twips on emit); line is the raw w:line value (use units.line_auto(mult) for
    lineRule="auto") and line_rule is one of "auto" | "atLeast" | "exact"."""
    space_before_pt: float = 0.0
    space_after_pt: float = 6.0
    line: int = 276                     # line_auto(1.15)
    line_rule: str = "auto"

    def to_spacing_xml(self) -> str:
        return (
            f'<w:spacing w:before="{twips_from_pt(self.space_before_pt)}" '
            f'w:after="{twips_from_pt(self.space_after_pt)}" '
            f'w:line="{self.line}" w:lineRule="{self.line_rule}"/>'
        )


# Presets - the house report rhythm. Body is answer-density prose (1.15 line,
# 6pt after); headings get air above and keep-with-next (set on the style).
R_BODY = ParaRhythm(space_after_pt=6, line=line_auto(1.15))
R_TIGHT = ParaRhythm(space_after_pt=0, line=line_auto(1.0))
# List items: single line, only a hair of after-space between items - so a list
# reads as one tight block, NOT as body prose (which carries 6pt after each
# paragraph). Carried by the P_LIST style; every bullet/numbered/outline item
# rides on it (see styles.py / primitives.py), never P_BODY.
R_LIST = ParaRhythm(space_after_pt=2, line=line_auto(1.0))
R_H1 = ParaRhythm(space_before_pt=18, space_after_pt=6, line=line_auto(1.0))
R_H2 = ParaRhythm(space_before_pt=12, space_after_pt=4, line=line_auto(1.0))
R_H3 = ParaRhythm(space_before_pt=10, space_after_pt=4, line=line_auto(1.0))
R_TITLE = ParaRhythm(space_before_pt=0, space_after_pt=12, line=line_auto(1.0))
R_CAPTION = ParaRhythm(space_before_pt=2, space_after_pt=10, line=line_auto(1.0))
R_SOURCE = ParaRhythm(space_before_pt=2, space_after_pt=6, line=line_auto(1.0))


# ---------------------------------------------------------------------------
# Page margins
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class PageMargins:
    """Page margins, in inches (converted to twips on emit). header/footer are
    the distance from the page edge to the header/footer band."""
    top_in: float = 1.0
    bottom_in: float = 1.0
    left_in: float = 1.0
    right_in: float = 1.0
    header_in: float = 0.5
    footer_in: float = 0.5
    gutter_in: float = 0.0

    def to_pgmar_xml(self) -> str:
        return (
            f'<w:pgMar w:top="{twips_from_in(self.top_in)}" '
            f'w:right="{twips_from_in(self.right_in)}" '
            f'w:bottom="{twips_from_in(self.bottom_in)}" '
            f'w:left="{twips_from_in(self.left_in)}" '
            f'w:header="{twips_from_in(self.header_in)}" '
            f'w:footer="{twips_from_in(self.footer_in)}" '
            f'w:gutter="{twips_from_in(self.gutter_in)}"/>'
        )


PAGE_MARGINS_REPORT = PageMargins(top_in=1.0, bottom_in=1.0, left_in=1.0, right_in=1.0)
