# 2026-06-03 — Workbook cross-deck standardization: tab renames, new chartdata group, Note/Basis column strip + native-note re-anchor

## Scope

Standardized the two workbooks (`projects/ddg/workbook`, `projects/submarines/workbook`) against `workbook_core` and against each other, in four threads:

1. **Tab names** — make analogous tabs identical across both decks.
2. **Groups / colors / order** — add a dedicated last group for the chart-data loader.
3. **Note/Basis columns** — enforce the guide as written: strip the visible `Label | Value | Note`/`Basis` commentary columns from model/inputs/data/validation blocks (Sources keeps its one context note); relabel any column that is genuine data but mislabeled.
4. **Native Excel notes** — keep, but anchor each on the value cell it explains (off the label col in DDG, off the note col in subs), text concise/analyst-voiced.

Worked in 6 phases. This log covers Phases 1–4 (Phase 4 left at 2 subs sheets remaining); Phases 5 (specs) and 6 (final verification) are not started. Full continuation detail is in `docs/2026-06-03_workbook_standardization_HANDOFF.md`. Workspace is **not** under git and has no backup (a tar was made then deleted per direction); every change was followed by a rebuild.

Key decisions (from the user): strip the Note/Basis columns (don't bless them); full rename cascade (`_TAB` + module `.py` + spec `.md` + imports + registry); analogous tabs get identical names; `z_ChartData` kept (not "Chart Data"), moved to its own last group; `Methodology`/`Assumptions` (not the longer "& Scope"/"& Controls"); mislabeled-but-real-data columns get **relabeled** not stripped; core files stay domain-generic.

---

## 1. Core foundation (`workbook_core/`)

- **`groups.py`** — added `("chartdata", "Chart data", "404040")` (charcoal) as the **last** group in `SHEET_GROUPS`, plus docstring/reader-flow updates. The build's group-contiguity assertion now lets each deck park its `z_ChartData` loader tab last in its own color.
- **`sheet_guide.md`** — rewrote the "Native Excel Notes" paragraph: anchor a note on the **value/headline cell it explains, never a label or a note column**; concise/analyst-voiced. Added `chartdata` to the Groups & tab-colors list. (The "no note columns except Sources" rule already existed; we now enforce it rather than amend it.)
- **`sheet_snippets.md`** — removed the `Note` column from the row-cursor/section worked examples (they were teaching the now-banned pattern); native-note snippet now anchors on the value cell.

All core insertions are domain-generic (no DDG/submarine/TAM specifics), keeping the engine reusable.

## 2. DDG rename cascade (built green)

Ran a deterministic script (`/tmp/ddg_cascade.py`): renamed 10 modules, updated each module's `_TAB`/`_GROUP`/SheetEntry constant/docstring, rewrote dotted `sheets.<mod>` imports across the package, then hand-wrote `sheets/__init__.py` with the new tab order (z_ChartData last, in `chartdata`). Renames: Inputs→Assumptions, Entities→Entity Master, Locations→Location Master, Bucket Evidence→Worktype Evidence, Deck Outputs→Figure Register, Figure Audit→Number Audit, QA Checks→QA Reconciliation, POP Audit→POP Source Audit, Source Lineage→Source Index, z_ChartData (group outputs→chartdata). Verified the 24-tab order/group/color.

## 3. Submarines rename cascade (built green)

Same approach (`/tmp/sub_cascade.py`): Assumptions & Controls→Assumptions, Methodology & Scope→Methodology, SCN Annual→SCN Budget, LLTM AP→AP Bridge, POP Location Parse→POP Corpus, POP Source Audit (group **data→validation**, so it now sits with the other audits), Chart Data→z_ChartData (group→chartdata, last). Hand-wrote `__init__.py`.

**Bug caught + fixed:** the cascade rewrote only the dotted import form (`sheets.<mod>`); the package-level form `from workbook_submarines.sheets import <mod> as _x` was missed and broke the build (circular-import error). Fixed by hand in `model_sam_build.py` (`inputs_assumptions`) and `validation_pop_source_audit.py` (`data_pop_corpus`). Lesson for future renames: grep **both** `sheets\.<old>` and `sheets import <old>`. Verified the 21-tab order.

## 4. Note/Basis column strip + native-note re-anchor

The recurring rule:
- **Strip** prose-commentary `Note`/`Basis` columns on curated model/summary/coefficient/check blocks (header + every data row + matching style; `c.total(...,n_cols=N)`→N−1). The commentary col is always rightmost, so cols B/C don't shift and formulas stay valid.
- **Keep + relabel** columns that are genuine data but mislabeled: classification `Basis`→`Arbiter`, crosswalk `Basis`→`Rationale`; left real `Method`/`Source`/`Interpretation`/`Class rule` columns alone.
- **Leave** wide native data tables, FY matrices, prose "Caveats" sections, and the `z_ChartData` deck-loader sheet (the PowerPoint pipeline reads it).
- **Re-anchor** every `ExcelNote` from the label col (B, DDG) or the note col (D/E, subs) to the row's **value cell** (usually C); keep the analyst-grade wording; fix stale renamed-tab references in note/Source text (e.g. subs summary `LLTM AP`→`AP Bridge`).

`model_tam_build` (both decks) had a `line(key,label,value,basis,…)` helper feeding ~16 coefficient rows — changed the helper **body** to write `[label, value]` and kept `basis` as a defaulted/ignored param, so all call-sites stayed untouched.

Execution: column-only sheets (no notes) were fanned out to parallel sub-agents with a precise spec + the `data_ap_bridge` exemplar; note-bearing sheets were done directly (DDG) or by sub-agents constrained to keep note wording (subs). 

**DDG: complete** — built green; all 13 native-note anchors on col C/D (none on B); no residual commentary headers (kept data cols: `Source`, `Arbiter`, `Reason`, `Rationale`, `Interpretation`; chartdata loader untouched). Notable: `summary` kept `Source`+`Interpretation` and dropped a redundant FFATA note; `validation_sensitivity` dropped an orphan FFATA memo row and trimmed to `cols=[44,14]`; `pop_source_audit` trimmed to `cols=[44,12,12]`.

**Submarines: ~85%** — column-only sheets + 5 note-bearing sheets done (`data_ap_bridge` relabel Basis→Rationale, `inputs_assumptions`, `model_tam_build`, `summary_executive_summary` (fixed `LLTM AP`→`AP Bridge` in Source col), `validation_sib_excluded`); `validation_sensitivity` already clean (notes on C, no Note cols).

---

## Verification (at handoff)

| Check | Result |
|---|---|
| DDG build | exit 0 — 24 tabs, 12 native tables, 6 note parts |
| Submarines build | exit 0 — 21 tabs, 12 native tables, 8 note parts |
| z_ChartData | last tab, group `chartdata`, color `404040`, both decks |
| POP Source Audit | in `validation` (gray) on both decks |
| DDG native-note anchors | 12× col C + 1× col D; **zero on col B** |
| DDG residual commentary `Note`/`Basis` headers | none (only relabeled/kept data columns remain) |

Audit gates (QA Reconciliation / Number Audit "0 FAIL") are runtime Excel formulas — **not** evaluated by the Python build; confirm in Excel / via `validate_workbook.py` during Phase 6. The Phase-4 edits touched no formula or value, so gates should be unaffected.

## Open items / remaining (see HANDOFF doc for line-level steps)

- **Phase 4 finish (2 subs sheets):** `guide_methodology.py` (strip §2 `Coefficient (live)|Value|Note` + §5a `Measure|$M|Note`; keep §3 `Method`; 4 glossary notes on C are fine) and `model_sam_build.py` (strip §9 `Check|Status|Note` + §1 `Measure|Value|Note`; re-anchor 2 notes `B`→`C`). The agents assigned these got confused by the shell cwd (DDG) and inspected the DDG copies instead of editing the subs files.
- **subs `chartdata_z_chart_data.py`** still has a `Measure|Value|Note` at-a-glance block — intentionally deferred (loader sheet left untouched, matching DDG); strip only that at-a-glance if strict consistency is wanted, never the deck tables.
- **Phase 5 — sheet specs (45 files):** rename to match new modules; update tab/group/color + Module lines; remove stale `Note column`/`Basis column` lines; update note anchors/text; subs `data_pop_source_audit.md` group data→validation; z_ChartData → chartdata/`404040`.
- **Phase 6 — final verification:** both builds green; tab counts; audit gates 0 FAIL in Excel; greps confirm no col-B note anchors and no stray commentary headers.
- **Scratch:** `/tmp/ddg_cascade.py`, `/tmp/sub_cascade.py` are the rename scripts (one-shot; already run).
