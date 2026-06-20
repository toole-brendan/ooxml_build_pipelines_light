# 2026-06-12 — Window sensitivity, class/PIID cuts, and the Award Analysis data workbook

## Goal

Three asks in sequence, all on the competability corpus from the 06-11 session:
(1) is the FY22–25 analysis window right, or should it reach back further;
(2) can the data be cut by PIID and by vessel type; (3) a workbook to display
the data — which the user redirected mid-design from a gate-centric layout to
**pure descriptive cuts** ("just presenting the data, not characterized yet…
by vessel, by PIID, by FY"), then split out into its own pipeline.

## 1. Window sensitivity — FY22–25 holds, demonstrated not argued

- The raw pulls already cover all of FSRS (subs FY2013–26, ddg FY2002–26);
  FY22–25 was only the analysis window, a single constant inherited from
  deck_mini_v2 and **justified nowhere** in the handoff or memo.
- Parameterized instead of edited: `_corpus.py` reads `COMP_WINDOW`
  (e.g. `2019:2025`) and `COMP_OUTDIR`; `compute_competability_signals.py`
  now takes FY_LO/FY_HI from the shared constant; `build_target_list.py`
  reads/writes OUT_DIR. Regression: with no overrides all four headline CSVs
  reproduce **byte-identical**.
- Sensitivity runs at FY20–25 and FY19–25 (`extracted/sensitivity_fy*/`) +
  new `compare_window_sensitivity.py` → `window_sensitivity_comparison.csv`:
  **13 of 14 lane gates stable across all three windows.** The one mover is
  DDG castings — SEEDED at FY22–25 *and* FY19–25 but COMPETABLE at FY20–25,
  where HHI lands at 0.2957, a hair under the 0.30 cutoff that lets the
  entrant arm fire. Non-monotonic = threshold artifact; lane carries barrier 5
  + active seeding in every window, so SEEDED is the robust reading.
- The counter-intuition worth keeping: **widening the window backward weakens
  the entrant signal** — censoring needs deep pre-window history, and 54–58%
  of records sit pre-FY22 today. Memo gained caveat 6 + a line in open item 1.

## 2. Class / builder / PIID cuts (descriptive only, per user choice)

- `_corpus.iter_records` now threads `vclass`/`bgroup` from scope meta onto
  every record (+ `scope_meta()` accessor) — proven inert: headline CSVs
  byte-identical after the change.
- `compute_class_cut.py` → `class_cut_scorecard.csv` (31 cut-lanes, thin-lane
  flags), `vendor_class_matrix.csv` (1,411 vendors, per-cut $/dates/profile),
  `piid_profile.csv` (39 in-corpus PIIDs incl. 17 with zero FSRS records).
  Cut = vessel class for subs (Virginia/Columbia), builder group for ddg
  (single-class DDG-51 → GD-BIW vs HII-Ingalls). Pools reconcile to the
  headline scorecard to the dollar. NO gates at cut level (handoff's
  unit-of-analysis rule; user picked "descriptive only").
- Reads (memo §3a): **Columbia is now the larger sub pool** ($2,405M vs
  Virginia $1,773M FY22–25) and entry lanes are fragmented on *both* classes;
  subs electrical splits sharply (Virginia HHI 0.88 / top-1 94% vs Columbia
  0.44 — the COMPONENT-TIER read lives on Columbia); **182 Columbia-only
  vendors ($246M**, Graham Corp $82M piping the headline name); **the DDG
  scorecard is effectively an Ingalls-visibility scorecard** (Ingalls 93% of
  pool, 6 of 7 BIW lanes thin); per-hull reads viable only at Ingalls
  (DDG 128 / FY23 award / DDG 125). Subs PIID cut collapses into the class
  cut — the two master contracts hold ~85% of records.

## 3. Award Analysis workbook (the big deliverable)

- **User steering, saved to memory**: present data cut by basic dimensions,
  no characterization (no COMPETABLE labels, no scoring) — second time this
  preference surfaced; memory `present-data-before-characterization` written.
- `extract_workbook_cuts.py` (research side) pivots the classified corpus into
  five wide FY-columned CSVs (`wb_annual_{program,worktype,class,piid}.csv`,
  `wb_vendor_fy.csv`; columns ≤FY12 + FY13–FY26 + total). All five cuts agree
  to the cent per program — supplier full history **$7,685.8M subs /
  $3,095.4M ddg**; FY22–25 slices tie to the scorecard ($4,177.3M / $1,572.6M).
- First built into workbook_consolidated (it was the empty scaffold); user
  redirected: **separate workbook named "Distributed Shipbuilding Award
  Analysis"**, consolidated restored. New sibling pipeline
  `projects/consolidated/workbook_award_analysis/` (same layout as the other
  pipelines: launcher → lib.py bindings → sheets/ registry → shared
  workbook_core engine; `_layout.py`/`_taxonomy.py` are copy-from helpers,
  taxonomy copy carries a COPY-FROM header). Output:
  `projects/consolidated/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`.
- 8 tabs: Overview (role × FY, supplier share), Data Notes, By Work Type,
  By Vessel, By PIID (zero-record PIIDs visible with data_status), By Vendor
  (native table `VendorFY`, 1,411 rows, filterable), Tie-Outs, Source Index.
- **Styling conformance pass** (user caught the violation): house canon is
  blue `S_NUM_INPUT` = hardcoded input, black `S_NUM` = derived via live
  formula, green `S_LINK_NUM` = cross-sheet link
  (`workbook_core/sheet_guide.md:181`; POP Corpus / Entity Master precedent).
  All extracted FY/record cells → blue; every per-row Total → live
  `=SUM(C{r}:Q{r})` black (the extracted `total` CSV column stays for
  script-side reconciliation only); Tie-Outs links green; new By Vessel
  "Checks" section ties each summary row to its detail grid live. Verified
  with an openpyxl font-color audit on the built file (FF0000FF / FF000000 /
  FF008000) + formula spot-dumps.
- Tie-Outs reconciles all five tabs' program totals via green links + a
  max-min<0.5 check; the link targets are live row-sums whose inputs are the
  blue cells.
- workbook_consolidated reverted exactly: registry restored, modules moved
  (not copied) out, extracted/ empty again, rebuilds as the 2-sheet chart-data
  workbook (z_ChartData, z_ChartData_OutsourcedBC).

## Lessons / mechanics worth keeping

- `col_letter` is **0-indexed** (0→A). The FY span is 15 FY columns + Total,
  so Total = column R on label+16 grids — the suspected off-by-one in the
  tie-out links was a miscount of mine, not a bug.
- SAM.gov windowed-vs-fullhistory and the FY22–25 basis now have an
  evidence-backed robustness claim; gate thresholds' one borderline case
  (DDG castings at HHI 0.30) is documented.
- Regeneration flow for the new workbook: `extract_workbook_cuts.py` →
  `cd projects/consolidated/workbook_award_analysis && python3
  build_workbook.py` (validate_workbook.py for QA).

## State / open items

- Phase F (deck `$##B` fill) still gated on user review of the findings memo
  (unchanged from 06-11); basis choice (FSRS floors vs TAM-allocated) still
  open.
- Workbook-side `entity_naics_lookup.csv` copies still not synced with the
  282 new lookups (carried from 06-11).
- FY2025–26 columns will grow with FFATA lag — re-run the extraction +
  rebuild when corpora are re-pulled.

## Files

New: `projects/consolidated/research/scripts/{compare_window_sensitivity,compute_class_cut,extract_workbook_cuts}.py`,
`projects/consolidated/research/extracted/{window_sensitivity_comparison,class_cut_scorecard,vendor_class_matrix,piid_profile}.csv`,
`projects/consolidated/research/extracted/sensitivity_fy{19,20}_25/` (4 CSVs each),
`projects/consolidated/workbook_award_analysis/` (full pipeline: launcher,
validator, lib, 8 sheet modules + `_cuts`/`_layout`/`_taxonomy` helpers,
`extracted/wb_*.csv` ×5),
`projects/consolidated/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`.
Modified: `projects/consolidated/research/scripts/{_corpus,compute_competability_signals,build_target_list}.py`
(window/outdir parameterization + vclass/bgroup threading; headline outputs
byte-identical), `projects/consolidated/findings_competability_scorecard.md`
(caveat 6, §3a, artifacts line), repo memory
(`present-data-before-characterization`).
Restored: `projects/consolidated/workbook/` (chart-data-only, rebuilt) and its
`20260605_…Consolidated_vS.xlsx`.
