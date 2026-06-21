# 2026-06-03 — Slide-spec format standard + engine image wiring

## Scope

Two pieces of work, one session:

1. **Authored a standardized slide-spec format** under a new `docs/spec_format/`
   (`SPEC_FORMAT.md` + two worked examples). These are **proposals** — no existing
   `slide_specs/*.md` were migrated. Reached the final shape by reconciling a
   build-facing draft from a second (engine-only) AI agent against a leanness pass,
   then iterating with the user.
2. **Fixed a real engine gap: images/logos are now wired by the build.** Edited
   `deck_core/lib.py` (+ `primitives.py` docstring, `slide_snippets.md`). This was an
   **explicit, authorized core change** (the locked-core rule yields when the task is
   to change the engine).

Preceded by a read-only audit of both decks' slide specs (content + format). The only
other repo change was deleting one orphaned spec. No VCS in this workspace, so the
safety net is: both `build_deck.py` exit 0 and a throwaway image-wiring test (since
removed).

## 0. How the task evolved (user decisions)

- Started as a **rename** task (align `slide_specs/*.md` names to `slides/*.py`
  modules). Finding: **names already match 1:1** in both decks — nothing to rename.
  (Corrected an early over-reach where I started building missing slide modules; the
  user clarified the task was rename-only, then pivoted to format design.)
- `projects/submarines/deck/slide_specs/appendix_basic_construction_backup.md` — the
  module was deliberately removed earlier; user confirmed **delete the spec**. Done.
- Pivot: design a **standardized spec format** whose consumer is a *future AI agent*
  translating spec → OOXML module. Specs are handoff files.
- Detailed typography / object-level styling is **wanted** (makes spec→OOXML
  mechanical), expressed in the engine's own token/factory vocabulary — not dropped.
- `tables`/`charts`/`shapes`/`images` are **required-if-present** (omit if absent;
  fully specified when present).
- `commentary.reserve` is **mandatory** (body/appendix) and should be **ample** — a
  two-layer "density bank" so a later agent can raise information density without
  re-research.
- The format doc must be **domain-neutral, version-less, and standalone** (no
  defense/market-sizing examples, no "v1.x" label, no changelog) so future agents
  aren't misled. Concrete domain content lives only in the two example files.
- **Images/logos must be supported** by the format — which surfaced that the engine
  didn't actually wire images. → fix the engine.

## 1. Audit findings (read-only)

- **Three inconsistent spec formats existed:** DDG (21 files, uniform ALL-CAPS template
  w/ a keyed `*-CONTRACT` block + internal/visible source split); submarines body
  (17 files, light Title-case template); submarines appendix (9 files, heavy template
  with `OBJECT-LEVEL STYLE PLAN` / `TYPOGRAPHY PLAN` / literal EMU coords /
  `IMPLEMENTATION NOTES FOR THE AGENT`). The subs heavy-appendix template was the most
  translation-ready and became the north star.
- Spec filenames already match module basenames 1:1 in both decks (DDG specs carry an
  `sNN_` prefix only in their *internal* `MODULE NAME:` text, not the filename).

## 2. The standard — `docs/spec_format/`

Three new files; nothing else in the repo references them yet.

- **`SPEC_FORMAT.md`** — the format definition. Domain-neutral, version-less, standalone.
- **`example_ddg_sam_scenarios.md`** — worked spec: ranked bar chart **and** an inclusion
  matrix table (exercises required-if-present on both).
- **`example_submarines_bucket_tam.md`** — worked spec: chart-only with `tables: []`
  (the conditional rule from the other side) + a full two-layer reserve bank.

Key structural decisions baked in:

- **Single `element_inventory` registry** is the *only* place position / prominence /
  paint-order live. Exhibit blocks reference element `id`s (`frame_element`,
  `title_element`, `element`) instead of repeating `region`. Kills the "describe each
  object 5×" duplication.
- **Closed BODY-relative region grammar** — `{x,y,w,h}` from a fixed vocabulary
  (`%` of BODY, `BODY_*` edges, sibling refs `right_of()`/`below()`/`align_top()`/
  `body_until()`, named constants `GAP`/`NOTE_H`/`TITLE_BAND_H`, sizes
  `remaining`/`fit_content`). **No absolute slide EMUs**, no vague prose.
- **Chrome maps 1:1 to module symbols:** `_SECTION`/`_TOPIC`/`_TAKEAWAY`/`_SOURCES`
  (underscore-private) and `LAYOUT`/`CHARTS`/`IMAGES` (public attrs the builder reads).
  `prelim_chip` + slide numbers are automatic → **not** spec fields.
- **Chart → rId is positional:** `chart_index 0 → rId2`, `1 → rId3` (per `lib.py`).
- **Tables:** column widths are **ratios** the builder resolves to EMU (`col_w_emu_override`
  optional after a probe pass); cell `size` is **single-source** (hundredths; row heights
  derive `size_pt = size/100`); `house_table` skin/aligns/cell-maps required when a table
  exists.
- **Sources policy (no "footer" — just `sources`):** exact, ready-to-go **real external
  citations** only; required on body/appendix. Internal provenance (workbook tabs, chart
  IDs, wiki chapters) lives only in `meta.inputs` / per-datum `tie_out` / reserve
  `evidence` and is **never** rendered.
- **`reserve` = two layers:** `context` (ample prose reservoir, absorbs old speaker
  commentary) + `approved_extra_points` (region-tagged, priority-tiered, source-tagged,
  ~8–12 drop-in chips).
- **Images/logos** are first-class: a `picture` element type + an `images[]`
  required-if-present block; "no logos" is a *project convention*, not a format limit.

## 3. Engine change — image/logo wiring in `deck_core`

Before: `build_pptx(images=…)` copied bytes into `ppt/media/` but **did not** add the
slide relationship → a `<p:pic>` referencing an unwired `rId` triggered PowerPoint's
"repair" on open. (Content-types for png/jpg/jpeg/svg/emf were already declared.)

`deck_core/lib.py` — images now wire symmetrically to charts:

- A slide module declares `IMAGES = [{"rId": "rIdN", "file": "<name in ppt/media>"}, …]`
  and draws with `picture(sp_id, name, "rIdN", x, y, cx, cy)`. The build appends the
  per-slide rel `(rId, "image", "../media/<file>")`.
- **Image rIds continue after chart rIds** (no charts → first image `rId2`; one chart →
  `rId3`). New accumulator `declared_images` + a post-media validation pass.
- **Fails loudly** on: malformed `IMAGES` entry; `rId` colliding with the layout / a
  chart / another image; or a declared `file` not present in `ppt/media/`.
- Docstrings updated (module header + `build_pptx` `images:` param).

`deck_core/primitives.py` — `picture()` docstring updated to describe the `IMAGES`
auto-wiring (the function body was already correct; it was just never wired).

`deck_core/slide_snippets.md` — the `images` section no longer says "not wired yet, use
`_draft_slot`"; it now documents the working `IMAGES` + `picture()` pattern, the
rId-after-charts rule, supported extensions, and the loud-failure behavior.

## 4. Verification

- **Image wiring test** (throwaway script, now deleted): a 1-slide deck with
  `IMAGES=[{"rId":"rId2","file":"image2.svg"}]` + `picture(...,"rId2",...)` → asserted the
  `relationships/image` rel with `Target="../media/image2.svg"` in
  `slide1.xml.rels`, the media part packaged, the svg content-type present, `r:embed="rId2"`
  in the slide, and both XML parts well-formed. Three misuse paths (missing file,
  colliding `rId1`, malformed entry) each raised a clear `ValueError`.
- **No regression:** both decks rebuild identical to baseline — DDG **20 slides / 7
  charts**, submarines **25 slides / 5 charts** (neither declares `IMAGES`, so
  `getattr(mod,"IMAGES",[])` → `[]`).
- `import deck_core.lib, deck_core.primitives` clean after the docstring edits.

## 5. Files touched

- **Deleted:** `projects/submarines/deck/slide_specs/appendix_basic_construction_backup.md`
- **Created:** `docs/spec_format/SPEC_FORMAT.md`,
  `docs/spec_format/example_ddg_sam_scenarios.md`,
  `docs/spec_format/example_submarines_bucket_tam.md`
- **Modified (core):** `deck_core/lib.py` (image rel-wiring + validation + docstrings),
  `deck_core/primitives.py` (`picture()` docstring), `deck_core/slide_snippets.md`
  (`images` section)
- **No other existing specs or slide modules changed.** Session memories were written
  outside the repo under `~/.claude/.../memory/` (scope-discipline; spec-format project).

## 6. Notes / leftovers

- **Specs not migrated.** The 47 existing specs still use the three old formats; the
  standard is a proposal. Migration is a separate pass when the user is ready.
- **Unbuilt body slides remain.** Both decks still have specced-but-unbuilt S12–S16
  (DDG: `sam_scenarios`, `supplier_landscape`, `ffata_visibility_gap`, `market_direction`,
  `implications`; subs: `work_type_taxonomy`, `bucket_tam`, `sam_scenarios`,
  `visible_suppliers`, `sib_exclusion`). Not built this session (out of scope). Subs has a
  written-but-unregistered `divider_sam_supplier.py` to wire in when that section lands.
- **Optional core token.** A `TABLE_DENSE_9_5PT = 950` token in `style.py` would remove
  the one "tokens-only" exception (dense 9.5pt tables currently use a raw `950`). Noted,
  **not** applied — it's a separate locked-core change.
- **Engine edits vs docs.** The `deck_core` image-wiring edits and the `docs/spec_format/`
  docs landed in the same session; offered to split the engine edits onto their own branch
  for isolated review if preferred (no VCS here, so this is a manual concern).
