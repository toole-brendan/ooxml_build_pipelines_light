# Session log & handoff — pptx→idiomatic converter, and the charts→idiomatic question

**Date:** 2026-06-23 → 2026-06-24
**Project:** `projects/commercial_strategy_reference/`
**Source deck:** `/Users/brendantoole/projects3/reference/20260325_Commercial Strategy_Market Analysis_vS.pptx` (168 slides, 88 native charts)

> **STATUS (2026-06-24, continued): the open question in §5–6 is RESOLVED — see §8.**
> R1 (extractor) + R2 (`styled_chart`, data-over-template) are shipped in `deck_core/charts.py`,
> wired into the converter, and the two chart modules were regenerated. Charts now expose their
> data as Python `_DATA` literals while rendering **pixel-identical** to the bundled originals
> (verified, combos included). R3 (factory rebuild) was evaluated and rejected.

---

## 1. Goal

Build a **curated reference corpus** of slides ported 1:1 from a real think-cell deck
into native `deck_core` Python modules, so future AI agents can be pointed at them as
worked examples when authoring custom slides. The strategic intent (drives every design
choice): if this works, **phase out house-style-specific primitives** (e.g. `house_table`)
and just point agents at these converted modules — so the converter emits **general**
primitives that faithfully reproduce the source, not opinionated house helpers.
**Faithfulness > house-style conformance.**

The work is a **two-stage workflow**: a *mechanical, faithful* conversion (the script),
then optional *idiomatic refactor* (semantic renames). QA is **render-and-look** (build
the pptx, render to PNG, eyeball) — not the old `src_png`/`png` diffing harness.

---

## 2. Where everything lives

```
projects/commercial_strategy_reference/
├── 20260325_Commercial Strategy Market Analysis (reference port)_vS.pptx   ← built output (4 slides)
├── 2026-06-24_converter_and_chart_idiomatic_handoff.md                     ← this file
└── deck_commercial_strategy/
    ├── build_deck.py                       ← `python build_deck.py` → builds the .pptx
    ├── _tools/
    │   ├── convert_slide.py                ← THE CONVERTER (current)
    │   └── convert_slide_v1_flat.py        ← backup: early flat-output version (restore by copying over)
    ├── _qa/                                ← renders + backups (not built into the deck)
    │   ├── out-*.png                        ← rendered slides for visual QA
    │   ├── ships_act_volume_by_type_handpolished.py.txt   ← the hand-polished idiomatic v of slide 59 (kept for reference)
    │   └── chart59_bundled_vs_factory.pptx  ← the chart prototype: slide1=bundled, slide2=factory rebuild
    └── deck_commercial_strategy/
        ├── __init__.py  lib.py             ← pipeline bindings (mirror gso_JM_reference)
        └── slides/
            ├── __init__.py                  ← SLIDE_RENDERS registry (source order: 3, 4, 59, 104)
            ├── research_scope.py            ← src 3
            ├── project_calendar.py          ← src 4
            ├── ships_act_volume_by_type.py  ← src 59
            ├── cost_comparison_automation.py← src 104
            └── _src/                        ← verbatim chart parts (chartNN.xml + .xlsb) read by the modules
```

Shared-engine change this session: **`deck_core/style.py` gained `IN(inches)` and `PT(points)`**
(plus `EMU_PER_INCH`). Backward-compatible (raw EMU ints still work). Modules now express
coordinates as `IN(1.064)` and font sizes as `PT(10)`; the build converts to EMU/centipoints.

---

## 3. What the converter does (current feature set)

`_tools/convert_slide.py` — stdlib-only, copy-next-to-any-pipeline. Pipeline:
**parse every shape → detect roles/structure → emit a Python module.**

- **Native `<c:chart>`** → bundled verbatim + its `.xlsb` via `editable_bundled_chart`
  (byte-exact, still "Edit Data"-editable; never rebuilt from data). Chart part + workbook
  copied into `slides/_src/`.
- **think-cell OLE frame** ("… do not delete") + its **EMF preview `<p:pic>`** → dropped.
- **`<a:fld>` labels** (think-cell) → frozen to static `run()`s from their cached text.
- **Clusters**: shapes sharing a style (≥3) → a module-level data table + a loop, including
  only the fields that vary. Auto-named (`_AXIS_YEARS`, `_LEGEND_SWATCHES`, `_CALLOUTS`, …).
- **Chrome detection**: breadcrumb / title / Preliminary chip / sources → house builders
  (`breadcrumb()` / `title_placeholder()` / `prelim_chip()` / `sources_line()`), **but only
  when within 0.1″ of the house position** — otherwise kept verbatim so nothing moves.
- **Native tables** (`<a:tbl>`): reconstructed with low-level `table()` / `trow()` / `tcell()`
  — merges via `grid_span`/`row_span` (filler cells dropped, engine re-synthesizes), per-cell
  fill / borders / insets / anchor preserved. (NOT `house_table` — per the phase-out plan.)
- **Borders** inherited from `<p:style><a:lnRef>` (with or without an explicit `<a:ln>`) are
  resolved (color from the ref, width from the theme line-style list).
- **Colors**: `schemeClr` + `lumMod`/`lumOff`/`shade`/`tint` baked to hex; exact deck_core
  token matches emitted as the token (`BLACK`, `GRAY_1`, …); off-ramp colors as quoted hex.
- **Units**: coords `IN(<inches>)`, sizes `PT(<points>)` (3-decimal inches = visually exact,
  sub-0.05px, not byte-exact). `--units emu` opts back to raw EMU.
- **Raw fallback**: gradient/pattern/picture fills, custGeom, or placeholders without geometry
  → verbatim OOXML string (dangling-ref cruft — `custDataLst`/`extLst`/hyperlinks — stripped
  first, id renumbered). Tagged with a `# RAW verbatim` comment.

### Run it

```bash
cd projects/commercial_strategy_reference/deck_commercial_strategy/_tools
python3 convert_slide.py "<source.pptx>" <N> \
    --out ../deck_commercial_strategy/slides/<name>.py \
    --src-dir ../deck_commercial_strategy/slides/_src \
    --module-name <name> --layout slideLayout4
# then register <name> in slides/__init__.py SLIDE_RENDERS, and:
cd .. && python3 build_deck.py
```

### QA

- Build must print `wrote … (N slides, M charts)`.
- **Verify rels resolve** (PowerPoint repairs on dangling `r:id`; soffice silently ignores —
  see the `pptx-port-dangling-rels-cause-powerpoint-repair` memory): unzip the output, regex
  every `r:id`/`r:embed` in each slide/chart part against its `.rels`.
- **Render and look** (soffice → PDF → `pdftoppm` → PNG). soffice can hang on a stale lock;
  `pkill -9 soffice` and use a fresh `-env:UserInstallation=file://<tmp>` profile.

---

## 4. Slides converted (4, proven across distinct archetypes)

| src | module | archetype | result |
|---|---|---|---|
| 3 | `research_scope` | framework **diagram** (10 ellipses, 9 connectors, no chart) | 0 raw, fully idiomatic, faithful |
| 4 | `project_calendar` | timeline **table** (merged `<a:tbl>`, grid borders) + overlays | 0 raw, table reconstructed, faithful |
| 59 | `ships_act_volume_by_type` | stacked-column **native chart** + think-cell overlays | chart bundled + 1 raw shape; faithful |
| 104 | `cost_comparison_automation` | dual grouped **charts** + % badges + 8 connectors | chart bundled; faithful |

All build green, all rels resolve, all render visually faithful.

### Verbatim residue (what is NOT idiomatic primitives)

Only two kinds, across all four modules:
1. **The 2 bundled native charts** (`_src/slide59_chart42.xml`+`.xlsb`, `_src/slide104_chart59.xml`+`.xlsb`)
   — verbatim **by design** (see §5).
2. **One RAW `<p:sp>`** — `ships_act_volume_by_type.py`, the `ltDnDiag` pattern-fill legend
   swatch. `text_box` has no pattern-fill option. (Would be idiomatic with a small
   `pattern_fill=` param on `text_box`.)

Slides 3 and 4 are 100% idiomatic primitives.

---

## 5. The charts→idiomatic question (the open thread)

**A chart is data + style, and the style is huge.** chart42 (slide 59) = 1,075 XML elements;
chart59 (slide 104) = 1,995. Style = type, per-series colors, axes (min/max/format/ticks),
gridlines, gap/overlap, data-label placement + selection, number formats, legend, plot layout.
think-cell draws the **labels, legend, and category axis as separate overlay shapes**; the
native chart is essentially bars + selective `dLbls` + (often hidden) axes.

The two source charts sit on opposite ends of feasibility:
- **chart59 (slide 104)**: pure **stacked bar**, 11 series → `column_chart(mode="stacked")` exists.
- **chart42 (slide 59)**: **bar + line combo**, stacked **and** standard grouping → **no factory**.

### The prototype (do look at it)

`_qa/chart59_bundled_vs_factory.pptx`:
- **Slide 1 = bundled** (current approach): the verbatim chart XML reattached. Pixel-perfect
  because it *is* the original. Faithful but opaque (`read_text("chart59.xml")`).
- **Slide 2 = factory rebuild**: `column_chart()` from data extracted out of the chart's caches
  (categories, 11 series with names/values/colors, axis max, gap), then styling tuned (axis +
  gridlines hidden, `value_label_format="0.0"`).

**Findings:**
- ✅ The factory reproduced the **data, colors, stacking order, and bar heights** faithfully.
- ✅ Axis/gridlines/number-format matched via params.
- ⚠️ **It still looks worse than bundled.** The source *selectively suppressed* labels on thin
  segments; the factory's `show_value_labels` is all-or-nothing, so tiny bands (`0.0`, `0.1`)
  clutter and overlap. Minor bar-geometry differences too.
- ❌ chart42's combo (bar+line, dual grouping) **can't be rebuilt** by any current factory.

**Verdict:** for a real, style-dense chart, the pure-factory "idiomatic" rebuild **visibly
degrades fidelity** — you don't get idiomatic *and* faithful from it. The bundled (verbatim)
chart is the faithful choice, and is what the modules use today. **Charts are the one place
where verbatim is genuinely correct.** The data isn't truly lost — it lives in the embedded
`.xlsb` — it's just not inline Python.

---

## 6. RECOMMENDATIONS — how to work the converter on charts→idiomatic

The honest framing: **"idiomatic + faithful" for charts means exposing the editable DATA as
Python while keeping the exact STYLE.** Pure-factory reproduction trades away fidelity; pure
bundling hides the data. Ranked plan:

### R1 (recommended, do first): build the **chart-data extractor** — independent of approach
A reusable function that reads a chart part and returns `{categories, series:[{name, values,
color}], value_axis_max, gap, grouping, type}` from the `<c:numCache>`/`<c:strCache>` caches +
`<c:spPr>` fills. The prototype code in the scratchpad (`chart_proto.py`) already does this —
**lift it into `convert_slide.py`.** Every chart path needs it. Low risk, high reuse.
- Watch-outs found: categories can be absent (think-cell) → synthesize N blanks; cache values
  carry float artifacts (`0.3999…`) → round; some series have no fill (spacer/`no_fill`).

### R2 (recommended primary path): **data-over-template** — faithful look + editable data
A new primitive, e.g. `deck_core.charts.styled_chart(template_xml, data, *, embed_ext=...)`:
- keep the source chart XML as the **styling template** (so the look is byte-identical to the
  bundled version — i.e. as good as prototype slide 1),
- rewrite each series' `<c:numCache>` and the category `<c:strCache>` `<c:pt>` values from the
  Python `data`, and regenerate the embedded workbook (.xlsx) from `data` (or keep the source
  `.xlsb` when data is unchanged),
- the module reads: `_DATA = {categories:[…], series:[{name, values}]}` then
  `CHARTS = [styled_chart(_TEMPLATE, _DATA)]`.
- **Gives:** faithful styling (slide 1 quality) + the data visible/editable in Python — the
  best-of-both for the reference-corpus goal. **Limitation:** per-series *colors* live in the
  template's `<c:spPr>`, so style stays templated (not pure-Python); an agent edits data, not look.
- **Effort:** moderate — cache-rewriting is mechanical (`<c:pt idx><c:v>`); the workbook
  regen can reuse the existing `_build_embed_xlsx` in `charts.py`.

### R3 (opportunistic): **factory path only for simple, low-fidelity-tolerance charts**
Where a chart is a plain single-grouping bar/column/line/waterfall/marimekko AND minor styling
drift is acceptable, emit `column_chart(...)` etc. from the extracted data (fully idiomatic).
To make it faithful enough, the factory needs **per-datapoint label suppression** (the one gap
the prototype exposed) — add a `value_label_points=[…]` / per-series label mask to `_bars()`.
Do **not** use this for hero/complex charts; it degrades them.

### R4: **bundle remains the fallback** — always
For combos (chart42), exotic types, or anything R2/R3 can't reproduce faithfully, keep
`editable_bundled_chart`. The converter should **auto-route**: factory/styled if the type is
supported and faithful, else bundle. Never silently degrade a chart to be "idiomatic."

### Suggested sequence
1. R1 extractor into the converter (+ tests on chart59 and chart42 data).
2. R2 `styled_chart` primitive; re-port slide 104 with it; render vs `_qa/chart59_bundled_vs_factory.pptx`
   slide 1 — should be pixel-identical, but with data now in Python.
3. Decide if R3 is worth it (it only helps simple charts); if so add per-point label control.
4. Wire auto-routing (type-supported → R2/R3, else R4) into `convert_slide.py`.

### Decision still open for the user
- Is **data-editable-but-style-templated** (R2) "idiomatic enough"? It exposes the data (the
  thing agents most want to read/adapt) but keeps colors/axes in a template asset. If yes, R2 is
  the path. If you want **colors/style also as Python**, that's the big factory-extension
  investment (R3 generalized) and it still can't cover combos.

---

## 7. Related context

- Methodology: `docs/faithful_deck_port_methodology.md` (the original faithful-port playbook).
- Prior worked ports: `projects/gso_JM_reference/`, `projects/mro/`.
- Memories: `pptx-to-idiomatic-module-workflow`, `pptx-port-dangling-rels-cause-powerpoint-repair`.
- Converter backup: `_tools/convert_slide_v1_flat.py`. Hand-polished slide-59 reference:
  `_qa/ships_act_volume_by_type_handpolished.py.txt`.

---

## 8. RESOLUTION (2026-06-24, continued) — R1 + R2 shipped; charts are now data-over-template

The open question (§5–6, "is data-editable-but-style-templated idiomatic enough?") is settled
with a concrete, render-verified artifact: **R2 is the path, and it is strictly better than both
bundling (R4) and a factory rebuild (R3) for the corpus goal.**

### What shipped
- **`deck_core/charts.py`** — two new public functions (+ private helpers), placed right after
  `editable_bundled_chart`; module docstring updated:
  - `extract_chart_data(chart_xml)` **(R1)** → `{categories, series:[{name,values,color}],
    value_axis_max, gap_width, overlap, types}`. Walks `<c:ser>` in document order across every
    chart-type container (barChart then lineChart…), so combos work. think-cell omissions
    (`<c:cat>`/`<c:tx>`) come back `None` (categories/series-names are separate slide text boxes).
  - `styled_chart(template_xml, data, embed_bytes, *, embed_ext="xlsb")` **(R2)** → keeps the
    source chart part as the exact STYLE template, rewrites **only** its data caches from `data`
    (ElementTree; all 8 chart-namespace prefixes registered so the parse→serialize round-trip
    preserves the full element inventory), then delegates to `editable_bundled_chart` to reattach
    the workbook + `<c:externalData>`. Returns the same CHARTS dict the build loop consumes.
- **`_tools/convert_slide.py`** — added a stdlib mirror of the extractor (keeps the tool
  copy-next-to-any-pipeline) and now emits `_CHART*_DATA` literals + `CHARTS =
  [styled_chart(_CHART*_TPL, _CHART*_DATA, _XLSB*)]`. **Auto-routes:** styled_chart when data +
  .xlsb are recoverable; else `editable_bundled_chart`; else a raw `{"chart_xml": …}`. The
  `from deck_core.charts import …` line now reflects actual usage.
- **Modules regenerated** through the new converter (same shape-stats as before, only the chart
  path changed): `cost_comparison_automation` (src 104, 11-series stacked bar) and
  `ships_act_volume_by_type` (src 59, 7-bar + 1-line **combo**). Each now carries a readable
  `_CHART0_DATA` literal next to `CHARTS`.

### Proof (render-and-look + pixel diff)
- 4-slide prototype, bundled-vs-styled for BOTH charts → visually identical
  (`_qa/chart_bundled_vs_styled.pptx`: slides 1/3 bundled, 2/4 styled).
- **Regenerated deck vs the bundled baseline → pixel-identical** (PIL bbox-of-difference =
  `None`, mean abs diff = `0.0000`) on both chart slides; identical file sizes. All chart rels
  resolve, all embeds present.
- Byte-parity: `deck_core.styled_chart` output == the render-verified prototype output.

### Why R2 wins (and R3 is not worth building)
- **vs R4 (bundle):** same faithful render, but the data is no longer opaque — it's a Python
  literal an agent can read/adapt. Strictly better for a reference corpus.
- **vs R3 (factory):** the factory degraded fidelity (all-or-nothing labels clutter thin
  segments; bar-geometry drift) and **cannot build the bar+line combo at all**. R2 keeps the
  template's exact `dLbls` (selective label suppression), `dPt` per-point colors, and pattern
  fills, so the combo and the hero stacked bar come through untouched. The only thing R2 leaves
  templated is per-series COLOR / axis STYLE — exactly the "huge style" you want kept verbatim,
  not re-expressed in Python. **So the §5 verdict flips: a real chart CAN be both faithful and
  data-in-Python — just not via a factory.**

### Caveat (also in the `styled_chart` docstring)
The reattached workbook is the source's. Editing `_DATA` re-renders the chart (caches are
rewritten from it) but PowerPoint's "Edit Data" pane shows the original workbook until it's
regenerated. For the corpus goal (agents read/adapt the data; the render follows `_DATA`) this is
the right trade. A future `embed_bytes=None` path could regenerate the workbook from `_DATA` for
full Edit-Data consistency — it would also need to rewrite the `<c:f>` refs, since think-cell
lays data out **transposed** (series-as-rows, e.g. `Sheet1!$A$1:$E$1` per series; categories and
series names absent from the chart entirely).

### If continuing
- Port more chart slides — `styled_chart` is the default path now; nothing special to do.
- Only build the `embed_bytes=None` regenerate path if Edit-Data-follows-`_DATA` becomes a real
  need; it's the only thing R2 doesn't already give you.
- Memories: `[[styled-chart-data-over-template]]`, `[[pptx-to-idiomatic-module-workflow]]`.
