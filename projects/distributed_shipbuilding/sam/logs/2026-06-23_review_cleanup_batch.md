# 2026-06-23 — Award-classification workbook: review-driven consolidation & cleanup batch

Executed an external design review's recommendations on
`award_classification/workbook_award_classification_refactor` (`award_classification_refactor.xlsx`),
**excluding the transaction-sheet edits** (per the user). Seven independent workstreams (E, G, F, A,
B, D, C), each built + validated + style-audited on its own, with name-keyed worksheet-XML byte-diffs
confirming that only the intended sheets changed at each step.

**Final state: 21 → 19 sheets, 15 native tables** (table count unchanged). Build clean — **0 XML
errors, 0 error-literal cells, 0 style hard-failures, 0 warnings**. All changes are **working-tree
only** — nothing committed (HEAD `631edbdf` was clean for this project at session start; the only
pre-existing dirty paths were under the unrelated `projects/other/awards_methodology/`).

- Plan file: `~/.claude/plans/please-consider-doing-all-rustling-babbage.md` (user-approved).
- Inputs read this session (the 5 prior logs): concentration-accessor anchor unification,
  AP/LLTM/EOQ scope audit, subaward-activity churn split, methodology lean rewrite, subaward-activity
  review incorporation.

**Decisions locked with the user before coding** (via AskUserQuestion):
- **#3 Supplier-Master spine = reduced scope** (sheets + guard read from Supplier Master; prose moves
  into Supplier Master; keep `*_program_vendors.csv` for research-prep; do not delete the CSVs / retire
  the builder).
- **#5 Taxonomy + Methodology = keep separate** (no merge — it conflicts with the recent lean rewrite
  and the two use different layouts).
- **#9 Operating Role (R) = remove**; rename `Resolution → Mapping Status`.
- **#2 HII Co-Build = fold a condensed ledger into Market Bridge, delete the tab** (drop the CRS
  cross-check / 10-K bound detail).

Two findings surfaced during exploration that shaped scope: `workbook_core/groups.py` is a **shared**
module (so regrouping was done without touching it), and `*_program_vendors.csv` is consumed by **5
research-prep scripts** (so reduced scope keeps it).

---

## Verification (final)

```
python3 build_workbook.py     # 19 sheets, 15 native tables, 7 note parts
python3 validate_workbook.py  # 70 parts, 0 xml errors, 0 error-literal cells
python3 tools/style_audit.py  # 0 hard failures, 0 warnings
```
(PYTHONPATH = `<REPO_ROOT>:<workbook dir>`.) Grep gates over the built workbook: **0** occurrences of
`Parent Concentration`, `HII Co-Build`, `NAICS-6 Archetype Map`, `Vendor Archetype Overrides`,
`HII Work-Item SWBS Crosswalk`, `Operating Role`. Source gates: **0** `W_CONF`, **0** hardcoded
`/Users/brendantoole/projects3/...` paths in scripts/corpus. `py_compile` passes on every sheet module
+ script.

**Final group layout** (group-contiguous, canonical order):
- **summary** — Executive Summary · Domain Concentration · Subaward Activity · Market Bridge
- **guide** — Taxonomy · Methodology
- **inputs** — Mapping - NAICS Defaults · Mapping - Vendor Overrides · Mapping - HII Code to SWBS · Deflators
- **model** — Supplier Master · DDG Program Vendors · DDG SWBS by Ship-System · Virginia Program Vendors · Columbia Program Vendors
- **data** — Prime Awards · DDG / Virginia / Columbia Subaward Transactions

**Cumulative sheet diff vs the pre-session baseline:** removed Parent Concentration, HII Co-Build
Workshare, and (by rename) the 3 old mapping tabs; added Mapping - NAICS Defaults / Vendor Overrides /
HII Code to SWBS; `~` on Domain Concentration, Executive Summary, Market Bridge, Methodology, Taxonomy,
Supplier Master, DDG/Virginia/Columbia Program Vendors, DDG Subaward Transactions, Deflators;
**unchanged**: Subaward Activity, DDG SWBS by Ship-System, Prime Awards, Virginia/Columbia Subaward
Transactions.

---

## Workstream detail

### E — Confidence cleanup
- `extracted/swbs_curated_c.csv`: dropped the `Confidence` column (22 data rows; now 3 cols).
- `scripts/build_swbs_crosswalk.py`: removed the `conf` read; Evidence is now `Rationale` verbatim
  (no `[High]`/`[Medium]` prefix); docstring de-confidence'd. Regenerated `hii_swbs_crosswalk.csv`
  (113 X + 22 C = 135 rows).
- `sheets/_widths.py`: `W_CONF (=15) → W_SHORT_FLAG` (it is a width for short code/basis/date columns,
  not a confidence field). Updated its 8 use sites across `naics6_archetype_map.py`,
  `vendor_archetype_overrides.py`, `supplier_master.py`, `_program_vendors.py`.
- `CLASSIFICATION_METHODOLOGY_OVERVIEW.md`: removed the A/B/C/U confidence coverage-segmentation line
  (kept the assignment-basis segmentation).
- **Verify:** built workbook went 16×`[High]` + 6×`[Medium]` → **0** (the labels lived in hover notes,
  not visible cells, so worksheet XML was byte-identical; the note part shrank); SWBS codes/basis
  byte-identical.

### G — Pipeline path cleanup
- **Added `scripts/_paths.py`** — `REPO / REFACTOR / AC / EXTRACTED / SCRIPTS / CORPUS_SCRIPTS` derived
  from `Path(__file__).resolve()`, with an `assert REPO/"workbook_core"` self-check.
- Replaced **18** hardcoded `/Users/brendantoole/projects3/ooxml_build_pipelines_light` literals: 16
  `from _paths import REPO`, the multi-line `REFACTOR = Path(...)` form in 4 worklist scripts
  (`merge_archetype_pulls`, `build_primary_output_worklists`, `extract_research_results`,
  `merge_research_pulls`, `build_capability_domain_worklists` → `from _paths import REFACTOR`), and
  `corpus/scripts/_corpus.py` → self-derives via `parents[6]`.
- **Added `scripts/rebuild_all.py`** — one orchestrator declaring the generated-artifact order
  (`pull_prime_awards` [gated `--pull`] → `build_prime_scope_manifest` → `build_swbs_crosswalk` →
  `tag_ddg_transactions_swbs` → `build_program_transactions` → `build_program_vendors` →
  `build_supplier_master` → `build_subaward_activity` → `build_ddg_swbs_rollup` → `build_workbook`),
  passing `PYTHONPATH` to the build stage and preserving the integrity asserts (no bypass).
- **Verify:** all scripts compile; `_paths` resolves to the right absolute paths; `build_program_vendors`
  + `build_supplier_master` re-ran and reproduced their CSVs identically; the workbook stayed
  byte-identical (G touches no build input). `rebuild_all.py --list` prints the plan. A full chain run
  was **not** exercised (the transaction builder is heavy).

### F — Remove the Operating Role (R) axis; rename Resolution → Mapping Status
- `extracted/naics6_archetype_map.csv`: dropped `Operating Role (R, internal)` + `R Rationale`; renamed
  `Resolution → Mapping Status` (176 rows; 10 → 8 cols).
- `sheets/naics6_archetype_map.py`: removed R from `input_cols` / the R-Rationale note map / `_WIDTHS`
  (6 → 5 visible); `Resolution → Mapping Status`; docstring + intro de-R'd.
- `sheets/_taxonomy.py`: removed `ROLE_INTRO` + `ROLES`; renumbered the Output/SWBS section comments;
  rewrote the 3-axis docstring to two published axes (D, P); `GRAIN_INTRO` drops "role".
- `sheets/taxonomy.py`: removed the §2 Operating Role legend; renumbered §3 Output → §2, §4 SWBS → §3;
  dropped the `ROLE_INTRO, ROLES` import; docstring de-R'd.
- `sheets/guide_methodology.py`: removed the §2 Operating Role KV; "Three → Two independent entity
  axes"; "D / R / P → D / P" in the §4 Inputs NAICS-map line.
- **Verify:** **0** `Operating Role` / role text in the built workbook; `Mapping Status` present; no
  formula consumed R/Resolution. Critically, the P-column lookup followed the layout shift —
  `naics_map_cols("Primary Output (P)")` → **col E** (the real P column, distinct from `Mapping Status`
  at F), confirming no silent miswire. Supplier Master changed only by that P-column-letter ripple.

### A — Merge Parent Concentration into Domain Concentration
- `sheets/domain_concentration.py`: appended 6 ultimate-parent columns (cols L..Q): Parent Top-1 %,
  Parent HHI, Parent Eff Firms, Parent Firms, HHI uplift, Firm reduction — reusing the existing hidden
  program-vendor helpers (`Parent Domain $` / `Parent HHI Numerator` / `Parent Firm Weight`). Extended
  `_HEADERS`/`_COLS`/`_NCOLS` (10 → 16), `_BODY_STY`, and the total row; the diagnostics retarget Domain
  Concentration's own `HHI` (col I) and `Suppliers` (col E). Updated the caveat + docstring.
- `sheets/executive_summary.py`: dropped the `parent_conc_range` import; §3 now reads
  `domain_conc_range(name, "Parent Top-1 %")`; updated the §1 caveat.
- `sheets/__init__.py`, `sheets/_tabs.py`: removed the `parent_concentration` import/registry entry and
  `TAB_PARENT_CONC`.
- `sheets/_program_vendors.py`: two comments "Parent Concentration → Domain Concentration".
- **Deleted** `sheets/parent_concentration.py` and the dead `scripts/build_parent_concentration.py`.
- **Verify:** the new parent formulas are byte-identical to the old Parent Concentration sheet (only
  self-ref column letters remapped: H→M, D→I, F→E, J→O); existing cols C..K unchanged; Exec §3 now
  references `'Domain Concentration'!$L`; no leftover refs. 21 → 20 sheets.

### B — Fold HII Co-Build into Market Bridge, delete the tab
- `sheets/market_bridge.py`: replaced the §3 "Co-build derivation" pointer with a self-contained
  ledger — Virginia Low ($10.2B, Block V 2023-05-24 cumulative) + Columbia Low (~$3.4B lineage-summed)
  basis rows + a Sources row (CRS / DoD announcements / HII disclosures / FAR 52.204-10) — keeping the
  existing overlap/scenario/scope rows; renamed §3 to "Derivation, disclosed ledger & sources"; dropped
  the CRS cross-check and 10-K bound. Updated the docstring pointer.
- `sheets/executive_summary.py` + `sheets/domain_concentration.py`: "see HII Co-Build (Workshare)" →
  "see Market Bridge" (caveat + docstring).
- `sheets/__init__.py`, `sheets/_tabs.py`: removed the `hii_co_build` import/registry entry and
  `TAB_HII_CO_BUILD`. **Deleted** `sheets/hii_co_build.py`.
- **Verify:** **0** "HII Co-Build" in the built workbook; note parts 7 → 6 (the removed CUM_NOTE). 20 →
  19 sheets.

### D — Rename + regroup the mapping / dimension / deflator tabs
- `sheets/_tabs.py` renames (all ≤31 chars, ASCII hyphen): `NAICS-6 Archetype Map → Mapping - NAICS
  Defaults` (24), `Vendor Archetype Overrides → Mapping - Vendor Overrides` (26), `HII Work-Item SWBS
  Crosswalk → Mapping - HII Code to SWBS` (26).
- Regroup via per-sheet `group=` + a `SHEETS`/import reorder, **no edit to the shared
  `workbook_core/groups.py`**: `hii_swbs_crosswalk.py` and `deflators.py` `data → inputs`;
  `supplier_master.py` `data → model`. Updated `__init__.py` docstring + group comments.
- Updated docstrings naming the renamed sheets (the 3 accessor docstrings + `supplier_master.py`).
  Formulas auto-followed (all cross-sheet refs go through the `TAB_*` constants).
- **Verify:** **0** old mapping names in the built workbook; new names present; group-contiguity assert
  passed; the expected ripples appeared (Supplier Master + DDG Transactions formula-ref renames,
  Methodology Inputs text, Deflators/Supplier Master tab-color) and nothing else.

### C — Supplier Master as the sole Program×UEI spine (REDUCED scope)
- `scripts/build_supplier_master.py`: added `Role / Description` + `Source URLs` columns, sourced via
  the **exact** `build_program_vendors` prose precedence (research_prose[uei] → old_prose[uei] →
  old_prose[dollar-modal parent], reusing the imported loaders + `d["pudol"]`).
  **Cross-checked: 0 prose mismatches** vs the program-vendor CSVs across DDG/Virginia/Columbia.
- `sheets/_flat.py`: added a backward-compatible `table=(headers, rows)` override to `make_flat_sheet`
  (defaults to `load_table(csv_name)` — zero blast radius on the ~10 other flat sheets) and a
  `headers=` override to `flat_header_letters`.
- `sheets/_program_vendors.py`: added `PV_HEADERS` (the canonical program-vendor column layout) and
  `_program_vendor_table(program)` — builds the sheet's rows from `supplier_master.csv` filtered on
  Program (UEI + Role/Description + Source URLs as static leaf values; everything else is a live
  formula). `make_program_vendor_sheet` now passes `table=`, derives `_last` from the filtered count,
  and gets its letters from `flat_header_letters(headers=PV_HEADERS, ...)`. The program-vendor CSV is
  no longer a workbook input.
- `sheets/supplier_master.py`: render `Role / Description` (W_TEXT_WIDE) with `Source URLs` folded into
  a hover Note (`note_from`); updated `_CSV_WIDTHS`/`_L`/docstring/intro.
- **Verify:** identical UEI set + **0** Role/Description mismatches per program (DDG/Virginia identical
  row order; Columbia reordered only by a dollar-tie-break — cosmetic, same set/values); the D/P lookup
  correctly follows the SM column insertion (program-vendor D cell `INDEX`es `'Supplier Master'!$N`,
  the real `override_or_map` D column, not Role/Description at K); Domain Concentration / Executive
  Summary / Market Bridge byte-identical. The 3-way universe guard passed at build.

---

## Complete file inventory

**Added (2):** `scripts/_paths.py`, `scripts/rebuild_all.py`.

**Deleted (3):** `sheets/parent_concentration.py`, `sheets/hii_co_build.py`,
`scripts/build_parent_concentration.py`.

**Modified — sheet modules / helpers (16):** `__init__.py`, `_flat.py`, `_program_vendors.py`,
`_tabs.py`, `_taxonomy.py`, `_widths.py`, `deflators.py`, `domain_concentration.py`,
`executive_summary.py`, `guide_methodology.py`, `hii_swbs_crosswalk.py`, `market_bridge.py`,
`naics6_archetype_map.py`, `supplier_master.py`, `taxonomy.py`, `vendor_archetype_overrides.py`.

**Modified — scripts (17):** path-only (`build_capability_domain_worklists`, `build_columbia_hedge_worklist`,
`build_ddg_swbs_rollup`, `build_description_rerun_worklists`, `build_primary_output_worklists`,
`build_prime_scope_manifest`, `build_program_transactions`, `build_program_vendors`,
`build_research_worklist`, `build_subaward_activity`, `extract_research_results`,
`merge_archetype_pulls`, `merge_research_pulls`, `pull_prime_awards`, `tag_ddg_transactions_swbs`);
path + content (`build_supplier_master` — prose; `build_swbs_crosswalk` — confidence).

**Modified — data / other (5):** `extracted/swbs_curated_c.csv`, `extracted/hii_swbs_crosswalk.csv`,
`extracted/naics6_archetype_map.csv`, `extracted/supplier_master.csv`,
`corpus/scripts/_corpus.py`, plus `CLASSIFICATION_METHODOLOGY_OVERVIEW.md` and the regenerated
`award_classification_refactor.xlsx`.

---

## Deviations from the approved plan (both to reduce risk)

- **Universe guard left as the 3-way check** (`program-vendor == transaction == Supplier Master`) in
  `sheets/_integrity.py` rather than simplified to `SM == transactions`. The 3-way guard is strictly
  stronger, still passes, and `*_program_vendors.csv` survives for the worklists — so simplifying buys
  nothing. Simplify only if those CSVs are ever removed.
- **`build_program_vendors.py` left intact (not slimmed).** It still emits the full
  `*_program_vendors.csv` for the research-prep worklists. The reduced-scope win holds regardless: the
  workbook (sheets + the rendered universe) now sources identity + prose from the single Supplier-Master
  dimension, so there is no workbook-side drift; the aggregation in `build_program_vendors` now feeds
  only the worklists + the guard's `pv` leg.

## Carry-forward / gotchas

- ⚠️ **Do NOT run `scripts/build_archetype_overrides.py`.** It lifts archetype codes from
  `*_program_vendors.csv`, whose archetype columns are now blank placeholders, so it **silently
  overwrites the curated `vendor_archetype_overrides.csv` with a near-empty table** (it stripped 38
  rows when accidentally run during a worklist smoke-test this session; reverted via `git checkout`).
  Treat `vendor_archetype_overrides.csv` as a hand-curated source of truth; the generator is stale and
  is intentionally excluded from `rebuild_all.py`. (Saved as a memory.)
- **3 worklist scripts** (`build_research_worklist`, `build_description_rerun_worklists`,
  `build_columbia_hedge_worklist`) fail only because their output dir `projects/research_shared/` is
  absent from this checkout — they read `*_program_vendors.csv` fine. `mkdir -p projects/research_shared`
  to run them. (`build_primary_output_worklists` + `build_capability_domain_worklists` write to
  `award_classification/` and ran OK; their 6 regenerated worklist `.xlsx` were reverted.)
- **Columbia Program Vendors** row order now follows Supplier-Master's raw-dollar sort vs the old
  `round(dol,6)` sort — cosmetic only (same UEI set/values). Align the sort keys for a clean byte-diff.
- **Out-of-scope artifacts still carrying old vocab:** `extracted/taxonomy.csv` (vestigial export, not
  referenced anywhere) and `extracted/naics6_archetype_map.pre_mece.csv` (inactive) still contain
  `Operating Role` columns. The `classifications.csv` `Registry confidence` column is display-only.
- **Subaward Activity recalc verification** (a pre-existing gate from earlier logs) is untouched —
  the sheet is byte-identical this session; that gate stands on its own before a commit.
- **Nothing committed** — all working tree. A full `python3 scripts/rebuild_all.py` was not run
  end-to-end (heavy transaction builder); `--list` + per-generator reproduction were verified.
