# DECK_PROPOSED.md - Pending Revisions

Pending edits to `deck/DECK_PROPOSED.md` not yet back-ported into
the spec. When applied, remove the corresponding entry from this
file.

---

## Slide 5 - TAM Composition

### 1. Drop the 4-chip status legend on this slide

The Mekko already carries an inline work-segment legend (Depot /
HM&E / Combat Sys / Electronics / Port & Technical). Adding the
deck-global 4-chip scope legend on top of that is a second legend
competing for the same top-right real estate. Keep the inline
work-segment legend only; drop the 4-chip legend on Slide 5.

Other slides retain the 4-chip legend per `SLIDE_STYLE_TEMPLATE.md`
§4a - this is a Slide 5-only exception driven by the Mekko's own
inline segment legend.

### 2. Change summary-stat ovals from `Avg. Contract Size` to `Depot Ship Repair Size`

Replace the current `Avg. Contract Size:` oval row with one oval per
vessel-category column carrying that column's **Depot Ship Repair $M**
(the navy stack height, pulled out as an explicit dollar number
beneath each column).

- Label (bold italic, left margin): `Depot Ship Repair Size:`
- One oval per vessel-category column, plain black bold `$##M` on
  white inside a thin black outline (no highlighter fill; per
  the 2026-04-19 oval convention change in
  `SLIDE_STYLE_TEMPLATE.md` §4e-ii)
- Values snap from the Services sheet Vessel Type x Work Segment
  crosstab at build time (Depot Ship Repair row, one cell per
  vessel-category column)
- Column sum should reconcile to the $4,781M Depot Ship Repair row
  on the right-side work-segment summary table

Rationale: the title sentence's anchor is "depot drove ~68% of FY2025
MRO TAM." Pulling the depot $ out of each stack into an explicit
oval reinforces that reading at a glance without requiring the
audience to eyeball stack heights.

### 3. Drop the `65 Services PSCs` scope pill

Remove the light-blue scope pill on Slide 5. The breadcrumb
(`Market Sizing / Structure`) and title already orient the reader;
the PSC filter is a methodology detail, not a slice identifier the
audience needs to hold in mind while reading the Mekko.

### 4. No semicolons in the title / lede

Rewrite the current title to remove the semicolon.

Current: `TAM Composition | Depot ship repair drove ~68% of FY2025 MRO
TAM; ~62% of hull spend concentrated on surface combatants,
amphibious warfare ships, and submarines`

Suggested rewrite (pick one or draft another - no semicolons):
- `TAM Composition | Depot ship repair drove ~68% of FY2025 MRO TAM,
  concentrated on surface combatants, amphibious warfare ships, and
  submarines`
- `TAM Composition | Depot ship repair drove ~68% of FY2025 MRO TAM
  with ~62% of hull spend on surface combatants, amphibious warfare
  ships, and submarines`

### 5. Mekko segment labels - percentage only, no segment names

Inside each Mekko column, segment labels should show the percentage
only (e.g. `85%`, `6%`) - NOT the segment name repeated on the
segment (e.g. `Depot 85%`, `HM&E 6%`). The inline work-segment
legend at the top of the chart already identifies which color is
which segment; repeating the name inside every stack segment is
redundant and clutters the columns.

Applies to all six vessel-category columns and all five work-segment
stacks within each column.

### 6. No dashed outline around the "Other" column

Remove the light-outlined / dashed treatment on the `Other` vessel
column in the Mekko. Render it in the same neutral column-outline
treatment as the five named vessel-category columns. Consistent
with revision 1 (no 4-chip legend on this slide) - without the
legend, the dashed outline has no referent.

### 7. Footnote describing what composes "Other"

Add a footnote under the Mekko defining what the `Other` vessel
column contains. Composition snaps from the Services sheet Vessel
Type x Work Segment crosstab at build time (the rows that fall
outside the five named vessel categories), but the footnote should
enumerate the top contributors explicitly so the audience is not
left guessing.

- Format: small gray italic text, one line, placed under the Mekko
  OR folded into the existing `Note:` line at the slide footer
- Draft language (top contributors per the vessel taxonomy; exact
  ranking snaps from the Services sheet Vessel Type rollup at
  build):
  `Note: "Other" ($1,477M, or 21% of TAM) rolls up every vessel
  type outside the five named categories. Top contributors include
  USCG cutters (National Security Cutters, Offshore Patrol Cutters,
  Fast Response Cutters, medium-endurance cutters, icebreakers, and
  buoy tenders) and boats, mine countermeasure ships, expeditionary
  and seabasing ships (EPF, ESB, ESD, and LSM), auxiliary ships
  (research, cargo, and hospital), support craft (yard, barge, and
  tug), combatant craft (patrol, LCAC, LCU, and special warfare),
  unmanned maritime platforms, and unclassified or unmatched PIIDs.`

Before ship, snap the top 3-5 actual $ contributors to `Other` from
the Services sheet Vessel Type x Work Segment crosstab and tighten
the enumeration to the ones that materially move the $1,477M.

### 8. Note and footer prose - proper capitalization, no math-symbol shorthand (deck-wide)

Applies deck-wide; prompted by Slide 5 but enforced on every
`Note:` line, footer `Source:` line, and pointer-callout (Variant B)
body across all 11 slides.

**Capitalization**: capitalize the first word of every sentence,
including the first word immediately after `Note:` and `Source:`.
Proper nouns (PSC codes, contractor names, agency acronyms, hull
classes) stay as written.

**No math-symbol shorthand in prose**. Write the connective out in
full words:

| Current shorthand | Rewrite as |
|---|---|
| `=` (as a connective in prose) | `is`, `equals`, or `is defined as` |
| `+` | `and` or `plus` |
| `x` or `×` | `times` or `by` |
| `~` (inside footnote prose) | `approximately` or `about` |
| Numeric range `$4-6B` | `$4 billion to $6 billion` |
| `/` used as "or" / alternation | `or` |
| `/` used as an enumeration separator in a list | commas with `and` before the final item |

`%` and `$` remain allowed (standard units, not shorthand). Tildes
and ASCII arrows (`->`) remain allowed in titles, chart labels,
step-arrow diagrams, and process-flow connectives per
`SLIDE_STYLE_TEMPLATE.md` §3 and the `CLAUDE.md` workbook-text rule.
The rule above scopes the rewrite to prose only (`Note:`, `Source:`,
pointer callouts).

**Example rewrite - Slide 5 current `Note:`**

Current: `Note: segment detail sums to $7,068M; TAM headline reports
$7,067M ($1M rounding delta). Depot Ship Repair = FPDS PSCs J998 +
J999. Nuclear Propulsion Sustainment PSCs (J044/K044/N044) appear
at ~$0 because reactor work is contracted under shipbuilding codes
at HII Newport News, Fluor Marine Propulsion, and Bechtel (see
Slide 4).`

Rewrite: `Note: Segment detail sums to $7,068M; the TAM headline
reports $7,067M, a $1M rounding delta. Depot Ship Repair is defined
as FPDS PSCs J998 and J999. Nuclear Propulsion Sustainment PSCs
J044, K044, and N044 appear at approximately $0 because reactor
work is contracted under shipbuilding codes at HII Newport News,
Fluor Marine Propulsion, and Bechtel (see Slide 4).`

Apply the same rewrite pass to the `Note:` and `Source:` lines on
Slides 3, 4, 6, 7, 8, 9, 10, and 11, and to the pointer-callout
body text on Slides 4, 5, 7, and 8.
