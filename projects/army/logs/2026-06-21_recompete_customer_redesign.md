# 2026-06-21 — Recompete + customer redesign (the 7-item critique)

Session log AND handoff. Continues the same-day Phase-1 integrity refactor
(`2026-06-21_phase1_analytical_integrity_refactor.md`) and Phase 2-3 model/dashboard build
(`2026-06-21_phase2-3_market_model_and_dashboard.md`). Two independent reviews concluded the
Recompete Radar was a sound contract/incumbent **landscape but not a valid opportunity
forecast**, the Calendar had material **timing flaws** (not decision-grade), and the Customer
Map was a **3-row placeholder**. This session executed the approved 7-item redesign in one
pass while preserving the good architecture (contract-family spine, reconciliation,
segmentation, evidence-scored lineage, faithful-facts-vs-analyst separation).

Build is green: **19 sheets, 16 native tables, 2 note parts, 0 error cells.** Output:
`projects/army/20260620_US Army Market Mapping_vS.xlsx`. Verification: **`verify_timing.py`
19/19 checks pass**, **0 `t="e"` cells**, **0 `#REF!`/`#NAME?` formula literals**.

The two recompete sheets were RENAMED per the critique:
- **Recompete Radar → "Timing & Incumbent Screen"** (a contract/incumbent screen, not a
  forecast). Tab is 25 chars — the plan's "Contract Timing & Incumbent Screen" was 34, over
  Excel's 31-char tab limit.
- **Recompete Calendar → "Recompete Research Queue"** (timing flags to chase, Saronic-first).

---

## The #1 defect — recompete dates, fixed (critique items 2 & 3)

The old IDV recompete date was `MAX(child task-order ends)`, which pushed expired vehicles
years into the future. Replaced with a **classified `effective_decision_date`** on
`contract_families.csv` (`aggregate_contracts.py:_effective_decision`):
- **IDV** → ordering-period end (hydrated SAM CA), High confidence; → base-record PoP end,
  Medium; → child max only as an explicitly-flagged Low fallback.
- **BOA** → nominal end, Low ("not a guaranteed recompete"); **BPA** → call-period end, Medium;
  **Standalone** → own PoP end.
- `date_basis` / `date_confidence` / `date_anomaly` carry the rule + caveats.

Canonical cases (verified by `verify_timing.py`):
- **Birdon `W56HZV19D0093`** — decision **2025-08-12** (was mis-placed at 2030), latest-TO
  2030, anomaly `child order ends >5y after vehicle end`. **5 such "stopped-but-look-future"
  vehicles** now sit correctly in the past.
- **BOA `W912BU07G0001`** — **BOA / Low / 2050 anomaly** (`decision date 2050 > As-of+15y`).

Rendered as a **live green INDEX/MATCH link** into Contract Families; every As-of clock
(Months to decision, Recompete window, Decision FY, Capture-start, Notice-by, Option yrs)
re-points to the decision cell. Raw live inputs (Current end, Parent/vehicle end, Latest
task-order end) sit beside it for provenance. Architectural call: the date is a research
conclusion like `customer_segment` (BOA/anomaly logic is NOT honestly expressible in Excel),
so it's a classified VALUE surfaced via a link — not a baked Python value, not a fake formula.

### Correctness improvement beyond the plan — PIID position-9 agreement type
The plan's `agreement_type` helper read `idv_type`, but **hydration overwrites that field to
`"IDV (hydrated)"`**, masking the underlying instrument. Added **DoD PIID position-9 decoding**
(`mapping_rules._piid_instrument`): the 9th char of a legacy 13-char PIID is the authoritative
type code (DFARS PGI 204.16) and survives hydration — `G`=BOA, `A`=BPA, `D`=IDC, `F`=order.
Recovered **26 BOAs + 7 BPAs** previously masked → now correctly Low-confidence (the
agreement-specific discipline the review asked for). Date confidence shifted High=193 /
Low=26 / Medium=7.

---

## Opportunity hierarchy — multiple-award cohorts (critique item 1)

`aggregate_contracts.build_award_cohorts`: vehicles sharing office + PoP-start window +
ordering-end window + PSC under one **MULTIPLE-AWARD** requirement are ONE cohort (count
once), not N independent recompetes. Single-award/blank families are never clustered (the
over-merge guard). **24 cohorts, 32 screened families co-awarded.** `cohort_id` / `cohort_role`
(Lead vs Co-awarded) / `cohort_size` render on the screen.

### Latent bug `verify_timing.py` caught — cohort_id collisions
`COH-{office}-{psc}-{start_year}` collided across buckets with different ordering-end windows:
two distinct cohorts shared a label and the count understated by 3 (reported 21, true 24).
Fixed with a deterministic collision-safe suffix (`-2`, `-3`) → every cohort_id unique, one
Lead per cohort.

---

## Confirmed notice links (critique item 4)

The old "In-market notice" keyed on `award_number` and **never fired** (an open notice has no
award number yet). New **`Notice Links`** data sheet (`data_notice_links.py`, group=data, after
Pipeline Events) renders `notice_family_links.csv`; `_radar_formulas.inmkt` rewired to
`COUNTIFS(family_key, fam, analyst_confirmed, "Y")` — only an analyst-confirmed link fires.
Same-PSC stays a **separate** "Related activity (PSC)" flag on the Research Queue, captioned
as related activity not a confirmed link (21 of 22 signals are two PSC-1935 notices). Seeding
auto-confirms the single top-scored open link on a fresh build (analyst edits always win), so
the signal is non-empty end-to-end. **1 confirmed link** verified.

---

## Saronic-first + relevance (critique items 5 & 6)

- **`saronic_tier`** (`mapping_rules.saronic_tier`, pure derivation from `customer_segment`):
  Core (Army ops + autonomy/RDT&E) / Adjacent (MRO + logistics) / Peripheral (USACE +
  excluded). Distribution on the screen: **Core 38 / Adjacent 8 / Peripheral 180.**
- **Sort**: screen ranks `(tier_rank, -priority_score, -selected_measure)`; queue ranks
  `(tier_rank, decision_date)` within forward/overdue. All rows present — USACE/MRO just sort
  last and hide via the native AutoFilter. Verified **tier-monotonic**.
- **Relevance knobs on Market Size** (`model_market_size.py`): Mission / Platform / Autonomy-C2
  fit (blue, `analyst/saronic_relevance.csv`) + live **Saronic priority** composite
  (`AVG(fits) × timing × pursuit × win`, same product mechanics as Weighted pursuit).
- **Triage trio** on the screen: Opportunity (blue, from `award_opportunity_attribution.csv`)
  + Saronic priority score (live INDEX/MATCH into the Market Size composite, blank when a
  family isn't attributed — an honest "not scored", not 0). A build-time Python replica drives
  the sort and is asserted equal to the formula in `verify_timing.py`.

---

## Customer Map → relationship graph (critique item 7)

`customer_org_map.csv` rebuilt from a 3-row stub to a **13-org relationship graph**
(`aggregate_contracts.seed_customer_org_map`, `reseed_if_seed_only` so a real analyst map is
never clobbered): ASA(ALT), AMC, AFC, ACC, ACC-DTA (CSO route), CPE Combat Sustainment (new
nomenclature), PM Transportation Systems, Sustainment CDID, Contested Logistics CFT, USARPAC,
8th TSC, 569th Dive Det, ERDC — wired via `parent_org_id`, with decision rights, acquisition
pathways (FAR/OTA/CSO/prototype/experiment), geography, associated opportunity ids, and
citations in `notes`; engagement fields left blank for the analyst. `data_customer_map.py`
adds a live **`Vehicles at this office` = COUNTIFS** joining the org layer to the fact layer
through `contracting_office` (W56HZV→33, ERDC `W912HZ`→16; the seed's `W912` prefix was fixed
to the real 6-char DoDAAC so the join is meaningful, not a misleading 0).

---

## Seeding / migration (no clobbering analyst edits)

- **Facts** (mechanical from `build_families`): agreement_type, single_or_multiple_award,
  is_multiple_award, cohort_*, effective_decision_date, date_basis/confidence/anomaly,
  latest_task_order_end, saronic_tier.
- **New analyst tables**: `saronic_relevance.csv` (3 seeded OPP-* rows). **Migrations**:
  `ensure_columns` added 5 milestone cols (planned_rfi/solicitation/award_date,
  capture_lead_override_days, milestone_source) to the existing 226-row `recompete_reviews.csv`
  **preserving values**; `reseed_if_seed_only` upgraded the customer_org_map schema in place.

---

## Verification

1. **`workbook/verify_timing.py`** (new; csv+datetime only, no workbook imports) — 19 asserts
   straight from `contract_families.csv` + analyst bridges: hydrated-IDV decision ==
   ordering_period_end; child-later families separated; Birdon/BOA cases; 5 stopped-but-future
   vehicles; 24 cohorts / one Lead each; tier-monotonic sort; priority-score replica;
   confirmed notice fires; blank-potential → "unknown". **ALL 19 PASS.**
2. **`t="e"` / error-literal scan** over `xl/worksheets/sheet*.xml` — 0 error cells, 0
   `#REF!`/`#NAME?`. Cross-sheet formulas spot-checked: INDEX/MATCH into Contract Families
   (`$AK`=effective_decision_date), Market Size (`$Q`=Saronic priority), COUNTIFS over Notice
   Links (`$E`/`$L`) and the Customer Map office join all resolve to the right columns.
3. **Build green** — `aggregate_contracts.py` → `build_workbook.py`, 19 sheets; the
   `len(_COLS)==_NCOLS` / `len(styles)==_NCOLS` guards and `_assert_group_blocks` (one new
   contiguous data tab) all pass.

---

## Critical files

- `research/contracts/scripts/`: `config.py` (date-horizon / ceiling / child-lag / cohort
  windows / capture-lead / tier ranks), `mapping_rules.py` (`saronic_tier`, `agreement_type`
  + PIID position-9), `aggregate_contracts.py` (timing engine, cohorts, tier, seeding +
  migration helpers).
- `workbook/workbook_army/sheets/`: `model_recompete_radar.py` (the Screen — 43 cols),
  `model_recompete_calendar.py` (the Queue — 30 cols), `_radar_formulas.py` (inmkt rewire),
  `data_contract_families.py`, **new** `data_notice_links.py`, `data_customer_map.py`,
  `model_market_size.py` (relevance knobs + composite + `market_size_cols`), `_tabs.py`
  (renames + `TAB_NOTICE_LINKS`), `__init__.py`, `config.py` (capture-lead + tier-rank
  mirror), prose ripple in `summary_overview.py` / `scope_assumptions.py` /
  `data_pipeline_events.py`.
- `workbook/`: **new** `verify_timing.py`.

---

# HANDOFF — what remains

## A. The analyst pass (human; structures wired, values blank/seed today)
- **`analyst/saronic_relevance.csv`** — replace seed mission/platform/autonomy fit (the
  Saronic priority + sort move live). **`analyst/recompete_reviews.csv`** — fill the new
  milestone cols (planned RFI/solicitation/award, capture override) + the existing Window /
  Confidence / Pursuit / program / capability_node / Notes.
- **`analyst/notice_family_links.csv`** — confirm/reject the auto-seeded link + others (only
  `analyst_confirmed="Y"` fires In-market). **`analyst/award_opportunity_attribution.csv`** —
  only 1 family attributed today; attribute more to populate the triage trio.
- **`analyst/customer_org_map.csv`** — fill engagement_status / next_action / relationship
  owner; extend beyond the 13 seeded orgs. **`market_assumptions.csv`** — real % / probs.

## B. Deferred coding (when prioritized)
1. **FPDS Atom → SAM Contract Awards API migration** (still deferred from Phase 1 decision #4;
   FPDS ezSearch decommissioned 2026-02-24). `pull_sam_contract_awards.py` is the foundation.
2. **Different-vendor (competed-away) successors** — generalize `build_lineage_edges` beyond
   same-UEI (same PSC + office + different UEI + gap, lower-confidence tier).
3. **Work-package routes on the opportunity layer** — `work_package_saronic_route` was NOT
   surfaced on Market Size this pass (it is per-work-package grain, N per opportunity; forcing
   it onto the opportunity-grain sheet would break grain integrity). If wanted, give work
   packages their own sheet rather than denormalizing.
4. **Periodic recompete snapshots** — persist dated screen snapshots to show movement.

## C. Invariants to hold (unchanged)
Faithful facts (`workbook/extracted/`, written by `aggregate_contracts.py`) vs analyst
judgment (`workbook/analyst/`, seeded-if-absent / never clobbered, merged blue + rebuild-
durable). Provenance: every rendered cell is a LIVE formula (black/green) or an honest BLUE
input — classified facts (segment, coverage, agreement type, decision date, tier, cohort) are
loaded leaf values, a distinct allowed category. Money discipline (never sum across amount
type; historical obligations ≠ TAM/SAM). Group contiguity (`_assert_group_blocks`). Single
As-of cell re-clocks all timing. `python3` only; verify via Python replica + `t="e"` scan
(LibreOffice can't recalc this book).
