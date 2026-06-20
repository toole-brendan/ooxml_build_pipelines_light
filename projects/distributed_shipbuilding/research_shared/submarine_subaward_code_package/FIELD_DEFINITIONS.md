# Field definitions & package contents

Subcontract ("subaward") records reported to the U.S. government (SAM.gov FSRS /
Acquisition Subaward Reporting API) for a set of U.S. Navy submarine-construction
prime contracts. All values are reproduced verbatim from the API response.

## Files

- **`submarine_subawards.csv`** — one row per subaward record. Every native field
  from the API response is a column, verbatim. Nested objects are flattened to
  dotted column names (e.g. `primeNaics.code`); list-valued fields
  (`subBusinessType`, `subTopPayEmployee`) are stored as JSON strings. No derived,
  computed, split, or annotated columns have been added.
- **`raw_json/`** — the original per-PIID pull files (one JSON per prime contract),
  unmodified. Source of truth; the CSV is a 1:1 flatten of the `published` arrays.
- **`vendor_naics_reference.csv`** — industry codes per subawardee UEI, from the SAM
  Entity Management API (a separate pull). Columns: `uei`, `naics6`, `naics_desc`,
  `is_primary`. Long format (one row per NAICS code per UEI). Covers 654 of the 1,401
  distinct UEIs in the data; not every vendor is present.
- **`FIELD_DEFINITIONS.md`** — this file.

## `submarine_subawards.csv` columns

Definitions are the SAM/FSRS field meanings; they describe the source of each field,
not its contents.

| column | definition |
|---|---|
| `primeContractKey` | Internal key for the prime contract record. |
| `piid` | Procurement Instrument Identifier (PIID) of the prime contract. |
| `agencyId` | Contracting agency identifier of the prime contract. |
| `referencedIDVPIID` | PIID of the referenced Indefinite Delivery Vehicle (parent IDV), if any. |
| `referencedIDVAgencyId` | Agency identifier of the referenced IDV. |
| `subAwardReportId` | System-generated unique identifier of the subaward report record. |
| `subAwardReportNumber` | Report number for the subaward report. |
| `submittedDate` | Date the subaward report was submitted. |
| `subAwardNumber` | Identifier of the subaward, as assigned by the prime contractor. |
| `subAwardAmount` | Dollar amount of the subaward. |
| `subAwardDate` | Date of the subaward action. |
| `subEntityLegalBusinessName` | Legal business name of the subawardee. |
| `subEntityUei` | Unique Entity ID (SAM) of the subawardee. |
| `primeAwardType` | Type of the prime award. |
| `totalContractValue` | Total value of the prime contract. |
| `primeEntityUei` | Unique Entity ID of the prime contractor. |
| `primeEntityName` | Name of the prime contractor. |
| `baseAwardDateSigned` | Date the base prime award was signed. |
| `descriptionOfRequirement` | Description of the requirement, at the prime-award level. |
| `primeNaics.code` | NAICS code associated with the prime award. |
| `primeNaics.description` | NAICS description associated with the prime award. |
| `primeOrganizationInfo.fundingAgency` | Funding agency of the prime award. |
| `primeOrganizationInfo.fundingOffice` | Funding office of the prime award. |
| `primeOrganizationInfo.contractingAgency` | Contracting agency of the prime award. |
| `primeOrganizationInfo.contractingOffice` | Contracting office of the prime award. |
| `primeOrganizationInfo.fundingDepartment` | Funding department of the prime award. |
| `primeOrganizationInfo.contractingDepartment` | Contracting department of the prime award. |
| `entityPhysicalAddress.streetAddress` | Subawardee physical street address. |
| `entityPhysicalAddress.streetAddress2` | Subawardee physical street address, line 2. |
| `entityPhysicalAddress.city` | Subawardee city. |
| `entityPhysicalAddress.congressionalDistrict` | Subawardee congressional district. |
| `entityPhysicalAddress.state` | Subawardee state. |
| `entityPhysicalAddress.country` | Subawardee country. |
| `entityPhysicalAddress.zip` | Subawardee ZIP code. |
| `subBusinessType` | Business-type codes/names of the subawardee (JSON list of `{code, name}`). |
| `subParentUei` | Unique Entity ID of the subawardee's parent entity. |
| `subawardDescription` | Description of the subaward, as entered by the prime contractor. |
| `subEntityDoingBusinessAsName` | "Doing business as" name of the subawardee. |
| `subTopPayEmployee` | Highest-compensated officers of the subawardee, if reported (JSON). |
| `subEntityParentLegalBusinessName` | Legal business name of the subawardee's parent entity. |
