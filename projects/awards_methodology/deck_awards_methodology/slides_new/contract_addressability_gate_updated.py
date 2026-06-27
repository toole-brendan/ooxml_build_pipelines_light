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
Post-edit: decision-gate nodes were tightened and set on a common vertical step;
elbow paths are drawn as straight orthogonal segments so routing stays clean as
node geometry changes.
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
_NODE_H_IN = 0.56
_NODE_STEP_Y = 1.091
_NODE_TOP_Y = 1.457
_BAND_Y = 5.818
_BRANCH_X = 10.718

_NODE_H = IN(_NODE_H_IN)
_NODE2_W, _NODE2_H = IN(0.7), IN(0.25)
_NODE2_W_IN, _NODE2_H_IN = 0.7, 0.25


def _node_top(i: int) -> float:
    return _NODE_TOP_Y + i * _NODE_STEP_Y


# ── the four decision gates (big white boxes, painted UNDER the connectors) ──
# local_meaning: flow nodes; top y advances by the same _NODE_STEP_Y for each node.
_FLOW_NODES = [    # (x, y, cx, label) x4
    (0.512, _node_top(0), 2.956, "Does the requirement recur?"),
    (2.748, _node_top(1), 2.956, "Can we compete?"),
    (5.029, _node_top(2), 2.956, "Is there budget alignment?"),
    (7.34, _node_top(3), 2.957, "Can the opportunity be shaped?"),
]


def _left(i: int) -> float:
    return _FLOW_NODES[i][0]


def _top(i: int) -> float:
    return _FLOW_NODES[i][1]


def _width(i: int) -> float:
    return _FLOW_NODES[i][2]


def _right(i: int) -> float:
    return _left(i) + _width(i)


def _center_x(i: int) -> float:
    return _left(i) + _width(i) / 2


def _center_y(i: int) -> float:
    return _top(i) + _NODE_H_IN / 2


def _bottom_y(i: int) -> float:
    return _top(i) + _NODE_H_IN


def _hseg(n: int, name: str, x1: float, y: float, x2: float, *, arrow: bool = False) -> str:
    """Horizontal segment of an orthogonal connector path."""
    return connector(n, name, IN(x1), IN(y), IN(x2 - x1), IN(0), color=BLACK, width=12700, arrow=arrow)


def _vseg(n: int, name: str, x: float, y1: float, y2: float, *, arrow: bool = False) -> str:
    """Vertical segment of an orthogonal connector path."""
    return connector(n, name, IN(x), IN(y1), IN(0), IN(y2 - y1), color=BLACK, width=12700, arrow=arrow)


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
        out.append(text_box(n(), "Decision Gate", IN(_x), IN(_y), IN(_cx), _NODE_H, [paragraph([run(_t, size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", space_after=80, line_spacing=100000)], fill=WHITE, line_color=BLACK, line_width=19050, anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(text_box(n(), "Non Addressable Band", IN(0.495), IN(_BAND_Y), IN(7.87), IN(0.552), [paragraph([run("Non-addressable", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="808080", anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(text_box(n(), "Output Note", IN(8.82), IN(6.185), IN(3.79), IN(0.185), [paragraph([run("Direct recompete  •  vehicle on-ramp  •  prime / holder route", size=PT(8), italic=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color="none", anchor="ctr", wrap="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0))
    out.append(text_box(n(), "Timing Handoff", IN(9.018), IN(6.596), IN(3.4), IN(0.4), [paragraph([run("Determine recompete timing, outlook & pathway", size=PT(10), bold=True, font=FONT), line_break(), run("see following page for timing estimation", size=PT(8), italic=True, font=FONT)], align="ctr", line_spacing=100000)], fill=WHITE, line_color=BLACK, anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))
    out.append(_vseg(n(), "Addressable to Timing", _BRANCH_X, 6.302, 6.596, arrow=True))
    out.append(text_box(n(), "Addressable Band", IN(8.602), IN(_BAND_Y), IN(4.232), IN(0.552), [paragraph([run("Addressable", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="223E59", line_color="223E59", anchor="ctr", l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432))

    # connectors + the verdict/evidence chips that sit on them, in source z-order
    # Requirement recurs? — Yes to competition gate; No to non-addressable.
    out.append(_hseg(n(), "Requirement Yes H", _right(0), _center_y(0), _center_x(1)))
    out.append(_vseg(n(), "Requirement Yes V", _center_x(1), _center_y(0), _top(1), arrow=True))
    out.append(_verdict(n(), 3.873, _top(1) - 0.407, "D1E8DD", "1B8A57", "Yes"))
    out.append(_vseg(n(), "Requirement No", _center_x(0), _bottom_y(0), _BAND_Y, arrow=True))
    out.append(_verdict(n(), _center_x(0) - _NODE2_W_IN / 2, 3.422, "F2CCCC", "C00000", "No"))

    # Can we compete? — Yes to budget gate; No to non-addressable.
    out.append(_vseg(n(), "Competition No", _center_x(1), _bottom_y(1), _BAND_Y, arrow=True))
    out.append(_hseg(n(), "Competition Yes H", _right(1), _center_y(1), _center_x(2)))
    out.append(_vseg(n(), "Competition Yes V", _center_x(2), _center_y(1), _top(2), arrow=True))
    out.append(_verdict(n(), 6.166, _top(2) - 0.431, "D1E8DD", "1B8A57", "Yes"))

    # Budget alignment? — Yes directly to addressable; No to shaping gate.
    out.append(_hseg(n(), "Budget Yes H", _right(2), _center_y(2), _BRANCH_X))
    out.append(_vseg(n(), "Budget Yes V", _BRANCH_X, _center_y(2), _BAND_Y, arrow=True))
    out.append(_vseg(n(), "Budget No V", _center_x(2), _bottom_y(2), _center_y(3)))
    out.append(_hseg(n(), "Budget No H", _center_x(2), _center_y(3), _left(3), arrow=True))
    out.append(_evidence(n(), 3.426, 3.566, 1.53, 0.23, "Holder-gated / Incumbent-led"))

    # Can the opportunity be shaped? — Likely to addressable; Not likely to non-addressable.
    out.append(_vseg(n(), "Shaping Likely", 9.602, _bottom_y(3), _BAND_Y, arrow=True))
    out.append(_verdict(n(), _center_x(1) - _NODE2_W_IN / 2, 4.054, "F2CCCC", "C00000", "No"))
    out.append(_verdict(n(), 9.58, _center_y(2) - _NODE2_H_IN / 2, "D1E8DD", "1B8A57", "Yes"))
    out.append(_verdict(n(), _center_x(2) - _NODE2_W_IN / 2, _bottom_y(2) + 0.30, "F2CCCC", "C00000", "No"))
    out.append(_vseg(n(), "Shaping Not Likely", 7.927, _bottom_y(3), _BAND_Y, arrow=True))
    out.append(_evidence(n(), 1.34, 2.747, 1.3, 0.2, "One-time"))
    out.append(_evidence(n(), 5.866, 2.945, 1.3, 0.17, "Open competition"))
    out.append(_evidence(n(), 3.503, _center_y(0) + 0.09, 1.5, 0.2, "FYDP / recurring obligations"))
    out.append(_verdict(n(), 9.252, _bottom_y(3) + 0.16, "D1E8DD", "1B8A57", "Likely"))
    out.append(_evidence(n(), 8.43, _center_y(2) - 0.15, 0.9, 0.3, "Requested appropriations"))
    out.append(_verdict(n(), 7.569, _bottom_y(3) + 0.16, "F2CCCC", "C00000", "Not likely"))
    return "".join(out)


def render() -> str:
    return slide(_body())
