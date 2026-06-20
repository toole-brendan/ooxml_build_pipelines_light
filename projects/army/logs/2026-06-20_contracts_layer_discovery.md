# 2026-06-20 — Contracts layer kickoff: discovery stage (session log + handoff)

Sixth session (same day). Started the **contracts/awards layer** — the stage after the funding
layer in the evidence chain (*mission → user → requirement → acquisition → funding → **contract** →
timing → competitive route*). This session: chose the architecture, scaffolded the pull pipeline,
wrote shared helpers + the discovery script, and ran **Stage 1 (discovery)** live. Stages 2–6 are
designed but not built.

Companion notes from earlier today (read for context): `2026-06-20_schema_adjustments_killchain.md`
(the schema spine + 4-node kill-chain taxonomy) and `2026-06-20_budget_extraction_p5_rdte_oma.md`
(the funding layer this builds on).

## Source-of-truth inputs (read these)
- `projects3/Federal_Award_API_Research_Methodology.docx` — the FPDS/USAspending/SAM API playbook.
- `projects3/army_transcript.xml` (methodology) + `army_transcript_2.xml` (schema) — the analyst's intent;
  contracts table design = transcript-2's `awards / award_actions / subawards / pipeline_events` +
  (later) `contract_family / recompete_snapshots`.
- Reference implementations (proven pattern, DIFFERENT scope/market):
  `projects/distributed_shipbuilding/{ddg,submarines}/research/` — pull scripts + `SAM_GOV_HOWTO.md`.

## Architecture decision (the answer to "JSON raw → CSV?")
**Yes** — per-source RAW pulls saved as JSON → aggregate scripts → CSVs into `workbook/extracted/`
(the same build contract the funding layer uses). This matches both the sibling shipbuilding projects
and transcript-2's `raw_extracts → standardized → research_links` tiers. **Two upgrades over the
reference:**
1. **Keep ALL native fields in raw** (user direction). The reference trimmed FPDS to ~30 picked
   elements and USAspending subawards to 6; we keep full records. `_common.xml_to_dict` captures every
   FPDS element/attribute/repeat; USAspending/SAM JSON objects are stored whole. *Discovery is a thin
   index; the per-award DETAIL stage pulls the complete record.*
2. **Discovery is USAspending-led, NOT FPDS-led** (deviation from the reference, evidence-driven — see
   gotcha #1). FPDS is reserved for its real strength: authoritative per-mod actions by `VENDOR_NAME`.

## Output state (`research/contracts/`)
```
scripts/_common.py                     IPv4 patch + .env loader + http get/post + faithful xml_to_dict
scripts/pull_usaspending_discovery.py  STAGE 1 (built + run)
usaspending_raw/discovery_*.json       46 raw response files (full returned fields)
extracted/contracts_discovered.csv     1,121 in-scope (Army+USACE) candidate awards
extracted/contracts_discovered_all.csv 6,873 unique awards + in_scope flag (audit)
extracted/_discovered_piids.json       1,121 seed handles {generated_internal_id, piid, recipient, ...}
pull_logs/usaspending_discovery.log    run log (per-query counts, agency calibration, top-25)
```
Empty dirs awaiting later stages: `fpds_raw/ sam_subawards/ sam_opportunities/ sam_entity/`.

## Scope (locked)
**Army + USACE/ERDC only; Navy/USMC dropped entirely** (not even context). ERDC (Engineer R&D Center,
incl. Coastal & Hydraulics Lab) is *inside* USACE. **Calibration win:** USACE engineer-district awards
(PIID prefix `W912xx`) file under USAspending awarding subtier **"Department of the Army"** — so that one
subtier captures Army + USACE and excludes Navy. The current discovery post-filters on agency strings
containing `army` / `corps of engineers` / `engineer`.

## SAM.gov key
`SAM_API_KEY` (entity-role, 1,000 req/day) in `/Users/brendantoole/projects3/ooxml_build_pipelines_light/.env`.
`_common.env()` reads it; `_common` also installs the macOS IPv4 monkeypatch and raises `QuotaExhausted`
on HTTP 429. **Never echo the key.**

## The 6-stage pipeline (status)
| # | Stage | Source | Script | Status |
|---|-------|--------|--------|--------|
| 1 | Discover candidate awards | USAspending `spending_by_award` | `pull_usaspending_discovery.py` | **DONE** |
| 2 | Award detail / FY obligations / funding accounts | USAspending `/awards/{id}/`, `/transactions/`, `/awards/funding/` | `pull_usaspending_detail.py` (TODO) | pending |
| 3 | Authoritative per-mod actions | FPDS Atom by `VENDOR_NAME` | `pull_fpds_actions.py` (TODO) | pending |
| 4 | First-tier subawards | SAM.gov `/contract/v1/subcontracts/search?piid=` | `pull_sam_subawards.py` (TODO) | pending |
| 5 | Pre-award pipeline | SAM.gov Opportunities | `pull_sam_opportunities.py` (TODO) | pending |
| 6 | Vendor enrichment | SAM.gov Entity (UEI→NAICS/CAGE) | `pull_sam_entity.py` (TODO) | pending |
| — | Aggregate → workbook CSVs | local | `aggregate_contracts.py` (TODO) | pending |

## Stage-1 results (2026-06-20)
6,873 unique awards → **1,121 in-scope (Army+USACE)**, 403 distinct recipients, ~$3.0B in award amounts;
Navy (5,024 awards) correctly excluded. Watercraft cast that surfaced:
- **Vigor Works LLC** — MSV(L) new-construction (`W56HZV` = ACC-Detroit Arsenal / TACOM).
- **Birdon America Inc** — PSC 1940 small craft (`W56HZV`); a second watercraft prime.
- **Bay Ship & Yacht Co / Colonna's Shipyard** — LCU/LSV SLEP & repair (= the **ESP** work).
- USACE-district builders (Eastern Shipbuilding, Conrad, Gunderson, Alabama Shipyard, …) under `W912xx`.
- **DCS Corporation** — matched "army watercraft" engineering (likely SETA / C2-integration — watch).

## HANDOFF — read first if picking this up cold

### A. How to re-run / extend
```bash
cd projects/army/research/contracts/scripts
python3 pull_usaspending_discovery.py        # idempotent; overwrites extracted/ + usaspending_raw/
```
- **Add a discovery term:** append to `KEYWORD_QUERIES` (clean phrase match) or `CODE_QUERIES`
  (NAICS/PSC). Keyword queries run agency-unrestricted + post-filter; code queries run DoD-scoped.
- **Tune scope:** `in_scope()` is the Army+USACE gate. `contracts_discovered_all.csv` keeps everything
  with the flag, so widening scope = relax that predicate and re-consolidate (no re-pull needed if you
  parse the `usaspending_raw/` JSON).

### B. Gotchas (load-bearing — don't relearn the hard way)
1. **FPDS description search OR-tokenizes multi-word phrases.** `"MANEUVER SUPPORT VESSEL"` →
   `MANEUVER OR SUPPORT OR VESSEL` → ~1.6M records. Useless for program-name discovery. Use USAspending
   keyword search for discovery; use FPDS only by `VENDOR_NAME` (reliable) for authoritative per-mod data.
2. **macOS IPv6 hang** — `_common` forces IPv4 via `socket.getaddrinfo` monkeypatch (else ~225s/request
   on api.sam.gov). Keep it. (From the shipbuilding `SAM_GOV_HOWTO.md`.)
3. **SAM 429 = daily quota gone** until midnight UTC; there is no quota-check endpoint. `_common` traps it
   and halts cleanly. Pull biggest-value PIIDs first so a mid-run halt still yields the important data.
4. **USAspending: contracts (A–D) and IDVs (IDV_*) can't mix** in one call → HTTP 422. Query each group
   separately (the discovery script already loops both).
5. **USAspending `fields` must be valid display names** or the call 422s. Current set is known-good; if
   you add a field and get 422, read the returned `detail` (http_post_json returns the error body).
6. **NAICS/PSC discovery ran DoD-wide and hit the 1,500 cap** (15 pages, Navy-dominated, sorted by amount
   desc). The Army *tail* below top-1500-by-amount is therefore undercaptured. **FIX (do first next
   session):** re-run code queries scoped to awarding subtier `"Department of the Army"`
   (add `{"type":"awarding","tier":"subtier","name":"Department of the Army"}` to the `agencies` filter)
   so the cap applies within Army — full tail, no Navy.
7. **FPDS:** never sum `totalObligatedAmount` across mods (double-counts); sum per-mod `obligatedAmount`.
   Direct PIID lookup returns nothing — use USAspending for PIID lookups.
8. **SAM subawards:** keep `/prod/` in the path; `piid` must be lowercase (uppercase silently dropped —
   verify the echoed `nextPageLink`); amounts are strings; reporting lags primes 6–18 months. Prefer the
   SAM subaward API over USAspending's (which caps ~2,500/prime and repeats cumulative snapshots).

### C. How it lands in the workbook (schema target)
Aggregate (`aggregate_contracts.py`, TODO) flattens `*_raw/` JSON → tidy CSVs in `workbook/extracted/`,
following the funding-layer invariants (see [[army-schema-spine]] / the schema note):
- **`awards`** (one per PIID/IDV/TO — current/potential value, ceiling, dates, incumbent, vehicle) ≠
  **`award_actions`** (one per mod — **the ONLY table you sum**; `amount_type=obligation`) ≠
  **`subawards`** ≠ **`pipeline_events`** ≠ (later) **`contract_family` + `recompete_snapshots`**.
- **Money discipline = the funding spine extended:** add `amount_type` values
  `obligation / current_value / potential_value / ceiling`; **never sum across budget + contract money**,
  and never sum across `amount_type` values.
- **Tie-back to the budget layer:** Stage-2 `/awards/funding/` gives the Treasury Account Symbol → maps to
  appropriation / PE / BLI, so the workbook can show *funded → on-contract* through the same line_item keys.
  Program-name → opportunity goes through the analyst **attribution bridge**; classify each contract to
  **Platform / Sensors / Effectors / C2** via the **capability bridge** (`workbook/analyst/capability_nodes.csv`).
- Provenance: every raw record carries source_system + the full native object; add `extract_run_id` +
  `row_hash` at aggregate time (same pattern as the funding facts) so analyst tags survive a re-pull.

### D. Open items / next steps (in order)
1. **Re-scope NAICS/PSC discovery to "Department of the Army" subtier** (gotcha #6) — full Army tail.
2. **Stage 2 — USAspending detail** per `generated_internal_id` from `_discovered_piids.json`: award
   detail + per-mod transactions (FY decomposition) + funding accounts (TAS → budget tie-back). Full fields.
3. **Stage 3 — FPDS per-mod** by the discovered vendor list (Vigor, Birdon, Bay Ship, Colonna's, …) for
   authoritative obligations + dates; reconcile against USAspending (FPDS wins on conflict).
4. **Stage 4–6 — SAM** subawards (by piid), Opportunities (recompete/pre-award signal), Entity enrich.
5. **`aggregate_contracts.py`** → the four workbook CSVs above.
6. **Recompete radar** inputs fall out of Stage 2/3: current_end_date vs potential_end_date, parent-IDV vs
   task-order expiries, option years, competition type → confidence + pursuit-access ratings.

### E. Cross-cutting notes
- The discovery `_discovered_piids.json` is the seed contract for stages 2–6 (mirrors the reference's
  `_discovered_piids.json` handoff between scripts).
- Many in-scope rows are USACE civil-works dredges/survey boats — relevant to **Platform** and **Sensors**
  (hydrographic survey) nodes, but confirm each is watercraft-relevant before tagging (some are pure
  dredging). The `description` + NAICS/PSC + later capability bridge handle this; keep judgment out of the
  raw pulls (invariant #2).
- `W56HZV` = ACC-Detroit Arsenal/TACOM (Army watercraft contracting office); `W912xx` = USACE districts.
  These office codes are a reliable secondary filter once confirmed against the data.
