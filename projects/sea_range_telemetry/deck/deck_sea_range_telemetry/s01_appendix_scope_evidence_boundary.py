"""s01_appendix_scope_evidence_boundary - set the modeling boundary before any TAM
or SAM math: what is being sized (sea-range telemetry / maritime range-support), what
evidence feeds it, and what makes work ASV-addressable (vessel share AND role share).

Shape-built boundary map (no chart). A central rounded model-boundary card defines the
sized object (market name, paired TAM / SAM definitions, the ASV-addressable definition);
four evidence-source cards stack on the left and merge into the card through a black bus +
arrow; two addressability gate chips (vessel share AND role share) sit beneath it. A
compact scope ledger (native table with thin included / excluded side bands) sits right.
Two no-fill commentary findings run along the bottom; a small gray caveat chip flags the
future-capture exclusion. No market-size values appear.

Spec: specs/sea_range_telemetry/s01_appendix_scope_evidence_boundary.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, house_table, connector,
)
from deck_core.text_metrics import estimate_row_heights
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4,
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
_TAKEAWAY = ("The model sizes annual maritime range-support spend before filtering "
             "to ASV-addressable roles.")
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

# Central card: three internal bands (market name / TAM-SAM / ASV-addressable).
_CARD_Y = _EXH_Y
_CARD_H = 2_000_000
_B1_H = 440_000                        # market-name band
_B2_H = 1_030_000                      # TAM | SAM paired band
_B3_H = _CARD_H - _B1_H - _B2_H        # 530_000  ASV-addressable band
_CARD_MID_Y = _CARD_Y + _CARD_H // 2

# Addressability gate chips beneath the central card.
_CHIP_ROW_Y = _CARD_Y + _CARD_H + 200_000
_CHIP_H = 520_000
_CHIP_W = 1_500_000
_OP_W   = 600_000

# Scope ledger: dimension | included | excluded. The semantic in-model / out-of-model
# orientation is carried by light full-cell tints on the two value columns (E2E9EF
# included, D9D9D9 excluded) rather than sub-0.1in ghost band columns, whose default
# 0.05in cell insets would exceed the column width and trip a PowerPoint repair.
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
_LED_ALIGNS = ["l", "l", "l"]
# Light semantic tints: E2E9EF on Included (in-model), D9D9D9 on Excluded (out-of-model).
_LED_FILLS = {}
for _r in range(1, len(_LED_ROWS)):
    _LED_FILLS[(_r, 1)] = BLUE_1
    _LED_FILLS[(_r, 2)] = GRAY_2
# 6 rows (header + 5). Floor each at 500_000 so the ledger bottom clears the
# commentary band even at house_table's ~115% render (use-cases row stays tallest).
_LED_ROW_H = estimate_row_heights(_LED_ROWS, _COL_W, size_pt=8.5, min_row_h=500_000)

# Evidence cards: (cap, body, fill, fg).
_EVIDENCE = [
    ("CONTRACTS",
     "PIID-level awards, vendors, values, periods, vessels, agencies, TAM buckets, "
     "source IDs", BLUE_1, BLACK),
    ("BUDGETS",
     "PE rows, FY27 PB, maritime shares, SBX decomposition, NAVAIR layer",
     BLUE_2, BLACK),
    ("EVENTS AND RATES",
     "Test cadence, per-event cost, vessel share, role share, overlap group, "
     "day rates", BLUE_3, WHITE),
    ("EUROPE ANCHORS",
     "Country / segment modeled spend, public-record floors, vessel share, "
     "role share, source IDs", BLUE_4, WHITE),
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
        fill=fill, anchor="ctr", insets=(60_000, 40_000, 60_000, 40_000))


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

    # Central model-boundary card: rounded background + 3 bands + 2 dividers.
    card_bg = text_box(40, "CentralCard", _CEN_X, _CARD_Y, _CEN_W, _CARD_H,
                       [paragraph([])], fill=BLUE_1, prst="roundRect",
                       geom_adj={"adj": 7_000}, anchor="t")
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

    # Scope ledger (native table, rule skin, thin included/excluded side bands).
    ledger = house_table(60, "ScopeLedger", _LED_X, _EXH_Y, _COL_W, _LED_ROWS,
                         row_h=_LED_ROW_H, table_skin="rule", aligns=_LED_ALIGNS,
                         size=850, cell_fills=_LED_FILLS)

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
