"""recompete_window_simplified — Strategic Contracts deck, replacement slide module.

EXHIBIT — "Finding the Recompete Window": a simplified, left-to-right method for
constructing an actionable recompete window.  The slide reads horizontally:
find the opportunity unit → pick the right timing anchor → back-solve the
calendar → publish the capture / solicitation / award window.  Funding and edge
cases are kept as compact checks below the main flow.

DESIGN NOTES
  • Uses project-source styling: house chrome, compact Arial copy, dark navy
    headers, light-gray / pale-blue method cards, hairline rules, and small
    chip-style keys.
  • Reduces the prior version from five dense process cards plus a long warning
    rail to four process cards and three short check cards.
  • Keeps the key correction from the notes: color of money is a constraint, not
    the main timing driver; last-date-to-order applies to parent vehicles only.
"""
from __future__ import annotations

from pathlib import Path

from deck_core.primitives import (
    slide,
    run,
    paragraph,
    text_box,
    connector,
    breadcrumb,
    title_placeholder,
    prelim_chip,
)
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_2, GRAY_4, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# Local palette drawn from repeated project colors.
SECTION_NAVY = "223E59"
MID_NAVY = "364D6E"
BLUE = "447BB2"
LIGHT_BLUE = "CEDDEC"
TEAL = "007770"
PURPLE = "7030A0"
RULE_GRAY = "808080"
PALE_NOTE = "F7F9FB"
RED = "C00000"


# ── layout anchors ───────────────────────────────────────────────────────────
_FLOW_X, _FLOW_Y = IN(0.495), IN(1.48)
_FLOW_CARD_W, _FLOW_CARD_H = IN(2.78), IN(1.58)
_FLOW_GAP = IN(0.16)
_FLOW_HEADER_H = IN(0.35)
_STEP_BADGE = IN(0.28)

_FORMULA_X, _FORMULA_Y = IN(0.495), IN(3.46)
_FORMULA_W, _FORMULA_H = IN(12.30), IN(0.82)
_FORMULA_NODE_W, _FORMULA_NODE_H = IN(2.05), IN(0.50)
_FORMULA_OP_W = IN(0.30)
_FORMULA_GAP = IN(0.12)

_CHECK_Y, _CHECK_H = IN(4.66), IN(1.25)
_CHECK_GAP = IN(0.18)
_CHECK_W1, _CHECK_W2, _CHECK_W3 = IN(4.10), IN(3.75), IN(4.09)

_RULE_Y, _RULE_H = IN(6.15), IN(0.55)


# local_meaning: four-card horizontal story. Copy is intentionally short so the
# process reads before the viewer studies details.
_FLOW_STEPS = [
    (
        "1",
        "Find the unit",
        [
            ("Standalone contract", ""),
            ("Task / delivery order", ""),
            ("Parent IDIQ / MAC / GWAC", ""),
        ],
        "Unit determines the anchor.",
        GRAY_1,
        BLACK,
    ),
    (
        "2",
        "Pick the anchor",
        [
            ("Completion + options", "contract"),
            ("Order end + options", "order"),
            ("LDO + order velocity", "parent vehicle"),
        ],
        "Anchor gives the endpoint.",
        GRAY_1,
        BLACK,
    ),
    (
        "3",
        "Back-solve",
        [
            ("Transition / protest", "reserve"),
            ("PALT", "solicitation → award"),
            ("Shaping time", "pre-RFP / market-watch"),
        ],
        "Start before the public event.",
        LIGHT_BLUE,
        BLACK,
    ),
    (
        "4",
        "Output window",
        [
            ("Capture start", "FY__–FY__"),
            ("Solicitation", "FY__ / Q__"),
            ("Award target", "FY__ / Q__"),
        ],
        "One actionable view.",
        SECTION_NAVY,
        WHITE,
    ),
]

# local_meaning: formula row that makes the back-solve logic explicit.
_FORMULA_NODES = [
    ("Timing anchor", "forced decision point", DK, WHITE),
    ("Reserve", "transition / protest", GRAY_1, BLACK),
    ("PALT", "solicitation → award", GRAY_1, BLACK),
    ("Shaping", "pre-RFP / market-watch", GRAY_1, BLACK),
    ("Capture start", "actionable window", TEAL, WHITE),
]

# local_meaning: validation chips; these narrow / confirm the window after the
# anchor gives a first-pass date.
_SIGNAL_CHIPS = [
    ("Budget persists", "FYDP / obligations"),
    ("Buy is forming", "forecast / RFI"),
    ("Customer signal", "PM / sponsor"),
    ("History", "prior cycle"),
]

# local_meaning: compact color-of-money key.
_MONEY_CHIPS = [
    ("O&M", "1 yr", GRAY_4),
    ("RDT&E", "2 yr", PURPLE),
    ("Proc.", "3 yr", BLUE),
    ("SCN", "5 yr", TEAL),
]

# local_meaning: only the highest-value edge cases, kept short to avoid a dense
# right-side rule wall.
_TRAPS = [
    ("Options remain", "completion may not force recompete"),
    ("LDO trap", "parent vehicles only"),
    ("Child orders", "may run after parent closes"),
    ("Early successor", "rebuy can appear years ahead"),
]


def _flow_body(items: list[tuple[str, str]], *, color: str) -> list:
    """Three short lines for a method card."""
    paras = []
    for _lead, _detail in items:
        runs = [run(_lead, size=PT(7.8), bold=True, color=color, font=FONT)]
        if _detail:
            runs.extend([
                run("  ", size=PT(7.6), color=color, font=FONT),
                run(_detail, size=PT(7.4), color=color, font=FONT),
            ])
        paras.append(paragraph(runs, line_spacing=100000, space_after=80))
    return paras


def _check_header(title: str, *, color: str = SECTION_NAVY) -> list:
    return [paragraph([run(title, size=PT(8.8), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(title_placeholder(
        "Finding the Recompete Window",
        "Pick the right timing anchor, then back-solve to the capture start window.",
    ))
    out.append(prelim_chip())

    # ── main horizontal flow: arrows first so cards mask line ends ──
    for i in range(3):
        _x = _FLOW_X + (_FLOW_CARD_W + _FLOW_GAP) * i + _FLOW_CARD_W
        out.append(connector(
            n(), "Flow Arrow", _x, _FLOW_Y + IN(0.80), _FLOW_GAP, IN(0),
            color=DK, width=6350, arrow=True,
        ))

    for i, (_num, _hdr, _items, _caption, _fill, _txt) in enumerate(_FLOW_STEPS):
        _x = _FLOW_X + (_FLOW_CARD_W + _FLOW_GAP) * i
        _header_fill = SECTION_NAVY if i < 3 else TEAL
        _line = BLACK if i == 3 else RULE_GRAY

        out.append(text_box(
            n(), "Flow Card", _x, _FLOW_Y, _FLOW_CARD_W, _FLOW_CARD_H,
            [paragraph([])], fill=_fill, line_color=_line, line_width=12700,
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
        out.append(text_box(
            n(), "Flow Card Header", _x, _FLOW_Y, _FLOW_CARD_W, _FLOW_HEADER_H,
            [paragraph([run(_hdr, size=PT(9.0), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_header_fill, line_color=_header_fill, anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))
        out.append(text_box(
            n(), "Step Badge", _x + IN(0.055), _FLOW_Y + IN(0.065), _STEP_BADGE, _STEP_BADGE,
            [paragraph([run(_num, size=PT(8.0), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
            fill=WHITE, line_color=WHITE, prst="ellipse", anchor="ctr",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
        out.append(text_box(
            n(), "Flow Card Body", _x + IN(0.16), _FLOW_Y + IN(0.50), _FLOW_CARD_W - IN(0.32), IN(0.70),
            _flow_body(_items, color=_txt),
            fill=None, line_color="none", anchor="t",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
        out.append(text_box(
            n(), "Flow Card Caption", _x + IN(0.16), _FLOW_Y + IN(1.27), _FLOW_CARD_W - IN(0.32), IN(0.17),
            [paragraph([run(_caption, size=PT(7.1), italic=True, color=_txt if i == 3 else GRAY_4, font=FONT)], align="ctr", line_spacing=100000)],
            fill=None, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── explicit back-solving equation ──
    out.append(text_box(
        n(), "Formula Frame", _FORMULA_X, _FORMULA_Y, _FORMULA_W, _FORMULA_H,
        [paragraph([])], fill=WHITE, line_color=DK, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Formula Label", _FORMULA_X + IN(0.12), _FORMULA_Y + IN(0.08), IN(1.22), IN(0.15),
        [paragraph([run("Back-solving equation", size=PT(7.2), italic=True, color=GRAY_4, font=FONT)], line_spacing=100000)],
        fill=WHITE, line_color="none", anchor="ctr", wrap="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    _node_y = _FORMULA_Y + IN(0.22)
    _x = _FORMULA_X + IN(0.18)
    for i, (_top, _bottom, _fill, _txt) in enumerate(_FORMULA_NODES):
        out.append(text_box(
            n(), "Formula Node", _x, _node_y, _FORMULA_NODE_W, _FORMULA_NODE_H,
            [
                paragraph([run(_top, size=PT(8.2), bold=True, color=_txt, font=FONT)], align="ctr", line_spacing=100000, space_after=40),
                paragraph([run(_bottom, size=PT(6.5), italic=True, color=_txt, font=FONT)], align="ctr", line_spacing=100000),
            ],
            fill=_fill, line_color=BLACK if i in (0, 4) else RULE_GRAY, line_width=6350, anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))
        _x = _x + _FORMULA_NODE_W
        if i < len(_FORMULA_NODES) - 1:
            _op = "−" if i < 3 else "="
            out.append(text_box(
                n(), "Formula Operator", _x + _FORMULA_GAP // 2, _node_y + IN(0.11), _FORMULA_OP_W, IN(0.25),
                [paragraph([run(_op, size=PT(14), bold=True, color=DK, font=FONT)], align="ctr", line_spacing=100000)],
                fill=None, line_color="none", anchor="ctr",
                l_ins=0, t_ins=0, r_ins=0, b_ins=0,
            ))
            _x = _x + _FORMULA_OP_W + _FORMULA_GAP

    # ── check card 1: validation signals ──
    out.append(text_box(
        n(), "Signals Card", IN(0.495), _CHECK_Y, _CHECK_W1, _CHECK_H,
        [paragraph([])], fill=PALE_NOTE, line_color=RULE_GRAY, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Signals Header", IN(0.495), _CHECK_Y, _CHECK_W1, IN(0.30),
        _check_header("Validate that the buy is forming"),
        fill=SECTION_NAVY, line_color=SECTION_NAVY, anchor="ctr",
        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
    ))
    for i, (_label, _detail) in enumerate(_SIGNAL_CHIPS):
        _x = IN(0.68 + (i % 2) * 1.86)
        _y = IN(5.08 + (i // 2) * 0.37)
        out.append(text_box(
            n(), "Signal Chip", _x, _y, IN(1.55), IN(0.24),
            [paragraph([run(_label, size=PT(6.9), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
            fill=WHITE, line_color=RULE_GRAY, line_width=6350, anchor="ctr",
            l_ins=18288, t_ins=9144, r_ins=18288, b_ins=9144,
        ))
        out.append(text_box(
            n(), "Signal Detail", _x, _y + IN(0.22), IN(1.55), IN(0.13),
            [paragraph([run(_detail, size=PT(6.0), italic=True, color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000)],
            fill=None, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── check card 2: funding constraint ──
    _fund_x = IN(0.495) + _CHECK_W1 + _CHECK_GAP
    out.append(text_box(
        n(), "Funding Card", _fund_x, _CHECK_Y, _CHECK_W2, _CHECK_H,
        [paragraph([])], fill=GRAY_1, line_color=RULE_GRAY, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Funding Header", _fund_x, _CHECK_Y, _CHECK_W2, IN(0.30),
        _check_header("Funding check"),
        fill=SECTION_NAVY, line_color=SECTION_NAVY, anchor="ctr",
        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
    ))
    out.append(text_box(
        n(), "Funding Body", _fund_x + IN(0.18), _CHECK_Y + IN(0.43), _CHECK_W2 - IN(0.36), IN(0.26),
        [paragraph([run("Obligation life can constrain the latest feasible award, but is not period of performance.", size=PT(6.9), color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
        fill=None, line_color="none", anchor="ctr",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    for i, (_label, _yrs, _fill) in enumerate(_MONEY_CHIPS):
        out.append(text_box(
            n(), "Color Money Chip", _fund_x + IN(0.31 + i * 0.80), IN(5.56), IN(0.62), IN(0.17),
            [paragraph([
                run(_label, size=PT(5.9), bold=True, color=WHITE, font=FONT),
                run(" ", size=PT(5.9), color=WHITE, font=FONT),
                run(_yrs, size=PT(5.9), color=WHITE, font=FONT),
            ], align="ctr", line_spacing=100000)],
            fill=_fill, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── check card 3: common traps ──
    _trap_x = _fund_x + _CHECK_W2 + _CHECK_GAP
    out.append(text_box(
        n(), "Traps Card", _trap_x, _CHECK_Y, _CHECK_W3, _CHECK_H,
        [paragraph([])], fill=WHITE, line_color=RULE_GRAY, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Traps Header", _trap_x, _CHECK_Y, _CHECK_W3, IN(0.30),
        _check_header("Stress-test the date"),
        fill=SECTION_NAVY, line_color=SECTION_NAVY, anchor="ctr",
        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
    ))
    for i, (_label, _detail) in enumerate(_TRAPS):
        _x = _trap_x + IN(0.20 + (i % 2) * 1.92)
        _y = IN(5.05 + (i // 2) * 0.38)
        out.append(text_box(
            n(), "Trap Line", _x, _y, IN(1.70), IN(0.30),
            [paragraph([
                run(_label + ": ", size=PT(6.7), bold=True, color=RED if _label == "LDO trap" else BLACK, font=FONT),
                run(_detail, size=PT(6.4), color=BLACK, font=FONT),
            ], line_spacing=100000)],
            fill=None, line_color="none", anchor="t",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── bottom decision rule ──
    out.append(text_box(
        n(), "Decision Rule", IN(0.495), _RULE_Y, IN(12.30), _RULE_H,
        [paragraph([
            run("Practical rule: ", size=PT(9.4), bold=True, color=WHITE, font=FONT),
            run("start with the earliest plausible capture date, then tighten as budget, forecast, and customer signals become visible.", size=PT(8.5), color=WHITE, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=MID_NAVY, line_color=MID_NAVY, anchor="ctr",
        l_ins=60960, t_ins=27432, r_ins=60960, b_ins=27432,
    ))

    return "".join(out)


def render() -> str:
    return slide(_body())
