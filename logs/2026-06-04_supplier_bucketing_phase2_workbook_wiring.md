# 2026-06-04 — Supplier bucketing Phase 2: wired the methodology into the workbook build pipeline

## Scope

After the owner signed off on the revised supplier-bucketing **market definition** (Phase 1 reconciliation
tables), wired the approved methodology into the **OOXML build pipeline** for both workbooks and
regenerated the real `.xlsx` **in place** (no backups / no versioned copies, per owner). **Decks
untouched. No `workbook_core` / `deck_core` changes.** Governing signal = operating-entity NAICS resolved
by `sub_entity_uei` via the 136-entity evidence registry.

## What was done (8 steps, rebuilt green after each)

1. Registry into the repo (`projects/research_shared/supplier_bucketing/vendor_evidence_registry.csv`) +
   `sheets/_registry.py` loader (×2) + `REGISTRY_CSV` in each `lib.py`.
2. Taxonomy: removed `3364`/`3344 → electrical` artifact; dropped DDG description step; `5511 → holding`;
   refreshed bucket display labels (keys unchanged).
3. DDG `data_entity_master`: classify **registry-first** by `sub_entity_uei`; added `Modular`/`VLS` flag
   columns + `modular_range`/`vls_range`; role summary +mission_systems/holding/foreign_fms; foreign-flag
   fallback to match the reconciliation.
4. Subs `data_entity_master`: **moved to record-level** (reads `nc_records_long.csv`, signed $),
   preserving every downstream accessor; added flag columns + `§4b` observed modular/VLS cells.
5. Scenarios: `HM&E += electrical`; `modular` made **entity-driven** (sentinel set; SAM Build special-cases
   it as `PortfolioTAM × modular-flagged $ / addressable`). Extended excluded-role audits.
6. VLS launch-control out-vs-in sensitivity added to both `validation_sensitivity` sheets.
7. Text/labels: methodology-guide precedence + exclusion tables (registry-led, new roles), exec-summary
   scenario interpretations, worktype-evidence arbiter table; scrubbed stale "description-led" docstrings.
8. Validation (below).

## Validation (two independent methods agree)

- **Python oracle** (`check_build.py`, runs the build's own classify+registry): both books **STATUS OK** vs
  the signed-off reconcile View 2. DDG physical $4,000M, mission $2,665M, foreign $359M, residual $2,027M,
  addressable $6,027M; subs physical $4,786M, electrical $2,031M (holds in), modular $618M, addressable
  $5,451M. Deltas <0.4% (NAICS-edge), immaterial.
- **LibreOffice headless recompute** of the actual `.xlsx`: **0 formula errors** in any sheet; live
  readback confirms Entity Master addressable (DDG $6,027M / subs $5,451M), mission $2,664.7M, modular
  $70M/$618M, VLS sensitivity DDG $4,000M→$5,678M (+$1,678M, +41.9%) / subs $4,786M→$4,787M.
- `validate_workbook.py` (DDG): 0 xml errors, 0 error-literal cells, 22 sheets, tables intact.
- Headline TAM **unchanged** (`model_tam_build.py` untouched); denominator discipline preserved
  (addressable = bucketed + residual; residual explicit, out of scenario SAM; `broad` < 100% of TAM).

## Files touched

- **New:** `projects/research_shared/supplier_bucketing/vendor_evidence_registry.csv`,
  `workbook_<proj>/sheets/_registry.py` (×2), `.../check_build.py` (oracle).
- **Edited (×2 / project):** `lib.py`, `_taxonomy.py`|`taxonomy.py`, `data_entity_master.py`,
  `inputs_scenarios.py`|`inputs_assumptions.py`, `model_sam_build.py`, `validation_sensitivity.py`,
  `guide_methodology.py`, `summary_executive_summary.py`, DDG `data_worktype_evidence.py`.
- **Regenerated in place:** both `20260601_…_vS.xlsx`.
- **Deliverable:** `projects2/2026-06-04_supplier_bucketing_PHASE2_workbook_implementation.md`
  (comprehensive note: context → plan → execution → validation).
- **No deck / `deck_core` / `workbook_core` edits.**

## Status / next

Phase 2 complete; both workbooks rebuilt green, validated, and match the signed-off market definition.
Decks remain untouched, awaiting a separate pass if/when the owner wants deck language updated to match.
