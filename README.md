# OOXML Build Pipelines

Raw-OOXML build pipelines that emit polished, fully-editable Office documents —
**PowerPoint decks** (`.pptx`) and **Excel workbooks** (`.xlsx`) — directly as XML,
with no `python-pptx` / `openpyxl` in the build path. Slide and sheet modules are
plain Python files that return complete OOXML strings; the shared core engines handle
the packaging, relationships, chart parts, embedded workbooks, content types, and the
final zip.

Two document types, two shared engines, and any number of projects that plug into them.

## Layout

```
ooxml_build_pipelines_light/
  README.md              ← you are here (covers both pipelines, every project)

  deck_core/             ← shared PowerPoint engine (importable package `deck_core`)
    charts.py  lib.py  ooxml.py  primitives.py  style.py  text_metrics.py
    slide_base_template.py        starting point for a new slide module
    slide_probe.py                read-only OOXML inspector (CLI)
    slide_guide.md  slide_snippets.md   house style + copy-from recipes

  workbook_core/         ← shared Excel engine (importable package `workbook_core`)
    groups.py  lib.py  notes.py  ooxml.py  primitives.py  styles.py
    table_style_names.py  tables.py
    sheet_base_template.py        starting point for a new sheet module
    sheet_probe.py                read-only inspector / linter (CLI)
    sheet_guide.md  sheet_snippets.md   house style + copy-from recipes

  infra/                 ← shared build chrome + reference (not code)
    template/            unzipped pptx template (slideLayouts, master, theme)
    assets/              brand media/ + embeddings/ used by the deck builder
    ooxml_reference/     OOXML cheat sheets, schema (.xsd), Open-XML SDK docs

  projects/              ← one folder per project; add more freely
    research_shared/     cross-project source research (not read by any build)
    distributed_shipbuilding/   Distributed Shipbuilding — consolidated program (holds the two source projects)
      <date>_…_vS.pptx / .xlsx  consolidated deck + workbook build output (lands at the project root)
      deck/      build_deck.py · deck_consolidated/ (slides/) · slide_specs/
      workbook/  build_workbook.py · workbook_consolidated/ (sheets/) · extracted/
      deck_primary/  methodology deck · workbook_award_analysis/  award-analysis workbook
      research/  consolidated source research (not read by any build)
      ddg/                 Distributed Shipbuilding — Destroyers
        <date>_…_vS.pptx          deck build output  (lands at the project root)
        <date>_…_vS.xlsx          workbook build output (lands at the project root)
        deck/      build_deck.py · deck_ddg/ (slides/) · slide_specs/
        workbook/  build_workbook.py · workbook_ddg/ (sheets/) · extracted/ · sheet_specs/
        research/  project source research (not read by any build)
      submarines/          Distributed Shipbuilding — Submarines
        <date>_…_vS.pptx
        <date>_…_vS.xlsx
        deck/      build_deck.py · deck_submarines/ (slides/) · slide_specs/
        workbook/  build_workbook.py · workbook_submarines/ (sheets/) · extracted/ · sheet_specs/
        research/  project source research (not read by any build)
        docs/      deck_spec.txt + session logs

  docs/   logs/          ← shared workspace history (prompts, reports, refactor logs)
```

## How a project plugs into a core

Each pipeline is a **thin per-project package** that imports the shared engine and binds
only what is project-specific. Nothing is vendored — every project imports the single
source of truth at `deck_core` / `workbook_core`.

- **`<project>/<deck|workbook>/<pkg>/__init__.py`** puts two dirs on `sys.path` so imports
  resolve from any entry point: the build dir (so the project package resolves) and the
  workspace root (so `deck_core` / `workbook_core` resolve).
- **`<pkg>/lib.py`** binds the bindings: the output path (`OUT`, written to the **project
  root**), the docProps identity, the shared `infra/template` + `infra/assets` (decks) or
  the `extracted/` data dir (workbooks), and a `build()` that packages the registered
  modules via the core builder (`deck_core.lib.build_pptx` / `workbook_core.lib.package_workbook`).
- **`<pkg>/slides/`** (decks) or **`<pkg>/sheets/`** (workbooks) hold the content modules,
  registered in that subpackage's `__init__.py`.

`build_deck.py` / `build_workbook.py` are tiny launchers — `sys.exit(build())`.

## Build / validate

Run each build from its own directory; the output `.pptx` / `.xlsx` is written to that
project's **root** (e.g. `projects/distributed_shipbuilding/ddg/`):

```sh
cd projects/distributed_shipbuilding/deck         && python3 build_deck.py      # → distributed_shipbuilding/*.pptx
cd projects/distributed_shipbuilding/workbook     && python3 build_workbook.py  # → distributed_shipbuilding/*.xlsx
cd projects/distributed_shipbuilding/ddg/deck     && python3 build_deck.py      # → ddg/*.pptx
cd projects/distributed_shipbuilding/ddg/workbook && python3 build_workbook.py  # → ddg/*.xlsx
cd projects/distributed_shipbuilding/submarines/deck     && python3 build_deck.py      # → submarines/*.pptx
cd projects/distributed_shipbuilding/submarines/workbook && python3 build_workbook.py  # → submarines/*.xlsx
```

Read-only inspection of an emitted document or module (geometry, text, fills,
borders, tables, charts, relationships):

```sh
python3 deck_core/slide_probe.py <target> [--text-estimate] [--table-fit]
python3 workbook_core/sheet_probe.py <target> [--all]
```

`projects/distributed_shipbuilding/ddg/workbook/validate_workbook.py` is an optional `openpyxl`-based read-back QA
for the built DDG workbook (not part of the build; never imported by a sheet module).

## Authoring model

Your usual job is to **author or update content modules** (a slide or a sheet), not to
change the engines.

- **Decks** — a slide module exposes `LAYOUT`, optional `CHARTS`, a `_body()`, and a
  `render()` returning slide XML. Keep body objects inside the `BODY` box, use `style.py`
  tokens instead of hard-coded geometry, use native `house_table()` for row/column data,
  and the `charts.py` factories for native editable charts. Name the module file for its
  role — `cover_*` (slideLayout1), `divider_*` (slideLayout2), `appendix_*`, or a plain
  descriptive name for a body slide. Full rules: `deck_core/slide_guide.md`;
  worked recipes: `deck_core/slide_snippets.md`.
- **Workbooks** — a sheet module builds a `WorksheetSpec` via the shared primitives, with a
  short tab name, compact section labels, and native Excel tables / defined names. Full rules:
  `workbook_core/sheet_guide.md`; recipes: `workbook_core/sheet_snippets.md`.

Each project also carries co-located, human-authored **design specs** —
`deck/slide_specs/` (and `workbook/sheet_specs/`, when present) — as plain-text
wireframes, one file per module and named to match it. They're non-OOXML reference
notes that sit alongside the modules; they are not read by the build.

Raw OOXML reference (cheat sheets, schema, SDK docs) lives in `infra/ooxml_reference/`.

## Locked-core rule

Treat the engine files in `deck_core/` and `workbook_core/` as **locked during normal
content work** — do not edit, refactor, or "clean up" `charts.py`, `lib.py`, `ooxml.py`,
`primitives.py`, `style.py`/`styles.py`, `text_metrics.py`, `tables.py`, `groups.py`,
`notes.py`, the probes, or the shared guides while authoring slides/sheets. If you spot a
possible core issue, report it separately rather than patching it inline. (This rule
governs routine content work — it does not apply when the task is explicitly to change a
core engine.)

## Adding a new project

Copy an existing project folder under `projects/`, rename the package (`deck_<name>` /
`workbook_<name>`), update the `OUT` filename + docProps identity in `lib.py`, and replace
the `slides/` or `sheets/` modules. The `__init__.py` path math and the shared
`infra/` + cores need no changes — a new project resolves them the same way the existing
ones do.
