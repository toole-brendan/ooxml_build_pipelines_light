# Subaward Documentation Non-Compliance — Primary Source Inventory

**Date compiled:** 2026-05-24
**Purpose:** Document that FFATA / FSRS subaward reporting non-compliance is a
known issue, and inventory the primary-source reports that defensibly support
that claim. Created because the FFATA-visible subaward gap is the single
biggest data limitation in the cost-funnel analysis — and the prior project
notes had no specific GAO/CRS citation behind the "known FFATA enforcement
gap" framing.

---

## Short answer

**Yes — subaward documentation non-compliance is a well-documented, recurring
finding.** But the prior project work did NOT cite a specific CRS/GAO report
for it. The non-compliance discussion lives in two places in this folder:

1. `reference_prior_analysis/Federal_Procurement_Research_Lessons_Learned.md`
   §6 "Subaward Reporting Gaps -- Who Doesn't Report" (lines 340-384)
2. `logs/2026-05-22_session_log.md:341`

Both describe it as direct observation — calling it "a known FFATA enforcement
gap" — without a primary-source citation. The five reports listed below are
the actual primary sources that back up that claim.

---

## What's already in this folder on this topic

- **`reference_prior_analysis/Federal_Procurement_Research_Lessons_Learned.md`
  §6 "Subaward Reporting Gaps -- Who Doesn't Report"** (lines 340-384) — the
  most useful in-folder summary. Names specific primes (Bath Iron Works,
  Bollinger, Birdon, Austal, BIW, foreign-owned primes like Rauma / Davie /
  VT Halter) as 0-subaward filers across FY20-26 contracts. Documented
  patterns:
  - Foreign-owned primes don't report (Rauma FI, Davie CA, VT Halter pre-acq)
  - New contracts (last 12-24 months) don't yet have sub records — reporting
    lags prime obligation
  - Some US primes are systematically non-compliant (Bollinger, BIW, Birdon)
  - The same prime can report on one contract and not another (Bechtel, LM
    Sippican)

- **`reference_prior_analysis/SAM_Submarine_Cutter_Contract_Awards.md`** lines
  56, 722, 797, 912, 1098 — same observation, applied to the cutter program.

- **`SAM_GOV_HOWTO.md`** lines 588-598 — "Empty result on a PIID you expect to
  have subs" caveat: "pre-FY2010 contracts predate FFATA; some primes never
  file at the prime-master level (Lockheed Martin is a known offender)."

- **`logs/2026-05-22_session_log.md:341`** — one-liner: "Some primes
  systematically under-report. GDEB does report; some other primes
  (Bollinger, BIW, etc.) don't."

- **`logs/2026-05-24_session_log.md`** — references "FFATA non-compliance"
  as part of the "unseen layer" in the cost funnel (lines 51-53, 447-449) but
  again does not cite a specific report.

---

## Primary-source reports you can actually cite (NONE are in this folder yet)

Listed in order of usefulness for the submarine outsourcing analysis.

### 1. DCMA Contractor Purchasing System Review (CPSR) findings — STRONGEST for contract subawards

The closest thing to a primary-source statement that **defense primes
systematically fail to report FFATA subs**. Per DCMA's own published
deficiency rankings (cited in the DCMA CPSR Guidebook and recycled by
DCAA-adjacent consultancies):

> **FFATA reporting has consistently ranked among the top 3 most-common CPSR
> deficiencies over the past 5 years**, alongside Price Analysis (#1) and
> Sole Source Justification (#2).

**Why it matters:** This is the only primary source identified that hits
*contract* (not grant) subaward non-compliance head-on, and it comes from
the DOD oversight body that actually audits the primes (DCMA). Directly
relevant to GDEB / HII / BIW / Bollinger — all of which are subject to CPSR.

**Citation chain:** DCMA CPSR Guidebook (Sept 10, 2021 ed.) → restated in
industry summaries (SpendLogic, Forvis Mazars, RedstoneGCI). The DCMA
guidebook itself is the primary source; the industry articles are the
clearest narrative recap.

- DCMA CPSR Guidebook: https://www.dcma.mil/Portals/31/Documents/CPSR/CPSR_Guidebook_091021.pdf
- SpendLogic — Top 5 Deficiencies: https://spendlogic.com/top-5-deficiencies-cpsr-audit/
- Forvis Mazars — FFATA reporting for contractors: https://www.forvismazars.us/forsights/2025/01/subaward-executive-compensation-reporting-for-government-contractors

### 2. GAO-24-106237 — STRONGEST for quantified data-quality findings

**Title:** "Federal Spending Transparency: Opportunities Exist to Improve
COVID-19 and Other Grant Subaward Data on USAspending.gov"
**Published:** November 16, 2023.
**Scope caveat:** This report scopes to **grants, not contracts.** Useful as
illustrative of the systemic data-quality problem but does NOT directly hit
the contract side.

Specific quantified findings GAO documented:
- 14% of prime-grant award records have combined subaward totals that exceed
  the prime award amount (34,009 of ~247K records)
- 26% of non-COVID-19 grant subawards are likely duplicate records
- 11% of COVID-19 grant subawards are likely duplicate records
- One record shows a $1 quintillion subaward; five others exceed the US GDP
  for the year they were made
- Root cause: FSRS includes mandatory data fields but **few validation
  tests** to catch errors at entry; prime recipients lacked knowledge of
  FFATA requirements due to insufficient guidance

**GAO recommendations:** Two to GSA (incorporate data validation controls
into the FSRS modernization plan); one to Treasury (improve grant subaward
data quality disclosures); one to OMB (clarify agency roles).

- Landing page: https://www.gao.gov/products/gao-24-106237
- Full PDF: https://www.gao.gov/assets/gao-24-106237.pdf

### 3. GAO-18-546 — Government-wide DATA Act quality

**Title:** "DATA Act: Reported Quality of Agencies' Spending Data Reviewed by
OIGs Varied Because of Government-wide and Agency Issues"
**Published:** July 23, 2018.

Useful for the government-wide framing of inconsistent data quality across
agencies under the DATA Act. Less granular than GAO-24-106237 but earlier in
the timeline.

- Full PDF: https://www.gao.gov/assets/gao-18-546.pdf

### 4. GAO-14-476 — Foundational data-transparency report

**Title:** "Data Transparency: Oversight Needed to Address Underlying
Limitations in Data on Federal Agencies' Spending"
**Published:** 2014.

The foundational GAO report identifying USAspending data quality problems.
Useful only for historical framing — the issues GAO flagged here predate the
DATA Act implementation and are well superseded by the 2018/2023 reports.

- Full PDF: https://www.gao.gov/assets/gao-14-476.pdf

### 5. CRS R44027 — Canonical explainer (NOT a primary-source citation of non-compliance)

**Title:** "Tracking Federal Awards: USAspending.gov and Other Data Sources"
**Author:** Garrett Hatch, Congressional Research Service. Updated periodically.

The canonical CRS explainer report for USAspending.gov as a data source.
Acknowledges general data-quality issues — notes that 25 executive-branch
agencies didn't report to USAspending in FY2022 — but does NOT identify
specific non-compliant prime contractors or sectors. Useful as context, not
as the primary citation for the non-compliance claim.

- Congress.gov: https://www.congress.gov/crs-product/R44027
- EveryCRSReport mirror (per `.gov` 403 workaround): https://www.everycrsreport.com/reports/R44027.html

### 6. HUD OIG Report — Agency-specific case study

**Title:** "HUD's Subaward Data on USASpending.gov Were Not Complete nor Accurate"
**Source:** HUD Office of Inspector General.

Specific finding: HUD's prime recipients lacked knowledge of FFATA subaward
reporting requirements due to insufficient guidance and oversight by HUD
program offices and lack of an enterprise-level policy. Useful as a
single-agency case study showing the gap is real and recognized inside the
federal IG community.

- HUD OIG: https://www.hudoig.gov/reports-publications/report/huds-subaward-data-usaspendinggov-were-not-complete-nor-accurate

---

## Recommended citation chain for the deck

The cleanest defensible chain for the cost-funnel "unseen layer" framing is:

1. **DCMA CPSR Guidebook** — "FFATA non-compliance is a top-3 recurring
   contractor purchasing system review deficiency over the past 5 years"
   (contract-side primary source from DOD's own oversight body)

2. **GAO-24-106237 (Nov 2023)** — "GAO has separately documented systemic
   data-quality problems on the grants side, including 26% duplicate
   records and 14% of prime grants with subaward totals exceeding the prime"
   (GAO-issued acknowledgement of the systemic problem, used as supporting
   evidence even though the scope is grants)

3. **Direct observation from this project** — "Across the FY20-26 submarine
   PIID set, 12 primes filed 0 subawards despite >$X billion in prime
   obligations, including Bath Iron Works (DDG-51), Bollinger entities,
   Birdon, Austal, and foreign primes" (citing
   `Federal_Procurement_Research_Lessons_Learned.md` §6)

That triplet gives you: (a) a DOD contract-side primary source, (b) a
GAO-issued report acknowledging the systemic problem, and (c) project-
specific empirical evidence — which together strongly support the
"FFATA-visible ≠ actual subcontracting" framing in the funnel.

---

## Open items / next steps

- [ ] Download `GAO-24-106237.pdf` and `DCMA CPSR Guidebook (Sept 2021).pdf`
      into `research_primary_sources/`
- [ ] Add rows for both to `extracted/industry_baseline_citations.csv` with
      verbatim quotes + page numbers
- [ ] If the cost-funnel deck calls out the non-compliance gap explicitly,
      cite the DCMA CPSR ranking as the primary source rather than relying
      on the prior session's bare assertion
- [ ] Note that FSRS is being retired in early 2025 and subaward reporting
      is moving to SAM.gov — this means the historical FFATA data quality
      issues are anchored to a system that is itself being deprecated;
      worth a one-line footnote in the deck

---

## Sources

- [GAO-24-106237 — Federal Spending Transparency (Grant Subawards) landing](https://www.gao.gov/products/gao-24-106237)
- [GAO-24-106237 — full PDF](https://www.gao.gov/assets/gao-24-106237.pdf)
- [GAO-25-107315 — Grants Management: Subaward Oversight](https://files.gao.gov/reports/GAO-25-107315/index.html)
- [GAO-18-546 — DATA Act Reported Quality (PDF)](https://www.gao.gov/assets/gao-18-546.pdf)
- [GAO-14-476 — Data Transparency (PDF)](https://www.gao.gov/assets/gao-14-476.pdf)
- [CRS R44027 — Tracking Federal Awards (Congress.gov)](https://www.congress.gov/crs-product/R44027)
- [CRS R44027 — EveryCRSReport mirror (use per the `.gov` 403 workaround)](https://www.everycrsreport.com/reports/R44027.html)
- [DCMA CPSR Guidebook — Sept 10, 2021 ed.](https://www.dcma.mil/Portals/31/Documents/CPSR/CPSR_Guidebook_091021.pdf)
- [SpendLogic — Top 5 Deficiencies in a CPSR Audit](https://spendlogic.com/top-5-deficiencies-cpsr-audit/)
- [Forvis Mazars — FFATA reporting for contractors and grant recipients (Jan 2025)](https://www.forvismazars.us/forsights/2025/01/subaward-executive-compensation-reporting-for-government-contractors)
- [HUD OIG — HUD Subaward Data on USAspending Were Not Complete nor Accurate](https://www.hudoig.gov/reports-publications/report/huds-subaward-data-usaspendinggov-were-not-complete-nor-accurate)
