# Session log & handoff — affordance naming + local_meaning, converter durability, rich-text fidelity, and the `library/` consolidation

**Date:** 2026-06-25 (continues the five 2026-06-24 docs in this `logs/` folder)
**Project:** `projects/style_library/`
**Engine touched:** `deck_core/primitives.py` (workspace-root package)
**Converter touched:** `_tools/convert_slide.py`
**Corpus:** the 40-module curated schematic corpus — **renamed and consolidated to `projects/style_library/library/`** this session (was `archetypes/schematics_curated/`).

Big picture: the corpus's cluster naming moved from converter-generic / business-specific to a **reusable affordance vocabulary + a slide-specific `local_meaning` comment**; that convention was folded into the **converter** so it's durable; a real **rich-text fidelity gap** (underline / paragraph spacing / shadow) was closed in the engine; and the whole `archetypes/` tree was **deleted/renamed/flattened to a single `library/` deck**. Nothing committed to git (project dir is untracked). No standing PNG QA except the targeted bug-render in §4.

---

## 0. The naming decision (the spine of the session)

**Canonical cluster name = (optional `_CHART_` prefix) + visual/structural affordance + a suffix that encodes the primitive.** It says *what the thing is* and *what emits it*, reusable on any slide — NOT the slide's business topic (that goes in `local_meaning`) and NOT its position (the coordinates already carry that). Worked example of the only allowed change:

```python
# BEFORE (converter generic)            # AFTER (affordance + local_meaning)
_LEGEND_SWATCHES = [...]                 # local_meaning: paired Retirements/Orderbook legend by archetype
                                         _CHART_SERIES_KEY = [...]   # same values, same paint order
for x,y,fill in _LEGEND_SWATCHES:        for x,y,fill in _CHART_SERIES_KEY:
    text_box(n(), "LegendSwatch", ...)       text_box(n(), "LegendSwatch", ...)   # shape-name STRING preserved
```

Design rules that held all session:
- **Suffix → primitive:** `_LABELS/_TICKS/_NOTES`→no-fill text_box; `_BOXES/_BANDS/_CELLS/_CHIPS/_BADGES/_CHEVRONS`→filled text_box; `_FRAMES`→no-fill bordered; `_CONNECTORS/_RULES/_BRACES/_LEADERS`→connector; `_GLYPHS/_ICONS`→custom_geometry; `_KEY`→swatch+label; `_TABLE`→table(); `_LOGOS/_MEDIA`→picture().
- **Rename the VARIABLE, never the shape-name STRING.** The string arg (`"LegendSwatch"`, `"YearLabel"`) is `cNvPr/@name` — it is in the rendered XML. Variables aren't. This is what makes the whole refactor render-faithful.
- **`local_meaning` is mandatory and is what keeps the corpus concrete.** Generic name = reusable pattern; `# local_meaning:` line = the specific slide read. Without it, generic naming + the merges (below) would flatten the corpus into interchangeable blandness.

---

## 1. The affordance rename + merges (done by the **deep-research agent**, verified by me)

The user handed the 40 modules to a **deep-research agent** in 4 batches (the READMEs travel with the files: "first 10", "11-20", "21-30", "31-40"). The agent applied the affordance vocabulary AND went beyond rename: it **merged** style-separated clusters and **split** style-overloaded ones, moving the distinguishing attribute to a per-row field. Examples:
- `_LIGHT_BOXES` + `_DARK_BOXES` → one `_FLOW_NODES` (fill/text_color as row data)
- `_EQUALS_SIGNS` + `_PLUS_SIGNS_COL/_ROW` → one `_OPERATOR_GLYPHS` dict (the converter's old `"LegendSwatch"` mislabel, now correctly named — string preserved)
- `_RETIREMENT_BAR_LABELS` + `_ORDERBOOK_BAR_LABELS` → `_DATA_LABELS` (anchor row field)
- `_DARK_BOXES` → split into `_FLOW_NODES` (calc rows) + `_GRID_CELLS` (mission rows)
- `_AXIS_YEARS`→`_CATEGORY_TICK_LABELS`, `_YAXIS_TICKS`→`_VALUE_TICK_LABELS`, `_LEGEND_SWATCHES`→`_LEGEND_KEYS`, `_BAR_VALUE_LABELS`→`_DATA_LABELS`, `_VALUE_RINGS`→`_HIGHLIGHT_RINGS`, `_STEP_LABELS`→`_STEP_RAIL_LABELS`(+`_ANNOTATION_BOXES`), `_STEP_CHEVRONS`→`_STAGE_HEADERS`, etc.

**Verification (the byte gate).** I copied the staged updates over a pristine build of the corpus and byte-diffed all **62 parts (40 slides + 22 charts)** vs baseline → **all byte-identical**, i.e. the renames + merges + row-field restructuring are provably **render-faithful** — *including* the one batch whose README only self-claimed `py_compile`. The 30 updated modules were internally consistent (no old-name leaks). The agent did NOT add `local_meaning` (0/30); it added generic primitive-mechanics comments instead — that gap is §2.

---

## 2. The `local_meaning` pass (me) — 122 lines, then provenance tags stripped

Added a `# local_meaning:` line above every cluster in the **31 cluster-bearing modules** (the other 9 are pure table/chrome — correctly none). Content was **recovered**, not invented: the original curated modules + the READMEs say exactly what each merged cluster absorbed, so e.g. `status_quo_fleet_outlook._DATA_LABELS` got:

```python
# local_meaning: the net gross-tonnage printed on each bar; the 21 net-negative (retirement)
#   years and the 4 early net-positive (orderbook) years are placed differently via the per-row
#   anchor/shape_name field.
```

Mechanics: a name-matching inserter (insert a `# local_meaning:` line above each `^_CLUSTER =`), wrapped at 94 chars. During the pass each line carried a `[absorbed _A + _B]` / `[was _X]` provenance tag; **at the end I stripped all 114 tags** (they reference old converter names and would read as stale once the converter emits affordance names). Comment-only throughout → byte gate stayed **62/62 green** after every batch and after the strip.

---

## 3. Converter durability — affordance names + a `local_meaning` slot (`convert_slide.py`)

So re-conversion stops regressing to `_LEGEND_SWATCHES`/`_AXIS_YEARS`/`"LegendSwatch"`-for-operators, the convention was folded into the converter:

- **New `affordance_name(lead, texts)`** classifies a style-cluster → affordance VARIABLE name by shape preset + fill + text: `math*`→`_OPERATOR_GLYPHS`, `*Callout`→`_CALLOUTS`, `chevron/homePlate`→`_STAGE_HEADERS`, empty no-fill ellipse→`_HIGHLIGHT_RINGS`, year/FY ticks→`_CATEGORY_TICK_LABELS`, empty+filled→`_LEGEND_KEYS`, numeric→`_DATA_LABELS`, filled+text→`_FLOW_NODES`, else `_LABELS`/`_GROUP`.
- **`cluster_identity` restructured** to compute the shape-name STRING (`sn`) with the **OLD heuristic untouched** (so `cNvPr/@name` and thus the produced XML are byte-identical) and the table VARIABLE + anchor prefix from the new classifier. **Variables never enter the XML** — that's the invariant.
- **`# local_meaning: TODO - <affordance>; sample: <text>`** seeded above each emitted cluster (the converter knows the affordance, not the slide's meaning).

**Verified:** re-converted 5 real source slides (CS 44/30/31/33, Navy 18) → `render()` **byte-identical** to the curated modules on all 5; every branch fired (`_OPERATOR_GLYPHS`, `_STAGE_HEADERS`, `_CALLOUTS`, `_CATEGORY_TICK_LABELS`, `_LEGEND_KEYS`, `_FLOW_NODES`) + `local_meaning` stubs.

**Honest limits (told to the user):** the converter classifies by STYLE, so it does NOT reproduce the agent's semantic **merges** (it emits numbered siblings `_FLOW_NODES2`, `_OPERATOR_GLYPHS2/3`), can't specialize the `_LABELS` fallback (legend/axis/rail), and only **stubs** `local_meaning`. So: **the `library/` corpus is the source of truth; do NOT re-convert a refined module** (you'd lose its merges + local_meaning). The converter is for NEW slides + a much better starting point. Names are durable through re-convert; merges/local_meaning are not.

---

## 4. Rich-text fidelity fix — underline / paragraph spacing / shadow (engine + converter)

The user spotted that the two text-heavy "Key Findings" slides (registry slides 3 & 4 = CS source **8 & 9**) rendered without the source's **blue-italic-underlined** "link-styled" text, **bullet spacing**, or the contingencies-callout **drop shadow**. Root cause: the converter was **dropping** that formatting (and `render_tpara` silently dropped table-cell `spcAft`/`lnSpc` too, flattening all bullet spacing). Confirmed against source: slide 8 had 9 underline runs / 13 `spcBef`; slide 9 had 8 underline / 16 `spcBef` / 2 `effectLst`; **0 actual hyperlinks** (the "links" are just blue+italic+underline styling).

Closed the gap durably:
- **`deck_core/primitives.py`:** `run(underline=)` (`_emit_run` already emitted `u="sng"`, just unwired), `paragraph(space_before=)`, `tpara(space_before=)`, `_emit_paragraph` `spcBef`, and `text_box(effects=<verbatim a:effectLst>)` injected into spPr.
- **`convert_slide.py`:** `parse_run` captures `u`; `parse_para` captures `spcBef`; `render_run`/`render_trun` emit `underline=`; `render_para`/`render_tpara` emit `space_before/after` (+ `render_tpara` now also emits the previously-dropped `space_after`/`line_spacing`); `parse_sp` captures `effectLst` verbatim via `_elem_inner_xml`; `render_sp` emits `effects=`.

Re-converted slides 8 & 9 → emitted **underline=10, space_before=29 (exactly 13+16), effects=1**; **render-verified vs the source** (high-res crops show the blue/italic/underlined header and the shadowed dashed callout, with bullet spacing restored). Hand docstrings (EXHIBIT/CODE MAP) re-applied to the two re-converted modules with an honest note about the fidelity restore. NOTE: only these 2 were re-converted — **other text-heavy slides that had underline/spacing/shadow in their source still carry the older flattened render** until re-converted (eyeball candidate for a future pass).

---

## 5. Consolidation → a single `library/` deck (deletes + rename + flatten)

The refined deck was promoted to be the canonical corpus, then the whole `archetypes/` tree was collapsed:
- **Promoted** the 40 refined modules over `schematics_curated` (kept renders; added affordance names + 122 local_meaning + the §4 fix).
- **Deleted:** the staging deck `archetypes/schematics/` (regenerable), the root `20260325_…(reference port)_vS.pptx`, and the stale early prototype `deck_commercial_strategy/` (only 4 modules + `_qa/` chart prototypes from the original converter project).
- **Renamed + flattened** `archetypes/schematics_curated/schematics/` → a clean two-level deck:

```
projects/style_library/
├── _tools/convert_slide.py        # THE CONVERTER (stdlib-only)
├── logs/                          # these handoffs
└── library/                       # build dir: build_deck.py + library.pptx
    └── library/                   # Python package: lib.py, __init__.py, slides/ (+ _src/, images/)
```

Code that had to change for the rename/flatten (path depth dropped one level): `build_deck.py` → `from library.lib import build`; `lib.py` → `from library.slides import`, `IMAGES` path `"library"`, `OUT="library.pptx"`, identity strings, and **`ROOT = parents[5]` → `parents[4]`**; `__init__.py` → **`_CORE_DIR = parents[5]` → `parents[4]`** (this is what puts the workspace root on `sys.path` so `deck_core` resolves — missing it is what broke the first flatten build). Build: `cd library && python3 build_deck.py` → `library/library.pptx` (40 slides, 22 charts). DECK_DIR=`parents[1]`, ROOT=`parents[4]`.

---

## 6. State & for the next agent

- **Canonical corpus:** `projects/style_library/library/` — 40 modules, affordance names + 122 `local_meaning`, builds green. Single source of truth; **do not re-convert refined modules.**
- **Converting NEW slides** now emits affordance names + `local_meaning: TODO` stubs + (since §4) underline/spacing/shadow automatically. The human pass shrinks to: merge style-siblings, specialize `_LABELS`, fill the stubs.
- **`local_meaning` durability:** it's human content; a future converter `local_meaning` side-car (keyed per cluster) is the only way to survive a re-convert, and isn't built. Not currently needed (corpus is stable).
- **Eyeball candidates:** other text-heavy slides with source underline/shadow/spacing (e.g. any with dense bulleted tables or callout boxes) still render pre-§4-fix until re-converted; and the converter's affordance classifier is heuristic (the `_LABELS`/`_GROUP` fallback + numbered merge-siblings are where a human still intervenes).
- **Older docs in this folder + many memory path references are PRE-rename** (`archetypes`, `schematics_curated`, `schematics`, the staging deck, the byte-identical gate the user de-emphasized). Mentally map `schematics_curated/schematics` → `library/library`.
- **Memory:** `[[pptx-to-idiomatic-module-workflow]]` updated this session with the affordance naming + invariant, the rich-text fidelity additions, and the `library/` paths. Related: `[[styled-chart-data-over-template]]`, `[[pptx-port-dangling-rels-cause-powerpoint-repair]]`, `[[awards-deck-visual-qa]]`.
