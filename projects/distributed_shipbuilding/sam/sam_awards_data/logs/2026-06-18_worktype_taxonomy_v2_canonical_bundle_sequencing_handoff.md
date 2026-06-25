# 2026-06-18 — Work-Type Taxonomy v2: canonical bundle rebuild + AI-taxonomy-design handoff

**Mission for the next agent:** the user is **right now running an AI taxonomy-design agent**
on the canonical bundle this session built. When its output lands, (1) critically evaluate
it the way we evaluated the first attempt (see §6), (2) drive the targeted registry research
on the *contested* high-dollar entities it flags, (3) lock the taxonomy, then (4) implement
the v2 classifier and re-extract/rebuild the three deliverables (the big roadmap lives in the
2026-06-17 v2 handoff §8).

> ⚠️ Process discipline carried from prior sessions and reinforced hard this one:
> **verify against the data/code before asserting; separate "confirmed" (ran it) from
> "inferred" (looks like).** This session's biggest find was a provenance error that a
> verification step caught — see §3 and the Lessons.

---

## 0. TL;DR status

- **Architecture for v2: DECIDED** (two-track + multi-dimensional schema + SWBS-anchored). §4.
- **Canonical input bundle: BUILT & VERIFIED.** A wrong-universe bundle was caught and
  replaced. New bundle at `projects/research_shared/taxonomy_design_input_canonical/`. §3, §5.
- **Taxonomy-design agent: RUNNING NOW** (user's separate deep-agent run) on that bundle with
  the finalized prompt. §5. Output not yet in hand.
- **Sequencing taxonomy vs registry: DECIDED** — draft taxonomy first, then targeted research,
  then lock, then full enrich. §7.
- **First taxonomy attempt: evaluated, rejected on numbers (architecture kept).** §6.
- **Implementation: NOT STARTED.** No taxonomy/registry/workbook/deck code changed this session.

---

## 1. What this work is

Classifying Navy **new-construction subawards** (Virginia + Columbia submarines, DDG-51
destroyers) by **type of work**. v1 classifies the operating *entity* (registry-first, else a
NAICS-4 name/crosswalk ladder) and projects that onto all its subawards. v2 moves toward
**record-first where evidence exists, entity-fallback elsewhere**, with **SWBS/ESWBS** as the
canonical reference taxonomy. Background: the v1 methodology doc
(`/Users/brendantoole/projects3/worktype_classification_methodology.md`) and the two
2026-06-17 logs (v2 refactor handoff; DDG field-audit/SWBS-mining). The design dialogue that
motivated the pivot is `/Users/brendantoole/projects3/t1.rtf`.

---

## 2. Confirmed data constraints (verified live this session)

- **No subawardee NAICS/PSC on the transaction.** Entity NAICS/PSC come from a SAM entity
  lookup keyed by UEI. (Re-confirmed in the field audit; unchanged.)
- **Descriptions are bimodal:** submarine descriptions are junk; **HII-Ingalls DDG**
  descriptions carry a structured work-item code (`NNNNN-NN`) and often an explicit SWBS token.
- **HII code is a finer sub-index of SWBS, not a rival scheme.** Verified: of the 365 HII
  codes, **113 (≈31%) carry an explicit SWBS cross-ref; on those, code→SWBS purity = 100%**
  (each maps to exactly one 3-digit subsystem; subsystems fan out into several codes). Coverage
  by HII $: explicit token **55%**, propagated via pure stems **71%**, any code **85%**,
  coded-but-opaque tail **14%**. So HII can resolve *below* SWBS-subsystem; subs/BIW generally
  can't reach subsystem at all → **achievable granularity differs by segment**.
- **The "forged propulsion shaft" collision is real, not hypothetical.** Code
  `03003-01` = "PROPULSION SHAFT, FWD": **Ellwood National Forge $87.9M (NAICS 332111 forging)**
  and **Erie Forge & Steel $35.6M (NAICS 336611 shipbuilding)**. Classify the *vendor* → forging;
  classify the *subaward scope* → propulsion. Both true → justifies a primary-scope axis +
  separate process tags. NB: those shaft records have **blank `swbs_group`** — propulsion is
  read from description **text**, not SWBS; in submarines this collision is invisible.
- **Modular is not recoverable from records.** Scanned all HII descriptions: module/modular =
  10 recs / $0.7M, and they're component-name noise ("dryer module", "MODULE ALARM"), not ship
  modules (block=1, section=0). **Modular must remain an entity-level capability flag**
  (`entity_modular_capability`), sourced from the registry/research — it dropped out of both the
  taxonomy run (no data) and the current taxonomy prompt; re-insert it in the registry pass.

---

## 3. ⚠️ The provenance error that was caught and fixed (most important section)

**The first taxonomy bundle used the WRONG data universe.** It was assembled from
`projects/research_shared/sam_entity_enrichment/` — a *parallel* product built by
`pull_entities.py` / `profile_entities.py` that profiled the raw UEI list directly and **never
ran through `_corpus.iter_records`**, the stream the award-analysis workbook actually consumes.
Consequences, all verified:

| | wrong bundle (enrichment lineage) | canonical (`_corpus.iter_records`) |
|---|---|---|
| total $ | **$17,777M** | **$13,168M** (→ $13,111M after LCS strip) |
| program split | all `'ddg'` (broken) | submarines $9,563M / ddg $3,547M |
| BlueForge | **included, $4,173M** | $0 (excluded) |
| UEIs | 1,352 | 1,203 |

The $4.6B gap = pass-through/MIB exclusion (BlueForge + TMG + IALR) + out-of-scope work +
program attribution that `iter_records` applies and the enrichment scripts skipped.

**Canonical exclusion list is not hand-rolled** — it lives in `nc_scope_summary.json` under
`excluded_mib_ueis` (submarine side: `F8PEZKXES8B1` BlueForge, `QLJZVM6XKR71` Training
Modernization Group, `TCM3R4JPRKY4` IALR; DDG side: 0), applied by `_corpus.load_scope`/
`iter_records` and `aggregate_new_construction.py`. **LCS contamination** (59 records, $56.9M:
waterjets, planning-yard) sits inside the DDG file and was stripped by `sub_report_id`.

**Takeaway for next agent:** any time you build an input from "the corpus," derive it from
`_corpus.iter_records`, not from the `sam_entity_enrichment` profiles. The enrichment files are
fine *only* as a per-UEI attribute lookup (NAICS-6/PSC), never as the universe or the dollars.

---

## 4. v2 architecture (decided this session)

- **Two tracks, one output vocabulary.** Track A = HII-Ingalls DDG (transaction SWBS via the
  code/text). Track B = everything else (entity registry + SAM NAICS-6 fallback). Both emit the
  *same* SWBS-anchored categories; Track A resolves system-scope directly, Track B resolves it
  only for narrow single-system vendors and otherwise gives component/process + unresolved scope.
- **Multi-dimensional schema, not one overloaded field:** one **mutually-exclusive primary
  scope category** + **non-exclusive process tags** (forging, machining, coating…) + a
  **nullable SWBS field** (only where evidence supports) + an **evidence tier** (SWBS / HII code
  / record text / supplier profile / unresolved) + **`entity_modular_capability`** (registry).
- **SWBS is the anchor, not the cage:** design categories from the data, crosswalk each to SWBS
  groups; don't force a flat SWBS classification (most of the corpus can't resolve to SWBS).
- **Reporting granularity is asymmetric** and combined cross-program cuts must report at the
  coarsest common level (~SWBS group); HII-only views can go finer.
- **Terminology (still to implement):** rename `bucket`→`work_type`; deprecate roll-up
  `SCENARIOS`; keep modular as a standalone entity flag. (From the v2 handoff; unchanged.)

---

## 5. The canonical bundle (what the agent is running on NOW)

`projects/research_shared/taxonomy_design_input_canonical/` — built by `build_bundle.py`
(reproducible; in the folder). Universe driven by `_corpus.iter_records`; SAM NAICS-6/PSC
joined per-UEI; old `role`/`bucket`/`basis` dropped so the prior scheme can't leak.

Files: `naics6_distribution.csv` (176 NAICS-6 on $13.1B), `uei_entity_profile.csv` (1,203 UEIs
with **real `dollars_submarines_$M`/`dollars_ddg_$M` columns** + SAM attrs),
`uei_naics_long.csv`, `uei_psc_long.csv`, `hii_ddg_record_components.csv` (LCS-stripped),
`hii_ddg_code_dictionary.csv` (recomputed), `swbs_hierarchy.csv` (1,962 ESWBS codes),
`DATA_DICTIONARY.md`.

**Verified universe:** $13,111M (subs $9,563M / ddg $3,547M); 1,203 UEIs; BlueForge $0;
**87.5% of $ carries a primary NAICS-6**, $1.6B (12.5%) has none → unresolved floor.

**Top NAICS-6 (canonical $M):** 335312 motor/gen **2,160** (one entity — Northrop Grumman,
all-submarine), `(no_primary_naics6)` **1,639** (429v), 336611 shipbuilding **1,203** (43v,
role-mixed), 335311 transformer 580, 332911 valve 545, 333914 pump 521, 332111 forging 467,
333415 A/C 395, 332312 struct-metal 357, 336412 marine-GT 350, 332410 boiler/HX 340,
332313 plate 335, 335313 switchgear 227, 332710 machine-shop 220, 325212 synth-rubber 218.

**The finalized taxonomy-design prompt** (verbose context+goal, lean mechanics; SWBS as
reference; no category cap; no prior schemes; **deliverable #4 = prioritized ambiguous-entity
research queue**) is what the user is running. It is reproduced in the chat transcript; if the
run needs re-issuing, regenerate it next to the bundle as `PROMPT.md` (was offered, not yet
saved). The earlier wrong-universe bundle is still at `…/taxonomy_design_input/` — **superseded;
do not use.**

---

## 6. First taxonomy attempt — evaluated, architecture kept, numbers rejected

An external agent produced a full v2 (≈23 categories: S1–S11 system, P1–P7 process, U1–U3
support, O1, X1; precedence Rules 0–6; process tags; NAICS-6 + HII code dictionaries). Verdict:

- **Adopt the architecture** — primary scope + process tags + nullable SWBS + evidence tier; the
  precedence ladder; explicit unresolved reason codes. Strong, and it caught LCS contamination
  on its own.
- **Reject the numbers** — it ran on the wrong (pre-fix) universe: **BlueForge sat inside it as
  a 24% category (U1, $4.25B)**; program coverage was undoable (all-`ddg`); and it folded the
  **$2.2B motor/generator (335312) into Propulsion** on a coin-flip (now known to be one entity,
  NG, all-submarine → a single adjudication, not diffuse). The re-run on the canonical bundle
  exists precisely to fix these.

**Watch-list for the NEW run's output:** does it net out the $1.6B no-NAICS-6 floor honestly;
how it places 336611 ($1.2B role-mixed) and 335312 ($2.16B NG); whether "clean coverage"
distinguishes strong (SWBS/HII) from weak (entity-profile proxy, ≈ all of the $9.6B submarine
side); and the quality of deliverable #4 (the research queue).

---

## 7. Sequencing decision: taxonomy draft FIRST, then targeted registry

Not a true chicken-egg. Registry enrichment needs the taxonomy as a target for **100%** of its
output; the taxonomy needs the registry for only a **few** contested high-$ clusters. ~$8B of
the $13.1B is NAICS-clean (taxonomy places it now); ~$5B is contested and needs research for
**assignment** (not for deciding the category set). Order:

1. **Draft taxonomy** (the run in flight) → its key byproduct is the **prioritized
   contested-entity list** (deliverable #4).
2. **Targeted web research** on just those entities (motor/gen=NG, the 336611 cluster, the
   $1.6B no-NAICS-6, diversified multi-system vendors), into SWBS groups + capability tags.
3. **Lock the taxonomy** on that ground truth.
4. **Full registry enrichment** into the locked vocabulary for the rest, with
   `entity_modular_capability` re-inserted. Don't do full registry first (no target vocabulary;
   wastes research on NAICS-clean vendors).

---

## 8. Roadmap / next steps (ordered)

1. **Receive + critically evaluate** the taxonomy agent's output (§6 watch-list).
2. **Run the targeted research** on its contested-entity queue (§7 step 2). The web-research
   deep-agent prompt should ask for `role`, `primary_work_type` (locked vocab) / `likely_swbs_groups[]`,
   component/process capability tags, **`entity_modular_capability`**, evidence URLs, confidence.
3. **Lock taxonomy v2**; write it into the canonical methodology doc (supersede the 7-bucket v1).
4. **Implement:** rename `bucket`→`work_type`; build the two-track classifier (HII code→SWBS→
   category record-first; entity registry+NAICS-6 fallback); the multi-dim schema fields.
   Key code: `…/sheets/_taxonomy.py` (+ submarines `taxonomy.py`), `_registry.py`,
   `data_entity_master.py`, and `_corpus.py`/`extract_workbook_cuts.py`.
5. **Re-extract & rebuild** the three deliverables (deck_primary, workbook_award_analysis,
   workbook_outsourcing_ceiling) — commands in the 2026-06-17 v2 handoff §2. Run a v1/v2 parallel
   diff on top-dollar movers. (User has said deck/workbook *compatibility* is not a constraint —
   don't contort the taxonomy to preserve the old buckets; keep v1 only as a comparison column.)
6. **Still-open from the v2 handoff (parallel, not blocked):** finish the SAM entity pull
   (413 tail UEIs, quota-gated) then re-profile; run the two staged accuracy audits
   (`registry_audit_top40.csv`, `midtail_audit_top50.csv`).

---

## 9. Open decisions for the user / next agent

- **335312 motor/generator $2.16B → Propulsion vs Electrical.** It's one entity (Northrop
  Grumman, all-submarine), so it's a single high-leverage adjudication — resolve via research.
- **336611-as-subawardee $1.2B / 43 vendors** — role adjudication (primes/integrators/foreign
  vs real suppliers), not a work-type call; registry territory.
- **The $1.6B no-primary-NAICS-6 floor** — how aggressively to research vs leave unresolved.
- **Component-tag layer** — build now or defer (coverage is patchy; v2 handoff leaned defer).

---

## 10. Lessons (carry forward)

- **Check data provenance before using a file.** The single biggest issue this session was
  feeding the agent a parallel, un-scope-filtered product ($17.8B incl. BlueForge, all-`ddg`)
  instead of the canonical `_corpus.iter_records` universe ($13.1B, program-split). A
  reconciliation step caught it. Build corpus inputs from `_corpus`, not the enrichment profiles.
- **Verify the marquee examples.** "Forged propulsion shaft," "HII code = SWBS," "modular
  overlay," "BlueForge already stripped" — each was checked against the data; several were more
  nuanced than the slogan (shaft is text-resolved not SWBS; modular signal is absent; the strip
  is submarine-scoped and skipped by the enrichment scripts).
- **Pass-throughs distort every share** — net out BlueForge et al. *before* reading any
  distribution; the canonical stream already does this.
- **Design the category set vs assign contested vendors are different jobs** — only the second
  needs the registry, which is why the taxonomy draft can and should go first.

## 11. Key paths

- Canonical bundle + builder: `projects/research_shared/taxonomy_design_input_canonical/`
- Superseded (wrong-universe) bundle: `projects/research_shared/taxonomy_design_input/` (don't use)
- SAM enrichment source (attribute lookup only): `projects/research_shared/sam_entity_enrichment/`
- Canonical record stream: `projects/distributed_shipbuilding/research/scripts/_corpus.py` (`iter_records`)
- Workbook cuts: `…/research/scripts/extract_workbook_cuts.py` → `workbook_award_analysis/extracted/wb_*.csv`
- Pass-through list: `…/{submarines,ddg}/workbook/extracted/nc_scope_summary.json` (`excluded_mib_ueis`)
- SWBS codebook (source): `projects/mro/research/award_based/docs/ESWBS_potential_codes.xls`
- v1 methodology doc: `/Users/brendantoole/projects3/worktype_classification_methodology.md`
- Prior handoffs: `logs/2026-06-17_worktype_classification_methodology_v2_refactor_handoff.md`,
  `logs/2026-06-17_ddg_subaward_field_audit_swbs_mining.md`
- Design dialogue: `/Users/brendantoole/projects3/t1.rtf`
