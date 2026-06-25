"""outsourcing_ceiling_method_v3 - the Outsourcing Ceiling calculation bridge: the
third (and recommended) treatment, built to sit beside method.py (v1) and
method_v2.py (v2) so the three can be compared.

This page explains HOW the maximum supplier share is sized - it is not a methods
appendix and it does not pre-sell the result, because a results exhibit follows it.
It reads as an analytical bridge: no budget line splits must-stay assembly from
outsourceable work, so the ceiling is built by isolating the must-stay core and
then applying a material pass-through dial p.

Layout (a calculation bridge, top to bottom):

  - Framer (no-fill, full width): why the ceiling is BUILT, not looked up - no
    budget line splits the work; published place-of-performance is only a floor.
  - Build machine (left/center): a four-box left->right flow, Addressable base
    (Basic Construction) -> Labor mechanics (h, L) -> Must-stay core (= L(1-h)) ->
    Structural ceiling (= 1-core), light->dark on the blue ramp (no BLUE_5, so the
    page does not over-weight). Real connectors with visible travel carry the flow.
  - The bridge: the structural ceiling drops into a bridge-formula node -
    Dollarized supplier share = hL + p(1 - L) - which distributes (tick
    connectors) into THREE READ CARDS, the same build at p = 0 / 50% / 100%
    (~25% / ~51% / ~76%). The cards share one weight; the next slide owns the
    headline result, so p=100% is not given a hero badge here.
  - Right rail: the lever ledger - the four variables (h, L, p, POP), each with
    its basis and role in the estimate - and a quiet interpretive note.
  - Guardrail chips (full width, bottom): the three predictable challenges.

Pure deck_core primitives (no chart). Rendered copy carries no self-reference
(no "slide"/"deck"/process narration). Chrome + sources are shared with the
sibling ceiling slides; Sources sits at this deck's ported y=6_085_448. Numbers
are kept in sync with the workbook headline and the sibling slides by hand (this
build is NOT wired to the workbook): the portfolio-weighted reads ~25% / ~51% /
~76% match the results exhibit's floor->ceiling reads. The by-program result
table is intentionally absent - the results exhibit that follows carries it.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell,
)
from deck_core.style import (
    BODY_X, BODY_CX, BODY_R, BLACK, GRAY_1, GRAY_5, FONT,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    RIBBON_KPI_18PT, INSETS_CARD, INSETS_CHIP, INSETS_NONE, blue_pair,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

# ── Chrome text (shared with the sibling ceiling slides) ─────────────────────
_SECTION = "Executive Summary"
_TOPIC_LABEL = "Supplier TAM and SAM"
_TOPIC = "Outsourcing Ceiling"
_TAKEAWAY = ("The maximum supplier share is built from the must-stay core and a "
             "material pass-through dial.")
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

# ── Two-zone layout: LEFT/center build zone + RIGHT ledger rail ──────────────
_LEFT_X = BODY_X
_LEFT_CX = 7_500_000
_ZONE_CX = _LEFT_X + _LEFT_CX // 2             # left-zone center axis
_RAIL_X = _LEFT_X + _LEFT_CX + 180_000         # gutter between zones
_RAIL_CX = BODY_R - _RAIL_X

_CONN_PT = 9525                                # ¾pt black flow weight — heavier
#                                              # than the ½pt hairline so the short
#                                              # connector runs read with presence

# ── Framer: why the ceiling is built, not looked up (one no-fill line) ───────
_FRAMER_Y, _FRAMER_H = 1_380_000, 300_000


def _framer() -> str:
    return text_box(
        10, "Framer", BODY_X, _FRAMER_Y, BODY_CX, _FRAMER_H,
        [paragraph([
            run("No budget line splits must-stay assembly from outsourceable "
                "work. ", size=LABEL_9PT, bold=True, color=BLACK, font=FONT),
            run("Published place-of-performance (POP) sets today's floor, so the "
                "ceiling is built from Basic Construction, labor share, movable "
                "hours, and material pass-through.", size=LABEL_9PT, color=BLACK,
                font=FONT)])],
        fill=None, anchor="ctr", insets=INSETS_NONE)


# ── The build machine: four-box flow, left to right ──────────────────────────
# (ramp index, number, title, [sublines]). The ramp climbs base -> mechanics ->
# core -> ceiling but stops at BLUE_4 (no BLUE_5), so no single box over-weights.
_FLOW_Y, _BOX_H = 1_800_000, 960_000
_BOX_GAP = 380_000                            # roomy gap -> connectors with travel
_BOX_W = (_LEFT_CX - 3 * _BOX_GAP) // 4
_BOX_PITCH = _BOX_W + _BOX_GAP
_FLOW_B = _FLOW_Y + _BOX_H
_FLOW_MID = _FLOW_Y + _BOX_H // 2
# Trimmed side insets (0.1" vs INSETS_CARD's 0.125") so the sublines breathe in
# these compact four-across boxes; vertical insets stay on the card value.
_BOX_INSETS = (91_440, 76_200, 91_440, 76_200)

_BOXES = [
    (0, "1", "Addressable base",
     ["FY22–27 Basic Construction", "Excludes GFE and non-BC cost"]),
    (1, "2", "Labor mechanics",
     ["h = movable labor-hour share", "L = labor share of BC"]),
    (2, "3", "Must-stay core",
     ["Core = L × (1 − h)", "Final assembly, integration, test"]),
    (3, "4", "Structural ceiling",
     ["Ceiling = 1 − core", "Maximum outsourceable share"]),
]


def _box_x(i: int) -> int:
    return _LEFT_X + i * _BOX_PITCH


def _flow() -> str:
    parts = []
    for i, (ramp, num, title, subs) in enumerate(_BOXES):
        fill, txt = blue_pair(ramp)
        paras = [paragraph([run(f"{num}.  {title}", size=LABEL_9PT, bold=True,
                                color=txt, font=FONT)], space_after=100)]
        paras += [paragraph([run(s, size=FINEPRINT_8_5PT, color=txt, font=FONT)],
                            space_after=60) for s in subs]
        parts.append(text_box(20 + i, f"Box{i + 1}", _box_x(i), _FLOW_Y,
                              _BOX_W, _BOX_H, paras, fill=fill, anchor="ctr",
                              insets=_BOX_INSETS))
    # three black arrows that touch both boxes: tail on box i's right edge,
    # arrowhead on box i+1's left edge (the full gap is the connector run)
    for i in range(3):
        x = _box_x(i) + _BOX_W
        parts.append(connector(30 + i, f"Step{i + 1}to{i + 2}", x, _FLOW_MID,
                              _BOX_GAP, 0, arrow=True,
                              width=_CONN_PT, color=BLACK))
    return "".join(parts)


# ── The bridge: structural ceiling -> formula node -> three reads ────────────
# The dial drops from the STRUCTURAL CEILING box (not the page center): the p-dial
# belongs after the core/ceiling identity. The formula node is the bridge that
# resolves hours -> dollars; its bottom edge is the distribution bus that ticks
# down into the three read cards.
_CEIL_CX = _box_x(3) + _BOX_W // 2            # structural-ceiling box center

_FORMULA_Y, _FORMULA_H = 3_090_000, 420_000
_FORMULA_B = _FORMULA_Y + _FORMULA_H
_FORMULA_INSETS = (114_300, 40_000, 114_300, 40_000)

# the dial drop touches both ends: ceiling-box bottom edge -> formula top edge
_DIAL_DROP_Y = _FLOW_B
_DIAL_DROP_CY = _FORMULA_Y - _FLOW_B


def _dial_drop() -> str:
    return connector(33, "DialDrop", _CEIL_CX, _DIAL_DROP_Y, 0, _DIAL_DROP_CY,
                     arrow=True, width=_CONN_PT, color=BLACK)


def _formula() -> str:
    return text_box(
        34, "BridgeFormula", _LEFT_X, _FORMULA_Y, _LEFT_CX, _FORMULA_H,
        [paragraph([run("Dollarized supplier share = hL + p(1 − L)",
                        size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=60),
         paragraph([run("p sets how much non-labor material travels with "
                        "outsourced packages.", size=FINEPRINT_8_5PT,
                        italic=True, color=BLACK, font=FONT)], align="ctr")],
        fill=GRAY_1, anchor="ctr", insets=_FORMULA_INSETS)


# ── Three reads: the same build dialed up (blue-ramp progression) ────────────
# (cap, value, sub, ramp index). One shared weight - the results exhibit owns the
# headline, so p=100% gets a darker fill but NO hero badge (no oversized value,
# no 1.5pt border).
_READS_Y, _READS_H = 3_690_000, 1_140_000
_READ_GAP = 200_000
_READ_W = (_LEFT_CX - 2 * _READ_GAP) // 3
_TICK_CY = _READS_Y - _FORMULA_B              # bridge bus -> card top
_READS = [
    ("p = 0", "~25%", "Movable labor only", 0),
    ("p = 50%", "~51%", "Selected working case", 1),
    ("p = 100%", "~76%", "Material-inclusive ceiling", 3),
]


def _read_x(i: int) -> int:
    return _LEFT_X + i * (_READ_W + _READ_GAP)


def _reads() -> str:
    parts = []
    for i, (cap, val, sub, ramp) in enumerate(_READS):
        fill, txt = blue_pair(ramp)
        x = _read_x(i)
        parts.append(text_box(
            40 + i, f"Read{i + 1}", x, _READS_Y, _READ_W, _READS_H,
            [paragraph([run(cap, size=LABEL_9PT, bold=True, color=txt,
                            font=FONT)], align="ctr", space_after=160),
             paragraph([run(val, size=RIBBON_KPI_18PT, bold=True, color=txt,
                            font=FONT)], align="ctr", space_after=160),
             paragraph([run(sub, size=FINEPRINT_8_5PT, italic=True, color=txt,
                            font=FONT)], align="ctr")],
            fill=fill, anchor="ctr", insets=INSETS_CARD))
        # tick from the bridge bus (formula bottom) down into this card
        parts.append(connector(37 + i, f"Tick{i + 1}", x + _READ_W // 2,
                              _FORMULA_B, 0, _TICK_CY, arrow=True,
                              width=_CONN_PT, color=BLACK))
    return "".join(parts)


# ── Lever ledger: the four variables, each with basis and role ───────────────
_LED_HEADER = ["Lever", "Basis", "Role in estimate"]
_LED_ROWS = [
    ["h", "Sourced for submarines; DDG-51 judgment", "Movable labor-hour share"],
    ["L", "Sourced total-cost anchor, rebased to BC",
     "Labor share of Basic Construction"],
    ["p", "Scenario input", "Material pass-through share"],
    ["POP", "Announced place-of-performance", "Current floor"],
]
_LED_ALL = [_LED_HEADER] + _LED_ROWS
_LED_COL_W = [520_000, 1_700_000, 1_382_362]   # sum = _RAIL_CX
assert sum(_LED_COL_W) == _RAIL_CX, "ledger columns must sum to the rail width"
_LED_SZ = LABEL_9PT
_LED_ALIGNS = ["ctr", "l", "l"]
_LED_ROW_H = estimate_row_heights(_LED_ALL, _LED_COL_W, size_pt=_LED_SZ / 100.0)
_LED_CY = sum(_LED_ROW_H)
_LED_LAST = len(_LED_ALL) - 1

_RAIL_CAP_Y, _RAIL_CAP_H = 1_800_000, 380_000
_LED_Y = _RAIL_CAP_Y + _RAIL_CAP_H + 60_000
_RAIL_NOTE_Y = _LED_Y + _LED_CY + 120_000
_RAIL_NOTE_H = 560_000

_RULE_HEADER = {"color": BLACK, "width": 19_050}    # 1.5pt under the header
_RULE_BODY = {"color": GRAY_5, "width": 6_350}      # ½pt between body rows


def _rail_caption() -> str:
    return text_box(
        50, "LedgerCaption", _RAIL_X, _RAIL_CAP_Y, _RAIL_CX, _RAIL_CAP_H,
        [paragraph([run("Key levers and basis. ", size=DENSE_BODY_10PT,
                        bold=True, color=BLACK, font=FONT),
                    run("Each input is sourced, derived, or an explicit "
                        "assumption.", size=DENSE_BODY_10PT, color=BLACK,
                        font=FONT)])],
        fill=None, anchor="t", insets=INSETS_NONE)


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
    return table(51, "LeverLedger", _RAIL_X, _LED_Y, _RAIL_CX, _LED_CY,
                 col_widths=_LED_COL_W, rows=rows)


def _rail_note() -> str:
    return text_box(
        52, "RailNote", _RAIL_X, _RAIL_NOTE_Y, _RAIL_CX, _RAIL_NOTE_H,
        [paragraph([run("L starts from a total-cost labor anchor and is rebased "
                        "to Basic Construction. p moves the dollarized supplier "
                        "share, so the estimate is read as a range, not a single "
                        "point.", size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, anchor="t", insets=INSETS_NONE)


# ── Guardrail chips: pre-empt the three predictable challenges ───────────────
_CHIPS = ["p = 100% is the upper bound; p = 50% is the working case",
          "DDG-51 h and L are explicit assumptions",
          "POP sets today's floor, not the ceiling"]
_GUARD_GAP = 200_000
_GUARD_W = (BODY_CX - 2 * _GUARD_GAP) // 3
_GUARD_Y, _GUARD_H = 4_960_000, 420_000

assert _GUARD_Y + _GUARD_H <= _BOTTOM, (
    "guardrail chips pushed past the body bottom - tighten the flow/reads band")
assert _READS_Y + _READS_H <= _GUARD_Y, "read cards overlap the guardrail band"
assert _RAIL_NOTE_Y + _RAIL_NOTE_H <= _GUARD_Y, "rail note overlaps the guardrails"


def _guardrails() -> str:
    parts = []
    for i, text in enumerate(_CHIPS):
        x = BODY_X + i * (_GUARD_W + _GUARD_GAP)
        parts.append(text_box(
            60 + i, f"Guard{i + 1}", x, _GUARD_Y, _GUARD_W, _GUARD_H,
            [paragraph([run(text, size=LABEL_9PT, color=BLACK, font=FONT)],
                       align="ctr")],
            fill=GRAY_1, anchor="ctr", insets=INSETS_CHIP))
    return "".join(parts)


def _body() -> str:
    return (_framer()
            + _flow() + _dial_drop() + _formula() + _reads()
            + _rail_caption() + _ledger() + _rail_note()
            + _guardrails())


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC_LABEL)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES, y=_SOURCES_Y)
    )
