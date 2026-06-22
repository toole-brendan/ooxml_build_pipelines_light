# 2026-06-21 — Adopt two ICAEW Financial Modelling Code practices (in-workbook checks + input fill)

A **value-preserving, pipeline-only** pass over the master TAM workbook (`tam/master/`)
that closes the two genuine gaps between the model and the ICAEW *Financial Modelling
Code*: it had no live in-workbook checks, and it marked input cells by font colour only.
Driven by a claim-by-claim comparison of the Code against the built workbook; the
architecture (per-program model tabs, `_program_tam` builder, combined-by-source data
tabs, accessor pattern, external `validate_workbook.py`) was already sound and is kept.
Follows the same-day structural refactor; same canonical pipeline.

## Why
The workbook already conforms to most of the Code — inputs/calcs/outputs layering, live
formulas (no baked values), single edit surface, traceable accessor refs, the "call-up"
pattern, no hardcoding, no VBA, an external recalc/tie-out validator. Two gaps remained:
1. **Checks (Principle #17).** Fidelity was asserted *externally only*, at build time, by
   `validate_workbook.py` — which never runs when a user opens the `.xlsx` and edits a
   knob. The model's own ethos is live recalculation, so live in-sheet checks belong here.
2. **Input cells (Layout, explicit red-X).** Inputs were blue *font* only. The Code says
   distinguish them by a fill colour and/or border, "not just a defined font colour".

User scope (chosen via Q&A): just these two, **pipeline-only** — do not edit `workbook_core`.

## Master invariant
Every change is **value-preserving** — `validate_workbook.py` hits the *same* baselines
throughout (cum 13636.3 / 4507.1 / 6421.7; coeffs 34.0/22.0/25.3%; FY28-31 band 4383→4409
low / 4922→4931 high). The input fill is cosmetic; the checks are additive (new tab + one
Exec line). Any tie-out drift = a regression, not a re-baseline.

## The work
1. **Pale-yellow input fill (no engine edit).** New `_inputfill.py` mirrors the per-build
   style-append trick `_factor.py`/`_italic.py` use: append a pale-yellow fill (`FFF2CC`)
   to `workbook_core.styles.FILLS` and three filled clones of the input xfs
   (`S_NUM_INPUT_FILL`/`S_PCT_INPUT_FILL`/`S_INT_INPUT_FILL`) to `CELL_XFS`, **in this
   process only** — `build_styles_xml()` reads both lists at build, so nothing in the
   engine source changes and every other pipeline is unaffected. Fully additive: existing
   fill/xf indices (and all `S_*` constants) are untouched. Repointed the editable knob
   cells on `assumptions.py` (`S_PCT_INPUT` → `S_PCT_INPUT_FILL`); left link/formula cells
   unfilled. **Scoped to the Assumptions single edit surface** — data-storage tabs (SCN /
   FYDP / OBBBA / POP / Deflators) keep blue-font-only inputs (the Code cautions against
   heavy formatting inside data tables; can be extended later if wanted).
2. **In-workbook checks + master check.** New `checks.py` → a dedicated **Checks** tab in
   the `validation` group (gray, sorts last after the data tabs). Ten live checks, each
   row `[label, value, =IF(cond,"OK","FAIL")]` with status cells in column D:
   - §1 bounds — 3 applied BC coefficients ∈ (0,1]; 2 OBBBA modeled shares ∈ [0,1]; DDG
     AP/LLTM coefficient ∈ [0,1].
   - §2 band ordering — outyear high ≥ low across FY28-31, per program (MIN-margin ≥ 0).
   - §3 completeness — the 6 key behavioral knobs are present & numeric (`COUNT` = 6).
   - **Master check** — `=IF(COUNTIF(D{first}:D{last},"FAIL")=0,"OK","CHECK FAILED")`,
     surfaced as a one-line "Model integrity check" at the top of the Executive Summary
     (B4/C4 link the master cell). Conditional formatting red-fills any FAIL / CHECK
     FAILED cell (a per-build red dxf appended to `DXFS[1]`; `DXFS[0]` stays the reserved
     no-format table style).

   These are **sanity/structural** checks that flip on a genuinely bad edit; they
   *complement* `validate_workbook.py`'s external baseline-regression anchors rather than
   duplicate them (re-checking captured magic numbers in-sheet would just hardcode them).
   Two candidate checks were deliberately **dropped**: spillover conservation (the
   execution-aligned gross deflates the FY27-spilled portion by FY27's factor, so the
   constant-$ sum *legitimately* diverges when spillover>0 — a conservation check would
   false-FAIL) and an in-sheet Exec cross-foot (it would create an executive_summary↔checks
   import cycle and is near-tautological; `validate_workbook.py` already does it externally).

## Conventions now in force
Editable knobs carry a pale-yellow fill (not just blue font) · live OK/FAIL checks live on
the Checks tab (validation group) and recalc with the model · the master check is the
single verdict, mirrored on the answer page · `validate_workbook.py` stays the external
baseline-regression guard (the two layers reinforce each other).

## Verification
Build → 12 sheets, exit 0. `validate_workbook.py` → **RESULT: PASS** after the change: 0
XML errors, 0 formula-error cells; all 12 tie-out anchors, 6 Exec FY-total cross-checks and
8 outyear-band checks match baseline. Recalc (LibreOffice) confirms all 10 checks read OK
and the master = OK (Exec C4 = OK). **Negative test:** forcing the Virginia OBBBA adjustment
to 0.5 (modeled share → 1.082 > 1) flipped row 12 → FAIL, master → CHECK FAILED, Exec C4 →
CHECK FAILED; reverted and rebuilt clean. Styles inspection confirms fill id 6 (`FFF2CC`),
filled-input xfs 58/59/60, the red FAIL dxf, and that Assumptions knob cells reference xf 59.

## Files touched
New: `workbook_master_tam/sheets/_inputfill.py`, `workbook_master_tam/sheets/checks.py`.
Modified: `sheets/assumptions.py` (filled input styles + docstring), `sheets/executive_summary.py`
(master-check line), `sheets/_tabs.py` (`TAB_CHECKS`), `sheets/__init__.py` (register `checks.CHECKS`),
`lib.py` (validation tab colour), `sheets/_program_tam.py` (docstring). Untouched: everything
under `workbook_core/` (pipeline-only constraint honored).

## Open / not done
- Input fill is **Assumptions-only**. Extending it to the blue-font source values on the
  data tabs is a one-line-per-sheet change, deferred (kept data tables clean per the Code).
- Considered-but-skipped Code items (out of chosen scope): frozen panes, hyperlinked TOC,
  formatting-key legend, data-validation restrictions, sensitivity data-table, sheet
  protection. Frozen panes / hyperlinks / input *borders* would need `workbook_core` edits.
- `validate_workbook.py` was left unchanged; it could optionally gain an anchor asserting
  the in-sheet master check reads "OK".
