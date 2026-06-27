# 2026-06-25 — Archive the ceiling/lane slides, drop `house_table` via re-port, polish all slides to the study convention

Pipeline: `projects/distributed_shipbuilding/deck_primary/`
Output:   `projects/distributed_shipbuilding/deck_primary/20260610_Distributed Shipbuilding New Construction_vS.pptx`
Build:    `cd deck_primary && python3 build_deck.py`   → expect `(8 slides, 5 charts)`
Registry: `deck_primary/deck_primary/slides/__init__.py` (`SLIDE_RENDERS`; list order = slide order)

## Outcome

The rendered deck went **14 → 8 slides**. Six methodology slides were archived out of the
build; the deck — which had been **silently broken** on a removed `house_table` primitive —
now builds green again, with the two offending slides re-ported to general `table()`
primitives and **all eight** rendered modules hand-annotated to the
`style_library` study-corpus convention. Every step was held to a produced-XML **byte
gate**; no PNG render pass (standing preference — memory `awards-deck-visual-qa`). Nothing
committed (changes staged in git).

---

## Phase 1 — Archive slides 7–12 (+ their helper)

Per the user, the slides rendering as **7–12** were taken out of `SLIDE_RENDERS` and moved to
`deck_primary/deck_primary/archived/` (a new holding dir, not a package — archived modules are
not imported):

| former slide | module |
|---|---|
| 7  | `outsourcing_ceiling_method` |
| 8  | `outsourcing_ceiling_method_v2` |
| 9  | `outsourcing_ceiling_method_v3` |
| 10 | `outsourcing_ceiling_results` |
| 11 | `supplier_lane_method_part1` |
| 12 | `supplier_lane_method_part2` |
| —  | `_lane_method_kit.py` (shared helper, imported **only** by part1/part2 — moved with them so the archive is a self-contained, restorable unit) |

- Moves done with `git mv` (recorded as renames). Verified first that **nothing outside the
  archived set** referenced these (no refs in `_qa/`, `lib.py`, `build_deck.py`; the only
  intra-package import was part1/part2 → `_lane_method_kit`, both archived). None of the six
  read `_chart_xml/` assets (method/results built fresh; the lane pair uses the kit), so no
  assets had to move.
- `slides/__init__.py`: removed the 6 imports + 6 `SLIDE_RENDERS` entries; former slides
  **13/14 renumbered to 7/8**; docstring refreshed to describe the 8-slide deck + the archival.
- The unrelated, already-unregistered twin `slides/outsourced_bc_annual_tam.py` (the superseded
  v3-slide-3 verbatim port) was **left untouched** — it was a candidate in an earlier framing of
  the task that the user redirected away from.

New 8-slide deck: `outsourced_bc_walk`, `worktype_by_program`, `outsourced_bc_annual_tam_ref`,
`penetration_outlook`, `worktype_by_fy`, `contracts_outlook_placeholder`,
`sam_methodology_outsourcing_ceiling_questions_v2`, `data_reference`.

---

## Phase 2 — Discovered: the deck was already broken on `house_table`

The first build attempt raised `ImportError: cannot import name 'house_table' from
'deck_core.primitives'`. Findings:

- **`house_table` is no longer defined in `deck_core/primitives.py`** — absent in the working
  tree *and* in `HEAD` (removed in the latest commit `2a956809 "Reorganize projects tree; fold in
  working-tree WIP"`; it lingers only in stale comment/docstring mentions). This is the
  house-primitive phase-out described in the `style_library` logs.
- **Two *kept* modules still import it:** `sam_methodology_outsourcing_ceiling_questions_v2`
  (slide 7) and `data_reference` (slide 8). So the deck had been unbuildable independent of the
  archival; the on-disk pptx was a stale Jun-20 build.
- **None of the six archived modules** imported `house_table` (`outsourcing_ceiling_method` only
  name-drops it in a comment, having already been built on low-level `table()`).

The user decided **not to restore `house_table`** ("we are not bringing house_table back — gotta
do it this way") and to fix the two modules via the converter.

---

## Phase 3 — Re-port the two broken slides through `convert_slide.py`

The converter at `projects/style_library/_tools/convert_slide.py` emits the **general**
`table()/trow()/tcell()` primitives (zero `house_table`), so re-porting the two table slides
removes the dependency.

**Source = the deck's OWN build output.** `sam_methodology` and `data_reference` were authored
fresh in Python (no think-cell source deck exists), so their only rendered form is the pipeline's
output pptx. Both module files predate the stale build and were unchanged since, so the output
faithfully captures their current content. Converted **slide 13 → sam_methodology, slide 14 →
data_reference**:

```bash
python3 projects/style_library/_tools/convert_slide.py \
  "…/deck_primary/20260610_Distributed Shipbuilding New Construction_vS.pptx" 13 \
  --out "…/slides/sam_methodology_outsourcing_ceiling_questions_v2.py" \
  --src-dir <scratch>/_src_unused \
  --module-name sam_methodology_outsourcing_ceiling_questions_v2 \
  --layout slideLayout4 --deck-name "Distributed Shipbuilding New Construction"
# …and the same for slide 14 → data_reference
```
(`--src-dir` pointed at scratch: these are table-only slides, so no chart parts are written;
the emitted `CHARTS = []` and the `_SRC` line are dead, matching the corpus's table modules.)

Result: both re-ported, **0 `house_table`**, deck builds **green (8 slides, 5 charts)**, all rels
resolve.

**Faithfulness (content/structure, since byte-identity isn't expected across a primitive swap):**
| slide | tables / rows / cells | text |
|---|---|---|
| 7 `sam_methodology` | 1 / 9 / 27 — match original | identical |
| 8 `data_reference`  | 3 / 17 / 67 — match original | identical |

Byte deltas vs the originals are only `table()`-vs-`house_table` XML + `IN()` 3-decimal rounding
(sub-0.05px). **Tradeoff (accepted):** the re-port flattens the hand-authored data-driven
authoring (`_ROWS` / `_PIID_ROWS`) and the original INTENT docstrings → recoverable via git.

---

## Phase 4 — Polish all 8 rendered modules to the EXHIBIT/CODE MAP convention

Reference corpus studied: `projects/style_library/library/library/slides/` (canonical
`funding_components.py`; table-heavy `approach_unit_economics.py`). The convention per module:
provenance line → `EXHIBIT —` paragraph → `CODE MAP` bullets (paint order) → an honest
annotation note → `Converter stats` / `Structure` (+ `Residue` where apt), plus `# ── section ──`
headers and a table-cell layout-commentary block where the body warrants them.

- **Two re-ported modules** (slides 7/8): full treatment — docstring + table-cell commentary
  block + `# ── section ──` headers. Note reads *"byte-identical to the raw re-port."*
- **Six hand-authored modules** (slides 1–6): **docstring-focused** polish (their `_body()` is a
  one-line verbatim concatenation, and the big reference module already carries its own
  `# ═══ section ═══` banners — so docstrings are where the convention adds value, matching how
  the corpus treats verbatim/reference modules). **Honest provenance preserved:** these are
  *hand-authored 1:1 ports* (verbatim-XML transcriptions from `_chart_xml/` + native charts via
  `editable_bundled_chart`), **not** converter output — so their note reads *"Hand-authored
  port… byte-identical to the pre-annotation module,"* never "auto-converted." The slide-3
  reference module's rich teaching content (the chart semantic mirror, 8 named layers, the
  data-driven penetration layer) was reframed under EXHIBIT/CODE MAP, not discarded.

> Method note: attempted a parallel-subagent fan-out (the `style_library` polish workflow) but
> the Agent/Bash classifier was briefly unavailable, so the six were polished directly with
> Read/Edit. Same discipline, same byte gate.

---

## Verification (build-green + rels + byte gate; no PNG)

- **Build:** `wrote … (8 slides, 5 charts)`. (The 14-slide build had 6 charts; the one dropped
  chart belonged to the archived `outsourcing_ceiling_results`.)
- **Rels resolve** both directions for all slide+chart parts (mandatory — PowerPoint silently
  *repairs* dangling `r:id`; soffice won't catch it. memory
  `pptx-port-dangling-rels-cause-powerpoint-repair`).
- **Byte gate held twice.** After the slide-7/8 polish: all 8 `slideN.xml` byte-identical to the
  pre-polish (post-re-port) build. After the slides-1–6 polish: all 8 byte-identical to that
  baseline. So every annotation pass was provably docstring/comment-only — **zero pixels moved**.
- All 8 modules `py_compile` clean.

---

## Files touched (nothing committed)

- **Renamed → `archived/`** (7): `outsourcing_ceiling_method[/_v2/_v3].py`,
  `outsourcing_ceiling_results.py`, `supplier_lane_method_part1/part2.py`, `_lane_method_kit.py`.
- **`slides/__init__.py`** — registry trimmed 14 → 8; docstring updated.
- **Re-ported + polished:** `sam_methodology_outsourcing_ceiling_questions_v2.py`,
  `data_reference.py`.
- **Polished (docstring):** `outsourced_bc_walk.py`, `worktype_by_program.py`,
  `outsourced_bc_annual_tam_ref.py`, `penetration_outlook.py`, `worktype_by_fy.py`,
  `contracts_outlook_placeholder.py`.
- **Rebuilt:** the output `.pptx`.
- **Untouched:** the unregistered twin `outsourced_bc_annual_tam.py`; `deck_core/` (no engine
  change — we routed *around* the missing `house_table`, did not restore it).

---

## For the next agent

- **Eyeball pass owed** (no PNG run): slides 7 (`sam_methodology`) and 8 (`data_reference`) are
  the only renders that changed this session, and only by the `table()`-vs-`house_table` swap +
  `IN()` rounding — worth a glance. Slides 1–6 are byte-identical to before.
- **`house_table` is gone for good here.** Any *other* deck/module still importing it will break
  the same way; port it to `table()/trow()/tcell()` (or re-port via `convert_slide.py`), don't
  reintroduce the primitive. The archived `outsourcing_ceiling_method.py` is an in-repo worked
  example of a hand `house_table → table()` port.
- **Restoring an archived slide** = `git mv` it back from `archived/` (bring `_lane_method_kit.py`
  too for the lane pair) + re-add its import and `SLIDE_RENDERS` entry in source order.
- **The two re-ported modules are flatter than hand-authored.** If you want their data-driven
  authoring back, the originals are in git history; otherwise leave as-is (faithful render).
- **Convention reference:** `projects/style_library/library/library/slides/` and the spec used
  this session, `<scratch>/POLISH_SPEC.md`. Memories: `pptx-to-idiomatic-module-workflow`,
  `styled-chart-data-over-template`, `pptx-port-dangling-rels-cause-powerpoint-repair`,
  `awards-deck-visual-qa`, `house-table-row-height-is-a-minimum`.
