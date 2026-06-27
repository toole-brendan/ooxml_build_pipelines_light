"""recompete_qualification_filter — Awards data-analysis deck, replacement slide module.

EXHIBIT — "Recompete Qualification Filter": a diagonal decision-tree screen that
preserves the manager's wireframe geometry while reframing the process from a
binary contract-addressability screen into a qualification filter for recompete
opportunities. The slide screens requirement family, event probability,
addressability, and pursuit path, then routes candidates to drop / archive,
monitor / shape, or recompete-window analysis.

DESIGN NOTES
  • The source wireframe structure is preserved: four diagonal decision boxes,
    compact evidence chips, verdict chips, bottom output bands, and a timing
    handoff.
  • Funding is moved out of the main gate sequence and treated as evidence for
    event probability / timing confidence.
  • Addressability is tested after event probability and includes both direct
    access and credible partner / holder routes.
  • Language is company-neutral so the module can be reused across contract
    award-analysis decks.
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
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_4, FONT

LAYOUT = "slideLayout4"

_SRC = Path(__file__).parent / "_src"
CHARTS: list = []


# Local palette drawn from repeated project colors.
SECTION_NAVY = "223E59"
MID_NAVY = "364D6E"
BLUE = "447BB2"
LIGHT_BLUE = "CEDDEC"
PALE_BLUE = "DFE7EB"
TEAL = "007770"
GREEN = "1B8A57"
RED = "C00000"
AMBER = "FFC000"
PALE_AMBER = "FFF2CC"
RULE_GRAY = "808080"
PALE_NOTE = "F7F9FB"


# ── layout anchors that mirror the source wireframe ──────────────────────────
_QUESTION_H = IN(0.641)
_VERDICT_H = IN(0.247)
_EVIDENCE_H = IN(0.272)
_BAND_H = IN(0.430)


# ── repeated-shape data tables ───────────────────────────────────────────────
# local_meaning: the four diagonal decision gates, updated to qualification-filter
# language while retaining the source wireframe placement.
_QUESTIONS = [
    # x, y, cx, number, question, subline
    (0.495, 1.386, 2.956, "1", "What recurring mission work is this?", "Requirement family, not PIID"),
    (1.974, 2.396, 2.956, "2", "Will the government likely buy it again?", "Event probability, not certainty"),
    (3.709, 3.347, 2.956, "3", "Can we reach and credibly compete?", "Vehicle access, partner route, and fit"),
    (6.197, 4.325, 2.957, "4", "What action should we take?", "Pursue, team, shape, monitor, or drop"),
]

# local_meaning: evidence chips that sit in the same positions as the manager's
# original blue factor boxes; funding now appears as an event-probability signal.
_EVIDENCE_CHIPS = [
    # x, y, cx, fill, line, label
    (4.623, 1.826, 2.356, PALE_BLUE, BLUE, "Scope / customer / incumbent / buying history"),
    (6.184, 2.842, 2.356, PALE_BLUE, BLUE, "Obligations / FYDP / forecast / decision point"),
    (7.711, 3.339, 2.356, PALE_BLUE, BLUE, "Vehicle access / prime-holder route / fit"),
    (10.122, 4.325, 2.356, PALE_BLUE, BLUE, "Pursue directly / team / shape / monitor / drop"),
    (2.193, 3.460, 2.356, PALE_AMBER, AMBER, "Holder-gated / incumbent / transition barriers"),
]

# local_meaning: verdict chips, preserving the original decision-node positions
# while moving away from overly binary Yes / No language.
_VERDICT_CHIPS = [
    # x, y, cx, fill, line, label, text_color
    (3.560, 1.839, 0.970, GREEN, GREEN, "Recurring", WHITE),
    (1.330, 2.067, 1.220, RED, RED, "One-time", WHITE),
    (4.965, 2.854, 0.980, GREEN, GREEN, "High / med.", WHITE),
    (3.022, 3.064, 0.859, RED, RED, "Low", WHITE),
    (6.650, 3.364, 1.020, GREEN, GREEN, "Reachable", WHITE),
    (4.680, 4.044, 0.970, RED, RED, "No route", WHITE),
    (8.980, 4.325, 1.310, GREEN, GREEN, "Pursue / team", WHITE),
    (6.980, 5.146, 1.390, AMBER, AMBER, "Shape / monitor", BLACK),
]

# local_meaning: bottom output bands. These replace the former binary
# non-addressable / addressable bands with a more useful qualification result.
_OUTPUT_BANDS = [
    # x, cx, fill, line, title, title_color, note, note_color
    (0.495, 3.610, GRAY_1, RULE_GRAY, "Drop / Archive", BLACK, "One-time buy • weak signal • no route", GRAY_4),
    (4.255, 4.090, PALE_BLUE, BLUE, "Monitor / Shape", BLACK, "Demand exists, but timing / funding / access needs development", DK),
    (8.602, 4.232, SECTION_NAVY, SECTION_NAVY, "Advance to Timing", WHITE, "Likely recompete + reachable path", WHITE),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Awards Data Analysis", "Recompete Screening"))
    out.append(prelim_chip())
    out.append(title_placeholder(
        "Recompete Qualification Filter",
        "A requirement becomes actionable when it is likely to be bought again and we can realistically reach the resulting action.",
    ))

    # ── question boxes: same diagonal skeleton as the manager's wireframe ──
    for _x, _y, _cx, _num, _question, _subline in _QUESTIONS:
        out.append(text_box(
            n(), "Decision Gate", IN(_x), IN(_y), IN(_cx), _QUESTION_H,
            [
                paragraph([
                    run(f"{_num}. ", size=PT(10.8), bold=True, color=SECTION_NAVY, font=FONT),
                    run(_question, size=PT(10.8), bold=True, color=BLACK, font=FONT),
                ], align="ctr", line_spacing=100000, space_after=70),
                paragraph([run(_subline, size=PT(7.5), italic=True, color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000),
            ],
            fill=WHITE, line_color=BLACK, line_width=12700, anchor="ctr",
            l_ins=45720, t_ins=36576, r_ins=45720, b_ins=36576,
        ))

    # ── evidence chips: pale fill, colored outline, compact text ──
    for _x, _y, _cx, _fill, _lc, _label in _EVIDENCE_CHIPS:
        _txt_color = DK if _fill != PALE_AMBER else BLACK
        out.append(text_box(
            n(), "Evidence Chip", IN(_x), IN(_y), IN(_cx), _EVIDENCE_H,
            [paragraph([run(_label, size=PT(7.8), italic=True, color=_txt_color, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=_lc, line_width=12700, anchor="ctr",
            l_ins=36576, t_ins=18288, r_ins=36576, b_ins=18288,
        ))

    # ── verdict chips: probability / reachability labels rather than simple Yes / No ──
    for _x, _y, _cx, _fill, _lc, _label, _tc in _VERDICT_CHIPS:
        out.append(text_box(
            n(), "Verdict Chip", IN(_x), IN(_y), IN(_cx), _VERDICT_H,
            [paragraph([run(_label, size=PT(8.8), bold=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=_lc, line_width=12700, anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))

    # ── bottom output bands: drop / monitor-shape / advance to timing ──
    for _x, _cx, _fill, _line, _title, _title_color, _note, _note_color in _OUTPUT_BANDS:
        out.append(text_box(
            n(), "Output Band", IN(_x), IN(5.818), IN(_cx), _BAND_H,
            [paragraph([run(_title, size=PT(11.3), bold=True, color=_title_color, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=_line, line_width=12700, anchor="ctr",
            l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432,
        ))
        out.append(text_box(
            n(), "Output Note", IN(_x + 0.080), IN(6.185), IN(_cx - 0.160), IN(0.185),
            [paragraph([run(_note, size=PT(6.9), italic=True, color=_note_color, font=FONT)], align="ctr", line_spacing=100000)],
            fill=None, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── direct handoff into the next methodology slide ──
    out.append(text_box(
        n(), "Timing Handoff", IN(8.602), IN(6.502), IN(4.233), IN(0.459),
        [paragraph([
            run("Advance to Recompete Window Analysis", size=PT(10.4), bold=True, color=BLACK, font=FONT),
            line_break(),
            run("estimate capture start, solicitation window, and target award", size=PT(7.7), italic=True, color=GRAY_4, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=WHITE, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432,
    ))

    # ── connector logic: retained source-wireframe routing with revised semantics ──
    out.append(connector(n(), "One-time to Drop", IN(1.974), IN(2.026), IN(0), IN(3.792), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(connector(n(), "Low Event to Monitor Shape", IN(3.452), IN(3.037), IN(2.848), IN(2.781), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_h=True))
    out.append(connector(n(), "No Route to Drop", IN(5.363), IN(3.812), IN(0.658), IN(1.010), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_h=True, rot=16200000))
    out.append(connector(n(), "Shape Monitor to Monitor Band", IN(7.675), IN(4.966), IN(0), IN(0.852), color=BLACK, width=12700, arrow=True, flip_h=True))

    out.append(connector(n(), "Requirement to Event Gate", IN(3.452), IN(1.706), IN(0.014), IN(0.690), color=BLACK, width=12700, arrow=True, prst="bentConnector4", adj={"adj1": "val 2458071", "adj2": "val 73209"}))
    out.append(connector(n(), "Event to Addressability Gate", IN(4.930), IN(2.717), IN(0.257), IN(0.631), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Addressability to Pursuit Gate", IN(6.665), IN(3.668), IN(4.053), IN(2.151), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Pursue Team to Timing Band", IN(9.153), IN(4.646), IN(1.540), IN(1.173), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Timing Band to Handoff", IN(10.718), IN(6.248), IN(0), IN(0.254), color=BLACK, width=12700, arrow=True))

    # ── small source-of-truth note: event probability × addressability ──
    out.append(text_box(
        n(), "Method Note", IN(0.495), IN(6.540), IN(7.870), IN(0.300),
        [paragraph([
            run("Recompetes are inferred events. ", size=PT(7.4), bold=True, color=DK, font=FONT),
            run("Screen requirement family first; funding is a confidence / timing signal inside event probability, not the primary key.", size=PT(7.4), color=DK, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=PALE_NOTE, line_color=RULE_GRAY, line_width=6350, anchor="ctr",
        l_ins=45720, t_ins=18288, r_ins=45720, b_ins=18288,
    ))

    return "".join(out)


def render() -> str:
    return slide(_body())
