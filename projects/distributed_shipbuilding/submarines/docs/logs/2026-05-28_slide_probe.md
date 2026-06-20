# 2026-05-28 — slide_probe: read-only OOXML inspector

## Scope

First deck-tooling session that wasn't slide-content work. Built a
generic, read-only OOXML inspector script at
[sub_pptx/tools/slide_probe.py](../sub_pptx/tools/slide_probe.py) that
imports a slide module (or opens a built `.pptx`), parses the emitted
`<p:sld>` XML, and writes a Markdown + JSON inventory of every shape:
identity, geometry, fills, borders, text, fonts, anchors, insets, native
tables, chart frames, connector arrowheads, group-shape flattened
coordinates, plus OLE / thinkcell detection. Final state: ~1200 LOC
stdlib-only script, 22 fresh reports under `sub_pptx/reports/slide_probe/`
(11 module-mode + 11 file-mode against `sub.pptx`), and a 6-line pointer
section added to
[body_template.py](../sub_pptx/deck_submarines/slides/body_template.py).

Plan file:
`C:\Users\BrendanToole\.claude\plans\putting-you-in-plan-zany-lovelace.md`.

The motivation came out of the styling-review session's bug class
(doubled borders, overlapping fills, source-line drift, off-by-40k chip
overhang, sparse-vs-zero confusion in charts) — all of which traced back
to the agent having no deterministic way to see what was actually on
the rendered slide vs what the `DIMENSIONS` docstring claimed.

---

## 1. Scope decisions (plan phase)

Before any code, two scope decisions hardened around an explicit list of
non-goals:

- **No validation, lint, or pass/fail gates.** A pasted analysis from
  another agent suggested layering on a `validateLayout()` / `layout_lint.py`
  framework with rules like `OUT_OF_BOUNDS`, `OVERLAP`, `TEXT_OVERFLOW`,
  `LOW_MARGIN`. Rejected as overkill and the wrong shape of help — the
  agent doesn't need a judge, it needs a sensor. Inspector reports facts;
  judgment stays with the agent.
- **No docstring rewriting / sync mode.** Generated-block rewrites of the
  `DIMENSIONS` section would introduce merge noise and churn. Better to
  treat reports as canonical and let the docstring carry intent /
  rationale only.
- **No render-preview / PNG export.** Considered briefly, dropped.
- **Generic across pptx — not catered to sub_pptx's existing shapes.**
  User pushed back when I scoped the first exploration agent at
  cataloging constructs from the existing slide modules: "the helper
  should not be catered specifically to the slides that are already
  created." Re-scoped to drive the parser checklist from
  `ooxml_cheat_sheet_pptx.md` directly. Parser handles canonical pptx
  OOXML, not just constructs the deck currently uses.

CLI ergonomics decided via three `AskUserQuestion` items, all
"Recommended" accepted: location `sub_pptx/tools/slide_probe.py`
(keeps `deck_submarines/` as pure rendering, 4 primitives); both input modes
(module name OR `.pptx` file path, auto-detected by `.pptx` suffix);
text-estimate in v1 (stdlib-only crude estimator now, Pillow upgrade
later).

## 2. v1 architecture

Single file, stdlib only (`xml.etree.ElementTree`, `zipfile`,
`importlib`, `json`, `argparse`, `pathlib`, `dataclasses`). No
`python-pptx`, no `openpyxl`, no `lxml` — matches the rest of the build
pipeline.

Layered internally:

1. **Constants + qname helpers.** Namespace map for `p` / `a` / `r` /
   `c` / `cx` / `mc`; `_q(prefix, local)` builds `{ns}localname`. All
   element refs use these constants — never raw strings — so a typo
   surfaces at import time, not at parse time.
2. **Frozen dataclasses.** `TextRun`, `Paragraph`, `BodyPr`, `TextBody`,
   `Geometry`, `Fill`, `EndCap`, `Line`, `TableCell`, `TableProbe`,
   `ChartProbe`, `PictureProbe`, `OleProbe`, `CustGeomSummary`,
   `ShapeProbe`. Each layer mirrors an OOXML construct. `ShapeProbe`
   is the union — only the relevant payload field is populated per kind.
3. **Field-level parsers** — `_parse_xfrm`, `_parse_geometry`,
   `_parse_fill`, `_parse_line`, `_parse_end_cap`, `_parse_prst`,
   `_parse_color_in_rpr`, `_parse_run`, `_parse_paragraph`,
   `_parse_body_pr`, `_parse_text_body`, `_parse_table`,
   `_parse_table_border`, `_parse_placeholder`, `_identity`.
   Each is small, side-effect-free, and accepts `Element | None`.
4. **Shape parsers** — one per top-level shape kind: `_parse_sp`,
   `_parse_cxn_sp`, `_parse_pic`, `_parse_graphic_frame`. Each produces
   a fully-populated `ShapeProbe`.
5. **Walker** — `_walk_sp_tree` recursively descends `<p:spTree>` and
   any nested `<p:grpSp>`. Tracks z-order via a shared counter list
   (`counter = [0]` mutated across recursion). Handles
   `<mc:AlternateContent>` by descending into the first `<mc:Choice>`
   (falling back to `<mc:Fallback>` if no Choice) without consuming a
   z slot. Skips the root `<p:nvGrpSpPr>` / `<p:grpSpPr>` wrapper.
6. **Loaders** — `load_from_module` (importlib + `mod.render(page_num=1,
   total_pages=1)`) and `load_from_pptx` (zipfile + read
   `ppt/slides/slideN.xml` + rels + `presentation.xml` for `p:sldSz`).
   Both return a 5-tuple `(slide_name, sld_xml, rels, canvas, layout_target)`.
7. **Region summary** — derived from parsed shapes, no judgment: total
   shape count, by-kind histogram, top-most / bottom-most body object
   coordinates, OLE / thinkcell counts, chrome shape detection (sp_id
   matches against locked `CHROME_SP_IDS = {2: Breadcrumb, 3: Title,
   4: PrelimChip, 4500: PageNumber, 9999: SourcesLine}`).
8. **Renderers** — `render_markdown` (~250 lines, 8-9 sections per
   slide) and `render_json` (dataclasses serialized with custom
   `_text_body_to_dict` / `_table_to_dict` shims to handle nested
   tuples).
9. **Text estimator** — `estimate_text_fit` with `AVG_CHAR_WIDTH_RATIO
   = 0.50` for Arial-ish glyph width; greedy word wrap; height as
   `lines × font_pt × line_spacing / 72 × 914_400` EMU. No FAIL labels,
   just arithmetic + a `fits` boolean.
10. **CLI** — argparse: `target`, `--slide N`, `--text-estimate`,
    `--json`, `--all`, `--out-dir`. Auto-detection of `.pptx` suffix vs
    dotted module path.

## 3. Body template docstring update

Initial plan called for a ~25-line section in
[body_template.py](../sub_pptx/deck_submarines/slides/body_template.py) with CLI
examples and full usage explanation. User pushed back: "it should just
be text guidance with the file path directing anyone who reads the
docstring to previously run probe runs to the json or markdown - i
think if we include it in the docstring of the slide module it would
just take up too much space."

Replaced with a 6-line block: points at `sub_pptx/reports/slide_probe/<name>.{md,json}` as the
authoritative source for current slide geometry, contrasts that with the
docstring's DIMENSIONS block ("they are parsed from the emitted XML,
not maintained by hand"), names the script path for regeneration.
Confirmed deck still builds after edit (`python build_deck.py` runs
clean — body_template.py is imported transitively).

## 4. Stale-output wiping

User flagged that re-probing should fully replace prior outputs, not
stack: "every time the slide probe is run on a slide that has already
previously had a probe run on it - it should completely replace those
old results - they shouldn't stack - so as to reduce technical debt."

Added to `_probe_one` before any new file is written:

```python
for stale in out_dir.glob(f"{slide_name}.*"):
    try:
        stale.unlink()
    except OSError:
        pass
```

Per-slide wipe — doesn't touch unrelated reports in the same directory.
Verified: full run wrote `framing.md` + `framing.json`; subsequent
`--json` run wiped the stale `.md` and left only the fresh `.json`.

## 5. Four generic-pptx additions

Another agent's pasted analysis raised several "v2" concerns. Most
rejected (full inheritance / theme resolution, PackageReader class
split, extension list reporting, deck-specific profile layer — all
overkill or already chosen against). Four small additions accepted:

### 5.1 Rotation and flip on `a:xfrm`

`Geometry` dataclass gained `rot_deg`, `flip_h`, `flip_v`. Extracted in
`_parse_xfrm` from `@rot` (divided by 60_000 → degrees), `@flipH` /
`@flipV` (truthy strings). Propagated through every shape parser
(`_parse_sp`, `_parse_cxn_sp`, `_parse_pic`, `_parse_graphic_frame`,
and the `_walk_sp_tree` grpSp branch).

Markdown: new "Transformed shapes (rotation or flip)" section, only
emitted when anything qualifies. Includes a header note flagging that
absolute boxes in the z-order table are axis-aligned and ignore
rotation (per the other agent's recommendation — don't try to compute
the rotated visual footprint in v1).

JSON: `geometry` dict gains the three new fields.

### 5.2 `mc:AlternateContent` handling

Real-world pptx files (anything authored by recent Office) wrap newer
markup in `<mc:AlternateContent><mc:Choice>...</mc:Choice><mc:Fallback>...</mc:Fallback></mc:AlternateContent>`.
Before this change, the parser caught these as `kind="unknown"` and
stopped descending — the shapes inside would silently vanish.

Fix: in `_walk_sp_tree`, intercept `mc:AlternateContent` before the
z-counter increment. Descend into the first `<mc:Choice>` (preferred,
since Choice carries the newer markup that produced the file); fall
back to `<mc:Fallback>` if no Choice. Wrapper itself is not a visible
object — does not consume a z slot. Recursion is transparent: the
walker iterates the chosen branch's children as if they were direct
spTree siblings, so nested groups / further mc-wrappers handle
correctly.

Added `MC_ALTERNATE`, `MC_CHOICE`, `MC_FALLBACK` qname constants. Added
`mc` to the namespace map.

### 5.3 Image rId on shape fills

`<a:blipFill>` can appear inside `<p:spPr>` (background image on a
rectangle) or inside `<a:tcPr>` (table cell image), not only inside
`<p:pic>`. Previous code reported `kind="blip"` without the embed rId.

Fix: in `_parse_fill`, when seeing `<a:blipFill>`, drill into the
`<a:blip>` child and extract `r:embed` / `r:link`. New fields
`blip_embed_rid` / `blip_link_rid` on `Fill`. `_fill_str` (Markdown
renderer helper) shows `blip:rId7` instead of just `blip`.

### 5.4 Layout binding in pptx-file mode

`load_from_pptx` already read the slide's `.rels` for chart / image rId
resolution. Added a side-channel: scan the same rels for the relationship
typed `relationships/slideLayout`, expose the target path as
`layout_target`.

Threaded through to renderers via additional `layout_target: str | None`
keyword. Markdown Canvas section gains a `- layout: ../slideLayouts/slideLayout4.xml`
line when present (suppressed in module mode where the binding is
unknown). JSON `canvas` dict gains a `layout_target` field.

## 6. OLE / thinkcell detection

User flagged thinkcell as important: "is there anything useful from
this analysis ... is it overkill? - **OLE bodies** - that would include
thinkcell right? my company uses thinkcell a lot."

Thinkcell embeds in pptx in two known forms:

1. **Classic OLE** — `<p:graphicFrame>` with `graphicData uri="...presentationml/2006/ole"`
   containing `<p:oleObj progId="thinkcell.Chart.X" r:id="..." showAsIcon="0">`.
   The oleObj is often wrapped in `<mc:AlternateContent>` for backward
   compat, so it can sit one or two levels under `<a:graphicData>`.
2. **Custom URI** — newer thinkcell uses its own `graphicData @uri`
   like `http://www.think-cell.com/document/9`, no `<p:oleObj>` —
   PowerPoint just stores the thinkcell payload opaquely.

Added:

- `OleProbe` dataclass — `prog_id`, `rid`, `resolved_path`,
  `show_as_icon`, `is_thinkcell`.
- `ShapeProbe` gained `ole`, `frame_uri`, `is_thinkcell` fields. Every
  existing call site updated to pass defaults (`None` / `False`).
- `_parse_graphic_frame` now captures `graphicData @uri` on every
  graphicFrame into `frame_uri`. Added OLE branch (`uri == URI_OLE` →
  recursive `.//p:oleObj` find to handle mc-wrapped OLE → extract
  `progId`, `r:id`, `showAsIcon` → resolve embed via rels). Added
  diagram URI branch (`graphicFrame.diagram` kind). Both thinkcell
  heuristics fire `is_thinkcell = True`:
  - progId starts with `thinkcell` (case-insensitive)
  - URI contains `thinkcell` or `think-cell`
- Region summary gained `ole_count` and `thinkcell_count`. Markdown
  surfaces the line only when at least one is non-zero (no clutter on
  decks that don't use OLE).
- Markdown "OLE and other graphic frames" section — lists every shape
  with kind in `{graphicFrame.ole, graphicFrame.diagram,
  graphicFrame.unknown}`. Surfaces URI, progId, rId, resolved embed
  path, `**thinkcell embed**` callout when flagged, frame box geometry.
  Only emitted when any such shape exists.
- JSON shape dicts gain `ole`, `frame_uri`, `is_thinkcell`.

Verified against a synthetic fixture with both forms:

| Form | kind | frame_uri | OleProbe? | is_thinkcell |
|---|---|---|---|---|
| Classic OLE (mc-wrapped) | `graphicFrame.ole` | `...ole` | yes, progId=thinkcell.Chart.20, rId=rId7, resolved=`../embeddings/oleObject1.bin` | True |
| Custom URI | `graphicFrame.unknown` | `http://www.think-cell.com/document/9` | None (no OLE structure) | True |

Both flagged. Real deck has zero OLE — re-ran the full deck after this
change, confirmed no false positives and no regressions.

## 7. Smoke-test results

Eleven slide modules × two modes:

| Slide module | Module mode | File mode (slide #) | Notable constructs verified |
|---|---|---|---|
| cover | ✓ | sub_slide1 | Placeholder-bound shapes (`<p:ph type="body" idx="12"/>`) report `(layout)` for geometry |
| executive_answer | ✓ (`--text-estimate`) | sub_slide2 | KPI cards; text estimator gave per-shape fit arithmetic |
| framing | ✓ | sub_slide3 | OrbitFrame composition |
| scope | ✓ | sub_slide4 | Native `<a:tbl>` ghost-stripe table (3 cols × 5 rows) — cell merges, vMerge, per-cell fills |
| cost_funnel | ✓ | sub_slide5 | Native `<a:tbl>` lens ledger; 5 `<p:cxnSp>` connectors detected via endpoint bindings |
| methodology | ✓ | sub_slide6 | `mathMinus` / `mathMultiply` / `mathEqual` AutoShape presets; DependencyConnector with `dash=sysDash` / `color=BFBFBF` (GRAY_3) / `0.75pt` |
| annual_modeled_pool | ✓ | sub_slide7 | `<p:graphicFrame>` chart with `rId2`; resolved chart part path `../charts/chart1.xml` in file mode |
| visibility_gap | ✓ | sub_slide8 | Two `_bar_gauge` calls → 10 shapes (5 sp_ids each per styling-review log) |
| geography | ✓ | sub_slide9 | Stacked horizontal bar segments; caveat band |
| supplier_concentration | ✓ | sub_slide10 | Second chart slide; rId resolution; ranking ladder |
| meaning_limits | ✓ | sub_slide11 | Single-frame border pattern on callout; caveat ledger |

All 22 reports parse cleanly. `--json` skips Markdown write. `--all` in
module mode walks `deck_submarines/slides/*.py`, filters to modules exposing a
`render()` callable. `--all` in file mode iterates every
`ppt/slides/slideN.xml` part in the pptx.

## 8. Architectural notes

### Why stdlib only
Matches the rest of `sub_pptx/` — the deck-build pipeline emits raw
OOXML via f-strings with zero deps. Adding a parsing library here would
have been the first deviation. `xml.etree.ElementTree` handles
everything the parser needs; the inner loops are small enough that
performance isn't a concern.

### Why parse the rendered string, not the source
Module mode renders the slide via `mod.render(page_num=1,
total_pages=1)` and parses the resulting XML, instead of trying to
introspect the slide module's Python source. The rendered XML is
authoritative — it's what would actually land in the .pptx — and parses
the same way as the pptx file mode. Identical code path for both
modes.

### Why no theme resolution
The other agent's analysis spent ~40% of its words on "effective scene"
inheritance (theme color → RGB, layout placeholder geometry, font
scheme). Useful for arbitrary foreign pptx files where placeholders are
sparse. Explicitly out of scope for v1. Parser reports
`scheme:accent1` verbatim instead of resolving. Adding theme resolution
later is a non-breaking extension — every `Fill` carrying `kind="scheme"`
gains a sibling `resolved_rgb` field.

### Why `<p:graphicFrame>` URI is always captured now
Before the OLE additions, only known URIs (chart / chartEx / table)
were handled — anything else became `kind="graphicFrame.unknown"` with
no URI surfaced. After: every graphicFrame's URI is captured in
`frame_uri`, so unknowns are diagnosable. Thinkcell's custom URI
embeds are the canonical use case — without URI capture they would be
silent.

### Why per-slide wipe and not whole-directory wipe
Per-slide replacement preserves reports for slides not in the current
run. If you probe `visibility_gap` after probing the whole deck, the
other 10 reports stay valid. Whole-directory wipe would force a
recomputation cascade. Matches user intent: "every time the slide
probe is run on a slide that has already previously had a probe run on
it" — per-slide, not per-directory.

---

## Final state

```
sub_pptx/
├── tools/
│   ├── __init__.py            # empty package marker
│   └── slide_probe.py         # ~1200 LOC, stdlib only
├── reports/
│   └── slide_probe/           # 22 fresh reports (11 module + 11 file)
│       ├── annual_modeled_pool.{md,json}
│       ├── cost_funnel.{md,json}
│       ├── cover.{md,json}
│       ├── executive_answer.{md,json}
│       ├── framing.{md,json}
│       ├── geography.{md,json}
│       ├── meaning_limits.{md,json}
│       ├── methodology.{md,json}
│       ├── scope.{md,json}
│       ├── supplier_concentration.{md,json}
│       ├── visibility_gap.{md,json}
│       └── sub_slide{1..11}.{md,json}
└── deck_submarines/slides/body_template.py  # +12 lines: INSPECTING A SLIDE section
```

`tools/slide_probe.py` public surface:

```
python tools/slide_probe.py <target> [--slide N] [--text-estimate] [--json] [--all] [--out-dir DIR]
```

- `<target>` auto-detects: ends in `.pptx` → file mode; otherwise → Python module path.
- `--slide N` — pptx mode only; defaults to 1.
- `--text-estimate` — adds wrap/height arithmetic to text shapes.
- `--json` — skip Markdown.
- `--all` — module mode walks `deck_submarines.slides`; file mode walks every `slideN.xml`.

Coverage:

- **Shape kinds**: `p:sp`, `p:cxnSp`, `p:graphicFrame` (chart / chartEx
  / table / ole / diagram / unknown), `p:pic`, `p:grpSp`, plus catch-all
  for unknown spTree-level elements (reports raw tag name).
- **Geometry**: x, y, cx, cy, x_in, y_in, w_in, h_in, right, bottom,
  flattened absolute (through groups), rotation, flipH, flipV.
- **Fills**: solid (hex), scheme (name), none, gradient, blip (with
  embed/link rIds), pattern, unset.
- **Lines**: kind, color, width (EMU and pt), dash, head/tail caps.
- **Geometry presets**: prstGeom verbatim (`rect`, `roundRect`,
  `ellipse`, `mathMinus`, `mathMultiply`, `mathEqual`, `straightConnector1`,
  `bentConnector2/3`, etc.) + custGeom path-command counts.
- **Text**: paragraphs, runs (font, size_pt, bold, italic, underline,
  color), bodyPr (anchor, wrap, lIns/rIns/tIns/bIns, rot), pPr (algn,
  lnSpc pct/pts, level), bullets (char, autonum).
- **Tables**: grid widths, row heights, per-cell text body, merges
  (gridSpan, rowSpan, hMerge, vMerge), per-cell borders (lnL/R/T/B),
  per-cell fill, per-cell padding, anchor.
- **Charts**: rId, chart vs chartEx kind, resolved chart part path
  (file mode).
- **Pictures**: embed rId, link rId, resolved media path, crop
  percentages.
- **OLE**: progId, rId, resolved embed path, show-as-icon, thinkcell
  flag.
- **Connectors**: endpoint bindings (`stCxn` / `endCxn` → target sp_id).
- **Placeholders**: ph_type, ph_idx, `is_placeholder` flag, geometry
  reported as `None` (markdown shows `(layout)`).
- **Markup compatibility**: `mc:AlternateContent` transparently
  resolved to first Choice (or Fallback).

## Out of scope (deferred or rejected)

- Theme color / font resolution to absolute values.
- Placeholder geometry inheritance from layout / master.
- Effective-vs-direct scene distinction.
- PackageReader / SceneParser / ThemeResolver class split.
- Extension list (`p:extLst`, `p14:*`, `p15:*`) detail reporting —
  caught via raw_tag fallback.
- Hyperlinks (`a:hlinkClick`) — minor.
- Pillow-backed text measurement — stdlib estimator covers v1.
- Validation / lint / pass-fail framework.
- Docstring rewriting / sync mode.
- Render preview / PNG export.
- Computer-vision layout checks.
- Deck-specific profile layer ("chrome / sources / guardrail" tagging).

---

## Open follow-ups

1. **Pillow upgrade for text estimator.** Crude `AVG_CHAR_WIDTH_RATIO =
   0.50` works as a sanity check but undersells multi-paragraph text
   bodies with mixed fonts. Pillow-backed measurement would tighten the
   `fits` arithmetic. Wrapped behind a single function (`estimate_text_fit`)
   so the upgrade is one swap, no API change.
2. **Theme resolution.** Most of the agent's "effective scene"
   analysis. Would let the probe report `scheme:accent1 → RGB 4472C4`
   instead of just `scheme:accent1`. Worth doing when a foreign pptx
   with placeholder-driven sparse formatting needs inspection. Adds
   `resolved_rgb` to `Fill`, `resolved_font` to runs — non-breaking.
3. **Group rotation/flip propagation.** Group shapes can have their own
   `@rot` / `@flipH` / `@flipV`. Currently we report them on the group
   `ShapeProbe` but don't propagate to children. Per the agent's
   recommendation, v1 reports raw values and leaves visual-footprint
   computation to consumers. A follow-up could add `absolute_rot`
   per child.
4. **OLE coverage beyond thinkcell.** Excel / Word / Equation embeds
   surface correctly via `OleProbe` (progId fully reported), but no
   dedicated callouts. If non-thinkcell OLE becomes a frequent
   inspection target, add per-progId annotations.
5. **`p:cSld/p:bg`** (slide background) — not parsed. Affects visual
   interpretation when present. Simple add when needed.
6. **Notes / comments / media beyond `p:pic`.** Caught as unknowns in
   raw_tag, not specifically parsed. Low priority.

---

## Reference files

- Plan: `C:\Users\BrendanToole\.claude\plans\putting-you-in-plan-zany-lovelace.md`
- Implementation: [sub_pptx/tools/slide_probe.py](../sub_pptx/tools/slide_probe.py)
- Docstring update: [sub_pptx/deck_submarines/slides/body_template.py](../sub_pptx/deck_submarines/slides/body_template.py) (INSPECTING A SLIDE section, ~line 209)
- Reports: [sub_pptx/reports/slide_probe/](../sub_pptx/reports/slide_probe/) (22 fresh files)
- OOXML reference (canonical): [sub_pptx/ooxml_cheat_sheet_pptx.md](../sub_pptx/ooxml_cheat_sheet_pptx.md)
- Prior session logs:
  [logs/2026-05-28_methodology_deck_session.md](2026-05-28_methodology_deck_session.md),
  [logs/2026-05-28_methodology_deck_session_2.md](2026-05-28_methodology_deck_session_2.md),
  [logs/2026-05-28_deck_expansion_session.md](2026-05-28_deck_expansion_session.md),
  [logs/2026-05-28_deck_styling_review_pass.md](2026-05-28_deck_styling_review_pass.md) — established the chrome convention (sp_ids 2/3/4/4500/9999), color role table, single-ownership border pattern, ghost-stripe table technique, and the bug class that motivated this tooling.
