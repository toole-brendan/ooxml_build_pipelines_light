"""s14_body_supplier_visibility - prove the supplier layer exists with visible DDG and
submarine names while making the evidence ceiling explicit: first-tier filings identify
suppliers and work-type cues but capture only a floor of total supplier flow.

Layout (no chart, no table): two side-by-side evidence panels (DDG left / submarine
right) - a program header band over a flowed row of E2E9EF supplier-name chips; two
larger program-colored evidence metric cards under the panels; a grouped missed-flow
limitation ledger (reporting limits / supply-chain depth) as two chip rows; and a
two-column no-fill commentary block that is now the slide's closing point. The former
dark focal-callout strip is removed - the title and commentary #2 already make the
point - and the freed bottom space is intentional breathing room, not a gap to backfill.

Supplier names are proof points, not a ranking, so they render as equal-weight name
chips, not a bar chart.

Spec: ds_specs/s14_body_supplier_visibility.txt (SLIDE 14 - SUPPLIER VISIBILITY).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_B, BODY_CX,
    BLUE_1, BLUE_3, BLUE_4, GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_CHIP, INSETS_CARD,
    FINEPRINT_8_5PT, DENSE_BODY_10PT, CAP_12PT,
    RIBBON_KPI_18PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Evidence"
_BREADCRUMB_TOPIC = "Supplier Visibility"
_TOPIC            = "Supplier Visibility"
_TAKEAWAY = ("Visible suppliers prove the layer exists, but first-tier filings "
             "capture only a floor.")
_SOURCES = ("Sources: (1) FFATA/FSRS subaward records and the operating-entity "
            "supplier registry, FY2017–FY2026; (2) DDG MYP-corrected outside-yards "
            "place-of-performance evidence; (3) submarine visible-supplier "
            "classification and parent-universe analysis")

_EVID_95 = 950   # 9.5pt: commentary supporting evidence (style.py allows raw sizes)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_COL_GAP = 280_000
_COL_W   = (BODY_CX - _COL_GAP) // 2            # 5_501_181
_X_L     = BODY_X                               # DDG column
_X_R     = BODY_X + _COL_W + _COL_GAP           # 6_234_260  submarine column

# Bands stack top-down: panels (header + chips), metric cards, ledger, commentary.
# With no bottom focal strip, the bands and gaps are sized to fill the body box so
# the stack reaches the bottom evenly rather than leaving a large gap below.
_PANEL_Y = BODY_Y                               # 1_371_600
_HDR_H   = 330_000
_CHIPS_Y = _PANEL_Y + _HDR_H + 60_000           # 1_761_600
_CHIPS_H = 960_000

_CARD_Y  = _CHIPS_Y + _CHIPS_H + 180_000        # 2_901_600
_CARD_H  = 900_000

_LEDG_Y  = _CARD_Y + _CARD_H + 180_000          # 3_981_600
_LEDG_ROW_H = 340_000
_LEDG_GAP   = 46_000

_COMM_Y  = _LEDG_Y + 2 * _LEDG_ROW_H + _LEDG_GAP + 200_000   # 4_907_600
_COMM_H  = BODY_B - 40_000 - _COMM_Y            # ends ~40k above the body floor


# ── Content ──────────────────────────────────────────────────────────────────
_DDG_NAMES = ["Leonardo", "Arctic Slope", "Major Tool", "GE", "Rolls-Royce",
              "Northrop Grumman", "Johnson Controls"]
_SUB_NAMES = ["Northrop Grumman", "Leonardo", "Curtiss-Wright Electro-Mechanical",
              "Scot Forge", "DC Fabricators", "Rhoads", "Graham", "Austal"]

# Evidence metric cards: (cap, value, subline, fill).
_DDG_CARD = ("DDG FFATA-VISIBLE YARD-SIDE FLOW", "~$2.7B",
             "vs estimated yard-side outsourcing midpoint ~$13.6B", BLUE_3)
_SUB_CARD = ("SUBMARINE SUPPLIER-ADDRESSABLE VISIBLE VALUE", "~$5.5B",
             "across ~150 classified recipients; broader visible parent universe ~759",
             BLUE_4)

# Missed-flow ledger groups: (label, items, fill).
_LEDGER = [
    ("Reporting limits",
     "reporting threshold and lag; yard filing differences; HII Newport News "
     "visibility gap", GRAY_1),
    ("Supply-chain depth",
     "direct material booked as direct cost; lower-tier subcontracting; standing "
     "agreements", GRAY_2),
]

_FINDINGS = [
    ("Visible supplier names prove the layer exists, not the target list.",
     "DDG and submarine filings identify real suppliers and work-type cues, but some "
     "visible names are services, prime-affiliated, or outside the physical-component "
     "boundary."),
    ("First-tier filings set a floor, not the market size.",
     "Visibility thins below tier one and varies by yard, so TAM is sized from the "
     "budget base rather than by summing subawards."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _panel_header(sp_id: int, x: int, text: str, fill: str) -> str:
    # Matches the evidence-metric-card cap: 12pt bold ALL CAPS, white, left.
    return text_box(
        sp_id, "PanelHeader", x, _PANEL_Y, _COL_W, _HDR_H,
        [paragraph([run(text, size=CAP_12PT, bold=True, color=WHITE,
                        font=FONT)], align="l")],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(160_000, 30_000, 160_000, 30_000))


def _chip_flow(base_id: int, names: list[str], x0: int, max_w: int) -> str:
    """Flow equal-weight supplier-name chips left-to-right, wrapping within max_w.
    E2E9EF fill, BLACK 8.5pt, 1pt black border - proof points, not a ranking."""
    CH, GX, GY, PAD, CHARW = 235_000, 70_000, 64_000, 175_000, 56_000
    parts: list[str] = []
    x, y, sid = x0, _CHIPS_Y, base_id
    for nm in names:
        w = len(nm) * CHARW + PAD
        if x > x0 and x + w > x0 + max_w:        # wrap to next row
            x, y = x0, y + CH + GY
        parts.append(text_box(
            sid, "NameChip", x, y, w, CH,
            [paragraph([run(nm, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
                       align="ctr")],
            fill=BLUE_1, line_width=12_700, anchor="ctr", insets=INSETS_CHIP))
        x += w + GX
        sid += 1
    return "".join(parts)


def _metric_card(sp_id: int, x: int, cap: str, value: str, subline: str,
                 fill: str) -> str:
    return text_box(
        sp_id, "EvidenceMetricCard", x, _CARD_Y, _COL_W, _CARD_H,
        [paragraph([run(cap, size=CAP_12PT, bold=True, color=WHITE, font=FONT)],
                   space_after=120),
         paragraph([run(value, size=RIBBON_KPI_18PT, bold=True, color=WHITE, font=FONT),
                    run("   " + subline, size=FINEPRINT_8_5PT, italic=True,
                        color=WHITE, font=FONT)])],
        fill=fill, line_width=12_700, anchor="ctr", insets=INSETS_CARD)


def _ledger_row(sp_id: int, y: int, label: str, items: str, fill: str) -> str:
    return text_box(
        sp_id, "MissedFlowGroup", BODY_X, y, BODY_CX, _LEDG_ROW_H,
        [paragraph([
            run(label + ":  ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
            run(items, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
        fill=fill, line_width=12_700, anchor="ctr",
        insets=(140_000, 40_000, 140_000, 40_000))


def _commentary(sp_id: int, x: int, finding: str, evidence: str) -> str:
    return text_box(
        sp_id, "Commentary", x, _COMM_Y, _COL_W, _COMM_H,
        [paragraph([run(finding, size=_EVID_95, bold=True, color=BLACK, font=FONT)],
                   space_after=90),
         paragraph([run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
                   bullet=True)],
        fill=None, line_color=None, anchor="t", insets=(40_000, 30_000, 40_000, 30_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    panels = (
        _panel_header(10, _X_L, "DDG VISIBLE SUPPLIERS", BLUE_3)
        + _panel_header(11, _X_R, "SUBMARINE VISIBLE SUPPLIERS", BLUE_4)
        + _chip_flow(100, _DDG_NAMES, _X_L, _COL_W)
        + _chip_flow(120, _SUB_NAMES, _X_R, _COL_W))

    cards = (_metric_card(20, _X_L, *_DDG_CARD)
             + _metric_card(21, _X_R, *_SUB_CARD))

    ledger = "".join(
        _ledger_row(30 + i, _LEDG_Y + i * (_LEDG_ROW_H + _LEDG_GAP), label, items, fill)
        for i, (label, items, fill) in enumerate(_LEDGER))

    commentary = "".join(
        _commentary(40 + i, (_X_L if i == 0 else _X_R), finding, evidence)
        for i, (finding, evidence) in enumerate(_FINDINGS))

    return panels + cards + ledger + commentary


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
