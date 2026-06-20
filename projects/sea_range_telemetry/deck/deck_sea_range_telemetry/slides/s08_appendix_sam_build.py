"""s08_appendix_sam_build - explain how the model filters annual TAM-related value into
current ASV-addressable SAM and validates it. SAM is not a penetration-rate haircut: each
relevant contract, event, and Europe row passes a vessel-share gate and an ASV-role-suitable
role-share gate, then the U.S. rollup subtracts a targeted Pacific MRIS overlap amount. The
workbook currently passes 31 validation checks.

One native table (the SAM output bridge) carries the rollup; everything else is shape-built.
A full-width two-gate filter shows annual value -> vessel share -> role share -> SAM; three
stream cards give the contract, event, and Europe formula variants; a role-treatment chip row
shows counted / discounted / excluded roles; a six-card audit rail sits beside the bridge; a
dark diligence band keeps the limitations visible.

Spec: specs/alternative_v1/04_sam_build.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.text_metrics import estimate_row_heights, line_height_emu, wrapped_line_count
from deck_sea_range_telemetry.slides._house import dark_table
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_5,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "SAM Build and Validation"
_TOPIC            = "SAM Build"
_TAKEAWAY = ("Vessel and role gates narrow TAM into current ASV-addressable value.")
_SOURCES = ("Sources: (1) SAM Build contract, event, and Europe rollups; (2) Data "
            "Contracts ASV factors; (3) Data Events event cadence, per-event cost, "
            "and overlap group; (4) Data Europe vessel / role shares; (5) Checks tab")

_CAPTION = ("SAM is current ASV-addressable annual value, not expected revenue. It is "
            "scored row by row using vessel-related share and ASV-role-suitable share.")
_STEP = "STEP 4 / 4 — SAM + CHECKS"
_OUTPUT = ("Current ASV-addressable SAM is $118.69M base, 7.44% of TAM: U.S. $90.08M "
           "and Europe $28.61M.")
_FORMULA = "ASV-addressable SAM = annual value × vessel share × role share"
_ROLE_LEAD = ("Role suitability is conservative — count support roles, discount "
              "authority roles, exclude replacement assumptions")
_DILIGENCE_LEAD = "Visible limitations: "
_DILIGENCE = ("Europe modeled gap, commercial / institutional launch TAM, Pacific MRIS "
              "overlap, event cadence refresh, and ASV role suitability remain diligence "
              "items. Current SAM is not a revenue forecast and does not assume full "
              "crewed-vessel replacement.")

# Raw sizes (style.py permits raw sizes with a nearby comment).
_SZ_CHIP_HDR = 900    # 9pt output chip / bridge label
_SZ_CHIP_BODY = 850   # 8.5pt caption / step marker
_SZ_GATE_HDR = 800    # 8pt gate-node header
_SZ_GATE_BODY = 750   # 7.5pt gate-node body
_SZ_FORMULA = 950     # 9.5pt two-gate formula line
_SZ_LANE_HDR = 900    # 9pt stream-card header strip (caps)
_SZ_LANE_FORM = 800   # 8pt stream-card formula (one line)
_SZ_LANE_SUB = 780    # 7.8pt stream-card subline (one line)
_SZ_ROLE_LEAD = 850   # 8.5pt role-treatment lead
_SZ_ROLE_LBL = 780    # 7.8pt role chip label
_SZ_ROLE_BODY = 780   # 7.8pt role chip body
_SZ_TBL = 800         # 8pt table body
_SZ_TBL_HDR = 830     # 8.3pt table header
_SZ_VR_HDR = 900      # 9pt validation-rail header
_SZ_VR_LEAD = 780     # 7.8pt validation-card lead
_SZ_VR_BODY = 780     # 7.8pt validation-card body
_SZ_DILIGENCE = 920   # 9.2pt diligence band

# ── Vertical band geometry (all EMU) ─────────────────────────────────────────
_CAP_Y, _CAP_H   = BODY_Y, 150_000
_CHIP_Y, _CHIP_H = BODY_Y + 170_000, 225_000               # ends 1_766_600
_GATE_Y, _GATE_H = _CHIP_Y + _CHIP_H + 25_000, 420_000     # two-gate filter
_GATE_MID        = _GATE_Y + _GATE_H // 2
_FORMULA_Y, _FORMULA_H = _GATE_Y + _GATE_H + 5_000, 100_000
_LANE_Y, _LANE_H = _FORMULA_Y + _FORMULA_H + 25_000, 420_000   # stream cards
_ROLE_Y, _ROLE_H = _LANE_Y + _LANE_H + 25_000, 455_000        # role-treatment chips

_DIL_H = 400_000
_DIL_Y = BODY_B - _DIL_H                                    # 5_470_000
_BR_Y = _ROLE_Y + _ROLE_H + 40_000                         # bridge zone
_BR_B = _DIL_Y - 60_000

# ── Two-gate filter geometry (4 nodes) ───────────────────────────────────────
_GGAP = 300_000
_GNODE_W = (BODY_CX - 3 * _GGAP) // 4                       # 2_595_590
_GPITCH = _GNODE_W + _GGAP

def _gnode_x(i: int) -> int:
    return BODY_X + i * _GPITCH

# ── Stream-lane geometry (3 cards) ───────────────────────────────────────────
_LGAP = 200_000
_LANE_W = (BODY_CX - 2 * _LGAP) // 3                        # 3_627_454
_LANE_HDR_H = 100_000

def _lane_x(i: int) -> int:
    return BODY_X + i * (_LANE_W + _LGAP)

# ── Role-chip geometry (3 chips) ─────────────────────────────────────────────
_RGAP = 200_000
_ROLE_LEAD_H = 130_000
_ROLE_CHIP_W = (BODY_CX - 2 * _RGAP) // 3
_ROLE_CHIP_Y = _ROLE_Y + _ROLE_LEAD_H + 15_000
_ROLE_CHIP_H = _ROLE_Y + _ROLE_H - _ROLE_CHIP_Y

def _role_x(i: int) -> int:
    return BODY_X + i * (_ROLE_CHIP_W + _RGAP)

# ── Bridge zone: native table (left) + validation rail (right) ───────────────
_BT_X = BODY_X
_BT_W = 7_400_000
_VR_X = BODY_X + 7_500_000
_VR_W = BODY_R - _VR_X
_BT_LABEL_H = 165_000
_BT_TOP = _BR_Y + _BT_LABEL_H
_VR_HDR_H = 250_000

# ── Step marker / caption band ───────────────────────────────────────────────
_STEP_W = 2_200_000
_STEP_X = BODY_R - _STEP_W
_CAP_W = _STEP_X - 60_000 - BODY_X

# ── Content ──────────────────────────────────────────────────────────────────
# Two-gate nodes: (header, body, fill, fg).
_GATE_NODES = [
    ("Annual value",
     "contract annual TAM, event annual value, or Europe modeled spend",
     GRAY_1, BLACK),
    ("Gate 1 — vessel share",
     "portion tied to surface-vessel or vessel-enabled work", BLUE_1, BLACK),
    ("Gate 2 — role share",
     "portion suitable for current ASV execution or support", BLUE_2, BLACK),
    ("ASV-addressable SAM",
     "counted annual value after both gates", BLUE_5, WHITE),
]

# Stream cards: (header, formula, subline). Sublines kept to one rendered line.
_STREAMS = [
    ("CONTRACT-ANCHORED SAM", "Annual contract TAM × vessel share × role share",
     "Annualized contract TAM with ASV factors by PIID."),
    ("EVENT-DERIVED SAM",
     "Annual events × per-event cost × vessel share × role share",
     "Range-support package cost, not weapon or launch cost."),
    ("EUROPE SAM", "Modeled annual spend × vessel share × role share",
     "No U.S. event overlay; no Pacific MRIS correction."),
]

# Role-treatment chips: (label, body, fill).
_ROLE_CHIPS = [
    ("Counted",
     "local_surface_surveillance, modular_payload_hosting, telemetry / relay, "
     "splash / debris monitoring", BLUE_2),
    ("Discounted",
     "range clearance support, blocking / hailing awareness, authority-adjacent "
     "support", BLUE_1),
    ("Excluded",
     "full MRIS replacement, SBX replacement, flight termination authority, "
     "coercive enforcement, boarding", GRAY_1),
]

_BT_COL_W = [2_200_000, 850_000, 900_000, 850_000, 2_600_000]   # sum 7_400_000
_BT_ROWS = [
    ["COMPONENT", "LOW ($M / YR)", "BASE ($M / YR)", "HIGH ($M / YR)", "TREATMENT"],
    ["Contract-anchored subtotal", "$6.43M", "$39.88M", "$73.34M",
     "Annual contract TAM × vessel × role"],
    ["Event-derived subtotal", "$10.63M", "$53.14M", "$95.65M",
     "Events × per-event cost × vessel × role"],
    ["Gross U.S. SAM", "$17.05M", "$93.02M", "$168.99M",
     "Contract + event before overlap"],
    ["Pacific MRIS overlap amount", "($0.67M)", "($2.94M)", "($5.21M)",
     "10% × Pacific_MRIS-tagged event SAM"],
    ["U.S. SAM", "$16.38M", "$90.08M", "$163.78M", "Gross - overlap"],
    ["Europe SAM", "$5.88M", "$28.61M", "$51.33M",
     "Europe modeled spend × vessel × role"],
    ["Total SAM", "$22.26M", "$118.69M", "$215.11M", "U.S. + Europe"],
]
_BT_ALIGNS = ["l", "r", "r", "r", "l"]
_BT_ROW_H = estimate_row_heights(_BT_ROWS, _BT_COL_W, size_pt=8.0,
                                 header_size_pt=8.3, min_row_h=239_000)
# Shade Gross combined (3) BLUE_1, Pacific overlap (4) GRAY_1, Total SAM (7) GRAY_2.
# Bold value columns on every row; total row bold across all cells.
_BT_CELL_FILLS, _BT_CELL_BOLD = {}, {}
for _c in range(5):
    _BT_CELL_FILLS[(3, _c)] = BLUE_1
    _BT_CELL_FILLS[(4, _c)] = GRAY_1
    _BT_CELL_FILLS[(7, _c)] = GRAY_2
    _BT_CELL_BOLD[(7, _c)] = True
for _r in range(1, 8):
    for _c in (1, 2, 3):
        _BT_CELL_BOLD[(_r, _c)] = True

# Validation rail cards: (lead, body, fill).
_VCARDS = [
    ("Scenario integrity", "U.S. and Europe SAM base lie between low and high.", BLUE_1),
    ("Formula tie-outs",
     "U.S. TAM = defense + commercial; U.S. SAM = gross - overlap.", GRAY_1),
    ("Factor integrity", "TAM factors remain inside [0, 1].", GRAY_1),
    ("Double-count guards",
     "LRHW separate row is zero; SLCM-N cadence is zero-current.", BLUE_1),
    ("Provenance",
     "Data and assumption source IDs resolve in Sources & Glossary.", GRAY_1),
    ("Output integrity",
     "Executive Summary, Segmentation, and z_ChartData tie to TAM / SAM engines.",
     BLUE_2),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _gate_node(sp_id, i) -> str:
    hdr, body, fill, fg = _GATE_NODES[i]
    return text_box(
        sp_id, "GateNode", _gnode_x(i), _GATE_Y, _GNODE_W, _GATE_H,
        [paragraph([run(hdr, size=_SZ_GATE_HDR, bold=True, color=fg, font=FONT)],
                   align="ctr", space_after=40, line_spacing=102_000),
         paragraph([run(body, size=_SZ_GATE_BODY, color=fg, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=fill, anchor="ctr", insets=(70_000, 35_000, 70_000, 35_000))


def _stream_card(sp_id, i) -> str:
    header, formula, subline = _STREAMS[i]
    x = _lane_x(i)
    bg = text_box(sp_id, "StreamCard", x, _LANE_Y, _LANE_W, _LANE_H,
                  [paragraph([])], fill=WHITE, anchor="t")
    hdr = text_box(
        sp_id + 1, "StreamHeader", x, _LANE_Y, _LANE_W, _LANE_HDR_H,
        [paragraph([run(header, size=_SZ_LANE_HDR, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_5, anchor="ctr", insets=(60_000, 12_000, 60_000, 12_000))
    body = text_box(
        sp_id + 2, "StreamBody", x, _LANE_Y + _LANE_HDR_H, _LANE_W,
        _LANE_H - _LANE_HDR_H,
        [paragraph([run(formula, size=_SZ_LANE_FORM, bold=True, color=BLACK,
                        font=FONT)], space_after=70, line_spacing=104_000),
         paragraph([run(subline, size=_SZ_LANE_SUB, italic=True, color=BLACK,
                        font=FONT)], line_spacing=104_000)],
        fill=None, line_color=None, anchor="ctr", insets=(90_000, 30_000, 80_000, 30_000))
    return bg + hdr + body


def _role_chip(sp_id, i) -> str:
    label, body, fill = _ROLE_CHIPS[i]
    # Inline bold label + body in one paragraph so each chip stays to two lines.
    return text_box(
        sp_id, "RoleChip", _role_x(i), _ROLE_CHIP_Y, _ROLE_CHIP_W, _ROLE_CHIP_H,
        [paragraph([run(label.upper() + ": ", size=_SZ_ROLE_LBL, bold=True,
                        color=BLACK, font=FONT),
                    run(body, size=_SZ_ROLE_BODY, color=BLACK, font=FONT)],
                   line_spacing=104_000)],
        fill=fill, anchor="ctr", insets=(95_000, 35_000, 90_000, 35_000))


def _vcard(sp_id, y, h, lead, body, fill) -> str:
    return text_box(
        sp_id, "AuditCard", _VR_X, y, _VR_W, h,
        [paragraph([run(lead + " — ", size=_SZ_VR_LEAD, bold=True, color=BLACK,
                        font=FONT),
                    run(body, size=_SZ_VR_BODY, color=BLACK, font=FONT)],
                   line_spacing=102_000)],
        fill=fill, anchor="ctr", insets=(100_000, 30_000, 90_000, 30_000))


def _vcard_height(lead, body) -> int:
    # Estimate at size_pt=8.8 (not the 7.8pt render size) so the line count tracks
    # soffice's wider Arial; height is pinned to the 7.8pt render pitch + insets.
    usable = _VR_W - 180_000
    lines = wrapped_line_count(f"{lead} - {body}", usable, size_pt=8.8)
    return max(180_000, lines * line_height_emu(7.8) + 60_000)


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
        fill=BLUE_1, anchor="ctr", insets=(60_000, 18_000, 60_000, 18_000))
    output = text_box(
        12, "OutputChip", BODY_X, _CHIP_Y, BODY_CX, _CHIP_H,
        [paragraph([run(_OUTPUT, size=_SZ_CHIP_HDR, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_1, anchor="ctr", insets=(150_000, 25_000, 150_000, 25_000))

    # Two-gate filter: 4 nodes + right-arrow connectors behind them.
    arrows = "".join(
        connector(24 + i, "GateArrow", _gnode_x(i) + _GNODE_W, _GATE_MID, _GGAP, 0,
                  color=BLACK, width=12_700, arrow=True)
        for i in range(3))
    nodes = "".join(_gate_node(20 + i, i) for i in range(4))
    formula = text_box(
        27, "GateFormula", BODY_X, _FORMULA_Y, BODY_CX, _FORMULA_H,
        [paragraph([run(_FORMULA, size=_SZ_FORMULA, bold=True, italic=True,
                        color=BLACK, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)

    streams = "".join(_stream_card(30 + 10 * i, i) for i in range(3))

    role_lead = text_box(
        40, "RoleLead", BODY_X, _ROLE_Y, BODY_CX, _ROLE_LEAD_H,
        [paragraph([run(_ROLE_LEAD, size=_SZ_ROLE_LEAD, bold=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)
    role_chips = "".join(_role_chip(41 + i, i) for i in range(3))

    # SAM output bridge table (the one native table on this slide).
    bt_label = text_box(
        50, "SamBridgeLabel", _BT_X, _BR_Y, _BT_W, _BT_LABEL_H,
        [paragraph([run("SAM bridge — contract, event, overlap, and geography rollup",
                        size=_SZ_CHIP_HDR + 100, bold=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    table = dark_table(51, "SamBridge", _BT_X, _BT_TOP, _BT_COL_W, _BT_ROWS,
                       _BT_ROW_H, aligns=_BT_ALIGNS, size=_SZ_TBL,
                       header_size=_SZ_TBL_HDR, cell_fills=_BT_CELL_FILLS,
                       cell_bold=_BT_CELL_BOLD)

    # Validation rail: dark header + six content-fit audit cards (alternating fill).
    vr_hdr = text_box(
        60, "AuditHeader", _VR_X, _BR_Y, _VR_W, _VR_HDR_H,
        [paragraph([run("AUDIT CONTROLS — 31 CHECKS PASS", size=_SZ_VR_HDR, bold=True,
                        color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, anchor="ctr", insets=(90_000, 18_000, 90_000, 18_000))
    vr_top = _BR_Y + _VR_HDR_H + 25_000
    vr_gap = 16_000
    heights = [_vcard_height(lead, body) for lead, body, _ in _VCARDS]
    cards = []
    y = vr_top
    for j, (lead, body, fill) in enumerate(_VCARDS):
        cards.append(_vcard(61 + j, y, heights[j], lead, body, fill))
        y += heights[j] + vr_gap

    diligence = text_box(
        70, "Diligence", BODY_X, _DIL_Y, BODY_CX, _DIL_H,
        [paragraph([run(_DILIGENCE_LEAD, size=_SZ_DILIGENCE, bold=True, color=WHITE,
                        font=FONT),
                    run(_DILIGENCE, size=_SZ_DILIGENCE, color=WHITE, font=FONT)],
                   line_spacing=104_000)],
        fill=BLUE_5, anchor="ctr", insets=(160_000, 35_000, 160_000, 35_000))

    # Paint order: gate arrows behind nodes; stream backgrounds behind their headers.
    return (arrows + nodes + caption + step + output + formula + streams
            + role_lead + role_chips + bt_label + table + vr_hdr + "".join(cards)
            + diligence)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
