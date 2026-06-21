# 2026-06-08 — MRO workbook LLM-ism scrub (pass 4): green-link semantics, banners, docstrings

## Scope

Fourth presentation pass on the MRO workbook sheet modules
(`projects/mro/workbook/workbook_mro/sheets/`), executing a user-specified two-layer
cleanup — **visible workbook output first, then source-only scaffolding** — measured
against `workbook_core/sheet_guide.md`. Prior 06-08 passes had fixed `c.total()`
mechanics, dropped prose-provenance columns, and done a first LLM-ism sweep; this pass
finishes the job: green-link styling semantics, narrative banner shortening, residual
editorial-cell text, the last leading-space fake-indents, and module
docstrings/registry/helper comments.

**Every edit is presentation/style/source text only — no model/value change.** All
gates green with **no `regen-baseline`**: `build_workbook.py` → 18 sheets, **0 defined
names**, 8 native tables; `qa/verify_crosstab.py` → OK (4,290 formulas);
`qa/tie_out.py compare … --tol 1.0` → **Invariant B (86 figures) + Invariant A (engine
multiset) both match**. Workbook 7,366,347 → 7,364,289 bytes.

## Why value-neutral (safety model)

- **Style recolors** (`S_LINK_NUM`→`S_NUM`) change a font color only; tie-out reads
  numeric *values*, never styles → can't move a figure.
- **Label/banner/docstring text** edits touch no numeric `<c>` → Invariant A (numeric
  multiset over the 9 engine tabs, incl. `Output`) is unchanged.
- **Text-only row/section deletions** (Services §11 "Takeaway", OP-5 §4 prose) remove no
  numeric cells; Invariant A is relocation-proof and the producer accessors capture
  cursor-relative positions, so the row shift re-validates automatically under Invariant B.
- **`Output` (chartdata) is an engine tab** — so chartdata cleanup was held to **text
  only** (no numeric reference rows deleted); the §5 narrowing-path rows were kept (their
  `%`/`$M` cells are in the multiset) and only relabeled / de-fake-indented.

## P0 — green-link styling (the load-bearing semantic fix)

Guide rule: green `S_LINK_*` is for a **pure** `=Sheet!Cell` link only; a formula that
scales/adds/subtracts/wraps a cross-sheet ref is **derived → black `S_NUM`/`S_PCT`**.
Recolored every `=accessor()/1000`, `=-accessor()/1000`, `=a+b`, and `/1000`-in-loop cell
to `S_NUM`, leaving bare `=accessor()` pulls green:

- **model_tam_bridge** — 6 `/1000` top-down pulls → `S_NUM`; bare `wpn`/`cg_tam` links stay green.
- **model_private_addressable** — `b_op5/b_msc/b_scn/b_opn/b_uscg` `/1000` + `b_pubnsy`
  `-…/1000` → `S_NUM`; bare `wpn`/`fms` links stay green.
- **validation_scope_reconciliation** — §2/§3 OMN SAG `/1000` rows (6), §5 pre-rebase
  `mro_tas/1000` loop col, §13.3/13.4/13.5 `/1000` checks → `S_NUM`; §4.1/§7/§8/§11 bare
  pulls stay green.
- **guide_methodology** — §2a `navy+cg` sum → `S_NUM` (added the `S_NUM` import); bare
  embedded/reconciled links stay green.
- **model_reconciliation** — deferred `RECONCILED_MRO_TAM` (`navy+cg+D…`) → `S_NUM`
  (dropped the now-unused `S_LINK_NUM` import).
- **summary_verification_answers** — §4 `uscg_isvs/1000`, §5 `op5_private/1000` → `S_NUM`;
  §1 bare `navy/cg` pulls stay green.

Verified in the built xlsx: TAM Bridge col-D `/1000` cells now `FF000000` (black), the bare
`='Assumptions'!C16` plug `FF008000` (green).

## P0 — delete "Use in model" from the raw data tabs

Removed the visible `§2 - Use in model` banner + "Services / TAM Bridge … SUMIFS against
'X'…" sentence from **data_awards / data_j998_j999 / data_psc_1905_classified**; each tab
is now just the §1 native table. Lineage already lives in Source Index / References.

## P1 — banners → `§N - noun phrase`

- **model_services** — stripped the `  --  slide "…"` deck-target suffix from §4/§5/§9/§10/
  §13/§14 and the editorial parentheticals from §6/§7; trimmed two subsection banners and
  the stale `(no defined name)` (also fixed it in the Reconciliation §2 sec row).
- **model_private_addressable** — `§1 Derivation A: bottom-up ($9B…)` → `§1 - Bottom-up
  addressable TAM`; `§2 Derivation B: top-down (…)` → `§2 - Top-down addressable TAM`;
  `§3 Convergence (target: …$500M)` → `§3 - Convergence`.
- **model_tam_bridge** — `§3 …(see Private Addressable sheet)` → `§3 - Private-addressable
  drop-through`; `TOTAL TOP-DOWN (Narrative B sum)` → `TOTAL TOP-DOWN`.
- **model_op5** — dropped `(contract-executable)` / `(federal civilian workforce)`
  parentheticals from §1/§2.
- data tabs / figure register — `§1 …(one row per…/one cross-sheet link…)` → terse `§1`.

## P1 — residual editorial cell text

`(critical test)`, `(structural scan result)`, `(reference, not pasted)`,
`(dominant gap component)`, `(plan Section 6.5)`, `LOW CONFIDENCE`, `(structural gap)`
removed from visible labels across validation_scope §10/§13, summary §4/§5, tam_bridge,
figure register S06 label, and Services §11. Deleted **OP-5 §4 "Source & confidence"**
prose section (redundant with Sources SRC-04 / Methodology §7) and the Services §11
"Takeaway: …; see Prime Landscape series and methodology notes." row. Removed the
**guide_methodology** standalone sentence rows (the §2a SUMIFS sentence, §2b "triangulated
…" intro + "…a STRUCTURAL gap, not an error.", §2c "Derived two ways …see Private
Addressable sheet."), keeping the formula-framework definition lines so §2 stays
table-first.

## P1 — leading-space fake indents → `S_LABEL_INDENT_1`

- **model_reconciliation §2** (BudgetAnchors) — the `"  of which …"` / `"  47-Foot…"`
  sub-band rows: detect leading whitespace, `lstrip()` the Line-Item text, apply
  `S_LABEL_INDENT_1`. Verified in the built xlsx: indent=1.0, no leading spaces.
  *(Note: §2 is a native ExcelTable; the guide nominally says native-table rows are flat,
  but these are genuine "of which" components of the SAG/total above them, so the indent is
  semantically correct and matches the guide's indentation section. Flagged for the user.)*
- **chartdata_output §5** — the `"  Depot share of TAM"` / `"  Marauder share…"` /
  `"  Independent-filter lower bound…"` narrowing-path rows similarly de-spaced + indented
  (added the `S_LABEL_INDENT_1` import).
- model_services already used `S_LABEL_INDENT_1` (its labels were flush) — unchanged.

## P2 — docstrings → INTENT / LAYOUT

Rewrote the migration-flavored docstrings (`the "X" tab (MRO, … one module = one sheet)`,
`Promoted accessors`, `mechanical deck-facing`, `pure consumer`, `reader-facing …QA page`)
to the gold `INTENT` / `LAYOUT` form across **data_awards, data_j998_j999,
data_psc_1905_classified, inputs_assumptions, outputs_figure_register, guide_methodology,
model_reconciliation, model_services, model_tam_bridge, model_private_addressable,
validation_scope_reconciliation, summary_verification_answers, chartdata_output,
sources_source_index, sources_references** — preserving the load-bearing notes (the
Reconciliation↔Services cycle break, the Services `_ref()` resolver, the green/black link
convention, header-stability / TEXT-column rules).

## P2 — chartdata scaffolding

Text-only (engine tab): stripped `(reference, not pasted)` / `(overlay line)` /
`(reference, chip styling)` / the verbose §12 total parenthetical / the §10
"(placeholder - structure only)" comment. Kept the `[chart_key]` block tags, terse section
names, and every numeric reference row (Invariant A).

## P3 — registry / helper trim

`sheets/__init__.py` — dropped the reader-flow narrative paragraph and the
"hand-authored RowCursor builder…" sentence; kept the tab-order/group-invariant note +
producer-first note; compacted the import-block group comments. `_layout.py` — trimmed the
long framework prose to the cursor's essentials (gutter, return-the-row safety invariant,
the callable self-reference pattern).

Also removed two now-unused imports (`S_LINK_NUM` in reconciliation, a pre-existing unused
`S_BOLD` in the psc_1905 data tab).

## Verification (final, all green)

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py            # 18 sheets, 0 defined names, 8 native tables
/usr/bin/python3 qa/verify_crosstab.py        # CROSSTAB VERIFY OK (4,290 formulas)
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0
# -> Invariant B: 86 figures match; Invariant A: engine multiset matches
```

Grep sweeps clean: no `reference, not pasted` / `overlay line` / `Use in model` /
`critical test` / `LOW CONFIDENCE` / `STRUCTURAL gap` / `no defined name` / `Takeaway:` in
visible cells; no `--  slide` / `(see …)` banner suffixes; no `one module = one sheet` /
`Promoted accessor` / `reader-facing` / `mechanical deck-facing` / `pure consumer`
docstring tells. (Remaining `(ref)` micro-tags on chartdata reference *columns* left as-is
— terse analyst annotation, not prose.)

## Not done / deliberate

- chartdata `§10 HII MT Financials` kept as an intentional structure-only paste block (its
  metric rows carry no numbers; the `[hii_financials]` block id is preserved for the deck
  loader).
- Sources context notes (e.g. SRC-09 "Confidence LOW on top-down") left intact — Sources is
  the guide's sanctioned one-line-context-note exception.
- The Reconciliation §1 "Line" provenance column (legacy-name lineage) left intact, as in
  prior passes — descriptive, numeric-free, no gate impact.
- The convention is recorded in memory `mro-workbook-styling-contract` (S_LINK_* only for
  single-source pulls; indent styles not leading spaces; no prose/editorial banners; terse
  INTENT/LAYOUT docstrings).
