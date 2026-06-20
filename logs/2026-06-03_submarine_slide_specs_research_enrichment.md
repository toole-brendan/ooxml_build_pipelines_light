# 2026-06-03 — Submarine slide specs: merge alt-agent conversions + research/workbook enrichment, replace originals

## Scope

Finalized the **21 built-module submarine slide specs** by reconciling a set of
new-format conversions (authored by other AI agents that did **not** have access to
the research repo or workbook) against the research-grounded originals, verifying every
number against the actual workbook modules + research wiki, fleshing out the reserve /
sources, and **overwriting each original in place** with the cleared new-format version
(no backup — the new file replaces the old).

Input was six `~/Downloads/converted*` folders. First task was to **classify** them
submarine vs DDG; only the submarine set was in scope.

| Download folder | Project | Specs |
|---|---|---|
| `converted_slide_specs` | **submarine** | demand_backdrop, executive_summary, market_primer, methodology, sizing_boundary (5 body) |
| `converted_specs` | **submarine** | annual_cadence, ap_and_lltm, basic_construction, coefficient_evidence, data_limits, implications, tam_bridge (7 body) |
| `converted_slide_specs (1)` | **submarine** | 9 appendix (A1, A2, A4-A10 in the download's own numbering; A3 already removed) |
| `converted_slide_specs (2)` | DDG | tam_method, annual_tam_build, tam_timing, sam_taxonomy, worktype_allocation |
| `converted_slide_specs (3)` | DDG | market_primer, executive_summary, scope, cost_funnel, myp_redaction, appendix_bucket_rules |
| `converted_slide_specs (4)` | DDG | a01-a05 appendix |

The 21 submarine targets = 12 body (S02-S11, S17, S18) + 9 appendix (A1-A9). The five
**unbuilt** SAM-section specs (S12-S16: work_type_taxonomy, bucket_tam, sam_scenarios,
visible_suppliers, sib_exclusion) were migrated in an earlier session and were **out of
scope** — left untouched (and used `bucket_tam.md` as the gold-standard depth reference).

Workspace is **not** under git. Specs are not on any build path, so there was no rebuild;
the safety net was read-only research + a mechanical verification sweep over all 21 files.
`deck_core`, the DDG specs, the README, the registry, and the download sources were all
left unmodified.

---

## 1. Ground truth established first

Before fanning out, read the authoritative references so every agent spoke the engine's
real vocabulary: `docs/spec_format/SPEC_FORMAT.md` (the standard), `deck_core/style.py`
(the **only** valid tokens), the gold-standard `slide_specs/bucket_tam.md`, the deck
registry `deck_submarines/slides/__init__.py` (authoritative slide order + the contiguous
**A1-A9** appendix numbering after A3's removal), and the research layout
(`research/wiki/` 16 chapters + `workbook_submarines/sheets/` 24 modules).

## 2. Per-spec process (the 5-step ask)

For each spec: (1) read the new conversion (structure) + the original (research); (2) read
the mapped workbook module(s) + wiki chapter(s) and **verify every number**, correcting
drift, tagging anything unverifiable; (3) fold useful original content (speaker commentary
→ `reserve.context`, data deps → `meta.inputs`/`tie_out`, design notes → `story`/`qa`,
exact citation lines → `chrome.sources`); (4) flesh the reserve to gold depth (ample
`context` + 9-12 region/source-tagged `approved_extra_points`); (5) **overwrite** the
original at `projects/submarines/deck/slide_specs/<name>.md`.

## 3. Execution — 8 parallel research-grounded subagents

Grouped by shared research sources to minimize redundant reading:

- **G1** TAM core (basic_construction, tam_bridge, coefficient_evidence) — `model_tam_build`,
  `data_scn_budget`, `data_pop_corpus`, wiki 04/06/07.
- **G2** AP/LLTM + cadence (ap_and_lltm, annual_cadence) — `data_ap_bridge`, wiki 05/07/02.
- **G3** framing (market_primer, sizing_boundary, methodology) — `guide_methodology`, wiki 01/02/03/16/12.
- **G4** demand/exec/implications (demand_backdrop, executive_summary, implications) — `summary_executive_summary`, wiki 06/13/14/10/11/15.
- **G5** limits (data_limits, appendix_data_limitations_and_unseen_layer, appendix_qa_reconciliation) — `validation_*`, wiki 12/16/11.
- **G6** appendix A1/A2 (definitions_and_scope, model_map_and_figure_register) — `outputs_figure_register`, wiki 01/16.
- **G7** appendix A3/A4 (ap_and_lltm_detail, coefficient_sensitivity) — `data_ap_bridge`, `validation_sensitivity`, wiki 05/06.
- **G8** appendix A5/A6/A8 (sam_bucket_crosswalk, top_25_visible_suppliers, sib_exclusion_detail) — `taxonomy`, `model_sam_build`, `data_entity_master`, `validation_sib_excluded`, wiki 09/08/10.

**Hiccup:** a transient server-side rate limit ("not your usage limit") cut off four agents'
**final summary messages** — but the file writes had already landed. Filesystem mtime check
confirmed 19/21 written; only G8's `top_25_visible_suppliers` + `sib_exclusion_detail` were
unwritten. Re-dispatched a single fresh agent for those two (it also resolved the placeholder
ranks, below).

## 4. Corrections the research caught

- **`appendix_top_25_visible_suppliers` — placeholder ranks resolved.** The conversion left
  ranks 11-25 as `WORKBOOK_REQUIRED` (no data access). Filled all 15 from the entity master /
  CD_15 top-visible block + vendor-concentration wiki (Rosyth/Babcock $84.0M, W International
  ×2, Curtiss-Wright Flow Control, Oil States, …), with the duplicate-filer (two W
  International UEIs kept separate) and foreign-by-incorporation caveats preserved. Full
  two-panel `house_table` (ranks 1-13 / 14-25) specified; gray/BLUE_1 styling, never the
  counted-SAM blues.
- **Appendix numbering collision fixed.** Agents diverged: most used the registry-contiguous
  A1-A9, but the G5 agent used the download's A-numbers, producing a duplicate `subs-a8` and
  wrong ids. Renumbered to the registry: `data_limitations` **a8 → a7**, `qa_reconciliation`
  **a10 → a9**, and fixed the matching `related_appendix` pointer in `data_limits` (which
  backs `appendix_data_limitations_and_unseen_layer`). `sib_exclusion_detail` correctly keeps
  a8; `slide_order` normalized to the `A7`/`A9` sibling form.
- **2 YAML syntax errors** — region maps written `key:{x: …}` (missing the space YAML
  requires after a key) in `demand_backdrop` (×2) and `appendix_coefficient_sensitivity` (×1).
  Fixed to `key: {x: …}`.
- **Body slide_id de-padding** — `subs-s02`…`subs-s09` → `subs-s2`…`subs-s9`, for one
  uniform unpadded convention deck-wide (matches the appendix `subs-aN` and the 2-digit body
  ids). No other file referenced the padded ids.
- **2 comment em-dashes** normalized to hyphens (line-1 `# SlideSpec` comments) to match the
  gold-standard house style.

Key figures re-verified against the workbook/wiki and held: BC base $56.647B, strict applied
coefficient 35.0235% (shown 35.0%), cumulative TAM $19.840B, average annual TAM $3.307B, the
$36.807B removed prime/co-prime/excluded share, the AP/LLTM **$0 additive** guardrail, the
all-gated POP anchor 51.8% / applied 35.0% distinction, the SIB exclusion total $4,251.8M
(BlueForge $4,173.3M + TMG $77.0M + IALR $1.5M), and the seven work-type buckets + residual.

---

## Verification

| Check | Result |
|---|---|
| Specs rewritten | 21 (12 body + 9 appendix) |
| New-format (`meta:`… present) | 21/21 |
| Valid YAML (`yaml.safe_load`) | 21/21 after the `key:{…}` fixes |
| Required blocks (`meta`/`chrome`/`story`/`regions`/`element_inventory`/`qa` + `commentary.reserve`) | all present |
| Tokens-only (validated vs `style.py` colors/sizes/insets) | 0 invalid tokens |
| Coordinates (closed BODY-relative grammar, no raw slide EMU) | clean |
| `chrome.sources` = real external citations only (no wiki/workbook tab/CD_xx leakage) | clean |
| Em-dashes in rendered fields | 0 (remaining em-dashes are internal `context` prose only) |
| `module_name` == filename; `slide_id`/`order`/`section` vs registry | all consistent |
| Reserve depth | 9-12 `approved_extra_points` per spec; ample `context` |
| `WORKBOOK_REQUIRED`/`TBD` placeholders remaining | 0 (top-25 ranks 11-25 resolved) |
| DDG ↔ submarine cross-clobber | none (verified both directions) |

## Files touched

- **Rewritten in place** (`projects/submarines/deck/slide_specs/`): `market_primer`,
  `sizing_boundary`, `executive_summary`, `demand_backdrop`, `methodology`,
  `basic_construction`, `tam_bridge`, `annual_cadence`, `coefficient_evidence`,
  `ap_and_lltm`, `data_limits`, `implications`, and the 9 `appendix_*` specs
  (definitions_and_scope, model_map_and_figure_register, ap_and_lltm_detail,
  coefficient_sensitivity, sam_bucket_crosswalk, top_25_visible_suppliers,
  data_limitations_and_unseen_layer, sib_exclusion_detail, qa_reconciliation).
- **Not changed:** `deck_core/*`, the workbook + research (read-only), `docs/spec_format/*`,
  the registry, the README, the 5 unbuilt S12-S16 specs, and the `~/Downloads/converted*`
  sources.

## Open items / follow-ups

- **Concurrent DDG migration.** While this ran, the 16 DDG specs from download folders
  (2)/(3)/(4) were independently rewritten to new format (a parallel session) — left
  untouched per the submarine-only scope; verified **zero cross-clobber** in both directions.
- **Specs describe built modules, but were not rebuilt.** These 21 back already-built slide
  modules; the specs are documentation/handoff only and not on any build path, so no deck
  rebuild was run. If a module is later regenerated from its enriched spec, run `slide_probe`
  against it.
- **Mixed-provenance numbers flagged, not invented.** Where a figure is a wiki/industry band
  (e.g. the 50-65% outsourced band, the ~78%/~52% place-of-performance shares) rather than a
  single workbook cell, it is kept as evidence with an internal `tie_out` and labeled a band,
  never promoted to a headline coefficient.
- **`Source`/`Reads`/`Feeds`-style depth.** Reserve sections are now generous (the explicit
  ask); if a terser house form is later preferred, the `approved_extra_points` are the first
  trim target.
