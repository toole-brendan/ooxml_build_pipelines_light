# 2026-06-20 — Contracts layer: full 6-stage pipeline built + run (session log + handoff)

Seventh session (same day), continuing directly from `2026-06-20_contracts_layer_discovery.md`.
That session built + ran **Stage 1 (discovery)** and *designed* Stages 2–6. This session **built,
smoke-validated, and ran** the rest of the pipeline: fixed the Stage-1 Army-tail gap, built Stages
2–6 + the aggregate, and produced the four workbook contract CSVs. Two live-API gotchas surfaced
that invalidate parts of the reference playbook (documented below + in memory).

## TL;DR of what changed
- **Stage 1 re-scoped** (gotcha #6 fix): code-axis (NAICS/PSC) queries now scope to awarding
  **subtier "Department of the Army"** instead of DoD-wide, so the 1,500-record cap applies within
  Army. **In-scope universe grew 1,121 → 2,595** (2,677 unique; only 82 out-of-scope; Navy excluded).
- **Stage 2 (USAspending detail)** built + run: per-award detail + per-mod transactions + File-C
  funding (TAS) for all 2,595 in-scope awards. Emits `_detail_index.json` + `_vendors.json`.
- **Stage 3 (FPDS per-mod)** built + run: authoritative per-mod obligations by vendor, Army-scoped.
- **Stages 4–6 (SAM)** built + smoke-validated: subawards (by piid), opportunities (pre-award),
  entity (UEI→NAICS/CAGE). Quota-aware + resumable; full subaward/opportunity runs are cheap-to-
  resume and left as deliberate runs.
- **`aggregate_contracts.py`** built + run → four tidy CSVs in `workbook/extracted/`.

## ⚠ Two load-bearing gotchas found this session (reference playbook is STALE)

### G1. "Department of Defense" is also "Department of War" (~2025 rename)
Agency-name filters must NOT pin the toptier DoD label. Verified live on USAspending: a
`toptier "Department of War"` filter returns **0 rows** today; `"Department of Defense"` works — but
don't depend on either. **Fix applied everywhere:** scope by **subtier** (`Department of the Army`)
or **codes** (Treasury `9700`, FPDS contracting-agency `2100`, UEI, TAS), never the toptier name.
The Stage-1 `in_scope()` post-filter (matches `army`/`corps of engineers`/`engineer`) is already
robust. Memory: `dod-department-of-war-rename`.

### G2. FPDS `VENDOR_NAME` is dead; use `VENDOR_UEI` / `VENDOR_FULL_NAME`
The May-2026 shipbuilding `pull_fpds_*` scripts key off `VENDOR_NAME:"..."`. **That field is now
silently dropped** — FPDS echoes it in the feed `<title>` but returns the entire ~17M-record dataset.
Verified working replacements:
- `VENDOR_UEI:"<uei>"` (primary; we have UEIs from Stage 2) — exact, drift-proof.
- `VENDOR_FULL_NAME:"<legal name>"` (exact-phrase fallback).
- `CONTRACTING_AGENCY_ID:"2100"` = **Army + USACE Engineer Districts (ENDIST...) + TACOM (W4GG)** in
  one code — the complete Army+USACE scope. `DEPARTMENT_*` filters don't resolve.
Validation: Eastern Shipbuilding `W912BU23C0020` FPDS per-mod sum = **$258.5M = USAspending exactly**.
Memory: `fpds-atom-field-changes`.

## The 6-stage pipeline (status)
| # | Stage | Source | Script | Status |
|---|-------|--------|--------|--------|
| 1 | Discover candidates | USAspending `spending_by_award` | `pull_usaspending_discovery.py` | **DONE (re-scoped+re-run)** |
| 2 | Award detail / per-mod txns / File-C funding | USAspending `/awards/{id}/`, `/transactions/`, `/awards/funding/` | `pull_usaspending_detail.py` | **RUN (2,595 awards)** |
| 3 | Authoritative per-mod actions | FPDS Atom by `VENDOR_UEI`+agency 2100 | `pull_fpds_actions.py` | **RUN (vendors ≥ $1M)** |
| 4 | First-tier subawards | SAM `/contract/v1/subcontracts/search?piid=` | `pull_sam_subawards.py` | **BUILT + smoke-validated** |
| 5 | Pre-award pipeline | SAM Opportunities (title search) | `pull_sam_opportunities.py` | **BUILT + smoke-validated** |
| 6 | Vendor enrichment | SAM Entity (UEI→NAICS/CAGE) | `pull_sam_entity.py` | **BUILT + smoke-validated** |
| — | Aggregate → workbook CSVs | local | `aggregate_contracts.py` | **RUN** |

## Output state (`research/contracts/`)
```
scripts/pull_usaspending_discovery.py   Stage 1 (edited: ARMY_SUBTIER code-axis scope)
scripts/pull_usaspending_detail.py      Stage 2 (NEW)
scripts/pull_fpds_actions.py            Stage 3 (NEW)
scripts/pull_sam_subawards.py           Stage 4 (NEW)
scripts/pull_sam_opportunities.py       Stage 5 (NEW)
scripts/pull_sam_entity.py              Stage 6 (NEW)
scripts/aggregate_contracts.py          Aggregate (NEW)
usaspending_raw/discovery_*.json        Stage 1 raw (re-run)
usaspending_raw/detail|transactions|funding/<gid>.json   Stage 2 raw (full native)
fpds_raw/<vendor>.json + _fpds_index.json                Stage 3 raw (full native xml_to_dict)
sam_subawards/<piid>_*.json             Stage 4 raw (smoke: 1 PIID so far)
sam_entity/<uei>.json                   Stage 6 raw (smoke: 4 UEIs so far)
sam_opportunities/<term>_<yr>.json      Stage 5 raw (smoke: 1 query so far)
extracted/_detail_index.json            Stage 2 per-award index (seed for 3–6/aggregate)
extracted/_vendors.json                 distinct-vendor roster (seed for Stage 3 & 6)
extracted/_fpds_index.json              Stage 3 per-vendor reconciliation summary
extracted/_subawards_index.json _entity_index.json _opportunities_index.json
workbook/extracted/contract_awards.csv               one row per award (register)
workbook/extracted/contract_award_actions.csv        one row per mod — THE sum-able table
workbook/extracted/contract_subawards.csv            first-tier FFATA subs
workbook/extracted/contract_pipeline_events.csv      pre-award notices
```

## Architecture / money discipline (unchanged from session-6, now realized)
- **awards** (register; distinct amount_type COLUMNS obligation/current_value/ceiling — never summed
  across) ≠ **award_actions** (one per mod, `amount_type=obligation`, **THE ONLY table you sum**) ≠
  **subawards** (`amount_type=subaward`, a separate money universe) ≠ **pipeline_events** (no $).
- **FPDS wins on $ conflict:** award_actions take FPDS per-mod `obligatedAmount` where the vendor was
  pulled; USAspending `/transactions/` fill awards FPDS didn't return. `actions_source` column flags
  which. Expect per-mod sum to differ a few % from award-level obligation (FPDS Army-scope drops
  DCMA-administered admin mods; deobligations).
- **Budget tie-back:** Stage-2 File-C funding gives the **TAS** (`federal_account`, e.g. `021-2035` =
  Other Procurement Army; `021-2020` = O&M Army) → maps to appropriation/PE/BLI via the budget
  `line_item` keys. ~Many awards report 0 File-C rows (recent / IDV task orders report under parent) —
  that's expected, the `has_tas` flag marks it.
- **Provenance** on every CSV row: `source_system`, `source_id`, `extract_run_id`, `row_hash` (same
  pattern as `budget_funding_facts.csv`).
- **Analyst bridges left BLANK** (invariant #2 — no judgment in the mechanical aggregate):
  `program` (program-attribution bridge) and `capability_node` (Platform/Sensors/Effectors/C2 via
  `workbook/analyst/capability_nodes.csv`) columns are emitted empty for the analyst to fill.

## HANDOFF — next steps (in order)
1. **Finalize the full runs** (this session kicked them): confirm `pull_usaspending_detail.py`
   finished all 2,595, then run `pull_fpds_actions.py` (all vendors ≥ $1M) and re-run
   `aggregate_contracts.py`. (Tally section below is finalized once these complete.)
2. **Run SAM Stage 4 fuller** — `python3 pull_sam_subawards.py` pulls subs for all primes ≥ $1M
   (~2 calls each, biggest-first, resumable; 1,000/day quota). Then re-run aggregate to populate
   `contract_subawards.csv`.
3. **Run SAM Stage 6** — `python3 pull_sam_entity.py` over the full vendor roster (~1 call/UEI).
4. **Run SAM Stage 5 deliberately** — `pull_sam_opportunities.py` full plan is ~72 calls × ~60s
   (~70 min). Title-only search; AWSM + watercraft-targets notices already validated.
5. **Recompete radar** — derive from award_actions + awards: `pop_current_end_date` vs
   `pop_potential_end_date`, parent-IDV vs task-order expiries, option years, `extent_competed` →
   confidence + pursuit-access ratings. (Fields are all present in `contract_awards.csv`.)
6. **Analyst tagging pass** — fill `program` + `capability_node` on the four CSVs via the bridges.

## How to re-run (all idempotent + resumable; existing raw files are skipped)
```bash
cd projects/army/research/contracts/scripts
python3 pull_usaspending_discovery.py     # Stage 1 (overwrites extracted/ + usaspending_raw/discovery_*)
python3 pull_usaspending_detail.py        # Stage 2 (all seeds; arg N = first-N smoke)
python3 pull_fpds_actions.py              # Stage 3 (vendors ≥ $1M; arg N = top-N; MIN_OBL env to tune)
python3 pull_sam_subawards.py             # Stage 4 (primes ≥ $1M; "1 <PIID>" = smoke one)
python3 pull_sam_entity.py                # Stage 6 (arg N = top-N vendors)
python3 pull_sam_opportunities.py smoke   # Stage 5 (one call) | bare = full ~70-min plan
python3 aggregate_contracts.py            # → workbook/extracted/contract_*.csv
```

## RESULTS (smoke-validated; full tally finalized at end of session)
- Stage 1 re-run: **2,677 unique awards → 2,595 in-scope (Army+USACE)**, 82 out-of-scope; Navy excl.
- Stage 3 smoke (4 watercraft primes): Eastern reconciles to the dollar ($258.5M); Vigor/Birdon FPDS
  totals exceed the smoke-only USAspending subtotal because the smoke `_vendors.json` summed just 3
  awards each (closes on full run).
- Stage 4 smoke: Vigor TO `W56HZV21F0381` → 74 published subs, $20.6M (task-order `referencedIDVPIID`
  handling validated; the 0-record pagination-hang bug was found+fixed — SAM returns a non-null
  `nextPageLink` even at 0 records, so stop on empty/short page or `totalPages`, NOT on null link).
- Stage 5 smoke: "watercraft" 2025 → 4 notices incl. **Army Watercraft Sustainment Maintenance (AWSM)**.
- Stage 6 smoke: 4/4 vendors resolved (Vigor primary NAICS 332312 fab-metal, not 336611 — a signal).
- Aggregate smoke (8 awards): 252 FPDS mod-actions, $774.8M sum-able; 74 subs; 4 pipeline events.

## FINAL TALLY (full runs complete)
- **Stage 2:** 2,595 awards indexed, **0 failures** (detail/txn/funding all clean); 826 awards with
  File-C TAS tie-back; **751 distinct vendors, 141 ≥ $1M**. Outputs: `_detail_index.json` (4.4 MB),
  `_vendors.json`.
- **Stage 3:** 141 vendors pulled, **20,756 per-mod actions**, $12,655.3M summed obligatedAmount
  *across the vendors' FULL Army books* (390 PIIDs for Defense Systems & Solutions, etc.). The
  watercraft-relevant slice is what reconciles to discovered PIIDs in the aggregate. Dropped tail =
  610 sub-$1M vendors = $76.6M (~3%, already in Stages 1-2). Vigor reconciles to 0.6% ($422.4M FPDS
  vs $420.0M USAspending).
- **Aggregate → `workbook/extracted/`:**
  - `contract_awards.csv` — **2,595 awards** (44 cols; actions_source = 1,446 FPDS / 1,149 USAspending).
  - `contract_award_actions.csv` — **7,757 mod actions**, all `amount_type=obligation`, **sum =
    $3,249.6M** (THE sum-able number; 5,808 FPDS + 1,949 USAspending rows; FY 2010-2026). Bounds to
    the discovered watercraft universe — NOT the $12.66B vendor-book total. Cross-check: awards-level
    obligation sum $3,587.0M (9.4% above per-mod, = FPDS Army-scope dropping DCMA admin mods +
    deobligations + FPDS-wins reconciliation).
  - `contract_subawards.csv` — **305 first-tier subs, $112.5M** (Stage 4 RAN: 364 primes ≥ $1M,
    Published-only via SKIP_DELETED to fit quota; 19 primes carry subs — mostly Vigor MSV(L) task
    orders = the watercraft supplier base).
  - `contract_pipeline_events.csv` — 4 notices (Stage 5 Opportunities NOT run — slow/quota; smoke only).

**SAM stages run (2026-06-20):** Stage 4 subawards (Published-only, ≥$1M primes) + Stage 6 entity
(top 150 vendors → **143 resolved** in SAM registry; UEI→NAICS/CAGE/business-types in
`_entity_index.json` + `sam_entity/<uei>.json`). ~528 SAM calls used (of 1,000/day). Stage 5
Opportunities left for a deliberate ~70-min run. **Quota gotcha relived:** the resumable scripts only
work from the scripts dir — a stale `cd` made the first launch fail to find the script (no calls spent);
re-launched from `research/contracts/scripts/`.

**Key takeaway for the analyst:** the prime-contract spine (awards + award_actions, $3.25B) is COMPLETE
+ reconciled, and the subaward + vendor-registry enrichment is populated. Remaining = Stage 5
Opportunities (optional) + the analyst tagging pass (program + capability_node via the bridges) +
recompete-radar derivation (all input fields already on `contract_awards.csv`).
