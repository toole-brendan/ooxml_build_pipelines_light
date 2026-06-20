# 2026-06-07 (session 2) — MRO workbook native rewrite: Phase 1 complete (Services + Reconciliation)

## Scope

Continued the **full native rewrite** of the MRO workbook (`projects/mro/workbook/workbook_mro/sheets`),
picking up from the prior session's checkpoint (Phase 0 scaffolding + two native producers: MSC SCN USCG
Top-Down, OP-5 Navy Top-Down). This session converted the remaining two Phase-1 producers —
**Services** and **Reconciliation** — finishing **Phase 1**. The build is **green**: 4 of 13 sheets
native, the other 9 still reflow, and both idioms continue to coexist in the registry. Plan + running
progress log: `~/.claude/plans/putting-you-in-plan-enumerated-reddy.md`; resume pointer in memory
`mro-native-rewrite`.

## What was built

### Services → native (`model_services.py`)

The largest sheet. Rewritten from the `_reflow` replay into a hand-authored `RowCursor` build:

- **§1-§3 cross-tabs** are Python loops over the `_crosstab` axis constants emitting `sumifs_award(...)`
  against the `Awards` table. Structured refs are position-independent, so the loop reproduces the v4.33
  SUMIFS strings (proven by `qa/verify_crosstab.py`); the per-row `Total` = `SUM(D{r}:…{r})` and the totals
  row = `SUM(col{lo}:col{hi})` reference the new native positions. Two label columns (PSC code @ B,
  Description @ C) → axis data starts at **col D**.
- **§4 FY2025 MRO TAM** is the PRODUCER of the two TAM names: Navy `=(Σ_65 sumifs(Service,Navy))/1e6` and
  CG `=(…Coast Guard…)/1e6`; hosts `NAVY_TAM_SVC`/`CG_TAM_SVC` (bridge) and exposes `navy_tam_svc_cell` /
  `cg_tam_svc_cell` accessors (the Reconciliation↔Services cycle nodes).
- **§5** work-segment TAM; **§6/§7** budget-reconciliation / budget-book anchors authored as
  **bare-name formula rows** (`MRO_TAS_*/1000`, `OMN_*/1000`, `NAVY_TAM_SVC+CG_TAM_SVC`, …) — position-
  independent and valid while Reconciliation publishes those names via its own bridge. (Phase 2/4 switches
  these to accessors.) **§9** coverage; **§10** top-10 contractors (cumulative col F; rank-10 S.C.A. is a
  hand-keyed input `112.20543451`, not a SUMIFS); **§11** HII margin inputs; **§12** market-share top-3 per
  segment; **§13/§14** vessel-type × work-segment ($M and %). **§8 narrative dropped** (moves to
  guide_methodology in Phase 3).
- The §10/§12 FPDS `Corporate Parent` criteria strings are preserved EXACTLY, including their load-bearing
  double-spaces (`THE CHARLES STARK DRAPER LABORATORY  INC.`, `DETYENS SHIPYARDS  INC.`, etc.) — extracted
  programmatically to avoid transcription error.

### Reconciliation → native (`model_reconciliation.py`)

The named-range backbone (~52 names) + the one true import cycle:

- **§1 deck-evidence anchors** (values in $M, value column D): the 14 `PSC1905_MRO_*` rows,
  `RECONCILED_MRO_TAM`, `PUBLIC_SHIPYARD_NWCF`, three `HII_MT_*`.
- **§2 native `BudgetAnchors` ExcelTable** (values in $K, FY25 Enacted column F): the appropriation
  attribution + OMN BA-1 + SCN + USCG + NWCF rows hosting the `MRO_TAS_*` / `OMN_*` / `SCN_*` /
  `USCG_ISVS_*` names. Internal appropriation sub-bands stay as subsection-styled single-cell rows **inside
  the table range** — `ExcelTable` only validates the ref rectangle/headers, so embedded banner rows are
  fine. The 4 intra-table rollup rows (TAS Total, BA-1 total, BA-1 928, Columbia rollup) re-express their
  v4.33 column-sum formulas in the new native columns (FY24→E, FY25→F, FY26→G) over captured row positions.
  §2 table data was baked in as static literals (generated once from the grid; the build never reads it).
- Exposes accessors `reconciled_mro_tam_cell`, `public_shipyard_nwcf_cell`, `hii_mt_*_cell`,
  `psc1905_mro_cell(bucket)`, `mro_tas_cell(key)`, `omn_cell(key)`, `scn_cell(key)`, `uscg_isvs_cell(key)`;
  bridges all ~52 cell names plus the two formula-defined date names (`FY25_START`/`FY25_END`).
- **Cycle break (the one real one).** Services reaches Reconciliation's anchors by bare name (no import),
  so Services is the clean producer. Reconciliation's single back-link to Services (`RECONCILED_MRO_TAM` =
  `NAVY_TAM_SVC + CG_TAM_SVC + PSC1905_MRO_EMBEDDED`) is a **deferred row**, exactly like gold
  `inputs_assumptions`: `_build_body()` returns `(rows_before, recon_row, rows_after, …)`; `_render()` does
  `from workbook_mro.sheets.model_services import navy_tam_svc_cell, cg_tam_svc_cell` and splices the C19
  formula in, so there is no module-level `model_reconciliation ↔ model_services` cycle.

## Verification

`build_workbook.py` → 13 sheets, 4 native tables, green. `qa/verify_crosstab.py` → OK (§1 1188 / §2 1980 /
§3 1122). `qa/tie_out.py compare qa/gold/baseline.json "../20260607_…vS.xlsx" --tol 1.0 --multiset warn`
→ **`TIE-OUT OK — 88 names match`** after each conversion. **Services and Reconciliation each added ZERO
multiset deltas** (every cross-tab, budget, and anchor value ties out by recompute). The only multiset
deltas remaining are the MSC (count 51→37) and OP-5 (81→66) source-line integers rendered as text from the
prior session — no model number changed.

## Gotchas hit this session

- **RowCursor resolves callable cell values EAGERLY** (inside the `c.write` that emits the row). So a
  forward reference to a not-yet-written row via `P[...]` inside a `lambda` raises `KeyError`. Fix: for the
  §4 %-cells (which reference the total row two rows below), compute the three consecutive row numbers up
  front and write plain-string formulas.
- **Column base differs by label-column count.** The §1-§3 cross-tabs have TWO label columns (code,
  description) so axis data starts at col D; §13/§14 have ONE label column so the 5 vessel categories start
  at col **C** (Other @ H, Total @ I). Got the §13 "Other"/Total/§14 column math wrong on the first pass
  (off-by-one), caught by reasoning before the soffice run; fixed to base col 2 (C).

## Current state / how to resume

- **Green.** Native: MSC SCN USCG Top-Down, OP-5 Navy Top-Down, Services, Reconciliation. Reflow
  (unchanged): Verification Answers, Depot Ship Repair, TAM Bridge, Private Addressable, Scope
  Reconciliation, Output + the 3 data tabs.
- `qa/gold/baseline.json` left **frozen** (v4.33 oracle, not regenerated).
- **NEXT — Phase 2 consumers:** Depot Ship Repair (J998J999 SUMIFS/COUNTIFS loops via
  `_crosstab.sumifs_j` / `countifs_j`), TAM Bridge, Private Addressable, Verification Answers, Scope
  Reconciliation, Output. As each converts, switch its bare-name pulls to the producer accessors
  (`navy_tam_svc_cell`, `op5_cell`, `mro_tas_cell`, …). Then Phase 3 (new inputs/guide/sources/outputs
  groups + explicit-`_COLUMNS` data tabs + registry reorder) and Phase 4 (drop bridge names, regen
  baseline, retire `_reflow.py`/`_datadump.py`).

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py
/usr/bin/python3 qa/verify_crosstab.py
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0 --multiset warn   # soffice ~1-2 min
```
