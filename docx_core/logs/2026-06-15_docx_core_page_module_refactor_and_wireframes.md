# 2026-06-15 — docx_core: page-module refactor, spec mode dropped, wireframe toolkit

Follow-on to `2026-06-15_docx_core_word_pipeline_engine_and_spec_mode.md`. Same-day
refactor of the new Word engine to make its public vocabulary match the slide/sheet
siblings, remove the spec-specific surface from the shared core, and add a real
wireframe/diagram toolkit. Stdlib-only throughout; the build stays the only strict
layer, the probe stays read-only ("never builds, repairs, or judges").

Planned + approved via plan mode (`~/.claude/plans/i-want-you-to-greedy-shore.md`).
Three user decisions (AskUserQuestion): **clean rename, no back-compat aliases**;
**all three wireframe layers incl. DrawingML**; **delete spec_blocks entirely and
rewrite the demo as generic/wireframe pages**. Blast radius confirmed first: exactly
one consumer pipeline, zero tests.

Demo: `projects/distributed_shipbuilding/doc/`
Output: `projects/distributed_shipbuilding/20260615_Distributed Shipbuilding_Build Spec_vS.docx`
Build:  `cd projects/distributed_shipbuilding/doc && python3 build_doc.py`

---

## 1. Vocabulary — the authoring unit is now the PAGE MODULE (clean rename)

Word "section" (`<w:sectPr>`) is kept as the internal mechanism; the author-facing
unit is the page module, mirroring slide/sheet module-first pipelines.

- `specs.SectionSpec` → **`PageModuleSpec`** (field `section_props` → `page_setup`);
  `DocumentSpec.sections` → `pages`. Added **`PageEntry(title, render)`** — the
  `workbook_core.SheetEntry` analog — so one source file can register several pages.
- `sections.py` → **`page_setup.py`**; `SectionProps` → **`PageSetup`** with a new
  `start` field (`nextPage|continuous|oddPage|evenPage`) emitting `<w:type>` as the
  **first** `<w:sectPr>` child. `SECTION_REPORT`/`SECTION_LANDSCAPE_TABLE` →
  **`PAGE_PORTRAIT`/`PAGE_LANDSCAPE`**; added `PAGE_PORTRAIT_NARROW`.
- `lib.package_docx(out, page_modules, …)` (was `document_modules`). Added
  `_is_entry`/`_item_render`/`_page_title` (ported from workbook_core) so the loop
  accepts a bare module OR a `PageEntry`; title precedence = spec.title → module
  `PAGE_TITLE` → filename stem. Prints "N page(s)".
- **No aliases** — the single consumer was updated in the same pass (house style:
  workbook_core keeps zero back-compat aliases).

## 2. Spec mode removed from the core

- **Deleted `spec_blocks.py`** (SlideSpecBlock / SheetSpecBlock / CommentaryItem /
  ChartSpec / TableSpec / render_*_spec_section).
- `style_ids`: `P_SPEC_HEADING/FIELD_LABEL/BODY` → generic
  **`P_BLOCK_HEADING`/`P_FIELD_LABEL`/`P_COMPACT_BODY`**; styleId strings + style.py
  size tokens (`BLOCK_HEADING_PT`/`COMPACT_BODY_PT`) renamed to match.
- New **`structured_blocks.py`** — the generic replacement (recommended look for
  structured docs, not "spec writing"): `field_block`, `card_block`,
  `checklist_block`, `definition_list`. Imports primitives + style_ids only.

## 3. Wireframe toolkit — `wireframes.py` (three layers)

- **A — ASCII.** `ascii_block(text, small=)` → monospace paragraph (one `<w:r>` per
  line + `<w:br/>`, `xml:space="preserve"`). New `P_CODE`/`P_CODE_SMALL` styles
  (`Courier New`, added `MONO` token to style.py).
- **B — table-grid.** `wire_table(rows, col_widths_twips=)` / `wire_cell(…)` on a new
  `T_WIREFRAME` table style. `primitives.tcell()` extended (backward-compatibly) with
  `grid_span` (`<w:gridSpan>`), `borders` (per-side `<w:tcBorders>` via
  `_tc_borders_xml`), `v_align` (`<w:vAlign>`); tcPr child order locked.
- **C — DrawingML shapes.** `shape_box` / `shape_line` (flipH/flipV for negative
  vectors, `a:tailEnd` arrows) / `shape_label` (no-fill box) / **`canvas(children,
  w_in=, h_in=)`** with frozen `CanvasBox`/`CanvasLine`. canvas groups via `wpg:wgp`
  with an **identity child coordinate system** (`chOff=0,0`, `chExt=w,h`) so child
  inches map 1:1. `ooxml.py` gained `NS_WP/NS_A/NS_WPS/NS_WPG` (declared on the
  `<w:document>` root, NOT in `mc:Ignorable`); `units.py` gained `EMU_PER_PT` +
  `emu_from_in/pt`.
- **The repair-avoidance contract** (encoded once): `mc:AlternateContent` →
  `mc:Choice Requires="wps"` → `w:drawing` → `wp:inline`/`wp:anchor` → `a:graphic` →
  `a:graphicData uri=` NS_WPS (shapes) / NS_WPG (canvas), with a minimal VML
  `mc:Fallback` (what real Word writes). Child order is fixed in the builders:
  `wp:inline` = extent→effectExtent→docPr→cNvGraphicFramePr→graphic; `wps:wsp` =
  cNvPr?→cNvSpPr→spPr→txbx?→bodyPr; `wps:spPr` = xfrm(off→ext)→prstGeom→fill→ln;
  `wp:anchor` adds simplePos/positionH/V + a wrap element. Shape text is real `<w:p>`
  (via primitives) inside `wps:txbx`/`w:txbxContent`. `wp:docPr id` from a module
  monotonic counter. (Word free-floating shapes use `wps:wsp`, not PowerPoint's
  `p:sp` — only the DrawingML geometry/fill/text idioms were reused from deck_core.)

## 4. Probe — inventory the new concepts (still read-only, no judgment)

- `sections` rollup → **`page_setups`** (size/orient/margins kept).
- `spec_blocks` rollup → generic **`structured_block_headings`** (P_BLOCK_HEADING).
- New **`drawings`** inventory: per `<w:drawing>` report kind (inline|anchor), name
  (`wp:docPr@name`), extent (`wp:extent` cx/cy). Search scoped to `mc:Choice` (skips
  `mc:Fallback`) so the VML fallback is never double-counted — verified ElementTree
  traverses `mc:*` as ordinary elements (no ns registration); docPr/extent attrs are
  unprefixed. Added `ascii_blocks` (P_CODE/P_CODE_SMALL) and `wire_tables`
  (T_WIREFRAME) counts. No scoring/lint/blocking.

## 5. Authoring kit + demo

- `__init__.py` docstring, `doc_base_template.py`, `doc_guide.md`, `doc_snippets.md`
  reframed around page modules + structured_blocks + the three wireframe layers
  (ASCII → table-grid → DrawingML guidance), with the honest caveat that a page
  module is the atomic unit, not a one-physical-page guarantee (Word repaginates).
- Demo migrated: `sections/` → `pages/`, `DOCUMENTS` → `PAGES`. Deleted
  `slide_specs.py`/`sheet_specs.py`; added `build_register.py` (structured_blocks
  re-expression of the old build contracts) and `process_map.py` (landscape, exercises
  all three wireframe layers — ASCII sketch + DrawingML canvas + table-grid matrix).
- **Per user request**, the pipeline package was renamed
  `doc_consolidated` → **`doc_distributed_shipbuilding`** (dir + imports + docProps
  creator/app). Sibling `deck_consolidated`/`workbook` packages untouched.

---

## Verification (structural; Word not assumed — user opens to eyeball)

- Build green, 4 pages; `zipfile.testzip()` is `None`; all 10 parts present; every
  `word/*.xml` + `docProps/*.xml` parses with ElementTree.
- 5 original WordprocessingML traps still hold; plus `<w:type>` is first in every
  `<w:sectPr>` (sectPr count == 4 pages).
- DrawingML: `graphicData@uri` valid (NS_WPG for the canvas); `wpg:wgp` identity
  `chOff/chExt`; `wp:docPr` id unique; `mc:Choice Requires="wps"` + `mc:Fallback`
  present; root declares wp/a/wps/wpg.
- Probe works both modes: module (`doc_distributed_shipbuilding.pages.process_map` →
  1 drawing, 1 ASCII block, 1 wireframe table, landscape page setup) and file (the
  built `.docx` → 48 paragraphs, 4 page setups, drawing extent reported in EMU).
  Reports under `projects/distributed_shipbuilding/doc/reports/doc_probe/`.
- Grep confirms zero dangling old names (SectionSpec/SectionProps/SECTION_*/
  spec_blocks/SlideSpecBlock/SheetSpecBlock/P_SPEC_/DOCUMENTS/document_modules) and
  zero `doc_consolidated` references in source.

## Notes / follow-ups

- Word fields remain off the roadmap (no `fldChar`/`instrText`); wireframes introduce
  no fields. See memory `docx-no-word-fields`.
- The demo `canvas` is inline (flows between paragraphs). Anchored shapes (free X/Y,
  `wp:anchor`) are implemented and smoke-tested but not yet exercised by the demo.
- Still deferred (unchanged from the prior log): images/media parts, footnotes,
  headers/footers, comments, hyperlinks, native charts, content controls, tracked
  changes, `spec_check.py`.
- Verification is structural only (unzip + parse + probe); the user visually verifies
  by opening in Word (no headless render, per house convention).
