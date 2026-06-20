# 2026-06-07 (session 4) — MRO workbook native rewrite: Phase 3 complete (new groups + data tabs + registry)

## Scope

Continued the **full native rewrite** of the MRO workbook
(`projects/mro/workbook/workbook_mro/sheets`) from the Phase-2 checkpoint (all 10
formula sheets native; consumers reference producer accessors). This session did
**Phase 3**: added the five missing **guide / inputs / outputs / sources** sheets,
rewrote the two big raw data tabs into the explicit `_COLUMNS` idiom (and **deleted
`_datadump.py`**), and reordered `sheets/__init__.py` into the canonical **9-group
order**. The workbook now ships **18 sheets** matching the DDG / submarines group
structure end-to-end. Build is **green**: `build_workbook.py` → 18 sheets;
`qa/verify_crosstab.py` → OK; `qa/tie_out.py … --multiset warn` →
**`TIE-OUT OK — 88 names match`** with the only multiset deltas being the
pre-existing MSC/OP-5 source-line integers (every Phase-3 change added ZERO new
deltas). Plan + running log: `~/.claude/plans/putting-you-in-plan-enumerated-reddy.md`;
resume pointer in memory `mro-native-rewrite`.

## What the gate actually checks (the lever this phase relied on)

`qa/tie_out.py` has two parts: the **hard gate** `_name_msgs` (every baseline defined
name must still exist AND recompute to baseline within tol — and crucially it flags
**any *added* defined name** as a failure too), and the **multiset tripwire**
`_multiset_msgs` (per-sheet numeric multisets, run `warn` mid-migration; excludes the
3 raw data tabs; only diffs sheets present on **both** sides). Three consequences
drove the whole phase:

1. **New sheets are free.** Methodology / Assumptions / Figure Register / Source
   Index / References aren't in the frozen `baseline.json`, so they appear on the new
   side only → the multiset tripwire never compares them → **zero** messages. (inputs
   / outputs "intentionally add numbers", but those numbers live only on the new tabs.)
2. **The Figure Register must ship ZERO `defined_names`.** The DDG register declares
   ~10 deck names; doing that here would trip "DEFINED NAMES added" on the hard gate.
   So `outputs_figure_register` ships none — `value_cell(fid)` is the deck contract,
   every Value cell a pure `=accessor()` link.
3. **Rewiring the WPN/FMS plugs is value-neutral.** Replacing the literal `500` /
   `-100` on TAM Bridge & Private Addressable with `='Assumptions'!C…` recomputes to
   the same number → those two sheets (which ARE in the baseline) added zero deltas,
   confirmed by tie-out.

## Sheets added / changed

- **inputs_assumptions.py** (`inputs`, tab "Assumptions") — the editable surface. §1
  run settings (program, FY anchor, units, sizing-scenario selector); §2 the two
  out-of-scope plan plugs (**WPN ~$500M**, **FMS −$100M**) — the only non-source-pinned
  $ in the model. Data validations: whole-number FY, scenario list, decimal-bounded
  plugs. Accessors `wpn_estimate_cell`, `fms_estimate_cell`, `fy_anchor_cell`,
  `scenario_cell`.
- **model_tam_bridge.py / model_private_addressable.py** — rewired the WPN/FMS literals
  to read the inputs accessors (S_LINK_NUM); converted each to return
  `(SheetEntry, accessors…)` and promoted §-total cells for the Figure Register:
  `topdown_total_cell` / `bottomup_total_cell` / `bridge_gap_cell` (TAM Bridge) and
  `addressable_bottomup_cell` / `addressable_topdown_cell` / `convergence_delta_cell`
  (Private Addressable). WPN single edit point now (was used twice; FMS twice).
- **guide_methodology.py** (`guide`, tab "Methodology") — pure consumer. §1 definitions;
  §2 formula framework (§2a TAM = Navy+USCG services-MRO + embedded PSC 1905; §2b the
  **two-universe model** budget-pot vs award-data; §2c private-addressable derivation,
  with live links via reconciled_mro_tam / navy+cg / psc1905('EMBEDDED')); §3 sizing
  flow; §4 scope boundary; §5 exclusion rules; §6 **appropriation map** (1804N OMN vs
  1810N OPN no-double-count, SCN/WPN/MSC/USCG); §7 confidence levels. ExcelNotes on the
  key definitions.
- **sources_source_index.py** (`sources`, tab "Source Index") — native table
  `tbl_mro_source_index`; **live** data-row counts for awards/j998/psc1905 + the v433
  provenance entries; §2 consumers-by-model-area roll; accessor `dataset_row_cell`.
- **sources_references.py** (`sources`, tab "References") — two native tables
  (`tbl_mro_references_primary` 10 SRC-* + `tbl_mro_references_citations` 5 CITE-*);
  FPDS pulls, PSC 1905 classifier, OP-5/MSC/SCN/OPN/WPN/USCG exhibits, HII-MT EDGAR,
  PL 116-93, NAVSEA RMC structure, internal methodology; accessor `source_ref_cell`.
- **outputs_figure_register.py** (`outputs`, tab "Figure Register") — `tbl_mro_deck_figures`,
  16 figures (DO-01..16) across S05 headline / S06 bridge / S07 convergence / S17 prime
  landscape, each a pure `=accessor()` link into a producer/consumer cell. **Zero
  defined names.** Exposes `REGISTRY`, `value_cell`, `source_ref`, `is_pct`.
- **data_awards.py / data_j998_j999.py** — rewritten from the `build_datadump(...)`
  wrapper into explicit `_COLUMNS = [(csv_key, header, width, is_numeric), …]` + local
  `_make_*()` builders (matching `data_psc_1905_classified.py`). Headers + table names
  (`Awards` / `J998J999Data`) + numeric flags + `_num` semantics (blank→None, 0.0 kept)
  preserved exactly; csv_key == header (the CSV columns already carry the load-bearing
  labels). Added a text-only §2 "Use in model" (data tabs are excluded from the
  multiset, so this is gate-neutral). **`_datadump.py` deleted** (no other importers).
- **sheets/__init__.py** — `SHEETS` reordered into the canonical 9-group block order:
  summary(1) → guide(1) → inputs(1) → model(7) → data(3) → outputs(1) → validation(1)
  → sources(2) → chartdata(1). `_assert_group_blocks` passes (verified, incl. a negative
  control that the split-group check bites). Docstring rewritten for the 18-sheet native
  state.

## Gotchas / notes

- **`col_letter` is 0-indexed** (`col_letter(0)=="A"`). The table ref idiom
  `f"B{hdr}:{col_letter(n_cols)}{last}"` is therefore correct (Awards = `B…:AU…`, 46
  cols). Carried over from `data_psc_1905_classified.py`.
- **Awards row count = 24,027, not 28,219.** `wc -l` over-counts because Description /
  other quoted fields contain embedded newlines; `csv.DictReader` (and the old
  `csv.reader`) parse them as single records, so the rewrite matches the prior build and
  `Source Index` shows the same csv-parsed count.
- Import order in `__init__` is robust regardless of producer-first listing — Python
  resolves the `from …model_services import …` etc. on demand, and the only real cycle
  (Reconciliation ↔ Services) stays broken via the deferred lazy import in
  Reconciliation `_render`. inputs_assumptions has no model imports, so wiring it into
  TAM Bridge / Private Addressable introduces no cycle.

## Verification

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py                                   # 18 sheets, green
/usr/bin/python3 qa/verify_crosstab.py                              # CROSSTAB VERIFY OK (4,290 formulas)
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0 --multiset warn   # soffice ~1-2 min
# -> TIE-OUT OK — 88 names match; multiset deltas = MSC (51->37) + OP-5 (81->66) source-line ints only
```

## Current state / how to resume

- **Green.** 18 sheets, canonical 9-group order, all native. `_datadump.py` gone.
  `qa/gold/baseline.json` left **frozen** (v4.33 oracle, not regenerated).
- Files added: `inputs_assumptions.py`, `guide_methodology.py`,
  `sources_source_index.py`, `sources_references.py`, `outputs_figure_register.py`.
  Rewritten: `data_awards.py`, `data_j998_j999.py`, `model_tam_bridge.py`,
  `model_private_addressable.py`, `sheets/__init__.py`. Deleted: `_datadump.py`.
- **NEXT — Phase 4 (final):** drop the bridge `defined_names` from the 4 producers
  (Reconciliation/Services/OP-5/MSC); add `qa/name_map.py` (`NAME_TO_ACCESSOR`) and
  evolve `qa/tie_out.py` to Invariant A (engine-only value-multiset, relocation-proof) +
  Invariant B (accessor-target spot checks fed from name_map instead of the workbook's
  definedNames); regenerate `qa/gold/baseline.json` via the **self-asserting
  anti-laundering** protocol (regen asserts `accessor_values == legacy name baseline` for
  all 86/88 keys before writing); **delete `_reflow.py`** (only its own file + a stale
  doc reference remain); retire `qa/dump_cells.py`; mark `extracted/v433/` read-only
  provenance. End state: workbook ships **zero** defined names.
