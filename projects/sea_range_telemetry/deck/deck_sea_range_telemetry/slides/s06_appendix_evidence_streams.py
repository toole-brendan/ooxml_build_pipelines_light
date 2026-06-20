"""s06_appendix_evidence_streams - show how the evidence base enters the workbook and
why the four evidence streams are not interchangeable: contracts, budgets, events / rates,
and Europe anchors each feed a different part of the model, and raw evidence, assumptions,
calculations, provenance, and checks stay separated so the workbook is auditable.

One native table (the four-stream evidence ledger) carries the primary evidence; everything
else is shape-built. A seven-node workbook-flow spine runs full width under the output chip
(source tabs -> assumptions -> engines -> outputs / checks); a right-side model-control rail
stacks five evidence / judgment separation cards beside the table; a bottom example strip
gives one concrete calculation per stream.

Spec: specs/alternative_v1/02_evidence_streams.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.text_metrics import estimate_row_heights
from deck_sea_range_telemetry.slides._house import dark_table
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1,
    WHITE, BLACK, FONT,
    INSETS_NONE,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Evidence Streams"
_TOPIC            = "Evidence Streams"
_TAKEAWAY = ("Four source types feed distinct workbook engines rather than one "
             "summed evidence pool.")
_SOURCES = ("Sources: (1) Data Contracts, Data Budget, Data Events, Data Europe "
            "tabs; (2) Assumptions and Sources & Glossary tabs; (3) TAM Build, "
            "SAM Build, Checks, and z_ChartData tabs")

_CAPTION = ("Source records live in Data tabs; editable judgment lives in "
            "Assumptions; source IDs and support mapping live in Sources & Glossary; "
            "checks tie outputs back to the model.")
_STEP = "STEP 2 / 4 — EVIDENCE + CONTROL"
_OUTPUT = ("Contracts, budgets, events and rates, and Europe anchors each anchor a "
           "different model calculation and validation path.")
_NOTE = "Editable scenario knobs stay separate from raw evidence."

# Raw sizes (style.py permits raw sizes with a nearby comment).
_SZ_SPINE = 800      # 8pt spine node
_SZ_CHIP_HDR = 900   # 9pt output chip / table label / rail header
_SZ_CHIP_BODY = 850  # 8.5pt caption / step marker
_SZ_CARD_LEAD = 850  # 8.5pt control-card lead
_SZ_CARD_BODY = 820  # 8.2pt control-card body
_SZ_TBL = 800        # 8pt table body
_SZ_MC_TAG = 750     # 7.5pt mini-card stream tag
_SZ_MC_TITLE = 870   # 8.7pt mini-card title
_SZ_MC_FORMULA = 770 # 7.7pt mini-card formula
_SZ_NOTE = 800       # 8pt assumptions note

# ── Vertical band geometry (all EMU) ─────────────────────────────────────────
_CAP_Y, _CAP_H   = BODY_Y, 180_000
_CHIP_Y, _CHIP_H = BODY_Y + 200_000, 280_000
_SPINE_Y, _SPINE_H = _CHIP_Y + _CHIP_H + 40_000, 540_000
_SPINE_MID       = _SPINE_Y + _SPINE_H // 2
_NOTE_Y, _NOTE_H = _SPINE_Y + _SPINE_H + 5_000, 130_000

_STRIP_H = 900_000
_STRIP_Y = BODY_B - _STRIP_H
_MAIN_Y  = _NOTE_Y + _NOTE_H + 50_000
_MAIN_B  = _STRIP_Y - 80_000

# ── Spine horizontal geometry (7 nodes) ──────────────────────────────────────
_SGAP = 240_000
_SNODE_W = (BODY_CX - 6 * _SGAP) // 7                       # 1_406_051
_SPITCH = _SNODE_W + _SGAP

def _snode_x(i: int) -> int:
    return BODY_X + i * _SPITCH

# ── Main zone columns: native table (left) + control rail (right) ────────────
_TBL_X = BODY_X
_TBL_W = 7_050_000
_RAIL_X = BODY_X + 7_200_000
_RAIL_W = BODY_R - _RAIL_X
_TBL_LABEL_H = 200_000
_TBL_TOP = _MAIN_Y + _TBL_LABEL_H

# ── Step marker / caption band ───────────────────────────────────────────────
_STEP_W = 2_350_000
_STEP_X = BODY_R - _STEP_W
_CAP_W = _STEP_X - 60_000 - BODY_X

# ── Content ──────────────────────────────────────────────────────────────────
# Spine: (label, fill, fg).
_SPINE = [
    ("Data Contracts", GRAY_1, BLACK),
    ("Data Budget", GRAY_1, BLACK),
    ("Data Events", GRAY_1, BLACK),
    ("Data Europe", GRAY_1, BLACK),
    ("Assumptions", BLUE_1, BLACK),
    ("TAM Build / SAM Build", BLUE_5, WHITE),
    ("Executive Summary / Segmentation / Checks / z_ChartData", BLUE_2, BLACK),
]

_TBL_COL_W = [1_339_500, 1_692_000, 2_185_500, 1_833_000]   # 19/24/31/26% of 7_050_000
_TBL_ROWS = [
    ["EVIDENCE STREAM", "PRIMARY WORKBOOK TABS", "WHAT IT ANCHORS",
     "EXAMPLE EVIDENCE / FIELDS"],
    ["Contracts", "Data Contracts; TAM Build; SAM Build",
     "Awarded / obligated activity; recognized contract TAM; contract-anchored SAM",
     "PIID, vendor, reported value, PoP, TAM factors, ASV factors"],
    ["Budgets", "Data Budget; TAM Build; Assumptions",
     "PE maritime slices; NAVAIR layer; SBX / MDA / Pacific Collector cross-checks",
     "FY27 PB, maritime share, PE code, NAVAIR sub-rows"],
    ["Events & rates", "Data Events; SAM Build; Segmentation",
     "Test cadence; event-derived SAM; Pacific_MRIS overlap eligibility; "
     "charter-rate economics",
     "annual events, per-event cost, day rates, overlap group"],
    ["Europe anchors", "Data Europe; TAM Build; SAM Build; Segmentation",
     "Europe TAM; Europe SAM; country / segment cuts",
     "modeled spend, public-record floor, vessel share, role share"],
]
_TBL_ROW_H = estimate_row_heights(_TBL_ROWS, _TBL_COL_W, size_pt=8.0,
                                  header_size_pt=8.5, min_row_h=250_000)
# Per spec row fills: contracts white, budgets GRAY_1, events white, europe BLUE_1.
_TBL_CELL_FILLS = {}
for _c in range(4):
    _TBL_CELL_FILLS[(2, _c)] = GRAY_1
    _TBL_CELL_FILLS[(4, _c)] = BLUE_1

# Control rail cards: (lead, body, fill).
_CARDS = [
    ("Raw evidence", "Data tabs carry source records and source IDs.", GRAY_1),
    ("Editable judgment",
     "Assumptions carries low / base / high knobs and basis summaries.", BLUE_1),
    ("Calculation engines", "TAM Build and SAM Build perform the math.", GRAY_1),
    ("Provenance",
     "Sources & Glossary resolves source IDs and assumption support.", BLUE_1),
    ("Output integrity",
     "Checks and z_ChartData tie model values to presentation ranges.", GRAY_1),
]

# Example mini-cards: (stream, title, formula).
_MINI = [
    ("CONTRACTS", "Recognized TAM",
     "reported value × relevance × maritime × instrumentation"),
    ("BUDGETS", "PE maritime slice", "FY27 PB × maritime instrumentation share"),
    ("EVENTS", "Event annual value", "annual cadence × per-event maritime support cost"),
    ("EUROPE", "Country / segment anchor",
     "modeled annual spend × vessel share × role share"),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _spine_node(sp_id, i) -> str:
    label, fill, fg = _SPINE[i]
    return text_box(
        sp_id, "SpineNode", _snode_x(i), _SPINE_Y, _SNODE_W, _SPINE_H,
        [paragraph([run(label, size=_SZ_SPINE, bold=True, color=fg, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=fill, anchor="ctr", insets=(55_000, 30_000, 55_000, 30_000))


def _control_card(sp_id, y, h, lead, body, fill) -> str:
    return text_box(
        sp_id, "ControlCard", _RAIL_X, y, _RAIL_W, h,
        [paragraph([run(lead, size=_SZ_CARD_LEAD, bold=True, color=BLACK, font=FONT)],
                   space_after=45, line_spacing=102_000),
         paragraph([run(body, size=_SZ_CARD_BODY, color=BLACK, font=FONT)],
                   line_spacing=102_000)],
        fill=fill, anchor="ctr", insets=(110_000, 35_000, 110_000, 35_000))


def _mini_card(sp_id, x, y, w, h, stream, title, formula) -> str:
    return text_box(
        sp_id, "ExampleMiniCard", x, y, w, h,
        [paragraph([run(stream, size=_SZ_MC_TAG, bold=True, color=BLUE_4, font=FONT)],
                   space_after=40, line_spacing=100_000),
         paragraph([run(title, size=_SZ_MC_TITLE, bold=True, color=BLACK, font=FONT)],
                   space_after=45, line_spacing=100_000),
         paragraph([run(formula, size=_SZ_MC_FORMULA, color=BLACK, font=FONT)],
                   line_spacing=100_000)],
        fill=WHITE, anchor="t", insets=(95_000, 50_000, 80_000, 40_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, _CAP_W, _CAP_H,
        [paragraph([run(_CAPTION, size=_SZ_CHIP_BODY, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    step = text_box(
        11, "StepMarker", _STEP_X, _CAP_Y, _STEP_W, _CAP_H,
        [paragraph([run(_STEP, size=_SZ_CHIP_BODY, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_1, anchor="ctr", insets=(60_000, 20_000, 60_000, 20_000))
    output = text_box(
        12, "OutputChip", BODY_X, _CHIP_Y, BODY_CX, _CHIP_H,
        [paragraph([run(_OUTPUT, size=_SZ_CHIP_HDR, bold=True, color=BLACK, font=FONT)],
                   align="ctr", line_spacing=106_000)],
        fill=BLUE_1, anchor="ctr", insets=(150_000, 30_000, 150_000, 30_000))

    # Workbook-flow spine: 7 nodes with right-arrow connectors in the gaps.
    arrows = "".join(
        connector(20 + i, "SpineArrow", _snode_x(i) + _SNODE_W, _SPINE_MID, _SGAP, 0,
                  color=BLACK, width=9_525, arrow=True)
        for i in range(6))
    nodes = "".join(_spine_node(30 + i, i) for i in range(7))
    note = text_box(
        37, "AssumptionsNote", _snode_x(4) - 250_000, _NOTE_Y, _SNODE_W + 500_000,
        _NOTE_H,
        [paragraph([run(_NOTE, size=_SZ_NOTE, italic=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # Evidence-stream ledger (the one native table on this slide).
    tbl_label = text_box(
        40, "LedgerLabel", _TBL_X, _MAIN_Y, _TBL_W, _TBL_LABEL_H,
        [paragraph([run("Evidence stream ledger — what each stream anchors",
                        size=_SZ_CHIP_HDR + 100, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    ledger = dark_table(41, "EvidenceLedger", _TBL_X, _TBL_TOP, _TBL_COL_W,
                        _TBL_ROWS, _TBL_ROW_H, aligns=["l", "l", "l", "l"],
                        size=_SZ_TBL, header_size=850, cell_fills=_TBL_CELL_FILLS)

    # Model-control rail: dark header + five separation cards.
    rail_hdr = text_box(
        50, "RailHeader", _RAIL_X, _MAIN_Y, _RAIL_W, 300_000,
        [paragraph([run("MODEL CONTROL — EVIDENCE AND JUDGMENT STAY SEPARATE",
                        size=_SZ_CHIP_HDR, bold=True, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=BLUE_5, anchor="ctr", insets=(90_000, 20_000, 90_000, 20_000))
    card_top = _MAIN_Y + 300_000 + 50_000
    card_gap = 45_000
    card_h = (_MAIN_B - card_top - 4 * card_gap) // 5
    cards = "".join(
        _control_card(51 + j, card_top + j * (card_h + card_gap), card_h, *_CARDS[j])
        for j in range(5))

    # Example strip: gray panel, title, four white mini-cards.
    strip_bg = text_box(60, "ExampleStrip", BODY_X, _STRIP_Y, BODY_CX, _STRIP_H,
                        [paragraph([])], fill=GRAY_1, anchor="t")
    strip_title = text_box(
        61, "ExampleStripTitle", BODY_X, _STRIP_Y, BODY_CX, 200_000,
        [paragraph([run("Examples — each source stream becomes a different "
                        "calculation input", size=_SZ_CHIP_HDR, bold=True,
                        color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=(150_000, 30_000, 150_000, 20_000))
    pad = 150_000
    mgap = 120_000
    mc_w = (BODY_CX - 2 * pad - 3 * mgap) // 4
    mc_y = _STRIP_Y + 220_000
    mc_h = _STRIP_H - 220_000 - 110_000
    minis = "".join(
        _mini_card(62 + k, BODY_X + pad + k * (mc_w + mgap), mc_y, mc_w, mc_h, *_MINI[k])
        for k in range(4))

    # Paint order: spine arrows behind nodes; strip background behind its cards.
    return (arrows + nodes + caption + step + output + note
            + tbl_label + ledger + rail_hdr + cards
            + strip_bg + strip_title + minis)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
