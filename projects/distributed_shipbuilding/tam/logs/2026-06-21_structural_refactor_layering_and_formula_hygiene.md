# 2026-06-21 — Master TAM structural refactor (layering + formula hygiene)

A nine-step, **value-preserving** structural pass over the master TAM pipeline
(`tam/master/`): tighten layer responsibilities, kill formula noise, and remove a
misleading control — without moving a single headline number. The architecture
(per-program model tabs, the shared `_program_tam` builder, combined-by-source data
tabs, `RowCursor` accessors) was already sound and is kept. Follows the outyear
low/high-band rebuild; same canonical pipeline. Driven by an external structural
review, verified claim-by-claim against the code before executing.

## Why
The workbook was acyclic and correct but had accumulated layer leaks and formula
cruft that would make it unwieldy as it grows: a false FY-range control, source data
hardcoded on the inputs tab, opaque coefficient SUMPRODUCT walls, ~186 repeated
cross-sheet deflator refs on SCN Budget, `IF(N(...)=0,"")` guards everywhere, and
hard-coded validator anchors that forced manual re-baselining on every row shift.

## Master invariant
Every change is **value-preserving** — `validate_workbook.py` must hit the *same*
baseline values throughout (cum 13636.3 / 4507.1 / 6421.7; coeffs 34.0/22.0/25.3%;
the FY28-31 band 4383→4409 low / 4922→4931 high). Any tie-out drift = a regression,
not a re-baseline. The one intended *visible* change: zero-procurement cells (Columbia
FY22/23/25) now render `-` instead of blank.

## The nine steps
0. **Validator anchors → label-resolved.** `validate_workbook.py` `_ANCHORS` now carry
   a row LABEL + column and resolve by scanning column B (reusing the Exec-Summary
   label-scan), not a hard-coded address. Enabler: every later row shift auto-revalidates.
1. **Doc drift.** `methodology.py` §2 Outyears rewritten to the coefficient-based model;
   `obbba.py` banner "Assumptions §4" → "§3".
2. **DDG OBBBA BC-share** standardized to Observed|Adjustment|Modeled (Modeled=C+D);
   `obbba_bc_share_cell` always points at Modeled — per-program column branch gone.
3. **Fixed period + central `_periods.py`.** New `_periods.py` exports `FY`/`OY`,
   replacing the `_FY` copy-pasted in 5 modules. Removed the editable FY-range knobs +
   `n_years_count_formula` (they changed the avg denominator but not the cumulative —
   a false control); avg is now `=C{cum}/len(FY)` (blank-safe; `=AVERAGE` would break
   Columbia's blank years).
4. **Light `build_model()`** in `lib.py`: documents the one-directional dependency
   order in one place, returns the existing SHEETS registry. The full refs-threading
   version was rejected — it would rewrite the kept module-level accessor pattern, and
   Python's import graph already enforces the order.
5. **Deflators + numeric-zero.** Deflator factors are now real floats with an inline
   2-decimal style (`_factor.py`, per-build `NUM_FMTS`/`CELL_XFS` append — the `_italic.py`
   trick; no workbook_core change). One local "Constant-FY2026 factor" row per data tab
   (SCN, FYDP) cuts SCN's Deflators dependency **186 → 6**. Stripped the *display* guards
   (stream TAMs, OBBBA BC base, GFE remainder) and `SUM/4`→`AVERAGE`; the existing dash
   format renders the resulting numeric 0 as `-`. **Division guards kept** (penetration,
   SCN ratios) — removing them would `#DIV/0!` on Columbia's zero years.
6. **POP coefficient auditability + localization.** Each coefficient split into visible
   **Eligible $M | Supplier $M | Coefficient** cells (same SUMPRODUCT masks, just split —
   value-preserving, no SUMIFS criteria-translation risk); accessors moved C→E. The BC
   coefficient is now localized onto each program tab as a per-FY row, so each annual TAM
   cell is same-sheet (base × local coefficient).
7. **OBBBA execution-aligned gross row.** Added a Virginia "Gross award, execution-aligned,
   constant FY2026 $M" row (FY26/FY27 spillover split) + `obbba_gross_execaligned_cell`;
   the kept penetration denominator links to it instead of reconstructing the split inline.
   (Skipped the cosmetic data→bridge group reclassification — no "bridge" group exists in
   `workbook_core.groups`; not worth a shared-engine change.)
8. **DDG AP/LLTM → SCN Budget.** P-10 Ship Construction EOQ source dollars moved off the
   Assumptions (inputs) tab into the data pipeline: new `extracted/ap_lltm.csv` +
   `build_ap_lltm()` in `build_extracted.py`; rendered as SCN Budget §5; `ddg_ap_base_cell`
   now lives on `scn_budget`. Only the AP *coefficient* remains an Assumptions knob.

## Conventions now in force
Every external driver enters a program tab once (downstream is same-sheet) · data tabs
carry one local deflator row · model cells hold numeric 0 (dashed by format), only raw
source may be blank · validation resolves anchors by label, not address.

## Verification
`validate_workbook.py` → **RESULT: PASS** after every step. 0 XML errors, 0 formula-error
cells; all 12 tie-out anchors, 6 Exec FY-total cross-checks, and 8 outyear-band checks
match baseline. Build-time `assert c.at()==…` / `fac_r==_FACTOR_ROW` invariants guard the
new row positions.

## Files touched
New: `_periods.py`, `_factor.py`, `extracted/ap_lltm.csv`. Modified: `validate_workbook.py`,
`build_extracted.py`, `lib.py`, and the sheet modules `_program_tam`, `assumptions`,
`place_of_performance`, `scn_budget`, `obbba`, `deflators`, `fydp_outyears`, `methodology`,
`executive_summary`.

## Open / not done
- OBBBA group stays `data` (the data→bridge reclassification needs a new `workbook_core`
  group; cosmetic, deferred).
- AP source data CSV-ified but `build_extracted.py` not re-run end-to-end (the new
  `ap_lltm.csv` was written directly; re-running the extractor reproduces it identically).
- Decks / consolidated pipeline still reference prior outputs (out of scope; unchanged).
