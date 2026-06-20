"""appendix_sam_classification_field_audit - the field-audit console: how FFATA /
FSRS award evidence becomes clean, auditable work-type shares before those shares
are applied to the fixed TAM pool.

Three-zone console layout (deliberately different from the roadmap, the retained-
base ledger, and the formula machine): a caption + light output chip, a full-width
seven-node evidence-flow spine (rounded pills joined by right-facing arrows), a
middle field-audit zone (one native classification ledger on the left; a nine-step
"first clean match wins" precedence ladder + a work-type-home chip cluster on the
right), and a bottom zone (DDG / submarine evidence-volume cards + a shape-built
examples board) with two no-fill commentary findings above it. One native table;
everything else is shape-built. No bottom guardrail strip, and no arithmetic
operator chips (this page classifies evidence, it does not compute dollars).

The internal step codes (the M-series) stay OUT of the visible copy: the page uses
descriptive references ("the fixed TAM dollar pool", "the allocation step") rather
than the codes.

Spec: specs/distributed_shipbuilding/methodology/alternative_v3/
appendix_sam_classification_field_audit_spec.md (SAM CLASSIFICATION FIELD AUDIT).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector, table, trow, tcell_rich, trun,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_4,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "SAM Classifier"
_TOPIC            = "Methodology (4/5)"
_TAKEAWAY = ("PIID scopes the award, UEI resolves the operating entity, and the "
             "registry assigns one work-type home.")
_SOURCES = ("Sources: (1) SAM.gov FSRS / FFATA first-tier subaward records, "
            "FY2017–FY2026; (2) SAM.gov Entity API and USAspending UEI / "
            "NAICS enrichment; (3) FPDS / DoD PIID records and program "
            "scope-exclusion registers")

# Raw point sizes (style.py allows raw sizes with a nearby note).
_SZ_MICRO  = 760    # 7.6pt: ladder / examples chip text
_SZ_WT     = 750    # 7.5pt: work-type chip text
_SZ_FN     = 780    # 7.8pt: spine node body, evidence-card body, connector note
_SZ_DESC   = 800    # 8.0pt: ledger body, evidence-card numbers
_SZ_BODY   = 850    # 8.5pt: caption, node header, ledger header, commentary bullet
_SZ_CHIP   = 900    # 9.0pt: output chip / examples title / work-type header
_SZ_LABEL  = 1000   # 10pt:  table label, rail header
_EVID_95   = 950    # 9.5pt: commentary finding


# ── Vertical band cascade (top-down; each band = prev bottom + gap) ───────────
_CAP_Y, _CAP_H = BODY_Y, 158_000                     # italic evidence-window caption
_CHIP_Y = _CAP_Y + _CAP_H + 22_000                   # light output chip
_CHIP_H = 292_000
_SPINE_Y = _CHIP_Y + _CHIP_H + 30_000                # evidence-flow spine
_SPINE_H = 560_000
_FA_Y = _SPINE_Y + _SPINE_H + 32_000                 # middle field-audit zone
_FA_H = 2_216_000
_FA_B = _FA_Y + _FA_H
_CM_Y = _FA_B + 26_000                               # two no-fill commentary findings
_CM_H = 294_000
_BOTTOM_RULE_CLEARANCE = 40_000                      # gap above and below the bottom rule
_BZ_Y = _CM_Y + _CM_H + 2 * _BOTTOM_RULE_CLEARANCE   # bottom evidence + examples zone
_BZ_H = BODY_B - _BZ_Y

# ── Spine geometry ───────────────────────────────────────────────────────────
_PILL_Y = _SPINE_Y + 8_000
_PILL_H = 410_000
_ARROW_GAP = 150_000
_PILL_W = (BODY_CX - 6 * _ARROW_GAP) // 7
_CONN_Y = _PILL_Y + _PILL_H // 2
_NOTE_Y = _PILL_Y + _PILL_H + 14_000
_NOTE_H = 116_000

# ── Field-audit geometry ─────────────────────────────────────────────────────
_TABLE_X = BODY_X
_TABLE_W = 6_950_000
_GAP_COL = 240_000
_RAIL_X = BODY_X + _TABLE_W + _GAP_COL
_RAIL_W = BODY_R - _RAIL_X
_TLABEL_Y, _TLABEL_H = _FA_Y, 214_000
_TABLE_Y = _TLABEL_Y + _TLABEL_H + 18_000

# Right rail: precedence header + 9 ladder rows + work-type header + 8 chips.
_PREC_Y, _PREC_H = _FA_Y, 258_000
_LAD_Y0 = _PREC_Y + _PREC_H + 26_000
_LAD_CHIP_H = 140_000
_WT_HEAD_Y = _LAD_Y0 + 9 * _LAD_CHIP_H + 28_000
_WT_HEAD_H = 128_000
_WT_ROW_Y0 = _WT_HEAD_Y + _WT_HEAD_H + 14_000
_WT_GAP = 22_000
_WT_CHIP_H = 240_000
_WT_CHIP_W = (_RAIL_W - 3 * _WT_GAP) // 4

# ── Bottom-zone geometry ─────────────────────────────────────────────────────
_EVID_LEFT_W = 5_200_000
_EVID_MID_GAP = 90_000
_EVID_CARD_W = (_EVID_LEFT_W - _EVID_MID_GAP) // 2
_EVID_GAP = 300_000
_EX_X = BODY_X + _EVID_LEFT_W + _EVID_GAP
_EX_W = BODY_R - _EX_X
_RIBBON_H = 170_000
_HRULE_Y = _BZ_Y - _BOTTOM_RULE_CLEARANCE

# ── Commentary geometry ──────────────────────────────────────────────────────
_CM_GAP = 280_000
_CM_W = (BODY_CX - _CM_GAP) // 2


# ── Content ──────────────────────────────────────────────────────────────────
_SPINE_NODES = [
    ("FFATA / FSRS record", "Subaward $, recipient, NAICS"),
    ("Parent-prime PIID", "Program scope arbiter"),
    ("Recipient UEI", "Entity identifier"),
    ("Operating entity", "Legal name + NAICS"),
    ("Role filter", "Supplier vs excluded"),
    ("Work-type home", "Registry / override / NAICS-4"),
    ("Bucket shares", "Named buckets + residual"),
]
_NOTE_TEXT = "UEI resolves the entity that received the dollars."

_LED_COL_W = [1_110_000, 2_572_000, 1_948_000, 1_320_000]   # sum 6,950,000
_LED_HEADERS = ["STAGE", "SOURCE FIELDS USED", "RULE APPLIED", "OUTPUT / GUARDRAIL"]
# Terse fragments (mostly one line each) so the 7-stage ledger stays ~2 in tall
# beside the precedence rail; the source lists are abbreviated, not paragraphs.
_LED_BODY = [
    ["1. Award pull", "Subaward ID, parent PIID, UEI, NAICS, $",
     "Collect visible supplier evidence", "Mix, not TAM"],
    ["2. PIID scope", "Parent-prime + discovered PIID flags",
     "Scope to DDG or submarine", "Not hull-level proof"],
    ["3. Entity resolution", "sub_entity_uei, legal name, NAICS",
     "Resolve the operating entity paid", "Not parent brand"],
    ["4. Role filter", "Role, prime / co-prime, GFE, FMS flags",
     "Drop non-supplier / non-component", "Excluded roles leave base"],
    ["5. Work-type assign", "Registry bucket, override, NAICS-4",
     "First clean match wins one home", "QA, not classifier"],
    ["6. Residual discipline", "Addressable, bucketed, unbucketed $",
     "Keep unresolved $ in denominator", "Dilutes named shares"],
    ["7. Share output", "Bucket $ over addressable base",
     "Modeled work-type and residual %", "Feeds allocation step"],
]
_LED_ROWS = [_LED_HEADERS] + _LED_BODY
# Row 3 (operating entity) + row 7 (output) E2E9EF; row 4 (role filter) F2F2F2;
# row 6 (residual) D9D9D9 — a deliberately retained classification outcome.
_LED_ROW_FILL = {3: BLUE_1, 4: GRAY_1, 6: GRAY_2, 7: BLUE_1}
_LED_ROW_H = estimate_row_heights(_LED_ROWS, _LED_COL_W, size_pt=8.0,
                                  header_size_pt=8.5, min_row_h=210_000)
_LED_CY = sum(_LED_ROW_H)

_LADDER = [
    ("Registry / operating-entity UEI", " assigns role and bucket."),
    ("Prime / co-prime name", " excludes final-assembly yards."),
    ("GFE / SIB / Navy-directed name", " routes out of supplier SAM."),
    ("Vendor-name override", " handles known exceptions."),
    ("NAICS-4 fallback", " assigns a bucket where registry is missing."),
    ("Service / non-component NAICS", " routes to excluded service."),
    ("Holding-company NAICS 5511", " routes to excluded holding."),
    ("Foreign / FMS", " routes out of U.S. supplier SAM."),
    ("Residual", " stays supplier / unbucketed when unresolved."),
]
_WT_CHIPS = ["Structural / modules", "Machining / propulsion", "Castings / forgings",
             "Piping / fluid handling", "Electrical power", "HVAC / chilled water",
             "Coatings / insulation", "Residual / unbucketed"]

_DDG_EVID = [("22,867", "FFATA / FSRS records"), ("118", "discovered PIIDs"),
             ("1,555", "cleaned vendors"), ("151", "NAICS lookups"),
             ("$6.0B", "supplier-addressable")]
_SUB_EVID = [("929", "classified entity rows"), ("$6.1B", "all-recipient base"),
             ("$5.5B", "supplier-addressable"), ("$664.8M", "unbucketed value"),
             ("12%", "residual / unbucketed")]

_EX_ROWS = [
    ["Northrop Sunnyvale generators", "Ship-power operating entity", "Electrical power"],
    ["Curtiss-Wright / Circor valves", "Industrial fluid-handling", "Piping / fluid handling"],
    ["Lockheed / Raytheon Aegis, SPY-6", "Navy-directed mission systems", "Excluded role"],
    ["Blank NAICS, no registry match", "Supplier evidence, unresolved", "Residual / unbucketed"],
]
_EX_COL_FRAC = [0.40, 0.33, 0.27]

_COMMENTARY = [
    ("The classifier is entity-first and role-first.",
     "PIID scopes; UEI resolves the entity; roles filtered first."),
    ("Residual is unclassified award spend.",
     "Unresolved dollars stay in the denominator, outside SAM."),
]


# ── Spine builders ───────────────────────────────────────────────────────────
def _pill(sp_id: int, x: int, header: str, body: str, fill: str) -> str:
    """Rounded evidence-flow node: 8.5pt bold header over a 7.8pt body line."""
    return text_box(
        sp_id, "SpineNode", x, _PILL_Y, _PILL_W, _PILL_H,
        [paragraph([run(header, size=_SZ_BODY, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=120, line_spacing=104_000),
         paragraph([run(body, size=_SZ_FN, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=fill, line_width=12_700, anchor="ctr", prst="roundRect",
        geom_adj={"adj": 9_000}, insets=(64_000, 40_000, 64_000, 40_000))


# ── Ledger table ─────────────────────────────────────────────────────────────
def _tc(text: str, *, fill, bold: bool, size: int, dark: bool, borders: dict):
    """One ledger cell at 100% line spacing so rendered height matches
    estimate_row_heights (house 115% cells render ~15% taller)."""
    color = WHITE if dark else BLACK
    return tcell_rich(
        [{"align": "l",
          "runs": [trun(text, size=size, bold=bold, color=color, font=FONT)],
          "line_spacing": 100_000}],
        fill=fill, anchor="ctr", borders=borders)


def _ledger(sp_id: int) -> str:
    """Native classification ledger: dark BLUE_5 header (8.5pt white caps), 8pt
    body, bold first column, highlighted entity/output rows, gray residual row,
    cascading horizontal rules only."""
    n = len(_LED_ROWS)
    rows = [trow([
        _tc(_LED_HEADERS[c], fill=BLUE_5, bold=True, size=850, dark=True,
            borders={"B": {"color": BLACK, "width": 19_050}})
        for c in range(len(_LED_COL_W))
    ], h=_LED_ROW_H[0])]
    for ri in range(1, n):
        bb = {"B": "none"} if ri == n - 1 else {"B": {"color": BLACK, "width": 12_700}}
        fill = _LED_ROW_FILL.get(ri)
        cells = [
            _tc(_LED_ROWS[ri][ci], fill=fill, bold=(ci == 0), size=_SZ_DESC,
                dark=False, borders=bb)
            for ci in range(len(_LED_COL_W))
        ]
        rows.append(trow(cells, h=_LED_ROW_H[ri]))
    return table(sp_id, "ClassificationLedger", _TABLE_X, _TABLE_Y,
                 sum(_LED_COL_W), _LED_CY, col_widths=_LED_COL_W, rows=rows)


# ── Right-rail builders ──────────────────────────────────────────────────────
def _ladder_chip(chip_id: int, badge_id: int, i: int, lead: str, rest: str) -> str:
    """One precedence row: alternating white / F2F2F2 bar with the number as an
    inline bold text run (not a separate badge box) and a bold-lead 7.6pt line."""
    _ = badge_id  # retained so existing call sites / id spacing do not change
    y = _LAD_Y0 + i * _LAD_CHIP_H
    fill = WHITE if i % 2 == 0 else GRAY_1
    return text_box(
        chip_id, "PrecedenceChip", _RAIL_X, y, _RAIL_W, _LAD_CHIP_H,
        [paragraph([
            run(f"{i + 1}. ", size=800, bold=True, color=BLACK, font=FONT),
            run(lead, size=_SZ_MICRO, bold=True, color=BLACK, font=FONT),
            run(rest, size=_SZ_MICRO, color=BLACK, font=FONT),
        ], line_spacing=100_000)],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(64_000, 8_000, 36_000, 8_000))


def _wt_chip(sp_id: int, i: int, label: str) -> str:
    """Work-type-home chip: E2E9EF, centered 7.5pt, two rows of four."""
    col, row = i % 4, i // 4
    x = _RAIL_X + col * (_WT_CHIP_W + _WT_GAP)
    y = _WT_ROW_Y0 + row * (_WT_CHIP_H + _WT_GAP)
    return text_box(
        sp_id, "WorkTypeChip", x, y, _WT_CHIP_W, _WT_CHIP_H,
        [paragraph([run(label, size=_SZ_WT, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=100_000)],
        fill=BLUE_1, line_width=12_700, anchor="ctr", insets=(20_000, 10_000, 20_000, 10_000))


# ── Bottom-zone builders ─────────────────────────────────────────────────────
def _evidence_card(ribbon_id: int, body_id: int, x: int, ribbon_fill: str,
                   body_fill: str, title: str, lines: list) -> str:
    """Evidence-volume card: program ribbon over a pale body of bold-number
    lines (one stat per line, tight 100%-spacing)."""
    ribbon = text_box(
        ribbon_id, "EvidenceHeader", x, _BZ_Y, _EVID_CARD_W, _RIBBON_H,
        [paragraph([run(title, size=_SZ_CHIP, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=ribbon_fill, line_width=12_700, anchor="ctr",
        insets=(54_000, 16_000, 54_000, 16_000))
    paras = []
    for num, txt in lines:
        # 7.5pt (in-spec for evidence body) so all five stat lines clear the
        # body after the bottom-rule clearance shortens this zone.
        paras.append(paragraph(
            [run(num + "  ", size=750, bold=True, color=BLACK, font=FONT),
             run(txt, size=750, color=BLACK, font=FONT)],
            line_spacing=100_000))
    body = text_box(
        body_id, "EvidenceBody", x, _BZ_Y + _RIBBON_H, _EVID_CARD_W,
        _BZ_H - _RIBBON_H, paras,
        fill=body_fill, line_width=12_700, anchor="ctr",
        insets=(84_000, 20_000, 60_000, 20_000))
    return ribbon + body


def _examples_board(panel_id: int, title_id: int, base_cell_id: int,
                    base_div_id: int) -> str:
    """Shape-built examples board: F2F2F2 panel, 9pt bold title, three columns of
    four micro-rows separated by light 0.5pt horizontal dividers (no grid)."""
    panel = text_box(panel_id, "ExamplesBoard", _EX_X, _BZ_Y, _EX_W, _BZ_H,
                     [paragraph([])], fill=GRAY_1, line_width=12_700, anchor="ctr")
    title = text_box(
        title_id, "ExamplesTitle", _EX_X, _BZ_Y + 16_000, _EX_W, 146_000,
        [paragraph([run("Examples: why operating entity beats parent brand",
                        size=_SZ_CHIP, bold=True, color=BLACK, font=FONT)],
                   line_spacing=100_000)],
        fill=None, line_color=None, anchor="t", insets=(94_000, 0, 94_000, 0))
    pad = 94_000
    inner_w = _EX_W - 2 * pad
    col_x = [_EX_X + pad]
    for f in _EX_COL_FRAC[:-1]:
        col_x.append(col_x[-1] + int(inner_w * f))
    col_w = [int(inner_w * f) for f in _EX_COL_FRAC]
    rows_top = _BZ_Y + 16_000 + 146_000 + 6_000
    rows_h = (_BZ_Y + _BZ_H - 36_000) - rows_top
    row_h = rows_h // len(_EX_ROWS)
    parts = [panel, title]
    cid, did = base_cell_id, base_div_id
    for r, rowvals in enumerate(_EX_ROWS):
        ry = rows_top + r * row_h
        if r > 0:                                   # light divider above each row but the first
            parts.append(connector(did, "ExampleDivider", _EX_X + pad, ry,
                                    inner_w, 0, color=GRAY_4, width=6_350))
            did += 1
        for c, val in enumerate(rowvals):
            bold = (c == 0)
            parts.append(text_box(
                cid, "ExampleCell", col_x[c], ry, col_w[c], row_h,
                [paragraph([run(val, size=_SZ_MICRO, bold=bold, color=BLACK, font=FONT)],
                           line_spacing=100_000)],
                fill=None, line_color=None, anchor="ctr", insets=(8_000, 4_000, 22_000, 4_000)))
            cid += 1
    return "".join(parts)


def _commentary(sp_id: int, x: int, finding: str, bullet: str) -> str:
    """No-fill / no-border commentary: 9.5pt bold finding over an 8.5pt bullet."""
    return text_box(
        sp_id, "Commentary", x, _CM_Y, _CM_W, _CM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=70, line_spacing=102_000),
         paragraph([run(bullet, size=_SZ_BODY, color=BLACK, font=FONT)],
                   bullet=True, line_spacing=100_000)],
        fill=None, line_color=None, anchor="t", insets=(0, 6_000, 24_000, 6_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(
            "FY2017–FY2026 FFATA / FSRS evidence window. Award records set "
            "supplier mix percentages; the fixed TAM dollar pool comes from the "
            "supplier-share step.", size=_SZ_BODY, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    output_chip = text_box(
        11, "OutputChip", BODY_X, _CHIP_Y, BODY_CX, _CHIP_H,
        [paragraph([
            run("Classifier output: ", size=_SZ_CHIP, bold=True, color=BLACK, font=FONT),
            run("program-specific modeled bucket shares, an excluded-role audit, "
                "and residual share. The allocation step applies these shares to "
                "fixed supplier TAM.", size=_SZ_CHIP, color=BLACK, font=FONT)],
            line_spacing=106_000)],
        fill=BLUE_1, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Evidence spine: arrows behind, then rounded pills, then the connector note.
    arrows = []
    for i in range(6):
        sx = BODY_X + i * (_PILL_W + _ARROW_GAP) + _PILL_W
        arrows.append(connector(41 + i, f"SpineArrow{i + 1}", sx, _CONN_Y,
                                _ARROW_GAP, 0, color=BLACK, width=12_700, arrow=True))
    pills = "".join(
        _pill(20 + i, BODY_X + i * (_PILL_W + _ARROW_GAP), h, b,
              GRAY_1 if i % 2 == 0 else BLUE_1)
        for i, (h, b) in enumerate(_SPINE_NODES))
    # Connector note centered under the arrow between Recipient UEI (node 3) and
    # Operating entity (node 4); widened to read on one line.
    note_w = 2 * _PILL_W + _ARROW_GAP
    note_mid = BODY_X + 2 * (_PILL_W + _ARROW_GAP) + _PILL_W + _ARROW_GAP // 2
    note = text_box(
        30, "SpineNote", note_mid - note_w // 2, _NOTE_Y, note_w, _NOTE_H,
        [paragraph([run(_NOTE_TEXT, size=_SZ_FN, italic=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # Middle field-audit: table label + ledger (left); rail header + ladder +
    # work-type chips (right); subtle dashed divider between.
    table_label = text_box(
        50, "TableLabel", _TABLE_X, _TLABEL_Y, _TABLE_W, _TLABEL_H,
        [paragraph([run("Classification ledger: how a record becomes one "
                        "work-type home",
                        size=_SZ_LABEL, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    ledger = _ledger(51)
    vdivider = connector(52, "RailDivider", _RAIL_X - _GAP_COL // 2, _FA_Y + 40_000,
                         0, _FA_H - 80_000, color=GRAY_4, dashed=True, width=9_525)
    prec_header = text_box(
        60, "PrecedenceHeader", _RAIL_X, _PREC_Y, _RAIL_W, _PREC_H,
        [paragraph([run("CLASSIFICATION PRECEDENCE: FIRST CLEAN MATCH WINS",
                        size=_SZ_LABEL, bold=True, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=(96_000, 24_000, 96_000, 24_000))
    ladder = "".join(_ladder_chip(100 + 2 * i, 101 + 2 * i, i, lead, rest)
                     for i, (lead, rest) in enumerate(_LADDER))
    wt_header = text_box(
        70, "WorkTypeHeader", _RAIL_X, _WT_HEAD_Y, _RAIL_W, _WT_HEAD_H,
        [paragraph([run("Work-type homes: one per retained supplier dollar",
                        size=_SZ_CHIP, bold=True, color=BLACK, font=FONT)],
                   line_spacing=102_000)],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    wt_chips = "".join(_wt_chip(120 + i, i, lab) for i, lab in enumerate(_WT_CHIPS))

    # Commentary (above the bottom zone) + thin rule + bottom evidence/examples.
    commentary = (_commentary(300, BODY_X, *_COMMENTARY[0])
                  + _commentary(301, BODY_X + _CM_W + _CM_GAP, *_COMMENTARY[1]))
    hrule = connector(250, "BottomRule", BODY_X, _HRULE_Y, BODY_CX, 0,
                      color=BLACK, width=9_525)
    ddg_card = _evidence_card(200, 201, BODY_X, BLUE_3, BLUE_1,
                              "DDG EVIDENCE BASE", _DDG_EVID)
    sub_card = _evidence_card(202, 203, BODY_X + _EVID_CARD_W + _EVID_MID_GAP,
                              BLUE_4, GRAY_1, "SUBMARINE EVIDENCE BASE", _SUB_EVID)
    examples = _examples_board(210, 211, 220, 233)

    return (caption + output_chip
            + "".join(arrows) + pills + note
            + table_label + ledger + vdivider
            + prec_header + ladder + wt_header + wt_chips
            + commentary + hrule + ddg_card + sub_card + examples)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
