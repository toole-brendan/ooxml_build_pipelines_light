"""overview - context + objectives, on the 50%-block dark-left layout (v3.3 slide 2).

Faithful port of v3.3 slide 2: slideLayout3 ('50% Block + Title') supplies the
dark-left panel; this module places the light 'Overview' title, the two header +
bulleted-body columns (light text on the dark left, dark text on the white
right), and the yellow preliminary note. The think-cell wrapper tables of the
source are reproduced as header text + rule + bulleted body. (BuildCo -> Saronic.)
"""
from __future__ import annotations

from deck_core.primitives import slide, run, paragraph, text_box, connector
from deck_core.style import (
    GRAY_1, GRAY_3, DK, BLACK, FONT, PRELIM,
    INSETS_NONE,
    BADGE_16PT, BODY_12PT,
)

LAYOUT = "slideLayout3"   # '50% Block + Title' — dark-left panel from the layout

_LIGHT = GRAY_1   # #F2F2F2 text on the dark left panel
_DARK = DK        # #162029 text on the white right side
_BODY_PT = 1400   # 14pt body (source sz=1400)

# Geometry from the source slide (EMU).
_TITLE_XY = (457200, 566928, 5184648, 566928)
_COL_Y = 1508760
_HDR_H = 411480
_LEFT_X = 457200
_RIGHT_X = 6409944
_COL_W = 5212080
_NOTE = (6409944, 5879592, 5212080, 484632)

# (text, level) — level 1 renders as an en-dash sub-bullet
_CONTEXT = [
    ("Saronic is deciding which defense MRO work to pursue and how candidate sites map to the "
     "Navy and Coast Guard footprint:", 0),
    ("Priority work segments and vessel classes that define the reachable opportunity", 1),
    ("Gulf Coast and California site fit against existing USN and USCG MRO demand", 1),
]
_OBJECTIVES = [
    "FY2025 USN and USCG MRO contracting market by work segment, vessel category, prime, RMC "
    "geography, and appropriation",
    "Priority-segment volume and average contract value",
    "USG industrial-base funding and path to access",
    "Competitor archetypes, positioning, and capability requirements",
    "Saronic financial outlook and required USG investment",
    "Scorecard summary and sequenced path to market",
]
_NOTE_TEXT = ("Estimate confidence improves with expert validation, additional contract-level "
              "diligence, and site-specific inputs")


def _bullet(text: str, level: int, color: str, *, last: bool) -> str:
    sa = 0 if last else 60
    if level == 0:
        return paragraph([run(text, size=_BODY_PT, color=color, font=FONT)],
                         bullet=True, mar_l=285750, indent=-228600, space_after=sa)
    return paragraph([run("–  ", size=_BODY_PT, color=color, font=FONT),
                      run(text, size=_BODY_PT, color=color, font=FONT)],
                     mar_l=461963, indent=-176213, space_after=sa)


def _column(base_id: int, x: int, header: str, color: str, items, rule_color: str) -> str:
    hdr = text_box(
        base_id, f"Hdr{base_id}", x, _COL_Y, _COL_W, _HDR_H,
        [paragraph([run(header, size=BADGE_16PT, bold=True, color=color, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
    rule = connector(base_id + 1, f"Rule{base_id}", x, _COL_Y + _HDR_H, _COL_W, 0,
                     color=rule_color, width=9_525)
    body_y = _COL_Y + _HDR_H + 70_000
    paras = []
    for i, item in enumerate(items):
        last = (i == len(items) - 1)
        if isinstance(item, tuple):
            paras.append(_bullet(item[0], item[1], color, last=last))
        else:
            paras.append(_bullet(item, 0, color, last=last))
    body = text_box(
        base_id + 2, f"Body{base_id}", x, body_y, _COL_W, 4_000_000, paras,
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE,
    )
    return hdr + rule + body


def _body() -> str:
    title = text_box(
        10, "OverviewTitle", *_TITLE_XY,
        [paragraph([run("Overview", size=2000, color=_LIGHT, font=FONT)], align="l")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE,
    )
    left = _column(20, _LEFT_X, "Context", _LIGHT, _CONTEXT, GRAY_3)
    right = _column(30, _RIGHT_X, "Current sizing outputs", _DARK, _OBJECTIVES, GRAY_3)
    note = text_box(
        40, "PrelimNote", *_NOTE,
        [paragraph([run(_NOTE_TEXT, size=BODY_12PT, bold=True, italic=True, color=BLACK, font=FONT)],
                   align="l")],
        fill=PRELIM, line_width=19_050, anchor="ctr", insets=(91440, 45720, 91440, 45720),
    )
    return title + left + right + note


def render() -> str:
    return slide(_body())
