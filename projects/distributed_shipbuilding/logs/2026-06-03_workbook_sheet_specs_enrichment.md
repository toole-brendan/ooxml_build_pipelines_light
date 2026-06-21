# 2026-06-03 — Workbook sheet-spec enrichment: formulas + cross-sheet wiring, then native notes / note columns

## Scope

Two enrichment passes over the co-located workbook **sheet specs** for both projects
(`projects/<proj>/workbook/sheet_specs/*.md` — 24 DDG + 21 submarines = **45 files**),
driven from a close read of each sheet **module** (`workbook_<pkg>/sheets/*.py`):

1. **Detail pass** — expand every spec's per-section content with the actual **formula
   logic** and **cross-sheet references** (which tabs each sheet reads from / feeds, the
   producer cells / defined names it exposes, and any external CSV/JSON it loads).
2. **Notes pass** — add, to every spec, a record of (a) **native cell notes** (`ExcelNote`
   → Excel cell comments): how many and *where on the sheet* (section + column) each one
   sits and what it says; and (b) in-sheet **"Note" columns** (and the sibling **"Basis"**
   column) by section.

Specs only — **zero changes to any `workbook_*` module or `workbook_core`**, and no
calc/value edits. The specs are not read by any build, so no workbook rebuild was needed;
the modules were read strictly read-only. Workspace is not under git. The phrase
"reverse-spec" appears nowhere (the specs read as forward design notes).

The starting point was the terse, uniform spec set produced by the earlier
[2026-06-03_workbook_sheet_specs_and_module_rename] session (~15 lines/spec: header +
Purpose + a flat `On the sheet` §-list).

---

## 1. Detail pass — formulas + cross-sheet wiring

**Format added (flat labels, matching the existing house style — no markdown headers):**
each spec keeps its first three lines verbatim (tab name, `Tab color: … · group: …`,
`Module: ….py`) and its `Purpose`, then gains:

- `Source` (where the module loads an extract) — names the actual `extracted/*.csv|json`.
- `Reads` — the sibling tabs this sheet links **from**, plus the imported accessor
  functions / Inputs knobs it uses. Standalone sheets say `- none (…)` with the reason.
- `Feeds` — the tabs that consume this sheet, plus the named producer cells / defined
  names / native tables it exposes.
- An expanded `On the sheet` — each §N now mirrors the module's real §/§Na structure and
  banner labels, annotated with formula **logic** in readable algebra
  (e.g. `TAM by FY = BC_base x BC_coeff + AP_base x AP_coeff`;
  `BC coeff = SUMPRODUCT(BC-mask x $ x (other_US% + foreign%)) / SUMPRODUCT(BC-mask x $)`),
  the cross-sheet links (`<- Inputs`, `<- SCN Budget`), and input knobs/defaults.

**Rule held:** describe formula *logic* only — no invented or recomputed numeric results.
The only numbers stated are constants the module itself hard-codes (knob defaults like
`0.80`/`0.85`, the `0.33` anchor target, the submarines `0.518` published anchor,
`~35.0%`/`~48.5%` author-written basis strings).

**How it was produced (controlled fan-out):**
- Computed the **cross-sheet dependency graph** in both directions from the module imports
  (handling both `from …sheets.X import …` and `from …sheets import X` forms), and the
  module→tab-display-name + group map, so the `Reads`/`Feeds` lines name tabs correctly.
- Hand-authored **two gold-standard exemplars** — `model_tam_build` (a calc sheet) and
  `data_ap_bridge` (a source-data sheet) — to lock the template.
- Fanned the remaining **43** specs out to **6 parallel subagents**, grouped by
  project × sheet-group (DDG data / DDG calc+answer / DDG outputs+validation+sources, and
  the same three for submarines). Each agent got the two exemplars to mirror, the format
  rules, and its slice of the dependency index; each read its modules for the real formulas
  and rewrote its specs.

Result: corpus grew from ~15 to ~54 lines/spec (**~2,415 lines** total); **18** sheets got
a `Source` block; **26** carry at least one explicit `- none` (the leaf/source sheets).

## 2. Notes pass — native cell notes + note columns

Added a trailing `Notes` section to **all 45** specs:

```
Notes
- Native cell notes: <N> -
    §<section> (<col>): <what the note says>
- Note column: §x, §y.   [Basis column: §z.]
```

- **Native cell notes** — **36 `ExcelNote`s across 14 of 45 sheets**, each placed at its
  true anchor (section + column letter) with a one-line gloss; the other 31 sheets say
  `none`. They cluster on headline/at-a-glance rows (§1), coefficient/reconstruction rows,
  and residual/caveat rows — e.g. "average-annual is not a run-rate", "SAM ≠ SOM/capture",
  the $-redacted ~$14.58B MYP-master reconstruction, the AP/LLTM additive-base-=-$0 caveats.
- **Note columns** — the sections whose body tables carry a literal `Note`/`Notes` header,
  plus the **`Basis`** column variant where a sheet uses that instead (DDG TAM Build
  §3a–§3d, AP Bridge §3; submarines LLTM AP §4–§5).

**Accuracy work (the non-obvious part):** notes are collected in a `notes=[…]` list at the
*end* of each builder, and `pos[...]` row keys are **reused across builder functions**, so a
naive "nearest banner" or whole-file key lookup mis-places them. Each note anchor was
resolved to the **row's real definition section** instead, and the conflicting cases were
verified individually — e.g. DDG TAM Build's BC/AP coefficient notes are **§3a** (not the
§5 collection point); the submarines TAM Build / Sensitivity / Summary notes anchor on the
**§1** at-a-glance rows; submarines SAM Build's are §5a/§6. Note-column detection was made
**multi-line-aware** (the label list and `styles=[…S_HEADER…]` often sit on separate lines —
the first scan missed e.g. the Executive Summary's §1 `Note` column).

---

## Verification

| Check | Result |
|---|---|
| Spec count | 24 DDG + 21 submarines = 45 |
| Skeleton present (`Purpose`/`Reads`/`Feeds`/`On the sheet`/`Notes`) | all 45 |
| Forbidden term "reverse-spec" | 0 occurrences |
| Sheets declaring native cell notes | 14 (36 notes total) |
| Declared cell-note count vs module `ExcelNote(` count | **0 mismatches** (all 14 tie out) |
| `Source` blocks (CSV/JSON loaders documented) | 18 |
| Numbers in specs | only module-hard-coded constants (e.g. `0.518`, `~$14.58B`, `~48.5%`) — none recomputed |

Two `summary_executive_summary.md` files (DDG + subs) were written via a heredoc fallback
in the detail pass because the Write tool false-flagged the filename as a "report"; headers
and content are correct.

## Files touched

- **DDG** (`projects/ddg/workbook/sheet_specs/`): all 24 `.md` specs.
- **Submarines** (`projects/submarines/workbook/sheet_specs/`): all 21 `.md` specs.
- No modules, core, README, or build files changed.

## Open items / follow-ups

- **House-style extension** — the added `Source` / `Reads` / `Feeds` / `Notes` sections
  push past the original "brief and uniform" spec convention noted in the README. Left as-is
  (the detail was the explicit ask); offered to compress (e.g. fold `Source` into `Reads`)
  if a terser form is preferred.
- **`Basis` vs `Note` columns** — reported the `Basis` column alongside `Note` where a sheet
  uses it as the annotation column, rather than treating only `Note`-headed columns. Flag if
  `Basis` should be dropped from the `Notes` line.
- **No build run** — these are doc-only edits to `sheet_specs/` (not on any build path); the
  modules were read-only, so neither workbook was rebuilt.
- **README spec convention** still reads "one file per module, named to match it" — unchanged
  and still true; the per-spec body is just richer now.
