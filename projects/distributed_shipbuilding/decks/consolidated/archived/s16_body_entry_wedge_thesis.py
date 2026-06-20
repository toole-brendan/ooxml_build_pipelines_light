"""s16_body_entry_wedge_thesis - frame the entry-wedge opportunity as a diligence
hypothesis, not a finding: modular and component work MAY reach revenue earlier than
prime-level ship construction, but backlog, award lock-up, and margin have to be proven
before any conclusion. The page sets the test, what is already known, and what is still
missing, then screens the entry lanes qualitatively.

Layout (no chart): a top thesis message strip; a three-column diligence board
(Demand and backlog / Entry feasibility / Economics and margin), each with stacked
Test / Have / Need under a light B6C8D8 header chip and no-fill bodies; a compact
dark-header entry-lane heatmap table (text-only High/Medium/Low, no traffic-light fill)
on the left with a due-diligence workplan and a no-fill commentary block stacked on the
right; and one focal callout strip at the bottom.

The heatmap is a qualitative screen, not a scored model, so its cells stay text-only.

Spec: ds_specs/s16_body_entry_wedge_thesis.txt (SLIDE 16 - ENTRY WEDGE DILIGENCE THESIS).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_5,
    WHITE, BLACK, FONT,
    INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT, CAP_12PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Implications"
_BREADCRUMB_TOPIC = "Entry Wedge"
_TOPIC            = "Entry Wedge"
_TAKEAWAY = ("Modular and component work may be an entry wedge, but backlog, award "
             "lock-up, and margin require diligence before any conclusion.")
_SOURCES = ("Sources: (1) DDG and submarine program implications analysis; "
            "(2) modeled TAM and SAM by work-type bucket, FY2022–FY2027; (3) FFATA/FSRS "
            "supplier-visibility evidence and stated opportunity hypotheses")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_G = 60_000

_THESIS_Y, _THESIS_H = BODY_Y, 330_000                  # 1_371_600 (1-line message)
_BOARD_Y = _THESIS_Y + _THESIS_H + _G                   # 1_761_600
_BOARD_H = 1_474_000
_HDR_CHIP_H = 270_000
_BOARD_BODY_Y = _BOARD_Y + _HDR_CHIP_H + 24_000         # 2_055_600
_BOARD_BODY_H = _BOARD_H - _HDR_CHIP_H - 24_000         # 1_180_000

_CALL_H = 340_000
_CALL_Y = BODY_B - _CALL_H                              # 5_530_000

_ROWC_Y = _BOARD_Y + _BOARD_H + _G                      # 3_295_600
_ROWC_B = _CALL_Y - 60_000                              # 5_470_000
_ROWC_H = _ROWC_B - _ROWC_Y                             # 2_174_400

# Three diligence-board columns across the full width.
_BCOL_GAP = 200_000
_BCOL_W = (BODY_CX - 2 * _BCOL_GAP) // 3                # 3_627_454
_BCOL_X = [BODY_X + i * (_BCOL_W + _BCOL_GAP) for i in range(3)]

# Row C split: heatmap left, workplan + commentary stacked right.
_RIGHT_W = 4_400_000
_RIGHT_X = BODY_R - _RIGHT_W                            # 7_335_441
_HEAT_X = BODY_X
_HEAT_W = _RIGHT_X - 200_000 - BODY_X                   # 6_682_362

_WP_Y, _WP_H = _ROWC_Y, 950_000
_RC_COMM_Y = _WP_Y + _WP_H + 30_000                     # 4_275_600
_RC_COMM_H = _ROWC_B - _RC_COMM_Y                       # 1_194_400


# ── Content ──────────────────────────────────────────────────────────────────
_THESIS = ("Modular structural units, pre-outfit, machining, and broad component "
           "manufacturing may reach revenue earlier than prime-level ship "
           "construction.")

# Diligence board: (column header, [(label, text), ...]).
_BOARD = [
    ("Demand and backlog", [
        ("Test", "backlog depth by bucket; prime need for external capacity; "
                 "near-term procurement timing; open and recompete work."),
        ("Have", "policy and prime direction of travel; modeled TAM and SAM; "
                 "visible supplier layer."),
        ("Need", "supplier-level backlog; award status; delivery schedule; "
                 "bottleneck items."),
    ]),
    ("Entry feasibility", [
        ("Test", "qualification path; QA and Navy standards; facility and capex; "
                 "weld, cyber, and certification; prime onboarding."),
        ("Have", "work-type buckets and supplier examples; modular and structural "
                 "alignment."),
        ("Need", "exact qualification timelines; make-buy posture by prime; "
                 "part-family eligibility."),
    ]),
    ("Economics and margin", [
        ("Test", "prime versus supplier margin pools; pricing power in bottlenecked "
                 "parts; learning curve, labor, and subcontract-tier economics."),
        ("Have", "prime-level margin context and visible public supplier flow."),
        ("Need", "third-tier economics; comparable supplier margins; contract type; "
                 "cost-plus versus fixed-price exposure."),
    ]),
]

# Entry-lane heatmap: header + 7 lanes ordered by speed-to-revenue logic. Text-only.
_HEAT_ROWS = [
    ["ENTRY LANE", "SPEED TO REVENUE", "QUALIFICATION BURDEN", "CAPEX INTENSITY",
     "INCUMBENT LOCK-UP", "EVIDENCE CONFIDENCE"],
    ["Structural/pre-outfit", "High", "Medium", "Medium", "Medium", "Medium"],
    ["Coatings/insulation", "High", "Low", "Low", "Low", "Low"],
    ["Machining", "Medium", "Medium", "Medium", "Medium", "Low"],
    ["Piping/valves/pumps", "Medium", "High", "Medium", "Medium", "Medium"],
    ["HVAC", "Medium", "Medium", "Low", "Medium", "Low"],
    ["Electrical/power", "Low", "High", "Medium", "High", "Medium"],
    ["Castings/forgings", "Low", "High", "High", "High", "Low"],
]
_HEAT_COL_W = [1_800_000, 976_472, 976_472, 976_472, 976_472, 976_474]  # sum = _HEAT_W
_HEAT_ROW_H = [366_000] + [258_000] * 7                                 # 2-line header

_WORKPLAN = [
    "Build a target-account list by bucket",
    "Map open awards and recompete windows",
    "Interview primes and tier-1 suppliers on make-buy posture",
    "Validate qualification path and capex by part family",
    "Test margin pool using public comps and supplier interviews",
]

_FINDINGS = [
    ("The entry-wedge case still needs proof.",
     "Backlog depth, open awards, make-buy posture, qualification path, and "
     "part-family economics determine whether lower-barrier work is investable."),
    ("Openness should lead the screen before size.",
     "Modeled SAM defines the pool to test; the first diligence question is which "
     "parts are open, qualifiable, and economically attractive."),
]

_CALL_TEXT = "Separate market size from investability before drawing a conclusion."


# ── Local helpers ────────────────────────────────────────────────────────────
def _thesis_card(sp_id: int) -> str:
    return text_box(
        sp_id, "ThesisCard", BODY_X, _THESIS_Y, BODY_CX, _THESIS_H,
        [paragraph([run(_THESIS, size=MESSAGE_11PT, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_1, line_width=12_700, anchor="ctr", insets=INSETS_CARD)


def _board_column(base_id: int, x: int, header: str,
                  blocks: list[tuple[str, str]]) -> str:
    chip = text_box(
        base_id, "BoardHeaderChip", x, _BOARD_Y, _BCOL_W, _HDR_CHIP_H,
        [paragraph([run(header, size=CAP_12PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_2, line_width=12_700, anchor="ctr", insets=(120_000, 30_000, 120_000, 30_000))
    paras = []
    for i, (label, body) in enumerate(blocks):
        last = i == len(blocks) - 1
        paras.append(paragraph(
            [run(label + "  ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
             run(body, size=LABEL_9PT, color=BLACK, font=FONT)],
            space_after=(0 if last else 140)))
    body_box = text_box(
        base_id + 1, "BoardColumnBody", x, _BOARD_BODY_Y, _BCOL_W, _BOARD_BODY_H,
        paras, fill=None, line_color=None, anchor="t",
        insets=(40_000, 30_000, 40_000, 30_000))
    return chip + body_box


def _heatmap(sp_id: int) -> str:
    return house_table(
        sp_id, "EntryLaneHeatmap", _HEAT_X, _ROWC_Y, _HEAT_COL_W, _HEAT_ROWS,
        row_h=_HEAT_ROW_H, table_skin="dark",
        aligns=["l", "ctr", "ctr", "ctr", "ctr", "ctr"], size=900)   # 9pt cells


def _workplan(sp_id: int) -> str:
    # Same pattern as the commentary block below it: a bold (unbulleted) 11pt lead
    # over bulleted 9.5pt body lines, with 100-unit lead->body spacing - so the
    # right column uses one consistent bulleted pattern.
    paras = [paragraph(
        [run("Due-diligence workplan", size=_EVID_95, bold=True, color=BLACK,
             font=FONT)], space_after=100)]
    for i, item in enumerate(_WORKPLAN):
        last = i == len(_WORKPLAN) - 1
        paras.append(paragraph(
            [run(item, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 30)))
    return text_box(
        sp_id, "DueDiligenceWorkplan", _RIGHT_X, _WP_Y, _RIGHT_W, _WP_H,
        paras, fill=None, line_color=None, anchor="t",
        insets=(40_000, 14_000, 40_000, 14_000))


def _commentary(sp_id: int) -> str:
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=100))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 130)))
    return text_box(
        sp_id, "Commentary", _RIGHT_X, _RC_COMM_Y, _RIGHT_W, _RC_COMM_H,
        paras, fill=None, line_color=None, anchor="t",
        insets=(40_000, 14_000, 40_000, 14_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    thesis = _thesis_card(10)
    board = "".join(
        _board_column(20 + i * 2, _BCOL_X[i], header, blocks)
        for i, (header, blocks) in enumerate(_BOARD))
    heatmap = _heatmap(40)
    workplan = _workplan(50)
    commentary = _commentary(60)
    callout = text_box(
        70, "FocalCallout", BODY_X, _CALL_Y, BODY_CX, _CALL_H,
        [paragraph([run(_CALL_TEXT, size=MESSAGE_11PT, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)
    return thesis + board + heatmap + workplan + commentary + callout


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
