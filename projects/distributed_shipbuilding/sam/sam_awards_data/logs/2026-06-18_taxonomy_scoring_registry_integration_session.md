# 2026-06-18 — Taxonomy HII-scoring + registry integration: session log

Continues `logs/2026-06-18_taxonomy_and_vendor_registry_agent_handoff.md`. This session brought the
two external agents' deliverables in, validated the taxonomy against the HII-DDG referee, settled the
classification axes, and built the consolidated vendor-classification workbook (now an expandable
registry). Written to be read cold. Next steps live in `projects/research_shared/REMAINING_TASKS.md`;
the methodology is in `projects/research_shared/CLASSIFICATION_METHODOLOGY.md`.

---

## 1. Deliverables received & filed (both agents returned)

- **Agent A — work-type taxonomy** → `projects/research_shared/taxonomy_design_output/`
  (`navy_supplier_work_type_schema.xlsx` [7 sheets], `navy_all_observed_naics_crosswalk.csv` [506 codes],
  `navy_work_type_schema.csv`, `navy_supplier_classification_schema.md`). **18 process categories + 99
  Unresolved**, one mutually-exclusive label per UEI; lands on the canonical base exactly (1,203 UEIs,
  $13,110.75M; 429 no-primary-NAICS / 12.5%; review pool 571 / 26%).
- **Agent B — vendor registry** → `projects/research_shared/vendor_registry_output/`
  (`navy_shipbuilding_vendor_registry_top50.xlsx`, 4 sheets). Top-50 by $ = **71.1%** of $, hand-verified
  operating-entity facts + `supplier_type` + `typical_deliverable` + NAICS assessment + sources. 44
  high-confidence, 13 foreign-owned, 18/50 file-NAICS flagged misleading.

## 2. Decisions settled this session

- **Three orthogonal axes**, one label each per UEI:
  - `work_type` (18 + 99, process axis) — agent A.
  - `delivered_output_class` — **5-class MA / CE "Discrete component / equipment" / MT / SV / UN**.
    EQ vs CP **deliberately merged** into CE (boundary too low-confidence to defend; collapsing is
    reversible and aligns 1:1 with the registry's `typical_deliverable`). Verified the registry's
    `typical_deliverable` and the agent's later `deliverable_category` agree on all 50 (wording only).
  - `scope_status` — **4-class** (core / enabling / probable_leakage / uncertain), **designed, not yet
    applied**. Quarantine-and-report (don't purge the corpus for the ~$22M workforce / ~$71M consulting
    residuals).
- **Two curated work-type sign-offs** (top-50): **BWXT Nuclear Operations 04→02** (naval nuclear
  propulsion plant; OEM, kept distinct from PCC the fabricator in 05) and **Northrop Grumman #1 = 01
  affirmed** (turbine-*generator* = electrical power generation). Effect: 02 $941.5M→$1,231.4M,
  04 $1,197.0M→$907.2M. Recorded in `audit_log.md` §5.

## 3. HII-DDG validation (the §6 referee task)

Built `projects/research_shared/taxonomy_hii_scoring/score_taxonomy_vs_hii.py` (+ `FINDINGS.md`,
`naics6_hii_purity.csv`, `category_hii_agreement.csv`, `low_purity_flags.csv`). Method: join each HII
subaward's observed SWBS ship-system to the vendor's NAICS→category; measure per-category SWBS agreement
and per-NAICS purity. Key results:

- **0% join gap**; 70.6% of HII $ resolve to a real category by NAICS, 24.9% no-primary (concentrated in
  registry-covered vendors — Rolls-Royce, York, SOCAIL), 4.5% weak→99.
- **Clean where observable:** 01 Electrical 1.00, 02 Propulsion 0.99, 03 Fluid 0.91; 04 Thermal 0.67
  (genuine thermal/fluid boundary). Weighted ≈ 0.91.
- **Excused as data artifacts (not taxonomy faults):** 05 Structural (hull built in-house by Ingalls) and
  10 Sensors (combat/C4ISR is GFE, excluded upstream). Process-only cats graded by component text — 06
  forgings/castings 0.96 corroborates the no-SWBS-home category.
- **Low-purity flag list** doubled as the enrichment queue; biggest was 336611 (scattered) → confirms the
  taxonomy's decision to treat it as a review trigger, not auto-shipyard.

## 4. Consolidated workbook + registry expansion

- Built `vendor_registry_output/top50_vendor_classifications.xlsx` via
  `build_classifications_workbook.py` (plain openpyxl, not the pipeline). Sheets:
  **Classifications** (work_type + delivered_output_class merged) and **Vendor Context** (curated registry
  facts — identity, program $, verified owners, NAICS assessment, full Source URLs; junk dropped). All
  source formatting stripped to a single plain style.
- **Flagged-vendor deep dive** (the 5 uncovered NAICS-flag vendors) returned and was integrated:
  Parker-Hannifin, Alfa Laval, AAE/Trident-Canada, Young Engineering, INDEECO
  (`flagged_vendor_research_top5.md` + `vendor_registry_additions.csv`). **Parker 333310→03** and
  **AAE 332420→03** flipped (engineered naval fluid subsystems behind generic codes), validating the flag
  mechanism; the other 3 confirmed their NAICS default. Added to the workbook at **true global $-ranks**
  (52, 87, 108, 138, 149 — sparse beyond 50; gaps are unresearched vendors). Workbook now **55 vendors**;
  builder appends future additions from `vendor_registry_additions.csv` with no code changes.

## 5. Artifacts produced this session (all under `projects/research_shared/`)

- `taxonomy_hii_scoring/` — scoring harness, 3 CSVs, `FINDINGS.md`.
- `vendor_registry_output/top50_vendor_classifications.xlsx`, `build_classifications_workbook.py`,
  `vendor_registry_additions.csv`, `flagged_vendor_research_top5.md`.
- `audit_log.md` — HII validation write-up (plain-speak + numbers + method) and §5 curated sign-offs.
- `CLASSIFICATION_METHODOLOGY.md` — the settled methodology.
- `REMAINING_TASKS.md` — the roadmap for finishing.
- Memory updated: `[[subaward-classification-vocab]]` now carries the 3-axis decisions.

## 6. Where things stand / next

Taxonomy is validated; registry covers 71%+ and is now expandable; top-50+5 carry work_type +
delivered_output_class. **Not yet done:** close the flag-queue audit entry (§A), apply `scope_status`
(§B), build the **full 1,203-UEI × 3-axis applied table** joined to `all_subawards.csv` and tied to
$13.1B (§C), continue registry expansion (§D), then reconcile + publish the work_type × deliverable ×
program matrices (§E). Critical path B + F → C → E. Details + open decisions in `REMAINING_TASKS.md`.
