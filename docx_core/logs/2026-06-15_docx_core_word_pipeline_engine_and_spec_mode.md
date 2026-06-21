# 2026-06-15 — docx_core: new Word (.docx) build pipeline — lean engine + artifact-spec mode

New top-level core library: `docx_core/` — the third sibling of `deck_core`
(.pptx) and `workbook_core` (.xlsx). Stdlib-only hand-built WordprocessingML +
`zipfile`, mirroring the existing house architecture.

Demo pipeline: `projects/distributed_shipbuilding/doc/`
Output:        `projects/distributed_shipbuilding/20260615_Distributed Shipbuilding_Build Spec_vS.docx`
Build:         `cd projects/distributed_shipbuilding/doc && python3 build_doc.py`
Probe:         `python3 docx_core/doc_probe.py <module-or-.docx> [--json] [--out-dir DIR]`
(System `python3` is 3.9; the engine is stdlib-only so it runs on it directly.)

Design source: a long design transcript the user had with another agent,
`/Users/brendantoole/projects3/word doc.rtf` (read in full), plus the official
slide-spec template `/Users/brendantoole/projects3/slide_spec_template.md`.
Planned + approved via plan mode (`~/.claude/plans/i-want-you-to-vast-harp.md`).

---

## Scope (user decisions via AskUserQuestion)

- **Lean engine + spec mode.** Phase-1 plain-document engine (named styles,
  rhythm/margins, bullet/numbered/outline lists, rule-tables, sections, packager,
  read-only probe) + spec mode. **Deferred:** images, footnotes/endnotes,
  headers/footers, comments, hyperlinks, native charts, content controls, tracked
  changes, `spec_check.py`.
- **Spec mode = slides + sheets, both first-class. NO sidecar files** — spec
  blocks render into the Word document only; no JSON/customXml written anywhere.
- **Demo attached under `projects/distributed_shipbuilding/`** as a `doc/`
  sibling of `deck/` and `workbook/` (package `doc_consolidated`, mirroring
  `deck_consolidated` / `workbook_consolidated` at the same path depth).

---

## Architecture (mirrors the two existing cores)

Authoring unit = an ordered **section/block stream**, not pages (Word paginates
at render time). A section module's `render()` returns a `SectionSpec`; the
packager concatenates section bodies into `word/document.xml`. Acyclic import
direction:

```
ooxml <- {style, units} <- {style_ids, rhythm} <- {styles, numbering, sections}
      <- specs <- primitives <- spec_blocks <- lib
```

Files created in `docx_core/`:

- `ooxml.py` — leaf: `XML_DECL` + WordprocessingML namespace constants
  (`NS_DOCUMENT` for the `<w:document>` root incl. `mc:Ignorable="w14"`, `NS_WR`
  for styles/numbering/settings/fontTable).
- `style.py` — pure tokens: `FONT="Arial"` (house font, not Word's Calibri),
  BLUE/GRAY ramps (mirror deck), type scale, `hp()` (pt→half-points).
- `units.py` — `twips_from_pt/in`, `line_auto(mult)` (240/276/360).
- `style_ids.py` — semantic style IDs (`P_BODY`, `P_H1/2/3` named `Heading1/2/3`
  so the nav pane/outline recognize them, `R_STRONG`, `T_RULE`, `T_DARK_HEADER`,
  spec styles `P_SPEC_HEADING/FIELD_LABEL/BODY`).
- `rhythm.py` — `ParaRhythm`/`PageMargins` dataclasses + presets (R_BODY 1.15
  line/6pt after, R_H1/2/3, PAGE_MARGINS_REPORT). The margins+spacing layer.
- `styles.py` — manifest dataclasses (`RunProps`/`ParaProps`/`ParagraphStyle`/
  `CharacterStyle`/`TableStyle`) → `build_styles_xml(style_overrides=None)`. Emits
  `docDefaults` → the three type defaults (Normal/DefaultParagraphFont/TableNormal/
  NoList) → paragraph/character/table styles. `style_overrides` is re-skin data.
- `numbering.py` — `build_numbering_xml()` (bullet/numbered/outline; `NUMID_*`
  constants are the author-facing contract).
- `sections.py` — `SectionProps.to_sectpr_xml()` + presets `SECTION_REPORT`,
  `SECTION_LANDSCAPE_TABLE`.
- `specs.py` — `SectionSpec(body, section_props, title)`, `DocumentSpec`.
- `primitives.py` — `run/paragraph/heading/bullet/bullets/numbered/outline_item/
  caption/page_break/bookmark_*/tcell/trow/table/table_block/document` + escaping.
  Rule-table is the default table posture.
- `spec_blocks.py` — `SlideSpecBlock` (+ `CommentaryItem/ChartSpec/TableSpec`) and
  `SheetSpecBlock`, with `render_slide_spec_section` / `render_sheet_spec_section`.
- `lib.py` — `package_docx(out_path, document_modules, *, title, creator,
  app_name, style_overrides=None)`. Owns all OPC parts; ports `package_workbook`'s
  module-resolution + ValueError-on-collision + named builders, and `build_pptx`'s
  OPC content-type guard.
- `__init__.py` — module-role + import-direction docstring (code-free, like
  `workbook_core/__init__.py`).
- `doc_probe.py` — read-only inspector, module + file mode, Markdown+JSON,
  "never builds, repairs, or judges."
- `doc_base_template.py`, `doc_guide.md`, `doc_snippets.md` — authoring kit.

`.docx` archive (10 parts): `[Content_Types].xml` (first), `_rels/.rels`,
`docProps/{core,app}.xml`, `word/document.xml`, `word/_rels/document.xml.rels`,
`word/{styles,numbering,settings,fontTable}.xml`.

---

## Spec mode

- **`SlideSpecBlock`** reproduces `slide_spec_template.md` **verbatim** — heading
  literals are module constants so they can't drift: `SLIDE ## - NAME`, `Type:`,
  `Slide's purpose:`, `TITLE`, `HIGH-LEVEL LAYOUT`, `COMMENTARY COPY, IF NEEDED`
  (per-item Copy + Text/shape treatment), `OTHER VISIBLE COPY, IF NEEDED`,
  `CHART, IF NEEDED` (Copy/data/labels/chips, Purpose, Structure, Text/visual
  treatment, Fit behavior), `TABLE, IF NEEDED` (same shape), `OBJECT NOTES,
  IF NEEDED`, `SOURCES`. Filled mode (empty optional fields omitted).
- **`SheetSpecBlock`** mirrors the real `sheet_specs/*.md` shape: header
  (`{Tab Name}` / `Tab color · group` / `Module:`), `Purpose`, `Reads`, `Feeds`,
  `On the sheet` (§N), `Sources`, `Checks`.
- Both render to Word paragraphs only — **no JSON sidecar** (per the user).
  One spec block per page (page break between blocks).

---

## Demo program

`projects/distributed_shipbuilding/doc/` — `build_doc.py` launcher +
`doc_consolidated/{__init__.py (sys.path bootstrap), lib.py (OUT/title/creator),
sections/}`. Four registered sections: `overview` (answer-first brief),
`findings` (dark-header rule table = the boundary register), `slide_specs`
(2 `SlideSpecBlock`: Sizing Boundary, Reachable Market — drawn from the real
submarines `sizing_boundary` slide spec), `sheet_specs` (1 `SheetSpecBlock`:
SAM Build — from the real ddg `model_sam_build` sheet spec).

---

## Verification (structural; Word not assumed)

- Build green; `zipfile.testzip()` is `None`; all 10 expected parts present;
  every `word/*.xml` + `docProps/*.xml` parses with ElementTree.
- The 5 high-risk WordprocessingML traps all confirmed in the emitted XML:
  1. final `<w:sectPr>` is the **last child of `<w:body>`**; mid-doc breaks ride
     inside a paragraph's `<w:pPr>` (sectPr count == 4 sections).
  2. element child-order (pPr/rPr/style) encoded once in the dataclass serializers.
  3. numbering linkage resolves (every `numId` → `num` → `abstractNum`;
     abstractNum before num).
  4. styles floor: `docDefaults` present, `Normal w:default="1"`, headings named
     `heading 1/2/3`.
  5. OPC guard: every part content-typed (the build raises otherwise).
- `doc_probe.py` works in both modes: module mode
  (`doc_consolidated.sections.slide_specs` → 2 spec blocks detected) and file mode
  (the built `.docx` → 81 paragraphs, 1 table `T_DARK_HEADER`, 4 sections, styles
  resolved back to their `style_ids` names). Probe report written under
  `projects/distributed_shipbuilding/doc/reports/doc_probe/`.

---

## Post-build fixes (this session)

1. **Removed the "update fields?" prompt.** Word showed *"This document contains
   fields that may refer to other files…"* on every open. Cause: a speculative
   `<w:updateFields w:val="true"/>` in `build_settings_xml()` (added for a future
   TOC/page-number field). The MVP emits **no fields at all**, so the flag was
   pure downside. Removed it; the doc now has zero field codes (no `fldChar` /
   `instrText` anywhere in `docx_core`). Decision recorded: **don't build Word
   field capability** (TOC/page-number/cross-ref) — see memory `docx-no-word-fields`.
   (Note: `spec_blocks.py`'s "field" naming = spec *form-field labels* like
   `Copy:`/`Purpose:`, plain bold text — unrelated to Word fields.)
2. **Bullet/list indentation fix.** Bullet glyphs were sitting flush with the
   parent paragraph at the margin (`_ind` used `left=360 hanging=360` → glyph at
   twip 0). Matched the house reference doc
   `/Users/brendantoole/projects3/Federal_Award_API_Research_Methodology.docx`
   (top-level bullet = `left=720 hanging=360`, glyph at 0.25in / text at 0.5in;
   nested levels step 360 → 720/1080/1440). Updated `numbering.py::_ind` to
   `_LEVEL0_LEFT=720` + `_LEVEL_STEP=360`; applies to bullets, numbered, outline.

---

## Notes / follow-ups

- Each registered section currently starts on a **new page** (default next-page
  section break between modules). Reads well for a spec doc; flagged that a
  "continuous" section type is a one-line change if flowing report prose is wanted.
- Deferred phases (per scope): images/figures, footnotes, headers/footers,
  comments, hyperlinks, native charts, content controls, tracked changes,
  `spec_check.py` (compare spec to slide_probe/sheet_probe). **Word fields are
  dropped from the roadmap entirely** (the one exception that would reintroduce a
  field is footer page numbers — raise it only if the user asks).
- Verification is structural only (unzip + parse + probe); the user visually
  verifies by opening in Word (no headless render, per house convention).
- `style_overrides` is wired through `package_docx` → `build_styles_xml` as
  re-skin data but unused by the demo; first real use will be a per-program brand
  color / heading scale.
