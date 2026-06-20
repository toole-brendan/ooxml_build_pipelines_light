# Session 2026-04-18 (viii): Deck Finalization Plan + OPN PA Drill - v2.79 -> v2.80

## Context

User asked to finalize the slide deck first, then scope the workbook
so it only carries what the deck needs (and delete the rest). Starting
point:

- `deck/DECK.md` = 4 delivered slides (TAM & Scope / Vessel Mix / Work
  Segments / Prime Landscape).
- Two mockups on disk: Slide 3 budget-anchor callout augmentation
  (`SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md`) and Slide 5 Sub & Carrier
  Scope (`SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md`).
- Workbook at v2.79 with TAS appropriation attribution, depot J998/J999
  deep dive, sub/carrier coverage, etc.

Ended at **v2.80** with three deck mockups renumbered to match the
final order, a new Depot Deep Dive mockup drafted, the Slide 3 callout
proposal promoted into its own standalone Slide 5 Appropriation
Sourcing mockup, and the OPN row of that slide drilled one level
deeper using Program Activity data already in the funding cache.

The workbook-scope-to-deck cleanup (delete sheets / columns / sections
not needed for deck support) was discussed but not started.

---

## Part A - Deck finalization

### 1. Discussion on deck shape

User asked "what state is my analysis in?" then "finalize what my deck
should be, and then make sure my workbook has the data tables for the
deck." Key questions resolved via chat:

- **Slide 3 budget-anchor callout augmentation dropped** -- promoted
  into its own standalone slide instead. Reasoning: the appropriation-
  mixing story is more than a callout deserves; it either justifies a
  full slide or belongs only in the methodology doc.
- **Does the TAS work support the $7.1B figure?** Honest answer:
  *no*, it doesn't derive or cross-check $7.1B. It explains the
  *appropriation mix underneath* it (38% OMN / 36% OPN / 11% RDT&E-DW
  / 0.5% SCN). Defensibility slide, not TAM-size validation.
- **Depot deep dive slide** requested. No mockup existed; created new.

**Final deck order (proposed):**

1. TAM & Scope (delivered)
2. Vessel Mix (delivered)
3. MRO Work Segments (delivered)
4. Prime Landscape (delivered)
5. **Appropriation Sourcing** (new mockup - where the $7.1B comes from)
6. **Depot Ship Repair Deep Dive** (new mockup - drills Slide 3)
7. **Sub & Carrier Scope** (existing mockup - renumbered from Slide 5)

### 2. Mockup file rename + rewrite

File operations:

- `SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md` -> renamed to
  `SLIDE5_APPROPRIATION_SOURCING_MOCKUP.md` and **fully rewritten** as
  a standalone slide (not an augmentation). Headline: "$7.1B funded
  across ~10 appropriations; OMN and OPN each ~one-third; RDT&E-DW a
  surprising 11%."
- `SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` -> renamed to
  `SLIDE7_SUB_CARRIER_SCOPE_MOCKUP.md`. Content unchanged.
- `SLIDE6_DEPOT_DEEP_DIVE_MOCKUP.md` -> **new file.** Headline: "Six
  CONUS Tier-1 yards captured ~60% of $4.9B; 65% is full-ship
  availabilities via three-tier MSRA / MAC-MO structure."

The Slide 6 mockup's left-visual numbers (RMC x tier crosstab, Tier-1
prime roster) are flagged as approximations; final slide should pull
from the live `Depot Ship Repair` sheet at build time.

---

## Part B - OPN PA drill (data-v2-free path)

### 3. User question: can we identify the specific budget programs?

"For the appropriation slide, is there no way we can use data_v2.xlsx
to identify the likely specific programs of the budget books that fund
the awards we've identified / pulled?"

Investigated two paths:

**Option A (use what's already in the funding cache):** the
USAspending `/awards/funding/` rows also carry `program_activity_code`
and `program_activity_name`. For OPN, this splits cleanly:

- PA 0007 BA-7 Personnel & Command Support Equip
- PA 0008 BA-8 Spares & Repair Parts
- PA 0001 BA-1 Ships Support Equipment
- PA 0020 Undistributed, PA OPTN pre-FY21 optional, etc.

For OMN, the same PA field is *noisy*: $2.5B of the $2.8B OMN total
lands at PA 0004 "Administration and Service-Wide Activities" rather
than the functional PA 0001 "Operating Forces" where SAG 1B4B Ship
Maintenance actually lives. Navy appears to route NAVSEA contract
actions through an admin PA regardless of work type. OMN PA drill was
therefore skipped.

SCN on MRO PSCs is entirely at PA 0002 "Shipbuilding" (single PA, no
drill possible). RDT&E-DW PA data is thin ($20M at PA 009S
Miscellaneous out of $780M total).

**Option B (probabilistic join to data_v2.xlsx line items):** would
need to match award metadata (vessel hull + PSC + contracting office)
against data_v2.xlsx budget line items because USAspending funding
data doesn't expose Program Element Number or Cost Element. Accurate
maybe 70-90% on identifiable hulls, weaker on multi-hull IDIQs.
Not implemented; path A got the headline finding at zero new pull cost.

**User decision**: Option A only for the deck. Slide 5 shows OPN
drilled to BA; OMN / RDT&E-DW / SCN stay at appropriation level.

### 4. Implementation - `data_pull/classify_opn_pa_split.py`

New classifier. For each award in `approp_attribution.json` with OPN
attribution:
1. Read its cache file from `data_pull/output/usaspending/funding/`.
2. Sum `abs(transaction_obligated_amount)` across OPN (017-1810) rows
   by PA code.
3. Convert to ratios, multiply by the award's OPN FY25 $.

For the PSC-bucket-imputed slice (~$320M of the $2,588M OPN total,
which has no per-award cache signal), apply the global directly-
classified OPN PA ratio as a fallback so totals reconcile.

Rationale for using `abs()` of transaction amounts: mirrors the
existing `classify_approp_colors.py::build_classifier` approach. File
C data is noisy at the absolute-$ level (negative nets, de-obligations
across quarters), but the RATIOS within an award are reliable because
both sides share the same noise pattern.

**Output**: `data_pull/output/usaspending/approp_opn_pa_split.json`.

**Results (FY25 MRO-PSC OPN, TAS-attributed)**:

| PA     | Label                                        | FY25 $M   | % of OPN |
|--------|----------------------------------------------|----------:|---------:|
| 0007   | BA-7 Personnel & Command Support Equip       | $1,591    |  61.5%   |
| 0008   | BA-8 Spares & Repair Parts                   |   $825    |  31.9%   |
| 0001   | BA-1 Ships Support Equipment                 |    $65    |   2.5%   |
| 0020   | Undistributed                                |    $64    |   2.5%   |
| OPTN   | Pre-FY21 (optional field)                    |    $22    |   0.8%   |
| -      | Unspecified PA                               |    $20    |   0.8%   |
| 0002   | PA 0002                                      |    $0.5   |   0.0%   |
| **Total** |                                           | **$2,588**|  100%    |

Sub-rows reconcile cleanly to the OPN parent ($2,588M) from
`approp_rollup_imputed.json`.

### 5. Budget Anchors sheet additions

`sheets/budget_anchors.py`:

- New `_TAS_OPN_PA_PATH` constant + `_load_opn_pa_split()` memoized
  loader.
- New `kind='tas_pa'` row type handled via new
  `_resolve_tas_pa_values(row, opn_pa_split)` helper (mirrors
  `_resolve_tas_values` pattern).
- Three new indented sub-rows under the existing `TAS OPN` row:
  `TAS OPN BA-7`, `TAS OPN BA-8`, `TAS OPN Other`. Each carries a
  pa_codes list for aggregation.
- Three new workbook-scope defined names: `MRO_TAS_OPN_BA7_FY25`,
  `MRO_TAS_OPN_BA8_FY25`, `MRO_TAS_OPN_BAOTHER_FY25`.
- Dispatch loop extended to handle `tas_pa` alongside existing `data`
  / `memo` / `tas` / `formula`.
- TAS Total rollup formula unchanged - it only sums the 10
  appropriation parent rows, so the PA sub-rows do not double-count.

Budget Anchors now: 36 line items across 5 sections, **33 named
cells** (up from 30 in v2.79).

### 6. Services sheet reconciliation block

`sheets/services.py::_write_mro_budget_reconciliation`:

- After the OPN parent row (MRO_TAS_OPN_FY25) emits, loop injects 3
  sub-rows referencing MRO_TAS_OPN_BA7/BA8/BAOTHER.
- Sub-row column D (`% of TAS Total` header) shows % of OPN parent
  instead of % of grand total, since the nested hierarchy makes OPN
  the natural denominator. Notes column flags the distinction.
- Ordinary appropriation rows unchanged.

### 7. Slide 5 mockup updates

`SLIDE5_APPROPRIATION_SOURCING_MOCKUP.md`:

- Subtitle extended: "OPN drilled to Budget Activity."
- Left-visual table reshaped as a nested hierarchy: OPN parent bar
  with three BA sub-bars (BA-7 / BA-8 / Other).
- Takeaway table OPN row rewritten: "OPN splits 62% Command Support
  Equip / 32% Spares -- depot availabilities funded through BA-7, not
  through OMN CE 928."
- Named-cells count updated (11 -> 14 TAS-attributed, inc. 3 OPN BA
  sub-rows).

### 8. Build v2.80

Smoke-tested `_load_opn_pa_split()` + `create_budget_anchors()` in
isolation. Confirmed:

- Loader returns 7 PA codes with correct $ totals.
- Budget Anchors writes 36 rows; 4 rows named with OPN in line label
  (TAS OPN + 3 sub-rows).
- Defined names `MRO_TAS_OPN_BA7_FY25` / `_BA8_` / `_BAOTHER_` point
  at `'Budget Anchors'!$E$8` / `$E$9` / `$E$10`.

Ran full build: `python3 -m domnann.build_from_data`. v2.79 auto-
archived. v2.80 saved. Sheet order unchanged. No build errors.

---

## Files created

- `data_pull/classify_opn_pa_split.py` - new per-(award, PA)
  aggregator for OPN.
- `data_pull/output/usaspending/approp_opn_pa_split.json` - rollup
  artifact (7 PA rows + coverage metadata + global direct ratio).
- `deck/SLIDE6_DEPOT_DEEP_DIVE_MOCKUP.md` - new depot deep dive
  mockup.
- `sessions/SESSION_2026-04-18_viii_deck_finalization_opn_pa_drill.md`
  - this file.

## Files modified

- `sheets/budget_anchors.py` - OPN PA loader + tas_pa row kind +
  dispatch.
- `sheets/services.py::_write_mro_budget_reconciliation` - inject OPN
  PA sub-rows inline under the OPN parent.
- `deck/SLIDE5_APPROPRIATION_SOURCING_MOCKUP.md` - full rewrite
  (renamed from SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md).

## Files renamed

- `deck/SLIDE3_MRO_BUDGET_ANCHOR_MOCKUP.md` ->
  `deck/SLIDE5_APPROPRIATION_SOURCING_MOCKUP.md` (then rewritten).
- `deck/SLIDE5_SUB_CARRIER_SCOPE_MOCKUP.md` ->
  `deck/SLIDE7_SUB_CARRIER_SCOPE_MOCKUP.md` (content unchanged).

## Files unchanged (intentionally)

- `build_from_data.py` - no new sheets.
- `data_pull/classify_approp_colors.py` - original classifier
  untouched; new PA drill is additive.
- `approp_rollup_imputed.json` - unchanged; new PA split is a sibling
  artifact.
- `DECK.md` - still reflects delivered state only.
- `docs/methodology/*` - not updated this session; the headline
  narrative (OPN as a major MRO funder, OMN CE 928 as only a partial
  anchor) is unchanged.

## Memories added

None.

---

## Workbook progression

| Version | Change | Impact |
|---|---|---|
| v2.79 -> v2.80 | Budget Anchors gains 3 OPN Program Activity sub-rows (BA-7 / BA-8 / Other BAs) with named cells; Services reconciliation block injects matching indented sub-rows under the OPN parent. | Budget Anchors: 33 -> 36 line items, 30 -> 33 named cells. Services reconciliation block: +3 rows (nested under OPN). No other sheet, row count, or total changed. |

v2.80 is current.

---

## Open flags

- **v2.80 not opened in Excel yet.** Smoke test confirms formula
  strings + defined names resolve; only Excel evaluation confirms the
  rendered numbers match the smoke-test expectations. Expect
  Budget Anchors E8/E9/E10 = 1,591,498 / 824,996 / 171,342 ($K) and
  Services reconciliation column D for the sub-rows to show
  61.5% / 31.9% / 6.6% of OPN.

- **Slides 5, 6, 7 not yet drawn.** Three mockup files in `deck/`
  describe what should go on each. DECK.md will not be updated until
  each slide is redrawn in the deck app and a screenshot is captured.

- **Workbook-scope-to-deck cleanup not started.** User's end goal was
  to finalize deck THEN prune the workbook to only data tables the
  deck needs. Mapping from (finalized) slides to sheets / sections:

  | Slide | Sheets used | Sections used |
  |---|---|---|
  | 1 TAM & Scope | Services, Overview | TAM headline only |
  | 2 Vessel Mix | Services | Vessel Type x Work Segment crosstab |
  | 3 Work Segments | Services | Work Segment rollup + coverage table |
  | 4 Prime Landscape | Services | Top Contractors + market share per segment |
  | 5 Appropriation Sourcing | Budget Anchors, Services | TAS Attribution section; Budget Reconciliation block |
  | 6 Depot Deep Dive | Depot Ship Repair, J998 J999 Data | Most of the sheet |
  | 7 Sub & Carrier Scope | Sub & Carrier Coverage, Budget Anchors | Scope reconciliation + SCN anchors |

  Sheets with no deck role: **Product Procurement** (no newbuild
  slide proposed), **Sub Ratios** (not referenced), **Public Comps**
  (not referenced), **Subcontract Data** (not referenced),
  **Awards** (data backend; keep), **Vessel Taxonomy** (reference
  lookup; keep). Proposed deletion candidates: Product Procurement,
  Sub Ratios, Public Comps, Subcontract Data. Worth a final
  confirmation pass with user before removing anything.

- **data_v2.xlsx join for program-level specificity** still possible
  via path B (probabilistic match on hull + PSC + contracting office).
  Not done this session; would give "likely program" labels on
  specific high-$ awards (Boise EOH, Draper Trident, specific Columbia
  line items). Not worth pursuing unless a specific deck claim needs
  it.

- **Depot deep dive mockup numbers are approximate.** The RMC x tier
  crosstab and Tier-1 prime roster on
  `SLIDE6_DEPOT_DEEP_DIVE_MOCKUP.md` are drawn from earlier session
  notes and should be snapped to live Depot Ship Repair sheet values
  when the actual slide is drawn. IDV scope group numbers are exact
  from the classifier output.
