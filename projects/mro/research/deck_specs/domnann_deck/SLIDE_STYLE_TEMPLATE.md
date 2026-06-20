# Slide Style Template - Gold-Standard Reference

Reverse-engineered visual and verbal template deduced from 15 finished
slides (manager-authored) stored in
`deck/slide_style_gold_standard_examples/`, cross-checked against a
second independent review of the same screenshots. Treat this file as
the authoritative style guide for any new slide added to
`DECK_PROPOSED.md` or built into the final deck. When a new reference
slide arrives, update this file first, then propagate the change into
the deck spec.

Terminology rules inherited from `CLAUDE.md`: hyphens (-) and ASCII
arrows (->) only. No em dashes, en dashes, Unicode arrows, or curly
quotes. Straight apostrophes (') throughout.

---

## 1. Source slides this template is drawn from

Fifteen screenshots, grouped by the deck section they appeared in:

**Market Sizing / Coast Guard and other DHS entities** (funding scope):
1. Funding Archetypes - two-archetype comparison table
2. Components - funding inputs / sources / colors-of-money matrix
3. Other DHS maritime funding - CBP / FEMA / S&T addressable table
4. Definitions - Total Funding / TAM / SAM / TCV / ACV bullseye
5. Approach to find TCV - numbered process flow with operators
6. TAM inputs - platform x mission allocation matrix
7. SAM inputs - ASV adoption rate table
8. TCV to ACV Approach - waterfall + exercise-timing table

**Market Analysis / Segment Selection** (commercial maritime):
9. Overview (1/3) - five-photo ship-segment row
10. Overview (3/3) - ten-photo offshore-vessel grid
11. Global fleet overview - 100%-stacked-column + share ovals
12. Offerings - product/service matrix with dashed-outline potentials
13. Near-term Selection Criteria - Yes/No decision tree
14. Evaluation Approach (1/3) - Right-to-Win x Want-to-Win matrix

**Deck navigation**:
15. Agenda - dark-slate section list with current-position highlight

Two additional element-level references supplied by the author as
partial crops: a pointer-callout (speech-bubble style) from the MRO
deck and a row of per-column summary ovals. Both covered under
Section 4 below.

---

## 2. Canvas and page chrome

### 2a. Canvas

- **Background**: off-white or very light gray canvas (not pure
  white) on all **content slides**. Avoids the "bright PowerPoint
  default" feel and lets bounded panels and rule-lines read
  cleanly.
- **Body text color**: dark charcoal (not pure black). Softens the
  page and pairs with the navy / slate palette.
- **Outer margins**: generous. All content sits inside a visible
  alignment grid that hugs the chrome elements on all four edges.

**Framing-slide canvas exceptions** (see §6):

| Framing slide | Canvas | Text |
|---|---|---|
| **Agenda** | Full-bleed dark-slate (~#4A5568) | White |
| **Overview** | Two-tone split-color: left half dark-slate (~#4A5568) / right half off-white | White on the dark half, dark-charcoal on the light half |

These are the only two canvas deviations in the deck. Every other
slide uses the off-white content-slide canvas described above.

### 2b. Page-chrome elements

Every slide has the same hairline elements outside the content area.
They cost almost no space and carry almost all the navigation value.
Content density lives in the middle of the slide; the edges are for
wayfinding.

| Position | Element | Purpose | Observed examples |
|---|---|---|---|
| Top-left | **Breadcrumb** in small gray text, format `Section / Subsection` | Locates the slide in the deck's section tree. Replaces a dedicated section-divider slide. | `Market Sizing / Coast Guard and other DHS entities`, `Market Sizing / funding`, `Market Analysis / Segment Selection`, `Market Analysis / Overview` |
| Top-center or top-right | **Orange "Key discussion page" pill** | Flags the 2-3 slides the audience should actually debate. Everyone else is skimmable. Pill is bold and unmistakable. | `Key discussion page` (orange fill, white text) |
| Top-right | **Institutional seals** (MRO deck) or **author avatar** (other decks) | Institutional branding from day one on the MRO deck (decision 2026-04-19); author-avatar circle reserved for other projects where WIP attribution is wanted. | MRO deck: USN + USCG seals (assets at `deck/MRO_slide_deck_draft_v3/assets/usn-crest.jpg` + `uscg-crest.png`). No DHS seal on this deck. |
| Bottom | **Thin horizontal rule** above the footer line | Visually separates chrome from content without a chunky footer band | Hairline gray rule, full slide width |
| Bottom-left | **`Source:` or `Note:` footer line** | Always present on data slides; small gray italic. `Note:` for caveats and acronym expansions, `Source:` for citations. | `Source: FY26 Congressional Justification books; OBBBA` |

### 2c. What is absent

- No slide numbers
- No running "deck name" bar
- No horizontal divider line below the title (the title bleeds
  directly into the content)
- No chunky colored footer band
- No page-of-pages counter
- No title-of-titles ("Chapter 2: ...") bar

Every pixel outside the content area earns its place by answering
"where am I?", "what is this for?", or "who wrote it?".

---

## 3. Title format (the single most recognizable tell)

Every title is exactly:

```
{Topic} | {full-sentence finding, no ending period}
```

Rules:

- Topic is 1-4 words, Title Case
- The pipe (`|`) is the separator, with single spaces around it
- The right half is a **complete English sentence** stating the
  takeaway - never just a description of what the slide shows
- No ending period
- Straight quotes only; hyphens (-) only; tilde (~) for approximations
- No semicolons in titles. One sentence after the pipe. If the
  assertion will not fit in one clean sentence, pick the stronger
  half or move the second clause into the slide body
- Title is typically large (~28-32pt), **dark charcoal**, and
  left-aligned, hugging the slide's left edge below the breadcrumb

### Sub-patterns

- **Numbered series**: topic gets a `(1/3)`, `(2/3)`, `(3/3)` suffix
  when a single topic spans multiple slides.
  Example: `Overview (1/3) | The commercial maritime market is
  segmented by use case`.
- **Methodology / process slides**: right half names the artifact, not
  a finding.
  Examples: `Definitions | Sizing breaks the market down into five
  levels`, `Approach to find TCV | USV-specified`, `TCV to ACV
  Approach | Finding Company ACV`.
- **Data slides**: right half names a specific number or ranked
  finding.
  Example: `Global fleet overview | Containerships comprise ~6% of the
  total world fleet by number of vessels`.

### Voice

Third-person, often passive:
- "Sizing includes both USV-specified and currently manned capability
  funding..."
- "Funding for CBP, FEMA, and the DHS Science and Technology
  Directorate is potentially addressable"
- "Segments with potential for near-term market entry were determined
  by mission equipment and range requirements"

Avoids "we" except when scoping what the organization could do
("Offerings | We could potentially serve the commercial maritime
market by offering products and services"). Never uses "I".

### Numbers in titles

Specific numbers live in the title when the slide carries a single
hero finding. Approximations use tilde: `~6%`, `~$26M`, `~$812M`.
Fiscal-year ranges use spelled "through": `FY2026 through FY2028`.

### Fiscal-year format - always four-digit

Write fiscal years in the four-digit form (`FY2025`, `FY2026`,
`FY2030`) everywhere in the deck: titles, chart labels, table
headers, `Note:` / `Source:` lines, pointer callouts, footnotes,
and body copy. Two-digit abbreviations (the short form `FY` followed
by a two-digit year, e.g. the twenty-five / twenty-six / twenty-
thirty abbreviations) are not used anywhere on-slide. Applies
across all content slides and framing slides; the rule also applies
to the DECK_PROPOSED.md spec and any deck-adjacent markdown
(revisions notes, session logs that feed into slide copy).

### No judgment adjectives

Neutral descriptors only. `potentially addressable`, not
`compelling`. `the primary architecture to compete in depot`, not
`attractive`. Let the data carry the implication.

### Subtitles

**None.** The right half of the title **is** the subtitle. Explicit
subtitle lines below the title do not appear on any of the 15
reference slides. If a spec has a subtitle, collapse it into the
title's right half or drop it.

### Title examples pulled verbatim

```
Funding Archetypes | Sizing includes both USV-specified and currently
manned capability funding to provide a holistic view of the potential
ASV market

Components | The following funding inputs, sources, and colors of
money are considered for sizing the Coast Guard and other DHS
agencies market

Other DHS maritime funding | Funding for CBP, FEMA, and the DHS
Science and Technology Directorate is potentially addressable

Definitions | Sizing breaks the market down into five levels

Approach to find TCV | USV-specified

TAM inputs | Allocating platforms to missions (cutters and boats,
USCG only)

SAM inputs | ASV adoption is expected to grow from FY26 through FY28

TCV to ACV Approach | Finding Company ACV

Overview (1/3) | The commercial maritime market is segmented by use
case

Overview (3/3) | The "Offshore" subsegment includes wide array of
specialized vessels, largely for the Oil and Gas industry

Global fleet overview | Containerships comprise ~6% of the total
world fleet by number of vessels

Offerings | We could potentially serve the commercial maritime
market by offering products and services

Near-term Selection Criteria | Segments with potential for near-term
market entry were determined by mission equipment and range
requirements

Evaluation Approach (1/3) | Priority segments were determined
through evaluation across "Right to Win" and "Want to Win"
dimensions
```

---

## 4. Visual grammar

Six conventions applied consistently across every content slide.

### 4a. The 4-chip status legend

Anywhere a matrix, tree, process diagram, or chart carries scope
information, the same four status chips appear - usually in the
top-right of the visual, labeled in a small inline legend:

| Chip | Fill | Meaning |
|---|---|---|
| **In scope** | Solid navy (#1F314F or similar dark navy) | Included in sizing / hero / primary focus / selected segment |
| **Adjacent ship-dollar pool** (MRO deck label) | Solid gray (medium, ~50% luminosity) | Adjacent to but outside the MRO scope of the current slide (e.g. PSC 1905 newbuild, 4470 reactor procurement, public-yard labor). Generic label: "out, covered elsewhere / sized in another campaign". |
| **Future effort** | Light-blue fill OR light outline on white | To be assessed in next phase / out-of-current-scope but planned |
| **Non-addressable** | Hatched fill (diagonal lines) | Permanently out / structurally excluded / cannot be served (e.g. nuclear MRO PSCs J044/K044/N044; in-house public-yard NWCF labor) |

**Corollary (this is the key rule)**: every box, cell, and column in
any content visual is colored according to one of these four states.
Absolutely nothing is left uncolored. This is the visual grammar that
ties the whole deck together - a viewer can parse any slide by
cross-referencing the chip colors back to the legend chips at the
top-right.

**Exception - charts with their own inline segment legend**. When
the chart idiom carries its own inline segment legend (Mekko with
an inline work-segment legend, stacked column with a segment
legend, any chart that must legend its own colors), the deck-global
4-chip legend is dropped to avoid two legends competing for the
same top-right real estate. Pick one legend per chart. When the
4-chip legend is dropped, its visual treatments (light-outlined
dashed chip, hatched chip) drop with it - the treatments and the
legend travel together.

### 4b. Secondary palette (non-status markers)

Used for signaling outcomes, not scope:

| Marker | Meaning |
|---|---|
| **Green circle with white check** | Yes / confirmed / meets criterion |
| **Black circle with white X** | No / excluded / fails criterion |
| **Dashed-outline box** | Potential / "to be assessed in next phase" |
| **Navy solid highlight within an otherwise-gray set** | The "one thing the slide is about" (e.g. Containerships column highlighted in Slide 11 while the other 8 fleet columns stay gray) - see chart emphasis rule in 4d |

### 4c. Six repeating visual idioms

Your manager reuses these six shapes over and over. Pick ONE per
slide; don't mix two in the same visual.

#### Idiom 1 - Two-column comparison table

Two column headers in **filled navy/slate bars** (white text). Rows
are attributes of each column: Archetype name / Definition / Explicit
yes-no indicator / Funding examples. Used when contrasting two
mutually exclusive options side-by-side.

Reference: Slide 1 (USV-specified funding vs Currently manned
capability funding).

Best fit for: any "X vs Y" frame where the reader must hold two
options in mind simultaneously.

#### Idiom 2 - Matrix with row-group bars

Left-most column is a dark-gray "row-group header" bar spanning 3-5
rows. Each row within the group has 3-8 cells across. Row-group bars
are stacked vertically down the slide, each one banding its own
rows.

Reference: Slide 2 (Funding Inputs / Sources / Color of Money
row-groups). Slide 12 (Products / Services row-groups). Slide 14
(Right to Win / Want to Win / Market row-groups).

Best fit for: taxonomic decomposition, multi-dimensional scope
breakouts, any slide where 3-4 row-groups each contain 3-5 items.

#### Idiom 3 - Bullseye / concentric circles

Five nested rings labeled Total > TAM > SAM > TCV > ACV (or
equivalent), rendered as flat concentric circles in a gradient from
light blue (outer) to dark navy (inner). Paired with an
adjacent A-E lettered definition table (see Idiom 5).

Reference: Slide 4 (Definitions bullseye).

Best fit for: nested scope funnels, TAM-SAM-SOM structures, anywhere
the narrative is "total pool shrinks to addressable slice to
serviceable slice to company-capturable slice".

#### Idiom 4 - Numbered process flow with operators

Large numbered circles (1-5) down the left margin. Each step is a
horizontal box-chain showing an equation: `Input box (x) Multiplier
box (=) Output box`. Multiplication and equals symbols rendered as
actual math operators between boxes. Sometimes a `+` sign for
summations. Boxes colored per the 4-chip legend.

Reference: Slide 5 (Approach to find TCV - 5 steps each with
operators). Slide 8 (TCV to ACV Approach).

Best fit for: explaining the computation chain of a sizing or
valuation, any place where the reader needs to understand "we
multiplied this by that to get the other thing".

#### Idiom 5 - Lettered A-E pointers

Small filled circles with letters A, B, C, D, E inside, placed as
pointers on a visual (e.g. on each ring of a bullseye, on each step
of a flow, on each cell of a matrix). The same letters then appear
as the leftmost column of an adjacent definition / rationale table,
tying visual to text row-for-row.

Reference: Slide 4 (A-E letters on bullseye rings -> definition
table rows).

Best fit for: any slide where a visual needs a definition layer that
would overwhelm the visual if placed in-line.

#### Idiom 6 - Photo-grid segmentation

Row of 5 (or 2x5 grid of 10) ship / platform photos in a flush grid.
Each photo has a short segment name ABOVE and a one-line
descriptor caption BELOW. One photo in the row can be highlighted
with a dashed outline to flag "the segment this slide zooms into
next".

Reference: Slide 9 (5-photo commercial maritime segments with Other
Ships dashed). Slide 10 (10-photo offshore subsegment grid).

Best fit for: vessel / platform taxonomy slides, segmentation
overviews, "the market breaks down into these N categories" framing.

### 4d. Grid proportions, bounded panels, chart emphasis

**Grid proportions**. The manager's slides consistently use:

- **Left visual**: ~55-60% of slide width, contains the primary
  chart or diagram
- **Right visual**: ~40-45% of slide width, contains the companion
  table, definitions column, or rationale callout
- **Title bar**: ~8% from top, left-aligned, hugging the slide's left
  margin, breadcrumb strip immediately above
- **Source / Note footer**: ~4% from bottom, left-aligned, small
  gray italic, sitting below a hairline separator rule

Exceptions observed:
- Slide 4 (Definitions) uses left-visual ~45% / right-table ~55%
  because the bullseye is compact and the definitions table needs
  width for two-column definitions
- Slide 9 / 10 (photo grids) use full-width single-row or
  two-row layouts with no right-side companion
- Slide 15 (Agenda) is a full-bleed dark-slate slide with no
  content-area split

**Bounded-panel discipline**. Every content module lives inside a
bounded panel - either a thin rule outline or a pale-fill background
rectangle. Nothing floats on the canvas ungrounded. Tables sit
inside a panel that aligns to the slide's grid; callout boxes have
consistent size and position; legends are compact and integrated
into the chart's panel rather than floating off to one side. The
"consulting deck" feel comes from this box discipline more than
from any single typography or color choice.

**Chart emphasis rule - neutral base + one navy hero**. In every
chart where multiple series/bars/columns are shown, all but one are
rendered in neutral slate/gray. Exactly one series, segment, or
endpoint gets the dark-navy emphasis - and that is the element the
slide's title sentence is about.

Reference: Slide 11's 9-column fleet chart - 8 columns rendered gray,
only the Containerships column rendered navy, and the title
sentence is about exactly that column. Slide 8's waterfall -
intermediate bars neutral, start and end anchors navy.

Corollary: if more than one element is emphasized, the slide is
trying to make more than one point - split it into two slides.

**Stack-segment labels - show the metric only, not the segment name**.
In any stacked chart (stacked columns, Mekko, stacked bars) where a
legend already identifies each segment, in-stack labels carry the
metric only (the percent or the dollar value), not the segment
name. The legend carries identification; the label carries the
number. Repeating the segment name inside every stack segment
duplicates the legend and clutters the chart at presentation scale.

### 4e. Annotation layer (callouts + summary ovals)

Two annotation patterns sit on top of charts and matrices. Both are
**used intermittently, not on every slide**. Reserve for slides where
a specific sentence or number needs to attach to a specific visual
element.

#### 4e-i. Callouts - two variants

The manager uses two distinct callout shapes. They are NOT
interchangeable.

**Variant A - `Note:` line (plain, no box)**

- Plain text, small gray italic, sits at the slide bottom
- Lead with the literal prefix `Note:`
- One or two lines max; longer caveats go in a numbered footnote
- Used for acronym expansions, methodology notes, data-source
  caveats, and other "read this if you need to understand the
  small print" content
- No fill, no outline, no pointer

Use for: slide-level caveats that apply to the whole slide and do
not need to attach to a specific chart element.

**Variant B - Pointer callout (speech-bubble shape)**

- Rounded rectangle with a thin black outline
- Pale-gray or pale-blue fill (NOT navy, NOT the 4-chip scope
  legend colors)
- Small pointer tail on one corner attaching the box to a specific
  chart element, cell, or column
- Italic dark-charcoal text inside, one short sentence
- Sits mid-slide beside or beneath the element it annotates

Example text: `"Military Sealift Command (MSC) vessels sit across
Combatant Ships and Auxiliary Ships"` - attached to a specific
column of a vessel-category chart.

Use for: single-element commentary that requires spatial attachment
to a chart feature. If the annotation applies to the whole slide
rather than one element, use Variant A instead.

**Frequency discipline**. Both variants are used intermittently.
Most slides have a `Note:` line at the bottom; a minority of slides
additionally have one pointer callout attached to a chart element.
No slide in the reference set has more than one pointer callout.
Default to zero pointer callouts and add one only when a specific
chart element genuinely needs an inline sentence.

**Prose rules** (apply to both variants plus the footer `Source:`
line):

- **Sentence capitalization**: capitalize the first word
  immediately after `Note:` and `Source:`, just as you would at the
  start of any sentence. Proper nouns (PSC codes, contractor names,
  agency acronyms, hull classes) stay as written regardless of
  position.
- **No math-symbol shorthand in prose**. Write connectives out in
  full words: `=` -> `is` / `equals` / `is defined as`; `+` ->
  `and` / `plus`; `x` or `×` -> `times` / `by`; `~` ->
  `approximately` / `about`; numeric-range `-` (e.g. `$4-6B`) ->
  `$4 billion to $6 billion`; alternation `/` (e.g. `HII / GD`) ->
  `HII or GD`. `%` and `$` remain allowed as standard units.
  Tildes and ASCII arrows remain allowed in titles, chart labels,
  and process-flow step arrows per §3; the rule scopes to
  `Note:` / `Source:` / pointer-callout prose only.
- **Multi-note numbering**. When a slide carries more than one
  note in its bottom `Note:` line, number each note with a
  parenthetical marker and separate the notes with semicolons:
  `Note: (1) first note goes here; (2) second note goes here; (3)
  third note goes here.` Semicolons are allowed between numbered
  items (and inside a numbered item's own prose) - they are the
  only place in `Note:` / `Source:` / pointer-callout prose where
  semicolons are used. A single-note `Note:` line omits the
  numbering.

#### 4e-ii. Summary-stat ovals

Small oval badges positioned above or below a chart's columns,
carrying one summary metric per column.

Form:
- Thin black oval outline
- White fill inside the oval
- Black bold text inside: one number per oval, e.g. `$##M`, `~6%`,
  `n=47`. No highlighter fill behind the text - plain black text on
  white
- Left-margin label in bold italic explaining what the row shows,
  e.g. `Avg. Contract Size:`, `% of fleet:`, `FY2025 Obligation:`

Placement:
- A single row of ovals above or below the chart's columns
- One oval per chart column, horizontally aligned with that column
- Left-margin label outside the leftmost oval

Use for: per-column summary statistics that the reader should read
at a glance (average contract size per segment, percentage of
total per column, count of awards per column). When the chart
already shows raw totals, the oval row should carry a *derived*
metric (average, share, count) rather than repeat the raw total.

Reference: Slide 11 (Global fleet overview) has `% of fleet` ovals
beneath the stacked columns. The MRO deck's chart slides will
typically carry an `Avg. Contract Size` or `Share of TAM` oval row.

**Note on highlighter fill**: earlier versions of this template
described the ovals as carrying a yellow highlighter-style fill
behind the text. That treatment has been removed (2026-04-19);
ovals now render as plain black bold text on white inside a thin
black outline, with no highlighter fill.

#### 4e-iii. Preliminary disclaimer box

Pale-yellow box carrying a single italic sentence flagging that the
content on the slide is work-in-progress or preliminary. Reused
element from the manager's reference Overview slide.

Form:
- Rounded rectangle with a thin black rule outline
- Pale-yellow fill (~#FFF9B0 or similar warm-pale, highlighter-
  adjacent but slightly softer)
- Italic dark-charcoal text inside, centered horizontally,
  ~11-12pt
- Typical two-line content reading something like:
  `Answers shown are preliminary; fidelity and insights will
  increase with further analysis, additional data, and expert
  input`

Placement:
- Default placement is the **bottom-right of the Overview slide**
  (beneath the Objectives column, anchored to the slide's lower-
  right corner)
- Can also appear on any content slide where the slide's data or
  conclusions are explicitly flagged as preliminary; in that case,
  anchor below the right-side table / callout module, not mid-
  canvas
- Width typically matches the containing column width minus small
  inset padding

Frequency: one per slide maximum. Appears by default on the
Overview; optional on other slides with WIP content that needs
explicit flagging. When the deck ships externally, revisit whether
the box still applies - if the content is final, remove the box;
if not, the box travels with the slide.

Reference: Overview slide (Slide 1 in `DECK_PROPOSED.md`).
The MRO deck uses one Preliminary box, on the Overview.

### 4f. Residual / "Other" columns require a composition footnote

Any chart or table with a residual / "Other" column must carry a
footnote enumerating what rolls up into it. Applies to:

- Mekko `Other` column (Slide 5 TAM Composition pattern)
- Stacked-column residual segment
- Pareto / top-N chart with `ranks 11+` aggregated into a single
  residual bar
- Photo-grid residual tile
- Matrix / crosstab row or column labeled `Other`

The reader should not have to guess what's in `Other`. Enumerate
the top 3-5 dollar contributors explicitly; if the residual is
large (greater than $500M or greater than 10% of the chart's
total), raise the threshold to the top 5-7. The footnote can live
as the slide's `Note:` line or as a dedicated one-line
residual-composition caption directly under the chart panel.

---

## 5. Table styling standard

All tables in the deck use an open-rule consulting-table treatment,
not a default PowerPoint grid. This section is the paste-ready
standard; apply it to every table on every slide.

### 5a. Overall form

- Tables sit inside the right-hand support module and align to the
  slide grid
- Default table background is white or very light gray
- Avoid heavy outer borders; tables should feel integrated into the
  slide, not boxed like spreadsheets
- Standard row order: optional super-header band -> column-header
  row -> body rows -> optional subtotal/total row -> optional notes

### 5b. Header treatment

- Use a **navy-filled super-header band** when the table needs a
  grouped title or scoped label above multiple columns (e.g.
  "Potentially addressable CMC funding" spanning three fiscal-year
  columns on the Other DHS maritime funding reference slide)
- Column headers sit on white or very light-gray background in bold
  dark-charcoal text
- Text headers are left-aligned; numeric headers are centered
- Separate the header row from the body with a single medium-weight
  dark rule

### 5c. Gridlines

- **Prefer horizontal rules only**
- **Do not use full vertical gridlines** through the body unless the
  table becomes unreadable without them (the depot prime x RMC
  crosstab on Slide 8 is the explicit exception - see 7b)
- Use thin gray horizontal dividers between rows
- Use a slightly heavier divider between logical row groups
- Use only one closing rule at the bottom of the table

### 5d. Row grouping

Where rows fall into sections, show the section in one of two ways:
- A merged first-column group label (vertical bar spanning the
  group's rows), or
- A pale-gray subheader band above the relevant rows

Do not repeat the same category label on every row unless the table
is otherwise too dense to read.

### 5e. Typography

- Super-header band: bold white text
- Column headers: 12-14 pt bold
- Body text: 11-12 pt regular
- Numeric cells: 11-12 pt semibold
- Subtotal / total rows: bold; italic allowed for the label
- Notes / footnotes under table: 9-10 pt

### 5f. Alignment

- First text column left-aligned
- Long descriptive columns left-aligned
- Short numeric comparison columns centered
- Large dollar figures may be right-aligned, but alignment choice
  must be **consistent within the table**
- Units, rounding, and decimal precision must be uniform by column

### 5g. Fill and color

- **Navy** = super-header bands and highest-importance labels
- **Slate / cool gray** = divider bands, secondary headers, or
  low-emphasis shading
- **Very light gray** = subtotal / total row fill or soft row
  emphasis
- **Light blue** is reserved for separate callout boxes (see 4e-i
  Variant B), not used as routine body-row fill
- **Yellow highlighter** fill is not used anywhere in the deck
  (removed from the summary-ovals convention 2026-04-19; was never
  used inside table cells)
- Avoid multicolor tables; emphasis comes from type weight and rule
  hierarchy, not color variety

### 5h. Emphasis rules

Each table gets **one primary emphasis only**:
- A total row, OR
- A key row, OR
- A key column group

Emphasize with bold text, light-gray fill, or a heavier rule. Do
not highlight multiple cells in different colors. The page-level
implication belongs in the separate pointer callout (4e-i Variant
B), not inside the table.

### 5i. Density

- Keep row count tight enough that body text remains readable at
  presentation scale
- When a table is too dense, collapse it into grouped sections, or
  move detail into notes / appendix
- Tables should summarize and support the chart, not compete with
  it

### 5j. Bottom treatment

End tables with either:
- A bold total row, OR
- A thin closing rule followed by 1-2 lines of note text

Footer sources remain in the slide footer strip (2b), not inside
the table itself, unless the source column is analytically
necessary (e.g. Slide 3 reference has a linked-source column).

### 5k. Shortest version

Navy header band, sparse rules, almost no vertical lines, no heavy
box border, bold total row, emphasis by hierarchy rather than
color.

---

## 6. Framing slides (Agenda + Overview)

The deck uses two framing-slide patterns that break the content-
slide canvas convention (§2a). Both appear at the front of the deck
and orient the reader before the content slides begin. Both omit
the footer source strip and the title-assertion rule (§3).

### 6a. Agenda slide

Full-bleed single-color slide:

- Full-bleed dark-slate background (~#4A5568 or similar)
- Single word "Agenda" in large white serif or sans (~48-60pt),
  top hat
- Below it, a vertical list of section names, each as a
  full-width horizontal bar
- The **current section** is highlighted: darker fill, bold white
  text, small bullet at left
- Non-current sections are light gray fill with standard-weight
  dark text

**Placement decision (MRO deck, 2026-04-19)**: one Agenda slide
placed **immediately after the Overview** at the front of the
deck. Not reinserted between sections. The Overview and Agenda
sit adjacent as the only two framing slides; all remaining slides
are content slides.

#### Agenda text examples (verbatim)

```
Agenda
  Briefing Materials
  Summary and Scorecard          <- current section, highlighted
  Market Segmentation
  Want to Win: Newbuild
  Want to Win: MRO
  Want to Win: USG Funding
  Right to Win: Newbuild
  Right to Win: MRO
  Financial Outlook
```

Breadcrumbs at the top of every content slide then echo the agenda
bar the slide belongs under, providing two-layer wayfinding (agenda
slide between sections + breadcrumb on every page).

### 6b. Overview slide

Two-tone split-color slide placed at the front of the deck, either
before or after the Agenda. Layout:

- **Canvas**: left half dark-slate (~#4A5568), right half off-
  white. The color boundary IS the column divider - no additional
  rule
- **Title**: single word `Overview` (framing exception to the
  `Topic | assertion` rule, matching the Agenda slide convention)
- **Left column - "Context"** (white bold header + thin white
  rule):
  - Two or three top-level bullets
  - Top-level bullets may have indented hyphen sub-bullets where
    enumeration is needed
  - Covers: the business decision(s) this document informs, and
    the data sources / providers feeding the analysis
- **Right column - "Objectives of this document"** (dark-charcoal
  bold header + thin dark-charcoal rule):
  - Single-level dot bullets, no sub-bullets
  - Each bullet starts with an action verb (Size, Decompose,
    Characterize, Map, Reconcile, Extend, Layer, ...)
  - Deferred / later-phase items prefixed with italic
    `(Ongoing effort)` - reference-deck convention for
    deprioritized work
- **Preliminary disclaimer box** (see §4e-iii) anchored to the
  bottom-right of the Objectives column when the slide's content
  is preliminary / WIP

The split mirrors the narrative structure: left = setup (where
we're coming from), right = plan (what this document does). The
Overview answers *why* and *what*; the Agenda answers *where we
are*. The two are complementary, not duplicative - decks with
both place them adjacent at the front.

Breadcrumbs on the Overview slide sit at the top-left on the
dark-slate half, rendered in light-gray.

---

## 7. Compliance checklist for new slides

Before a slide is considered style-compliant, verify:

**Canvas + chrome (content slide)**
- [ ] Off-white canvas, dark-charcoal body text (not pure black)
- [ ] Breadcrumb top-left (`Section / Subsection` format)
- [ ] Orange `Key discussion page` pill IF this is a slide the
      audience should debate; skip otherwise
- [ ] Author avatar OR institutional seals top-right (pick one based
      on WIP vs anchored status)
- [ ] Thin horizontal separator rule above the footer line
- [ ] `Source:` or `Note:` footer line at the bottom, small gray
      italic
- [ ] No slide number, no footer band, no horizontal divider under
      the title

**Canvas + chrome (framing slide - Agenda or Overview, §6)**
- [ ] Canvas exception correctly applied: Agenda = full-bleed
      dark-slate; Overview = two-tone split-color (left dark-slate
      / right off-white)
- [ ] Title is the single word `Agenda` or `Overview` (no
      `Topic | assertion` - framing exception to §3)
- [ ] Breadcrumb present on Overview (Agenda omits per §6a)
- [ ] Footer source strip omitted on framing slides
- [ ] Preliminary disclaimer box (§4e-iii) added on the Overview
      slide IF the content is preliminary / WIP; anchored
      bottom-right of the Objectives column
- [ ] Overview right column uses `(Ongoing effort)` italic prefix
      for deferred bullets

**Title**
- [ ] Title in exact `Topic | full-sentence finding` format, no
      ending period, straight quotes, hyphens only
- [ ] No semicolons in the title; one sentence after the pipe
- [ ] No subtitle line under the title
- [ ] Numbers in the title use tildes (`~6%`) for approximations
- [ ] No judgment adjectives (attractive, compelling, risky)

**Visual grammar**
- [ ] Primary visual on the left (~55-60% width); companion table or
      callout on the right (~40-45%)
- [ ] Visual uses exactly ONE of the six idioms - not a mix
- [ ] 4-chip status legend placed top-right of the visual IF the
      slide carries scope information AND the chart does not already
      carry its own inline segment legend (see §4a exception)
- [ ] Every cell / box / column colored per the 4-chip grammar; no
      uncolored elements (when the 4-chip legend is dropped per
      §4a, its dashed / hatched treatments drop with it)
- [ ] Every module sits inside a bounded panel (rule or pale fill);
      nothing floats ungrounded
- [ ] Charts use neutral slate/gray base with exactly one navy hero
      element that matches what the title sentence is about
- [ ] Stack-segment labels show the metric only (percent or $),
      not the segment name (legend carries identification)
- [ ] Any residual / "Other" column carries a bottom footnote
      enumerating its composition (see §4f)

**Tables**
- [ ] Navy super-header band where grouped columns warrant it
- [ ] Horizontal rules only (vertical gridlines only if genuinely
      unreadable without them - Slide 8 crosstab is the sole
      allowed exception)
- [ ] One primary emphasis per table (total row / key row / key
      column group)
- [ ] Consistent alignment by column; consistent units / rounding
- [ ] No multicolor body cells

**Annotation layer (only where needed)**
- [ ] `Note:` line at bottom for slide-level caveats
- [ ] At most ONE pointer callout (Variant B), only if a specific
      chart element needs inline commentary
- [ ] Summary-stat ovals (plain black bold text on white, thin
      black outline, no highlighter fill) only when a per-column
      derived metric genuinely adds value
- [ ] Preliminary disclaimer box (§4e-iii) only on slides where
      the content is genuinely WIP; one per slide maximum; revisit
      at ship time and remove if content is final
- [ ] `Note:` and `Source:` lines use sentence capitalization
      (first word after the label capitalized)
- [ ] No math-symbol shorthand in `Note:` / `Source:` /
      pointer-callout prose (`=`, `+`, `x`, `~`, numeric-range `-`,
      alternation `/` written out in words)

---

## 8. Mapping to `DECK_PROPOSED.md`

How the current 10-slide spec maps onto the template, with per-slide
deltas. Current titles already follow `Topic | sentence` format
correctly; gaps are primarily in chrome, legend grammar, table
styling, and a few visual-idiom swaps.

### 8a. Global additions (apply to all 10 slides)

1. **Canvas** - set off-white background and dark-charcoal body
   text as the deck default. Not pure white, not pure black.
2. **Breadcrumbs** - add top-left on every slide:
   - Slides 1-3: `Market Sizing / Scope`
   - Slides 4-6: `Market Sizing / Structure`
   - Slides 7-8: `Market Sizing / Competitive Landscape`
   - Slides 9-10: `Methodology / Appendix`
3. **4-chip status legend** - add to the top-right of every chart
   that carries in-scope vs out-of-scope information (Slides 2, 3,
   4, 9, 10 at minimum). Proposed mapping:
   - Navy = in-scope MRO TAM
   - Gray = adjacent FPDS pool (PSC 1905 newbuild, 4470 reactor)
   - Light-outlined = future phase (newbuild-side TAS work)
   - Hatched = non-addressable (public-yard NWCF labor, nuclear
     PSC 1905 bundling)
4. **Key discussion page pill** - orange fill, white text. On the
   MRO deck, used on Slides 5 (Depot Deep Dive) and 8 (Depot
   Primes) - the two the audience should debate. Scope pills are
   not used on this deck (see §9 item 7).
5. **Author avatar** - green circle top-right for WIP; swap to
   Navy + USCG seals when deck ships externally
6. **Retire subtitles** - every current spec slide has a `Subtitle:`
   line; the manager's template has no subtitles. Collapse into
   the right half of the title OR into the scope pill text.
7. **Callout boxes - tighten the discipline**. The current spec uses
   light-blue italic callout boxes on most slides. Under the
   template, callouts are used **intermittently**, in two distinct
   forms:
   - `Note:` line at the slide bottom (plain gray italic) for
     slide-level caveats - keep on every data slide
   - Pointer callout (Variant B, pale fill, pointer tail, italic
     text) - only where a specific chart element needs inline
     commentary, at most one per slide, and only on the 3-4 slides
     where there is genuinely one thing worth attaching that way
   Delete the existing callout boxes that are currently acting as
   a subtitle surrogate or a summary paragraph.
8. **Table styling** - apply Section 5 to every right-side table.
   The biggest visible change: switch from default PowerPoint grids
   to navy super-header band + horizontal rules only + one primary
   emphasis per table.
9. **Chart emphasis** - apply the neutral-base + navy-hero rule
   (4d). In each chart, color all series gray/slate except for the
   one the title sentence names; render that series in navy.
10. **Acts become breadcrumbs**. The current spec labels slide
    groupings as Act I / II / III / Appendix. The manager's
    template has no act labels on-slide; the breadcrumb carries
    that job. Renamed in item 2 above.

### 8b. Per-slide idiom swaps

| # | Current spec visual | Template-aligned swap |
|---|---|---|
| 1 | Two-column text (Context / Objectives) | Reformat as **Agenda slide** (full-bleed dark slate, 10 section-bar list with first section highlighted) OR keep as two-column Context / Objectives but add breadcrumb + `Key discussion page` pill. Agenda version is probably the stronger fit. |
| 2 | Arrow funnel (2,539 -> 65 PSCs -> $7.1B) + Note/Detail table | Keep funnel but render as **Idiom 4 (numbered process flow)** - steps 1-3 with arrows between, each step box colored per 4-chip legend (65 PSCs navy, filtered-out PSCs gray, J044/K044/N044 hatched non-addressable) |
| 3 | Waterfall + 3-section budget-anchor table | Consider leading with **Idiom 3 (bullseye)** - Total $56.6B > Newbuild $38.1B > Public-yard $9.5B > Reactor $1.9B > MRO TAM $7.1B - with **Idiom 5 (A-E pointers)** into the right-side line-item table. Cleaner than a waterfall with de-emphasized starting anchor. Right-side table is a candidate for mini-section bands (OMN / SCN / Nuclear-PSC) since it is a budget-book anchor table. Keep the waterfall as an alternate if the bullseye nesting doesn't hold. |
| 4 | Mekko (vessel x work segment) | Works as-is - Mekko matches Slide 11 (Global fleet overview) idiom. Add 4-chip legend: "Other" vessel column as light-outlined (non-primary focus). Consider adding a summary-stat oval row beneath the columns (e.g. `Avg. Contract Size: $##M`) per 4e-ii. |
| 5 | Mekko (IDV-scope x tier) + entry-structure bullets | Keep Mekko. Replace entry-structure bullets with **Idiom 4 (numbered process flow)**: steps 1-3 MSRA pre-qualification -> MAC-MO IDIQ capture -> Fixed-price task order, each step in a box with an arrow between. **Style the Entry-structure box with the same navy header band and rule weights as the Section 5 table family** so it visually reads as a table-family sibling rather than as a loose bullet list. |
| 6 | Mekko (RMC x tier) + geography table + candidate-site table | Keep Mekko. Merge the two right-side tables into **Idiom 2 (matrix with row-group bars)**: row-group 1 = Active RMCs, row-group 2 = Candidate sites |
| 7 | Pareto + segment-#1/#2/#3 table | Works as-is - Pareto matches Slide 11's highlighted-column idiom. Enforce 4-chip coloring: #1 contractor per segment filled navy, #2/#3 in gray. A pointer callout (4e-i Variant B) attaching HII Mission Technologies 5% OI margin to the HII column is a good candidate use of Variant B. |
| 8 | Pareto + prime-x-RMC crosstab | Works as-is (same convention as Slide 7). Add `Key discussion page` pill - this slide carries the actual competitive-entry argument. **Explicit exception to the 5c no-vertical-rules rule**: the prime x RMC crosstab is the one table in the deck where vertical gridlines are allowed, because the crosstab is hard to scan without them. Still open-rule treatment on horizontal boundaries. |
| 9 | Two stacked columns (appropriations + OPN BA drill) + takeaway column | Works as-is. Formalize 4-chip legend: OMN + OPN navy (Navy-direct), RDT&E-DW slate (Defense-Wide), other agencies light-blue. Replace the right-side takeaway callouts with bottom `Note:` line(s) per the no-callout rule. Right-side table is a candidate for mini-section bands (Navy-direct / Defense-Wide / Other-agency) since it is a budget-book anchor table. |
| 10 | Combination chart (Frame A vs Frame B methods) + apportionment table | Frame the slide as an equation using **Idiom 4 (numbered process flow)** at top: `FY2025 $7.1B Obligations (x) POP apportionment % (=) ~$3.5B FY2025-delivered revenue`. Keep the sensitivity-range combination chart as the primary visual beneath the equation. Matches the manager's `Input (x) Multiplier (=) Output` grammar from Slides 5 and 8 |

### 8c. Title compression passes

Current titles all follow `Topic | sentence` correctly. Two tighten:

- **Slide 1** is 19 words on the right of the pipe; template average
  is ~11-15. Current: `Sizing U.S. Navy and Coast Guard MRO
  contracting activity to support the new shipyard's business-line
  decision`. Try: `Sizing Navy and Coast Guard MRO activity to inform
  the new shipyard's business-line decision`.
- **Slide 3** is 39 words across three semicolon-separated clauses -
  too long. Current: `The $7.1B MRO TAM is the addressable slice of a
  much larger FY2025 Navy and Coast Guard ship-dollar pool; ~$38B
  newbuild, ~$9.5B implied public-yard labor, and ~$1.9B reactor
  product sit adjacent to but outside the MRO scope`. Try: `The $7.1B
  MRO TAM is the addressable slice of a $56.6B FY2025 Navy and Coast
  Guard ship-dollar pool`. Let the chart labels carry the newbuild /
  public-yard / reactor breakdown.

All other 8 titles pass.

### 8d. What to stop doing relative to the template

- Stop writing subtitles under titles (retire the `Subtitle:` line
  from every slide spec)
- Stop using light-blue italic callout boxes on every slide as
  summary-paragraph surrogates. Callouts become intermittent: a
  `Note:` line at the bottom is the default; pointer callouts
  (Variant B) appear only on 3-4 slides where a specific chart
  element genuinely needs inline commentary.
- Stop labeling Acts on-slide (breadcrumbs carry that job)
- Stop leaving boxes/cells uncolored (every visual element must
  map to one of the 4 status chips)
- Stop writing judgment adjectives in titles or callouts
  ("attractive", "compelling", "risky") - the data carries the
  implication
- Stop treating tables as default PowerPoint grids - every table
  gets the Section 5 treatment (navy super-header, horizontal rules
  only, one primary emphasis)
- Stop using multi-color emphasis within a single chart - one navy
  hero element, everything else neutral

---

## 9. Resolved decisions (MRO deck, 2026-04-19)

All open template questions resolved. Decisions baked into the
template above; captured here for posterity.

1. **`Key discussion page` pill meaning** - marks slides the
   AUDIENCE should debate. On the MRO deck: Slides 6 and 9
   (Depot Ship Repair Deep Dive + Prime Landscape - Depot).
2. **Author avatar vs institutional seals** - skip the author
   avatar entirely on the MRO deck; use institutional seals from
   day one. Seal set: USN + USCG only (no DHS). Assets at
   `deck/MRO_slide_deck_draft_v3/assets/usn-crest.jpg` +
   `uscg-crest.png`.
3. **Agenda slide placement** - one Agenda slide, placed
   immediately after the Overview slide at the front of the
   deck. Not reinserted between sections.
4. **4-chip legend gray-chip label** - renamed from "Sized in
   another campaign" to `Adjacent ship-dollar pool` for
   MRO-specific clarity (§4a updated).
5. **Breadcrumb naming** - reflects the workbook's section
   structure: `Market Sizing / Scope`, `Market Sizing /
   Structure`, `Market Sizing / Competitive Landscape`,
   `Methodology / Appendix`. Narrative structure (Orient / Size
   / Compete / Defend) rejected.
6. **Summary-stat ovals** - conservative placement: only where
   a per-column derived metric genuinely adds information. On
   the MRO deck that means Slides 5, 8, 9 (TAM Composition /
   Prime Landscape Total / Prime Landscape Depot). Not applied
   universally. Ovals render as plain black bold text on white
   inside a thin black outline - no highlighter fill behind the
   text (convention changed 2026-04-19).
7. **Scope pills dropped from this deck** - the light-blue scope
   pill convention from the manager's reference deck (§2b) is
   not used on the MRO deck. The breadcrumb and title orient the
   reader; repeating the PSC-filter methodology detail in a pill
   added clutter without adding signal. All mentions of scope
   pills were removed from §2b, §7 checklist, §8a, and
   DECK_PROPOSED.md on 2026-04-19.

Future decks may re-open these questions if their context
differs materially; MRO-specific answers above should not be
treated as universal.
