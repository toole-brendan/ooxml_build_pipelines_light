"""appendix_sam_allocation_scenario_views - the final allocation board: how the
fixed outsourced supplier TAM is sliced into mutually exclusive work-type homes
and then re-cut into overlapping scenario SAM views.

Calculation-board layout (no process spine): a full-width caption + output chip, a
light formula / reconciliation strip (fixed TAM × modeled share = work-type TAM;
named buckets + residual = fixed TAM) built from white cards and bare
math-operator AutoShapes (mathMultiply / mathPlus / mathEqual — vector geometry,
not typed glyphs and not boxed; see
ooxml_arithmetic_shapes_conventions.md), one native work-type-to-scenario
crosswalk table on the left, a right-side
scenario output stack (broad envelope card over a 2x2 grid of cut cards) closed by
a compact "do not add scenarios" caveat chip, and two no-fill commentary findings
along the bottom. One native table; everything else is shape-built. No bottom
guardrail strip (the output chip and caveat chip carry the boundaries instead).

The upstream step codes (the M-series) are internal slide notations, so the copy
uses descriptive references ("the supplier-share step", "the evidence classifier")
rather than the codes.

Spec: specs/distributed_shipbuilding/methodology/alternative_v3/
appendix_sam_allocation_scenario_views_spec.md (APPENDIX M5 - SAM ALLOCATION).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, trow, tcell_rich, trun,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "SAM Allocation"
_TOPIC            = "Methodology (5/5)"
_TAKEAWAY = ("Fixed TAM is sliced into work-type homes and overlapping scenario "
             "views.")
_SOURCES = ("Sources: (1) SAM.gov FSRS / FFATA subaward records, "
            "FY2017–FY2026; (2) SAM.gov Entity API / USAspending NAICS "
            "enrichment and work-type evidence; (3) DoD/DoW POP corpus and "
            "Navy SCN budget books supporting fixed supplier TAM")

# Raw point sizes (style.py allows raw sizes with a nearby note).
_SZ_CARD   = 800    # 8.0pt: formula-card header/body, cut-card subline base
_SZ_BODY   = 850    # 8.5pt: chip / caveat / table / footnote-adjacent body
_SZ_LABEL  = 1000   # 10pt:  table label, right-rail header
_SZ_FN     = 780    # 7.8pt: table footnotes (italic)
_EVID_95   = 950    # 9.5pt: commentary finding sentence
_SZ_BROAD  = 1500   # 15pt:  broad scenario value
_SZ_CUTVAL = 1100   # 11pt: cut-card value (compact so cuts fit beside the taller broad card)

# Intra-shape paragraph spacing (1/100 pt) - deliberate gaps between blocks.
_GAP_HEAD = 260
_GAP_VAL  = 100
_GAP_FIND = 240


# ── Horizontal geometry (all EMU) ────────────────────────────────────────────
_GAP_COL = 300_000                                   # table | scenario-stack gutter
_TABLE_W = 6_800_000                                 # ~7.4in left table
_TABLE_X = BODY_X
_RAIL_X  = BODY_X + _TABLE_W + _GAP_COL              # 7_553_079
_RAIL_W  = BODY_R - _RAIL_X                          # 4_182_362 (~4.6in)


# ── Vertical geometry (all EMU) ──────────────────────────────────────────────
_CAP_Y, _CAP_H = BODY_Y, 210_000                     # italic evidence-window caption
_CHIP_Y = _CAP_Y + _CAP_H + 56_000                   # full-width output chip
_CHIP_H = 256_000
_STRIP_Y = _CHIP_Y + _CHIP_H + 56_000                # formula / reconciliation strip
_STRIP_H = 620_000
_EXH_Y = _STRIP_Y + _STRIP_H + 72_000                # main exhibit zone top

_COMM_H = 520_000                                    # two no-fill commentary findings
_COMM_Y = BODY_B - _COMM_H
_EXH_B = _COMM_Y - 70_000                            # exhibit zone bottom
_EXH_H = _EXH_B - _EXH_Y

_COMM_GAP = 260_000
_COMM_W = (BODY_CX - _COMM_GAP) // 2

# Formula strip internals: two 3-card chains, each card joined by operator chips.
_STRIP_PAD = 120_000
_CHAIN_GAP = 220_000
_CHAIN_SPAN = (BODY_CX - 2 * _STRIP_PAD - _CHAIN_GAP) // 2
_LEFT_X0  = BODY_X + _STRIP_PAD
_RIGHT_X0 = _LEFT_X0 + _CHAIN_SPAN + _CHAIN_GAP
_OP_SZ = 300_000
_GLYPH_SZ = 170_000   # math AutoShape centered inside the D9D9D9 operator chip
_FCARD_GAP = 30_000
_FCARD_W = (_CHAIN_SPAN - 2 * _OP_SZ - 4 * _FCARD_GAP) // 3
_FCARD_H = 380_000
_FCARD_Y = _STRIP_Y + (_STRIP_H - _FCARD_H) // 2
_OP_Y = _STRIP_Y + (_STRIP_H - _OP_SZ) // 2

# Left column: table label, table, two footnotes.
_TLABEL_Y, _TLABEL_H = _EXH_Y, 220_000
_TABLE_Y = _TLABEL_Y + _TLABEL_H + 36_000

# Right column: rail header, broad card, 2x2 cut grid, caveat chip - sized to fill
# the exhibit zone so the table top and the scenario-stack top stay aligned.
_RH_Y, _RH_H = _EXH_Y, 280_000
_BROAD_Y, _BROAD_H = _RH_Y + _RH_H + 60_000, 640_000
_GRID_Y = _BROAD_Y + _BROAD_H + 64_000
_CUT_GAP = 90_000
_CUT_W = (_RAIL_W - _CUT_GAP) // 2
_CAVEAT_H = 380_000
# Two grid rows fill the slack between the broad card and the caveat chip.
_CUT_H = (_EXH_B - _GRID_Y - 60_000 - _CAVEAT_H - _CUT_GAP) // 2
_CAVEAT_Y = _EXH_B - _CAVEAT_H


# ── Table content ────────────────────────────────────────────────────────────
# Six columns: work-type home, avg annual TAM ($M), then four scenario-membership
# flags. Modular is NOT a column (it is entity-flagged - see the modular footnote).
_T_COL_W = [2_584_000, 1_156_000, 748_000, 748_000, 748_000, 816_000]   # sum 6,800,000
_T_ALIGNS = ["l", "r", "ctr", "ctr", "ctr", "ctr"]
_T_HEADERS = ["WORK-TYPE HOME", "AVG TAM ($M)", "BROAD", "HM&E", "METAL", "ELECTRICAL"]
# Body rows descending by combined avg annual TAM, residual separated at the bottom.
_T_BODY = [
    ["Electrical power / distribution / generation", "$1,353M", "Yes", "Yes", "No",  "Yes"],
    ["Piping / valves / pumps",                       "$710M",  "Yes", "Yes", "No",  "No"],
    ["Structural fabrication / modules",              "$633M",  "Yes", "No",  "Yes", "No"],
    ["Machining / mechanical / propulsion",           "$375M",  "Yes", "Yes", "Yes", "No"],
    ["Coatings / insulation / decking",               "$206M",  "Yes", "No",  "No",  "No"],
    ["Castings / forgings",                           "$162M",  "Yes", "No",  "Yes", "No"],
    ["HVAC / ventilation / chilled water",            "$102M",  "Yes", "Yes", "No",  "No"],
    ["Residual / unbucketed",                         "$653M",  "No",  "No",  "No",  "No"],
]
_T_ROWS = [_T_HEADERS] + _T_BODY

# Yes B6C8D8 / No F2F2F2 carry the matrix; residual row D9D9D9 full width; value
# column bold. First column + header are bolded by house_table.
_T_FILLS: dict[tuple[int, int], str] = {}
_T_BOLD: dict[tuple[int, int], bool] = {}
for _ri in range(1, len(_T_ROWS)):
    _T_BOLD[(_ri, 1)] = True
    if _T_ROWS[_ri][0].startswith("Residual"):
        for _ci in range(len(_T_COL_W)):
            _T_FILLS[(_ri, _ci)] = GRAY_2
    else:
        for _ci in range(2, 6):
            _T_FILLS[(_ri, _ci)] = BLUE_2 if _T_ROWS[_ri][_ci] == "Yes" else GRAY_1

# 100%-line-spacing cells (see _crosswalk_table) render close to this estimate,
# so the authored table height is honest and the footnotes clear the last row.
_T_ROW_H = estimate_row_heights(_T_ROWS, _T_COL_W, size_pt=8.0,
                                header_size_pt=8.5, min_row_h=215_000)
_TABLE_CY = sum(_T_ROW_H)
_FN_Y0 = _TABLE_Y + _TABLE_CY + 40_000
_FN_H = 150_000
_FN_GAP = 14_000


# ── Other content ────────────────────────────────────────────────────────────
_LEFT_CHAIN = [
    ("Fixed supplier TAM", "$4.2B / yr"),
    ("Modeled bucket share", "Share per work type"),
    ("Work-type TAM", "One home per dollar"),
]
# Operators are prst names (the visible mark is the AutoShape, not a typed glyph).
_LEFT_OPS = ["mathMultiply", "mathEqual"]
_RIGHT_CHAIN = [
    ("Named-bucket SAM", "$3.5B / yr"),
    ("Residual", "$0.7B / yr"),
    ("Fixed supplier TAM", "$4.2B / yr"),
]
_RIGHT_OPS = ["mathPlus", "mathEqual"]

# Scenario cut cards: (cap, value, subline). Broad is rendered apart (the envelope).
_CUTS = [
    ("HM&E", "$2.5B / yr", "machining + piping + electrical + HVAC"),
    ("ELECTRICAL / POWER", "$1.4B / yr", "ship power, distribution, generation only"),
    ("METAL COMPONENTS", "$1.2B / yr", "structural + machining + castings"),
    ("MODULAR ASSEMBLIES", "$408M / yr", "entity-flagged suppliers, not bucket union"),
]

_FOOTNOTES = [
    ("Residual treatment: ",
     "residual stays inside fixed TAM and dilutes named-bucket shares, but stays "
     "outside broad and targeted scenario SAM."),
    ("Modular treatment: ",
     "modular assemblies come from registry entity flags, not from summing one or "
     "more work-type rows."),
]

_FINDINGS = [
    (40, BODY_X,
     "Work types classify dollars once; scenarios re-cut them multiple ways.",
     "Each supplier dollar is assigned one work-type home or residual, but Broad, "
     "HM&E, Metal, Electrical, and Modular are overlapping views built from those "
     "homes and flags."),
    (41, BODY_X + _COMM_W + _COMM_GAP,
     "Residual keeps the allocation conservative.",
     "Unresolved supplier dollars remain in the fixed TAM reconciliation, but they "
     "stay outside named scenario SAM until registry, NAICS, or override evidence "
     "supports assignment."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _tc(text: str, *, fill, bold: bool, align: str, borders: dict, size: int = _SZ_CARD):
    """One crosswalk cell, forced to 100% line spacing so the rendered row height
    matches estimate_row_heights (house_table's 115% cells render ~15% taller and
    would push the table into the footnotes)."""
    return tcell_rich(
        [{"align": align,
          "runs": [trun(text, size=size, bold=bold, color=BLACK, font=FONT)
                   if fill != BLUE_5 else
                   trun(text, size=size, bold=bold, color=WHITE, font=FONT)],
          "line_spacing": 100_000}],
        fill=fill, anchor="ctr", borders=borders)


def _crosswalk_table(sp_id: int) -> str:
    """Native work-type-to-scenario crosswalk: dark BLUE_5 header (8.5pt white
    caps), 8pt body, Yes B6C8D8 / No F2F2F2 fills, full GRAY_2 residual row, bold
    first + value columns, cascading horizontal rules only (1.5pt under the header,
    1pt under each body row, none under the last)."""
    n = len(_T_ROWS)
    rows = [trow([
        _tc(_T_HEADERS[c], fill=BLUE_5, bold=True, align=_T_ALIGNS[c], size=_SZ_BODY,
            borders={"B": {"color": BLACK, "width": 19_050}})
        for c in range(len(_T_COL_W))
    ], h=_T_ROW_H[0])]
    for ri in range(1, n):
        bb = {"B": "none"} if ri == n - 1 else {"B": {"color": BLACK, "width": 12_700}}
        cells = [
            _tc(_T_ROWS[ri][ci], fill=_T_FILLS.get((ri, ci)),
                bold=(ci == 0 or _T_BOLD.get((ri, ci), False)),
                align=_T_ALIGNS[ci], borders=bb)
            for ci in range(len(_T_COL_W))
        ]
        rows.append(trow(cells, h=_T_ROW_H[ri]))
    return table(sp_id, "WorkTypeScenarioCrosswalk", _TABLE_X, _TABLE_Y,
                 sum(_T_COL_W), _TABLE_CY, col_widths=_T_COL_W, rows=rows)


def _formula_card(sp_id: int, x: int, header: str, body: str) -> str:
    """White formula card: 8pt bold header over an 8pt value/body line, centered."""
    return text_box(
        sp_id, "FormulaCard", x, _FCARD_Y, _FCARD_W, _FCARD_H,
        [paragraph([run(header, size=_SZ_CARD, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=130, line_spacing=104_000),
         paragraph([run(body, size=_SZ_CARD, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=WHITE, line_width=12_700, anchor="ctr", insets=(50_000, 36_000, 50_000, 36_000))


def _operator_chip(chip_id: int, glyph_id: int, x: int, prst: str) -> str:
    """Bare math-operator AutoShape (vector geometry, font-independent): no gray
    backing chip. Black fill is the ink, the outline matches the fill so no rim
    prints, the box is square, and the text body is empty. See
    ooxml_arithmetic_shapes_conventions.md."""
    _ = chip_id  # retained so existing call sites / id spacing do not change
    gx = x + (_OP_SZ - _GLYPH_SZ) // 2
    gy = _OP_Y + (_OP_SZ - _GLYPH_SZ) // 2
    return text_box(
        glyph_id, f"MathOperator {prst}", gx, gy, _GLYPH_SZ, _GLYPH_SZ,
        [paragraph([])], fill=BLACK, line_color=BLACK, line_width=12_700,
        anchor="ctr", prst=prst, tx_box=False)


def _chain(base_id: int, x0: int, cards: list, ops: list) -> str:
    """Lay out a 3-card formula chain joined by bare math operators across its
    span. Each operator still consumes two shape ids (kept for stable id spacing)."""
    parts = []
    cx = x0
    cid = base_id
    for i, (header, body) in enumerate(cards):
        parts.append(_formula_card(cid, cx, header, body)); cid += 1
        cx += _FCARD_W
        if i < len(ops):
            cx += _FCARD_GAP
            parts.append(_operator_chip(cid, cid + 1, cx, ops[i])); cid += 2
            cx += _OP_SZ + _FCARD_GAP
    return "".join(parts)


def _cut_card(sp_id: int, x: int, y: int, cap: str, value: str, subline: str) -> str:
    """Scenario cut card: BLUE_4, white - 8pt caps cap, 12.5pt value, 7.8pt subline."""
    return text_box(
        sp_id, "ScenarioCut", x, y, _CUT_W, _CUT_H,
        [paragraph([run(cap, size=_SZ_CARD, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=_GAP_VAL),
         paragraph([run(value, size=_SZ_CUTVAL, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=_GAP_VAL),
         paragraph([run(subline, size=_SZ_FN, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=BLUE_4, line_width=12_700, anchor="ctr", insets=(80_000, 22_000, 80_000, 22_000))


def _footnote(sp_id: int, y: int, lead: str, body: str) -> str:
    """No-fill / no-border table footnote: 7.8pt italic, bold lead phrase."""
    return text_box(
        sp_id, "TableFootnote", _TABLE_X, y, _TABLE_W, _FN_H,
        [paragraph([run(lead, size=_SZ_FN, bold=True, italic=True, color=BLACK, font=FONT),
                    run(body, size=_SZ_FN, italic=True, color=BLACK, font=FONT)],
                   line_spacing=106_000)],
        fill=None, line_color=None, anchor="t", insets=(0, 14_000, 40_000, 14_000))


def _commentary(sp_id: int, x: int, finding: str, bullet: str) -> str:
    """No-fill / no-border commentary: 9.5pt bold finding over an 8.5pt bullet."""
    return text_box(
        sp_id, "Commentary", x, _COMM_Y, _COMM_W, _COMM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=_GAP_FIND, line_spacing=108_000),
         paragraph([run(bullet, size=_SZ_BODY, color=BLACK, font=FONT)],
                   bullet=True, line_spacing=106_000)],
        fill=None, line_color=None, anchor="t", insets=(0, 20_000, 40_000, 20_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(
            "FY2022–FY2027 average annual TAM and SAM; constant FY2026 dollars. The "
            "supplier-share step supplies the fixed TAM dollar pool; the evidence "
            "classifier supplies modeled work-type shares and residual.",
            size=_SZ_BODY, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    output_chip = text_box(
        11, "OutputChip", BODY_X, _CHIP_Y, BODY_CX, _CHIP_H,
        [paragraph([
            run("Allocation output: ", size=900, bold=True, color=BLACK, font=FONT),
            run("work-type TAM, broad component SAM, and scenario SAM views. "
                "Scenario views overlap; they are not additive markets.",
                size=900, color=BLACK, font=FONT)])],
        fill=BLUE_1, line_width=12_700, anchor="ctr", insets=(140_000, 32_000, 140_000, 32_000))

    # Formula / reconciliation strip: light panel (behind) + the two card chains.
    strip_panel = text_box(
        12, "FormulaStrip", BODY_X, _STRIP_Y, BODY_CX, _STRIP_H, [paragraph([])],
        fill=GRAY_1, line_width=12_700, anchor="ctr")
    chains = (_chain(100, _LEFT_X0, _LEFT_CHAIN, _LEFT_OPS)
              + _chain(120, _RIGHT_X0, _RIGHT_CHAIN, _RIGHT_OPS))

    # Left column: label, native crosswalk table, two footnotes.
    table_label = text_box(
        20, "TableLabel", _TABLE_X, _TLABEL_Y, _TABLE_W, _TLABEL_H,
        [paragraph([run("Work-type allocation: mutually exclusive homes mapped "
                        "into overlapping scenario views",
                        size=_SZ_LABEL, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    table_xml = _crosswalk_table(21)
    footnotes = "".join(
        _footnote(22 + i, _FN_Y0 + i * (_FN_H + _FN_GAP), lead, body)
        for i, (lead, body) in enumerate(_FOOTNOTES))

    # Right column: rail header, broad envelope card, 2x2 cut grid, caveat chip.
    rail_header = text_box(
        30, "ScenarioRailHeader", _RAIL_X, _RH_Y, _RAIL_W, _RH_H,
        [paragraph([run("SCENARIO VIEWS: CUTS OF ONE TAM POOL",
                        size=_SZ_LABEL, bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=(120_000, 40_000, 120_000, 40_000))
    broad = text_box(
        31, "ScenarioBroad", _RAIL_X, _BROAD_Y, _RAIL_W, _BROAD_H,
        [paragraph([run("BROAD COMPONENT MFG", size=_SZ_BODY, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=120),
         paragraph([run("$3.5B / yr", size=_SZ_BROAD, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=120),
         paragraph([run("$21.2B cumulative; all seven named work-type homes",
                        size=_SZ_CARD, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=BLUE_2, line_width=12_700, anchor="ctr",
        insets=(150_000, 80_000, 150_000, 80_000))
    grid = []
    for i, (cap, value, subline) in enumerate(_CUTS):
        gx = _RAIL_X + (i % 2) * (_CUT_W + _CUT_GAP)
        gy = _GRID_Y + (i // 2) * (_CUT_H + _CUT_GAP)
        grid.append(_cut_card(32 + i, gx, gy, cap, value, subline))
    caveat = text_box(
        36, "CaveatChip", _RAIL_X, _CAVEAT_Y, _RAIL_W, _CAVEAT_H,
        [paragraph([
            run("Do not add scenarios: ", size=_SZ_BODY, bold=True, color=BLACK, font=FONT),
            run("broad, HM&E, electrical, metal, and modular are overlapping "
                "leadership views of one fixed supplier TAM pool.",
                size=_SZ_BODY, color=BLACK, font=FONT)], line_spacing=106_000)],
        fill=GRAY_1, line_width=12_700, anchor="ctr", insets=(120_000, 40_000, 120_000, 40_000))

    commentary = "".join(_commentary(sp_id, x, finding, bullet)
                         for (sp_id, x, finding, bullet) in _FINDINGS)

    # Paint order: strip panel behind its chains; otherwise the zones don't overlap.
    return (caption + output_chip + strip_panel + chains
            + table_label + table_xml + footnotes
            + rail_header + broad + "".join(grid) + caveat
            + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
