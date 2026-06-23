"""awards_universe - map the contract-vehicle ecosystem and reframe
obligated-vs-ceiling plus vehicle-authority expiry as a forward opportunity pipeline.

Three zones in reading order: a vehicle-taxonomy tree (left), an obligated-vs-
ceiling decomposition (center), and a recompete-signal panel with the decision-
date rule table and the screened-universe funnel (right). A money-discipline
caveat rail runs along the bottom.

Style + chrome rules: deck_core/slide_guide.md. Builders imported from deck_core.
"""
from __future__ import annotations

from deck_core import text_metrics
from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, table, tcell, trow, connector,
)
from deck_core.charts import column_chart, graphic_frame
from deck_core.style import (
    BODY_X, BODY_CX, BODY_R, BODY_B, BODY_Y,
    BLUE_1, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_3, GRAY_5,
    DK, WHITE, BLACK, FONT,
    INSETS_BADGE, INSETS_ANSWER_CARD,
    FINEPRINT_8_5PT, LABEL_9PT, CHART_TITLE_10PT, MESSAGE_11PT,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers

# ── FILL IN: chrome text ─────────────────────────────────────────────────────
_SECTION     = "Market structure"
_TOPIC_LABEL = "Awards universe and recompete signal"
_TOPIC       = "Reading the awards universe"
_TAKEAWAY    = ("Obligated is today; the ceiling and the recompete clock are "
                "the opportunity")
_SOURCES = ("Sources: (1) Per-modification obligations from the FPDS Atom feed, "
            "reconciled with USAspending transactions; (2) vehicle ceiling and "
            "IDV ordering-period end from the SAM.gov Contract Awards API; "
            "(3) recompete, lineage, and cohort logic from the internal Army "
            "Market Mapping workbook")


# ════════════════════════════════════════════════════════════════════════════
# GEOMETRY  (computed from the BODY box so the three zones stay flush)
# ════════════════════════════════════════════════════════════════════════════
GAP = 137_160                                    # 0.15in inter-zone gap
LEFT_W   = 2_750_000
CENTER_W = 4_050_000
RIGHT_W  = BODY_CX - LEFT_W - CENTER_W - 2 * GAP  # 4_208_042
LEFT_X   = BODY_X                                 # 453_079
CENTER_X = LEFT_X + LEFT_W + GAP                  # 3_340_239
RIGHT_X  = CENTER_X + CENTER_W + GAP              # 7_527_399  (right edge == BODY_R)

# Screened-universe funnel strip (spans center + right, just above the rail).
STRIP_Y, STRIP_H = 4_730_000, 560_000             # bottom 5_290_000 (clears the rule)
# Bottom money-discipline rail + the hairline rule that sets it off.
RAIL_Y, RAIL_H = 5_330_000, 430_000               # bottom 5_760_000 (clears Sources)
RULE_Y = 5_300_000


# ── Center exhibit: obligated-vs-ceiling stacked column ──────────────────────
# Obligated is the solid base; remaining capacity is the open (light) band that
# stacks up to the latest restated ceiling. Illustrative figures, then-year $M.
_CATS = ["Watercraft IDIQ", "Support BPA", "Sustainment IDV"]
_CHART = column_chart(
    mode="stacked",
    categories=_CATS,
    series=[
        {"name": "Obligated to date", "values": [180, 95, 240], "color": BLUE_5},
        {"name": "Remaining capacity", "values": [320, 60, 410], "color": BLUE_1},
    ],
    value_axis_format='"$"#,##0"M"',
    show_value_labels=True,
    value_label_size_pt=9,
    show_legend=True,
    legend_pos="b",
    cat_label_size_pt=9,
    gap_width=90,
)
CHARTS = [_CHART]   # build_pptx writes the chart part + embedded xlsx and wires rId2


# ── slide-local helpers (thin wrappers over the imported builders) ───────────
def _node(sp_id, name, x, y, w, h, title, fill, txt, *, subline=None,
          line_width=12_700):
    """One vehicle-taxonomy node card: bold title, optional italic subline."""
    paras = [paragraph([run(title, size=LABEL_9PT, bold=True, color=txt, font=FONT)],
                       space_after=(200 if subline else 0))]
    if subline:
        paras.append(paragraph([run(subline, size=FINEPRINT_8_5PT, italic=True,
                                    color=txt, font=FONT)]))
    return text_box(sp_id, name, x, y, w, h, paras, anchor="ctr",
                    fill=fill, line_width=line_width, insets=INSETS_BADGE)


def _label(sp_id, name, x, y, w, h, runs, *, align=None, anchor="t",
           line_spacing=None):
    """A no-fill / no-border text label or commentary rail."""
    kw = {} if line_spacing is None else {"line_spacing": line_spacing}
    return text_box(sp_id, name, x, y, w, h,
                    [paragraph(runs, align=align, **kw)],
                    anchor=anchor, fill=None)


# ── Left zone: vehicle-taxonomy tree ─────────────────────────────────────────
def _vehicle_tree() -> str:
    parts = [_label(10, "Tree header", LEFT_X, BODY_Y, LEFT_W, 260_000,
                    [run("Vehicle taxonomy", size=CHART_TITLE_10PT, italic=True,
                         color=DK, font=FONT)])]
    y0, nh, ng = 1_680_000, 470_000, 90_000
    step = nh + ng
    indent = 240_000
    child_x, child_w = LEFT_X + indent, LEFT_W - indent

    parts.append(_node(11, "Node Definitive", LEFT_X, y0, LEFT_W, nh,
                       "Definitive contract", GRAY_1, DK))
    parts.append(_node(12, "Node IDV", LEFT_X, y0 + step, LEFT_W, nh,
                       "IDV (IDIQ or Requirements)", GRAY_1, DK,
                       subline="task and delivery orders nest below"))
    # Task/Delivery child nests under the IDV node (indented + connected).
    parts.append(_node(13, "Node TaskOrders", child_x, y0 + 2 * step, child_w, nh,
                       "Task and Delivery Orders", BLUE_1, DK,
                       subline="roll up into the IDV family key"))
    parts.append(connector(14, "IDV nest Connector", child_x + 90_000,
                           y0 + step + nh, 0, (y0 + 2 * step) - (y0 + step + nh),
                           color=GRAY_5, width=12_700))
    parts.append(_node(15, "Node BPA", LEFT_X, y0 + 3 * step, LEFT_W, nh,
                       "BPA and BPA calls", GRAY_1, DK))
    parts.append(_node(16, "Node BOA", LEFT_X, y0 + 4 * step, LEFT_W, nh,
                       "BOA", GRAY_1, DK))
    # OT node accent-flagged as the defense-tech-relevant pathway (focal).
    parts.append(_node(17, "Node OT", LEFT_X, y0 + 5 * step, LEFT_W, nh,
                       "OT agreement or order", BLUE_5, WHITE,
                       subline="defense-tech-relevant pathway",
                       line_width=19_050))
    return "".join(parts)


# ── Center zone: money rail + chart header + obligated-vs-ceiling exhibit ─────
def _center() -> str:
    c1_y, c1_h = BODY_Y, 930_000
    rail = text_box(
        20, "Money measures rail", CENTER_X, c1_y, CENTER_W, c1_h,
        [paragraph([run("Three dollar measures, never summed.",
                        size=LABEL_9PT, bold=True, color=DK, font=FONT)],
                   space_after=300),
         paragraph([run("Obligated is money legally committed; current value is "
                        "base and exercised options; ceiling is base and all "
                        "options. These are distinct amount-types, a register not "
                        "a fact table. Only the per-modification action stream is "
                        "additive: sum that, never the restated cumulative totals.",
                        size=LABEL_9PT, color=DK, font=FONT)])],
        anchor="t", fill=None)

    hdr_y, hdr_h = c1_y + c1_h + 30_000, 400_000
    header = text_box(
        21, "ChartTitle obligated ceiling", CENTER_X, hdr_y, CENTER_W, hdr_h,
        [paragraph([run("Obligated to date vs potential ceiling",
                        size=CHART_TITLE_10PT, italic=True, color=DK, font=FONT)]),
         paragraph([run("Per vehicle or family; latest restated ceiling",
                        size=FINEPRINT_8_5PT, italic=True, color=GRAY_5, font=FONT)])],
        anchor="t", fill=None)

    chart_y = hdr_y + hdr_h + 20_000
    chart_h = (STRIP_Y - 80_000) - chart_y           # sits above the funnel strip
    frame = graphic_frame(sp_id=22, name="ObligatedCeiling chart",
                          x=CENTER_X, y=chart_y, cx=CENTER_W, cy=chart_h, rId="rId2")
    return rail + header + frame


# ── Right zone: recompete reframe card + decision-date rule table ────────────
def _recompete_card() -> str:
    y, h = BODY_Y, 1_320_000
    return text_box(
        30, "Recompete reframe card", RIGHT_X, y, RIGHT_W, h,
        [paragraph([run("The recompete is when the government loses authority to "
                        "place new orders, not the latest task-order end date.",
                        size=1050, bold=True, color=WHITE, font=FONT)],  # 10.5pt
                   space_after=400),
         paragraph([run("IDV: ordering-period end, hydrated from the SAM Contract "
                        "Awards API. BOA or BPA: a master-agreement date, not a "
                        "guaranteed recompete, lower confidence. Standalone: its "
                        "own period-of-performance end. Option-years-left equals "
                        "potential end minus decision date, the unexercised "
                        "ceiling expressed as time.",
                        size=LABEL_9PT, color=WHITE, font=FONT)])],
        anchor="t", fill=BLUE_5, line_width=19_050, insets=INSETS_ANSWER_CARD)


def _recompete_table():
    """Decision-date rule per vehicle. Confidence graded on the blue ramp
    (dark = high, light = low) to stay inside the locked palette. Returns
    (xml, table_height)."""
    grade = {"High": (BLUE_5, WHITE), "Medium": (BLUE_3, WHITE), "Low": (BLUE_1, DK)}
    col_w = [1_200_000, 2_240_000, 768_042]
    rows_text = [
        ["Vehicle type", "Recompete date rule", "Confidence"],
        ["Standalone contract", "Its own period-of-performance end", "High"],
        ["IDV (hydrated)", "Ordering-period end, SAM Contract Awards", "High"],
        ["IDV (base record)", "Vehicle base-record PoP end", "Medium"],
        ["BPA", "Call-period end; orders may continue under parent", "Medium"],
        ["BOA", "Nominal end, NOT a guaranteed recompete", "Low"],
    ]
    heights = text_metrics.estimate_row_heights(
        rows_text, col_w, size_pt=9.0, header_size_pt=9.0)

    def _b(width):   # cascading bottom rule
        return {"B": {"color": BLACK, "width": width}} if width else {"B": "none"}

    rows = []
    n = len(rows_text)
    for r, (vt, rule, conf) in enumerate(rows_text):
        last = (r == n - 1)
        bw = 19_050 if r == 0 else (0 if last else 12_700)
        if r == 0:   # header: rule skin (no fill, bold, 1.5pt bottom rule)
            rows.append(trow([
                tcell(vt, size=LABEL_9PT, bold=True, color=DK, align="l", borders=_b(bw)),
                tcell(rule, size=LABEL_9PT, bold=True, color=DK, align="l", borders=_b(bw)),
                tcell(conf, size=LABEL_9PT, bold=True, color=DK, align="ctr", borders=_b(bw)),
            ], h=heights[r]))
            continue
        fill, txt = grade[conf]
        rows.append(trow([
            tcell(vt, size=LABEL_9PT, bold=True, color=DK, align="l", borders=_b(bw)),
            tcell(rule, size=LABEL_9PT, color=DK, align="l", borders=_b(bw)),
            tcell(conf, size=LABEL_9PT, bold=True, color=txt, align="ctr",
                  fill=fill, borders=_b(bw)),
        ], h=heights[r]))

    table_h = sum(heights)
    y = BODY_Y + 1_320_000 + 80_000
    xml = table(31, "Recompete rule table", RIGHT_X, y, sum(col_w), table_h,
                col_widths=col_w, rows=rows)
    return xml, y + table_h


# ── Bottom band: screened-universe funnel strip + money-discipline caveat ─────
def _funnel_and_caveat() -> str:
    strip_y, strip_h = STRIP_Y, STRIP_H
    # Commentary 3 - count opportunities once (under the center chart).
    c3 = text_box(
        40, "Count once Commentary", CENTER_X, strip_y, CENTER_W, strip_h,
        [paragraph([run("Count opportunities once. ",
                        size=LABEL_9PT, bold=True, color=DK, font=FONT),
                    run("Lineage chaining (incumbent, PSC, gap) tells a real "
                        "overdue recompete from a superseded follow-on; cohort "
                        "logic folds co-awarded vehicles into one requirement.",
                        size=FINEPRINT_8_5PT, color=GRAY_5, font=FONT)])],
        anchor="t", fill=None)
    # Screened-universe funnel as a muted inline figure (under the right panel).
    funnel = text_box(
        41, "Screened universe figure", RIGHT_X, strip_y, RIGHT_W, strip_h,
        [paragraph([run("Screened once: ", size=LABEL_9PT, bold=True, color=DK, font=FONT),
                    run("1,688 award families to 226.", size=LABEL_9PT, color=DK, font=FONT)],
                   space_after=300),
         paragraph([run("124 overdue", size=LABEL_9PT, bold=True, color=BLUE_4, font=FONT),
                    run("  ·  62 superseded  ·  40 active",
                        size=FINEPRINT_8_5PT, italic=True, color=GRAY_5, font=FONT)])],
        anchor="t", fill=None)

    rule = connector(50, "Caveat divider Rule", BODY_X, RULE_Y, BODY_CX, 0,
                     color=GRAY_3, width=9_525)
    caveat = text_box(
        51, "Money discipline Rail", BODY_X, RAIL_Y, BODY_CX, RAIL_H,
        [paragraph([run("Money discipline. ", size=LABEL_9PT, bold=True, color=DK, font=FONT),
                    run("Reconcile award-reported obligations against an independent "
                        "FPDS and USAspending reconstruction, and carry a coverage "
                        "ratio so a partial reconstruction can never pass as a "
                        "vehicle's value. Figures are per vehicle or family, "
                        "then-year $M, illustrative of method.",
                        size=LABEL_9PT, color=DK, font=FONT)])],
        anchor="t", fill=None)
    return c3 + funnel + rule + caveat


def _body() -> str:
    table_xml, _ = _recompete_table()
    return (_vehicle_tree()
            + _center()
            + _recompete_card()
            + table_xml
            + _funnel_and_caveat())


def render() -> str:
    """Assemble chrome + body into a complete <p:sld> (no page number; auto)."""
    return slide(
        breadcrumb(_SECTION, _TOPIC_LABEL)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
