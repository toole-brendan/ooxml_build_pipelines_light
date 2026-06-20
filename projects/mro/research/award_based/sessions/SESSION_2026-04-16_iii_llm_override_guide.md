# Session 2026-04-16 (III): LLM Override Guide + Residual Reduction to ~3%

## Context

Building on `SESSION_2026-04-16.md` and `SESSION_2026-04-16_ii.md`. Entered this session at v2.41 workbook with Services residual at $3.75B / ~50% of services $. Goal: push residual toward 10%.

Ended at **v2.44 workbook with residual at $213M / ~3.1% of net services**. The final push from ~18% → ~3% came from an LLM classification pass that user can trivially revert by deleting two JSON files.

---

## For future AI agents picking up this work

Read these files first to get oriented:

### Essential context (read in order)

1. **`SESSION_2026-04-16.md`** — Tier 0 regex / proper-name cascade foundation (per-mod sweep, IDV enrichment, supergroup classification, LCS EMERGENT/CONTINUOUS patterns, `vcs\b` bugfix).
2. **`SESSION_2026-04-16_ii.md`** — Wikipedia-sourced proper-name lookup (Tier 0 via `proper_names_lookup.py`), J028/J069 aviation PSC exclusions, Vessel Type supergroup column on PP, `in_tam=True` for Combatant Crafts / Support Crafts / Boats.
3. **`SESSION_2026-04-16_iii_llm_override_guide.md`** — THIS FILE. Residual reduction $3.76B → $213M via extractor cleanup, shore/base filter, hull-number tier (0b), DAP tier (0c), FPDS MOD 0 override (Tier -1), recipient priors (Tier 5), LLM sweep, and cross-platform engineering exclusions.
4. **`EXCLUSION_CROSS_PLATFORM_ENG_IDIQS.md`** — Rationale for excluding SEAPORT-NXG / Cyber Mission Engineering / Combat Environment Instrumentation / ATC Platform from Services TAM ($400M+ decision).
5. **`DATA_SHEETS.md`** — Awards Data vs Awards By Hull sheet split (created in session II).
6. **`OBJECTIVE.md`** — Project objective: size USN/USCG newbuild + MRO market from USAspending awards.
7. **`CLAUDE.md`** (root) — Coding conventions and commands for this project.

### Files CREATED in THIS session (2026-04-16 III)

| File | Purpose | How to run |
|---|---|---|
| `data_pull/enrich_residual_piids.py` | Pulls FPDS Atom Feed MOD 0 base-award SOW for top-N residual PIIDs, runs full classification cascade against the base text, writes `residual_piid_overrides.json` as Tier -1. Resumable (merges existing overrides on re-run). Per-PIID cache in `residual_piid_cache/`. | `python3 -m domnann.data_pull.enrich_residual_piids --top 500` |
| `data_pull/llm_classify_residual.py` | Async Claude Sonnet 4.6 classifier with prompt caching + structured outputs (Pydantic). Classifies residual PIIDs into 15 supergroups + NOT_SHIP_MRO + UNKNOWN. Writes `llm_overrides.json`, `llm_exclusions.json`, `llm_review.json`. Resumable — skips PIIDs already in review. | `python3 -m domnann.data_pull.llm_classify_residual --top 500 --concurrency 8` |
| `EXCLUSION_CROSS_PLATFORM_ENG_IDIQS.md` | Written rationale doc for the cross-platform engineering IDIQ exclusion decision. Shows data, why these IDVs aren't ship MRO, what remains excluded vs kept. | (read-only) |
| `SESSION_2026-04-16_iii_llm_override_guide.md` | This file. Full session writeup. | (read-only) |

### Files MODIFIED in THIS session

Key deltas to understand the classification cascade:

- **`data_pull/classify_awards.py`** — Extractor cleanups in `extract_uss_names`; added `VESSEL_CLASS_TO_HULL` entries; `SUPERGROUP_DESC_PATTERNS` greatly expanded (bare abbrevs, availability acronyms, CG cutter type codes, MSC type codes, IDV-scope phrases, submarine/surface program markers); added `RECIPIENT_SUPERGROUP_PRIORS` (Tier 5); added `_load_residual_overrides()` merging LLM + FPDS layers; added Tier -1 override logic in `classify_vessel()`; added Tier 0b hull-number lookup in `classify_vessel()`.
- **`data_pull/vessel_explode_v2.py`** — `classify_mod` signature now takes `(mod, idv_rec, award_desc='', award_dap='', recipient='', piid='')`; added Tier -1 override, Tier 0 name via award, Tier 0b hull# via mod/idv/award, Tier 0c DAP via award, Tier 5 recipient prior; `_load_residual_overrides()` merges LLM + FPDS layers; `_load_base_descs()` loads from `residual_piid_cache/` and merges into exploded rows' `base_award_description` field.
- **`data_pull/proper_names_lookup.py`** — Added `_HULL_KEY_RE`, `_build_hull_number_index`, `HULL_NUMBER_INDEX`, `HULL_NUMBER_PATTERN`, `match_hull_number()`. Added Tier 1a in `match_ship_name()` (longest-prefix match on raw body before noise-tail strip) to fix `USS PEARL HARBOR` gap.
- **`data_pull/extract_unclassified_services.py`** — `_process_service` now takes `base_descs` arg; shore_probe includes `piid`, `award_description`, `base_award_description`; `classify_mod` call passes all of award_desc/award_dap/recipient/piid.
- **`sheets/services.py`** — Added `SHORE_BASE_IDV_PATTERNS`, `SHORE_BASE_OFFICE_PATTERNS`, `NON_SHIP_MRO_PIID_PREFIXES`, `FMS_AWARD_PATTERNS`, `is_shore_base_excluded()`, `_load_llm_exclusions()`. Patterns cover ATFP/shore base/cross-platform engineering/Marine Corps/Army/FMS/inactive-vessels/LLM-flagged.
- **`.env`** — Added `ANTHROPIC_API_KEY` (gitignored).

### Data files PRODUCED in THIS session (don't commit; cacheable)

| Path | Role | Loaded by |
|---|---|---|
| `data_pull/output/fpds/residual_piid_cache/{piid}.json` | Per-PIID FPDS MOD 0 base-award record cache. ~1,100 entries. | `enrich_residual_piids.py`, `vessel_explode_v2._load_base_descs`, `extract_unclassified_services._load_base_descs` |
| `data_pull/output/fpds/residual_piid_overrides.json` | 80 FPDS-MOD0-driven PIID classifications. **Tier -1 override, HIGHER priority than LLM.** | `classify_awards._load_residual_overrides`, `vessel_explode_v2._load_residual_overrides` |
| `data_pull/output/fpds/residual_piid_classifications.json` | Verbose per-PIID enrich output with all text sources checked. Audit-only. | Not loaded by pipeline |
| `data_pull/output/fpds/llm_overrides.json` | **340 LLM-driven PIID classifications. Tier -1 override, lower priority than FPDS layer.** | `classify_awards._load_residual_overrides`, `vessel_explode_v2._load_residual_overrides` |
| `data_pull/output/fpds/llm_exclusions.json` | **130 LLM-flagged NOT_SHIP_MRO PIIDs. Stripped from TAM.** | `sheets/services._load_llm_exclusions` |
| `data_pull/output/fpds/llm_review.json` | Full 500-entry audit trail with LLM reasoning. Manual-review only. | Not loaded by pipeline (used by llm_classify_residual.py for resume / dedup) |
| `data_pull/output/fpds/services_unclassified_piids.json` | Current residual state with top 25 unclassified mod descriptions per PIID. | `enrich_residual_piids.py`, `llm_classify_residual.py` |
| `data_pull/output/fpds/services_unclassified_proper_names.json` | Residual names audit (matched/unmatched via `match_ship_name`). Audit-only. | Not loaded by pipeline |

### Workbook artifacts

| File | State |
|---|---|
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.42.xlsx` | Archived. Pre-LLM + pre-FPDS-MOD0 state at ~29% residual. |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.43.xlsx` | Archived. Pre-LLM, post-FPDS-MOD0 + pre-LLM-exclusions, at ~25% residual. |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.44.xlsx` | **Current. Post-LLM. Residual ~3.1% of net services.** |

---

## TL;DR — How the LLM override layer works (read this first)

Two files in `data_pull/output/fpds/` control the LLM layer. **Delete either to revert that layer of changes; all other classification is unaffected.**

| File | What it does | Count | $ impact |
|---|---|---|---|
| `llm_overrides.json` | PIID → `{supergroup, vessel_class, hull_number, ...}`. Loaded by `classify_mod` (Tier -1 in vessel_explode_v2) and `classify_vessel` (Tier -1 in classify_awards). Overrides every other tier for the listed PIIDs. | 340 PIIDs | ~$823M moved from residual to classified |
| `llm_exclusions.json` | PIID → `{reason, confidence, dollars}`. Loaded by `sheets/services.is_shore_base_excluded()`. Listed PIIDs are stripped from Services TAM entirely (same treatment as ATFP/FMS/Army/Marine Corps). | 130 PIIDs | ~$247M removed from TAM |

Plus one audit file:

- `llm_review.json` — full 500-PIID audit trail with the model's reasoning string per PIID. Not loaded by the pipeline; for spot-checking.

### Undo

```bash
# Revert all LLM classifications and exclusions:
rm data_pull/output/fpds/llm_overrides.json
rm data_pull/output/fpds/llm_exclusions.json

# Rebuild:
cd /Users/brendantoole/projects2 && python3 -m domnann.data_pull.vessel_explode_v2
# then ask user to re-run build_from_data
```

The FPDS-MOD0 Tier -1 overrides in `residual_piid_overrides.json` are separate and unaffected — those came from pulling real FPDS base-award text and running the regex cascade, not from an LLM.

### Re-run / add more PIIDs

```bash
cd /Users/brendantoole/projects2
python3 -m domnann.data_pull.llm_classify_residual --top 1000 --concurrency 8
# Resumes from wherever it left off - skips PIIDs already in llm_review.json
# Costs ~$0.003/PIID, ~$3 for 1000 total. Sonnet 4.6.
```

### Rejecting individual classifications

If you disagree with a specific PIID's LLM classification after reviewing `llm_review.json`:

```python
# Open llm_overrides.json, remove that PIID's entry, save.
# Open llm_exclusions.json, remove if applicable, save.
# Rebuild pipeline. That PIID goes back to regex/prior/residual.
```

No blocklist mechanism yet — it's direct file editing. If you reject a lot, write a quick blocklist and I can wire it in.

---

## Work completed, in order

### 1. Regenerated stale residual JSON (opening task)

The existing `services_unclassified_piids.json` was from before SESSION 2's Tier 0 Wikipedia name lookup landed. Re-ran `extract_unclassified_services.py`; residual JSON shrank from $7.43B → $3.76B because now-classified PIIDs were dropping out.

### 2. Extractor cleanups in `classify_awards.extract_uss_names`

Added to `NAME_STOP_TOKENS`: `UNIT`, `SETTLE`, `MATERIAL`, `VARIOUS`, `UCO`, `TRANSFER`, `TPPC`, `DMP`, `DMA`, `INSTALLS`, `MODIFICATION`.

Other fixes:
- Strip trailing `-` from each token (`USS BATAAN-` → `USS BATAAN`)
- Pre-dash check: `TPPC-LHD` stops on the `TPPC` segment
- Strip trailing possessive `'S` (`HALSEY'S` → `HALSEY`)
- Run extracted names back through `match_ship_name` in the names report so user can see which extracted names already classify vs genuine gaps

Cumulative impact on the audit: unique names 497 → 470; $ touching a name $913M → $664M; top-20 list now shows match hull number per entry.

### 3. Shore/base filter `is_shore_base_excluded` in `sheets/services.py`

New helper that filters non-ship-MRO awards out of Services TAM. Wired into `awards_by_hull.load_exploded_rows()` and `extract_unclassified_services._process_service`.

Categories (grew over the session):
- **Shore infrastructure IDV patterns**: ATFP / Anti-Terrorism / Force Protection; Public Safety Systems; Facility Investment Services.
- **Shore/base office patterns**: `NAVFACSYSCOM*`, `NAVFAC SYSTEMS AND EXP WARFARE CTR`.
- **Cross-platform engineering MACs**: SEAPORT-NXG, Cyber Mission Engineering, Combat Environment Instrumentation, ATC Platform Integration, NIEF Engineering Services, Depot Systems Support.
- **Ground weapons**: JCREW, INACTIVE VESSELS (decommissioned fleet).
- **Non-ship contracting activities (PIID prefix)**: `M67854` (Marine Corps Systems Command), `W912CH` (Army Contracting — watercraft), `W9127N` (USACE Portland — dredges).
- **Foreign Military Sales**: `FMS CASE`, `FOREIGN MILITARY SALES`, `(EGYPTIAN|IRAQI|SAUDI|KUWAITI|JORDANIAN|JAPANESE|KOREAN|AUSTRALIAN|TAIWANESE|PHILIPPINE) NAVY`.
- **LLM-flagged non-ship-MRO** (loaded from `llm_exclusions.json` at runtime).

Critical bugfix mid-session: `is_shore_base_excluded` originally only checked `parent_idv_description` against IDV patterns. Many markers (INACTIVE VESSELS, SEAPORT-NXG, JCREW) appear in the AWARD description not the IDV. Fixed by combining `idv + award_desc + base_desc` into one string for the IDV-pattern scan.

See `EXCLUSION_CROSS_PLATFORM_ENG_IDIQS.md` (root of repo) for the detailed rationale on the cross-platform engineering exclusion decision.

### 4. Hull-number tier (Tier 0b) — `match_hull_number()` in `proper_names_lookup.py`

Residual mod text constantly says "DDG 75 SRA" without "USS DONALD COOK". The existing proper-name lookup completely missed these. Built a new hull-number lookup tier between Tier 0 (name) and Tier 1 (VESSEL_DESC_PATTERNS class regex):

- `_HULL_KEY_RE = r'^([A-Z][A-Z-]*?)-(\d{1,4})$'` — parses hull keys like `DDG-75`, `T-AO-205`, `WMSL-750` correctly (multi-hyphen prefixes like `T-AO` survive).
- `HULL_NUMBER_INDEX` built from USS/USNS/CGC canonical dicts: 462 entries. Keys like `DDG-75` → class string `DDG-75 Arleigh Burke`.
- `HULL_NUMBER_PATTERN` regex: `\b(T-AGOS|T-AGM|…|DDG|CVN|…|CG|AS)[\s-]?(\d{1,4})\b` with prefixes ordered longest-first so `T-AO` wins over `AO`.
- `match_hull_number(text)` returns `(wiki_class_str, hull_number, hull_label)` or `(None, None, None)`.

Wired as Tier 0b in both:
- `vessel_explode_v2.classify_mod` — runs on mod desc → idv desc → award desc.
- `classify_awards.classify_vessel` — runs on award desc.

Big discovery during this work: `classify_mod` originally only looked at mod + IDV, never at the AWARD description. Fixed that; also enabled bare hull numbers in award-level text. See §12 for impact.

### 5. DAP field tier (Tier 0c) — `classify_mod`

Many residual PIIDs have a populated `dod_acquisition_program_description` on the award (e.g. `TRIDENT II MISSILE`, `LCS`, `DDG 51`, `LPD 17`, `SSN 774`). Added a tier that consults `DAP_TO_VESSEL` at the award level for every mod. Contributes $79M classified. Limited further gain because parent IDV DAPs are mostly empty.

### 6. PEARL HARBOR lookup gap fix

`USS PEARL HARBOR` (LSD-52) was in the Wikipedia lookup but `match_ship_name` returned no match. Root cause: `HARBOR` is in `_NOISE_TAIL_TOKENS`, so normalization stripped it to `PEARL`, which isn't in the lookup.

Fix: try longest-prefix match on the raw body BEFORE noise-tail stripping. If that hits, return. Otherwise, strip and retry. Only one ship was affected (audited all 222 multi-word entries).

### 7. Loosened `SUPERGROUP_DESC_PATTERNS`

The original supergroup regex required specific phrases like `cvn class`, `cvn fleet`, `cvn program` — bare `CVN` alone didn't match. Expanded to accept:

- **Bare abbreviations**: `CVN`, `DDG`, `FFG`, `LCS`, `LPD`, `LHD`, `LHA`, `LSD`, `SSN`, `SSBN`, `SSGN`, `MCM`, CG cruiser hull numbers.
- **Class names**: arleigh burke, zumwalt, ticonderoga, virginia, columbia, ohio, seawolf, los angeles, san antonio, wasp, america, whidbey island, harpers ferry, freedom, independence, constellation, nimitz, ford, gerald r ford, henry j kaiser, john lewis, lewis and clark, mercy, bob hope, watson, juniper, keeper, healy, polar, mackinaw, bay class, spearhead, montford point, lewis b puller, safeguard, powhatan, navajo, pathfinder, victorious, impeccable, zeus.
- **CG cutter type codes**: `WMSL`, `WMEC`, `WPC`, `WLB`, `WLM`, `WAGB`, `WLBB`, `WTGB`.
- **MSC type codes**: `T-AO`, `T-AKE`, `T-AOE`, `T-EPF`, `T-AGOS`, `T-AGM`, `T-AGS`, `T-ATS`, `T-ATF`, `T-ARS`, `T-AH`, `T-AK`, `T-AKR`, `T-ESB`, `T-ESD`, `T-ARC`.
- **Availability / program acronyms**:
  - Carriers: `RCOH` (refueling complex overhaul), `DPIA` (docking planned incremental availability)
  - Surface combatants: `SRA`, `DSRA`, `EDSRA`, `CMAV`; NAVSEA/TYCOM contract codes `C440A/B`, `C430A/B`
  - Submarines: `SWFTS`, `CWITT`, `submarine warfare federated`, `undersea warfare`, `torpedo`, `sonar`
  - Aegis surface combatants: `MK 41 VLS`, `mk 57 vls`, `vertical launch system`, `aegis (weapon|combat|program|baseline|modernization)`
- **IDV-scope phrases**:
  - `EO 14042` → LCS (Surface Combatants)
  - `LCS EMERGENT|CONTINUOUS|CONTRACT|MAINTENANCE` → Surface Combatants
  - `ROTA SURFACE SHIP REPAIR` → Surface Combatants
  - `47 MLB|MOTOR LIFE BOAT` → Boats (USCG)
  - `MESSING AND BERTHING BARGES|YFN|YFNB` → Support Crafts
  - `HUSBANDING|PORT VISIT SERVICES` → Multi-class

### 8. Recipient priors (Tier 5) — `RECIPIENT_SUPERGROUP_PRIORS` in classify_awards.py

A last-resort tier for contractors with distinctive vessel focus. Applied only when all text-based tiers fail. Curated list of 12 vendors:

- **Ship repair yards**: Pacific Shipyards Intl HI → Surface Combatants; Colonna's Shipyard VA → Surface Combatants; Metro Machine Corp VA → Aircraft Carriers; Mare Island Dry Dock CA → Cutters.
- **Undersea specialists**: Oceaneering International → Submarines.
- **Newbuild primes**: Austal USA → Surface Combatants (LCS+EPF); Bath Iron Works → Surface Combatants (DDG-51); General Dynamics Electric Boat → Submarines; Huntington Ingalls (Newport News) → Aircraft Carriers; Fincantieri Marinette Marine → Surface Combatants (FFG-62).
- **CG boat program**: Birdon America → Boats (47 MLB SLEP).

Diverse IT/C4ISR primes (Lockheed, Northrop, BAE TS&S, SAIC, Leidos, CACI, L3) are intentionally omitted — they span multiple ship types.

Contribution: $238M at low confidence.

### 9. FPDS MOD 0 base-award enrichment (`enrich_residual_piids.py`)

FY25-only residual PIIDs often have rich SOW text on their MOD 0 base-award record, which FPDS Atom Feed returns but we hadn't pulled. New script:

- Sorts residual PIIDs by $, takes top N.
- For each, fetches FPDS Atom Feed with `PIID:"<piid>" MODIFICATION_NUMBER:"0"`.
- Extracts the base SOW description, runs through the full classification cascade (name → hull# → DAP → supergroup regex).
- Writes two files:
  - `residual_piid_cache/{piid}.json` — per-PIID cache of the FPDS MOD 0 record (reusable across re-runs).
  - `residual_piid_overrides.json` — clean PIID → classification map.
- Also merges existing overrides on re-run (don't clobber prior batches).

Pulled top 1000 residual PIIDs (first 500 mostly fetched in the first pass, next 500 added later). ~$0.27 worth of FPDS calls — free but rate-limited at 1.2s/request.

Wired `residual_piid_overrides.json` as **Tier -1** in both `classify_mod` and `classify_vessel` — highest-priority override that wins over all other tiers. Result: 80 PIIDs classified via base-SOW text.

### 10. Base-award SOW visible to exclusion filter

The FPDS MOD 0 base-award description is much richer than the FY25 mod-level description. Some non-ship-MRO markers (SEAPORT-NXG, JCREW, INACTIVE VESSELS) ONLY appear in the base SOW, not in the FY25 mods.

Merged `base_award_description` into:
- Exploded rows (as a new `base_award_description` field — not a display column).
- `extract_unclassified_services` shore_probe dict.

Then updated `is_shore_base_excluded` to scan `idv + award_desc + base_desc` for the IDV patterns. This caught another ~$300M of non-ship-MRO that had signals hidden in base SOWs.

### 11. Workbook rebuild v2.42 → v2.43

Residual at ~25% of net services. Still above the user's 10% target.

### 12. LLM classification pass (`llm_classify_residual.py`)

Final push below 10% — Claude Sonnet 4.6 classifier over the remaining residual.

**Design decisions:**

- **Model**: `claude-sonnet-4-6` at user's request (Haiku 4.5 would have been cheaper but user wanted accuracy).
- **Structured outputs**: `client.messages.parse()` with a Pydantic `Classification` model (`supergroup` enum, `vessel_class`, `hull_number`, `confidence`, `reasoning`).
- **Prompt caching**: full taxonomy + 10 worked examples + classification guidance in a cached system prompt (~5K tokens). Cache write premium on request 1, ~10% cache-read cost on requests 2-500.
- **Async concurrency**: 8 concurrent requests via `asyncio.Semaphore`; fire one request alone first to warm the cache, then fan out.
- **Resumable**: script loads existing `llm_overrides.json` + `llm_review.json` and skips already-classified PIIDs on re-run. Batches can be run incrementally with `--top 100`, then `--top 200`, etc.
- **Schema**: 18 output choices — 15 vessel supergroups + `Multi-class` + `NOT_SHIP_MRO` + `UNKNOWN`.

**Per-PIID input to the model** (what I pass in the user message):
- Service (Navy/CG), FY25 total obligation, FY25 unclassified $
- Recipient + Ultimate Parent + POP state + Contracting Office
- PSC code + description (e.g. `K012 (Modification - Fire Control Equipment)`)
- DoD Acquisition Program, NAICS
- Award description (FY25 most-recent, trimmed to 500 chars)
- Base Award SOW from MOD 0 cache (trimmed to 800 chars) — "often the richest ship signal"
- Parent IDV description (trimmed to 400 chars)
- ALL FY25 mod descriptions, dedup'd by text, top 25 by summed $, trimmed to 300 chars each

The dedup was important — an earlier version passed top-5 by individual action $, which often gave the model 4 identical "ENGINEERING AND TECHNICAL SERVICES" rows and one admin mod. Dedup'd top-25 surfaces the signals hiding in smaller mods.

**Outputs:**
- `llm_overrides.json` — in-taxonomy classifications only (340 PIIDs / $823M). Keyed by PIID, values include `vessel_class`, `supergroup`, `tier: "llm"`, `source: "llm_<confidence>"`, `reasoning`.
- `llm_exclusions.json` — NOT_SHIP_MRO classifications (130 PIIDs / $247M). Loaded by `is_shore_base_excluded` as a PIID set.
- `llm_review.json` — all 500 entries with full per-PIID reasoning (deduped across re-runs), sorted by $.

**Results on top 500 residual PIIDs:**

Cumulative by supergroup ($M, n):
- NOT_SHIP_MRO: 130 / $247M
- Multi-class: 76 / $255M
- Surface Combatants: 66 / $167M
- Submarines: 54 / $158M
- Support Crafts: 66 / $110M
- UNKNOWN: 30 / $77M
- Combat Logistics Ships: 10 / $34M
- Combatant Crafts: 24 / $31M
- Mine Warfare: 6 / $25M
- Cutters: 13 / $18M
- Unmanned Maritime Platforms: 8 / $6M
- Other supergroups: ~$25M combined

Confidence: high 186 / $338M, medium 234 / $561M, low 80 / $249M.

Cost: **$0.83 total** for all 500 (first 100 = $0.37 due to cache write; remainder = $0.46).

### 13. Final pipeline chain and workbook v2.44

Ran the full chain one last time:
1. `enrich_residual_piids.py` (cached, instant)
2. `llm_classify_residual.py` (done)
3. `classify_awards navy_fy2025_deduped.json` (applies Tier -1 to Awards Data)
4. `classify_awards cg_fy2025_deduped.json`
5. `vessel_explode_v2.py` (applies Tier -1 + base-desc + all other tiers to AwardsByHull)
6. `extract_unclassified_services.py` (final residual)
7. `build_from_data.py` (v2.43 → v2.44, v2.43 archived)

Final residual: **$213M / ~3.1% of net services $6.79B**.

---

## Residual trajectory across the session

| Checkpoint | Residual | % net svc | Notes |
|---|---|---|---|
| Session start (v2.41) | $3.76B | ~55% | Stale residual JSON from pre-Tier 0 |
| After extractor + shore/base filter | $3.48B | ~45% | NAVFAC + ATFP + Marine Corps excluded |
| After Tier 0b hull-number + award-desc threading | $3.16B | ~41% | `DDG 75`-style refs caught |
| After FMS + Army exclusions | $2.89B | ~37% | |
| After DAP tier (Tier 0c) | $2.83B | ~37% | Smaller lift than expected |
| After loosened supergroup regex + IDV patterns | $2.43B | ~32% | LCS/CVN/DDG/AEGIS/undersea warfare catches |
| After recipient priors (Tier 5) | $2.23B | ~29% | |
| After cross-platform eng IDIQ exclusion | $1.82B | ~25% | v2.43 rebuild |
| After FPDS MOD 0 Tier -1 overrides | $1.28B | ~18% | 80 PIIDs classified from base SOWs |
| **After LLM Sonnet-4.6 sweep** | **$213M** | **~3.1%** | **v2.44 rebuild — 500 PIIDs / $0.83** |

---

## Files touched

### Created

| File | Purpose |
|---|---|
| `data_pull/enrich_residual_piids.py` | FPDS MOD 0 base-award pulls for top-N residual PIIDs + classification cascade; writes `residual_piid_overrides.json`. |
| `data_pull/llm_classify_residual.py` | Sonnet 4.6 classifier over residual PIIDs with prompt caching, async concurrency, resumable batching. |
| `EXCLUSION_CROSS_PLATFORM_ENG_IDIQS.md` | Written rationale for excluding SEAPORT-NXG / Cyber Mission / Combat Environment / ATC Platform from ship MRO TAM. |
| `SESSION_2026-04-16_iii_llm_override_guide.md` | This file. |

### Modified

| File | What changed |
|---|---|
| `data_pull/classify_awards.py` | Extractor cleanups (NAME_STOP_TOKENS, trailing-dash strip, `'S` strip, pre-dash check); `VESSEL_CLASS_TO_HULL` additions; Tier 0b hull-number; expanded SUPERGROUP_DESC_PATTERNS (bare abbrevs, availability acronyms, class names, IDV phrases); `RECIPIENT_SUPERGROUP_PRIORS` (Tier 5); `_load_residual_overrides()` merging LLM + FPDS layers. |
| `data_pull/vessel_explode_v2.py` | Threaded award_desc + award_dap + recipient + piid through `classify_mod`; added Tier -1 (residual overrides), Tier 0b (hull-number via mod/idv/award), Tier 0c (DAP via award), Tier 5 (recipient prior); `_load_base_descs` + merged base SOW into exploded rows' `base_award_description` field; `_load_residual_overrides()` merges LLM + FPDS layers. |
| `data_pull/proper_names_lookup.py` | `_HULL_KEY_RE` regex-based hull parsing; `_build_hull_number_index`; `HULL_NUMBER_PATTERN`; `match_hull_number`; Tier 1a (longest-prefix match on raw body before noise-tail strip — fixes `USS PEARL HARBOR`). |
| `data_pull/extract_unclassified_services.py` | Passes award_desc, award_dap, recipient, piid to `classify_mod`; loads `residual_piid_cache` at top level and merges base-desc into shore_probe dict; threads `base_descs` into `_process_service`. |
| `sheets/services.py` | Added `SHORE_BASE_IDV_PATTERNS` (ATFP, Public Safety, Facility Investment, SEAPORT-NXG, Cyber Mission Engineering, Combat Environment Instrumentation, ATC Platform, JCREW, Inactive Vessels, NIEF Engineering, Depot Systems Support); `SHORE_BASE_OFFICE_PATTERNS` (NAVFACSYSCOM variants); `NON_SHIP_MRO_PIID_PREFIXES` (M67854, W912CH, W9127N); `FMS_AWARD_PATTERNS`; `_load_llm_exclusions()` for runtime-loaded PIID exclusion set; `is_shore_base_excluded()` helper that scans idv + award + base desc and consults all exclusion lists. |
| `.env` | Added `ANTHROPIC_API_KEY` (gitignored). |

### Data files produced

| Path | Contents |
|---|---|
| `data_pull/output/fpds/residual_piid_cache/{piid}.json` | Per-PIID FPDS MOD 0 base-award record cache (1,100 entries). |
| `data_pull/output/fpds/residual_piid_overrides.json` | Clean PIID → classification map from FPDS MOD 0 cascade (80 PIIDs). Tier -1 override. |
| `data_pull/output/fpds/residual_piid_classifications.json` | Verbose per-PIID enrich output with all text sources. |
| `data_pull/output/fpds/llm_overrides.json` | PIID → classification from LLM pass (340 in-taxonomy PIIDs). Tier -1 override, lower priority than FPDS. |
| `data_pull/output/fpds/llm_exclusions.json` | PIID → reason/confidence/dollars for LLM-flagged NOT_SHIP_MRO (130 PIIDs). Loaded by `is_shore_base_excluded`. |
| `data_pull/output/fpds/llm_review.json` | Full 500-entry audit trail with LLM reasoning per PIID. Manual-review only, not loaded by pipeline. |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.43.xlsx` | Pre-LLM rebuild at ~25% residual. Archived. |
| `output/08APR2028_Newbuild_and_MRO_Spend_v2.44.xlsx` | Final rebuild at ~3.1% residual. |

---

## Outcomes

Workbook counts before / after this session:

|  | v2.41 (session start) | v2.44 (end) |
|---|---|---|
| Services Navy hull programs | 30 | 29 |
| Services CG hull programs | 16 | 15 |
| Product Procurement hull programs | 31 Navy / 19 CG | 31 Navy / 19 CG |
| Services total classified % (of services $) | 54.6% | ~82% |
| Services residual $ | $3.75B | $213M |
| Residual as % of net services | ~50% | ~3.1% |
| Non-ship-MRO exclusions (Navy) | 0 | 744 rows / $1.45B |
| Non-ship-MRO exclusions (CG) | 0 | 11 rows / $6M |

Qualitative wins:
- **Aviation, ground weapons, shore infra, FMS, Army watercraft, and cross-platform engineering are all out of Services TAM** — the sum of exclusions is now large enough to see clearly as a separate bucket, not blended into "Unclassified".
- **Residual is honest**: the 3.1% that remains is mostly the long tail of small PIIDs (avg $64K) that the LLM either couldn't classify (30 UNKNOWN) or that were below the top-500 cutoff.
- **Every classification above Tier 0 has an audit trail**: the `Hull Source` column on AwardsByHull rows shows one of `residual_override`, `name_lookup_mod/idv/award`, `hull_number_mod/idv/award`, `dap`, `mod_description`, `idv`, `supergroup_mod`, `supergroup_idv`, `recipient_prior`. Reviewer can trace any TAM row back to the signal that drove it.
- **LLM layer is fully revertible**: two JSON files, delete to undo. FPDS MOD 0 cascade and regex / prior / DAP tiers are unaffected by LLM toggling.

---

## Potential next steps

### Tighten the LLM layer (if concerned about quality)

1. **Hand-review the "low" confidence LLM classifications first** — there are 80 of them covering $249M. Open `llm_review.json`, filter to `confidence: "low"`, read the reasoning, reject any that are overreaching. Per-PIID rejection today is direct file editing; add a `llm_rejects.json` blocklist if needed.
2. **Hand-review the "medium" NOT_SHIP_MRO exclusions** — ~$100M of the $247M excluded is medium-confidence. Same workflow.
3. **Spot-check high-confidence LLM classifications against actual contract text** — sample 20-30 PIIDs, read the base SOW directly, compare to what the LLM said. If it's reliably right, trust the layer; if not, tighten the prompt or require a stricter confidence bar.

### Scale or improve the LLM layer

4. **Run on the remaining ~3,300 residual PIIDs** — the long tail is small per-PIID ($64K avg) but together is $213M. Cost would be ~$5-10.
5. **Upgrade to Opus 4.7** for the ambiguous cases — more expensive but likely more accurate on the "low" confidence PIIDs. Would need `thinking: {type: "adaptive"}` and removal of sampling params.
6. **Feed the subaward narratives to the LLM** — `usa_client.get_subawards()` exists but is unused for classification. Subaward narratives often name the hull being fed.

### Pipeline quality

7. **Add reconciliation check to `build_from_data`** — verify Vessel Type total equals Hull Program total on Services sheet (both query AwardsByHull). Fail the build loudly if not equal.
8. **Export rejected-by-LLM list separately** — emit NOT_SHIP_MRO entries as a separate workbook sheet so reviewers can see what was filtered out and why, instead of just seeing lower TAM.

### Not recommended

- **Running LLM on top 1000+ at once** — diminishing returns similar to the FPDS MOD 0 enrich. Top-500 already covered the concentrated $. Long tail is genuinely ambiguous.
- **Blanket LLM classification without the base-SOW context** — the LLM's quality depends heavily on the base-SOW text in the prompt. Without MOD 0 enrichment first, accuracy would drop.
