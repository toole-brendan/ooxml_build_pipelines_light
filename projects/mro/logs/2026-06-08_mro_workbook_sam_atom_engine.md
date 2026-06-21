# 2026-06-08 — MRO workbook: atom-based SAM scenario engine

Replaced the single hardcoded "Marauder-like" SAM funnel (`chartdata_output.py §5`) with a
real, leadership-grade SAM engine: **one** headline TAM (Reconciled FPDS-visible MRO TAM),
a **mutually-exclusive TAM-atom ledger**, an **editable axis-based Scenarios matrix**, and
an **atom-level SAM Build** that selects subsets of atoms — `SUM(atom $ × scenario inclusion)`
— instead of adding independent cuts that double-count. SAM is now a *menu of overlapping
options*, never a second TAM, and every scenario sits inside TAM by construction. Builds on
the native rewrite (`2026-06-07_mro_workbook_native_rewrite_phase4_*`).

## Architecture
- **One TAM**: `reconciled_mro_tam_cell()` = Navy+USCG services-MRO + embedded PSC 1905 ($8,970.87M).
- **SAM = scenario-selected subset of TAM atoms.** Inclusion rule: **within an axis OR,
  across axes AND.** Each atom carries exactly one bucket per axis, so the AND-product never
  silently drops a constraint.
- **Seven axes**: work_segment, hull, buyer_rmc, contractor_tier, idv_scope, scope_class, service.
- Depot-only axes (buyer_rmc / contractor_tier / idv_scope) carry sentinel **`n/a`** on
  non-depot atoms and **`unmapped`** on depot atoms with no J998J999 tag match — so nothing
  silently drops and the enrichment delta is disclosed.

## New modules
- `sheets/taxonomy_mro.py` — non-sheet helper (modelled on `_crosstab.py`). Consolidates the
  vocabularies that used to be **hidden** in `chartdata_output.py` (RMC buckets, contractor
  tiers, IDV scopes, marauder hulls, prime lists) + `model_depot_ship_repair.py`. Holds
  `AXES`, `SCENARIOS` (9), `SCENARIO_SPEC` (axis→target buckets), classifiers
  (`work_segment_for_psc`, `hull_group`, `scope_class_for`, `rmc_bucket`), `CAPTIVE_PARENT_MARKERS`.
- `sheets/data_tam_atoms.py` — native `TAMAtoms` table; one atom per source row (8,644 atoms).
  **Dollars from ONE table per atom** (Awards for services+depot, PSC1905 for embedded);
  `J998J999Data` joined on PIID **only to attach depot tags**, never as a dollar source. The
  per-atom inclusion cube (9 `inc_<scenario>` + `inc_selected`) sits to the RIGHT of the
  ledger and is emitted in `_render()` via a **lazy import** of `inputs_scenarios` (breaks the
  data↔inputs cycle). Positions are constant-derived so accessors work at import.
- `sheets/inputs_scenarios.py` — editable 0/1 axis matrix (`tbl_mro_scenarios`); rows
  machine-derived from `distinct_tags(axis)` so every tag (incl. sentinels) has a row;
  whole-number 0/1 data validation; defaults from `SCENARIO_SPEC`.
- `sheets/model_sam_build.py` — compact reader. Each scenario SAM = `SUMPRODUCT(amount,
  inc_<k>)`; per-axis inclusion factor = `SUMIFS(flag_axis_range, key_axis_range, atom_tag_cell)`
  which returns **0 on miss (no `#N/A`)**, with coverage guaranteed by the machine-derived
  matrix. §1 menu · §2 base+QA-1..7 · §3 selected · §4 selected drilldowns.

## Modified modules (consumers wired to the producers)
- `sheets/__init__.py` — registered `inputs_scenarios` (inputs), `model_sam_build` (model,
  after `model_private_addressable`), `data_tam_atoms` (data) in group order.
- `sheets/inputs_assumptions.py` — §3 selected-SAM-scenario dropdown + `selected_scenario_cell()`.
- `sheets/summary_executive_summary.py` — §4 SAM scenario menu (links only).
- `sheets/guide_methodology.py` — TAM/SAM/addressability definitions + §2d SAM engine + the
  explicit "scenario SAMs are a MENU — do NOT sum" warning.
- `sheets/outputs_figure_register.py` — S08 DO-rows (selected SAM, % TAM, broad addressable,
  every scenario SAM + % TAM).
- `sheets/chartdata_output.py` — §5 funnel → **§5 SAM Scenario Menu** + **§5b Selected
  Scenario Drilldown** (sourced from SAM Build); hidden constants now import from `taxonomy_mro`.
- `qa/tie_out.py` — added `SAM Build` to `_ENGINE_TABS`; baseline `engine_multiset` regenerated.

## Key figures (FY2025)
- atoms total $8,971.02M (services 7,066.87 + embedded Central 1,904.16) ties to Reconciled
  TAM ($8,970.87) within **$0.16** (embedded classifier rounding vs the hardcoded $1,904 anchor).
- Broad TAM 8,971.02 (=100%), Broad Addressable 7,134.69, Core Depot 4,780.91 (=depot),
  USCG 272.62 (=CG TAM), Regional Yard 392.73, MSC/Aux 551.44, Technical Services 430.88,
  Electronics & C4ISR 332.81, Target Hull Set 623.15.
- Depot dollar-source delta disclosed (SAM Build §2b): J998J999Data $5,007.78M vs Awards
  depot $4,780.91M ≈ **$227M** not in the Awards depot universe; unmapped depot atoms = $0.

## Two bugs caught + fixed
1. **dataValidation `<formula1>` unescaped `&`** — the scenario dropdown embedded
   "Electronics & C4ISR"; the raw `&` is invalid XML. **soffice silently tolerated it and the
   tie-out passed**, but openpyxl/Excel reject it. Fixed `inputs_assumptions._dv_list` to
   XML-escape. Lesson: validate the **raw** build XML (expat/openpyxl on the un-recomputed
   file), not just the soffice-recomputed copy.
2. **Drilldown sentinel tie gap** — `SAM Build §4c/§4d` drilldowns used curated RMC/tier label
   lists with no `n/a` row, so for **non-depot** selected scenarios (atoms carry
   buyer_rmc/tier = `n/a`) the per-axis totals showed ~0 instead of tying to selected SAM.
   Fixed by driving §4c/§4d from `distinct_tags(axis)` (includes `n/a`/`unmapped`). Verified:
   for selected = "Electronics & C4ISR", all four drilldowns now total 332.81 = selected SAM.

## QA / tie-out (both gates green)
- **Invariant B** (86 legacy model figures) unchanged — no regression in the existing model.
- **Invariant A** engine value-multiset regenerated (6,346 values) and passes the hard gate.
- soffice full recompute of the workbook = ~14s; **no `#N/A` anywhere** in SAM Build or the
  TAMAtoms cube.
- Live editability confirmed: switching the selected scenario moved Selected SAM 4,780.91 →
  8,971.02; flipping the Core Depot × HM&E matrix flag moved Core Depot 4,780.91 → 5,718.67.

## Verify / regenerate
```bash
cd projects/mro/workbook
python3 build_workbook.py                                  # green: 22 sheets, 9 native tables
XLSX="../20260607_Defense Drivers MRO_vS.xlsx"
python3 qa/tie_out.py regen-baseline qa/gold/baseline.json "$XLSX"   # self-asserts Invariant B
python3 qa/tie_out.py compare qa/gold/baseline.json "$XLSX" --invariant-a fail   # TIE-OUT OK
```

## Deferred / follow-ups (not done — by decision or pending business input)
- **Source Index / References** future-pull rows (parent IDV vehicles, multi-year awards, TAS,
  entity enrichment, opportunities, availability plan, FSRS subawards) — **deliberately
  deferred** per the planning decision; add when each pull lands. New-module documentation
  rows (TAMAtoms / taxonomy / scenarios / SAM Build) not yet added.
- SAM QA not yet surfaced in the validation sheet (lives in `SAM Build §2` today).
- No committed Python atom-vs-formula regression test (validation was performed interactively
  and matched Excel exactly).
- Scenario **defaults** are defensible seeds; business tuning (e.g. Regional Yard +Tier 3,
  USCG +cutter hulls) is a leadership call — the 0/1 matrix is editable in Excel.
- `z_ChartData §13` top-down funnel uses a negative "end" bar — **pre-existing**, untouched by
  this work; depends on the deck think-cell waterfall convention (not changed blind).

## Files
- new: `sheets/taxonomy_mro.py`, `sheets/data_tam_atoms.py`, `sheets/inputs_scenarios.py`,
  `sheets/model_sam_build.py`
- edited: `sheets/__init__.py`, `sheets/inputs_assumptions.py`,
  `sheets/summary_executive_summary.py`, `sheets/guide_methodology.py`,
  `sheets/outputs_figure_register.py`, `sheets/chartdata_output.py`, `qa/tie_out.py`,
  `qa/gold/baseline.json` (engine_multiset regen)
- review copies (snapshot only): `projects3/updated/updated_*.py`
