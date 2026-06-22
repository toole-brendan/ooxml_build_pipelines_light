# 2026-06-21 — New SAM.gov Contract Awards API: HII-gap long-shot test + methodology-doc addendum

Session goal: a user long-shot — could the **new SAM.gov Contract Awards API** (open.gsa.gov/api/contract-awards,
v1.0 released 2025-12-05) surface the HII↔GDEB co-build workshare that the
`DOMAIN_SHARE_CONCENTRATION_CAVEAT.md` nine-method investigation found structurally absent? Tested it
empirically rather than asserting. **Answer: no — it re-confirms the gap but cannot crack it.** This API is
the modern replacement for the FPDS *prime* Atom feed; it serves prime award + IDV actions, **not** subawards,
so the GDEB→HII subcontract is invisible here for the same reason it is in FFATA/USAspending. Byproduct: a
full param/usage map of the new API was captured into the personal methodology doc, and the stale subaward
`piid`-casing note there was corrected.

Key: `SAM_API_KEY` in `projects3/ooxml_build_pipelines_light/.env` (40-char personal key, ≥role tier — async
extracts worked, so ≥1,000 req/day).

---

## Why this API structurally cannot see the HII gap

It is a **prime / IDV award** feed (Definitive Contracts, IDVs, Delivery/Task Orders, Purchase Orders, BPAs &
Calls, OT). HII's co-build is a **first-tier subcontract under GDEB's construction primes** — i.e. FSRS/subaward
data, a different feed. The one genuinely new field vs FPDS — **Immediate/Domestic Parent UEI** — is (a) DoD-only
"unrevealed" data a personal key can't get, and (b) the awardee's *corporate* parent, **not** a subcontractor.
So even with access it would not expose the linkage.

---

## HII prime re-test through the new API (definitive)

Pulled HII Newport News (UEI `WMXDDH6HJNA5`) entire NAICS-336611 prime history via the async CSV extract:
**32,655 mod-records / 613 distinct base PIIDs.** Obligations by DoD acquisition program:

| Program | Obligated | Note |
|---|--:|---|
| CVN 78 (Ford carrier) | $32.2B | core HII work |
| NONE (largely carrier RCOH/refuel) | $27.1B | program code untagged |
| CVN 68 (Nimitz) | $9.4B | |
| **SSN 774 (Virginia)** | **$32.7M** | maintenance/repair DOs under NAVSEA IDVs, not construction |
| SSN 688 / Seawolf / SSGN | ~$3.2M | |
| **All submarine-tagged programs** | **$35.9M** | |
| **Records referencing a GDEB construction prime (C2100/C2120/C2117)** | **0** | the decisive result |

The SSN-774-tagged HII records are delivery orders under unrelated NAVSEA IDVs (`N0002404D4409`,
`N0002416G4303`, …) and a NUWC-Newport standalone (`N6660405C3314`); PSCs are MAINT/REPAIR, not construction.
**None reference the GDEB Virginia/Columbia construction primes.** This independently re-confirms the caveat
doc: HII's construction co-build is absent from prime data, and the multi-billion workshare lives only in
subawards/issuer disclosures. **No re-opening of the forensics** — consistent with "data forensics exhausted."

---

## New-API mechanics captured (for reuse)

- **Endpoint:** `GET https://api.sam.gov/contract-awards/v1/search?api_key=…`; deleted (last 6 mo) via
  `&deletedStatus=yes`. OpenAPI at `…/v1/openapi.yaml`.
- **piid casing:** UPPERCASE, no dashes (`N0002417C2100`). Dashed → HTTP 400. (Same casing the subaward
  endpoint now wants — see below.)
- **Verified params:** `awardeeUniqueEntityId`, `ultimateParentUniqueEntityId`, `awardeeLegalBusinessName`,
  `naicsCode`, `productOrServiceCode`, `dateSigned`, `lastModifiedDate`, `dollarsObligated`,
  `contractingDepartmentCode`, `awardOrIDVType`, `piid`, `referencedIdvPiid`, `q`, `deletedStatus`.
  `includeSections` ∈ {contractId, coreData, awardDetails, awardeeData, nasaSpecific} to trim payload.
- **Dollars** live in `awardDetails`: `dollars.actionObligation` (this mod) vs
  `totalContractDollars.totalActionObligation` (cumulative) — same never-sum-the-cumulative rule as FPDS.
- **`piidAggregation=yes`** (with `piid`; add `referencedIdvPiid` if non-unique) → award-family rollup.
  Worked example: `N0002417C2100` → **520 records / $34.95B** (GDEB Block V Virginia prime family) in one call.
  Useful as a fast EB-denominator completeness cross-check. Columbia prime `N0002417C2117` = 374 records,
  program code **000/NONE** (so program code is useless for isolating submarine construction).
- **Async extract (bulk):** `format=csv|json` **and** `emailId=Yes|No` must be sent together (else 400).
  Returns a `presignedUrl` with `REPLACE_WITH_API_KEY` + token; substitute key and GET. Early polls
  303→S3 "key does not exist" (404) = still generating; poll until the ZIP (`PK…`) lands (~1–2 min). Up to
  1,000,000 records, CSV ZIP-wrapped, mod-level (group by `piid` for base contracts).
- **Paging:** `limit` ≤ 100; `offset × limit` ≤ 400,000 (hard sync cap). **Rate limits:** 10 / 1,000 / 10,000
  per day (no-role / role / federal-system).

---

## Methodology-doc update (`projects3/Federal_Award_API_Research_Methodology.docx`)

- Appended **§5 Addendum (2026-06-21)** documenting the Contract Awards API (all of the above + the HII
  case-study limitation), style-matched to the existing doc (Calibri, manual `•`/`◦` bullets, bold 11.5pt
  numbered headers). Done with `python-docx` (no pandoc on box).
- **Corrected §3 inline:** the old gotcha "piid must be lowercase (uppercase silently dropped)" is now
  **REVERSED** — the subaward endpoint (`api.sam.gov/prod/contract/v1/subcontracts/search`) now wants
  UPPERCASE no-dash; lowercase silently returns HTTP 200 / `totalRecords:0`. (Matches the casing flip recorded
  in `SAM_GOV_HOWTO.md` / the EB-denominator log.)
- Produced **`Federal_Award_API_Research_Methodology.md`** — full Markdown conversion of the updated doc.
- Backup `…docx.bak-20260621` was created then deleted at user request.

---

## Carry-forward

- **The HII workshare answer is unchanged and now triple-sourced** (FSRS nine-method + completed EB prime set +
  this prime API): recover it via issuer disclosures (Block V ≈ $10.2B) + NAVSEA FOIA / PIEE-EDA, **not** any
  federal transactional feed. Do not re-run forensics.
- **The new Contract Awards API is a useful prime-side tool going forward** — esp. `piidAggregation` for
  denominator-completeness checks and the async extract for bulk vendor/NAICS sweeps. It does **not** replace
  the §3 subaward endpoint for supplier-layer work.
- Temp pulls left in `/tmp/hii_extract`, `/tmp/hii_dollars` (clear on reboot); nothing committed to the repo
  data layer — this session was investigation + personal-doc only, no workbook/CSV changes.
