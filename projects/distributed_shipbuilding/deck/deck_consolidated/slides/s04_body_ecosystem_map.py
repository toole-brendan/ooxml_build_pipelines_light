"""s04_body_ecosystem_map - locate the supplier opportunity in the flow from Navy
new-construction funding through prime/team-build yards to purchased component work,
as two parallel program lanes (DDG left, submarine right) fused into one counted
supplier layer.

Shape-built system map (no chart). Each lane reads top to bottom: Navy funding
node, prime/team-build nodes, counted in-scope supplier node; black solid arrows
carry the funding-to-prime-to-supplier flow and both in-scope nodes feed one
BLUE_4 unifying supplier-layer chip. Gray exclusion/context tags sit below the
counted lanes (dashed context connectors), with a definition-guardrail line and a
legend beneath. A two-finding commentary rail runs down the right; the top thesis
strip carries the point (no separate focal callout).

Spec: ds_specs/s04_body_ecosystem_map.txt (SLIDE 04 - ECOSYSTEM MAP).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B, BODY_CX,
    BLUE_1, BLUE_2, BLUE_4,
    GRAY_1, GRAY_2,
    WHITE, BLACK, FONT,
    INSETS_NONE,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
    EXHIBIT_HEADER_13PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Market Definition"
_BREADCRUMB_TOPIC = "Supplier Layer"
_TOPIC            = "Supplier Layer"
_TAKEAWAY = ("The opportunity sits between Navy budget authority and prime-yard "
             "construction, in component work yards buy out rather than self-perform.")
_SOURCES = ("Sources: (1) Navy SCN shipbuilding budget justification and line-item "
            "structure, FY2022–FY2027; (2) prime-yard place-of-performance award "
            "corpus; (3) FFATA/FSRS first-tier subaward records")

_THESIS = ("Supplier-addressable component work sits inside Navy new-construction "
           "funding, not total ship cost.")
_GUARD_LEAD = "Electrical and power"
_GUARD_BODY = (" means ship power, distribution, and generation; combat and mission "
               "electronics leave the boundary before bucket assignment.")
_LEGEND = ("Blue = counted supplier layer; gray = excluded or context only; "
           "outline = prime or team-build layer.")
_CHIP_TITLE = "Distributed supplier work"
_CHIP_BODY = ("Structural/pre-outfit, machining, castings/forgings, "
              "piping/valves/pumps, electrical/power, HVAC, coatings/insulation")

_EVID_95 = 950    # 9.5pt commentary evidence
_NODE_LNSPC = 104_000


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_TH_Y, _TH_H = BODY_Y, 340_000                       # thesis strip (top)
_MZ_Y = _TH_Y + _TH_H + 50_000                       # main zone top

# Left zone = two lanes + fused chip; right zone = commentary rail.
_LZ_W = 7_300_000
_LANE_GUT = 280_000
_LANE_W = (_LZ_W - _LANE_GUT) // 2
_DDG_LX = BODY_X
_SUB_LX = BODY_X + _LANE_W + _LANE_GUT

_RZ_X = BODY_X + _LZ_W + 360_000
_RZ_W = BODY_R - _RZ_X

# Lane rows (top to bottom): header, funding, prime row, in-scope. The first
# two connector bands are intentionally a bit taller than the original so the
# split/merge arrow levels read more clearly at presentation scale. Below the
# counted in-scope node each lane's exclusion/context tag branches to the OUTER
# side via a catty-cornered dashed connector; the fused chip, guardrail line,
# and legend then stack full-width below.
_H_Y,    _H_H    = _MZ_Y, 240_000
_FUND_Y, _FUND_H = _H_Y + _H_H + 70_000, 360_000
_FUND_TO_PRIME_GAP = 200_000   # was 90k; lengthen the first arrow level
_PRIME_TO_INS_GAP  = 200_000   # was 90k; lengthen the second arrow level
_PRIME_Y, _PRIME_H = _FUND_Y + _FUND_H + _FUND_TO_PRIME_GAP, 380_000
_INS_Y,  _INS_H  = _PRIME_Y + _PRIME_H + _PRIME_TO_INS_GAP, 440_000
_EXC_Y,  _EXC_H  = _INS_Y + _INS_H + 180_000, 600_000
_EX_W = (_LANE_W - 520_000) // 2          # narrow, outer-offset exclusion tag
_CHIP_Y, _CHIP_H = _EXC_Y + _EXC_H + 120_000, 540_000
_GUARD_Y, _GUARD_H = _CHIP_Y + _CHIP_H + 40_000, 330_000
_LEG_Y,  _LEG_H  = _GUARD_Y + _GUARD_H + 30_000, 240_000

# Prime row = two nodes side by side within a lane.
_PW_GAP = 60_000
_PW = (_LANE_W - _PW_GAP) // 2

# Commentary rail spans from the main-zone top to the fused-chip bottom.
_COMM_Y = _MZ_Y
_COMM_H = (_CHIP_Y + _CHIP_H) - _MZ_Y

# Lane geometry helpers.
def _prime_x(lane_x: int) -> list[int]:
    return [lane_x, lane_x + _PW + _PW_GAP]

def _lane_c(lane_x: int) -> int:
    return lane_x + _LANE_W // 2

def _prime_c(lane_x: int) -> list[int]:
    return [x + _PW // 2 for x in _prime_x(lane_x)]

def _exclusion_x(i: int, lane_x: int) -> int:
    # DDG (i=0) branches to the lane's left/outer edge; submarine to the right.
    if i == 0:
        return lane_x + 80_000
    return lane_x + _LANE_W - _EX_W - 80_000


# ── Content ──────────────────────────────────────────────────────────────────
# (lane_x, header, funding_title, funding_sub, [(prime_title, prime_tag), ...],
#  inscope_title, inscope_tag, exclusion_text)
_LANES = [
    (_DDG_LX, "DDG",
     "Navy SCN funding", "Line item 2122",
     [("GD Bath Iron Works", "[prime yard]"), ("HII Ingalls", "[prime yard]")],
     "Yard-side non-GFE component suppliers", "[in scope]",
     "GFE; weapons and sensors; sustainment/depot; FFATA-visible evidence floor"),
    (_SUB_LX, "SUBMARINE",
     "Navy SCN funding", "Virginia and Columbia",
     [("GDEB", "[prime construction]"), ("HII Newport News", "[team-build context]")],
     "Non-nuclear supplier component layer", "[in scope]",
     "GFE/GFP; nuclear reactor plant; SIB capacity funding; depot/sustainment"),
]

_FINDINGS = [
    ("The primes differ, but the serviceable cut is the same.",
     "DDG dollars run through Bath Iron Works and Ingalls; submarine dollars run "
     "through Electric Boat and Newport News. In both lanes, the counted layer is "
     "supplier component work outside GFE, sustainment, and yard self-perform."),
    ("Visible subawards prove the layer, not its full size.",
     "FFATA-visible filings provide supplier names and work-type cues; first-tier "
     "visibility thins below the first tier and differs by yard."),
]


# ── Local helpers ────────────────────────────────────────────────────────────
def _node(sp_id, name, x, y, w, h, title, sub, *, fill, fg, line_color, line_width,
          title_size=LABEL_9PT, sub_size=FINEPRINT_8_5PT, sub_italic=False,
          insets=(90_000, 40_000, 90_000, 40_000)):
    paras = [paragraph([run(title, size=title_size, bold=True, color=fg, font=FONT)],
                       align="ctr", space_after=50, line_spacing=_NODE_LNSPC)]
    if sub:
        paras.append(paragraph(
            [run(sub, size=sub_size, italic=sub_italic, color=fg, font=FONT)],
            align="ctr", line_spacing=_NODE_LNSPC))
    return text_box(sp_id, name, x, y, w, h, paras, fill=fill, line_color=line_color,
                    line_width=line_width, anchor="ctr", insets=insets)


def _lane_header(sp_id, lane_x, text) -> str:
    header = text_box(
        sp_id, "LaneHeader", lane_x, _H_Y, _LANE_W, _H_H,
        [paragraph([run(text, size=EXHIBIT_HEADER_13PT, bold=True, color=BLACK,
                        font=FONT)], align="ctr")],
        fill=None, line_color=None, anchor="b", insets=INSETS_NONE)
    rule = connector(sp_id + 1, "LaneRule", lane_x, _H_Y + _H_H, _LANE_W, 0,
                     color=BLACK, width=9_525)
    return header + rule


def _flow(base, lane_x, ex_cx) -> str:
    """Solid black 1pt funding-to-prime-to-supplier flow into the fused chip, plus
    a catty-cornered dashed context connector that branches sideways from the
    in-scope node out and down into the outer-offset exclusion tag, so it never
    crosses the counted flow or the guardrail text."""
    lc = _lane_c(lane_x)
    pc = _prime_c(lane_x)
    parts = []
    # Funding -> prime row (split).
    y_split = _FUND_Y + _FUND_H + (_PRIME_Y - (_FUND_Y + _FUND_H)) // 2
    parts += [
        connector(base + 0, "FundDrop", lc, _FUND_Y + _FUND_H, 0,
                  y_split - (_FUND_Y + _FUND_H), color=BLACK, width=12_700),
        connector(base + 1, "FundSplit", pc[0], y_split, pc[1] - pc[0], 0,
                  color=BLACK, width=12_700),
        connector(base + 2, "ToPrimeL", pc[0], y_split, 0, _PRIME_Y - y_split,
                  color=BLACK, width=12_700, arrow=True),
        connector(base + 3, "ToPrimeR", pc[1], y_split, 0, _PRIME_Y - y_split,
                  color=BLACK, width=12_700, arrow=True),
    ]
    # Prime row -> in-scope node (merge).
    y_merge = _PRIME_Y + _PRIME_H + (_INS_Y - (_PRIME_Y + _PRIME_H)) // 2
    parts += [
        connector(base + 4, "PrimeLDrop", pc[0], _PRIME_Y + _PRIME_H, 0,
                  y_merge - (_PRIME_Y + _PRIME_H), color=BLACK, width=12_700),
        connector(base + 5, "PrimeRDrop", pc[1], _PRIME_Y + _PRIME_H, 0,
                  y_merge - (_PRIME_Y + _PRIME_H), color=BLACK, width=12_700),
        connector(base + 6, "PrimeMerge", pc[0], y_merge, pc[1] - pc[0], 0,
                  color=BLACK, width=12_700),
        connector(base + 7, "ToInScope", lc, y_merge, 0, _INS_Y - y_merge,
                  color=BLACK, width=12_700, arrow=True),
    ]
    # In-scope node -> fused chip (counted flow runs straight down the centre,
    # past the offset exclusion tag).
    parts.append(connector(base + 8, "ToChip", lc, _INS_Y + _INS_H, 0,
                           _CHIP_Y - (_INS_Y + _INS_H), color=BLACK, width=12_700,
                           arrow=True))
    # Catty-cornered dashed context tie: branch out from the centre, then drop
    # into the outer-offset exclusion tag (context, not counted -> no arrowhead).
    y_branch = _INS_Y + _INS_H + 70_000
    parts.append(connector(base + 9, "ContextElbow", lc, y_branch, ex_cx - lc, 0,
                           color=BLACK, width=9_525, dashed=True))
    parts.append(connector(base + 10, "ContextDrop", ex_cx, y_branch, 0,
                           _EXC_Y - y_branch, color=BLACK, width=9_525,
                           dashed=True))
    return "".join(parts)


def _commentary(sp_id) -> str:
    paras = []
    for i, (finding, evidence) in enumerate(_FINDINGS):
        last = i == len(_FINDINGS) - 1
        paras.append(paragraph(
            [run(finding, size=MESSAGE_11PT, bold=True, color=BLACK, font=FONT)],
            space_after=90))
        paras.append(paragraph(
            [run(evidence, size=_EVID_95, color=BLACK, font=FONT)],
            bullet=True, space_after=(0 if last else 240)))
    return text_box(sp_id, "Commentary", _RZ_X, _COMM_Y, _RZ_W, _COMM_H, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(137_160, 30_000, 100_000, 30_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    thesis = text_box(
        10, "ThesisStrip", BODY_X, _TH_Y, _LZ_W, _TH_H,
        [paragraph([run(_THESIS, size=MESSAGE_11PT, color=BLACK, font=FONT)],
                   align="ctr")],
        fill=BLUE_1, line_width=12_700, anchor="ctr",
        insets=(160_000, 40_000, 160_000, 40_000))

    # Connectors behind the nodes (paint order). Each lane's dashed context tie
    # aims at the centre of its outer-offset exclusion tag.
    flows = (_flow(100, _DDG_LX, _exclusion_x(0, _DDG_LX) + _EX_W // 2)
             + _flow(120, _SUB_LX, _exclusion_x(1, _SUB_LX) + _EX_W // 2))

    headers = "".join(_lane_header(11 + 2 * i, lane[0], lane[1])
                      for i, lane in enumerate(_LANES))

    nodes = []
    for li, (lane_x, _hdr, f_title, f_sub, primes, ins_title, ins_tag,
             _exc) in enumerate(_LANES):
        b = 20 + 20 * li
        px = _prime_x(lane_x)
        # Funding node (F2F2F2).
        nodes.append(_node(b + 0, "FundingNode", lane_x, _FUND_Y, _LANE_W, _FUND_H,
                           f_title, f_sub, fill=GRAY_1, fg=BLACK, line_color=BLACK,
                           line_width=12_700))
        # Prime / team-build nodes (no fill, 1pt outline).
        for pi, (p_title, p_tag) in enumerate(primes):
            nodes.append(_node(b + 1 + pi, "PrimeNode", px[pi], _PRIME_Y, _PW,
                               _PRIME_H, p_title, p_tag, fill=None, fg=BLACK,
                               line_color=BLACK, line_width=12_700,
                               sub_italic=True, insets=(50_000, 30_000, 50_000, 30_000)))
        # In-scope counted supplier node (B6C8D8).
        nodes.append(_node(b + 3, "InScopeNode", lane_x, _INS_Y, _LANE_W, _INS_H,
                           ins_title, ins_tag, fill=BLUE_2, fg=BLACK,
                           line_color=BLACK, line_width=12_700, sub_italic=True))
    nodes = "".join(nodes)

    # Fused unifying supplier-layer chip (BLUE_4) spanning both lanes.
    chip = text_box(
        50, "UnifyingSupplierChip", _DDG_LX, _CHIP_Y, _LZ_W, _CHIP_H,
        [paragraph([run(_CHIP_TITLE, size=DENSE_BODY_10PT, bold=True, color=WHITE,
                        font=FONT)], align="ctr", space_after=80,
                   line_spacing=_NODE_LNSPC),
         paragraph([run(_CHIP_BODY, size=LABEL_9PT, color=WHITE, font=FONT)],
                   align="ctr", line_spacing=_NODE_LNSPC)],
        fill=BLUE_4, line_width=12_700, anchor="ctr",
        insets=(160_000, 50_000, 160_000, 50_000))

    # Definition guardrail (no-fill line near the chip).
    guardrail = text_box(
        55, "DefinitionGuardrail", _DDG_LX, _GUARD_Y, _LZ_W, _GUARD_H,
        [paragraph([run(_GUARD_LEAD, size=LABEL_9PT, bold=True, color=BLACK,
                        font=FONT),
                    run(_GUARD_BODY, size=LABEL_9PT, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # Exclusion / context tags (gray, secondary): narrow, outer-offset, reached
    # by the catty-cornered dashed tie so they read as off the counted flow.
    exclusions = "".join(
        text_box(60 + i, "ExclusionTag", _exclusion_x(i, lane[0]), _EXC_Y, _EX_W,
                 _EXC_H,
                 [paragraph([run("Excluded and context", size=FINEPRINT_8_5PT,
                                 bold=True, color=BLACK, font=FONT)],
                            align="ctr", space_after=20, line_spacing=100_000),
                  paragraph([run(lane[7], size=SOURCES_8PT, color=BLACK,
                                 font=FONT)], align="ctr", line_spacing=100_000)],
                 fill=GRAY_2, line_width=12_700, anchor="ctr",
                 insets=(55_000, 26_000, 55_000, 26_000))
        for i, lane in enumerate(_LANES))

    legend = text_box(
        70, "Legend", BODY_X, _LEG_Y, BODY_CX, _LEG_H,
        [paragraph([run(_LEGEND, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    commentary = _commentary(80)

    # Paint order: connectors behind; chip/exclusions over their ends; rail last.
    return (flows + thesis + headers + nodes + chip + guardrail + exclusions
            + legend + commentary)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
