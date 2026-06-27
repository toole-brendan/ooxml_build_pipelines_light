"""recompete_timing_updated — Strategic Contracts deck, variables-of-timing exhibit.

EXHIBIT — "Recompete Timing": the variables that set and move the recompete
window. Color of money caps the latest feasible award (the upper bound); award
type fixes the governing-date anchor; and a handful of acquisition variables
stretch or compress the window in between. The output is an inferred window, not
a database field. This is the *drivers* view — companion to, not a duplicate of,
the two window-construction process slides (which carry the back-solve procedure).

DESIGN NOTES
  • Keeps the prior wireframe format: color-of-money bars (upper bound) up top, a
    left-edge likely-window output bracket, a spine + rows method stack, and
    right-side reference cards.
  • Color of money is presented as the upper-bound variable — the latest feasible
    award for a given FY's money — not the primary timing clock.
  • The middle stack is the playbook's driver set, grouped by direction of effect:
    variables that pull capture earlier vs. variables that push the opening later.
  • The lower-right card is reframed from "how to treat the governing date" into
    the edge cases where that date misleads or moves the expected timeline.
  • Qualitative throughout — no PALT / lead-time figures asserted on-slide.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    connector,
    line_break,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_2, GRAY_3, GRAY_4, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# Local palette drawn from repeated project colors.
SECTION_NAVY = "223E59"
MID_NAVY = "364D6E"
BLUE = "447BB2"
LIGHT_BLUE = "CEDDEC"
TEAL = "007770"
GREEN = "1B8A57"
PURPLE = "7030A0"
AMBER = "FFC000"
RED = "C00000"
RULE_GRAY = "808080"
PALE_NOTE = "F7F9FB"


# ── layout anchors ───────────────────────────────────────────────────────────
_SPINE_X = IN(1.419)
_MAIN_X = IN(2.834)
_MAIN_W = IN(5.98)
_RIGHT_X = IN(9.045)
_RIGHT_W = IN(3.789)
_MONEY_H = IN(0.38)
_VAR_CARD_W = IN(3.52)


# ── upper-bound color-of-money bars (length = obligation availability) ─────────
_MONEY_ROWS = [
    (2.834, 1.698, 10.000, TEAL,   "SCN", "5-year obligation availability"),
    (2.834, 2.240,  6.000, BLUE,   "Procurement", "3-year obligation availability"),
    (2.834, 2.781,  4.000, PURPLE, "RDT&E", "2-year obligation availability"),
]

# compact color-of-money key, shown in the funding-read card
_MONEY_CHIPS = [
    (9.225,  2.935, 0.78, GRAY_4, "O&M", "1 yr"),
    (10.075, 2.935, 0.78, PURPLE, "RDT&E", "2 yr"),
    (10.925, 2.935, 0.78, BLUE,   "Proc", "3 yr"),
    (11.775, 2.935, 0.78, TEAL,   "SCN", "5 yr"),
]

# anchor: the governing date, fixed by award type
_ANCHOR_ROWS = [
    ("Standalone definitive contract", "ultimate completion + options"),
    ("Task / delivery order", "order completion + order options"),
    ("Parent IDIQ / MAC / GWAC", "last date to order + parent options"),
]

# slim "is the buy forming?" signal cue (kept for timing confidence)
_SIGNAL_ROWS = [
    (GREEN, "Buy is forming", "FYDP / obligations, forecast, sources-sought, draft RFP"),
    (BLUE,  "Customer intel", "acquisition authority, operational sponsor, PM signal"),
]

# variables that move the window, grouped by direction of effect
_EARLIER = [
    "Award type (vehicles slowest)",
    "Dollar value & complexity",
    "Full-and-open competition",
    "Incumbency barriers",
    "Scope changes / bundling",
]
_LATER = [
    "Options exercised",
    "Bridge / sole-source",
    "Protest delay",
    "Date drift (mods move LDO)",
]

# lower-right: edge cases where the governing date misleads or moves
_MISLEADS = [
    (BLACK, "Options remain", "may trigger an option, not a recompete"),
    (RED,   "LDO ≠ performance end", "an ordering deadline, not a PoP"),
    (BLACK, "Parent / child mismatch", "child orders can outlast the parent"),
    (BLACK, "Successor early", "rebuy can land before incumbent LDO"),
    (BLACK, "Retention path", "bridge or in-scope mod can defer it"),
]


def _bullets(items):
    return [
        paragraph([
            run("•  ", size=PT(9), color=SECTION_NAVY, font=FONT),
            run(t, size=PT(9), color=BLACK, font=FONT),
        ], line_spacing=100000, space_after=90)
        for t in items
    ]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(title_placeholder(
        "Recompete Timing",
        "Color of money caps the latest feasible award; award type fixes the anchor; the variables between them stretch or compress the window.",
    ))
    out.append(prelim_chip())

    # ── upper bound: color-of-money definition card (top-left) ──
    out.append(text_box(
        n(), "Upper Bound Card", IN(0.495), IN(1.676), IN(2.128), IN(1.416),
        [
            paragraph([run("Upper bound", size=PT(11.5), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000, space_after=160),
            paragraph([run("Color-of-money obligation period", size=PT(9.6), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000, space_after=160),
            paragraph([run("Latest feasible award that can use a given FY’s money — not period of performance.", size=PT(7.8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=GRAY_1, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=54864, t_ins=36576, r_ins=54864, b_ins=36576,
    ))

    # ── color-of-money bars: length = obligation life ──
    for _x, _y, _cx, _fill, _label, _avail in _MONEY_ROWS:
        out.append(text_box(
            n(), "Color of Money Bar", IN(_x), IN(_y), IN(_cx), _MONEY_H,
            [paragraph([
                run(_label, size=PT(10.5), bold=True, color=WHITE, font=FONT),
                run("  |  ", size=PT(10), color=WHITE, font=FONT),
                run(_avail, size=PT(9.5), color=WHITE, font=FONT),
            ], align="l", line_spacing=100000)],
            fill=_fill, line_color=BLACK, line_width=6350, anchor="ctr",
            l_ins=91440, t_ins=27432, r_ins=91440, b_ins=27432,
        ))
    out.append(text_box(
        n(), "Upper Bound Caption", _MAIN_X, IN(3.185), _MAIN_W, IN(0.15),
        [paragraph([run("Bar length = how long that year’s money stays obligable; the cap moves only if a later appropriation funds the award.", size=PT(7.6), italic=True, color=GRAY_4, font=FONT)], line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    # ── funding-read card (right, upper) ──
    out.append(text_box(
        n(), "Funding Read Card", _RIGHT_X, IN(2.261), _RIGHT_W, IN(0.867),
        [
            paragraph([run("Funding read", size=PT(10), bold=True, color=BLACK, font=FONT)], line_spacing=100000, space_after=110),
            paragraph([run("Which color of money funds it, and how much obligation life remains — that sets the latest feasible award.", size=PT(7.7), color=BLACK, font=FONT)], line_spacing=100000),
        ],
        fill=WHITE, line_color=RULE_GRAY, line_width=12700, anchor="t",
        l_ins=73152, t_ins=36576, r_ins=73152, b_ins=36576,
    ))
    for _x, _y, _cx, _fill, _label, _yrs in _MONEY_CHIPS:
        out.append(text_box(
            n(), "Color Money Chip", IN(_x), IN(_y), IN(_cx), IN(0.145),
            [paragraph([
                run(_label, size=PT(6.3), bold=True, color=WHITE, font=FONT),
                run(" ", size=PT(6.3), color=WHITE, font=FONT),
                run(_yrs, size=PT(6.3), color=WHITE, font=FONT),
            ], align="ctr", line_spacing=100000)],
            fill=_fill, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── left output bracket: likely window ──
    out.append(text_box(
        n(), "Likely Window Output", IN(0.495), IN(3.317), IN(0.827), IN(3.577),
        [
            paragraph([run("LIKELY", size=PT(9.4), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run("WINDOW", size=PT(9.4), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000, space_after=400),
            paragraph([run("FY__–FY__", size=PT(9.0), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000, space_after=320),
            paragraph([run("Inferred", size=PT(7.6), italic=True, color=LIGHT_BLUE, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run("not a database field", size=PT(7.1), italic=True, color=LIGHT_BLUE, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=SECTION_NAVY, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=27432, t_ins=36576, r_ins=27432, b_ins=36576,
    ))

    # ── anchor: governing date by award type ──
    out.append(text_box(
        n(), "Anchor Spine", _SPINE_X, IN(3.317), IN(1.204), IN(1.12),
        [
            paragraph([run("Anchor", size=PT(10.4), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run("by award type", size=PT(7.8), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=GRAY_2, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288,
    ))
    for (_headline, _detail), _y in zip(_ANCHOR_ROWS, (3.317, 3.705, 4.093)):
        out.append(text_box(
            n(), "Anchor Row", _MAIN_X, IN(_y), _MAIN_W, IN(0.355),
            [paragraph([
                run(_headline, size=PT(9.0), bold=True, color=BLACK, font=FONT),
                run("  —  ", size=PT(8.5), color=GRAY_4, font=FONT),
                run(_detail, size=PT(8.0), italic=True, color=DK, font=FONT),
            ], align="l", line_spacing=100000)],
            fill=GRAY_1, line_color=BLACK, line_width=6350, anchor="ctr",
            l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288,
        ))

    # ── slim "is the buy forming?" signal cue ──
    out.append(text_box(
        n(), "Signal Spine", _SPINE_X, IN(4.55), IN(1.204), IN(0.66),
        [
            paragraph([run("Forming?", size=PT(9.6), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
            paragraph([run("signal check", size=PT(7.4), italic=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000),
        ],
        fill=LIGHT_BLUE, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288,
    ))
    for (_fill, _headline, _detail), _y in zip(_SIGNAL_ROWS, (4.55, 4.88)):
        out.append(text_box(
            n(), "Signal Row", _MAIN_X, IN(_y), _MAIN_W, IN(0.30),
            [paragraph([
                run(_headline, size=PT(9.0), bold=True, color=BLACK, font=FONT),
                run("  |  ", size=PT(8.5), color=GRAY_4, font=FONT),
                run(_detail, size=PT(7.8), color=BLACK, font=FONT),
            ], align="l", line_spacing=100000)],
            fill=_fill, fill_alpha=16000, line_color=_fill, line_width=9525,
            anchor="ctr", l_ins=60960, t_ins=18288, r_ins=60960, b_ins=18288,
        ))

    # ── variables that move the window ──
    out.append(text_box(
        n(), "Variables Label", _SPINE_X, IN(5.27), IN(7.22), IN(0.20),
        [paragraph([run("Variables that stretch or compress the window", size=PT(9.0), bold=True, color=BLACK, font=FONT)], line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr", wrap="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    out.append(text_box(
        n(), "Earlier Card", _SPINE_X, IN(5.50), _VAR_CARD_W, IN(1.40),
        [paragraph([])], fill=PALE_NOTE, line_color=RULE_GRAY, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Earlier Header", _SPINE_X, IN(5.50), _VAR_CARD_W, IN(0.30),
        [paragraph([run("Pull earlier  ↑", size=PT(10.5), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
        fill=SECTION_NAVY, line_color=SECTION_NAVY, anchor="ctr",
        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
    ))
    out.append(text_box(
        n(), "Earlier Body", _SPINE_X + IN(0.14), IN(5.86), _VAR_CARD_W - IN(0.28), IN(1.00),
        _bullets(_EARLIER),
        fill=None, line_color="none", anchor="t",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    _later_x = _SPINE_X + _VAR_CARD_W + IN(0.16)
    out.append(text_box(
        n(), "Later Card", _later_x, IN(5.50), _VAR_CARD_W, IN(1.40),
        [paragraph([])], fill=PALE_NOTE, line_color=RULE_GRAY, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Later Header", _later_x, IN(5.50), _VAR_CARD_W, IN(0.30),
        [paragraph([run("Push later  ↓", size=PT(10.5), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
        fill=MID_NAVY, line_color=MID_NAVY, anchor="ctr",
        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
    ))
    out.append(text_box(
        n(), "Later Body", _later_x + IN(0.14), IN(5.86), _VAR_CARD_W - IN(0.28), IN(1.00),
        _bullets(_LATER),
        fill=None, line_color="none", anchor="t",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    # ── lower-right: when the governing date misleads (reframed) ──
    out.append(text_box(
        n(), "Misleads Frame", _RIGHT_X, IN(3.865), _RIGHT_W, IN(3.03),
        [paragraph([])], fill=WHITE, line_color=BLACK, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Misleads Header", _RIGHT_X, IN(3.865), _RIGHT_W, IN(0.34),
        [paragraph([run("When the date misleads", size=PT(11), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
        fill=SECTION_NAVY, line_color=SECTION_NAVY, anchor="ctr",
        l_ins=36576, t_ins=18288, r_ins=36576, b_ins=18288,
    ))
    _mis_paras = [
        paragraph([run("Stress-test the date before trusting it.", size=PT(8.4), italic=True, color=GRAY_4, font=FONT)], line_spacing=100000, space_after=170)
    ]
    for _lc, _label, _detail in _MISLEADS:
        _mis_paras.append(paragraph([
            run(_label + ": ", size=PT(9.2), bold=True, color=_lc, font=FONT),
            run(_detail, size=PT(8.6), color=BLACK, font=FONT),
        ], line_spacing=100000, space_after=150))
    out.append(text_box(
        n(), "Misleads Body", _RIGHT_X + IN(0.14), IN(4.32), _RIGHT_W - IN(0.28), IN(2.50),
        _mis_paras,
        fill=None, line_color="none", anchor="t",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    # ── light flow cues from spine into the rows ──
    out.append(connector(n(), "Anchor Cue", IN(2.63), IN(3.49), IN(0.20), IN(0), color=DK, width=6350, arrow=True))
    out.append(connector(n(), "Signal Cue", IN(2.63), IN(4.70), IN(0.20), IN(0), color=DK, width=6350, arrow=True))

    return "".join(out)


def render() -> str:
    return slide(_body())
