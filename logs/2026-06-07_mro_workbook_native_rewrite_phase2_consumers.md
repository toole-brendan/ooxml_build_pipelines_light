# 2026-06-07 (session 3) — MRO workbook native rewrite: Phase 2 complete (all 6 consumers)

## Scope

Continued the **full native rewrite** of the MRO workbook
(`projects/mro/workbook/workbook_mro/sheets`), picking up from the Phase-1 checkpoint
(4 native producers: MSC/SCN/USCG, OP-5, Services, Reconciliation). This session converted
the **six consumer sheets** — TAM Bridge, Private Addressable, Verification Answers, Depot
Ship Repair, Scope Reconciliation, Output — finishing **Phase 2**. With this, **all ten
formula sheets are native**; only the three raw data tabs remain on the `_datadump` idiom.
The build is **green**: `python build_workbook.py` → 13 sheets, `qa/verify_crosstab.py` → OK,
`qa/tie_out.py … --multiset warn` → **`TIE-OUT OK — 88 names match`** with the only multiset
deltas being the pre-existing MSC/OP-5 source-line integers (every converted sheet added
ZERO deltas). Plan + running log: `~/.claude/plans/putting-you-in-plan-enumerated-reddy.md`;
resume pointer in memory `mro-native-rewrite`.

## Approach

Each consumer was re-authored as a hand-authored `RowCursor` builder (the DDG/submarines
idiom): `§N` collapsible banners, content in col B (gutter), explicit Python formulas. The
key correctness levers:

- **Cross-sheet pulls → producer accessors.** Bare named-range references (`OP5_PRIVATE_FY25`,
  `NAVY_TAM_SVC`, `MRO_TAS_OPN_FY25`, `PSC1905_MRO_EMBEDDED`, …) were replaced with imports of
  the producer closures (`op5_private_cell()`, `navy_tam_svc_cell()`, `mro_tas_cell('OPN')`,
  `psc1905_mro_cell('EMBEDDED')`, …). The bridge names still exist, so the build stays green;
  this advances the Phase-4 goal of dropping the names entirely.
- **Cross-tabs → `_crosstab` builders.** Depot/Output SUMIFS/COUNTIFS blocks reuse
  `sumifs_j` / `countifs_j` and, for Output's segment arrays, `WORK_SEGMENTS` / `PSC_CODES` —
  so a Python loop reproduces the v4.33 formulas. The tie-out **multiset is value-exact, not
  byte-exact**, which gives latitude in formula construction (e.g. summing the marauder-hull
  union in display order rather than the original's order) while still pinning every value.
- **Intra-sheet refs → captured positions.** Subtotals/ratios reference rows captured from the
  same `c.write(...)`/`c.at()` that emitted them; the `$M` column shifts to native col D on the
  waterfall sheets (source col C + gutter), so BAR-row refs map there.
- Authoring aid: **`qa/dump_cells.py`** (new) — full untruncated per-cell dump of a v433 sheet
  (transitional; retires with `extracted/v433` in Phase 4).

## Sheets converted

- **TAM Bridge** (`model_tam_bridge.py`) — pure consumer. §1 8-component dual-narrative bridge
  (top-down = OP-5/MSC/SCN/OPN/USCG accessors; bottom-up = live FPDS SUMIFS incl. the 7-office
  RMC sum); §2 grand totals; §3 private-addressable drop-through. Gap col = `=D{r}-F{r}`.
- **Private Addressable** (`model_private_addressable.py`) — two derivations (bottom-up Services
  TAM − captive PSC1905 SUMIFS − FMS; top-down OP-5+MSC+SCN+OPN+WPN+USCG less Public NSY/captive/
  FMS) + convergence.
- **Verification Answers** (`summary_verification_answers.py`, group `summary`) — 6 Q&A blocks;
  ranked top-15 PSC / top-10 office SUMIFS lists; §6 PSC1905 captive share over a per-block base.
- **Depot Ship Repair** (`model_depot_ship_repair.py`) — 13 J998/J999 cross-tab sections via
  reusable `_dim_section` / `_matrix_section` helpers; §7/§11 corporate-parent criteria preserved
  EXACT (load-bearing double-spaces); §13 is header-only (no data rows in the grid).
- **Scope Reconciliation** (`validation_scope_reconciliation.py`, group `validation`) — the S22
  10-bar waterfall; all $ via Reconciliation/Services/OP-5/MSC accessors + intra-sheet BAR-row
  refs; §10 think-cell paste block; "Named range" provenance text kept as documentation.
- **Output** (`chartdata_output.py`, group `chartdata`) — 13 think-cell chart blocks (Mekko /
  waterfall / funnel / stacked); segment arrays from `WORK_SEGMENTS`; §6 FMS-net `IF(ABS<0.5,"")`
  blanking; §8/§9 expanding cumulative-% ranges; SAM funnel marauder-hull unions; §10 HII
  placeholder (labels only).

## Bugs found & fixed (all caught by the multiset tie-out, then pinpointed by recompute)

The per-sheet `collections.Counter(gold) - Counter(new)` diff (after a soffice recompute) found
every error precisely:

1. **Private Addressable** — "Total top-down" value written into col C (bottom-up) instead of
   col D; the downstream `=D{b_total}+…` then summed an empty cell (→ −9,488 instead of 8,008).
   Fix: move the formula to col D.
2. **Depot Ship Repair** — §1 row-10 "# Awards" referenced col **E** (% of Total) rather than
   col **F** (# Awards) → 1.02 instead of 2,844. Fix: `=F{r8}-F{r9}`.
3. **Output** — (a) §1 total `SUM(C{first+1}:…)` skipped the Depot row (8,970.87 → 4,189.96);
   (b) §3 `z_col`/`aa_col` column offsets were off by one, so the residual "Other" cell
   referenced **itself** (circular → blank) — exactly the 6 missing numeric cells. Fixed both.

**Takeaway:** value-in-wrong-column and `col_letter` off-by-one in wide matrices are the
recurring failure mode of this idiom; the value-multiset tripwire is the cheap, exact detector.

## Verification

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py                                   # 13 sheets, green
/usr/bin/python3 qa/verify_crosstab.py                              # CROSSTAB VERIFY OK
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0 --multiset warn   # soffice ~1-2 min
# -> TIE-OUT OK — 88 names match; multiset deltas = MSC (51->37) + OP-5 (81->66) source-line ints only
```

Per-sheet result for the six conversions: **TAM Bridge / Private Addressable / Verification
Answers / Depot Ship Repair / Scope Reconciliation / Output each added ZERO multiset deltas.**

## Current state / how to resume

- **Green.** All 10 formula sheets native; data tabs (`data_awards`, `data_j998_j999`,
  `data_psc_1905_classified`) still `_datadump`. No module calls `reflow_sheet`/`ReflowSpec`
  anymore — only `_reflow.py` itself and the `__init__.py` docstring still name reflow.
- `qa/gold/baseline.json` left **frozen** (v4.33 oracle, not regenerated).
- Files added: `qa/dump_cells.py`. Files rewritten (reflow → native): `model_tam_bridge.py`,
  `model_private_addressable.py`, `summary_verification_answers.py`, `model_depot_ship_repair.py`,
  `validation_scope_reconciliation.py`, `chartdata_output.py`. `sheets/__init__.py` docstring
  updated to reflect the native state.
- **NEXT — Phase 3:** add `inputs_assumptions` / `guide_methodology` / `sources_source_index` /
  `sources_references` / `outputs_figure_register`; rewrite the two big data tabs into the explicit
  `_COLUMNS` idiom (then delete `_datadump.py`); reorder `sheets/__init__.py` into the canonical
  9-group order. **Phase 4:** drop the bridge `defined_names`, regenerate `baseline.json` via the
  self-asserting anti-laundering protocol, delete `_reflow.py`, mark `extracted/v433` read-only.
