# Session log + handoff — charts resolved, and a playbook for converting slides at scale

**Date:** 2026-06-24
**Project:** `projects/commercial_strategy_reference/`
**Source deck:** `/Users/brendantoole/projects3/reference/20260325_Commercial Strategy_Market Analysis_vS.pptx` (168 slides, 88 native charts)
**Audience:** the next agent, who will convert **a lot** of source slides into the reference corpus.

This doc has two parts: **(A)** a log of what this session changed (charts), and **(B)** an
operational playbook for bulk conversion. For the deep converter internals and the full chart
write-up, see the companion `2026-06-24_converter_and_chart_idiomatic_handoff.md` (esp. §3 and §8).

---

## PART A — Session log (what changed this session)

The open thread from the prior session was *"how should charts become idiomatic — bundle them
verbatim, or rebuild them from data with a factory?"* **Resolved.** A third way — **data-over-template**
— turned out to be strictly best, and it's now the converter's default.

### Shipped
- **`deck_core/charts.py`** — two new public functions (+ helpers), placed after `editable_bundled_chart`:
  - `extract_chart_data(chart_xml)` → `{categories, series:[{name,values,color}], value_axis_max, gap_width, overlap, types}`.
  - `styled_chart(template_xml, data, embed_bytes, *, embed_ext="xlsb")` → keeps the source chart
    part as the **exact style template**, rewrites only its data caches from `data`, then reuses
    `editable_bundled_chart` to reattach the workbook. Render is byte-identical to the source; the
    values now live in Python.
- **`_tools/convert_slide.py`** — extracts chart data (stdlib mirror) and emits `_CHART*_DATA`
  literals + `CHARTS = [styled_chart(...)]`. Auto-falls back to `editable_bundled_chart`, then to a
  raw `{"chart_xml": …}`, if data/.xlsb can't be recovered. Import line reflects actual usage.
- **Modules regenerated** through the new converter: `cost_comparison_automation` (slide 104) and
  `ships_act_volume_by_type` (slide 59) — each now carries a readable `_CHART0_DATA` literal.

### Verified
- Regenerated deck vs. the bundled baseline: **pixel-identical** (PIL bbox-of-difference `None`,
  mean abs diff `0.0000`) on both chart slides; all chart rels resolve; embeds present.
- Side-by-side proof saved: `_qa/chart_bundled_vs_styled.pptx` (slides 1/3 bundled, 2/4 styled).

### The decision, settled
- **No combo (bar+line) factory is needed.** `styled_chart` is type-agnostic — it reproduces the
  slide-59 bar+line combo that a factory cannot build — so the factory path (R3) is not worth
  building. `column_chart`/`bar_chart`/etc. remain useful only for *from-scratch* simple charts.
- The one thing `styled_chart` leaves templated is per-series **color/axis style** — exactly the
  "huge style" you want kept verbatim, not re-expressed in Python.
- Caveat (in the docstring): the reattached workbook is the source's, so editing `_DATA` updates the
  render but not PowerPoint's "Edit Data" pane until the workbook is regenerated. Fine for the corpus.

Memories written: `styled-chart-data-over-template`, and `pptx-to-idiomatic-module-workflow` updated.

---

## PART B — Bulk conversion playbook

### B0. The goal (don't lose the plot)
Build a **curated reference corpus**: source slides ported **1:1** into `deck_core` modules that
(a) render faithfully and (b) read like hand-authored `deck_core` code, so future agents study them
as worked examples. **Strategic intent:** if this works, the user phases out house-style-specific
primitives and just points agents at these modules. So the converter emits **general** primitives
that reproduce the source — **faithfulness > house-style conformance.** Don't "improve" the source;
reproduce it.

### B1. Where things live
```
projects/commercial_strategy_reference/deck_commercial_strategy/
├── build_deck.py                  # python3 build_deck.py -> the .pptx
├── _tools/convert_slide.py        # THE CONVERTER (stdlib-only; do not add deck_core imports)
├── _qa/                           # renders + proof artifacts (NOT built into the deck)
└── deck_commercial_strategy/
    ├── lib.py                     # build bindings
    └── slides/
        ├── __init__.py            # SLIDE_RENDERS registry — order = output order
        ├── _src/                  # verbatim chart parts (chartNN.xml + .xlsb) the modules read
        └── *.py                   # one module per converted slide
```
Engine is the workspace-root `deck_core/` package (charts.py, primitives.py, style.py, lib.py).

### B2. Convert one slide
```bash
cd projects/commercial_strategy_reference/deck_commercial_strategy/_tools
SRC="/Users/brendantoole/projects3/reference/20260325_Commercial Strategy_Market Analysis_vS.pptx"
python3 convert_slide.py "$SRC" <N> \
    --out ../deck_commercial_strategy/slides/<module_name>.py \
    --src-dir ../deck_commercial_strategy/slides/_src \
    --module-name <module_name> --layout slideLayout4
# (add --units emu to emit raw EMU instead of IN()/PT(); inches is the default and is fine)
```
Pick a `<module_name>` that's a snake_case gist of the slide title (e.g. `addressable_demand`,
`build_price_comparison`). The converter prints a stats line — sanity-check `chart=`, `table=`,
`raw=`, `dropped=`.

### B3. Register it (so it builds)
Edit `deck_commercial_strategy/slides/__init__.py`:
1. add `<module_name>,` to the `from . import ( ... )` block (keep the `# src N: …` comment style);
2. add `(<module_name>, <module_name>.render),` to `SLIDE_RENDERS` — **list order = slide order in
   the output deck.** Keep entries in source-slide order so the corpus reads coherently.

### B4. Build + QA (do this every batch; keep the deck green)
```bash
cd projects/commercial_strategy_reference/deck_commercial_strategy
python3 build_deck.py            # expect: wrote …  (K slides, M charts)
```
**(a) Rels must resolve** — PowerPoint silently *repairs* dangling `r:id` (soffice ignores them, so a
clean soffice render is NOT enough). Check every chart part:
```python
import zipfile, re
OUT="…/20260325_Commercial Strategy Market Analysis (reference port)_vS.pptx"
z=zipfile.ZipFile(OUT); names=z.namelist()
for c in sorted(n for n in names if re.match(r'ppt/charts/chart\d+\.xml$',n)):
    refs=set(re.findall(r'r:(?:id|embed)="([^"]+)"',z.read(c).decode()))
    rels=c.rsplit('/',1)[0]+'/_rels/'+c.rsplit('/',1)[1]+'.rels'
    defined=set(re.findall(r'Id="([^"]+)"',z.read(rels).decode()))
    assert refs<=defined,(c,refs-defined)
print("all chart rels resolve")
```
**(b) Render-and-look** (this is the real QA — no diff harness):
```bash
pkill -9 soffice; sleep 1
PROF="file:///tmp/lo_profile"                  # fresh profile dodges stale locks
soffice=/Applications/LibreOffice.app/Contents/MacOS/soffice
"$soffice" --headless --norestore -env:UserInstallation=$PROF --convert-to pdf --outdir /tmp "OUT.pptx"
pdftoppm -png -r 150 /tmp/OUT.pdf /tmp/page      # then open the new pages and eyeball
```
**(c) Compare to the source slide.** Render the *source* deck once for reference (source slide N =
PDF page N) and eyeball the converted page against it. For a numeric check, PIL
`ImageChops.difference(a,b).getbbox()` over same-size PNGs (`None` = identical) — but exact match only
happens when the source slide is already pure native shapes; most slides differ slightly (fonts,
think-cell vector text) and that's fine. Judge by eye.

### B5. What the converter does for you (so you know what to expect, and what to fix by hand)
- **native `<c:chart>`** → `styled_chart(_CHART*_TPL, _CHART*_DATA, _XLSB*)`; chart part + .xlsb
  copied to `_src/`; data emitted as a `_CHART*_DATA` literal. Multi-chart slides get
  `_CHART0/_CHART1/…` and graphic_frames at `rId2, rId3, …`. **Charts are never factory-rebuilt.**
- **think-cell OLE frame** ("… data — do not delete") + its **EMF preview `<p:pic>`** → dropped.
- **`<a:fld>`** think-cell fields → frozen to static `run()`s from cached text.
- **clusters** (≥3 shapes sharing a style) → a module-level data table + a loop (generic names like
  `_LABELS`, `_VALUE_LABELS`, `_LEGEND_SWATCHES`).
- **chrome** (breadcrumb / title / Preliminary chip / sources) → house builders, **but only within
  0.1″ of the house position** — otherwise kept verbatim so nothing moves.
- **native tables** (`<a:tbl>`) → low-level `table()/trow()/tcell()`, merges via `grid_span`/`row_span`,
  per-cell fill/borders/insets preserved. (NOT `house_table` — per the phase-out plan.)
- **colors** → `schemeClr`+lumMod/etc. baked to hex; exact `deck_core.style` token matches emitted as
  the token, off-palette as quoted hex.
- **raw fallback** → gradient/pattern/picture fills, custGeom, geometry-less placeholders emitted as a
  verbatim OOXML string (`# RAW verbatim`; dangling-ref cruft stripped, id renumbered).

### B6. Two-stage workflow
1. **Convert** (mechanical, faithful) — the command above. Get it building + rendering right first.
2. **Refactor** (optional, semantic) — rename the generic cluster vars to meaningful names, group
   related anchors, add a short module docstring line about the exhibit. Re-render after — must look
   identical. Do this for hero slides; skip for bulk if time-boxed.

### B7. Gotchas / watch-outs
- **Dangling rels → PowerPoint "repair" dialog.** Always run the B4(a) rels check. soffice will look
  fine even when PowerPoint would repair. (memory: `pptx-port-dangling-rels-cause-powerpoint-repair`)
- **soffice stale lock / hang.** `pkill -9 soffice` and use a fresh `-env:UserInstallation=file://…`
  profile every render.
- **The converter is stdlib-only on purpose** ("copy next to any pipeline"). Do **not** add
  `from deck_core …` imports to `convert_slide.py`; its chart extractor is a deliberate stdlib copy of
  `deck_core.charts.extract_chart_data`. If you change one, change both.
- **Chrome kept verbatim** when >0.1″ off the house position — that's intentional faithfulness, not a
  bug. Don't force it into a house builder if it would move.
- **Raw residue is expected.** Two kinds of non-idiomatic output exist: (1) the templated chart parts
  in `_src/` (by design), (2) RAW shapes for fills `text_box` can't express (e.g. a `ltDnDiag`
  pattern-fill swatch — slide 59 has one). Leave them; note them.
- **Tables expand in LibreOffice.** Row height is a *minimum*; wrapped cells grow. If a table overflows
  in the render, that's a layout reality — pin neighbors to a fixed bottom edge if needed.
  (memory: `house-table-row-height-is-a-minimum`)
- **`_DATA` series count must equal the template's series count** (the converter guarantees this; only
  a concern if you hand-edit `_DATA` without editing the template — `styled_chart` raises if they
  diverge).
- **think-cell stores chart data transposed** (series-as-rows; categories/series-names absent from the
  chart, drawn as separate slide text boxes). So `_CHART*_DATA` usually has `"categories": None` and
  unnamed series — that's correct, not a miss.

### B8. Source-deck inventory (plan your batches)
Scan captured this session for slides **2–110** (rerun the script below for **111–168**, not captured).
Counts are `chart / table` graphicFrames per slide.

**Confirmed chart-bearing slides ≤110:** 13(×2), 14, 15, 16(×4), 17(×4), 19, 26(×3), 32, 33, 34(×5),
42, 43, 44, 45, 46, 47, 51, 52, 53, 54, 55(×4), 56(×4), 59✓, 60, 61, 62(×2), 67, 70, 71, 72, 96, 97,
102(×3), 103(×3), 104✓, 109, 110.  (✓ = already done.)

**Table-heavy slides ≤110** (good warm-ups — no chart path): 2, 4✓, 5, 8, 9, 10, 12, 18, 20, 24, 27(×6),
30, 31, 36–39, 41(×6), 49, 65, 66, 73, 76, 77, 78, 79, 80, 82, 86, 92, 95, 98, 99, 101, 105, 106.

**Already in the corpus:** 3 (diagram), 4 (timeline table), 59 (combo chart), 104 (stacked chart).

Regenerate the full inventory (incl. 111–168) with this stdlib scan:
```python
import re, zipfile
from xml.etree import ElementTree as ET
SRC="/Users/brendantoole/projects3/reference/20260325_Commercial Strategy_Market Analysis_vS.pptx"
A="http://schemas.openxmlformats.org/drawingml/2006/main"; P="http://schemas.openxmlformats.org/presentationml/2006/main"
C="http://schemas.openxmlformats.org/drawingml/2006/chart"
def q(n,t): return f"{{{n}}}{t}"
z=zipfile.ZipFile(SRC)
for sf in sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$",n)),
                 key=lambda n:int(re.search(r"\d+",n.split('/')[-1]).group())):
    no=int(re.search(r"\d+",sf.split('/')[-1]).group()); r=ET.fromstring(z.read(sf))
    nc=sum(1 for g in r.iter(q(P,"graphicFrame")) if g.find(".//"+q(C,"chart")) is not None)
    nt=sum(1 for g in r.iter(q(P,"graphicFrame")) if g.find(".//"+q(A,"tbl")) is not None)
    ti=next(("".join(t.text or "" for t in sp.iter(q(A,"t"))) for sp in r.iter(q(P,"sp"))
             if (sp.find(".//"+q(P,"ph")) is not None and sp.find(".//"+q(P,"ph")).get("type") in ("title","ctrTitle"))), "")
    if nc or nt: print(f"{no:>4}  chart={nc} table={nt}  {' '.join(ti.split())[:60]}")
```

### B9. Suggested approach for "a lot of slides"
1. **Smoke-test first.** Convert 2–3 untouched slides (one table-only, one single-chart, one
   multi-chart e.g. 34 or 102) to a throwaway `--out`, confirm they parse and — once registered —
   build + render. This catches any converter edge case before you commit to volume. (I was about to
   do this when the session ended; it has *not* been run, so do it.)
2. **Batch by deck section** (the deck is sectioned: Key Findings, Demand, Build Cost, Economics,
   Autonomy, …). Convert a section, register all, build once, eyeball all new pages, fix, move on.
   Keep the deck building green after every batch.
3. **Order:** warm up on table/text slides, then single-chart, then multi-chart/combo. The chart path
   is proven (59, 104); tables and clusters are where surprises live.
4. **Don't over-refactor during bulk.** Get faithful renders first (stage 1). Do the semantic rename
   pass (stage 2) only on the slides that matter, or in a later cleanup sweep.
5. **Log residue.** For each slide note any RAW shapes or dropped frames in the module docstring (the
   converter already emits a stats line + "Converter notes"). That's the corpus's honesty.

### B10. Known limitations (don't chase these unless asked)
- `text_box` has no `pattern_fill=` param → pattern-fill swatches stay RAW. A small primitive
  extension would make them idiomatic.
- Pictures (`<p:pic>` real images) are emitted as a `TODO` drop — wire via `IMAGES = [...]` +
  `picture(...)` if a slide needs a real image (see `lib.py` build_pptx docstring + snippets "images").
  Several slides have `pic` counts >1 (e.g. 31 has 26 — likely icons); check before converting those.
- `styled_chart` doesn't sync PowerPoint's "Edit Data" to an edited `_DATA` (render follows `_DATA`,
  workbook doesn't). Only matters if someone edits the literal and reopens Edit Data. A future
  `embed_bytes=None` regenerate path could fix it (must also rewrite `<c:f>` refs for the transposed
  think-cell layout) — not currently needed.

### B11. Files touched this session (state for the next agent)
- `deck_core/charts.py` — **modified** (added `extract_chart_data`, `styled_chart`, helpers; import
  line). Public API otherwise intact; existing factories untouched.
- `_tools/convert_slide.py` — **modified** (chart extractor + styled_chart emission + docstrings).
- `slides/cost_comparison_automation.py`, `slides/ships_act_volume_by_type.py` — **regenerated**.
- `_qa/chart_bundled_vs_styled.pptx` — **new** proof artifact.
- Both handoff docs — updated. Nothing committed to git (the whole project dir is untracked).
