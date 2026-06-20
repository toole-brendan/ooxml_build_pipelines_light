# 2026-06-20 — Army project scaffolding (deck + workbook + doc pipelines): session log

First session for the new `army` project. Scaffolded a fresh project under
`projects/army/` with the three thin per-project pipelines (PowerPoint, Excel, Word) that plug into the
shared `deck_core` / `workbook_core` / `docx_core` engines, seeded each with one placeholder content
module, and verified all three build a valid document. Written to be read cold by whoever picks up the
real content work. No engine (`*_core/`) or shared `infra/` files were touched.

**Identity baked into all three pipelines:** title `U.S. Army - Market Mapping`; outputs land at the
project root `projects/army/` as `20260620_US Army Market Mapping_vS.{pptx,xlsx,docx}`.

---

## 1. Decisions settled this session

- **Three pipelines, not two.** The request was "workbook, pptx, etc"; confirmed the "etc" = the Word
  pipeline too, so `army` gets all three (`deck` / `workbook` / `doc`), mirroring `distributed_shipbuilding`
  (the only existing project that carries all three). `mro` and `saronic_usv` carry fewer.
- **Subject / identity = "U.S. Army — Market Mapping."** Sets the docProps title and the `OUT` filenames.
  In the embedded `lib.py` strings the em-dash is written as an ASCII hyphen (`U.S. Army - Market Mapping`)
  to match the existing files' convention; the workbook packager's `normalize_dashes=True` normalizes
  dashes anyway.
- **Seed modules are throwaway placeholders.** Each pipeline is registered with exactly one placeholder
  module so the build is non-empty and provably valid on first run. They are clearly labeled
  `SCAFFOLD PLACEHOLDER` and carry the "to add a module" recipe in each registry's docstring.

## 2. What was created

```
projects/army/
  research/                              (empty placeholder for source research; read by no build)
  logs/                                  (this log)

  deck/
    build_deck.py                        launcher: sys.exit(build())
    deck_army/
      __init__.py                        sys.path math (parents[1] build dir + parents[4] workspace root)
      lib.py                             OUT, TEMPLATE/ASSETS/IMAGES, docProps identity, build()
      slides/__init__.py                 SLIDE_RENDERS registry
      slides/overview.py                 seed slide (chrome-only body slide, slideLayout4)
    slide_specs/                         (empty; plain-text wireframes go here)

  workbook/
    build_workbook.py
    workbook_army/
      __init__.py
      lib.py                             OUT, EXTRACTED, load_extracted_csv wrapper, build()
      sheets/__init__.py                 SHEETS registry
      sheets/summary_overview.py         seed sheet (title banner only; SheetEntry "Overview", group "summary")
    extracted/                           (empty; per-pipeline CSV data dir that lib.py points at)
    sheet_specs/                         (empty)

  doc/
    build_doc.py
    doc_army/
      __init__.py
      lib.py                             OUT, docProps identity, build()
      pages/__init__.py                  PAGES registry
      pages/overview.py                  seed page (H1 + lead paragraph, portrait)
```

## 3. How the wiring works (so the next editor doesn't have to re-derive it)

Each pipeline is a **thin per-project package** that imports the shared engine and binds only what is
project-specific — nothing is vendored. The mechanism, identical across all three:

- **`<pipeline>/<pkg>/__init__.py`** puts two dirs on `sys.path` so imports resolve from any entry point:
  the build dir (`parents[1]`, e.g. `projects/army/deck/`) so the project package resolves, and the
  workspace root (`parents[4]`) so `deck_core` / `workbook_core` / `docx_core` resolve. **Because `army`
  sits at the same depth as every other project, this path math is copied verbatim — no edits.**
- **`<pkg>/lib.py`** binds the project-specifics: `OUT` (written to the project root, `parents[2]`), the
  docProps identity (`_TITLE` / `_CREATOR` / `_APP`), the shared `infra/template` + `infra/assets` (decks)
  or the `extracted/` data dir (workbooks), and a `build()` that packages the registered modules via the
  core builder (`build_pptx` / `package_workbook` / `package_docx`).
- **`<pkg>/slides|sheets|pages/__init__.py`** is the ordered registry; the build reads it.
- **`build_*.py`** is a one-line launcher: `sys.exit(build())`.

Registry object shapes (confirmed against `mro` / `distributed_shipbuilding`):
- deck — `SLIDE_RENDERS: list[tuple]` of `(module, module.render)`; `render()` returns a `<p:sld>` string;
  module may carry `LAYOUT` (str) and `CHARTS` (list).
- workbook — `SHEETS` list of `SheetEntry(tab_name, group, render_fn)`; `render_fn()` returns a
  `WorksheetSpec`. Tab order must group into contiguous `workbook_core.groups.SHEET_GROUPS` blocks
  (summary → guide → inputs → model → data → outputs → validation → sources → chartdata);
  `package_workbook()` asserts that invariant at build.
- doc — `PAGES` list of page modules; `render()` returns a `docx_core.specs.PageModuleSpec`; the packager
  concatenates page bodies and inserts a section break between modules.

## 4. Build verification (all green)

Ran each build from its own directory:

```sh
cd projects/army/deck     && python3 build_deck.py
cd projects/army/workbook && python3 build_workbook.py
cd projects/army/doc      && python3 build_doc.py
```

| Pipeline  | Output (at `projects/army/` root)            | Result                         |
|-----------|----------------------------------------------|--------------------------------|
| Deck      | `20260620_US Army Market Mapping_vS.pptx`    | exit 0 · 1 slide, 0 charts · 41.5 KB |
| Workbook  | `20260620_US Army Market Mapping_vS.xlsx`    | exit 0 · 1 sheet ("Overview") · 4.7 KB |
| Doc       | `20260620_US Army Market Mapping_vS.docx`    | exit 0 · 1 page ("Overview") · 5.4 KB |

Read-only probes ran clean:
`deck_core/slide_probe.py` and `workbook_core/sheet_probe.py` both wrote reports without error.

## 5. Open items / next steps

- **Real content modules.** Replace the three `overview` / `summary_overview` placeholders with actual
  slides / sheets / pages and register them. Copy-from starting points: `deck_core/slide_base_template.py`,
  `workbook_core/sheet_base_template.py`, `docx_core/doc_base_template.py`. House rules: the `*_guide.md`
  and `*_snippets.md` in each core.
- **README project map not updated.** The repo `README.md` tree still lists only the pre-existing projects;
  `army/` was intentionally left out pending confirmation. Add it when the project is real.
- **Log location note.** There is a standing convention that work logs live in the **repo-root `logs/`**,
  not a per-subproject `logs/`. This log was placed in `projects/army/logs/` at explicit request for this
  session. If the project-local location is the new intent, the convention note should be updated; otherwise
  this log should be mirrored/moved to the repo-root `logs/`.
- **Subject is provisional.** "Market Mapping" is the working title; if the project's real scope firms up
  (e.g. a specific TAM/SAM framing like the other projects), update `_TITLE` and the `OUT` filename in all
  three `lib.py` files and re-run the builds.
