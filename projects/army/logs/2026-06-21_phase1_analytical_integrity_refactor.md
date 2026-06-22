# 2026-06-21 — Phase 1: analytical-integrity refactor (+ HANDOFF for Phases 2-4)

Session log AND cold-start handoff. Two independent AI reviews of the `army` project
(captured in the user's prompt; mirrored in the approved plan
`~/.claude/plans/2-different-ai-agents-vectorized-shannon.md`) reached the same verdict:
the extraction/evidence layer is well-built and should be PRESERVED, but the workbook is a
contract-evidence register + recompete prototype, **not yet a defensible Saronic-addressable
Army market-sizing model**. The agreed 4-phase fix: **(1) fix analytical integrity →
(2) render budget + build the TAM/SAM model → (3) executive Overview → (4) recompete/source
enhancements.** This session executed **Phase 1 in full**. Phases 2-4 are the handoff below.

Build is green: **7 sheets, 6 native tables, 0 error cells.** Output:
`projects/army/20260620_US Army Market Mapping_vS.xlsx`.

---

## 0. Verified findings (confirmed against the actual code/data, not just the reviews)
- **Workbook rendered only contract evidence** — Overview (stub) + 2 recompete models + 4
  contract leaves; **zero budget data** (1,008 funding facts / 1,272 P-5 / O&M / source log
  all in CSVs, unused).
- **Obligation reconciliation broken** — the $1M filter keyed on award-level
  `obligation_amount`; the displayed "Obligated $M" was a SUMIFS over per-mod actions. They
  diverge for 186 families; **117 have negative-or-zero action sums** (e.g. `W52P1J09C0049`:
  −$1.58M actions vs $47.83M award).
- **Parent-IDV gap = 71%** — 171 of 241 referenced parent IDVs had no standalone Contract
  Awards record (reviewers guessed ~29%). 94 of those are material (≥$250k; incl. all 72
  ≥$1M); 77 are sub-floor micro-buys.
- **Analyst layer essentially empty** (only an unused `capability_nodes.csv`); no `config.py`.

---

## 1. What was built this session (Phase 1, eight work items)

### 1.1 Central config + classification rules
- `research/contracts/scripts/config.py` (**canonical** for the data side) — materiality
  floor, lineage windows, notice lead, watercraft scope sets, customer-segment labels,
  coverage thresholds. `scripts/mapping_rules.py` — `watercraft_relevance()` +
  `customer_segment()` functions.
- `workbook/workbook_army/sheets/config.py` (workbook display constants + a mirrored
  watercraft set for the no-canonical-CSV fallback). `model_recompete_radar.py` /
  `model_recompete_calendar.py` now import from it (constants removed from the radar).

### 1.3 Parent-IDV hydration via the SAM Contract Awards API  *(done first; data dependency)*
- New `scripts/pull_sam_contract_awards.py` (Stage 7) — SAM Contract Awards API
  (`api.sam.gov/contract-awards/v1/search`) **PIID Aggregation**. Resumable, biggest-family
  first, traps `QuotaExhausted`. Pulled **446 families ≥ $250k** (under the 1,000/day quota);
  **all 94 material orphan IDVs hydrated** with an ordering-period end + ceiling.
- `aggregate_contracts.py` **synthesizes an award row** for each orphan parent IDV
  (`obligation=0`, `pop_current_end_date`=ordering-period end, `ceiling_value`, `hydrated=Y`,
  `source_system=sam_contract_awards`) so the live MAXIFS resolves **Parent/vehicle end** —
  all 90 radar IDV families now resolve it (were blank).
- **Reconciliation caveat captured:** the SAM CA API is REVEALED-only on a non-federal key
  (DoD <90-day awards excluded) and its DO backfill trails legacy FPDS — e.g. Vigor
  `W56HZV17D0086` shows SAM $56.2M vs our $417.8M. So SAM family $ is a **third lens / flag**,
  never overwritten onto our action sums; only the structural fields (ordering end, ceiling)
  are used as authoritative hydration.

### 1.2 Obligation reconciliation — single selected measure
- `aggregate_contracts.py` now emits **`workbook/extracted/contract_families.csv`** (the
  canonical per-family fact table, 1,688 rows): award-reported obligation, reconstructed
  action sum, **coverage ratio + status** (complete/partial/over/negative/no-actions),
  SAM third-lens total, hydrated dates, segment, and a **single `selected_measure`**
  (action sum when coverage complete, else award-level with `materiality_basis="award
  (fallback)"`).
- Radar `load_families()` reads this table; the $1M floor + ranking use `selected_measure`.
  **Result: 0 of 226 radar families fall below $1M or negative on their selected measure**
  (the bug). The 12 negative-reconstruction families now select on award fallback and are
  flagged. Radar gained columns: **Award-reported $M** (live), **Recon. $M (actions)** (live),
  **Coverage** (live ratio), **Materiality basis**.

### 1.4 Lineage = evidence score, not verdict
- `aggregate_contracts.py` emits **`workbook/analyst/lineage_edges.csv`** — 454 scored
  candidate edges (same-incumbent+PSC temporal chaining; similarity signals + `evidence_score`
  + blank `analyst_disposition`), **preserving analyst dispositions across re-runs**. One
  validated chain seeded Confirmed (Birdon `W56HZV14C0015→W56HZV19D0093`).
- Radar reads dispositions: a predecessor is **Superseded only when Confirmed/Probable**;
  unreviewed expired tails read **"Expired - successor unresolved"** (was "Overdue").
  Candidate predecessor/successor PIIDs still shown. Calendar folds out **only**
  confirmed-superseded (164 → 225 tails — expired-with-candidate vehicles no longer hidden).

### 1.5 Pipeline notices → solicitation lifecycle + family links
- `aggregate_contracts.py` collapses notices to **one row per solicitation lifecycle**
  (88 → 37; some solicitations had 15-20 amendment notices), keeping first/latest posted,
  current stage/deadline, ultimate award PIID, `n_notices`. Raw notices retained in
  `_opportunities_index.json`. Pipeline leaf updated (date typing + intro).
- Emits **`workbook/analyst/notice_family_links.csv`** — 51 scored candidate notice↔vehicle
  links (open notices × same-PSC families), confirmations preserved across re-runs.

### 1.6 Army vs USACE customer segmentation
- `customer_segment` column on families, awards, and notices via `mapping_rules.customer_segment`.
  **Headline:** of 226 radar families — **USACE civil works 172, Army operational watercraft
  36, MRO 8, peripheral 8, Army RDT&E/autonomy 2**. The open pipeline is **78/88 USACE**. The
  "$3.0B" was never one homogeneous Army market.

### 1.7 Durable analyst tables + loader
- `workbook/workbook_army/sheets/_analyst.py` reads analyst CSVs and merges them onto model
  rows at build time (rendered blue). The radar's Window/Confidence/Pursuit/program/
  capability_node/Notes + the calendar's Confidence/Pursuit/Notes now come from durable
  **`workbook/analyst/recompete_reviews.csv`** (keyed by `family_key`) — **proven to survive a
  rebuild** (set value → rebuild → persists; reverted).
- Seeded-if-absent bridge schemas (never clobbered): `opportunities.csv`,
  `budget_opportunity_attribution.csv`, `award_opportunity_attribution.csv`,
  `work_packages.csv`, `work_package_capability.csv`, **`work_package_saronic_route.csv`**
  (Saronic routes Marauder/Echelon as **editable input**, not hardcoded — decision #2),
  `customer_org_map.csv`, plus `recompete_reviews.csv`, `lineage_edges.csv`,
  `notice_family_links.csv`. A few illustrative rows flagged `source=seed`.

### 1.8 Source freshness clocks
- **`workbook/extracted/source_clocks.csv`** — per-source data-through date + reporting lag,
  including the **Contract Awards API DoD 90-day Revealed** exclusion. (Rendered on the QA/
  Overview sheet in Phase 3; captured now.)

---

## 2. Files created / changed
**Created:** `scripts/config.py`, `scripts/mapping_rules.py`, `scripts/pull_sam_contract_awards.py`,
`workbook_army/sheets/config.py`, `workbook_army/sheets/_analyst.py`,
`workbook/extracted/contract_families.csv`, `workbook/extracted/source_clocks.csv`,
`research/contracts/extracted/_contract_awards_agg_index.json`,
`research/contracts/sam_contract_awards/*.json` (446 raw), and `workbook/analyst/*.csv` (10 tables).
**Changed:** `scripts/aggregate_contracts.py` (families, hydration, segments, lifecycle, lineage
edges, notice links, source clocks, expanded report), `workbook_army/sheets/_radar_formulas.py`
(+`obl_award`), `model_recompete_radar.py` (canonical load + reconciliation cols + scored
lineage + rename), `model_recompete_calendar.py` (segment col + durable analyst cols + honest
labels), `data_pipeline_events.py` (lifecycle columns).

## 3. How to re-run (full Phase-1 pipeline)
```bash
cd projects/army/research/contracts/scripts
python3 pull_sam_contract_awards.py     # Stage 7 hydration (resumable; ~446 SAM calls)
python3 aggregate_contracts.py          # -> contract_families.csv + analyst/*.csv + source_clocks
cd ../../../workbook && python3 build_workbook.py   # -> 7 tabs, 0 error cells
```
Use `python3` (never `python`). LibreOffice can NOT recalc this book (outline rows don't
round-trip) — verify live math via Python over the CSVs + a source-XML `t="e"` scan.

## 4. Verification done (all green)
0 error cells (all 7 sheets); radar 30 cols × 226 rows, calendar 18 × 225, awards 46 × 2689
(+94 hydrated), pipeline 24 × 37. 0 radar families below $1M/negative on selected measure;
12 negative-reconstruction flagged; 90/90 radar IDV families resolve parent end; lineage
Confirmed-suppression + analyst-input durability both round-trip-tested.

---

# HANDOFF — what remains

## A. Phase-1 carve-outs / immediate follow-ups (small, do alongside Phase 2)
1. **Wire In-market to confirmed notice links.** Radar "In-market notice" still keys on
   `award_number` only (live formula). `notice_family_links.csv` exists but isn't wired,
   because a live formula needs the links ON a sheet. Do this when the Pipeline/Opportunity
   sheet is built in Phase 2/3 (render links → reference with COUNTIFS over confirmed links).
2. **Reconciliation detail on a sheet.** SAM third-lens total, coverage %, first/last action
   date, difference live in `contract_families.csv` but only 4 reconciliation columns are on
   the radar. Surface the rest on the Phase-2 "Contract & Vendor Landscape" / QA sheet.
3. **Seed coverage for new families.** `recompete_reviews.csv` is seeded-if-absent over today's
   ≥$1M families; families added later won't get a row (delete-to-regen or add manually).
   Same for the other seeded bridges. Document for the analyst.
4. **77 sub-$250k orphan IDVs** are unhydrated (immaterial — their families are <$1M micro-buys,
   below the radar). Lower `FAMILY_PULL_FLOOR` in `scripts/config.py` + re-run the pull if ever
   needed.
5. **The analyst pass itself.** Every bridge/judgment cell is blank/seed: addressable %, fit %,
   pursuit/win probs, lineage dispositions, notice confirmations, customer_org. This is human
   work the structures now support.

## B. Phase 2 — render budget evidence + canonical models + market sizing (NEXT)
- **Render budget leaves** via `_flat.make_flat_sheet` (none are in the workbook yet):
  `budget_funding_facts` (1,008), `budget_p5_cost_elements` (1,272), `budget_oma_watercraft_notes`,
  `source_log`. Mirror the contract-leaf pattern (`data_*.py`).
- **Canonical budget table** — one accepted observation per `program × measure × observed_FY ×
  vintage`. Anti-double-count rules (enforce, don't just document): never add
  request_base+request_total; never add P-5 components to subtotals; never add an RDT&E PE total
  to its project breakout; never mix gross/net/TOA; never blend vintages without a labeled
  series; OMA = qualitative only.
- **`model_contract_families.py`** — promote `contract_families.csv` to a rendered sheet so the
  radar/calendar can reference it directly (and reduce the thousands of live SUMIFS/MAXIFS).
- **Populate the two bridges** (preserve the distinction): **attribution** (budget/contract →
  opportunity/work-package + addressable %) and **capability** (work package → Platform/Sensors/
  Effectors/C2 + Saronic fit/gap/partner). Schemas already seeded under `workbook/analyst/`.
- **Market measures** (separate, never summed): Gross Funded = Σ eligible budget $; Addressable
  = Σ budget$×addressable%; Saronic-Serviceable = Σ addressable$×fit%; Weighted Pursuit = Σ
  serviceable$×timing-conf×pursuit-access×win-prob. Historical obligations stay a SEPARATE lens.
  *(Reviewers' starting universe: a gross FY27–31 funding spine ≈ $443M across ESP + MSV(L) +
  Project 526 — emphatically not yet SAM until attribution/fit are applied.)*

## C. Phase 3 — decision-output layer
- Replace the stub Overview with an executive bridge: Gross Funded / Saronic-Addressable /
  Weighted 36-mo pursuit, % classified, % tied budget→contract, # reviewed recompetes,
  per-source data-through dates (from `source_clocks.csv`), top-5 opportunities + confidence.
- New sheets + recommended tab order: Overview → Scope & Assumptions → Customer Map → Budget
  Market → Opportunity Map → Saronic Fit → Contract & Vendor Landscape → Recompete Radar →
  Recompete Calendar → Pipeline → QA & Reconciliation → Source Log → raw data. (Sheet groups
  must stay contiguous per `workbook_core.groups`; registry = `sheets/__init__.py`.)

## D. Phase 4 — recompete + source modernization
- Evidence-scored lineage live in the radar; **different-vendor (competed-away) successors**
  (needs the office join + a lower confidence tier — generalize `build_lineage_edges` beyond
  same-UEI); confirmed notice linkage live; periodic recompete snapshots.
- **Migrate the per-mod actions pull off FPDS Atom onto the SAM Contract Awards API** (FPDS
  ezSearch decommissioned 2026-02-24). The Stage-7 `pull_sam_contract_awards.py` is the
  foundation; add per-record action retrieval. Keep the 355MB FPDS raw as historical backstop.

## E. Cross-cutting invariants to hold (don't relearn the hard way)
- **Money discipline:** never sum across `amount_type` (request/enacted/obligation/ceiling) or
  across budget + contract $. Historical obligations ≠ TAM/SAM and are NOT additive to budget.
- **Faithful facts vs analyst judgment** stay physically separate: `workbook/extracted/` =
  mined; `workbook/analyst/` = editable judgment merged at build (blue, rebuild-durable).
- **SAM Contract Awards $ is a third lens**, not ground truth (Revealed-only + new-API backfill
  lag) — only its structural fields (ordering end, ceiling) are used as authoritative.
- The single editable **As-of cell** (`'Recompete Radar'!$C$6`) re-clocks every expiry column;
  keep it. `python3` only; verify via Python replica + `t="e"` scan, not LibreOffice.
