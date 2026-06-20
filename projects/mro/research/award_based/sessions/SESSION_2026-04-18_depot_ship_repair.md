# Session 2026-04-18: Depot Ship Repair Deep Dive (J998/J999) - v2.65 -> v2.67

## Context

FY25 analysis showed massive J998 / J999 spend ($5.0B across 2,861 awards, 9,231
mods). User wanted a standalone workbook sheet and eventual deck slide that
drills into that PSC pair to surface what kind of work is actually being done.
Existing research doc at `docs/research/J998_J999_RESEARCH.md` and dedicated
extract at `data_pull/output/fpds/j998_j999_awards.json` (11 MB, per-award mods
+ parent_idvs + all_mod_descriptions).

Ended at **v2.67 workbook** with a new **Depot Ship Repair** sheet, four
classification dimensions on every J998/J999 award (availability, RMC,
contractor tier, IDV scope), and the underlying LLM-generated taxonomy
artifacts committed to `data_pull/output/fpds/`.

---

## Work completed, in order

### 1. Initial proposal + standalone-vs-integrated decision

User asked "how should we do this analysis" and "can we classify mods / PIIDs
to clarify what work is going on". I proposed:

- Tiered cascade classifier (parent IDV name match -> availability regex ->
  contracting office regex -> LLM residual sweep)
- Primary dimensions: Availability Type x Hull Program, RMC, Contractor Tier
- Standalone deep-dive sheet rather than adding sections to Services, since
  the new dimensions don't apply elsewhere

User approved standalone. First-pass shipped in one build.

### 2. Initial classifier + sheet (v2.64 -> v2.65)

**`data_pull/classify_j998_j999.py`** (new). Reads `j998_j999_awards.json`,
tags each award with:
- `availability_type` - DSRA, SRA, CMAV, DPIA, PIA/CIA, EDSRA, DMP, PSA,
  PMAV, CNO Availability, Emergent, Voyage Repair, Drydock (other),
  Inspection/Survey, Husbanding, Other
- `availability_group` - Drydocked / Pierside / CMAV / Emergent & Voyage /
  Inspection/Survey / Other
- `rmc` - SWRMC, MARMC, SERMC, NW RMC, Pearl Harbor RMC, SRF-JRMC
  Yokosuka, FDRMC Naples, FLC Bahrain, MSC HQ, NAVSEA HQ, USCG SFLC,
  NUWC, Portsmouth NSY, Norfolk NSY, Army/USACE, Other
- `contractor_tier` - Tier 1 CONUS Complex (BAE/HII/GD/Vigor/NASSCO/
  Detyens/Metro Machine/Marine Hydraulics/Continental Maritime), Tier 2
  Regional, Tier 3 Technical Services, Tier 4 FDNF Foreign Yard
  (Hanwha/Navantia/Sumitomo/UniThai/Cabras/Mitsubishi/Samsung/Viktor
  Lenac/Seatrium/Shinko/Motoyama/Hosei), Other

Cascade: award MOD 0 desc -> `all_mod_descriptions` -> parent IDV descs ->
husbanding IDV fallback -> Other. Rule-based only; no LLM dependency. Writes
`j998_j999_classified.json` to same folder.

Initial numbers reconciled to the research doc (DSRA $1,438M, SRA $451M, CMAV
$275M, DPIA $170M, SWRMC $1,584M, MARMC $1,022M, Tier 1 primes $3,017M =
~60% of total). Pearl Harbor RMC $125M came out 100% in "Other" availability
bucket - first flag that the regex was Navy-centric and missing MSC/USCG
vocabulary.

**`sheets/depot_ship_repair.py`** (new). Nine sections:
1. TAM Headline (J998 East / J999 West)
2. Availability Group rollup
3. Availability Type detail
4. Availability Group x Hull Program crosstab (primary deck source)
5. RMC rollup + RMC x Availability Group
6. Contractor Tier rollup + Tier x Availability Group
7. Top contractors within each tier (subsubsec-banded)
8. Top 15 task orders (PIID, ship, $, availability, RMC, recipient)
9. Top 15 parent IDV vehicles ($ allocated by share-of-parent-IDVs)

Pattern: static values computed in Python, not SUMIFS. The new dimensions
don't exist as columns on the unified Awards table and the sheet is a
report/snapshot, not a live driver - static is cleaner.

Fallback: if `j998_j999_classified.json` is missing, re-classify in-memory
from the raw JSON so the workbook build never hard-fails.

**Wired into `build_from_data.py`:** `create_depot_ship_repair(wb)` after
`create_mro(wb)`; `1B5E20` (deep green) tab color; new sheet sits between
Services and Sub Ratios. README.md + CLAUDE.md updated per structural-change
rule.

Built v2.65; spot-check confirmed layout + numbers reconciled.

### 3. Empirical push-back: "read the actual JSON, not the markdown"

User challenged the taxonomy choices and asked for a fresh empirical dive into
the JSON rather than relying on my summary of the research doc. Ran several
probes across all 9,231 mod descriptions:

| Signal | Awards | FY25 $ | Notes |
|---|---|---|---|
| Growth work / new work | 168 | $1,616M | 32% of total - mod lifecycle, not scope |
| Option exercise | 29 | $1,577M | Same |
| Descope | 133 | $1,231M | Same |
| Admin / reconcile | 112 | $732M | Same |
| RCC / RCCS codes | 239 | $1,793M | Same |
| Hull / coatings | 153 | $31M | 0.6% |
| Propulsion / MRG | 67 | $28M | 0.6% |
| Combat systems | 15 | $5M | 0.1% |
| Electronics / C4I | 4 | $0.2M | ~0% |

**Key finding:** SWBS / system-level signals are nearly absent (~2% of $).
Big mods (>$50M) carry only the availability wrapper ("USS GREEN BAY FY25
DSRA"); small mods (<$200K) sometimes name a specific trade ("PIPE LAGGING",
"NON-SKID ALTERATIONS", "PUMPS AND MOTORS OVERHAUL").

**Second finding:** The $1.34B "Other" residual was mostly a vocabulary gap,
not genuine residual:

| Missed pattern | Awards | $M | Example |
|---|---|---|---|
| MSC ROH (Regular Overhaul) | 18 | $353M | USNS MATTHEW PERRY FY25 REGULAR OVERHAUL AND DRY-DOCKING AVAILABILITY |
| MSC MTA (Mid-Term Avail) | 27 | $219M | USNS ROBERT E. PEARY MID-TERM AVAILABILITY |
| MSC CAT A / CAT B | 15 | $198M | USNS WALLY SCHIRRA ROH CAT A |
| MSC SIA | 11 | $23M | FY25 ROOSEVELT SIA LABOR |
| USCG DOCKSIDE REPAIR | ~16 | ~$25M | CGC HEALY FY25 DOCKSIDE REPAIR |
| FMS (out of scope) | 17 | $85M | EGYPTIAN NAVY FOTS (FMS) |
| Barges / APL / YRBM | 64 | $71M | APL-61 MESSING AND BERTHING BARGES |

**Third finding:** The real "what work is being done" signal lives in the
**parent IDV description**, not the award or mod text. IDV names are
explicit and specific:
- "CNO AVAILABILITIES COMPLEX SURFACE COMBATANTS IDIQ" - full-ship CNO avail
- "HULL MECHANICAL & ELECTRICAL (HM&E) REPAIR IDIQ" - single-trade IDIQ
- "CIS PIPE LAGGING SERVICES" - single-trade IDIQ
- "SCAFFOLDING IDIQ" - single-trade IDIQ
- "MSRA WITH HANWHA OCEAN CO., LTD." - FDNF foreign yard
- "CVN PACIFIC NORTHWEST PRIVATE SECTOR MAINTENANCE (PSM)" - CVN-specific

Proposed two improvements: **v1.1** = extend the availability classifier with
the missing vocabulary; **v2** = hand-curated (or LLM-generated) IDV Scope
Type taxonomy. User approved both, requested Opus 4.6 specifically for v2
(saved to memory as `project_j998_j999_v2_llm.md`).

### 4. v1.1 - MSC/USCG vocabulary fix (v2.65 -> v2.66)

`classify_j998_j999.py` - extended `AVAILABILITY_PATTERNS` with MSC parallel
cycle (ROH, MTA, SIA, CAT A/B, DOS Period, Deactivation), USCG/FDNF pierside
(Dockside Repair, Lay Berth Repair), shipyard production labor, and generic
"MAINTENANCE AVAILABILITY" catch-all. Added FMS and Barge pre-empt patterns
that bypass the normal cascade so those awards get their own buckets. Also
fixed a regex bug where `\bAVAIL\b` failed to match "AVAILABILITY" (word
boundary between AVAIL and A fails since both are word chars).

Three new `availability_group` values: **MSC Availability**, **USCG / FDNF
Pierside**, **Shipyard Production Labor**, **Support Infrastructure**, **Out
of Scope (FMS)**. Sheet's `AVAILABILITY_GROUP_ORDER` and
`AVAILABILITY_TYPE_ORDER` updated. TAM headline gained a FMS carve-out line:
**$5,008M gross - $85M FMS = $4,922M in-scope US TAM**.

Results:
- "Other" residual shrank from $1,341M to **$524M (-61%)**
- MSC Availability emerged as its own $792M bucket (~16% of total)
- FMS cleanly carved out for TAM reconciliation

v2.66 built successfully.

### 5. v2 - LLM-generated IDV Scope Type taxonomy (v2.66 -> v2.67)

Per user preference (memory: project_j998_j999_v2_llm.md), used
**claude-opus-4-6**.

**`data_pull/classify_j998_j999_idv_scope.py`** (new). Two phases:

**Phase 1 - Taxonomy generation.** First attempt tried a single Opus call
producing both taxonomy + 360 IDV assignments in one structured output. Two
iterations failed:
1. Non-streaming call rejected by SDK: "Streaming is required for operations
   that may take longer than 10 minutes" (max_tokens=32K).
2. Switched to streaming + `output_config.format.json_schema`; 400 error
   because Pydantic's auto-generated schema omits the mandatory
   `additionalProperties: false` at every object level.
3. Switched to `stream() + output_format=<PydanticModel>` - SDK handles the
   strict-schema requirements internally. Ran, but adaptive thinking consumed
   all 64K output tokens on thinking alone, returned zero text blocks.

**Final architecture - split Phase 1 into 1a + 1b:**
- **Phase 1a** (one call, no thinking, 8K max_tokens): generate taxonomy
  only. Returns 15 categories across 7 groups. ~2K tokens output.
- **Phase 1b** (batched async, no thinking, 8K max_tokens): classify 360
  IDVs in batches of 30 at concurrency=8. 12 batches. System prompt (with
  embedded taxonomy) cached via `cache_control`.

**Phase 2 - Residual sweep.** 471 awards have no parent IDV at all (mostly
direct-award DSRAs, MSC ROHs, FMS, and one-off task orders). Async
per-award calls against the cached taxonomy at concurrency=8.

**Results:**

| Phase | Duration | Calls | Cost | Notes |
|---|---|---|---|---|
| 1a (taxonomy) | ~30 sec | 1 | ~$0.32 | 15 categories, 7 groups |
| 1b (IDV assign) | ~2 min | 12 batches | ~$1.03 | 360/360 assigned, 0 errors |
| Phase 2 (residuals) | ~5 min | 471 | $10.84 | 468/471 classified, 3 errors |
| **Total** | ~8 min | 484 | **$12.20** | |

Phase 2 cost was higher than expected because prompt caching did not
trigger - the system prompt was ~1,800 tokens, below Opus 4.6's 4,096-token
minimum cacheable prefix. Future iteration: batch Phase 2 the same way
Phase 1b is batched, which both shrinks the per-call input and keeps the
amortized cost near $3.

**Taxonomy generated by Opus:**

| Group | Category | Assignments |
|---|---|---|
| Full-Ship Availability | CVN Private Sector Maintenance | 5 |
| Full-Ship Availability | CNO Avails - Surface Combatants | 47 |
| Full-Ship Availability | CNO Avails - Amphibious Ships | 22 |
| Full-Ship Availability | LCS Maintenance Vehicles | 28 |
| MSC Availability | MSC General Ship Repair | 35 |
| FDNF Foreign MSRA | MSC / FDNF Foreign Yard MSRA | 36 |
| USCG Cutter | USCG Cutter Maintenance | 47 |
| Trade IDIQ | Trade IDIQ - HM&E Repair | 22 |
| Trade IDIQ | Trade IDIQ - Surface Coatings | 22 |
| Trade IDIQ | Trade IDIQ - Insulation & Lagging | 5 |
| Trade IDIQ | Trade IDIQ - Other Trades | 25 |
| Other / Support Services | Barge & Small Craft Support | 27 |
| Other / Support Services | Production & Workforce Support | 15 |
| Planning & Engineering Support | Planning, Engineering & Logistics | 10 |
| Other / Support Services | Army Watercraft Maintenance | 13 |

**Join into classifier.** `classify_j998_j999.py` extended with
`classify_idv_scope()` that looks up the IDV scope category for each
award's parent IDV (taking the first-assigned IDV when multiple are
referenced) or from the residual map when no IDV. Adds `idv_scope_type`
and `idv_scope_group` fields alongside the existing v1.1 fields.

**Final attribution (FY25 $):**

| IDV Scope Group | $M | % |
|---|---|---|
| Full-Ship Availability | 3,258 | 65% |
| MSC Availability | 551 | 11% |
| FDNF Foreign MSRA | 513 | 10% |
| Other / Support Services | 306 | 6% |
| USCG Cutter | 144 | 3% |
| Trade IDIQ | 123 | 2% |
| Planning & Engineering Support | 108 | 2% |

**Answer to user's "what work is actually being done":** 65% of J998/J999
is the full-ship availability wrapper pattern (CNO avails / DSRAs / DPIAs on
specific hulls). Trade-specific IDIQs (HM&E, coatings, insulation, other)
are only **2%** of the $. Availability-type dimension covers the 65%; the
Trade IDIQ slice is where system-specific scope is explicit.

**Sheet update:** three new sections in `depot_ship_repair.py` positioned
between "Top Contractors Within Each Tier" and "Top 15 Task Orders":
1. IDV Scope Group rollup
2. IDV Scope Type detail (with dollars by ordered category)
3. Two crosstabs: IDV Scope Group x Availability Group, Group x Tier

Sheet gracefully skips all three sections if the taxonomy JSON is missing.

### 6. Bug fix: Services formula length

On opening v2.67, Excel flagged "Removed Records: Formula from
/xl/worksheets/sheet3.xml" (sheet3 = Services). Repair log pointed at one
cell.

Root cause: `_write_top_contractors` in `services.py` builds a formula of
the form `(SUMIFS + SUMIFS + ...)/1000000` looping over all 65 `MRO_PSCS`
with the parent name embedded in every `SUMIFS`. For parent names >=45
chars, formula length exceeds Excel's 8,192-char per-cell limit. Example:
S.C.A. - SHIPPING CONSULTANTS ASSOCIATED LTD. at rank 10 generated a
formula of 8,200 chars -> stripped by Excel on open.

Fix: when the built formula exceeds 8,000 chars (80-char safety margin),
write the pre-computed `$M` value (which is already known at write time
from the Python ranking pass) instead of the formula. Short-name contractors
keep the live SUMIFS; long-name ones degrade gracefully.

**Not yet rebuilt** - fix staged for the next build.

---

## Files created

**New in `data_pull/`:**
- `classify_j998_j999.py` - rule-based availability/RMC/tier/scope classifier
- `classify_j998_j999_idv_scope.py` - Opus 4.6 taxonomy + residual classifier

**New in `sheets/`:**
- `depot_ship_repair.py` - standalone deep-dive sheet

**New LLM / classifier artifacts in `data_pull/output/fpds/`:**
- `j998_j999_classified.json` (11.3 MB) - every award tagged with 6 new fields
- `idv_scope_taxonomy.json` (82 KB) - 15 categories + per-IDV assignments with
  Opus's citations
- `idv_scope_residuals.json` (283 KB) - 468 no-IDV awards classified with
  citations + confidence (high/medium/low)

**New in `sessions/`:**
- This file.

## Files modified

- `build_from_data.py` - added `create_depot_ship_repair` import + call +
  tab color
- `README.md` - added Depot Ship Repair to repository layout + workbook
  build reference
- `CLAUDE.md` - added classifier versioning note
- `sheets/services.py` - formula-length guardrail in `_write_top_contractors`

## Memories added

- `project_j998_j999_v2_llm.md` - use `claude-opus-4-6` for v2 IDV taxonomy
  work, not the pipeline's default `claude-sonnet-4-6`

---

## Workbook progression

| Version | Change | New Sheet | Rows | Awards classified |
|---|---|---|---|---|
| v2.64 -> v2.65 | Initial Depot Ship Repair | **Depot Ship Repair** (9 sections) | 174 | 2,861 |
| v2.65 -> v2.66 | v1.1 MSC/USCG vocabulary fix | (updated) | 174 | 2,861 |
| v2.66 -> v2.67 | v2 IDV Scope Type crosstabs | (updated) | 253 | 2,861 |

v2.67 is current. Known bug fix staged for next build: Services sheet formula
length guardrail.

## Open flags

- **Army Watercraft Maintenance ($137M)** - USACE dredge work (W9127N
  prefix). Already excluded from main Services TAM via
  `NON_SHIP_MRO_PIID_PREFIXES` but appears here because
  `j998_j999_awards.json` is a separate extract that doesn't apply that
  filter. If we want the Depot Ship Repair TAM to match Services TAM
  exactly, add a PIID-prefix exclusion to `classify_j998_j999.py`.

- **Phase 2 cost optimization** - batch the residual classification the
  same way Phase 1b batches (~30 awards per call with the taxonomy-embedded
  system prompt shared via cache). Should cut $10 -> ~$3 and pull the
  total run cost to ~$5.

- **Phase 2 missed 3 errors** - 3 of 471 no-IDV awards returned API errors
  during classification. They stay with empty `idv_scope_type` and roll up
  into the "(empty)" row in the sheet. Low $ tail - worth a small pass to
  retry these.

- **One IDV unassigned in Phase 1b** (`N4002721D1006`). LLM omitted it
  from a batch. $0 FY25 impact. Not worth a retry.
