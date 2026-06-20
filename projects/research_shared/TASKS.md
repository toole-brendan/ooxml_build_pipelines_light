# Supplier classification — task list

**As of 2026-06-18.** Roadmap for finishing the classification effort. Approach is in
`CLASSIFICATION_METHODOLOGY_OVERVIEW.md`. Base is the post-filtered **$13.1B** canonical universe.

## Done

- `work_type` taxonomy defined — 18 process categories + `99 Unresolved`.
- `delivered_output_class` defined — `MA / CE / MT` (+ `SV / UN`); EQ/CP merged into CE.
- Vendor registry — top-50 by $ (71.1% of $), hand-verified; expanded to 55 via flagged-vendor research
  (Parker & AAE flipped 333310/332420 → 03 Fluid).
- Top-55 classified on `work_type` + `delivered_output_class`; curated sign-offs (BWXT → 02, NG#1 = 01).
- Builder appends future vendors from `vendor_registry_additions.csv` — no code changes.

## Remaining

### A. Subsystem dimension (SWBS) — HII-DDG only
Map observed SWBS → `subsystem` label, attached at the **transaction** level on HII-DDG subaward rows;
null elsewhere. Repurpose the existing HII join in `taxonomy_hii_scoring/` (keep the join, drop the
purity-scoring layer).

### B. Deliverable prior table
Build the **NAICS-6 → `delivered_output_class`** default prior for the long tail (registry covers named
vendors; the prior covers the rest). `MA` is positive-evidence-only — assembly-suggestive codes set a
candidate flag, never an automatic module.

### C. Full applied table — all 1,203 UEIs
- Precedence per entity axis: **registry override → NAICS-6 default → unresolved**.
- Columns: `work_type`, `delivered_output_class` (entity-level) + `subsystem` (transaction-level, from A).
- Join per-UEI labels to `all_subawards.csv` (20,702 rows) on `entity_uei`; attach `subsystem` from SWBS;
  **verify it ties to $13.1B**. Stamp every row with `assignment_basis` + `confidence`.

### D. Registry expansion (parallel/ongoing)
Append researched vendors to `vendor_registry_additions.csv`, driven by **dollars**. Coverage milestones:
top 100 = 83% of $, top 200 = 93%. Target depth ~top 100–200.

### E. scope_status — applied LAST
Once mapping + registry are complete, assign `scope_status` per UEI/record:
`core_shipbuilding_capability / enabling_shipbuilding_service / probable_scope_leakage / scope_uncertain`.
Independent of `work_type`. Quarantine-and-report (don't purge; totals still tie to $13.1B). Leakage
reasons are **open / non-exhaustive** (workforce-training, GFE, prime-owned in-house, …). Decide the
17 vs 17/19 work_type split here — recommend not splitting; let `scope_status` carry the disposition.

### F. Reconcile + publish
- Dollar matrices: `work_type × delivered_output_class × program` (submarines vs DDG-51).
- HII-only cut: `subsystem × work_type`.
- Coverage segmented by `assignment_basis` / `confidence`; show `scope_status` **separately**.
- **Never compare subsystem mix across programs** (subsystem is HII-DDG only).

### G. Housekeeping
- Consolidate curated sign-offs into one override registry shared by C and the workbook.

## Sequencing

`A + B + D → C → F`; **E (scope_status) runs last**, after C and D are substantially complete. Critical
path: **B → C → F**, with A feeding C. G is cleanup, do anytime.

## Open decisions

1. **17 vs 17/19 work_type split** (blocks E) — recommend: don't split.
2. **Alfa Laval 03 vs 04** — currently 04; revisit only if the matrix makes it material.
3. **Registry expansion depth target** (drives D / F coverage claims).

## Key paths

- Canonical base + record-level `all_subawards.csv`: `taxonomy_design_input_canonical/` /
  taxonomy_design_package.
- Taxonomy: `taxonomy_design_output/`.
- HII join (repurpose for subsystem): `taxonomy_hii_scoring/`.
- Consolidated workbook (registry + applied classifications): `award_classification_refactor.xlsx` (research_shared root).
