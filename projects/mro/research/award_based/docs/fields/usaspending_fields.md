# USAspending API -- Available Fields Reference

Verified 2026-04-15 against live API responses for NAICS 336611 Navy contracts.

Field names are case-sensitive. The search endpoint uses a mix of Title Case (`"Award ID"`) and
lowercase (`"naics_code"`) -- using the wrong case returns null silently.

---

## 1. Award Search -- `POST /api/v2/search/spending_by_award/`

Paginated search. Returns only requested fields. All dollar amounts are **cumulative lifetime**
obligation, not per-FY. Per-FY amounts require transaction-level decomposition (see section 3).

Used by `data_pull/usa_client.py :: search_awards()`.

### Captured fields (our client requests these)

| API Field Name | Our Key | Type | Example |
|---|---|---|---|
| `Award ID` | `piid` | string | `"N0002424C2301"` |
| `Recipient Name` | `recipient_name` | string | `"NATIONAL STEEL AND SHIPBUILDING COMPANY"` |
| `Award Amount` | `total_obligation` | float | `2501740929.0` (cumulative lifetime) |
| `Total Outlays` | `total_outlays` | float | `null` (often null) |
| `Description` | `description` | string | `"T-AO 214 - 221 DD&C BLOCK BUY"` |
| `Start Date` | `start_date` | date | `"2024-09-09"` (PoP start) |
| `End Date` | `end_date` | date | `"2036-01-17"` (PoP end) |
| `Base Obligation Date` | `date_signed` | date | `"2024-09-13"` (date first obligated) |
| `Award Type` | `award_type` | string | `null` (usually null for contracts) |
| `Contract Award Type` | `contract_award_type` | string | `"DEFINITIVE CONTRACT"` |
| `Awarding Agency` | `awarding_agency` | string | `"Department of Defense"` |
| `Awarding Sub Agency` | `awarding_sub_agency` | string | `"Department of the Navy"` |
| `Awarding Sub Agency Code` | `awarding_sub_agency_code` | string | `"1700"` |
| `Funding Agency` | `funding_agency` | string | `"Department of Defense"` |
| `Funding Sub Agency` | `funding_sub_agency` | string | `"Department of the Navy"` |
| `Funding Sub Agency Code` | `funding_sub_agency_code` | string | `"1700"` |
| `naics_code` | `naics_code` | string | `"336611"` |
| `naics_description` | `naics_description` | string | `"SHIP BUILDING AND REPAIRING"` |
| `psc_code` | `psc_code` | string | `"1915"` |
| `psc_description` | `psc_description` | string | `"CARGO AND TANKER VESSELS"` |
| `generated_internal_id` | `generated_internal_id` | string | `"CONT_AWD_N0002424C2301_9700_-NONE-_-NONE-"` |
| `Last Modified Date` | `last_modified` | datetime | `"2025-12-19 15:21:52"` |
| `Recipient UEI` | `recipient_uei` | string | `"Q85KVUK3JBF5"` |
| `recipient_id` | `recipient_id` | string | `"d3b182df-5daa-..."` (stable hash) |
| `Place of Performance State Code` | `pop_state` | string | `"CA"` |
| `Place of Performance Country Code` | `pop_country` | string | `"USA"` |
| `Place of Performance Zip5` | `pop_zip` | string | `"92113"` |
| `pop_city_name` | `pop_city` | string | `"SAN DIEGO"` |
| `recipient_location_city_name` | `recipient_city` | string | `"SAN DIEGO"` |
| `recipient_location_state_code` | `recipient_state` | string | `"CA"` |
| `recipient_location_address_line1` | `recipient_address` | string | `"2798 HARBOR DR"` |

### Available but not captured (requestable, not needed yet)

| API Field Name | Type | Notes |
|---|---|---|
| `Awarding Agency Code` | string | Top-tier code (`"097"` = DoD) |
| `Funding Agency Code` | string | Same |
| `Recipient DUNS Number` | string | Deprecated, replaced by UEI |
| `Place of Performance City Code` | string | Usually null |
| `pop_state_code` | string | Duplicate of `Place of Performance State Code` |
| `pop_country_name` | string | `"UNITED STATES"` |
| `recipient_location_country_name` | string | `"UNITED STATES"` |
| `recipient_location_address_line2` | string | Usually null |
| `recipient_location_address_line3` | string | Usually null |
| `prime_award_recipient_id` | string | Usually null |
| `def_codes` | list | Disaster/emergency codes (e.g. `["Q"]`) |
| `COVID-19 Obligations` | float | COVID supplemental $ |
| `COVID-19 Outlays` | float | |
| `Infrastructure Obligations` | float | IIJA/BIL $ |
| `Infrastructure Outlays` | float | |

### Fields that exist but always return null from search

These are requestable but only populated on the detail endpoint (`/awards/{id}/`):

- `Recipient Parent Name`, `Recipient Parent UEI`
- `Sub-Award Count`
- `base_and_all_options_value`, `base_exercised_options_val`
- `ordering_period_end_date` (IDV-specific)
- `"NAICS Code"` (Title Case) -- **use `naics_code` (lowercase)**
- `"PSC Code"` (Title Case) -- **use `psc_code` (lowercase)**

### Always-returned bonus fields (not requested, always present)

- `internal_id` (int) -- USAspending internal ID
- `awarding_agency_id` (int) -- agency FK
- `agency_slug` (string) -- URL slug

---

## 2. Award Detail -- `GET /api/v2/awards/{generated_internal_id}/`

Per-award detail. Returns the full record with nested objects. All dollar amounts are
**cumulative lifetime**.

Used by `data_pull/usa_client.py :: get_award_detail()`.

### Top-level fields

| Field | Our Key | Type | Example | Notes |
|---|---|---|---|---|
| `piid` | `piid` | string | `"N0002424C2301"` | |
| `total_obligation` | `total_obligation` | float | `2501740929.0` | Cumulative |
| `base_and_all_options` | `base_and_all_options` | float | `6775705341.0` | **Contract ceiling** |
| `base_exercised_options` | `base_exercised_options` | float | `6775705341.0` | Options exercised |
| `date_signed` | `date_signed` | date | `"2024-09-13"` | Award date |
| `subaward_count` | `subaward_count` | int | `0` / `1622` | |
| `total_subaward_amount` | `total_subaward_amount` | float | `null` / `233668057.54` | |
| `parent_award` | `parent_award_piid` | object | `null` or `{"piid":...}` | Parent IDV |
| `category` | -- | string | `"contract"` | |
| `type` | -- | string | `"D"` | A/B/C/D or IDV_A-E |
| `type_description` | -- | string | `"DEFINITIVE CONTRACT"` | |
| `total_outlay` | -- | float | `null` | |

### `latest_transaction_contract_data` -- classification fields

| API Field | Our Key | Example (T-AO 214) | Example (IWO JIMA SRA) | Example (SSN 792) |
|---|---|---|---|---|
| `product_or_service_code` | `psc_code` | `"1915"` | `"J998"` | `"1905"` |
| `product_or_service_description` | `psc_description` | `"CARGO AND TANKER VESSELS"` | `"NON-NUCLEAR SHIP REPAIR (EAST)"` | `"COMBAT SHIPS AND LANDING VESSELS"` |
| `naics` | `naics_code` | `"336611"` | `"336611"` | `"336611"` |
| `naics_description` | `naics_description` | `"SHIP BUILDING AND REPAIRING"` | `"SHIP BUILDING AND REPAIRING"` | `"SHIP BUILDING AND REPAIRING"` |
| `dod_acquisition_program` | `dod_acquisition_program` | `"000"` | `"000"` | `"516"` |
| `dod_acquisition_program_description` | `dod_acquisition_program_description` | `"NONE"` | `"NONE"` | `"SSN 774"` |
| `dod_claimant_program` | `dod_claimant_code` | `null` | `null` | `"A3"` |
| `dod_claimant_program_description` | `dod_claimant_description` | `null` | `null` | `"SHIPS"` |

### `latest_transaction_contract_data` -- competition and pricing

| API Field | Our Key | Example (T-AO 214) | Example (IWO JIMA SRA) |
|---|---|---|---|
| `type_of_contract_pricing_description` | `type_of_contract_pricing` | `"FIXED PRICE INCENTIVE"` | `"FIRM FIXED PRICE"` |
| `extent_competed_description` | `extent_competed` | `"NOT COMPETED"` | `"FULL AND OPEN COMPETITION"` |
| `number_of_offers_received` | `number_of_offers` | `"1"` | `"3"` |
| `solicitation_identifier` | `solicitation_id` | `"N0002423R2501"` | `"N0002425R4405"` |
| `solicitation_procedures_description` | `solicitation_procedures` | `"ONLY ONE SOURCE"` | `"NEGOTIATED PROPOSAL/QUOTE"` |
| `other_than_full_and_open_description` | `other_than_full_and_open` | `"MOBILIZATION, ESSENTIAL R&D (FAR 6.302-3)"` | `null` |

### `latest_transaction_contract_data` -- ownership and business type

| API Field | Our Key | Example (NASSCO) | Example (BAE Norfolk) |
|---|---|---|---|
| `domestic_or_foreign_entity_description` | `domestic_or_foreign_entity` | `"U.S. OWNED BUSINESS"` | `"FOREIGN-OWNED... IN THE U.S."` |
| `subcontracting_plan_description` | `subcontracting_plan` | `"INDIVIDUAL SUBCONTRACT PLAN"` | `"PLAN NOT REQUIRED"` |
| `small_business_competitive` | `small_business_competitive` | `false` | `false` |

### `latest_transaction_contract_data` -- not captured (low value for this project)

| API Field | Type | Example | Notes |
|---|---|---|---|
| `type_set_aside_description` | string | `"NO SET ASIDE USED."` | All major shipbuilders are large business |
| `evaluated_preference_description` | string | `"NO PREFERENCE USED"` | |
| `commercial_item_acquisition_description` | string | `"COMMERCIAL PROCEDURES NOT USED"` | All defense shipbuilding is non-commercial |
| `multi_year_contract_description` | string | `"NO"` | |
| `consolidated_contract_description` | string | `"NOT CONSOLIDATED"` | |
| `cost_or_pricing_data_description` | string | `"YES"` / `"NO"` | |
| `fed_biz_opps_description` | string | `"YES"` | SAM.gov posting |
| `information_technology_commercial_item_category_description` | string | `"NOT IT PRODUCTS OR SERVICES"` | Always this for ships |
| `sea_transportation_description` | string | `"NO"` | |
| `clinger_cohen_act_planning_description` | string | `"NO"` | IT-related |
| `labor_standards_description` | string | `"NO"` / `"NOT APPLICABLE"` | |
| `construction_wage_rate_description` | string | `"NOT APPLICABLE"` / `"NO"` | Davis-Bacon |
| `materials_supplies_description` | string | `"YES"` | |
| `foreign_funding_description` | string | `"NOT APPLICABLE"` | |
| `interagency_contracting_authority_description` | string | `"NOT APPLICABLE"` | |
| `purchase_card_as_payment_method_description` | string | `"NO"` | |
| `price_evaluation_adjustment` | string | `"0.00"` | |
| `national_interest_action_description` | string | `null` | |
| `major_program` | string | `null` | |
| `program_acronym` | string | `null` | |
| `fair_opportunity_limited_description` | string | `null` | IDV task order field |
| `idv_type_description` | string | `null` | IDV-only |
| `type_of_idc_description` | string | `null` | IDV-only |

### Recipient object

| Path | Our Key | Type | Example |
|---|---|---|---|
| `.recipient_name` | `recipient_name` | string | `"BAE SYSTEMS MARITIME SOLUTIONS NORFOLK INC."` |
| `.recipient_uei` | `recipient_uei` | string | `"ERMDZBE4J8Q9"` |
| `.parent_recipient_name` | `parent_recipient_name` | string | `"BALL CORPORATION"` |
| `.parent_recipient_uei` | `parent_recipient_uei` | string | `"UVUTB62B9AV3"` |
| `.business_categories` | `business_categories` | list | `["Foreign Owned", "Corporate Entity Not Tax Exempt", ...]` |
| `.location.city_name` | `recipient_city` | string | `"NORFOLK"` |
| `.location.state_code` | `recipient_state` | string | `"VA"` |
| `.location.county_name` | `recipient_county` | string | `"NORFOLK (CITY)"` |
| `.location.zip5` | `recipient_zip` | string | `"23523"` |
| `.location.congressional_code` | `recipient_congressional` | string | `"03"` |
| `.location.address_line1` | -- | string | `"750 W BERKLEY AVE"` |
| `.location.state_name` | -- | string | `"VIRGINIA"` |
| `.location.county_code` | -- | string | `"710"` |
| `.location.country_name` | -- | string | `"UNITED STATES"` |
| `.recipient_hash` | -- | string | `"881cc7b1-..."` |

### Place of Performance object

| Path | Our Key | Type | Example |
|---|---|---|---|
| `.city_name` | `pop_city` | string | `"NORFOLK"` |
| `.state_code` | `pop_state` | string | `"VA"` |
| `.county_name` | `pop_county` | string | `"NORFOLK CITY"` |
| `.zip5` | `pop_zip` | string | `"23523"` |
| `.congressional_code` | `pop_congressional` | string | `"03"` |
| `.state_name` | -- | string | `"VIRGINIA"` |
| `.county_code` | -- | string | `"710"` |
| `.country_name` | -- | string | `"UNITED STATES"` |

### PSC Hierarchy object

| Path | Our Key | Example (construction) | Example (maintenance) |
|---|---|---|---|
| `.toptier_code.code` | -- | _(empty)_ | `"J"` |
| `.toptier_code.description` | -- | _(empty)_ | `"MAINT, REPAIR, REBUILD EQUIPMENT"` |
| `.midtier_code.code` | `psc_midtier_code` | `"19"` | `"J9"` |
| `.midtier_code.description` | `psc_midtier_description` | `"SHIPS, SMALL CRAFT, PONTOON, DOCKS"` | `"NON-NUCLEAR SHIP REPAIR"` |
| `.base_code.code` | -- | `"1915"` | `"J998"` |
| `.base_code.description` | -- | `"CARGO AND TANKER VESSELS"` | `"NON-NUCLEAR SHIP REPAIR (EAST)"` |

Note: toptier is empty for product PSCs (19xx) but populated for service PSCs (Jxxx). The midtier
is always populated and is the best level for newbuild-vs-MRO classification.

### NAICS Hierarchy object

| Path | Example |
|---|---|
| `.toptier_code` | `{"code": "33", "description": "Manufacturing"}` |
| `.midtier_code` | `{"code": "3366", "description": "Ship and Boat Building"}` |
| `.base_code` | `{"code": "336611", "description": "Ship Building and Repairing"}` |

### Executive Details (not captured)

Top 5 compensated officers -- names and amounts. Available for large primes. Not useful for
market sizing.

### Period of Performance

| Path | Type | Example |
|---|---|---|
| `.start_date` | date | `"2024-09-09"` |
| `.end_date` | date | `"2036-01-17"` |
| `.last_modified_date` | date | `"2025-12-19"` |
| `.potential_end_date` | datetime | `"2036-01-17 00:00:00"` |

---

## 3. Transactions -- `POST /api/v2/transactions/`

Per-modification transaction data for one award. This is the endpoint that enables **FY-specific
obligation decomposition**: sum `federal_action_obligation` on transactions where `action_date`
falls within the target FY window (e.g. 2025-10-01 to 2026-09-30 for FY2026).

The `total_obligation` on the award is cumulative lifetime. The only way to get per-FY spending
is to pull all transactions and sum within the FY date range. This is what
`data_pull/enrich_fy_obligations.py` does.

Used by `data_pull/usa_client.py :: get_transactions()`.

| Field | Our Key | Type | Example | Captured |
|---|---|---|---|---|
| `modification_number` | `modification_number` | string | `"P00005"` | Yes |
| `action_date` | `action_date` | date | `"2025-12-19"` | Yes |
| `federal_action_obligation` | `federal_action_obligation` | float | `62356.0` | Yes |
| `description` | `description` | string | `"T-AO 214-221 DD&C..."` | Yes |
| `action_type` | `action_type` | string | `"L"` | Yes |
| `action_type_description` | `action_type_description` | string | `"DEFINITIZE CHANGE ORDER"` | Yes |
| `id` | -- | string | `"CONT_TX_9700_-NONE-_N0002424C2301_P00005..."` | No |
| `type` | -- | string | `"D"` | No |
| `type_description` | -- | string | `"DEFINITIVE CONTRACT"` | No |
| `face_value_loan_guarantee` | -- | float | `0.0` | No (irrelevant) |
| `original_loan_subsidy_cost` | -- | float | `0.0` | No (irrelevant) |

This endpoint is fully exploited. All useful fields are captured.

---

## 4. Subawards -- `POST /api/v2/subawards/`

First-tier subaward data for one award.

Used by `data_pull/usa_client.py :: get_subawards()`.

| Field | Our Key | Type | Example | Captured |
|---|---|---|---|---|
| `subaward_number` | `subaward_number` | string | `"SNE224=032"` | Yes |
| `amount` | `amount` | float | `49865.0` | Yes |
| `recipient_name` | `recipient_name` | string | `"NORTHROP GRUMMAN SYSTEMS CORPORATION"` | Yes |
| `description` | `description` | string | `"MECHANICAL"` | Yes |
| `action_date` | `action_date` | date | `"2018-11-19"` | Yes |
| `id` | -- | int | `204061` | No |

This endpoint is fully exploited.

---

## Field Name Bugs Found (2026-04-15)

Three field name bugs caused null values in pulled data:

1. **Search endpoint**: `"NAICS Code"` (Title Case) returns null. Correct: `"naics_code"` (lowercase).
2. **Search endpoint**: `"PSC Code"` (Title Case) returns null. Correct: `"psc_code"` (lowercase).
3. **Detail endpoint**: `contract.get("dod_claimant_program_code")` returns null. Correct field name: `"dod_claimant_program"`.

All three fixed in `usa_client.py` on 2026-04-15.
