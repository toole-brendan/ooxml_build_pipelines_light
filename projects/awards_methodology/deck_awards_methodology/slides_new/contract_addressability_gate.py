"""contract_addressability_gate — Awards Analysis Market Timing vPrelim deck, source slide 1.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=8, connector=9, chart=0, table=0, picture=0, custom_geometry=0, chrome_builders=3, clusters=3 (covering 13 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_NODE_H = IN(0.641)
_NODE2_W, _NODE2_H = IN(0.7), IN(0.25)

# ── the four decision gates (big white boxes, painted UNDER the connectors) ──
# local_meaning: TODO - flow nodes; sample: Does the requirement recur?, Can we compete?, Is there budget alignment?
_FLOW_NODES = [    # (x, y, cx, label) x4
    (0.512, 1.457, 2.956, "Does the requirement recur?"),
    (2.748, 2.547, 2.956, "Can we compete?"),
    (5.029, 3.638, 2.956, "Is there budget alignment?"),
    (7.34, 4.54, 2.957, "Can the opportunity be shaped?"),
]


def _verdict(n: int, x: float, y: float, fill: str, line: str, label: str, size=PT(9)) -> str:
    """A small Yes/No/Likely verdict chip — painted ON TOP of the connectors it sits on."""
    return text_box(n, "Verdict Chip", IN(x), IN(y), _NODE2_W, _NODE2_H,
                    [paragraph([run(label, size=size, bold=True, font=FONT)], align="ctr", line_spacing=100000)],
                    fill=fill, line_color=line, anchor="ctr", l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144)


def _evidence(n: int, x: float, y: float, cx: float, cy: float, label: str) -> str:
    """A white, borderless evidence caption (8pt italic DK) — painted ON TOP of the connectors."""
    return text_box(n, "Evidence Chip", IN(x), IN(y), IN(cx), IN(cy),
                    [paragraph([run(label, size=PT(8), italic=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)],
                    fill=WHITE, line_color="none", anchor="ctr", l_ins=36576, t_ins=18288, r_ins=36576, b_ins=18288)


def _body() -> str:
    # Shapes are emitted in the source slide's z-order: the decision gates and
    # bands sit at the bottom, the connectors paint over them, and the small
    # verdict/evidence chips paint last so they mask the lines they sit on.
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(prelim_chip())
    out.append(title_placeholder("Contract Addressability", "A recompete opportunity becomes actionable when demand recurs, access exists, and funding is executable."))
    for _x, _y, _cx, _t in _FLOW_NODES:
        out.append(text_box(n(), "Decision Gate", IN(_x), IN(_y), IN(_cx), _NODE_H, [paragraph([run(_t, size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", space_after=80, line_spacing=100000)], fill=WHITE, line_color=BLACK, line_width=19050, anchor="ctr", l_ins=45720, t_ins=36576, r_ins=45720, b_ins=36576))
    out.append(text_box(n(), "Non Addressable Band", IN(0.495), IN(5.818), IN(7.87), IN(0.552), [paragraph([run("Non-addressable", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="808080", anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(text_box(n(), "Output Note", IN(8.82), IN(6.185), IN(3.79), IN(0.185), [paragraph([run("Direct recompete  •  vehicle on-ramp  •  prime / holder route", size=PT(7.2), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Timing Handoff", IN(9.018), IN(6.596), IN(3.4), IN(0.4), [paragraph([run("Determine recompete timing, outlook & pathway", size=PT(10), bold=True, font=FONT), line_break(), run("see following page for timing estimation", size=PT(8), italic=True, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=BLACK, anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(connector(n(), "Addressable to Timing", IN(10.718), IN(6.302), IN(0), IN(0.294), color=BLACK, width=12700, arrow=True))
    out.append(text_box(n(), "Addressable Band", IN(8.602), IN(5.818), IN(4.232), IN(0.552), [paragraph([run("Addressable", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="223E59", line_color="223E59", anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    # connectors + the verdict/evidence chips that sit on them, in source z-order
    out.append(connector(n(), "Connector: Elbow 14", IN(3.468), IN(1.778), IN(0.758), IN(0.77), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(_verdict(n(), 3.873, 2.14, "D1E8DD", "1B8A57", "Yes", size=PT(9.2)))
    out.append(connector(n(), "Straight Arrow Connector 20", IN(1.98), IN(2.098), IN(0.01), IN(3.72), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(_verdict(n(), 1.659, 3.422, "F2CCCC", "C00000", "No", size=PT(9.2)))
    out.append(connector(n(), "Straight Arrow Connector 27", IN(4.226), IN(3.188), IN(0.002), IN(2.63), color=BLACK, width=12700, arrow=True))
    out.append(connector(n(), "Connector: Elbow 29", IN(5.713), IN(2.854), IN(0.794), IN(0.784), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(_verdict(n(), 6.166, 3.207, "D1E8DD", "1B8A57", "Yes"))
    out.append(connector(n(), "Connector: Elbow 32", IN(7.985), IN(3.958), IN(2.733), IN(1.86), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Connector: Elbow 35", IN(6.633), IN(4.153), IN(0.582), IN(0.834), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_h=True, rot=16200000))
    out.append(_evidence(n(), 3.426, 3.566, 1.53, 0.23, "Holder-gated / Incumbent-led"))
    out.append(connector(n(), "Straight Arrow Connector 43", IN(9.602), IN(5.177), IN(0.01), IN(0.641), color=BLACK, width=12700, arrow=True))
    out.append(_verdict(n(), 6.157, 4.49, "F2CCCC", "C00000", "No"))
    out.append(_verdict(n(), 9.58, 3.833, "D1E8DD", "1B8A57", "Yes"))
    out.append(_verdict(n(), 3.876, 4.054, "F2CCCC", "C00000", "No"))
    out.append(connector(n(), "Straight Arrow Connector 47", IN(7.927), IN(5.177), IN(0.002), IN(0.641), color=BLACK, width=12700, arrow=True))
    out.append(_evidence(n(), 1.34, 2.747, 1.3, 0.2, "One-time"))
    out.append(_evidence(n(), 5.866, 2.945, 1.3, 0.17, "Open competition"))
    out.append(_evidence(n(), 3.503, 1.87, 1.5, 0.2, "FYDP / recurring obligations"))
    out.append(_verdict(n(), 9.252, 5.334, "D1E8DD", "1B8A57", "Likely"))
    out.append(_evidence(n(), 8.43, 3.808, 0.9, 0.3, "Requested appropriations"))
    out.append(_verdict(n(), 7.569, 5.334, "F2CCCC", "C00000", "Not likely"))
    return "".join(out)


def render() -> str:
    return slide(_body())
