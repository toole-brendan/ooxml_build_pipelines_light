# Saronic / Port Alpha MRO Entry Due Diligence Deck - PROPOSED

**Status**: proposed redesign, styling-locked against
`deck/SLIDE_STYLE_TEMPLATE.md`. None of these slides have been drawn
yet. `DECK.md` remains the authoritative transcription of the
currently delivered 4-slide deck. This file specifies the target
11-slide redesign (2 framing slides + 9 content slides) with full
styling applied at both the deck-global and per-slide level. When
slides are drawn and screenshots captured, promote the content into
`DECK.md` and delete or archive this file.

## Research context

Saronic (autonomous surface vessel company) is finalizing dimensions
for a prospective new shipyard. Candidate sites under consideration:
a Gulf Coast option (Brownsville, TX) and a California option (site
TBD). Saronic leadership is evaluating whether to add U.S. Navy +
U.S. Coast Guard MRO contracting as a business line for the new
yard. This deck is the evidence-forward market map that supports that
decision.

**Important distribution note**: the internal codename "Port Alpha"
is kept OFF the slides. On-slide language uses neutral descriptors
("new shipyard," "prospective yard," "candidate sites," "Gulf Coast
candidate," "California candidate"). The codename only appears in
speaker notes and verbal discussion, and in this spec file for
internal reference. Sanitize any filename before the deck travels.

## Tone

Evidence-forward and implication-led. The deck is designed to inform
a senior decision, not make it. Each slide should (1) state the
market fact, (2) surface the commercially relevant implication, (3)
stop just short of explicit "should / should not" language. Avoid
judgment-laden adjectives ("attractive / risky / hard") in slide
content; use neutral descriptors and let the data carry the
implication.

This deck frames the decision by laying out the size, structure, and
constraints of the market. The final recommendation sits outside the
deck.

---

## Styling - deck-global defaults

All slides conform to `deck/SLIDE_STYLE_TEMPLATE.md`. That file is
the authoritative style guide; this section summarizes the global
defaults and names the per-slide parameter values used below. All
template open questions were resolved on 2026-04-19 (the MRO deck
also drops the scope pill convention and the highlighter fill on
summary-stat ovals); the resolutions are baked into the values
below.

### Canvas and page chrome (SLIDE_STYLE_TEMPLATE.md §2)

- **Canvas** (content slides): off-white background, dark-charcoal
  body text (not pure black), generous outer margins
- **Canvas** (framing slides, §6): Slide 1 Overview uses two-tone
  split-color (left dark-slate, right off-white); Slide 2 Agenda
  uses full-bleed dark-slate
- **Breadcrumb** top-left on content slides, small gray, format
  `Section / Subsection`. Overview slide carries a breadcrumb; Agenda
  slide omits the breadcrumb (the Agenda IS the wayfinder)
- **Key discussion page pill** orange fill, white text, only on the
  2 slides the audience is expected to debate (Slide 6 Depot Ship
  Repair Deep Dive + Slide 9 Prime Landscape - Depot Ship Repair)
- **Institutional seals** top-right on content slides: USN + USCG
  crests (assets at `deck/MRO_slide_deck_draft_v3/assets/usn-crest.jpg`
  + `uscg-crest.png`). No DHS seal on this deck. Framing slides omit
  the seals. No author-avatar on any slide - seals from day one.
- **Thin horizontal separator rule** above the footer on every
  content slide; framing slides (Overview, Agenda) omit the footer
- **Footer source line** bottom-left on content slides, small gray
  italic, lead with `Source:` or `Note:`

### Title (SLIDE_STYLE_TEMPLATE.md §3)

- Content slides: `{Topic} | {full-sentence finding, no ending
  period}`. Large dark-charcoal text, left-aligned below the
  breadcrumb.
- Framing slides: single topic word (`Overview` or `Agenda`) per §6
  framing exception.
- Straight quotes; hyphens (-) only; tildes (~) for approximations.
- No semicolons in titles; one sentence after the pipe.
- Fiscal years in four-digit form (`FY2025`, `FY2026`, `FY2030`),
  never the two-digit short form. Applies to chart labels, table
  headers, `Note:` / `Source:` lines, and pointer callouts as
  well as titles.
- No subtitles under the title.

### Visual grammar (SLIDE_STYLE_TEMPLATE.md §4)

- Layout: left visual ~55-60% / right module ~40-45%; see per-slide
  exceptions below.
- **4-chip status legend** top-right of every scope-bearing visual:
  - **Navy** = in-scope MRO TAM (the slide's primary focus)
  - **Gray** = `Adjacent ship-dollar pool` (PSC 1905 newbuild, 4470
    reactor procurement, public-yard labor)
  - **Light-outlined** = future phase (newbuild-side TAS work,
    long-tail MRO PIIDs still imputed)
  - **Hatched** = non-addressable (public-yard NWCF in-house labor,
    nuclear MRO PSCs J044/K044/N044)
- **Inline-legend exception**: when a chart carries its own inline
  segment legend (Mekko work-segment legend, stacked-column segment
  legend, any chart that legends its own colors), drop the 4-chip
  legend on that chart to avoid two legends competing for the same
  top-right real estate. The dashed / hatched treatments travel
  with the 4-chip legend - when it is dropped, they drop with it.
  See `SLIDE_STYLE_TEMPLATE.md` §4a exception.
- **Chart emphasis rule**: every chart has exactly one navy hero
  element (the series, bar, or column the title sentence names);
  every other element neutral slate/gray.
- **Stack-segment label rule**: in any stacked chart (Mekko,
  stacked columns, stacked bars) where the legend already names
  each segment, in-stack labels show the metric only (percent or
  dollar value), not the segment name. Legend carries
  identification; label carries the number.
- **Residual column composition**: any chart with an `Other` /
  residual column carries a bottom footnote enumerating its
  composition (top 3-5 $ contributors). See `SLIDE_STYLE_TEMPLATE.md`
  §4f.
- **Bounded-panel discipline**: every content module (chart, table,
  callout) lives inside a bounded panel with a thin rule or pale
  fill; nothing floats on the canvas ungrounded.

### Tables (SLIDE_STYLE_TEMPLATE.md §5)

- Open-rule consulting treatment, NOT a default PowerPoint grid
- Navy-filled super-header band above column headers when a grouped
  scope label is warranted
- Column headers: white / very-light-gray background, bold
  dark-charcoal text
- Horizontal rules only (vertical gridlines prohibited except Slide
  9's prime x RMC crosstab, the explicit exception)
- Thin gray horizontal dividers between rows; slightly heavier
  divider between logical row groups; one closing rule at the
  bottom
- One primary emphasis per table (total row / key row / key column
  group) - via type weight and rule hierarchy, not color variety
- Mini-section bands (pale-gray sub-header bands) allowed on Slides
  4 and 10 (budget-book anchor tables)

### Annotation layer (SLIDE_STYLE_TEMPLATE.md §4e)

- **`Note:` line** at slide bottom for slide-level caveats (plain
  gray italic, no box) - default annotation on every content slide
- **Pointer callout (Variant B)** - pale-fill rounded rectangle
  with pointer tail, italic text - intermittent use only; at most
  one per slide. Used on Slides 4, 5, 7, 8.
- **Summary-stat ovals** - thin black oval outline, plain black
  bold text on white (no highlighter fill), one per chart column,
  with bold italic left-margin label (e.g. `Avg. Contract Size:`).
  Used only where a per-column derived metric genuinely adds
  information: Slides 5, 8, 9.
- **Preliminary disclaimer box** (§4e-iii) - pale-yellow fill, thin
  black outline, italic centered text. Used on Slide 1 Overview
  only.
- **Prose rules** on `Note:` / `Source:` / pointer-callout text:
  sentence capitalization (first word after the label capitalized)
  and no math-symbol shorthand (`=`, `+`, `x`, `~`, numeric-range
  `-`, alternation `/` all written out in words; `%` and `$`
  remain allowed as standard units). See `SLIDE_STYLE_TEMPLATE.md`
  §4e-i "Prose rules".

---

## Deck flow (11 slides: 2 framing + 9 content)

**Front matter** (Slides 1-2, framing)
1. Overview
2. Agenda

**Scope** (Slides 3-4)
3. TAM & Scope
4. Addressable vs Adjacent Spend

**Structure** (Slides 5-7)
5. TAM Composition (Work Segments x Vessel Mix)
6. Depot Ship Repair Deep Dive *(key discussion page)*
7. Geographic Context - Depot Ship Repair

**Competitive Landscape** (Slides 8-9)
8. Prime Landscape - Total MRO
9. Prime Landscape - Depot Ship Repair *(key discussion page)*

**Methodology / Appendix** (Slides 10-11)
10. Appropriation Sourcing
11. TAM Framing

### Visual system summary

| # | Slide | Left idiom | Right module | 4-chip? | Ovals? | Variant B callout? |
|---|-------|----|----|:---:|:---:|:---:|
| 1 | Overview | Two-column split-color text (Context / Objectives of this document) | (shared column space, yellow Preliminary disclaimer box at bottom-right) | - | - | - |
| 2 | Agenda | Full-bleed dark-slate section list | (no right module) | - | - | - |
| 3 | TAM & Scope | Numbered process flow (filter funnel, 3 steps) | Note / Detail table | yes | - | - |
| 4 | Addressable vs Adjacent Spend | Bullseye concentric circles + A-E pointers | Budget-anchor table with 3 mini-section bands | yes | - | yes (SCN bundling) |
| 5 | TAM Composition | Mekko (vessel x work segment) | Work-segment summary table | yes | yes (`Avg. Contract Size`) | yes (submarine in-house) |
| 6 | Depot Ship Repair Deep Dive | Mekko (IDV scope x tier) | Numbered process flow (MSRA -> MAC-MO -> task order), styled as table-family sibling | yes | - | - |
| 7 | Geographic Context - Depot Ship Repair | Mekko (RMC x tier) | Matrix with row-group bars (Active RMCs / Candidate sites) | yes | - | yes (Gulf Coast candidate) |
| 8 | Prime Landscape - Total MRO | Pareto combination (columns + cumulative line) | Segment top-3 table | - | yes (`Avg. Contract Size`) | yes (HII MT margin) |
| 9 | Prime Landscape - Depot Ship Repair | Pareto combination (scoped to depot) + FDNF roster block beneath | Depot prime x RMC crosstab *(vertical rules allowed - exception)* | yes | yes (`Avg. Contract Size`) | - |
| 10 | Appropriation Sourcing | Two stacked columns side-by-side (MRO-PSC by approp + OPN BA drill) | Finding / Implication table | yes | - | - |
| 11 | TAM Framing | Numbered equation flow (top) + combination chart (bottom) | Apportionment table | yes | - | - |

### Chart type counts

- Mekko: 3 (Slides 5, 6, 7)
- Stacked column (or 100% variant): 1 (Slide 10)
- Bullseye concentric circles: 1 (Slide 4)
- Pareto combination / combination chart: 3 (Slides 8, 9, 11)
- Numbered process flow: 3 (Slides 3, 6 RHS, 11 top)
- Full-bleed section list: 1 (Slide 2 Agenda)
- Text layout (no chart): 1 (Slide 1 Overview)

No simple variants. No horizontal bars. No clustered columns. No
butterfly / tornado. No pie.

---

## Slide 1 - Overview

**Breadcrumb**: `Market Sizing / Scope`
**Key discussion page**: no
**Seals**: omitted (framing slide)
**Title**: `Overview` (framing-slide exception to the
`Topic | assertion` rule - just the topic word, matching the
manager's reference Overview + Agenda slides)
**Layout**: two-column split-color text, equal width, no chart, no
right-side table. Framing-slide exception to both the 55/45 split
and the all-off-white canvas rule.
**Footer**: omitted on this slide (framing convention).

### Canvas - split-color treatment (framing exception)

The Overview slide is a **two-tone split-color slide**, not the
deck's default off-white canvas:

- **Left half**: dark-slate fill (`~#4A5568`), white text - matches
  the manager's reference Overview + Agenda slide convention
- **Right half**: off-white fill (deck default), dark-charcoal text
- Edge-to-edge vertical boundary where the colors meet (the color
  change IS the divider; no additional rule needed)

This is the single place in the deck where the canvas convention
departs from all-off-white. The split mirrors the narrative
structure: left = setup (where we're coming from), right = plan
(what this document does).

### Left column - Context

Header: **Context** (large white bold, ~20pt, thin white rule
underneath).

- These materials provide foundational analysis to inform two key
  decisions:
  - The type of defense work to conduct at the new shipyard (Port
    Alpha internal reference)
  - How the Gulf Coast vs California candidate sites sit relative
    to the existing U.S. Navy and U.S. Coast Guard MRO footprint
- Analysis leverages federal contract award data (FPDS Atom Feed),
  Treasury File C appropriation data (USAspending
  `/awards/funding/`), FY2026 President's Budget exhibits (OMN, SCN,
  USCG), SAM.gov entity registration metadata, SEC 10-K filings for
  public-comp benchmarks, and federal procurement research
  publications.

Bullet style: top-level bullets prefixed with a bold white dot;
sub-bullets prefixed with a hyphen (-) and indented one level.

### Right column - Objectives of this document

Header: **Objectives of this document** (large dark-charcoal bold,
~20pt, thin dark-charcoal rule underneath).

- Size the FY2025 U.S. Navy and U.S. Coast Guard MRO contracting
  market (TAM) using FPDS contract obligations
- Decompose TAM by work segment, vessel category, prime contractor,
  Regional Maintenance Center (RMC) geography, and funding
  appropriation
- Characterize the structural entry barriers to the largest segment
  (depot ship repair) and its MSRA -> MAC-MO -> task-order entry
  architecture
- Map the competitive landscape of prime contractors at the
  total-MRO and depot-only levels
- Reconcile the TAM against adjacent ship-dollar pools (newbuild,
  reactor procurement, public-yard labor) that are outside MRO scope
  but potentially relevant context
- *(Ongoing effort)* Extend the TAS-attributed appropriation
  analysis to the newbuild-side PSC universe (SCN-backed HII
  Newport News submarine + carrier programs)
- *(Ongoing effort)* Layer in budget-book projections (30-year
  shipbuilding plan, forward OMN ship-maintenance authority) to
  extend sizing from FY2025 into FY2026-FY2030
- *(Ongoing effort)* Characterize the newbuild-side TAM and
  competitive landscape to the same depth as the MRO side

Bullet style: dark-charcoal dot bullets, single-level only (no
sub-bullets in the Objectives column). `(Ongoing effort)` tag in
italic dark-charcoal at the start of deferred items, mirroring the
manager's reference-deck convention for deprioritized / later-phase
work.

### Preliminary disclaimer box

Sits at the **bottom-right** of the Objectives column, below the
final bullet. Reused element from the manager's reference Overview
slide.

- **Fill**: pale yellow (~#FFF9B0 or similar warm-pale)
- **Outline**: thin black rule
- **Text**: italic dark-charcoal, centered inside the box, ~11-12pt
- **Content**: `Answers shown are preliminary; fidelity and insights
  will increase with further analysis, additional data, and expert
  input`

Box width matches the Objectives column width minus small inset
padding on both sides. Height sized to two lines of italic text plus
~8pt internal padding top and bottom.

### Layout notes

- Two equally-weighted columns, split 50/50, separated by the
  left-half/right-half color boundary (no additional vertical
  divider rule needed - the color change IS the divider)
- Left column headers and body in white; right column headers and
  body in dark-charcoal
- Top-level bullets in the left column may have sub-bullets (hyphen
  prefix, indented) where enumeration is needed; right column is
  single-level only
- `(Ongoing effort)` prefix in italic for deferred right-column
  items
- Breadcrumb present at top-left (on the dark-slate half, rendered
  in light-gray); scope pills / seals / footer all omitted
- The yellow Preliminary disclaimer box is the last element on the
  slide, anchored to the bottom-right corner of the Objectives
  column

---

## Slide 2 - Agenda

**Breadcrumb**: omitted (the Agenda IS the wayfinder)
**Key discussion page**: no
**Seals**: omitted (framing slide)
**Title**: `Agenda` (framing-slide exception - single topic word)
**Layout**: full-bleed dark-slate background, section list centered
vertically on the slide. No chart, no right-side module.
**Footer**: omitted on this slide (framing convention).

### Canvas - full-bleed dark-slate (framing exception)

- **Background**: full-bleed dark-slate fill (`~#4A5568`), no other
  content areas or margins - the dark-slate reaches the slide's
  edges on all four sides
- **Title `Agenda`**: large white text (~48-60pt, sans or serif),
  top-left or top-centered, ~10% from the top edge

### Section list

Vertical list of 4 section bars, each spanning most of the slide
width, stacked with ~8-12pt vertical spacing between bars. Each bar
is ~10-14% of slide height.

The **current section** (Front matter, on this slide) is
highlighted: darker fill, bold white text, small bullet at left.
Remaining sections use light-gray fill with standard-weight
dark-charcoal text.

```
Agenda
  Front matter                   <- current section (highlighted)
    (Overview + Agenda)
  Scope
    (Slides 3-4: TAM & Scope, Addressable vs Adjacent Spend)
  Structure
    (Slides 5-7: TAM Composition, Depot Ship Repair Deep Dive,
     Geographic Context - Depot Ship Repair)
  Competitive Landscape
    (Slides 8-9: Prime Landscape - Total MRO, Prime Landscape -
     Depot Ship Repair)
  Methodology / Appendix
    (Slides 10-11: Appropriation Sourcing, TAM Framing)
```

Section labels sit inside the bar, left-aligned. Parenthetical
slide listings beneath each section label render in smaller text
(~10-11pt) for at-a-glance orientation.

### Layout notes

- No breadcrumb, no scope pill, no seals, no footer - the Agenda
  stands alone as the deck's wayfinding reference
- The first section bar (Front matter) is highlighted as the
  current section because this slide is inside Front matter
- If the Agenda were reinserted between sections (which it is not
  on this deck - the user's decision is one Agenda at the front
  only), each reinserted copy would highlight the new section

### Placement decision (2026-04-19)

One Agenda slide, placed immediately after the Overview. Not
reinserted between sections. Slides 3-11 carry breadcrumbs that
echo the current section name, providing single-layer wayfinding
from here onward.

---

## Slide 3 - TAM & Scope

**Breadcrumb**: `Market Sizing / Scope`
**Key discussion page**: no (orientation slide)
**Seals**: USN + USCG top-right
**Title**: `TAM & Scope | FY2025 Navy and Coast Guard MRO TAM totaled
$7.1B`
**Layout**: left numbered process flow (~55%) + right Note/Detail
table (~45%)

### Left visual - numbered process flow (filter funnel)

**Idiom**: Numbered process flow (§4c Idiom 4), rendered as a
downward funnel with three filter steps and a terminal hero box.

**4-chip legend** (top-right of visual):
- Navy = in-scope (final 65 PSCs)
- Gray = Adjacent ship-dollar pool (other Services PSCs, product
  PSCs)
- Light-outlined = future phase (none on this slide)
- Hatched = non-addressable (J044 / K044 / N044 nuclear MRO PSCs)

**Chart hero**: the terminal $7.1B emphasis box, rendered navy. All
upstream filter stages rendered in progressively darker slate from
light-gray at top to medium slate at the third stage.

**Stages**:

| Step | Stage label (bold) | Subtitle (plain) | Fill |
|-----:|--------------------|------------------|------|
| 1 | 2,539 Active PSCs | Every federal contract-action code category | Light gray |
| - | Filter: USN / USCG only, Services codes only | (arrow) | - |
| 2 | ~1,800 Services-class PSCs | Services-only codes (J, K, N, H, L, M families); products excluded | Medium gray |
| - | Filter: MRO codes only | (arrow) | - |
| 3 | 65 Ship MRO PSCs | Navy + USCG ship repair, modification, overhaul and husbanding codes | Slate |
| - | (no filter, reveal arrow) | -> | - |
| 4 | FY2025 MRO TAM = $7.1B | (hero box - navy-filled) | Navy |

Hatched callout adjacent to Step 3: `J044 / K044 / N044 nuclear MRO
PSCs (non-addressable)` - shows the hatched-fill chip in use.

### Right module - Note / Detail table

**Table styling**: Section 5 open-rule treatment. Navy super-header
band reading `TAM Scope Definitions`. Two columns (Note / Detail),
four body rows, no vertical gridlines, thin horizontal dividers.

| Note | Detail |
|------|--------|
| PSC | A 4-character Product and Service Code assigned by the contracting officer at the buying command to every federal contract action. |
| Awards data vs. budget materials | FPDS obligations capture executed contract-level spend, attributing dollars to vendor, work type, and hull program. Navy and Coast Guard budget exhibits report planned maintenance at the program level, with no contractor attribution and no PSC-level work-type detail. |
| In scope | All U.S. Navy and U.S. Coast Guard vessel types. Work types: depot ship repair, equipment maintenance, modification, installation, QC and inspection, OEM technical representation, and husbanding services. |
| Out of scope | In-house labor at the four public naval shipyards (Portsmouth, Norfolk, Puget Sound, and Pearl Harbor); RCOH and reactor-plant sustainment (bundled under shipbuilding PSCs); newbuild and product procurement. |

### Annotation layer

- **`Note:` line** at bottom: `Note: previous deck transcription
  cited 68 services PSCs; updated to 65 per b1aa621 (nuclear PSCs
  J044 / K044 / N044 removed from the MRO filter; TAM value does
  not change because those three PSCs contained ~$0).`
- **Pointer callout**: none.
- **Summary-stat ovals**: none.

### Footer

`Source: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
Guard, 65 services PSCs, post-exclusions). Data as of April 2026.`

### Supporting workbook sheets

Services, Overview. TAM headline via `NAVY_TAM_SVC` + `CG_TAM_SVC`
defined names.

---

## Slide 4 - Addressable vs Adjacent Spend

**Breadcrumb**: `Market Sizing / Scope`
**Key discussion page**: no (scoping slide)
**Seals**: USN + USCG top-right
**Title**: `Addressable vs Adjacent Spend | The $7.1B MRO TAM is the
addressable slice of a $56.6B FY2025 Navy and Coast Guard ship-dollar
pool`
**Layout**: left bullseye concentric circles (~50%) + right
budget-anchor table with three mini-section bands (~50%). Slight
RHS widening exception to accommodate three row-groups on the
table.

### Left visual - bullseye concentric circles

**Idiom**: Bullseye concentric circles (§4c Idiom 3) paired with
lettered A-E pointers (§4c Idiom 5).

**4-chip legend** (top-right of visual):
- Navy = in-scope MRO TAM (innermost ring)
- Gray = Adjacent ship-dollar pool (newbuild PSC 1905, reactor PSC
  4470, public-yard labor)
- Hatched = non-addressable (nuclear MRO PSCs J044 / K044 / N044)
- Light-outlined = not used on this slide

**Chart hero**: innermost ring (MRO TAM $7.1B) in solid navy. Outer
rings render in a gradient from very-light gray (outermost Total
pool) to slate (reactor) to medium slate (public-yard labor) to
medium-dark gray (newbuild) to navy (MRO TAM).

**Rings, outermost to innermost**:

| Letter | Ring label | $M | Fill |
|:------:|------------|---:|------|
| A | Total FY2025 Navy + USCG ship-dollar pool (computed) | 56,577 | Very light gray |
| B | Less PSC 1905 Newbuild (all platforms) | -38,100 | Medium gray |
| C | Less Implied public-yard labor (OMN 1B4B derivation) | -9,535 | Medium slate |
| D | Less PSC 4470 Nuclear Reactors | -1,875 | Slate |
| E | FY2025 MRO TAM (addressable via private contract) | 7,067 | **Navy (hero)** |

Nuclear MRO PSCs (J044 / K044 / N044) sit as a small hatched wedge
OUTSIDE the bullseye, annotated: `~$0, non-addressable - reactor
work bundles under shipbuilding PSCs`.

Tie-out check: 56,577 - 38,100 - 9,535 - 1,875 = 7,067. Clean.

### Right module - Budget-anchor table with mini-section bands

**Table styling**: Section 5 open-rule treatment with **mini-section
bands** (Section 5d row-grouping rule) - three pale-gray subheader
bands grouping three logical row-groups. Navy super-header band
reading `FY2025 Budget-Book Anchors`. Columns: Line Item / FY2025 $M /
Source (blue hyperlink style).

**Row-group 1 - OMN Ship Maintenance (SAG 1B4B)**

| Line Item | FY2025 $M | Source |
|-----------|--------:|--------|
| Total 1B4B Ship Maintenance | 11,764 | OMN FY2026 PB Justification Vol 1, p. 153 |
| of which Ship Maintenance By Contract (CE 928) | 2,228 | OMN FY2026 PB Justification Vol 1, p. 178 |
| Implied non-contract (public-yard labor + supt.) | 9,535 | Computed (1B4B total minus CE 928) |

**Row-group 2 - SCN Nuclear-Platform Line Items**

| Line Item | FY2025 $M | Source |
|-----------|--------:|--------|
| LI 1045 Columbia Class (construction + CY AP) | 9,581 | SCN FY2026 PB P-40 pp. 31 + 57 |
| LI 2013 Virginia Class (construction + CY AP) | 13,221 | SCN FY2026 PB P-40 pp. 155 + 171 |
| LI 2086 CVN Refueling Overhauls | 1,480 | SCN FY2026 PB P-40 p. 175 |
| LI 2001 Carrier Replacement (CVN-80) | 1,359 | SCN FY2026 PB P-40 p. 73 |
| LI 2004 CVN-81 | 675 | SCN FY2026 PB P-40 p. 117 |
| **SCN nuclear-platform subtotal** | **26,316** | Sum |

**Row-group 3 - Nuclear MRO PSC Emptiness**

| PSC | FY2025 $M | Note |
|-----|--------:|------|
| J044 Nuclear Maintenance | ~0 | Empty - reactor maintenance bundles under shipbuilding PSCs |
| K044 Nuclear Modification | ~0 | Same |
| N044 Nuclear Installation | ~0 | Same |

**Primary emphasis**: the SCN nuclear-platform subtotal row (bold
text, light-gray fill, heavier closing rule), since that row is the
slide's largest reconciliation figure.

### Annotation layer

- **`Note:` line** at bottom: `Note: the $56,577M Total pool is a
  computed aggregate of the four inner rings, not a cited
  budget-book line. Public-yard labor is "implied" from OMN SAG
  1B4B Total minus CE 928 Ship Maintenance By Contract - this
  figure covers all Navy ships, not just nuclear.`
- **Pointer callout (Variant B)**: pale-fill rounded rectangle
  with pointer tail attaching to the SCN row-group band. Italic
  text: `PSC 1905 is not purely newbuild - individual depot events
  on nuclear-platform hulls (e.g. $424M HII USS Boise SSN-764
  Engineered Overhaul) are coded as shipbuilding rather than
  J998/J999. The Slide 3 MRO TAM therefore undercounts private-yard
  sub and carrier depot work that is bundled under the newbuild
  PSC.`
- **Summary-stat ovals**: none.

### Footer

`Sources: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
Guard, Awards master post-exclusions); FY2026 President's Budget
exhibits (OMN Vol 1 SAG 1B4B OP-5, SCN P-1). Data as of April 2026.`

### Supporting workbook sheets

Budget Anchors, Sub & Carrier Coverage. SCN line items, OMN 1B4B
derivation, PSC 1905 / 4470 subtotals.

---

## Slide 5 - TAM Composition

**Breadcrumb**: `Market Sizing / Structure`
**Key discussion page**: no
**Seals**: USN + USCG top-right
**Title**: `TAM Composition | Depot ship repair drove ~68% of FY2025
MRO TAM; ~62% of hull spend concentrated on surface combatants,
amphibious warfare ships, and submarines`
**Layout**: left Mekko (~55%) + right work-segment summary table
(~45%)

### Left visual - Mekko (vessel x work segment)

**Idiom**: Mekko. Column widths proportional to total MRO $ per
vessel category. Segments within each column stacked to 100%,
colored by work segment. Legend inline at top of chart.

**4-chip legend** (top-right of visual):
- Navy = the Depot Ship Repair series (the slide's hero)
- Slate = HM&E, Combat Systems, Electronics, Port & Technical (other
  work segments - neutral)
- Light-outlined = the "Other" vessel column (non-primary focus -
  distinguished from the five named vessel columns)
- Hatched = not used on this slide

**Chart hero**: Depot Ship Repair stack series in solid navy across
all columns. All other work-segment stacks in slate shades.

**Column widths (vessel category $)**:

| Vessel Category | FY2025 $M | Width share |
|-----------------|--------:|------------:|
| Surface Combatants | 2,120 | 30% |
| Amphibious Warfare Ships | 1,440 | 20% |
| Submarines | 838 | 12% |
| Combat Logistics Ships | 770 | 11% |
| Aircraft Carriers | 422 | 6% |
| Other *(light-outlined)* | 1,477 | 21% |
| **Total MRO TAM** | **7,067** | **100%** |

**Stacks within each column (work segment composition)**:

| Vessel Category | Depot | HM&E | Combat Sys | Electronics & C4ISR | Port & Technical |
|-----------------|------:|-----:|-----------:|-------------------:|-----------------:|
| Surface Combatants | 85% | 6% | 6% | 4% | - |
| Amphibious Warfare Ships | 93% | 5% | - | 1% | - |
| Submarines | 53% | 19% | 22% | 5% | 1% |
| Combat Logistics Ships | 83% | 11% | - | - | 5% |
| Aircraft Carriers | 86% | 8% | - | 5% | 1% |
| Other | 40% | 33% | 1% | 14% | 11% |

**Summary-stat oval row** beneath the columns (§4e-ii):
`Avg. Contract Size:` label on left (bold italic), followed by one
oval per column with plain black bold `$##M` average-contract-size
values for each vessel category. Ovals render as thin black outline
on white; no highlighter fill behind the text.

### Right module - Work-segment summary table

**Table styling**: Section 5 open-rule treatment. Navy super-header
band reading `FY2025 MRO Work Segments`. No mini-section bands (single
row-group). Bold total row as the primary emphasis.

| Work Segment | FY2025 $M | % | Coverage |
|--------------|--------:|--:|----------|
| Depot Ship Repair | 4,781 | 68% | Whole-ship availabilities at Pacific / Atlantic RMCs, awarded through MAC-MO IDIQ task orders. |
| Hull, Mechanical & Electrical | 938 | 13% | Propulsion accessories, pumps, valves, piping, HVAC, diesel engines, ship structural systems. |
| Combat Systems Sustainment | 585 | 8% | Weapons, fire control, VLS, guided missiles (including Trident II sustainment on Ohio-class SSBNs), launch / arresting gear. |
| Port & Technical Services | 431 | 6% | QC and inspection, OEM technical representation, husbanding (fuel, transport, port visits), shipyard operations support. |
| Electronics & C4ISR Sustainment | 333 | 5% | Afloat radar, sonar, radio and network systems, navigation, alarms, electrical signal equipment. |
| **Total FY2025 MRO TAM** | **7,068** | **100%** | |

### Annotation layer

- **`Note:` line** at bottom: `Note: segment detail sums to $7,068M;
  TAM headline reports $7,067M ($1M rounding delta). Depot Ship
  Repair = FPDS PSCs J998 + J999. Nuclear Propulsion Sustainment
  PSCs (J044/K044/N044) appear at ~$0 because reactor work is
  contracted under shipbuilding codes at HII Newport News, Fluor
  Marine Propulsion, and Bechtel (see Slide 4).`
- **Pointer callout (Variant B)**: pale-fill rounded rectangle
  with pointer tail attaching to the Submarines column of the
  Mekko. Italic text: `Submarine MRO $ is structurally understated
  - an estimated ~$4-6B of annual nuclear depot work is performed
  in-house at the four public naval shipyards and does not generate
  FPDS contract records; only private-sector OEM and specialty
  work is captured here. See Slide 4 for the full ship-dollar
  reconciliation.`
- **Summary-stat ovals**: `Avg. Contract Size:` row beneath
  columns (see left-visual spec above).

### Footer

`Source: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
Guard, 65 services PSCs, post-exclusions). Data as of April 2026.`

### Supporting workbook sheet

Services. Vessel Type x Work Segment crosstab + Work Segment rollup
totals + coverage definitions.

---

## Slide 6 - Depot Ship Repair Deep Dive

**Breadcrumb**: `Market Sizing / Structure`
**Key discussion page**: **YES** (orange pill top-right) - one of
the two slides the audience is expected to debate
**Seals**: USN + USCG top-right (alongside the Key discussion pill)
**Title**: `Depot Ship Repair Deep Dive | 65% of the $4.9B FY2025
depot segment is full-ship availabilities awarded through a
three-tier MSRA / MAC-MO prime structure`
**Layout**: left Mekko (~55%) + right numbered process flow styled
as table-family sibling (~45%)

### Left visual - Mekko (IDV scope x contractor tier)

**Idiom**: Mekko. Column widths proportional to depot $ per IDV
scope group. Segments within each column (stacked to 100%) colored
by contractor tier.

**4-chip legend** (top-right of visual):
- Navy = Tier 1 CONUS Complex (the slide's hero tier - dominates
  Full-Ship Availability column)
- Slate = Tier 2 Regional (secondary)
- Medium blue = Tier 3 Technical Services (tertiary)
- Light-outlined = Tier 4 FDNF Foreign Yard (future phase / adjacent
  - uncompetable for a CONUS entrant by construction)
- Hatched = not used on this slide
- Gray = Other (unclassified residual)

**Chart hero**: Tier 1 CONUS navy stacks dominate the Full-Ship
Availability column (the slide's focus per the title sentence).

**Column widths (IDV scope group $)**:

| IDV Scope Group | Depot $M | Width share |
|-----------------|---------:|------------:|
| Full-Ship Availability (CNO Avails / DSRAs / DPIAs / LCS Maint) | 3,258 | 65% |
| MSC Availability (ROH / MTA / SIA / CAT A-B) | 551 | 11% |
| FDNF Foreign MSRA (Hanwha + Navantia + Sumitomo + others) | 513 | 10% |
| Other / Support Services | 306 | 6% |
| USCG Cutter Maintenance | 144 | 3% |
| Trade IDIQ (HM&E + Coatings + Insulation + Other Trades) | 123 | 2% |
| Planning & Engineering Support | 108 | 2% |
| **Depot Ship Repair total (pre-FMS gross)** | **5,003** | **100%** |

**Segment tier shades**: Tier 1 navy, Tier 2 slate, Tier 3 medium
blue, Tier 4 light-outlined, Other gray (per 4-chip legend above).

**Denominator note**: Mekko drawn on the $5,003M pre-FMS gross depot
base. Slide title references the $4.9B in-scope figure ($5,003M
gross minus $85M FMS carve-out). Use $4.9B as the rounded in-scope
headline.

### Right module - Numbered process flow (styled as table-family)

**Idiom**: Numbered process flow (§4c Idiom 4), BUT styled per §5
so it reads as a table-family sibling to the deck's other RHS
tables. Navy super-header band reading `Entry structure: MSRA ->
MAC-MO -> task order`. Each step sits inside a bounded panel with
the same thin horizontal rules and pale-gray step-separator bands
as a Section 5 table.

**Steps**:

1. **MSRA pre-qualification**. Master Ship Repair Agreement. Yard
   pre-qualifies on facilities, workforce, safety, and quality
   credentials. MSRA certification is required before bidding on
   any MAC-MO.
2. **MAC-MO IDIQ capture**. Multi-Award Contract, Multiple Order.
   Fixed contractor pool per RMC region (typically ~6-8 primes on
   each coast). Awards run on ~5-year cycles; missing a cycle means
   waiting for the next one.
3. **Fixed-price task orders**. Depot availabilities awarded as
   firm-fixed-price task orders against the MAC-MO pool, priced
   from third-party planner specs (work packages developed
   independently of the primes).

**Closing text under the flow**: `Entry requires qualification at
ALL THREE levels plus a yard footprint aligned with an RMC region.
The depot-specific prime roster and RMC footprint are broken out on
Slide 9.`

### Annotation layer

- **`Note:` line** at bottom: `Note: $4.9B in-scope TAM = $5.0B
  gross J998 / J999 obligations less $85M FMS (Egyptian Navy FOTS
  and other foreign-military-sales) carve-out. Figures on this
  slide exclude FMS unless otherwise noted. Contractor-tier
  definitions: Tier 1 = CONUS complex full-ship MSRA holders;
  Tier 2 = regional yards; Tier 3 = technical services; Tier 4 =
  FDNF foreign yard (Hanwha Ocean, Navantia, Sumitomo, UniThai,
  Mitsubishi, Samsung, Seatrium); Other = unclassified / small.
  IDV scope taxonomy generated via LLM classification of 360 parent
  IDV descriptions + 471 residual no-IDV awards (Claude Opus 4.6).`
- **Pointer callout**: none on this slide (the key-discussion-page
  pill already signals the slide's prominence; an additional
  pointer callout would overcrowd it).
- **Summary-stat ovals**: none (the slide's numeric anchor is the
  $4.9B headline in the title).

**Footnote - Depot $ by vessel category (for reference only, not
shown in main chart)**: Surface Combatants $1,687M (34%), Amphibious
Warfare Ships $1,417M (28%), Combat Logistics & MSC $968M (19%),
Other/Unclassified $450M (9%), Aircraft Carriers $304M (6%), USCG
Cutters $148M (3%), Submarines $9M (0.2%). Submarines appear small
because submarine depot events are coded under PSC 1905 shipbuilding
(see Slide 4).

### Footer

`Source: FPDS FY2025 contract obligations on PSCs J998 + J999 (U.S.
Navy + U.S. Coast Guard), classifier-enriched. Data as of April
2026.`

### Supporting workbook sheets

Depot Ship Repair, J998 J999 Data. IDV Scope Group x Contractor Tier
crosstab, IDV scope group rollup, vessel category rollup (secondary
reference).

---

## Slide 7 - Geographic Context - Depot Ship Repair

**Breadcrumb**: `Market Sizing / Structure`
**Key discussion page**: no
**Seals**: USN + USCG top-right
**Title**: `Geographic Context - Depot Ship Repair | FY2025 depot $
concentrates on the West Coast (SWRMC $1.6B) and East Coast (MARMC
$1.0B), with no established RMC anchor on the Gulf Coast`
**Layout**: left Mekko (~55%) + right matrix with two row-group
bands (~45%)

### Left visual - Mekko (RMC region x contractor tier)

**Idiom**: Mekko. Column widths proportional to depot $ per RMC
region. Segments within each column colored by contractor tier.

**4-chip legend** (top-right of visual):
- Navy = Tier 1 CONUS Complex (the slide's hero tier in the anchor
  columns)
- Slate = Tier 2 Regional
- Medium blue = Tier 3 Technical Services
- Light-outlined = Tier 4 FDNF Foreign Yard (adjacent, uncompetable)
- Gray = Other (unclassified residual)

**Chart hero**: SWRMC column Tier 1 CONUS navy stack (the slide's
title explicitly names SWRMC $1.6B).

**Column widths (RMC $)**:

| RMC Region (Geography) | FY2025 Depot $M | Width share |
|------------------------|-------------:|------------:|
| SWRMC (Pacific / San Diego) | ~1,584 | ~33% |
| MARMC (Atlantic / Norfolk) | ~1,022 | ~21% |
| Other (MSC HQ, NAVSEA HQ, CONUS misc) | ~688 | ~14% |
| SERMC (Atlantic / Mayport) | ~540 | ~11% |
| FDNF (Yokosuka / Naples / Bahrain) | ~510 | ~11% |
| NW RMC (Pacific Northwest) | ~430 | ~9% |
| USCG SFLC | ~148 | ~3% |

**Segment tier cell values** (approximations, snap to live values
at build):

| Tier | SWRMC | MARMC | SERMC | NW RMC | FDNF | USCG SFLC | Other |
|------|------:|------:|------:|-------:|-----:|----------:|------:|
| Tier 1 CONUS Complex | ~1,140 | ~680 | ~350 | ~330 | - | ~95 | ~420 |
| Tier 2 Regional | ~310 | ~200 | ~120 | ~60 | - | ~35 | ~150 |
| Tier 3 Technical Services | ~110 | ~110 | ~50 | ~30 | - | ~15 | ~70 |
| Tier 4 FDNF Foreign Yard | - | - | - | - | ~510 | - | - |
| Other | ~24 | ~32 | ~20 | ~10 | - | ~3 | ~48 |

### Right module - Matrix with row-group bars

**Idiom**: Matrix with row-group bars (§4c Idiom 2). Two row-groups
stacked vertically: Active RMCs (7 rows) and Candidate sites (2
rows). Row-group labels in filled dark-gray bars on the left.

**Table styling**: Section 5 open-rule. Navy super-header band
reading `RMC Footprint and Candidate Sites`.

**Row-group 1 - Active RMCs**

| RMC Region | Geography | Tier-1 Primes in Region | Major Fleet Homeports |
|-----------|-----------|-------------------------|-----------------------|
| SWRMC | San Diego, CA | BAE San Diego; GD NASSCO; HII Continental Maritime + MHI | San Diego (largest Pacific Fleet concentration) |
| MARMC | Norfolk, VA | BAE Norfolk; HII Metro Machine + MHI | Norfolk (largest Atlantic Fleet concentration) |
| SERMC | Mayport, FL + Charleston, SC | Detyens; NASSCO Mayport; BAE Jacksonville | Mayport; Kings Bay (SSBN base); Charleston (CG homeport) |
| NW RMC | Bremerton / Everett, WA + Portland, OR | Vigor Seattle + Portland | Bremerton; Everett (Pacific Fleet North) |
| FDNF | Yokosuka JP + Naples IT + Bahrain | Hanwha Ocean (KR); Navantia (ES); Sumitomo / Mitsubishi / UniThai | Forward-deployed squadrons |
| USCG SFLC | Baltimore, MD (HQ); regional product lines | None (USCG work distributed across Tier-2/3) | USCG homeports nationwide |
| Other | Multi-location | N/A | N/A |

**Row-group 2 - Candidate Sites** *(pale-gray subheader band
separating from row-group 1)*

| Candidate Site | Geography | Nearest Active RMC | Approx Distance |
|---------------|-----------|--------------------|-----------------|
| Gulf Coast candidate (Brownsville, TX) | Gulf of Mexico, south Texas | SERMC (Mayport) | ~1,100 nm |
| California candidate (site TBD) | West Coast | SWRMC (San Diego) or NW RMC (WA) | 0-1,000 nm depending on specific site |

### Annotation layer

- **`Note:` line** at bottom: `Note: RMC $ and tier composition
  approximations snap to live values from the Depot Ship Repair
  workbook sheet RMC x Tier crosstab (J998 / J999 only, FY2025
  post-FMS). Non-depot Services MRO $ ($2.3B across HM&E / Combat
  Systems / Electronics / Port & Technical) is not allocated to
  RMCs on this slide because those segments are not organized
  around the RMC structure. FDNF = Forward Deployed Naval Forces;
  Tier 4 is 100% of FDNF $ by construction. Distance from
  Brownsville, TX to Mayport, FL is approximately 1,100 nautical
  miles.`
- **Pointer callout (Variant B)**: pale-fill rounded rectangle with
  pointer tail attaching to the Gulf Coast candidate row in
  row-group 2. Italic text: `The Gulf Coast candidate does not sit
  within an established RMC footprint. The California candidate
  would sit within or adjacent to SWRMC ($1.6B annual depot pool)
  or NW RMC ($430M) depending on specific site. Slide 9 decomposes
  RMC $ by prime contractor.`
- **Summary-stat ovals**: none (RMC $ values already embedded in
  column headers).

### Footer

`Source: FPDS FY2025 contract obligations on PSCs J998 + J999 (U.S.
Navy + U.S. Coast Guard), classifier-enriched with RMC geography
tags. Data as of April 2026.`

### Supporting workbook sheet

Depot Ship Repair. RMC x Tier crosstab, RMC Geography column.

---

## Slide 8 - Prime Landscape - Total MRO

**Breadcrumb**: `Market Sizing / Competitive Landscape`
**Key discussion page**: no
**Seals**: USN + USCG top-right
**Title**: `Prime Landscape - Total MRO | BAE, General Dynamics, and
HII collectively captured ~36% of the FY2025 MRO TAM; the top 10
primes captured ~57%`
**Layout**: left Pareto combination chart (~60%) + right segment
top-3 table (~40%)

### Left visual - Pareto combination chart

**Idiom**: Combination chart (columns + cumulative line).

Primary axis (left): FY2025 $M, 0 to 1,100.
Secondary axis (right): Cumulative % of FY2025 MRO TAM, 0 to 100%.

Vertical columns ranked left-to-right by descending FY2025 $M. Cumulative
line (navy) traces the cumulative percentage-of-TAM across the top of
the columns.

**4-chip legend** (top-right of visual):
- Navy = top 3 primes (BAE, GD, HII - the slide's hero trio)
- Slate = ranks 4-10 (secondary)
- Gray = Adjacent ship-dollar pool (ranks 11+ aggregated into a
  residual, not visualized individually)
- Hatched = not used on this slide

**Chart hero**: the top-3 columns (BAE, GD, HII) in solid navy;
ranks 4-10 in neutral slate. The cumulative line renders navy
throughout, with text labels anchoring at `Top 3 = 36%` and
`Top 10 = 57%`.

| Rank | Contractor | FY2025 $M | Cumulative $M | Cumulative % of TAM |
|-----:|------------|--------:|--------------:|--------------------:|
| 1 | BAE | 1,073 | 1,073 | 15.2% |
| 2 | GD | 939 | 2,012 | 28.5% |
| 3 | HII | 516 | 2,528 | 35.8% |
| 4 | Vigor | 440 | 2,968 | 42.0% |
| 5 | Draper | 318 | 3,286 | 46.5% |
| 6 | Detyens | 225 | 3,511 | 49.7% |
| 7 | Epsilon | 149 | 3,660 | 51.8% |
| 8 | East Coast Repair | 142 | 3,802 | 53.8% |
| 9 | Lockheed | 132 | 3,934 | 55.7% |
| 10 | S.C.A. | 112 | 4,046 | 57.3% |

**Summary-stat oval row** beneath the columns (§4e-ii):
`Avg. Contract Size:` label on left (bold italic), followed by one
oval per contractor with plain black bold `$##M` values. Ovals
render as thin black outline on white; no highlighter fill behind
the text.

### Right module - Segment top-3 table

**Table styling**: Section 5 open-rule. Navy super-header band
reading `FY2025 Top 3 Primes by Work Segment`. No mini-section bands.
Primary emphasis via bolding the #1 cell in each row.

| Work Segment | #1 | #2 | #3 |
|--------------|----|----|-----|
| Depot Ship Repair | **BAE - 22%** | GD - 18% | HII - 10% |
| Hull, Mechanical & Electrical (HM&E) | **Global PCCI - 7%** | Oceaneering - 6% | HII - 6% |
| Combat Systems Sustainment | **Draper - 54%** | Lockheed - 22% | Leidos - 10% |
| Electronics & C4ISR Sustainment | **Amentum - 15%** | L3 - 15% | SAIC - 15% |
| Port & Technical Services | **S.C.A. - 26%** | Waypoint - 9% | Fairlead - 6% |

### Annotation layer

- **`Note:` line** at bottom: `Note: "Obligations" (not "revenue"
  or "sales") chosen deliberately for consistency with Slide 11's
  Frame A vs Frame B distinction. Top-10 sum of $4,046M / $7,067M
  = 57.25%. BAE includes San Diego, Norfolk, and Jacksonville ship
  repair operations; GD includes NASSCO, Electric Boat,
  Continental Maritime, and Mission Systems; HII includes Newport
  News, Ingalls, Metro Machine, and Marine Hydraulics
  International.`
- **Pointer callout (Variant B)**: pale-fill rounded rectangle
  with pointer tail attaching to the HII column of the Pareto.
  Italic text: `HII Mission Technologies posted a ~5.0% OI margin
  in 2025 ($3.0B revenue / $153M OI). At ~91% service revenue mix,
  it is the cleanest pure-services proxy in public comps. Slide 9
  drills into the depot-only prime concentration and per-RMC
  footprint.`
- **Summary-stat ovals**: `Avg. Contract Size:` row beneath Pareto
  columns (see left-visual spec above).

### Footer

`Sources: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
Guard, 65 services PSCs, post-exclusions); SEC 10-K filings (HII,
GD, BWXT), FY2025. Data as of April 2026.`

### Supporting workbook sheets

Services, Public Comps. Top contractors + #1/#2/#3 per segment; HII
Mission Technologies margin.

---

## Slide 9 - Prime Landscape - Depot Ship Repair

**Breadcrumb**: `Market Sizing / Competitive Landscape`
**Key discussion page**: **YES** (orange pill top-right) - second
of the two slides the audience is expected to debate
**Seals**: USN + USCG top-right (alongside the Key discussion pill)
**Title**: `Prime Landscape - Depot Ship Repair | BAE, General
Dynamics, and HII held ~50% of the $4.9B FY2025 depot segment; the top
10 depot primes held ~75%`
**Layout**: left column split vertically into Pareto (~70% of
left height) + FDNF roster block (~30% of left height); right
depot prime x RMC crosstab (~45% width). Overall: ~55% left /
~45% right.

### Left-top visual - Pareto combination chart (depot-scoped)

**Idiom**: Combination chart (columns + cumulative line). Same format
as Slide 8 by intent - same chart type, different denominator
($4,923M in-scope depot).

Primary axis (left): FY2025 depot $M, 0 to 1,200.
Secondary axis (right): Cumulative % of in-scope depot, 0 to 100%.

**4-chip legend** (top-right of visual):
- Navy = top 3 depot primes (BAE, GD, HII)
- Slate = ranks 4-10 CONUS primes
- Light-outlined = FDNF yards (shown separately in the roster
  block below - uncompetable for a CONUS entrant by construction)
- Hatched = not used on this slide

**Chart hero**: top-3 columns (BAE, GD, HII) in solid navy;
cumulative line (navy) with labels at `Top 3 = 50%` and
`Top 10 = 75%`.

| Rank | Contractor | FY2025 Depot $M | Cumulative $M | Cumulative % of Depot |
|-----:|------------|--------------:|--------------:|----------------------:|
| 1 | BAE | 1,073 | 1,073 | 21.8% |
| 2 | GD (NASSCO + Continental Maritime) | ~886 | 1,959 | 39.8% |
| 3 | HII (Continental Maritime + Metro Machine + MHI) | ~492 | 2,451 | 49.8% |
| 4 | Vigor | 440 | 2,891 | 58.7% |
| 5 | Detyens | 225 | 3,116 | 63.3% |
| 6 | East Coast Repair & Fabrication LLC | ~85 | 3,201 | 65.0% |
| 7 | Epsilon Systems Solutions Inc. | ~149 | 3,350 | 68.0% |
| 8 | Pacific Shipyards International LLC | ~100 | 3,450 | 70.0% |
| 9 | Colonna's Ship Yard Incorporated | ~95 | 3,545 | 72.0% |
| 10 | Amentum Services Inc. | ~90 | 3,635 | 73.8% |

Note: ranks 6-10 are Python-ranked from the workbook's
consolidated-parent rollup per Session
`2026-04-19_iii_deck_data_slide_reflow.md`. The FDNF yards
(Hanwha, Navantia, Sumitomo et al.) that appeared in earlier
placeholder drafts now live in the dedicated FDNF roster block
below rather than competing against CONUS Tier-2 primes in the
Pareto top-10.

**Summary-stat oval row** beneath the columns (§4e-ii):
`Avg. Contract Size:` label on left (bold italic), followed by one
oval per contractor with plain black bold `$##M` values. Ovals
render as thin black outline on white; no highlighter fill behind
the text.

### Left-bottom block - FDNF roster

Small supplementary table sitting beneath the Pareto on the left
panel, styled per Section 5 open-rule treatment. Navy super-header
band reading `FDNF Foreign MSRA Yards (~$510M FY2025, uncompetable)`.
Light-outlined chip applied to all rows to reinforce the
out-of-CONUS-scope classification.

| Rank (within FDNF) | Yard | Country | Approx FY2025 Depot $M |
|-------------------:|------|---------|---------------------:|
| 1 | Hanwha Ocean | Korea | ~200 |
| 2 | Navantia | Spain | ~130 |
| 3 | Sumitomo Heavy Industries | Japan | ~80 |
| 4 | UniThai | Thailand | ~45 |
| 5 | Mitsubishi Heavy Industries | Japan | ~30 |
| 6 | Samsung Heavy Industries | Korea | ~15 |
| 7 | Seatrium | Singapore | ~10 |
| **FDNF subtotal** | | | **~510** |

**Purpose**: recover the FDNF narrative that the live CONUS-ranked
Pareto buries. FDNF yards collectively hold ~$510M / ~10% of
depot $ via forward-deployed MSRA task orders, but none compete
against CONUS entrants. The roster makes the FDNF scope visible
without polluting the CONUS Pareto ranking.

**Primary emphasis**: bold FDNF subtotal row with heavier closing
rule. Individual rank rows use standard table weight.

### Right module - Depot prime x RMC crosstab

**Table styling**: Section 5 open-rule **WITH THE §5c EXCEPTION
ACTIVATED** - vertical gridlines are allowed on this table because
the prime x RMC crosstab becomes unreadable without them. Still
open-rule treatment on horizontal boundaries: navy super-header
band reading `FY2025 Depot Obligations - Prime x RMC ($M)`; thin
horizontal dividers; one primary-emphasis row (Top 10 subtotal,
bolded with pale-gray fill); bold closing rule at bottom.

Vertical gridlines: thin gray, full column-height, distinguishing
each of the 7 RMC columns from each other.

| Depot Prime | SWRMC | MARMC | SERMC | NW RMC | FDNF | Other | Total |
|-------------|------:|------:|------:|-------:|-----:|------:|------:|
| BAE | ~300 | ~550 | ~220 | - | - | ~3 | ~1,073 |
| GD | ~886 | - | - | - | - | - | ~886 |
| HII | ~280 | ~210 | - | - | - | ~2 | ~492 |
| Vigor | - | - | - | ~440 | - | - | ~440 |
| Detyens | - | - | ~225 | - | - | - | ~225 |
| East Coast Repair | - | ~85 | - | - | - | - | ~85 |
| Epsilon Systems | mixed | mixed | mixed | - | - | mixed | ~149 |
| Pacific Shipyards | - | - | - | ~100 | - | - | ~100 |
| Colonna's Ship Yard | - | ~95 | - | - | - | - | ~95 |
| Amentum Services | mixed | mixed | mixed | mixed | - | mixed | ~90 |
| **Top 10 CONUS subtotal** | **~1,466** | **~940** | **~445** | **~540** | **-** | **~5** | **~3,635** |
| FDNF yards (see roster block) | - | - | - | - | ~510 | - | ~510 |
| RMC total (all primes) | ~1,584 | ~1,022 | ~540 | ~430 | ~510 | ~837 | ~4,923 |

Exact per-cell $ figures snap from the Depot Ship Repair sheet
prime x RMC crosstab at build time. Single-RMC primes (Vigor,
Detyens, Pacific Shipyards, Colonna's) are exact; multi-RMC primes
(BAE, HII, Epsilon, Amentum) are approximated from yard-level
task-order rollups.

### Annotation layer

- **`Note:` line** at bottom: `Note: BAE / GD / HII depot totals
  derived from Slide 8 segment top-3 depot shares (22% / 18% / 10%)
  applied to the $4,923M in-scope depot denominator. "Top 10 CONUS
  subtotal" row values may drift off RMC totals due to multi-RMC
  approximation at the BAE / HII / Epsilon / Amentum cell level;
  exact values reconcile when snapped from the workbook at build
  time. "Other" RMC column captures MSC HQ, NAVSEA HQ, CONUS
  miscellaneous, and the USCG SFLC bucket (~$148M). FDNF row on the
  crosstab reconciles to the FDNF roster block on the left panel.`
- **Pointer callout**: none (the key-discussion-page pill already
  signals the slide's prominence).
- **Summary-stat ovals**: `Avg. Contract Size:` row beneath Pareto
  columns (see left-top visual spec above).

### Footer

`Source: FPDS FY2025 contract obligations on PSCs J998 + J999 (U.S.
Navy + U.S. Coast Guard), classifier-enriched with RMC geography
tags. Data as of April 2026.`

### Supporting workbook sheets

Depot Ship Repair, Awards. Depot prime Pareto top-10 (PSC
J998/J999-only contractor rollup) + Depot prime x RMC crosstab +
FDNF roster (foreign-yard filter on Corporate Parent).

---

## Slide 10 - Appropriation Sourcing (Appendix)

**Breadcrumb**: `Methodology / Appendix`
**Key discussion page**: no
**Seals**: USN + USCG top-right
**Title**: `Appropriation Sourcing | The $7.4B FY2025 MRO-PSC
universe is funded across ~10 federal appropriations; OMN and OPN
each carry ~35-37%, with Defense-Wide RDT&E a surprising 11%`
**Layout**: left two stacked columns side-by-side (~55%) + right
Finding / Implication table (~45%)

### Left visual - two stacked columns side-by-side

**Idiom**: 100%-stacked columns, two columns side-by-side. Column 2
visually ties to Column 1's OPN segment via a connecting bracket at
the same y-height.

**4-chip legend** (top-right of visual):
- Navy = Navy-direct (OMN, OPN, Navy-other = 76% of MRO-PSC universe)
- Slate = Defense-Wide (RDT&E-DW + DW-other = 15%)
- Light blue = other agencies (USCG, AF, Army, SCN, memo = 9%)
- Hatched = not used on this slide

**Chart hero**: OMN segment of Column 1 (navy), since OMN is the
plurality appropriation and the title sentence's anchor.

**Column 1 - MRO-PSC universe by appropriation**:

| Appropriation | FY2025 $M | % of TAS Total |
|---------------|--------:|---------------:|
| OMN (Operation & Maintenance, Navy) | 2,761 | 37.3% |
| OPN (Other Procurement, Navy) | 2,588 | 35.0% |
| RDT&E, Defense-Wide | 780 | 10.5% |
| USCG (OE + AC&I + other) | 320 | 4.3% |
| Defense-Wide other (Proc-DW + O&M-DW) | 307 | 4.2% |
| Navy other (APN + WPN + other) | 295 | 4.0% |
| Air Force (OMAF + other) | 165 | 2.2% |
| Army (OMA + other) | 131 | 1.8% |
| SCN + other agency (memo) | 53 | 0.7% |
| **TAS Total** | **7,400** | **100%** |

**Column 2 - OPN drill by Budget Activity**:

| OPN Budget Activity | FY2025 $M | % of OPN |
|---------------------|--------:|---------:|
| BA-7 Personnel & Command Support Equip | 1,591 | 61.5% |
| BA-8 Spares & Repair Parts | 825 | 31.9% |
| Other BAs (BA-1 + Undistributed) | 171 | 6.6% |
| **OPN Total (= Column 1's OPN row)** | **2,588** | **100%** |

### Right module - Finding / Implication table

**Table styling**: Section 5 open-rule. Navy super-header band
reading `Takeaways`. Two-column table with bold Finding column and
regular Implication column. One row per takeaway. No mini-section
bands.

| Finding | Implication |
|---------|-------------|
| **OMN + OPN = 72% of MRO $** | Navy sustainment drives the market; the appropriation story is a Navy story, not a DoD-wide one. |
| **OPN splits 62% Command Support Equip / 32% Spares** | BA-7 funds installation / modernization electronics + C4ISR + combat system integration. BA-8 is spares and consumable parts. Depot availabilities (DSRAs, DPIAs, CNO avails) are funded through BA-7, not through OMN CE 928 contract maintenance. |
| **RDT&E Defense-Wide = $780M (11%)** | Almost entirely Trident II / SSP / SMDC sustainment on J-series PSCs. Draper MK7 Trident ($318M FY2025) is the single-largest MRO PIID. |
| **SCN on MRO PSCs = $40M** | De minimis. Nuclear-platform MRO bundles under PSC 1905 shipbuilding, not onto MRO PSCs - see Slide 4 for the full scope reconciliation. |

### Annotation layer

- **`Note:` line** at bottom: `Note: 49% of FY2025 MRO $ directly
  TAS-attributed from Treasury File C submissions (USAspending
  /api/v2/awards/funding/); 51% imputed via per-PSC-bucket
  appropriation ratios from the directly-classified peer sample.
  The $7,400M TAS Total is the pre-exclusion MRO-PSC universe
  (v2.79 workbook post-outlay-fallback rebuild), ~$333M larger
  than the $7,067M Services TAM (Slide 3) which applies
  shore-base and FMS exclusions. Account-level detail for the ~30
  individual Treasury accounts that aggregate into these 9 buckets
  lives on the Budget Anchors workbook sheet and in
  data_pull/output/usaspending/approp_rollup_imputed.json.
  Reconciling FPDS FY2025 MRO $ to OMN cost-element 928 Ship
  Maintenance By Contract ($2.4B across BA-1 Ship Operations)
  alone leaves a naive $4.7B gap; the gap disappears once OPN,
  RDT&E-DW, USCG, and the other appropriation colors are included.`
- **Pointer callout**: none.
- **Summary-stat ovals**: none.

### Footer

`Source: USAspending /api/v2/awards/funding/ joined to FPDS FY2025
contract obligations (U.S. Navy + U.S. Coast Guard, 65 services
PSCs). Treasury File C DAIMS coverage lags FPDS by ~1 quarter for
the smallest-$ tail. Data as of April 2026.`

### Supporting workbook sheet

Budget Anchors. `MRO_TAS_*` named cells (10 appropriation rows + 3
OPN BA sub-rows).

---

## Slide 11 - TAM Framing (Appendix)

**Breadcrumb**: `Methodology / Appendix`
**Key discussion page**: no
**Seals**: USN + USCG top-right
**Title**: `TAM Framing | The $7.1B FY2025 contracting-market TAM
apportions to a ~$3.3-3.8B range of FY2025-delivered contractor
revenue under period-of-performance sensitivity; the workbook
presents Frame A (contracting activity) by industry convention`
**Layout**: three-zone - top equation flow spanning slide width
(~15%) + bottom-left combination chart (~55% of remaining) +
bottom-right apportionment table (~45% of remaining)

### Top visual - numbered equation flow

**Idiom**: Numbered process flow with operators (§4c Idiom 4),
rendered as a single-row horizontal equation spanning the slide
width.

**Equation**:

```
[1] FY2025 $7.1B Obligations  (x)  [2] POP apportionment %  (=)  [3] ~$3.5B FY2025-delivered revenue
```

Boxes colored per 4-chip legend:
- Box [1] navy (Frame A - in-scope contracting activity)
- Box [2] slate (derived multiplier)
- Box [3] slate with a dashed light outline (derived estimate, not
  measured)

The equation frames the slide's methodology discussion.

### Bottom-left visual - combination chart

**Idiom**: Combination chart (columns + horizontal reference line).

**4-chip legend** (top-right of visual):
- Navy = Frame A (hero - the workbook's presented frame)
- Slate = Frame B methods M1, M2, M3, M4 (sensitivity alternatives)
- Dashed horizontal reference line = Central Frame B estimate

**Chart hero**: Frame A column (navy) at $7,067M. Frame B methods
in neutral slate.

Five vertical columns. A horizontal dashed reference line drawn
across the chart at $3,500M labeled
`Central Frame B estimate ~$3.5B (49% of Frame A)`.

| Rank | Method | FY2025 $M | % of Frame A | Column color |
|-----:|--------|--------:|-------------:|--------------|
| 1 | **M5 Frame A - no apportionment** | **7,067** | **100.0%** | Navy |
| 2 | M2 12-month POP cap | 3,747 | 53.0% | Slate |
| 3 | M3 18-month POP cap | 3,499 | 49.5% | Slate |
| 4 | M1 Pure Linear | 3,354 | 47.5% | Slate |
| 5 | M4 Front-loaded 60/40 | 3,266 | 46.2% | Slate |

Labels above each column: $M value + % of Frame A.

### Bottom-right module - Apportionment table

**Table styling**: Section 5 open-rule. Navy super-header band
reading `Frame B M1 Apportionment by Work Segment`. No mini-section
bands. Bold total row as primary emphasis.

| Work Segment | Frame A $M | Frame B M1 $M | Apport % |
|--------------|-----------:|--------------:|---------:|
| Port & Technical Services | 431 | 307 | 71.3% |
| Depot Ship Repair | 4,781 | 2,468 | 51.6% |
| Hull, Mechanical & Electrical (HM&E) | 938 | 363 | 38.7% |
| Electronics & C4ISR Sustainment | 333 | 105 | 31.4% |
| Combat Systems Sustainment | 585 | 112 | 19.1% |
| **Total** | **7,067** | **3,354** | **47.5%** |

### Annotation layer

- **`Note:` line** at bottom: `Note: FY2025 window = 2024-10-01 to
  2025-09-30. POP apportionment uses start_date / end_date fields
  on FPDS award rows (100% populated in the MRO dataset). M1 Pure
  Linear is the primary Frame B estimate; M2-M4 are bounds. Combat
  Systems apportions at only 19% under Frame B M1 because Trident II
  / AEGIS integration work runs on 5-10 year POPs (Draper MK7 LE2
  alone is $318M with POP starting FY24 and extending into FY29).
  Port & Technical apportions at 71% because husbanding and QC work
  is short-cycle and POP aligns with FY2025. True Frame B would
  require contractor-side billing / earned-value data unavailable
  in federal sources. Frame A (contracting activity) is the
  industry convention for federal contracting TAM in PE / M&A /
  sell-side diligence; readers modeling a specific contractor can
  multiply the relevant segment $ by the apportionment rate for a
  first-order Frame B estimate.`
- **Pointer callout**: none.
- **Summary-stat ovals**: none.

### Footer

`Source: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
Guard, 65 services PSCs, post-exclusions). Period-of-performance
dates per FPDS. Methodology:
docs/methodology/METHODOLOGY_TAM_FRAMING.md. Data as of April 2026.`

### Supporting workbook sheets

Methodology doc + scratch compute (no dedicated workbook sheet).
`METHODOLOGY_TAM_FRAMING.md` tables.

---

## Sheet-to-slide support mapping

Workbook `output/08APR2028_Newbuild_and_MRO_Spend_v2.XX.xlsx`
supplies the following workbook sheets for each slide:

| Slide | Primary workbook sheet | Key data elements |
|-------|----------------------|-------------------|
| 1 Overview | (none - framing) | - |
| 2 Agenda | (none - framing) | - |
| 3 TAM & Scope | Services, Overview | TAM headline via `NAVY_TAM_SVC` + `CG_TAM_SVC` defined names |
| 4 Addressable vs Adjacent Spend | Budget Anchors, Sub & Carrier Coverage | SCN line items, OMN 1B4B derivation, PSC 1905 / 4470 subtotals |
| 5 TAM Composition | Services | Vessel Type x Work Segment crosstab + Work Segment rollup totals + coverage definitions; `Avg. Contract Size` per-vessel oval data |
| 6 Depot Ship Repair Deep Dive | Depot Ship Repair, J998 J999 Data | IDV Scope Group x Contractor Tier crosstab, IDV scope group rollup, vessel category rollup (secondary reference) |
| 7 Geographic Context - Depot Ship Repair | Depot Ship Repair | RMC x Tier crosstab, RMC Geography column |
| 8 Prime Landscape - Total MRO | Services, Public Comps | Top contractors + #1/#2/#3 per segment; HII Mission Technologies margin; `Avg. Contract Size` per-prime oval data |
| 9 Prime Landscape - Depot Ship Repair | Depot Ship Repair, Awards | Depot prime Pareto top-10 (PSC J998/J999-only contractor rollup) + Depot prime x RMC crosstab + FDNF roster (foreign-yard filter on Corporate Parent); `Avg. Contract Size` per-prime oval data |
| 10 Appropriation Sourcing | Budget Anchors | `MRO_TAS_*` named cells (10 appropriation rows + 3 OPN BA sub-rows) |
| 11 TAM Framing | (methodology doc + scratch compute) | `METHODOLOGY_TAM_FRAMING.md` tables |

Sheets with no deck role under this proposed flow: **Product
Procurement**, **Sub Ratios** (deprecated), **Public Comps**
(supports the Slide 8 pointer callout only), **Subcontract Data**
(deprecated), **Awards** (supports Slide 9 depot-prime Pareto and
FDNF roster rollups; primary role is data backend), **Vessel
Taxonomy** (reference lookup; keep). Sheet-pruning review is a
follow-up to this deck redesign, not part of it.

---

## Consistent elements across the deck

Styling specifics live in `deck/SLIDE_STYLE_TEMPLATE.md`. Brief
recap only:

- **Title format**: `Topic | action-statement assertion` at top
  (content slides); single topic word for framing slides (Overview,
  Agenda)
- **Layout**: left-side chart or primary visual (~55-60% of slide
  width), right-side table or callout column (~40-45%), thin
  separator rule above the footer at the bottom. Exceptions: Slide
  1 Overview (two equal-width text columns, split-color canvas, no
  footer); Slide 2 Agenda (full-bleed dark-slate, section list,
  no right module, no footer); Slide 9 (left panel split into
  Pareto + FDNF roster block); Slide 11 (three-zone with top
  equation + bottom-left chart + bottom-right table)
- **Color palette**:
  - Navy: hero numbers, Tier-1 primes, Frame A, in-scope segments,
    Navy-direct appropriations
  - Slate-gray: secondary categories, Frame B methods,
    Adjacent ship-dollar pool bars, Defense-Wide appropriations
  - Light-blue: tertiary segments, FDNF foreign yards,
    other-agency appropriations
  - Hatched: non-addressable (nuclear MRO PSCs, public-yard NWCF
    labor)
  - Medium-gray: neutral columns (Slides 8 + 9 Pareto columns;
    Slide 4 bullseye outer ring)
- **4-chip legend** top-right of every scope-bearing visual (gray
  chip labeled `Adjacent ship-dollar pool` on this deck), EXCEPT
  on charts that carry their own inline segment legend - then the
  4-chip legend drops to avoid competing legends (e.g. Slide 5
  Mekko with its work-segment legend). See
  `SLIDE_STYLE_TEMPLATE.md` §4a exception.
- **Chart emphasis rule**: one navy hero element per chart,
  everything else neutral
- **Stack-segment labels**: metric only (percent or $), not the
  segment name - legend carries identification
- **Residual columns**: any `Other` column carries a bottom
  footnote enumerating its composition
- **Scope pills**: not used on this deck (breadcrumb + title
  orient the reader)
- **Institutional seals**: USN + USCG top-right on every content
  slide (Slides 3-11). No DHS seal; no author avatar.
- **Pointer callouts (Variant B)**: at most one per slide,
  intermittent - used on Slides 4, 5, 7, 8 only
- **Summary-stat ovals**: used on Slides 5, 8, 9 (bold italic
  left-margin label + one oval per column, plain black bold text
  on white inside a thin black outline - no highlighter fill)
- **Note / Source prose**: sentence capitalization on `Note:` /
  `Source:` / pointer-callout text; no math-symbol shorthand
  (`=`, `+`, `x`, `~`, numeric-range `-`, alternation `/` all
  written out in words)
- **Fiscal-year format**: four-digit form (`FY2025`, `FY2026`)
  everywhere on-slide; never the two-digit short form
- **Preliminary disclaimer box**: on Slide 1 Overview only
- **Footer source strip**: always follows the pattern "Source:
  FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast Guard,
  65 services PSCs, post-exclusions). Data as of April 2026."
  Slides 4, 8, 10, 11 add specific additional sources. Slides 1
  and 2 omit the footer.

---

## Build order when slides are drawn

1. Draw Slide 5 (TAM Composition) first - repurposes the former
   Vessel Mix Mekko with the merged work-segment summary table on
   the RHS. Chart work is straightforward; the main edit is the
   RHS work-segment table doing triple duty (totals + %s +
   coverage definitions) plus the new summary-stat oval row.
2. Draw Slides 3 + 8 next - evolutions of currently delivered
   slides with refinements (Slide 3 funnel converted to numbered
   process flow; Slide 8 title clarified to "Total MRO", callout
   adds the Slide 9 cross-reference, summary-stat ovals added).
3. Draw Slides 4, 6, 7 next - mockup-sourced slides needing fresh
   chart work. Slide 4 bullseye + A-E pointer layout is the
   biggest new construction; Slide 6's RHS entry-structure flow
   needs the Section 5 table-family styling; Slide 7's RHS matrix
   merges the two former tables into row-group-banded form.
4. Draw Slide 9 (Prime Landscape - Depot Ship Repair) - the only
   genuinely new slide. Fresh Pareto chart (same format as Slide 8,
   scoped to the $4.9B depot base) plus FDNF roster block on the
   left panel plus prime x RMC crosstab with the §5c
   vertical-rules exception on the right.
5. Draw Slides 10 + 11 (appendix material) - Slide 10's RHS
   converts from the former callout column to a Section 5
   Finding / Implication table; Slide 11's top equation flow is a
   small new element.
6. Draw Slides 1 + 2 (framing) last - Overview split-color canvas
   and Preliminary disclaimer box on Slide 1; full-bleed dark-slate
   Agenda on Slide 2. Framing slides omit the footer and seals
   (scope pills are not used anywhere on this deck).

After each slide is drawn, capture a screenshot into `deck/` and
promote the slide's spec from this file into `DECK.md` in the same
transcription style as the four currently-delivered slides. Once
all 11 slides have been promoted, this file can be deleted.

---

## Resolved decisions (MRO deck, 2026-04-19)

All template open questions resolved, plus deck-wide style rules
codified in the 2026-04-19 (v) update. Decisions baked into the
styling above; captured here for reference alongside the
corresponding section in `deck/SLIDE_STYLE_TEMPLATE.md` §9.

1. **`Key discussion page` pill meaning** - marks slides the
   AUDIENCE should debate. On this deck: Slides 6 and 9 (Depot
   Ship Repair Deep Dive + Prime Landscape - Depot Ship Repair).
2. **Author avatar vs institutional seals** - institutional seals
   from day one. Seal set: USN + USCG only (no DHS). Assets at
   `deck/MRO_slide_deck_draft_v3/assets/usn-crest.jpg` +
   `uscg-crest.png`. No intermediate WIP author-avatar phase.
3. **Agenda slide placement** - one Agenda slide (Slide 2),
   placed immediately after the Overview (Slide 1). Not
   reinserted between sections.
4. **4-chip legend gray-chip label** - renamed from "Sized in
   another campaign" to `Adjacent ship-dollar pool` for
   MRO-specific clarity. Applied across all scope-bearing visuals
   on Slides 3-11.
5. **Breadcrumb naming** - reflects the workbook's section
   structure (Scope / Structure / Competitive Landscape /
   Methodology), not narrative structure.
6. **Summary-stat ovals** - conservative placement: only where a
   per-column derived metric genuinely adds information. Applied
   on Slides 5, 8, 9 only (`Avg. Contract Size:` label + one oval
   per column). Not applied universally.
7. **Slide 9 FDNF treatment** (MRO-deck-specific) - added a
   separate FDNF roster block beneath the Pareto on Slide 9's
   left panel, showing the 7 foreign yards summing to ~$510M.
   Live CONUS Tier-2 primes occupy the Pareto's slots 6-10; FDNF
   yards are visible but not mixed with the CONUS ranking.
8. **Scope pills dropped from this deck** (deck-wide) - the
   light-blue scope pill convention from
   `SLIDE_STYLE_TEMPLATE.md` §2b is not used on the MRO deck.
   Breadcrumb and title orient the reader; repeating the
   PSC-filter methodology detail in a pill added clutter without
   adding signal. Removed from every slide spec.
9. **Summary-stat oval treatment** (deck-wide) - ovals render as
   plain black bold text on white inside a thin black outline.
   The yellow highlighter-style fill mentioned in earlier
   template drafts is not used on this deck; the convention
   changed 2026-04-19 and propagated into the template and into
   every per-slide oval spec.
10. **`Note:` / `Source:` / callout prose** (deck-wide) -
    sentence capitalization (first word after `Note:` or
    `Source:` capitalized) and no math-symbol shorthand (`=`,
    `+`, `x`, `~`, numeric-range `-`, alternation `/` all
    written out in words; `%` and `$` remain allowed as units).
    Rule added to `SLIDE_STYLE_TEMPLATE.md` §4e-i 2026-04-19.
11. **Fiscal-year format** (deck-wide) - four-digit form
    (`FY2025`, `FY2026`, `FY2030`) everywhere on-slide, never
    the two-digit short form. Rule added to
    `SLIDE_STYLE_TEMPLATE.md` §3 and mass-replace applied across
    `DECK_PROPOSED.md` and `DECK_PROPOSED_revisions.md` on
    2026-04-19.
12. **Title rules - no semicolons** (deck-wide) - the right half
    of `Topic | assertion` is one sentence; no semicolon-chained
    clauses. Rule added to `SLIDE_STYLE_TEMPLATE.md` §3 2026-04-19.
13. **Inline-legend exception to the 4-chip legend** (deck-wide)
    - when a chart has its own inline segment legend (Mekko
    work-segment legend, stacked-column segment legend), drop
    the 4-chip legend on that chart to avoid competing legends.
    The dashed / hatched treatments travel with the 4-chip legend
    and drop with it. Rule added to `SLIDE_STYLE_TEMPLATE.md`
    §4a 2026-04-19.
14. **Stack-segment labels - metric only** (deck-wide) - in any
    stacked chart where the legend names each segment, in-stack
    labels show the metric only (percent or $ value), not the
    segment name. Rule added to `SLIDE_STYLE_TEMPLATE.md` §4d
    2026-04-19.
15. **Residual / "Other" column composition footnote required**
    (deck-wide) - any chart or table with an `Other` column
    carries a bottom footnote enumerating what rolls up into
    `Other`. New §4f in `SLIDE_STYLE_TEMPLATE.md` 2026-04-19.
