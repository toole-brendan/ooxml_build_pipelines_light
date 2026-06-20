"""docx_core.page_setup - page setup (the <w:sectPr> layer).

A Word document is flow; the only thing that changes per page module is page
setup - size, orientation, margins, columns, and the section-break type. This
module owns that, the way slide layouts own deck geometry and tab metadata owns
workbook structure. Paragraph and table *content* styling lives in styles.py;
page *layout* lives here.

"Word section" is the internal OOXML mechanism (a <w:sectPr>); the author-facing
unit is the PAGE MODULE (docx_core.specs.PageModuleSpec). A page module attaches
one of these PageSetup presets; the packager turns it into the right <w:sectPr>
(the final one as the last child of <w:body>, earlier ones inside a section-break
paragraph). Authors never hand-place sectPr.

Imports docx_core.units and docx_core.rhythm only.
"""
from __future__ import annotations

from dataclasses import dataclass

from docx_core.units import twips_from_in
from docx_core.rhythm import PageMargins, PAGE_MARGINS_REPORT


@dataclass(frozen=True)
class PageSetup:
    """Page setup for one page module. orient="landscape" swaps the emitted
    w:w/w:h so width > height AND sets w:orient (Word trusts the numbers, so both
    must agree). `start` is the section-break type that introduces this module:
    "nextPage" (default) | "continuous" | "oddPage" | "evenPage"."""
    page_w_in: float = 8.5
    page_h_in: float = 11.0
    orient: str = "portrait"            # "portrait" | "landscape"
    margins: PageMargins = PAGE_MARGINS_REPORT
    cols: int = 1
    start: str = "nextPage"             # nextPage | continuous | oddPage | evenPage

    def _pgsz_xml(self) -> str:
        w_in, h_in = self.page_w_in, self.page_h_in
        if self.orient == "landscape":
            # Emit width > height with the orient flag; callers pass portrait
            # dimensions and just flip orient, or pass swapped dims - support both
            # by normalizing here so the long edge is always w:w in landscape.
            w_in, h_in = max(w_in, h_in), min(w_in, h_in)
            return (f'<w:pgSz w:w="{twips_from_in(w_in)}" '
                    f'w:h="{twips_from_in(h_in)}" w:orient="landscape"/>')
        return f'<w:pgSz w:w="{twips_from_in(w_in)}" w:h="{twips_from_in(h_in)}"/>'

    def to_sectpr_xml(self) -> str:
        # Child order is locked: type, pgSz, pgMar, cols, docGrid.
        return (
            "<w:sectPr>"
            + f'<w:type w:val="{self.start}"/>'
            + self._pgsz_xml()
            + self.margins.to_pgmar_xml()
            + f'<w:cols w:space="720" w:num="{self.cols}"/>'
            + '<w:docGrid w:linePitch="360"/>'
            + "</w:sectPr>"
        )


# Presets.
PAGE_PORTRAIT = PageSetup()                              # Letter portrait, 1in margins
PAGE_LANDSCAPE = PageSetup(
    page_w_in=11.0, page_h_in=8.5, orient="landscape",
    margins=PageMargins(top_in=0.6, bottom_in=0.6, left_in=0.55, right_in=0.55),
)
PAGE_PORTRAIT_NARROW = PageSetup(
    margins=PageMargins(top_in=0.6, bottom_in=0.6, left_in=0.65, right_in=0.65),
)

# Slide-mock pages. The deck is 16:9 at 13.333 x 7.5 in (deck_core SLIDE_W/SLIDE_H
# = 12_192_000 / 6_858_000 EMU); a slide-mock page mirrors the SLIDE, not a sheet
# of paper, so the wireframe keeps the deck's true width. See wireframes.py
# (slide_canvas / slide_frame) and doc_guide.md (Slide mocks).
SLIDE_16x9_W_IN = 13.333                                 # deck_core SLIDE_W
SLIDE_16x9_H_IN = 7.5                                    # deck_core SLIDE_H

_SLIDE_MARGINS = PageMargins(top_in=0.3, bottom_in=0.3, left_in=0.3, right_in=0.3,
                             header_in=0.2, footer_in=0.2)

# Exact full-bleed slide page (no room for annotation below the slide).
PAGE_SLIDE_16x9 = PageSetup(
    page_w_in=SLIDE_16x9_W_IN, page_h_in=SLIDE_16x9_H_IN, orient="landscape",
    margins=_SLIDE_MARGINS,
)
# Slide width, taller page: the 16:9 slide region on top, the layout/object
# annotation (slide_frame) below it on the same page. The recommended slide-mock
# page setup.
PAGE_SLIDE_16x9_TALL = PageSetup(
    page_w_in=SLIDE_16x9_W_IN, page_h_in=10.5, orient="landscape",
    margins=_SLIDE_MARGINS,
)
