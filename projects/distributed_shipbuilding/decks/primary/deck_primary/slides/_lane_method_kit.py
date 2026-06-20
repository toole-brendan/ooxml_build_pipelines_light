"""_lane_method_kit - shared helpers for the supplier-lane methodology slides.

NOT a slide module (leading underscore, never registered in SLIDE_RENDERS). It
holds the geometry, node/chip/connector vocabulary, the SME-question rail, and
the shared chrome strings used by the three supplier-lane working slides:

  - supplier_lane_mece_overview  (the whole MECE map on one page)
  - supplier_lane_method_part1   (build the lane, test dominance)
  - supplier_lane_method_part2   (shared lanes, cadence and timing)

These are WORKING / SME-REVIEW slides: a methodology flow on the left, a column
of discussion / SME-challenge questions on the right. The flow logic is
conceptual - the live thresholds and timing windows stay in the Award Analysis
workbook (Assumptions + the indicator-screen tabs), not on the page.

Imports only deck_core (the shared engine) - never the build engine, never a
sibling slide module's render().
"""
from __future__ import annotations

from deck_core.primitives import (
    run, paragraph, text_box, connector, table, trow, tcell,
)
from deck_core.style import (
    BODY_X, BODY_Y, BODY_R, BODY_B,
    BLACK, WHITE, BLUE_1, BLUE_2, GRAY_2, GRAY_5, FONT,
    FINEPRINT_8_5PT, LABEL_9PT, DENSE_BODY_10PT, CONNECTOR_NOTE_8_5PT, INSETS_NONE,
)

# ── Shared chrome (the slides share the section + sources; topic differs per slide) ─
SECTION = "SAM Methodology"                 # breadcrumb section (bold first part), shared
# Breadcrumb topic (the non-bold second part) is per-slide, set as _TOPIC_LABEL in
# each slide module:  part1 → "Building the Lane"   part2 → "Concentration Tracks"
# This deck pins its Sources strip lower than the style.py default (every other
# built slide passes y=6_085_448); match it so the footer stays level slide-to-slide.
SOURCES_Y = 6_085_448
SOURCES = (
    "Note: Conceptual screen logic; the live thresholds and timing windows sit "
    "in the workbook, not on the page. | Source: Distributed Shipbuilding Award "
    "Analysis workbook (Award Events, Lane Detail, Lane Vendor FY, Assumptions, "
    "and the indicator-screen tabs); FSRS supplier-role subaward records as of "
    "2026-05-22"
)

# ── Two-pane geometry: LEFT methodology flow + RIGHT SME-question rail ────────
# The question rail is deliberately narrow (it is supporting commentary); the
# flow pane takes the rest. PANE_* are derived, so the flow auto-widens with the
# rail width.
GUTTER = 200_000
RAIL_CX = 2_805_000                          # ~10% wider than the prior 2_550_000
RAIL_X = BODY_R - RAIL_CX                    # 8_930_441
PANE_X = BODY_X                              # 453_079  (left flow pane)
PANE_CX = RAIL_X - GUTTER - BODY_X           # 8_277_362
PANE_R = PANE_X + PANE_CX                    # 8_730_441
DIVIDER_X = RAIL_X - GUTTER // 2             # thin rule between the two panes

# ── Title-strip row (shared) ─────────────────────────────────────────────────
# The flow-pane caption and the rail's "To discuss:" header are both single-cell
# title strips on ONE aligned row, lifted into the band just under the slide
# title (above BODY_Y) so the strip rules clear the flow content below on the
# vertically-full part-1 layout.
TITLE_STRIP_H = 251_778                      # strip height (matches the deck's caption strips)
TITLE_STRIP_GAP = 70_000                     # gap below a strip's rule before its content
TITLE_STRIP_Y = 1_240_000                    # the header-row y (clears the slide title at 1_194_580)

# ── Connector weights / node insets ──────────────────────────────────────────
CONN_PT = 9525                              # 0.75pt flow line (house secondary guide)
MIN_ARROW = 250_000                         # below ~0.27in an arrowhead is dropped
CHIP_INSETS = (68_580, 36_000, 68_580, 36_000)

# Fill marks POSITION IN THE SCREEN, not a verdict. The blue depth-gradient is the
# active analytical machinery: focal SUPPLIER LANE (BLUE_3 + white) -> process /
# gate / test stages (BLUE_1) -> the live tracks (BLUE_2). Gray is the framing that
# brackets the screen: the entry-context banner and EVERY terminal read. The
# opening-vs-monitor call lives in each terminal's LABEL, never in its fill — so the
# slide describes the screen without editorializing where the opportunity is.
CONTEXT_FILL = GRAY_2     # entry context + terminal reads (was GRAY_1: too near BLUE_1)
LEGEND = "Blue: lane, stages, and tracks. Gray: entry and terminal reads."
LEGEND_Y = 5_745_000                         # bottom-left, clear of the bands + Sources


def node(sp_id, name, x, y, cx, cy, cap, sub=None, *, fill=BLUE_1, txt=BLACK,
         cap_size=LABEL_9PT, sub_size=FINEPRINT_8_5PT, line_width=12700,
         anchor="ctr", align="ctr", insets=CHIP_INSETS):
    """A flow / decision / outcome node: a bold cap with optional italic
    subline(s). `sub` may be a string or a list of strings."""
    space = 60 if sub else 0
    paras = [paragraph([run(cap, size=cap_size, bold=True, color=txt, font=FONT)],
                       align=align, space_after=space)]
    if sub:
        subs = [sub] if isinstance(sub, str) else list(sub)
        for i, s in enumerate(subs):
            paras.append(paragraph(
                [run(s, size=sub_size, italic=True, color=txt, font=FONT)],
                align=align, space_after=(40 if i < len(subs) - 1 else 0)))
    return text_box(sp_id, name, x, y, cx, cy, paras, fill=fill,
                    line_width=line_width, anchor=anchor, insets=insets)


def caption(sp_id, name, x, y, cx, text, *, size=LABEL_9PT, bold=True,
            italic=False, align="l", cy=240_000):
    """A no-fill / no-border label or section caption."""
    return text_box(sp_id, name, x, y, cx, cy,
                    [paragraph([run(text, size=size, bold=bold, italic=italic,
                                    color=BLACK, font=FONT)], align=align)],
                    fill=None, line_color=None, anchor="t", insets=INSETS_NONE)


def arrow(sp_id, name, x, y, cx, cy, *, dashed=False, width=CONN_PT):
    """A flow connector; the arrowhead is dropped automatically when the run is
    too short to read it (style guidance)."""
    has_arrow = (abs(cx) + abs(cy)) >= MIN_ARROW
    return connector(sp_id, name, x, y, cx, cy, arrow=has_arrow, width=width,
                     color=BLACK, dashed=dashed)


EDGE_CHIP_H = 188_000


def edge_chip(sp_id, name, cx_center, line_y, text, *, w=None,
              size=CONNECTOR_NOTE_8_5PT, place="center", gap=44_000):
    """A terse branch label for a connector: a white-filled, no-border, italic
    chip. place='center' rides the line at line_y (the white fill masks it — a
    decision condition on the edge), so paint these AFTER the connectors.
    place='above' floats the chip just above line_y (bottom `gap` above the line),
    which reads cleaner on a short horizontal tap where a centered chip would
    split the arrow. Width auto-sizes to the text (a touch generous, since Arial
    italic renders wider than the estimate) unless `w` is given."""
    if w is None:
        w = min(max(len(text) * 62_000 + 130_000, 460_000), 2_400_000)
    top = line_y - gap - EDGE_CHIP_H if place == "above" else line_y - EDGE_CHIP_H // 2
    return text_box(sp_id, name, cx_center - w // 2, top, w, EDGE_CHIP_H,
                    [paragraph([run(text, size=size, italic=True, color=BLACK,
                                    font=FONT)], align="ctr")],
                    fill=WHITE, line_color="none", anchor="ctr",
                    insets=(45_720, 9_144, 45_720, 9_144))


def orthogonal_fork(sid, name, feed_x, feed_y, rail_y, child_xs, child_y, *,
                    width=CONN_PT):
    """A right-angled fan-out (never a diagonal): a vertical feed drop from
    (feed_x, feed_y) down to a horizontal rail at rail_y, then a vertical drop
    into each child top at child_y. The feed + rail are structural (no
    arrowhead); each child drop lands on a box and carries one. `sid` is the
    shared id counter; returns a list of connector XML strings to extend with."""
    parts = []
    xs = list(child_xs) + [feed_x]
    lo, hi = min(xs), max(xs)
    parts.append(connector(next(sid), f"{name}Feed", feed_x, feed_y, 0,
                           rail_y - feed_y, arrow=False, color=BLACK, width=width))
    parts.append(connector(next(sid), f"{name}Rail", lo, rail_y, hi - lo, 0,
                           arrow=False, color=BLACK, width=width))
    for i, cx in enumerate(child_xs):
        parts.append(connector(next(sid), f"{name}Drop{i + 1}", cx, rail_y, 0,
                               child_y - rail_y, arrow=True, color=BLACK,
                               width=width))
    return parts


def legend(sp_id, *, x=BODY_X, y=LEGEND_Y, cx=None):
    """The bottom-left semantic-fill key (LEGEND), a quiet italic caption clear of
    the flow bands and the Sources strip."""
    if cx is None:
        cx = (BODY_R - BODY_X)
    return caption(sp_id, "Legend", x, y, cx, LEGEND, size=FINEPRINT_8_5PT,
                   bold=False, italic=True, align="l", cy=200_000)


def divider(sp_id):
    """The thin vertical rule that separates the flow pane from the SME rail. It
    starts below the title-strip row (that row is the shared header band) and
    runs to just above the bottom of the body box."""
    top = TITLE_STRIP_Y + TITLE_STRIP_H + 40_000     # below the strip rules
    return connector(sp_id, "PaneDivider", DIVIDER_X, top, 0,
                     (BODY_B - 40_000) - top, arrow=False, color=GRAY_5,
                     width=6350)


def title_strip(sp_id, name, x, y, cx, text, *, h=TITLE_STRIP_H):
    """A section-title strip: 10pt bold text over a 1pt black bottom rule, no fill
    — the treatment the deck uses for its caption strips (e.g. the 'Methodology'
    caption over the slide-2 ledger). Used for BOTH the flow-pane caption and the
    rail's 'To discuss:' header so they read as one aligned title row."""
    cell = tcell(text, size=DENSE_BODY_10PT, bold=True, color=BLACK, align="l",
                 anchor="ctr", borders={"B": {"color": BLACK, "width": 12_700}})
    return table(sp_id, name, x, y, cx, h, col_widths=[cx],
                 rows=[trow([cell], h=0)])


def sme_rail(sid, name, groups, *, title="To discuss:", x=RAIL_X,
             y=TITLE_STRIP_Y, cx=RAIL_CX, cy=None, q_size=FINEPRINT_8_5PT,
             group_gap=130, q_gap=40, q_mar_l=247_650, q_indent=-152_400):
    """The right-hand discussion rail: a single-cell title strip ('To discuss:')
    over groups of (header, [questions]) in a no-fill text box (an interpretation
    rail). `groups` is a list of (header:str, questions:list[str]); `sid` is the
    shared id counter (the title strip + the question box take one id each).

    The question bullets hang-indent UNDER their group header: the glyph sits at
    q_mar_l + q_indent (≈0.10in in from the header), wrapped lines align at
    q_mar_l (≈0.27in), so the bullet block reads as nested, not flush-left."""
    parts = [title_strip(next(sid), f"{name}Title", x, y, cx, title)]
    q_y = y + TITLE_STRIP_H + TITLE_STRIP_GAP
    if cy is None:
        cy = BODY_B - q_y
    paras = []
    for gi, (header, qs) in enumerate(groups):
        paras.append(paragraph([run(header, size=LABEL_9PT, bold=True,
                                    color=BLACK, font=FONT)], space_after=50))
        for qi, q in enumerate(qs):
            last_group = gi == len(groups) - 1
            last_q = qi == len(qs) - 1
            sa = 0 if (last_group and last_q) else (group_gap if last_q else q_gap)
            paras.append(paragraph([run(q, size=q_size, color=BLACK, font=FONT)],
                                   bullet=True, mar_l=q_mar_l, indent=q_indent,
                                   space_after=sa))
    parts.append(text_box(next(sid), name, x, q_y, cx, cy, paras, fill=None,
                          line_color=None, anchor="t",
                          insets=(100_000, 60_000, 70_000, 40_000)))
    return "".join(parts)
