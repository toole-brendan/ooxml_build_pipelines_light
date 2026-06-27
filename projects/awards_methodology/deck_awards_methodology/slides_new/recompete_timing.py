"""recompete_timing — US Defense Market Strategy Kickoff (20260626) deck (20260626), source slide 33.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=3, connector=0, chart=0, table=0, picture=0, custom_geometry=0, chrome_builders=3, clusters=1 (covering 14 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: TODO - labels; sample: Likely window, Operational Commanders, SCN 5 years
_LABELS = [    # (x, y, cx, cy, label, highlight) x14 — highlight = FFFF00 yellow text-highlighter or None
    (0.495, 3.317, 0.827, 3.577, "Likely window", None),
    (2.834, 4.949, 2.956, 0.318, "Operational Commanders", None),
    (2.834, 1.698, 10, 0.317, "SCN 5 years", None),
    (2.834, 2.24, 6, 0.317, "Proc – 3 years", None),
    (2.834, 2.781, 4, 0.317, "RD&TE – 2 years", None),
    (2.834, 4.407, 2.956, 0.318, "Acquisition Authority", None),
    (2.834, 5.492, 2.956, 0.318, "Contract Vehicle A", None),
    (2.834, 6.034, 2.956, 0.318, "Contract Vehicle B", None),
    (2.834, 6.576, 2.956, 0.318, "Contract Vehicle C", None),
    (1.419, 3.317, 1.204, 0.866, "FYDP ", None),
    (2.834, 3.323, 2.956, 0.318, "AAA", "FFFF00"),
    (2.834, 3.865, 2.956, 0.318, "AAA", "FFFF00"),
    (9.045, 2.261, 3.789, 0.867, "Obligation %s ", "FFFF00"),
    (1.428, 5.485, 1.204, 1.408, "Contract Vehicle", None),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(prelim_chip())
    out.append(title_placeholder("Recompete Timing", "…"))
    for _x, _y, _cx, _cy, _t, _hl in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(12), bold=True, italic=True, underline=True, color=BLACK, highlight=_hl, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 21", IN(0.495), IN(1.676), IN(2.128), IN(1.416), [paragraph([run("Upper bound: ", size=PT(12), bold=True, italic=True, underline=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Color of Money Obligation Period", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 34", IN(9.045), IN(3.865), IN(3.789), IN(3.029), [paragraph([run("Does this apply to contracts whose last delivery date has elapsed? ", size=PT(12), bold=True, italic=True, color=BLACK, highlight="FFFF00", font=FONT)], align="ctr", line_spacing=100000), paragraph([], align="ctr", line_spacing=100000), paragraph([run("What about contracts whose delivery dates have not? ", size=PT(12), bold=True, italic=True, color=BLACK, highlight="FFFF00", font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 35", IN(1.419), IN(4.407), IN(1.204), IN(0.866), [paragraph([run("Customer", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000), paragraph([run("Intel", size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=19050, anchor="ctr"))
    return "".join(out)


def render() -> str:
    return slide(_body())
