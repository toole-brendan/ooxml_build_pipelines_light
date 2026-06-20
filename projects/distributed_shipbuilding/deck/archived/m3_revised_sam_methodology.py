"""m3_revised_sam_methodology - show how a FIXED outsourced supplier TAM becomes
SAM by work type: pull award evidence, gate for program and role, classify
supplier dollars, calculate work-type shares, then apply those shares to the
fixed TAM pool.

Updated layout: the right audit rail is retained, while the main exhibit is
repositioned into five larger workflow nodes plus off-spine terminators. The
shorter node copy, taller rows, tighter dense line spacing, and taller scenario
chips prevent text clipping while preserving the separate fixed-TAM input.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_DEFAULT, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "SAM Build"
_TOPIC            = "SAM Methodology"
_TAKEAWAY = ("Award-derived work-type shares are applied to the outsourced TAM "
             "pool.")
_SOURCES = ("Sources: (1) FFATA/FSRS subaward records, FY2017–FY2026; "
            "(2) shared vendor and operating-entity registry, UEI evidence; "
            "(3) parent-prime PIID program-scope attribution")

_X = "×"   # multiplication operator in the apply-to-TAM formula

# Raw point sizes with no exact token (style.py allows raw sizes with a note).
_BODY_75PT = 750    # 7.5pt: compact scenario-chip body
_BODY_78PT = 780    # 7.8pt: dense side-node body
_BODY_8PT  = 800    # 8pt: dense process-node body
_LABEL_95  = 950    # 9.5pt: compact node title
_TITLE_105 = 1050   # 10.5pt: major process-node title

_LNSPC_DENSE = 100_000  # 100% line spacing for dense process nodes
_TIGHT_SIDE = (58_000, 30_000, 58_000, 30_000)
_TIGHT_CHIP = (50_000, 24_000, 50_000, 24_000)


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
_GAP = 120_000

# Caption (top, no-fill).
_CAP_Y, _CAP_H = BODY_Y, 320_000

# Guardrail strip (bottom, full width). Slightly shorter than the other modules so
# its top sits ~one row-gap below the scenario chips instead of crowding them.
_GUARD_H = 570_000
_GUARD_Y = BODY_B - _GUARD_H

# Left = evidence-flow diagram; Right = audit rail (~70 / 30 split).
_LEFT_W = 8_000_000
_RAIL_X = BODY_X + _LEFT_W + _GAP
_RAIL_W = BODY_R - _RAIL_X
# Rail text left inset; the divider is centered in the whitespace between the
# diagram's right edge and where the rail text begins (not the rail box edge).
_RAIL_LINSET = 137_160
_SEP_X = (BODY_X + _LEFT_W + _RAIL_X + _RAIL_LINSET) // 2

# Main workflow column + right-side terminators / fixed TAM input.
_SPINE_W = 4_550_000
_SPINE_X = BODY_X
_SPINE_R = _SPINE_X + _SPINE_W
_SPINE_CX = _SPINE_X + _SPINE_W // 2
_PEEL = 270_000
_SIDE_X = _SPINE_R + _PEEL
_SIDE_W = (BODY_X + _LEFT_W) - _SIDE_X

# Five larger rows replace the cramped seven-row stack.
_DIAG_TOP = _CAP_Y + _CAP_H + 50_000
_G = 55_000
_R1_Y, _R1_H = _DIAG_TOP, 430_000
_R2_Y, _R2_H = _R1_Y + _R1_H + _G, 505_000
_R3_Y, _R3_H = _R2_Y + _R2_H + _G, 530_000
_R4_Y, _R4_H = _R3_Y + _R3_H + _G, 640_000
_R5_Y, _R5_H = _R4_Y + _R4_H + _G, 570_000
_DIAG_BOT = _R5_Y + _R5_H

# Side nodes; offset slightly so the peel-off arrows do not stack on one line.
_OUT_Y, _OUT_H = _R2_Y, 430_000
_EXCL_Y, _EXCL_H = _R2_Y + _OUT_H + 25_000, 520_000
_RESID_Y, _RESID_H = _R4_Y + 100_000, 490_000
_TAM_Y, _TAM_H = _R5_Y, _R5_H

# Scenario chips, pinned above the guardrail.
_SCEN_TOP = 4_670_000
_SCEN_LBL_H = 125_000
_SCEN_GAP = 25_000
_CHIP_Y, _CHIP_H = _SCEN_TOP + _SCEN_LBL_H + _SCEN_GAP, 425_000
_CHIP_GAP = 80_000
_CHIP_W = (_LEFT_W - 4 * _CHIP_GAP) // 5
_CHIP_X = [BODY_X + i * (_CHIP_W + _CHIP_GAP) for i in range(5)]


# ── Local helpers ────────────────────────────────────────────────────────────
def _p(text, size, *, bold=False, italic=False, color=BLACK, align="ctr", space_after=0):
    return paragraph(
        [run(text, size=size, bold=bold, italic=italic, color=color, font=FONT)],
        align=align, space_after=space_after, line_spacing=_LNSPC_DENSE,
    )


def _box(sp_id, name, x, y, cx, cy, lines, *, fill, line_width=12_700, fg=BLACK,
         insets=INSETS_DEFAULT, anchor="ctr", line_color=None):
    """Filled/no-fill node. lines = (text, size, bold, italic, align, space_after)."""
    paras = [_p(t, sz, bold=b, italic=i, color=fg, align=al, space_after=sa)
             for (t, sz, b, i, al, sa) in lines]
    kwargs = {}
    if line_color is not None:
        kwargs["line_color"] = line_color
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill,
                    line_width=line_width, anchor=anchor, insets=insets, **kwargs)


def _rail(sp_id, x, y, cx, cy, title, bullets):
    """No-fill / no-border audit rail: italic title then bold-lead-in bullets."""
    paras = [paragraph([run(title, size=LABEL_9PT, bold=True, italic=True,
                            color=BLACK, font=FONT)], space_after=150)]
    for i, (lead, body) in enumerate(bullets):
        paras.append(paragraph(
            [run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
             run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
            bullet=True, space_after=(110 if i < len(bullets) - 1 else 0)))
    return text_box(sp_id, "MethodRail", x, y, cx, cy, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(_RAIL_LINSET, 45_000, 50_000, 45_000))


def _stub(sp_id, y):
    """Quiet gray vertical connector on the centre spine (no arrowhead)."""
    return connector(sp_id, "SpineStub", _SPINE_CX, y, 0, _G, color=BLACK, width=12_700)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    # Caption.
    caption = _box(
        10, "Caption", BODY_X, _CAP_Y, BODY_R - BODY_X, _CAP_H,
        [("Evidence window FY2017–FY2026 FFATA/FSRS subawards. Award dollars set mix percentages only; they are not summed into market size. Outputs are average annual because spend is lumpy.",
          FINEPRINT_8_5PT, False, True, "l", 0)],
        fill=None, insets=INSETS_NONE, anchor="ctr", line_color="none")

    # ── Main workflow spine ─────────────────────────────────────────────────
    r1 = _box(20, "AwardEvidencePull", _SPINE_X, _R1_Y, _SPINE_W, _R1_H,
              [("AWARD EVIDENCE PULL", _TITLE_105, True, False, "ctr", 90),
               ("FFATA/FSRS subawards over FY2017–FY2026; award dollars set mix, not market size.",
                _BODY_8PT, False, False, "ctr", 0)],
              fill=GRAY_1, insets=INSETS_CARD)

    r2 = _box(21, "ScopeAndRoleGates", _SPINE_X, _R2_Y, _SPINE_W, _R2_H,
              [("SCOPE AND ROLE GATES", _TITLE_105, True, False, "ctr", 90),
               ("Parent-prime PIID maps program scope; retain physical component suppliers.",
                FINEPRINT_8_5PT, False, False, "ctr", 40),
               ("Wrong-scope records and non-component roles peel off before share math.",
                _BODY_8PT, False, True, "ctr", 0)],
              fill=BLUE_1, insets=INSETS_DEFAULT)

    r3 = _box(22, "ClassifySupplierDollars", _SPINE_X, _R3_Y, _SPINE_W, _R3_H,
              [("CLASSIFY SUPPLIER DOLLARS", _TITLE_105, True, False, "ctr", 90),
               ("Registry/UEI first; known-vendor override; conservative NAICS-4 fallback; description as QA only; residual if unresolved.",
                _BODY_8PT, False, False, "l", 0)],
              fill=GRAY_1, insets=INSETS_DEFAULT)

    r4 = _box(23, "AssignWorkTypeHome", _SPINE_X, _R4_Y, _SPINE_W, _R4_H,
              [("ASSIGN ONE WORK-TYPE HOME", _LABEL_95, True, False, "ctr", 90),
               ("Structural/pre-outfit; machining/mechanical/propulsion; castings/forgings; piping/valves/pumps; electrical power/distribution/generation; HVAC/ventilation/chilled water; coatings/insulation/decking.",
                _BODY_75PT, False, False, "l", 0)],
              fill=BLUE_2, insets=INSETS_DEFAULT)

    r5 = _box(24, "ApplySharesToTam", _SPINE_X, _R5_Y, _SPINE_W, _R5_H,
              [("APPLY SHARES TO FIXED TAM", _TITLE_105, True, False, "ctr", 70),
               (f"Work-type SAM = average annual outsourced supplier TAM {_X} award-derived work-type share",
                LABEL_9PT, True, False, "ctr", 55),
               ("Fed by share calculation and the fixed TAM input only.",
                FINEPRINT_8_5PT, False, True, "ctr", 0)],
              fill=BLUE_4, line_width=12_700, fg=WHITE, insets=INSETS_DEFAULT)

    spine = r1 + r2 + r3 + r4 + r5

    # ── Off-spine side column ───────────────────────────────────────────────
    out_scope = _box(30, "OutOfScopeRecords", _SIDE_X, _OUT_Y, _SIDE_W, _OUT_H,
                     [("OUT-OF-SCOPE RECORDS", LABEL_9PT, True, False, "ctr", 70),
                      ("Wrong ship, service, or appropriation; contaminant PIIDs; weapons/OPN/WPN; outside supplier boundary.",
                       _BODY_78PT, False, False, "l", 0)],
                     fill=GRAY_2, insets=_TIGHT_SIDE)

    excl_roles = _box(31, "ExcludedRoles", _SIDE_X, _EXCL_Y, _SIDE_W, _EXCL_H,
                      [("EXCLUDED ROLES", LABEL_9PT, True, False, "ctr", 70),
                       ("Prime and co-prime yard work; GFE/SIB/MIB; mission systems and combat electronics; services, IT, holding-company flow; foreign/FMS; other non-component roles.",
                        _BODY_78PT, False, False, "l", 0)],
                      fill=GRAY_2, insets=_TIGHT_SIDE)

    residual = _box(32, "ResidualUnbucketed", _SIDE_X, _RESID_Y, _SIDE_W, _RESID_H,
                    [("RESIDUAL / UNBUCKETED", LABEL_9PT, True, False, "ctr", 70),
                     ("Unassigned supplier dollars stay in the denominator, dilute named-bucket shares, and stay outside scenario SAM until evidence improves.",
                      _BODY_78PT, False, False, "l", 0)],
                    fill=GRAY_2, insets=_TIGHT_SIDE)

    fixed_tam = _box(33, "FixedTamInput", _SIDE_X, _TAM_Y, _SIDE_W, _TAM_H,
                     [("FIXED TAM INPUT", DENSE_BODY_10PT, True, False, "ctr", 80),
                      ("Average annual outsourced supplier TAM from the TAM methodology. This is the dollar pool being sliced, and it feeds only the final bridge.",
                       FINEPRINT_8_5PT, False, False, "ctr", 0)],
                     fill=BLUE_5, line_width=12_700, fg=WHITE, insets=INSETS_DEFAULT)

    side = out_scope + excl_roles + residual + fixed_tam

    # ── Connectors ───────────────────────────────────────────────────────────
    stubs = (_stub(40, _R1_Y + _R1_H) + _stub(41, _R2_Y + _R2_H)
             + _stub(42, _R3_Y + _R3_H) + _stub(43, _R4_Y + _R4_H))

    peel = (
        connector(46, "GateToOutOfScope", _SPINE_R, _OUT_Y + _OUT_H // 2, _PEEL, 0,
                  color=BLACK, width=12_700, arrow=True)
        + connector(47, "GateToExcludedRoles", _SPINE_R, _EXCL_Y + _EXCL_H // 2, _PEEL, 0,
                    color=BLACK, width=12_700, arrow=True)
        + connector(48, "HomeToResidual", _SPINE_R, _RESID_Y + _RESID_H // 2, _PEEL, 0,
                    color=BLACK, width=12_700, arrow=True))

    tam_feed = connector(49, "FixedTamToBridge", _SIDE_X, _TAM_Y + _TAM_H // 2,
                         -_PEEL, 0, color=BLACK, width=12_700, arrow=True)

    sep = connector(55, "RailSeparator", _SEP_X, _DIAG_TOP,
                    0, _CHIP_Y + _CHIP_H - _DIAG_TOP, color=BLACK, width=9_525)

    # ── Scenario-view chips (overlapping lenses, not additive) ───────────────
    scen_label = text_box(
        56, "ScenarioLabel", BODY_X, _SCEN_TOP, _LEFT_W, _SCEN_LBL_H,
        [paragraph([run("Scenario views: overlapping lenses, not additive.",
                        size=LABEL_9PT, bold=True, italic=True, color=BLACK, font=FONT)],
                   line_spacing=_LNSPC_DENSE)],
        fill=None, line_color=None, anchor="ctr", insets=INSETS_NONE)

    chips_data = [
        ("BROAD", "all seven physical buckets", BLUE_1),
        ("HM&E", "machining, piping/valves, power, HVAC", BLUE_1),
        ("METAL", "structural, machining, castings/forgings", BLUE_1),
        ("ELECTRICAL", "ship power only", BLUE_1),
        ("MODULAR", "entity flag, not bucket union", GRAY_1),
    ]
    chips = "".join(
        _box(70 + i, f"ScenarioChip{i}", _CHIP_X[i], _CHIP_Y, _CHIP_W, _CHIP_H,
             [(name, _LABEL_95, True, False, "ctr", 60),
              (defn, _BODY_75PT, False, False, "ctr", 0)],
             fill=fill, insets=_TIGHT_CHIP)
        for i, (name, defn, fill) in enumerate(chips_data))

    # ── Right rail ───────────────────────────────────────────────────────────
    rail = _rail(
        60, _RAIL_X, _DIAG_TOP, _RAIL_W, _CHIP_Y + _CHIP_H - _DIAG_TOP,
        "SAM evidence checks",
        [("Award data is not TAM:",
          "Award records create the work-type percentages; the budget-derived "
          "TAM supplies the dollar base."),
         ("PIID attribution:",
          "Subawards inherit program scope from the parent-prime PIID; stronger "
          "than keyword matching, but not hull-level work-order proof."),
         ("Registry first:",
          "UEI and operating entity govern classification; NAICS-4 is fallback "
          "only; descriptions support QA and exceptions."),
         ("Electrical boundary:",
          "Electrical means ship power, distribution, and generation. VLS, "
          "radar, combat systems, and mission electronics are base-case "
          "exclusions or sensitivity only."),
         ("Residual discipline:",
          "Residual supplier dollars remain visible and dilute shares, but are "
          "excluded from scenario SAM until evidence supports assignment."),
         ("Reliability flags:",
          "No-recoverable-NAICS gaps, registry coverage, VLS and mission-systems "
          "treatment, modular entity flags, and bucket-share adjustments.")])

    # ── Bottom guardrail strip ───────────────────────────────────────────────
    guardrail = text_box(
        80, "Guardrails", BODY_X, _GUARD_Y, BODY_R - BODY_X, _GUARD_H,
        [paragraph([
            run("SAM guardrail: ", size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run("SAM slices the TAM dollar pool; it does not re-size the market. "
                "Award-derived shares, residual treatment, and scenario "
                "definitions move SAM allocation, while the fixed TAM headline "
                "stays unchanged.",
                size=DENSE_BODY_10PT, color=WHITE, font=FONT)])],
        fill=GRAY_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Paint order: connectors behind nodes; guardrail last.
    return (stubs + peel + tam_feed + sep
            + caption + spine + side + scen_label + chips + rail + guardrail)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
