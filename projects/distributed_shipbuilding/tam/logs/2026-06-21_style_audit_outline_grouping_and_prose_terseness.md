# 2026-06-21 — Master TAM style-audit pass (outline grouping + formatting hygiene + prose terseness)

A **value-preserving, presentation-only** pass over the master TAM workbook
(`tam/master/`) implementing an external style audit (`workbook_style_audit.md`): make
the workbook read analyst-native and behave correctly without moving a single headline
number. Two genuine engine touches (both backward-compatible, opt-in, zero collateral on
the sibling pipelines), a layout-cursor extension for nested outline grouping, then
sheet-by-sheet re-leveling + formatting fixes + prose cuts. Follows the same-day
structural refactor and ICAEW-checks passes; same canonical pipeline.

## Why
The model structure was already sound; the gaps were presentation: (1) the gutter `x`
collapse marks were cosmetic because Excel's outline symbols were hidden, (2) the row-3
italic captions averaged ~172 chars (127-222) and, with no-wrap, spilled like generated
prose; section banners and many row labels were sentence-length and clipped, (3) a visible
percentage-format bug (Virginia OBBBA observed BC share rendered ~0.6 not 58.2%), and
(4) several cell styles violated the house color / number-format / total-border rules.

## Master invariant
Every change is **value-preserving** — `validate_workbook.py` hits the *same* baselines
throughout (cum 13636.3 / 4507.1 / 6421.7; coeffs 34.0/22.0/25.3%; FY28-31 band 4383→4409
low / 4922→4931 high). All re-leveling, style, and prose edits preserve cell values and
row numbers (the cursor advances identically; load-bearing positions are asserted at
build time). Renaming a *validator-anchored* label is the one coupling: it forces a
lockstep `_ANCHORS` update, else label-resolution fails.

## The work
1. **Engine: opt-in outline symbols + leveled banners** (`workbook_core/primitives.py`,
   the only core edit). `worksheet()` gained `show_outline_symbols: bool = False` —
   gutter mode hard-set `showOutlineSymbols="0"` for *every* gutter workbook; the flag
   lets a sheet surface Excel's native +/- controls. `banner_row()` gained
   `outline_level: int = 0` so a §-banner can act as the summary row for its detail.
   Both default to prior behavior → army / MRO / award_classification / consolidated are
   byte-identical (verified).
2. **Cursor: nested-level helpers + leveled blanks** (`sheets/_layout.py`). `RowCursor`
   tracks a running `_detail` level and exposes `title`/`caption`/`section`/`subsection`,
   building a deliberate `title(0) → section(1) → subsection(2) → detail(3)` hierarchy;
   `write`/`total` default `outline_level` to `_detail`; `blank()` now *emits* empty
   `<row outlineLevel=.../>` rows when nested (an absent row is an implicit level-0 row
   that would split the group). At level 0 it stays silent → un-migrated callers identical.
3. **Re-leveled all 12 sheets + row-2 `x`.** Each sheet swapped raw `c.banner(...)` for
   `c.title/c.section/c.subsection`, dropping explicit `outline_level=1`. Whole-sheet fold
   via the row-2 title; per-section / per-subsection folds below. The native PoP table was
   the delicate case (3 cursors, position asserts, ExcelTable overlay) — handled by
   threading the detail level so the corpus folds under §2.
4. **Style / format corrections** (value-preserving). `assumptions` Virginia OBBBA observed
   share `S_LINK_NUM`→`S_LINK_PCT` (the % bug). Green→black on transformed (non-pure-link)
   formula rows: `scn_budget` constant-FY2026 + DDG AP/LLTM rows, `fydp` constant rows,
   `obbba` gross + Virginia BC constant rows, `_program_tam` DDG `N()`-link. Exec
   `Total`/`Total low`/`Total high` and SCN `Portfolio Basic Construction` → `c.total()`
   (continuous medium top border via `BORDER_TOP_FOR`). PoP `Master`/`FY18-22 vintage`
   flags and FYDP `Procurement quantity` → `S_INT_INPUT` (integer; no more `1.0`).
5. **Prose: maximally terse (audit followed fully).** All 12 captions rewritten to one
   clause (now ≤62 chars). Methodology collapsed to 4 sections (Scope / Formula /
   Coefficients / Sources), paragraph rows removed, source names abbreviated; Assumptions
   `§1 - Run settings` dropped and the 5 Notes cut to one line each; OBBBA `Scope` column
   moved into cell Notes (Award/Section/Gross $M kept visible); Exec 4-row Scope narrative
   → terse key-values and the `Model integrity check` row removed (validation stays on the
   Checks tab); Checks `Master check` banner numbered `§4`. Stripped visible `artifact`,
   `-> TAM`, the FYDP `Refresh` instruction row (→ docstring), and `folded` from the three
   program captions. Banners and ~30 row labels shortened per the audit's tables.
6. **Validator coupling** (`validate_workbook.py`). Three renamed Place-of-Performance
   coefficient labels updated in `_ANCHORS` (values/tolerances unchanged); they re-resolve
   to the same rows (E11/E13/E20). The TAM-tab anchors were not renamed.
7. **Late reversal — collapse controls dormant by default.** After seeing the live
   workbook, the user did **not** want the outline gutter / 1-2-3-4 level bar showing on
   open. Flipped `show_outline_symbols=True`→`False` on all 12 sheet `worksheet()` calls:
   the workbook opens clean (`showOutlineSymbols="0"`), but the full nested `outlineLevel`
   grouping + gutter `x` cues stay baked in — re-enable interactivity in one keystroke per
   sheet, or via Excel **View → Show Outline Symbols**.

## Conventions now in force
Sheet layout is a deliberate nested outline (title 0 / §-section 1 / §Na-subsection 2 /
detail 3), emitted always but with the controls hidden by default · blank rows inside a
group are emitted leveled (contiguity) · editable knobs keep the pale-yellow input fill ·
green is reserved for pure cross-sheet links; transformed/`N()`-wrapped formulas are black ·
labels beginning Total/Portfolio use `c.total()` (bordered) · round-integer flags use an
integer style · row-3 captions are one clause; `validate_workbook.py` stays the external
baseline guard, with anchors renamed in lockstep when a labeled row is.

## Verification
Build → 12 sheets, exit 0. `validate_workbook.py` → **RESULT: PASS** (0 XML errors, 0
formula-error cells; all 12 tie-out anchors, 6 Exec FY-total cross-checks, 8 outyear-band
checks match baseline) after each sheet and after the final reversal. Emitted-XML sweep:
`showOutlineSymbols="0"` on all 12 (clean on open); 0 visible `artifact`/`-> TAM`/`Refresh`/
`folded`; 0 em/en dashes; captions ≤62 chars. Style spot-checks confirmed: Assumptions
observed share xf 12 (S_LINK_PCT), Exec/SCN totals bordered (3/13/16), PoP master/vintage
xf 45 (S_INT_INPUT). Collateral: rebuilt the army workbook — all 19 gutter sheets still
`showOutlineSymbols="0"` (engine change provably opt-in; only the 10 master-TAM sheet
modules reference the flag).

## Files touched
Engine: `workbook_core/primitives.py` (`worksheet` show_outline_symbols, `banner_row`
outline_level). Pipeline: `sheets/_layout.py` (nested-level cursor + leveled blanks);
`validate_workbook.py` (3 PoP anchor labels); and the sheet modules `executive_summary`,
`methodology`, `assumptions`, `_program_tam` (+ `virginia_tam`/`columbia_tam`/`ddg_tam`
captions), `scn_budget`, `place_of_performance`, `obbba`, `fydp_outyears`, `deflators`,
`checks`.

## Open / not done
- Outline controls ship **dormant** (`show_outline_symbols=False`). The grouping is fully
  built; flip the flag (or Excel View) to surface it. Not done: a *default-collapsed* open
  state (would bake `hidden`/`collapsed` row attributes) — offered, not requested.
- Deferred audit minors: a green 2-dp `S_FACTOR_LINK` clone for the deflator driver rows,
  recomputing the hardcoded Deflators factors in-sheet, and the build-time emitted-XML
  style linter (a separate new tool, not one of the requested changes).
- The army `.xlsx` was rebuilt in place for the collateral check (it was already modified
  in the working tree; the rebuild reproduces it from unchanged army source).
