# 2026-06-07 (session 5) — MRO workbook native rewrite: Phase 4 complete (zero defined names; Invariants A+B)

## Scope

Final phase of the **full native rewrite** of the MRO workbook
(`projects/mro/workbook/workbook_mro/sheets`). Phase 4 retires the migration scaffolding:
**dropped every workbook defined name** (the "bridge"), rewired the last bare-name formula
dependencies onto closure accessors, evolved the tie-out gate to two relocation-proof
invariants fed by a new `qa/name_map.py`, regenerated the baseline under a self-asserting
anti-laundering protocol, and deleted the dead `_reflow.py` / `_names.py` / `qa/dump_cells.py`.
The workbook now ships **0 defined names** and matches the DDG / submarines idiom end-to-end
(cross-sheet coupling = import-time accessors only). Build is **green**: `build_workbook.py`
→ 18 sheets; `qa/verify_crosstab.py` → OK (4,290 cross-tab formulas); `qa/tie_out.py compare`
→ **`TIE-OUT OK — Invariant B: 86 model figures match at their accessors; Invariant A: engine
value-multiset matches`**. Plan + running log: `~/.claude/plans/putting-you-in-plan-enumerated-reddy.md`;
resume pointer in memory `mro-native-rewrite`. Phase 3 log:
`logs/2026-06-07_mro_workbook_native_rewrite_phase3_new_groups.md`.

## The load-bearing discovery: 73 live bare-name formulas (not just a kwarg delete)

"Drop the bridge" was **not** just removing `defined_names=` from four `WorksheetSpec`s.
Scanning the *built* xlsx (openpyxl, `data_only=False`) for cell formulas containing any of
the 88 names — the ground truth, vs. grepping source which mixes in label/description text —
found **73 live formulas that resolve through a defined name** and would have gone `#NAME?`:

- **Services: 72.** §6/§7 budget-reconciliation rows were still `=MRO_TAS_OMN_FY25/1000`,
  `=OMN_1B4B_TOTAL_FY25/1000`, `=USCG_ISVS_TOTAL_FY25/1000`, pct cells `=NAME/MRO_TAS_TOTAL_FY25`;
  §6 TAM display rows `=NAVY_TAM_SVC` / `=CG_TAM_SVC`; §10 concentration denominators
  `(NAVY_TAM_SVC+CG_TAM_SVC)`. These were the "valid while Reconciliation still publishes
  them" bare names noted back in Phase 1 — never switched to accessors until now.
- **OP-5: 1.** §3 cross-check `=G33-OMN_1B4B_TOTAL_FY25`.
- **Every other sheet: 0.** TAM Bridge / Private Addressable / Depot / Scope / Output /
  Verification / Reconciliation were fully rewired to accessors (or intra-sheet refs) back in
  Phase 2; the remaining source grep hits there are *label/provenance text*, not formulas.

So Phase 4's real work was concentrated in two producers. Fixes:
- **Services §4 TAM names → intra-sheet refs.** `NAVY_TAM_SVC`/`CG_TAM_SVC` are defined on
  Services itself (§4 Navy/CG producer cells `C{P['navy']}` / `C{P['cg']}`), so the §6 display
  rows and the §10 `_TAM` denominator became `f"=C{P['navy']}+C{P['cg']}"` etc.
- **Services §6/§7 budget anchors → Reconciliation accessors** via a local `_ref(name)`
  resolver: `MRO_TAS_<K>_FY25 → mro_tas_cell(K)`, `OMN_<K>_FY25 → omn_cell(K)`,
  `USCG_ISVS_<K>_FY25 → uscg_isvs_cell(K)`. The `_S6_APPR`/`_S7_*` data tuples keep the name
  string (it drives `_ref`); only the formula construction changed.
- **OP-5 §3** → `f"={_FY25}{P['grand']}-{omn_cell('1B4B_TOTAL')}"`.

**No new import cycle.** Services and OP-5 now `from model_reconciliation import mro_tas_cell,
omn_cell, uscg_isvs_cell` at top level. Safe because the Reconciliation↔Services cycle is
broken on Reconciliation's side — it imports Services *lazily inside `_render()`* — so
`model_reconciliation` fully imports (running `_build_body()`, no Services dep) before anyone
calls its accessors. Services calls `mro_tas_cell(...)` during its own `_make()` at import,
by which point Reconciliation's `_NAME_CELL`/`_NAME_COL` are populated. Smoke-import of the
18-sheet `SHEETS` registry confirms no cycle.

## qa/name_map.py (new) — the defined-name table's replacement

`NAME_TO_ACCESSOR = {legacy_name: zero-arg callable -> 'Sheet'!Cell}` for all **86
cell-anchored** names, built from the SAME producer accessors the consumer sheets use (so a
wrong captured row breaks the live model and this map identically — it can't agree with itself
against a broken build). Parameterized families mirror the producers (PSC1905 buckets ×14,
MRO_TAS ×14, OMN ×10, SCN ×5, USCG_ISVS ×4, OP5 codes ×15, …). The **2 formula-date names**
`FY25_START`/`FY25_END` (= `DATE(...)`, no cell target, referenced by **no** formula —
verified) are intentionally dropped, tracked in `_DROPPED_FORMULA_NAMES`. `coverage_report()`
diffs the map vs. the baseline name set both ways; against the frozen oracle it reports
`uncovered=[]`, `stale=[]` (86 covered + 2 date = 88).

## qa/tie_out.py — evolved to Invariants A + B

- **Invariant B (hard) — accessor-target spot checks.** Snapshot reads each name's accessor
  cell (via name_map) from the soffice recompute → `accessor_values`. Compare asserts each
  equals `baseline.json["defined_names"][name]` (the frozen v4.33 numeric oracle) within tol,
  AND enforces coverage both ways (a numeric oracle name with no accessor, or an accessor
  absent from the oracle, fails — so nothing passes vacuously).
- **Invariant A (hard) — engine value-multiset.** One workbook-wide sorted multiset of every
  numeric cell over the **9 engine tabs** (`Reconciliation, Services, Depot Ship Repair, OP-5,
  MSC SCN USCG, TAM Bridge, Private Addressable, Scope Reconciliation, Output`), reusing the
  greedy `_diff_multiset`. Excludes the 3 raw data dumps and the pure link/label tabs
  (summary/guide/inputs/outputs/sources) that re-present figures. Relocation-proof: a number
  can move *between* engine sheets and still tie out.
- **`regen-baseline` subcommand — self-asserting anti-laundering.** Keeps
  `baseline.json["defined_names"]` **frozen** (passed through verbatim; never rewritten);
  snapshots the build; **refuses to write** unless Invariant B already holds against that
  frozen oracle; only then writes the fresh `engine_multiset`. A regression in any of the 86
  figures aborts the regen — it cannot be laundered into a new baseline.
- `compare` skips Invariant A (with a note) when the baseline predates the `engine_multiset`
  block, so the pre-regen checkpoint runs B as the standalone proof.

Negative control (synthetic): B catches a perturbed figure (`6,794.25 → 6,800.00`), A catches
a perturbed engine cell — the gate is not vacuous.

## Verification sequence (each soffice recompute ~1-2 min)

1. **Pre-change B vs the Phase-3 build (names still present):** `compare` → B green, 86 match.
   Isolates "name_map/gate correct?" from "did dropping names break anything?".
2. **Drop bridge from all 4 producers + rewire Services/OP-5; rebuild:** 18 sheets,
   `wb.defined_names == []`. `verify_crosstab` OK.
3. **Post-drop B vs frozen oracle:** green, 86 match — the rewiring is value-neutral
   (with names *gone*, the only path to the figures is name_map).
4. **`regen-baseline`:** `defined_names` sha256 identical before/after (`ea6dfef8…`, 88 names);
   `engine_multiset` (6,432 values) written; `value_multisets` dropped.
5. **Final `compare`:** B + A both hard-green.

## Files

- **Added:** `qa/name_map.py`.
- **Rewritten:** `qa/tie_out.py` (Invariants A+B, `regen-baseline`), `qa/gold/baseline.json`
  (now `{_doc, defined_names (frozen), engine_multiset}`).
- **Edited:** `model_services.py` (`_ref` resolver, §4/§6/§7/§10 rewires, drop bridge),
  `model_op5_navy_topdown.py` (§3 accessor, drop bridge + `_NAME`), `model_msc_scn_uscg_topdown.py`
  (drop bridge), `model_reconciliation.py` (drop bridge + `_DATE_NAMES`/`_bridge_names`),
  `sheets/__init__.py` (docstring), `qa/inspect_v433.py` (docstring).
- **Deleted:** `workbook_mro/sheets/_reflow.py`, `workbook_mro/sheets/_names.py`,
  `qa/dump_cells.py`.
- **Provenance:** `extracted/v433/PROVENANCE.md` marks the grid read-only / not a build input
  (build is fully decoupled — verified no module opens a v433 file; only `inspect_v433.py` and
  `verify_crosstab.py` read it for QA).

## Gotchas / notes

- **Ground truth = the built xlsx, not the source grep.** Source greps for the 88 names
  surface dozens of *label/description/source-note* strings (e.g. Scope/Verification keep
  "PUBLIC_SHIPYARD_NWCF" / "NAVY_TAM_SVC named range" as audit-trail documentation). Only the
  built-cell formula scan distinguished the 73 *live* dependencies from harmless text.
- **Audit-trail text left as-is.** Provenance cells that mention legacy names (e.g. Scope §5/§8,
  Verification §6, the Reconciliation "Line" column) are descriptive text, not formulas, and
  numeric-free → no Invariant-A/B impact. Left intact as intentional documentation rather than
  risk a reword; they read as the legacy-name lineage of each figure.
- **`defined_names` block stays frozen forever.** The anti-laundering guarantee depends on it
  never being rewritten; `regen-baseline` only ever (re)writes `engine_multiset`.

## Current state / how to resume

- **DONE. Phase 4 complete; the native rewrite is finished.** 18 sheets, canonical 9-group
  order, all native, **0 defined names**, cross-sheet coupling via accessors only. `_reflow.py`,
  `_names.py`, `_datadump.py` (Phase 3), `dump_cells.py` all gone. `extracted/v433/` is
  read-only provenance. Build + `verify_crosstab` + tie-out (A+B) green.
- **Re-verify end-to-end:**
  ```
  cd projects/mro/workbook
  /usr/bin/python3 build_workbook.py                       # 18 sheets; defined_names == 0
  /usr/bin/python3 qa/verify_crosstab.py                   # CROSSTAB VERIFY OK
  /usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
      "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0   # B+A green (soffice ~1-2 min)
  ```
- **If a producer cell moves**, just rebuild + `compare` (accessors + name_map follow the
  cell; Invariant B re-validates the value, Invariant A the relocation). To re-bless an
  intentional, B-verified model change, run `qa/tie_out.py regen-baseline …`.
