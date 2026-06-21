# 2026-06-03 — Workbook sheet specs + per-tab module rename (DDG + submarines)

## Scope

Authored **per-sheet specs for both workbooks** (previously-empty
`workbook/sheet_specs/`), then **renamed every sheet module file** to match the
spec filenames (`<group>_<tab-slug>.py`), rewired all cross-sheet imports,
regenerated both `sheets/__init__.py` registries, and verified both workbooks
still build. **Zero `workbook_core` changes**; no calc/formula changes — this is
documentation + a mechanical file/identifier rename. No VCS in this workspace, so
`build_workbook.py` (exit 0) was the safety net.

Followed earlier read-only audits this session (deck slide-modules vs specs for
submarines and DDG; appendix-material comparison). Those produced no repo changes;
a personal change-list was saved outside the repo at
`~/projects2/submarine_deck_changes.txt`.

## 0. Decisions carried in from the user

- **Spec granularity = strict per-module** (one spec file per sheet), not a single
  per-workbook roster.
- **Spec filename format = `<group>_<tab-slug>.md`** — group key prefix, then the
  *visible tab name* slugified (not the old module name). Where they diverge, tab
  name wins.
- **Module `.py` files renamed to match the specs** (same base name, 1:1).
- **Tab color stated on every sheet** (even though color derives from the group).
- Specs describe structure only — **no calculated values**, and the phrase
  "reverse-spec" appears nowhere.

## 1. Spec format

Each `sheet_specs/<group>_<tab-slug>.md` is brief and uniform:

```
<Tab Name>
Tab color: <HEX> (<color name>)  ·  group: <Group Label>
Module: <group>_<tab-slug>.py

Purpose
<one line>.

On the sheet
- <§ section 1>
- <§ section 2>
...
```

Tab color is per **group** (`workbook_core.groups.SHEET_GROUPS`), restated on each
sheet for convenience:

| group | label | color |
|---|---|---|
| summary | Executive summary | 6A4C93 purple |
| guide | Guide & scope | 2C6E6E teal |
| inputs | Inputs & levers | B8860B ochre |
| model | Model (TAM/SAM) | 34406B indigo |
| data | Source data | 7B1F3A burgundy |
| outputs | Outputs | 2E7D4F green |
| validation | Validation | 6E6E6E gray |
| sources | Sources | 1F3A5F navy |

Section lists were extracted from each module's `§N` banner labels and docstring
intent; dynamic-title sheets (DDG `methodology`, subs `source_index`) were read
directly to describe them accurately.

## 2. Files created — 45 specs

- **DDG: 24** in `projects/ddg/workbook/sheet_specs/`
  (`summary_executive_summary`, `guide_methodology`, `inputs_inputs`,
  `inputs_scenarios`, `model_tam_build`, `model_sam_build`, 9× `data_*`,
  `outputs_deck_outputs`, `outputs_z_chart_data`, 5× `validation_*`,
  `sources_source_lineage`, `sources_references`).
- **Submarines: 21** in `projects/submarines/workbook/sheet_specs/`
  (`summary_executive_summary`, `guide_methodology_scope`,
  `inputs_assumptions_controls`, `model_tam_build`, `model_sam_build`, 7× `data_*`,
  3× `outputs_*`, 4× `validation_*`, `sources_source_index`, `sources_references`).

## 3. Module rename

All 24 DDG + 21 subs sheet modules renamed `<old>.py → <group>_<tab-slug>.py`.
Helpers **not** renamed and **not** registered: `_layout.py`, `_taxonomy.py`
(DDG), `taxonomy.py` (subs).

Slug rule: lowercase; spaces / `&` / camel boundaries → `_`; acronym runs kept
whole. Two slugs diverge from the old module name (tab name won):

| project | old module | new module | tab |
|---|---|---|---|
| DDG | `chart_data.py` | `outputs_z_chart_data.py` | z_ChartData |
| subs | `mib_excluded.py` | `validation_sib_excluded.py` | SIB Excluded |

Everything else: new name = `<group>_<oldname>` (tab slug already equalled the
module name).

### Import rewiring

Done with a deterministic script (mapping old→new per package). Two import forms
both had to be handled:

1. **Dotted path** `from workbook_<pkg>.sheets.<old> import …` /
   `workbook_<pkg>.sheets.<old>` — rewritten in pass 1 (anchored on the
   `…sheets.` prefix, `\b`-terminated; order-independent and body-safe).
2. **Package-level name** `from workbook_<pkg>.sheets import <old> as …` — *missed*
   by pass 1 (no dot after `sheets`); caught the submarines build and fixed in a
   second pass restricted to import lines. **6 occurrences, all submarines**
   (`inputs_assumptions_controls`, `model_sam_build`, `data_worktype_evidence`,
   `data_pop_source_audit`); DDG had none.

Each module's **leading docstring token** was updated to the new name. Each
`sheets/__init__.py` was **regenerated** (group-block comments preserved; only the
module tokens changed — `SheetEntry` constant names like `TAM_BUILD`,
`SIB_EXCLUDED` are unchanged). Tab names/colors are driven by explicit
`_TAB`/`_GROUP` literals inside each module, so renaming files did not change any
tab name or color.

## 4. Verification

Both builds run from their own dir, exit 0:

- **DDG** → `20260601_Distributed Shipbuilding DDG_vS.xlsx`, **24 tabs**, 12 native
  tables, 6 note parts. Tabs render `Executive Summary … z_ChartData … References`.
- **Submarines** → `20260601_Distributed Shipbuilding Submarines_vS.xlsx`,
  **21 tabs**, 12 native tables, 8 note parts. Tabs render
  `Executive Summary … SIB Excluded … References`.

A green build means the full import graph (`lib.py → sheets.SHEETS → every
module`) resolved and `package_workbook()`'s group-contiguity assertion passed.

## 5. Notes / leftovers

- `workbook_<pkg>/reports/sheet_probe/` may still hold outputs named for the old
  modules — generated artifacts; they regenerate on the next probe run. Harmless to
  the build.
- README convention ("specs … one file per module, named to match it") still holds:
  spec base name == module base name after the rename.
- `lib.py` imports only the package-level `SHEETS`; `build_workbook.py` /
  `validate_workbook.py` carry no per-module references — nothing outside
  `sheets/` needed editing.
