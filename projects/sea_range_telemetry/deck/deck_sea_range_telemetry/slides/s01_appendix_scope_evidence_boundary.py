"""s01_appendix_scope_evidence_boundary - set the modeling boundary before any TAM
or SAM math: what is being sized (sea-range telemetry / maritime range-support), what
evidence feeds it, and what makes work ASV-addressable (vessel share AND role share).

Shape-built boundary map (no chart). A central model-boundary card defines the
sized object (market name, paired TAM / SAM definitions, the ASV-addressable definition);
four evidence-source cards stack on the left and merge into the card through a black bus +
arrow; two addressability gate chips (vessel share AND role share) sit beneath it. A
compact scope ledger (native table, dark header, light included / excluded cell tints) sits right.
Two no-fill commentary findings run along the bottom; a small gray caveat chip flags the
future-capture exclusion. No market-size values appear.

Spec: specs/sea_range_telemetry/s01_appendix_scope_evidence_boundary.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell_rich, trun,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    CAP_12PT, BADGE_16PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Methodology"
_BREADCRUMB_TOPIC = "Scope & Boundary"
_TOPIC            = "Scope"
_TAKEAWAY = ("The model sizes current U.S. and Europe maritime range-support "
             "spend before applying ASV addressability gates.")
_SOURCES = ("Sources: (1) USAspending.gov / FPDS award records and DoD FY2027 "
            "Budget Justification Books; (2) DOT&E FY2025 Annual Report, NAVAIR "
            "VX-30, NASA Wallops, and Point Mugu Sea Range EIS / OEIS; "
            "(3) QinetiQ FY25 Annual Report, U.K. MOD LTPA / MSCA releases, "
            "DGA EM, CNES / CSG, FMV, Andøya Space, SaxaVord, and company analysis")

_QUALIFIER = "Current annualized view; U.S. and Europe; USD $M"
_CAVEAT = "Current SAM excludes future capture upside"

# Raw sizes with no exact token (style.py allows raw sizes with a note).
_SZ_83 = 830    # 8.3pt: dense ledger / evidence-card body
_SZ_8  = 800    # 8pt:   chip subline


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Three columns: evidence cards (left) -> bus -> central card (centre) -> ledger.
_LEFT_X = BODY_X                       # evidence-source cards
_LEFT_W = 2_400_000
_LEFT_R = _LEFT_X + _LEFT_W            # 2_853_079
_BUS_X  = _LEFT_R + 120_000           # 2_973_079  vertical merge bus
_CEN_X  = 3_303_079                    # central model-boundary card
_CEN_W  = 3_600_000
_CEN_R  = _CEN_X + _CEN_W              # 6_903_079
_LED_X  = 7_253_079                    # scope ledger (native table)
_LED_W  = BODY_R - _LED_X             # 4_482_362

# Top band: qualifier (left) + caveat chip (right), then the exhibit zone.
_QUAL_Y, _QUAL_H = BODY_Y, 250_000
_EXH_Y  = BODY_Y + 320_000            # 1_691_600  exhibit top (cards / card / ledger align)

_CAVEAT_W = 2_150_000
_CAVEAT_X = BODY_R - _CAVEAT_W
_CAVEAT_Y = BODY_Y
_CAVEAT_H = 300_000

# Bottom commentary band.
_COMM_H = 880_000
_COMM_Y = BODY_B - _COMM_H            # 4_990_000
_EXH_H  = _COMM_Y - _EXH_Y - 90_000  # 3_208_400

# Evidence cards: four stacked, filling the exhibit zone.
_EV_GAP = 120_000
_EV_H   = (_EXH_H - 3 * _EV_GAP) // 4  # 712_100

def _ev_y(i: int) -> int:
    return _EXH_Y + i * (_EV_H + _EV_GAP)

def _ev_mid(i: int) -> int:
    return _ev_y(i) + _EV_H // 2

# Central card: center it on the merge-bus midpoint so the incoming arrow
# is vertically centered on the feeder manifold, not just on the original card.
_BUS_MID_Y = (_ev_mid(0) + _ev_mid(3)) // 2

_CARD_H = 2_000_000
_CARD_Y = _BUS_MID_Y - _CARD_H // 2
_B1_H = 440_000                        # market-name band
_B2_H = 1_030_000                      # TAM | SAM paired band
_B3_H = _CARD_H - _B1_H - _B2_H        # 530_000  ASV-addressable band
_CARD_MID_Y = _BUS_MID_Y

# Addressability gate chips beneath the lowered central card.
# Tighten the gap so the chips still clear the commentary band.
_CHIP_ROW_Y = _CARD_Y + _CARD_H + 120_000
_CHIP_H = 500_000
_CHIP_W = 1_500_000
_OP_W   = 600_000

# Scope ledger: dimension | included | excluded. Built in the consolidated ledger
# idiom — a low-level table() with a dark BLUE_5 header (white caps), bold first
# column, cascading horizontal rules only, and light in-model / out-of-model cell
# tints on the two value columns (BLUE_1 included, GRAY_2 excluded). Cells render at
# 100% line spacing so heights match estimate_row_heights.
_COL_W = [1_150_000, 1_580_000, 1_752_362]   # sum 4_482_362
_LED_ROWS = [
    ["Dimension", "Included in model", "Excluded / not current model"],
    ["Geography", "U.S.; Europe", "Rest of world"],
    ["Metric", "TAM; ASV-addressable SAM", "Full SOM / capture model"],
    ["Time basis", "Current annualized view", "Multi-year forecast"],
    ["Use cases", "Vessel-hosted telemetry; range and event support",
     "Full MRIS replacement; SBX replacement; coercive enforcement"],
    ["Addressability test", "Vessel share and role share", "Generic penetration rate"],
]
# Light in/out tint per value column (col 1 included, col 2 excluded).
_LED_COL_FILL = {1: BLUE_1, 2: GRAY_2}
_LED_ROW_H = estimate_row_heights(_LED_ROWS, _COL_W, size_pt=8.0,
                                  header_size_pt=8.5, min_row_h=210_000)
_LED_CY = sum(_LED_ROW_H)

# Evidence cards: (cap, body, fill, fg).
_EVIDENCE = [
    ("CONTRACTS",
     "Awards, vendors, values, periods, vessels, TAM buckets", BLUE_1, BLACK),
    ("BUDGETS",
     "PE rows, FY27 PB, maritime shares, SBX and NAVAIR layers", BLUE_2, BLACK),
    ("EVENTS AND RATES",
     "Cadence, event cost, vessel / role shares, day rates", BLUE_3, WHITE),
    ("EUROPE ANCHORS",
     "Country / segment spend, floors, vessel / role shares", BLUE_4, WHITE),
]

_FINDINGS = [
    ("The boundary is intentionally narrow.",
     ["The model starts with sea-range telemetry and maritime range-support, not "
      "broader naval autonomy.",
      "It covers current annual TAM and ASV-addressable SAM for the U.S. and Europe."]),
    ("Addressability is role-specific.",
     ["SAM only counts work that is vessel-related and suitable for ASV execution.",
      "Monitoring, relay, sensing, and patrol-like support enter the filter; major "
      "platform replacement and enforcement do not."]),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _evidence_card(sp_id, i) -> str:
    cap, body, fill, fg = _EVIDENCE[i]
    return text_box(
        sp_id, "EvidenceCard", _LEFT_X, _ev_y(i), _LEFT_W, _EV_H,
        [paragraph([run(cap, size=DENSE_BODY_10PT, bold=True, color=fg, font=FONT)],
                   space_after=50, line_spacing=104_000),
         paragraph([run(body, size=FINEPRINT_8_5PT, color=fg, font=FONT)],
                   line_spacing=104_000)],
        fill=fill, anchor="ctr", insets=(90_000, 45_000, 90_000, 45_000))


def _gate_chip(sp_id, x, cap, sub, fill) -> str:
    return text_box(
        sp_id, "GateChip", x, _CHIP_ROW_Y, _CHIP_W, _CHIP_H,
        [paragraph([run(cap, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=50),
         paragraph([run(sub, size=_SZ_8, italic=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=fill, prst="roundRect", geom_adj={"adj": 14_000}, anchor="ctr",
        insets=(60_000, 40_000, 60_000, 40_000))


def _commentary(sp_id, x, w, finding, bullets) -> str:
    paras = [paragraph([run(finding, size=MESSAGE_11PT, bold=True, color=BLACK,
                            font=FONT)], space_after=90, line_spacing=108_000)]
    for j, b in enumerate(bullets):
        paras.append(paragraph([run(b, size=LABEL_9PT, color=BLACK, font=FONT)],
                               bullet=True, line_spacing=108_000,
                               space_after=(0 if j == len(bullets) - 1 else 100)))
    return text_box(sp_id, "Commentary", x, _COMM_Y, w, _COMM_H, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(110_000, 20_000, 90_000, 20_000))


def _tc(text, *, fill, bold, size, dark, borders):
    """One ledger cell at 100% line spacing so the rendered height matches
    estimate_row_heights (house_table's 115% cells render ~15% taller)."""
    color = WHITE if dark else BLACK
    return tcell_rich(
        [{"align": "l",
          "runs": [trun(text, size=size, bold=bold, color=color, font=FONT)],
          "line_spacing": 100_000}],
        fill=fill, anchor="ctr", borders=borders)


def _ledger(sp_id) -> str:
    """Native scope ledger: dark BLUE_5 header (white caps), 8pt body, bold first
    column, light in/out cell tints on the value columns, cascading horizontal
    rules only."""
    n = len(_LED_ROWS)
    rows = [trow([
        _tc(_LED_ROWS[0][c].upper(), fill=BLUE_5, bold=True, size=850, dark=True,
            borders={"B": {"color": BLACK, "width": 19_050}})
        for c in range(len(_COL_W))
    ], h=_LED_ROW_H[0])]
    for ri in range(1, n):
        bb = {"B": "none"} if ri == n - 1 else {"B": {"color": BLACK, "width": 12_700}}
        cells = [
            _tc(_LED_ROWS[ri][ci], fill=_LED_COL_FILL.get(ci), bold=(ci == 0),
                size=830, dark=False, borders=bb)
            for ci in range(len(_COL_W))
        ]
        rows.append(trow(cells, h=_LED_ROW_H[ri]))
    return table(sp_id, "ScopeLedger", _LED_X, _EXH_Y, sum(_COL_W), _LED_CY,
                 col_widths=_COL_W, rows=rows)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    # Qualifier (no-fill italic) + caveat chip on the top band.
    qualifier = text_box(
        10, "Qualifier", BODY_X, _QUAL_Y, 7_000_000, _QUAL_H,
        [paragraph([run(_QUALIFIER, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    caveat = text_box(
        11, "CaveatChip", _CAVEAT_X, _CAVEAT_Y, _CAVEAT_W, _CAVEAT_H,
        [paragraph([run(_CAVEAT, size=FINEPRINT_8_5PT, bold=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=GRAY_1, prst="roundRect", geom_adj={"adj": 20_000}, anchor="ctr",
        insets=(80_000, 30_000, 80_000, 30_000))

    # Merge bus: four feeders -> vertical bus -> one arrow into the central card.
    feeders = "".join(
        connector(30 + i, "Feeder", _LEFT_R, _ev_mid(i), _BUS_X - _LEFT_R, 0,
                  color=BLACK, width=12_700)
        for i in range(4))
    bus = connector(34, "MergeBus", _BUS_X, _ev_mid(0), 0, _ev_mid(3) - _ev_mid(0),
                    color=BLACK, width=12_700)
    merge_arrow = connector(35, "MergeArrow", _BUS_X, _CARD_MID_Y, _CEN_X - _BUS_X, 0,
                            color=BLACK, width=12_700, arrow=True)

    cards = "".join(_evidence_card(20 + i, i) for i in range(4))

    # Central model-boundary card: sharp background + 3 bands + 2 dividers.
    card_bg = text_box(40, "CentralCard", _CEN_X, _CARD_Y, _CEN_W, _CARD_H,
                       [paragraph([])], fill=BLUE_1, anchor="t")
    div1 = connector(41, "CardDiv1", _CEN_X + 60_000, _CARD_Y + _B1_H,
                     _CEN_W - 120_000, 0, color=BLACK, width=9_525)
    div2 = connector(42, "CardDiv2", _CEN_X + 60_000, _CARD_Y + _B1_H + _B2_H,
                     _CEN_W - 120_000, 0, color=BLACK, width=9_525)
    name_band = text_box(
        43, "MarketName", _CEN_X, _CARD_Y, _CEN_W, _B1_H,
        [paragraph([run("SEA-RANGE TELEMETRY / MARITIME RANGE-SUPPORT",
                        size=CAP_12PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=104_000)],
        fill=None, line_color=None, anchor="ctr", insets=(120_000, 20_000, 120_000, 20_000))
    half = _CEN_W // 2
    tam_cell = text_box(
        44, "TamCell", _CEN_X + 40_000, _CARD_Y + _B1_H, half - 60_000, _B2_H,
        [paragraph([run("TAM", size=BADGE_16PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=60),
         paragraph([run("Total annual spend pool", size=FINEPRINT_8_5PT, italic=True,
                        color=BLACK, font=FONT)], align="ctr", line_spacing=104_000)],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    sam_cell = text_box(
        45, "SamCell", _CEN_X + half + 20_000, _CARD_Y + _B1_H, half - 60_000, _B2_H,
        [paragraph([run("SAM", size=BADGE_16PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr", space_after=60),
         paragraph([run("ASV-relevant vessel / role use cases", size=FINEPRINT_8_5PT,
                        italic=True, color=BLACK, font=FONT)], align="ctr",
                   line_spacing=104_000)],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    asv_band = text_box(
        46, "AsvDefinition", _CEN_X, _CARD_Y + _B1_H + _B2_H, _CEN_W, _B3_H,
        [paragraph([run("ASV-addressable = vessel-related work with an ASV-suitable role",
                        size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=108_000)],
        fill=None, line_color=None, anchor="ctr", insets=(120_000, 20_000, 120_000, 20_000))
    central = card_bg + div1 + div2 + name_band + tam_cell + sam_cell + asv_band

    # Two-gate addressability chips (conceptual relationship, not a process arrow).
    gate_tie = connector(47, "GateTie", _CEN_X + _CEN_W // 2, _CARD_Y + _CARD_H,
                         0, _CHIP_ROW_Y - (_CARD_Y + _CARD_H), color=BLACK, width=12_700)
    vessel_chip = _gate_chip(50, _CEN_X, "VESSEL SHARE", "Vessel-related fraction", BLUE_1)
    operator = text_box(
        51, "GateOperator", _CEN_X + _CHIP_W, _CHIP_ROW_Y, _OP_W, _CHIP_H,
        [paragraph([run("AND", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    role_chip = _gate_chip(52, _CEN_X + _CHIP_W + _OP_W, "ROLE SHARE",
                           "ASV-suitable fraction", BLUE_2)
    chips = gate_tie + vessel_chip + operator + role_chip

    # Scope ledger: dark-header native table, light in/out cell tints, horizontal rules.
    ledger = _ledger(60)

    commentary = (_commentary(70, BODY_X, 5_500_000, *_FINDINGS[0])
                  + _commentary(71, BODY_X + 5_800_000, BODY_R - (BODY_X + 5_800_000),
                                *_FINDINGS[1]))

    # Paint order: connectors behind; cards/card/chips over their ends; ledger +
    # commentary independent; qualifier + caveat on the top band.
    return (feeders + bus + merge_arrow + cards + central + chips
            + ledger + qualifier + caveat + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
