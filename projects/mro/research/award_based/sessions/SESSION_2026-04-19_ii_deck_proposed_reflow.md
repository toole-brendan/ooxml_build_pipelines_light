# Session 2026-04-19 (ii): DECK_PROPOSED Reflow - 10-Slide Restructure

## Context

Session (i) earlier today landed the `Deck Data` sheet + POP
apportionment helpers that back the 10-slide `DECK_PROPOSED.md` spec
(workbook v2.85). No slides have been drawn yet; `DECK_PROPOSED.md`
remains the authoritative spec while `DECK.md` holds the delivered
4-slide version.

This session worked the spec itself, not the workbook. User walked
through the slide-by-slide flow, flagged redundancies and narrative
gaps, and asked for a restructured 10-slide arc that concentrates
depth on the depot-ship-repair segment (the ~68% / $4.9B workhorse
slice and the actual decision focus for the Saronic / Port Alpha
yard-site question).

**No workbook rebuild this session.** Output: `DECK_PROPOSED.md`
rewritten in place; no version bump to the model.

---

## Part A - Slide-consolidation proposal (old 4 + old 6)

User's first question: can old Slide 4 (Work Segments, a 100% stacked
column) and old Slide 6 (Vessel Mix, a Mekko of vessel category x
work segment) collapse to a single slide?

Assessment: yes - a Mekko already encodes both dimensions. The
work-segment totals from old Slide 4 are mathematically identical to
the sum of each horizontal work-segment stack across all vessel
columns in old Slide 6's Mekko. The only reason the two slides
coexisted in the first spec was readability: segment totals are
harder to read off a Mekko than off a dedicated single-column stack.

Resolution: consolidate to a single slide, using a **right-side
work-segment summary table** that does triple duty (segment $M + % +
coverage definition). This recovers the totals and merges in the old
Slide 4 coverage table simultaneously.

### Designed title and lede

- **Title**: "TAM Composition | Depot ship repair drove ~68% of FY25
  MRO TAM; ~62% of hull spend concentrated on surface combatants,
  amphibious warfare ships, and submarines"
- **Subtitle**: "FY2025 MRO TAM by Vessel Type x Work Segment ($M)"
- **RHS Block 1** (5-row table): Segment / $M / % / Coverage -
  merges work-segment totals (old Slide 4) with coverage definitions
  (old Slide 4 right-side table).
- **RHS Block 2** (callout): submarine public-yard structural
  understatement caveat (migrated from old Slide 6 margin callout;
  directly relevant because the Mekko's Submarine column is now
  visible).
- "Concentration tracks fleet tempo" callout from old Slide 6
  absorbs into the title assertion - no longer needs slide real
  estate.

---

## Part B - Deeper reflow

User then raised three more structural moves:

1. **Move old Slide 8 (Geographic Context) up** to directly follow
   the Depot Deep Dive. Rationale: old Slide 8's Mekko is drawn on
   J998/J999 data (RMC x contractor tier) - it is *already* a
   depot-specific view, so pairing it next to old Slide 5 creates a
   natural "depot scope -> depot geography" arc with two Mekkos on
   the same $4.9B base sliced different ways.

2. **Keep the Prime Landscape (total MRO) slide** at the current
   slot 7.

3. **Add a new Prime Landscape - Depot slide** at slot 8,
   specifically for the $4.9B depot segment.

Assessment: geography move is analytically correct (same data, same
subject matter). The new depot-primes slide needs to do something
different from old Slide 5's former Tier-1 CONUS prime roster block
to justify its existence. Options canvased:

- (a) Pareto of top-10 depot primes with cumulative line - mirrors
  Slide 7's format, scoped to the $4.9B denominator. Gives a
  "depot top-10 = ~75%" concentration statistic that pairs with
  Slide 7's "total-MRO top-10 = ~57%".
- (b) Depot prime x IDV-scope-group crosstab (who runs Full-Ship
  vs MSC vs Trade IDIQ).
- (c) Depot prime x RMC crosstab (which primes sit in which RMC -
  ties directly to the yard-site decision).

User picked **(a) as LHS chart + (c) as RHS table**. (a) gives the
concentration statistic; (c) gives the regional-footprint view that
is most directly actionable for the site question. (b) deferred.

User also confirmed the **Slide 5 RHS cleanup**: drop the Tier-1
CONUS prime roster block (BAE $1,073 / GD $640 / HII $390 / Vigor
$440 / Detyens $225 / NASSCO Mayport $100 / subtotal ~$2,868M) and
keep only the Entry-structure bullets. Rationale: once new Slide 8
carries the full depot-prime picture, that roster would appear
twice. Better to slim Slide 5 to the entry-structure story alone
(MSRA -> MAC-MO -> task order) and let Slide 8 carry the prime
quantification.

---

## Part C - Final 10-slide flow

```
Act I - Orient the Decision Landscape
  1. Research Context & Approach          (unchanged)
  2. TAM & Scope                          (unchanged)
  3. Addressable vs Adjacent Spend        (unchanged)

Act II - Structure of the Addressable Market
  4. TAM Composition                      (NEW: merged old 4 + old 6)
  5. Depot Ship Repair Deep Dive          (RHS slimmed; title trimmed)
  6. Geographic Context                   (moved up from old slot 8)

Act III - Competitive Landscape           (new act name)
  7. Prime Landscape - Total MRO          (title clarified; callout pointer)
  8. Prime Landscape - Depot Ship Repair  (NEW)

Appendix - Methodology Defense
  9. Appropriation Sourcing               (unchanged)
 10. TAM Framing                          (unchanged)
```

Act III renamed from "Geographic Context (Act payoff)" to
"Competitive Landscape" - better captures what slots 7 + 8 do
together (prime concentration zoomed out then zoomed in).

---

## Part D - Edits applied to DECK_PROPOSED.md

Eight sequential `Edit` operations on
`/Users/brendantoole/projects2/domnann/deck/DECK_PROPOSED.md`:

1. **Deck-flow section**: replaced Act II/III listings.
2. **Visual system summary table**: 10 rows reshuffled; Slide 5
   moves to "Table? No" (bullets, not table); Slides 7 + 8 both
   listed as Pareto.
3. **Chart type counts**: Mekko now (4, 5, 6); Pareto now (7, 8, 10);
   stacked column drops to 1 (slide 9).
4. **Slide 4 full replacement**: Work Segments 100%-stacked column
   out; TAM Composition Mekko in. New RHS triple-duty table + new
   callout + 4 footnotes.
5. **Slide 5 title update**: "Six CONUS Tier-1 yards captured ~60%
   of the $4.9B" claim removed from title (now lives on Slide 8);
   title now leads with "65% of depot $ is full-ship availabilities
   via three-tier MSRA / MAC-MO structure".
6. **Slide 5 RHS + callout**: Block 1 (Tier-1 prime roster) dropped;
   Block 2 (Entry structure) retained and expanded with 1-sentence
   elaborations per bullet + footprint-and-Slide-8-pointer closer.
   Callout rewritten to focus on trade-IDIQ-<3% and Tier-1-CONUS-
   concentration narrative without quantified roster claim.
7. **Slides 6-8 combined replacement** (biggest edit): deleted old
   Slide 6 Vessel Mix; moved old Slide 8 Geographic Context content
   up to new Slide 6 position (content essentially unchanged, added
   "Slide 8 decomposes RMC $ by prime contractor" pointer to
   callout); updated Slide 7 title to "Prime Landscape - Total MRO"
   and added Slide 8 cross-reference to callout; inserted brand-new
   Slide 8 Prime Landscape - Depot Ship Repair.
8. **Consistent elements + sheet-to-slide mapping + build order**:
   no-table exception changed from Slide 6 -> Slide 5; medium-gray
   palette note now covers Pareto columns on Slides 7 + 8; footer-
   additional-source list changed from "Slides 3, 8, 9, 10" ->
   "Slides 3, 9, 10" (new Slide 8 uses FPDS + classifier only);
   10-row sheet-to-slide table re-keyed (Slide 4 now Services for
   vessel x segment crosstab; Slide 6 now Depot Ship Repair; Slide
   8 now Depot Ship Repair + Awards); build-order list restructured
   from 3 buckets -> 5 buckets with Slide 8 called out as the only
   genuinely new slide.

---

## Part E - Slide 8 spec details worth preserving

The new Slide 8 is the only genuinely net-new slide in the reflow.
Key specs captured in the markdown:

**Pareto data** (denominator = $4,923M in-scope depot, post-FMS):

| # | Contractor | FY25 Depot $M | Cumulative % |
|--:|------------|--------------:|-------------:|
| 1 | BAE | 1,073 | 21.8% |
| 2 | GD (NASSCO + Continental Maritime) | ~886 | 39.8% |
| 3 | HII (Continental Maritime + Metro Machine + MHI) | ~492 | 49.8% |
| 4 | Vigor | 440 | 58.7% |
| 5 | Detyens | 225 | 63.3% |
| 6 | Hanwha Ocean | ~200 | 67.4% |
| 7 | Navantia | ~130 | 70.0% |
| 8 | NASSCO Mayport | ~100 | 72.0% |
| 9 | East Coast Repair | ~85 | 73.8% |
| 10 | Sumitomo | ~80 | 75.4% |

BAE / GD / HII figures derived from Slide 7's segment top-3 depot
shares (22% / 18% / 10%) applied to the $4,923M denominator. Ranks
6-10 are approximate placeholders; exact figures will snap from
`Depot Ship Repair` + `Awards` sheets at build time.

**Prime x RMC crosstab** (RHS) - 10 rows x 7 RMC columns plus
subtotal / RMC-total / top-10-%-of-RMC rows. Multi-RMC primes (BAE,
HII) approximated from yard geography; single-RMC primes exact.

**Headline comparison**: depot top-10 = ~75% of $4.9B vs total MRO
top-10 = ~57% of $7.1B (Slide 7). Depot is materially more
concentrated because of the MSRA -> MAC-MO -> task order entry
structure (Slide 5). Deck narrative: depot is structurally harder
to enter than the rest of MRO.

**Site-decision callout**: every Tier-1 prime is RMC-anchored; the
candidate Gulf Coast site sits outside any established RMC cluster;
the California candidate would sit within / adjacent to SWRMC
(~$1.6B) or NW RMC (~$430M).

---

## Files changed

- `deck/DECK_PROPOSED.md` - 10-slide flow reshuffled; Slide 4 + 5 + 6 +
  7 + 8 content rewritten or relocated; flow / visual / chart-count /
  mapping / build-order sections all re-keyed. ~1050 lines (similar
  length to prior version; one slide gained, one absorbed).

## Files NOT touched

- `deck/DECK.md` - still the 4-slide delivered reference.
- Workbook / sheet builders - no Python changes.
- `data_pull/` - no data regeneration needed (numbers are all already
  in the workbook; Slide 8 Pareto + crosstab will pull from existing
  `Depot Ship Repair` and `Awards` sheets when built).

## Follow-ups

- When Slide 8's Pareto + crosstab are actually drawn, snap the
  ranks-6-10 figures from the workbook to replace the placeholder
  approximations. GD and HII totals will also reconcile against the
  full parent-company depot rollup (Slide 5's former roster used
  NASSCO + Continental Maritime sub-units only, which is why the
  reflow left a footnote flagging that reconciliation).
- Build order starts with Slide 4 (TAM Composition) because it
  repurposes the old Slide 6 Mekko most directly. Slide 8 is the
  only fully-new slide and is called out as such in the build-order
  list.
- Once all 10 slides are drawn + captured, promote into `DECK.md`
  and archive / delete `DECK_PROPOSED.md` per the in-file guidance.
