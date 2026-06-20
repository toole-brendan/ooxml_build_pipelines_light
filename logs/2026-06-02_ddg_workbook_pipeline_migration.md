# 2026-06-02 — ddg_workbook pipeline: engine de-dup, relocation into core/, sheet migration

> ⚠ **Superseded names.** A later same-day restructure renamed the tree:
> `ddg_work`→`ddg`, `ddg_workbook`→`workbook`, `ddg_pptx`→`deck`,
> `destroyer_outsourced_work`→`research`. Prose paths in the body below use
> the **old** names; relative links still resolve (depth unchanged). The
> engine/import logic is unchanged. See
> [../../../logs/2026-06-02_core_tree_restructure.md](../../../logs/2026-06-02_core_tree_restructure.md).

> **Folder relocation note (read first).** As of this session, the entire
> `ddg_work/` tree was **moved** from `Documents\ddg_work\` to
> `Documents\core\ddg_work\`. This `logs/` folder had **no prior logs** —
> this is the first one written, and it post-dates the move. Guidance for
> anything that references the old location:
> - **Relative links resolve** (e.g. `../workbook_ddg/...`,
>   `../build_workbook.py`) because `logs/` moved together with the rest
>   of the tree.
> - **Absolute paths are now stale.** Any `C:\...\Documents\ddg_work\...`
>   reference (in external docs, plan files, or hard-coded strings) should
>   be read as `C:\...\Documents\core\ddg_work\...`.
> - The shared engine an older doc calls "the sibling `workbook_core`" is
>   **no longer vendored** inside the pipeline — see §2.
>
> This mirrors the submarine pipeline migration done the same day; see
> `core/sub_work/logs/2026-06-02_sub_workbook_pipeline_migration.md`.

## Scope

Applied the exact same fix to the **Destroyer Outsourced Construction**
workbook that was applied to the submarine workbook earlier today. The ddg
pipeline had the identical wrong setup: a stale, vendored copy of
`workbook_core` nested inside the pipeline was silently shadowing the
canonical `core/workbook_core`, so the workbook was building off the *old*
engine. This session: (1) proved the shadowing, (2) deleted the stale copy
and relocated the pipeline under `core/` so it imports the canonical
engine, (3) migrated the sheet modules, (4) verified with a clean build +
probe.

Final state: `python build_workbook.py` from
[../](../) (i.e. `core/ddg_work/ddg_workbook/`) produces the 10-sheet,
8-native-table workbook off `core/workbook_core`, with no vendored engine
copy anywhere in the pipeline.

---

## 1. Diagnosis — confirmed identical bug

The nested `ddg_work/ddg_workbook/workbook_core` was a **stale vendored
copy**, frozen Jun 1 11:55 — byte-for-byte the same old snapshot the
submarine pipeline had (same module sizes: `lib.py` 20,269; `primitives.py`
19,282; `styles.py` 14,364; `tables.py` 6,825; no `notes.py` / `ooxml.py`
/ `table_style_names.py`). Running the import the build runs (from
`ddg_workbook/`) resolved `workbook_core` to that nested copy — proving it
shadowed `core/workbook_core`.

`core/workbook_core` is the maintained source-of-truth that gets copied out
to each pipeline. (The maritime `refactoring_workbook/workbook_core` is a
*different* engine and is not a reference.)

---

## 2. Structural reorg — delete the shadow, relocate under core/

1. **Deleted** the stale vendored copy
   `ddg_work/ddg_workbook/workbook_core/` (kept `workbook_ddg`,
   `build_workbook.py`, `extracted/`, `logs/`, `validate_workbook.py`, and
   the output xlsx).
2. **Moved** the whole `ddg_work/` tree → `core/ddg_work/`.
3. **Repointed imports**: the pipeline now imports `core/workbook_core`
   directly. No local engine copy remains.

`sys.path` wiring lives in
[../workbook_ddg/\_\_init\_\_.py](../workbook_ddg/__init__.py): it puts the
project root (`ddg_workbook/`, so `workbook_ddg` resolves) and the repo
`core/` dir three levels up (so `workbook_core` resolves to
`core/workbook_core`) on the path. Verified the import resolves to
`core\workbook_core\__init__.py`.

Pre-move safety check: grepped for external hard-coded references to
`ddg_work` — only two planning docs matched (not runtime code), so the move
broke nothing outside the tree. `core/ddg_work` did not already exist.
Stale `__pycache__` under the moved tree was purged.

---

## 3. Sheet-module migration to the newer engine API

Same approach as the submarine pipeline: AST gap-check first to find every
`workbook_core.*` import the new engine doesn't export.

- **Gap-check result**: the **only** import-level incompatibility was
  `S_TITLE_SLIDE` (renamed to `S_TITLE_SHEET` in the newer `styles.py`).
  Everything else already resolved.
- **Applied the rename**: `S_TITLE_SLIDE` → `S_TITLE_SHEET`, **18
  occurrences across 8 sheet modules** (corpus 3; deck_audit 3;
  budget/guide/input/sam/source/tam 2 each).
- **Registry needed no change**:
  [../workbook_ddg/sheets/\_\_init\_\_.py](../workbook_ddg/sheets/__init__.py)
  already registers the `SheetEntry` objects (`METHODOLOGY`, `INPUTS`,
  `BUDGET`, `CORPUS`, `SUPPLIERS`, `TAM`, `SAM`, `DECK_OUTPUTS`, `AUDIT`,
  `SOURCES`) in canonical group order (guide → inputs → data → model →
  outputs → validation → sources).
- **Thin binding unchanged**:
  [../workbook_ddg/lib.py](../workbook_ddg/lib.py) stayed as the project
  binding (`OUT`, `EXTRACTED`, `SHEETS`, `package_workbook(...)`).

No runtime/signature mismatches — clean once `S_TITLE_SLIDE` was renamed.

---

## 4. Build + probe verification

From `core/ddg_work/ddg_workbook/`, `python build_workbook.py` succeeded:

| # | sheet | | # | sheet |
|---|-------|---|---|-------|
| 1 | Methodology | | 6 | TAM |
| 2 | Inputs | | 7 | SAM |
| 3 | Budget | | 8 | Deck_Outputs |
| 4 | Corpus | | 9 | Audit |
| 5 | Suppliers | | 10 | Sources |

- 10 sheets, **8 native tables**, ~80 KB output, passing the new packager's
  strict name/group/table/defined-name/notes validation.
- Zip integrity OK; 10 worksheet parts + 8 table parts + valid
  `workbook.xml` / `[Content_Types].xml`.
- `sheet_probe --all` wrote per-sheet md+json to
  `../workbook_ddg/reports/sheet_probe/`; problem-keyword scan clean. The
  probe ran **without** the `PYTHONUTF8=1` workaround — the UTF-8 encoding
  fix made to `core/workbook_core/tools/sheet_probe.py` in the submarine
  session is already in effect for ddg.

---

## 5. Notes / differences from the submarine migration

- **No `.claude/settings.local.json`** in this tree, so there were no stale
  permission paths to repoint (the submarine migration had three).
- **ddg's logs live deeper** — at `ddg_workbook/logs/` (this folder), not at
  the work-tree root like the submarine's `sub_work/logs/`.
- **`validate_workbook.py` left untouched.**
  [../validate_workbook.py](../validate_workbook.py) is a standalone
  openpyxl QA reader (not part of the build, no `workbook_core` import). It
  has a **pre-existing** stale `OUT` path — it points at
  `destroyer_outsourced_construction_workbook.xlsx` one dir above
  `ddg_workbook/`, whereas the build writes
  `20260601_Destroyer Outsourced Construction_vS.xlsx` into `ddg_workbook/`.
  This is unrelated to the relocation and was deliberately not changed in
  this pass; fix separately if the validator is meant to be used.

---

## How to rebuild

```text
cd "core/ddg_work/ddg_workbook"
python build_workbook.py
python -m workbook_core.tools.sheet_probe \
  "20260601_Destroyer Outsourced Construction_vS.xlsx" \
  --all --out-dir "workbook_ddg/reports/sheet_probe"
```

The engine is `core/workbook_core` (canonical, shared). The pipeline owns
only `workbook_ddg/` (binding + sheets) and its `extracted/` data — no
vendored engine copy.
