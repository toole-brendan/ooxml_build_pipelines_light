# Slide Guide — Distributed-Shipbuilding decks (shared, both programs)

Reference for hand-building body slides: how to build one, the style rules, and
the locked chrome. The body builders (run, paragraph, text_box, table,
connector) are imported from `deck_core.primitives`; recipes and local-helper
patterns (grid, draft_slot, chips, chevrons, callouts, charts) live in
`deck_core/slide_snippets.md`; the deeper raw OOXML mechanics (cell props, chart
data model, custom geometry, relationships) live in
`deck_core/ooxml_cheat_sheet_pptx.md`.

---

## Building a slide

The base template imports the engine (`slide`), the chrome builders, and the
body builders from `deck_core.primitives`, plus the design tokens from
`deck_core.style`. (`cover_layout` / `section_divider_layout` cover the cover +
divider slides.) The chrome is pre-wired in `render()`; you set its text and
build the empty `_body()`. Compose `_body()` from the **imported builders**
(`text_box`, `table`, `connector`, `run`, `paragraph`), from slide-local
`_`-prefixed helpers that wrap them, or from raw OOXML `<p:sp>` /
`<p:graphicFrame>` / `<p:cxnSp>` strings when a primitive does not fit — mix
freely. The imports own the OOXML mechanics (escaping, schema order, insets, the
filled-shape border rule, connector vector normalization); the page design is
yours.

1. Copy `slide_base_template.py` to `deck_{sub,ddg}/slides/<slide_name>.py` — it
   has the locked chrome + palette + BODY pre-written.
2. Write the one-sentence INTENT in the docstring — what this slide is for.
3. Set the breadcrumb / title / sources text, then build `_body()` at the
   BUILD-HERE marker — compose imported builders, slide-local `_`-prefixed
   helper functions, or raw OOXML, and place shapes within `BODY`. (No slide
   number — the layout auto-numbers.)
4. Register the module in `deck_{sub,ddg}/slides/__init__.py`'s `SLIDE_RENDERS`
   list, in slide order. `build()` reads the registry — there's no count to bump.

**Module naming.** Name the module file for its role: `cover_*` for the cover
(slideLayout1), `divider_*` for a section divider (slideLayout2), `appendix_*`
for an appendix slide, and a plain descriptive name for a body slide. Cover and
divider modules skip the base template — they call `cover_layout` /
`section_divider_layout` directly (see **Cover and divider copy**). The filename
is only the registry key; every module keeps its render function named `render`.

**Inspecting.** Geometry truth is auto-generated, never hand-maintained. Read
`deck_{sub,ddg}/reports/slide_probe/<slide_name>.{md,json}` for current geometry
(fills, borders, text, fonts, anchors, insets, tables, chart frames) — parsed
from the emitted XML. Regenerate via `deck_{sub,ddg}/tools/slide_probe.py`.

---

## The body box

Everything between the title and the Sources line is the content area. The
template exposes it as `BODY = (x, y, cx, cy)` (plus `BODY_R` / `BODY_B` for the
right / bottom edges). Place body shapes inside it so every slide stays flush and
clear of the chrome — `text_box(11, "Card", *BODY, ...)`, or index `BODY` for
sub-regions.

- **x 453,079, width 11,282,362** — flush with the breadcrumb and title (right edge 11,735,441).
- **y 1,371,600 (1.5in)** — below a *2-line* title. The title is `noAutofit` Arial 20pt, so a `Topic | Finding` that wraps to a 2nd line overflows the title box; `BODY_Y` clears a real 2-line title with a small gap. Keep findings short enough to stay within 2 lines — a 3-line title collides with the body.
- **bottom 5,870,000** — ~0.07in above the Sources box (top 5,930,000).

To lay out N equal items across the body with even gaps, compute rather than
hand-type coordinates: `item_w = (BODY_CX - (n - 1) * gap) // n`, then item `i`
sits at `BODY_X + i * (item_w + gap)` (same formula vertically with `BODY_CY` /
`BODY_Y`; a ~91,440 EMU / 0.1in gap reads well). The `_grid_x` / `_grid_y`
helpers in `slide_snippets.md` package this.

---

## Style system (every slide, both decks)

Source of truth: `target_copy.txt`. The deck speaks as an analyst stating
conclusions, not a narrator walking through an analysis. One system governs every
visible object — titles, labels, commentary, captions, callouts, notes, charts,
tables, shapes, color, and type. Lead with the point; use layout, hierarchy, fill,
and borders to make the answer easy to read. These are the house defaults, not a
gate: `slide_probe` inspects what you built, it does not police it.

### Structure

- **Commentary** interprets the exhibit; it does not restate it. Active-voice,
  evidence-based readings of what a chart or table means — the trend, the contrast,
  the implication — each point tied to a figure or named specific. The common form
  is a bold finding sentence followed by non-bold, usually bulleted, sentences that
  carry the evidence. The bold lines, read alone, are the takeaways.
- **Titles** — `Topic | Finding.` Topic is a Title Case noun phrase; the Finding
  carries the real claim in full (capitalized at the first word after the pipe,
  sentence case thereafter, ending in a period), long enough to state the
  conclusion, short enough to stay within two lines.
- **Breadcrumbs** (locked chrome) — bold `{Section}` + ` / ` + non-bold
  `{Topic Label}`; the Topic Label is a near, not identical, variant of the title's
  Topic.
- **Section dividers** — the subtitle previews the shape of the answer,
  qualitatively: no hard numbers, no agenda list, no terminal period. State the
  answer where there is one; frame the inquiry where there isn't. If a section has
  no crisp conclusion yet, drop the subtitle rather than force a claim.

### Chart slides

A chart slide pairs a measured exhibit with its reading: the chart carries the
quantitative shape, the commentary states the sizing implication. A units caption
sits above the chart; the commentary lives outside it.

Pick the chart type by the sizing question:
- **Waterfall** — builds or bridges a total from signed parts.
- **Single-series column** — compares levels, rankings, rates, or cadence.
- **Clustered column** — compares values that must not be summed, including nested
  ones (SAM against TAM).
- **Stacked column** — mutually exclusive parts of a total, across periods or
  categories.
- **100% column** — mix when the absolute total is secondary.
- **Marimekko** — size and mix together, where tile area represents value.

Three layout patterns:
- **Pattern A** — chart left, commentary right. Chart ~7.7 in × ~3.7 in; commentary
  in one right-side box ~4.2 in × ~3.4 in, 3–4 finding paragraphs (~100–140 words).
  An optional strip under the chart carries one evidence, anchor, or implication line.
- **Pattern B** — full-width chart (~12.5 in) with commentary below as cards or a
  table (~4.0 in × ~1.2 in each): a bold mini-title and one ~50-word paragraph.
- **Pattern C** — chart left, commentary right *and* below.

Commentary register: a no-fill shape with black text — a bold "parent" finding
sentence, then a few bulleted, non-bold supporting sentences; a blank line; repeat.

### Tables

Tables are structured evidence, not spreadsheet excerpts. Use a table when
row-and-column structure makes exact values, assumptions, definitions, source
comparisons, scenarios, or named records easier to read. Use shapes for cards,
chips, panels, and normal commentary. (If the content has column headers, row
labels, and comparable values across rows or columns, it is a table — use
`house_table()`, or the low-level `table()` for merges, not a grid of `text_box()`
shapes.)

- **Layout** — table-only slides: full-width table under the title (~12.0–12.5 in).
  Table plus commentary follows the chart Patterns A/B/C.
- **Copy** — lead with the analytic point, not the category label; short headers
  with units, dates, and basis in the header; fragments in cells, not paragraphs;
  round consistently in deck notation ($M, $B, %, ~, ranges); order rows and columns
  by logic (size, priority, chronology, build sequence, scenario, implication);
  separate totals, subtotals, and scenario rows visibly.
- **Build** — horizontal rules only; no vertical borders. Default to a ½ pt `GRAY_5`
  rule between body rows, a 1 pt rule under the header, and no rule under the last
  row. Step a body-row rule up to 1 pt black where heavier separation reads better.
  Default to an unfilled header carried by its rule (`house_table` `table_skin="rule"`);
  reserve a dark `BLUE_5` header (`table_skin="dark"`) for the one primary table on a
  page. Keep heavy black borders to one object family per slide. Use ghost rows or
  columns as invisible gutters (merged where needed, near-zero padding, no visible
  border or fill, usually under ~0.1 in). Use color only through the fill rules below
  (column or row headers, thin ghost-column accents, highlighted rows, key cells).
  Size rows to content so grids read even, not ragged — keep in mind how cell font
  size compares to row height. `text_metrics.estimate_row_heights(rows, col_w,
  size_pt=…)` gives honest per-row heights, and `slide_probe --table-fit` reports
  that estimate (informational).
- **Commentary** is optional for simple lookup tables and required when the table
  carries a sizing implication; when present it follows the deck register — a bold
  finding sentence, then non-bold evidence tied to specific rows or figures.

### Color and fills

Color is a hierarchy system, not decoration. Use only the house text colors and the
blue/gray ramps; do not introduce one-off colors.

**Palette**
```
Text (body/exhibit):  BLACK 000000 default · WHITE FFFFFF on dark fills · BLACK 000000 borders + draft-chip text
Blue ramp:  E2E9EF  B6C8D8  6E91B1  3D5972  263746
Gray ramp:  F2F2F2  D9D9D9  BFBFBF  7F7F7F  646464
Draft:      FFFFCC  (draft-yellow only — never a content color)
```
The locked chrome keeps its own `DK 162029` / `BREADCRUMB 44505C` text colors (see
Locked chrome); body and exhibit text is BLACK.

**Fill logic**
- Use fill only when the object carries semantic weight: answer/KPI, denominator,
  evidence chip, method badge, unit caveat, program or row identity, focal warning.
  Fill may ramp in intensity across successive shapes or table headers.
- Keep structural and interpretive text no-fill and usually no-border: commentary,
  legend bullets, method notes, axis labels, captions, row labels, divider labels,
  explanatory bullets.
- Dark fills use white text. Blue flips to white at the third step; gray at the
  darkest. `blue_pair(i)` / `gray_pair(i)` return the correct (fill, text) pair.

**Borders**
- Every shape with any fill carries a 1 pt black border (`text_box` adds it
  automatically; pass `line_width=19_050` to step up). Step to 1.5 pt black for the
  hero, answer, or high-risk caveat block — keep that heavy-border family to one
  object per slide.
- Body draft placeholders use `FFFFCC` with a 1 pt black border. The Preliminary
  chip is locked chrome; do not restyle it here.
- A no-fill shape usually carries no border (bulleted commentary, captions, chart
  and table titles), though a thin rule is allowed as a caption / axis / container.
- Tables follow the same fill logic but with horizontal rules only (see Tables).

**Connectors and dividers** — connector lines are black, solid or dashed, usually
with an arrow at one end; typically ¼–½ pt for flow, leader, and divider lines,
stepping to 1 pt for emphasis (a non-black line is allowed but should be defined in a
legend). A short italic caption beside a connector is encouraged. Divider lines are
allowed, but not excessively.

### Typography

Arial throughout. Size signals hierarchy; bold carries structure or value; italic
marks qualifiers, captions, subtitles, and connector notes. ALL CAPS is explicit
text, used sparingly for caps and headers. The point-size tokens live in
`deck_core.style` (and the `TYPE QUICK REF` in `slide_base_template.py`); prefer the
token names over bare numbers, but use a raw size with a nearby comment when a slide
needs one. Every body-shape `run()` passes `size=` and `font=FONT`; only chrome
inherits.

Core scale: 8 pt sources, footnotes, tiny ticks · 8.5 pt fine print, sublines, unit
notes, chip bodies, qualifiers · 9 pt row/column/bar/segment/map labels · 10 pt
dense body, ledgers, rails, compact callouts, chart titles · 11 pt message strips,
readouts, concise findings · 12 pt default body, with bold/ALL CAPS for caps and
in-shape headers · 13 pt exhibit headers (bold, sparingly) · 14 pt compact numeric
values in bars/chips/KPI cells · 16 pt badges, row identities, gates · 18 pt ribbon
KPIs · 24 pt answer-card KPI · 32 pt the one hero headline.

In-shape hierarchy: cap + subline (12 pt bold/ALL CAPS + 9 pt italic); value +
qualifier (18 pt bold + 8.5 pt italic); label prefix + value (8.5 pt bold + 11 pt);
section + bullets (10 pt bold label + 9 pt bullets); map or flow box (9 pt bold title
+ 8.5 pt body); connector note (8.5 pt italic, no fill, no border).

Chrome sizes (locked by the layout, not part of the scale): content-slide title
`Topic | Finding.` 20 pt; cover and divider title 28 pt, subtitle 20 pt italic;
Preliminary chip 12 pt; sources 8 pt.

### Text mechanics

- No em dashes; en dashes only for number ranges.
- Keep natural and domain slashes (Virginia/Columbia, AP/LLTM, GFE/GFP, FFATA/FSRS,
  castings/forgings); spell `/` out as "and" only where it is a lazy organizational
  separator.
- Avoid `+`, `x`, and `->` as separators — use "and" or restructure — unless inside a
  formula or to show a deliberate flow (not as shorthand for a real sentence).
- Keep `$XXM`, `$XXB`, `~`, `%`, and program acronyms; no double spaces.
- Number hygiene: every figure states currency and magnitude (`$M`, `$B`, `K`) and
  its dollar basis — a real (inflation-adjusted) figure carries a base year (a units
  caption like `$M, real 2025` or `$M, 2025$`), a nominal figure is labeled `nominal`
  (`$M, nominal`); the basis usually rides in the exhibit's units caption. Render an
  explicit zero in a numeric cell as "- -"; round at the half (down below .5, up at or
  above .5).
- No meta, hype, or process talk — don't narrate the deck ("this chart shows", "as we
  can see"), describe what a section does, or reach for hype adjectives ("robust",
  "comprehensive", "deep-dive", "leverage"); show the result.
- No self-reference or role labels in body, commentary, or exhibit text (no
  "Summary:", "(internal)", "this exhibit") — except the dedicated bottom
  Note / Source footnote line, which does carry those labels.
- No build-process leakage — version tags, phase markers, status notes never reach a
  rendered string.

Beyond the above, design the page however reads best.

---


## Cover and divider copy

The cover (`cover_layout`, slideLayout1) and the section dividers
(`section_divider_layout`, slideLayout2) are structural slides — no breadcrumb,
no Sources, and **exempt from the Preliminary chip** (see Locked chrome). Their
*type* is locked by the layout builders and is correct as-is: **title 28pt,
non-italic; subtitle 20pt, italic**. Set the words, not the sizes. The rules
below govern the copy.

### Cover

- **Title** — short, confident noun phrase, Title Case. Names the engagement;
  makes no claim. No verb, no period. Pattern: `<Subject> <Analysis Type>`, ~two
  to four words.
- **Subtitle** — one line, sentence case (rendered italic). States scope and
  time horizon. Pattern: `<population or scope> covered, <time horizon>`.
- **Footer** — date only, formatted `Month YYYY` (e.g. `June 2026`). No fidelity
  word, no author, no separator. Because the cover carries no Preliminary chip,
  it intentionally shows **no draft marker** — keep it clean.

### Section divider

- **Title** — Title Case noun phrase naming the section. No numbering.
- **Subtitle** — the section's governing thought, stated *qualitatively*:
  preview the shape of the answer — not the agenda, not the process — with no
  hard numbers and no terminal period.

The subtitle ladder, worst to best:

| | form | example shape |
|---|---|---|
| ✗ | agenda — lists the topics the section will cover | "Scope, method, results, and caveats" |
| ✗ | process — describes what the section *does* | "How the estimate is built and defended" |
| ✗ | answer, but numeric — states the conclusion with figures | "The reachable market is about $312M" |
| ✓ | answer, qualitative — direction or shape of the conclusion, in words | "Only a narrow, gated subset is realistically reachable" |

Illustrative qualitative subtitles (form only):

- *The total opportunity exceeds what is immediately visible*
- *Only a narrow, gated subset is realistically reachable*
- *Where the estimate is firm, where it is soft, and what would move it*

The third is a *framing* line, not a hard conclusion — right for an
open-question or sensitivity section. State the answer where there is one; frame
the inquiry where there isn't.

**Fallback:** if a section has no crisp conclusion yet, **drop the subtitle**
rather than force a claim. Never fall back to the agenda list.

---

## Locked chrome

`slide_base_template.py` pre-writes these staples — geometry, fonts, and colors
ready to go — with `#` comments saying what each is. Read the OOXML there for the
mechanics; this section just names them and the rules the markup doesn't show.
They're locked project-wide: set their text, but don't move or restyle them.
(Geometry of a built slide: `slide_probe`, see Inspecting. Body builders are not
chrome — they're imported from `deck_core.primitives`; recipes live in
`slide_snippets.md`.)

- **Breadcrumb** and **Title** — locked staples; their wording rules are under Style rules → Text.
- **Sources line** — `Sources: ...; ...; ...`; 2–3 primary sources, semicolon-separated (no parenthetical numbering), no final period. A notes line is labeled "Note" and may be combined with the sources on one line via a pipe (`Note: ... | Sources: ...`); superscript-tie notes to the page (not sources), and hyperlink sources where able.
- **Preliminary chip** — reads "Preliminary"; required on every body slide, exempt only on cover and section-divider slides.
- **Slide number** — auto-provided by the base layout; never build one.

### Draft elements

Anything provisional uses the `FFFFCC` draft-yellow fill so the required
Preliminary chip and optional body draft slots read consistently. The border weight
differs by role: the **Preliminary chip** is locked chrome and keeps its 1.5 pt
black border (do not restyle it); **body draft slots** use a 1 pt black border like
any other filled body shape.

- **Draft slot** — marks where an unbuilt image / chart / table will land (the `_draft_slot` helper in `slide_snippets.md`, or an inline `<p:sp>`): draft-yellow fill, 1 pt black border, italic centered descriptor (e.g. "Chart: metric by scenario"), sized to the slot. (Named to avoid clashing with the OOXML `<p:ph>` *placeholder* element used by the breadcrumb and title.)
