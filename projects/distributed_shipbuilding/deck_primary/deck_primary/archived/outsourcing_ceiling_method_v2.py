"""outsourcing_ceiling_method_v2 - alternative Methodology treatment for the
Outsourcing Ceiling, built to sit right after outsourcing_ceiling_method.py so the
two can be compared side by side.

Where the first method slide builds the ceiling as a left-to-right input -> engine
-> reads flow over a result table, this version is Pattern C: a five-step build
flow across the upper left and center, a right-side commentary rail that argues the
method's defensibility, and a compact assumption-status ledger under the flow that
makes the judgment levers (h, L, p, POP) auditable rather than buried. Three
guardrail chips pre-empt the predictable reviewer challenges.

Pure deck_core primitives (no chart). Flow boxes ramp light -> dark as the estimate
moves from input to answer, with dark fill reserved for the two conceptual-answer
boxes (must-stay core, ceiling). Chrome + sources are shared with the sibling
ceiling slides; sources stay external (no internal workbook-tab names).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell,
)
from deck_core.style import (
    BODY_X, BODY_R, BLACK, GRAY_1, GRAY_5, FONT,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
    INSETS_CARD, INSETS_CHIP, INSETS_NONE, blue_pair,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

# ── Chrome text (shared with the sibling ceiling slides) ─────────────────────
_SECTION = "Executive Summary"
_TOPIC_LABEL = "Supplier TAM and SAM"
_TOPIC = "Outsourcing Ceiling Methodology"
_TAKEAWAY = ("The ceiling is built from the must-stay core, not read from a "
             "budget line.")
_SOURCES = (
    "Sources: Defense News, \"Defense firms outsource sub, carrier construction "
    "amid labor woes\" (M. Eckstein, Oct 2022); O'Rourke (CRS), State of U.S. "
    "Shipbuilding, House Armed Services Committee testimony (Mar 2025), "
    "cross-checked against the CBO Shipbuilding Composite Index (Apr 2024); "
    "DoD FMR 7000.14-R Vol 2B Ch 4, Exhibit P-5 ship cost element categories "
    "(Nov 2017); DoD contract award announcements (announced place-of-performance): "
    "Virginia Block V (2019), Columbia Build I (2020), DDG-51 FY23–27 multiyear "
    "(2023)"
)
_SOURCES_Y = 6_085_448
_BOTTOM = 6_023_400

# ── Two-zone layout: LEFT/center build zone + RIGHT commentary rail ──────────
_LEFT_X = BODY_X
_LEFT_CX = 7_500_000
_RAIL_X = _LEFT_X + _LEFT_CX + 180_000        # gutter between zones
_RAIL_CX = BODY_R - _RAIL_X

# ── Flow band: five build-up steps, left to right ────────────────────────────
_FLOW_Y, _BOX_H = 1_460_000, 1_220_000
_BOX_GAP = 300_000
_BOX_W = (_LEFT_CX - 4 * _BOX_GAP) // 5
_BOX_PITCH = _BOX_W + _BOX_GAP
_FLOW_MID = _FLOW_Y + _BOX_H // 2
_CONN_PT = 6350                               # ½pt black flow weight

# (ramp index, number, title, [sublines]). Dark fill (ramp 3/4) is reserved for
# the must-stay core and the ceiling - the two conceptual answers.
_BOXES = [
    (0, "1", "Define addressable base",
     ["Basic Construction, FY22–27 P-5c", "Excludes GFE and non-BC ship cost"]),
    (1, "2", "Set labor mechanics",
     ["h = movable labor-hour share", "L = labor share of BC"]),
    (3, "3", "Isolate must-stay core",
     ["Core = L × (1 − h)", "Final assembly, integration, test"]),
    (4, "4", "Convert core into ceiling",
     ["Ceiling = 1 − core", "p=100% material-inclusive upper bound"]),
    (1, "5", "Compare with floor",
     ["Current POP is the floor", "Headroom = ceiling / current"]),
]


def _box_x(i: int) -> int:
    return _LEFT_X + i * _BOX_PITCH


def _flow() -> str:
    parts = []
    for i, (ramp, num, title, subs) in enumerate(_BOXES):
        fill, txt = blue_pair(ramp)
        paras = [paragraph([run(f"{num}.  ", size=LABEL_9PT, bold=True,
                                color=txt, font=FONT),
                            run(title, size=LABEL_9PT, bold=True, color=txt,
                                font=FONT)], space_after=80)]
        paras += [paragraph([run(s, size=FINEPRINT_8_5PT, color=txt, font=FONT)],
                            space_after=60) for s in subs]
        parts.append(text_box(20 + i, f"Box{i + 1}", _box_x(i), _FLOW_Y,
                              _BOX_W, _BOX_H, paras, fill=fill, anchor="t",
                              insets=INSETS_CARD))
    # four straight black arrows, box -> box, sitting in the gaps
    for i in range(4):
        x = _box_x(i) + _BOX_W
        parts.append(connector(30 + i, f"Step{i + 1}to{i + 2}", x, _FLOW_MID,
                              _BOX_GAP, 0, arrow=True, width=_CONN_PT,
                              color=BLACK))
    return "".join(parts)


# ── Bridge inset under boxes 3-4 (a labeled rail, not a competing flow) ──────
_BRIDGE_X = _box_x(2)
_BRIDGE_W = _box_x(3) + _BOX_W - _BRIDGE_X
_BRIDGE_Y, _BRIDGE_H = _FLOW_Y + _BOX_H + 70_000, 440_000


def _bridge() -> str:
    return text_box(
        40, "Bridge", _BRIDGE_X, _BRIDGE_Y, _BRIDGE_W, _BRIDGE_H,
        [paragraph([run("Hours-to-dollars bridge", size=FINEPRINT_8_5PT,
                        bold=True, italic=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=50),
         paragraph([run("p=0 labor-only  ·  p=50% selected case  ·  "
                        "p=100% structural ceiling", size=FINEPRINT_8_5PT,
                        italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=GRAY_1, line_color="none", anchor="ctr",
        insets=(114_300, 40_000, 114_300, 40_000))


# ── Method ledger: the four levers, made auditable (horizontal rules only) ───
_LED_HEADER = ["Lever", "Workbook treatment", "Deck wording"]
_LED_ROWS = [
    ["h", "Sourced for submarines; DDG-51 assumption", "Movable labor-hour share"],
    ["L", "Sourced total-cost anchor, rebased to BC",
     "Labor share of Basic Construction"],
    ["p", "Scenario input", "Material pass-through dial"],
    ["POP", "Sourced / derived current state", "Current floor, not ceiling"],
]
_LED_ALL = [_LED_HEADER] + _LED_ROWS
_LED_COL_W = [1_150_000, 3_000_000, 3_350_000]   # Deck wording widest; sum LEFT_CX
assert sum(_LED_COL_W) == _LEFT_CX, "ledger columns must sum to the left zone width"
_LED_SZ = LABEL_9PT
_LED_ALIGNS = ["ctr", "l", "l"]
_LED_ROW_H = estimate_row_heights(_LED_ALL, _LED_COL_W, size_pt=_LED_SZ / 100.0)
_LED_CY = sum(_LED_ROW_H)
_LED_Y = _BRIDGE_Y + _BRIDGE_H + 120_000
_LED_LAST = len(_LED_ALL) - 1

_RULE_HEADER = {"color": BLACK, "width": 19_050}    # 1.5pt under the header
_RULE_BODY = {"color": GRAY_5, "width": 6_350}      # ½pt between body rows


def _led_border(ri: int) -> dict:
    if ri == 0:
        return {"B": _RULE_HEADER}
    if ri == _LED_LAST:
        return {"B": "none"}
    return {"B": _RULE_BODY}


def _ledger() -> str:
    rows = []
    for ri, row in enumerate(_LED_ALL):
        border = _led_border(ri)
        cells = [
            tcell(text, size=_LED_SZ, align=_LED_ALIGNS[ci],
                  bold=(ri == 0 or ci == 0), anchor="ctr", borders=border)
            for ci, text in enumerate(row)
        ]
        rows.append(trow(cells, h=_LED_ROW_H[ri]))
    return table(50, "MethodLedger", _LEFT_X, _LED_Y, _LEFT_CX, _LED_CY,
                 col_widths=_LED_COL_W, rows=rows)


# ── Guardrail chips: pre-empt the three predictable challenges ───────────────
_CHIPS = ["Upper bound, not working case", "DDG-51 h/L are assumptions",
          "Shares are the answer; $ show magnitude"]
_CHIP_GAP = 150_000
_CHIP_W = (_LEFT_CX - 2 * _CHIP_GAP) // 3
_CHIP_H = 320_000
_CHIP_Y = _LED_Y + _LED_CY + 110_000
assert _CHIP_Y + _CHIP_H <= _BOTTOM, (
    "guardrail chips pushed past the body bottom - ledger copy grew past its "
    "budget; tighten the flow band or drop the ledger's Deck-wording column")


def _chips() -> str:
    parts = []
    for i, text in enumerate(_CHIPS):
        x = _LEFT_X + i * (_CHIP_W + _CHIP_GAP)
        parts.append(text_box(
            60 + i, f"Chip{i + 1}", x, _CHIP_Y, _CHIP_W, _CHIP_H,
            [paragraph([run(text, size=LABEL_9PT, color=BLACK, font=FONT)],
                       align="ctr")],
            fill=GRAY_1, anchor="ctr", insets=INSETS_CHIP))
    return "".join(parts)


# ── Right commentary rail: why the method is defensible ──────────────────────
_RAIL_BLOCKS = [
    (1_460_000, 1_450_000,
     "The denominator choice is the defensibility move.",
     "Basic Construction isolates the work the prime yard can make or buy. GFE "
     "and total ship cost stay outside the addressable base, so the model does "
     "not treat combat systems, reactor content, or other government-furnished "
     "items as outsourcing opportunity."),
    (2_980_000, 1_100_000,
     "The model estimates a ceiling, not a forecast.",
     "Current POP is the starting floor. The structural ceiling is the p=100% "
     "upper bound; the selected p=50% case is the more conservative working read."),
    (4_180_000, 1_700_000,
     "The slide shows the judgment points before reviewers ask.",
     "DDG-51 h and L are analyst assumptions, L is rebased from total cost to "
     "Basic Construction, and p materially moves the dollar answer."),
]


def _rail() -> str:
    parts = []
    for i, (y, h, lead, body) in enumerate(_RAIL_BLOCKS):
        parts.append(text_box(
            70 + i, f"Rail{i + 1}", _RAIL_X, y, _RAIL_CX, h,
            [paragraph([run(lead + " ", size=DENSE_BODY_10PT, bold=True,
                            color=BLACK, font=FONT),
                        run(body, size=950, color=BLACK, font=FONT)])],
            fill=None, anchor="t", insets=INSETS_NONE))
    return "".join(parts)


def _body() -> str:
    return _flow() + _bridge() + _ledger() + _chips() + _rail()


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC_LABEL)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES, y=_SOURCES_Y)
    )
