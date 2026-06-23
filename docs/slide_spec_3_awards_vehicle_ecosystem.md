# Slide Spec — 03 · The Awards Universe (Vehicles, Obligated-vs-Ceiling, Recompete Signal)

```text
SLIDE 03 - THE AWARDS UNIVERSE: VEHICLES, OBLIGATED-vs-CEILING, AND THE RECOMPETE SIGNAL
Type: Body

Slide's purpose:
  Map the contract-vehicle ecosystem and show how the obligated-vs-ceiling structure plus
  vehicle-authority expiry becomes a forward opportunity pipeline. This is the "who buys,
  and when" payoff: obligated is what has already flowed; the unexercised ceiling and the
  recompete clock are the opportunity. Demonstrate the discipline that keeps the numbers
  honest (distinct money measures, vehicle roll-up, recompete date logic, anti-overcount).

TITLE
-----
Copy:
  Reading the awards universe | Obligated is today; the ceiling and the recompete clock are
  the opportunity.

HIGH-LEVEL LAYOUT
-----------------
  Three zones. Left: a vehicle-taxonomy tree (Definitive contract / IDV -> task orders /
  BPA + BPA calls / BOA / OT). Center: an obligated-vs-ceiling decomposition (stacked bar or
  three-tier bar) with the gap labeled as remaining capacity. Right: a recompete-signal
  panel (decision-date logic + capture timeline + the screened-universe funnel). A money-
  discipline caveat rail runs along the bottom.

COMMENTARY COPY, IF NEEDED
--------------------------
Commentary 1
  Copy:
    Three dollar measures, never summed.
    Obligated (money legally committed), current value (base + exercised options), and
    ceiling (base + all options) are distinct amount-types - a register, not a fact table.
    Only the per-modification action stream is sum-able; sum it, never the restated
    cumulative totals. Reconcile award-reported vs reconstructed obligations and carry a
    coverage ratio so a partial reconstruction can never masquerade as a vehicle's value.
  Text / shape treatment:
    Bold finding; no-fill rail above the center bar; the three measures echoed as the bar's
    own labels (see CHART).

Commentary 2
  Copy:
    The recompete is when the government loses authority to place new orders - NOT the latest
    task-order end date.
    For an IDV that is the ordering-period end (hydrated from the SAM Contract Awards API);
    for a BOA / BPA the nominal end is a master-agreement date, not a guaranteed recompete
    (lower confidence); for a standalone it is its own period-of-performance end. Option-
    years-left = (potential end - decision date) is the unexercised ceiling expressed as time.
  Text / shape treatment:
    Filled card in the right panel - the slide's key reframe; highest weight of the three.

Commentary 3
  Copy:
    Count opportunities once.
    Lineage chaining (same incumbent + PSC + temporal gap) separates a true overdue
    recompete from a vehicle already superseded by a follow-on; cohort logic folds co-awarded
    multiple-award vehicles into one requirement. On Army watercraft this took 1,688 award
    families down to 226 screened, split 124 overdue / 62 superseded / 40 active.
  Text / shape treatment:
    Below-exhibit note tied to the screened-universe funnel; muted, with the 1,688 -> 226
    reduction as a small inline figure.

OTHER VISIBLE COPY, IF NEEDED
-----------------------------
Copy:
  Vehicle-tree node labels: Definitive contract | IDV (IDIQ / Requirements) -> Task &
  Delivery Orders | BPA + BPA calls | BOA | OT agreement / order.
  Confidence chips for the recompete date: High (standalone / hydrated IDV) · Medium (IDV
  base record / BPA) · Low (IDV child-max fallback / BOA nominal).

Text / visual treatment:
  OT node visually flagged (accent) as the defense-tech-relevant pathway. Task/Delivery
  Orders nest under the IDV node to show roll-up. Confidence chips color-graded.

CHART, IF NEEDED
----------------
Copy / data / labels / chips:
  Center exhibit. Units caption "Per vehicle / family, $M". Two bars side by side:
  "Obligated to date" and "Potential ceiling (base + all options)"; the difference banded and
  labeled "remaining capacity - options / task orders not yet obligated."
  Purpose:
    Make "obligated vs unobligated/ceiling" visceral - the gap is the future opportunity
    already inside an existing vehicle.
  Structure:
    Paired/stacked bar; obligated as the solid base, remaining ceiling as the open band; take
    the latest restated ceiling, never a sum across mods.
  Text / visual treatment:
    Obligated solid and emphasized; remaining-capacity band outlined/hatched (muted) to read
    as "available." Data labels on both segments.
  Fit behavior:
    If space is tight, collapse to a single vehicle (e.g. an IDV family) rather than several;
    keep both segments and the gap label. Do not add an outlay segment.

TABLE, IF NEEDED
----------------
Copy / rows / columns:
  Small reference table in/under the right panel. Columns: Vehicle type | Recompete date =
  | Confidence.
  Row 1: Standalone contract | Its own period-of-performance end | High.
  Row 2: IDV (hydrated) | Ordering-period end (SAM Contract Awards) | High.
  Row 3: IDV (base record) | Vehicle base-record PoP end | Medium.
  Row 4: BPA | Call-period end (orders may continue under parent) | Medium.
  Row 5: BOA | Nominal end - NOT a guaranteed recompete | Low.
  Purpose:
    Document the decision-date rule per agreement type so the recompete dates are auditable,
    not a black box.
  Structure:
    Five rows, highest-to-lowest confidence; "Confidence" is the scan column.
  Cell / table treatment:
    Vehicle type bold; confidence cells color-graded (green/amber/red), centered. Header
    underlined; light rules.
  Fit behavior:
    Merge the two IDV rows first if space is short; the BOA "not a guaranteed recompete" row
    must remain (it is the most common misread).

OBJECT NOTES, IF NEEDED
-----------------------
  - Reading order: vehicle tree (left) -> obligated/ceiling bar (center) -> recompete panel
    (right) -> caveat rail.
  - Task/Delivery Order nodes are children of the IDV node (indented, connected) to show
    that orders collapse into their parent family key.
  - A worked-example callout may pin to the recompete panel: lineage pair Birdon
    W56HZV14C0015 -> W56HZV19D0093 (415-day overlap); capture row Gunderson W912BU24C0046
    (decision 2026-07-01, notice-by 2026-04-02, $49.8M). Keep as one small annotation, not a
    second table.
  - Do not add: a full recompete calendar / queue (that is a workbook deliverable, not this
    methodology slide).

Do not repeat:
  - Title copy.
  - Commentary copy or treatment.
  - Chart copy, data, labels, or treatment.
  - Table copy, data, or cell treatment.
  - Source note.

SOURCES
-------
Copy:
  Per-modification obligations: FPDS Atom feed (authoritative) reconciled with USAspending
  transactions. Vehicle ceiling and IDV ordering-period end: SAM.gov Contract Awards API
  (base+all-options ceiling; ordering-period hydration). Worked examples and the recompete /
  lineage / cohort logic: internal Army Market Mapping workbook (Timing & Incumbent Screen;
  Recompete Research Queue). Then-year dollars; figures illustrative of method.
```
