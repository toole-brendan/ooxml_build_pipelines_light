"""s20_appendix_bucket_scenario_crosswalk - the bucket-to-scenario membership crosswalk:
which of the seven physical work-type buckets belong to each overlapping SAM scenario
(Broad, Metal, HM&E, Electrical), with the residual held outside broad SAM and modular
kept as an entity-flagged note rather than a column.

Layout (primary dense table, no chart): a dark-header crosswalk house_table top-left (five
columns, Yes/No inclusion flags). The annotations are split by role so the page does not
read as one jumbled rail of mismatched font sizes:
  - Right of the table: the modular note (a pale filled note) above the two-finding
    commentary - a coherent "note over interpretation" stack.
  - Directly under the table, where the short matrix frees space: the two fine-print
    reference lines (example-supplier evidence cue and the classification-order standard)
    as unified 8.5pt bold-lead footnotes.
There is no focal callout: the modular note already carries "entity-flagged work, not a
bucket union", and the freed space is intentional breathing room, not a gap to backfill.

The Yes/No fills (B6C8D8 Yes, F2F2F2 No) carry the matrix structure so the table needs no
vertical borders; the residual row is shaded D9D9D9 across the full row to show its exclusion
from broad SAM. No checkmarks, icons, or traffic-light colors - only the house ramps.

Spec: ds_specs/s20_appendix_bucket_scenario_crosswalk.txt (SLIDE 20 - APPENDIX A3).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, GRAY_1, GRAY_2,
    BLACK, FONT,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Bucket Crosswalk"
_TOPIC            = "Bucket Crosswalk"
_TAKEAWAY = ("Buckets map into overlapping scenarios by union; modular is "
             "entity-flagged and the residual stays outside broad SAM.")
_SOURCES = ("Sources: (1) operating-entity supplier registry and the SAM "
            "bucket-to-scenario crosswalk; (2) FFATA/FSRS subaward records, DDG and "
            "submarine; (3) NAICS-4 bucket classification standard")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Crosswalk table ──────────────────────────────────────────────────────────
# Five functional columns: Bucket (widest scan column) plus four equal-width
# scenario columns. Eight bucket rows; Yes/No inclusion flags only.
_COL_W = [2_700_000, 900_000, 900_000, 900_000, 900_000]   # sum 6_300_000

_ROWS = [
    ["BUCKET", "BROAD", "METAL", "HM&E", "ELECTRICAL"],
    ["Structural/Pre-Outfit",  "Yes", "Yes", "No",  "No"],
    ["Machining",              "Yes", "Yes", "Yes", "No"],
    ["Castings/Forgings",      "Yes", "Yes", "No",  "No"],
    ["Piping/Valves/Pumps",    "Yes", "No",  "Yes", "No"],
    ["Electrical/Power",       "Yes", "No",  "Yes", "Yes"],
    ["HVAC/Ventilation",       "Yes", "No",  "Yes", "No"],
    ["Coatings/Insulation",    "Yes", "No",  "No",  "No"],
    ["Residual",               "No",  "No",  "No",  "No"],
]

# Bucket label left, the four scenario flags centered (scan columns).
_ALIGNS = ["l", "ctr", "ctr", "ctr", "ctr"]

# Yes cells B6C8D8; No cells F2F2F2 (the fills carry the matrix structure). The
# residual row is shaded D9D9D9 across the full row to mark exclusion from broad SAM.
_RESIDUAL_ROW = len(_ROWS) - 1
_CELL_FILLS: dict[tuple[int, int], str] = {}
for _r in range(1, len(_ROWS)):
    if _r == _RESIDUAL_ROW:
        for _c in range(len(_COL_W)):
            _CELL_FILLS[(_r, _c)] = GRAY_2          # D9D9D9 full residual row
        continue
    for _c in range(1, len(_COL_W)):
        _CELL_FILLS[(_r, _c)] = BLUE_2 if _ROWS[_r][_c] == "Yes" else GRAY_1


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Both blocks - the LHS crosswalk + its under-table footnotes, and the RHS rail -
# are centered on the body midline (midway between the title and the sources line),
# so they share a common center and the page reads vertically balanced like the
# method-deltas slide rather than top-weighted.
_BODY_CENTER = (BODY_Y + BODY_B) // 2               # 3_620_800

# Left block: crosswalk table over the two under-table reference footnotes.
_TABLE_X  = BODY_X
_TABLE_W  = sum(_COL_W)                             # 6_300_000 (~6.9 in)
_ROW_H = estimate_row_heights(_ROWS, _COL_W, size_pt=9.0, min_row_h=240_000)
_TABLE_CY = sum(_ROW_H)
_NOTE_GAP = 220_000                                 # table -> footnotes
_NOTE_V   = 110_000                                 # between footnotes
_NOTE_H   = 380_000
_LEFT_H   = _TABLE_CY + _NOTE_GAP + 2 * _NOTE_H + _NOTE_V
_TABLE_Y  = _BODY_CENTER - _LEFT_H // 2
_TABLE_B  = _TABLE_Y + _TABLE_CY
_NOTE_X   = BODY_X
_NOTE_W   = _TABLE_W
_NOTE_Y0  = _TABLE_B + _NOTE_GAP

# Right rail: the modular note above the two-finding commentary (note over
# interpretation), centered on the same midline as the left block.
_RAIL_GAP  = 360_000
_RAIL_X    = _TABLE_X + _TABLE_W + _RAIL_GAP        # 7_113_079
_RAIL_W    = BODY_R - _RAIL_X                       # 4_622_362 (~5.05 in)
_RAIL_V    = 170_000                                # gap between rail items
_MODULAR_H = 470_000
_COMM_H    = 640_000
_RAIL_H    = _MODULAR_H + 2 * _COMM_H + 2 * _RAIL_V
_RAIL_Y0   = _BODY_CENTER - _RAIL_H // 2


# ── Content ──────────────────────────────────────────────────────────────────
_MODULAR_LABEL = "Modular: "
_MODULAR_BODY = ("entity-flagged module-assembly work, specific module assemblers "
                 "identified in the registry, not a bucket union; it is not a column "
                 "here.")

# Two fine-print footnotes share one bold-lead + 8.5pt-body structure so they read as
# a matched pair of reference lines rather than mismatched blocks.
_FOOTNOTES = [
    ("Example suppliers by bucket (illustrative): ",
     "Scot Forge (castings/forgings), DC Fabricators (structural/pre-outfit), "
     "Curtiss-Wright Electro-Mechanical and Leonardo DRS Naval Power "
     "(electrical/power)."),
    ("Recommended classification order: ",
     "(1) exclusion role; (2) operating-entity registry, SAM-resolved; (3) NAICS-4 "
     "bucket fallback; (4) service-NAICS exclusion; (5) residual. Description "
     "keywords are a QA sensitivity, not the classifier."),
]

_FINDINGS = [
    ("Scenario membership is a union rule, not an additive math rule.",
     "Broad includes all seven named buckets; metal, HM&E, and electrical are "
     "overlapping cuts that should not be summed across columns."),
    ("Residual stays in TAM until evidence assigns it.",
     "Residual maps to no scenario, which prevents broad SAM from automatically "
     "equaling total TAM."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _modular_note(sp_id: int) -> str:
    """Pale blue-gray filled note (E2E9EF, 1pt black border): bold label + body."""
    return text_box(
        sp_id, "ModularNote", _RAIL_X, _RAIL_Y0, _RAIL_W, _MODULAR_H,
        [paragraph([
            run(_MODULAR_LABEL, size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run(_MODULAR_BODY, size=LABEL_9PT, color=BLACK, font=FONT)],
            line_spacing=112_000)],
        fill=BLUE_1, line_width=12_700, anchor="ctr",
        insets=(140_000, 50_000, 140_000, 50_000))


def _commentary(sp_id: int, y: int, finding: str, evidence: str) -> str:
    return text_box(
        sp_id, "Commentary", _RAIL_X, y, _RAIL_W, _COMM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=90),
         paragraph([run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t", insets=(40_000, 20_000, 40_000, 20_000))


def _footnote(sp_id: int, y: int, lead: str, body: str) -> str:
    """No-fill / no-border reference footnote: 8.5pt bold lead-in + 8.5pt body."""
    return text_box(
        sp_id, "ReferenceFootnote", _NOTE_X, y, _NOTE_W, _NOTE_H,
        [paragraph([
            run(lead, size=FINEPRINT_8_5PT, bold=True, color=BLACK, font=FONT),
            run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
            line_spacing=112_000)],
        fill=None, line_color=None, anchor="t", insets=(0, 20_000, 40_000, 20_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    table_xml = house_table(
        10, "BucketScenarioCrosswalk", _TABLE_X, _TABLE_Y, _COL_W, _ROWS,
        row_h=_ROW_H, table_skin="dark", aligns=_ALIGNS, size=900,   # 9pt
        cell_fills=_CELL_FILLS)

    # Right rail: modular note over the two commentary findings.
    rail = [_modular_note(20)]
    y = _RAIL_Y0 + _MODULAR_H + _RAIL_V
    for i, (finding, evidence) in enumerate(_FINDINGS):
        rail.append(_commentary(30 + i, y, finding, evidence))
        y += _COMM_H + _RAIL_V

    # Under-table footnotes: example-supplier cue, then classification order.
    notes = []
    yn = _NOTE_Y0
    for i, (lead, body) in enumerate(_FOOTNOTES):
        notes.append(_footnote(40 + i, yn, lead, body))
        yn += _NOTE_H + _NOTE_V

    return table_xml + "".join(rail) + "".join(notes)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
