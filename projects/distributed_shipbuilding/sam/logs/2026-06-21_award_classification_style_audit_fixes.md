# 2026-06-21 — Award-Classification workbook: readability / house-style audit fixes

Session goal: implement an independent **style/readability audit** of the
`award_classification_refactor` workbook (the build was already correct; the audit found it
"technically strong but visibly over-explained"). Highest-value work was copy reduction and
removing implementation detail, not a restyle. All 8 audit areas implemented across 4 passes;
a new `tools/style_audit.py` linter now enforces the rules. Build is clean (**20 sheets, 0 XML
errors, 0 error-literal cells, 0 en/em dashes in any worksheet XML**); the headline math is
untouched.

## Pass 1 — structural consistency

- **Native outline controls surfaced.** `worksheet()` already had `show_outline_symbols`; set
  it `True` on every outlined sheet — `_flat.make_flat_sheet()` render + all 6 custom renderers
  (exec summary, domain/parent conc, market bridge, taxonomy, methodology, hii co-build). The
  gutter `x` stays as the house marker; Excel's real `+/-` controls now work. Row-2 title keeps
  no `x` (it is the sheet title, not an outline anchor).
- **Title / section numbering.** Market Bridge row-2 title is now `Market Bridge` (was the long
  "Illustrative cumulative…"). Domain Concentration `S1/S2/S3` → `§1/§2/§3`; HII Co-Build
  `S1..S6` → `§1..§6`. Methodology cross-ref `Taxonomy §5` → `§4` (the SWBS legend is Taxonomy §4).
- **Duplicate-Report Audit moved `data` → `validation`** (gray tab; still sorts last).
- **Helper columns hidden.** New engine support: `worksheet(cols=[{"width":w,"hidden":True}…])`
  + `make_flat_sheet(hidden_headers=…)` keep a formula-helper column in the grid (A1 refs stay
  valid) but hide it from the reader. Hidden: `SM Match Row` (program vendors), `Override/NAICS
  Map Match Row` + composite `Key` (Supplier Master), `Key` (Overrides), `SWBS Match Row` (DDG tx).

## Pass 2 — copy reduction

- **All 20 row-3 captions** replaced with the audit's compact versions (8–18 words, <120 chars).
  Dropped the data-derived `cy_span(...)` from the program-vendor / transaction captions (the
  detail lives in Methodology now).
- **Methodology rewritten to six sections** — `§1 Scope and grain … §6 Coverage and QA`. Stripped
  all pipeline narration (`scope_status`, `prime_contract_scope.csv`, `include=Y/N`, "The build
  fails unless…", "reviewer finding", "re-baseline (REMOVE)", the dated decision, "locked as
  observed-in-this-pull"). The PIID scope is now one clean rule: *"Only Basic Construction prime
  contracts are included. Design, lead-yard support, ship alteration, planning-yard work, GFE
  primes and MIB pass-throughs are excluded."*
- **HII Co-Build de-LLM-ed.** Removed "two procurement games", "you don't win this by being a good
  sub", all-caps emphasis (OWN/NOT/EXCLUDE/TENS OF BILLIONS/DERIVED), the `=>`/`<--` arrows, and
  the machine labels → reader-facing `Ceiling` / `Incremental modification` / `Cumulative disclosed
  value`. "DO NOT SUM this column-wise" moved into a hover **Note** on the *Cumulative $M* header;
  numeric blanks are `None` (not `"-"`).
- **Market Bridge simplified.** Title = tab; removed the `Other modeled reporting gaps` placeholder
  row and the leading `=` on the total label; `->` → plain words; leading-space indent →
  `S_LABEL_INDENT_1`; the long derivation prose became a compact (Component, Basis) table. Row
  labels: `Virginia co-build workshare` / `Less reported HII-NNS overlap` / `Columbia co-build
  workshare` / `Estimated cumulative outsourced / co-build total`.
- **Domain Concentration** uses neutral tiers — `Highly concentrated` / `Concentrated` /
  `Contestable` (the "fortress" metaphor is gone, label + intro + caveat).
- **Executive Summary** scope block cut to three neutral lines; removed "fortress", "Critical for
  submarines", "live figure", "unexplained reporting/data-treatment gap", "not a clean teaming
  carve-out", and an all-caps "NOT".
- Shared `_taxonomy.py` swept of reader-facing `->` arrows (→ "to" / plain words) and the
  "version it / re-validate on new pulls" guardrail narration.

## Pass 3 — visual tightening

- `_widths.py` retuned: `W_TEXT` 46→35, `W_TEXT_WIDE` 64→42, `W_VENDOR` 34→31, `W_NAME` 30→27,
  `W_NAICS_DESC` 34→31, `W_UUID` 38→31, `W_CONTRACTKEY` 42→34.
- Sheet-specific: Taxonomy `[7,42,86]`→`[8,34,58]`; Exec Summary first col 50→44; Methodology
  `[26,46,40,20]`→`[24,40,32,16]`; Market Bridge → `[36,34,12,12,12,9,9]`; HII Co-Build → `[24,12,12,14,18,38]`.
- **Display-header aliases** (new `make_flat_sheet(display_headers=…)`): the program-vendor sheets
  show `Records`, `Primary location`, `Domain (D)`, `Domain basis`, `Output (P)`, `Output basis`
  while formulas/accessors keep the canonical names (cross-sheet refs unaffected).

## Pass 4 — dashes + regression linter

- **`normalize_dashes=True`** at the build level. Root-caused a subtlety: the flat sheets build
  their cell XML **eagerly at import**, so the switch must be set *before* the sheet modules import
  — `lib.build()` now calls `set_normalize_dashes(True)` ahead of the `SHEETS` import (package-level
  flag alone was too late). DDG `SWBS basis` formula literals fixed at source (`na="-"`,
  `unmapped="U - no SWBS evidence"`). Result: **0 en/em dashes in any worksheet XML.**
- **New `tools/style_audit.py`** (openpyxl reader, like `validate_workbook.py`; honors `WB_OUT`).
  Hard-fails on: B2 ≠ tab, a section banner not matching `^§\d+[a-z]? - .+`, a gutter `x` without
  outlined detail (and vice-versa), any en/em dash in a literal/formula, a forbidden helper header
  left visible, an invalid cross-ref (`Taxonomy §5`). Warns on: caption >120, section title >60,
  visible column >44 (Taxonomy def col allowlisted), leading-space prose, implementation terms.
  Caught 15 real dash failures + the spacer-column false positives during development; now reports
  **0 hard failures / 0 warnings**.

## Build / verify

```
python3 build_workbook.py        # 5 data guards run, then packages (normalize on)
python3 validate_workbook.py     # 20 sheets, 0 XML errors, 0 error-literal cells
python3 tools/style_audit.py     # 0 hard failures, 0 warnings
```

Spot-checked: every B2 == tab name; Market Bridge bridge math intact (observed nominal subtotal +
co-build, FY2026$ memo, total `=D12+SUM(D17:D19)`); Exec Summary §2 program totals still
`=SUM('… Program Vendors'!$I…)`; hidden cols + `showOutlineSymbols=1` present. Headline unchanged
($12.08B nominal / $13.88B FY2026$).

## Files

- **New:** `tools/style_audit.py`.
- **Engine:** `workbook_core/primitives.py` (`worksheet` cols accept `{width,hidden}`),
  `sheets/_flat.py` (`hidden_headers` + `display_headers` + `show_outline_symbols=True`),
  `lib.py` (`normalize_dashes=True` + early `set_normalize_dashes`).
- **Sheets:** `guide_methodology.py` (rewrite), `hii_co_build.py` (rewrite), `market_bridge.py`
  (rewrite), `executive_summary.py`, `domain_concentration.py`, `taxonomy.py`, `_taxonomy.py`,
  `_widths.py`, `_program_vendors.py`, `supplier_master.py`, `vendor_archetype_overrides.py`,
  `ddg/virginia/columbia_program_vendors.py`, `ddg/virginia/columbia_subaward_transactions.py`,
  `ddg_swbs_rollup.py`, `hii_swbs_crosswalk.py`, `deflators.py`, `naics6_archetype_map.py`,
  `parent_concentration.py`, `duplicate_audit.py`, `sheets/__init__.py`; regenerated
  `award_classification_refactor.xlsx`.

## Carry-forward

- **Nothing committed** — staged in the working tree only; commit when ready.
- `normalize_dashes` only affects **literal text**; formula strings bypass it, so a dash in a new
  formula must be fixed at source — `tools/style_audit.py` will catch it on the next build.
- `cy_span` / `cy_span_union` in `_cuts.py` are now unused (captions no longer embed the span);
  left in place as reusable helpers.
- Not verified headless beyond formula structure — open in Excel/LibreOffice, force a recalc, and
  confirm the headline + 100% Primary-Output matrices, and that the native outline `+/-` controls
  now collapse the sections.

---

## Follow-up (2026-06-22) — Parent Concentration made LIVE

The Parent Concentration sheet was the one analytical tab still **baked from a Python script**
(`scripts/build_parent_concentration.py` → `extracted/parent_concentration.csv`) while its sibling
Domain Concentration computes live. Converted it to live formulas.

- **Blocker** was the parent grain: a parent spans multiple UEI rows, so a flat SUMIFS can't group
  by parent. **Fix:** three hidden per-row helper columns on the program-vendor sheets
  (`_program_vendors.py`) — `Parent Key` (parent UEI, else self), `Parent Domain $` (that parent's
  positive FY2026$ within the row's domain), `Parent Domain Rows` (positive rows sharing
  parent+domain, `MAX(1,…)`-guarded). They turn the per-parent grouping into one value per row.
- `parent_concentration.py` rewritten as a **custom live renderer** (like `domain_concentration.py`):
  UEI grain = `MAXIFS/SUMPRODUCT/COUNTIFS` over per-UEI `Subaward $M`; parent grain = the same
  shapes over the helpers — Parent Top-1 `MAXIFS(Parent Domain $)`, Parent HHI
  `SUMPRODUCT(M, Parent Domain $)/pos²` (= Σ parentTotal²), distinct Parent Firms
  `SUMPRODUCT(1/Parent Domain Rows)`. One §-section per program, all 12 domains.
- **Verified** by replicating the exact Excel formula semantics in Python and diffing against the
  script's validated CSV: **0 mismatches across all 36 (program × domain) rows.** The helpers'
  same-sheet ranges are guarded against layout drift (`cols.first/last == 9 / 8+nrows`).
- `build_parent_concentration.py` + its CSV are now vestigial (kept as an offline cross-check;
  the workbook no longer reads the CSV). Build/validate/style-audit remain green (now **13** native
  tables — Parent Concentration is no longer a flat table).
