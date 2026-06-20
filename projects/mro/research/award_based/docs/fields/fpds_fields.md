# FPDS Atom Feed -- Available Fields Reference

Verified 2026-04-15 against live FPDS responses for three Navy contracts:
- N0002424C2301 (T-AO 214, NASSCO, newbuild)
- N0002426C4405 (USS Iwo Jima SRA, BAE Norfolk, MRO)
- N0002412C2115 (SSN 792 LLTM, Electric Boat, newbuild material)

Endpoint: `GET https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC&q=...`

Returns XML (Atom Feed), 10 entries per page. Per-modification records, not per-award.
Query by PIID + MODIFICATION_NUMBER to get a specific mod.

---

## Fields Only Available from FPDS

These fields are **not exposed** by the USAspending API. The only way to get them is FPDS.

### Contract structure

| XML Path | Our Key | Type | Example (T-AO 214) | Example (IWO JIMA) | Example (SSN 792) |
|---|---|---|---|---|---|
| `contractData/GFE-GFP` | `gfe_gfp` | code | `Y` | `Y` | `N` |
| `contractData/GFE-GFP @description` | `gfe_gfp_description` | string | `"Transaction uses GFE/GFP"` | `"Transaction uses GFE/GFP"` | `"Transaction does not use GFE/GFP"` |
| `contractData/undefinitizedAction` | `undefinitized_action` | code | `X` (NO) | `X` (NO) | `B` (OTHER UCA) |
| `contractData/contractFinancing` | `contract_financing` | code | `A` | `A` | `Z` |
| `contractData/contractFinancing @description` | `contract_financing_description` | string | `"FAR 52.232-16 PROGRESS PAYMENTS"` | `"FAR 52.232-16 PROGRESS PAYMENTS"` | `"NOT APPLICABLE"` |
| `contractData/costAccountingStandardsClause` | `cost_accounting_standards` | code | `Y` | `Y` | `Y` |

- **GFE-GFP** (Government Furnished Equipment/Property): Identifies contracts where the government
  provides equipment (engines, combat systems, etc.) for the contractor to integrate. Directly
  relevant to identifying module vs. integration work.
- **undefinitizedAction**: Whether the contract is a UCA. Common in shipbuilding for long-lead
  material contracts. SSN 792 LLTM was undefinitized ("B").
- **contractFinancing**: "A" = progress payments (standard for large shipbuilding), "Z" = N/A.

### Manufacturing and origin

| XML Path | Our Key | Type | Example (T-AO 214) | Example (IWO JIMA) | Example (SSN 792) |
|---|---|---|---|---|---|
| `productOrServiceCode @productOrServiceType` | `product_or_service_type` | string | `PRODUCT` | `SERVICE` | `PRODUCT` |
| `placeOfManufacture` | `place_of_manufacture` | code | `D` (MFG IN U.S.) | `C` (NOT MANUFACTURED) | `D` (MFG IN U.S.) |
| `countryOfOrigin` | `country_of_origin` | code | `USA` | `USA` | `USA` |

- **productOrServiceType**: Attribute on the PSC code element. "PRODUCT" for construction PSCs
  (19xx), "SERVICE" for maintenance PSCs (Jxxx). Clean binary newbuild/MRO signal.
- **placeOfManufacture**: "D" = manufactured in U.S., "C" = not a manufactured end product
  (service contracts).

### Vendor identity

| XML Path | Our Key | Type | Example (NASSCO) | Example (BAE Norfolk) | Example (EB) |
|---|---|---|---|---|---|
| `ultimateParentUEI` | `ultimate_parent_uei` | string | `Q85KVUK3JBF5` | `UVUTB62B9AV3` | `VF58HFRNGEL8` |
| `ultimateParentUEIName` | `ultimate_parent_name` | string | `GENERAL DYNAMICS CORPORATION` | `BAE SYSTEMS NORFOLK SHIP REPAIR INC.` | `GENERAL DYNAMICS CORPORATION` |
| `cageCode` | `cage_code` | string | `81220` | `07243` | _(in full record)_ |
| `stateOfIncorporation` | `state_of_incorporation` | code | `NV` | `VA` | _(in full record)_ |
| `countryOfIncorporation` | `country_of_incorporation` | code | `USA` | `USA` | _(in full record)_ |

Note on parent company data: USAspending's `parent_recipient_name` can disagree with FPDS's
`ultimateParentUEIName`. For example, NASSCO appears as its own parent in USAspending but as
General Dynamics Corporation in FPDS. The FPDS value traces the corporate ownership chain
through SAM.gov registration data. Both sources reflect different update cadences and data
pipelines, so neither is guaranteed to be current.

### Traceability

| XML Path | Our Key | Type | Example |
|---|---|---|---|
| `transactionInformation/createdBy` | `contracting_officer` | string | `CHRISTIANA.CASEY.N00024@NAVY.MIL` |
| `transactionInformation/approvedBy` | `approving_officer` | string | `JAMIE.OPPENHEIMER.N00024@NAVY.MIL` |
| `treasuryAccountSymbol/agencyIdentifier` | `treasury_agency_id` | string | `17` |
| `treasuryAccountSymbol/mainAccountCode` | `treasury_main_account` | string | `1611` |

- Treasury account codes link contracts to specific appropriation accounts (e.g., 17-1611 = Navy
  Shipbuilding and Conversion).

---

## Fields Duplicated in USAspending

These fields are available from both FPDS and USAspending. USAspending is the better source
(JSON, paginated, aggregated per-award). Listed here for completeness.

### Award identification

| XML Path | USAspending equivalent |
|---|---|
| `awardContractID/PIID` | `piid` |
| `awardContractID/modNumber` | transaction `modification_number` |
| `awardContractID/agencyID` | `awarding_sub_agency_code` |
| `referencedIDVID/PIID` | `parent_award_piid` (from detail) |

### Dollar values

| XML Path | USAspending equivalent | Notes |
|---|---|---|
| `obligatedAmount` | `federal_action_obligation` (per-transaction) | Per-mod amount |
| `totalObligatedAmount` | `total_obligation` | Cumulative |
| `baseAndAllOptionsValue` | `base_and_all_options` (from detail) | Per-mod ceiling |
| `totalBaseAndAllOptionsValue` | `base_and_all_options` (from detail) | Cumulative ceiling |

### Dates

| XML Path | USAspending equivalent |
|---|---|
| `signedDate` | `date_signed` |
| `effectiveDate` | `start_date` |
| `currentCompletionDate` | `end_date` |
| `ultimateCompletionDate` | `end_date` (USAspending uses current, not ultimate) |

### Classification

| XML Path | USAspending equivalent |
|---|---|
| `productOrServiceCode` | `psc_code` |
| `principalNAICSCode` | `naics_code` |
| `claimantProgramCode` | `dod_claimant_code` (from detail) |
| `systemEquipmentCode` | `dod_acquisition_program` (from detail) |
| `typeOfContractPricing` | `type_of_contract_pricing` (from detail) |
| `extentCompeted` | `extent_competed` (from detail) |
| `numberOfOffersReceived` | `number_of_offers` (from detail) |
| `solicitationID` | `solicitation_id` (from detail) |
| `reasonNotCompeted` | `other_than_full_and_open` (from detail) |
| `subcontractPlan` | `subcontracting_plan` (from detail) |

### Vendor and location

| XML Path | USAspending equivalent |
|---|---|
| `vendorName` | `recipient_name` |
| `vendorUEIInformation/UEI` | `recipient_uei` |
| `vendorLocation/city` | `recipient_city` |
| `vendorLocation/state` | `recipient_state` |
| `vendorLocation/congressionalDistrictCode` | `recipient_congressional` (from detail) |
| `principalPlaceOfPerformance/stateCode` | `pop_state` |
| `placeOfPerformanceZIPCode` | `pop_zip` |
| `placeOfPerformanceCongressionalDistrict` | `pop_congressional` (from detail) |

---

## Full XML Structure Reference

Top-level sections in an FPDS `<award>` element:

```
award
  awardID/awardContractID      -- PIID, mod number, agency
  relevantContractDates        -- signed, effective, completion dates
  dollarValues                 -- per-mod obligation, base+options
  totalDollarValues            -- cumulative versions of above
  purchaserInformation         -- contracting/funding agency and office
  contractMarketingData        -- fee paid (usually 0)
  contractData                 -- action type, pricing, GFE, financing, UCA, description
  legislativeMandates          -- ClingerCohen, labor standards, wage rates
  productOrServiceInformation  -- PSC, NAICS, claimant, DAP, bundling, manufacture
  vendor                       -- name, socioeconomic flags, business types, location, UEI, CAGE
  placeOfPerformance           -- state, ZIP, congressional district
  competition                  -- competed, set-aside, offers, solicitation procedures
  preferencePrograms           -- subcontract plan
  transactionInformation       -- contracting officer, created/modified dates, status
  genericTags                  -- internal FPDS fields
```

### Low-value fields (available but not extracted)

- **Socioeconomic flags** (~30 boolean fields): isSmallBusiness, isVeteranOwned, isWomenOwned,
  minority subcategories, etc. All false for major shipbuilders.
- **Business type booleans**: federalGovernment, stateGovernment, localGovernment subtypes,
  tribalGovernment, foreignGovernment. All false for defense contractors.
- **Education entity flags**: land grant colleges, HBCUs, etc. Not applicable.
- **Vendor certifications**: DOT disadvantaged, SBA 8(a), HUBZone. Not applicable for primes.
- **Regulatory compliance**: recoveredMaterialClauses, useOfEPADesignatedProducts,
  informationTechnologyCommercialItemCategory. Low analytical value.
- **CCR registration**: registrationDate, renewalDate. SAM.gov admin data.
- **Vendor contact**: phoneNo, faxNo. Not useful for market sizing.
- **genericTags**: Internal FPDS strings/booleans with no documented meaning.
