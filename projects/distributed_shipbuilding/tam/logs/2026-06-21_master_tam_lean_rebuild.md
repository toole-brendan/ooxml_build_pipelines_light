# 2026-06-21 — Master TAM lean rebuild (tam/master replaced) + POP/colors refinements

Rebuilt the master TAM workbook from scratch (surgically porting the formula logic,
dropping the unwieldy structure), retired the old one, then refined it: moved the
place-of-performance masters onto their own data tab, split Virginia/Columbia, converted
the FY headers, and repainted the tabs. The lean build is now canonical at `tam/master/`.
Follows `2026-06-20_master_tam_consolidation.md` and the
`2026-06-21_gfe_vs_bc_base_investigation.md` "no change to methodology" finding.

Build sequence note: the rebuild was authored in a temporary `tam/master_v2/`, verified,
then the old `tam/master/` was deleted and `master_v2` renamed to `master`. Paths below
say `tam/master/` (the final location).

## Why
`tam/master/` was 8,116 LOC of sheet code across per-program subfolders
(`submarines/ ddg/ ceiling/`) with copy-pasted infra (`_layout`/`_bind`/`_registry`/
duplicated taxonomy) and ~30 of 42 tabs being per-program copies of the same 6 functions.
Per user: lean rebuild, three programs treated INDIVIDUALLY, one executive summary, data
sheets embedded as the live-formula spine (the award_classification pattern), **no toggle
checkboxes and no in-sheet OK/FAIL checks**, ceiling **tabled**.

## Result — `tam/master_v2/`, 11 tabs, 1,785 LOC sheet code (-78%)
Flat SAM-style layout: one file = one tab under `sheets/`, every helper `_`-prefixed and
single-copy (`_layout _tabs _widths _cuts _program_tam`).
- **summary** Executive Summary (Virginia | Columbia | DDG-51 | Total; all links)
- **guide** Methodology (merged the per-program methodology + source index + references)
- **inputs** Assumptions (single edit surface; toggles + dropdown validations removed)
- **model** Virginia TAM · Columbia TAM · DDG-51 TAM — each self-contained: BC×coeff +
  OBBBA (+ DDG AP/LLTM) + folded FY28-31 outyear projection. Built by one shared
  `_program_tam.build_program_tam()` with per-program config (Va: BC+OBBBA spillover;
  Col: BC only; DDG: BC+AP+OBBBA, FY2022-vintage coeff). No checks blocks.
- **data** (combined by type, all 3 programs each) SCN Budget · Place of Performance ·
  OBBBA Mandatory · FYDP Outyears · Deflators.

## Data layer
`build_extracted.py` reshapes raw exhibits in `source_data/{submarines,ddg}/` (copied
verbatim from the upstream corpora so v2 is self-contained) into 5 clean combined CSVs in
`extracted/`. Transforms mirror the original per-program data modules exactly.
- Place of Performance is GATED-rows-only (43 sub + 152 DDG + 2 live-linked DDG MYP master
  rows). Every coefficient SUMPRODUCT is gate-masked, so dropping non-gated rows changes
  no number. DDG applied BC coeff is a live SUMPRODUCT over its corpus (masters dominate,
  25.3%); submarines apply announced-master POP (Va 34% / Col 22%) with the corpus as
  reference (35.0% / AP 48.5%). Deflators regenerated from `workbook_core.deflators`.

## What was dropped / folded
9 ceiling tabs (tabled); stream toggles + all dataValidation dropdowns; OK/FAIL checks and
the validation tabs (now an external `validate_workbook.py`); the separate Outlook tabs
(folded into each program TAM tab); 6 per-program guide/sources tabs (→ one Methodology);
the submarine AP/LLTM stream (=0, explained in Methodology); DDG per-hull / production
schedule / AP-bridge tabs (AP base+coeff live on Assumptions). Editable numeric inputs
(coefficients, OBBBA BC-share, intent uplift, spillover) are kept.

## Verification — exact tie-out to the retired master
LibreOffice headless recalc: 0 XML errors, 0 error-literal cells, 0 formula-error cells.
Per-program cumulative TAM matches the old master to the digit (Virginia 13,626.76;
Columbia 4,507.09; DDG-51 6,421.73; Portfolio 24,555.58), as do average annual, applied
coefficients, and FY28-31 outyears (Va+Col low 3,631.61 = old Sub-portfolio; DDG
720.89/937.15). `validate_workbook.py` embeds these anchors as a regression guard (survives
master/ deletion) — `RESULT: PASS`.

## Cutover
`tam/master/` deleted (was git-tracked, 132 files → recoverable). Nothing outside it
referenced it; `master_v2` rebuilds from scratch self-contained. Output filename unchanged
(`20260620_Distributed Shipbuilding Master TAM_vS.xlsx`).

## Follow-up edits (same session, after the rebuild)
- **Renamed `master_v2` -> `master`** (the lean build is now canonical at `tam/master/`).
- **Construction masters moved from Assumptions to the Place of Performance tab** (they
  are themselves DoD award announcements). Each program's applied BC coefficient is now
  derived on the POP sheet as a $-weighted SUMPRODUCT over its own rows (master +
  disclosed) - the same mechanism for all three programs. Effect: Virginia 34.00% ->
  **34.024%** (Block V master dominates; +~$9M, portfolio TAM 24,555.6 -> **24,565.1**);
  Columbia 22.00% and DDG 25.29% unchanged. Assumptions now holds only behavioral levers
  (DDG AP/LLTM, OBBBA BC-share + spillover, outlook uplift).
- **Va/Col split + GFE rows dropped (2a):** POP `program` column is now Virginia /
  Columbia / DDG-51 (no "Submarine" bucket). GFE-excluded rows (27 shared-submarine GFE +
  the DDG GFE announcements) are dropped - they never entered any coefficient - leaving 51
  gated, BC-eligible, class-attributable rows. New columns: `master`, `vintage` (FY18-22),
  `source` (the DoD-announcement URL/citation on every row).
- **Source verified:** the master POP traces to the DoD daily Contracts releases -
  Virginia Block V (2019-12-02, defense.gov Article 2030017, $22.2B, N00024-17-C-2100),
  Columbia Build I (2020-11-05, Article 2406922, $9.47B, N00024-17-C-2117), DDG FY18-22
  (2018-09-27, Article 1647166). PIIDs confirmed correct. These big multiyear awards are
  NOT in the disclosed corpus CSV (which spans ~2022+), which is why they're carried as
  explicit master rows.
- **FY column headers** converted from calendar-year integers to `FY2022`..`FY2031`
  across SCN Budget, OBBBA, FYDP Outyears, Assumptions, and the three TAM tabs.
- **Tab colors** repainted to mirror the SAM `award_analysis` muted scheme via a per-build
  `_groups._COLOR` override in `lib.py` (no sheet-module change): summary `262626`
  charcoal · guide `2C5E5E` muted teal (added; award_analysis has no guide tab) · inputs
  `556B2F` olive · model `48596B` slate · data `203864` navy. Also cleaned the stale
  `master_v2` strings out of `lib.py`.
- `validate_workbook.py` anchors re-baselined to the new values; `RESULT: PASS` (0 XML /
  0 formula errors, all anchors OK, Exec total reconciles).

## Open / not done
- Ceiling layer intentionally not ported (tabled per user); the FYDP/outyear integration
  with a ceiling remains future work.
- Decks still reference the old per-program outputs (out of scope; no live links wanted).
