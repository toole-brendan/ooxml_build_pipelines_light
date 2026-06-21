# 2026-06-18 — Subaward work-type taxonomy + vendor registry: session log & agent handoff

Continues `logs/2026-06-17_ddg_subaward_field_audit_swbs_mining.md`. This doc is
both a session log and a **handoff for the next AI agent** — it is written to be
read cold. Goal of this workstream: turn the Navy new-construction **subaward
supplier base** into (a) a defensible **work-type taxonomy** and (b) an
authoritative **vendor registry**, then reconcile them. Two external agents are
running in parallel right now; the highest-value next task is **scoring the
taxonomy against the HII-DDG ground truth** (spec in §6).

---

## 1. The canonical data bundle (source of truth)

`projects/research_shared/taxonomy_design_input_canonical/` — built by
`build_bundle.py` from `_corpus.iter_records` (the same scope-filtered, deduped
stream the award-analysis workbook consumes). **Use this, not the raw pulls.**

- **$13,111M total — submarines $9,563M, DDG-51 $3,547M; 1,203 supplier entities;
  20,702 deduped subaward records.**
- This is the **post-filtered** universe for **both programs (DDG and
  submarines)**: Navy-directed **GFE primes** and **SIB / industrial-base
  pass-throughs** (BlueForge ~$4.2B, Training Modernization Group, IALR) are
  **excluded**, LCS line-item contamination stripped, out-of-scope PIIDs removed.
  This is why the universe is $13.1B, not the ~$17.8B raw pull. **Always work from
  this post-filtered stream — never the raw per-PIID JSON pulls, which still
  contain GFE/SIB and out-of-scope records.**
- **87.5% of dollars carry a primary NAICS-6; ~12.5% (~$1.6B) do not** (no SAM
  record / foreign / unregistered).
- Files: `naics6_distribution.csv`, `uei_entity_profile.csv` (per-UEI, dollars
  split by program, full self-certified NAICS list, PSC, owner, CAGE, org
  structure), `uei_naics_long.csv`, `uei_psc_long.csv`, plus the HII/SWBS files
  (§5) and `build_bundle.py` (provenance). `DATA_DICTIONARY.md` documents it — but
  note it contains our analytical conclusions, so it is **withheld** from the
  external agents.

Key data fact that drives everything: **a subaward transaction has no NAICS/PSC
of its own** — NAICS is a *self-reported entity attribute* joined by UEI, and the
primary NAICS is often missing or misleading for big/diversified vendors (e.g.
Rolls-Royce Marine has no primary NAICS; GE is coded 336412 aerospace; several
336611 "Ship Building" entities are component suppliers, not shipbuilders).

---

## 2. Two-axis insight (the core methodological finding)

The supplier signal splits into two orthogonal axes:

- **Process / capability axis** — what the company *makes/does* (forging,
  machining, electrical equipment, …). This is what **NAICS** encodes, it's
  available **corpus-wide**, and it's **comparable across programs**. → the
  taxonomy's primary axis.
- **Ship-system axis** — *where on the ship* the part goes (SWBS). Available
  **only** for the HII-Ingalls DDG slice (~13% of corpus $), one builder/one
  program. → an enrichment / validation signal, **never** the corpus-wide primary.

Consequence: the work-type taxonomy is built from **NAICS (process)**; SWBS/HII is
used to **grade** it, not to define it. Forcing a system-leaning taxonomy on the
whole corpus would make program comparisons an artifact of which yard files
better descriptions. (Castings & forgings is a *process* with no SWBS home — a
forged shaft is SWBS-coded by where it goes, not that it was forged; NAICS is the
only signal for it.)

---

## 3. Where things stand — two external agents running in parallel

### A. Taxonomy-design agent → `taxonomy_design_package/` (projects3 root + .zip)
Independent design of the **work-type taxonomy** from NAICS-6.
- Files: `all_subawards.csv` (20,702 record-level rows; no NAICS, no description —
  join to suppliers by `entity_uei`), `naics6_distribution.csv`,
  `uei_entity_profile.csv`, `uei_naics_long.csv`, `uei_psc_long.csv`,
  `DATA_NOTES.md`, `PROMPT.md`.
- Prompt: classify suppliers into **one mutually-exclusive, exhaustive work type
  each**, **process/capability-framed**. Single task — no secondary axis.
- **Deliberately withheld to keep it independent + non-leading:** our existing
  7-bucket taxonomy, the HII work-item codes, `swbs_hierarchy.csv`, the
  subaward descriptions (DDG ones carry the HII/SWBS codes), and the prior
  14-category proposal. Verified clean (no taxonomy/SWBS/HII strings in the data).

### B. Vendor-registry research agent → `vendor_registry_research_package/` (projects3 root + .zip)
Research the **durable factual attributes** of the top-dollar vendors (what they
make, manufacturer vs distributor, real parent, typical deliverable, NAICS
correct-or-misleading, sources/confidence). Explicitly **not** assigning final
categories (taxonomy isn't done) — so the work is forward-compatible.
- Files: `uei_entity_profile.csv` (ranked by $), `uei_naics_long.csv`,
  `uei_psc_long.csv`, `REGISTRY_DATA_NOTES.md`, `PROMPT.md`.
- Scope by dollars: top 50 = 71% of $, top 100 = 83%, top 200 = 93%, top 300 = 96%
  (1,203 total). Recommended depth: top 200–300.

---

## 4. Methodological guardrails established (carry these forward)

- **Don't lead the design agent.** Give it data facts, not our conclusions. It was
  told "process framing" (legitimate — NAICS *is* a process classification) but
  not our buckets/SWBS.
- **NAICS is entity-level & self-reported** → every subaward of a vendor inherits
  one NAICS; tags built from it are entity-uniform (fine for work type; can't vary
  per subaward). Watch the artifact codes: **541614** (logistics — was BlueForge,
  now removed), **336611** (shipbuilding on component suppliers), **336412**
  (aerospace on marine-turbine makers), **3344/3364** (deliberately excluded
  upstream as corporate-NAICS artifacts).
- **Modular/component (“deliverable”) is an overlay, not the primary axis**, and it
  needs the **registry** (hand judgment) — NAICS can't tell a module from a
  component. Parked as a follow-on pass for the taxonomy agent.
- **Always use the post-filtered data** (the canonical bundle / `_corpus.iter_records`)
  whenever it's relevant — for **both DDG and submarines**. It already removes
  Navy-directed **GFE primes**, **SIB / industrial-base pass-throughs** (BlueForge,
  TMG, IALR), LCS contamination, and out-of-scope PIIDs. The raw per-PIID pulls
  still contain all of that, so don't analyze them directly. Every dollar/coverage
  figure in this workstream is on the post-filtered $13.1B base.
- **Never edit originals** — packages contain copies; canonical bundle untouched.

---

## 5. The HII-DDG ground-truth (the referee signal)

HII-Ingalls DDG subawards carry, in `subawardDescription`, an internal **work-item
code `NNNNN-NN`** that **nests 1:1 inside a single SWBS 3-digit subsystem** (100%
purity on the codes that carry an explicit `CSE PS ###` SWBS cross-reference).
This is the *only* record-level "what the work actually was" signal in the corpus.

Files (in the canonical bundle):
- `hii_ddg_record_components.csv` — per HII-DDG subaward: `code`, `swbs_group`
  (explicit or propagated from the recurring code), `component_text`, `amount_usd`,
  `vendor_uei`, …
- `hii_ddg_code_dictionary.csv` — `code → modal_swbs_group → top_components` ($-ranked).
- `swbs_hierarchy.csv` — authoritative Navy SWBS/ESWBS codebook (`eswbs_code`,
  `one_digit_group`, `group_name`, `nomenclature`). Also at projects3 root as
  `swbs_hierarchy.csv` / `.xlsx`.

Coverage (HII-DDG ≈ $3.5B, ~one quarter of the corpus): work-item code present on
~73% of HII rows / ~90% of HII $; SWBS resolvable for ~70% of HII $; component
text on ~34%. **~65% of HII $ resolves to a specific component, ~30% to a
component class (SWBS only), ~5% opaque.** SWBS→work-type mapping: 1xx structural,
2xx machining/propulsion, 3xx electrical, **51x HVAC / 53x–59x piping**, 6xx
coatings/outfit, 4xx/7xx out-of-scope (combat/GFE).

---

## 6. ★ NEXT-AGENT TASK #1 — score the candidate taxonomy against HII-DDG

When the taxonomy agent returns its NAICS-6 → work-type mapping, **run the HII-DDG
comparison to grade it.** HII is the *neutral referee*: it's the one place we
observe the real work, so it tells us which NAICS/categories are clean vs mushy.

**Inputs:** the candidate taxonomy (categories + NAICS-6→category map);
`hii_ddg_record_components.csv` (observed SWBS/component per record);
`swbs_hierarchy.csv`; `uei_entity_profile.csv` / `uei_naics_long.csv` (vendor NAICS).

**Method:**
1. For each HII-DDG record with an observed `swbs_group` (and/or `component_text`),
   look up the vendor's primary NAICS-6 → its **candidate category** via the taxonomy.
2. Map the observed `swbs_group` to its process-category equivalent via
   `swbs_hierarchy` + the SWBS→work-type rule in §5 (so the system signal is made
   comparable to the process category).
3. **Per candidate category, measure agreement / purity:** of the HII-DDG dollars
   the taxonomy assigns to category C, what share land on the SWBS/component you'd
   expect for C? Equivalently, per NAICS-6: is the observed HII work *consistent*
   (high purity) or scattered (mushy)?
4. **Output:** per-category and per-NAICS-6 purity/confidence scores; rank multiple
   candidate taxonomies head-to-head (highest aggregate purity **and** an honest
   unresolved home wins); and a **low-purity flag list** → the manual-research
   queue that feeds the vendor registry (§3B).

**Critical caveats (don't misuse the referee):**
- HII is **~13% of corpus $, one builder, one program, and a *system* axis** — use
  it to **calibrate/validate**, never to *redefine* categories.
- The taxonomy is **process**, HII is **system** — they only align for the
  system-ish categories. **Process-only categories (castings/forgings, coatings,
  machining) will NOT map to SWBS — that's expected; assess those via
  `component_text` and NAICS-internal purity, don't penalize them for SWBS
  mismatch.**
- Earlier framing called this "HII-calibrated NAICS priors": estimate
  `P(work-type | NAICS-6)` from HII-labeled records, with a dominance/confidence
  threshold (clean NAICS like 332911 valves ~98%; mushy ones like 336611, 332312
  flagged). That table is the bridge from the HII slice to the SWBS-missing 87%.

---

## 7. Other next-agent tasks (after / alongside #1)

- **Taxonomy pass 2 — deliverable overlay.** Once the work types are set, introduce
  the modular/component overlay (`integrated assembly · component/equipment ·
  material/process input · service · unknown`) as an *additive* second dimension,
  sourced from the **registry** (hand judgment), not NAICS. Kept out of pass 1 on
  purpose.
- **Fold the registry research in** as the authoritative override for high-dollar
  vendors (registry-first, then HII-calibrated NAICS for the long tail, then
  unresolved). The registry research (§3B) is the input.
- **Apply + reconcile:** assign every supplier one work type (registry override →
  HII-calibrated NAICS → unresolved), total dollars by category per program, and
  publish coverage segmented by `assignment_basis`/confidence — **never compare
  "system mix" across programs** (it's an HII-evidence artifact).

---

## 8. File inventory / key paths

- Canonical bundle: `projects/research_shared/taxonomy_design_input_canonical/`
- Taxonomy agent package: `/Users/brendantoole/projects3/taxonomy_design_package/` (+ `.zip`)
- Registry agent package: `/Users/brendantoole/projects3/vendor_registry_research_package/` (+ `.zip`)
- SWBS codebook: canonical `swbs_hierarchy.csv`; also `/Users/brendantoole/projects3/swbs_hierarchy.{csv,xlsx}`
- HII extraction script (provenance): `projects/distributed_shipbuilding/ddg/research/scripts/extract_ingalls_components.py`
- Canonical build script: `…/taxonomy_design_input_canonical/build_bundle.py`
- Corpus stream: `projects/distributed_shipbuilding/research/scripts/_corpus.py` (`iter_records(program)`)
- Prior session log: `logs/2026-06-17_ddg_subaward_field_audit_swbs_mining.md`
