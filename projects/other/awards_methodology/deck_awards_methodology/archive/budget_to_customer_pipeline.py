"""budget_to_customer_pipeline - the one-page mental model linking familiar
budget materials to awards data, and the payer-vs-buyer-vs-user visibility gap.

Style + chrome rules: deck_core/slide_guide.md. Builders imported from
deck_core (style tokens, primitives, text_metrics for honest table rows).

Visual read: a dominant left-to-right pipeline (six nodes, narrow TAS connector,
flow chevrons) under a one-line finding; one focal caveat card (the TAS vs
curated-bridge distinction) plus a worked-example rail; a full-width
question/evidence/confidence/discipline table; a thin "what this unlocks" rail.
"""
from __future__ import annotations

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, tcell, trow, connector,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_CX, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5,
    DK, WHITE, BLACK, FONT,
    PAD_X_LG, PAD_Y_LG,
    INSETS_NONE, INSETS_CHIP, INSETS_CARD, INSETS_MESSAGE,
    FINEPRINT_8_5PT, LABEL_9PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, MESSAGE_11PT, BODY_12PT,
)
from deck_core.text_metrics import estimate_row_heights

LAYOUT = "slideLayout4"   # body slide; auto-numbers

# ── FILL IN: chrome text ─────────────────────────────────────────────────────
_SECTION  = "Federal Customer"
_TOPIC_LB = "Budget-to-award pipeline"
_TOPIC    = "From Budget Authority to the Real Customer"
_TAKEAWAY = ("Money, buyer, and end-user are connected, but rarely the same "
             "organization.")
_SOURCES  = ("Sources: (1) President's Budget P-1, R-1, R-2 and justification "
             "books; (2) USAspending funding and transactions (TAS, fiscal "
             "year); (3) SAM.gov Contract Awards and USAspending "
             "awarding-office fields, with FPDS as legacy lineage")


# ── Confidence palette (chips + table cells share one ramp) ──────────────────
# blue = visible in awards data; gray = low visibility / externally sourced.
_CONF = {
    "HIGH":   (BLUE_4, WHITE),
    "MEDIUM": (BLUE_2, DK),
    "LOW":    (GRAY_3, DK),
}
# Lighter grade for inside the table so the dark chips stay the louder signal.
_CONF_CELL = {
    "HIGH":   (BLUE_3, WHITE),
    "MEDIUM": (BLUE_1, DK),
    "LOW":    (GRAY_2, DK),
}


# ── Slide-local helpers ──────────────────────────────────────────────────────
def _node(sp_id, name, x, y, cx, cy, title, cue):
    """Light pipeline-stage card: bold stage name + small evidence cue.
    Secondary panel -> light fill, light GRAY_3 hairline (not a black border)."""
    return text_box(
        sp_id, name, x, y, cx, cy,
        [paragraph([run(title, size=LABEL_9PT, bold=True, color=DK, font=FONT)],
                   space_after=200),
         paragraph([run(cue, size=FINEPRINT_8_5PT, color=DK, font=FONT)])],
        fill=BLUE_1, line_color=GRAY_3, line_width=9525,   # 0.75pt secondary
        insets=INSETS_CARD, anchor="t",
    )


def _chip(sp_id, x, y, cx, cy, level):
    """Confidence tag under a node: color-graded sharp rect, black 1pt border."""
    fill, txt = _CONF[level]
    return text_box(
        sp_id, f"ConfChip {level}", x, y, cx, cy,
        [paragraph([run(level, size=LABEL_9PT, bold=True, color=txt, font=FONT)],
                   align="ctr")],
        fill=fill, line_width=12700, insets=INSETS_CHIP, anchor="ctr",
    )


def _chevron(sp_id, x, y, cx, cy):
    """Flow marker in the gap between two nodes (approved non-rect: chevron)."""
    return text_box(
        sp_id, "FlowChevron", x, y, cx, cy, [paragraph([])],
        fill=GRAY_3, line_color=GRAY_3, line_width=9525, prst="chevron",
    )


def _caption(sp_id, name, x, y, cx, text, *, align="l"):
    """No-fill italic framing label above the pipeline."""
    return text_box(
        sp_id, name, x, y, cx, 165_000,
        [paragraph([run(text, size=FINEPRINT_8_5PT, italic=True, color=DK,
                        font=FONT)], align=align)],
        fill=None, insets=INSETS_NONE, anchor="b",
    )


def _tcell(text, *, bold=False, italic=False, color=DK, fill=None, align="l",
           bottom=None):
    """Table cell with a clean horizontal-rule skin (only bottom borders)."""
    borders = {"T": "none", "L": "none", "R": "none",
               "B": ({"color": BLACK, "width": bottom} if bottom else "none")}
    return tcell(text, fill=fill, size=LABEL_9PT, bold=bold, italic=italic,
                 color=color, align=align, anchor="ctr", borders=borders)


# ── Body ─────────────────────────────────────────────────────────────────────
def _body() -> str:
    parts: list[str] = []

    # Vertical bands (EMU), stacked from BODY_Y.
    y = BODY_Y
    H_C1, G1 = 270_000, 70_000
    H_CAP, G_CAP = 165_000, 24_000
    H_CARD, G_CHIP = 760_000, 40_000
    H_CHIP, G2 = 230_000, 86_000
    H_MID, G3 = 650_000, 80_000
    G4, H_UNLK = 60_000, 200_000

    # 1) One-line finding above the pipeline (no-fill rail).
    c1_y = y
    parts.append(text_box(
        10, "Finding", BODY_X, c1_y, BODY_CX, H_C1,
        [paragraph([run("Budget materials size the funded demand; awards data "
                        "reveal where money flows and who buys through which "
                        "office.", size=BODY_12PT, bold=True, color=DK,
                        font=FONT)])],
        fill=None, insets=INSETS_NONE, anchor="ctr"))

    # ── Pipeline geometry ───────────────────────────────────────────────────
    gap_w = 235_000
    n_nodes, n_gaps = 6, 5
    node_area = BODY_CX - n_gaps * gap_w
    weights = [1.0, 0.60, 1.0, 1.0, 1.0, 1.0]      # TAS is the narrow connector
    unit = node_area / sum(weights)
    widths = [int(round(unit * w)) for w in weights]
    # Absorb integer rounding into the last node so node 6 ends exactly at BODY_R.
    xs, cur = [], BODY_X
    for i, w in enumerate(widths):
        xs.append(cur)
        cur += w + (gap_w if i < n_nodes - 1 else 0)
    widths[-1] = BODY_R - xs[-1]

    cap_y = c1_y + H_C1 + G1
    card_y = cap_y + H_CAP + G_CAP
    chip_y = card_y + H_CARD + G_CHIP

    # 2) Framing captions: budget language (left) -> bridge -> awards language.
    parts.append(_caption(20, "Caption budget", xs[0], cap_y,
                          (xs[1] + widths[1]) - xs[0],
                          "Budget materials language (familiar)"))
    parts.append(_caption(21, "Caption bridge", xs[2], cap_y, widths[2],
                          "Analyst-curated bridge", align="ctr"))
    parts.append(_caption(22, "Caption awards", xs[3], cap_y,
                          BODY_R - xs[3], "Awards data language (where money "
                          "flows)", align="r"))
    rule_y = cap_y + H_CAP - 4_000
    parts.append(connector(23, "Caption rule L", xs[0], rule_y,
                           (xs[1] + widths[1]) - xs[0], 0,
                           color=GRAY_3, width=9525))
    parts.append(connector(24, "Caption rule R", xs[3], rule_y,
                           BODY_R - xs[3], 0, color=GRAY_3, width=9525))

    # 3) Nodes + cues.
    nodes = [
        ("Node budget",   "Budget authority",    "P-1, R-1, R-2; justification books"),
        ("Node tas",      "TAS",                 "Treasury Account Symbol"),
        ("Node program",  "Program attribution", "Budget-line owner; curated bridge"),
        ("Node buyer",    "Contracting office",  "Awarding office, DODAAC, PIID"),
        ("Node vehicle",  "Award vehicle",       "Parent PIID, IDV, task and delivery orders"),
        ("Node user",     "End user",            "Requirement docs, demos; externally sourced"),
    ]
    for i, (nm, title, cue) in enumerate(nodes):
        parts.append(_node(30 + i, nm, xs[i], card_y, widths[i], H_CARD,
                           title, cue))

    # 4) Flow chevrons in the gaps.
    chev_w, chev_h = 170_000, 320_000
    chev_y = card_y + (H_CARD - chev_h) // 2
    for i in range(n_gaps):
        gap_center = xs[i] + widths[i] + gap_w // 2
        parts.append(_chevron(40 + i, gap_center - chev_w // 2, chev_y,
                              chev_w, chev_h))

    # 5) Confidence chips under each node.
    levels = ["HIGH", "HIGH", "MEDIUM", "HIGH", "HIGH", "LOW"]
    for i, lvl in enumerate(levels):
        cw = int(widths[i] * (0.90 if i == 1 else 0.66))
        cx = xs[i] + (widths[i] - cw) // 2
        parts.append(_chip(50 + i, cx, chip_y, cw, H_CHIP, lvl))

    # ── Middle row: focal caveat (left) + worked example rail (right) ─────────
    mid_y = chip_y + H_CHIP + G2
    caveat_w = 6_900_000
    parts.append(text_box(
        60, "CaveatCallout", BODY_X, mid_y, caveat_w, H_MID,
        [paragraph([run("The TAS is the mechanical hook; the curated bridge is "
                        "the semantic hook.", size=DENSE_BODY_10PT, bold=True,
                        color=WHITE, font=FONT)], space_after=400),
         paragraph([run("A TAS lands a transaction in an account such as Other "
                        "Procurement, Army, FY-XX; the program line comes from "
                        "curated attribution, not an automatic join.",
                        size=FINEPRINT_8_5PT, color=WHITE, font=FONT)])],
        fill=BLUE_5, line_width=19050,          # 1.5pt focal/anchor border
        insets=INSETS_MESSAGE, anchor="ctr"))

    we_x = BODY_X + caveat_w + 160_000
    we_w = BODY_R - we_x
    parts.append(text_box(
        61, "Worked example commentary", we_x, mid_y, we_w, H_MID,
        [paragraph([run("Worked example", size=FINEPRINT_8_5PT, bold=True,
                        color=DK, font=FONT)], space_after=300),
         paragraph([run("MSV(L) OPA line › OPA TAS › PM Transportation "
                        "Systems › ACC-Detroit Arsenal (W56HZV) › "
                        "watercraft award family › USARPAC and 8th TSC "
                        "(externally sourced)",
                        size=CONNECTOR_NOTE_8_5PT, italic=True, color=DK,
                        font=FONT)])],
        fill=None, insets=INSETS_NONE, anchor="t"))

    # ── Full-width question / evidence / confidence / discipline table ───────
    col_w = [1_900_000, 3_860_000, 1_290_000, 4_232_362]
    header = ["Question", "Best evidence", "Confidence", "What not to overclaim"]
    body_rows = [
        ("What was funded?",     "P-1, R-1, R-2; justification books; Congressional marks",
         "HIGH",             "Funded demand is not yet-obligated spend"),
        ("Which account paid?",  "USAspending funding and TAS by transaction and fiscal year",
         "HIGH (account)",   "TAS does not resolve to PE, BLI, or program line"),
        ("Which opportunity?",   "Curated bridge joining budget lines to award families",
         "MEDIUM",           "Do not force one-to-one joins on ambiguous descriptions"),
        ("Who bought?",          "Contracting agency and office, DODAAC, awarding office, PIID",
         "HIGH",             "The contracting office is not always the requirement owner"),
        ("Who uses it?",         "Program reporting, demos, requirement docs, fielding news",
         "LOW (from awards)", "Place of performance is not the end user"),
    ]
    grid_text = [header] + [list(r) for r in body_rows]
    heights = estimate_row_heights(grid_text, col_w, size_pt=9.0,
                                   header_size_pt=9.0)

    table_y = mid_y + H_MID + G3
    rows = [trow([
        _tcell(header[0], bold=True, color=WHITE, fill=BLUE_5, bottom=19050),
        _tcell(header[1], bold=True, color=WHITE, fill=BLUE_5, bottom=19050),
        _tcell(header[2], bold=True, color=WHITE, fill=BLUE_5, align="ctr",
               bottom=19050),
        _tcell(header[3], bold=True, color=WHITE, fill=BLUE_5, bottom=19050),
    ], h=heights[0])]
    for ri, (q, ev, conf, not_) in enumerate(body_rows):
        last = ri == len(body_rows) - 1
        b = None if last else 12700
        lvl = conf.split()[0]
        cfill, ctxt = _CONF_CELL[lvl]
        rows.append(trow([
            _tcell(q, bold=True, color=DK, bottom=b),
            _tcell(ev, color=DK, bottom=b),
            _tcell(conf, bold=True, color=ctxt, fill=cfill, align="ctr", bottom=b),
            _tcell(not_, color=DK, bottom=b),
        ], h=heights[ri + 1]))
    parts.append(table(70, "ConfidenceTable", BODY_X, table_y, BODY_CX,
                       sum(heights), col_widths=col_w, rows=rows))

    # ── Thin "what this unlocks" rail at the bottom ───────────────────────────
    unlk_y = table_y + sum(heights) + G4
    parts.append(text_box(
        80, "Unlocks commentary", BODY_X, unlk_y, BODY_CX, H_UNLK,
        [paragraph([
            run("What this unlocks:  ", size=DENSE_BODY_10PT, bold=True,
                color=DK, font=FONT),
            run("customer map  •  funded-demand confidence  •  "
                "budget-to-award bridge  •  buyer and contracting-office "
                "map  •  end-user gaps to research",
                size=DENSE_BODY_10PT, color=DK, font=FONT)])],
        fill=None, insets=INSETS_NONE, anchor="ctr"))

    return "".join(parts)


def render() -> str:
    return slide(
        breadcrumb(_SECTION, _TOPIC_LB)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
