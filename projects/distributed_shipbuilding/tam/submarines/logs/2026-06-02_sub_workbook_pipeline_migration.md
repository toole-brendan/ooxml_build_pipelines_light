# 2026-06-02 — sub_workbook pipeline: engine de-dup, relocation into core/, sheet migration

> ⚠ **Superseded names.** A later same-day restructure renamed the tree:
> `sub_work`→`submarine`, `sub_workbook`→`workbook`, `sub_pptx`→`deck`,
> `submarine_outsourced_work`→`research`. Prose paths in the body below use
> the **old** names; relative links were updated to the new ones. The
> engine/import logic is unchanged. See
> [../../logs/2026-06-02_core_tree_restructure.md](../../logs/2026-06-02_core_tree_restructure.md).

> **Folder relocation note (read first).** As of this session, the entire
> `sub_work/` tree was **moved** from `Documents\sub_work\` to
> `Documents\core\sub_work\`. Every log in this folder *dated before
> 2026-06-02* was written while `sub_work` still lived at
> `Documents\sub_work\`. Consequences for those older logs:
> - **Relative links still resolve** (e.g. `../sub_pptx/...`,
>   `../sub_workbook/...`) because the `logs/` folder moved together with
>   the rest of the tree.
> - **Absolute paths are now stale.** Any `C:\...\Documents\sub_work\...`
>   reference in an older log should be read as
>   `C:\...\Documents\core\sub_work\...`. This also applies to absolute
>   plan-file paths and any hard-coded `Documents\sub_work\...` strings.
> - The shared workbook engine an older log calls "the sibling
>   `workbook_core`" is **no longer vendored** inside the pipeline — see §2.

## Scope

Untangled and fixed how the **Distributed Shipbuilding Submarines**
workbook actually builds. Starting point was a confusion: the workbook was
believed to build off `core/workbook_core`, but a stale, vendored copy of
`workbook_core` nested inside the pipeline was silently shadowing it. This
session: (1) proved which engine was really used, (2) deleted the stale
copy and relocated the pipeline under `core/` so it imports the canonical
engine, (3) migrated the sheet modules to the newer engine API, (4)
verified with a clean build + probe, and (5) fixed two follow-on path /
encoding issues.

Final state: `python build_workbook.py` from
[../workbook/](../workbook/) produces the 10-sheet,
8-native-table workbook off `core/workbook_core`, with no vendored engine
copy anywhere in the pipeline.

---

## 1. Diagnosis — which `workbook_core` was really building the workbook?

Three candidates were in play:

- `core/workbook_core` — the maintained master (newest; only copy with
  `notes.py`, `ooxml.py`, `table_style_names.py`).
- `sub_work/sub_workbook/workbook_core` — a **vendored copy**, frozen at
  Jun 1 11:35.
- the pipeline package `workbook_sub` itself.

Resolution was proven, not guessed. Running the same import the build runs
(from the project root) resolved `workbook_core` to the **nested vendored
copy**, because the launcher's directory is `sys.path[0]` and that dir
contained a `workbook_core/` that shadowed `core/`. `__pycache__`
timestamps corroborated: the nested `.pyc`s (valid from 11:45) were reused
unchanged at the build, while the source was frozen at 11:35.

Confirmed the vendored copy was genuinely **stale**: every shared module
differed from `core/`, and `core/` had three modules the vendored copy
lacked entirely. So the workbook was being built by the *old* engine — the
opposite of the assumption.

Also discovered: **every** pipeline in the workspace (ddg, maritime srt,
sub) carried its own vendored `workbook_core`. `core/workbook_core` is the
source-of-truth that gets copied out. (Note: the maritime
`refactoring_workbook/workbook_core` is a *different* engine again — not
the same as `core/workbook_core` — so it is **not** a migration reference.)

---

## 2. Structural reorg — delete the shadow, relocate under core/

Decisions confirmed with the user before any destructive action:

1. **Deleted** only the stale vendored copy
   `sub_work/sub_workbook/workbook_core/` (kept `workbook_sub`,
   `build_workbook.py`, `extracted/`, and the output xlsx).
2. **Moved** the whole `sub_work/` tree → `core/sub_work/`.
3. **Repointed imports**: the submarine pipeline now imports
   `core/workbook_core` directly — the first pipeline to break from the
   per-pipeline-vendoring convention. No local engine copy remains.

`sys.path` wiring lives in
[../workbook/workbook_sub/\_\_init\_\_.py](../workbook/workbook_sub/__init__.py):
it puts two dirs on the path — the project root (`sub_workbook/`, so
`workbook_sub` resolves) and the repo `core/` dir three levels up (so
`workbook_core` resolves to `core/workbook_core`). Verified the import
resolves to `core\workbook_core\__init__.py`.

Pre-move safety check: grepped the workspace for external hard-coded
references to `sub_work` — the only code hits were two docstring lines in
`deck_core/charts.py` and `ddg_pptx/.../charts.py` (not runtime paths), so
the move broke nothing outside the tree. Stale `__pycache__` under the
moved tree was purged to force recompilation.

---

## 3. Sheet-module migration to the newer engine API

Worked from a migration checklist. Approach: find **all** API gaps
statically before building, rather than discovering them one failed import
at a time.

- **AST gap-check** (temporary script, since removed): parsed every module
  under [../workbook/workbook_sub/sheets/](../workbook/workbook_sub/sheets/)
  and diffed its `workbook_core.*` imports against the new engine's actual
  exports. Result: the **only** import-level incompatibility was
  `S_TITLE_SLIDE` — the newer `styles.py` renamed that role to
  `S_TITLE_SHEET` (alongside `S_TITLE_SECTION` / `S_TITLE_SUBSECTION`).
  Everything else already resolved.
- **Applied the rename**: `S_TITLE_SLIDE` → `S_TITLE_SHEET`, **22
  occurrences across 8 sheet modules** (guide 6; corpus 3; deck_audit 3;
  budget/input/sam/source/tam 2 each).
- **Registry needed no change**:
  [../workbook/workbook_sub/sheets/\_\_init\_\_.py](../workbook/workbook_sub/sheets/__init__.py)
  already registers the `SheetEntry` objects (`README_METHODOLOGY`,
  `INPUTS`, `BUDGET_BASE`, `POP_CORPUS`, `VENDOR_BUCKETS`, `TAM_MODEL`,
  `SAM_MODEL`, `DECK_OUTPUTS`, `VALIDATION`, `SOURCES`) — not the modules —
  in canonical group order (guide → inputs → data → model → outputs →
  validation → sources), which the packager asserts at build time.
- **Thin binding unchanged**:
  [../workbook/workbook_sub/lib.py](../workbook/workbook_sub/lib.py)
  stayed as the project binding (`OUT`, `EXTRACTED`, `SHEETS`,
  `package_workbook(...)`), separate from the core packager.

No runtime/signature mismatches surfaced — once `S_TITLE_SLIDE` was
renamed, the migration was clean.

---

## 4. Build + probe verification

From `core/sub_work/sub_workbook/`, `python build_workbook.py` succeeded:

| # | sheet | | # | sheet |
|---|-------|---|---|-------|
| 1 | README_Methodology | | 6 | TAM_Model |
| 2 | Inputs | | 7 | SAM_Model |
| 3 | Budget_Base | | 8 | Deck_Outputs |
| 4 | POP_Corpus | | 9 | Validation |
| 5 | Vendor_Buckets | | 10 | Sources |

- 10 sheets, **8 native tables**, ~114 KB output, passing the new
  packager's strict name/group/table/defined-name/notes validation.
- Zip integrity OK; 10 worksheet parts + 8 table parts + valid
  `workbook.xml` / `[Content_Types].xml`.
- `sheet_probe --all` wrote per-sheet md+json to
  `../sub_workbook/workbook_sub/reports/sheet_probe/`. Scan for
  `#REF`/broken-ref/warnings: clean (only literal cell text like
  "redacted / missing-$" matched the keyword scan).

---

## 5. Follow-on fixes

- **`sheet_probe` UTF-8 crash (core-wide bug).**
  [../../workbook_core/tools/sheet_probe.py](../../workbook_core/tools/sheet_probe.py)
  `_write()` called `write_text(...)` without an encoding, so on Windows
  (cp1252 default) it raised `UnicodeEncodeError` on `→` (U+2192) in the
  report markdown. Added `encoding="utf-8"` to both the `.md` and `.json`
  writes. Re-ran the probe **without** the `PYTHONUTF8=1` workaround — all
  10 reports write cleanly. Affects every pipeline that runs the probe.
- **Stale permission paths.**
  [../.claude/settings.local.json](../.claude/settings.local.json) had
  three `allow` entries pointing at `Documents\sub_work\...`. Repointed all
  to `Documents\core\sub_work\...`; JSON re-validated.

---

## How to rebuild

```text
cd "core/sub_work/sub_workbook"
python build_workbook.py
# probe (encoding fix means no PYTHONUTF8 needed):
python -m workbook_core.tools.sheet_probe \
  "20260601_Distributed Shipbuilding Submarines_vS.xlsx" \
  --all --out-dir "workbook_sub/reports/sheet_probe"
```

The engine is `core/workbook_core` (canonical, shared). The pipeline owns
only `workbook_sub/` (binding + sheets) and its `extracted/` data — no
vendored engine copy.
