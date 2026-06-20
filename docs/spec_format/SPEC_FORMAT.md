# SlideSpec — standardized slide-spec format

**What this is.** One spec file per slide. It is a *handoff file*: one agent (or human)
authors it; a second agent then builds the slide module
(`projects/<deck>/deck/deck_<deck>/slides/<module_name>`, which returns a `<p:sld>` string).
The build agent can read anything in the repo — the engine, the guides, neighboring
modules — but the spec should be detailed enough that it **doesn't have to**: everything
required to build the slide should already be in the spec.

**Design goal.** Make spec → module translation reliable, complete, and low-ambiguity,
**without restating anything the engine already owns**. The spec speaks the engine's own
vocabulary (style tokens, primitive/factory names, BODY anchors) so the build is close to
mechanical, and it carries a *reserve* content layer so a later agent can raise information
density without re-doing research.

---

## 1. Global conventions (true for every slide — never restate per-file)

- **Tokens only.** Never write raw hex or point sizes. Use the named tokens from `style.py`
  — colors (`DK`, `WHITE`, `BLUE_1`…`BLUE_5`, `GRAY_1`…`GRAY_5`), sizes (`CAP_12PT`,
  `VALUE_14PT`, `MESSAGE_11PT`, `DENSE_BODY_10PT`, `LABEL_9PT`=900, `FINEPRINT_8_5PT`,
  `CHART_TITLE_10PT`, `RIBBON_KPI_18PT`, `BADGE_16PT`, `SOURCES_8PT`), insets
  (`INSETS_NONE`, `INSETS_CARD`, `INSETS_CHIP`, `INSETS_MESSAGE`, `INSETS_MICRO_CAP`), and
  `FONT`. The point/hex value lives once, in `style.py`. **One exception:** a table's cell
  `size` may be a raw hundredths-of-a-point integer (the engine's dense-table default is
  `950` = 9.5pt and has no named token — see `slide_snippets.md`). Use a token where one
  exists, else the raw hundredths value. (A `TABLE_DENSE_9_5PT = 950` token would remove even
  this exception, but adding it edits `style.py` — locked core — so it's tracked separately,
  not assumed here.)
- **Coordinates: a closed, BODY-relative grammar — no absolute slide EMUs.** Every region is
  `{x, y, w, h}`, each value drawn only from this vocabulary (the build module resolves it to
  EMU):
  - **Percent of BODY:** `0%`…`100%` (x/w over BODY width from `BODY_X`; y/h over BODY height
    from `BODY_Y`).
  - **BODY edges + constants:** `BODY_X, BODY_Y, BODY_R, BODY_B` in arithmetic with the named
    EMU constants `GAP` (standard inter-object gap), `NOTE_H` (one-line note height),
    `TITLE_BAND_H` (chart-title band) — e.g. `BODY_B - NOTE_H`.
  - **Sibling references:** `<region>.x|y|right|bottom|top`, and helpers `right_of(<region>)`,
    `below(<region>)`, `align_top(<region>)`, and `body_until(<region>)` (extend height down to
    `GAP` above that region's top — valid only when the target's position is already fixed,
    e.g. a bottom-pinned note).
  - **Sizes:** `remaining` (fill leftover width/height) and `fit_content` (builder computes via
    `text_metrics`).
  Nothing else is allowed — no `x=453079`, no freeform prose like `"left-ish"`. The named
  constants (`GAP`, `NOTE_H`, `TITLE_BAND_H`) are house-style EMU values the builder owns; the
  spec never hard-codes them.
- **Chrome maps 1:1 to module symbols.** `chrome.section → _SECTION`,
  `chrome.breadcrumb_topic → _TOPIC`, `chrome.title_finding → _TAKEAWAY`,
  `chrome.sources → _SOURCES` (the underscore-private render constants), and
  `chrome.layout → LAYOUT` (a **public** module attribute the builder reads, like `CHARTS` —
  no underscore). The engine wires `breadcrumb(_SECTION, _TOPIC)` +
  `title_placeholder(<title_topic>, _TAKEAWAY)` + `prelim_chip()` + `sources_line(_SOURCES)`.
- **`prelim_chip` and slide numbers are automatic** — never authored per slide, so they are
  **not** fields in `chrome`.
- **Chart → rId mapping is positional.** Per slide, `rId1` is the slideLayout; charts get
  `rId2, rId3, …` in module `CHARTS` order (confirmed in `lib.py`). So `chart_index: 0 → rId2`,
  `chart_index: 1 → rId3`. The spec gives `chart_index`; the builder derives the rId.
- **Images and logos are supported.** A picture (photo or brand logo) is declared in an
  `images[]` entry and drawn with the `picture()` primitive; the build wires its relationship
  from the `{rId, file}` you give it. Image rIds **continue after chart rIds** (no charts →
  first image `rId2`; one chart → `rId3`). Brand media lives in `assets/media/`, per-deck
  pictures in the deck's `images/` dir. A "no logos" rule, if a project has one, is a *project
  convention* (it lives in the conventions doc / `story.do_not_say`), not a limit of this format.
- **Paint order = `_body()` concatenation order.** Objects emit back-to-front; the last string
  concatenated paints on top. Encode it with the `paint_order` integer on each
  `element_inventory` row (low = behind). No separate paint-order section.
- **Sources (there is no "footer" — just sources).** `chrome.sources → _SOURCES`, rendered by
  `sources_line()`. Provide the **exact, final, ready-to-drop-in citations**: the list items are
  verbatim citation strings, and `source_line_exact` may carry the fully assembled
  `"Sources: (1) …; (2) …"`. If `source_line_exact` is present it **is** the rendered
  `_SOURCES`, and `sources` is only validation support. **Required on every body and appendix
  slide.** The only exception is a body/appendix slide whose content genuinely has no external
  source. Cover/divider: none.
- **Real citations only.** A source is an externally verifiable, published primary document —
  e.g. a government budget exhibit, a regulatory filing, an agency or oversight report, a public
  data API, or a company financial filing. **Never** cite an internal artifact: not an internal
  research document (e.g. a project "wiki" chapter), not a workbook sheet/tab name, not a
  chart-data block ID. Those internal documents carry their own citations — trace through them to
  the underlying real source and cite *that*.
- **Internal provenance is separate and never rendered.** Which workbook tab, chart ID, or wiki
  chapter produced a number is traceability, not a citation. It lives only in internal fields
  (`meta.inputs`, per-datum `tie_out`, reserve `evidence`) and must never appear in `sources` or
  anywhere on the slide.
- **Standing conventions live once, not per slide.** Project-wide rules — banned framings,
  numeric conventions, label and logo rules — are assumed across all specs and kept in the
  project's conventions doc, not restated in each file. Put only a slide-specific twist in
  `story.do_not_say`.
- **`slideLayout4`** is the body/appendix workhorse; `slideLayout1` cover, `slideLayout2` divider.

---

## 2. Which blocks are required

| Block | Rule |
|---|---|
| `meta`, `chrome`, `story`, `regions`, `element_inventory`, `qa` | **Always required** |
| `commentary.reserve` | **Required** for `slide_type: body` and `appendix`; n/a for `cover`/`divider` |
| `charts`, `tables`, `shapes`, `images` | **Required-if-present** — fully specified when present |
| `commentary.visible` | Required only if a rail/callout/note element exists |
| `data_and_calculations` | Optional — include when the slide reconciles or derives numbers |

**Omit-vs-empty:** a missing `charts`/`tables`/`shapes`/`images` is normalized to `[]`. Include
an explicit `tables: []` only when "no table here" is a deliberate design statement worth
signaling (as in `example_submarines_bucket_tam.md`).

**Required-if-present** is the core rule: a half-specified `tables[]` entry yields a broken,
overflowing slide (`house_table` depends on column widths, `rows`, `row_h`, `table_skin`,
`aligns`), so when a table exists, *every* `render` field is mandatory. Same for charts, shape,
and image exhibits.

---

## 3. Top-level schema

```yaml
# SlideSpec — one file per slide. Detailed enough to build the module from the spec
# alone (the build agent may read more, but should not need to).

meta:                          # REQUIRED
  slide_id:                    # stable id, e.g. <deck>-s<n>
  slide_order:                 # deck position (int) or appendix A-number
  module_name:                 # REAL module basename, no slide-number prefix (e.g. <name>.py)
  slide_type: body             # body | cover | divider | appendix
  section:                     # narrative section this slide sits in
  archetype:                   # reusable layout pattern, e.g. ranked_bar_plus_right_matrix
  story_role:                  # one line: why this slide is in the deck
  inputs: []                   # internal models/tabs/chart-IDs that produced the numbers
  related_appendix: []         # appendix slide_ids that back this slide

chrome:                        # REQUIRED — copies 1:1 into module symbols
  section:                     # -> _SECTION  (breadcrumb left)
  breadcrumb_topic:            # -> _TOPIC    (breadcrumb right)
  title_topic:                 # title topic, Title Case; usually == breadcrumb_topic
  title_finding:               # -> _TAKEAWAY; the answer, sentence case, <= 2 title lines
  layout: slideLayout4         # -> LAYOUT  (public module attribute; no underscore)
  sources: []                  # -> _SOURCES; EXACT, ready-to-go REAL citations (see §1)
  source_line_exact:           # optional; if present it IS the rendered _SOURCES

story:                         # REQUIRED — slim
  objective:                   # the slide's job (its "purpose")
  do_not_say: []               # slide-specific banned framing
  known_caveats: []

regions:                       # REQUIRED — closed BODY-relative grammar (see §1). No raw EMU.
  coord_basis: BODY
  layout_pattern:              # optional human label, usually == meta.archetype
  # <name>: {x:, y:, w:, h:}   every element references a region key
  # chart:       {x: 0%, y: below(title_band), w: 62%, h: body_until(note_strip)}
  # matrix:      {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  # note_strip:  {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}

element_inventory:             # REQUIRED — the ONE registry of position/prominence/paint order
  - id:                        # e.g. e2  (exhibit/commentary blocks reference this id)
    type:                      # exhibit_title | chart_frame | table | rail | callout | note | diagram | connector | picture | source
    region:                    # a regions key  (this is the ONLY place region is stated)
    prominence:                # primary | secondary | tertiary
    paint_order:               # int, low = painted first (behind)
    content:                   # one-line what-it-is
    tie_out:                   # optional internal provenance (never rendered)

charts: []                     # REQUIRED-IF-PRESENT — see §4 (references element ids)
tables: []                     # REQUIRED-IF-PRESENT — see §4
shapes: []                     # REQUIRED-IF-PRESENT — see §4
images: []                     # REQUIRED-IF-PRESENT — see §4 (photos, brand logos)

commentary:
  visible:                     # required only if a rail/callout/note element exists
    element:                   # -> element_inventory id (position comes from it)
    container:                 # right_rail | callout | chart_annotation | table_note | method_note
    title:
    bullets:
      - {lead:, body:}
    body_size: LABEL_9PT
  reserve:                     # MANDATORY for body | appendix
    purpose: Approved extra material for denser future versions of this slide.
    context: |                 # AMPLE prose — the research/narrative reservoir. Err LONG; this
                               # is the one section where verbosity is a feature. Every figure
                               # source-tagged. (This is where old "speaker commentary" lives.)
    density_modes:
      normal: {visible_bullets:, keep: []}
      dense:  {add_bullets:, safe_containers: [], allowed_font_step_down: []}
    approved_extra_points:     # drop-in chips distilled from context; aim for ~8-12, not 3
      - {priority:, lead:, body:, evidence:, safe_container:, density_trigger:}
    do_not_add: []

data_and_calculations:         # OPTIONAL — include when the slide derives/reconciles
  data_inputs: []              # {input, value, unit, year, tie_out, used_in}  (tie_out = internal, never a citation)
  calculations: []             # {name, formula, output, used_in}
  rounding_rules:
  reconciliation:

qa:                            # REQUIRED — guardrails + engine only (NOT number echoes)
  guardrails: []               # slide-unique semantic traps
  source_checks: []            # sources are real external citations; no internal docs/tabs/chart IDs
  engine_checks:               # standard battery
    - all body objects within BODY
    - title <= 2 lines
    - chart rIds match CHARTS order (chart_index 0 -> rId2)
    - if a table exists: resolved column widths sum to its region width
```

---

## 4. Exhibit sub-schemas (required-if-present)

Exhibit blocks **never restate a region** — they point at `element_inventory` ids, which carry
position, prominence, and paint order.

### `charts[]`
```yaml
- id:                  # the chart's own id (not an element id)
  factory:             # column_chart | bar_chart | line_chart | waterfall_chart | marimekko_chart
  chart_index:         # 0-based position in module CHARTS; index 0 -> rId2, 1 -> rId3
  title_element:       # -> element_inventory id of the external chart title (type exhibit_title)
  frame_element:       # -> element_inventory id of the chart frame (type chart_frame)
  data:
    categories: []     # may embed share % to match house style
    series:
      - {name:, values: [], data_point_colors: []}   # colors = style tokens
  params:              # passed to the factory; omit any that take the house default
    mode:              # ranked | clustered | stacked | percent
    value_axis_format: # e.g. '"$"#,##0"M"'  or  '0.0%'
    show_legend:
    show_gridlines:
    major_gridline_color:
    show_value_labels:
    value_label_format:
    value_label_size_pt:
    cat_label_size_pt:
    gap_width:
    cat_header:
    title: null        # ALWAYS null — house style uses the external exhibit_title element
  external_title:      # styling of the title; position comes from title_element
    text:
    size: CHART_TITLE_10PT
    italic: true
    color: DK
  annotations: []      # optional small chart notes {text, anchor_to: <element id>}
```

### `tables[]`
```yaml
- id:                  # the table's own id
  element:             # -> element_inventory id (region comes from it)
  role:                # primary | chart_side_evidence | appendix_detail
  factory: house_table # use low-level table/trow/tcell ONLY for spans/merges/per-cell sizes
  semantic:
    table_name:
    purpose:           # compare | summarize | reconcile | calculate | define | sensitivity
    reader_takeaway:
    row_order:
    highlight_rows: []
    guardrails: []
  render:
    table_skin: rule   # rule | light | dark
    size: 900          # house_table size= arg, hundredths of a pt (900 = LABEL_9PT; 950 = 9.5pt
                       # dense default). May be a token where one exists. SINGLE SOURCE for size.
    column_widths:
      mode: ratio      # ratio | percent | emu
      values: []       # e.g. [3.4, 1.0, 1.0, 1.0, 1.0, 1.0]
      builder_resolves_to_emu: true
      sum_to_region_width: true
    col_w_emu_override: []   # optional; only after a build/probe tuning pass
    aligns: []         # e.g. ["l","ctr","ctr","ctr"]
    row_h:
      fn: estimate_row_heights
      size_pt_from: size          # = size / 100; NEVER state a second number
      header_size_pt_from: size
      min_row_h:                  # optional
    rows:
      - []             # header row first, then body rows
    cell_fills: {}     # "(r,c)": TOKEN
    cell_bold: {}      # "(r,c)": true
    cell_text_colors: {}
    footnotes: []
  columns: []          # optional per-column {name, unit, tie_out, formula} for reconciling tables
```

### `shapes[]`  (cards, rails, callouts, notes, dividers, connectors)
```yaml
- id:                  # the shape's own id
  element:             # -> element_inventory id (region comes from it)
  factory:             # text_box | connector | section_divider_layout
  fill:                # token or null
  line_color:          # token or null
  insets:              # INSETS_* token (text_box only)
  text:                # the copy (or a paragraphs: [] list for multi-run cards)
  meaning:             # why it exists
```

### `images[]`  (photos and brand logos)
```yaml
- id:                  # the image's own id
  element:             # -> element_inventory id (type picture; region comes from it)
  factory: picture
  file:                # filename present in ppt/media/ (from assets/media/ or the images dir)
  rId:                 # slide-rels rId; MUST continue after chart rIds (no charts -> rId2,
                       # one chart -> rId3). The build wires it; picture()'s r_embed must match.
  alt:                 # short description / accessibility text
  meaning:             # why it's here (e.g. brand logo, site photo)
```
Brand assets live in `assets/media/`; per-deck pictures in the deck's `images/` dir. Logos are
supported — a "no logos" rule, if any, is a project convention, not a format limit.

---

## 5. The element-registry spine (how the blocks link)

`element_inventory` is the **single source of truth** for *what objects exist, where, how
prominent, and in what paint order*. Region/position lives there and **only** there. The exhibit
blocks (`charts`/`tables`/`shapes`) and the `commentary` blocks **reference element `id`s** and
add only build detail — a chart names its `title_element` and `frame_element`; a table/shape/
visible-commentary names its `element`. This removes a common failure mode where the same object gets described in several places at
once (a layout block, an object registry, a separate "primary exhibit" block, per-exhibit
`region` fields, a visual-hierarchy ranking, and a paint-order list all restating it). One
registry; everything else keys off it.

The same `id`s let the `reserve` block tag each spare bullet to a `safe_container` region, so
"make this denser" is "pull the next-priority reserve points into their region" — mechanical,
not a re-research task.

The `reserve` block has **two layers**: `context` (ample prose — the research reservoir, where
the old speaker commentary lives) and `approved_extra_points` (finished, region-tagged,
source-tagged chips ready to drop in). Be generous with `context` and aim for ~8–12 chips: it
is the seam a future agent mines to author new on-slide copy, and the one place in the spec
where more is better.

---

## 6. Minimal skeleton (chart-only body slide, no table)

```yaml
meta: {slide_id: , slide_order: , module_name: , slide_type: body, section: , archetype: , story_role: , inputs: [], related_appendix: []}
chrome: {section: , breadcrumb_topic: , title_topic: , title_finding: , layout: slideLayout4, sources: []}
story: {objective: , do_not_say: [], known_caveats: []}
regions:
  coord_basis: BODY
  layout_pattern: ranked_bar_plus_right_rail
  title_band: {x: 0%, y: 0%, w: 70%, h: TITLE_BAND_H}
  chart:      {x: 0%, y: below(title_band), w: 70%, h: body_until(note_strip)}
  rail:       {x: right_of(chart) + GAP, y: align_top(chart), w: remaining, h: fit_content}
  note_strip: {x: 0%, y: BODY_B - NOTE_H, w: 100%, h: NOTE_H}
element_inventory:
  - {id: e1, type: exhibit_title, region: title_band, prominence: tertiary,  paint_order: 1, content: external chart title}
  - {id: e2, type: chart_frame,   region: chart,      prominence: primary,   paint_order: 2, content: ranked bar}
  - {id: e3, type: rail,          region: rail,       prominence: secondary, paint_order: 3, content: caveat rail}
  - {id: e4, type: note,          region: note_strip, prominence: tertiary,  paint_order: 4, content: sizing note}
charts:  [ { id: chart_1, factory: bar_chart, chart_index: 0, title_element: e1, frame_element: e2, ... } ]
tables:  []                    # none -> normalized to []
shapes:  [ { id: rail_1, element: e3, factory: text_box, ... }, { id: note_1, element: e4, factory: text_box, ... } ]
commentary:
  visible: { element: e3, container: right_rail, title: , bullets: [ {lead: , body: } ] }
  reserve: { purpose: ..., context: "...", density_modes: {...}, approved_extra_points: [...], do_not_add: [] }
qa: { guardrails: [], source_checks: [], engine_checks: [ "objects within BODY", "title <= 2 lines" ] }
```

See `example_ddg_sam_scenarios.md` (chart **and** table) and
`example_submarines_bucket_tam.md` (chart only, `tables: []`) for full worked specs.
