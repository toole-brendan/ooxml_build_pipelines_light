# Deck RHS Pattern Mapping

Mapping of each content slide's supporting module (the "right-hand
side" or secondary content that accompanies the main chart) to the
patterns observed in the manager's gold-standard slide examples.

Framing slides (Overview, Agenda) follow separate conventions and are
omitted from this mapping.

---

## Pattern catalog

**#1 Two-column comparison table** - contrast 2-3 mutually-exclusive
archetypes across shared attributes.

**#2 Legend table** - label + one-line definition pairs, often tied to
a visual via lettered pointers (A, B, C...).

**#3 Filled matrix** - 2-D lookup, rows x columns with numeric /
status cells.

**#4 Process flow** - numbered steps with arrows or operator boxes
(+, x, =); encodes a pipeline or equation.

**#5 Image grid with captions** - photo thumbnails in a row with
one-line captions.

**#6 Hierarchical block diagram** - tiered strips of labeled
rectangles showing grouping, bundling, or scope.

**#7 Decision tree / flowchart** - branching diagram for selection /
filter logic.

**#8 Callout pills (top-right)** - navigation tags for slide state,
not content.

**#9 Grouped bullet commentary** - bold section headers with bulleted
items beneath, 2-4 sections stacked. Used for grouped assumptions or
derivation commentary.

**#10 Callout card stack** - bordered cards stacked vertically, each
with a bold-header insight and prose body. One atomic insight per
card.

### #9 vs #10 distinction

- **#9 Grouped bullets**: section theme -> list of items in that
  section. Headers are categories; bullets are the items.
- **#10 Callout cards**: atomic insight -> explanation of it. Each
  card stands alone and can be read in any order.

---

## Slide-by-slide mapping

### TAM & Scope
**RHS pattern**: #2 Legend table

Four label-definition pairs covering PSC, awards-data vs budget
materials, in-scope work types, and out-of-scope work types. Matches
current `DECK_PROPOSED.md` spec.

### Addressable vs Adjacent Spend
**RHS pattern**: #2 Legend table (top) + #10 Callout card stack
(bottom)

Top module: A-E ring legend with $M per ring and a one-line
definition, tying each lettered pointer on the bullseye to the ring
it labels.

Bottom module: atomic takeaway cards covering the scope-reconciliation
narrative (e.g., "PSC 1905 on nuclear hulls", "Implied public-yard
labor derivation", "Nuclear MRO PSC emptiness").

Replaces the current dense three-band matrix of budget-anchor source
rows.

### TAM Composition
**RHS pattern**: #10 Callout card stack *(changed from matrix)*

One card per work segment. Card header carries segment name + $M +
%. Card body carries the coverage prose (e.g., "Whole-ship
availabilities at Pacific / Atlantic RMCs, awarded through MAC-MO
IDIQ task orders"). Five cards total.

Replaces the current Work Segment x ($M / % / Coverage) matrix. Card
format handles the prose-heavy Coverage content more naturally than
forcing it into a narrow table cell.

### Depot Ship Repair Deep Dive
**RHS pattern**: #4 Process flow

Three-step numbered pipeline: MSRA pre-qualification -> MAC-MO IDIQ
capture -> fixed-price task orders. Matches current spec.

### Geographic Context - Depot Ship Repair
**RHS pattern**: #9 Grouped bullet commentary *(changed from matrix)*

Two sections: Active RMCs and Candidate Sites. Each RMC (or candidate
site) rendered as a bold header with 2-3 sub-bullets (geography /
Tier-1 primes in region / major fleet homeports).

Replaces the current two-row-group matrix. Bullet structure handles
the per-RMC sub-fields better than a wide matrix row, and the grouped
treatment keeps Active vs Candidate visually distinct.

### Prime Landscape - Total MRO
**RHS pattern**: #3 Filled matrix

Work Segment x (#1 / #2 / #3 prime) lookup. Matches current spec -
data shape is genuinely matrix-native.

### Prime Landscape - Depot Ship Repair
**RHS pattern**: #3 Filled matrix

Prime x RMC crosstab with Section 5c vertical-gridline exception
activated. Matches current spec - data shape is genuinely
matrix-native.

### Appropriation Sourcing (Appendix)
**RHS pattern**: #10 Callout card stack *(changed from 2-col table)*

Four atomic insight cards, one per takeaway:
- `OMN + OPN = 72% of MRO $` + Navy-story implication
- `OPN splits 62% Command Support Equip / 32% Spares` + BA-7 vs BA-8
  implication
- `RDT&E Defense-Wide = $780M (11%)` + Trident II / Draper MK7
  implication
- `SCN on MRO PSCs = ~$40M` + PSC 1905 bundling implication

This is the exact layout in the manager's reference screenshot.

### TAM Framing (Appendix)
**RHS pattern**: #4 Process flow (top strip) + #3 Filled matrix
(bottom-right)

Top: `Obligations x Apportionment = Revenue` equation spanning slide
width.

Bottom-right: Segment x (Frame A $ / Frame B M1 $ / Apport %) lookup.

Matches current spec.

---

## Pattern distribution

| Pattern | Count | Slides |
|---------|------:|--------|
| #2 Legend table | 1-2 | TAM & Scope; Addressable vs Adjacent (top) |
| #3 Filled matrix | 3 | Prime Landscape Total MRO; Prime Landscape Depot; TAM Framing (bottom) |
| #4 Process flow | 2 | Depot Ship Repair Deep Dive; TAM Framing (top) |
| #9 Grouped bullets | 1 | Geographic Context |
| #10 Callout cards | 3 | Addressable vs Adjacent (bottom); TAM Composition; Appropriation Sourcing |

Five distinct patterns in play. No single pattern carries more than
three slides. Visual variety across the deck mirrors what the
manager's gold-standard examples demonstrate.

---

## Changes from current DECK_PROPOSED.md

**Reframed**:
- Addressable vs Adjacent Spend - split RHS into legend (top) + card
  stack (bottom)
- TAM Composition - reframe RHS as card stack
- Geographic Context - reframe RHS as grouped bullet commentary
- Appropriation Sourcing - reframe RHS as card stack

**Unchanged**:
- TAM & Scope (#2 legend)
- Depot Ship Repair Deep Dive (#4 process flow)
- Prime Landscape - Total MRO (#3 matrix)
- Prime Landscape - Depot Ship Repair (#3 matrix)
- TAM Framing (#4 top + #3 bottom)
