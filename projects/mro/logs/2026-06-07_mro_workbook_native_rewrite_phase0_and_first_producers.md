# 2026-06-07 — MRO workbook native rewrite: Phase 0 scaffolding + first two native producers

## Scope

Kicked off the **full native rewrite** of the MRO workbook
(`projects/mro/workbook/workbook_mro/sheets`), converting it from the `_reflow` grid-replay
idiom (which replays the extracted v4.33 grid from `extracted/v433/*.json`) into the native
hand-authored idiom of the sibling pipelines `workbook_ddg` / `workbook_submarines`
(RowCursor builders, explicit Python formulas, closure accessors instead of defined names,
and the richer group structure). User-approved scope is maximal: convert **every** reflow
sheet, add four groups (`guide`/`inputs`/`outputs`/`sources`), replace all ~86 defined names
with Python accessors, and retire `_reflow`. Full plan + the running progress log live in
`~/.claude/plans/putting-you-in-plan-enumerated-reddy.md`.

This session delivered **Phase 0 (verification scaffolding + de-risking)** and the **first
two native producer sheets** (MSC SCN USCG Top-Down, OP-5 Navy Top-Down), both tying out
green. Everything below is committed/working on disk. The build is **green at this
checkpoint**: 2 sheets native, the other 11 still reflow, and the two idioms coexist in the
registry by design so the build stays green through an incremental migration.

## Approach (and why it's safe)

The migration is incremental and verifiable because:

1. **Reflow and native `SheetEntry`s coexist** — `package_workbook()` treats them identically,
   so sheets convert one at a time without breaking the build.
2. **Bridge defined names.** A converted producer keeps re-publishing its old workbook defined
   names (via `WorksheetSpec(defined_names=...)`) at the **new native cells**, so the existing
   tie-out name gate keeps validating the model figures while consumers are still reflow.
   Consumers keep referencing producers by bare name until they too convert. Names are dropped
   only in Phase 4.
3. **Formulas emit as live `<f>` with no cached `<v>`** → an identical formula string ties out
   by construction. For the big SUMIFS cross-tabs this means a Python loop that reproduces the
   v4.33 formula *string byte-for-byte* is provably equivalent.

## What was built (Phase 0)

- **`sheets/_crosstab.py`** — canonical axis constants transcribed **once** from
  `extracted/v433/Services.json` and held as static literals (build never reads the grid):
  `PSC_ROWS` (the 65 services-MRO PSCs), `VESSEL_TYPES` (17), `HULL_PROGRAMS_NAVY` (29),
  `HULL_PROGRAMS_CG` (16), and `WORK_SEGMENTS` (the 5-segment partition of the 65 PSCs,
  verified disjoint + exhaustive). Plus structured-ref builders `sumifs_award`, `sumifs_j`,
  `countifs_j`, `sumifs_psc1905`, and `axis_crit` (maps the `Unclassified` column to the `""`
  criterion).
- **`sheets/_names.py`** — `abs_target(ref)` / `bridge(dict)` helpers. **A workbook
  defined-name target MUST be absolute** (`'Sheet'!$E$32`); a relative target shifts per
  referencing cell and resolves to the wrong cell (or 0) when used from another sheet. The
  accessors return relative refs (fine as direct `=Sheet!cell` formula refs); `bridge()`
  absolutises them for the defined-name table. Mirrors what gold's `outputs_figure_register`
  does with `_abs(...)`.
- **`qa/verify_crosstab.py`** — proves the native `_crosstab` builders reproduce Services
  §1/§2/§3 (**4,290 cross-tab formulas**) by **string equality** vs the extracted JSON, no
  soffice needed. Fast deterministic gate that runs before the heavyweight recompute. Result:
  `§1 1188 OK / §2 1980 OK / §3 1122 OK / CROSSTAB VERIFY OK`. (Transitional — retires with
  `extracted/v433` in Phase 4.)
- **`qa/tie_out.py`** — evolved with `--multiset {fail,warn,off}`. The **defined-name check is
  the hard gate** (= "the 86 load-bearing figures recompute to baseline by name"); the
  **per-sheet value-multiset is a reviewed tripwire**. `fail` (default) is the all-reflow
  checkpoint; `warn` is used mid-migration so expected cleanup deltas (provenance line-numbers
  rendered as text) can be eyeballed without failing the run. Refactored `compare()` into
  `_name_msgs` + `_multiset_msgs`.

## Sheets converted (Phase 1, 2 of 4 producers)

- **MSC SCN USCG Top-Down → native.** Producer; four banded input sections (MSC M&R, SCN CVN
  RCOH LI 2086, USCG ISVS [confidence LOW], OPN LI 1000). Captures 14 model anchors (FY25→col E,
  FY26→col F), exposes closure accessors (`msc_mr_*_cell`, `scn_cvn_rcoh_li2086_cell(fy)`,
  `uscg_isvs_floor_cell`, `opn_li1000_cell(fy)`, …) and re-publishes the 14 names as bridge.
  Source-line refs rendered as TEXT.
- **OP-5 Navy Top-Down → native.** Producer; private availability categories (11) + public
  naval shipyards (4) + grand total/cross-checks, driven by `_PRIVATE`/`_PUBLIC` data tables.
  Hosts the 18 `OP5_*` anchors (all in FY25-Current col G), accessors `op5_cell(code)`,
  `op5_private_cell`, `op5_public_nsy_cell`, `op5_total_cell`. The §3 cross-check still
  references Reconciliation's `OMN_1B4B_TOTAL_FY25` by bare name (valid while Recon is reflow).

**Tie-out after each (`--multiset warn`):** `TIE-OUT OK — 88 names match`. The only multiset
deltas are exactly the source-line integers now rendered as text (MSC 51→37, i.e. 14 ints;
OP-5 81→66, i.e. 15 ints). No model number changed.

## Bug found and fixed (the tripwire earned its keep)

The first native-MSC tie-out passed the name gate but the multiset tripwire flagged value
changes across the **consumer** sheets (TAM Bridge, Output, Private Addressable, Scope,
Verification) — every MSC/USCG/SCN/OPN-derived `$M` value had collapsed to 0. Root cause: the
bridge defined-name targets were **relative** (`'MSC…'!E32`); the original reflow names were
**absolute** (`$D$32`). A relative defined name resolves correctly on a direct read (so the
name gate looked fine) but resolves to the wrong cell / 0 when referenced **from another
sheet**. Fixed by absolutising all bridge targets (`_names.bridge`). Re-ran: clean.

## Current state

- **Green.** `python build_workbook.py` → 13 sheets, 4 native tables. `qa/verify_crosstab.py`
  → OK. `qa/tie_out.py compare qa/gold/baseline.json <xlsx> --tol 1.0 --multiset warn`
  → `TIE-OUT OK — 88 names match` (multiset deltas = source-line ints only).
- Native: **MSC SCN USCG Top-Down**, **OP-5 Navy Top-Down**. Reflow (unchanged): the other 11.
- `qa/gold/baseline.json` left **frozen** as the v4.33 oracle (not regenerated). Files added:
  `sheets/_crosstab.py`, `sheets/_names.py`, `qa/verify_crosstab.py`. Files edited:
  `sheets/model_msc_scn_uscg_topdown.py`, `sheets/model_op5_navy_topdown.py`, `qa/tie_out.py`.

## Remaining work (next passes — fully specified)

- **Phase 1 cont.** — **Services** (the complete authoring spec, incl. the exact corporate-parent
  criteria strings with their load-bearing double-spaces, the §13 "Other"-column formula, and the
  §6/§7 named-pull tables, is captured in the plan file's **"Services authoring spec"** appendix);
  then **Reconciliation** (52 names + native `BudgetAnchors` table + the one cycle break —
  `Reconciliation!C19` RECONCILED_MRO_TAM defers its Services pull to render via a lazy
  `from model_services import navy_tam_svc_cell, cg_tam_svc_cell`).
- **Phase 2** — Depot Ship Repair (J998J999Data SUMIFS/COUNTIFS loops), TAM Bridge, Private
  Addressable, Verification Answers, Scope Reconciliation, Output (consumers; switch bare names to
  accessors as producers convert).
- **Phase 3** — add `inputs_assumptions` / `guide_methodology` / `sources_source_index` /
  `sources_references` / `outputs_figure_register`; rewrite `data_awards` / `data_j998_j999` to the
  explicit `_COLUMNS` idiom; reorder `sheets/__init__.py` to the canonical 9-group order.
- **Phase 4** — drop all bridge names, regenerate `baseline.json` via the anti-laundering protocol
  (self-assert == legacy oracle), retire `_reflow.py` / `_datadump.py`, mark `extracted/v433`
  read-only provenance.

## How to resume / verify

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py                                   # must stay green
/usr/bin/python3 qa/verify_crosstab.py                              # fast string-equiv proof
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0 --multiset warn   # soffice ~1-2 min
```

Resume pointer + gotchas are also in memory (`mro-native-rewrite`) and the plan file's progress log.
