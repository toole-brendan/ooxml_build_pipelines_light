"""awards_universe - decode an award record as a nested ecosystem: vehicles
authorize buying routes, orders record activity, dollar fields are distinct
money lenses, and first-tier subawards expose the supplier layer prime data hides.

Style + chrome rules: deck_core/slide_guide.md. Builders imported from deck_core.

Visual read: a four-layer nesting map on the left (vehicle -> order -> money ->
supplier) with down-arrows for parent-child flow, a "what this unlocks" panel on
the right, and a money-discipline caveat rail across the bottom. The reference
glossary table, the obligated-vs-ceiling bar, and the recompete strip from the
spec are deliberately folded into the map descriptors / unlocks bullets rather
than drawn as separate objects, so the page stays a legible ecosystem map and
not a dense table (spec: "Use nesting and indentation, not a dense table";
"Do not let the recompete logic dominate the slide").
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R,
    BLUE_1, BLUE_4, BLUE_5, GRAY_2, GRAY_3, GRAY_4,
    DK, WHITE, BLACK, FONT,
    LABEL_9PT, FINEPRINT_8_5PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, CAP_12PT,
)

LAYOUT = "slideLayout4"   # body slide; auto-numbers (no page-number shape)

# -- chrome text --------------------------------------------------------------
_SECTION         = "Awards Data"
_BREADCRUMB_TOPIC = "Anatomy of an award record"
_TITLE_TOPIC     = "Reading the awards universe"
_TAKEAWAY        = ("Vehicles, obligations, ceilings, and subawards reveal "
                    "the market structure")
_SOURCES = ("Sources: (1) SAM.gov Contract Awards and Entity Management APIs; "
            "(2) USAspending award, transaction, and subaward records; "
            "(3) SAM Acquisition Subaward Reporting, first-tier and may lag prime activity")


# ── Layout geometry ──────────────────────────────────────────────────────────
# Left two-thirds: the layer map. Right third: the unlocks panel. Bottom: rail.
_LX  = BODY_X                       # left map region x
_LW  = 7_050_000                    # left map region width
_LR  = _LX + _LW                    # 7_503_079 left region right edge

_GUT = 170_000                      # gutter between map and panel
_PX  = _LR + _GUT                   # 7_673_079 panel x
_PW  = BODY_R - _PX                 # 4_062_362 panel width

_RAIL_H = 470_000
_RAIL_Y = 5_350_000                 # bottom rail (bottom 5_820_000, clears BODY_B + sources)

_MAP_TOP    = BODY_Y                # 1_371_600
_MAP_BOTTOM = _RAIL_Y - 70_000      # 5_380_000
_MAP_H      = _MAP_BOTTOM - _MAP_TOP

_GAP    = 250_000                                   # inter-band gap (holds an arrow)
_BAND_H = (_MAP_H - 3 * _GAP) // 4                  # 814_600
_IDW    = 1_700_000                                 # identity-cell width
_ID_GAP = 80_000                                    # identity -> body gap
_BX     = _LX + _IDW + _ID_GAP                      # body cell x
_BW     = _LR - _BX                                 # body cell width

_DOT = '  ·  '   # neutral member separator (no "/" or "+" separators, per guide)


def _band_top(i: int) -> int:
    return _MAP_TOP + i * (_BAND_H + _GAP)


def _members(parts: list[tuple[str, bool]]) -> list:
    """Build a members paragraph: bold member runs joined by quiet GRAY_4 dots.
    parts is a list of (text, accent) — accent=True flags an OT route in BLUE_4."""
    runs: list = []
    for idx, (text, accent) in enumerate(parts):
        if idx:
            runs.append(run(_DOT, size=DENSE_BODY_10PT, color=GRAY_4, font=FONT))
        runs.append(run(text, size=DENSE_BODY_10PT, bold=True,
                        color=(BLUE_4 if accent else DK), font=FONT))
    return runs


# Each layer: (number, name, role, member parts, descriptor runs-builder, focal)
def _identity_cell(sp_id: int, i: int, num: str, name: str, role: str) -> str:
    top = _band_top(i)
    return text_box(
        sp_id, f"Layer{num}Id", _LX, top, _IDW, _BAND_H,
        [paragraph([run(f"{num}  {name}", size=CAP_12PT, bold=True,
                        color=WHITE, font=FONT)], align="l"),
         paragraph([run(role, size=LABEL_9PT, italic=True, color=WHITE, font=FONT)],
                   align="l", space_after=0)],
        anchor="ctr", fill=BLUE_5, line_color=BLACK, line_width=12_700,
        l_ins=110_000, r_ins=70_000, t_ins=50_000, b_ins=50_000,
    )


def _body_cell(sp_id: int, i: int, name: str, member_runs: list,
               descriptor_runs: list, *, focal: bool = False) -> str:
    top = _band_top(i)
    line_w = 19_050 if focal else 12_700
    line_c = BLACK if focal else GRAY_3      # focal=black 1.5pt; else GRAY_3 secondary
    return text_box(
        sp_id, f"Layer{name}Body", _BX, top, _BW, _BAND_H,
        [paragraph(member_runs, align="l", space_after=300),
         paragraph(descriptor_runs, align="l", space_after=0)],
        anchor="ctr", fill=BLUE_1, line_color=line_c, line_width=line_w,
        l_ins=114_300, r_ins=114_300, t_ins=63_500, b_ins=63_500,
    )


def _arrow(sp_id: int, i: int) -> str:
    """Down-arrow in the gutter between band i and band i+1 (parent -> child)."""
    bottom = _band_top(i) + _BAND_H
    x = _LX + _IDW // 2
    return connector(sp_id, f"FlowArrow{i}", x, bottom + 24_000, 0, _GAP - 48_000,
                     color=BLUE_4, width=19_050, arrow=True)


def _rel_note(sp_id: int, i: int, text: str) -> str:
    """Italic relationship note beside the flow arrow (no fill, no border)."""
    bottom = _band_top(i) + _BAND_H
    return text_box(
        sp_id, f"FlowNote{i}", _BX, bottom, _BW, _GAP,
        [paragraph([run(text, size=CONNECTOR_NOTE_8_5PT, italic=True,
                        color=BLUE_4, font=FONT)], align="l")],
        anchor="ctr", fill=None, line_color="none",
        l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    )


def _bullet(lead: str, rest: str) -> str:
    return paragraph(
        [run(lead, size=DENSE_BODY_10PT, bold=True, color=DK, font=FONT),
         run(rest, size=DENSE_BODY_10PT, color=DK, font=FONT)],
        bullet=True, space_after=500,
    )


def _body() -> str:
    parts: list[str] = []

    # ── Layer 1 — Vehicle ────────────────────────────────────────────────────
    parts.append(_identity_cell(10, 0, "1", "VEHICLE", "How gov buys"))
    parts.append(_body_cell(
        11, 0, "Vehicle",
        _members([("Definitive contract", False), ("IDV (IDIQ, GWAC, FSS)", False),
                  ("BPA", False), ("BOA", False), ("OT agreement", True)]),
        [run("Standalone buys, ordering authority, and agreement pathways. ",
             size=LABEL_9PT, italic=True, color=DK, font=FONT),
         run("OT routes", size=LABEL_9PT, italic=True, bold=True, color=BLUE_4, font=FONT),
         run(" matter most for rapid defense-tech capability.",
             size=LABEL_9PT, italic=True, color=DK, font=FONT)],
    ))

    # ── Layer 2 — Order / action ─────────────────────────────────────────────
    parts.append(_identity_cell(12, 1, "2", "ORDERS", "Activity recorded"))
    parts.append(_body_cell(
        13, 1, "Order",
        _members([("Base award", False), ("Modifications", False),
                  ("Task and delivery orders", False), ("BPA calls", False),
                  ("OT orders", True)]),
        [run("Orders and modifications consume a vehicle's authority; each child "
             "action references its parent vehicle.",
             size=LABEL_9PT, italic=True, color=DK, font=FONT)],
    ))

    # ── Layer 3 — Money ──────────────────────────────────────────────────────
    parts.append(_identity_cell(14, 2, "3", "MONEY", "Different lenses"))
    parts.append(_body_cell(
        15, 2, "Money",
        _members([("Action and cumulative obligation", False), ("Current value", False),
                  ("Potential value", False), ("Ceiling", False)]),
        [run("Obligated is past execution; ceiling and ordering authority are future "
             "opportunity, read as remaining capacity plus recompete timing.",
             size=LABEL_9PT, italic=True, color=DK, font=FONT)],
    ))

    # ── Layer 4 — Supplier (focal: subaward caution) ─────────────────────────
    parts.append(_identity_cell(16, 3, "4", "SUPPLIER", "Industrial base"))
    parts.append(_body_cell(
        17, 3, "Supplier",
        _members([("Prime awardee", False), ("First-tier subawardees", False),
                  ("UEI and CAGE", False), ("Parent-company rollups", False),
                  ("Capability tags", False)]),
        [run("Separate reporting universe: ", size=LABEL_9PT, bold=True, color=DK, font=FONT),
         run("a prime-award feed cannot show the full industrial base. Subawards "
             "expose supplier positions, workshare, and teaming.",
             size=LABEL_9PT, italic=True, color=DK, font=FONT)],
        focal=True,
    ))

    # ── Parent-child flow arrows + relationship notes ────────────────────────
    parts.append(_arrow(20, 0))
    parts.append(_rel_note(23, 0, "Orders consume a vehicle's ordering authority"))
    parts.append(_arrow(21, 1))
    parts.append(_rel_note(24, 1, "Every action carries its own dollar fields"))
    parts.append(_arrow(22, 2))
    parts.append(_rel_note(25, 2, "Primes report their first-tier subawards"))

    # ── "What this unlocks" panel (right third) ──────────────────────────────
    cap_h = 380_000
    parts.append(text_box(
        30, "UnlocksContainer", _PX, _MAP_TOP, _PW, _MAP_H,
        [_bullet("Incumbent map: ",
                 "by agency, contracting office, PSC, NAICS, and program theme."),
         _bullet("Vehicle-route map: ",
                 "standalone, IDV family, BPA and BOA, or OT."),
         _bullet("Remaining capacity: ",
                 "obligated-to-date against ceiling and potential value."),
         _bullet("Recompete signal: ",
                 "when the government loses authority to place new work."),
         _bullet("Supplier map: ",
                 "first-tier subawardees, UEIs, parents, and capability clusters."),
         _bullet("De-duplicated families: ",
                 "parent, children, and modifications collapsed into one opportunity.")],
        anchor="t", fill=None, line_color=GRAY_3, line_width=12_700,
        l_ins=114_300, r_ins=114_300, t_ins=cap_h + 60_000, b_ins=80_000,
    ))
    parts.append(text_box(
        31, "UnlocksCap", _PX, _MAP_TOP, _PW, cap_h,
        [paragraph([run("WHAT AWARDS DATA UNLOCKS", size=CAP_12PT, bold=True,
                        color=WHITE, font=FONT)], align="ctr")],
        anchor="ctr", fill=BLUE_5, line_color=BLACK, line_width=12_700,
        insets=(120_000, 30_000, 120_000, 30_000),
    ))

    # Compact recompete note fills the lower panel (spec: "if space allows";
    # kept small so it does not dominate the ecosystem map).
    _pad = 114_300
    parts.append(connector(32, "PanelDivider", _PX + _pad, 4_550_000,
                           _PW - 2 * _pad, 0, color=GRAY_3, width=9_525))
    parts.append(text_box(
        33, "RecompeteNote", _PX + _pad, 4_610_000, _PW - 2 * _pad, 590_000,
        [paragraph([run("RECOMPETE CLOCK: ", size=LABEL_9PT, bold=True, color=DK, font=FONT),
                    run("the signal is authority to place new work.",
                        size=LABEL_9PT, italic=True, color=DK, font=FONT)],
                   align="l", space_after=200),
         paragraph([run("Standalone, PoP end · IDV family, ordering-period end · "
                        "BPA and BOA, agreement terms at lower confidence · "
                        "OT, validate externally.",
                        size=FINEPRINT_8_5PT, italic=True, color=GRAY_4, font=FONT)],
                   align="l")],
        anchor="t", fill=None, line_color="none", l_ins=0, t_ins=0, r_ins=0, b_ins=0,
    ))

    # ── Money-discipline rail (bottom, full width caveat strip) ──────────────
    parts.append(text_box(
        40, "MoneyDisciplineRail", BODY_X, _RAIL_Y, BODY_CX, _RAIL_H,
        [paragraph(
            [run("MONEY DISCIPLINE   ", size=DENSE_BODY_10PT, bold=True, color=DK, font=FONT),
             run("Sum action-level obligations only.   Never sum cumulative totals.   "
                 "Do not add budget demand, obligations, ceilings, and subawards.   "
                 "Keep each money universe as a separate lens.",
                 size=DENSE_BODY_10PT, color=DK, font=FONT)],
            align="l")],
        anchor="ctr", fill=GRAY_2, line_color=BLACK, line_width=12_700,
        l_ins=140_000, r_ins=140_000, t_ins=50_000, b_ins=50_000,
    ))

    return "".join(parts)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld> (no page number; auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TITLE_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
