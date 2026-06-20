# 2026-06-02 — sub workbook restructure: 10 → 19 tabs, one module per sheet, answer-first

## Scope

Substantial restructure of `core/submarine/workbook/workbook_sub` (the Distributed
Shipbuilding Submarines TAM/SAM workbook). Rebuilt from **10 consolidated tabs (8
source modules)** into a **19-tab, answer-first workbook with ONE source module per
rendered sheet** (plus one shared non-sheet helper). The calc chain is preserved;
the work is tab-registration, accessor re-homing, control relocation, the headline
semantic fix, and net-new presentation blocks. Also a one-line edit to the shared
engine (`core/workbook_core/groups.py`). DDG was deliberately **not** touched (its
build now breaks — see §1). Plan file approved before implementation; built against a
detailed sheet-by-sheet spec the user supplied, with two design forks resolved by the
user (see §0).

---

## 0. Decisions carried in from the user

Two forks were resolved by the user before any edit, and one structural directive
arrived after planning:
- **`Assumptions & Controls` becomes the PRODUCER of modeled bucket shares** (not
  just the editable adjustment). This is the more invasive of the two options — it
  repoints `modeled_share_cell` (which TAM allocation + QA depend on) and pulls the
  observed shares from a new producer on Entity Master.
- **Full enriched spec in one pass** — every section in the spec, including the
  net-new at-a-glance / role-bucket-basis summaries / unbucketed watchlist / register
  coverage / citation-completeness blocks, built before the first verification.
- **One module per rendered sheet** (mid-implementation directive, after the plan was
  approved against an "8-modules-transformed" structure). The plan file was updated to
  the one-module-per-sheet layout before coding.

Operating principle kept throughout: **summary/answer sheets LINK to producer cells
(green cross-sheet links); they never recompute.**

---

## 1. Engine change (shared) — `core/workbook_core/groups.py`

Added a `summary` group as the FIRST entry and reordered so `model` precedes `data`:

```
summary → guide → inputs → model → data → outputs → validation → sources
```

`("summary", "Executive summary", "6A4C93")` (purple; adjustable). Moving `model`
before `data` is what lets `TAM Build` / `SAM Build` sit ahead of the data appendix.

**Known, accepted consequence:** this reorders the *canonical* group order globally.
The ddg registry is still `data`-before-`model`, so **ddg's build now fails
`_assert_group_blocks`** until ddg is refactored the same way. The user explicitly
chose to let ddg break rather than add a compatibility shim. No ddg files were edited.

---

## 2. New file layout — `workbook_sub/sheets/`

The 8 consolidated modules were **deleted** (`guide_sheets, input_sheets,
budget_data_sheets, corpus_sheets, tam_sheets, sam_sheets, deck_audit_sheets,
source_sheets`) and replaced with **19 sheet modules + 1 helper**:

- **`taxonomy.py`** (NEW, non-sheet helper, NOT in SHEETS) — the load-bearing bucket
  vocabulary + `classify()` extracted from the former `guide_sheets`. Keeping it out
  of any rendering module means a consumer (entity_master, sam_build, …) never has to
  import a renderer, so `taxonomy` is a true leaf everyone can depend on.
- **19 sheet modules**, each exposing one `SheetEntry`, in registry order:
  `executive_summary, methodology_scope, assumptions_controls, tam_build, sam_build,
  scn_annual, lltm_ap, pop_location_parse, pop_source_audit, entity_master,
  location_master, worktype_evidence, figure_register, mib_excluded, sensitivity,
  number_audit, qa_reconciliation, source_index, references`.

Old visible tab → new tab(s):

| Old | New |
|-----|-----|
| `README_Methodology` | `Methodology & Scope` (front matter dropped) |
| `Inputs` | `Assumptions & Controls` (+ controls absorbed) |
| `Budget_Base` | `SCN Annual`, `LLTM AP` |
| `POP_Corpus` | `POP Location Parse`, `POP Source Audit` |
| `Vendor_Buckets` | `Entity Master`, `Location Master`, `Worktype Evidence` |
| `TAM_Model` | `TAM Build` |
| `SAM_Model` | `SAM Build` |
| `Deck_Outputs` | `Figure Register` |
| `Validation` | `MIB Excluded`, `Sensitivity`, `Number Audit`, `QA Reconciliation` |
| `Sources` | `Source Index`, `References` |
| (new) | `Executive Summary` |

Visible tab names use spaces; module files, accessor names, and native-table names
keep underscores.

---

## 3. The control relocation + accessor re-homing (the risky part)

Driven by the "A&C becomes producer" choice. New homes for load-bearing accessors:

- **Observed bucket shares + addressable total → `entity_master.py`** (new §Bucket
  summary): `observed_bucket_share_cell`, `observed_bucket_dollar_cell`,
  `addressable_total_cell` (moved from the old SAM subaward section). DO-07 now sources
  here. Also added §Role summary + §Basis summary.
- **Modeled shares + scenario matrix + stream toggles + selector → `assumptions_controls.py`**:
  `modeled_share_cell` (= observed link + adjustment), `bucket_share_range`,
  `modeled_share_total_cell`, `unbucketed_share_cell`, `bucket_adjustment_cell`,
  `scenario_keys/scenario_name/scenario_flag_range/scenario_flag_cell` (the `SCENARIOS`
  membership moved here), `include_bc_stream_cell`/`include_ap_lltm_stream_cell`,
  `selected_sam_scenario_cell`, plus `n_years_count_formula` / `fy_range_*_cell`.
- **`sam_build.py`** became a calc + linked-view sheet: observed shares link from
  Entity Master, modeled shares + scenario flags link from A&C, TAM allocation uses
  `assumptions_controls.modeled_share_cell`, and a new §Selected scenario uses
  `INDEX/MATCH` on the A&C selector.
- **`tam_build.py`** stream toggles now reference `assumptions_controls.include_*`; the
  n-years formula uses `assumptions_controls.n_years_count_formula()` (no more hardcoded
  `'Inputs'!C8-'Inputs'!C7`).

**Import-cycle break:** the only new cycle risk is `assumptions_controls ↔ sam_build`
(A&C's selector display needs SAM Build's selected cells, SAM Build needs A&C's modeled
shares). Broken exactly like the old `guide_sheets`: A&C's §Scenario-selector display
is built at **render time via a lazy `import sam_build`**; A&C's accessor-promoting code
(module load) depends only on `entity_master` + `taxonomy`, never `sam_build`. Final
module-level graph is acyclic (verified by a clean build).

---

## 4. Semantic + structural fixes folded in

- **Headline TAM source fix:** `Figure Register` DO-01 and the `portfolio_tam` defined
  name now source from `tam_build.cumulative_tam_cell()` (the true TAM producer),
  not the SAM tab's carried TAM basis. Confirmed in the built file: `portfolio_tam ->
  'TAM Build'!$C$108`.
- **Three hardcoded tab strings removed** (the Phase-11 "zero stale refs" goal):
  the former `'Inputs'!` in the AP accessors, `'Inputs'!C8-'Inputs'!C7+1` in TAM, and
  `'Deck_Outputs'!E…` in `value_cell` — all now flow through `_TAB`/accessors.
- **`Figure Register`** gained a Producer-tab column (parsed from each figure's `ref`)
  and is now a native table (`tbl_sub_figure_register`); `Number Audit` likewise
  (`tbl_sub_number_audit`). Build order preserved as cross-module imports
  (MIB → Figure Register → Number Audit → QA).
- **Net-new blocks** added per spec across nearly every tab (at-a-glance rollups,
  SCN portfolio rollup, Entity Master role/bucket/basis summaries, Location Master
  prime-flag block, Worktype Evidence unbucketed watchlist, MIB rationale/tie-outs,
  Number Audit exceptions, Source Index refresh control, References citation
  completeness, local TAM/SAM/LLTM check blocks).

---

## 5. Verification (read-only / structural — the agreed ceiling)

Built via `python build_workbook.py`: **19 sheets in the target order, first tab
`Executive Summary`, 130,999 bytes, 10 native tables**; the packager's sheet/table/
defined-name validators and the group-contiguity assertion all passed.

A read-only scan of the built `.xlsx` (using `sheet_probe.probe_file`) confirmed:
- 19 sheets, correct order, first = `Executive Summary`; **no underscores / no numeric
  prefixes** in any visible tab.
- **Zero stale references** to any retired tab name, and **zero dangling references** —
  every formula-referenced sheet is one of the 19 (13 sheets are referenced).
- 10 native tables, all workbook-unique, refs valid.
- Defined names point to the intended producers: `portfolio_tam → 'TAM Build'!$C$108`,
  `bc_supplier_coeff → 'TAM Build'!$C$46`, `ap_lltm_supplier_coeff → 'TAM Build'!$C$47`,
  `sam_broad → 'SAM Build'!$C$76`.
- Spot-checked the highest-risk formulas and confirmed correct: the modeled-share chain
  (`A&C E47 = C47+D47`, `C47 = 'Entity Master'!D178`; total `E55 = SUM(E47:E54)` = 1 by
  construction); the cross-sheet `SUMPRODUCT` scenario pairing (`SAM C74` electrical =
  `SUMPRODUCT('SAM Build'!C60:C66,'Assumptions & Controls'!E37:E43)`); the `INDEX/MATCH`
  selector; the relocated toggles + n-years. The QA identities (shares sum to 1,
  bucketed TAM = portfolio TAM, broad SAM = TAM − unbucketed) hold structurally.

**Environment:** `python` on PATH; read-only probe + a temp verifier (removed after);
no mutations beyond the workbook build output.

---

## 6. Deliberately NOT done / known gaps

- **No Excel recompute.** `Number Audit` FAIL = 0 and `QA Reconciliation` FAIL = 0
  cannot be confirmed in this environment (they require Excel to evaluate the formulas).
  The formula chains are verified intact and reference valid cells, and the QA identities
  hold by construction, so they should evaluate to 0 on open — but a real Excel pass is
  the remaining confirmation.
- **Figure Register at-a-glance omits the Number Audit fail-count link** — linking it
  would create a `figure_register → number_audit → figure_register` import cycle. That
  fail count lives on Number Audit, QA Reconciliation, and the Executive Summary
  audit-status block instead.
- **No §N section-numbering labels.** Used descriptive banners ("At a glance - …")
  consistently instead of the spec's `§N - Title` addressing, matching the existing
  pipeline voice; the Executive Summary "Source" column references sheets by name.
- **No styling upgrade** — out of scope for this pass (structure + content + verification
  only), per the recommended order.

---

## 7. Files changed this session

- **Engine (shared):** `core/workbook_core/groups.py` (summary group + reorder).
- **Added:** `workbook_sub/sheets/taxonomy.py` + the 19 sheet modules listed in §2.
- **Rewritten:** `workbook_sub/sheets/__init__.py` (registry → 19 SheetEntries in the
  new group order; `taxonomy` imported but not registered).
- **Deleted:** the 8 former consolidated modules (§2).
- **Rebuilt artifact:** `20260601_Distributed Shipbuilding Submarines_vS.xlsx` (19 tabs).
- **This log:** `core/logs/2026-06-02_sub_workbook_19tab_restructure.md`.

---

## 8. Follow-ups

- **Open in Excel** to confirm the numeric tie-out (Number Audit 0 FAIL, QA 0 FAIL,
  AP/LLTM additive base = 0, Broad SAM ≤ TAM, bucketed TAM = portfolio TAM) and that no
  cell trips a repair dialog.
- **DDG** needs the same restructure (its build is currently broken by the §1 group
  reorder): split its consolidated modules one-per-sheet, relocate controls to a DDG
  `Assumptions & Controls`, and re-home the observed/modeled-share producers.
- **Optional polish (next pass):** the styling upgrade; the deck pipeline can then point
  at the new producer cells / defined names.
