"""contract_addressability_framework_updated — Strategic Contracts deck, replacement working module.

EXHIBIT — "Contract Addressability": a diagonal decision-tree screen that keeps
manager's wireframe geometry while replacing directional placeholder text with a
presentation-ready opportunity screen. The slide separates recurring demand,
access, funding, and shaping/entry into four gates, then routes the output to
non-addressable / monitor or addressable timing analysis.

DESIGN NOTES
  • The source wireframe structure is preserved: four diagonal question boxes,
    evidence chips, yes/no verdict chips, bottom output bands, and a final
    timing handoff.
  • Yellow placeholder highlights and underlines are removed.
  • Budget is treated as a confidence and executability signal, not as the
    primary key for the opportunity.
  • Language is company-neutral so the module can be reused in agnostic decks.
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
from deck_core.style import IN, PT, BLACK, WHITE, DK, GRAY_1, GRAY_2, GRAY_4, FONT

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


# ── repeated-shape data tables ───────────────────────────────────────────────
# local_meaning: the four manager-wireframe decision gates, updated to methodology
# language while retaining the diagonal placement.
_QUESTIONS = [
    # x, y, cx, number, question, subline
    (0.495, 1.386, 2.956, "1", "Does the requirement recur?", "Requirement family, not PIID"),
    (1.974, 2.396, 2.956, "2", "Who can access the action?", "Open, holder-gated, or incumbent-led"),
    (3.709, 3.347, 2.956, "3", "Is funding executable?", "Budget support and color of money"),
    (6.197, 4.325, 2.957, "4", "If budget is short, can funding be shaped?", "Possibility of shaping the appropriation process"),
]

# local_meaning: evidence chips that sit in the same positions as the manager's
# blue factor boxes.
_EVIDENCE_CHIPS = [
    # x, y, cx, fill, line, label
    (4.623, 1.826, 2.356, PALE_BLUE, BLUE, "FYDP / to-complete / recurring obligations"),
    (6.184, 2.842, 2.356, PALE_BLUE, BLUE, "Open competition / vehicle access"),
    (7.711, 3.339, 2.356, PALE_BLUE, BLUE, "Requested appropriations / TAS / budget line"),
    (10.122, 4.325, 2.356, PALE_BLUE, BLUE, "POM input / UPL / congressional add / reprogramming"),
    (2.193, 3.460, 2.356, PALE_AMBER, AMBER, "Holder-gated / incumbents only"),
]

# local_meaning: yes/no verdict chips, preserving the original decision-node
# positions and replacing placeholder highlighted text with finished labels.
_VERDICT_CHIPS = [
    # x, y, cx, fill, line, label, text_color
    (3.615, 1.839, 0.859, GREEN, GREEN, "Yes", WHITE),
    (1.544, 2.067, 0.859, RED, RED, "No", WHITE),
    (5.019, 2.854, 0.859, GREEN, GREEN, "Yes", WHITE),
    (3.022, 3.064, 0.859, RED, RED, "No", WHITE),
    (6.712, 3.364, 0.859, GREEN, GREEN, "Yes", WHITE),
    (4.719, 4.044, 0.859, RED, RED, "No", WHITE),
    (9.208, 4.325, 0.859, GREEN, GREEN, "Likely", WHITE),
    (7.092, 5.146, 1.143, RED, RED, "Not likely", WHITE),
]

# local_meaning: bottom callout labels for output route semantics. These sit
# under the manager's non-addressable / addressable bands.
_OUTPUT_NOTES = [
    (0.715, 6.185, 7.43, "No recurring demand  •  locked access  •  unfunded with no path to shape the appropriation", GRAY_4),
    (8.820, 6.185, 3.79, "Direct recompete  •  vehicle on-ramp  •  prime / holder route", WHITE),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Defense Market Strategy", "Market Access Framework"))
    out.append(prelim_chip())
    out.append(title_placeholder(
        "Contract Addressability",
        "A contract becomes actionable when demand recurs, access exists, and funding is executable—or, where it falls short, the appropriation can be shaped to support it.",
    ))

    # ── question boxes: same diagonal skeleton as the manager's wireframe ──
    for _x, _y, _cx, _num, _question, _subline in _QUESTIONS:
        out.append(text_box(
            n(), "Decision Gate", IN(_x), IN(_y), IN(_cx), _QUESTION_H,
            [
                paragraph([
                    run(f"{_num}. ", size=PT(11.5), bold=True, color=SECTION_NAVY, font=FONT),
                    run(_question, size=PT(11.5), bold=True, color=BLACK, font=FONT),
                ], align="ctr", line_spacing=100000, space_after=80),
                paragraph([run(_subline, size=PT(7.6), italic=True, color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000),
            ],
            fill=WHITE, line_color=BLACK, line_width=12700, anchor="ctr",
            l_ins=45720, t_ins=36576, r_ins=45720, b_ins=36576,
        ))

    # ── evidence chips: pale fill, colored outline, compact text ──
    for _x, _y, _cx, _fill, _lc, _label in _EVIDENCE_CHIPS:
        _txt_color = DK if _fill != PALE_AMBER else BLACK
        out.append(text_box(
            n(), "Evidence Chip", IN(_x), IN(_y), IN(_cx), _EVIDENCE_H,
            [paragraph([run(_label, size=PT(8.2), italic=True, color=_txt_color, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=_lc, line_width=12700, anchor="ctr",
            l_ins=36576, t_ins=18288, r_ins=36576, b_ins=18288,
        ))

    # ── verdict chips: finished green/red tags, no yellow placeholder marks ──
    for _x, _y, _cx, _fill, _lc, _label, _tc in _VERDICT_CHIPS:
        out.append(text_box(
            n(), "Verdict Chip", IN(_x), IN(_y), IN(_cx), _VERDICT_H,
            [paragraph([run(_label, size=PT(9.2), bold=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=_lc, line_width=12700, anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))

    # ── bottom output bands, preserving the manager's terminal structure ──
    out.append(text_box(
        n(), "Non Addressable Band", IN(0.495), IN(5.818), IN(7.870), IN(0.430),
        [paragraph([run("Non-addressable / monitor", size=PT(11.5), bold=True, color=BLACK, font=FONT)], align="ctr", line_spacing=100000)],
        fill=GRAY_1, line_color=RULE_GRAY, line_width=12700, anchor="ctr",
        l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432,
    ))
    out.append(text_box(
        n(), "Addressable Band", IN(8.602), IN(5.818), IN(4.232), IN(0.430),
        [paragraph([run("Addressable", size=PT(11.5), bold=True, color=WHITE, font=FONT)], align="ctr", line_spacing=100000)],
        fill=SECTION_NAVY, line_color=SECTION_NAVY, line_width=12700, anchor="ctr",
        l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432,
    ))
    for _x, _y, _cx, _label, _tc in _OUTPUT_NOTES:
        out.append(text_box(
            n(), "Output Note", IN(_x), IN(_y), IN(_cx), IN(0.185),
            [paragraph([run(_label, size=PT(7.2), italic=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000)],
            fill=None, line_color="none", anchor="ctr", wrap="none",
            l_ins=0, t_ins=0, r_ins=0, b_ins=0,
        ))

    # ── direct handoff into timing, exactly where the source wireframe placed it ──
    out.append(text_box(
        n(), "Timing Handoff", IN(8.602), IN(6.502), IN(4.233), IN(0.459),
        [paragraph([
            run("Determine recompete timing, outlook & pathway", size=PT(10.6), bold=True, color=BLACK, font=FONT),
            line_break(),
            run("see following page for timing estimation", size=PT(8.0), italic=True, color=GRAY_4, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=WHITE, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432,
    ))

    # ── connector logic: retained positions from the wireframe, renamed by role ──
    out.append(connector(n(), "No Demand to Non Addressable", IN(1.974), IN(2.026), IN(0), IN(3.792), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(connector(n(), "Locked Access to Non Addressable", IN(3.452), IN(3.037), IN(0), IN(2.781), color=BLACK, width=12700, arrow=True, flip_h=True))
    out.append(connector(n(), "Unfunded to Non Addressable", IN(5.363), IN(3.812), IN(0.658), IN(1.010), color=BLACK, width=12700, arrow=True, prst="bentConnector2", flip_h=True, rot=16200000))
    out.append(connector(n(), "Not Likely to Non Addressable", IN(7.675), IN(4.966), IN(0), IN(0.852), color=BLACK, width=12700, arrow=True, flip_h=True))

    out.append(connector(n(), "Demand Yes to Access Gate", IN(3.452), IN(1.706), IN(0.014), IN(0.690), color=BLACK, width=12700, arrow=True, prst="bentConnector4", adj={"adj1": "val 2458071", "adj2": "val 73209"}))
    out.append(connector(n(), "Access Yes to Funding Gate", IN(4.930), IN(2.717), IN(0.257), IN(0.631), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Funding Yes to Shape Gate", IN(6.665), IN(3.668), IN(4.053), IN(2.151), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Likely to Addressable", IN(9.153), IN(4.646), IN(0.859), IN(1.173), color=BLACK, width=12700, arrow=True, prst="bentConnector2"))
    out.append(connector(n(), "Addressable to Timing", IN(10.718), IN(6.248), IN(0), IN(0.254), color=BLACK, width=12700, arrow=True))

    # ── small source-of-truth note: requirement-family first, budget as signal ──
    out.append(text_box(
        n(), "Method Note", IN(0.495), IN(6.540), IN(7.870), IN(0.300),
        [paragraph([
            run("Screen the requirement family first. ", size=PT(7.4), bold=True, color=DK, font=FONT),
            run("Weak budget alignment is not disqualifying on its own; gauge whether the appropriation can be shaped before ruling an opportunity out.", size=PT(7.4), color=DK, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=PALE_NOTE, line_color=RULE_GRAY, line_width=6350, anchor="ctr",
        l_ins=45720, t_ins=18288, r_ins=45720, b_ins=18288,
    ))

    return "".join(out)


def render() -> str:
    return slide(_body())
