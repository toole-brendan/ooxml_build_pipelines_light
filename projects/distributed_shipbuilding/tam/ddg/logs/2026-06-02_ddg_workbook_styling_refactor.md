# 2026-06-02 — DDG workbook styling refactor (all 23 sheet modules → current house style)

## Scope

Comprehensive styling migration of `core/ddg/workbook/workbook_ddg` — all 23 sheet
modules brought up to the current `core/workbook_core` house style. Driven by an
external audit (sheet bodies still carried pre-guide habits: unnumbered banners,
missing spacer rows, built-in `TableStyleLight1`, hard-coded row offsets, manual
accessors, already-total styles fed to `total_row()`, mis-applied green links,
leading-space fake indents, left-aligned numeric headers, long prose). This is a
SOURCE-MODULE migration (the prior built `.xlsx` was just a stale artifact); the
23-tab structure + group order were already correct, so no group/registry change.

Mirrors the in-progress submarine refactor (`core/submarine/workbook/workbook_sub`)
as the authoritative template. Plan approved before implementation.

## Decisions carried in (from the user)

1. **Accessor refs — mirror submarine (closures), NOT `sheet_ref()`/`range_ref()`.**
   Accessors return f-string closures over cursor-captured rows (`lambda: f"'{tab}'!C{r}"`).
   The captured-row pattern prevents generator drift; relative-vs-absolute is moot
   (Excel auto-adjusts on insert). This is a deliberate divergence from the audit's
   Phase 4 — the two sibling workbooks stay structurally identical.
2. **Scope = Everything** — full style conformance + Phase-9 data validations + the
   two native-table conversions (Deck Outputs, Figure Audit).
3. **Methodology — keep & slim** (renumber §N, compress prose, strip fake indents,
   reduce widths).

## Engine / shared

No `core/workbook_core` change. The `RowCursor` was **copied** (copy-from, per the
"snippets stay copy-from" principle) into `workbook_ddg/sheets/_layout.py`,
byte-identical to submarine's `_layout.py` (composes `banner_row`/`write_row`/
`total_row`; `.banner/.write/.total/.feed/.blank/.at`; `_resolve()` lets a value be a
`lambda r: …` for self-referential formulas).

## What every module got

`RowCursor`-driven layout; section banners renumbered to `§N - Title` /
sub-sections `§Na - Title`; the 1/1/2 spacing rhythm via `c.blank()` / `c.blank(2)`;
`S_HEADER_CENTER` on numeric/FY headers; `S_LABEL_INDENT_1/2` for hierarchy (no more
leading-space fakes); `style="TableStyleLight1"` dropped from every `ExcelTable`
(now the default `WorkbookCore_NoFormatTable`); `total_row()` passed BASE styles;
green `S_LINK_*` only on pure single-cell links; widths nudged toward house ranges;
prose compressed.

## Highest-risk conversions

- **`tam_build.py`** (two-pass, mirrors submarine `tam_build`): four
  `_build_<section>(tab, base)` builders (§2 Normalized Budget, §3 Coefficients,
  §4 MYP, §5 Model) run at import, capture load-bearing rows into `pos` dicts, return
  `(rows, next, acc)` of accessor closures; module scope promotes all 24 accessors by
  name; `_render_tam_build()` builds the §1 at-a-glance, `assert c.at() == _NB_BASE`,
  then `c.feed`s the blocks. The `Rb/Rc/Rm/Rt` offset scheme + offset dicts are gone;
  `_ccell(k)` → `f"C{pos[k]}"`; same-row sums → `lambda r:`; the SUMPRODUCT coefficient
  masks (`_INSCOPE`/`_BC`/`_BC_DISC`/…) are built only from imported POP-corpus ranges,
  copied verbatim. Three `S_NUM_TOTAL`→base-style fixes on the `total_row` calls.
- **`sam_build.py`** (two-pass, explicit-anchor-via-cursor): §2 Subawards → §3
  Allocation → §4 Scenarios; preserves the modeled/observed/bucket/sam column letters
  and 15 accessors. **Green-link fix (audit #6): the portfolio-TAM row is now a single
  pure link `=tam_build.portfolio_tam_cell()` (green), replacing the six-cell
  `=N(...)+N(...)` sum** — both correct-green and removes a redundant re-summation
  (improves on the submarine template, which still sums there).
- **`deck_outputs.py` + `figure_audit.py`** converted to native no-format tables
  (`tbl_ddg_deck_figures`, `tbl_ddg_figure_audit`); native tables 9 → 11.

## Other notable per-module work

- **`inputs`**: Phase-9 data validations (scenario-key dropdown, 0/1 toggles,
  decimal-bounded knobs/POP%/adjustments) via local `_dv_*` helpers; centered FY/value
  headers; note column 48→30.
- **`scenarios`**: 0/1 validation on the matrix; bucket-count split into §4.
- **green/black fixes** also applied in `tam_build` §4 MYP (combined master $ and
  combined other+foreign % → black `S_NUM`/`S_PCT`; the §4b swing → black) and the
  AP/LLTM coefficient row → green `S_LINK_PCT` (pure link to Inputs).
- **`locations`**: domestic/foreign split is now formula-driven (% = $/total) with a
  `total_row` SUM (was a hand-built literal total row).
- **`fpds_primes`**: hand-built "Total" → `total_row` with `SUM` formulas; centered
  vendor-group headers.
- **`scope_exclusions`**: class subtotals (hand-built `write_row` + `S_TOTAL`/
  `S_NUM_TOTAL`) → `total_row` base styles.
- **`qa_checks`/`figure_audit`/`executive_summary`**: added `figure_audit.fail_count_cell()`
  and `qa_checks.qa_fail_count_cell()`/`qa_status_cell()`; QA Checks and Executive
  Summary now LINK to those rendered cells instead of recomputing the COUNTIF.
- **`pop_audit`**: leading-space fake indents → `S_LABEL_INDENT_1`; dropped the
  exported-audit-cells prose block.
- **`methodology`**: §1-§5 / §Na renumbering, leading-space continuation prose
  stripped, blank-after-banner rhythm, widths 46→42.

## Verification (read-only / structural — the agreed ceiling; mirrors submarine)

Rebuilt from source: **23 sheets in order (first Executive Summary, last References),
11 native tables, 96,617 bytes**; the packager's sheet/table/defined-name validators +
group-contiguity assertion all pass; the two-pass `assert c.at() == BASE` invariants
hold in `tam_build`, `sam_build`, `figure_audit`, `qa_checks`.

A temp XML-level audit + a final verifier (both removed after) confirmed:
- `xl/styles.xml` carries the current **23 cellXfs**; all 11 native tables use
  `WorkbookCore_NoFormatTable` (zero `TableStyleLight1`).
- Every `S_TITLE_SECTION`/`S_TITLE_SUBSECTION` banner matches `^§\d+[a-z]? - `; no
  banner is immediately followed by content (1-blank rule); no leading-space labels.
- No green-styled formula contains arithmetic / `N(...)` / `SUM`; FY/numeric headers
  use `S_HEADER_CENTER`; no `S_*_TOTAL`/indent style reaches `total_row()`.
- **619 formulas scanned — zero references to any unknown/retired tab** (no dangling
  refs), zero `#REF!`/error literals; all 51 parts well-formed XML.
- Defined names point to producers: `portfolio_tam → 'TAM Build'!$I$114`,
  `portfolio_bc_tam → $I$112`, `portfolio_ap_tam → $I$113`, `bc_supplier_coeff → $C$42`,
  `sam_broad → 'SAM Build'!$C$70` (cells moved with the restructure; the accessor-driven
  names tracked them automatically).
- **No domain accessor or domain constant dropped** (build resolves every cross-module
  import; surface diff vs a pre-refactor baseline showed only engine-helper /
  style-constant import-surface shrinkage).

**Environment:** `python` 3.14.4 on PATH; read-only checks + the workbook build output.
Per the agreed ceiling, NOT opened in Excel.

## Deliberately NOT done / known gaps

- **No Excel recompute.** `Number Audit`/`QA Checks` FAIL=0 and the numeric tie-outs
  (bucketed TAM = portfolio TAM, broad SAM ≤ TAM, AP/LLTM additive, anchor OK) cannot be
  confirmed without Excel. Formula chains are verified intact and reference valid cells;
  the QA identities hold by construction — but a real Excel pass is the remaining check.
- Native Excel **Notes** were not used; long derivations were compressed on-sheet or
  left to Methodology/References rather than minting hover cards (Notes stay rare).
- Source tables (`Source Lineage`, `References`) keep one-line context notes (the
  documented source-table exception) at reduced widths.

## Files changed this session

- **Added:** `workbook_ddg/sheets/_layout.py` (copied from submarine).
- **Rewritten (all 23 sheet modules):** `executive_summary, methodology, inputs,
  scenarios, tam_build, sam_build, scn_budget, production_schedule, ap_bridge,
  pop_corpus, entities, locations, vendors, fpds_primes, bucket_evidence, deck_outputs,
  qa_checks, figure_audit, sensitivity, scope_exclusions, pop_audit, source_lineage,
  references`.
- **Unchanged:** `workbook_ddg/sheets/__init__.py` (registry/group order already
  correct), `workbook_ddg/sheets/_taxonomy.py`, `lib.py`, `__init__.py`,
  `build_workbook.py`; all of `core/workbook_core`.
- **Rebuilt artifact:** `20260601_Destroyer Outsourced Construction_vS.xlsx`.
- **Temporary (created then removed):** `_baseline.py`, `_baseline_surface.json`,
  `_audit.py`, `_verify_final.py`.
- **This log:** `core/ddg/workbook/logs/2026-06-02_ddg_workbook_styling_refactor.md`.

## Follow-ups

- **Open in Excel** to confirm the numeric tie-out (QA 0 FAIL, Figure Audit 0 FAIL,
  bucketed TAM = portfolio TAM, broad SAM ≤ TAM) and that no cell trips a repair dialog.
- The deck pipeline can point at the new producer cells / defined names (unchanged
  names; cells moved).
- Optional: the submarine workbook can adopt the same SAM portfolio-TAM pure-link fix
  (it still sums the annual TAM cells).
