# 2026-06-20 — Schema adjustments: amount_type / dollars_basis / provenance + kill-chain spine

Fifth session (same day). Drove by re-reading the two source transcripts
(`projects3/army_transcript.xml` = methodology brainstorm; `army_transcript_2.xml` = data-schema
arrangement) against the funding layer already built (see `2026-06-20_budget_extraction_p5_rdte_oma.md`).
Verdict: **nothing built was wrong** — both transcripts independently re-derive and *validate* our core
invariants (the column_role / never-sum-overlapping-money spine; faithful-source vs analyst-judgment
separation; child-value-is-an-allocation crosswalk). This pass makes six targeted adjustments, calibrated
to the user's explicit phase ("data-gathering mode for budget + awards + subawards") and their standing
caution to **not over-name / over-normalize too early**. We did NOT rebuild into transcript-2's full
~25-table `d_/f_/x_/rpt_` star schema (that is the north star, not this phase).

## What changed (1–3: extractor; 4: new reference table; 5–6: plan)

### 1. `amount_type` added to `budget_funding_facts` + `budget_p5_cost_elements`
A semantic money-kind label (`request | enacted | actual | prior_year | outyear_estimate | to_complete |
total`) derived from `column_role` via the `AMOUNT_TYPE` map. We keep our richer `column_role` spine
(Base/OCO/Total/out-years/To-Complete are first-class) **and** now expose the coarse "kind of money"
the transcript's whole money-discipline keys on. Lets the workbook filter/guard "all request rows"
without enumerating roles, and is the join axis when contract money (its own roles) lands on the spine.
**It is never valid to sum across distinct `amount_type` values** — this is the no-double-count invariant
made enforceable at the semantic level. (transcript-2 core rule, "do not mix request, enacted, obligated,
ceiling… as if they are the same kind of money.")

### 2. `dollars_basis` added (= `then_year`)
DoD justification books (P-/R-forms) are in then-year (current) dollars; a constant-$ restatement would
come from the Green Book (National Defense Budget Estimates) deflators, never from the books themselves.
Captured as an explicit column (constant for now) so the basis is never ambiguous and so constant-$ or
contract-$ rows can coexist later without silent mixing.

### 3. Provenance spine: `extract_run_id` + `row_hash`
On `budget_funding_facts`, `budget_p5_cost_elements`, `budget_oma_watercraft_notes`.
- `extract_run_id` = `army-budget-extract-<ACCESS_DATE>` — **deterministic** (tied to corpus vintage, not
  wall-clock), so the extractor stays idempotent; bump only when the corpus is re-pulled.
- `row_hash` = 16-hex sha256 of the row's **identity tuple, excluding the amount**, so an analyst overlay
  (tags / crosswalk) keyed on it survives a re-extract that corrects a parsed value. Verified unique across
  all 1008 funding-fact rows. This is transcript-2's `raw_record_id` insurance ("rebuild without losing
  analyst review work") at low cost — we did NOT add a full separate raw-extracts tier (the extractor is
  deterministic and P-5 already keeps `raw_context`; revisit if/when human review state needs persisting).

Re-run verified clean: no `WARN`, **16/16 funded line-item-books reconcile <$0.05M**, RDT&E profile
unchanged (FY26 = 2.716), row counts identical (1008 / 1272 / 6 — only columns were added).

### 4. Capability stack = a 4-node KILL-CHAIN spine (not a 6-layer list)
New controlled vocabulary: **`workbook/analyst/capability_nodes.csv`** — first table in a new
`workbook/analyst/` dir that holds analyst-editable reference/crosswalk data, **physically separate from
mined `workbook/extracted/` facts** (invariant #2 made structural).

The spine is the sensor-to-shooter / JADC2 decomposition:

| seq | node | role | absorbs |
|-----|------|------|---------|
| 1 | **Platform** | host ("body") | the hull/vehicle that carries everything |
| 2 | **Sensors** | detect-track ("eyes & ears") | radar/EO-IR/sonar/ISR |
| 3 | **Effectors** | engage ("hands & arms") | **literal kinetic weapons only** |
| 4 | **C2** | decide-task ("brain & nervous system") | autonomy, assured PNT, comms, integration |

- **Effectors keeps its literal kinetic meaning** and is **expected to be BLANK for Army maritime**
  (logistics / operational-maneuver mission, not strike). A blank node is a valid, expected answer — do
  NOT back-fill it with cargo/bridging/survey to avoid emptiness. (This reverses an earlier suggestion to
  rename it "mission payloads/effectors"; the user wants the kinetic kill-chain node, blank if empty.)
- Autonomy / assured PNT / comms / systems-integration fold into **C2** in this 4-node collapse.
- **Lifecycle / sustainment / training are NOT kill-chain nodes** (out-of-spine; tracked via O&M evidence
  and the future acquisition/lifecycle layer), so they are deliberately absent from `capability_nodes.csv`.

### 5. A P-5 cost element is NOT a "work package"
Correction to the prior handoff (which said "the P-5 cost elements ARE the natural work packages").
Transcript-2 keeps these distinct and so do we:
- a **cost element** (LCU SLEP, MIBS, HCCC, …) is **budget-native faithful evidence** — it stays exactly
  as extracted in `budget_p5_cost_elements.csv`, judgment-free.
- a **work package** is an **analyst commercial decomposition** of an opportunity.
The work-package layer, when built, *references* cost elements as evidence; it never equates to them, and
analyst judgment is never baked back into the extracted facts (invariant #2).

### 6. The capability crosswalk is TWO bridges, not one
The prior plan's single `work_package_stack_map.csv` (line_item_id + cost_element → stack_layer +
parent_opportunity_id + addressable_content_%) conflated two different questions. Split them:
- **(a) attribution bridge** — *"what fraction of this budget line is addressable, and how?"*
  budget line / cost element → opportunity (or work package), carrying `addressable_content_%` + a
  relationship type (`Direct | Enabling | Comparable | Adjacent | Hypothesized`). Guards against summing
  one budget line across opportunities without explicit allocation.
- **(b) capability bridge** — *"which kill-chain node does this sit in, and how well?"*
  work package → `node_id` (FK to `capability_nodes.csv`), carrying fit/gap semantics
  (RelationshipType: Customer Requirement / Company Capability / Company Gap / Partner-Provided /
  Integration Dependency; Importance; FitRating; GapSeverity).
Both are analyst-editable, live under `workbook/analyst/`, and are **joined at build time — never new
columns in the extracted facts.** This preserves the guardrail that child values are *allocations* of the
parent, never additive new markets.

## Not done (deliberately deferred — respects "don't over-name early")
- No full transcript-2 star schema (25 tables) — that is the eventual target, not this phase.
- No separate raw-extracts tier — `row_hash` + `raw_context` + `source_log` suffice while the extractor is
  deterministic.
- No `OPA-…/RDTE-…` id-namespace normalization — it's a 1008-row join key; leave until the analyst /
  contracts layers force the decision.
- Seed tags (`mission_family`/`product_layer` on `budget_line_items`) left as columns for now; the
  transcript's polymorphic `record_tags` table is the eventual home (would unify budget + award + subaward
  tagging and the capability bridge under one pattern) — promote when the analyst layer grows.

## Files touched
- `research/budget_materials/extract_budget_cuts.py` — `AMOUNT_TYPE`, `DOLLARS_BASIS`, `EXTRACT_RUN_ID`,
  `row_hash()`; new columns wired into P-40 / R-2 / P-5 / O&M emitters + headers; `tie_out_p5` index +1.
- `workbook/extracted/{budget_funding_facts,budget_p5_cost_elements,budget_oma_watercraft_notes}.csv` —
  regenerated with the new columns (row counts unchanged).
- `workbook/analyst/capability_nodes.csv` — NEW (4-node kill-chain controlled vocabulary).
- `logs/2026-06-20_budget_extraction_p5_rdte_oma.md` — invariant-3 bullet + stack mention revised to point
  here.
