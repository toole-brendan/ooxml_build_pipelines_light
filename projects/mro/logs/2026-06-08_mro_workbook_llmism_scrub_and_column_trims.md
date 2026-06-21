# 2026-06-08 — MRO workbook LLM-ism scrub + editorial-column deletions

## Scope

Third presentation pass on the MRO workbook sheet modules
(`projects/mro/workbook/workbook_mro/sheets/`), bringing them fully into the gold
`workbook_submarines` / `workbook_ddg` idiom by removing the remaining **LLM-isms** measured
against the canonical style contract `workbook_core/sheet_guide.md`, then a follow-on round of
**editorial-column deletions** the user called out. Two prior 06-08 passes (styling hardening,
prose-column removal) had already fixed the `c.total()` / `S_HEADER_*` / `S_LINK_*` mechanics
and dropped the per-row prose-provenance columns; this pass finishes the job.

**Every edit is presentation/text only — no model/value change.** All gates stayed green with
**no `regen-baseline`**: `build_workbook.py` → 18 sheets, 0 defined names; `qa/verify_crosstab.py`
→ OK (4,290 formulas); `qa/tie_out.py compare … --tol 1.0` → **Invariant B (86 figures) +
Invariant A (engine multiset) both match** at every checkpoint (baseline, post-scrub,
post-column-deletions). Workbook size 7,371,013 → 7,366,347 bytes (net of removed prose/columns).

## Why this is value-neutral (same safety model as the prior 06-08 passes)

- **Deleting a prose row / a text column** removes only *text* cells (no numeric `<c>`), so
  Invariant A (relocation-proof numeric multiset over the 9 engine tabs) is unchanged. Numbers
  that appeared *inside* prose strings (`$120M`, `$2,392.190M`) were never numeric cells.
- **Row/column shifts** are absorbed: producer accessors capture cursor-relative positions and
  recompute, so Invariant B re-validates the 86 figures automatically; a missed update fails B
  loudly. All deleted columns were either the **last** column of their table or on **non-engine,
  non-accessor** tabs (summary / guide / inputs), so nothing shifted a producer cell.
- **Banner / check-text rewording, docstring/comment edits, and `S_NUM → S_LINK_NUM` recolor**
  change no numeric cell at all.

## Part 1 — LLM-ism scrub

### Calc-grid prose deleted (the real rendered LLM-isms)

User decision: **delete outright** (the load-bearing facts already live in `guide_methodology`
§5/§6/§7 and `sources_references`), not relocate to native Notes.

- **`model_msc_scn_uscg_topdown.py`** — deleted the 4 `_note()` section-intro paragraphs and the
  3 bold editorial rows (`CAVEAT` USCG-undercount, `CROSS-CHECK` OPN, `NO DOUBLE-COUNT`); removed
  the now-unused `_note` helper; reworded §3 banner `(confidence = LOW)` → plain.
- **`validation_scope_reconciliation.py`** — deleted all ~7 `_note()` prose blocks (§5 rebase
  narration, §6 addback, §10 paste instructions, §11 matrix commentary ×3); removed `_note`.

### Section banners → gold `§N - <noun phrase>`

`validation_scope` §2–§13 banners reworded: dropped the `Top-down:`/`Derived:`/`Intermediate:`/
`Final:` prefixes, the parentheticals, and the `[BAR n]` suffixes
(e.g. `"§2 - Top-down: OMN ship-maintenance budget authority  [BAR 1]"` → `"§2 - OMN
ship-maintenance budget authority"`). Bar identity is still carried by the §1 map, the `BAR n`
row labels, and §10/§12.

### Hedged / stale check text reworded

`validation_scope` §5/§12/§13 check descriptions: dropped the hedge word "should" and the
**dropped** defined-name identifiers (the Phase-4 names no longer exist) — e.g.
`"… should equal MRO_TAS_TOTAL_FY25 / 1000"` → `"TAS total (pre-rebase)"`;
`"… NAVY_TAM_SVC+CG_TAM_SVC = Services TAM"` → `"… (post-rebase = Services TAM)"`;
`"RECONCILED_MRO_TAM = Services + PSC 1905"` → `"(Services + PSC 1905 embedded)"`. Formulas
unchanged. Also reworded the one stale rendered chart label in `chartdata_output.py`
(`"Cumulative % of RECONCILED_MRO_TAM …"` → `"… Reconciled MRO TAM …"`).

### Cross-sheet link recolor (finished the deferred item)

Added a `link=` flag to `validation_scope`'s `_vrow` helper (the helper hardcoding one value
style was exactly why the prior pass deferred this), then applied `S_LINK_NUM` (green) to the
**single-source** cross-sheet pulls — bare accessors AND single-accessor `/1000` unit rescales
(§2/§3/§5-pre/§7/§8/§11/§13) — leaving multi-source / derived / bar rows black `S_NUM`. This
matches the established workbook convention already used by `tam_bridge`, `private_addressable`,
and `verification` (confirmed by reading them): **green = the cell's value is one upstream
figure; black = computed here.**

### Source hygiene (the `.py` reads hand-authored now)

- **Decorative comment dividers** — normalized every `# ---- §N … ----` box and `model_services`'
  full-rule `# -----` sandwiches to plain `# §N …` via a one-off comment-only script
  (`/tmp/scrub_dividers.py`, dry-run-previewed; comment-only so the build/tie-out backstop any
  over-match). ~60 lines across 11 modules.
- **Docstrings → terse gold form** — stripped migration meta-commentary ("Native producer/consumer
  (gold idiom)", "Phase 0-4", "v4.33 grid … byte-for-byte", "ships NO/ZERO defined names",
  "re-authored from reflow", "18-sheet port") from `__init__`, `_crosstab`, `model_services`,
  `model_reconciliation`, `model_depot_ship_repair`, `model_op5_navy_topdown`,
  `model_private_addressable`, `model_tam_bridge`, `summary_verification_answers`,
  `chartdata_output`, `data_awards`, `data_j998_j999`, `outputs_figure_register`, while keeping
  the factual intent + layout + load-bearing invariants (cycle-break note, `_ref` resolver, etc.).
- **Fixed a stale claim**: `model_reconciliation` docstring said "Services reaches it by bare name,
  no import" — false since Phase 4 (Services imports the accessors at module load). Reworded to
  the accurate cycle-break description.

### Methodology de-hedge (light touch — the sanctioned prose tab)

`guide_methodology.py`: dropped the migration sentence from the docstring; de-jargoned the §7
Basis cell ("byte-for-byte SUMIFS" → "SUMIFS over the 65 PSCs"); **removed the 3 conversational
`ExcelNote`s** (and the unused `ExcelNote` import + `_dn` plumbing) — they restated the adjacent
Treatment column / §2 tables ("What a private competitor could actually win…", `~$9B`/`~$17B`).

## Part 2 — editorial-column deletions (user-requested)

All value-neutral; tabs are non-engine so gates unaffected.

- **`summary_verification_answers.py`** — deleted the **Benchmark / Expected** column (col E):
  `_NCOLS 4→3`, `_COLS [42,14,10,22]→[42,14,10]`, header/HSTYLE trimmed, and the 4th value+style
  dropped from every §1–§6 row/total.
- **`guide_methodology.py`** — deleted **§3 "Output tab"**, **§1 Definitions "Treatment"**, and
  **§5 Exclusion-rules "Treatment"** (user chose §1+§5 via AskUserQuestion; **kept §6 "MRO
  treatment"** — load-bearing no-double-count content). Widest table is now 3 cols → `_NCOLS 4→3`,
  `cols [26,46,40,22]→[26,46,40]`.
- **`inputs_assumptions.py`** — deleted the §1 **Notes** column and the §2 **Where consumed**
  column (both the last/D column; accessors are on col C, so unshifted): `_NCOLS 3→2`,
  `_COLS [38,14,36]→[38,14]`. Data validations (on col C) intact.

## Verification (final, all green)

```
cd projects/mro/workbook
/usr/bin/python3 build_workbook.py            # 18 sheets, 0 defined names, 8 native tables
/usr/bin/python3 qa/verify_crosstab.py        # CROSSTAB VERIFY OK (4,290 formulas)
/usr/bin/python3 qa/tie_out.py compare qa/gold/baseline.json \
    "../20260607_Navy USCG Vessel MRO Spend_vS.xlsx" --tol 1.0
# -> TIE-OUT OK — Invariant B: 86 figures match; Invariant A: engine multiset matches
```

Grep sweeps clean: no `_note(`/`CAVEAT`/`CROSS-CHECK` in model/validation; no `# ----`/`# ====`
dividers; no `gold idiom`/`Phase N`/`Native producer|consumer`/`byte-for-byte`/`ships NO|ZERO
defined`/`re-authored`; no `should equal` or dropped-defined-name strings in visible cell text;
deleted column headers (`Benchmark / Expected`, `Output tab`, `Where consumed`, inputs `Notes`,
both `Treatment`) gone.

## Files touched

Rewritten/edited: `__init__.py`, `_crosstab.py`, `guide_methodology.py`, `inputs_assumptions.py`,
`model_msc_scn_uscg_topdown.py`, `model_op5_navy_topdown.py`, `model_services.py`,
`model_reconciliation.py`, `model_depot_ship_repair.py`, `model_tam_bridge.py`,
`model_private_addressable.py`, `validation_scope_reconciliation.py`,
`summary_verification_answers.py`, `chartdata_output.py`, `outputs_figure_register.py`,
`data_awards.py`, `data_j998_j999.py`. No QA/baseline files changed (presentation-only).

## Not done / minor remaining

- **`model_private_addressable.py` §1/§2/§3 banners** still use `Derivation A:` / `Derivation B:`
  prefixes + parentheticals (`"§1 - Derivation A: bottom-up ($9B FPDS universe)"`,
  `"§3 - Convergence (target: both within $500M)"`) — not strictly the gold `§N - <noun phrase>`
  form. Left as-is this pass (not flagged by the user); reword if a stricter banner sweep is wanted.
- `guide_methodology` §1 Definitions / §5 Exclusion-rules `treat` strings were removed from the
  source tuples entirely (not retained as unrendered `_`), since they were editorial fluff the
  user wanted gone.
