"""m1_revised_sizing_approach - orient the reader on the TAM-to-SAM architecture
as two linked evidence engines joined by one bridge formula (not a single funnel).

TAM builds the fixed, budget-derived outsourced supplier dollar pool; SAM uses a
separate award-evidence pull to derive work-type shares, then applies those
shares back to the TAM pool. Spec: slide_specs/m1_revised_sizing_approach (M1R).
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLUE_1, BLUE_4, BLUE_5,
    GRAY_1, GRAY_5,
    WHITE, BLACK, FONT,
    INSETS_NONE, INSETS_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, MESSAGE_11PT, CAP_12PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── Chrome text ──────────────────────────────────────────────────────────────
_SECTION          = "Appendix"
_BREADCRUMB_TOPIC = "Two-Engine Overview"
_TOPIC            = "Sizing Approach"
_TAKEAWAY = ("TAM estimates outsourced supplier dollars, and SAM applies "
             "award-derived work-type shares.")
_SOURCES = ("Sources: (1) Navy SCN and P-5c shipbuilding budget justification, "
            "FY2022–FY2027; (2) FFATA and FSRS subaward records, "
            "FY2017–FY2026; (3) DoD place-of-performance and parent-prime "
            "PIID attribution evidence")

# Glyph used as an operator in the bridge formula.
_X = "×"


# ── Layout geometry (all EMU) ────────────────────────────────────────────────
# Three body bands: caption, diagram zone with two evidence engines plus a right
# method-notes rail, and a full-width guardrail strip pinned to the bottom.
_GAP = 120_000

# Caption (top, no-fill). Tightened because the caption is a single italic line.
_CAP_Y, _CAP_H = BODY_Y, 280_000

# Guardrail strip (bottom, full width). Slightly shorter to return vertical room
# to the main diagram while staying clear of the Sources chrome.
_GUARD_H = 560_000
_GUARD_Y = BODY_B - _GUARD_H

# Middle diagram zone.
_MID_TOP = _CAP_Y + _CAP_H + 70_000

# Left = panels + bridge; Right = method rail.
_LEFT_W = 8_000_000
_RAIL_X = BODY_X + _LEFT_W + _GAP
_RAIL_W = BODY_R - _RAIL_X
# Rail text left inset; the divider is centered in the whitespace between the
# diagram's right edge and where the rail text begins (not the rail box edge), so
# it no longer hugs the diagram.
_RAIL_LINSET = 137_160
_SEP_X = (BODY_X + _LEFT_W + _RAIL_X + _RAIL_LINSET) // 2

# Two engine panels inside the left zone.
_PANEL_W = (_LEFT_W - _GAP) // 2
_TAM_X = BODY_X
_SAM_X = BODY_X + _PANEL_W + _GAP

# Internal panel stack. Heights are sized from the text outward so the evidence
# nodes no longer clip and the output nodes have more breathing room.
_ZGAP = 55_000
_HDR_Y,  _HDR_H  = _MID_TOP, 290_000
_Q_Y,    _Q_H    = _HDR_Y + _HDR_H + _ZGAP, 410_000
_D_Y,    _D_H    = _Q_Y + _Q_H + _ZGAP, 620_000
_MF_Y,   _MF_H   = _D_Y + _D_H + _ZGAP, 690_000
_OUT_Y,  _OUT_H  = _MF_Y + _MF_H + _ZGAP, 390_000
_PANEL_BOT = _OUT_Y + _OUT_H

# Bridge strip below both panels (output nodes drop into it).
_BR_GAP = 260_000
_BR_Y, _BR_H = _PANEL_BOT + _BR_GAP, 540_000


# ── Local helpers ────────────────────────────────────────────────────────────
# Calculation-path nodes carry a long arrow chain that nearly fills the box; trim
# only their top inset so the block lifts clear of the bottom border.
_CALC_INSETS = (INSETS_CARD[0], 25_400, INSETS_CARD[2], INSETS_CARD[3])


def _node(sp_id, name, x, y, cx, cy, label, body, *, fill, line_width=12_700,
          label_color=BLACK, body_color=BLACK, label_size=LABEL_9PT,
          body_size=FINEPRINT_8_5PT, anchor="t", insets=INSETS_CARD):
    """A labelled diagram node: small bold cap line + a smaller body line, in a
    filled box. Every filled shape carries the house 1pt black border."""
    return text_box(
        sp_id, name, x, y, cx, cy,
        [paragraph([run(label, size=label_size, bold=True, color=label_color, font=FONT)],
                   space_after=160),
         paragraph([run(body, size=body_size, color=body_color, font=FONT)])],
        fill=fill, line_width=line_width, anchor=anchor, insets=insets)


def _zone(sp_id, name, x, y, cx, cy, label, body):
    """No-fill question zone: a small bold cap plus the question it answers."""
    return text_box(
        sp_id, name, x, y, cx, cy,
        [paragraph([run(label, size=LABEL_9PT, bold=True, color=BLACK, font=FONT)],
                   space_after=140),
         paragraph([run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def _panel(base_id, x, header, question, data_used, method_flow, out_label,
           out_value, *, out_fill):
    """One engine panel: header, question, evidence, calculation path, output."""
    return (
        # Header band — dark BLUE_5 with a 1pt black border.
        text_box(base_id, f"{header} Header", x, _HDR_Y, _PANEL_W, _HDR_H,
                 [paragraph([run(header, size=CAP_12PT, bold=True, color=WHITE, font=FONT)],
                            align="ctr")],
                 fill=BLUE_5, line_width=12_700, anchor="ctr")
        + _zone(base_id + 1, f"{header} Question", x, _Q_Y, _PANEL_W, _Q_H,
                "QUESTION ANSWERED", question)
        + _node(base_id + 2, f"{header} Evidence", x, _D_Y, _PANEL_W, _D_H,
                "EVIDENCE INPUTS", data_used, fill=GRAY_1)
        + _node(base_id + 3, f"{header} CalculationPath", x, _MF_Y, _PANEL_W, _MF_H,
                "CALCULATION PATH", method_flow, fill=BLUE_1, insets=_CALC_INSETS)
        + text_box(base_id + 4, f"{header} Output", x, _OUT_Y, _PANEL_W, _OUT_H,
                   [paragraph([run(out_label + ": ", size=DENSE_BODY_10PT, bold=True,
                                   color=WHITE, font=FONT),
                               run(out_value, size=DENSE_BODY_10PT, bold=True,
                                   color=WHITE, font=FONT)], align="ctr")],
                   fill=out_fill, line_width=12_700, anchor="ctr", insets=INSETS_CARD)
    )


def _rail(sp_id, x, y, cx, cy, title, bullets):
    """No-fill / no-border method-notes rail: an italic title then bold-lead-in
    bullets (lead, body). Keeps the diagram dominant and the notes subordinate."""
    paras = [paragraph([run(title, size=LABEL_9PT, bold=True, italic=True,
                            color=BLACK, font=FONT)], space_after=180)]
    for i, (lead, body) in enumerate(bullets):
        paras.append(paragraph(
            [run(lead + " ", size=DENSE_BODY_10PT, bold=True, color=BLACK, font=FONT),
             run(body, size=FINEPRINT_8_5PT, color=BLACK, font=FONT)],
            bullet=True, space_after=(140 if i < len(bullets) - 1 else 0)))
    return text_box(sp_id, "MethodRail", x, y, cx, cy, paras,
                    fill=None, line_color=None, anchor="t",
                    insets=(_RAIL_LINSET, 60_000, 60_000, 60_000))


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    caption = text_box(
        10, "Caption", BODY_X, _CAP_Y, BODY_R - BODY_X, _CAP_H,
        [paragraph([run(
            "TAM sizing window FY2022–FY2027, nominal then-year. SAM evidence "
            "window FY2017–FY2026. Multi-year averages normalize lumpy "
            "shipbuilding budget and award timing.",
            size=FINEPRINT_8_5PT, italic=True, color=BLACK, font=FONT)])],
        fill=None, line_color=None, anchor="t", insets=INSETS_NONE)

    # TAM engine (left) — budget-derived, top-down narrowing.
    tam = _panel(
        20, _TAM_X, "TAM DOLLAR POOL",
        "How much outsourced, supplier-addressable new-construction work exists?",
        "SCN and P-5c Basic Construction; incremental AP/LLTM and EOQ; "
        "DoD place-of-performance evidence.",
        "Budget base is gated for supplier scope, converted with program "
        "coefficients, and adjusted only for incremental AP/LLTM.",
        "Output", "average annual outsourced supplier TAM",
        out_fill=BLUE_5)

    # SAM engine (right) — award-evidence workflow, parallel to TAM.
    sam = _panel(
        30, _SAM_X, "SAM MIX EVIDENCE",
        "What share of outsourced TAM belongs to each work type?",
        "FFATA and FSRS subawards; parent-prime PIID scope; UEI and registry; "
        "vendor names; NAICS-4 fallback; description QA.",
        "Subaward history is scoped to parent-prime PIIDs; supplier component "
        "roles are retained; each dollar receives one work-type home; shares "
        "are dollar-weighted.",
        "Output", "award-derived work-type shares",
        out_fill=BLUE_4)

    sep = connector(55, "RailSeparator", _SEP_X, _MID_TOP,
                    0, _BR_Y + _BR_H - _MID_TOP, color=BLACK, width=9_525)

    tam_arrow = connector(50, "TamToBridge", _TAM_X + _PANEL_W // 2, _PANEL_BOT,
                          0, _BR_GAP, color=BLACK, width=12_700, arrow=True)
    sam_arrow = connector(51, "SamToBridge", _SAM_X + _PANEL_W // 2, _PANEL_BOT,
                          0, _BR_GAP, color=BLACK, width=12_700, arrow=True)

    bridge = text_box(
        40, "BridgeFormula", BODY_X, _BR_Y, _LEFT_W, _BR_H,
        [paragraph([run(f"Work-type SAM = fixed supplier TAM pool {_X} award-derived work-type share",
                        size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT)],
                   align="ctr", space_after=160),
         paragraph([run("TAM is the fixed budget-derived pool; SAM changes the "
                        "share applied to that pool, not the pool size.",
                        size=LABEL_9PT, italic=True, color=WHITE, font=FONT)],
                   align="ctr")],
        fill=BLUE_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Method-notes rail (right column).
    rail = _rail(
        60, _RAIL_X, _MID_TOP, _RAIL_W, _BR_Y + _BR_H - _MID_TOP,
        "Method rules",
        [("Two evidence universes:",
          "TAM comes from Navy budget inputs; SAM mix comes from historical "
          "award evidence."),
         ("Fixed pool:",
          "Supplier reclassification changes the slicing percentages, not the "
          "TAM pool."),
         ("Bridge formula:",
          "Work-type SAM equals fixed supplier TAM pool multiplied by "
          "award-derived work-type share."),
         ("Attribution basis:",
          "Subawards inherit program scope from parent-prime PIID, not "
          "hull-level work-order proof."),
         ("Output discipline:",
          "Program dollar outputs are summed. Coefficients, stream treatments, "
          "and mix evidence are not blended.")])

    guardrail = text_box(
        70, "Guardrails", BODY_X, _GUARD_Y, BODY_R - BODY_X, _GUARD_H,
        [paragraph([
            run("Guardrails: ", size=MESSAGE_11PT, bold=True, color=WHITE, font=FONT),
            run("Award data determines mix, not market size. Scenario views "
                "overlap and should not be added. The model sizes TAM and SAM "
                "opportunity only, with no SOM, capture rate, win probability, "
                "pricing haircut, or revenue conversion.",
                size=DENSE_BODY_10PT, color=WHITE, font=FONT)])],
        fill=GRAY_5, line_width=12_700, anchor="ctr", insets=INSETS_CARD)

    # Paint order: separator + arrows behind, then panels/bridge/rail/guardrail.
    return (sep + tam_arrow + sam_arrow
            + caption + tam + sam + bridge + rail + guardrail)


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto)."""
    return slide(
        breadcrumb(_SECTION, _BREADCRUMB_TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
