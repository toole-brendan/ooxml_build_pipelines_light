# Session log & handoff — curated reference corpus + inline primitives

**Date:** 2026-06-24 (later session; continues the two docs now alongside this one in `logs/`)
**Project:** `projects/style_library/`
**Source decks ported from:**
- `/Users/brendantoole/projects3/reference/20260325_Commercial Strategy_Market Analysis_vS.pptx` ("Commercial Strategy")
- `/Users/brendantoole/projects3/reference/20251120_Market sizing_Navy (Surface incl MDA)_v2.1.pptx` ("Navy")

This session did four things: (A) converted 5 Navy schematic slides, (B) created a **frozen, hand-polished
copy** of the schematics corpus, (C) hand-annotated all 13 modules for an AI-agent study audience while
keeping every render byte-identical, and (D) replaced the raw-OOXML residue in two modules with **module-local
inline primitives**. For the converter internals and the charts→data-over-template resolution, see the two
companion docs in this folder.

---

## 0. The single most important structural fact

There are now **two parallel schematics decks**, and you must not confuse them:

| dir | output pptx | role |
|---|---|---|
| `archetypes/schematics/` | `Schematics (reference port).pptx` | **staging** — raw converter output; REGENERABLE; keep converting new slides here |
| `archetypes/schematics_curated/` | `Schematics (curated reference).pptx` | **frozen, hand-polished corpus**; the study artifact; do NOT point the converter's `--out` here |

The curated copy exists so hand-annotation survives re-conversion. The converter overwrites whatever `--out`
points at; the curated dir is simply never targeted, so polish there is durable. (This is the
`build-archetype-overrides-clobbers-curated-csv` memory pattern — curation must live where regeneration can't
reach it.) Both decks currently hold the **same 13 modules**; staging is raw, curated is polished.

Both are independent buildable packages (their own `build_deck.py` + `schematics/` package). The inner package
is named `schematics` in both — fine because each builds in its own process; only collides if something imports
both at once (the build never does). Path math is depth-relative (`parents[1]` build dir, `parents[5]` workspace
root), so the sibling copy resolves `deck_core` + `infra` correctly.

---

## 1. The 13 modules (curated registry order = slide order)

| # | module | src | deck | notable |
|---|---|---|---|---|
| 1 | `ships_act_overview` | 11 | CS | money-flow diagram, flag icons, 15 connectors |
| 2 | `value_chain_maritime_transport` | 30 | CS | 3 tables; 9 "$ TBD \| %" labels tripped title-detection (kept verbatim) |
| 3 | `value_chain_participation` | 31 | CS | 24 company-logo pictures, 2 tables, prelim chip |
| 4 | `addressable_demand` | 41 | CS | 6 tables, pure definitional |
| 5 | `ships_act_captive_demand` | 60 | CS | **styled_chart** + mandate table + inline `_pattern_swatch` |
| 6 | `approach_unit_economics` | 120 | CS | one giant cost-matrix table |
| 7 | `approach_volume_and_price` | 121 | CS | operator-glyph clusters (= + × ÷) |
| 8 | `freight_charges` | 134 | CS | **styled_chart** + inline `_glyph` (check/cross icons) |
| 9 | `funding_components` | 15 | Navy | mission×funding matrix (flow diagram) |
| 10 | `tcv_approach_usv` | 17 | Navy | TCV build-up, USV-specified |
| 11 | `tcv_approach_manned` | 18 | Navy | densest (52 shapes → 7 loops) |
| 12 | `tcv_to_acv_company_acv` | 19 | Navy | styled_chart + table + flattened group |
| 13 | `tcv_approach_iamd` | 29 | Navy | TCV build-up; title is a RAW placeholder (no xfrm) |

Provenance per module is now correct (6 CS, 5 Navy + 2 CS added mid-session). **This session converted Navy
15/17/18/19/29 from scratch**; the 6 original CS modules pre-existed; CS 60 + 134 were added to staging mid-session
and then pulled into curated.

---

## 2. Converting the 5 Navy slides (the standard loop, reaffirmed)

```bash
cd projects/style_library                                # converter now lives at the project root
SRC="/Users/brendantoole/projects3/reference/20251120_Market sizing_Navy (Surface incl MDA)_v2.1.pptx"
SLIDES=archetypes/schematics/schematics/slides           # STAGING, not curated
python3 _tools/convert_slide.py "$SRC" 15 \
    --out "$SLIDES/funding_components.py" \
    --src-dir "$SLIDES/_src" --images-dir "$SLIDES/images" \
    --module-name funding_components --layout slideLayout4
# then register in $SLIDES/__init__.py (source-deck group, source-slide order) and build_deck.py
```

Findings worth keeping:
- **Use `--layout slideLayout4` regardless of source.** The Navy slides reference `slideLayout13`, but `infra/template`
  only ships `slideLayout1–6`, and the whole corpus normalizes body slides to `slideLayout4`. Faithful *shapes*,
  house *chrome*.
- **Slide size matches** across decks (13.333×7.5 in = 12192000×6858000 EMU), so the converter's absolute EMU
  coordinates land correctly. Always check this when porting a new source deck — a different `sldSz` would
  silently misplace everything.
- **All 5 Navy slides share one brand asset** `image8_3071a231.jpeg` (a logo), content-dedup'd by the converter's
  sha1 naming — stored once.
- Each slide's only "drop" was the think-cell OLE data frame ("…do not delete"); a recursive pic count looks like
  2 pics/slide but the second is the OLE's nested preview, dropped with the frame. No real content lost.
- Slide 19's group flattened cleanly; its chart→styled_chart, table→table().

**QA used:** build green + the rels-resolution check (every `r:id`/`r:embed` in slides+charts resolves — PowerPoint
silently *repairs* dangling refs; soffice won't catch it). Render-and-look PNG QA was **deliberately not run** this
session (user preference: halt and let them eyeball the pptx — memory `awards-deck-visual-qa`). Slides worth a human
look: 29 (RAW title placeholder inherits slideLayout4 geometry, not source), 15/17/18 (Source line off house position,
kept verbatim).

---

## 3. The hand-polish convention (apply to any future curated module)

Goal: each module reads like a worked example for a **zero-context AI agent**. Every change is **names / comments /
docstring only — never a coordinate, value, colour, or append order** (append order = z-order; reordering changes the
render). The result is provably faithful (see §4).

Per module:
1. **Provenance line** — `<name> — <Deck> deck (<YYYYMMDD>), source slide <N>.` (the raw converter hardcodes
   "Commercial Strategy deck" for *every* deck — a real bug; see §6).
2. **`EXHIBIT`** paragraph — what the slide depicts and its visual structure.
3. **`CODE MAP`** — bullet list mapping each cluster / chart / table / helper to its role. Note explicitly that the
   body follows **source paint order**, so groups interleave and section headers mark roles *in place*.
4. **Semantic names** — rename the converter's style-clusters (`_LABELS`, `_LABELS2`, `_LEGEND_SWATCHES`…) to what
   they are. **Be honest about heterogeneous style-clusters**: if a cluster groups things by shared *style* not
   *meaning* (e.g. budget rows + mission boxes that happen to share one black-fill style), name it by the shared
   visual (`_BANNER_LABELS`) and list the contents in a comment — don't fabricate a misleading semantic name. A
   recurring honest correction: the converter labels math-operator glyphs (`mathEqual`/`mathPlus`) as
   `"LegendSwatch"`; rename those to `_EQUALS_SIGNS` / `_PLUS_SIGNS` / `_TIMES_SIGNS`.
5. **Section-header comments** in `_body()` — `# ── chrome ──`, `# ── legend ──`, etc., inserted in place (no reorder).
6. Keep a trimmed `Converter stats:` + `Residue:` note at the end for honesty.

`funding_components.py` is the canonical exemplar; read it first.

**Rename mechanics gotcha:** beware substring collisions when renaming via replace-all. `_LABELS` is a substring of
`_LABELS2`/`_VESSEL_LABELS`, so rename the longer/numbered names first and don't introduce a new name containing the
token you're about to replace (this bit me twice — a docstring `_VESSEL_LABELS` got double-subbed to
`_VESSEL_VESSEL_LABELS`, and a too-specific `_X1` edit caught only 1 of 5 connectors). The byte-identical gate +
`grep` for `NAME_NAME` double-subs catch these.

---

## 4. The faithfulness gate (the method that makes all of this safe)

Because the polish only touches names/comments/docstrings, the **produced slide XML must be unchanged**. That's an
exact, cheap check — no rendering needed:

```bash
# 1) BEFORE polishing: build, snapshot every ppt/slides/slideN.xml to a baseline dir
# 2) polish
# 3) AFTER: rebuild, assert each slideN.xml == baseline byte-for-byte
```

If a slide differs, you changed a value/order (or fat-fingered a literal) — fix it. If the build raises NameError,
a rename missed a usage. This gate held green across all 13 modules through every change this session, including the
inline-primitive refactor. (Baselines this session lived in the scratchpad; regenerate fresh whenever the registry
order changes, since slide indices shift.)

---

## 5. Inline primitives — reducing raw-OOXML residue without touching `deck_core`

Two modules carried raw `<p:sp>` blobs the converter couldn't express as primitives. We replaced them with
**module-local helper functions**. Key realization: *a primitive is just a function returning a shape-XML string*,
and the build does `"".join(out)` — so any local `def _foo(...) -> str` is a first-class primitive with **zero core
changes**. Contract: well-formed XML, a unique shape id, resolve any `rId`.

Two cases, two outcomes:
- **pattFill (fully reducible).** `ships_act_captive_demand`'s lone raw shape was a plain rect with a diagonal-hatch
  fill — all boilerplate except the pattern. Became `_pattern_swatch(sp_id, name, x, y, cx, cy, *, prst, fg, bg)`; a
  1034-char blob → ~80-char call. The verbatim genuinely *shrinks*.
- **custGeom (dedupable, not eliminable).** `freight_charges`'s "5 raw shapes" were really **2 unique icon
  geometries** — a green check (`"Haken, check"`) ×2 and a cross (`"Cross, kreuz"`) ×3, differing only in `id` + `y`.
  Became two named constants `_GLYPH_CHECK` / `_GLYPH_CROSS` + `_glyph(template, sp_id, y)`; 5 inline blobs → 5 clean
  calls. Honest limit: arbitrary bézier path data is intrinsic geometry — it can't become a parameterized primitive,
  but it's deduped, named, and lifted out of the body.

**Faithfulness for inline primitives:** the helper must emit *exact* bytes. Two subtleties: raw shapes use **fixed
ids** (2000+, outside the `n()` range) and **raw EMU** coords, so helper calls pass those explicitly (not `n()`/`IN()`).
We proved each helper reproduces its original raw string with an in-script `assert helper(...) == raw` BEFORE writing,
then confirmed with the byte gate. (Use sentinel placeholders `@ID@`/`@Y@` + `.replace()` for templating, not
`.format()` — OOXML can contain stray braces.)

---

## 6. Findings / open items for the next agent

- **Converter provenance bug.** `convert_slide.py` hardcodes `"… - Commercial Strategy deck, source slide N"` in the
  emitted docstring (it never took a deck-name param; only surfaced once we crossed decks). Fix: derive the deck name
  from the source `.pptx` filename / `docProps/core.xml` and thread it through. Low effort, fixes all future modules.
- **The real fix for the verbatim** (out of scope this session per "no core changes"): add `pattern_fill=` to
  `deck_core.text_box` and a `custom_shape()`/`custom_geometry()` primitive, then teach the converter to emit them.
  That makes pattFill/custGeom idiomatic for *every* future module instead of per-module helpers. Highest leverage.
- **Converter could emit a richer auto-docstring** (a per-slide "reading guide" / structure manifest + cluster
  sample-text comments) so raw output is more legible before any hand-polish — it already computes the structure.
- **Render-and-look QA not done** this session (per user preference). The curated deck builds green + all rels
  resolve + all 13 byte-identical, but no PNG eyeball pass. Candidates to scrutinize first: `tcv_approach_iamd`
  (RAW title placeholder position), `freight_charges` (the check/cross icon placement — named from source labels,
  not visually verified).
- **Promote helpers to a shared `slides/_local.py`** if `_pattern_swatch`/`_glyph`-style patterns recur across decks
  (kept module-local for now so each curated module is a self-contained study example).

---

## 7. Files touched this session

- **Converted (staging):** `archetypes/schematics/schematics/slides/{funding_components, tcv_approach_usv,
  tcv_approach_manned, tcv_to_acv_company_acv, tcv_approach_iamd}.py` + registry; chart parts into `slides/_src/`.
- **New deck:** `archetypes/schematics_curated/` — full buildable copy of `schematics/`, identity changed in
  `schematics/lib.py` (OUT/title/creator/app → "curated reference"). All 13 modules hand-polished; the 2 raw-heavy
  ones (`ships_act_captive_demand`, `freight_charges`) additionally carry inline primitives.
- **Moved into `logs/`:** the two prior handoff docs + this file.
- Nothing committed to git (the whole project dir is untracked).
- Memories in play: `pptx-to-idiomatic-module-workflow`, `styled-chart-data-over-template`,
  `pptx-port-dangling-rels-cause-powerpoint-repair`, `house-table-row-height-is-a-minimum`,
  `awards-deck-visual-qa`, `build-archetype-overrides-clobbers-curated-csv`,
  `prefers-agent-verification-over-audit-tools`.
