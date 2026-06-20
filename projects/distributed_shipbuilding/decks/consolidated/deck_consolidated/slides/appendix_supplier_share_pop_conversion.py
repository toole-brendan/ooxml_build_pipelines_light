"""appendix_supplier_share_pop_conversion - the conversion-method page: what the
supplier-share factor means and how POP evidence turns retained budget bases into
the fixed outsourced supplier TAM pool.

Calculation-machine layout (NOT a table or a ledger): an italic caption, a full-
width definition strip that names the supplier-share factor in plain English, a
POP "formula machine" (five white cards joined by real math-operator AutoShapes —
mathMultiply / mathEqual / mathDivide — that read Σ eligible POP $ × supplier-
location share ÷ Σ eligible POP $ = factor), two side-by-side program calculation
lanes (DDG additive AP/LLTM, submarine AP/LLTM reference-only) each with a colored
ribbon, a white body of two formula rows + a colored total, and small evidence
chips, then one dark combined output card (the fixed supplier TAM pool) and two
no-fill commentary findings. No native table, no chart — every object is shape-
built, and every arithmetic symbol is a vector AutoShape, not a typed glyph.

The internal step codes (the M-series) stay OUT of the visible copy: the page uses
descriptive references ("the budget-base step", "the allocation step") rather than
the codes.

Spec: specs/distributed_shipbuilding/methodology/alternative_v3/
appendix_supplier_share_pop_conversion_spec.md (SUPPLIER-SHARE / POP CONVERSION).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
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
_BREADCRUMB_TOPIC = "TAM Supplier Share"
_TOPIC            = "Methodology (3/5)"
_TAKEAWAY = ("POP evidence converts retained budget into fixed outsourced "
             "supplier TAM.")
_SOURCES = ("Sources: (1) DoD/DoW contract-announcement POP corpus, "
            "CY2022–CY2026; (2) FPDS Atom feeds and DDG MYP master-total "
            "reconstruction; (3) Navy SCN P-5c / P-10 budget exhibits, "
            "FY2022–FY2027; (4) FY 2026 Mandatory Funding Allocation Plan, "
            "PL 119-21 Sec. 20002")

# Raw point sizes (style.py allows raw sizes with a nearby note).
_SZ_DESC   = 800    # 8.0pt: formula-card desc, lane-card label, footprint labels
_SZ_BODY   = 850    # 8.5pt: caption, definition strip, commentary bullet
_SZ_LABEL  = 1000   # 10pt:  formula-machine title, lane ribbons
_SZ_HEAD   = 850    # 8.5pt: formula-card bold header
_SZ_VAL    = 1150   # 11.5pt: lane-card value
_SZ_FN     = 780    # 7.8pt: evidence chips, reference subnote (italic)
_EVID_95   = 950    # 9.5pt: commentary finding, output-card label
_SZ_OUTVAL = 1600   # 16pt:  output-card hero value
_SZ_TOTLBL = 900    # 9.0pt: lane total-card label
_SZ_TOTVAL = 1050   # 10.5pt: lane total-card value


# ── Operator + card sizing (all EMU) ─────────────────────────────────────────
_OP_SZ = 230_000          # operator-chip square
_GLYPH_SZ = 145_000       # math AutoShape inside the chip
_FM_GAP = 30_000          # formula-machine card<->chip gap
_R_GAP = 26_000           # lane-row card<->chip gap


# ── Vertical band cascade (top-down; each band = prev bottom + gap) ───────────
_CAP_Y, _CAP_H = BODY_Y, 175_000                     # italic window / numerator caption
_DEF_Y = _CAP_Y + _CAP_H + 32_000                    # definition strip
_DEF_H = 365_000
_FM_TITLE_Y = _DEF_Y + _DEF_H + 44_000
_FM_TITLE_H = 165_000
_FM_CARD_Y = _FM_TITLE_Y + _FM_TITLE_H + 6_000
_FM_CARD_H = 365_000
_FM_FOOT_Y = _FM_CARD_Y + _FM_CARD_H + 12_000
_FM_FOOT_H = 128_000
_LANE_Y = _FM_FOOT_Y + _FM_FOOT_H + 38_000           # lane ribbon top
_RIBBON_H = 175_000
_BP_Y = _LANE_Y + _RIBBON_H                           # lane body-panel top
_BP_H = 1_640_000
_FOOTER_Y = _BP_Y + _BP_H + 10_000                    # evidence-chip footer
_FOOTER_H = 200_000
_OB_Y = _FOOTER_Y + _FOOTER_H + 40_000                # output + commentary band
_OB_H = BODY_B - _OB_Y

# ── Horizontal geometry (all EMU) ────────────────────────────────────────────
# Formula machine: 5 cards across the full body width.
_FM_CARD_W = (BODY_CX - 4 * _OP_SZ - 8 * _FM_GAP) // 5

# Two program lanes, each half-width.
_LANE_GAP = 280_000
_LANE_W = (BODY_CX - _LANE_GAP) // 2
_DDG_X = BODY_X
_SUB_X = BODY_X + _LANE_W + _LANE_GAP
_BP_PAD_X = 100_000
_LANE_INNER_W = _LANE_W - 2 * _BP_PAD_X
_DDG_INNER_X = _DDG_X + _BP_PAD_X
_SUB_INNER_X = _SUB_X + _BP_PAD_X
_R_CARD_W = (_LANE_INNER_W - 2 * _OP_SZ - 4 * _R_GAP) // 3

# Footprint mini-labels under the formula machine (two halves).
_FP_GAP = 280_000
_FP_W = (BODY_CX - _FP_GAP) // 2

# Lane body internal stack (relative to _BP_Y). Row1 and the colored total align
# across lanes; DDG separates its two rows with a "+" chip, submarine with the
# reference subnote, so their middle gaps differ but the totals line up.
_BP_PAD_Y = 80_000
_CARD_H = 395_000
_TOTAL_H = 395_000
_ROW1_DY = _BP_PAD_Y
_DDG_GAP1 = 230_000
_DDG_GAP2 = 65_000
_SUB_GAP1 = 90_000
_DDG_ROW2_DY = _ROW1_DY + _CARD_H + _DDG_GAP1
_SUB_ROW2_DY = _ROW1_DY + _CARD_H + _SUB_GAP1
_TOTAL_DY = _ROW1_DY + 2 * _CARD_H + _DDG_GAP1 + _DDG_GAP2
_PLUS_DY = _ROW1_DY + _CARD_H                              # "+" centered in DDG gap1
_SUB_SUBNOTE_DY = _SUB_ROW2_DY + _CARD_H + 20_000

# Output + commentary band.
_OUT_W = 5_300_000
_CMT_GAP = 280_000
_CMT_X = BODY_X + _OUT_W + _CMT_GAP
_CMT_W = BODY_R - _CMT_X
_CMT_BOX1_H = 520_000
_CMT_BOX_GAP = 44_000

# Definition strip uses the full width; no separate workbook-term chip.
_DEF_RINS = 140_000


# ── Content ──────────────────────────────────────────────────────────────────
_FM_CELLS = [
    ("Eligible POP dollars", "Confirmed gated in-scope"),
    ("Supplier-location share", "Other US + Foreign POP %"),
    ("Weighted supplier dollars", "Dollar-weighted footprint"),
    ("Eligible POP dollars", "Same gated denominator"),
    ("Supplier-share factor", "Applied to retained base"),
]
_FM_OPS = ["mathMultiply", "mathEqual", "mathDivide", "mathEqual"]

_DDG_ROW1 = [("BC + OBBBA mandatory base", "$21.5B"),
             ("BC supplier-share factor", "13%"),
             ("BC supplier TAM", "$2.7B")]
_DDG_ROW2 = [("Retained AP/LLTM base", "$1.5B"),
             ("AP/LLTM supplier factor", "85%"),
             ("AP/LLTM supplier TAM", "$1.2B")]
_DDG_FOOTER = ["154 modeled POP actions", "$21.7B gated corpus",
               "$6.1B excluded / GFE", "$14.6B MYP restored"]

_SUB_ROW1 = [("BC + OBBBA mandatory base", "$60.6B"),
             ("BC supplier-share factor", "35%"),
             ("BC supplier TAM", "$21.2B")]
_SUB_ROW2 = [("AP/LLTM additive base", "$0"),
             ("Reference factor", "48%"),
             ("Additive TAM", "$0")]
_SUB_SUBNOTE = ("AP/LLTM is supplier evidence, not incremental TAM: already "
                "inside BC or out of scope.")
_SUB_FOOTER = ["658 POP rows", "$25.4B gated corpus", "$6.1B excluded / GFE"]

_COMMENTARY = [
    ("The supplier-share factor is a conversion rate, not an award total.",
     "POP records estimate the supplier share of retained budget dollars; the "
     "Navy budget base still supplies the TAM dollars."),
    ("DDG and submarine stay separate until outputs are summed.",
     "The two programs have different yard footprints and AP/LLTM treatment, so "
     "the model sums TAM dollars rather than blending supplier-share factors."),
]


# ── Primitive builders ───────────────────────────────────────────────────────
def _op(chip_id: int, glyph_id: int, x: int, y: int, prst: str) -> str:
    """Bare math operator AutoShape (vector geometry, font-independent): no gray
    backing chip. Black fill is the ink, the outline matches the fill so no rim
    prints, the box is square and the text body is empty. See
    ooxml_arithmetic_shapes_conventions.md."""
    _ = chip_id  # retained so existing call sites / id spacing do not change
    gx = x + (_OP_SZ - _GLYPH_SZ) // 2
    gy = y + (_OP_SZ - _GLYPH_SZ) // 2
    return text_box(
        glyph_id, f"MathOperator {prst}", gx, gy, _GLYPH_SZ, _GLYPH_SZ,
        [paragraph([])],
        fill=BLACK, line_color=BLACK, line_width=12_700,
        anchor="ctr", prst=prst, tx_box=False)


def _two_line_card(sp_id: int, x: int, y: int, w: int, h: int, line1: str,
                   line2: str, *, fill: str = WHITE, l1_sz: int, l1_bold: bool,
                   l2_sz: int, l2_bold: bool, l2_color: str = BLACK) -> str:
    """A centered two-line card: an upper line over a lower line. Drives both the
    formula-machine cards (bold name + plain desc) and the lane calc cards
    (plain label + bold value)."""
    return text_box(
        sp_id, "Card", x, y, w, h,
        [paragraph([run(line1, size=l1_sz, bold=l1_bold, color=BLACK, font=FONT)],
                   align="ctr", space_after=110, line_spacing=104_000),
         paragraph([run(line2, size=l2_sz, bold=l2_bold, color=l2_color, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(40_000, 40_000, 40_000, 40_000))


def _card_chain(base_id: int, x0: int, y: int, card_w: int, card_h: int,
                gap: int, cells: list, ops: list, *, fill: str = WHITE,
                l1_sz: int, l1_bold: bool, l2_sz: int, l2_bold: bool,
                l2_color: str = BLACK) -> str:
    """Lay out cards joined by bare math operators across a span. Each operator
    still consumes two shape ids (kept for stable downstream id spacing)."""
    parts = []
    cid = base_id
    cx = x0
    for i, (l1, l2) in enumerate(cells):
        parts.append(_two_line_card(cid, cx, y, card_w, card_h, l1, l2, fill=fill,
                                    l1_sz=l1_sz, l1_bold=l1_bold, l2_sz=l2_sz,
                                    l2_bold=l2_bold, l2_color=l2_color))
        cid += 1
        cx += card_w
        if i < len(ops):
            cx += gap
            parts.append(_op(cid, cid + 1, cx, y + (card_h - _OP_SZ) // 2, ops[i]))
            cid += 2
            cx += _OP_SZ + gap
    return "".join(parts)


def _chain_card_x(x0: int, i: int, card_w: int, gap: int) -> int:
    """Left x of card i in a _card_chain (card pitch = card_w + 2*gap + op)."""
    return x0 + i * (card_w + 2 * gap + _OP_SZ)


def _ribbon(sp_id: int, x: int, fill: str, text: str) -> str:
    """Lane header ribbon: white 10pt bold all-caps, sits atop the body panel."""
    return text_box(
        sp_id, "LaneRibbon", x, _LANE_Y, _LANE_W, _RIBBON_H,
        [paragraph([run(text, size=_SZ_LABEL, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(110_000, 12_000, 110_000, 12_000))


def _panel(sp_id: int, x: int) -> str:
    """White lane body panel (the cards sit on top of it)."""
    return text_box(sp_id, "LanePanel", x, _BP_Y, _LANE_W, _BP_H, [paragraph([])],
                    fill=WHITE, line_width=12_700, anchor="ctr")


def _total(sp_id: int, x: int, fill: str, label: str, value: str) -> str:
    """Colored lane total card spanning the panel inner width."""
    return text_box(
        sp_id, "LaneTotal", x, _BP_Y + _TOTAL_DY, _LANE_INNER_W, _TOTAL_H,
        [paragraph([run(label, size=_SZ_TOTLBL, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=120, line_spacing=104_000),
         paragraph([run(value, size=_SZ_TOTVAL, bold=True, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(80_000, 40_000, 80_000, 40_000))


def _footer(base_id: int, x: int, chips: list) -> str:
    """Row of small F2F2F2 evidence chips (3 or 4) across the lane width."""
    n = len(chips)
    gap = 40_000
    cw = (_LANE_W - (n - 1) * gap) // n
    parts = []
    for i, txt in enumerate(chips):
        cx = x + i * (cw + gap)
        parts.append(text_box(
            base_id + i, "EvidenceChip", cx, _FOOTER_Y, cw, _FOOTER_H,
            [paragraph([run(txt, size=_SZ_FN, bold=True, color=BLACK, font=FONT)],
                       align="ctr", line_spacing=104_000)],
            fill=GRAY_1, line_width=12_700, anchor="ctr",
            insets=(36_000, 28_000, 36_000, 28_000)))
    return "".join(parts)


def _commentary(sp_id: int, y: int, h: int, finding: str, bullet: str) -> str:
    """No-fill / no-border commentary: 9.5pt bold finding over an 8.5pt bullet."""
    return text_box(
        sp_id, "Commentary", _CMT_X, y, _CMT_W, h,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=180, line_spacing=108_000),
         paragraph([run(bullet, size=_SZ_BODY, color=BLACK, font=FONT)],
                   bullet=True, line_spacing=106_000)],
        fill=None, line_color=None, anchor="t", insets=(0, 18_000, 30_000, 18_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        12, "Caption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(
            "FY2022–FY2027 retained budget bases from the budget-base step. POP "
            "records estimate supplier share; they are not summed as the TAM "
            "numerator.", size=_SZ_BODY, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # Definition strip.
    def_strip = text_box(
        10, "DefinitionStrip", BODY_X, _DEF_Y, BODY_CX, _DEF_H,
        [paragraph([
            run("Supplier-share factor", size=_SZ_BODY, bold=True,
                color=BLACK, font=FONT),
            run(" = conversion rate that turns retained budget dollars into "
                "outsourced supplier TAM. It answers: ",
                size=_SZ_BODY, color=BLACK, font=FONT),
            run("for every $1 of retained budget base, how many cents become "
                "supplier work?", size=_SZ_BODY, italic=True,
                color=BLACK, font=FONT)
        ], line_spacing=108_000)],
        fill=BLUE_1, line_width=12_700, anchor="ctr",
        insets=(140_000, 40_000, _DEF_RINS, 40_000))

    # Formula machine: title, five cards joined by × = ÷ = operators, footprints.
    fm_title = text_box(
        20, "FormulaTitle", BODY_X, _FM_TITLE_Y, BODY_CX, _FM_TITLE_H,
        [paragraph([run("How POP evidence becomes the supplier-share factor",
                        size=_SZ_LABEL, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    fm_cards = _card_chain(100, BODY_X, _FM_CARD_Y, _FM_CARD_W, _FM_CARD_H, _FM_GAP,
                           _FM_CELLS, _FM_OPS, l1_sz=_SZ_HEAD, l1_bold=True,
                           l2_sz=_SZ_DESC, l2_bold=False)
    fp_ddg = text_box(
        30, "DDGFootprint", BODY_X, _FM_FOOT_Y, _FP_W, _FM_FOOT_H,
        [paragraph([
            run("DDG footprint: ", size=_SZ_DESC, bold=True, color=BLACK, font=FONT),
            run("BIW % + Ingalls % excluded; Other US % + Foreign % counted as "
                "supplier share.", size=_SZ_DESC, italic=True, color=BLACK, font=FONT)],
            line_spacing=104_000)],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    fp_sub = text_box(
        31, "SubFootprint", BODY_X + _FP_W + _FP_GAP, _FM_FOOT_Y, _FP_W, _FM_FOOT_H,
        [paragraph([
            run("Submarine footprint: ", size=_SZ_DESC, bold=True, color=BLACK, font=FONT),
            run("EB % + HII % excluded; Other US % + Foreign % counted as "
                "supplier share.", size=_SZ_DESC, italic=True, color=BLACK, font=FONT)],
            line_spacing=104_000)],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # DDG lane: ribbon, panel, two formula rows, "+" chip, total, footer chips.
    ddg_plus_x = (_chain_card_x(_DDG_INNER_X, 2, _R_CARD_W, _R_GAP)
                  + (_R_CARD_W - _OP_SZ) // 2)
    ddg = (_ribbon(200, _DDG_X, BLUE_3, "DDG: ADDITIVE AP/LLTM STREAM")
           + _panel(201, _DDG_X)
           + _card_chain(210, _DDG_INNER_X, _BP_Y + _ROW1_DY, _R_CARD_W, _CARD_H,
                         _R_GAP, _DDG_ROW1, ["mathMultiply", "mathEqual"],
                         l1_sz=_SZ_DESC, l1_bold=False, l2_sz=_SZ_VAL, l2_bold=True)
           + _op(218, 219, ddg_plus_x, _BP_Y + _PLUS_DY, "mathPlus")
           + _card_chain(220, _DDG_INNER_X, _BP_Y + _DDG_ROW2_DY, _R_CARD_W, _CARD_H,
                         _R_GAP, _DDG_ROW2, ["mathMultiply", "mathEqual"],
                         l1_sz=_SZ_DESC, l1_bold=False, l2_sz=_SZ_VAL, l2_bold=True)
           + _total(230, _DDG_INNER_X, BLUE_3, "DDG supplier TAM",
                    "$4.0B cumulative / $659M per year")
           + _footer(240, _DDG_X, _DDG_FOOTER))

    # Submarine lane: ribbon, panel, BC row, gray reference row, subnote, total, footer.
    sub_subnote = text_box(
        330, "RefSubnote", _SUB_INNER_X, _BP_Y + _SUB_SUBNOTE_DY, _LANE_INNER_W,
        165_000,
        [paragraph([run(_SUB_SUBNOTE, size=_SZ_FN, italic=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    sub = (_ribbon(300, _SUB_X, BLUE_4, "SUBMARINE: AP/LLTM REFERENCE-ONLY")
           + _panel(301, _SUB_X)
           + _card_chain(310, _SUB_INNER_X, _BP_Y + _ROW1_DY, _R_CARD_W, _CARD_H,
                         _R_GAP, _SUB_ROW1, ["mathMultiply", "mathEqual"],
                         l1_sz=_SZ_DESC, l1_bold=False, l2_sz=_SZ_VAL, l2_bold=True)
           + _card_chain(320, _SUB_INNER_X, _BP_Y + _SUB_ROW2_DY, _R_CARD_W, _CARD_H,
                         _R_GAP, _SUB_ROW2, ["mathMultiply", "mathEqual"], fill=GRAY_1,
                         l1_sz=_SZ_DESC, l1_bold=False, l2_sz=_SZ_VAL, l2_bold=True)
           + sub_subnote
           + _total(340, _SUB_INNER_X, BLUE_4, "Submarine supplier TAM",
                    "$21.2B cumulative / $3.5B per year")
           + _footer(350, _SUB_X, _SUB_FOOTER))

    # Combined fixed-TAM output card (dark) + two no-fill commentary findings.
    output = text_box(
        400, "FixedTAMOutput", BODY_X, _OB_Y, _OUT_W, _OB_H,
        [paragraph([run("FIXED OUTSOURCED SUPPLIER TAM", size=_EVID_95, bold=True,
                        color=WHITE, font=FONT)], align="ctr", space_after=150,
                   line_spacing=104_000),
         paragraph([run("$25.2B cumulative / $4.2B per year", size=_SZ_OUTVAL,
                        bold=True, color=WHITE, font=FONT)], align="ctr",
                   space_after=150, line_spacing=104_000),
         paragraph([run("This is the fixed dollar pool the allocation step will "
                        "slice; SAM does not resize it.", size=900, color=WHITE,
                        font=FONT)], align="ctr", line_spacing=106_000)],
        fill=BLUE_5, line_width=12_700, anchor="ctr",
        insets=(160_000, 70_000, 160_000, 70_000))

    box2_y = _OB_Y + _CMT_BOX1_H + _CMT_BOX_GAP
    box2_h = _OB_H - _CMT_BOX1_H - _CMT_BOX_GAP
    commentary = (_commentary(410, _OB_Y, _CMT_BOX1_H, *_COMMENTARY[0])
                  + _commentary(411, box2_y, box2_h, *_COMMENTARY[1]))

    return (caption + def_strip
            + fm_title + fm_cards + fp_ddg + fp_sub
            + ddg + sub
            + output + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
