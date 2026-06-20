"""s09_body_tam_bridge_ap_lltm - bridge each program's supplier TAM separately and
end on one combined output, making the asymmetric AP/LLTM rule visible: additive for
DDG (its filtered stream sits on top of a net-of-AP Basic Construction base) and
reference-only for submarine (additive base $0, because supplier long-lead already
sits inside Basic Construction).

Pattern B: one full-width shape-built exhibit (no native chart, no table) - a left
DDG compact waterfall (five colored step cards), a right submarine formula card
stack (four cards), and a center-bottom combined output card (the slide's one 24pt
value). A no-fill units caption sits above; three InterpBox cards sit below.

Spec: ds_specs/s09_body_tam_bridge_ap_lltm.txt (SLIDE 09 - TAM BRIDGE AND AP/LLTM).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, CAP_12PT,
    EXHIBIT_HEADER_13PT, VALUE_14PT, BADGE_16PT, RIBBON_KPI_18PT, ANSWER_KPI_24PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Sizing Methodology"
_BREADCRUMB_TOPIC = "TAM Bridge"
_TOPIC            = "TAM Bridge"
_TAKEAWAY = ("Combined supplier TAM is $4.2B per year, but AP/LLTM is additive for "
             "DDG and reference-only for submarine.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c Basic Construction and AP/LLTM budget "
            "justification, FY2022–FY2027; (2) DDG MYP-corrected outside-yards "
            "place-of-performance evidence; (3) submarine coefficient and AP/LLTM "
            "boundary analysis; (4) FY 2026 Mandatory Funding Allocation Plan, "
            "PL 119-21 Sec. 20002")

_UNITS = ("Supplier TAM bridge, $B cumulative and $M per year; constant FY2026 "
          "dollars, incl. OBBBA Sec. 20002 mandatory funding. Each program is "
          "bridged separately, then summed.")

_TIGHT = 100_000   # 100% line spacing for the compact bridge cards
_CARD_INSETS = (150_000, 50_000, 150_000, 50_000)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Heading band stays readable, but the one-line units caption is tightened so the
# bridge can sit a bit higher and leave room for longer merge arrows below it.
_CAP_Y, _CAP_H = BODY_Y, 180_000               # units caption (one line)

# Two bridge columns with a center gutter.
_GUTTER = 240_000
_COL_W  = (BODY_CX - _GUTTER) // 2             # 5_521_181
_DDG_X  = BODY_X                               # left column (DDG)
_SUB_X  = BODY_X + _COL_W + _GUTTER            # right column (submarine)

# Column headers, then the bridge bodies, then the combined output card.
_HDR_Y, _HDR_H = _CAP_Y + _CAP_H + 50_000, 250_000     # 1_601_600
_BRIDGE_TOP = _HDR_Y + _HDR_H + 40_000                  # 1_891_600

# InterpBox cards pinned to the bottom; the exhibit fills above them. Reclaim the
# gap above the InterpBox row so the bridge cards stand taller.
_CARDS_H = 1_010_000
_CARDS_Y = BODY_B - _CARDS_H                    # 4_860_000
_EXH_BOT = _CARDS_Y - 60_000                    # 4_800_000

_COMB_H = 560_000
_COMB_Y = _EXH_BOT - _COMB_H                    # 4_240_000
_COMB_W = 7_000_000
_COMB_X = BODY_X + (BODY_CX - _COMB_W) // 2     # 2_594_260

_ARROW_H = 280_000                              # longer merge arrows into the output
_BRIDGE_BOT = _COMB_Y - _ARROW_H                # 3_960_000
_BRIDGE_H   = _BRIDGE_BOT - _BRIDGE_TOP         # 2_068_400

# DDG = five uniform step cards; submarine = four uniform formula cards.
_DDG_GAP = 35_000
_DDG_H   = (_BRIDGE_H - 4 * _DDG_GAP) // 5       # ~385_680
_SUB_GAP = 40_000
_SUB_H   = (_BRIDGE_H - 3 * _SUB_GAP) // 4       # ~487_100

# Three InterpBox cards across the full width.
_IGAP = 200_000
_IW   = (BODY_CX - 2 * _IGAP) // 3               # 3_627_454
_IX   = [BODY_X + i * (_IW + _IGAP) for i in range(3)]


# ── Content ──────────────────────────────────────────────────────────────────
# DDG waterfall: (label, value, sub-value, fill, fg, value_size). Stream and
# endpoint elements are 6E91B1/white; base E2E9EF, scope removal D9D9D9, AP/LLTM
# B6C8D8, all black.
_DDG_STEPS = [
    ("BC construction base", "$21.5B cumulative",
     "incl. $3.4B OBBBA mandatory (Sec. 20002(17))", BLUE_1, BLACK, VALUE_14PT),
    ("Less prime, co-prime, and GFE place-of-performance", "$18.8B removed",
     "scope removal", GRAY_2, BLACK, VALUE_14PT),
    ("BC supplier stream", "$2.7B cumulative", "$451M per year",
     BLUE_3, WHITE, VALUE_14PT),
    ("Add AP/LLTM stream", "$1.2B cumulative", "$208M per year",
     BLUE_2, BLACK, VALUE_14PT),
    ("DDG supplier TAM", "$4.0B cumulative", "$659M per year",
     BLUE_3, WHITE, BADGE_16PT),
]

# Submarine formula stack: (label, value, qualifier, fill, fg).
_SUB_CARDS = [
    ("Basic Construction base", "$60.6B cumulative",
     "incl. $2.7B OBBBA mandatory (Sec. 20002(16))", BLUE_1, BLACK),
    ("Applied supplier share", "35%", "strict, non-nuclear, yard-excluded",
     BLUE_2, BLACK),
    ("Submarine supplier TAM", "$21.2B cumulative", "$3.5B per year",
     BLUE_4, WHITE),
    ("Additive AP/LLTM base", "$0", "supplier long-lead already inside Basic Construction",
     GRAY_2, BLACK),
]

_INTERP = [
    ("DDG has two additive supplier streams.",
     "Basic Construction supplier work is $451M per year and filtered AP/LLTM adds "
     "$208M per year, because DDG Basic Construction is net of prior-year AP."),
    ("Submarine AP/LLTM stays reference-only.",
     "The 35% supplier share on $60.6B of Basic Construction yields $3.5B per "
     "year; supplier long-lead material already sits inside the boundary, so "
     "additive AP/LLTM remains $0."),
    ("The combined TAM sums dollars, not rules.",
     "DDG and submarine outputs sum to $4.2B per year and $25.2B cumulative; the "
     "AP/LLTM treatment remains program-specific and should not be blended."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _header(sp_id: int, x: int, text: str) -> str:
    return text_box(
        sp_id, "BridgeHeader", x, _HDR_Y, _COL_W, _HDR_H,
        [paragraph([run(text, size=EXHIBIT_HEADER_13PT, bold=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)


def _ddg_step(sp_id: int, y: int, label: str, value: str, sub: str | None,
              fill: str, fg: str, value_size: int) -> str:
    val_runs = [run(value, size=value_size, bold=True, color=fg, font=FONT)]
    if sub:
        val_runs.append(run("   " + sub, size=LABEL_9PT, color=fg, font=FONT))
    line_w = 12_700 if value_size == BADGE_16PT else 9_525   # endpoint gets a full 1pt outline
    return text_box(
        sp_id, "DdgStep", _DDG_X, y, _COL_W, _DDG_H,
        [paragraph([run(label, size=LABEL_9PT, bold=True, color=fg, font=FONT)],
                   space_after=120, line_spacing=_TIGHT),
         paragraph(val_runs, line_spacing=_TIGHT)],
        fill=fill, line_width=line_w, anchor="ctr", insets=_CARD_INSETS)


def _sub_card(sp_id: int, y: int, label: str, value: str, qualifier: str | None,
              fill: str, fg: str) -> str:
    val_runs = [run(value, size=RIBBON_KPI_18PT, bold=True, color=fg, font=FONT)]
    if qualifier:
        val_runs.append(run("   " + qualifier, size=FINEPRINT_8_5PT, italic=True,
                            color=fg, font=FONT))
    line_w = 12_700 if fill == BLUE_4 else 9_525   # endpoint gets a full 1pt outline
    return text_box(
        sp_id, "SubCard", _SUB_X, y, _COL_W, _SUB_H,
        [paragraph([run(label, size=DENSE_BODY_10PT, bold=True, color=fg, font=FONT)],
                   space_after=110, line_spacing=_TIGHT),
         paragraph(val_runs, line_spacing=_TIGHT)],
        fill=fill, line_width=line_w, anchor="ctr", insets=_CARD_INSETS)


def _interp_card(sp_id: int, x: int, title: str, body: str) -> str:
    # Pattern B interpretation card: bold 9pt title over a bulleted 9pt body, so the
    # hierarchy reads through bold + bullet rather than a larger parent font.
    return text_box(
        sp_id, "InterpBox", x, _CARDS_Y, _IW, _CARDS_H,
        [paragraph([run(title, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   space_after=100),
         paragraph([run(body, size=LABEL_9PT, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t", insets=(60_000, 40_000, 60_000, 40_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "UnitsCaption", BODY_X, _CAP_Y, BODY_CX, _CAP_H,
        [paragraph([run(_UNITS, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    headers = _header(11, _DDG_X, "DDG supplier TAM bridge") \
        + _header(12, _SUB_X, "Submarine supplier TAM bridge")

    ddg = "".join(
        _ddg_step(20 + i, _BRIDGE_TOP + i * (_DDG_H + _DDG_GAP),
                  label, value, sub, fill, fg, vsize)
        for i, (label, value, sub, fill, fg, vsize) in enumerate(_DDG_STEPS))

    sub = "".join(
        _sub_card(30 + i, _BRIDGE_TOP + i * (_SUB_H + _SUB_GAP),
                  label, value, qual, fill, fg)
        for i, (label, value, qual, fill, fg) in enumerate(_SUB_CARDS))

    # Merge arrows from each column's bottom into the combined output card.
    ddg_cx = _DDG_X + _COL_W // 2
    sub_cx = _SUB_X + _COL_W // 2
    arrows = (
        connector(40, "DdgToCombined", ddg_cx, _BRIDGE_BOT, 0, _COMB_Y - _BRIDGE_BOT,
                  color=BLACK, width=12_700, arrow=True)
        + connector(41, "SubToCombined", sub_cx, _BRIDGE_BOT, 0, _COMB_Y - _BRIDGE_BOT,
                    color=BLACK, width=12_700, arrow=True))

    combined = text_box(
        45, "CombinedOutput", _COMB_X, _COMB_Y, _COMB_W, _COMB_H,
        [paragraph([run("COMBINED SUPPLIER TAM", size=CAP_12PT, bold=True,
                        color=WHITE, font=FONT)], align="ctr", space_after=120,
                   line_spacing=_TIGHT),
         paragraph([run("$4.2B per year", size=ANSWER_KPI_24PT, bold=True,
                        color=WHITE, font=FONT),
                    run("    $25.2B cumulative", size=FINEPRINT_8_5PT, italic=True,
                        color=WHITE, font=FONT)], align="ctr", line_spacing=_TIGHT)],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=_CARD_INSETS)

    interp = "".join(
        _interp_card(50 + i, _IX[i], title, body)
        for i, (title, body) in enumerate(_INTERP))

    # Paint order: arrows behind, then cards, combined output, interp.
    return (arrows + caption + headers + ddg + sub + combined + interp)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
