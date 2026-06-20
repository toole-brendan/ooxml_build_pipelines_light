"""s19_appendix_method_deltas - the method-delta audit trail: which sizing inputs stay
program-specific across DDG and submarine, and how the deck treats each, so the combined
headline reads as a disciplined sum of two models rather than one blended estimate.

Layout (table-left / annotation-right, no chart): a dark-header audit house_table on the
left (four columns, seven method-issue rows) as the primary evidence object, with a right
stack of two program mini-panels (a DDG MYP-correction panel and a submarine AP/LLTM panel,
each a program-colored label chip over a pale body) and a two-finding no-fill commentary.
There is no focal callout: the table's Deck-treatment column already states "never blend to
one %", so the freed foot of the right stack is intentional breathing room, not a gap.

The two highest-attention rows are shaded: AP/LLTM in light blue-gray (E2E9EF) as the
highest-risk asymmetry, MYP correction in very light gray (F2F2F2) as a secondary audit cue.
DDG and submarine treatment columns are NOT colored by program; the mini-panels carry the
program color instead.

Spec: ds_specs/s19_appendix_method_deltas.txt (SLIDE 19 - APPENDIX A2).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R,
    BLUE_1, BLUE_3, BLUE_4, GRAY_1,
    WHITE, BLACK, FONT,
    LABEL_9PT, DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Method Deltas"
_TOPIC            = "Method Deltas"
_TAKEAWAY = ("The combined headline holds only if AP/LLTM, supplier share, and MYP "
             "redaction stay separate across the two programs.")
_SOURCES = ("Sources: (1) DDG MYP-correction, AP/LLTM-sensitivity, and TAM-calculation "
            "appendix; (2) submarine AP/LLTM detail and coefficient-sensitivity "
            "evidence; (3) operating-entity supplier registry, FY2017–FY2026")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Method-delta table ───────────────────────────────────────────────────────
# Four columns: Issue (compact scan column); DDG treatment / Submarine treatment
# (near-equal); Deck treatment (the implication column). Seven method-issue rows.
_COL_W = [1_450_000, 1_780_000, 1_780_000, 1_990_000]   # sum 7_000_000

_ROWS = [
    ["ISSUE", "DDG TREATMENT", "SUBMARINE TREATMENT", "DECK TREATMENT"],
    ["Budget base", "LI 2122", "Virginia and Columbia P-5c Basic Construction",
     "Sum the two, do not pool"],
    ["Applied supplier share", "12.5%", "35.0%",
     "Keep separate; never blend to one %"],
    ["Broader POP evidence", "Corrected outside-yards POP ~32.8%",
     "All-gated POP anchor ~51.8%", "Evidence and sensitivity, not the headline"],
    ["AP/LLTM", "Additive filtered stream", "$0 additive base",
     "Additive only where the boundary allows"],
    ["MYP correction", "Restores $14.58B redacted masters", "No equivalent",
     "Keep visible in the audit trail"],
    ["SIB", "Not a central method issue", "Material capacity funding, excluded",
     "Context, not current component delivery"],
    ["Work-type classification", "Operating-entity registry",
     "Operating-entity registry", "One registry, aligned across both programs"],
]

# Fragments throughout; left-align every column so the treatment cells read cleanly.
_ALIGNS = ["l", "l", "l", "l"]

# Highlight rows: AP/LLTM (row 4) E2E9EF as the highest-risk asymmetry; MYP correction
# (row 5) F2F2F2 as a secondary audit cue. Whole-row fills (no per-program coloring).
_AP_ROW, _MYP_ROW = 4, 5
_CELL_FILLS: dict[tuple[int, int], str] = {}
for _c in range(len(_COL_W)):
    _CELL_FILLS[(_AP_ROW, _c)] = BLUE_1
    _CELL_FILLS[(_MYP_ROW, _c)] = GRAY_1


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_TABLE_X = BODY_X
_TABLE_W = sum(_COL_W)                              # 7_000_000 (~7.65 in)
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=8.5, min_row_h=240_000)
_TABLE_CY = sum(_ROW_H)

# Right annotation stack: two program mini-panels then commentary, pinned to the top
# of the body box.
_STACK_GAP = 320_000
_STACK_X   = _TABLE_X + _TABLE_W + _STACK_GAP       # 7_773_079
_STACK_W   = BODY_R - _STACK_X                      # 3_962_362 (~4.33 in)
_STACK_Y0  = BODY_Y
_STACK_V   = 170_000                                # gap between stack items

_CHIP_H    = 300_000                                # program label chip strip
_PANEL_BODY_H = 470_000                             # pale body under each chip
_PANEL_H   = _CHIP_H + _PANEL_BODY_H                # full mini-panel height
_COMM_GAP  = 210_000                                # panels -> commentary
_COMM_H    = 660_000

# Full extent of the right stack, then center the LHS table on its midline so the
# table reads as vertically aligned to the middle of the commentary rail rather than
# pinned to the top with empty space beneath it.
_STACK_BOTTOM = _STACK_Y0 + 2 * _PANEL_H + 2 * _STACK_V + _COMM_GAP + 2 * _COMM_H
_TABLE_Y = (_STACK_Y0 + _STACK_BOTTOM) // 2 - _TABLE_CY // 2


# ── Content ──────────────────────────────────────────────────────────────────
# Program mini-panels: (label, body, chip_fill). DDG = 6E91B1, submarine = 3D5972.
_DDG_PANEL = ("DDG MYP CORRECTION",
              "Restored masters correct the outside-yards evidence; do not confuse "
              "outside-yards POP with the applied supplier share.", BLUE_3)
_SUB_PANEL = ("SUBMARINE AP/LLTM",
              "Gross AP is large supplier evidence; the additive base stays $0 under "
              "the current Basic Construction boundary.", BLUE_4)

_FINDINGS = [
    ("The headline depends on summing two program-specific models.",
     "DDG and submarine budget bases, supplier shares, AP/LLTM treatment, and "
     "redaction issues stay separate until dollar outputs are summed."),
    ("Classification is aligned, but the major method deltas remain.",
     "Both programs use the same operating-entity registry; AP/LLTM treatment and "
     "DDG MYP restoration remain program-specific by design."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _mini_panel(base_id: int, y: int, label: str, body: str, chip_fill: str,
                body_fill: str) -> str:
    """Program-colored label chip (WHITE 10pt bold) over a pale body box (9pt).
    Both carry the default 1pt black border."""
    chip = text_box(
        base_id, "PanelChip", _STACK_X, y, _STACK_W, _CHIP_H,
        [paragraph([run(label, size=DENSE_BODY_10PT, bold=True, color=WHITE,
                        font=FONT)], align="l")],
        fill=chip_fill, line_width=12_700, anchor="ctr",
        insets=(140_000, 20_000, 140_000, 20_000))
    body_box = text_box(
        base_id + 1, "PanelBody", _STACK_X, y + _CHIP_H, _STACK_W, _PANEL_BODY_H,
        [paragraph([run(body, size=LABEL_9PT, color=BLACK, font=FONT)],
                   line_spacing=112_000)],
        fill=body_fill, line_width=12_700, anchor="ctr",
        insets=(140_000, 40_000, 140_000, 40_000))
    return chip + body_box


def _commentary(sp_id: int, y: int, finding: str, evidence: str) -> str:
    return text_box(
        sp_id, "Commentary", _STACK_X, y, _STACK_W, _COMM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=90),
         paragraph([run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t", insets=(40_000, 20_000, 40_000, 20_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    table_xml = house_table(
        10, "MethodDeltaAudit", _TABLE_X, _TABLE_Y, _COL_W, _ROWS,
        row_h=_ROW_H, table_skin="dark", aligns=_ALIGNS, size=850,   # 8.5pt
        cell_fills=_CELL_FILLS)

    # Right stack: DDG MYP panel (E2E9EF body), submarine AP/LLTM panel (F2F2F2 body),
    # then the two commentary findings; the freed foot is intentional breathing room.
    y = _STACK_Y0
    ddg = _mini_panel(20, y, *_DDG_PANEL[:2], _DDG_PANEL[2], BLUE_1)
    y += _PANEL_H + _STACK_V
    sub = _mini_panel(22, y, *_SUB_PANEL[:2], _SUB_PANEL[2], GRAY_1)
    y += _PANEL_H + _COMM_GAP

    comm_parts = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        comm_parts.append(_commentary(30 + i, y, finding, evidence))
        y += _COMM_H + _STACK_V

    return table_xml + ddg + sub + "".join(comm_parts)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
