# 2026-06-15 — docx_core: slide-mock wireframe convention (pptx slide → Word page)

Follow-on to today's three docx_core logs (`..._word_pipeline_engine_and_spec_mode`,
`..._page_module_refactor_and_wireframes`, `..._review_cleanup_pass`). Adds a
documented convention + thin tooling for **wireframing a real pptx slide inside a
Word document**: reproduce the slide at the deck's true 16:9 proportions, carry
every planned word, and annotate the layout/objects below it on one page.
Stdlib-only throughout; the build stays the only strict layer, the probe stays
read-only.

No plan-mode pass — scope was settled in conversation. Two user decisions
(AskUserQuestion); the rest followed the house guidance pattern read off the two
sibling pipelines (`deck_core`, `workbook_core`).

Demo: `projects/distributed_shipbuilding/doc/`
Output: `projects/distributed_shipbuilding/20260615_Distributed Shipbuilding_Build Spec_vS.docx`
Build:  `cd projects/distributed_shipbuilding/doc && python3 build_doc.py`

---

## Motivation

The existing `pages/jump_balls.py` (one ASCII slide on a generic `PAGE_LANDSCAPE`
page) "almost" read like a slide but mismatched the deck: Letter landscape is
11 × 8.5 (aspect 1.29), not 16:9. The ask was to make slide-mock pages first-class
and faithful, with three rules.

## User decisions (AskUserQuestion)

1. **Page geometry = slide-width, taller page.** The page keeps the deck's
   13.333 in width but is taller (13.333 × 10.5), so the 16:9 slide rides on top
   and the layout/object annotation sits below it on the **same** page.
   (Rejected: Letter-landscape + scaled 16:9 box; and exact-slide-page +
   separate annotation page.)
2. **Code surface = guidance + presets + a thin helper.** Not guidance-only;
   add small reusable builders, but no new module / no bespoke object schema.

## Deck dimensions — confirmed at source

Read straight from `deck_core/style.py:29-31`: `SLIDE_W = 12_192_000`,
`SLIDE_H = 6_858_000` EMU (914,400 EMU/in) → **13.333 × 7.5 in, 16:9** (the file
comment says so). The deck has **no 4:3** anywhere, so the planned `PAGE_SLIDE_4x3`
preset was dropped as overfit-in-reverse; `slide_canvas(ratio=…)` stays
parameterized (16:9 default) but only 16:9 page presets ship.

---

## Changes

### Core engine

- **`page_setup.py`** — added provenance constants `SLIDE_16x9_W_IN = 13.333` /
  `SLIDE_16x9_H_IN = 7.5` (annotated as `deck_core` `SLIDE_W`/`SLIDE_H`), a thin
  `_SLIDE_MARGINS` (0.3 in sides, 0.2 in header/footer), and two presets:
  - `PAGE_SLIDE_16x9` — exact full-bleed slide page (13.333 × 7.5, landscape).
  - **`PAGE_SLIDE_16x9_TALL`** — 13.333 × 10.5 landscape; the recommended
    slide-mock page (slide on top, annotation below). Sits next to
    `PAGE_PORTRAIT`/`PAGE_LANDSCAPE`/`PAGE_PORTRAIT_NARROW`; the landscape
    normalizer keeps the long edge as `w:w`.
- **`wireframes.py`** — two helpers appended after `canvas`, plus a docstring
  pointer and extended imports (`bullets`, `P_FIELD_LABEL`):
  - `slide_canvas(children, *, ratio="16:9", w_in=12.5, …)` — a `canvas()` whose
    `h_in` is **derived** from `w_in` (`_SLIDE_RATIOS = {"16:9": 9/16, "4:3": 3/4}`),
    so the region stays proportion-correct and child inches map 1:1. Raises
    `ValueError` on an unknown ratio.
  - `slide_frame(slide, *, layout, objects, layout_label="Layout",
    objects_label="Objects")` — concatenates the slide block(s) + a subordinate
    annotation block (a `P_FIELD_LABEL` heading then `bullets(...)`, twice:
    layout/grid first, then object inventory). Accepts one block or a list;
    returns a `list[str]` to splice into a body with `*`.
  - **`ratio` lives on `slide_canvas` only** (where it sizes the region); it was
    deliberately *not* added to `slide_frame` to avoid a no-op param, even though
    the AskUserQuestion preview sketched it there.

### Authoring kit

- **`doc_guide.md`** — new `### Slide mocks (wireframing a pptx slide)` subsection
  under §7, encoding the three rules:
  1. **Carry all the planned copy** — every word on the real slide appears in the
     wireframe; if it won't fit, shrink type or compress copy, but **within the
     deck copy law** (`target_copy.txt`: STRUCTURE / TEXT MECHANICS / TYPOGRAPHY)
     — lead with the point, keep `$XXM`/`%`/`~` and acronyms, no process talk;
     never silently drop an element.
  2. **Mirror the slide proportions** — `PAGE_SLIDE_16x9_TALL` +
     `slide_canvas(ratio="16:9")` (exact-page variant: `PAGE_SLIDE_16x9`).
  3. **Annotate layout + objects** — `slide_frame(...)`, high-level, not a
     re-transcription of the copy the slide region already carries.
- **`doc_snippets.md`** — new §8 copy-from recipe (a Pattern-A worktype slide:
  dark title band, left exhibit placeholder, right commentary card, source line +
  the layout/object annotation).

### Demo

- **`pages/slide_mock.py`** (new, registered as page 2 in `pages/__init__.py`) —
  a worktype-mix slide drawn as a DrawingML `slide_canvas` (title band /
  exhibit / commentary card / source line) wrapped by `slide_frame`. **Bonus:**
  this re-covers the canvas/DrawingML path the cleanup log flagged as no longer
  exercised by the live demo. `jump_balls.py` stays the pure-ASCII example.

**Deliberately not done (overfit guard):** no new module, no build-time
enforcement of copy fidelity (stays soft guidance + probe territory, per the
"build is strict-OOXML-only" rule), no bespoke object schema, no 4:3 page preset.

---

## Verification (structural; Word not assumed — user opens to eyeball)

- Build green, 2 pages; `zipfile.testzip()` is `None`; all 10 parts present;
  every `word/*.xml` + `docProps/*.xml` parses with ElementTree.
- Slide-mock page emits `<w:pgSz w:w="19200" w:h="15120" w:orient="landscape"/>`
  = **13.333 × 10.5 in** (19200 = round(13.333 × 1440)); 0.3 in margins (432 twips).
  Page 1 (jump_balls) stays 15840 × 12240 = 11 × 8.5 landscape.
- Slide drawing extent **11,430,000 × 6,429,146 EMU = 12.5 × 7.031 in = exactly
  16:9** (h derived from w). One `<w:drawing>`, `mc:Choice Requires="wps"` +
  `wpg:wgp` (NS_WPG), unique `wp:docPr id`. Both `<w:sectPr>` lead with `<w:type>`.
- Probe both modes: module (`…pages.slide_mock` → 1 drawing 'Slide', page setup
  19200 × 15120, 2 `FieldLabel` + 7 list paragraphs) and file (built `.docx` →
  2 page setups, 1 ASCII block + 1 drawing). Reports under
  `projects/distributed_shipbuilding/doc/reports/doc_probe/`.
- Helper unit checks pass: 16:9 extent derivation, bad-ratio `ValueError`,
  single-block vs list `slide` arg, exact-vs-tall page heights.

## Notes / follow-ups

- **Judgment call:** annotation labels use `P_FIELD_LABEL` (bold, matches the
  `structured_blocks` field pattern) rather than `P_CAPTION` (italic gray). Easy
  one-line switch if a lighter annotation is wanted.
- **Wireframe limitation:** a `CanvasBox` text box renders uniform weight, so the
  commentary card's "bold lead + bullets" pattern (`target_copy.txt`) isn't
  bolded per-line inside the slide region — the wireframe shows the copy; the
  annotation describes the treatment. Acceptable for a mock.
- The cleanup log's one open item — a real Word-open confirming the DrawingML
  layer triggers **no repair dialog** — is now at least exercised by the live
  demo again (the slide-mock canvas), but still needs the user's eyeball to
  confirm. Verification here remains structural only (unzip + parse + probe).
- Word fields remain off the roadmap (no `fldChar`/`instrText`); slide mocks add
  none. See memory `docx-no-word-fields`.
