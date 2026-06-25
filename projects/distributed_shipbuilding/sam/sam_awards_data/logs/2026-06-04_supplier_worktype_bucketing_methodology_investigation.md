# 2026-06-04 — Supplier work-type bucketing: methodology investigation + entity-resolution evidence pass (analysis only)

## Scope

Investigated the long-standing discrepancy between how the **DDG** and **submarine** workbooks
sort suppliers into the seven work-type buckets, decided on a standardized methodology, and ran a
targeted evidence pass to classify the firms that move the answer. **Analysis / decision / handoff
session only — no build code changed, no workbooks rebuilt.** All outputs are reference + decision
artifacts (briefings, an evidence registry, and a handoff for the implementing agent).

The discrepancy: **DDG is description-led** (award `description_of_requirement` primary, NAICS
fallback, record-level — a vendor can split across buckets); **submarines is NAICS-led** (vendor
NAICS primary + a hand `VENDOR_BUCKET_OVERRIDES` list, vendor-level on the top-150 lookup). Same
supplier could land in different buckets across the two books. Logic lives in each project's
`sheets/taxonomy.py` (DDG: `_taxonomy.py`) `classify()`, consumed in `data_entity_master.py`.

---

## What was established (data-grounded)

1. **No subawardee NAICS exists in the source.** FFATA/FSRS subaward records carry only the *prime's*
   NAICS; the supplier's own NAICS comes only from `entity_naics_lookup.csv` (SAM Entity API,
   top-150 cap). The ~14–20%-of-$ "not_found" hole is **structurally unrecoverable** (non-registered/
   foreign/holding UEIs have no `assertions.goodsAndServices` NAICS) — verified against the live API.
2. **Description is a weak, misleading signal** — resolves a work bucket for <2% of $ uniquely; one
   keyword (`"module"`) mis-bucketed $1.4B of VLS missile work as structural. Descriptions for the
   residual firms are program/admin boilerplate ("ADMIN MOD", "SSN CONSTRUCTION", "FUNDING").
3. **The `electrical` bucket (the biggest) was ~94–97% defense electronics via a NAICS artifact**
   (`3364` aerospace → electrical, a deliberate hack). Leonardo / Northrop / GE were the largest
   "suppliers", classified by a corporate-NAICS artifact.
4. **The decisive method = operating-entity resolution.** Looking up each record's `sub_entity_uei`
   in the SAM Entity API → operating entity legal name + primary NAICS is far more reliable than the
   description (carries the prime CLIN) or the parent brand (too coarse). It flipped the biggest
   calls and even corrected the research agents' brand-level reads.

## Decisions taken (accepted by owner)

Standardize both books on **NAICS-primary + evidence-backed overrides at `firm_entity` grain**;
classify by **operating-entity NAICS**, not brand/description. Keep bucket **keys** stable (rename
display labels only). Remove auto `3364`/`3344`→electrical. Add `mission_systems` / `service` /
`holding` / `foreign_fms` as first-class **excluded** roles. **Combat/mission systems excluded** from
the HM&E physical-supplier base on market-definition grounds (not "GFE"). **Signed dollars**
throughout. Modular = a scenario **tag**, not an 8th bucket.

## The reversal (entity-resolved)

- **DDG "electrical" was mostly weapons electronics** → Leonardo $1.68B = DRS VLS launch-control
  electronics (DRS Training & Control 334220 + Laurel Technologies 334511) → **out** (base case,
  boundary). Real DDG yard electrical ≈ $346M.
- **Submarine "electrical" is mostly real power equipment** → Northrop $1.4B = NG Sunnyvale turbine
  generators (335312/333611); Leonardo-subs = DRS Naval Power switchgear (335311/335313) → **in**.
- Physical VLS launcher cells (Major Tool/Superior/Merrill) → `machining`, **in**. ESCO/VACCO →
  `piping` (recovered from holding-residual). GE → `machining` (LM2500 propulsion).

## Three-view bridge (signed $, entity-resolved, top-45 entities = $10.8B of $17.3B)

| | DDG | Subs |
|---|--:|--:|
| Total visible subaward flow | $11,202M | $6,139M |
| **Physical HM&E base** | **$3,454M (31%)** | **$4,418M (72%)** |
| Excluded: VLS launch-control *(boundary)* | $1,678M | $1M |
| Excluded: mission systems | $659M | $117M |
| Excluded: services/IT/holding | $1,550M | $0M |
| Excluded: foreign/FMS | $261M | $84M |
| Dropped: prime/GFE | $456M | $67M |
| Residual (unresolved tail — a FLOOR) | $3,145M (28%) | $1,453M (24%) |

VLS-control sensitivity: DDG physical base $3.45B (out) vs $5.13B (in).

---

## Verification

| Check | Result |
|---|---|
| Build code changed | **none** — taxonomy/model/sheets untouched this session |
| Workbooks rebuilt | no (no code change; last known-green builds stand) |
| SAM Entity API | validated working (single-UEI v3 calls; batch multi-UEI returns empty) |
| Bridge dollars | signed (de-obligations net out; e.g. Northrop subs −$142.7M CLIN realignment) |
| Registry | 45 entities, $10,817M, written to `projects2/vendor_evidence_registry.csv` |

## Files touched

- **Created (reference / decision, all in `projects2/` root):**
  `2026-06-04_supplier_worktype_bucketing_methodology.md` (briefing #1),
  `2026-06-04_supplier_bucketing_FOLLOWUP_combat_systems_decision.md` (memo #2),
  `bucket_taxonomy_brief.md` (cold-start taxonomy brief),
  `2026-06-04_supplier_bucketing_MEMO3_entity_resolution_results.md` (memo #3),
  `vendor_evidence_registry.csv` (45-entity registry),
  `2026-06-04_HANDOFF_supplier_bucketing_NEXT_AGENT.md` (implementation handoff).
- **This log.**
- **Memory:** `supplier-worktype-bucketing-methodology.md` updated (entity-resolution method +
  corrected asymmetry).
- **No project code / no `deck_core` / `workbook_core` / no slide or sheet modules edited.**

## Open items / follow-ups (the next task — see the handoff)

- **A. Model-chain trace** — does revised classification move the headline modeled TAM (via the
  supplier coefficient) or only bucket shares? Trace `model_tam_build.py`.
- **B. Tail entity-resolution** — extend SAM operating-entity resolution to every entity ≥ $20–25M
  signed (DDG+subs); cache; classify; leave low-confidence as residual.
- **C. Registry + implementation** — finalize `vendor_evidence_registry.csv` and wire it into the
  workbook classification path (both books, entity-grain). Note: subs currently classifies the
  vendor-level lookup, not records — moving it to record-level (like DDG) is the clean way to use
  entity-grain overrides.
- **D. Scenario flags** — keep overlapping; note the HM&E definition difference (current
  `piping+hvac+machining` vs proposed `machining+piping+electrical+hvac`).
- **E/F. Reconciliation + checks** — 5-view bridge, top-25 movers, bucket-share old→new, residual
  composition, VLS sensitivity, TAM-vs-shares note. **Do not rewrite decks yet** — owner signs off on
  the market definition from the tables first.
