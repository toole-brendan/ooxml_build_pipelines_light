# Workbook TAM Calculation Changes — Integrating PSC 1905 Embedded MRO

_Companion to [ANSWER_psc_1905_embedded_mro.md](ANSWER_psc_1905_embedded_mro.md). Scoped to changes needed in `build_script_slim/output/08APR2028_MRO_Spend_v4.5.xlsx` (and its upstream builders) so that every TAM figure, Mekko, Prime Landscape, and reconciliation block in the deck source reflects the locked $1,904M PSC 1905 embedded MRO number. Deck copy edits (slide titles, lede text) are out of scope — that work is flagged in `PLAN_deck_revisions.md`._

## Headline change

The workbook currently anchors on **Services MRO TAM = $7,067M** (68 services PSCs, FPDS-post-exclusion). The PSC 1905 classifier work locks an additional **$1,904M of embedded MRO (Central)** that sits under PSC 1905 at SUPSHIP-administered yards (Electric Boat, HII Newport News, HII Ingalls). Every downstream TAM calculation needs to adopt a **Reconciled FPDS-visible MRO TAM of $8,971M** ($7,067M + $1,904M) as the denominator.

## What's already wired in the workbook

From the ANSWER doc sections 5.2 and 8, the Reconciliation sheet already defines:

- `PSC1905_MRO_EMBEDDED` = 1904 (Central)
- `PSC1905_MRO_SUBS` = 1255
- `PSC1905_MRO_CARRIERS` = 337
- `PUBLIC_SHIPYARD_NWCF` = 7500 (separate anchor, not in TAM)

The classifier's per-PIID output (`build_script_slim/output/psc_1905_classified.csv`) is generated but **not loaded into the workbook as a sheet**. All chart-source SUMIFS still run against the `Awards` and `J998J999Data` tables only.

## What's NOT yet wired

Every chart-source table on the Output sheet computes FY25 $M via `SUMIFS(Awards[FY2025 Obligation], Awards[PSC], {J/K/N/M/H/L services PSCs}, ...)`. None of those SUMIFS include PSC 1905 or reference `PSC1905_MRO_EMBEDDED`. So every TAM figure in the deck currently structurally excludes the $1,904M embedded PSC 1905 MRO.

### Attribution gap

The ANSWER doc locks the $1,904M headline and breaks it down by **vessel supergroup** (§4.3). But to feed the chart blocks below, we also need the $1,904M disaggregated along two axes that aren't yet in `psc_1905_summary.json`:

| Axis | Status |
|---|---|
| Vessel supergroup (Subs / Carriers / Surface Combatants / Unclassified) | **Locked** — ANSWER §4.3 |
| Work segment (Depot Ship Repair / HM&E / Combat Systems / C4ISR / Port & Tech) | **Not locked** — but per ANSWER §4.4 top anchors (SHT Seam Split Repairs, USS Boise EOH, CVN 68 Inactivation, USS Eisenhower PIA, DDG 1000 BYMP), virtually all $1,904M is Depot Ship Repair character. Treat as 100% Depot unless per-PIID review says otherwise. |
| Corporate parent (Electric Boat → GD / HII NN + Ingalls → HII / Metro Machine → HII / other) | **Not locked** — needs per-PIID Corporate Parent rollup added to `psc_1905_classified.csv` (top candidates from ANSWER §4.4: Electric Boat ~$900M+, HII ~$600M+) |

---

## Changes by workbook block

Row references use the Output sheet unless otherwise noted.

### A. Output sheet title (A1)

- Current: `Output -- Navy + Coast Guard FY2025 MRO TAM -- $7,067M (FPDS awards, PSC-filtered)`
- New: `Output -- Navy + Coast Guard FY2025 Reconciled MRO TAM -- $8,971M (Services $7,067M + Embedded PSC 1905 MRO $1,904M)`

### B. Slide 4 / Target S5 — TAM Sizing Approach (r19–33)

Current funnel is 3 rows: `Active PSCs → Services-class → Ship MRO PSCs × FY25 obligations = $7,067M`.

Change: add a 4th flow row after r26 for the PSC 1905 reconciliation addback:

```
Step 4 | + Embedded PSC 1905 MRO (SUPSHIP bundling) | Ship MRO TAM $7,067M | + | $1,904M classifier-locked | = | Reconciled MRO TAM | $8,971M
```

This preserves the existing 3-step derivation and makes the PSC 1905 uplift visible as a separate reconciliation step rather than burying it inside the services-PSC filter.

### C. Slide 7 / Target S8 — MRO Work Segments (r35–45)

Current 5-segment 100% stacked column sums to $7,067M. Embedded PSC 1905 MRO is Depot Ship Repair character (see Attribution gap above).

**Decision needed:** roll the $1,904M into the Depot Ship Repair row (r40) or add a 6th row.

- **Recommend roll-in** (cleanest narratively — PSC 1905 MRO *is* depot work). Depot row formula changes:
  - Before: `=SUM(SUMIFS(Awards[FY2025 Obligation], Awards[PSC], {"J998","J999"}))/1000000`
  - After: `=SUM(SUMIFS(Awards[FY2025 Obligation], Awards[PSC], {"J998","J999"}))/1000000 + PSC1905_MRO_EMBEDDED`
  - Coverage text (D40) needs a footnote: "Includes $1,904M of embedded PSC 1905 depot MRO at SUPSHIP yards (EB, HII NN, HII Ingalls) — see Scope Reconciliation."
- All 5 % shares recalculate against the $8,971M denominator. Expect Depot Ship Repair share to grow materially (largest absolute and relative change).

### D. Slide 6 / Target S9 — TAM Composition Marimekko (r49–58)

Mekko columns: 6 vessel buckets × 5 work-segment rows. Per ANSWER §4.3, PSC 1905 embedded MRO attribution by vessel:

| Vessel column | PSC 1905 MRO uplift | Where it lands |
|---|---:|---|
| Surface Combatants | +$119M | Depot row (r54), column B |
| Amphibious Warfare Ships | $0 | no change |
| Submarines | **+$1,255M** | Depot row (r54), column D |
| Combat Logistics Ships | $0 | no change |
| Aircraft Carriers | **+$337M** | Depot row (r54), column F |
| Other | +$193M | Depot row (r54), column G (from Unclassified-vessel per ANSWER §4.3) |

Per-cell formulas on r54 need to add `+ (named range for that vessel's PSC 1905 MRO slice)`. New named ranges needed on Reconciliation sheet: `PSC1905_MRO_SURFCOMBS` = 119, `PSC1905_MRO_UNCL` = 193 (sibling to the existing `_SUBS` and `_CARRIERS`).

Mekko column widths will re-proportion — Submarines column ~+150% wider, Aircraft Carriers ~+80% wider.

**Decision flagged in ANSWER §5.3:** "add a 6th Marimekko category 'Embedded Submarine/Carrier MRO' or footnote the uplift." Recommend footnote + absorb into Depot row per above for consistency with Slide 7 rollup choice.

### E. Slide 11 / Target S13 — Depot Spend Structure (r105–129)

Headline block (r107–111) currently: `Gross J998+J999 → less FMS → In-Scope Depot TAM`. Mekko is scoped to J998/J999 availabilities only.

PSC 1905 embedded MRO is depot-character but sits **outside the J998/J999 availability taxonomy** — SUPSHIP work runs on EOH / RCOH / SHT / Seam Split Repair availability types that don't exist in the J998/J999 data. Adding it into the Mekko would mix two incommensurable classification schemes.

**Recommend:** leave the Mekko scoped to J998/J999, but add one reference row to the headline block:

```
r112 (new): + Embedded PSC 1905 MRO (SUPSHIP, reference only) | =PSC1905_MRO_EMBEDDED
r113 (new): Depot TAM including PSC 1905 embedded (reference)  | =B111 + B112
```

Mekko cells (r116–120, 125–129) unchanged. Slide footnote: "Mekko shown is J998/J999 only; an additional $1,904M of depot-character MRO is bundled under PSC 1905 at SUPSHIP yards (EB, HII NN) — not included in this chart; see Scope Reconciliation."

### F. Target S11 — Marauder-Like Fleet MRO (NEW per TARGET_deck_structure.md)

Marauder comp-set is T-AKE, T-AO, T-AOE, LMSR (T-AKR), USNS Cape, T-EPF, auxiliaries — all auxiliaries / MSC-managed hulls. Per ANSWER §4.3 the PSC 1905 embedded MRO is entirely Submarines + Carriers + Surface Combatants + Unclassified, with **zero auxiliaries**.

**No change** to Marauder-Like Fleet MRO from PSC 1905 reconciliation. (The chart itself still needs to be built per the AUDIT doc, but PSC 1905 doesn't affect its numbers.)

### G. Target S12 — SAM Sizing (NEW per TARGET_deck_structure.md)

SAM = Marauder-like ∩ Depot ship repair. Marauder-like is auxiliaries; auxiliaries depot work is in J998/J999, not PSC 1905.

**No change** to SAM Sizing from PSC 1905 reconciliation.

### H. Slide 15 / Target S17 — Prime Landscape — TAM (r162–181)

Top-10 ranking by total services MRO $ will shift materially once PSC 1905 embedded MRO is included:

- **General Dynamics** (currently r164 col C, rank #2): +$900M+ expected via Electric Boat (ANSWER §4.4 top PIIDs: $831M SHT Seam Split Repairs + $38M NEMMI + $36M NRMD + $54M DDG 1000 BYMP ≈ $959M)
- **Huntington Ingalls Industries** (currently r164 col D, rank #3): +$600M+ expected via HII NN + Metro Machine (ANSWER §4.4: $424M USS Boise EOH + $97M CVN 68 inactivation + $45M CVN 69 PIA + $26M Comprehensive Incomplete Work List ≈ $592M)
- **BAE Systems** (rank #1): no PSC 1905 exposure — unchanged
- Others in top-10 (Vigor, Draper, Detyens, Epsilon, East Coast Repair, Lockheed, SCA): no material PSC 1905 exposure expected

Rank order likely shifts: GD could overtake BAE; HII could close the gap to GD. The Depot Ship Repair stack segment grows for GD and HII specifically.

**Change needed:**

1. Per-prime PSC 1905 MRO rollup. Requires adding a Corporate Parent column to `psc_1905_classified.csv` (mapping via the same recipient-to-parent lookup used for Awards) and summing per parent. Recommended: expose as named ranges `PSC1905_MRO_GD`, `PSC1905_MRO_HII`, `PSC1905_MRO_OTHERS`.
2. r171 `Total MRO $M` formula for GD column: `= <existing services sum> + PSC1905_MRO_GD`; same for HII column.
3. Re-rank the top-10 columns if parents change positions.
4. The secondary `#1 / #2 / #3 per Work Segment` block (r175–181) for Depot Ship Repair row (r177): top-3 for depot now needs to consider combined J998+J999+PSC 1905 MRO totals per prime. Likely new order: #1 BAE (J998/J999 dominant), #2 GD (EB pulls it up), #3 HII (NN + Metro Machine pull it up).

### I. Slide 16 / Target S18 — Prime Landscape — Depot (r185–220)

Scoped to J998+J999. Same logic as the Depot Spend Structure decision (E) — PSC 1905 depot work is outside J998/J999 scope.

**Recommend:** add a reference row to the headline block (r187–191) mirroring E above; leave the ranked stacked column and prime × RMC crosstab unchanged in scope. Footnote on slide: "Ranked depot primes shown are J998/J999 only; Electric Boat + HII Newport News have an additional combined ~$1.5B of SUPSHIP depot MRO bundled under PSC 1905 — see Scope Reconciliation."

Alternatively, if the narrative demand is "who competes for depot work at all," expand the ranking to include PSC 1905 MRO. Decision open.

### J. Slide 20 / Target S22 — Scope Reconciliation (r224–254)

Primary block (r228–230) waterfall: 5 columns, bar-type codes `s d d d e`.

Current flow:
```
Total Navy+USCG ship spend (s) → Less Newbuild (PSC 1905) (d) → Less Public-yard labor (d) → Less Reactor proc PSC 4470 (d) → FY2025 MRO contracting TAM (e)
```

The "Less Newbuild (PSC 1905)" subtracts all $38,053M of FY25 PSC 1905. That's wrong once $1,904M of it is locked as MRO.

**Recommend restructure** to 7 columns with bar codes `s d d d d d+ e`:

```
Total Navy+USCG ship spend (s)
→ Less Pure-Newbuild PSC 1905 ($36,149M, i.e., $38,053M total − $1,904M embedded MRO) (d)
→ Less Implied public-yard labor (OMN 1B4B − CE 928) (d)
→ Less Reactor procurement (PSC 4470) (d)
→ Services MRO TAM (staging value $7,067M) (d, mid-total)
→ + Embedded PSC 1905 MRO ($1,904M) (d+, negative-decrement / positive add)
→ Reconciled FPDS-visible MRO TAM ($8,971M) (e)
```

Alternatively, keep 6 columns and net it (`Less Pure-Newbuild PSC 1905 $36,149M`) without the explicit addback — less auditable but simpler visually. Decision open; recommend the 7-column structure for auditability.

Formula changes:
- r229 (FY2025 $M row) needs new column values.
- r230 (bar type) needs updated codes and one or two new columns.
- r228 (Category / Series labels) needs updated labels.

Secondary block: **"Nuclear MRO PSC emptiness"** (r250–254). Currently shows J044/K044/N044 as empty to support the narrative "nuclear MRO isn't in our TAM." The PSC 1905 finding flips this: **nuclear MRO IS in the TAM**, it's just routed through PSC 1905 at SUPSHIP yards rather than the nominal nuclear J/K/N codes. The block still has factual value (the J044/K044/N044 emptiness is real) but the narrative lede changes from "nuclear MRO is excluded" to "nuclear MRO is bundled under PSC 1905, not under the nominal nuclear PSCs — see primary waterfall add-back." No formula changes; only framing (text) changes.

### K. Slide 10 / Target S23 — Appropriation Sourcing (r62–101)

Column 1 rebases TAS-attribution $M values to the services TAM basis via `MRO_TAS_*_FY25 * (NAVY_TAM_SVC + CG_TAM_SVC) / MRO_TAS_TOTAL_FY25` (see formulas in r66–72).

Two levels of change possible:

1. **Light touch (recommended):** Keep Appropriation Sourcing scoped to services TAM ($7,067M basis), add one annotation on the slide: "+ $1,904M embedded PSC 1905 MRO is funded primarily via SCN 017-1611 and is not rebased into this breakdown; see Scope Reconciliation." Rationale: attributing the $1,904M across appropriations is speculative for the $1,669M non-Tier-0 remainder, and disrupts the existing services-TAM rollup logic.

2. **Full attribution:** Add an SCN column to the dual 100%-stacked or redistribute. The $235M Tier 0 upgrades have real TAS data in `psc_1905_funding_agg.json`. The $1,669M remainder would impute to SCN (017-1611) or via peer ratios. SCN row would jump from current ~$40M to ~$1.7B+, materially reshaping the appropriation mix. Bigger build, bigger narrative shift.

Recommend path 1 unless deck narrative specifically wants the appropriation-mix impact surfaced.

### L. Reconciliation sheet — add named ranges

Current anchors block has `PSC1905_MRO_EMBEDDED`, `PSC1905_MRO_SUBS`, `PSC1905_MRO_CARRIERS` (r5–7). Add siblings:

| New named range | Value | Source |
|---|---:|---|
| `PSC1905_MRO_SURFCOMBS` | 119 | ANSWER §4.3 |
| `PSC1905_MRO_UNCL` | 193 | ANSWER §4.3 |
| `PSC1905_MRO_AMPHIB` | 0 | ANSWER §4.3 (zero but explicit) |
| `PSC1905_MRO_LOGISTICS` | 0 | ANSWER §4.3 (zero but explicit) |
| `PSC1905_MRO_TIER0` | 235 | ANSWER §4.1 (TAS-confirmed subset) |
| `PSC1905_MRO_GD` | tbd (~$900M+) | Needs per-parent rollup added to classifier output |
| `PSC1905_MRO_HII` | tbd (~$600M+) | Needs per-parent rollup added to classifier output |
| `PSC1905_MRO_OTHER_PRIMES` | tbd | Needs per-parent rollup added to classifier output |
| `RECONCILED_MRO_TAM` | =NAVY_TAM_SVC+CG_TAM_SVC+PSC1905_MRO_EMBEDDED | Drives deck-wide $8,971M headline |

### M. Services sheet — secondary updates

- Rows 217–220 "FY2025 MRO TAM" block: add row "+ Embedded PSC 1905 MRO" = `PSC1905_MRO_EMBEDDED`. New summary row "Reconciled MRO TAM" = `RECONCILED_MRO_TAM`.
- Rows 384–404 "FY2025 MRO TAM by Vessel Type × Work Segment ($M and %)": Depot Ship Repair row needs per-vessel uplift from PSC 1905 (Subs +$1,255M, Carriers +$337M, Surface Combatants +$119M, Other +$193M). Either add columns into this block or parallel it with a new "(including embedded PSC 1905 MRO)" block below.

---

## Optional upstream change: add `PSC 1905 Classified` sheet

The cleanest way to source per-vessel, per-prime, per-work-segment PSC 1905 MRO attribution for the Mekko and Prime Landscape blocks is to load `build_script_slim/output/psc_1905_classified.csv` into the workbook as a new sheet (parallel to the `Awards` sheet) and drive attribution via SUMIFS against it.

Requires:

1. Loader in `build_script_slim/build_from_data.py` that appends `psc_1905_classified.csv` as a sheet
2. Join Corporate Parent column onto the 201 PIIDs (use the same recipient → parent lookup as Awards)
3. Work segment column — populate as "Depot Ship Repair" for all `MRO (*)` bucket rows (per ANSWER §4.4 character-based assumption)
4. Filter column: `is_mro = TRUE` where bucket ∈ {MRO (strong), MRO (TAS-confirmed), MRO (probable)} to match the Central $1,904M definition

This makes every downstream rollup auditable at the PIID level (match the Awards-sheet pattern) and removes the need for per-parent, per-vessel named ranges. Recommended if more than one iteration of the deck is expected, since the classifier may be rerun and supergroup amounts may shift.

---

## Decision checklist — confirm before editing

1. **Headline basis:** Replace deck-wide $7,067M with $8,971M reconciled? (ANSWER §5.3 recommends; I concur.)
2. **Work Segments stack (Slide 7):** Roll embedded MRO into Depot row + footnote, or add 6th row?
3. **TAM Composition Mekko (Slide 6):** Absorb per-vessel uplift into Depot row per ANSWER §4.3, or show as a footnote only?
4. **Depot Spend Structure (Slide 11):** J998/J999 Mekko stays scoped as-is with reference-only headline addition, or expand to include SUPSHIP column?
5. **Prime Landscape TAM (Slide 15):** Re-rank including PSC 1905 MRO per parent — confirm we want GD/HII re-scoring?
6. **Scope Reconciliation waterfall (Slide 20):** 7-column version with explicit addback, or 6-column netted "Pure-Newbuild PSC 1905 $36,149M" version?
7. **Appropriation Sourcing (Slide 10):** Light-touch annotation, or full PSC 1905 attribution across appropriations (SCN row blows up)?
8. **Upstream sheet-level change:** Load `psc_1905_classified.csv` as a new sheet for auditable per-PIID rollups, or keep attribution in named ranges only?

---

## Out of scope for this integration

- **$1,904M vs $2,057M upper bound.** Central is locked per ANSWER §4.2. Adding MRO (POP-only) $153M could move the Depot Ship Repair stack by ~2% and would not change any ranking or denominator materially. Keep Central.
- **Public naval shipyard NWCF labor** (~$7,500M, `PUBLIC_SHIPYARD_NWCF`). Separate anchor; lives only on S22 Scope Reconciliation as "outside FPDS, adjacent to TAM." Already handled.
- **Deck copy edits** (slide titles, leads, coverage cards). Flagged in `PLAN_deck_revisions.md` Step 3; will happen once `deck_script/` sources land in `branmut/`.
