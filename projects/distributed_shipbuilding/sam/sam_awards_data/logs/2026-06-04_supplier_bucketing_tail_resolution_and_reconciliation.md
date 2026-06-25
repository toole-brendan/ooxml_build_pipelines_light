# 2026-06-04 — Supplier work-type bucketing: tail entity-resolution + reconciliation bridge (analysis only)

## Scope

Continued the supplier-bucketing handoff (`projects2/2026-06-04_HANDOFF_supplier_bucketing_NEXT_AGENT.md`),
executing the **analysis-first** half: tasks **A** (model-chain trace), **B** (tail entity-resolution),
**C-data** (extend the evidence registry), and **E/F** (5-view reconciliation bridge + final checks).
**No build code changed; no workbooks rebuilt; decks untouched.** The owner asked for the tables first to
sign off on the market definition before any wiring. Task C-wire and task D (scenario-flag edits in the
sheet modules) are designed in the plan but **deferred to Phase 2** pending sign-off.

Owner-confirmed decisions this session: analysis-first; tail floor **≥ $20M** combined-signed; **HM&E
scenario += electrical**; **submarines → record-level** at wiring time.

---

## What was done

1. **Task A — model-chain trace (conclusion).** Headline modeled TAM is **invariant** to reclassification
   in both projects. TAM = exogenous budget base (`data_scn_budget`) × a supplier coefficient computed
   from the **POP corpus** (`data_pop_corpus`); classification feeds only `observed_bucket_share_cell` →
   modeled share → `model_sam_build` bucket TAM → scenario SAM. Refs: `model_tam_build.py` DDG :96-100,
   141,164,312 / subs :71-74,139,166,254; `model_sam_build.py` DDG :144,180 / subs :117,141.
   `observed_addressable_total()` is runtime metadata, not a TAM input.
2. **Task B — tail resolution (≥ $20M).** 91 entities ≥ $20M not already in the registry; **33 required a
   live SAM call** (58 cached). All cached. Operating-entity resolution flipped many parent-brand reads
   (KKR→CIRCOR Naval, TOTAL→Hutchinson, Everest Kanto→CP Industries [US, not foreign], Arcline→Hunt Valve).
3. **Task C-data — registry extended 45 → 136 rows**, full Task-C schema, role vocab normalized
   (`mission`→`mission_systems`, `foreign`→`foreign_fms`, Arctic Slope→`holding`, VLS→`mission_systems`
   + `vls_boundary`); scenario_flags recomputed to Task-D defs (HM&E+=electrical; modular = explicit
   structural module-assembly flags, coatings dropped). §4 judgment overrides applied (HII→prime,
   BWXT→gfe naval-nuclear, BAE Land&Armaments/L3/Teledyne-Defense→mission, DRS Naval Power→electrical,
   Wärtsilä/Woodward/Barnes/Remmele→machining, Parker/Maxim-evaporators→piping, Howden→hvac,
   Applied-Composite→coatings). ~81% of the $17.3B flow is now identity-resolved by UEI.
4. **Tasks E/F — reconciliation.** Standalone engine (`reconcile.py`) reads both `nc_records_long.csv`
   (signed) + registry, applies the planned entity-grain ladder (registry-by-UEI → prime/gfe name →
   vendor override → NAICS4 *without 3364/3344* → service → 5511 holding → residual), and reproduces
   View 1 via the **live project taxonomies** (imported by path). Produced the 5-view bridge + top-25
   movers, bucket-share old→new, residual composition, VLS sensitivity, TAM-vs-shares note.

## Headline results (signed $)

- DDG physical HM&E base **53.9% → 35.8% ($6.0B → $4.0B)** base case; the drop is the **electrical
  collapse 23.8% → 5.7%** (weapons electronics → `mission_systems`). Subs base **78.2% → 77.8%**
  (electrical holds ~37% — real ship power stays in). This is the methodology's central asymmetry,
  confirmed at full scale.
- VLS launch-control: DDG physical **$4.0B (out) vs $5.7B (in)**, Δ **$1.678B**; subs ~$1M.
- Residual cut ~$1.4B by the tail pass (DDG $2.93B→$2.03B; subs $1.18B→$0.66B); floor now **$2.69B**.
- DDG machining 11.5% → 39.0% (Major Tool VLS **cells** ~$0.95B corrected off the "module"→structural
  keyword; GE LM2500 $333M).

---

## Verification

| Check | Result |
|---|---|
| Build code changed | **none** (taxonomy/model/sheets/core byte-identical after 19:30) |
| Workbooks rebuilt | no (analysis-first; last known-green builds stand) |
| Control totals | DDG $11,202M, subs $6,139M signed — every view's categories sum to total |
| SAM live calls | 33 (single-UEI v3), all cached to `research/sam_entity_lookups/` |
| Residual ties | F3 $2,690M = View 2 DDG $2,027M + subs $663M |
| VLS Δ | $1,678M = the two Leonardo DRS VLS UEIs |
| Registry backup | original 45 → `vendor_evidence_registry_v1_45.csv.bak` (no git net) |

## Files touched

- **Created (analysis, in repo):** `projects/research_shared/supplier_bucketing/{resolve_tail.py,
  finalize_registry.py, reconcile.py, tail_resolved.csv, reconciliation_output.md}`.
- **Created (projects2 root):** `2026-06-04_supplier_bucketing_RECONCILIATION_tables.md` (owner
  deliverable), `vendor_evidence_registry_v1_45.csv.bak`.
- **Updated:** `vendor_evidence_registry.csv` (45 → 136 rows, full schema).
- **Cache:** 33 new SAM entity JSONs under each project's `research/sam_entity_lookups/`.
- **This log.**
- **No `deck_core` / `workbook_core` / sheet / model / taxonomy modules edited.**

## Open items / next (Phase 2, after owner sign-off)

- Wire the registry into both books' `classify()` path (registry-by-`sub_entity_uei`, before the NAICS
  crosswalk); remove the DDG description step; remove `3364`/`3344`→electrical; add roles
  `mission_systems`/`holding`/`foreign_fms`.
- Move **subs `data_entity_master.py` to record-level**, preserving the accessors the SAM model reads
  (`observed_bucket_dollar_cell`, `observed_bucket_share_cell`, `addressable_total_cell`,
  `role_dollar_cell`, `grand_total_cell`).
- Apply Task-D scenario sets (HM&E+=electrical; modular={structural} bucket-level); rebuild both green.
- Place the canonical registry in-repo (`projects/research_shared/supplier_bucketing/`) for the build to
  read. **Do not touch the decks** until the owner signs off on the market definition.
