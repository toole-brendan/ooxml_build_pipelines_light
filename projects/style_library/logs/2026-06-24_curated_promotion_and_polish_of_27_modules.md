# Session log & handoff — promote + hand-polish the 27 staging modules into the curated corpus

**Date:** 2026-06-24 (continues the four other 2026-06-24 docs in this `logs/` folder)
**Project:** `projects/style_library/`
**Outcome:** `archetypes/schematics_curated/` grew from **13 → 40** hand-polished modules. The
27 modules the bulk-conversion session had staged in `archetypes/schematics/` are now promoted,
registered, hand-annotated for study, and proven byte-faithful. Curated builds green
(`wrote Schematics (curated reference).pptx (40 slides, 22 charts)`); all slide+chart rels resolve.
No PNG render pass (standing preference — memory `awards-deck-visual-qa`); halt for the user's eyeball.

---

## 0. What this session did

The prior bulk-conversion session left 27 new modules in **staging** (`archetypes/schematics/`, the
regenerable raw converter output). The **curated** copy (`archetypes/schematics_curated/`, the frozen
hand-polished study corpus) still held only the original 13. This session **promoted all 27 into
curated and hand-polished each** to the curated convention, then proved every change was cosmetic via
a byte-identical produced-XML gate.

Result: curated now mirrors staging's full 40-module set, in the same source-grouped order, with every
module carrying the EXHIBIT / CODE MAP / semantic-names / section-comment treatment.

---

## 1. The method (repeatable promotion + polish pipeline)

1. **Verbatim promote.** Copy the 27 new `slides/*.py` staging→curated (skip the 13 already curated,
   so the hand-polished/retrofitted originals are never clobbered). Full-sync `slides/_src/` (22 chart
   `*.xml`+`*.xlsb` pairs) and `slides/images/` (28 files) staging→curated — overlapping assets were
   verified byte-identical first (`cmp`), so the copy only *adds* the missing parts.
2. **Register in staging order.** Rewrote curated `slides/__init__.py` to list all 40 in the SAME
   grouped source order as staging (CS → Navy Surface → Navy Undersea → Golden Dome). This aligns
   curated slideN ↔ staging slideN, which turns a cross-deck slide diff into a faithfulness check.
3. **Baseline snapshot.** Build curated (verbatim, unpolished) → snapshot every `ppt/slides/slideN.xml`
   and `ppt/charts/chartN.xml` to a scratchpad baseline. This is the gate's reference.
4. **Hand-polish.** One module done by hand first (`fleet_overview`) to validate the gate end-to-end;
   the remaining 26 fanned out to parallel subagents, **one module each**, all reading a single tight
   spec (`scratchpad/POLISH_SPEC.md`) + the three exemplars (`funding_components`,
   `tcv_to_acv_company_acv`, `fleet_overview`). Subagents edit **in place, names/comments/docstring
   only, no build** (avoids build races; the central gate is the authority). Done in 3 batches
   (6 → 10 → 10) with a gate after each.
5. **Byte gate after every batch.** Rebuild curated, byte-diff all 40 slides + 22 charts vs the
   baseline. **Any** changed part = a literal/order edit slipped in → fix it. Held green every batch.

**Why parallel subagents are safe here:** the polish is provably cosmetic *only if* the produced XML
is unchanged, and that is exactly what the byte gate checks centrally. A subagent that fattens a
coordinate, reorders an `out.append`, or fat-fingers a string fails the gate (or the build's import).
So fan-out trades a little rework risk for big throughput, with zero faithfulness risk. (Subagents do
NOT build and do NOT touch `__init__.py` — only their own module file — so concurrent edits never
collide.)

---

## 2. The polish convention (unchanged from the curated-corpus doc §3; reaffirmed)

Per module, **names / comments / docstring only — never a coordinate, value, colour, string, or
append order** (append order = z-order). Each module now has:
- Provenance line (auto-correct from the converter's `derive_provenance`), then an `EXHIBIT —`
  paragraph (what the slide depicts, from the real run() text), a `CODE MAP` (one bullet per cluster /
  chart / table / chrome / helper, noting paint-order interleave), the `styled_chart` caveat where a
  chart is present, the "hand-annotated for study … byte-identical to the raw port" note, a trimmed
  `Converter stats:` line, and a `Residue:` line where there's RAW/off-house honesty to record.
- Semantic cluster + anchor names replacing the converter's generics (`_LABELS`→`_SEGMENT_LABELS`,
  `_SW_X`→`_SWATCH_X`, …). Heterogeneous-by-style clusters are named by their shared *visual* with
  contents listed in a comment (not given a fake semantic name). The converter's recurring
  `mathEqual`/`mathPlus`/`rightArrow`-glyph-mislabeled-as-`"LegendSwatch"` clusters were renamed
  honestly (`_EQUALS_SIGNS` / `_PLUS_SIGNS` / `_TARGET_MARKER_ARROW_YS`), while the load-bearing
  `"LegendSwatch"` *shape-name string argument* was left untouched.
- `# ── section ──` headers inside `_body()`, in place (no reorder).

`scratchpad/POLISH_SPEC.md` is the exact brief each subagent followed; reuse it for future batches.

---

## 3. Verification (all green; no PNG)

- **Polish gate:** all 40 `slideN.xml` + 22 `chartN.xml` **byte-identical** to the promotion baseline
  after polishing — i.e. polish changed only names/comments/docstring on every one of the 27.
- **Convention coverage:** 40/40 modules carry `EXHIBIT —`, `CODE MAP`, the hand-annotated note, and
  a `Converter stats:` line. Zero leftover generic converter names (`_LABELS`, `_LBL_*`, `_SW_*`,
  `_VAL_*`, `_H1`/`_W1`/`_X1`/`_Y1`); no `NAME_NAME` double-sub artifacts.
- **Rels resolve** both directions for all 49 slide+chart parts (mandatory — PowerPoint silently
  *repairs* dangling `r:id`; soffice won't catch it. memory `pptx-port-dangling-rels-cause-powerpoint-repair`).
- **Existing 13 untouched:** byte-identical to their pre-promotion render (promotion did not perturb
  the frozen corpus, incl. the 2 retrofitted modules).
- **Cross-deck:** all **27 promoted modules byte-identical to staging** (promotion + polish preserved
  faithfulness to the current converter output).
- Build is deterministic (re-running yields identical slide/chart XML), which is what makes the gate exact.

---

## 4. Two findings worth the user's attention (NOT fixed this session — out of the stated scope)

### 4a. Seven of the original 13 curated modules are a converter-generation behind staging
A cross-deck diff (curated vs staging, aligned slide indices) shows **9** differing slides: the 2
known retrofits (`ships_act_captive_demand`, `freight_charges` — inline→core primitive, by design)
**plus 7 of the original CS/Navy modules**: `ships_act_overview`, `value_chain_maritime_transport`,
`value_chain_participation`, `addressable_demand`, `approach_unit_economics`,
`approach_volume_and_price`, `tcv_to_acv_company_acv`.

The deltas are **tiny and formatting-level, not structural** (identical `<a:p>`/`<a:r>`/table/shape
counts). Two causes, both = curated was hand-polished from an *older* converter than staging's current
output:
- `<a:spcPct val="115000"/>` (curated) vs `100000` (staging) — paragraph line-spacing 115% → single.
- `<a:pPr algn="…">` (curated) vs `<a:pPr algn="…" marL="0" indent="0">` (staging) — the newer
  converter explicitly zeroes margin/indent (and drops a stray `sz` on `endParaRPr`).

Staging's current output is marginally **more** faithful. **→ RESOLVED later this session (§7):**
the 7 were refreshed to the current converter **with their hand-polish preserved** (recorded then
re-applied). Cross-deck diff is now down to the 2 intentional retrofits only.

### 4b. Cosmetic provenance-phrasing inconsistency (docstring line 1 only)
The 27 promoted modules use the converter's `derive_provenance` phrasing ("Commercial Strategy Market
Analysis deck", "Market sizing Golden Dome deck", …); the 13 older originals use hand-written phrasing
("Commercial Strategy market-analysis deck", "Navy market-sizing deck"). Harmless (docstring comment),
and it harmonizes automatically if the 7 in §4a are refreshed (they'd pick up the converter form).

---

## 5. Files touched

- **`archetypes/schematics_curated/schematics/slides/`** — 27 new modules (promoted + polished),
  `__init__.py` rewritten to register all 40 in staging order, `fleet_overview.py` hand-polished by
  me. `_src/` +19 chart pairs, `images/` +3 logo files.
- **No engine/converter changes.** `deck_core/*` and `_tools/convert_slide.py` untouched.
- **Staging (`archetypes/schematics/`) untouched** except a rebuild for the cross-deck check.
- Scratchpad artifacts (reusable): `vlib.py` (snapshot/cmp/rels helpers), `POLISH_SPEC.md`, baseline
  + staging snapshots.
- Nothing committed to git (the new modules + `_src`/`images` show as untracked; `__init__.py` and the
  2 retrofitted originals show as modified — the latter from prior sessions).

---

## 6. For the next agent

- **Eyeball pass (no PNG was run):** highest-value first — the dense hero
  `archetype_comps_shipbuilder_margins` (5 small-multiple charts), the `status_quo_outlook_*` and
  `archetype_comps_*` chart families, the two Golden Dome `production_outlook_*` charts and
  `comparison_vs_ddgs`, the undersea diagrams (`tcv_*_undersea`), and the RAW-placeholder tables
  (`overview`, both `assumptions_income_statement_*`, `definitions_market_levels`).
- **Refreshing the 7 stale originals (§4a)** is the obvious next cleanup if you want corpus-wide
  converter parity; reuse the §1 pipeline + `POLISH_SPEC.md`.
- **Converting/promoting more slides is unchanged:** convert into staging, then promote with the §1
  pipeline. The byte gate makes parallel polish safe.
- **Related docs:** the four other `2026-06-24_*.md` here (converter internals, charts→styled_chart,
  curated convention, pattFill/custGeom primitives, bulk-conversion playbook). Memories:
  `[[pptx-to-idiomatic-module-workflow]]`, `[[styled-chart-data-over-template]]`,
  `[[pptx-port-dangling-rels-cause-powerpoint-repair]]`, `[[awards-deck-visual-qa]]`,
  `[[build-archetype-overrides-clobbers-curated-csv]]`.

---

## 7. Follow-up (same session): the 7 stale originals refreshed WITHOUT losing their polish

Per the user, the 7 modules in §4a were brought onto the current converter **while preserving their
existing hand-polish** — record the polish, swap in the newer code, re-apply the polish. Method
(reusable "polish port"):

1. **Preserve both references** to scratchpad: `polish_ref/` = the old polished curated file **B**
   (the docstring + semantic names + section comments to keep); `raw_ref/` = the current staging file
   **A** (the newer, more-faithful raw code).
2. **Confirm the gap is formatting-only.** A tag-tokenized diff of every divergent slide showed the
   only differing tags are `spcPct` / `pPr` / `endParaRPr` — i.e. structure, coordinates, values,
   strings, clusters and order are **identical** between A and B. That is what makes B's polish port
   onto A 1:1.
3. **Swap A into curated** (overwrite B), rebuild → the 7 slides now render identically to staging
   (verified 7/7), the other 33 unchanged. Snapshot this as the gate baseline.
4. **Port the polish (one subagent per module, `scratchpad/PORT_SPEC.md`):** edit the in-place A to
   carry B's docstring + B's semantic variable names (matched by identical data content) + B's
   `# ── section ──` headers — changing names/comments/docstring **relative to A** only. Reconcile the
   few converter-generation facts in the docstring (e.g. B said the table used `tcell`; A now uses
   `tcell_rich`/`tpara`/`trun` — keep A's code, fix the mention). Each subagent self-checked by
   reverse-renaming + stripping comments/docstring and asserting equality to `raw_ref` (A).
5. **Gate:** rebuild; all 40 slides+charts byte-identical to the step-3 baseline (port was cosmetic);
   cross-deck curated-vs-staging dropped **9 → 2** (only the 2 intentional retrofits remain); rels
   resolve; 40/40 EXHIBIT+CODE MAP; no leftover generics; no double-sub artifacts.

Net: **all 38 non-retrofit curated slides are now byte-identical to the current converter's output**,
and every module keeps its hand-annotation. The provenance-phrasing nit (§4b) is intentionally left:
those first lines were themselves hand-chosen polish (the converter had the provenance bug when the 13
were first polished), so "preserve the polish" means keeping B's wording; harmonizing the 13 originals
to the converter's auto-derived phrasing is a separate cosmetic call.
