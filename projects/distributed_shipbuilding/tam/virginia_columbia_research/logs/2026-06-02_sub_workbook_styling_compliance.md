# 2026-06-02 — sub workbook: full workbook_core styling-compliance refactor (all 19 sheets)

## Scope

Brought every one of the 19 `core/submarine/workbook/workbook_sub/sheets/` modules into
full compliance with the `workbook_core` authoring standard (the four 2026-06-01
hardening logs). Driven by an external audit; each audit claim was verified against the
live code first (some were imprecise — corrected below). The calc chain and every
cross-sheet accessor are preserved; this is a styling + layout + light-content pass plus
one real bug fix. No `workbook_core` engine files were touched. DDG untouched.

Final state: `python build_workbook.py` → 19 sheets in group order, first tab
`Executive Summary`, 126,640 bytes, 10 native tables; all packager validators pass.
A read-only oracle (built for the pass, then removed) reported **0 errors / 0 warnings /
0 dangling references** across: unnumbered banners, built-in table styles, banner→content
spacing, 2-blank inter-section gaps, sequential §N numbering, leading-space labels,
green-on-derived formulas, and >44 columns outside the Sources exception.

---

## 0. Decisions carried in from the user (three forks resolved before coding)

- **Prose reduction: aggressive.** Model/validation blocks reduced to label + value
  (+ short ref); standalone narrative sections and Note/Basis/Rationale/Treatment columns
  stripped, with the provenance relocated to docstrings / Source Index / References / QA,
  or kept terse only where the sheet is itself an audit/validation/source context (the
  guide's standing exception).
- **Lint tool: skip.** No new judging tool and no build-time gate (respects the standing
  "no optional lints — the probe stays a read-only inspector" decision). Verification ran
  through the existing read-only `sheet_probe` + a throwaway oracle + the workbook's own
  QA Reconciliation / Number Audit tabs. The throwaway oracle was deleted at the end.
- **Layout cursor: local copy-from.** A `RowCursor` adapted from the
  `sheet_snippets.md` snippet lives **inside `workbook_sub`** (`sheets/_layout.py`), not
  promoted into the shared engine (respects the "snippets stay copy-from" principle).

---

## 1. The local cursor — `workbook_sub/sheets/_layout.py` (the one new file)

A `RowCursor` (`at/banner/write/total/blank/feed`) where every emit returns the row it
wrote, so a producer captures load-bearing positions straight from the writing call —
making the safety invariant ("the accessor row derives from the same value used to write
the row") structural, with no second literal to drift. Two extensions beyond the snippet:
`total()` (passthrough to `total_row()` with base styles) and **callable values** —
a `lambda r: …` in the values list is resolved against the row just assigned, which is how
self-referential formulas (`=C{r}+D{r}`, `=SUM(C{r}:H{r})`, `=IF(ABS(F{r})…)`) are written
without a hardcoded row.

**Accessor-safety architecture (the crux).** Producer modules expose cell-ref accessors
that consumers call during their own render, so positions must resolve at *import* time,
not render time. Pattern used:
- **Producers** build a body at import via the cursor, capture every accessor-backing row
  into a dict, and promote module-level accessors that read it. (7 producers already used
  an offset-arithmetic `_build_*` pass; the two holdouts — `assumptions_controls`,
  `sam_build` — were converted from hand-numbered `_R_* = <literal>` constants to this
  captured-position pattern.)
- **Consumer-only sheets** (`executive_summary`, `methodology_scope`, `sensitivity`,
  `worktype_evidence`) use a fully render-local cursor.
- **At-a-glance wrappers** are built *after* the body (so they can reference promoted
  accessors) and spliced above it via `feed()`; an `assert c.at() == _BASE` guards the
  hand-set base against drift.
- The `assumptions_controls ↔ sam_build` cycle stays broken: A&C's §4 selector row is the
  one piece built at **render** time via a lazy `import sam_build`, spliced into the
  import-built body by row number.

---

## 2. What changed on every sheet (the global passes)

- **§N numbering.** Every non-title banner is now `§N - Title` / `§Na - Title`, sequential
  per sheet. Three-tier banner nests (scn_annual, lltm_ap) were flattened to the legal
  two levels (promoting the middle tier to sections, dropping redundant wrappers).
- **Spacing rhythm.** 1 blank after a section/subsection banner; 2 blanks between a
  section's last content and the next section banner — encoded as `c.blank()` / `c.blank(2)`.
- **Native table style.** Dropped `style="TableStyleLight1", show_row_stripes=False` from
  all 8 `ExcelTable(...)` (10 tables) → they take the `WorkbookCore_NoFormatTable` default.
- **Centered headers.** Numeric / FY / count column headers → `S_HEADER_CENTER`; text and
  mixed "Value" headers stay `S_HEADER_LEFT`. (`build_table` broadcasts one header style,
  so its all-text headers in `location_master` / `source_index` stay LEFT.)
- **Green-link discipline.** Derived multi-ref sums reclassified green→black: exec-summary
  `_bc_tam_sum`/`_ap_tam_sum`, `sam_build` portfolio-TAM sum, `entity_master`
  prime+co-prime, `scn_annual` per-FY portfolio cells. Single producer-cell displays stay
  green. (Audit was directionally right; several flagged cases were already correct.)
- **total_row().** Hand-built dividers converted to `cursor.total()` with **base** styles:
  `mib_excluded` (1), `lltm_ap` (2), exec-summary §4 total. `entity_master` / `sam_build`
  switched from pre-bordered `S_NUM_TOTAL`/`S_PCT_TOTAL` to base styles. (Note: `total_row`
  upgrades base styles idempotently, so passing a base like `S_LINK_PCT` was already
  correct — only the already-bordered variants were the real fix.)
- **Round-integer metadata → S_DEFAULT.** A&C FY years 2022/2027 (kept the integer, so
  `C8-C7+1` still evaluates), entity/MIB/worktype counts, figure/coverage counts. Real
  analytical inputs (dollars, %, coefficients, adjustments, anchors) stay `S_NUM_INPUT`.
- **Indentation.** Leading-space fake-indent removed (pop_source_audit, location_master);
  `S_LABEL_INDENT_1` applied to true component rows (the AP/LLTM bridge "less …" steps in
  `lltm_ap` and `executive_summary`).
- **Prose / widths (aggressive).** Standalone narrative sections relocated to docstrings
  (lltm_ap conclusion, A&C changelog, pop_source_audit protocol, mib rationale/tie-outs,
  number_audit basis, parse notes, coefficient-feed); Note/Basis/Rationale/Treatment
  columns dropped from model blocks; every >44 column brought into range (Sources sheets
  shortened but allowed to run a little wider).

---

## 3. Critical bug fixed — `worktype_evidence` row collision

The at-a-glance wrote bucket rows 6–12 then the unbucketed row at row 13, while
`_BASE = 13` put the evidence section banner on the same row 13 (banner style over live
formulas). The module is a pure consumer, so it was rewritten with a single render-local
cursor — the evidence block is now `blank(2)`-positioned after the at-a-glance, making
the collision structurally impossible (every emit advances the row).

---

## 4. Verification

After each module: rebuild + a read-only probe-based oracle checking that the
dangling-reference count stayed **0** (the signature of an accessor desynced by a row
shift — a producer's accessor pointing past the end of, or outside the used box of, its
sheet). It held at 0 through all 19 conversions, including both holdouts and `tam_build`
(the most-consumed accessor set). Final whole-workbook checks (all passed): 19 sheets /
group order / first tab / 10 no-format tables; 0 unnumbered banners; 0 banner→content
spacing violations; 0 <2-blank inter-section gaps; sequential §N per sheet; 0 leading-space
labels; 0 green-on-derived; 0 >44 columns outside Sources. The workbook's own QA
Reconciliation (12 checks) and Number Audit (registered-figure tie-out) formula chains all
reference valid cells.

**Remaining out-of-environment confirmation:** open the rebuilt `.xlsx` in Excel to confirm
`Number Audit` 0 FAIL / `QA Reconciliation` 0 FAIL evaluate numerically and that no cell
trips a repair dialog. The chains are structurally intact and the identities hold by
construction, so they should evaluate clean.

---

## 5. Files changed this session

- **Added:** `workbook_sub/sheets/_layout.py` (local `RowCursor`).
- **Rewritten:** all 19 sheet modules under `workbook_sub/sheets/` (executive_summary,
  methodology_scope, assumptions_controls, tam_build, sam_build, scn_annual, lltm_ap,
  pop_location_parse, pop_source_audit, entity_master, location_master, worktype_evidence,
  figure_register, mib_excluded, sensitivity, number_audit, qa_reconciliation,
  source_index, references). `taxonomy.py` (non-sheet helper) untouched.
- **Rebuilt artifact:** `20260601_Distributed Shipbuilding Submarines_vS.xlsx`.
- **Not touched:** any `core/workbook_core/` engine file; DDG.
- **This log.**

---

## 6. Follow-ups

- **Open in Excel** for the numeric tie-out (§4 above).
- **The deck pipeline** can now point at the stable defined names / producer cells
  (`portfolio_tam`, `bc_supplier_coeff`, `ap_lltm_supplier_coeff`, `sam_broad`) — unchanged
  by this pass.
- **DDG** still needs both the earlier group-reorder refactor and this styling pass; its
  build remains broken by the 2026-06-02 group reorder.
