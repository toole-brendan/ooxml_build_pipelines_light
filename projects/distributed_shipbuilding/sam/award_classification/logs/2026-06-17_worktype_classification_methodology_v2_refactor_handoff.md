# 2026-06-17 — Work-Type Classification Methodology v2: refactor/enhancement handoff

**Mission for the next agent:** complete the refactor + enhancement of the
**subaward work-type classification methodology** for *Distributed Shipbuilding*,
then propagate it through the three deliverables that consume it:

1. **`deck_primary`** — the primary new-construction deck (PPTX).
2. **`workbook_award_analysis`** — the award-analysis workbook (subaward data cuts).
3. **`workbook_outsourcing_ceiling`** — the outsourced-ceiling / cost-funnel workbook.

This session did the **discovery + data-foundation** phase (no production code changed
yet). It established the data constraints, pulled the richer SAM signal, profiled the
real distribution, drafted a v2 design, and staged two accuracy audits. The next agent
should **finalize the taxonomy from the data, then implement**. Nothing in the live
pipeline has been modified — all work is additive in new files.

> ⚠️ Process note for the next agent: this session repeatedly caught itself stating
> *inferences as confirmed facts* and had to walk them back (see "Lessons"). Verify
> against the data/code before asserting. Distinguish "confirmed" from "inferred."

---

## 0. TL;DR status

- **Data foundation: DONE.** SAM entity enrichment pulled for 939/1,352 UEIs (93% of
  dollars; quota cut the tail — resumable). Full profiling tables written.
- **Design: DRAFTED, partially validated.** A v2 methodology (10 work-types + component
  overlays + tri-state modular) exists and was pressure-tested against the real NAICS-6
  distribution. Two of its proposed new categories are data-validated; one is not.
- **Accuracy audits: STAGED, not yet run.** Two CSVs + prompts are ready to hand to a
  web-search-capable agent (registry core + un-curated mid-tail).
- **Implementation: NOT STARTED.** No taxonomy/registry/workbook/deck code changed.

---

## 1. The methodology as it stands today (v1) — what we're refactoring

**What it does:** classifies each de-duplicated subaward record by (a) a **role** and
(b) for suppliers, one of **7 mutually-exclusive work-type categories**, plus a separate
**modular-assemblies** capability flag.

**Pipeline (pull → classification):**
1. Pull SAM.gov FSRS subaward reports, one JSON per prime contract (PIID).
2. Scope-filter to in-scope new-construction PIIDs; drop pass-through recipients.
3. De-duplicate cumulative FSRS snapshots → one row per `subAwardReportId`.
4. Extract recipient UEI, parent UEI, amount, date→FY, foreign flag.
5. **Resolve each UEI → primary NAICS-4** via an external SAM-derived lookup (the raw
   subaward record has **no** subawardee NAICS).
6. Classify **registry-first**, else a deterministic fallback ladder:
   prime/co-prime name → GFE/integrator name → vendor-name override → NAICS-4 crosswalk
   → service NAICS → holding (5511) → residual.
7. Apply the modular flag (registry-only).

**The full v1 write-up** (with the data-field addendum) lives at:
`/Users/brendantoole/projects3/worktype_classification_methodology.md`
(this is the doc that was attached to the external design agent — keep it the canonical
spec; update it as v2 lands).

**Key code (per-program + consolidated; logic is identical across all three):**
- DDG taxonomy/classifier: `projects/distributed_shipbuilding/ddg/workbook/workbook_ddg/sheets/_taxonomy.py`
  (`BUCKETS`, `BUCKET_KEYS`, `NAICS4_BUCKET`, `SERVICE_NAICS4`, name-key lists, `classify()`)
- Submarines: `submarines/workbook/workbook_submarines/sheets/taxonomy.py` (note: no leading underscore)
- Registry loader (per workbook): `.../sheets/_registry.py` (`load_registry()`)
- Classification call-site (registry-first): `.../sheets/data_entity_master.py`
- Consolidated/award classification: `projects/distributed_shipbuilding/research/scripts/_corpus.py`
  (`iter_records()` — dedups by `subAwardReportId`, classifies registry-first) and
  `extract_workbook_cuts.py` (writes the `wb_*.csv` cuts the award workbook reads)

**Terminology (IMPORTANT — see §6):** in code, `bucket` = the 7 work-type categories
(NOT a roll-up). The roll-ups (`metal`/`hme`/`broad`/`modular`) are `SCENARIOS`.

---

## 2. The three deliverables & how the methodology reaches them

All three ultimately render the *output of this classification*. The classification
happens in the research/extract layer and is frozen into CSVs that the deck/workbooks read.
So a methodology change must flow: **taxonomy + registry + enrichment → re-extract → rebuild.**

| Deliverable | Dir | Build | Consumes |
|---|---|---|---|
| deck_primary | `projects/distributed_shipbuilding/deck_primary/` | `python3 build_deck.py` → `20260610_Distributed Shipbuilding New Construction_vS.pptx` | imports `taxonomy` directly (11 refs) — work-type vocab is baked into slides |
| workbook_award_analysis | `.../workbook_award_analysis/` | `python3 build_workbook.py` → `20260612_…Award Analysis_vS.xlsx` | `workbook_award_analysis/extracted/wb_*.csv` (from `extract_workbook_cuts.py`) |
| workbook_outsourcing_ceiling | `.../workbook_outsourcing_ceiling/` | `python3 build_ceiling_base.py` then `build_workbook.py` (two-step — verify) | its own `extracted/cost_funnel_*.csv`, `wb_anchors.csv`, `wb_cost_base.csv` |

**Implication:** when the taxonomy/registry change, you must re-run the extract scripts
that feed *each* deliverable, not just one. The deck pulls the taxonomy module directly,
so renaming `bucket`→`work_type` or changing categories touches deck code too.

---

## 3. Hard data constraints (these are immovable — design within them)

1. **No PSC on subaward transactions.** Confirmed by enumerating every key in the raw
   JSON. The only NAICS in a record is `primeNaics` (the *prime's*, ~always `336611`).
2. **No subawardee NAICS on the transaction.** Work-type cannot be read off the record;
   it must come from the **entity** (via SAM lookup) or the registry.
3. **Descriptions are junk** (`"PLEASE SEE BELOW"`, `"PUMP"`, blanks) — unusable.
4. **Entity-level PSC exists but is sparse/noisy** — only **12.3% of dollars** have any
   PSC; where present it's often aspirational (Scot Forge lists BOMBS/MISSILES). PSC is a
   bonus tie-breaker at best, NOT a backbone.
5. **The reliable lever is the entity NAICS *list* (6-digit), via the SAM Entity API** —
   present for **90.6% of dollars**, avg 4.3 codes/entity.
6. Useful secondary SAM fields discovered: `coreData.generalInformation.organizationStructureDesc`
   ("Manufacturer of Goods" vs service — present 64% of $), and
   `integrityInformation.corporateRelationships.immediateOwner/highestOwner` (parent
   rollup, present 47% of $) — both better than the subaward record's ~56%-filled parent fields.

Full field inventory of the SAM Entity API is in the methodology doc's addendum and was
verified live this session (sections: entityRegistration, coreData, assertions,
pointsOfContact, repsAndCerts, integrityInformation).

---

## 4. What was produced this session (all NEW, nothing live touched)

All under `projects/research_shared/sam_entity_enrichment/` unless noted:

- `pull_entities.py` — pulls + caches SAM entity JSON per UEI (dollar-desc, resumable, 429-safe).
- `profile_entities.py` — builds the profiling tables + coverage summary.
- `raw/` — **939 cached entity JSONs** (871 real + 68 no-record markers).
- `unique_uei_corpus.csv` — all 1,352 subawardee UEIs with $ / record / program / foreign weights.
- `unique_uei_sam_enrichment.csv` — normalized entity table (NAICS-6 primary+list, PSC,
  org-structure, owner, CAGE, exclusion, reg status) joined to corpus weights.
- `uei_naics_long.csv`, `uei_psc_long.csv` — long-form for pivoting.
- `naics6_primary_profile.csv` — **the key table**: primary NAICS-6 × dollars × vendor-count × current-v1-category.
- `psc_profile.csv`, `org_structure_profile.csv`.
- `registry_audit_top40.csv` — top 40 registry entities by $ (audit template, blank verdict cols).
- `midtail_audit_top50.csv` — top 50 un-curated/non-passthrough entities (audit template).
- `_pull.log`, `_pull_progress.json` — pull run state.

Canonical methodology doc (updated with field addendum this session):
`/Users/brendantoole/projects3/worktype_classification_methodology.md`

---

## 5. Empirical findings from the profiling (the analytical payoff)

Corpus: **1,352 unique subawardee UEIs, $17.78B deduped, 22,499 unique records.**
Pareto: top 50 = 76.4% of $, top 150 = 90.9%, top 300 = 96.6%, top 500 = 99%.

**Coverage of the 939 pulled (=93.2% of $):** primary NAICS-6 present for 90.6% of $;
PSC for 12.3%; org-structure 64%; immediate-owner 47%; no SAM record 6.8%.

**Current v1 categories by dollar (from primary NAICS-4):** service 26.7%, electrical
17.7%, structural 14.5%, **unbucketed/other 12.9%**, piping 10.5%, no-record 6.8%,
castings 3.3%, machining 3.0%, hvac 2.6%, coatings 2.1%, holding ~0%.

Key reads:
- **"Service 26.7%" is a mirage** — $4.17B of it is **BlueForge Alliance** (NAICS 541614),
  already excluded as a pass-through. Real service ex-BlueForge ≈ **3.2%**.
- **The 12.9% "unbucketed/other" ($2.29B) decomposes into two coherent clusters** that
  v1 drops because NAICS 3344/3345/3364 were deliberately excluded as corporate artifacts:
  - **Electronics / instrumentation / controls** (334511 nav/detection, 334417 connectors,
    334515/334513 instruments, 334416/334419 components) ≈ $700–900M. *Caveat: some is
    combat-systems/GFE-adjacent → needs ROLE review, not just a bucket.*
  - **Propulsion / gas-turbine / power-transmission** (336412 aircraft-engine parts =
    marine gas turbines like the DDG LM2500, $350M/6 vendors; + 333612 speed-changers/gears).
- **NAICS 336611 ("Ship Building") as subawardee = $1.28B / 44 vendors** — a ROLE problem,
  not a work-type one. Actual v1 disposition: registry handles 78% (37.6% supplier,
  26.1% mission_systems=BAE, 8.1% prime=HII, 6.6% foreign=Rosyth); 21.1% falls to
  NAICS-4→"structural"; name-rules only 0.5% (registry preempts them). The 21% fallback
  tail is where genuine error lives (IMIA→really coatings, US Joiner→outfitting,
  Erie Forge→forgings) — but for several, **the work-type signal isn't recoverable from
  NAICS** (IMIA's SAM lists only shipbuilding+remediation; Craft Machine has 16 codes).
  So the fix for the tail is **registry curation, not finer buckets**.
- **Component-tag coverage will be patchy** — NAICS-6 yields a clean component for the
  equipment families (valve 332911, pump 333914, transformer 335311, switchgear 335313,
  motor 335312, forging 332111, A/C 333415, connector 334417) but **nothing** for
  fabrication/machining (machine shops 332710, fabricated structural 332312, shipbuilding
  336611, misc 339999). Don't over-build the component vocabulary.

---

## 6. The v2 design + verdicts (what to finalize)

The external design agent produced a v2 methodology (full text in the chat transcript;
reproduce into the methodology doc when finalizing). Core architecture is **sound and
adopted**: keep registry-first / deterministic / auditable; **one additive work-type per
supplier record**; **multi-valued, NON-additive overlays** for components + modular;
**tri-state modular** (`true`/`false`/`unknown`); no descriptions; no prime NAICS; full
audit basis per assignment.

Its proposed **10-category** work-type taxonomy, pressure-tested against the data:

| Proposed category | Verdict from data |
|---|---|
| structural_fabrication_hull_metalwork | keep |
| castings_forgings_primary_metal_forms | keep |
| machining_mechanical_parts | keep (thin, ~3%) |
| **propulsion_power_transmission** | **VALIDATED add** (336412 + 333612, real $) |
| fluid_handling_piping_pressure | keep (strong) |
| electrical_power_distribution | keep (strong) |
| **controls_instrumentation_electronics** | **VALIDATED add** (~$700–900M now unbucketed) — but role-review the GFE overlap |
| hvac_thermal_management | keep |
| coatings_insulation_decking_surfaces | keep |
| **outfitting_closures_habitability** | **NOT validated** — no material NAICS signal; demote to component tags |

**Net v2 taxonomy recommendation:** the 7 → **~9** (add propulsion + controls/electronics;
do NOT add outfitting as a top-level type). PSC demoted to occasional tie-breaker. The
single highest-value lever is **role adjudication via the registry**, not granularity.

**Other adopted upgrades:** resolve UEI → **primary NAICS-6** (not -4); store the full
NAICS-6 list as evidence (ambiguity flags, component candidates, review prioritization)
but do NOT let a secondary NAICS auto-override the primary; add `organizationStructureDesc`
as a role/service backstop (flags only, never sets work-type); use owner fields for parent
rollup only (never inherit work-type from parent).

### Terminology decisions to implement
- **Rename `bucket` → `work_type`** everywhere (it was never a roll-up; the name caused
  repeated confusion). Concept unchanged.
- **Deprecate the roll-up `SCENARIOS`** (`metal`/`hme`/`broad`) — already out of scope in
  the methodology doc. **Keep `modular`**, but as a standalone overlay flag, not a scenario.
- **"Registry" ≠ "SAM lookup."** Registry = hand-adjudicated decision table
  (`research_shared/supplier_bucketing/vendor_evidence_registry.csv`, 169 entities; columns
  role/bucket/scenario_flags/confidence/basis/evidence_source/notes; maintained via
  `propose_registry_additions.py` → `merge_registry_additions.py`). SAM lookup = mechanical
  UEI→NAICS data (the new `sam_entity_enrichment`, supersedes the old per-program
  `entity_naics_lookup.csv`). Registry overrides; SAM lookup is the fallback signal.

---

## 7. Accuracy audits — staged, NOT yet run

Two CSVs ready to hand to a **web-search-capable agent** (prompts are in the chat
transcript; reproduce them next to the CSVs if needed):
- `registry_audit_top40.csv` — is the hand-curated registry right? (40 entities ≈ $11B assoc.)
- `midtail_audit_top50.csv` — did the mechanical NAICS/name fallback get the un-curated
  slice right? (50 entities = $1.4B; the higher-risk, less-watched ~17% of addressable $).
  Visible likely-misses to confirm: **L3 Technologies** (→ should be GFE, name-rule only
  matches "L3HARRIS"), **Waukesha Bearings** (→ machining, mis-coded "service"),
  **IMO Industries** (→ piping/pumps, left "unbucketed"), **Americast** (→ castings).

Internal cross-check already done (not a substitute for the web audit): registry is 81.6%
high-confidence by $; vs SAM NAICS it agrees 57 / disagrees 25 / 40 no-compare, and the
disagreements are mostly *justified overrides of bad NAICS* (e.g. bearings mis-mapped to
piping by the coarse NAICS-4 crosswalk). Looks sound; unverified against ground truth.

---

## 8. Roadmap to completion (ordered)

1. **Finish the SAM pull** — 413 tail UEIs remain (quota 429'd at ~1,000/day, resets
   midnight UTC). Re-run `pull_entities.py` (skips cached). Optional: switch to batched
   lookups to save quota. Then re-run `profile_entities.py`.
2. **Re-run the profile excluding pass-throughs** (BlueForge F8PEZKXES8B1, Training
   Modernization Group QLJZVM6XKR71, IALR TCM3R4JPRKY4) to show the true addressable denominator.
3. **Run both audits** (hand CSVs+prompts to a web agent). Then build a small ingest script
   that reports dollar-weighted pass/fail per slice and lists every FAIL with the correction.
4. **Apply audit corrections to the registry** via `propose_registry_additions.py` →
   `merge_registry_additions.py` (don't hand-edit the CSV; the merge validates vocab + backs up).
5. **Finalize the v2 taxonomy** from the profile + audits — lock the category list (likely
   the 7 + propulsion + controls/electronics; outfitting→tags). Define: the "all-NAICS
   consensus" rule, and the taxonomy-lock acceptance bar (e.g. residual < X% of $).
6. **Implement:** rename `bucket`→`work_type`; update `BUCKETS`/`NAICS4_BUCKET` →
   `NAICS6_*` crosswalk in `_taxonomy.py`/`taxonomy.py` (both programs + keep them in sync);
   wire `organizationStructureDesc`/owner into the role ladder + flags; switch enrichment
   source from `entity_naics_lookup.csv` to the new `sam_entity_enrichment` table.
7. **Re-extract** per-program (`data_entity_master.py` path) and consolidated
   (`_corpus.py` / `extract_workbook_cuts.py`) → regenerate the `wb_*.csv` / `nc_records_long.csv` /
   ceiling `cost_funnel_*.csv`.
8. **Rebuild + validate the three deliverables** (commands in §2). Run a **v1/v2 parallel
   diff** on top-dollar movers before committing (the v2 plan's parallel-run step).
9. **Update the canonical methodology doc** to v2 and refresh memory if conventions change.

---

## 9. Open decisions for the user / next agent

- Final category count (9 vs the proposed 10 — outfitting in or out?).
- Whether to add the component-tag layer at all in v1 of the refactor, given patchy
  coverage — or defer it until after the work-type + role upgrades land.
- Batched vs per-UEI for the tail pull (quota economics).
- How aggressively to expand the registry from the mid-tail audit (cost of curation vs
  the ~17% addressable $ at stake).

---

## 10. Lessons / cautions (carry forward)

- **Verify before asserting.** This session twice stated name-inferences as fact
  ("these are co-primes"; "IMIA = coatings, mis-registered") that the data partly refuted
  (most 336611 vendors are suppliers; IMIA's SAM data shows only shipbuilding+remediation).
  Always separate *confirmed* (ran it) from *inferred* (looks like).
- **The win is role + registry, not taxonomy granularity** for the hard cases — the data
  showed registry already carries ~78% of the addressable base, and the fallback tail
  often has no recoverable NAICS work-type signal.
- **PSC is a trap** — intuitive but empirically absent (12% of $). Don't design around it.
- **Pass-throughs distort raw cuts** — always net out BlueForge et al. before reading
  category shares.

## 11. API / quota notes

- Key in `.env` (`SAM_API_KEY`). Limit behaves like **~1,000 requests/day**; no
  quota-check endpoint — trap HTTP 429 and halt (the pull does). Resets midnight UTC.
- No-record lookups (totalRecords:0) still cost a request.
- Endpoint: `GET https://api.sam.gov/entity-information/v3/entities?ueiSAM=…&includeSections=entityRegistration,coreData,assertions,integrityInformation&api_key=…`
- API methodology reference: `/Users/brendantoole/projects3/Federal_Award_API_Research_Methodology.docx`.
