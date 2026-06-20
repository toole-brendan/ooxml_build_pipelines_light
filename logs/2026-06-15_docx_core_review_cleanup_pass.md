# 2026-06-15 — docx_core: review-driven cleanup pass (gridSpan, fossils, builtinId)

Follow-on to `2026-06-15_docx_core_page_module_refactor_and_wireframes.md`. An
external code review of the refactored core was triaged against the actual source
(not taken on trust); the endorsed subset was applied. Stdlib-only throughout; the
build stays the only strict layer, the probe stays read-only.

No plan-mode pass — small, well-scoped fixes. Three changes applied, two review
items deliberately rejected after verification.

---

## 1. gridSpan-aware table grid sizing — `primitives.py`

The table-grid bug the review flagged was real but narrower than stated. `table()`
sized `<w:tblGrid>` from `rows[0].count("<w:tc>")`, which (a) ignores `<w:gridSpan>`
and (b) only inspects the first row. **Blast radius:** `_even_grid` short-circuits
whenever `col_widths_twips` is passed, and both `wire_table()` and the demo always
pass explicit widths — so the malformed grid only occurred in the **auto-width
path** with a spanning/short first row. Nothing shipping hit it; fixed as hardening.

- New `_row_grid_cols()` (sums `<w:gridSpan w:val>` per `<w:tc>`, default 1) +
  `_table_grid_cols()` (max over **all** rows, not just `rows[0]`).
- `table()` now sizes the grid from `_table_grid_cols()`; when `col_widths_twips`
  is supplied it raises `ValueError` if fewer columns than the rows logically need
  (after gridSpan).
- Caveat encoded in a comment: the cell regex (`<w:tc\b.*?</w:tc>`, non-greedy)
  assumes **non-nested** rows; a cell holding a nested `<w:tbl>` would miscount.
  `<w:tcPr>` is correctly *not* counted (the `\b` after `tc` excludes it).

## 2. Section-language fossils swept — `lib.py`, `doc_probe.py`

Leftover "section" vocabulary that pulls future agents back to the pre-refactor
mental model:

- `build_app_props(section_titles=…)` → `page_titles`; the extended-properties
  HeadingPairs label `<vt:lpstr>Sections</vt:lpstr>` → `Page modules`. (Caller
  already passed `page_titles` positionally — no call-site change.)
- `doc_probe.py`: CLI `description` "Word section/.docx inspector" →
  "Word page-module/.docx inspector"; `_load_module` docstring "section module"
  → "page module".
- Left intentionally: the probe's `# … is a section break` comment and
  `page_setup.py`/`lib.py` prose that use "section" for the **OOXML `<w:sectPr>`
  mechanism** — that is the correct technical term, not a fossil.

## 3. builtinId claim corrected — `style_ids.py`

The module docstring claimed heading styles are tagged with matching
`w:builtinId`. `styles.py` emits **no** `<w:builtinId>` anywhere. Reworded to the
truth: nav pane / outline / TOC recognition comes from the reserved name
(`"heading 1/2/3"`), `custom=False`, and `<w:outlineLvl>` (which `styles.py:102`
does emit). Chose to soften the claim, not add builtinId emission — current
recognition already works (named built-in styles + outline level).

## Rejected review items (verified, not applied)

- **`PageSetup.start` docstring rewrite.** The review wanted "…causing the
  *following* module to begin on a new page." Per ECMA-376, `<w:type>` describes
  how *the current section* begins relative to the previous one, and the packager
  places module N's `PageSetup` in the sectPr that **terminates** module N's
  content (why the landscape demo lands on the right page). So `start` on module N
  governs how **module N itself** begins — the existing docstring ("the
  section-break type that introduces this module") is correct; the rewrite would
  attribute the type to the wrong section. Left as-is.
- **`wire_table()` auto-wrapping plain cells into `wire_cell()`.** The docstring
  already says plain values become "plain cells" (nothing false advertised), and
  auto-wrapping would remove the mixed plain/wireframe-cell escape hatch in a row.
  Left as-is.

---

## Verification (structural; Word not assumed)

- All four edited modules compile (`py_compile`).
- gridSpan unit check: spanning-first-row in auto-width mode → 3 `<w:gridCol>`
  (was 1); too-few explicit `col_widths_twips` → `ValueError`; single plain cell →
  1 `<w:gridCol>` (no `<w:tcPr>` false positive).
- Demo rebuilds green; `zipfile.testzip()` is `None`; 10 parts present; every
  `word/*.xml` + `docProps/*.xml` parses with ElementTree. `app.xml` shows the
  `Page modules` label and no `Sections`.
- `doc_probe.py` runs in file mode (built `.docx` → 1 paragraph, 1 ASCII block,
  landscape page setup) and `--help` shows the renamed description.

## Notes / follow-ups

- **Incidental (not from this pass):** the demo registry is now a single page,
  `pages/jump_balls.py` (landscape ASCII slide). The multi-page
  `process_map.py` / `build_register.py` from the prior log were replaced at some
  point, so the live demo no longer exercises the `gridSpan` / table-grid /
  DrawingML paths. The grid fix was covered by the standalone unit check above.
- **Still unproven (review's one valid open item):** a real Word-open to confirm
  the DrawingML layer triggers no repair dialog. No live demo path exercises it
  right now. Verification here remains structural only (unzip + parse + probe);
  the user visually verifies in Word (no headless render, per house convention).
