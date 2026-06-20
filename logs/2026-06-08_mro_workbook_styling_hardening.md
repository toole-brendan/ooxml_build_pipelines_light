# 2026-06-08 — MRO workbook styling hardening (semantic-style pass)

## Scope

Post-Phase-4 **formatting hardening** of the MRO workbook sheet modules
(`projects/mro/workbook/workbook_mro/sheets/`). No model/value changes — every edit is
pure presentation, so tie-out stayed green with **no `regen-baseline`**. Build green:
`build_workbook.py` → 18 sheets, **0 defined names**; `qa/verify_crosstab.py` → OK (4,290
formulas); `qa/tie_out.py compare … --tol 1.0` → **Invariant B (86 figures) + Invariant A
(engine multiset) both match**.

## The main bug fixed: total-ness was a cell style, not a row emitter

Across most modules, "total rows" were emitted as ordinary `c.write(..., styles=[S_BOLD,
S_NUM_TOTAL, S_PCT_TOTAL, ...])`. Because `S_BOLD`/`S_DEFAULT` carry no border, the
top-medium divider line had **gaps over the label/blank columns** (the "chunked borders"
look). The gold primitive `RowCursor.total()` → `total_row()` exists precisely for this: it
upgrades BASE styles to their bordered variants (`BORDER_TOP_FOR`) and pads to `n_cols`, so
the divider runs continuously. The port was bypassing it.

**Fix applied workbook-wide:** every genuine total/subtotal → `c.total(values,
styles=[BASE], n_cols=full_block_width)`. Verified in the built xlsx: e.g. Services §4
`Total Services TAM` label cell is now `s=3` (S_TOTAL, bordered) vs the old `s=1` (S_BOLD,
unbordered); Depot total rows have every cell bordered. Audit `grep -R "S_.*TOTAL"
sheets/*.py` is now clean of direct total-style usage (only name-string literals like
`MRO_TAS_TOTAL_FY25` remain).

## Per-module changes

- **model_reconciliation.py** — *completion fix*: `_build_body()` started at `RowCursor(2)`
  while `_render()` also emitted the sheet-title banner at row 2 → **duplicate `<row r="2">`**
  (§1 banner collided with the title; row 3 wasn't blank). Changed to `RowCursor(4)` (title
  2, blank 3, §1 banner 4) with a guard `assert s1_banner_row == 4`. §1 + §2 BudgetAnchors
  headers `[S_BOLD]*n` → `S_HEADER_LEFT`/`S_HEADER_CENTER`.
- **model_services.py** — §4–§14 headers `[S_BOLD]*n` → `S_HEADER_*` (the §1–§3 crosstabs
  were already correct, the in-file gold example). All crosstab/§4/§5/§6/§9/§10/§13/§14 totals
  → `c.total()`. Stripped redundant leading-space labels in §6/§7 "of which…" rows that already
  carried `S_LABEL_INDENT_1` (were double-indented).
- **model_op5_navy_topdown.py** — `priv_sub`/`pub_sub`/`grand` → `c.total()`. §3 delta
  cross-checks left as `S_NUM` (not totals).
- **model_msc_scn_uscg_topdown.py** — `_row(total=True)` branch refactored to `c.total()`.
- **model_tam_bridge.py** — `_row` helper Gap column `S_NUM_TOTAL` → `S_NUM` (was stamping a
  spurious divider on **every** bridge row); §2 grand total → `c.total()`; §3 single derived
  drop-through `S_NUM_TOTAL` → `S_NUM`.
- **model_private_addressable.py** — `a_total`/`b_total`/`b_addr` → `c.total()`; §3 Convergence:
  Delta → `c.total()`, A/B restate-rows → plain `S_BOLD`+`S_NUM`.
- **model_depot_ship_repair.py** — **deleted §13** (user decision). v4.33's §13 "Top 15 Parent
  IDV Vehicles" was itself a header-only stub (rows 223–224, no data; `J998J999Data` has no
  IDV-PIID dimension) — so "fill from v4.33" was impossible. Docstring 13→12 sections. §1
  gross/in-scope, §6 RMC, `_dim_section`, `_matrix_section` totals → `c.total()`.
- **summary_verification_answers.py** — totals → `c.total()`; §1 Navy/USCG `$M` data rows were
  mis-styled `S_NUM_TOTAL` (generic emphasis) → `S_LINK_NUM` (cross-sheet pulls); §4 ISVS
  floor + §5 OP-5 private single-accessor pulls → `S_LINK_NUM`; reworded the lone
  "NAVY_TAM_SVC named range" note to accessor wording.
- **validation_scope_reconciliation.py** — `_vrow(bar=True)` → `c.total()`. **Deliberately
  left** the "Named range" provenance column (intentional audit-trail per the module
  docstring) and the uniform `S_NUM` derived coloring (the cross-sheet-pull → `S_LINK_NUM`
  recolor was deferred here: the helper applies one style across mixed single-accessor /
  rebased / intra-sheet formulas, and it's value-neutral so no gate would catch a miscolor).
- **chartdata_output.py** — §1/§4/§8/§9/§9-secondary/§12 reference-total rows → `c.total()`.
  (§10 HII MT financials is an intentional structure-only paste placeholder — left as-is.)

Unused `S_NUM_TOTAL`/`S_PCT_TOTAL` imports removed from each edited module; `S_LINK_NUM`
added to summary_verification.

## Durable convention

Recorded in memory `mro-workbook-styling-contract`: totals via `c.total()` (never `S_*TOTAL`
in `c.write()`); `S_HEADER_*` for headers; `S_LINK_*` only for cross-sheet single-accessor
pulls; indent styles not leading spaces.

## Not done (intentional, low-priority)

- Broad cross-sheet → `S_LINK_NUM` recolor on **validation_scope** (deferred, see above).
- Aggressive note/prose trimming in dense model tables (kept analytical provenance intact).
- chartdata §10 HII financials placeholder (intentional paste-block stub).
