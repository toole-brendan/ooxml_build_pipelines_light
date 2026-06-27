# Data-Field Reference: Prime Awards & Subawards — Slide 04 (two-routes set)

**Reference / appendix slide.** Two enumerations of the fields that come back from the free
federal awards APIs — one for **prime awards**, one for **subawards** — each presented twice:
a curated **most-important** set (the fields that change the answer) and the **complete**
field list (every field present in the raw pulls). It is the data backing behind slides 01–03:
the prime route reads the prime-award fields; the subcontractor route reads the subaward fields.

Field lists below are the **union across all raw pull files in this repo** of each source
(verified with `jq`/Python over the saved JSON, not from documentation). Dot notation shows
nesting (`awardDetails.dates.lastDateToOrder`); `[]` marks a list; most SAM coded values arrive
as `{code, name}` pairs.

---

## Orientation — which source feeds which list

| List | Primary source(s) | Why |
|---|---|---|
| **Prime awards** | **SAM.gov Contract Awards** (complete prime feed, **the only one that includes OTs**); **USAspending** (discovery + per-mod dollars + appropriation); **FPDS** (legacy native schema) | A prime award is read for *classification, competition/access, money, timing, scope, appropriation*. |
| **Subawards** | **SAM.gov Subaward Reporting** (FFATA first-tier, the rich schema); **USAspending /subawards** (thin, 6 fields) | A subaward is read for *who supplies whom, how much, when reported, under which prime*. |

The two lists are not symmetric: the prime schema is deep (hundreds of fields across three
sources); the subaward schema is shallow (one rich FFATA record). **No single layer is the
market** — prime feeds omit OTs unless SAM Contract Awards is used; subaward reporting is
first-tier only and lags 6–18 months.

---

# (A) PRIME AWARDS

## A0 — Most important prime fields (the fields that change the answer)

**Identity & linkage**
- `piid` — contract / order number (normalize UPPERCASE, no dashes for SAM APIs).
- `contractId.referencedIDVPiid` — **parent IDV** — the unit for recompete and concentration.
- `contractId.modificationNumber` — per-action identity.
- `awardeeData…uniqueEntityId` (**UEI**) + `awardeeUltimateParentUniqueEntityId` — the reliable
  vendor key and its corporate parent (a company has **multiple UEIs** — query each).
- `generated_internal_id` (USAspending) — the handle for every detail call.

**Classification — decides the route (slide 01)**
- `coreData.awardOrIDVType` — award vs. IDV vs. Delivery Order vs. FSS vs. **Other Transaction
  Agreement** *(the only field that surfaces OTs — absent from USAspending/FPDS)*.
- `acquisitionData.multipleOrSingleAwardIdc` — **single- vs. multiple-award** (prime-as-holder
  vs. open).
- `acquisitionData.typeOfIdc` — IDV subtype (IDIQ / BPA / BOA / FSS).
- `acquisitionData.typeOfContractPricing` — FFP / cost-reimbursement / T&M (payment risk).

**Competition / access — the route selector**
- `competitionInformation.extentCompeted` — full-and-open vs. not competed.
- `fair_opportunity_limited` (USAspending) — holders-only order route (FAR 16.505).
- `competitionInformation.typeOfSetAside` — set-aside program eligibility.
- `numberOfOffersReceived` — competitive intensity (**999 = "not meaningful" sentinel**).
- `coreData.solicitationId` — bridge to the pre-award notice.

**Money — sum only the right one (§ money hygiene)**
- `awardDetails.dollars.actionObligation` — **per-mod obligation — the only field you sum.**
- `awardDetails.totalContractDollars.totalActionObligation` — cumulative-to-date (**never sum**).
- `awardDetails.totalContractDollars.totalBaseAndAllOptionsValue` — **ceiling = capacity, not
  spend** (shared across holders on a multiple-award IDV).

**Timing**
- `awardDetails.dates.dateSigned`; `periodOfPerformanceStartDate`; `currentCompletionDate`;
  `ultimateCompletionDate`.
- `awardDetails.dates.lastDateToOrder` — **IDV ordering-period end** — the recompete indicator.

**Scope, organization, appropriation**
- `productOrService` (**PSC**) + `principalNaics` — what is being bought (tier the market here);
  `descriptionOfContractRequirement` — free-text scope.
- `…contractingOffice` (sub-tier — scope joins off this, never the rename-prone top tier).
- `awardDetails.treasuryAccount` / USAspending `federal_account` — **TAS** appropriation tie-back.
- `contractingOfficerBusinessSizeDetermination` + `socioEconomicData.*` — vendor size / set-aside
  status.

## A1 — SAM.gov Contract Awards — complete fields
Endpoint `…/contract-awards/v1/search`; `includeSections=contractId,coreData,awardDetails,awardeeData`.
Record root = `.records[]`. Authoritative complete prime feed (incl. OTs). Family rollup under
`piidAggregation.*`.

**contractId** — award/mod identity
```
contractId.piid
contractId.modificationNumber
contractId.transactionNumber
contractId.reasonForModification.{code,name}
contractId.referencedIDVPiid
contractId.referencedIDVModificationNumber
contractId.referencedIDVSubtier.{code,name}
contractId.subtier.{code,name}
```

**coreData** — what / who / where; competition; organization
```
coreData.awardOrIDV
coreData.awardOrIDVType.{code,name}            # DELIVERY ORDER, IDC, FSS, OTHER TRANSACTION AGREEMENT, …
coreData.coreVersionId
coreData.solicitationId
coreData.solicitationDate
coreData.acquisitionData.consolidatedContract.{code,name}
coreData.acquisitionData.contractFinancing.{code,name}
coreData.acquisitionData.majorProgramCode
coreData.acquisitionData.programAcronym
coreData.acquisitionData.multipleOrSingleAwardIdc.{code,name}
coreData.acquisitionData.multiyearContract.{code,name}
coreData.acquisitionData.nationalInterestAction.{code,name}
coreData.acquisitionData.performanceBasedServiceContract.{code,name}
coreData.acquisitionData.reasonForInterAgencyContracting.{code,name}
coreData.acquisitionData.typeOfContractPricing.{code,name}
coreData.acquisitionData.typeOfIdc.{code,name}
coreData.acquisitionMarketingData.emailAddress
coreData.acquisitionMarketingData.whoCanUse.{code,name}
coreData.competitionInformation.a76Action.{code,name}
coreData.competitionInformation.extentCompeted.{code,name}
coreData.competitionInformation.localAreaSetAside.{code,name}
coreData.competitionInformation.otherThanFullAndOpenCompetition.{code,name}
coreData.competitionInformation.preAwardSynopsisRequirement.{code,name}
coreData.competitionInformation.sbirSTTR.{code,name}
coreData.competitionInformation.smallBusinessCompetitivenessDemonstrationProgram.{code,name}
coreData.competitionInformation.solicitationProcedures.{code,name}
coreData.competitionInformation.sourceSelectionProcess.{code,name}
coreData.competitionInformation.statutoryExceptionToFairOpportunity.{code,name}
coreData.competitionInformation.typeOfSetAside.{code,name}
coreData.federalOrganization.contractingInformation.contractingDepartment.{code,name}
coreData.federalOrganization.contractingInformation.contractingOffice.{code,name,country,regionCode}
coreData.federalOrganization.contractingInformation.contractingSubtier.{code,name}
coreData.federalOrganization.fundingInformation.foreignFunding.{code,name}
coreData.federalOrganization.fundingInformation.fundingDepartment.{code,name}
coreData.federalOrganization.fundingInformation.fundingOffice.{code,name}
coreData.federalOrganization.fundingInformation.fundingSubtier.{code,name}
coreData.initiative.{code,name}
coreData.legislativeMandates.clingerCohenAct.{code,name}
coreData.legislativeMandates.constructionWageRateRequirements.{code,name}
coreData.legislativeMandates.interagencyContractingAuthority.{code,name}
coreData.legislativeMandates.laborStandards.{code,name}
coreData.legislativeMandates.materialsSuppliesArticlesEquipment.{code,name}
coreData.legislativeMandates.otherStatutoryAuthority
coreData.preferenceProgramsInformation.priceEvaluationPercentDifference
coreData.principalPlaceOfPerformance.city.{code,name}
coreData.principalPlaceOfPerformance.congressionalDistrict
coreData.principalPlaceOfPerformance.country.{code,name}
coreData.principalPlaceOfPerformance.county.{code,name}
coreData.principalPlaceOfPerformance.state.{code,name}
coreData.principalPlaceOfPerformance.zipCode
coreData.productOrServiceInformation.contractBundling.{code,name}
coreData.productOrServiceInformation.countryOfOrigin.{code,name}
coreData.productOrServiceInformation.dodAcquisitionProgram.{code,name}
coreData.productOrServiceInformation.dodClaimantProgram.{code,name}
coreData.productOrServiceInformation.gfeGfp.{code,name}
coreData.productOrServiceInformation.informationTechnologyCommercialItemCategory.{code,name}
coreData.productOrServiceInformation.principalNaics[].{code,name}
coreData.productOrServiceInformation.productOrService.{code,name,type}      # PSC
coreData.productOrServiceInformation.recoveredMaterialClauses.{code,name}
```

**awardDetails.dates / dollars** — timing + money (the load-bearing fields)
```
awardDetails.dates.dateSigned
awardDetails.dates.fiscalYear
awardDetails.dates.periodOfPerformanceStartDate
awardDetails.dates.currentCompletionDate
awardDetails.dates.ultimateCompletionDate
awardDetails.dates.lastDateToOrder                          # IDV ordering-period end
awardDetails.dollars.actionObligation                       # per-mod — the only field to sum
awardDetails.dollars.baseAndAllOptionsValue
awardDetails.dollars.baseAndExercisedOptionsValue
awardDetails.dollars.baseDollarsObligated
awardDetails.dollars.feePaidForUseOfService
awardDetails.dollars.nonGovernmentDollars
awardDetails.dollars.totalEstimatedOrderValue
awardDetails.totalContractDollars.totalActionObligation     # cumulative — never sum
awardDetails.totalContractDollars.totalBaseAndAllOptionsValue   # ceiling
awardDetails.totalContractDollars.totalBaseAndExercisedOptionsValue
awardDetails.totalContractDollars.totalNonGovernmentDollars
```

**awardDetails.competitionInformation / contractData / contractMarketingData**
```
awardDetails.competitionInformation.alternativeAdvertising.{code,name}
awardDetails.competitionInformation.commercialItemTestProgram.{code,name}
awardDetails.competitionInformation.commercialProductsAndServicesAcquisitionProcedures.{code,name}
awardDetails.competitionInformation.contractOpportunitiesNotice.{code,name}
awardDetails.competitionInformation.evaluatedPreference.{code,name}
awardDetails.competitionInformation.extentCompetedForReferencedIdv.{code,name}
awardDetails.competitionInformation.idvNumberOfOffersReceived
awardDetails.competitionInformation.idvTypeOfSetAside.{code,name}
awardDetails.competitionInformation.nontraditionalGovernmentEntityParticipation.{code,name}
awardDetails.competitionInformation.numberOfOffersReceived          # 999 = sentinel
awardDetails.competitionInformation.numberOfOffersSource.{code,name}
awardDetails.competitionInformation.synopsisWaiverException.{code,name}
awardDetails.competitionInformation.typeOfAgreement.name
awardDetails.competitionInformation.typeOfSetAsideSource.{code,name}
awardDetails.contractData.costAccountingStandardsClause.{code,name}
awardDetails.contractData.costOrPricingData.{code,name}
awardDetails.contractData.emergencyAcquisition.{code,name}
awardDetails.contractData.natureOfServices.{code,name}
awardDetails.contractData.numberOfActions
awardDetails.contractData.part8OrPart13
awardDetails.contractData.purchaseCardAsPaymentMethod.{code,name}
awardDetails.contractData.referencedIDVMultipleOrSingle.{code,name}
awardDetails.contractData.referencedIDVPart8OrPart13
awardDetails.contractData.referencedIDVType.{code,name}
awardDetails.contractData.undefinitizedAction.{code,name}
awardDetails.contractMarketingData.fixedFeeValue
awardDetails.contractMarketingData.individualOrderLimit
awardDetails.contractMarketingData.orderingProcedure
awardDetails.contractMarketingData.typeOfFeeForUseOfService.{code,name}
awardDetails.contractMarketingData.websiteUrl
```

**awardDetails.productOrServiceInformation / preferencePrograms / legislativeMandates / treasuryAccount / transactionData**
```
awardDetails.productOrServiceInformation.descriptionOfContractRequirement   # free-text scope
awardDetails.productOrServiceInformation.domesticOrForeignEntity.{code,name}
awardDetails.productOrServiceInformation.idvNAICS.{code,name}
awardDetails.productOrServiceInformation.placeOfManufacture.{code,name}
awardDetails.productOrServiceInformation.seaTransportation.{code,name}
awardDetails.productOrServiceInformation.useOfEpaDesignatedProducts.{code,name}
awardDetails.preferenceProgramsInformation.contractingOfficerBusinessSizeDetermination[].{code,name}
awardDetails.preferenceProgramsInformation.idvContractingOfficerBusinessSizeDetermination.{code,name}
awardDetails.preferenceProgramsInformation.reasonNotAwardedToSmallBusiness.{code,name}
awardDetails.preferenceProgramsInformation.reasonNotAwardedToSmallDisadvantagedBusiness.{code,name}
awardDetails.preferenceProgramsInformation.subcontractPlan.{code,name}
awardDetails.legislativeMandates.additionalReporting.{code,name}
awardDetails.treasuryAccount.agencyIdentifier                # TAS
awardDetails.treasuryAccount.mainAccountCode
awardDetails.treasuryAccount.subAccountCode
awardDetails.transactionData.{approvedBy,approvedDate,createdBy,createdDate,lastModifiedBy,lastModifiedDate,closedBy,closedDate,closedStatus,version}
awardDetails.transactionData.status.{code,name}
```

**awardDetails.awardeeData** — vendor identity + socio-economic (present on UEI-scoped pulls)
```
awardeeData.awardeeHeader.{awardeeName,legalBusinessName,awardeeAlternateName,awardeeDoingBusinessAsName,awardeeNameFromContract}
awardeeData.awardeeUEIInformation.uniqueEntityId                       # vendor UEI
awardeeData.awardeeUEIInformation.cageCode
awardeeData.awardeeUEIInformation.awardeeUltimateParentUniqueEntityId  # parent UEI
awardeeData.awardeeUEIInformation.awardeeUltimateParentName
awardeeData.awardeeAlternateSiteCode
awardeeData.awardeeLocation.{streetAddress1,streetAddress2,city,zip,congressionalDistrict,phoneNumber,faxNumber,awardeeDataSource}
awardeeData.awardeeLocation.state.{code,name} / country.{code,name}
awardeeData.awardeeRegistrationDetails.{registrationDate,renewalDate}
awardeeData.consortia.memberFlag
awardeeData.organizationFactors.{organizationType,foreignOwned,limitedLiabilityCorporation,subchapterSCorporation,theAbilityOneProgram}
awardeeData.organizationFactors.countryOfIncorporation.{code,name} / stateOfIncorporation.{code,name}
awardeeData.organizationFactors.profitStructure.{forProfitOrganization,nonProfitOrganization,otherNotForProfitOrganization}
awardeeData.relationshipWithFederalGovernment.{allawards,contracts,federalassistanceawards}
# boolean flag families (each a set of true/false members):
awardeeData.awardeeBusinessTypes.businessOrOrganization.* (corporateEntityNotTaxExempt, corporateEntityTaxExempt, internationalOrganization, partnershipOrLimitedLiabilityPartnership, smallAgriculturalCooperative, soleProprietorship)
awardeeData.awardeeBusinessTypes.isUsFederalGovernment.* / isUsLocalGovernment.* (city,county,municipality,schooldistrict,township,…)
awardeeData.awardeeBusinessTypes.{communityDevelopmentCorporationOwnedConcern,foreignGovernment,laborSurplusAreaFirm,usGovernmentEntity,usStateGovernment,usTribalGovernment}
awardeeData.certifications.* (sbaCertified8aProgramParticipant, sbaCertifiedHubZoneFirm, sbaCertifiedSmallDisadvantagedBusiness, sbaCertifiedWomenOwnedSmallBusiness, sbaCertifiedEconomicallyDisadvantagedWomenOwnedSmallBusiness, sbaCertified8aJointVenture, dotCertifiedDisadvantagedBusinessEnterprise, selfCertifiedHubZoneJointVenture, selfCertifiedSmallDisadvantagedBusiness)
awardeeData.educationalEntities.* (historicallyBlackCollegeOrUniversity, minorityInstitution, 1862/1890/1994LandGrantCollege, privateUniversityOrCollege, stateControlledInstitutionOfHigherLearning, tribalCollege, …)
awardeeData.lineOfBusiness.* (communityDevelopmentCorporation, educationalInstitution, foundation, hospital, manufacturerOfGoods, hispanicServicingInstitution, …)
awardeeData.otherGovernmentalEntities.* (airportAuthority, councilOfGovernments, housingAuthoritiesPublicTribal, portAuthority, transitAuthority, …)
awardeeData.socioEconomicData.* (smallBusiness, emergingSmallBusiness, VerySmallBusiness, womenOwnedBusiness, womenOwnedSmallBusiness, economicallyDisadvantagedWomenOwnedSmallBusiness, serviceDisabledVeteranOwnedBusiness, veteranOwnedBusiness, alaskanNativeCorporationOwnedFirm, americanIndianOwned, indianTribeFederallyRecognized, nativeHawaiianOrganizationOwnedFirm, triballyOwnedFirm, + JointVenture variants)
awardeeData.socioEconomicData.isMinorityOwnedBusiness.* (asianPacificAmericanOwned, blackAmericanOwned, hispanicAmericanOwned, nativeAmericanOwned, subcontinentAsianAsianIndianAmericanOwned, minorityOwnedBusiness, individualOrConcernOtherThanOneOfThePreceding)
# NASA-only block (present on NASA actions): awardDetails.nasaSpecificData.* — 31 keys (accountingInstallation, administrativeCo, buyerCode, contractFundCode, contractingOfficerCode, cotrName, fieldOfScienceOrEngineering, fundedThroughDate, physicalCompletionDate, principalInvestigator{First,Last}Name, prNumber, securityCode, supportServicesTypeContract, valueEngineeringClause, …)
```

**piidAggregation** — award-family rollup (`&piidAggregation=yes`)
```
piidAggregation.awardFamilySummary.count
piidAggregation.awardFamilySummary.totalDollars
piidAggregation.referencingDosOrBpaCallsSummary.{baseCount,totalCount,totalDollars}   # task/delivery orders under an IDV
```

## A2 — USAspending — complete fields
Base `…/api/v2`. Free, no key.

**A2a. Discovery — `POST /search/spending_by_award/` → `.results[]`**
```
internal_id ; generated_internal_id              # CONT_AWD_{PIID}_{AG}_{REFIDV}_{REFAG}
Award ID (PIID) ; Recipient Name
Awarding Agency ; Awarding Sub Agency ; Funding Agency ; Funding Sub Agency
Award Amount ; Description ; Contract Award Type
Start Date ; End Date
NAICS.{code,description} ; PSC.{code,description}
awarding_agency_id ; agency_slug
_matched_query ; _award_type_group               # local tags (which query matched; contract vs idv)
```

**A2b. Award detail — `GET /awards/{id}/`** (root object)
```
id ; generated_unique_award_id ; piid ; category ; type ; type_description ; description ; date_signed
total_obligation ; base_and_all_options ; base_exercised_options
total_outlay ; total_account_obligation ; total_account_outlay
subaward_count ; total_subaward_amount
period_of_performance.{start_date,end_date,potential_end_date,last_modified_date}
account_obligations_by_defc[].{code,amount} ; account_outlays_by_defc[].{code,amount}
awarding_agency.{id,has_agency_page,office_agency_name}
awarding_agency.toptier_agency.{name,abbreviation,code,slug} ; awarding_agency.subtier_agency.{name,abbreviation,code}
funding_agency.{… same shape as awarding_agency …}
recipient.{recipient_name,recipient_uei,recipient_hash,recipient_unique_id}        # recipient_unique_id = DUNS
recipient.{parent_recipient_name,parent_recipient_uei,parent_recipient_hash,parent_recipient_unique_id}
recipient.business_categories[]
recipient.location.{address_line1,address_line2,address_line3,city_name,county_code,county_name,state_code,state_name,zip5,zip4,congressional_code,country_name,location_country_code,foreign_postal_code,foreign_province}
place_of_performance.{… same shape as recipient.location …}
naics_hierarchy.{toptier_code,midtier_code,base_code}.{code,description}
psc_hierarchy.{toptier_code,midtier_code,subtier_code,base_code}.{code,description}
parent_award.{award_id,piid,generated_unique_award_id,agency_id,agency_name,agency_slug,sub_agency_id,sub_agency_name,idv_type_description,multiple_or_single_aw_desc,type_of_idc_description}
executive_details.officers[].{name,amount}         # top-5 compensated officers
latest_transaction_contract_data.*                 # ≈70 keys, each coded value paired with _description:
   solicitation_identifier, extent_competed[/_description], fair_opportunity_limited[/_description],
   number_of_offers_received, solicitation_procedures[/_description], type_of_contract_pricing[/_description],
   type_set_aside[/_description], naics[/_description], product_or_service_code[/_description],
   idv_type_description, type_of_idc_description, multiple_or_single_award_description,
   referenced_idv_agency_iden/_desc, subcontracting_plan[/_description], major_program, program_acronym,
   dod_acquisition_program[/_description], dod_claimant_program[/_description], national_interest_action[/_description],
   price_evaluation_adjustment, small_business_competitive, clinger_cohen_act_planning,
   commercial_item_acquisition, commercial_item_test_program, consolidated_contract, construction_wage_rate,
   cost_or_pricing_data, domestic_or_foreign_entity, evaluated_preference, fed_biz_opps, foreign_funding,
   information_technology_commercial_item_category, interagency_contracting_authority, labor_standards,
   materials_supplies, multi_year_contract, other_than_full_and_open, purchase_card_as_payment_method,
   sea_transportation  (each with a paired _description)
```

**A2c. Transactions — `POST /transactions/` → `.results[]`** (one row per modification)
```
id ; modification_number ; action_date          # use action_date for FY
federal_action_obligation                        # PER-MOD obligation — the only field you sum
action_type[/_description] ; type[/_description] ; description
face_value_loan_guarantee ; original_loan_subsidy_cost
```

**A2d. Funding — `POST /awards/funding/` → `.results[]`** (appropriation tie-back)
```
federal_account                                  # Treasury Account Symbol (TAS)
account_title ; object_class[/_name] ; program_activity_code[/_name] ; disaster_emergency_fund_code
transaction_obligated_amount ; gross_outlay_amount
reporting_fiscal_year ; reporting_fiscal_quarter ; reporting_fiscal_month ; is_quarterly_submission
awarding_agency_{id,name,slug} ; awarding_toptier_agency_id
funding_agency_{id,name,slug} ; funding_toptier_agency_id
```

## A3 — FPDS (Atom feed) — complete fields
Each `.records[]` carries flattened convenience fields **plus** the full native FPDS XML under
`raw.*`. (Legacy cross-check; the native payload mirrors SAM CA's vendor/competition/contract
structure.)

**Flattened convenience fields**
```
piid ; full_piid ; mod_number ; transaction_number ; referenced_idv_piid
record_type ; contract_action_type ; pricing_type
signed_date ; effective_date ; current_completion_date ; ultimate_completion_date ; fiscal_year
this_obligated ; total_obligated ; base_and_exercised ; base_and_all_options ; total_base_and_all_options
naics ; naics_desc ; psc ; psc_desc
extent_competed ; number_of_offers ; solicitation_procedures
vendor_name ; vendor_alt_name ; vendor_uei
contracting_agency[/_id] ; contracting_office[/_id] ; funding_agency[/_id] ; funding_office[/_id]
```

**Native FPDS payload `raw.*`** (full federal schema, ≈230 leaf paths; coded elements = `{#text, @description}`)
```
raw.@version
raw.awardID.awardContractID.{PIID,modNumber,transactionNumber,agencyID.{#text,@name}}
raw.awardID.referencedIDVID.{PIID,modNumber,agencyID.{#text,@name}}
raw.contractID.IDVID.{PIID,modNumber,agencyID.{#text,@name}}
raw.dollarValues.{obligatedAmount,baseAndExercisedOptionsValue,baseAndAllOptionsValue,totalEstimatedOrderValue}
raw.totalDollarValues.{totalObligatedAmount,totalBaseAndExercisedOptionsValue,totalBaseAndAllOptionsValue}
raw.relevantContractDates.{signedDate,effectiveDate,currentCompletionDate,ultimateCompletionDate,lastDateToOrder}
raw.contractData.* — contractActionType, typeOfContractPricing, typeOfIDC, multipleOrSingleAwardIDC, multiYearContract,
   reasonForModification, descriptionOfContractRequirement, majorProgramCode, programAcronym, numberOfActions,
   nationalInterestActionCode, contractFinancing, costOrPricingData, costAccountingStandardsClause, consolidatedContract,
   GFE-GFP, inherentlyGovernmentalFunction, performanceBasedServiceContract, purchaseCardAsPaymentMethod, seaTransportation,
   undefinitizedAction, contingencyHumanitarianPeacekeepingOperation, referencedIDVType, referencedIDVMultipleOrSingle,
   referencedIDVPart8OrPart13, solicitationID,
   listOfTreasuryAccounts.treasuryAccount.treasuryAccountSymbol.{agencyIdentifier,mainAccountCode,subAccountCode}
raw.competition.* — extentCompeted, solicitationProcedures, typeOfSetAside, typeOfSetAsideSource, reasonNotCompeted,
   numberOfOffersReceived, numberOfOffersSource, idvNumberOfOffersReceived, idvTypeOfSetAside, evaluatedPreference,
   fedBizOpps, commercialItemAcquisitionProcedures, commercialItemTestProgram, A76Action, localAreaSetAside, research,
   priceEvaluationPercentDifference, smallBusinessCompetitivenessDemonstrationProgram, statutoryExceptionToFairOpportunity
raw.productOrServiceInformation.* — productOrServiceCode{,@productOrServiceType}, principalNAICSCode, claimantProgramCode,
   systemEquipmentCode, contractBundling, countryOfOrigin, placeOfManufacture, manufacturingOrganizationType,
   informationTechnologyCommercialItemCategory, recoveredMaterialClauses, useOfEPADesignatedProducts
raw.purchaserInformation.* — contractingOfficeAgencyID{,@departmentID,@departmentName,@name}, contractingOfficeID,
   fundingRequestingAgencyID, fundingRequestingOfficeID, foreignFunding
raw.placeOfPerformance.* — placeOfPerformanceCongressionalDistrict, placeOfPerformanceZIPCode{,@city,@county},
   principalPlaceOfPerformance.{countryCode,stateCode}
raw.legislativeMandates.* — ClingerCohenAct, constructionWageRateRequirements, interagencyContractingAuthority,
   laborStandards, materialsSuppliesArticlesEquipment, otherStatutoryAuthority, listOfAdditionalReportingValues[]
raw.preferencePrograms.subcontractPlan
raw.contractMarketingData.{whoCanUse,emailAddress,feePaidForUseOfService,individualOrderLimit,typeOfFeeForUseOfService}
raw.transactionInformation.{createdBy,createdDate,lastModifiedBy,lastModifiedDate,approvedBy,approvedDate,closedBy,closedDate,closedStatus,status}
raw.genericTags.genericStrings.* ; raw.genericTags.genericBooleans.*
raw.vendor.* — full SAM/CCR vendor block mirroring SAM CA awardeeData:
   vendorHeader.{vendorName,vendorLegalOrganizationName,vendorAlternateName};
   vendorSiteDetails.entityIdentifiers.{cageCode, vendorUEIInformation.{UEI,UEILegalBusinessName,ultimateParentUEI,ultimateParentUEIName}};
   vendorLocation.{streetAddress,city,state,ZIPCode,countryCode,congressionalDistrictCode,phoneNo,faxNo,entityDataSource};
   ccrRegistrationDetails.{registrationDate,renewalDate}; contractingOfficerBusinessSizeDetermination;
   vendorBusinessTypes / vendorSocioEconomicIndicators / vendorCertifications / vendorLineOfBusiness /
   vendorOrganizationFactors / vendorRelationshipWithFederalGovernment / typeOfEducationalEntity / typeOfGovernmentEntity
   (same socio-economic boolean taxonomy as SAM CA awardeeData)
```

---

# (B) SUBAWARDS

## B0 — Most important subaward fields
- `subAwardReportId` — unique report id (**no dedup needed**).
- `subAwardAmount` — subaward dollars (**string — coerce**).
- `subAwardDate` — subaward date (use for fiscal year).
- `submittedDate` — **the *reporting* date — use this for lag analysis, not `subAwardDate`.**
- `subEntityUei` + `subEntityLegalBusinessName` — subawardee identity.
- `subParentUei` + `subEntityParentLegalBusinessName` — **roll up to the corporate parent** (the
  unit for "recurring supplier" analysis).
- `subBusinessType` — subawardee size / socio-economic type.
- `subawardDescription` — what the subcontract is for.
- `piid` (+ `referencedIDVPIID`) — the prime award / vehicle it sits under.
- `primeEntityUei` + `primeEntityName` — the prime.
- `primeNaics` — the prime's market.
- `primeOrganizationInfo.contractingOffice` / `fundingOffice` — the buyer behind the prime.
- `totalContractValue` — prime context for the subaward's scale.

## B1 — SAM.gov Subaward Reporting (FFATA, first-tier) — complete fields
Endpoint `…/prod/contract/v1/subcontracts/search`; records under `.published[]` (and identical
`.deleted[]`). The authoritative, rich subaward schema.
```
subAwardReportId                       # unique report id
subAwardReportNumber
subAwardNumber                         # subcontract number
subAwardAmount                         # subaward $ (string)
subAwardDate                           # subaward date
submittedDate                          # REPORTING date — use for lag
subawardDescription                    # what the subcontract is for
descriptionOfRequirement               # prime requirement description
subBusinessType  (also list form: subBusinessType[].{code,name})
subEntityLegalBusinessName             # subawardee legal name
subEntityDoingBusinessAsName
subEntityUei                           # subawardee UEI
subEntityParentLegalBusinessName       # subawardee corporate parent name
subParentUei                           # subawardee parent UEI (roll up here)
subTopPayEmployee[].{fullname,salary}  # FFATA executive compensation
entityPhysicalAddress.{streetAddress,streetAddress2,city,zip,congressionalDistrict}
entityPhysicalAddress.state.{code,name} / country.{code,name}
piid                                   # prime PIID
referencedIDVPIID                      # prime's parent IDV
referencedIDVAgencyId
agencyId                               # prime contracting agency
baseAwardDateSigned                    # prime base award signed date
primeContractKey
primeAwardType
primeEntityName                        # prime vendor name
primeEntityUei                         # prime UEI
primeNaics.{code,description}
totalContractValue                     # prime total contract value
primeOrganizationInfo.contractingDepartment.{code,name}
primeOrganizationInfo.contractingAgency.{code,name}
primeOrganizationInfo.contractingOffice.{code,name}
primeOrganizationInfo.fundingDepartment.{code,name}
primeOrganizationInfo.fundingAgency.{code,name}
primeOrganizationInfo.fundingOffice.{code,name}
```

## B2 — USAspending sub-awards (`POST /subawards/`) — complete fields
Thin schema; the wrapper carries prime context (local enrichment), each row is six fields.
```
# wrapper (prime context): piid, vendor, group, gid (generated_internal_id), label,
#                           prime_recipient, prime_amount, subaward_count, subaward_total
subawards[].id                         # subaward id
subawards[].subaward_number            # subcontract number
subawards[].amount                     # subaward $
subawards[].action_date                # subaward action date
subawards[].description                # subcontract description (often line-item text)
subawards[].recipient_name             # subawardee name
```

---

## Reading rules (carry as fine print / speaker notes)

- **Money hygiene — three universes, never blended.** Sum only **per-mod** obligation
  (`actionObligation` / `federal_action_obligation` / FPDS `this_obligated`). **Never** sum
  cumulative (`totalActionObligation` / `total_obligation`) across mods. **Ceiling ≠ spend**
  (`totalBaseAndAllOptionsValue`), and a multiple-award ceiling is shared across holders. Dedup
  by **award family** (parent-IDV PIID).
- **OTs only appear in SAM Contract Awards** (`awardOrIDVType` = *Other Transaction Agreement*);
  a USAspending A–D/IDV pull silently omits them.
- **Recompete timing fields:** IDV → `lastDateToOrder`; standalone → `ultimateCompletionDate` /
  USAspending `period_of_performance.potential_end_date`; OT → agreement-specific (validate
  externally).
- **Subawards are a floor:** first-tier only, 6–18-month reporting lag, some primes file nothing
  — gate point-in-time reads on `submittedDate`. SAM/FFATA (B1) is far richer than USAspending
  sub-awards (B2); use B1 as the authoritative subaward schema.
- **`numberOfOffersReceived: 999`** is a "not meaningful" sentinel, not a count.

## Provenance — raw files behind these lists

- **Prime — SAM Contract Awards:** `…/saronic_specific_awards_data/research/contracts/sam_contract_awards_ota/TEXTRON_SYSTEMS.json` (richest, carries the full `awardeeData`); the DDG/ship-repair prime pulls under `…/research/recompete_cadence_ddg/sam_contract_awards/` and `…/recompete_radar_shiprepair/sam_contract_awards/`.
- **Prime — USAspending:** `…/recompete_cadence_ddg/usaspending_raw/{discovery,detail,transactions,funding}/`.
- **Prime — FPDS:** `…/distributed_shipbuilding/tam/ddg_research/research/fpds_raw_v2/gd_biw_navy_raw.json` (deepest native schema).
- **Subaward — SAM/FFATA:** `…/research/recompete_cadence_ddg/sam_subawards/N0002418C2307.json` (authoritative).
- **Subaward — USAspending:** `…/ddg_research/research/usaspending_subawards/*.json`.
- **Practitioner guide:** `/Federal_Awards_API_HowTo.md` (field semantics, money hygiene, the OT lesson, quota/casing gotchas).

## Leave to build / scope note

This spec lists **every field** for completeness; the slide face should show the **A0 / B0
most-important sets** as the visible content (two columns: prime | subaward), with the complete
A1–A3 / B1–B2 enumerations as a reference panel, appendix, or linked exhibit — not as body text.
Build decides column layout, what is shown vs. linked, and emphasis treatment.
