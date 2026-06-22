# Tentative plan — evolving `award_classification` (foundation first, then "where to play")

**Status: TENTATIVE — re-cut 2026-06-20.** This revision folds in (a) the 2026-06-20 audit of the
*current* workbook, (b) **two deep-research methodology passes** (an initial report + a follow-up that
corrected two things), and (c) a **direct data audit** that sized the dedup / cumulative-restatement risk.
Lives at the `sam/` root because it spans both sub-projects: it ports an *improved* contestability
("where to play") analysis onto the go-forward `award_classification` workbook, after a foundation block.

> Planning doc only — not being implemented yet. The research-pack the methodology came from lives at
> `/Users/brendantoole/projects3/sam_award_methodology_research_pack/`.

---

## Context

`sam/` holds two workbooks:

- **`award_analysis`** — `20260612_…Award Analysis_vS.xlsx`. The original contestability / market-entry
  analysis. **Frozen since 2026-06-16**; methodology judged not good enough → restarted. **But it is not
  worthless** — it already built a five-signal contestability funnel (materiality, concentration, entrant
  rate, cadence/churn, **barrier + seeding evidence**) plus two honesty fixes. Several pieces are *assets to
  salvage*, not discard (see PART B).
- **`award_classification`** — `award_classification_refactor.xlsx`. The go-forward workbook. Currently a
  *labeling* layer (Domain / Role / Output archetypes + raw transaction port) on the **hull-builder-directed
  subset**.

**Direction:** `award_classification` supersedes `award_analysis` — a foundation block, then an *improved,
more honest* contestability layer. Guiding posture (unchanged, now reinforced by both research passes):
**defensibility over completeness.** The honest output is a *prioritized investigation queue* with disciplined
disclosure — not a market-sizing census or a recompete-date forecaster.

## What the data audit established (2026-06-20) — load-bearing

Verified directly against the current `extracted/*.csv` (20,623 records). These supersede looser earlier
statements; **do not re-derive**:

- **Dedup status.** The data IS deduplicated on `Subaward Report ID` (0 duplicate report IDs). It is **not**
  collapsed to one row per real subcontract. Two distinct issues remain:
  - **Exact-duplicate report rows** (field-identical but for Report ID): **$247.7M ≈ 2.0% of total**
    (DDG 3.1% / Virginia 2.5% / Columbia 0.2%). Near-certainly duplicate filings → **excludable under an
    exact-duplicate rule.** Label it "excluded under the exact-duplicate rule," not a *proven* overstatement.
  - **Re-filing multiplicity.** Collapsing to instruments (prime UEI + sub UEI + normalized subaward number)
    yields ~4% fewer instruments than rows for DDG, but **~36% (Virginia) / ~28% (Columbia)**. 122 instrument
    groups span >1 Prime Contract Key.
- **The dollar total is "published signed report flow," not validated obligations.** A monotonicity test sized
  the cumulative-restatement exposure: after the exact-dup exclusion ($12.24B), **up to ~$685M (5.5%) more is
  at risk** of double-counting if monotonic re-files are cumulative restatements — and a *larger*
  non-monotonic band (Virginia $2.6B / Columbia $1.6B) is irreducibly ambiguous from the fields alone. So the
  economically-true total is **below $12.24B, plausibly ~$11.5–12.2B, unresolvable without prime
  purchase-order registers.** **DDG is clean; the risk is a submarine-program phenomenon.**
- **Corollary (the key reframe):** instrument-collapse fixes **counts and cadence** — it does **not** yield a
  clean dollar number. Do **not** reconstruct/publish a per-subcontract "obligated value." Separate instrument
  *identity* (for counting/timing) from monetary *flow* (disclosed as signed report flow, never reconstructed).
- **SWBS coverage** (DDG/HII subset): deterministic, observed-only crosswalk; 113 of 365 HII work-item codes
  map (each to exactly one SWBS group, no conflicts); **~70% of dollars but only ~30% of records.** Publishable
  as a mapped-core view — **do not impute the tail.**
- **Prime-award pull is cheap and already tooled** (FPDS Atom + USAspending + SAM, per
  `/Users/brendantoole/projects3/Federal_Award_API_Research_Methodology.docx`). It yields prime-level PoP end
  dates, per-mod option/award actions, obligated-per-action, IDV links, competition fields — at the *prime*
  level (not sub level).

### Audited current state — do NOT re-litigate (already implemented)
- `Published Subaward Records` is the rendered column (COUNTIFS) in all 3 vendor sheets — not "Subaward Actions."
- `Predominant Place of Performance (by records)` — the "Domestic/Foreign" rename is done.
- `Total Contract Value $` is never aggregated (context-only; one prime key shows up to 65 distinct TCVs).
- Dollars already labeled "nominal" in every sheet intro.
- **Full SWBS taxonomy is authored** (legend, mapping-method `E/X/C/L/U`, hierarchy, guardrails, §9). Only
  *application* to data is missing (Phase 3) — and the crosswalk itself already exists in
  `ddg_hii_swbs_subaward_package/`.
- **R (Operating Role) is a defined axis** (D/R/P) — just not a published column.

### Verified data facts (measured 2026-06-20)
- **20,623 records** — DDG 6,380 / Virginia 8,443 / Columbia 5,800. Report IDs unique, no cross-file overlap.
- **1,191 distinct UEIs** across 1,685 UEI×program rows; 399 UEIs on >1 program.
- 458 UEI×program rows missing primary NAICS; 832 negative amounts + 2 zeros (negatives are real adjustments).
- Subaward-date ranges: DDG 2001-10-22→2026-05-27, Virginia 2013-01-28→2025-08-22, Columbia 2016-01-06→2025-02-18.
- **Only ONE record predates 2013** (a 2001 DDG record) — corrects the earlier "~4" claim; no deflator
  back-extension problem.
- Country codes unstandardized (`CA`/`CAN`, `GB`/`GBR`).

---

## PART A — Foundation ("for-sure" block)

Every phase keeps the workbook building green and reconciles to the Phase 0 baseline. None commits us to the
PART B methodology.

### Phase 0 — Baseline & safety
- Commit current green state (workbook + `extracted/*.csv` + scripts) to git; snapshot `.xlsx` + CSVs (`.pre_*`).
- Record tie-outs (raw $12.487B, the $12.24B after-dedup figure, per-program $, sheet/table/note counts).

### Phase 1 — Instrument & observability layer (the new prerequisite)
Promoted to foundation because *any* honest count or timing claim depends on it. Two parts; only 1a is strictly
low-regret, but 1b is cheap and disclosure-only.

- **1a — instrument identity (for counts/cadence, NOT dollars).** Collapse report rows into reported
  subcontract instruments using **two keys**: conservative (`program + prime UEI + sub UEI + normalized
  subaward number`) and split (adds Prime Contract Key). Carry a `duplicate_cluster_id`, `cross_prime_key_flag`,
  `ledger_ambiguity_flag`, and a **lineage table preserving every child Report ID** (never discard a raw row).
  Apply the exact-duplicate exclusion rule.
- **1b — observability flags.** Time-varying **reporting-threshold regime** (~$25k pre-Oct-2015, ~$30k through
  Sep-2025, ~$40k from Oct-2025 — *verify exact dates against FAR 52.204-10 / 4.14 before hard-coding*);
  **recent-period incompleteness** flag (FFATA/FSRS lag); **first-tier-only** flag; **vendor-of-record masking**
  flag (Newport News / GDEB).
- **Dollar posture:** carry `raw_published_signed_flow`, `positive_reported_flow`, `negative_reported_adjustments`
  at report grain; at instrument grain carry the net signed flow **explicitly labeled "associated flow," not
  instrument value.** Never publish a reconstructed per-subcontract obligated value.
- **Exit:** green; totals reconcile to baseline; instrument + lineage tables exist; flags present.

### Phase 2 — Month/date dimension → derive both CY and FY + recent-period flag
- Make the base grain a **month/date dimension**; derive **both** CY and FY (don't convert). FY driven by
  `subAwardDate`. Carry `Submitted Date`, `first_observed_submitted_date` (instrument grain),
  `submission_lag_days` — cheap now, expensive to reconstruct later, and required for any vintage backtest.
- Implement in the 3 corpus-derived build scripts, not shared `_corpus`. Fix the date-range captions here.
- Independent of Phase 1; can run in parallel.
- **Exit:** green; totals unchanged; month/CY/FY derivable; recent periods flagged.

### Phase 3 — Apply SWBS to DDG transactions (observed-only)
- Apply the **existing deterministic crosswalk** (`ddg_hii_swbs_subaward_package/`) to the 5,900 HII-Ingalls
  rows; populate `subsystem` on HII-DDG rows (null elsewhere). **Do not impute the unmapped tail.**
- Carry `swbs_scope_eligible`, `swbs_mapped`, `swbs_code`, `swbs_mapping_method`, `swbs_confidence`,
  `swbs_crosswalk_version`, `swbs_multi_system_flag` (primary code + flag; no dollar splitting; leave unmapped if
  no defensible primary).
- **Presentation discipline (publishable at ~70% $ / ~30% records):** state coverage on every display; show
  eligible / mapped / **unmapped** explicitly; give **two shares per subsystem** — *within-mapped* and *minimum
  share of all eligible HII-DDG dollars* (the second stops a mapped-core share being read as a universe share).
  Distinguish `out-of-scope` from `eligible-but-unmapped`. Never use the SWBS distribution as an all-DDG
  denominator; never compare SWBS across programs.
- **DDG-only.** Independent of Phases 1–2.
- **Exit:** green; DDG rows carry `subsystem`; coverage + two-share reporting in place; cross-program comparison blocked.

### Phase 4 — FY2026$ standardization (manager-mandated; scope-limited)
- **Re-basing decision (the real question):** deflation only changes **cross-year dollar comparisons**
  (multi-year sizing/trends/pooled concentration where the year-mix differs). It does **not** change counts,
  timing, within-year shares/HHI, or anything that is a ratio. The stakeholder **mandates FY2026$ output**, so
  implement it — but as a **parallel derived view used only on the cross-year cuts**, nominal as system of record.
- Carry: `published_nominal_amount`, `analytic_nominal_after_exact_duplicate_rule`,
  `analytic_FY2026_procurement_price_equivalent` = nominal × (102.10 / Procurement-index at FY(subAwardDate)).
- **Basis:** FY25 Green Book Table 5-4 Procurement, project-local (do not mutate `workbook_core.deflators`).
  Use the actual FY2001 index for the single pre-2013 record (no flooring). Label the column: *"FY2026
  procurement-price equivalent — FY25 Green Book; action-date basis; FY2026 factor is a budget assumption."*
- Add a per-lane `deflation_changes_decision` flag (fires when deflation moves materiality status / priority
  band / rank). Do **not** imply the conversion estimates supplier-specific cost inflation, nor apply a single
  index as if it fit a heterogeneous bundle (materials/electronics/engineering/services).
- Depends on Phase 2.
- **Exit:** green; nominal + FY2026$ side by side on cross-year cuts; decision-impact flag present.

### Optional / minor refinements
- Rename `standardized Parent UEI` → `observed modal Parent UEI`.
- Place-of-performance cell value → dollar/record shares.
- (R as a column is no longer "optional polish" — see PART B: R belongs in the analytical unit as a coherence gate.)

---

## PART B — DEFERRED: the improved "where to play" analysis

Not started until the methodology is trusted. It is the SAME contestability funnel as `award_analysis`,
**hardened** — not a new paradigm. The three genuine upgrades over the frozen version (each confirmed by the
audit): instrument-collapse before any cadence; **probability-not-date** timing with a backtest gate;
**evidence-states not verdicts**.

### Concentration = a question, via four evidence gates (not a single score)
Compute, never collapse into one number:
1. **Observed reported structure** — top-1/top-3 share, **dollar HHI on *positive flow*** (signed shares can go
   negative), instrument-count HHI, effective supplier count (1/HHI), persistence. At **both** UEI and
   effective-dated control-family grain.
2. **Observed access behavior** (the one openness signal the data *can* see) — multiple control families in
   overlapping mature windows; switching; first-observed-family wins after a burn-in.
3. **Technical / commercial access** (the data *cannot* see this — external evidence) — IP/design authority,
   qualification regimes, SUBSAFE/nuclear/export, tooling, capacity. **Reuse `award_analysis`'s
   `barrier_scores.csv`** here; keep **seeding evidence separate** from barriers.
4. **Observability** — reporting maturity, threshold regime, vendor-of-record masking, mapped-dollar coverage,
   ledger-ambiguity. Wording: "observed reported first-tier concentration," never "monopoly."

### Buy-window radar — probability, gated, mostly "insufficient"
- Target = first action date of a **new reported instrument** in a lane (not "recompete," not "all buys").
- Hierarchical discrete-time recurrent-event hazard (cloglog) at lane-month grain; must **beat naive baselines**
  (trailing-rate, renewal, seasonal) and pass a **vintage backtest** (train only on `Submitted Date ≤ T`),
  scored on Brier + calibration. **Pre-registered predictability gate**; lanes that fail → `radar only` /
  `insufficient evidence`. Expect most lanes to fail — that is the honest outcome.

### Prime-event lag — collect now, model on a pilot
- **Pull complete prime history now** (cheap). **Gate the expensive modeling on a one-program HII-DDG pilot**
  (3–5 PIIDs, ≥5 mature years, 8–12 deepest lanes, 30–50 manually classified prime actions). Assume **zero
  incremental forecast value ex ante**; keep it only if it adds out-of-sample Brier skill (≥5% rel. at one
  horizon, no >2% deterioration at the other, ≥3 matured origins).
- **Highest-value use is NOT the forecast** — it's program-phase context (ramp/stable/tail, upcoming
  option/PoP milestones, "is a subaward decline just reduced prime exposure?"). Prime PoP = boundary/phase
  indicator, not inferred subcontract expiry; prime competition ≠ subaward competition.

### Units
- **Display lane:** `D×P`. **Calculation unit:** `program × buyer-of-record × D × P`, with **R as a
  coherence/heterogeneity gate** (an OEM and a build-to-print shop in one D×P are not substitutes — split or
  suppress). DDG-only `SWBS×P` as a mapped-universe appendix. **Reject** `PIID × work_type` (PIIDs churn).
- **Timing unit:** the deduped **subcontract instrument**, not the report row.

### Honesty guards — six families (the original three were necessary, not sufficient)
Observation/maturity · instrument identity (dup clusters, ambiguity flag) · supplier identity & **effective-dated
control family** (a current-parent rollup backcasts later M&A and erases historical competition) · lane coherence
· depth/materiality (distinct instruments/suppliers; largest-instrument share) · amount/adjustment sensitivity
(positive vs signed vs instrument-count; negative-adjustment ratio; exclude-ambiguous-ledger sensitivity → suppress
any conclusion that flips).

### Deliverable shape — a P × E decision queue (not a composite score)
- Two independent axes: **Action priority** (P1 investigate / P2 monitor / P3 deprioritize) × **Evidence state**
  (E3 forecast-certified / E2 opportunity-supported / E1 hypothesis / E0 not-assessable).
- Per-lane **card**: decision question · nominal + FY2026$ size · structure/depth · access evidence · barrier
  finding · seeding · timing status · observability + ledger-ambiguity flags · strongest contrary evidence ·
  single decision-critical unknown · next evidence action · owner to contact · upgrade/downgrade triggers.
- **Report the % of dollars and instrument-starts in each evidence state** — turns "few certified" into a
  measured coverage statement. Do **not** emit a 0–100 contestability score (implies materiality can offset bad data).
- Cross-program D/R/P spine; DDG-only SWBS drilldown appendix.

---

## Deliberately NOT doing (parked unless the workbook outgrows Excel)

- Full normalized relational model / ~20 typed tabs. Keep raw-vs-derived; most model tables = pipeline CSVs / hidden sheets.
- SCD-style versioning columns *everywhere* — **except one targeted exception:** effective-dated corporate-control
  families, **for material vendors only** (hand-curated; Parent UEI is too sparse/non-authoritative).
- Month-grain live Excel formula panels — do the panel work in **pandas at pipeline time**, surface summaries.
- `classification_evidence` / `sources` evidence-graph — premature (registry ~0 source URLs).
- **Reconstructing/publishing a per-subcontract "obligated value"** — the public ledger cannot support it;
  disclose signed flow + ambiguity instead.

---

## Critical path

```
Phase 0 → Phase 1 (instrument+observability) ─┬─ Phase 2 (month/CY/FY, ‖)
                                              ├─ Phase 3 (SWBS apply, ‖, DDG-only)
                                              └─ Phase 4 (FY2026$, depends on Phase 2)
                                                          │
                                                          ▼
              PART B — where-to-play  [deferred; prime pull collectable now, modeling gated on HII-DDG pilot]
```

## Open decisions

| # | Decision | Recommendation | Blocks |
|---|----------|----------------|--------|
| 1 | Austerity check: accept a prioritized **investigation queue** (few hard predictions) as the deliverable? | Yes — pre-socialize with the manager; it's the honest ceiling | Whole shape of PART B |
| 2 | Quantify the cumulative-restatement risk further? | Only resolvable with prime PO registers; otherwise disclose the ~$11.5–12.2B range | PART B sizing claims |
| 3 | Verify the reporting-threshold dates + Green Book indices before hard-coding | Verify FAR 52.204-10/4.14 + Green Book Table 5-4 | Phases 1b, 4 |
| 4 | Pull prime history now? | Yes (cheap); model only after the HII-DDG pilot proves skill | PART B radar |
| 5 | SWBS: publish observed-only at ~70%$/~30% records? | Yes, with the two-share presentation; no imputation | Phase 3 |

## Definite next step (pending go-ahead)
Phase 0 → **Phase 1 (instrument + observability)** as the new prerequisite, then **Phase 2 + Phase 3** in
parallel; decide **Phase 4 (FY2026$)** and the **prime pull** separately.

## Key facts & caveats to carry
- The base is the **hull-builder-directed subset**; filter lives in the 3 build scripts, not `_corpus`.
- **$12.487B = published signed report flow**, not validated obligations: −$248M exact-dups, up to −$685M
  cumulative-restatement candidates + an unbounded ambiguous band → true total ~$11.5–12.2B, submarine-driven.
- **Newport News gap:** HII-NNS ~invisible in the subaward stream (flows through GDEB as vendor of record).
  Understates submarine D1/P5; never read prime share as build share.
- `role`/`bucket` are a derived overlay — use the raw prime group as the scope lever.
- Per-firm classification changes: **audit + recommend first, wait for approval** before writing.
- Many domain shares are **1–2 contracts deep** — depth-flag before calling any lane contestable.
- **Salvage from `award_analysis`:** `barrier_scores.csv` + `seeding_evidence.csv` (the technical-access gate)
  and the two honesty fixes — don't rebuild what you already paid for.

---

## ADDENDUM — 2026-06-21: Phase 1 built, validated against the prime data, then reverted

*The plan above is left intact for the record. This addendum supersedes it on one specific question — the
re-filing / cumulative-restatement dollar risk — which we investigated and resolved.*

**Decision: Phase 1 (the instrument + observability layer) was implemented on a branch, then reverted. The dollar
double-count concern it was built to address turned out to be footnote-level**, confirmed by pulling the submarine
prime-contract obligations and cross-checking against USAspending. We are keeping the simple methodology (sum the
report rows).

### What we checked
- **Quantified the spread.** Re-valuing every instrument under competing interpretations (sum-all vs cumulative vs
  gross), the *credible* overstatement is ~2% (exact duplicates, near-certain) plus up to ~5–6% (monotonic
  "cumulative-candidate" instruments), submarine-driven; DDG is stable within ±1.5%. **45% of all dollars sit in
  single-report instruments with zero ambiguity.** (The −42% "cumulative = last filing" figure is an artifact of
  correction ledgers ending on a negative, not a credible bound.)
- **Pulled the 6 submarine prime contracts from USAspending** (open FPDS/USAspending, no API key — the
  `Prime Contract Key` already is USAspending's award id). Two findings settle it:
  1. **Subaward totals are ~9% of prime obligations** ($8.88B sub vs ~$95B obligated) — nowhere near the ceiling.
     The data *under*-captures real subcontracting (first-tier only, $30k floor, much contract value is yard labor
     / lower tiers); **over-counting is not the risk, under-capture is.**
  2. **Our methodology matches the government portal.** For **5 of 6** submarine prime contracts, USAspending's own
     published subaward total equals our naive row-sum **to the dollar** — i.e. "just sum the report rows" is
     exactly what USAspending does. That **validates the current approach** and makes the $12.487B defensible as
     the canonical public figure.

### The one Columbia discrepancy — and why it validates our scope
The only mismatch was Columbia contract **N0002417C2117**: USAspending **$7.75B** vs our **$3.50B** at nearly the
same record count. The entire ~$4.25B gap is **BlueForge Alliance — $4.214B across just 7 records**, all under one
subaward number (`1000042855`), classic cumulative snapshots ($1.56B, $1.40B, $600M …). **We correctly filter
BlueForge / MIB out** (the maritime-industrial-base intermediary / pass-through, not a hull subcontractor), so
**our number is the cleaner one and USAspending's is the inflated one here.** It is also a live example of the exact
cumulative-restatement double-count debated above — sitting entirely in records we already exclude.

### What we decided
- **Keep summing the report rows.** It matches USAspending and sits far under the prime ceiling; residual ambiguity
  is footnote-level.
- **Do NOT build the instrument-collapse / dollar-reconstruction layer for the dollars** → Phase 1 reverted
  (workbook back to the byte-identical 12-sheet baseline). An instrument layer can be rebuilt later *only if* Part B
  cadence work needs honest counts — it is not needed for the dollar totals.
- **Footnote, don't engineer.** Any headline "$X B" is labeled: *first-tier reported flow; matches USAspending;
  under-captures true subcontracting; BlueForge/MIB excluded.* Drive "where to play" off **shares / counts /
  rankings**, which are robust to the re-filing question.
- This **closes Open decision #2** and the Phase-1 portions of the plan above.
