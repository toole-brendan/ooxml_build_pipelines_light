# 2026-06-02 — DDG workbook restructure: 10 → 23 tabs, one module per sheet, answer-first

## Scope

Substantial restructure of `core/ddg/workbook/workbook_ddg` (the Destroyer
Outsourced Construction DDG-51 Flight III TAM/SAM workbook). Rebuilt from **10
composite tabs (8 source modules)** into a **23-tab, answer-first workbook with ONE
source module per rendered sheet** (plus one shared non-sheet helper). This mirrors
the submarine 19-tab restructure logged at
[../../../logs/2026-06-02_sub_workbook_19tab_restructure.md](../../../logs/2026-06-02_sub_workbook_19tab_restructure.md).
The calc chain is preserved; the work is the tab split, accessor re-homing, two
control relocations, the headline semantic fix, and net-new presentation blocks.
**Zero `workbook_core` changes** — and this fixes the DDG build, which was broken.

Plan approved before implementation. Two decisions taken with the user (see §0).

## 0. Decisions carried in from the user

- **Registration idiom = per-module `SheetEntry`** (matching the submarine reference,
  not the spec's module-first `TAB_NAME`/`render()` variant). Both are accepted by
  `package_workbook()`; this keeps DDG and submarine structurally identical. Each
  module exposes one `SheetEntry` constant; `sheets/__init__.py` lists them.
- **Styling deferred** (matching submarine). This pass = structure + accessor
  preservation + formulas + verification only. No `§N` banners, no green/blue
  restyle beyond existing usage, no total-row restyling. Section banners stay
  descriptive (as the old composites had them).

## 1. Why this was the moment — the broken build

The submarine restructure had already edited the shared
`core/workbook_core/groups.py` to add a `summary` group first and reorder `model`
before `data`. DDG's registry was still in the old order, so
`package_workbook()`'s `_assert_group_blocks()` (group contiguity + canonical
order) **failed on every DDG build**. Conforming DDG to
`summary → guide → inputs → model → data → outputs → validation → sources` is
exactly what fixes it. No core file was touched.

## 2. New file layout — `workbook_ddg/sheets/`

The 8 composite modules were **deleted** (`guide_sheets, input_sheets,
budget_data_sheets, corpus_sheets, tam_sheets, sam_sheets, deck_audit_sheets,
source_sheets`) and replaced with **23 sheet modules + 1 helper**:

- **`_taxonomy.py`** (NEW, non-sheet helper, NOT in SHEETS) — the load-bearing
  bucket vocabulary + `classify()` (3-arg, description-led for DDG), extracted from
  the former `guide_sheets`. Keeping it out of any renderer means a consumer
  (entities, sam_build, bucket_evidence, inputs, scenarios) never imports a
  rendering module; `_taxonomy` is a true leaf.
- **23 sheet modules**, each one `SheetEntry`, in registry order:
  `executive_summary, methodology, inputs, scenarios, tam_build, sam_build,
  scn_budget, production_schedule, ap_bridge, pop_corpus, entities, locations,
  vendors, fpds_primes, bucket_evidence, deck_outputs, qa_checks, figure_audit,
  sensitivity, scope_exclusions, pop_audit, source_lineage, references`.

Old visible tab → new tab(s):

| Old | New |
|-----|-----|
| `Methodology` | `Methodology` (shortened: tab-map + version-history prose dropped; taxonomy → `_taxonomy.py`) |
| `Inputs` (Control + Scenarios) | `Inputs` (+ stream toggles + bucket adjustments), `Scenarios` (matrix) |
| `Budget` (SCN/Production/AP) | `SCN Budget`, `Production Schedule`, `AP Bridge` |
| `Corpus` | `POP Corpus` |
| `Suppliers` (Entities/Locations/Vendors/FPDS/Buckets) | `Entities`, `Locations`, `Vendors`, `FPDS Primes`, `Bucket Evidence` |
| `TAM` | `TAM Build` (answer-first: at-a-glance on top) |
| `SAM` | `SAM Build` (answer-first: scenario menu on top) |
| `Deck_Outputs` | `Deck Outputs` |
| `Audit` (Gate/Figures/Sensitivity/Scope/POP) | `QA Checks`, `Figure Audit`, `Sensitivity`, `Scope Exclusions`, `POP Audit` |
| `Sources` (Lineage/References) | `Source Lineage`, `References` |
| (new) | `Executive Summary` |

Visible tab names use spaces; module files, accessor names, and native-table names
keep underscores. Native tables (9, all workbook-unique) preserved on Scenarios,
Production Schedule, POP Corpus, Entities, Vendors, FPDS Primes, Source Lineage, and
References (×2).

## 3. The two control relocations + accessor re-homing

The composite `R(orig)=base+(orig-2)` row-rebasing was dropped — each tab owns row 1,
so sections stack from a fresh base. All ~80 accessors keep their names; consumers
import from the new owner. Two relocations changed an owner:

- **Stream include-toggles → `inputs.py`** (`include_bc_stream_cell`,
  `include_ap_lltm_stream_cell`), moved off TAM Build. TAM Build's stream-base
  formulas now reference the Inputs toggle cells and display them as green links
  (mirrors submarine).
- **Bucket-share Adjustment → `inputs.py`** (`bucket_adjustment_cell`), moved off
  SAM Build (the spec's *lighter* approach, NOT submarine's observed-share
  relocation). Observed and modeled shares stay computed on SAM Build; the
  Subawards "Adj +/-" column is now a green link to Inputs and modeled =
  `observed + Inputs adjustment`. This keeps `inputs.py` a near-leaf (imports only
  `_taxonomy`) — **no import cycle**, no lazy import needed.

Other owner changes (mechanical extraction): `scn_cell`→`scn_budget`;
`hull_count`/`in_window_hull_count`→`production_schedule`; AP gross/inwindow/tam
cells→`ap_bridge`; POP ranges→`pop_corpus`; entity ranges + `classify`-driven
table→`entities`; the 5 POP coverage/$/partition cells→`pop_audit`;
`REGISTRY`/`value_cell`/`source_ref`/`is_pct`→`deck_outputs`;
`fail_count_formula`→`figure_audit`; QA → `qa_checks` (+ new `fail_count_qa_formula`);
`dataset_row_cell`→`source_lineage`; `source_ref_cell`→`references`. The dual-named
`ap_lltm_base_cell` (raw on `inputs`, TAM-derived on `tam_build`) and
`portfolio_tam_cell` (SAM-local basis on `sam_build`) are preserved as-is.

## 4. The deck_audit_sheets 6-way split + the headline fix

`deck_audit_sheets` (2 tabs, 5 audit sections, one factory) split into
`deck_outputs → figure_audit → qa_checks` (+ `sensitivity`, `scope_exclusions`),
with the POP audit builder moved to `pop_audit.py` (it reads `pop_corpus` ranges).
The producer→consumer direction is acyclic:
`pop_corpus → pop_audit → deck_outputs → figure_audit → qa_checks`, with
`executive_summary` and the deck contract as terminal consumers.

**Headline TAM source fix:** the `portfolio_tam` defined name and DO-01 now source
from `tam_build.portfolio_tam_cell()` (the true TAM producer), not the SAM
allocation layer. Confirmed in the built file: `portfolio_tam -> 'TAM Build'!$I$91`
(`portfolio_bc_tam`/`portfolio_ap_tam`/`bc_supplier_coeff` also → 'TAM Build';
`sam_broad` → 'SAM Build'). The five defined-name *strings* are unchanged, so the
downstream deck contract is unaffected. Defined names stay centralized on
`deck_outputs.py`.

## 5. Net-new presentation blocks

Answer-first per the spec, links-only (never recompute):
- **`executive_summary.py`** (NEW) — headline KPIs, TAM bridge, SAM scenario menu,
  bucket allocation (unbucketed residual visible), audit status, caveats; green
  links to TAM Build / SAM Build / POP Audit / Figure Audit / QA Checks.
- **TAM Build / SAM Build** — compact at-a-glance summary reserved at the top
  (rows 4-13 / 4-10), section bodies below; links to the promoted producer cells.
- **Entities** — Role summary + Bucket summary roll-ups; **POP Corpus** — field
  guide; **Production Schedule** — model-window block; **Vendors** — concentration;
  **Scenarios** — definitions + selected-scenario readout; **QA Checks** — status
  block + failure-detail; **Figure Audit** — tie-out status; **POP Audit** —
  exported-audit-cells note; **Source Lineage** — consumers-by-model-area.

## 6. Verification (read-only / structural — the agreed ceiling)

`python build_workbook.py` → **23 sheets in the target order, first tab
`Executive Summary`, 96,755 bytes, 9 native tables**; the packager's sheet/table/
defined-name validators **and the group-contiguity assertion all passed** (the
broken build is fixed). A read-only scan of the built `.xlsx` confirmed:
- 23 sheets, correct order; **no underscores / no numeric prefixes** in any visible tab.
- **Zero stale references** to any retired tab (`'Budget'!`, `'Suppliers'!`,
  `'Corpus'!`, `'TAM'!`, `'SAM'!`, `'Audit'!`, `'Deck_Outputs'!`, `'Sources'!`) and
  **zero dangling references** across all 598 formulas; every referenced tab is one
  of the 23 (12 tabs are formula-referenced).
- Defined names point to producers (headline fix `portfolio_tam → 'TAM Build'!$I$91`).
- Spot-checked the highest-risk relocated chains: the modeled-share chain (7 SAM
  `D+E` cells, the `E` column links to `'Inputs'!C35:C41`); the scenario
  `SUMPRODUCT('SAM Build'!C42:C48,'Scenarios'!C7:C13)` (×5); the TAM bridge
  (`'TAM Build'!C35` BC coeff applied to per-FY BC base).

**Environment:** `python` on PATH; read-only probe + a temp verifier (removed
after); no mutations beyond the workbook build output.

## 7. Deliberately NOT done / known gaps

- **No Excel recompute.** `QA Checks` and `Figure Audit` FAIL = 0 cannot be confirmed
  in this environment (they require Excel to evaluate the formulas). The formula
  chains are verified intact and reference valid cells, and the QA identities hold by
  construction, so they should evaluate to 0 on open — a real Excel pass is the
  remaining confirmation.
- **No styling upgrade** — deferred to a follow-up (per the user): compact `§N`
  banners, total-row styling, green-link/blue-input discipline beyond existing usage.
  Native tables kept their existing `TableStyleLight1` (a styling follow-up can switch
  them to the core no-format default).
- **No `§N` section-numbering labels** — descriptive banners kept (matches submarine).
- **`validate_workbook.py`** at the workbook root is stale (points at an old output
  filename, openpyxl-based); the stdlib `sheet_probe` is the live verifier. Left as-is.

## 8. Files changed this session

- **Added:** `workbook_ddg/sheets/_taxonomy.py` + the 23 sheet modules listed in §2.
- **Rewritten:** `workbook_ddg/sheets/__init__.py` (registry → 23 SheetEntries in the
  new group order; `_taxonomy` imported but not registered).
- **Deleted:** the 8 former composite modules (§2) + `sheets/__pycache__`.
- **Unchanged:** `workbook_ddg/lib.py`, `build_workbook.py`, all of `core/workbook_core/`.
- **Rebuilt artifact:** `20260601_Destroyer Outsourced Construction_vS.xlsx` (23 tabs).
- **This log.**

## 9. Follow-ups

- **Open in Excel** to confirm numeric tie-out (QA Checks 0 FAIL, Figure Audit 0 FAIL,
  bucketed TAM = portfolio TAM, broad SAM ≤ TAM, AP/LLTM stream ≤ in-window CY AP) and
  that no cell trips a repair dialog.
- **Styling upgrade** (the deferred pass).
- **DDG deck pipeline** (`core/ddg/deck`) can point at the new producer cells / defined
  names; the defined-name strings are preserved, so its contract is unaffected by this pass.

## How to rebuild

```text
cd "core/ddg/workbook"  &&  python build_workbook.py
```
