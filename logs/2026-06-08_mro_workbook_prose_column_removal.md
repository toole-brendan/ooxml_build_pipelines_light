# 2026-06-08 — MRO workbook prose-column removal (source-style compaction)

## Scope

Second styling pass on the MRO workbook sheet modules
(`projects/mro/workbook/workbook_mro/sheets/`). Goal (per user spec): make the model /
validation / summary / output sheets read like compact calculation grids by removing the
per-row prose-provenance columns (`Notes`, `Source / note`, `Gap Explanation`,
`Description`, `What It Covers`). Only `sources_*` and `guide_methodology` carry
explanatory prose; short source refs (SRC-xx, budget line refs, the `Source` column) stay
in the model sheets. **No model/value changes** — every edit is presentation only, so
tie-out stayed green with **no `regen-baseline`**.

Gates (all green at end): `build_workbook.py` → 18 sheets, **0 defined names**;
`qa/verify_crosstab.py` → OK (4,290 formulas); `qa/tie_out.py compare … --tol 1.0` →
**Invariant B (86 figures) + Invariant A (engine multiset) both match**. Plus an empirical
soffice-recompute spot-check of the Figure Register / TAM Bridge / Private Addressable
cells (the accessors that are NOT in the 86 Invariant-B names).

## Tie-out safety model (why this was safe)

- **Invariant A** = relocation-proof numeric multiset over the 9 engine tabs. Removing a
  **text** column changes no numeric cell → multiset unchanged. Moving a **numeric** cell
  to a different column on the same engine tab is also fine (relocation-proof) as long as
  no numeric value is added/removed/changed.
- **Invariant B** = the 86 model figures read at their producer-accessor cells. Accessors
  are module-local closures returning `'Sheet'!Cell`; `qa/name_map` calls them. So when a
  column shift moves an accessor's target, updating the module's own accessor keeps B green
  — and a missed update fails B loudly.
- The TAM Bridge / Private Addressable accessors (consumed by Figure Register) are **not**
  in the 86 names, so they were verified empirically by recompute, not by the gate.

## Per-module changes (pass order)

**Pass 1 (mechanical column drops):**
- `model_private_addressable.py` — dropped `Notes` (col E); `_NCOLS 4→3`,
  `_COLS [52,16,16,44]→[44,16,16]`. Bottom-up stays C, top-down stays D → all 3 accessors
  unchanged.
- `model_tam_bridge.py` — collapsed 8 cols → 5 (dropped `Top-Down Source`, `Bottom-Up
  Source`, `Gap Explanation`). Bottom-up **F→E**, Gap **H→F**; per-row + §2 gap formula
  `=D-F`→`=D-E`. Updated accessors: `bottomup_total_cell` F→**E**, `bridge_gap_cell`
  H→**F** (`topdown_total_cell` stays D). `_COLS [5,42,15,32,15,32,16,48]→[5,40,14,14,14]`.
- `model_msc_scn_uscg_topdown.py` — dropped `Notes` (col H); `_NCOLS 7→6`,
  `_COLS …→[12,44,12,12,12,12]`. FY25=E / FY26=F unchanged → all 11 producer accessors
  intact. Section CAVEAT/CROSS-CHECK annotation rows kept (they are not the Notes column).
- `summary_verification_answers.py` — dropped `Notes` (col F), kept `Benchmark / Expected`;
  `_NCOLS 5→4`, `_COLS …→[42,14,10,22]`. No accessors, not an engine tab → lowest risk.

**Pass 2 (load-bearing producers/consumers):**
- `model_reconciliation.py` — §1 dropped `Source / note`; §2 dropped `Description`;
  `_NCOLS 8→7`, dropped the 70-wide col I (`_COLS …→[14,14,60,16,16,16,32]`; Line Item D=60
  and Source H=32 kept as load-bearing). §1 value accessor (col **D**) and §2 FY25 accessor
  (col **F**) both unchanged. The `_ANCHORS_*` note fields and `_S2` `desc` fields are
  retained in-source (unpacking renamed to `_note`/`_desc`) but no longer rendered — zero
  risk of corrupting the numeric literals / captured rows. `_RECON_NOTE` constant removed
  (orphaned).
- `validation_scope_reconciliation.py` — `_vrow` simplified to `[step, comp, val]` (dropped
  `named`+`note`); all `_hdr` 5-col → 3-col. §5 restructured to keep **both** numerics
  (pre col D, post **F→E**) and dropped the `Named range` text; the post-rebase total's SUM
  range updated `F→E` to match. §12/§13 reduced to `[Check, Description, Computed value]`.
  §10 paste block (11 cols) + §11 matrix kept. `_NCOLS` stays 11 (the §10 paste sets the
  width); `_COLS` prose widths 30/50 compacted to 16. `$M` stays in col D so all
  `=D{bar}` waterfall arithmetic is unchanged. Hosts no accessors.

**Pass 3 (services prose, cross-tab widths untouched):**
- `model_services.py` — §6 dropped `Notes` (col F), kept `% of TAS Total`; §7 dropped
  `Description` (col E); §9 dropped `What It Covers` (col E, and the `_S9_COVERS` list).
  Total-row `n_cols` adjusted (5→4 in §6, 4→3 in §9). `_NCOLS=32` and the §2-driven `_COLS`
  cross-tab widths **untouched**. `_S6_APPR`/`_S7_*` note/desc fields retained in-source
  (unpacking ignores them). Navy/CG TAM accessors (col C) unchanged.

**Pass 4 (width polish + sweep):**
- `inputs_assumptions.py` — kept the (sanctioned) input-guidance Notes column, capped
  `_COLS [44,16,60]→[38,14,36]`.
- `model_op5_navy_topdown.py` — category col C 50→46 (width only).
- `model_depot_ship_repair.py`, `chartdata_output.py` — **left as-is**: no prose/notes
  columns; label widths (34/28 and 42) already inside the source-style band, and both are
  engine tabs (chartdata = `Output`), so touching them buys risk for no benefit.
- Grep sweep for leftover prose headers in non-source/non-guide/non-data modules: 3 hits,
  all legitimate — validation §12/§13 `Description` (a check-title label), inputs `Notes`
  (sanctioned), services cross-tab `Description` (the PSC name). Not prose-provenance.

## Empirical spot-check (recompute)

TAM Bridge row 19: D=17,495.9 / **E(bottom-up)=7,066.9** / **F(gap)=10,429.1**. Figure
Register DO-06 pulls `'TAM Bridge'!E19`=7,066.9 (bottom-up, = Navy 6,794.2 + USCG 272.6),
DO-07 pulls `F19`=gap — moved accessors resolve to the correct columns. Private Addressable
bottom-up C10=5,063.7 / top-down D26=8,007.9 / delta C33=−2,944.2 all resolve correctly.

## Deliberate decisions / not done

- **Prose was removed, not relocated into methodology/sources.** The provenance backbone
  (sources_references SRC-01..10 + CITE-01..05 with context notes, sources_source_index,
  the methodology tab) already lived in the workbook; the removed columns were largely
  redundant restatements + analytical commentary. Heavy narrative (TAM Bridge gap
  explanations, summary/validation per-row notes, §9 coverage) was deleted (git-recoverable);
  reconciliation/services note+desc strings are retained in-source but unrendered. Open
  offer: port any specific rationale into `guide_methodology` / `sources_references` if it
  should stay visible in-workbook.
- Removed one stale claim by deletion: Private Addressable's old convergence note said
  "~$700M apart"; the actual computed delta is −$2,944M (an unrelated pre-existing modeling
  matter, not touched here).
