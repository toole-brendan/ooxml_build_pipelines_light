# Session log & handoff — bulk conversion: 27 slides across 4 source decks into staging

**Date:** 2026-06-24 (continues the other 2026-06-24 docs in this `logs/` folder)
**Project:** `projects/style_library/`
**Target:** `archetypes/schematics/schematics/` (STAGING — the regenerable converter output, never
the curated copy). The staging deck now holds **40 modules** (was 13).
**Nothing committed to git** (project dir is untracked). **No PNG render pass** (standing user
preference — memory `awards-deck-visual-qa`): deck builds green + all rels resolve; eyeball is the
user's.

This session executed the bulk-conversion playbook (`2026-06-24_session_log_and_bulk_conversion_handoff.md`
§B) against a user-supplied slide list spanning **four** source decks — including two decks never
before run through the converter (Navy Undersea, Golden Dome). All 27 conversions succeeded on the
first pass; the staging deck builds green and every rel resolves.

---

## 0. Source decks (all four are 13.333×7.5in = 12192000×6858000 EMU — coords land correctly)

| deck | file (in `/Users/brendantoole/projects3/reference/`) | status |
|---|---|---|
| Commercial Strategy | `20260325_Commercial Strategy_Market Analysis_vS.pptx` | proven |
| Navy (Surface incl MDA) | `20251120_Market sizing_Navy (Surface incl MDA)_v2.1.pptx` | proven |
| Navy (Undersea) | `20251201_Market sizing_Navy (Undersea)_v1.6.pptx` | **NEW this session** |
| Golden Dome | `20260116_Market sizing_Golden Dome_v2.0.pptx` | **NEW this session** |

**Golden Dome was not in `/reference`.** Copied in from
`/Users/brendantoole/projects2/deck_new_cc/reference/20260116_Market sizing_Golden Dome_v2.0.pptx`
(per user; byte-identical to the archived copy under `mro/_archive/.../db_old_test/reference/`).

---

## 1. What was converted (27 new modules)

All emitted into `archetypes/schematics/schematics/slides/` and registered in `slides/__init__.py`
(grouped by source deck, source-slide order). Module name = snake_case gist of the slide title.

**Commercial Strategy (20 modules):** `overview` (2), `key_terms_glossary` (5),
`key_findings_demand_build_economics` (8), `key_findings_financial_outlook` (9),
`key_findings_what_must_be_true` (10), `archetype_comps_newbuild_prices` (32),
`archetype_comps_vocc_performance` (33), `archetype_comps_shipbuilder_margins` (34),
`fleet_overview` (42), `status_quo_fleet_outlook` (43), `status_quo_outlook_oceangoing` (44),
`status_quo_outlook_offshore_1` (45), `status_quo_outlook_offshore_2` (46), `ships_act_volume` (51),
`ships_act_plus_volume` (52), `us_delivery_capacity` (53), `assumptions_income_statement_1` (77),
`assumptions_income_statement_2` (78), `coordination_archetypes` (166), `key_inputs` (167).

**Navy Surface (1):** `definitions_market_levels` (16).

**Navy Undersea (3):** `tcv_approach_unmanned_undersea` (15), `tcv_approach_manned_undersea` (16),
`tcv_to_acv_company_acv_undersea` (25).

**Golden Dome (3):** `comparison_vs_ddgs` (8), `production_outlook_colocated` (11),
`production_outlook_separate` (12).

### Two naming/scope decisions
- **CS slide 50 was SKIPPED.** It is **byte-identical** to slide 11 (same 31 sp / 5 pic / 15 cxn,
  identical text — verified) and slide 11 is already the `ships_act_overview` module. The user's list
  put 50 among the already-converted schematic slides; converting it would just duplicate
  `ships_act_overview`.
- **Navy Undersea modules carry a `_undersea` suffix.** Slides 16 and 25 there share titles with the
  already-present Navy *Surface* modules `tcv_approach_manned` (src 18) and `tcv_to_acv_company_acv`
  (src 19); slide 15 ("Unmanned-specified") is the undersea sibling of Surface `tcv_approach_usv`
  ("USV-specified"). All three are suffixed so the single `slides/` package has unique module names.

---

## 2. Residue & drops (honest accounting)

- **raw_verbatim shapes: 8 total, ALL the same benign kind** — `no explicit xfrm (layout
  placeholder)`: a placeholder with no geometry, kept verbatim so it inherits the layout's position
  (same case as the pre-existing `tcv_approach_iamd` title). In: `overview` (1),
  `assumptions_income_statement_1` (2), `assumptions_income_statement_2` (2),
  `definitions_market_levels` (1) (+ existing `tcv_approach_iamd` (1)). **No** gradFill/blipFill/
  custGeom/pattFill residue anywhere — the pattFill→`text_box(pattern_fill=)` and
  custGeom→`custom_geometry()` paths (added earlier today) kept those out of RAW.
- **Drops:** every slide drops its one think-cell OLE data frame ("…do not delete") — expected. One
  extra `DROPPED <p:pic> ? (no media target or geometry)` (a geometry-less placeholder pic).
- **EMF chart previews dropped correctly:** Golden Dome 8/11/12 and comparison source have a native
  chart + an EMF preview over it; the preview is dropped, the chart bundled (pic counts 3→2 etc.).
- **Notes worth a human glance (chrome kept verbatim, not a bug):** most chart slides emit
  "Note/Source line off house position - kept verbatim"; Golden Dome 11/12 also emit "Preliminary
  chip off house position - kept verbatim". These are faithfulness-preserving (the source sits >0.1″
  off the house position, so the converter keeps the shape rather than snapping it).

---

## 3. QA performed (build-green + rels; no PNG, per preference)

- **Build:** `wrote Schematics (reference port).pptx (40 slides, 22 charts)`.
- **Charts — all faithful, none degraded:** 18 chart-bearing modules (15 new + 3 pre-existing) all
  route through `styled_chart` (data-over-template). **0** fell back to `editable_bundled_chart`, **0**
  to a raw `{"chart_xml":…}` dict. Every `_src/sliceN_chartN.xml` has its paired `.xlsb`/`.xlsx`
  workbook (22 pairs). Chart-count arithmetic checks out: 3 existing + 19 new = 22.
- **Rels resolve both directions:** all 49 slide/chart parts' `r:id`/`r:embed` resolve to a defined
  rel Id, AND every internal rel `Target` exists as a package part. (Mandatory — PowerPoint silently
  *repairs* dangling refs; soffice won't catch it. Memory
  `pptx-port-dangling-rels-cause-powerpoint-repair`.) 34 `ppt/media` parts + 23 embedded workbooks
  packed.

---

## 4. Follow-up fix — converter now maps the source layout by NAME (not forced body)

The first build put `overview` (CS src 2) on the body layout (`slideLayout4` "Light Blank"), so its
**50% block + title** chrome was missing. Root cause: the converter forced `--layout slideLayout4`
on every slide. CS slide 2's source layout is named **"50% Block + Title"**, and `deck_core`'s
`infra/template` ships exactly that layout as **`slideLayout3`** — it just needed to be used.

**Fix (in `_tools/convert_slide.py`):** the converter now reads the source slide's own layout
`<p:cSld name>` and selects the house layout of the **same name**, falling back to the `--layout`
default only when there's no name match. New pieces: a `HOUSE_LAYOUTS` name→`slideLayoutN` map
(Cover 1→1, Section Divider→2, 50% Block + Title→3, Light Blank→4, Blank→5, Glossary→6), a
`source_layout_name(z, slide_no)` reader, and a one-line override in `convert()` that emits a
converter note (`layout: source uses '50% Block + Title' -> house slideLayout3 (was --layout
slideLayout4)`). This is why the source decks reference nonexistent layout *numbers* (slideLayout12/13)
yet normalize correctly — the *names* line up. It's backward-compatible: a "Light Blank" source maps
to slideLayout4, i.e. the old behavior, so no other module changed.

`overview.py` was **regenerated** through the updated converter (not hand-patched, so a future
re-convert stays correct) and now carries `LAYOUT = "slideLayout3"`; the built deck's first slide
binds to slideLayout3. **Audited all 27 converted slides for layout name** — overview is the *only*
non-"Light Blank" slide in the batch, so it was the only one affected. (Worth knowing for future
batches: cover/divider/glossary source slides will now pick up their house base automatically.)

---

## 5. For the next agent

- **Eyeball candidates (highest-risk renders first):** the two NEW source decks —
  `tcv_*_undersea` (15/16/25) and Golden Dome `comparison_vs_ddgs` + `production_outlook_*` — since
  this converter had never seen those decks/themes. Then the dense CS slides:
  `archetype_comps_shipbuilder_margins` (src 34: 201 source shapes → 5 charts + 7 loops + 13
  connectors) and the `status_quo_outlook_*` family (charts + tables + many on-bar labels). Then the
  RAW-placeholder slides (`overview`, both `assumptions_income_statement_*`,
  `definitions_market_levels`) to confirm the geometry-less placeholders land where intended.
- **These are STAGING (raw converter output).** Hand-polish + the byte-identical faithfulness gate
  (companion doc `…curated_corpus_and_inline_primitives.md` §3–4) happens in the **curated** copy
  (`archetypes/schematics_curated/`), which was NOT touched this session. Promoting any of these 27
  into curated = copy the module across, hand-annotate (provenance line / EXHIBIT / CODE MAP /
  semantic cluster names), and prove produced-XML byte-identical.
- **Converting more is unchanged** — same playbook command (`_tools/convert_slide.py SRC N --out
  $SLIDES/<name>.py --src-dir $SLIDES/_src --images-dir $SLIDES/images --module-name <name> --layout
  slideLayout4`), then register in `slides/__init__.py`. `styled_chart` is the default chart path.
- **Related:** `2026-06-24_session_log_and_bulk_conversion_handoff.md` (the playbook this followed),
  `2026-06-24_pattern_fill_custom_geometry_and_provenance.md` (the primitives that keep RAW low),
  `2026-06-24_curated_corpus_and_inline_primitives.md` (curated convention + faithfulness gate).
  Memories: `[[pptx-to-idiomatic-module-workflow]]`, `[[styled-chart-data-over-template]]`,
  `[[pptx-port-dangling-rels-cause-powerpoint-repair]]`, `[[awards-deck-visual-qa]]`.
