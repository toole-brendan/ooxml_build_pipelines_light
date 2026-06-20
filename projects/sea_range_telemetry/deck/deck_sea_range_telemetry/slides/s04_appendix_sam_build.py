"""s04_appendix_sam_build - explain how annual TAM value becomes ASV-addressable SAM:
a two-gate suitability filter (annual value x vessel share x role share), the same logic
across contract / event / Europe streams, a treatment crosswalk of what counts and why,
and a Pacific_MRIS overlap deduction applied to SAM only.

Decision-board layout (deliberately different from the TAM bridge): a left vertical
formula rail (four cards separated by operator chips) carries the core SAM calculation;
three stream-formula chips and a de-duplication sidecar sit in the middle; a native
treatment crosswalk (dark header, light per-row counted / discounted / excluded tint) sits right.
Two filled interpretation cards close the page. No SAM result values, no capture / SOM share.

Spec: specs/sea_range_telemetry/s04_appendix_sam_build.md.
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
    BLUE_1, BLUE_2, BLUE_3, BLUE_5,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    CAP_12PT, EXHIBIT_HEADER_13PT, BADGE_16PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Methodology"
_BREADCRUMB_TOPIC = "SAM Build"
_TOPIC            = "SAM Build"
_TAKEAWAY = ("ASV-addressable SAM is limited by vessel and role suitability, "
             "then de-duplicated on the SAM side.")
_SOURCES = ("Sources: (1) USAspending.gov / FPDS award records; (2) DOT&E FY2025 "
            "Annual Report, NAVAIR VX-30, NASA Wallops, Point Mugu Sea Range "
            "EIS / OEIS, and SEC EDGAR vessel-rate filings; (3) QinetiQ FY25 "
            "Annual Report, U.K. MOD LTPA / MSCA releases, DGA EM, CNES / CSG, "
            "FMV, Andøya Space, SaxaVord, and company analysis")

_QUALIFIER = "SAM method only; capture share and future upside are outside current sizing"

_SZ_85 = 850    # 8.5pt: rail sublines, sidecar formulas, commentary support
_SZ_83 = 830    # 8.3pt: stream-formula text
_SZ_8  = 800    # 8pt:   crosswalk body


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_QUAL_Y, _QUAL_H = BODY_Y, 220_000
_MAIN_Y = BODY_Y + 290_000                        # 1_661_600
_COMM_H = 620_000
_COMM_Y = BODY_B - _COMM_H                         # 5_250_000
_MAIN_H = _COMM_Y - _MAIN_Y - 90_000              # 3_438_400

# Three column bands: formula rail | stream chips + sidecar | treatment crosswalk.
_RAIL_X, _RAIL_W = BODY_X, 2_750_000
_RAIL_R = _RAIL_X + _RAIL_W                        # 3_203_079
_MID_X, _MID_W = 3_503_079, 2_650_000
_MID_R = _MID_X + _MID_W                           # 6_153_079
_TBL_X = 6_453_079
_TBL_W = BODY_R - _TBL_X                            # 5_282_362

# Formula-rail card / operator stack heights.
_C1_H, _OP_H, _C2_H, _C3_H = 820_000, 240_000, 480_000, 480_000
_C4_H = _MAIN_H - (_C1_H + 3 * _OP_H + _C2_H + _C3_H)   # 938_400
_RAIL_Y = [
    _MAIN_Y,                                                       # card1
    _MAIN_Y + _C1_H,                                               # op1
    _MAIN_Y + _C1_H + _OP_H,                                       # card2
    _MAIN_Y + _C1_H + _OP_H + _C2_H,                              # op2
    _MAIN_Y + _C1_H + _OP_H + _C2_H + _OP_H,                      # card3
    _MAIN_Y + _C1_H + _OP_H + _C2_H + _OP_H + _C3_H,              # op3
    _MAIN_Y + _C1_H + _OP_H + _C2_H + _OP_H + _C3_H + _OP_H,      # card4
]
_C4_Y = _RAIL_Y[6]
_C4_MID = _C4_Y + _C4_H // 2

# Stream chips (top of the middle band) and the overlap sidecar (below).
# _STREAM_H nudged up from 1_430_000 so the three chips still clear their formulas
# once the cap takes 240_000 off the top (Event SAM is the longest, wraps to 3 lines).
_STREAM_H = 1_575_000
_STREAM_CAP_H = 240_000
_STREAM_GAP = 65_000

_SIDE_Y = _MAIN_Y + _STREAM_H + 120_000
_SIDE_H = _MAIN_H - _STREAM_H - 120_000
_SIDECAR_CAP_H = 210_000
_SIDE_BAND_H = (_SIDE_H - _SIDECAR_CAP_H) // 3
_SIDE_MID = _SIDE_Y + _SIDE_H // 2
_SIDE_US_SAM_MID = _SIDE_Y + _SIDECAR_CAP_H + _SIDE_BAND_H // 2

# Treatment crosswalk (native table). Activity | treatment | why. Built in the
# consolidated crosswalk idiom — a low-level table() with a dark BLUE_5 header
# (white caps), cascading horizontal rules only, and the classification color carried
# as a light per-row tint on the bold, centered Treatment cell (counted BLUE_1,
# discounted GRAY_1, excluded GRAY_2). Activity / Why stay white for readability.
# Cells render at 100% line spacing so heights match estimate_row_heights.
_COL_W = [1_950_000, 1_110_000, 2_222_362]   # sum 5_282_362
_TBL_ROWS = [
    ["Activity / role", "Current SAM treatment", "Why"],
    ["Vessel-hosted telemetry / comms relay", "Counted",
     "Surface vessel can host or relay instrumentation payloads"],
    ["Splash, debris, impact monitoring", "Counted",
     "Observation and local sensing can be positioned near event areas"],
    ["Environmental sensing", "Counted",
     "Persistent metocean and local sensing are ASV-suitable"],
    ["Range clearance / hazard patrol", "Discounted",
     "Monitoring role is suitable; authority and enforcement do not transfer"],
    ["Full MRIS replacement", "Excluded",
     "Current SAM does not assume replacement of major crewed range ships"],
    ["SBX replacement", "Excluded",
     "Current SAM does not assume replacement of SBX platform"],
    ["Flight termination authority", "Excluded",
     "Safety authority is not treated as ASV-addressable"],
    ["Coercive enforcement / boarding", "Excluded",
     "Enforcement and boarding are not assumed ASV roles"],
]
_TBL_ALIGNS = ["l", "ctr", "l"]
# Per-row tint on the Treatment cell: counted BLUE_1, discounted GRAY_1, excluded GRAY_2.
_TREATMENT_FILL = {1: BLUE_1, 2: BLUE_1, 3: BLUE_1, 4: GRAY_1,
                   5: GRAY_2, 6: GRAY_2, 7: GRAY_2, 8: GRAY_2}
_TBL_ROW_H = estimate_row_heights(_TBL_ROWS, _COL_W, size_pt=8.0,
                                  header_size_pt=8.5, min_row_h=240_000)
_TBL_CY = sum(_TBL_ROW_H)


# ── Local helpers ────────────────────────────────────────────────────────────
def _rail_card(sp_id, idx, fill, fg, cap, cap_size, sublines) -> str:
    y, h = _RAIL_Y[idx], (_C1_H, None, _C2_H, None, _C3_H, None, _C4_H)[idx]
    paras = [paragraph([run(cap, size=cap_size, bold=True, color=fg, font=FONT)],
                       align="ctr", space_after=(120 if sublines else 0),
                       line_spacing=104_000)]
    for s in sublines:
        paras.append(paragraph([run(s, size=_SZ_85, italic=True, color=fg, font=FONT)],
                               align="ctr", line_spacing=106_000))
    return text_box(sp_id, "RailCard", _RAIL_X, y, _RAIL_W, h, paras,
                    fill=fill, anchor="ctr",
                    line_width=(19_050 if idx == 6 else 12_700),
                    insets=(100_000, 40_000, 100_000, 40_000))


def _operator(sp_id, idx, sym) -> str:
    return text_box(
        sp_id, "RailOperator", _RAIL_X, _RAIL_Y[idx], _RAIL_W, _OP_H,
        [paragraph([run(sym, size=BADGE_16PT, bold=True, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)


def _stream_cap() -> str:
    return text_box(
        29, "StreamCap", _MID_X, _MAIN_Y, _MID_W, _STREAM_CAP_H,
        [paragraph([run("SAME FILTER BY STREAM",
                        size=DENSE_BODY_10PT, bold=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_5,
        anchor="ctr",
        insets=(80_000, 20_000, 80_000, 20_000),
    )


def _stream_chip(sp_id, j, label, formula) -> str:
    ch_h = (_STREAM_H - _STREAM_CAP_H - 3 * _STREAM_GAP) // 3
    y = _MAIN_Y + _STREAM_CAP_H + _STREAM_GAP + j * (ch_h + _STREAM_GAP)
    return text_box(
        sp_id, "StreamChip", _MID_X, y, _MID_W, ch_h,
        [paragraph([run(label, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   space_after=30, line_spacing=100_000),
         paragraph([run(formula, size=_SZ_83, color=BLACK, font=FONT)],
                   line_spacing=102_000)],
        fill=GRAY_1, anchor="ctr", insets=(70_000, 20_000, 70_000, 20_000))


def _sidecar() -> str:
    cap_h = _SIDECAR_CAP_H
    bg = text_box(40, "OverlapSidecar", _MID_X, _SIDE_Y, _MID_W, _SIDE_H,
                  [paragraph([])], fill=GRAY_1, anchor="t")
    cap = text_box(
        41, "OverlapCap", _MID_X, _SIDE_Y, _MID_W, cap_h,
        [paragraph([run("DE-DUPLICATION RULE", size=DENSE_BODY_10PT, bold=True,
                        color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, anchor="ctr", insets=(80_000, 20_000, 80_000, 20_000))
    body_y = _SIDE_Y + cap_h
    band_h = (_SIDE_H - cap_h) // 3
    bands = [
        ("U.S. SAM", "= contract SAM + event SAM − Pacific MRIS overlap"),
        ("Overlap amount", "= 10% × Pacific_MRIS-tagged event SAM"),
        ("Applied to SAM, not TAM", "Double-count risk is between SAM-side pools"),
    ]
    parts = []
    for j, (label, formula) in enumerate(bands):
        by = body_y + j * band_h
        parts.append(text_box(
            42 + j, "OverlapBand", _MID_X, by, _MID_W, band_h,
            [paragraph([run(label, size=FINEPRINT_8_5PT, bold=True, color=BLACK,
                            font=FONT)], space_after=30, line_spacing=102_000),
             paragraph([run(formula, size=_SZ_83, color=BLACK, font=FONT)],
                       line_spacing=104_000)],
            fill=None, line_color=None, anchor="ctr",
            insets=(90_000, 16_000, 90_000, 16_000)))
        if j > 0:
            parts.append(connector(45 + j, "OverlapDivider", _MID_X + 80_000, by,
                                   _MID_W - 160_000, 0, color=BLACK, width=9_525))
    return bg + cap + "".join(parts)


def _interpretation_card(sp_id, x, w, fill, finding, support) -> str:
    return text_box(
        sp_id, "InterpretationCard", x, _COMM_Y, w, _COMM_H,
        [paragraph([run(finding, size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
                   space_after=60, line_spacing=106_000),
         paragraph([run(support, size=LABEL_9PT, color=BLACK, font=FONT)],
                   line_spacing=108_000)],
        fill=fill, anchor="ctr", insets=(140_000, 50_000, 140_000, 50_000))


def _tc(text, *, fill, bold, align, size, dark, borders):
    """One crosswalk cell at 100% line spacing so the rendered height matches
    estimate_row_heights (house_table's 115% cells render ~15% taller)."""
    color = WHITE if dark else BLACK
    return tcell_rich(
        [{"align": align,
          "runs": [trun(text, size=size, bold=bold, color=color, font=FONT)],
          "line_spacing": 100_000}],
        fill=fill, anchor="ctr", borders=borders)


def _treatment_crosswalk(sp_id) -> str:
    """Native treatment crosswalk: dark BLUE_5 header (white caps), 8pt body, a bold
    centered Treatment column carrying the per-row classification tint, Activity / Why
    on white, cascading horizontal rules only."""
    n = len(_TBL_ROWS)
    rows = [trow([
        _tc(_TBL_ROWS[0][c].upper(), fill=BLUE_5, bold=True, align=_TBL_ALIGNS[c],
            size=850, dark=True, borders={"B": {"color": BLACK, "width": 19_050}})
        for c in range(len(_COL_W))
    ], h=_TBL_ROW_H[0])]
    for ri in range(1, n):
        bb = {"B": "none"} if ri == n - 1 else {"B": {"color": BLACK, "width": 12_700}}
        cells = [
            _tc(_TBL_ROWS[ri][ci],
                fill=(_TREATMENT_FILL.get(ri) if ci == 1 else None),
                bold=(ci == 1), align=_TBL_ALIGNS[ci], size=800, dark=False, borders=bb)
            for ci in range(len(_COL_W))
        ]
        rows.append(trow(cells, h=_TBL_ROW_H[ri]))
    return table(sp_id, "TreatmentCrosswalk", _TBL_X, _MAIN_Y, sum(_COL_W), _TBL_CY,
                 col_widths=_COL_W, rows=rows)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    qualifier = text_box(
        10, "Qualifier", BODY_X, _QUAL_Y, BODY_R - BODY_X, _QUAL_H,
        [paragraph([run(_QUALIFIER, size=FINEPRINT_8_5PT, italic=True, color=BLACK,
                        font=FONT)])],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)

    # Left formula rail: four cards separated by operator chips.
    rail = (
        _rail_card(20, 0, BLUE_1, BLACK, "ANNUAL VALUE", CAP_12PT,
                   ["Contract annual TAM", "Event annual value", "Europe modeled spend"])
        + _operator(21, 1, "×")
        + _rail_card(22, 2, BLUE_2, BLACK, "VESSEL SHARE", CAP_12PT,
                     ["Vessel-related fraction"])
        + _operator(23, 3, "×")
        + _rail_card(24, 4, BLUE_3, WHITE, "ROLE SHARE", CAP_12PT,
                     ["ASV-suitable fraction"])
        + _operator(25, 5, "=")
        + _rail_card(26, 6, BLUE_5, WHITE, "ASV-ADDRESSABLE SAM", EXHIBIT_HEADER_13PT,
                     ["Current addressable annual value"]))

    # Stream-formula chips (same addressability logic across three streams), under a
    # cap that names the shared filter.
    streams = (
        _stream_cap()
        + _stream_chip(30, 0, "Contract SAM",
                       "= annual TAM × vessel share × role share")
        + _stream_chip(31, 1, "Event SAM",
                       "= events × per-event cost × vessel share × role share")
        + _stream_chip(32, 2, "Europe SAM",
                       "= modeled spend × vessel share × role share"))

    sidecar = _sidecar()
    # Elbow tie from the ASV-addressable SAM output card to the sidecar's U.S. SAM
    # de-duplication band (SAM-side overlap), arrow at the sidecar. (ids 80-82; the
    # sidecar itself uses 40-47.)
    _TIE_X = (_RAIL_R + _MID_X) // 2
    side_tie = (
        connector(80, "SamToSidecarH1",
                  _RAIL_R, _C4_MID,
                  _TIE_X - _RAIL_R, 0,
                  color=BLACK, width=12_700)
        + connector(81, "SamToSidecarV",
                    _TIE_X, _C4_MID,
                    0, _SIDE_US_SAM_MID - _C4_MID,
                    color=BLACK, width=12_700)
        + connector(82, "SamToSidecarH2",
                    _TIE_X, _SIDE_US_SAM_MID,
                    _MID_X - _TIE_X, 0,
                    color=BLACK, width=12_700, arrow=True)
    )

    table_xml = _treatment_crosswalk(50)

    commentary = (
        _interpretation_card(60, BODY_X, 5_500_000, BLUE_1,
                             "SAM is a suitability filter, not a penetration rate.",
                             "Rows must pass both gates: vessel-related work and "
                             "ASV-suitable role.")
        + _interpretation_card(61, BODY_X + 5_800_000, BODY_R - (BODY_X + 5_800_000),
                               GRAY_1,
                               "The treatment logic is conservative by design.",
                               "Sensing, relay, monitoring, and patrol-like support "
                               "count; platform replacement, safety authority, and "
                               "enforcement do not."))

    # Paint order: sidecar tie behind the cards; the rest over.
    return (side_tie + rail + streams + sidecar
            + table_xml
            + qualifier + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
