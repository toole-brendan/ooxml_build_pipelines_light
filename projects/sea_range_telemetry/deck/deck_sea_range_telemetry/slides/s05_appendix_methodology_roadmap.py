"""s05_appendix_methodology_roadmap - orient the reader before the detailed evidence,
TAM, and SAM method pages: the workbook sizes a narrow current annual U.S. + Europe
sea-range telemetry / maritime range-support TAM first, then filters that pool into
ASV-addressable SAM. It does not size SOM, future capture, full MRIS / SBX replacement,
or coercive enforcement.

Shape-built roadmap plus scope gate (no chart, no native table). A full-width output
chip sits under the caption; a six-node left-to-right roadmap (Scope gate -> Source data
-> Assumptions -> TAM Build -> SAM Build -> Outputs / checks) carries two chapter labels
and a dashed TAM-ends / SAM-starts seam between the build steps. A two-column scope-gate
ledger (included vs excluded) sits lower-left, three reader-key definition chips lower-
right, and a dark guardrail strip runs along the bottom.

Spec: specs/alternative_v1/01_methodology_roadmap.md.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1, GRAY_4,
    WHITE, BLACK, FONT,
    INSETS_NONE,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Methodology Roadmap"
_TOPIC            = "Methodology Roadmap"
_TAKEAWAY = ("TAM defines the current annual pool; SAM filters it for "
             "ASV-addressable roles.")
_SOURCES = ("Sources: (1) Methodology & Scope tab; (2) Assumptions, TAM Build, "
            "SAM Build, Segmentation, Checks, and z_ChartData tabs; (3) sea-range "
            "telemetry methodology framework")

_CAPTION = ("Current annualized FY27-style view; USD $M per year. Geography is "
            "U.S. + Europe. TAM and ASV-addressable SAM are modeled; SOM and "
            "future capture are not.")
_STEP = "STEP 1 / 4 — SCOPE + FLOW"
_OUTPUT = ("The model defines scope, separates evidence from judgment, builds TAM, "
           "then filters TAM into ASV-addressable SAM.")
_GUARDRAIL_LEAD = "Guardrails: "
_GUARDRAIL = ("contract awards and budgets size / anchor the market; ASV factors only "
              "filter addressability. The model does not include SOM, win probability, "
              "pricing, generic autonomy penetration, full crewed-vessel replacement, "
              "SBX replacement, or coercive safety authority.")

# Raw sizes (style.py permits raw sizes with a nearby comment).
_SZ_NODE_HDR = 850   # 8.5pt roadmap node header
_SZ_NODE_BODY = 780  # 7.8pt roadmap node body
_SZ_CHAPTER = 900    # 9pt chapter label, bold caps (10pt wraps the right label in render)
_SZ_CHIP_HDR = 900   # 9pt reader-key chip header / output chip
_SZ_CHIP_BODY = 850  # 8.5pt chip body / caption
_SZ_FORMULA = 800    # 8pt chip formula line
_SZ_SCOPE = 820      # 8.2pt scope-gate item
_SZ_SCOPE_CAP = 830  # 8.3pt scope-gate column caption
_SZ_GUARD = 950      # 9.5pt guardrail strip
_SZ_SEAM = 780       # 7.8pt seam note

# ── Vertical band geometry (all EMU) ─────────────────────────────────────────
_CAP_Y, _CAP_H   = BODY_Y, 190_000                          # caption + step marker
_CHIP_Y, _CHIP_H = BODY_Y + 210_000, 290_000               # output chip
_CHAP_Y, _CHAP_H = _CHIP_Y + _CHIP_H + 50_000, 190_000     # chapter labels
_NODE_Y, _NODE_H = _CHAP_Y + _CHAP_H + 30_000, 680_000     # roadmap nodes
_NODE_MID        = _NODE_Y + _NODE_H // 2
_SEAM_Y, _SEAM_H = _NODE_Y + _NODE_H + 10_000, 140_000     # seam note band

_GUARD_H = 520_000
_GUARD_Y = BODY_B - _GUARD_H                                # 5_350_000
_LOWER_Y = _SEAM_Y + _SEAM_H + 70_000                      # scope gate + reader key
_LOWER_B = _GUARD_Y - 80_000

# ── Roadmap horizontal geometry ──────────────────────────────────────────────
_NGAP = 270_000
_NODE_W = (BODY_CX - 5 * _NGAP) // 6                        # 1_655_393
_PITCH = _NODE_W + _NGAP                                    # 1_925_393

def _node_x(i: int) -> int:
    return BODY_X + i * _PITCH

# Chapter labels: left over nodes 1-4 (Scope gate -> TAM Build), right over 5-6.
_CHAP_L_X = _node_x(0)
_CHAP_L_W = _node_x(3) + _NODE_W - _CHAP_L_X
_CHAP_R_X = _node_x(4)
_CHAP_R_W = _node_x(5) + _NODE_W - _CHAP_R_X

# Dashed TAM/SAM seam sits in the gap between node 4 (TAM Build) and node 5 (SAM Build).
_SEAM_X = _node_x(3) + _NODE_W + _NGAP // 2

# ── Step-marker / caption top band ───────────────────────────────────────────
_STEP_W = 2_200_000
_STEP_X = BODY_R - _STEP_W
_CAP_W = _STEP_X - 60_000 - BODY_X

# ── Lower band columns ───────────────────────────────────────────────────────
_SCOPE_X = BODY_X
_SCOPE_W = 6_300_000
_SCOPE_HDR_H = 260_000
_SCOPE_BODY_Y = _LOWER_Y + _SCOPE_HDR_H
_SCOPE_BODY_H = _LOWER_B - _SCOPE_BODY_Y
_SCOPE_COL_W = _SCOPE_W // 2

_RK_X = BODY_X + 6_480_000
_RK_W = BODY_R - _RK_X

# ── Content ──────────────────────────────────────────────────────────────────
# (header, body, fill, fg)
_NODES = [
    ("1 | Scope gate",
     "U.S. + Europe; current annual sea-range telemetry / maritime range support",
     BLUE_1, BLACK),
    ("2 | Source data",
     "Contracts, budgets, events / rates, Europe anchors", GRAY_1, BLACK),
    ("3 | Assumptions",
     "Editable low / base / high inputs; NAVAIR shown as calculated", BLUE_1, BLACK),
    ("4 | TAM BUILD",
     "Annual market size before ASV scoring", BLUE_5, WHITE),
    ("5 | SAM Build",
     "Annual value × vessel share × role share", BLUE_2, BLACK),
    ("6 | Outputs + checks",
     "Executive Summary, Segmentation, z_ChartData, 31 checks", GRAY_1, BLACK),
]

_INCLUDED = [
    "U.S. + Europe", "USD $M / year", "Current annualized FY27-style view",
    "Vessel-hosted telemetry", "Range / event support", "Maritime instrumentation",
    "Vessel share × role share addressability",
]
_EXCLUDED = [
    "Rest of world", "SOM / capture model", "Multi-year revenue forecast",
    "Full MRIS or SBX replacement", "Flight termination authority",
    "Coercive enforcement / boarding", "Generic ASV penetration rate",
]

# (header, body, formula, fill)
_READER_KEYS = [
    ("TAM",
     "Total annual spend pool for sea-range telemetry / maritime range-support.",
     "U.S. TAM + Europe TAM = Total TAM", BLUE_1),
    ("ASV-addressable SAM",
     "Portion of TAM tied to vessel-related work and ASV-suitable roles.",
     "annual value × vessel share × role share", GRAY_1),
    ("Low / base / high",
     "Base case is shown centrally; SAM base is the midpoint of modeled low and "
     "high SAM cases.",
     None, BLUE_1),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _node(sp_id, i) -> str:
    hdr, body, fill, fg = _NODES[i]
    return text_box(
        sp_id, "RoadNode", _node_x(i), _NODE_Y, _NODE_W, _NODE_H,
        [paragraph([run(hdr, size=_SZ_NODE_HDR, bold=True, color=fg, font=FONT)],
                   space_after=40, line_spacing=104_000),
         paragraph([run(body, size=_SZ_NODE_BODY, color=fg, font=FONT)],
                   line_spacing=104_000)],
        fill=fill, anchor="t", insets=(78_000, 60_000, 78_000, 50_000))


def _chapter(sp_id, x, w, text) -> str:
    return text_box(
        sp_id, "ChapterLabel", x, _CHAP_Y, w, _CHAP_H,
        [paragraph([run(text, size=_SZ_CHAPTER, bold=True, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=102_000)],
        fill=BLUE_4, anchor="ctr", insets=(60_000, 20_000, 60_000, 20_000))


def _scope_col(sp_id, x, caption, items, fill) -> str:
    paras = [paragraph([run(caption, size=_SZ_SCOPE_CAP, bold=True, color=BLACK,
                            font=FONT)], space_after=90, line_spacing=104_000)]
    for j, it in enumerate(items):
        paras.append(paragraph([run(it, size=_SZ_SCOPE, color=BLACK, font=FONT)],
                               bullet=True, line_spacing=104_000,
                               space_after=(0 if j == len(items) - 1 else 50)))
    return text_box(sp_id, "ScopeColumn", x, _SCOPE_BODY_Y, _SCOPE_COL_W,
                    _SCOPE_BODY_H, paras, fill=fill, anchor="t",
                    insets=(95_000, 60_000, 70_000, 45_000))


def _reader_chip(sp_id, y, h, header, body, formula, fill) -> str:
    paras = [paragraph([run(header, size=_SZ_CHIP_HDR, bold=True, color=BLACK,
                            font=FONT)], space_after=55, line_spacing=104_000),
             paragraph([run(body, size=_SZ_CHIP_BODY, color=BLACK, font=FONT)],
                       space_after=(55 if formula else 0), line_spacing=104_000)]
    if formula:
        paras.append(paragraph([run(formula, size=_SZ_FORMULA, italic=True,
                                    color=BLACK, font=FONT)], line_spacing=104_000))
    return text_box(sp_id, "ReaderKeyChip", _RK_X, y, _RK_W, h, paras, fill=fill,
                    anchor="ctr", insets=(120_000, 45_000, 120_000, 45_000))


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

    chapters = (_chapter(13, _CHAP_L_X, _CHAP_L_W,
                         "TAM CHAPTER — DEFINE AND SIZE THE ANNUAL MARKET")
                + _chapter(14, _CHAP_R_X, _CHAP_R_W,
                           "SAM CHAPTER — FILTER THE SAME POOL FOR ASV ROLES"))

    # Chain connectors behind the nodes: solid arrows within each chapter, a dashed
    # TAM/SAM seam in the central gap. Drawn before the nodes so node fills cover the
    # connector tails and only the arrowheads read in the gaps.
    arrows = []
    for i in (0, 1, 2, 4):
        x0 = _node_x(i) + _NODE_W
        arrows.append(connector(20 + i, "ChainArrow", x0, _NODE_MID, _NGAP, 0,
                                color=BLACK, width=12_700, arrow=True))
    seam = connector(25, "TamSamSeam", _SEAM_X, _NODE_Y, 0, _NODE_H,
                     color=GRAY_4, width=9_525, dashed=True)
    seam_note = text_box(
        26, "SeamNote", _SEAM_X - 950_000, _SEAM_Y, 1_900_000, _SEAM_H,
        [paragraph([run("TAM ends here; SAM starts here.", size=_SZ_SEAM,
                        italic=True, color=GRAY_4, font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)
    nodes = "".join(_node(30 + i, i) for i in range(6))

    # Scope gate: dark header + two filled columns (included / excluded).
    scope_hdr = text_box(
        40, "ScopeHeader", _SCOPE_X, _LOWER_Y, _SCOPE_W, _SCOPE_HDR_H,
        [paragraph([run("SCOPE GATE — CURRENT MODEL BOUNDARY", size=_SZ_CHIP_HDR,
                        bold=True, color=WHITE, font=FONT)], align="ctr")],
        fill=BLUE_5, anchor="ctr", insets=(120_000, 20_000, 120_000, 20_000))
    scope_cols = (_scope_col(41, _SCOPE_X, "INCLUDED IN MODEL", _INCLUDED, BLUE_1)
                  + _scope_col(42, _SCOPE_X + _SCOPE_COL_W,
                               "EXCLUDED / NOT CURRENT MODEL", _EXCLUDED, GRAY_1))

    # Reader-key definition chips (alternating fill).
    rk_gap = 70_000
    rk_h = (_LOWER_B - _LOWER_Y - 2 * rk_gap) // 3
    chips = "".join(
        _reader_chip(50 + j, _LOWER_Y + j * (rk_h + rk_gap), rk_h, *_READER_KEYS[j])
        for j in range(3))

    guardrail = text_box(
        60, "Guardrail", BODY_X, _GUARD_Y, BODY_CX, _GUARD_H,
        [paragraph([run(_GUARDRAIL_LEAD, size=_SZ_GUARD, bold=True, color=WHITE,
                        font=FONT),
                    run(_GUARDRAIL, size=_SZ_GUARD, color=WHITE, font=FONT)],
                   line_spacing=106_000)],
        fill=BLUE_5, anchor="ctr", insets=(160_000, 40_000, 160_000, 40_000))

    # Paint order: connectors behind nodes; everything else independent.
    return ("".join(arrows) + seam + nodes + caption + step + output + chapters
            + seam_note + scope_hdr + scope_cols + chips + guardrail)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
