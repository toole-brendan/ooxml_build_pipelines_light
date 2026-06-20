# 2026-06-15 — Award Analysis workbook: Overview tab restructure (scope block, de-breadcrumb, findings block)

Pipeline: `projects/distributed_shipbuilding/workbook_award_analysis/`
Output:   `projects/distributed_shipbuilding/20260612_Distributed Shipbuilding Award Analysis_vS.xlsx`
Build:    `python3.12 build_workbook.py` → `python3.12 validate_workbook.py`

## Trigger
User disliked the Overview's trailing breadcrumb row `Reported subaward $M by
role x FY is on By Role.` (a navigation *sentence* = the LLM-ish text-ism), and
asked what else / what better structure the Overview should carry given the rest
of the sheets — kept concise. Two real gaps: no scope/basis statement, and the
page only said *how big the corpus is*, never *what was found*.

Decided (AskUserQuestion): Scope + counts + findings, **including** the richer
emerging-competition + re-buy-due metrics (which needed new accessors).

## What changed — Overview is now three short sections (`summary_overview.py`)
- **§1 - Scope** (new, label:value, derived from constants so it can't drift):
  Source = FSRS reported subaward records; Window = `≤FY12 through FY26` (from
  `FY_LABELS[0/-1]`); Programs (from `PROGRAMS`); **As of 2026-05-22** (the real
  corpus latest-award date, verified — replaces a "pull date not recorded" prose).
- **§2 - Corpus shape** (existing block): renamed banner §1→§2, kept all six count
  rows + the both-classes note, **deleted the breadcrumb**.
- **§3 - Supplier base structure** (new per-program findings block): Multi-source
  lanes (2+ vendors) · Single-source lanes · Top vendor share of program $ ·
  Emerging-competition lanes · Lanes with re-buy due ≤12 mo.

## Engine constraint that shaped §3
`workbook_core/primitives.py:134` `cell()` emits only plain `<f>` cells — **no
`t="array"`**. So a CR3/top-3 concentration ratio (`LARGE(IF(…),{1,2,3})`, CSE)
would render only its first element. Used **top-vendor share (CR1) via
`_xlfn.MAXIFS`** instead (legacy-safe, already used in this workbook).

## New accessors (additive, `fn(program)->str` returning a bare COUNTIFS/MAXIFS
fragment over the table body `f..last`; consumer wraps `f"={…}"`):
- `data_piid_worktype.py`: `pw_cols()` + `pw_multi_count` / `pw_single_count`
  (COUNTIFS over the already-written Vendors count col H, ≥2 / =1). No new leaf col.
- `data_source_concentration.py`: `sc_emerging_count` = `COUNTIFS(Program B,
  Incumbent-active M = "yes")`. The "yes" incumbent rows are *exactly* the
  second-source-entered lanes (verified: 25 "yes" total = 7+6+12), so the single
  condition is unambiguous and dodges the empty-string `"<>"` gotcha.
- `data_rebuy_timing.py`: `rb_due_count` = `COUNTIFS(Program B, Next-re-buy L in
  [46164, 46529])` — **frozen serials** 2026-05-22 .. 2027-05-22 (reproducible,
  not drifting `TODAY()`; matches §1 "As of"). Blank "" next-re-buy cells drop out
  of the numeric comparison.
- `data_by_vendor.py`: extended `bv_cols()` with `tot` (the `$ Total` col, = Y)
  for the CR1 MAXIFS numerator; denominator is `vendor_total_cell` (both off By
  Vendor → exact reconciliation).
- Return-arity of the three model modules went `X = _make()` → `(X, fn) = _make()`;
  registry only references the `SheetEntry` constants, so unaffected.

## Verification
- Build clean: 0 xml errors, 0 error-literal cells; 13 native tables; 15 sheets.
- Overview XML (sheet1.xml): breadcrumb absent (`is on By Role` → 0); three new
  banners present; §3 formulas point at the right table bodies — PIID×Work Type
  `$B/$H$7:$138` (≥2 / =1), By Vendor `$Y` with per-program total cells, Source
  Concentration `$M="yes"`, Re-buy Timing `$L` in `>=46164 / <=46529`.
- §3 values **independently recomputed from the extracted CSVs** (build can't
  evaluate formulas; no headless recalc) — all match:
  - multi-source 34 / 24 / 68 · single-source 1 / 2 / 3
  - top-vendor share 0.339 / 0.158 / 0.136 (denoms 4343.6 / 3342.2 / 3095.4,
    matching the Tie-Outs oracle)
  - emerging 7 / 6 / 12 · re-buy-due 3 / 0 / 18
- Values appear on the user reopening in Excel (caches the recalc); the re-buy
  window is frozen so the count is stable across reopens.

## Notes
- Re-buy-due uses CSV `last_award_date`+gap for the offline recompute; the sheet
  uses `_xlfn.MAXIFS` over the Lane Vendors x FY `last` column — could differ by a
  row in edge cases, but the recompute lands on the targets.
- "Emerging-competition lanes" label shortened from "(1→multi, incumbent stays)"
  to fit the 34-wide label column; the full screen definition lives on the Source
  Concentration tab.
