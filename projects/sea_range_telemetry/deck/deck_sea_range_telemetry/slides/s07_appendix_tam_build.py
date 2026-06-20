"""s07_appendix_tam_build - explain how the model converts evidence into the current
annual TAM before any ASV addressability filters: contracts are recognized and
annualized, budgets are sliced to maritime instrumentation, the U.S. TAM is bridged
through defined segments, and Europe TAM is built from country / segment anchors.
Vessel share, role share, event SAM, and overlap logic are SAM-stage, not TAM, concepts.

One native table (the U.S. TAM bridge) carries the numeric build; everything else is
shape-built. A four-group formula machine runs under the output chip (recognize ->
annualize -> allocate -> bridge), and a right-side Europe TAM support stack sums the
U.K. anchor, the non-U.K. floor, and the modeled gap into Europe modeled TAM. A dark
caveat strip keeps SAM-stage concepts out of the TAM page.

Spec: specs/alternative_v1/03_tam_build.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.text_metrics import estimate_row_heights
from deck_sea_range_telemetry.slides._house import dark_table
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "TAM Build"
_TOPIC            = "TAM Build"
_TAKEAWAY = ("Contracts, budgets, and country anchors create the annual spend pool "
             "before ASV scoring.")
_SOURCES = ("Sources: (1) TAM Build tab; (2) Data Contracts TAM factors and "
            "recognized-TAM detail; (3) Data Budget PE allocation and NAVAIR layer; "
            "(4) Data Europe modeled spend bands; (5) Assumptions tab")

_CAPTION = ("TAM is the annual spend pool before ASV addressability. It is expressed "
            "in USD $M per year and built separately for the U.S. and Europe.")
_STEP = "STEP 3 / 4 — TAM ENGINE"
_OUTPUT = "Current annual TAM is $1,595.5M base: U.S. $1,388.5M and Europe $207.0M."
_CAVEAT_LEAD = "TAM boundary: "
_CAVEAT = ("TAM does not use vessel share, role share, event-derived SAM, Pacific "
           "MRIS overlap, or ASV adoption assumptions. Those are SAM-stage concepts.")

# Raw sizes (style.py permits raw sizes with a nearby comment).
_SZ_CHIP_HDR = 900    # 9pt output chip / table+stack label
_SZ_CHIP_BODY = 850   # 8.5pt caption / step marker
_SZ_FT = 1000         # 10pt formula-machine band title
_SZ_FC_HDR = 820      # 8.2pt formula-card header
_SZ_FC_BODY = 780     # 7.8pt formula-card body
_SZ_OP = 1100         # 11pt operator chip
_SZ_TBL = 810         # 8.1pt table body
_SZ_TBL_HDR = 850     # 8.5pt table header
_SZ_EUR_NAME = 800    # 8pt europe-card name
_SZ_EUR_VAL = 1200    # 12pt europe-card value
_SZ_EUR_SUB = 700     # 7pt europe-card subline
_SZ_CAVEAT = 950      # 9.5pt caveat strip

# ── Vertical band geometry (all EMU) ─────────────────────────────────────────
_CAP_Y, _CAP_H   = BODY_Y, 170_000
_CHIP_Y, _CHIP_H = BODY_Y + 190_000, 270_000
_FT_Y, _FT_H     = _CHIP_Y + _CHIP_H + 35_000, 160_000     # formula title
_FG_Y            = _FT_Y + _FT_H + 10_000                  # formula groups
_GROUP_H = 470_000
_FG_GAP = 40_000
_FG_B = _FG_Y + 2 * _GROUP_H + _FG_GAP

_CAV_H = 480_000
_CAV_Y = BODY_B - _CAV_H                                    # 5_390_000
_BR_Y = _FG_B + 60_000                                      # bridge zone
_BR_B = _CAV_Y - 80_000

# ── Formula-machine group geometry (2 x 2) ───────────────────────────────────
_GROUP_GAP = 300_000
_GW = (BODY_CX - _GROUP_GAP) // 2                           # 5_491_181
_OP_W = 320_000
_IG = 30_000
_FC_W = (_GW - 2 * _OP_W - 4 * _IG) // 3                    # formula-card width
_GX_L = BODY_X
_GX_R = BODY_X + _GW + _GROUP_GAP

# ── Bridge zone columns: native table (left) + Europe stack (right) ──────────
_UST_X = BODY_X
_UST_W = 7_200_000
_EUR_X = BODY_X + 7_300_000
_EUR_W = BODY_R - _EUR_X
_UST_LABEL_H = 190_000
_UST_TOP = _BR_Y + _UST_LABEL_H

# Europe stack: reserve a left gutter for the +/+/= arithmetic chips so they sit
# beside the cards (in empty space) instead of overlapping the card sublines.
_EUR_GUTTER = 470_000
_EUR_CARD_X = _EUR_X + _EUR_GUTTER
_EUR_CARD_W = _EUR_W - _EUR_GUTTER

# ── Step marker / caption band ───────────────────────────────────────────────
_STEP_W = 2_150_000
_STEP_X = BODY_R - _STEP_W
_CAP_W = _STEP_X - 60_000 - BODY_X

# ── Content ──────────────────────────────────────────────────────────────────
# Formula groups: each is (c1, op1, c2, op2, c3); a card is (header, body|None).
_GROUPS = [
    (("Reported contract value", "obligated / awarded / ceiling / annual"), "×",
     ("TAM factors", "relevance × maritime × instrumentation"), "=",
     ("Recognized contract TAM", "only in-scope portion counts")),
    (("Recognized contract TAM", None), "÷",
     ("Years in PoP", "max(1, end - start + 1)"), "=",
     ("Annual contract TAM", "annual rows are not re-divided")),
    (("FY27 PB", "program element budget line"), "×",
     ("Maritime instrumentation share", None), "=",
     ("PE maritime slice", None)),
    (("U.S. segment bridge", "vessel + telemetry + allocated + NAVAIR + commercial"),
     "+",
     ("Europe modeled anchors", "Σ country / segment modeled spend"), "=",
     ("Total TAM", "U.S. + Europe")),
]

_UST_COL_W = [2_400_000, 1_150_000, 1_150_000, 2_500_000]   # sum 7_200_000
_UST_ROWS = [
    ["SEGMENT", "BASE ($M / YR)", "SHARE OF U.S. TAM", "TREATMENT"],
    ["Vessel-operator prime spending", "$492.5M", "35.5%",
     "Composite estimate from vessel / range-support IDIQs"],
    ["Telemetry, range-support, data-processing", "$425.0M", "30.6%",
     "Range-services primes and task orders"],
    ["Allocated platform and range-support work", "$200.0M", "14.4%",
     "Mixed-scope platform / range-support allocation"],
    ["NAVAIR aviation maritime-range layer", "$241.0M", "17.4%",
     "Calculated from six NAVAIR / aviation range sub-rows"],
    ["Commercial / institutional launch TAM", "$30.0M", "2.2%",
     "Explicit base case, not midpoint"],
    ["U.S. TAM", "$1,388.5M", "100.0%", "Defense + commercial current annual pool"],
]
_UST_ALIGNS = ["l", "r", "r", "l"]
_UST_ROW_H = estimate_row_heights(_UST_ROWS, _UST_COL_W, size_pt=8.1,
                                  header_size_pt=8.5, min_row_h=255_000)
# NAVAIR row (4) shaded BLUE_1 (calculated); U.S. TAM total row (6) shaded GRAY_2.
# Value column bold on every row; total row bold across all cells.
_UST_CELL_FILLS, _UST_CELL_BOLD = {}, {}
for _c in range(4):
    _UST_CELL_FILLS[(4, _c)] = BLUE_1
    _UST_CELL_FILLS[(6, _c)] = GRAY_2
    _UST_CELL_BOLD[(6, _c)] = True
for _r in range(1, 7):
    _UST_CELL_BOLD[(_r, 1)] = True

# Europe stack cards: (name, value, subline, fill, fg).
_EUR_CARDS = [
    ("U.K. public-record anchor", "$130.0M base",
     "LTPA, MSCA, DragonFire vessel-relevant activity", BLUE_1, BLACK),
    ("Non-U.K. public-record floor", "$9.5M base",
     "visible lower-bound support from selected public records", GRAY_1, BLACK),
    ("Modeled non-U.K. gap", "$67.5M base",
     "explicit modeled gap where public visibility is incomplete", GRAY_1, BLACK),
    ("Europe modeled TAM", "$207.0M base",
     "country / segment modeled annual spend", BLUE_4, WHITE),
]
_EUR_OPS = ["+", "+", "="]


# ── Local helpers ────────────────────────────────────────────────────────────
def _formula_card(sp_id, x, y, w, h, header, body) -> str:
    paras = [paragraph([run(header, size=_SZ_FC_HDR, bold=True, color=BLACK, font=FONT)],
                       align="ctr", space_after=(35 if body else 0),
                       line_spacing=100_000)]
    if body:
        paras.append(paragraph([run(body, size=_SZ_FC_BODY, color=BLACK, font=FONT)],
                               align="ctr", line_spacing=100_000))
    return text_box(sp_id, "FormulaCard", x, y, w, h, paras, fill=WHITE, anchor="ctr",
                    insets=(55_000, 30_000, 55_000, 30_000))


def _op_chip(sp_id, x, y, w, h, sym) -> str:
    return text_box(sp_id, "OperatorChip", x, y, w, h,
                    [paragraph([run(sym, size=_SZ_OP, bold=True, color=BLACK,
                                    font=FONT)], align="ctr")],
                    fill=GRAY_2, anchor="ctr", insets=INSETS_NONE)


def _group(base_id, gx, gy, spec) -> str:
    c1, op1, c2, op2, c3 = spec
    op_h = 320_000
    op_y = gy + (_GROUP_H - op_h) // 2
    x = gx
    parts = [_formula_card(base_id, x, gy, _FC_W, _GROUP_H, *c1)]
    x += _FC_W + _IG
    parts.append(_op_chip(base_id + 1, x, op_y, _OP_W, op_h, op1))
    x += _OP_W + _IG
    parts.append(_formula_card(base_id + 2, x, gy, _FC_W, _GROUP_H, *c2))
    x += _FC_W + _IG
    parts.append(_op_chip(base_id + 3, x, op_y, _OP_W, op_h, op2))
    x += _OP_W + _IG
    parts.append(_formula_card(base_id + 4, x, gy, _FC_W, _GROUP_H, *c3))
    return "".join(parts)


def _eur_card(sp_id, y, h, name, value, subline, fill, fg) -> str:
    return text_box(
        sp_id, "EuropeCard", _EUR_CARD_X, y, _EUR_CARD_W, h,
        [paragraph([run(name, size=_SZ_EUR_NAME, bold=True, color=fg, font=FONT)],
                   space_after=30, line_spacing=100_000),
         paragraph([run(value, size=_SZ_EUR_VAL, bold=True, color=fg, font=FONT)],
                   space_after=30, line_spacing=100_000),
         paragraph([run(subline, size=_SZ_EUR_SUB, color=fg, font=FONT)],
                   line_spacing=100_000)],
        fill=fill, anchor="ctr", insets=(110_000, 30_000, 90_000, 30_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, _CAP_W, _CAP_H,
        [paragraph([run(_CAPTION, size=_SZ_CHIP_BODY, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    step = text_box(
        11, "StepMarker", _STEP_X, _CAP_Y, _STEP_W, _CAP_H,
        [paragraph([run(_STEP, size=_SZ_CHIP_BODY, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_1, anchor="ctr", insets=(60_000, 20_000, 60_000, 20_000))
    output = text_box(
        12, "OutputChip", BODY_X, _CHIP_Y, BODY_CX, _CHIP_H,
        [paragraph([run(_OUTPUT, size=_SZ_CHIP_HDR, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_1, anchor="ctr", insets=(150_000, 30_000, 150_000, 30_000))

    ft = text_box(
        13, "FormulaTitle", BODY_X, _FT_Y, BODY_CX, _FT_H,
        [paragraph([run("TAM conversion logic — recognize, annualize, allocate, and "
                        "bridge", size=_SZ_FT, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    groups = (_group(100, _GX_L, _FG_Y, _GROUPS[0])
              + _group(110, _GX_R, _FG_Y, _GROUPS[1])
              + _group(120, _GX_L, _FG_Y + _GROUP_H + _FG_GAP, _GROUPS[2])
              + _group(130, _GX_R, _FG_Y + _GROUP_H + _FG_GAP, _GROUPS[3]))

    # U.S. TAM bridge table (the one native table on this slide).
    ust_label = text_box(
        40, "UsTamLabel", _UST_X, _BR_Y, _UST_W, _UST_LABEL_H,
        [paragraph([run("U.S. TAM bridge — base-case annual spend pool",
                        size=_SZ_CHIP_HDR + 100, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    table = dark_table(41, "UsTamBridge", _UST_X, _UST_TOP, _UST_COL_W, _UST_ROWS,
                       _UST_ROW_H, aligns=_UST_ALIGNS, size=_SZ_TBL,
                       header_size=_SZ_TBL_HDR, cell_fills=_UST_CELL_FILLS,
                       cell_bold=_UST_CELL_BOLD)

    # Europe TAM support stack: dark header + three input cards + total, with
    # +/+/= operator chips overlaid on the gaps between cards.
    eur_hdr = text_box(
        50, "EuropeHeader", _EUR_X, _BR_Y, _EUR_W, 250_000,
        [paragraph([run("EUROPE TAM — MODELED COUNTRY / SEGMENT ANCHORS",
                        size=_SZ_CHIP_HDR, bold=True, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=BLUE_5, anchor="ctr", insets=(90_000, 18_000, 90_000, 18_000))
    eur_start = _BR_Y + 250_000 + 20_000
    eur_gap = 30_000
    eur_ch = (_BR_B - eur_start - 3 * eur_gap) // 4
    cards = []
    ops = []
    for k in range(4):
        y = eur_start + k * (eur_ch + eur_gap)
        cards.append(_eur_card(51 + k, y, eur_ch, *_EUR_CARDS[k]))
        if k < 3:
            gap_mid = y + eur_ch + eur_gap // 2
            op_h = 200_000
            op_w = 360_000
            ops.append(_op_chip(55 + k, _EUR_X + (_EUR_GUTTER - op_w) // 2,
                                gap_mid - op_h // 2, op_w, op_h, _EUR_OPS[k]))

    caveat = text_box(
        60, "Caveat", BODY_X, _CAV_Y, BODY_CX, _CAV_H,
        [paragraph([run(_CAVEAT_LEAD, size=_SZ_CAVEAT, bold=True, color=WHITE,
                        font=FONT),
                    run(_CAVEAT, size=_SZ_CAVEAT, color=WHITE, font=FONT)],
                   line_spacing=106_000)],
        fill=BLUE_5, anchor="ctr", insets=(160_000, 40_000, 160_000, 40_000))

    # Paint order: cards first, operator chips on top of the gaps between them.
    return (caption + step + output + ft + groups + ust_label + table
            + eur_hdr + "".join(cards) + "".join(ops) + caveat)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
