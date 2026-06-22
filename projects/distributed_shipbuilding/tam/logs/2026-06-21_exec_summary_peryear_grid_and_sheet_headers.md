# 2026-06-21 — Exec Summary per-year grid (transposed, FY22-31E) + house header pass

Reworked the Executive Summary from a cumulative/average measures block into a
transposed per-year TAM grid (FY2022-2031, with FY2026+ marked as estimates), deleted
the standalone outyear section, then propagated the award_classification "italic caption
under the title" header pattern — and the collapsible-§1 `x` marker — across every
remaining tab. Follows `2026-06-21_master_tam_lean_rebuild.md`; same canonical pipeline
at `tam/master/`. All numbers unchanged on the program tabs; this is a presentation pass.

## Why
The cumulative FY22-27 headline read poorly: it's a 6-year `SUM(C:H)`, and one program
(Columbia) is $0 in three of those years, so a single lumped number hides the
procurement lumpiness. Per user: show the **individual years, no roll-up**; mark which
years are firm vs estimate; and make the rest of the tabs visually consistent with the
exec summary's new title/caption spacing.

## Exec Summary §2 — now a transposed per-year grid
Programs DOWN the side (Virginia | Columbia | DDG-51 | Total), fiscal years ACROSS the
top, every cell a live link into the program tabs (`tam_cell(fy)` / `outyear_mid_cell(fy)`):
- **FY2022-2025** firm (no suffix). **FY2026E / FY2027E** = budget point estimate
  (`tam_cell`), still firm-ish but flagged (FY2026 carries the one-time OBBBA surge,
  FY2027 not yet enacted). **FY2028E-FY2031E** = **midpoint** of the low/high outyear
  band, `=(low+high)/2`.
- **Total** is now a per-year ROW (`=SUM` down the three program rows), a cross-section,
  not a temporal roll-up. Coefficients sit in a trailing **BC coeff** column (Total blank).
- Dropped: the FY22-27 cumulative row, the avg-annual row, the standalone OBBBA-cumulative
  row. Kept the Applied BC coefficient as context. **§3 (FY2028-31 low/high band) deleted.**
- Number format inherits numFmt 164 (`#,##0.0`) = the max-1-decimal house rule; the
  midpoint keeps full precision internally, renders rounded.

Final grid (recalc, constant FY2026 $M):

| $M | FY22 | FY23 | FY24 | FY25 | FY26E | FY27E | FY28E | FY29E | FY30E | FY31E | coeff |
|----|----|----|----|----|----|----|----|----|----|----|----|
| Virginia | 1,780.8 | 1,855.0 | 3,209.7 | 1,848.5 | 1,978.2 | 2,964.0 | 2,936.2 | 2,827.6 | 2,542.5 | 2,584.3 | 34.0% |
| Columbia | - | - | 1,454.3 | - | 1,575.1 | 1,477.7 | 1,464.1 | 1,465.2 | 1,445.1 | 1,447.9 | 22.0% |
| DDG-51 | 474.4 | 1,233.6 | 874.0 | 1,236.4 | 1,929.2 | 674.1 | 635.3 | 650.4 | 1,000.1 | 1,030.3 | 25.3% |
| **Total** | **2,255.2** | **3,088.6** | **5,537.9** | **3,084.9** | **5,482.6** | **5,115.8** | **5,035.7** | **4,943.2** | **4,987.8** | **5,062.4** | — |

Italic E-legend footnote spells out the convention; §1 Window/units + the row-3 caption
updated to "FY2022-2031 (E = estimate)".

## Model facts surfaced (no change made to them)
- The per-year "TAM (all streams)" row on each program tab is a true single-year figure
  (BC base × coeff + streams), **not** an average. The old cumulative was a plain `SUM`;
  the only genuine averaging in the model is the **FY22-25 penetration baseline** that
  drives the FY2028-31 projection (deliberately excludes FY26-27, which carry OBBBA).
- **OBBBA lands entirely in FY2026** (Virginia +$911M, DDG +$858M); FY22-25 is pure BC.
- Per-program cumulative (still on the program tabs, unchanged): Virginia 13,636.3 /
  Columbia 4,507.1 / DDG-51 6,421.7. The exec summary no longer surfaces it.

## House header pass — italic caption + collapsible §1, every tab
Ported `_italic.py` (italic-black `S_ITALIC`, fontId 5; same per-build CELL_XFS append
trick as award_classification) into `workbook_master_tam/sheets/`. Applied the Taxonomy/
`_flat` pattern everywhere: **title banner → italic one-line caption (no gap) → 2 blank
rows → §1 banner**. New captions, award_classification house style (terse, leads with the
sheet's nature), on all 11 tabs (exec summary, methodology, assumptions, the 3 program
TAMs via `_program_tam`, scn_budget, place_of_performance, obbba, fydp_outyears, deflators).

Three sheets carry fixed row-bases that the +2 header growth shifted:
- `_program_tam.py` `body_base` 9 → **11**; `scn_budget._DETAIL_BASE` 13 → **15**;
  `place_of_performance._DATA_BASE` 21 → **23** and headline base 6 → **8**.

Also added the collapsible-section `x` (gutter, `mark_collapsible=True`) + `outline_level=1`
to the **first-section banners** that lacked it — program TAM §1 Headline, SCN Budget §1,
OBBBA §1, FYDP §1, POP §1 — so §1 now folds like every other section. POP §1 is a parent
over §1a/§1b (which already fold individually); its `x` is a section marker, the actual
fold buttons live on the subsections (left as-is; flagged for optional flatten).

## Plumbing
- `_program_tam.py`: new `intro=` param (per-program caption); new `outyear_mid_cell(fy)`
  accessor (per-outyear low/high midpoint), exposed on all three program modules.
- `executive_summary.py`: transposed builder (`_PROGRAMS`, `_fy_label`, `_cell`,
  `col_letter`-driven per-FY Total); `_row`/`_NAMES` helpers removed.

## Verification
`validate_workbook.py` → **RESULT: PASS** after two anchor re-baselines:
- Internal cross-check rewritten for the transposed grid (sums DOWN program rows per FY
  column); ties out all ten FY columns.
- Tie-out anchors re-pointed **+2** (header shift): program-tab cumulative C7→C9, avg
  C8→C10, coeff C9→C11; POP coeffs C9/C11/C18 → C11/C13/C20. Values unchanged.
- 0 XML errors, 0 formula-error cells; output filename unchanged.

## Open / not done
- POP §1 left as a parent-of-subsections (decorative `x`); optional flatten to make §1
  itself fold would shift its coefficient rows up 2 and re-point 3 anchors.
- Decks still reference old per-program outputs (out of scope; unchanged from prior log).
