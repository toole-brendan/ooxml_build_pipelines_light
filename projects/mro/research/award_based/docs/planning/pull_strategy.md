# Pull Strategy and Field Reference

Consolidated recommendation for USAspending + FPDS data pulls. Based on field availability
analysis across all API endpoints, verified 2026-04-15.

---

## Pipeline (5 steps, in order)

```
Step 1: USAspending search    -- discover awards by NAICS/PSC + agency + FY
Step 2: FY decomposition       -- transactions -> per-FY obligation (not cumulative)
Step 3: USAspending detail     -- contract ceiling, PSC, DAP, subaward counts, competition
Step 4: FPDS enrichment        -- GFE/GFP, true parent company, CAGE, UCA status
Step 5: Subaward pull          -- first-tier subs for awards where subaward_count > 0
```

Steps 3 and 4 only run on awards that survive step 2 (positive FY obligation). Step 5 is
selective -- only awards with reported subawards.

---

## What to Pull

### Phase 1 collections (already defined in `pull_usaspending.py`)

| Collection | Filter | Agency | Notes |
|---|---|---|---|
| `shipbuilding` | NAICS 336611 | Navy subtier | Backbone. Newbuild + repair in one NAICS |
| `combat_electronics` | NAICS 334511 | Navy subtier | All combat system electronics |
| `ship_repair` | PSC J998/J999 | DoD toptier | Clean MRO depot -- catches J998 coded to non-336611 NAICS |
| `combat_vessels` | PSC 1901/1904/1905 | DoD toptier | Newbuild vessel primes -- richest subaward data |

### Add Coast Guard

The existing collections only filter for Navy. Need a parallel set for Coast Guard:

| Collection | Filter | Agency |
|---|---|---|
| `cg_shipbuilding` | NAICS 336611 | Coast Guard (DHS subtier) |

### FY range

FY22 through FY27. Pull the full window in one search, then decompose per-FY in step 2.

### Phase 2 (system-specific manufacturing)

Wait until Phase 1 is fully enriched and analyzed. The Tier 2/3 NAICS codes
(see `docs/data_pulling_instructions/naics_pull_strategy.md`) are smaller dollar values
and you'll know better where the gaps are after seeing Phase 1.

---

## Consolidated Field List

After all 5 steps, each award carries these fields. Organized by analytical use, not endpoint.

### Identity (from search)

| Field | Example | Source |
|---|---|---|
| `piid` | `N0002424C2301` | search |
| `generated_internal_id` | `CONT_AWD_N0002424C2301_9700_-NONE-_-NONE-` | search |
| `description` | `T-AO 214 - 221 DD&C BLOCK BUY` | search |
| `contract_award_type` | `DEFINITIVE CONTRACT` | search |

### Dollars (search + FY decomp + detail)

| Field | Example | Source | Notes |
|---|---|---|---|
| `total_obligation` | `2,501,740,929` | search | Cumulative lifetime |
| `base_and_all_options` | `6,775,705,341` | detail | Contract ceiling |
| `base_exercised_options` | `6,775,705,341` | detail | Options exercised |
| `fy2026_obligation` | `1,715,665,950` | transactions | **FY-specific spending** |
| `fy2026_actions` | `7` | transactions | Mods in FY window |
| `total_transactions` | `21` | transactions | All mods ever |
| `total_outlays` | `null` | search | Often null |

### Classification (search + detail + FPDS)

| Field | Example | Source | Notes |
|---|---|---|---|
| `psc_code` | `1915` | search | Newbuild vs MRO |
| `psc_description` | `CARGO AND TANKER VESSELS` | search | |
| `psc_midtier_code` | `19` | detail | PSC group |
| `psc_midtier_description` | `SHIPS, SMALL CRAFT, PONTOON, DOCKS` | detail | |
| `naics_code` | `336611` | search | |
| `naics_description` | `SHIP BUILDING AND REPAIRING` | search | |
| `product_or_service_type` | `PRODUCT` | FPDS | PRODUCT vs SERVICE |
| `gfe_gfp` | `Y` | FPDS | Module/integration signal |
| `gfe_gfp_description` | `Transaction uses GFE/GFP` | FPDS | |
| `dod_acquisition_program` | `000` | detail | DAP code |
| `dod_acquisition_program_description` | `NONE` | detail | |
| `dod_claimant_code` | `A3` | detail | |
| `dod_claimant_description` | `SHIPS` | detail | |

### Contract terms (detail + FPDS)

| Field | Example | Source |
|---|---|---|
| `type_of_contract_pricing` | `FIXED PRICE INCENTIVE` | detail |
| `extent_competed` | `NOT COMPETED` | detail |
| `number_of_offers` | `1` | detail |
| `solicitation_id` | `N0002423R2501` | detail |
| `solicitation_procedures` | `ONLY ONE SOURCE` | detail |
| `other_than_full_and_open` | `MOBILIZATION, ESSENTIAL R&D (FAR 6.302-3)` | detail |
| `undefinitized_action` | `X` | FPDS |
| `undefinitized_action_description` | `NO` | FPDS |
| `contract_financing` | `A` | FPDS |
| `contract_financing_description` | `FAR 52.232-16 PROGRESS PAYMENTS` | FPDS |
| `cost_accounting_standards` | `Y` | FPDS |
| `cost_accounting_standards_description` | `YES - CAS CLAUSE INCLUDED` | FPDS |
| `subcontracting_plan` | `INDIVIDUAL SUBCONTRACT PLAN` | detail |
| `small_business_competitive` | `false` | detail |

### Contractor identity (search + detail + FPDS)

| Field | Example | Source | Notes |
|---|---|---|---|
| `recipient_name` | `NATIONAL STEEL AND SHIPBUILDING COMPANY` | search | |
| `recipient_uei` | `Q85KVUK3JBF5` | search | |
| `recipient_id` | `d3b182df-...` | search | Stable hash |
| `parent_recipient_name` | `NATIONAL STEEL AND SHIPBUILDING COMPANY` | detail | Can be wrong |
| `ultimate_parent_name` | `GENERAL DYNAMICS CORPORATION` | FPDS | More accurate |
| `ultimate_parent_uei` | `Q85KVUK3JBF5` | FPDS | |
| `cage_code` | `81220` | FPDS | |
| `domestic_or_foreign_entity` | `U.S. OWNED BUSINESS` | detail | |
| `business_categories` | `["Corporate Entity Not Tax Exempt", ...]` | detail | |
| `state_of_incorporation` | `NV` | FPDS | |
| `country_of_incorporation` | `USA` | FPDS | |

### Geography (search + detail)

| Field | Source | Notes |
|---|---|---|
| `pop_state` / `pop_city` / `pop_zip` | search | Place of performance |
| `pop_county` / `pop_congressional` | detail | |
| `pop_country` | search | |
| `recipient_state` / `recipient_city` / `recipient_address` | search | Contractor location |
| `recipient_zip` / `recipient_county` / `recipient_congressional` | detail | |

### Dates and admin (search)

| Field | Example | Notes |
|---|---|---|
| `start_date` | `2024-09-09` | Period of performance start |
| `end_date` | `2036-01-17` | Period of performance end |
| `date_signed` | `2024-09-13` | Award date |
| `last_modified` | `2025-12-19` | |

### Agency (search + detail + FPDS)

| Field | Source |
|---|---|
| `awarding_agency` / `awarding_sub_agency` / `awarding_sub_agency_code` | search |
| `funding_agency` / `funding_sub_agency` / `funding_sub_agency_code` | search |
| `contracting_office` / `funding_office` | detail |
| `contracting_officer` / `approving_officer` | FPDS |

### Subaward summary (detail)

| Field | Example | Notes |
|---|---|---|
| `subaward_count` | `0` or `1622` | Number of reported subs |
| `total_subaward_amount` | `null` or `233,668,057` | Reported sub $ total |
| `parent_award_piid` | `null` | Parent IDV if any |

### Subawards (separate records, step 5)

| Field | Example |
|---|---|
| `subaward_number` | `4500656117` |
| `amount` | `196,841,514` |
| `recipient_name` | `NORTHROP GRUMMAN SYSTEMS CORPORATION` |
| `description` | `PO ITEM NO. 1 - CVN81 ADVANCE PROCUREMENT MATERIAL - MTG` |
| `action_date` | `2021-07-23` |

### FPDS traceability (FPDS)

| Field | Example | Notes |
|---|---|---|
| `place_of_manufacture` | `D` | MFG IN U.S. |
| `place_of_manufacture_description` | `MFG IN U.S.` | |
| `country_of_origin` | `USA` | |
| `treasury_agency_id` | `17` | Links to appropriation |
| `treasury_main_account` | `1611` | 17-1611 = SCN |

---

## Fields Not Worth Capturing

| Field / Category | Why excluded |
|---|---|
| Transaction `id`, subaward `id` | Internal USAspending PKs, no analytical use |
| FPDS socioeconomic booleans (~30 fields) | All false for major shipbuilders. `business_categories` from detail already captures this as a flat list |
| FPDS regulatory fields | recoveredMaterialClauses, useOfEPADesignatedProducts, etc. |
| COVID/Infrastructure obligations | Null for defense shipbuilding |
| `Recipient DUNS Number` | Deprecated, replaced by UEI |
| `award_type` | Always null for contracts, redundant with `contract_award_type` |
| FPDS vendor phone/fax | Not useful for market sizing |
| FPDS genericTags | Internal FPDS fields with no documented meaning |
| FPDS CCR registration/renewal dates | SAM.gov admin data |

---

## Practical Sequencing

Start with the pull that's already done (shipbuilding FY2026) and enrich it fully through
all 5 steps. That gives a complete FY2026 picture for NAICS 336611 Navy. Then expand.

### Immediate (tools are built)

1. Enrich `shipbuilding_fy2026_positive.json` with USAspending detail (`pull_usaspending.py` `--enrich` or standalone)
2. Enrich with FPDS (`enrich_fpds.py`)
3. Pull subawards for awards with `subaward_count > 0`

### Next

4. Pull remaining Phase 1 collections (combat_electronics, ship_repair, combat_vessels, CG)
5. Run FY decomposition for FY22-FY25 on all collections
6. Run detail + FPDS enrichment on each FY-positive set

### After Phase 1 analysis

7. Evaluate Phase 2 NAICS codes based on coverage gaps identified in Phase 1
8. Consider whether engineering services (541330) is in scope

---

## Subaward Data Quality by Prime

Subaward reporting varies dramatically by shipbuilder. This affects what's achievable
for subprime landscape analysis.

| Prime | Example contract | Subaward count | Reported $ | Data quality |
|---|---|---|---|---|
| HII (Newport News) | CVN 80 ($11.9B) | many pages | $1B+ (with duplicates) | Equipment-level descriptions |
| Electric Boat | SSN 792 ($19.9B) | 1,622 | $234M | Component names (terse) |
| BIW | DDG FY18-22 ($5.3B) | 24 | $53M | Sparse, some equipment |
| BIW | DDG FY13-17 ($4.9B) | 93 | $6.7M | Mostly "vendor service", tiny $ |
| NASSCO | T-AO 214 ($2.5B) | 0 | -- | No subaward reporting yet (new) |

**Key caveat:** Subaward records must be deduplicated by `subaward_number` before aggregating.
The same PO is re-reported on every prime modification that references it.

**FY filtering:** Subawards have `action_date` (when the PO was issued) and `amount` (total
PO value). There is no per-FY decomposition -- you get "subawards issued during the FY" not
"subaward spending in the FY."
