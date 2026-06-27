"""contract_addressability_framework — US Defense Market Strategy Kickoff (20260626) deck (20260626), source slide 32.

Auto-converted from the source .pptx by _tools/convert_slide.py.
Shapes are rebuilt through deck_core primitives.
Shapes are deck_core primitives at the source EMU coordinates; standard chrome
uses the house builders; repeated shape clusters are data tables + loops;
think-cell <a:fld> labels are frozen; <p:pic> images are copied into slides/images/
and wired via IMAGES + picture(); pattern-fill swatches become
text_box(pattern_fill=…) and freeform <a:custGeom> icons become custom_geometry()
over a deduped path constant; think-cell OLE frames (and the EMF chart previews
that sit over bundled charts) are dropped.

Converter stats: text_box=3, connector=9, chart=0, table=0, picture=0, custom_geometry=0, chrome_builders=3, clusters=2 (covering 17 shapes), raw_verbatim=0, dropped=1, frozen_fields=0.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide, run, paragraph, text_box, connector, line_break, breadcrumb, title_placeholder, prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, GRAY_1, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# ── layout anchors (shared coordinates) ──
_LBL_H = IN(0.641)

# ── repeated-shape data tables (each drives a loop in _body) ──
# local_meaning: TODO - labels; sample: Does the Navy need to procure more stuff…?, Who can compete?, Is there budget alignment?
_LABELS = [    # (x, y, cx, label) x4
    (0.495, 1.386, 2.956, "Does the Navy need to procure more stuff…?"),
    (1.974, 2.396, 2.956, "Who can compete?"),
    (3.709, 3.347, 2.956, "Is there budget alignment?"),
    (6.197, 4.325, 2.957, "What is likelihood of shaping?"),
]

# local_meaning: TODO - flow nodes; sample: FYDP / “To Complete” items, Open – 1 liner why, Yes
_FLOW_NODES = [    # (x, y, cx, cy, fill, line, label, fill_alpha, highlight) x13
    #   every verdict/factor box is a 20%-opacity wash (fill_alpha=20000) over a solid
    #   same-colour border (the source's explicit ln): green 1B8A57 / red C00000 / blue
    #   447BB2 (source bg2 × 50% lumMod). The red verdicts also carry an FFFF00 text highlight.
    (4.623, 1.826, 2.356, 0.272, "447BB2", "447BB2", "FYDP / “To Complete” items", 20000, None),
    (6.184, 2.842, 2.356, 0.272, "447BB2", "447BB2", "Open – 1 liner why", 20000, "FFFF00"),
    (3.615, 1.839, 0.859, 0.247, "1B8A57", "1B8A57", "Yes", 20000, None),
    (7.711, 3.339, 2.356, 0.272, "447BB2", "447BB2", "Requested appropriations", 20000, None),
    (1.544, 2.067, 0.859, 0.247, "C00000", "C00000", "No: ", 20000, "FFFF00"),
    (5.019, 2.854, 0.859, 0.247, "1B8A57", "1B8A57", "Yes", 20000, None),
    (6.712, 3.364, 0.859, 0.247, "1B8A57", "1B8A57", "Yes", 20000, None),
    (9.208, 4.325, 0.859, 0.247, "1B8A57", "1B8A57", "Likely", 20000, None),
    (3.022, 3.064, 0.859, 0.247, "C00000", "C00000", "No: ", 20000, "FFFF00"),
    (4.719, 4.044, 0.859, 0.247, "C00000", "C00000", "No: ", 20000, "FFFF00"),
    (7.092, 5.146, 1.143, 0.247, "C00000", "C00000", "Not likely", 20000, "FFFF00"),
    (10.122, 4.325, 2.356, 0.272, "447BB2", "447BB2", "Requested appropriations", 20000, None),
    (2.193, 3.46, 2.356, 0.272, "447BB2", "447BB2", "Incumbents only", 20000, "FFFF00"),
]

def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)   # noqa: E731 - sequential shape ids
    # DROPPED graphicFrame ('think-cell data - do not delete') - think-cell OLE
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(prelim_chip())
    out.append(title_placeholder("Contract Addressability", "…"))
    for _x, _y, _cx, _t in _LABELS:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), _LBL_H, [paragraph([run(_t, size=PT(12), bold=True, italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=19050, anchor="ctr"))
    for _x, _y, _cx, _cy, _fill, _lc, _t, _alpha, _hl in _FLOW_NODES:
        out.append(text_box(n(), "Label", IN(_x), IN(_y), IN(_cx), IN(_cy), [paragraph([run(_t, size=PT(12), italic=True, color=BLACK, highlight=_hl, font=FONT)], align="ctr", line_spacing=100000)], fill=_fill, fill_alpha=_alpha, line_color=_lc, line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 60", IN(0.495), IN(5.818), IN(7.87), IN(0.32), [paragraph([run("Non-addressable", size=PT(12), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=GRAY_1, line_color="808080", line_width=19050, anchor="ctr"))
    out.append(text_box(n(), "Rectangle 64", IN(8.602), IN(5.818), IN(4.232), IN(0.32), [paragraph([run("Addressable", size=PT(12), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)], fill="447BB2", line_color="0E1924", line_width=19050, anchor="ctr"))
    out.append(connector(n(), "Connector: Elbow 83", IN(6.665), IN(3.668), IN(4.053), IN(2.151), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Connector: Elbow 86", IN(9.153), IN(4.646), IN(0.859), IN(1.173), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Straight Arrow Connector 90", IN(1.974), IN(2.026), IN(0), IN(3.792), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(connector(n(), "Straight Arrow Connector 91", IN(3.452), IN(3.037), IN(0), IN(2.781), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(connector(n(), "Connector: Elbow 98", IN(5.363), IN(3.812), IN(0.658), IN(1.01), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_h=True, rot=16200000))
    out.append(connector(n(), "Connector: Elbow 125", IN(3.452), IN(1.706), IN(0.014), IN(0.69), color=BLACK, width=12700, arrow=True, prst="bentConnector4", adj={"adj1": "val 2458071", "adj2": "val 73209"}))
    out.append(connector(n(), "Connector: Elbow 129", IN(4.93), IN(2.717), IN(0.257), IN(0.631), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Straight Arrow Connector 136", IN(7.675), IN(4.966), IN(0), IN(0.852), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(text_box(n(), "Rectangle 148", IN(8.602), IN(6.502), IN(4.233), IN(0.459), [paragraph([run("Determine recompete timing, outlook & pathway", size=PT(12), bold=True, color=BLACK, font=FONT), run(" ", size=PT(12), color=BLACK, font=FONT), line_break(), run("(see following page for timing estimation)", size=PT(12), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)], fill=None, line_color=BLACK, line_width=19050, anchor="ctr"))
    out.append(connector(n(), "Straight Arrow Connector 149", IN(10.718), IN(6.139), IN(0), IN(0.364), color=BLACK, width=12700, arrow=True))
    return "".join(out)


def render() -> str:
    return slide(_body())
