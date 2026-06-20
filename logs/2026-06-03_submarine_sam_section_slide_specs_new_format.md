# 2026-06-03 — Submarine SAM-section slide specs (S12-S16) rewritten into the SlideSpec format

## Scope

Rewrote, **in place**, the five submarine deck slide specs that have **no slide module**
into the new standardized SlideSpec format from `docs/spec_format/SPEC_FORMAT.md`. These are
the "specced-but-unbuilt" S12-S16 set (the deck's KNOWN GAP — Divider 3 + the SAM and
Supplier Landscape section), authored **fresh from each original spec's content**, not copied
from the worked example. The five:

| File (deck slide) | New-format shape | archetype |
|---|---|---|
| `work_type_taxonomy.md` (S12) | 7 bucket cards + gray residual card; **no chart/table** | `card_grid_taxonomy` |
| `bucket_tam.md` (S13) | ranked bar (7 buckets, avg annual TAM) + gray residual strip + note; `tables: []` explicit | `ranked_bar_plus_residual_strip` |
| `sam_scenarios.md` (S14) | ranked bar (5 scenarios) + no-fill composition rail + guardrail strip; **no table** | `ranked_bar_plus_guardrail_strip` |
| `visible_suppliers.md` (S15) | ranked bar (top 10) **+ evidence table** (chart-and-table case) | `ranked_bar_plus_evidence_table` |
| `sib_exclusion.md` (S16) | gray ranked bar (3 SIB entities) + treatment card + SIB/MIB note | `ranked_bar_plus_treatment_card` |

Specs only — **no slide modules built**, **no `deck_core` / README / registry changes**, and the
other 42 specs were left on their old formats. Specs are not read by any build, so there was no
rebuild; the work was audited mechanically against the format instead. Workspace is not under git.

Follows the [2026-06-03_slide_spec_format_standard_and_image_wiring] session that authored the
SlideSpec standard + two worked examples. This session is the first real use of that standard.

## 0. Decisions carried in from the user

- **Author fresh.** `example_submarines_bucket_tam.md` is a finished new-format version of S13,
  but its author-effort was unknown, so it was **not** used as a source; bucket_tam was re-derived
  from the original spec (the numbers tie out to the same workbook block anyway).
- **Read all of `deck_core`** (the engine the future build agent reads) so the specs speak the
  real token / primitive / factory / BODY-anchor vocabulary.
- **Pull commentary context** from `projects/submarines/research/wiki` and the finished workbook
  (`workbook_submarines`) to enrich each `reserve`.
- **SIB, not MIB.** "Maritime Industrial Base / MIB" → **SIB / Submarine Industrial Base** in all
  visible copy (the deck standardizes on SIB even though the wiki uses MIB).

## 1. What was read first

- **Engine (all of `deck_core`):** `style.py` (tokens, BODY box, chrome geometry), `slide_base_template.py`,
  `lib.py` (CHARTS/IMAGES rId wiring), `primitives.py` (text_box / house_table / picture / chrome
  builders), `charts.py` (`bar_chart`/`_bars` params + `graphic_frame`), `text_metrics.py`,
  `slide_guide.md`, `slide_snippets.md`, and the `slide_probe.py` lint/CLI surface.
- **The standard:** `docs/spec_format/SPEC_FORMAT.md` + both worked examples.
- **The 5 originals** (three legacy formats) and the deck registry (`slides/__init__.py`),
  which confirmed S12-S16 are unregistered and names `divider_sam_supplier` as the insert point.
- **Authoritative data (finished workbook):** `taxonomy.py` (7 buckets + NAICS-4 crosswalk),
  `model_sam_build.py` (5 scenarios; bucket composition; broad = TAM − unbucketed),
  `validation_sib_excluded.py` (3 SIB entities, ~$4,251.8M total), `chartdata_z_chart_data.py`
  (CD_13..CD_16 tie-outs).
- **Wiki facts** for source-tagging reserves (>$10B SIB investment; AUKUS 2.0→2.33 vs ~1.3/yr;
  HII +30% outsourcing; ~70% sole-source; FFATA visible ≈ 10-20% of the outsourced layer;
  ~759 parents; HII-NNS team-build gap; FAR 52.204-10 $30k threshold).

## 2. How each original mapped to the new format

- **`element_inventory` is the spine.** Every slide gets one registry of objects (position,
  prominence, paint order); `charts`/`tables`/`shapes`/`commentary` reference element ids and add
  only build detail. The card grid (S12) is one `diagram` element + a `shapes` entry carrying the
  seven cards as a `cards:` list (built by a `_grid_x` loop, 4-over-3).
- **Old "Speaker commentary" + "Suggested copy" → `commentary.reserve`** (ample `context` + nine
  region-tagged, source-tagged `approved_extra_points` per slide), per the format's intent.
- **Numbers carried verbatim** from each original's chart-data block; nothing recomputed. The SAM
  scenario composition was verified against the workbook: metal = structural+machining+castings =
  865.4; modular = structural+coatings = 726.0; HM&E = piping+HVAC+machining = 679.6; broad = sum
  of all seven = 2,805.5 (machining shared between metal and HM&E → the non-additive caveat).
- **Closed BODY-relative region grammar only** (`%`, `BODY_*`, `right_of`/`below`/`align_top`/
  `body_until`, `GAP`/`NOTE_H`/`TITLE_BAND_H`, `remaining`/`fit_content`) — no raw slide EMU.
- **Chart params** expressed in the real `bar_chart` vocabulary (`mode: ranked`,
  `data_point_colors` as ramp tokens, `value_axis_format`, `gap_width`, external `CHART_TITLE_10PT`
  title element, `title: null`).

## 3. Citation / terminology / token decisions

- **Real external citations only** in `chrome.sources` (SAM.gov FFATA/FSRS, SAM.gov Entity
  Management API, FAR 52.204-10, SCN Justification Books, GAO-25-106286). All internal provenance
  (CD IDs, workbook tabs, wiki chapters) lives only in `meta.inputs` / `tie_out` / `reserve.evidence`.
- **`visible_suppliers` source swap:** the original cited "CRS R41129"; replaced with **FAR
  52.204-10**, the regulation that actually bounds the "visible is a floor" claim (the $30k
  threshold + first-tier exclusions) — a more accurate citation for that slide.
- **SIB terminology** applied throughout; `sib_exclusion` keeps an explicit SIB/MIB reconciliation
  note and gray (exclusion) bar styling, never the counted-TAM/SAM blues.
- **`"Unbucketed / ambiguous"`** keeps its slash despite the no-`/` copy rule — it is the canonical
  residual label across the workbook cells, the originals, and the example; cross-artifact
  consistency wins.
- **Tokens only.** No raw hex/pt; the only sanctioned numerics are table `size: 900` and the
  documented `major_gridline_width: 3175` (0.25pt), both allowed by the format/snippets.

## 4. House-copy cleanup (post-draft pass)

- Removed **30 em dashes** (house rule: none) — swept `—` → `-` across all five files.
- Removed visible `+` / `/` separators from the `sam_scenarios` composition rail and bullets
  (rewritten to comma/`and` lists); `+`/`/` left only in internal `reserve` prose, matching the
  worked examples.
- Tightened the `sam_scenarios` title finding to use `~` and stay ≤2 lines:
  "Broad component manufacturing is the largest scenario at ~$2.8B per year".

## Verification

Specs are not on any build path, so the safety net is a mechanical audit against the format (no
rebuild possible; no module built):

| Check | Result |
|---|---|
| Required blocks (`meta`/`chrome`/`story`/`regions`/`element_inventory`/`reserve`/`qa`) | present in all 5 |
| Element-registry spine (every chart/table/shape/commentary ref resolves to an inventory id) | 0 dangling in all 5 |
| Tokens only (no raw hex) | 0 raw hex |
| Closed coordinate grammar (no raw slide EMU) | clean |
| Real-citations-only (no internal docs/tabs/CD IDs in `sources`) | clean |
| Em dashes | 0 |
| Visible `+`/`/` separators in rendered fields | 0 |
| SIB vs MIB (MIB only inside the `sib_exclusion` reconciliation note) | contained |
| Numbers tie to originals + workbook (CD_13/14/15/16; SIB total ~$4,251.8M; scenario composition) | tie out |

## Files touched

- **Rewritten in place** (`projects/submarines/deck/slide_specs/`): `work_type_taxonomy.md`,
  `bucket_tam.md`, `sam_scenarios.md`, `visible_suppliers.md`, `sib_exclusion.md`.
- No modules, `deck_core`, README, registry, or other specs changed.

## Open items / follow-ups

- **Specs only; modules still unbuilt.** S12-S16 remain unregistered (and `divider_sam_supplier`
  unwired). When the section is built, a future agent translates these specs → modules and inserts
  Divider 3 ahead of S12.
- **Mixed-format corpus.** The other 42 submarine + DDG specs still use the three legacy formats;
  migrating them is a separate pass.
- **`slide_order` 12-16 is notional** (deck-spec narrative position), pending registration.
- **Year ranges kept as hyphens** (`FY2022-FY2027`) to match the worked-example specs/originals;
  the rendered deck uses en dashes, applied by the build agent at render time.
- **`sam_scenarios` title** was tightened from the original "~$2.8B average annual SAM"; revert to
  the original phrasing if preferred.
