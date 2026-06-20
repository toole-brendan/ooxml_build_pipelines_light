# Plan: Order of Operations for MRO Deck Revisions

_Drafted 2026-04-22. Sequences the 4 todos off your stream-of-consciousness list + blocker. Updated for v1.17 slide numbering (23 slides, new S05 Definitions)._

## Context

You sent v1.2 (5 slides) to boss on ~2026-04-17; he replied with comments covering 5 themes (TAM clarity, Marauder sizing, work-segment split, prime/HII separation, market share + geography). You've since rebuilt into a 23-slide architecture in [deck_script/](deck_script/) (v1.17 is the latest output). Most boss comments are already addressed structurally by the new manifest. Four loose ends remain:

1. PSC 1905 embedded MRO is estimated as a heuristic range but not rolled into the $7.067B TAM.
2. SAM (depot repair on Marauder-like vessels) is now formally defined on [S05 Definitions](deck_script/slide_copy.yaml) as "Depot Ship Repair spend on Marauder-type platforms" but is not yet sized anywhere in the deck.
3. Awards vs. budget reconciliation is currently awards-first with budget "adjacent" — boss asked whether they tie.
4. 23 slides is too many for the boss review — target is ~14-16 visible.

### Your decisions from clarifying questions
- **TAM posture:** reconciled into TAM, verified by a fresh classification run at the per-mod PIID level against raw FPDS JSON. **No heuristic provisionals — the number gets locked first, then cascades.**
- **Audience:** Mid-path (~14-16 slides) — cut clearly redundant slides, hide the rest to preserve appendix for internal use.
- **SAM placement:** Merge as an added row into the S23 TAM Framing matrix; leave S11 as Marauder TAM.

### Hard blocker
The three raw JSONs (`navy_awards_master.json`, `cg_awards_master.json`, `approp_rollup_imputed.json`) are on the other machine, per [OPEN_QUESTION_psc_1905_embedded_mro.md](OPEN_QUESTION_psc_1905_embedded_mro.md). All TAM-number work is blocked on transfer. The existing heuristic cascade yields a range ($1,553M / $1,647M / $1,912M) with ±$150-200M residual uncertainty — **not good enough for a headline number**, so no slide work that touches the TAM figure starts until Step 2 is complete.

### New-manifest quick reference (v1.17)
Key re-numbered slides you'll touch downstream:

| v1.17 spec_id | Title | Was in v1.4 |
|---|---|---|
| **S05** | Definitions (new) | — |
| **S07** | MRO Work Segments | S06 |
| **S08** | TAM Composition | S07 |
| **S11** | Marauder-Like Platform TAM | S10 |
| **S12** | Appropriation Sourcing | S11 |
| **S14** | Depot Geographic Footprint | S13 |
| **S17** | Prime Landscape - Total MRO | S16 |
| **S18** | Prime Landscape - Depot | S17 |
| **S19 / S20** | HII Mission Tech Overview / Financials | S18 / S19 |
| **S22** | Scope Reconciliation | S21 |
| **S23** | TAM Framing | S22 |

---

## Recommended order

### Step 1 — Transfer the 3 JSONs to this machine (prerequisite)
**Why first.** Everything downstream is blocked on this. No heuristic fallback — the whole sequence waits.

**Actions.** Copy from the other machine to `data_pull/output/fpds/` (or wherever [build_script/psc_1905_classifier.py](build_script/psc_1905_classifier.py) expects inputs):
- `navy_awards_master.json`
- `cg_awards_master.json`
- `approp_rollup_imputed.json`

**Effort:** Small (file transfer), but offline / manual.
**Verify:** All 3 files land; `psc_1905_classifier.py` can read them without a missing-path error.

---

### Step 2 — Classify PSC 1905 at mod level to lock the embedded MRO number
**Why second.** This is the work that converts the $1.5-2.0B range into a single defensible number. Following the "Recommended sequence" in [OPEN_QUESTION_psc_1905_embedded_mro.md §"Likely path to a single defensible answer"](OPEN_QUESTION_psc_1905_embedded_mro.md):

1. **TAS-first pass.** For each of the 201 PSC 1905 PIIDs, join `approp_rollup_imputed.json` to get Treasury Account Symbol → budget line item. Clean classifications:
   - SCN LI 2086 "CVN Refueling Overhauls" → MRO
   - SCN LI 1045 Columbia → Newbuild
   - SCN LI 2013 Virginia construction → Newbuild
   - OMN SAG 1B4B Ship Maintenance → MRO
   - OPN BA-01 LI 1000 CNO availabilities → MRO
   
   Expected: 60-80% of dollars cleanly classified.

2. **Mod-level LLM pass.** For residual ambiguous PIIDs, explode to mods using `navy_awards_master.json` / `cg_awards_master.json` (which preserve per-mod descriptions + obligations; the current `data/base_data.xlsx` collapses them). Classify each mod individually via LLM (reuse the pipeline pattern from [build_script/sheets/services.py](build_script/sheets/services.py) `llm_exclusions.json`). Aggregate dollars by mod classification.

3. **Reconcile.** TAS answer vs. LLM answer must agree on dollars where both fire. Flag divergences for spot-check (sort by $M, manual review top 10).

4. **Validate top-$ PIIDs.** Electric Boat SSN Seam Split Repairs ($831M) and USS Boise SSN-764 EOH ($424M) should come out as MRO in the final classification.

**Outcome:** `PSC 1905 embedded MRO = $X,XXXM` per supergroup (submarines vs. carriers vs. other), ready to fold into the Services TAM as an additive correction. This also updates the `PSC1905_MRO_EMBEDDED` named range in the `Reconciliation` sheet of [build_script_slim/output/08APR2028_MRO_Spend_v4.1.xlsx](build_script_slim/output/08APR2028_MRO_Spend_v4.1.xlsx).

**Effort:** Medium (infrastructure extension, not new research — classifier + services LLM patterns are already in place).
**Verify:** Single number, not a range. TAS-classified portion matches LLM-classified portion within tolerance on overlapping dollars. Workbook `PSC1905_MRO_EMBEDDED` cell is updated.

---

### Step 3 — Lock reconciliation approach and cascade verified TAM number across slides
**Why third.** Methodology narrative and TAM number update together — both depend on the Step 2 result. Doing one without the other risks inconsistent messaging (e.g., "awards-first methodology" next to a reconciled headline number).

**Actions.**

**3a. Methodology narrative (answers boss's "do FPDS and Budget reconcile?" question):**
- [slide_copy.yaml S22:502](deck_script/slide_copy.yaml) lede currently reads "measures from FPDS contract awards, with budget materials reconciling adjacent non-contract scope" — rewrite to describe PSC 1905 MRO as **inside** the reconciled TAM.
- [slide_copy.yaml S22:517,523](deck_script/slide_copy.yaml) matrix cells: replace "$7,067M FY2025 MRO TAM" with reconciled total; strip "includes ~$1.5 to 2.0B embedded MRO" from the PSC 1905 cell (that $ now lives inside the TAM).
- [slide_copy.yaml S22:541-546](deck_script/slide_copy.yaml) "PSC 1905 embedded MRO" callout: replace the $1.5-2.0B range with the verified number; remove "Not double-counted into the $7.1B TAM; sits adjacent" language.
- Add a single-sentence answer to boss's reconciliation question on [S02](decks/Boss_comments.txt) Overview or [S04](deck_script/slide_copy.yaml) TAM Sizing Approach.
- Update [S05:47-51](deck_script/slide_copy.yaml) Definitions table if any dollar figures appear (currently descriptive only — should survive).

**3b. TAM number cascade** — replace $7.067B / $7.1B with the reconciled total everywhere:
- [slide_copy.yaml S04](deck_script/slide_copy.yaml) TAM Sizing Approach headline.
- [slide_copy.yaml S08:61](deck_script/slide_copy.yaml) lede depot % (denominator changes) and [S08:75](deck_script/slide_copy.yaml) chart Total label ("$7,067M FY2025 MRO TAM").
- [slide_copy.yaml S08:86-112](deck_script/slide_copy.yaml) 5 work-segment callouts: $ totals may not change, but % shares will (denominator shifts).
- [slide_copy.yaml S11](deck_script/slide_copy.yaml) Marauder-Like Platform TAM — confirm denominator references tie.
- [slide_copy.yaml S23:740](deck_script/slide_copy.yaml) Frame A lede and [S23:761](deck_script/slide_copy.yaml) matrix Total row ("$7,067").
- **S08 Marimekko decision:** add a 6th category "Embedded Submarine/Carrier MRO" OR keep 5 categories and footnote the uplift. Marimekko is think-cell manual-add per [slide_copy.yaml:69-77](deck_script/slide_copy.yaml); this is a think-cell edit, not a code change.

**Effort:** Medium (number cascade across 5-7 slides + one Marimekko rebuild).
**Verify:** `grep -n "7,067\|7.1B\|\$7.1" deck_script/slide_copy.yaml` returns zero stale references. Every visible TAM figure on every slide is the same number. S22 lede no longer uses "adjacent" language for PSC 1905.

---

### Step 4 — Add SAM row to S23 TAM Framing matrix
**Why fourth.** Depends on locked TAM framework from Step 3. Small additive change once the rest is stable. SAM is already formally defined on [S05:49](deck_script/slide_copy.yaml) as "Depot Ship Repair spend on Marauder-type platforms" — Step 4 just sizes it.

**Actions.**
- Extend the S23 matrix at [slide_copy.yaml:744-761](deck_script/slide_copy.yaml) with a "SAM — Depot repair on Marauder-like hulls" row below Total.
- Data source: intersect S11's MSC comp-set (T-AKE, T-AO, T-AOE, LMSR Bob Hope/Watson, USNS Cape, T-EPF, T-AH, T-ARC, T-AGS) with Depot Ship Repair PSC filter on the `Depot Ship Repair` sheet of [08APR2028_MRO_Spend_v4.1.xlsx](build_script_slim/output/08APR2028_MRO_Spend_v4.1.xlsx). Add a `SAM_Marauder_Depot` cell via SUMIFS if not already present.
- Update [S23:740](deck_script/slide_copy.yaml) lede to mention the TAM → Marauder TAM → SAM progression.
- Adjust `row_heights_in` at [slide_copy.yaml:753](deck_script/slide_copy.yaml) from current 7 rows to 8 (add one 0.40 entry).
- Cross-check S23 SAM value against the S05 SAM definition so the two pages speak consistently.

**Effort:** Small.
**Verify:** SAM $ ≤ Marauder-Like TAM (S11) ≤ Total TAM (S23 Total row). Arithmetic ties on S23 and matches the S05 definition wording.

---

### Step 5 — Cull to ~14-16 visible slides; hide the rest
**Why last.** Cannot confidently cut until the TAM/SAM story is locked — cutting earlier risks removing a slide you later need.

**Candidate cuts / hides** (validate each against boss's 5 comment themes):
- **S04 TAM Sizing Approach** — hide if S22 carries methodology; keep if you want a front-loaded methodology page.
- **S05 Definitions** — load-bearing now (defines TAM and SAM cleanly for the boss); keep visible.
- **S09 Vessel Archetypes + S10 Fleet Reference** — boss asked for "pictures of the most common ships within the categories and lists the others"; S09 likely satisfies. Hide S10 if redundant.
- **S12 Appropriation Sourcing** — tangential to boss's 5 themes. Candidate for hide unless load-bearing for OMN/OPN reconciliation.
- **S14 Depot Geographic Footprint** — directly addresses boss's "where is work performed" ask; keep.
- **S18 Prime Landscape - Depot** — possibly redundant with S17; collapse or hide one.
- **S19 / S20 HII Mission Tech Overview / Financials** — boss explicitly asked for the split; keep both.
- **S23 TAM Framing** — now carries the SAM row, load-bearing; keep (possibly move out of appendix).

**Mechanism.** Hide via PPT slide-hide on the output (right-click slide → Hide Slide) so appendix survives for internal use. Cutting from [manifest.json](deck_script/manifest.json) removes from build entirely; prefer hide over cut unless certain.

**Effort:** Small (decisions + toggles).
**Verify:** Every one of boss's 5 comment themes is addressed by at least one visible slide. Visible deck flows narratively end-to-end when read without hidden slides.

---

## Summary table

| Step | What | Blocker | Effort | Hard prerequisite |
|---|---|---|---|---|
| 1 | Transfer 3 JSONs to this machine | Offline | Small | — |
| 2 | Run TAS + mod-level LLM classification → lock $ number | — | Medium | Step 1 |
| 3 | Lock reconciliation narrative + cascade TAM number across slides | — | Medium | Step 2 |
| 4 | Add SAM row to S23 matrix | — | Small | Step 3 |
| 5 | Cull / hide to ~14-16 visible slides | — | Small | Step 4 |

**No parallelism.** Every TAM-touching slide waits for Step 2 to lock the number. If the boss review has a near-term deadline, the critical path is Step 1 → 2 — everything else is fast once the number is verified.

---

## Critical files

- [deck_script/slide_copy.yaml](deck_script/slide_copy.yaml) — all slide text
- [deck_script/manifest.json](deck_script/manifest.json) — slide spec_id ↔ pptx_index map (23 slides)
- [deck_script/build_deck.py](deck_script/build_deck.py) — build orchestrator
- [deck_script/output/PA_MRO_Deck_v1.17.pptx](deck_script/output/PA_MRO_Deck_v1.17.pptx) — latest build
- [build_script/psc_1905_classifier.py](build_script/psc_1905_classifier.py) — existing 3-tier cascade; extend with TAS + mod-level LLM
- [build_script/sheets/services.py](build_script/sheets/services.py) — pattern to copy for the mod-level LLM harness
- [build_script_slim/output/08APR2028_MRO_Spend_v4.1.xlsx](build_script_slim/output/08APR2028_MRO_Spend_v4.1.xlsx) — data workbook; `Reconciliation` sheet holds `PSC1905_MRO_EMBEDDED` named range
- [OPEN_QUESTION_psc_1905_embedded_mro.md](OPEN_QUESTION_psc_1905_embedded_mro.md) — full classification methodology + blocker details
- [decks/Boss_comments.txt](decks/Boss_comments.txt) — reference for narrative cull decisions

## End-to-end verification

1. Build the deck: `python -m deck_script.build_deck` from the `PA MRO` root.
2. Open the new v1.x output in PowerPoint.
3. Walk slide-by-slide with [Boss_comments.txt](decks/Boss_comments.txt) open — every bullet boss raised maps to a visible slide.
4. TAM consistency: the headline TAM on S02/S04/S05/S08/S22/S23 is the same number everywhere.
5. SAM ≤ Marauder TAM ≤ Total TAM arithmetic ties on S23 and matches the S05 definition.
6. `grep -n "7,067\|\$7.1" deck_script/slide_copy.yaml` — expect zero matches after Step 3.
7. Workbook `PSC1905_MRO_EMBEDDED` cell holds the verified single number (not a range).
