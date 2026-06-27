# Session log & handoff — pattFill + custGeom go first-class, and the provenance bug is fixed

**Date:** 2026-06-24 (latest session; continues the three docs already in this `logs/` folder)
**Project:** `projects/style_library/`
**Engine touched:** `deck_core/primitives.py` (workspace-root package)
**Converter touched:** `_tools/convert_slide.py`
**Decks regenerated/retrofitted:** the `ships_act_captive_demand` (CS src 60) and `freight_charges` (CS src 134) modules in **both** `archetypes/schematics/` (staging) and `archetypes/schematics_curated/` (curated)

This session closed the two open items the prior handoff flagged in its §6 ("Findings / open
items for the next agent" in `2026-06-24_curated_corpus_and_inline_primitives.md`):

1. **Converter provenance bug** — every emitted module docstring hardcoded "Commercial Strategy
   deck", mislabeling the Navy modules.
2. **The real fix for the verbatim residue** — add `pattern_fill=` to `deck_core.text_box` and a
   `custom_geometry()` primitive, then teach the converter to emit them, so pattFill/custGeom are
   idiomatic for *all* future modules instead of per-module inline `_pattern_swatch`/`_glyph`
   helpers.

Then, by user decision, **(3)** the two curated modules that carried those inline helpers were
**retrofitted** to use the new core primitives.

All three are shipped and verified. No PNG render pass was run (standing user preference: halt and
let the user eyeball — memory `awards-deck-visual-qa`). Nothing committed to git (project dir is
untracked).

---

## 1. The provenance fix (`convert_slide.py`)

New top-level `derive_provenance(z, src_pptx, deck_name_override=None) -> (deck_name, date_str)`,
called inside `convert()` and threaded through `build_module_text()`. Resolution order:

1. **explicit `--deck-name`** CLI override (new arg) wins;
2. else the **source filename**, which follows `YYYYMMDD_<name>_<version>.pptx`: strip the leading
   `YYYYMMDD` (kept as `date_str`) and a trailing version tag, turn `_` into spaces;
3. else **`docProps/core.xml` `<dc:title>`** (fallback only — both reference decks have an *empty*
   title, so the filename is what actually drives it).

The version-tag stripper is `re.sub(r"[_\s-]+v(?:\d[\d.]*|[A-Z])\s*$", "", rest)` — deliberately
narrow so it eats `_vS` / `_v2.1` / `_v3` but **not** a real word like `_value` / `_version`
(verified with edge cases). The docstring first line changed from
`{module} - Commercial Strategy deck, source slide N.` to
`{module} — {deck_name} deck ({date}), source slide N.` (em-dash, matching the curated convention).

Resolved names (verified):
| source file | deck_name | date |
|---|---|---|
| `20260325_Commercial Strategy_Market Analysis_vS.pptx` | `Commercial Strategy Market Analysis` | `20260325` |
| `20251120_Market sizing_Navy (Surface incl MDA)_v2.1.pptx` | `Market sizing Navy (Surface incl MDA)` | `20251120` |
| `20251201_Market sizing_Navy (Undersea)_v1.6.pptx` | `Market sizing Navy (Undersea)` | `20251201` |

---

## 2. The two new primitives (`deck_core/primitives.py`)

Both are **general** (not house-specific), backward-compatible, and now part of the public surface
(module docstring updated). They are the "real fix" the prior handoff wanted — what used to be
RAW-OOXML residue (and then per-module inline helpers) is now a first-class call.

### 2a. `text_box(..., pattern_fill=None, ...)`
A new keyword-only param. When set it emits an `<a:pattFill>` instead of solid/no fill:
```python
text_box(n(), "swatch", x, y, cx, cy, [paragraph([])],
         pattern_fill={"prst": "ltDnDiag", "fg": "scheme:tx1", "bg": "scheme:bg1"},
         line_color="none", anchor="ctr")
```
- `pattern_fill` is `{"prst": <DrawingML pattern name>, "fg": <color>, "bg": <color>}`.
- `prst` is a pattern preset: `ltDnDiag`, `dkUpDiag`, `pct50`, `wdDnDiag`, … (the think-cell swatch
  is `ltDnDiag`).
- `fg`/`bg` accept a **6-char hex** OR a **`"scheme:NAME"`** theme ref (e.g. `scheme:tx1`); they
  default to `scheme:tx1` (dark) on `scheme:bg1` (light) — the think-cell standard. The
  `_fill_clr_xml()` helper renders the right `<a:schemeClr>`/`<a:srgbClr>`.
- It **overrides** `fill`, and counts as "filled" for the AUTO black-border house rule (so pass
  `line_color="none"` for a borderless swatch, as the converter does).

### 2b. `custom_geometry(sp_id, name, x, y, cx, cy, geom, *, fill=None, line_color="none", line_width=12700, rot=0)`
A `<p:sp>` whose outline is an arbitrary `<a:custGeom>` path — bézier/line art no preset `prst` can
express (think-cell status icons, logos, vector marks).
```python
custom_geometry(n(), "Haken, check", IN(8.302), IN(4.264), IN(0.3), IN(0.3),
                _GEOM_CHECK, fill="2E7D32")
```
- `geom` is the **verbatim `<a:custGeom>...</a:custGeom>` XML string** — the intrinsic path data
  (`gdLst`/`pathLst`) cannot be parameterized, so lift it from the source into a module-level
  constant and **dedupe** identical paths into ONE constant.
- The path's own coordinate space (`<a:path w=… h=…>`) scales to the `cx`/`cy` box, so position and
  **size** are parameters here, along with `fill` (hex or None) and `line` (default `"none"` — these
  marks are fill-only, unlike text_box's filled-border rule).
- The shape carries **no text** (empty body). Use `text_box` for anything text-bearing.

**The design split that makes this "faithful + idiomatic":** the *intrinsic geometry stays verbatim*
(a constant), and *everything around it reads as Python* (pos/size/fill/line as args). This is the
same philosophy as `styled_chart` (data-over-template): keep the un-expressible part verbatim,
surface the rest.

---

## 3. The converter now emits them (`convert_slide.py`)

- **`parse_sp` no longer bails pattFill/custGeom to RAW.** `gradFill`/`blipFill` still go raw (no
  param form). A `<a:pattFill>` is parsed by `_parse_pattfill()` into `rec["pattern_fill"]`
  (`{"prst","fg","bg"}`, fg/bg kept symbolic as `scheme:tx1`/`bg1`). A `<a:custGeom>` is captured
  (after the text body is parsed) into `rec["custgeom"]` via `_elem_inner_xml()` — **but only if the
  shape is text-free and has no pattern fill**; otherwise it stays RAW (the safety net survives).
- **`render_sp`** emits `pattern_fill={...}` when present.
- **`is_simple`** excludes pattern_fill/custgeom shapes from clustering (the cluster machinery only
  varies x/y/cx/cy/fill/line/text/geom_adj and would drop the pattern/path), so they emit as
  standalone calls.
- **Dedup:** `convert()` collects unique `custgeom` strings into `_GEOM0`, `_GEOM1`, … module
  constants (first-encounter order), each with a `# source: "<name>" xN` comment, and the body emits
  `custom_geometry(n(), name, …, _GEOMk, fill=…)`. (`freight_charges`' 5 icons → 2 constants.)
- **`_imports`** adds `custom_geometry` when used; `pattern_fill` needs no import (it's a kwarg).
- **Stats:** new `custom_geometry=` counter in the printed line and the module docstring; the
  docstring prose now mentions both new paths. Helper refactor: `_strip_ns_decls()` is shared by
  `raw_literal` and the new `_elem_inner_xml`.

### Re-run results (into **staging**, the regenerable dir — never `--out` at curated)
```
slide 60  ships_act_captive_demand:  text_box=13 ... custom_geometry=0 raw=0   (was raw_verbatim=1)
slide 134 freight_charges:           text_box=10 ... custom_geometry=5 raw=0   (was raw_verbatim=5)
```
Both now **raw=0**.

---

## 4. Curated retrofit (the chosen follow-up)

The two curated modules (`archetypes/schematics_curated/.../{ships_act_captive_demand,freight_charges}.py`)
previously carried the inline `_pattern_swatch` / `_GLYPH_CHECK`+`_GLYPH_CROSS`+`_glyph` helpers
documented in `2026-06-24_curated_corpus_and_inline_primitives.md` §5. Those are now **gone**,
replaced by the core primitives:
- `ships_act_captive_demand`: the `ltDnDiag` swatch is a `text_box(pattern_fill=…)` reusing the
  module's `_SWATCH_W/_SWATCH_H`. (No import change — `pattern_fill` is a kwarg.)
- `freight_charges`: the check/cross icons are `custom_geometry()` over two named path constants
  `_GEOM_CHECK` / `_GEOM_CROSS`, with shared `_GLYPH_X = IN(8.302)` / `_GLYPH_SZ = IN(0.3)` anchors.
  `custom_geometry` added to the imports.

The retrofit was done with a **self-asserting Python script** (extracts the verbatim `<a:custGeom>`
substring straight out of the old `_GLYPH_*` literals so the path bytes can't drift; `assert`s each
textual swap matched exactly once; guards that no `_glyph`/`_GLYPH_CHECK`/`_GLYPH_CROSS` residue
remains). Each module's docstring CODE MAP, stats line, and honesty note were updated — the note now
says the module was "retrofitted to the … primitive; paint order is unchanged and the render is
verified equivalent" (the old note claimed byte-identical-to-raw-port, which a primitive swap breaks;
honesty matters for the corpus).

**The faithfulness gate shifts for an intentional primitive swap.** The curated convention's
"byte-identical produced XML" gate (companion doc §4) is for *names/comments-only* hand-polish. A
deliberate implementation swap (inline blob → core primitive) changes bytes by design, so the gate
becomes **render-equivalence**, verified structurally (see §5). Coordinates move only by the
corpus-wide 3-decimal-inch rounding (sub-0.05px), same tradeoff every `IN()` coord already makes.

---

## 5. Verification (no PNG; structural + build + rels)

The method, given the "halt for human eyeball" preference, was build-green + rels + **structural
faithfulness against the source slides** — strong enough to trust the render without a diff harness:

- **Primitives smoke-tested in isolation**, including feeding `custom_geometry` a real `<a:custGeom>`
  lifted from source slide 134 and round-tripping it (well-formed; path embedded verbatim).
- **Both decks build green** (staging + curated, 13 slides / 3 charts each).
- **All slide + chart rels resolve** in both outputs (mandatory — PowerPoint silently *repairs*
  dangling `r:id`; soffice won't catch it. memory `pptx-port-dangling-rels-cause-powerpoint-repair`).
- **pattFill** (slide with "SHIPS Act Captive Demand"): `('ltDnDiag','tx1','bg1')` matches source
  slide 60; swatch position within inch-rounding (Δ ≈ 140/76 EMU < 0.01in).
- **custGeom** (slide with "Freight Charges"): 5 shapes, 2 unique, paths **byte-identical to source**
  slide 134 via `ET.canonicalize` (C14N); fills `2E7D32`×2 (check) + `C00000`×3 (cross).
- **Curated retrofit isolation:** snapshotted the pre-retrofit curated build, rebuilt after — **only
  slide5 + slide8 changed**; the other 11 are byte-identical (proves the engine change didn't
  perturb anything else).
- **Backward-compat:** the engine change is additive (`pattern_fill=None`, new fn) — for existing
  callers the AUTO-border logic reduces to its old form; the frozen curated deck and a Navy-slide
  regression conversion both pass.

---

## 6. Files touched

- **`deck_core/primitives.py`** — added `text_box(pattern_fill=)`, `custom_geometry()`,
  `_fill_clr_xml()`; module-docstring public surface updated. Backward-compatible.
- **`_tools/convert_slide.py`** — `derive_provenance()` + `--deck-name`; `_parse_pattfill()`;
  `_elem_inner_xml()` + `_strip_ns_decls()` (shared with `raw_literal`); pattFill/custGeom parse in
  `parse_sp`; `pattern_fill=` in `render_sp`; cluster exclusion in `is_simple`; `_GEOM*` dedup +
  `custom_geometry` emission + `custgeom` stat in `convert()`/`build_module_text()`; `custom_geometry`
  in `_imports`; provenance threaded into the docstring.
- **`archetypes/schematics/schematics/slides/{ships_act_captive_demand,freight_charges}.py`** —
  regenerated through the new converter (staging, raw=0).
- **`archetypes/schematics_curated/schematics/slides/{ships_act_captive_demand,freight_charges}.py`**
  — retrofitted to the new primitives (curated).
- **Memory** `pptx-to-idiomatic-module-workflow` — updated (pattFill/custGeom now first-class;
  provenance fix). Backups of all four pre-edit modules + the curated baseline slides are in this
  session's scratchpad.

---

## 7. For the next agent

- **Converting more slides is unchanged** — `styled_chart` is still the chart default, and now
  pattFill → `text_box(pattern_fill=)` and custGeom → `custom_geometry()` happen automatically. You
  should rarely see RAW residue anymore; if you do, it's gradFill/blipFill, a *textful* custGeom, or
  a custGeom+pattFill combo (all still kept verbatim on purpose).
- **Authoring by hand:** reach for `text_box(pattern_fill=…)` for any hatch/dot swatch and
  `custom_geometry()` for any freeform path. Keep each unique `<a:custGeom>` in one module constant
  and pass position/size/fill as args.
- **`--deck-name`** is there if a source file doesn't follow the `YYYYMMDD_name_version` convention.
- **Still open (low priority, from the prior handoff):** the converter could emit a richer
  auto-docstring (a per-slide reading guide) before hand-polish; and the `styled_chart`
  `embed_bytes=None` workbook-regenerate path (only needed if "Edit Data" must follow an edited
  `_DATA`). Neither was touched this session.
- **Related docs:** `2026-06-24_converter_and_chart_idiomatic_handoff.md` (charts/converter internals),
  `2026-06-24_curated_corpus_and_inline_primitives.md` (curated corpus + the now-superseded inline-
  helper technique), `2026-06-24_session_log_and_bulk_conversion_handoff.md` (bulk-conversion
  playbook). Memories: `[[pptx-to-idiomatic-module-workflow]]`, `[[styled-chart-data-over-template]]`,
  `[[pptx-port-dangling-rels-cause-powerpoint-repair]]`, `[[awards-deck-visual-qa]]`.
