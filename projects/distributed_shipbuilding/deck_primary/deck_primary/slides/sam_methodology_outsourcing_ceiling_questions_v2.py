"""sam_methodology_outsourcing_ceiling_questions_v2 — deck_primary slide 7 (SAM Methodology / Outsourcing Ceiling).

EXHIBIT — "Outsourcing Ceiling | Discussion questions": a discussion matrix that
pressure-tests the outsourcing-ceiling / headroom logic without exposing any
workbook variable, formula, or cell mechanic. One native table, three columns —
Question area · Question to discuss · Model implication — with a bold header row
(1.5pt rule beneath it) and eight question rows walking the argument from the
overall frame down to constraints + readout. Horizontal rules only, no fills;
the final row drops its bottom border.

CODE MAP (body follows source PAINT ORDER; the section headers mark roles in place):
  • chrome .......... breadcrumb() + prelim_chip() + title_placeholder() (house builders)
  • question matrix . one low-level table() — header trow() + 8 question trow()s;
                      each cell a plain tcell() carrying its bottom-border rule

Re-ported from the deck's own build output by _tools/convert_slide.py (source
slide 13 of the 14-slide build), then hand-annotated for study. The re-port
retired the now-removed house_table primitive in favour of the general
table()/trow()/tcell() primitives; this annotation changed names / comments /
docstring only — NO coordinate, value, colour, or paint-order — so the render is
byte-identical to the raw re-port.

Converter stats: table=1, chrome_builders=3, text_box=0, raw_verbatim=0, dropped=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, table, trow, tcell, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── table-cell layout commentary ──
# table(): col_widths is column-level geometry; trow(h=...) is a MINIMUM row
# height (LibreOffice grows a wrapped row past it — see the
# house-table-row-height-is-a-minimum note). Cells are the plain tcell() helper
# with no fills (the "rule" skin); per-cell borders={"B": ...} draw the
# horizontal rules — 19050 EMU (1.5pt) under the header, 12700 (1pt) between
# question rows, "none" on the last row. size/bold/color/anchor are per-cell.


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # ── chrome ──
    out.append(breadcrumb("SAM Methodology", "Outsourcing Ceiling"))
    out.append(prelim_chip())
    out.append(title_placeholder("Outsourcing Ceiling", "Discussion questions test whether the ceiling logic reflects shipbuilding reality."))
    # ── question matrix — area · question · implication; header + 8 question rows ──
    out.append(table(n(), "sam_methodology_outsourcing_ceiling_questions", IN(0.495), IN(1.993), IN(12.339), IN(3.933), col_widths=[IN(2.275), IN(7.283), IN(2.78)], rows=[
        trow([tcell("Question area", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 19050}}), tcell("Question to discuss", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 19050}}), tcell("Model implication", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 19050}})], h=IN(0.3)),
        trow([tcell("Overall frame", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Is an upper-bound ceiling a fair way to frame the question, separate from current outsourcing?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Confirms the output is an upside boundary, not a current-state estimate.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.6)),
        trow([tcell("Addressable base", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Does Basic Construction capture the controllable build work, or does it exclude important supplier opportunities?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Validates the denominator before comparing classes or sizing headroom.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.433)),
        trow([tcell("Current baseline", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("How reliable is place-of-performance as a floor for work already distributed away from the prime yard?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Calibrates the starting point for the headroom comparison.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.433)),
        trow([tcell("Yard-bound core", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("What work truly cannot leave the yard because of integration, nuclear controls, alignment, test, certification, or yard know-how?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Sets the irreducible core that limits the ceiling.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.433)),
        trow([tcell("Movable work", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Which build tasks can practically move outside the yard, and which are only theoretically movable?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Tests whether distributed labor is realistic capacity relief.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.433)),
        trow([tcell("Package economics", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("When work moves outside the yard, does material usually move with the package, or mainly labor / fabrication?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Translates movable work into supplier-dollar opportunity.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.433)),
        trow([tcell("Program differences", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Where should Virginia, Columbia, and DDG-51 be treated differently: yard, class, block maturity, GFE mix, or supplier base?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}}), tcell("Determines whether one model shape can travel across programs.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": {"color": BLACK, "width": 12700}})], h=IN(0.433)),
        trow([tcell("Constraints + readout", size=PT(10), bold=True, color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": "none"}), tcell("What most limits more outsourcing, and should the gap to the ceiling read as opportunity, capacity headroom, or a screen?", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": "none"}), tcell("Frames feasibility caveats and the external wording.", size=PT(10), color=BLACK, anchor="t", borders={"L": "none", "R": "none", "T": "none", "B": "none"})], h=IN(0.433)),
    ]))
    return "".join(out)


def render() -> str:
    return slide(_body())
