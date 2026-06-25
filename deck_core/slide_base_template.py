"""<slide_name> - ONE-SENTENCE INTENT: what this slide is for.

Style + chrome rules: deck_core/slide_guide.md. Importable builders live in
deck_core (no longer copied per slide):
  - deck_core.style       palette, type scale, the BODY box, insets (tokens)
  - deck_core.primitives  chrome (breadcrumb / title_placeholder / prelim_chip /
                          sources_line) + body builders (run, paragraph,
                          text_box, connector) + native tables (table / trow / tcell)
  - deck_core.charts      column / bar / line / waterfall / marimekko factories
Worked examples of the house conventions: deck_core/slide_snippets.md. Geometry
truth of a built slide: the emitted XML + deck_{prog}/reports/slide_probe/<name>.

To use:
  1. Copy to deck_{sub,ddg}/slides/<slide_name>.py.
  2. Rename render() to match the filename (optional).
  3. Write the one-sentence INTENT above.
  4. Fill the FILL IN chrome text below, then build _body() at the marker.
  5. Register in deck_{sub,ddg}/slides/__init__.py SLIDE_RENDERS, in order.

Imports, not inlining: palette + chrome + body builders are imported from
deck_core rather than copied into the slide. The chrome is pre-wired in
render() - set its text via the constants below and compose _body() from the
imported builders (or raw OOXML; drop down whenever it reads better).
"""
from __future__ import annotations

from xml.sax.saxutils import escape as _esc  # for raw-OOXML body text, if used

from deck_core.primitives import (
    slide,
    breadcrumb, title_placeholder, prelim_chip, sources_line,
    run, paragraph, text_box, connector,
    table, trow, tcell,   # native tables: row/column data, merges, spans
)
from deck_core.style import (
    BODY, BODY_X, BODY_Y, BODY_CX, BODY_CY, BODY_R, BODY_B,
    BLUE_1, BLUE_2, BLUE_3, BLUE_4, BLUE_5,
    GRAY_1, GRAY_2, GRAY_3, GRAY_4, GRAY_5,
    DK, WHITE, BREADCRUMB, BLACK, PRELIM, FONT,
    PAD_X, PAD_Y, PAD_X_LG, PAD_Y_LG,
    INSETS_NONE, INSETS_DEFAULT, INSETS_CARD, INSETS_CHIP,
    INSETS_LABEL, INSETS_MICRO_CAP, INSETS_BADGE, INSETS_EVIDENCE,
    INSETS_MESSAGE, INSETS_RIBBON_CAP, INSETS_ANSWER_CARD,
    SOURCES_8PT, FINEPRINT_8_5PT, LABEL_9PT, CONNECTOR_NOTE_8_5PT,
    DENSE_BODY_10PT, CHART_TITLE_10PT, MESSAGE_11PT, BODY_12PT, CAP_12PT,
    EXHIBIT_HEADER_13PT, VALUE_14PT, BADGE_16PT, RIBBON_KPI_18PT,
    ANSWER_KPI_24PT, HERO_32PT,
    blue_pair, gray_pair,
)

LAYOUT = "slideLayout4"   # body slide; the base layout auto-numbers (no page-number shape)

# ── FILL IN: chrome text ─────────────────────────────────────────────────────
_SECTION  = "Section"                              # breadcrumb {Section} (bold)
_TOPIC    = "Topic Label"                          # breadcrumb {Topic Label} + title topic
_TAKEAWAY = "the one-line finding."                # title finding, sentence case, terminal period
_SOURCES  = "Sources: (1) ...; (2) ...; (3) ..."   # 2-3 primary sources, no final period


# ════════════════════════════════════════════════════════════════════════════
# BUILD YOUR SLIDE BODY HERE
# ════════════════════════════════════════════════════════════════════════════
# Compose body shapes within BODY (x, y, cx, cy) so the slide stays flush and
# clear of chrome. Use the imported builders or raw OOXML. To lay out N equal
# items, compute coords: item_w = (BODY_CX - (n - 1) * gap) // n, then item i
# at BODY_X + i * (item_w + gap).
#
# Before coding, choose or invent the slide's visual read.
# Common polished reads include:
#   - chart/exhibit + no-fill commentary rail
#   - compact boundary cue + main exhibit
#   - answer card(s) + evidence
#   - axis-first exhibit
#   - native table/register for rectangular row-column data
#   - card grid/chip rail for independent visual objects
#   - system map
#
# Polished default:
#   one dominant visual object + integrated labels/commentary.
#   Use fills only for semantic objects: answer, boundary, evidence, method,
#   unit caveat, program identity. Use no-fill/no-border text for labels,
#   captions, row headers, tick labels, legends, and longer interpretation
#   bullets beside charts.
#
# Do NOT add a bottom readout bar by default. Prefer title findings, direct
# labels, no-fill commentary bullets, or a small unit/scope note when needed.
#
# For a chart: add a module-level `CHARTS = [_CHART]` and import a factory from
# deck_core.charts (column_chart / line_chart / waterfall_chart / marimekko_chart).
# build_pptx reads CHARTS, writes the chart parts, and wires the slide rels; the
# slide body holds the chart's graphic_frame. See slide_snippets.md "charts".
#
# For a table: build it with the low-level engine — table(sp_id, name, x, y, cx, cy,
# col_widths=[...], rows=[trow([tcell(...), ...]), ...]). tcell() carries fill /
# color / bold / align / borders / insets and grid_span / row_span for merges; the
# engine synthesizes the merge-filler cells. Cells default to single (100%) line
# spacing. See slide_snippets.md "tables".
#
# Object choice: if the content has column headers, row labels, and comparable
# values across rows/columns, it is a TABLE — use table()/trow()/tcell(), not a grid
# of text_box() shapes. Shape grids are for independent cards/chips/panels only.
#
# ── TYPE QUICK REF ───────────────────────────────────────────────────────────
# SOURCES_8PT           8pt    sources footer, true footnote/caveat
# FINEPRINT_8_5PT       8.5pt  dense subline, unit note, chip body
# LABEL_9PT             9pt    row/column/bar label; often bold or italic
# CONNECTOR_NOTE_8_5PT  8.5pt  tree/flow connector note; usually italic
# DENSE_BODY_10PT       10pt   compact body in dense cards, rails, ledgers
# CHART_TITLE_10PT      10pt   chart/exhibit title; italic, no fill
# MESSAGE_11PT          11pt   short message/readout sentence
# BODY_12PT             12pt   default spacious body text
# CAP_12PT              12pt   cap/header; bold, often ALL CAPS
# EXHIBIT_HEADER_13PT   13pt   local title inside a large visual block
# VALUE_14PT            14pt   compact numeric value; bold
# BADGE_16PT            16pt   program badge / gate / row identity; bold
# RIBBON_KPI_18PT       18pt   boundary-ribbon KPI; bold
# ANSWER_KPI_24PT       24pt   answer-card KPI; bold
# HERO_32PT             32pt   one content-slide hero; bold
#
# These are defaults, not a cage. If the slide needs another size, use a raw
# size with a nearby comment, e.g. size=1150  # 11.5pt.
#
# Body-text rule: every body-shape run should pass size=... and font=FONT.
# Chrome placeholders may inherit; body shapes should not.
#
# ── COMMON IN-SHAPE HIERARCHY ────────────────────────────────────────────────
# A polished shape is rarely one flat run — it has a small internal ladder:
#   1. Cap + subline       CAP_12PT bold/ALL-CAPS  + LABEL_9PT italic
#   2. Value + qualifier   RIBBON_KPI_18PT bold    + FINEPRINT_8_5PT italic
#   3. Label prefix + value  FINEPRINT_8_5PT bold prefix + MESSAGE_11PT value
#   4. Section + bullets   DENSE_BODY_10PT bold label + LABEL_9PT bullets
#   5. Map / flow box      LABEL_9PT bold title + FINEPRINT_8_5PT body
#   6. Connector note      CONNECTOR_NOTE_8_5PT italic, no fill, no border
#
# ── COLOR / FILL QUICK REF ───────────────────────────────────────────────────
# Filled shapes are semantic objects; labels and explanations are usually
# no-fill / no-border.
#   BLUE_5 + WHITE + 1.5pt black  primary anchor, hero, boundary cap, program/
#                                 implication badge
#   BLUE_5 + WHITE + 1pt black    strip cap, method cap, out-of-scope badge,
#                                 strong row identity
#   BLUE_4 + WHITE + 1pt black    secondary dark answer, strong range bar
#   BLUE_3 + WHITE + 1pt black    mid-strength bar / modeled signal
#   BLUE_1 + BLACK + 1pt black    in-scope body cell, method body, soft positive
#   GRAY_1 + BLACK + 1pt black    neutral support/context cell, band
#   GRAY_2 + BLACK + 1pt black    unit check, caveat, denominator strip
#   GRAY_3 + BLACK + 1pt black    residual, ambiguous segment, unattributed zone
#   GRAY_5 + WHITE + 1pt black    terminal marker, visible-floor tick (sparingly)
#   none   + no border            commentary, labels, captions, notes, row/column/
#                                 axis labels, ticks, connector notes, legends,
#                                 chart/exhibit and table titles, subtitles
#   none   + thin rule            container, location strip, bracket, axis rule,
#                                 separator only
# Border weights: 12_700 = 1pt standard · 19_050 = 1.5pt focal/anchor ·
#                 9_525 / 6_350 = thin rule / connector / axis only.
#
# ── SHAPE GEOMETRY QUICK REF ─────────────────────────────────────────────────
# Default geometry is a sharp rectangle (prst="rect"): cards, caps, bands, rails,
# bars, chips, badges, chart containers, method strips, unit checks,
# takeaway strips. Rectangular row-column data should be a native table, not
# shape-built cells.
# Rounded geometry is reserved for controlled tags/dots/chevrons only:
# classification tags, numbered process dots, flow chevrons. Never round normal
# cards, panels, ledgers, or bars.
# Object grammar:
#   filled + sharp rect + 1pt black    = normal object
#   filled + sharp rect + 1.5pt black  = focal / anchor object
#   no fill + no border                = label / caption / commentary
#   no fill + thin rule                = axis / container / separator
def _body() -> str:
    return ""   # chrome-only until you build the body


def render() -> str:
    """Assemble chrome + body into a complete <p:sld>. No page number (auto).

    The chrome pieces are spelled out and concatenated in paint order so
    _body() sits between the title and the sources line, matching the locked
    chrome order. Set the four FILL-IN constants above; build _body() at the
    marker.
    """
    return slide(
        breadcrumb(_SECTION, _TOPIC)
        + prelim_chip()
        + title_placeholder(_TOPIC, _TAKEAWAY)
        + _body()
        + sources_line(_SOURCES)
    )
