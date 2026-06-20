# doc_core — authoring guide

`docx_core` is the third sibling of `deck_core` (.pptx) and `workbook_core`
(.xlsx): a stdlib-only WordprocessingML engine. This guide is the human-facing
mirror of the rules; the machine-readable mirror is the code. Like the other
cores, **the build enforces valid OOXML, the guide recommends readable document
design, and the probe reports what actually shipped** — `doc_probe.py` never
judges taste.

## 1. Building a page module

1. Copy `docx_core/doc_base_template.py` to `doc_<program>/pages/<name>.py`.
2. Write the one-sentence INTENT, set `PAGE_TITLE`.
3. Build `_body()` from imported builders (`primitives`, `structured_blocks`,
   `wireframes`); `render()` returns a `PageModuleSpec`.
4. Register the module in `doc_<program>/pages/__init__.py` `PAGES`.
5. Inspect: `python docx_core/doc_probe.py doc_<program>.pages.<name>`.

The authoring unit is the **page module**. It normally starts a new Word page and
owns that page's setup (margins, orientation, columns). It is **not** a guarantee
that the content fits on exactly one physical page — Word repaginates at render
time, and the probe reports what shipped. "Word section" (`<w:sectPr>`) is the
internal mechanism; you never hand-place one. One source file can register several
page modules with a `specs.PageEntry`, but one file per module is the common case.

## 2. Named styles carry the formatting

Pick a **style ID** (`docx_core.style_ids`); the look comes from `word/styles.xml`.
Normal prose needs no direct run formatting.

| Style | Role |
|-------|------|
| `P_BODY` | normal prose (the default body style) |
| `P_H1/2/3` | page / subsection / minor headings (claim-bearing) |
| `P_TITLE` | cover / document title |
| `P_CAPTION` | figure / table caption (small, italic, gray) |
| `P_SOURCE` | source / provenance note (small, gray) |
| `P_LIST` | list item (bullet / numbered / outline); tight list rhythm |
| `P_BLOCK_HEADING` / `P_FIELD_LABEL` / `P_COMPACT_BODY` | structured-block heading / bold label / tight body |
| `P_CODE` / `P_CODE_SMALL` | monospace block (ASCII wireframes) |
| `R_STRONG` / `R_EMPH` / `R_LINK` | bold lead phrase / italic qualifier / link |
| `T_RULE` | default evidence table (horizontal rules, no vertical grid) |
| `T_DARK_HEADER` | the one primary table (dark header, white text) |
| `T_WIREFRAME` | layout grid for table-grid wireframes (borders painted per cell) |

Local run overrides exist (`run("x", bold=True, color=...)`) but should *mean*
something — emphasis, a link, a one-off. Reach for a style first.

## 3. Rhythm (margins + spacing)

Spacing is part of the **paragraph style**, not an argument on every paragraph
(`docx_core.rhythm`). Body is 1.15 line / 6 pt after; headings get air above and
keep-with-next. Do **not** use empty paragraphs as spacers. Page margins live on
the page setup (`docx_core.page_setup`: `PAGE_PORTRAIT`, `PAGE_LANDSCAPE`,
`PAGE_PORTRAIT_NARROW`), not on paragraph styles.

## 4. Tables

The default table is a **rule table** (`table_block(...)`): bold header with a
bottom rule, horizontal row rules, **no vertical grid**. Put units in the
caption/header, fragments in cells, and a source line below. Reserve
`dark_header=True` (`T_DARK_HEADER`) for the one primary table on a page. Use
color as hierarchy, not decoration.

## 5. Lists

Lists are real Word numbering, not styled paragraphs: `bullets([...])`,
`numbered([...])`, `outline_item(text, level=n)`. The geometry (indent/hanging,
glyphs, 1/1.1/1.1.1 outline) lives in `docx_core.numbering`. Item **spacing**
rides on the `P_LIST` paragraph style (tight: single line, 2 pt after) so a list
reads as one block — list items never inherit body prose's 6 pt-after.

## 6. Structured blocks

For structured documents (build registers, requirement lists, field/value forms),
`docx_core.structured_blocks` gives a recommended look without committing to any
template vocabulary: `card_block(title, lines)`, `field_block(label, value)`,
`checklist_block(items, label=...)`, `definition_list(pairs)`. Each returns a list
of blocks, spliced into a body with `*`.

## 7. Wireframes (three layers)

`docx_core.wireframes` lets a page sketch logic and layout. Reach for them in this
order — power and cost increase down the list:

- **ASCII** (`ascii_block(text)`) — monospace diagrams; the fastest, most reliable
  way to sketch process maps, source→output maps, and first-pass logic.
- **Table-grid** (`wire_table(rows, col_widths_twips=...)`, `wire_cell(...)`) — Word
  tables used as a stable, editable layout engine; the default for boxes, lanes,
  matrices, and swimlanes (Word handles tables more consistently than floating
  shapes).
- **DrawingML shapes** (`shape_box`, `shape_line`, `shape_label`, and the recommended
  `canvas(children, w_in=, h_in=)` with `CanvasBox` / `CanvasLine`) — free-positioned
  polished boxes and connectors. Use only when the page genuinely needs free
  positioning; `canvas` groups shapes in an inch coordinate system that maps 1:1.

### Slide mocks (wireframing a pptx slide)

To wireframe a real slide, the page mirrors the **slide**, not a sheet of paper.
The deck is 16:9 at 13.333 × 7.5 in (`deck_core` `SLIDE_W` / `SLIDE_H`). Three rules:

1. **Carry all the planned copy.** Every word meant to appear on the real slide
   appears in the wireframe. If it does not fit, shrink the type or compress the
   copy — never silently drop a planned element. Compress *within the deck copy
   law* (`target_copy.txt`: STRUCTURE, TEXT MECHANICS, TYPOGRAPHY): lead with the
   point, keep `$XXM` / `%` / `~` notation and program acronyms, no process talk.
   The wireframe is a faithful copy deck, not a sketch with placeholder text.
2. **Mirror the slide proportions.** Use the `PAGE_SLIDE_16x9_TALL` page setup
   (keeps the deck's 13.333 in width, taller so the annotation rides below) and
   draw the slide region with `slide_canvas(children, ratio="16:9")` — it derives
   the height from the width so the region stays 16:9 and child inches map 1:1.
   (Use `PAGE_SLIDE_16x9` for an exact full-bleed slide page with no annotation.)
3. **Annotate the layout and objects.** Close the page with
   `slide_frame(slide, layout=[...], objects=[...])`: it places the slide region,
   then a subordinate block — the layout/grid first, then the object inventory —
   as concise bullets. Keep these high-level (what regions exist, what sits in
   each), not a re-transcription of the copy the slide region already carries.

The slide region can be any layer (a `slide_canvas`, a `wire_table` grid, or an
`ascii_block`); `slide_frame` only owns the placement and the annotation.

## 8. What the build enforces vs. recommends

**Hard build rules** (else the build raises / Word repairs):
- `render()` must return a `PageModuleSpec`.
- bookmark names must be unique (load-bearing; never auto-renamed).
- every packaged part has a declared content type (the OPC guard).
- schema child-order in `styles.xml` / `document.xml` / wireframe DrawingML
  (handled by the builders).

**Soft guidance** (the probe reports, never fails):
- prefer `P_BODY` over ad hoc formatting; prefer heading helpers.
- `T_RULE` for ordinary tables; `T_DARK_HEADER` sparingly.
- ASCII first, table-grid for stable diagrams, DrawingML only when needed.
- keep source notes small and gray; keep visible text human-report-native.

## 9. What the probe reports

`doc_probe.py` inventories paragraphs (style resolved to its `style_ids` name),
runs, tables, lists, bookmarks, **drawings** (kind/name/extent), **page setups**
(size/orientation/margins), and rollups (heading outline, source lines,
structured-block headings, ASCII/wireframe-table counts). Module mode renders a
page module; file mode parses a built `.docx`. It never lints, scores, or blocks.
