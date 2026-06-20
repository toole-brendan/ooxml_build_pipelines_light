"""outsourcing_ceiling_method - how the outsourcing ceiling is sized: two sourced
numbers, built up into a core-and-ceiling identity, read at three values of the
material dial.

Slide-form companion to the Outsourcing Ceiling methodology doc
(projects/distributed_shipbuilding/doc/doc_outsourced_ceiling/pages/
ceiling_methodology_explainer.py). It sizes the OUTSOURCEABLE POOL - the
look-forward upper bound that the competability work scores for what inside it
is contestable. It closes the deck as the final methodology slide.

Built fresh (no _chart_xml source, no native chart). A left-to-right build-up
flow over a full-width result table, in five bands top to bottom:

  - Framer (no-fill): the clean split isn't published and the place-of-performance share
    is a floor, so the ceiling is BUILT from two sourced numbers.
  - Flow band: TWO INPUTS (h, L, each BLUE_1, sourced) -> THE ENGINE (BLUE_1, the
    core/ceiling identity + the material dial p) -> THREE READS (a blue-ramp
    progression p=0 / p~50 / p=100, the same build dialed up). The p=100 ceiling
    read is the slide's one focal object: a BLUE_5 1.5pt answer badge.
  - Exhibit caption + Table 1 (house_table, skin "rule"): core / selected /
    ceiling / vs-floor by program, the Portfolio rollup row set off.
  - Guardrail (no-fill): the four doc caveats compressed to one line.

Two clean orthogonal connector sets carry the flow (inputs -> engine ->
reads). Distinct silhouette from the table+rail competability slide and the
vertical-band jump-ball slide. Palette stays on the house BLUE_*/GRAY_* ramps;
the GS&O reference archetypes informed the flow structure, not the colors.

Chrome (breadcrumb / Preliminary chip / title / sources) comes from the
deck_core builders; Sources sits at this deck's ported y=6_085_448, matching the
sibling new slides.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell,
)
from deck_core.style import (
    BODY_X, BODY_CX, BODY_R, BLACK, BLUE_1, GRAY_1, GRAY_5, FONT,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, CAP_12PT, RIBBON_KPI_18PT, ANSWER_KPI_24PT,
    INSETS_CARD, INSETS_NONE, blue_pair,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION = "Executive Summary"            # deck-wide breadcrumb
_TOPIC_LABEL = "Supplier TAM and SAM"
_TOPIC = "Outsourcing Ceiling"
_TAKEAWAY = ("Built from two published numbers, the ceiling reaches ~75% of "
             "Basic Construction, ~3x the place-of-performance floor.")
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
_SOURCES_Y = 6_085_448      # this deck's ported chrome carries Sources here
_BOTTOM = 6_023_400         # body bottom edge (sibling new slides)

# ── Band geometry (top to bottom) ────────────────────────────────────────────
_FRAMER_Y, _FRAMER_H = 1_390_000, 300_000
_FLOW_Y, _FLOW_H = 1_790_000, 1_360_000
_CAP_Y, _CAP_H = 3_320_000, 250_000
_TBL_Y = 3_640_000

# ── Flow band: horizontal zones (inputs -> engine -> reads) ──────────────────
_IN_X, _IN_W = BODY_X, 2_600_000                       # two stacked input chips
_CONN_W = 520_000                                      # connector gap, both sides
_ENG_X, _ENG_W = _IN_X + _IN_W + _CONN_W, 2_900_000    # the engine card
_READ_X = _ENG_X + _ENG_W + _CONN_W                    # three-read ramp
_READ_W_TOTAL = BODY_R - _READ_X
_READ_GAP = 120_000
_READ_W = (_READ_W_TOTAL - 2 * _READ_GAP) // 3

_IN_GAP = 100_000
_IN_H = (_FLOW_H - _IN_GAP) // 2                        # ~630k - 3 snug lines each
_IN_H_CY = _IN_X + _IN_W                                # inputs right edge (conn start)

# Reads sit shorter than the band and vertically centered, so the panels stay
# snug around the cap / value / sublabel rather than stranding whitespace.
_READ_H = 860_000
_READ_Y = _FLOW_Y + (_FLOW_H - _READ_H) // 2


# ── Framer: why the ceiling is built, not looked up (one no-fill line) ───────
def _framer() -> str:
    return text_box(
        10, "Framer", BODY_X, _FRAMER_Y, BODY_CX, _FRAMER_H,
        [paragraph(
            [run("The clean split is not published, and the place-of-performance "
                 "share is only a floor, ", size=LABEL_9PT, bold=True, color=BLACK,
                 font=FONT),
             run("so the ceiling is built from two sourced numbers, not read off "
                 "a budget line.", size=LABEL_9PT, color=BLACK, font=FONT)])],
        fill=None, anchor="ctr", insets=INSETS_NONE)


# ── Two inputs (sourced; the build rests on these) ───────────────────────────
def _input_chip(sp_id: int, name: str, y: int, headline: str, what: str,
                source: str) -> str:
    return text_box(
        sp_id, name, _IN_X, y, _IN_W, _IN_H,
        [paragraph([run(headline, size=CAP_12PT, bold=True, color=BLACK,
                        font=FONT)], space_after=120),
         paragraph([run(what, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
                   space_after=120),
         paragraph([run(source, size=SOURCES_8PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=BLUE_1, anchor="ctr", insets=INSETS_CARD)


def _inputs() -> str:
    h_chip = _input_chip(
        20, "InputH", _FLOW_Y, "h ~50%",
        "Build hours that can leave the yard",
        "Navy submarine program executive, 2022")
    l_chip = _input_chip(
        21, "InputL", _FLOW_Y + _IN_H + _IN_GAP, "L ~50% / 45%",
        "Labor share of Basic Construction",
        "CRS testimony 2025, cost index 2024")
    return h_chip + l_chip


# ── The engine: the core/ceiling identity + the material dial ────────────────
def _engine() -> str:
    return text_box(
        30, "Engine", _ENG_X, _FLOW_Y, _ENG_W, _FLOW_H,
        [paragraph([run("THE MODEL", size=CAP_12PT, bold=True, color=BLACK,
                        font=FONT)], space_after=200),
         paragraph([run("core = L (1 − h)", size=DENSE_BODY_10PT,
                        bold=True, color=BLACK, font=FONT)], space_after=80),
         paragraph([run("The labor that must stay: assembly, integration, test",
                        size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)], space_after=200),
         paragraph([run("ceiling = 1 − core", size=DENSE_BODY_10PT,
                        bold=True, color=BLACK, font=FONT)], space_after=200),
         paragraph([run("Dial p ", size=FINEPRINT_8_5PT, bold=True, color=BLACK,
                        font=FONT),
                    run("= the share of a package's material that travels out "
                        "with the work", size=FINEPRINT_8_5PT, italic=True,
                        color=BLACK, font=FONT)])],
        fill=BLUE_1, anchor="ctr", insets=INSETS_CARD)


# ── Three reads: the same build dialed up (blue-ramp progression) ────────────
# (cap, value, sub, ramp index, focal). The p=100 ceiling is the one focal
# object - the BLUE_5 1.5pt answer badge (the slide's single heavy family).
_READS = [
    ("p = 0", "~25%", "Labor-only", 0, False),
    ("p ≈ 50%", "~50%", "Working case", 2, False),
    ("p = 100%", "~75%", "Ceiling", 4, True),
]


def _reads() -> str:
    parts = []
    for i, (cap, val, sub, ramp, focal) in enumerate(_READS):
        fill, txt = blue_pair(ramp)
        val_sz = ANSWER_KPI_24PT if focal else RIBBON_KPI_18PT
        x = _READ_X + i * (_READ_W + _READ_GAP)
        parts.append(text_box(
            40 + i, f"Read{i + 1}", x, _READ_Y, _READ_W, _READ_H,
            [paragraph([run(cap, size=LABEL_9PT, bold=True, color=txt,
                            font=FONT)], align="ctr", space_after=160),
             paragraph([run(val, size=val_sz, bold=True, color=txt, font=FONT)],
                       align="ctr", space_after=160),
             paragraph([run(sub, size=FINEPRINT_8_5PT, italic=True, color=txt,
                            font=FONT)], align="ctr")],
            fill=fill, anchor="ctr", insets=INSETS_CARD,
            line_width=19050 if focal else 12700))   # 1.5pt focal on the ceiling
    return "".join(parts)


# ── Flow connectors: inputs -> engine, engine -> reads ───────────────────────
# ½pt black (flow weight, not emphasis). The two inputs sit at a different height
# than the engine's center, so they converge via elbow (bentConnector3) right
# angles rather than diagonals; the engine -> reads hop is a straight run.
_CONN_W_PT = 6350      # ½pt - house flow-line weight


def _flow() -> str:
    eng_mid = _FLOW_Y + _FLOW_H // 2
    h_mid = _FLOW_Y + _IN_H // 2
    l_mid = _FLOW_Y + _IN_H + _IN_GAP + _IN_H // 2
    parts = [
        connector(50, "InHtoEngine", _IN_H_CY, h_mid, _CONN_W, eng_mid - h_mid,
                  arrow=True, width=_CONN_W_PT, prst="bentConnector3"),
        connector(51, "InLtoEngine", _IN_H_CY, l_mid, _CONN_W, eng_mid - l_mid,
                  arrow=True, width=_CONN_W_PT, prst="bentConnector3"),
        connector(52, "EngineToReads", _ENG_X + _ENG_W, eng_mid, _CONN_W, 0,
                  arrow=True, width=_CONN_W_PT),
        # connector note: the dial sweeping its full range (deliberate flow)
        text_box(60, "DialNote", _ENG_X + _ENG_W, eng_mid - 300_000, _CONN_W,
                 260_000,
                 [paragraph([run("Dial p", size=CONNECTOR_NOTE_8_5PT,
                                 italic=True, color=BLACK, font=FONT)],
                            align="ctr")],
                 fill=None, anchor="b", insets=INSETS_NONE),
    ]
    return "".join(parts)


# ── Result table: core / selected / ceiling / vs-floor, by program ───────────
# Mirrors the workbook headline and the methodology doc's RESULT_ROWS (the two
# are kept in sync by hand; this slide is NOT wired to the workbook). vs-floor
# multiples carry the house tilde and a plain lowercase "x".
#
# Built on the low-level table() (not house_table) for the house bottom-rule
# treatment house_table can't express per row: a 1.5pt black rule under the
# header, light ½pt GRAY_5 rules between body rows (the slide_guide alternative,
# matching the reference decks), a 1pt black rule above the Portfolio rollup to
# set the total off, and no rule under the last row.
_TBL_HEADER = ["Program", "Must stay (core)", "Selected (p ≈ 50%)",
               "Ceiling (p = 100%)", "vs. floor"]
_TBL_ROWS = [
    ["Virginia", "25%", "50%", "75%", "~2.2x"],
    ["Columbia", "25%", "50%", "75%", "~3.4x"],
    ["DDG-51", "20%", "52%", "80%", "~6.1x"],
    ["Portfolio", "24%", "51%", "76%", "~3.0x"],
]
_TBL_COL_W = [1_900_000, 2_200_000, 2_300_000, 2_300_000, 2_582_362]   # sum BODY_CX
assert sum(_TBL_COL_W) == BODY_CX, "table columns must sum to BODY_CX"

_TBL_SZ = DENSE_BODY_10PT
_TBL_ALIGNS = ["l", "ctr", "ctr", "ctr", "ctr"]
_TBL_ALL = [_TBL_HEADER] + _TBL_ROWS
_TBL_ROW_H = estimate_row_heights(_TBL_ALL, _TBL_COL_W, size_pt=_TBL_SZ / 100.0)
_TBL_CY = sum(_TBL_ROW_H)
_PORTFOLIO_RI = len(_TBL_ALL) - 1     # rollup row, set off with a light fill + bold

_RULE_HEADER = {"color": BLACK, "width": 19_050}     # 1.5pt under the header
_RULE_BODY = {"color": GRAY_5, "width": 6_350}       # ½pt light gray between rows
_RULE_TOTAL = {"color": BLACK, "width": 12_700}      # 1pt above the rollup total


def _caption() -> str:
    return text_box(
        70, "TableCaption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run("By program: ", size=DENSE_BODY_10PT, bold=True,
                        color=BLACK, font=FONT),
                    run("core, selected case, and ceiling, as a share of Basic "
                        "Construction", size=DENSE_BODY_10PT, color=BLACK,
                        font=FONT)])],
        fill=None, anchor="b", insets=INSETS_NONE)


def _row_border(ri: int) -> dict:
    """Bottom rule for row ri (header=0). 1.5pt black under the header; the 1pt
    total separator rides as the bottom rule of the row just above Portfolio;
    light ½pt gray between the other body rows; none under the last row."""
    if ri == 0:
        return {"B": _RULE_HEADER}
    if ri == _PORTFOLIO_RI:
        return {"B": "none"}
    if ri == _PORTFOLIO_RI - 1:
        return {"B": _RULE_TOTAL}
    return {"B": _RULE_BODY}


def _table() -> str:
    rows = []
    for ri, row in enumerate(_TBL_ALL):
        hdr = ri == 0
        total = ri == _PORTFOLIO_RI
        border = _row_border(ri)
        cells = [
            tcell(text, size=_TBL_SZ, align=_TBL_ALIGNS[ci],
                  bold=(hdr or total or ci == 0),
                  fill=(GRAY_1 if total else None),
                  anchor="ctr", borders=border)
            for ci, text in enumerate(row)
        ]
        rows.append(trow(cells, h=_TBL_ROW_H[ri]))
    return table(80, "CeilingByProgram", BODY_X, _TBL_Y, BODY_CX, _TBL_CY,
                 col_widths=_TBL_COL_W, rows=rows)


# ── Guardrail: the four doc caveats, compressed to one no-fill line ──────────
_GUARD_Y = _TBL_Y + _TBL_CY + 110_000
_GUARD_H = 360_000          # sized to its content (<= two 8pt lines), not the leftover
assert _GUARD_Y + _GUARD_H <= _BOTTOM, (
    "guardrail pushed past the body bottom - table copy grew past its budget; "
    "tighten the flow band or table sizing")


def _guardrail() -> str:
    return text_box(
        90, "Guardrail", BODY_X, _GUARD_Y, BODY_CX, _GUARD_H,
        [paragraph([
            run("Read with care: ", size=SOURCES_8PT, bold=True, italic=True,
                color=BLACK, font=FONT),
            run("the ceiling is the upper bound, the p ≈ 50% case is the "
                "working number; the destroyer inputs are analyst judgment; the "
                "shares, not the dollars, are the answer.", size=SOURCES_8PT,
                italic=True, color=BLACK, font=FONT)])],
        fill=None, anchor="t", insets=INSETS_NONE)


def _body() -> str:
    return (_framer()
            + _inputs() + _engine() + _flow() + _reads()
            + _caption() + _table()
            + _guardrail())


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC_LABEL)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES, y=_SOURCES_Y)
    )
