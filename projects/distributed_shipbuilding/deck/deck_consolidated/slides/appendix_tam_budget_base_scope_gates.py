"""appendix_tam_budget_base_scope_gates - the denominator-proof page: how Navy
new-construction budget streams become the retained stream bases that the
supplier-share step converts.

Retained-base proof layout (NOT a process spine): a full-width caption + output
chip, then a table-left / program-rail-right main zone (one native retained-base
ledger on the left, a stacked DDG / submarine treatment rail on the right), closed
by a full-width AP/LLTM incrementality example strip whose two arithmetic chains
are built from white formula cards joined by bare real math-operator AutoShapes
(mathMultiply / mathMinus / mathEqual, no backing chips) - the DDG additive
example and the submarine zero-base bridge. One native table; everything else is
shape-built. No bottom guardrail strip - the output chip carries the boundary.

The upstream / downstream step codes (the internal M-series) stay OUT of the
visible copy: the page uses descriptive references ("the supplier-share step",
"the next step", "supplier-share conversion") rather than the codes.

Spec: specs/distributed_shipbuilding/methodology/alternative_v3/
appendix_tam_budget_base_scope_gates_spec.md (TAM BUDGET BASE AND SCOPE GATES).
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
    GRAY_1,
    WHITE, BLACK, FONT,
    INSETS_NONE,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "TAM Budget Base"
_TOPIC            = "Methodology (2/5)"
_TAKEAWAY = ("Scope gates define the retained budget base before supplier-share "
             "conversion.")
_SOURCES = ("Sources: (1) Navy SCN budget justification books, FY2022–FY2027; "
            "(2) P-5c Basic Construction and P-10 AP/LLTM budget exhibits; "
            "(3) DDG-51, Virginia, and Columbia scope-exclusion reconciliations; "
            "(4) FY 2026 Mandatory Funding Allocation Plan, PL 119-21 Sec. 20002")

# Raw point sizes (style.py allows raw sizes with a nearby note).
_SZ_CARD   = 800    # 8.0pt: ledger body, DDG formula-card label
_SZ_BODY   = 850    # 8.5pt: chip body, program-card body, commentary bullet
_SZ_LABEL  = 1000   # 10pt:  table label, rail header, program ribbons
_SZ_FN     = 780    # 7.8pt: strip subnotes (italic)
_EVID_95   = 950    # 9.5pt: commentary finding sentence
_SZ_STITLE = 900    # 9.0pt: bottom-strip title
_SZ_DDGVAL = 1100   # 11pt:  DDG formula-card value
_SZ_SUBLBL = 750    # 7.5pt: submarine formula-card label (very short)
_SZ_SUBVAL = 1000   # 10pt:  submarine formula-card value


# ── Vertical geometry (all EMU) ──────────────────────────────────────────────
_CAP_Y, _CAP_H = BODY_Y, 200_000                     # italic window/boundary caption
_CHIP_Y = _CAP_Y + _CAP_H + 48_000                   # full-width output chip
_CHIP_H = 350_000
_ZONE_Y = _CHIP_Y + _CHIP_H + 56_000                 # main method zone top

_STRIP_H = 910_000                                   # AP/LLTM example strip (~1.0in)
_STRIP_Y = BODY_B - _STRIP_H
_ZONE_B = _STRIP_Y - 130_000                         # main zone bottom (extra gap before strip)
_ZONE_H = _ZONE_B - _ZONE_Y

# ── Horizontal geometry (all EMU) ────────────────────────────────────────────
# table-left / program-rail-right; the table top and the rail top align at _ZONE_Y.
_TABLE_X = BODY_X
_TABLE_W = 7_000_000                                 # ~7.65in left ledger
_GAP_COL = 270_000                                   # ~0.30in gutter
_RAIL_X  = BODY_X + _TABLE_W + _GAP_COL              # 7_723_079
_RAIL_W  = BODY_R - _RAIL_X                          # 4_012_362 (~4.39in)

# Left column: table label, then the native ledger.
_TLABEL_Y, _TLABEL_H = _ZONE_Y, 220_000
_TABLE_Y = _TLABEL_Y + _TLABEL_H + 30_000

# Right column: rail header, stacked DDG / submarine cards, commentary mini-block.
_RH_Y, _RH_H = _ZONE_Y, 250_000
_RIBBON_H = 190_000
_DBODY_H = 620_000
_SBODY_H = 620_000
_DDG_Y = _RH_Y + _RH_H + 50_000
_DDG_BODY_Y = _DDG_Y + _RIBBON_H
_SUB_Y = _DDG_BODY_Y + _DBODY_H + 56_000
_SUB_BODY_Y = _SUB_Y + _RIBBON_H
_COMM_Y = _SUB_BODY_Y + _SBODY_H + 40_000
_COMM_H = _ZONE_B - _COMM_Y                          # remainder fills the zone

# Bottom strip internals: title row, two card chains across a center divider, subnotes.
_SPAD = 120_000
_DIV_GAP = 200_000
_CENTER_X = BODY_X + BODY_CX // 2
_LEFT_X0  = BODY_X + _SPAD
_LEFT_W   = (_CENTER_X - _DIV_GAP // 2) - _LEFT_X0
_RIGHT_X0 = _CENTER_X + _DIV_GAP // 2
_RIGHT_W  = (BODY_X + BODY_CX - _SPAD) - _RIGHT_X0

_STITLE_Y, _STITLE_H = _STRIP_Y + 36_000, 175_000
_SCARD_Y, _SCARD_H = _STRIP_Y + 240_000, 420_000
_SUBN_Y, _SUBN_H = _SCARD_Y + _SCARD_H + 30_000, 150_000

_OP_SZ = 240_000                                     # operator-chip square
_GLYPH_SZ = 150_000                                  # math AutoShape inside the chip
_OP_Y = _SCARD_Y + (_SCARD_H - _OP_SZ) // 2
_FGAP = 30_000                                       # card<->chip gap

# DDG chain (3 cards, 2 ops) and submarine chain (5 cards, 4 ops).
_DDG_CARD_W = (_LEFT_W - 2 * _OP_SZ - 4 * _FGAP) // 3
_SUB_CARD_W = (_RIGHT_W - 4 * _OP_SZ - 8 * _FGAP) // 5


# ── Ledger content (no internal step codes in visible copy) ──────────────────
_LED_COL_W = [1_260_000, 2_380_000, 1_960_000, 1_400_000]   # sum 7,000,000
_LED_HEADERS = ["STEP", "SOURCE FIELDS USED", "RULE APPLIED", "RETAINED OUTPUT"]
_LED_BODY = [
    ["1. Program budget base",
     "Program; FY; appropriation; SCN / P-5c line; P-10 AP / LLTM / EOQ fields; "
     "OBBBA Sec. 20002 mandatory line",
     "Build the budget base by program and stream",
     "Budget is the sizing base; award flow is not"],
    ["2. Scope & cost boundary",
     "Total ship estimate; GFE / GFP; ordnance; plans; nuclear; sustainment / "
     "depot; design-only",
     "Retain the new-construction component boundary; remove non-component scope",
     "Total ship cost stays context"],
    ["3. Basic Construction stream",
     "P-5c Basic Construction; program flag; FY flag; non-GFE construction base",
     "Treat Basic Construction as the core retained denominator",
     "BC retained base by program"],
    ["4. AP/LLTM incrementality",
     "AP / LLTM / EOQ amount; overlap & incrementality flags; DDG construction "
     "share; submarine AP-bridge exclusions",
     "Add only where incremental to Basic Construction",
     "DDG additive; submarine nets to $0"],
    ["5. Handoff to next step",
     "Retained BC base; retained AP/LLTM base; stream flag; program flag",
     "Send the bases to supplier-share conversion",
     "No blended supplier-share factors; no supplier TAM yet"],
]
_LED_ROWS = [_LED_HEADERS] + _LED_BODY
# Row 4 (AP/LLTM incrementality) is the highest-attention row -> light blue full
# width; row 5 (handoff) -> light gray full width; rows 1-3 white.
_LED_ROW_FILL = {4: BLUE_1, 5: GRAY_1}
_LED_ROW_H = estimate_row_heights(_LED_ROWS, _LED_COL_W, size_pt=8.0,
                                  header_size_pt=8.5, min_row_h=274_320)
_LED_CY = sum(_LED_ROW_H)


# ── Program rail content ─────────────────────────────────────────────────────
_DDG_BODY = [
    ("Core base: ", "Basic Construction, LI 2122; OBBBA Sec. 20002(17) mandatory "
     "BC folds into the BC stream."),
    ("AP/LLTM: ", "additive, ship-construction-share filtered."),
    ("Output: ", "BC base (incl. OBBBA) + additive AP/LLTM base."),
]
_SUB_BODY = [
    ("Core base: ", "Virginia + Columbia Basic Construction; OBBBA Sec. 20002(16) "
     "runs as its own stream."),
    ("AP/LLTM: ", "reference-only; additive base = $0."),
    ("Output: ", "BC base + OBBBA stream + $0 additive AP/LLTM base."),
]
_RAIL_COMMENTARY = [
    ("Retained base stays program-specific.",
     "DDG and submarine stay separate because AP/LLTM rules and supplier-share "
     "evidence differ."),
    ("Conversion happens next.",
     "This page sizes eligible retained budget dollars; the next page applies "
     "supplier-share factors."),
]

# ── Bottom-strip content ─────────────────────────────────────────────────────
# Operators are prst names (the visible mark is the AutoShape, not a typed glyph).
_DDG_CHAIN = [("CY AP in window", "$1.8B"),
              ("Ship-construction share", "80%"),
              ("Retained AP/LLTM base", "$1.5B")]
_DDG_OPS = ["mathMultiply", "mathEqual"]
_DDG_SUBNOTE = ("The next step applies the AP/LLTM supplier-share factor; this "
                "page stops at the retained base.")
_SUB_CHAIN = [("Gross P-10 AP", "$44.7B"),
              ("GFE / design / weapons", "$27.3B"),
              ("Already in BC", "$16.8B"),
              ("Overlap", "$0.6B"),
              ("Additive AP base", "$0")]
_SUB_OPS = ["mathMinus", "mathMinus", "mathMinus", "mathEqual"]
_SUB_SUBNOTE = ("AP/LLTM stays useful evidence for supplier-share context, but "
                "it is not an incremental base.")


# ── Ledger table ─────────────────────────────────────────────────────────────
def _tc(text: str, *, fill, bold: bool, size: int, dark: bool, borders: dict):
    """One ledger cell, forced to 100% line spacing so the rendered row height
    matches estimate_row_heights (the house cells render ~15% taller at 115% and
    would push the table into the strip below)."""
    color = WHITE if dark else BLACK
    return tcell_rich(
        [{"align": "l",
          "runs": [trun(text, size=size, bold=bold, color=color, font=FONT)],
          "line_spacing": 100_000}],
        fill=fill, anchor="ctr", borders=borders)


def _ledger(sp_id: int) -> str:
    """Native retained-base ledger: dark BLUE_5 header (8.5pt white caps), 8pt
    body, bold first column, light-blue AP/LLTM row and light-gray handoff row,
    cascading horizontal rules only (1.5pt under header, 1pt under each body row)."""
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
            _tc(_LED_ROWS[ri][ci], fill=fill, bold=(ci == 0), size=_SZ_CARD,
                dark=False, borders=bb)
            for ci in range(len(_LED_COL_W))
        ]
        rows.append(trow(cells, h=_LED_ROW_H[ri]))
    return table(sp_id, "RetainedBaseLedger", _TABLE_X, _TABLE_Y,
                 sum(_LED_COL_W), _LED_CY, col_widths=_LED_COL_W, rows=rows)


# ── Program-rail builders ────────────────────────────────────────────────────
def _ribbon(sp_id: int, y: int, fill: str, text: str) -> str:
    """Program ribbon: white 10pt bold, sits directly atop its body card."""
    return text_box(
        sp_id, "ProgramRibbon", _RAIL_X, y, _RAIL_W, _RIBBON_H,
        [paragraph([run(text, size=_SZ_LABEL, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(120_000, 30_000, 120_000, 30_000))


def _program_body(sp_id: int, y: int, h: int, fill: str, lines: list) -> str:
    """Pale program body card: bold lead label + body run per line, 8.5pt."""
    paras = []
    for k, (lead, rest) in enumerate(lines):
        gap = 0 if k == len(lines) - 1 else 150
        paras.append(paragraph(
            [run(lead, size=_SZ_BODY, bold=True, color=BLACK, font=FONT),
             run(rest, size=_SZ_BODY, color=BLACK, font=FONT)],
            space_after=gap, line_spacing=106_000))
    return text_box(sp_id, "ProgramBody", _RAIL_X, y, _RAIL_W, h, paras,
                    fill=fill, line_width=12_700, anchor="t",
                    insets=(120_000, 70_000, 120_000, 60_000))


def _rail_commentary(sp_id: int) -> str:
    """No-fill / no-border rail commentary: two compact reminders (9.5pt bold
    finding over an 8.5pt bullet). Read alone, the bold lines are the takeaways."""
    paras = []
    for j, (finding, bullet) in enumerate(_RAIL_COMMENTARY):
        paras.append(paragraph(
            [run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
            space_after=100, line_spacing=104_000))
        gap = 0 if j == len(_RAIL_COMMENTARY) - 1 else 150
        paras.append(paragraph(
            [run(bullet, size=_SZ_BODY, color=BLACK, font=FONT)],
            bullet=True, space_after=gap, line_spacing=102_000))
    return text_box(sp_id, "RailCommentary", _RAIL_X, _COMM_Y, _RAIL_W, _COMM_H,
                    paras, fill=None, line_color=None, anchor="t",
                    insets=(0, 10_000, 30_000, 0))


# ── Bottom-strip builders ────────────────────────────────────────────────────
def _math_operator(chip_id: int, glyph_id: int, x: int, prst: str) -> str:
    """Bare math operator AutoShape (vector geometry, font-independent): no gray
    backing chip. The black fill is the ink; the outline matches the fill so no
    rim prints; the box is square and the text body is empty. See
    ooxml_arithmetic_shapes_conventions.md."""
    _ = chip_id  # retained so existing call sites / id spacing do not change
    gx = x + (_OP_SZ - _GLYPH_SZ) // 2
    gy = _OP_Y + (_OP_SZ - _GLYPH_SZ) // 2
    return text_box(
        glyph_id, f"MathOperator {prst}", gx, gy, _GLYPH_SZ, _GLYPH_SZ,
        [paragraph([])], fill=BLACK, line_color=BLACK, line_width=12_700,
        anchor="ctr", prst=prst, tx_box=False)


def _formula_card(sp_id: int, x: int, w: int, label: str, value: str,
                  label_sz: int, value_sz: int) -> str:
    """White formula card: a label line over a bold value line, centered."""
    return text_box(
        sp_id, "FormulaCard", x, _SCARD_Y, w, _SCARD_H,
        [paragraph([run(label, size=label_sz, color=BLACK, font=FONT)],
                   align="ctr", space_after=120, line_spacing=104_000),
         paragraph([run(value, size=value_sz, bold=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=WHITE, line_width=12_700, anchor="ctr",
        insets=(45_000, 40_000, 45_000, 40_000))


def _strip_chain(base_id: int, x0: int, card_w: int, items: list, ops: list,
                 label_sz: int, value_sz: int) -> str:
    """Lay out a card<->operator<->card chain across one half of the strip. Each
    operator consumes two shape ids (chip + math AutoShape)."""
    parts = []
    cid = base_id
    cx = x0
    for i, (label, value) in enumerate(items):
        parts.append(_formula_card(cid, cx, card_w, label, value, label_sz, value_sz))
        cid += 1
        cx += card_w
        if i < len(ops):
            cx += _FGAP
            parts.append(_math_operator(cid, cid + 1, cx, ops[i]))
            cid += 2
            cx += _OP_SZ + _FGAP
    return "".join(parts)


def _subnote(sp_id: int, x: int, w: int, text: str) -> str:
    """Quiet italic strip subnote (no fill, no border) under a formula chain."""
    return text_box(
        sp_id, "StripSubnote", x, _SUBN_Y, w, _SUBN_H,
        [paragraph([run(text, size=_SZ_FN, italic=True, color=BLACK, font=FONT)],
                   line_spacing=106_000)],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(
            "FY2022–FY2027 constant FY2026 dollars. DDG and submarine are run "
            "separately; this page stops at the retained budget stream bases sent "
            "to the supplier-share step.",
            size=_SZ_BODY, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    output_chip = text_box(
        11, "OutputChip", BODY_X, _CHIP_Y, BODY_CX, _CHIP_H,
        [paragraph([
            run("Retained-base output: ", size=950, bold=True, color=BLACK, font=FONT),
            run("retained stream bases by program: DDG Basic Construction (incl. "
                "OBBBA mandatory) + additive AP/LLTM base; submarine Basic "
                "Construction + OBBBA mandatory stream + $0 additive AP/LLTM base. "
                "Supplier-share factors are applied next.",
                size=900, color=BLACK, font=FONT)], line_spacing=108_000)],
        fill=BLUE_1, line_width=12_700, anchor="ctr", insets=(140_000, 38_000, 140_000, 38_000))

    # Left column: label + native ledger.
    table_label = text_box(
        20, "TableLabel", _TABLE_X, _TLABEL_Y, _TABLE_W, _TLABEL_H,
        [paragraph([run("Retained-base ledger: what survives into supplier-share "
                        "conversion",
                        size=_SZ_LABEL, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    ledger = _ledger(21)

    # Right column: rail header, two stacked program cards, commentary.
    rail_header = text_box(
        30, "ProgramRailHeader", _RAIL_X, _RH_Y, _RAIL_W, _RH_H,
        [paragraph([run("PROGRAM TREATMENT: RUN SEPARATELY",
                        size=_SZ_LABEL, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_5, line_width=12_700, anchor="ctr",
        insets=(120_000, 40_000, 120_000, 40_000))
    ddg = (_ribbon(31, _DDG_Y, BLUE_3, "DDG")
           + _program_body(32, _DDG_BODY_Y, _DBODY_H, BLUE_1, _DDG_BODY))
    sub = (_ribbon(33, _SUB_Y, BLUE_4, "SUBMARINE")
           + _program_body(34, _SUB_BODY_Y, _SBODY_H, GRAY_1, _SUB_BODY))
    commentary = _rail_commentary(50)

    # Bottom strip: pale panel (behind) + title + center divider + two chains + subnotes.
    strip_panel = text_box(
        40, "APLLTMStrip", BODY_X, _STRIP_Y, BODY_CX, _STRIP_H, [paragraph([])],
        fill=GRAY_1, line_width=12_700, anchor="ctr")
    strip_title = text_box(
        41, "StripTitle", _LEFT_X0, _STITLE_Y, BODY_CX - 2 * _SPAD, _STITLE_H,
        [paragraph([run("AP/LLTM incrementality test: add only when not already "
                        "inside the Basic Construction boundary",
                        size=_SZ_STITLE, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    divider = connector(42, "StripDivider", _CENTER_X, _STRIP_Y + 215_000, 0,
                        _STRIP_H - 320_000, color=BLACK, width=9_525)
    ddg_chain = _strip_chain(200, _LEFT_X0, _DDG_CARD_W, _DDG_CHAIN, _DDG_OPS,
                             _SZ_CARD, _SZ_DDGVAL)
    sub_chain = _strip_chain(240, _RIGHT_X0, _SUB_CARD_W, _SUB_CHAIN, _SUB_OPS,
                             _SZ_SUBLBL, _SZ_SUBVAL)
    ddg_subnote = _subnote(260, _LEFT_X0, _LEFT_W, _DDG_SUBNOTE)
    sub_subnote = _subnote(261, _RIGHT_X0, _RIGHT_W, _SUB_SUBNOTE)

    # Paint order: subordinate text first, then the strip panel behind its own
    # title / divider / chains / subnotes.
    return (caption + output_chip
            + table_label + ledger
            + rail_header + ddg + sub + commentary
            + strip_panel + strip_title + divider
            + ddg_chain + sub_chain + ddg_subnote + sub_subnote)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
