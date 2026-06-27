"""recompete_window_updated — Strategic Contracts deck, simplified replacement module.

EXHIBIT — "Finding the Recompete Window": construct the actionable recompete
window by first selecting the correct award-type timing anchor, then working
backward through transition / protest reserve, PALT, and pre-solicitation shaping.
Funding and buyer signals are treated as constraints / validation checks rather
than the primary organizing logic.

DESIGN NOTES
  • Replaces the prior budget-led wireframe with a five-step left-to-right
    recompete-window construction process.
  • Keeps color-of-money as a compact funding constraint, not the hero layer.
  • Renames the prior "governing award date" concept to "timing anchor" because
    the anchor is often a completion date, order end date, or last date to order.
  • Replaces elapsed / unelapsed date rules with practical pitfalls that make
    end dates misleading.
  • Output is made concrete: capture start, expected solicitation, and target
    successor award.
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
_MAIN_X = IN(0.495)
_MAIN_W = IN(9.225)
_RIGHT_X = IN(10.02)
_RIGHT_W = IN(2.815)

_CARD_Y = IN(1.50)
_CARD_W = IN(1.73)
_CARD_H = IN(2.03)
_CARD_GAP = IN(0.145)
_CARD_HEADER_H = IN(0.34)
_STEP_BADGE = IN(0.28)

_FORMULA_Y = IN(3.77)
_FORMULA_H = IN(0.58)
_BOTTOM_Y = IN(4.58)
_BOTTOM_H = IN(1.08)
_DECISION_Y = IN(5.88)
_DECISION_H = IN(0.74)


# local_meaning: five core steps in the recompete-window construction flow.
_PROCESS_STEPS = [
    (
        "1",
        "Identify award type",
        [
            ("Standalone", "definitive contract"),
            ("Task / delivery", "order"),
            ("Parent", "IDIQ / MAC / GWAC"),
        ],
        GRAY_1,
        BLACK,
    ),
    (
        "2",
        "Pick timing anchor",
        [
            ("Definitive", "ultimate completion + options"),
            ("Order", "order completion + order options"),
            ("Parent", "LDO + options + velocity"),
        ],
        GRAY_1,
        BLACK,
    ),
    (
        "3",
        "Work backward",
        [
            ("Subtract", "transition / protest reserve"),
            ("Subtract", "PALT"),
            ("Subtract", "market-watch / shaping time"),
        ],
        LIGHT_BLUE,
        BLACK,
    ),
    (
        "4",
        "Validate signals",
        [
            ("Demand", "FYDP, recurring obligations"),
            ("Buying motion", "forecast, RFI, draft RFP"),
            ("Customer intel", "PM / sponsor signal"),
        ],
        "DDEBF7",
        BLACK,
    ),
    (
        "5",
        "Output window",
        [
            ("Capture", "FY__–FY__"),
            ("Solicitation", "FY__ / Q__"),
            ("Award target", "FY__ / Q__"),
        ],
        SECTION_NAVY,
        WHITE,
    ),
]

# local_meaning: compact color-of-money chips in the funding-constraint card.
_MONEY_CHIPS = [
    ("O&M", "1 yr", GRAY_4),
    ("RDT&E", "2 yr", PURPLE),
    ("Proc.", "3 yr", BLUE),
    ("SCN", "5 yr", TEAL),
]

# local_meaning: factors that stretch or compress the back-solved window.
_WINDOW_FACTORS = [
    "award type",
    "dollar value / complexity",
    "competition strategy",
    "option structure",
    "color of money",
    "protest exposure",
    "scope changes",
    "incumbent barriers",
]

# local_meaning: right-side pitfalls that make the timing anchor misleading.
_PITFALLS = [
    ("Options remain", "Current completion may lead only to option exercise."),
    ("Wrong anchor", "LDO applies only to parent vehicles — not contracts or single orders."),
    ("Parent / child mismatch", "Child orders can perform after parent closes to new orders."),
    ("Successor appears early", "Major vehicles may recompete years before incumbent LDO."),
    ("Date drift", "LDO can move later through options or modifications."),
    ("Hidden competition", "Holder-only order competitions may never appear publicly."),
    ("Incumbent-retention path", "Bridge, logical follow-on, sole-source, or in-scope mod can delay the open event."),
]


def _step_body(label_pairs: list[tuple[str, str]], *, text_color: str) -> list:
    """Builds compact three-line rich text for a process card body."""
    paras = []
    for _lead, _detail in label_pairs:
        paras.append(paragraph([
            run(_lead, size=PT(7.3), bold=True, color=text_color, font=FONT),
            run("  ", size=PT(7.3), color=text_color, font=FONT),
            run(_detail, size=PT(7.1), color=text_color, font=FONT),
        ], line_spacing=100000, space_after=90))
    return paras


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(title_placeholder(
        "Finding the Recompete Window",
        "Start with the correct award-type anchor, then work backward through transition, PALT, and pre-solicitation shaping.",
    ))
    out.append(prelim_chip())

    # ── process connectors: drawn first so cards mask line ends ──
    for i in range(4):
        _x0 = IN(0.495 + (1.73 + 0.145) * i + 1.73)
        out.append(connector(
            n(), "Process Arrow", _x0, IN(2.52), _CARD_GAP, IN(0),
            color=DK, width=6350, arrow=True,
        ))

    # ── five-step horizontal process ──
    for i, (_num, _hdr, _items, _fill, _txt) in enumerate(_PROCESS_STEPS):
        _x = IN(0.495 + (1.73 + 0.145) * i)
        _header_fill = SECTION_NAVY if i < 4 else TEAL
        _header_txt = WHITE
        _line = BLACK if i == 4 else RULE_GRAY

        out.append(text_box(
            n(), "Process Card", _x, _CARD_Y, _CARD_W, _CARD_H,
            [paragraph([])], fill=_fill, line_color=_line, line_width=12700,
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
        out.append(text_box(
            n(), "Process Card Header", _x, _CARD_Y, _CARD_W, _CARD_HEADER_H,
            [paragraph([run(_hdr, size=PT(8.4), bold=True, color=_header_txt, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_header_fill, line_color=_header_fill, anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))
        out.append(text_box(
            n(), "Step Badge", _x + IN(0.055), _CARD_Y + IN(0.07), _STEP_BADGE, _STEP_BADGE,
            [paragraph([run(_num, size=PT(8.1), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
            fill=WHITE, line_color=WHITE, prst="ellipse", anchor="ctr",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))
        out.append(text_box(
            n(), "Process Card Body", _x + IN(0.11), _CARD_Y + IN(0.49), _CARD_W - IN(0.22), IN(1.36),
            _step_body(_items, text_color=_txt),
            fill=None, line_color="none", anchor="t",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── formula band ──
    out.append(text_box(
        n(), "Formula Band", _MAIN_X, _FORMULA_Y, _MAIN_W, _FORMULA_H,
        [paragraph([
            run("Governing date", size=PT(10.5), bold=True, color=BLACK, font=FONT),
            run("  −  transition / protest reserve  −  PALT  −  shaping time  =  ", size=PT(9.4), color=BLACK, font=FONT),
            run("capture start window", size=PT(10.5), bold=True, color=TEAL, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=WHITE, line_color=DK, line_width=12700, anchor="ctr",
        l_ins=60960, t_ins=27432, r_ins=60960, b_ins=27432,
    ))

    # ── funding constraint card ──
    out.append(text_box(
        n(), "Funding Constraint", _MAIN_X, _BOTTOM_Y, IN(3.02), _BOTTOM_H,
        [
            paragraph([run("Funding constraint", size=PT(8.9), bold=True, color=BLACK, font=FONT), run(": color of money", size=PT(8.9), color=BLACK, font=FONT)], line_spacing=100000, space_after=110),
            paragraph([run("Obligation availability can back-stop the latest feasible award using that FY’s funds — but is not period of performance.", size=PT(7.1), color=BLACK, font=FONT)], line_spacing=100000),
        ],
        fill=GRAY_1, line_color=RULE_GRAY, line_width=12700, anchor="t",
        l_ins=45720, t_ins=36576, r_ins=45720, b_ins=36576,
    ))
    for i, (_label, _yrs, _fill) in enumerate(_MONEY_CHIPS):
        out.append(text_box(
            n(), "Color Money Chip", IN(0.67 + i * 0.68), IN(5.37), IN(0.56), IN(0.16),
            [paragraph([
                run(_label, size=PT(5.8), bold=True, color=WHITE, font=FONT),
                run(" ", size=PT(5.8), color=WHITE, font=FONT),
                run(_yrs, size=PT(5.8), color=WHITE, font=FONT),
            ], align="ctr", line_spacing=100000)],
            fill=_fill, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── variables strip ──
    out.append(text_box(
        n(), "Window Variables", IN(3.75), _BOTTOM_Y, IN(5.97), _BOTTOM_H,
        [
            paragraph([run("Variables that stretch or compress the window", size=PT(8.9), bold=True, color=BLACK, font=FONT)], line_spacing=100000, space_after=120),
            paragraph([run(" · ".join(_WINDOW_FACTORS[:4]), size=PT(7.3), color=BLACK, font=FONT)], line_spacing=100000, space_after=50),
            paragraph([run(" · ".join(_WINDOW_FACTORS[4:]), size=PT(7.3), color=BLACK, font=FONT)], line_spacing=100000),
        ],
        fill=PALE_NOTE, line_color=RULE_GRAY, line_width=12700, anchor="t",
        l_ins=54864, t_ins=36576, r_ins=54864, b_ins=36576,
    ))

    # ── decision rule / interpretation note ──
    out.append(text_box(
        n(), "Interpretation Note", _MAIN_X, _DECISION_Y, _MAIN_W, _DECISION_H,
        [paragraph([
            run("Decision rule: ", size=PT(9.2), bold=True, color=WHITE, font=FONT),
            run("the anchor tells us when a decision is forced; validation signals tell us whether the recompete is actually forming.", size=PT(8.5), color=WHITE, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=MID_NAVY, line_color=MID_NAVY, anchor="ctr",
        l_ins=60960, t_ins=36576, r_ins=60960, b_ins=36576,
    ))

    # ── right-side warning card: when dates mislead ──
    out.append(text_box(
        n(), "Pitfalls Frame", _RIGHT_X, _CARD_Y, _RIGHT_W, IN(5.50),
        [paragraph([])], fill=WHITE, line_color=BLACK, line_width=12700,
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))
    out.append(text_box(
        n(), "Pitfalls Header", _RIGHT_X, _CARD_Y, _RIGHT_W, IN(0.40),
        [paragraph([run("When the date can mislead", size=PT(9.4), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
        fill=SECTION_NAVY, line_color=SECTION_NAVY, anchor="ctr",
        l_ins=36576, t_ins=18288, r_ins=36576, b_ins=18288,
    ))

    _pitfall_paras = [
        paragraph([run("Stress-test the anchor before treating it as the true open-rebuy point.", size=PT(7.3), italic=True, color=GRAY_4, font=FONT)], line_spacing=100000, space_after=160)
    ]
    for _label, _detail in _PITFALLS:
        _pitfall_paras.append(paragraph([
            run(_label + ": ", size=PT(7.2), bold=True, color=BLACK, font=FONT),
            run(_detail, size=PT(7.0), color=BLACK, font=FONT),
        ], line_spacing=100000, space_after=105))

    out.append(text_box(
        n(), "Pitfalls Body", _RIGHT_X + IN(0.12), _CARD_Y + IN(0.55), _RIGHT_W - IN(0.24), IN(4.78),
        _pitfall_paras,
        fill=None, line_color="none", anchor="t",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    # Emphasize the most common trap.
    out.append(text_box(
        n(), "LDO Trap Note", _RIGHT_X + IN(0.18), IN(6.70), _RIGHT_W - IN(0.36), IN(0.22),
        [paragraph([run("LDO = parent-vehicle ordering deadline, not PoP end date", size=PT(6.7), bold=True, color=RED, font=FONT)], align="ctr", line_spacing=100000)],
        fill=PALE_NOTE, line_color=RED, line_width=6350, dashed_line=True, anchor="ctr",
        l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
    ))

    return "".join(out)


def render() -> str:
    return slide(_body())
