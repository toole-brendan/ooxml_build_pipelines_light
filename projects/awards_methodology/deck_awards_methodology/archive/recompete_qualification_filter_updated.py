"""recompete_qualification_filter — Awards data-analysis deck, replacement slide module.

EXHIBIT — "Recompete Qualification Filter": a diagonal decision-tree screen that
preserves the manager's wireframe geometry while reframing the process from a
binary contract-addressability screen into a qualification filter for recompete
opportunities. The slide screens requirement family, event probability,
addressability, and pursuit path, then routes candidates to drop / archive,
monitor / shape, or recompete-window analysis.

DESIGN NOTES
  • Preserves the diagonal source-wireframe skeleton: four decision gates,
    evidence chips, verdict chips, output bands, and a timing handoff.
  • Updates geometry to remove unintended chip / label collisions and gives
    long labels enough horizontal room or shorter copy so text fits.
  • Paints connectors before all decision nodes / chips / labels. Because every
    overlaid label has an opaque fill, connector segments visually disappear
    behind the label instead of drawing across the text.
  • Funding is treated as evidence for event probability / timing confidence;
    addressability includes both direct access and credible partner / holder routes.
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
_VERDICT_H = IN(0.270)
_EVIDENCE_H = IN(0.310)
_BAND_H = IN(0.560)
_HANDOFF_H = IN(0.485)


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

# local_meaning: evidence chips that sit in the same role as the manager's
# original blue factor boxes. Coordinates were spaced to avoid touching gate boxes
# or verdict chips while keeping the diagonal screen readable.
_EVIDENCE_CHIPS = [
    # x, y, cx, fill, line, label
    (4.620, 1.830, 2.460, PALE_BLUE, BLUE, "Scope / customer / incumbent / buying history"),
    (6.215, 2.820, 2.460, PALE_BLUE, BLUE, "Obligations / FYDP / forecast / decision point"),
    (7.895, 3.390, 2.450, PALE_BLUE, BLUE, "Vehicle / partner route / fit"),
    (10.280, 4.295, 2.500, PALE_BLUE, BLUE, "Pursue / team / shape / monitor / drop"),
    (1.205, 3.415, 2.380, PALE_AMBER, AMBER, "Holder-gated / incumbent / transition barriers"),
]

# local_meaning: verdict chips. These are intentionally over connector paths,
# but no longer overlap the decision/evidence boxes themselves. Fills mirror the
# contract_addressability_framework exhibit (slide 8): each chip is a 20%-opacity
# shade wash (fill_alpha=20000) of its base color over a solid same-color border,
# so the labels read as black text on a pale red / green / amber tint.
_VERDICT_CHIPS = [
    # x, y, cx, fill, line, label, text_color
    (3.560, 1.830, 0.970, GREEN, GREEN, "Recurring", BLACK),
    (1.300, 2.065, 1.220, RED, RED, "One-time", BLACK),
    (4.985, 2.820, 1.020, GREEN, GREEN, "High / med.", BLACK),
    (2.750, 3.105, 0.890, RED, RED, "Low", BLACK),
    (6.775, 3.405, 1.020, GREEN, GREEN, "Reachable", BLACK),
    (4.795, 4.065, 0.990, RED, RED, "No route", BLACK),
    (9.435, 4.680, 1.320, GREEN, GREEN, "Pursue / team", BLACK),
    (6.895, 5.100, 1.430, AMBER, AMBER, "Shape / monitor", BLACK),
]

# local_meaning: bottom output bands. Notes are now inside the filled bands rather
# than separate transparent labels, which eliminates the former band/note overlap
# and prevents connector bleed-through behind the note text.
_OUTPUT_BANDS = [
    # x, cx, fill, line, title, title_color, note, note_color
    (0.495, 3.610, GRAY_1, RULE_GRAY, "Drop / Archive", BLACK, "One-time buy • weak signal • no route", GRAY_4),
    (4.255, 4.090, PALE_BLUE, BLUE, "Monitor / Shape", BLACK, "Timing / funding / access needs development", DK),
    (8.602, 4.232, SECTION_NAVY, SECTION_NAVY, "Advance to Timing", WHITE, "Likely recompete + reachable path", WHITE),
]

# local_meaning: connector routing from the original wireframe. Connectors are
# emitted before the labels/nodes so later opaque chips mask the parts beneath them.
_CONNECTORS = [
    # name, x, y, cx, cy, kwargs
    ("One-time to Drop", 1.974, 2.030, 0.000, 3.710, {"arrow": True, "flip_h": True}),
    ("Low Event to Monitor Shape", 3.475, 3.050, 2.825, 2.690, {"arrow": True, "prst": "bentConnector2", "flip_h": True}),
    ("No Route to Drop", 5.350, 3.835, 0.680, 1.050, {"arrow": True, "prst": "bentConnector2", "flip_h": True, "rot": 16200000}),
    ("Shape Monitor to Monitor Band", 7.610, 4.965, 0.000, 0.775, {"arrow": True, "flip_h": True}),
    ("Requirement to Event Gate", 3.452, 1.706, 0.014, 0.690, {"arrow": True, "prst": "bentConnector4", "adj": {"adj1": "val 2458071", "adj2": "val 73209"}}),
    ("Event to Addressability Gate", 4.930, 2.717, 0.257, 0.631, {"arrow": True, "prst": "bentConnector2"}),
    ("Addressability to Pursuit Gate", 6.665, 3.668, 4.053, 2.072, {"arrow": True, "prst": "bentConnector2"}),
    ("Pursue Team to Timing Band", 9.153, 4.646, 1.540, 1.094, {"arrow": True, "prst": "bentConnector2"}),
    ("Timing Band to Handoff", 10.718, 6.300, 0.000, 0.145, {"arrow": True}),
]


def _body() -> str:
    out: list[str] = []
    _ids = iter(range(100, 2000))
    n = lambda: next(_ids)  # noqa: E731 - sequential shape ids

    # ── chrome ──
    out.append(breadcrumb("Awards Data Analysis", "Recompete Screening"))
    out.append(prelim_chip())
    out.append(title_placeholder(
        "Contract Addressability",
        "A contract becomes actionable when demand recurs, access exists, and funding is executable",
    ))

    # ── connectors: deliberately first, so later chips / labels mask them ──
    for _name, _x, _y, _cx, _cy, _kw in _CONNECTORS:
        out.append(connector(
            n(), _name, IN(_x), IN(_y), IN(_cx), IN(_cy),
            color=BLACK, width=12700, **_kw,
        ))

    # ── question boxes: diagonal skeleton ──
    for _x, _y, _cx, _num, _question, _subline in _QUESTIONS:
        out.append(text_box(
            n(), "Decision Gate", IN(_x), IN(_y), IN(_cx), _QUESTION_H,
            [
                paragraph([
                    run(f"{_num}. ", size=PT(10.6), bold=True, color=SECTION_NAVY, font=FONT),
                    run(_question, size=PT(10.6), bold=True, color=BLACK, font=FONT),
                ], align="ctr", line_spacing=100000, space_after=55),
                paragraph([run(_subline, size=PT(7.4), italic=True, color=GRAY_4, font=FONT)], align="ctr", line_spacing=100000),
            ],
            fill=WHITE, line_color=BLACK, line_width=19050, anchor="ctr",
            l_ins=45720, t_ins=36576, r_ins=45720, b_ins=36576,
        ))

    # ── evidence chips: pale fill, colored outline, compact text ──
    for _x, _y, _cx, _fill, _lc, _label in _EVIDENCE_CHIPS:
        _txt_color = DK if _fill != PALE_AMBER else BLACK
        out.append(text_box(
            n(), "Evidence Chip", IN(_x), IN(_y), IN(_cx), _EVIDENCE_H,
            [paragraph([run(_label, size=PT(7.4), italic=True, color=_txt_color, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, line_color=_lc, line_width=12700, anchor="ctr",
            l_ins=27432, t_ins=18288, r_ins=27432, b_ins=18288,
        ))

    # ── verdict chips: probability / reachability labels rather than simple Yes / No ──
    # 20%-opacity shade wash over a solid same-color border (matches slide 8). Because
    # the wash is translucent, each chip first gets an opaque white backing of the same
    # geometry: the chips sit on top of connector paths, so without it the connector
    # segment beneath would bleed through the wash. The backing masks the line; the
    # wash then sits over white and reads as the intended pale tint.
    for _x, _y, _cx, _fill, _lc, _label, _tc in _VERDICT_CHIPS:
        out.append(text_box(
            n(), "Verdict Chip Backing", IN(_x), IN(_y), IN(_cx), _VERDICT_H,
            [paragraph([])],
            fill=WHITE, line_color="none", anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))
        out.append(text_box(
            n(), "Verdict Chip", IN(_x), IN(_y), IN(_cx), _VERDICT_H,
            [paragraph([run(_label, size=PT(8.7), bold=True, color=_tc, font=FONT)], align="ctr", line_spacing=100000)],
            fill=_fill, fill_alpha=20000, line_color=_lc, line_width=12700, anchor="ctr",
            l_ins=27432, t_ins=9144, r_ins=27432, b_ins=9144,
        ))

    # ── bottom output bands: drop / monitor-shape / advance to timing ──
    for _x, _cx, _fill, _line, _title, _title_color, _note, _note_color in _OUTPUT_BANDS:
        out.append(text_box(
            n(), "Output Band", IN(_x), IN(5.740), IN(_cx), _BAND_H,
            [
                paragraph([run(_title, size=PT(10.8), bold=True, color=_title_color, font=FONT)], align="ctr", line_spacing=100000, space_after=20),
                paragraph([run(_note, size=PT(6.9), italic=True, color=_note_color, font=FONT)], align="ctr", line_spacing=100000),
            ],
            fill=_fill, line_color=_line, line_width=12700, anchor="ctr",
            l_ins=45720, t_ins=18288, r_ins=45720, b_ins=18288,
        ))

    # ── direct handoff into the next methodology slide ──
    out.append(text_box(
        n(), "Timing Handoff", IN(8.602), IN(6.445), IN(4.233), _HANDOFF_H,
        [paragraph([
            run("Advance to Recompete Window Analysis", size=PT(10.2), bold=True, color=BLACK, font=FONT),
            line_break(),
            run("estimate capture start, solicitation window, and target award", size=PT(7.6), italic=True, color=GRAY_4, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=WHITE, line_color=BLACK, line_width=12700, anchor="ctr",
        l_ins=45720, t_ins=27432, r_ins=45720, b_ins=27432,
    ))

    # ── small source-of-truth note: event probability × addressability ──
    out.append(text_box(
        n(), "Method Note", IN(0.495), IN(6.535), IN(7.870), IN(0.320),
        [paragraph([
            run("Recompetes are inferred events. ", size=PT(7.3), bold=True, color=DK, font=FONT),
            run("Screen requirement family first; funding is a confidence / timing signal inside event probability, not the primary key.", size=PT(7.3), color=DK, font=FONT),
        ], align="ctr", line_spacing=100000)],
        fill=PALE_NOTE, line_color=RULE_GRAY, line_width=6350, anchor="ctr",
        l_ins=45720, t_ins=18288, r_ins=45720, b_ins=18288,
    ))

    return "".join(out)


def render() -> str:
    return slide(_body())
