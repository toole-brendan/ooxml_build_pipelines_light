---
title: Data sources, pipeline, and limitations
---

# Data sources, pipeline, and limitations

This article uses eight primary-source data feeds to construct its analysis of submarine new-construction outsourcing. The chapter documents each feed, how the article uses it, and the access patterns and quirks that affect the underlying data. It then sets out the multi-vintage reconciliation rules applied to the budget documents, the dollar-bucketing conventions for the procurement data, and the catalog of known limitations and uncertainty surrounding the article's findings.

## The eight primary-source data feeds

### 1. SCN Justification Books (U.S. Department of the Navy)

**What it gives:** Per-class per-fiscal-year cost structure (Total Ship Estimate, Basic Construction, Plans Costs, the four GFE categories, Other Cost, Change Orders), per-fiscal-year procurement quantity and unit cost, advance procurement detail (Exhibit P-10), and ship production schedules (Exhibit P-27). The principal exhibits used are P-40 (Budget Line Item Justification), P-5c (Ship Cost Analysis), and P-10 (Advance Procurement Requirements Analysis).

**Access pattern:** Published as PDF documents at the Office of the Assistant Secretary of the Navy (Financial Management & Comptroller) site. Direct URL: <https://www.secnav.navy.mil/fmc/fmb/Pages/Fiscal-Year-2027.aspx> for the FY2027 PB; prior-vintage books accessible via the archive section of the same site. Each book is approximately 700 pages.

**Conventions:** Line Item numbers (LI 1045 Columbia, LI 2013 Virginia) are stable across vintages and used throughout this article. P-1 line numbers drift across vintages and should not be used as the cross-vintage identifier. The article applies a "most recent PB year showing the target FY as settled actual, defaulting to PB year ≥ FY+2" reconciliation rule for per-fiscal-year values.

### 2. Federal Procurement Data System (FPDS) Atom Feed (U.S. General Services Administration)

**What it gives:** Per-contract-modification record of every federal contract action, including per-modification `obligatedAmount`, cumulative `totalObligatedAmount`, vendor name, North American Industry Classification System (NAICS) code, Product Service Code (PSC), signed and effective dates, contracting agency, and place-of-performance fields.

**Access pattern:** Public XML Atom feed at <https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC>. Paginated at 10 records per page, with `<link rel="last">` indicating the last page's start offset. Query syntax: field:value pairs joined by spaces (implicit AND), quoted phrases for multi-word values, square-bracket ranges for dates and numerics.

**Conventions:** The article uses **per-modification `obligatedAmount` summed by signed-date fiscal year** for annual rollups, not the latest cumulative `totalObligatedAmount`. The cumulative field is the running sum of all modifications since contract base; using it to estimate window flow would systematically overstate by counting pre-window obligations. Deduplication is by `(PIID, mod_number, signed_date)` to avoid double-counting records that appear in multiple queries.

### 3. FFATA Subaward Reporting System / SAM.gov

**What it gives:** First-tier subaward filings under FAR 52.204-10. Each filing includes the prime PIID, the subaward recipient parent legal entity (with SAM.gov Unique Entity Identifier and registered address), the subaward action date, the subaward amount, and a unique `subAwardReportId` per filed action.

**Access pattern:** Accessed via the SAM.gov subcontracts search API at `https://api.sam.gov/prod/contract/v1/subcontracts/search`. Authentication via SAM.gov API key. Pagination uses 0-indexed page numbers with `pageSize=1000` as the maximum; smaller page sizes produce more pages with random slow-page distribution. The article uses `pageSize=1000` for efficiency.

**Conventions:** Parameter casing is lowercase `piid` (not uppercase `PIID`, which is silently dropped). Date format `yyyy-MM-dd`. The system periodically returns `nextPageLink` past the actual end of data; stop conditions are empty page or `len(records) >= totalRecords`. Numeric fields are returned as strings and must be coerced. Each `subAwardReportId` is unique across the dataset (no deduplication required).

### 4. SAM.gov Entity Management API

**What it gives:** Per-Unique Entity Identifier (UEI) corporate-registration metadata, including the firm's primary NAICS code at the corporate level, registered address, samRegistered status, and a small set of additional attributes.

**Access pattern:** REST API at `https://api.sam.gov/entity-information/v3/entities`. Filter `ueiSAM=<UEI>&samRegistered=Yes`. NAICS is at `assertions.goodsAndServices.primaryNaics`.

**Conventions:** The article uses curl-via-subprocess rather than Python urllib for this endpoint because urllib has an IPv6-fallback delay against api.sam.gov that produces ~90-second response times versus curl's ~0.3-second response times. The `samRegistered=No` filter is server-side-very-slow and produces incomplete coverage; the article accepts a 30-percent "not found" rate among the top-150 enriched vendors rather than running with `samRegistered=No`.

### 5. SEC EDGAR (`data.sec.gov`)

**What it gives:** All SEC-filed documents from publicly traded companies, including Form 10-K Annual Reports (segment-level financial detail) and Form 8-K Current Reports (earnings releases). The XBRL company-facts endpoint provides consolidated financial facts but not segment-level data.

**Access pattern:** No authentication required; User-Agent header is required. Filing-history endpoint at `https://data.sec.gov/submissions/CIK<padded>.json`. Company-facts at `https://data.sec.gov/api/xbrl/companyfacts/CIK<padded>.json`. Per-filing exhibits at `https://www.sec.gov/Archives/edgar/data/<cik>/<accn-no-dashes>/`.

**Conventions:** The article uses HII (CIK 0001501585) and GD (CIK 0000040533) 10-K filings for FY2021 through FY2025. Segment-financial data is parsed from the 10-K HTML rather than from the XBRL company-facts endpoint, because the XBRL endpoint only returns consolidated facts. HII and GD use different 10-K segment-disclosure formats across the FY2021-FY2025 vintage range; the article handles both.

### 6. U.S. Department of Defense daily "Contracts" press releases

**What it gives:** Per-action announcement of all DoD contract awards equal to or greater than $7.5 million in value, including contractor name, action value, contract or modification description, place-of-performance percentage breakdown by city, expected completion date, funding source, statutory authority, and contracting activity.

**Access pattern:** Current and recent releases at <https://www.war.gov/News/Contracts/Contract/Article/<article_id>/>; historical releases through approximately January 2025 at <https://www.defense.gov/News/Contracts/>. The Internet Archive Wayback Machine (<https://web.archive.org/>) retains historical defense.gov bulletins. Third-party mirror at <https://www.globalsecurity.org/military/library/news/<YYYY>/<MM>/dod-contracts_<article_id>.htm> from approximately calendar year 2025.

**Conventions:** The article uses a combined accessor: globalsecurity.org for 2025-2026 bulletins (200-millisecond response time, no authentication); Wayback Machine for 2022-2024 bulletins (2-second rate-limited response time; `curl --compressed` required because some Wayback snapshots return gzipped content without proper Content-Encoding headers). Direct defense.gov / war.gov access from automated tools is blocked by Akamai edge filtering.

### 7. Public earnings-call-transcript publishers

**What it gives:** Verbatim transcripts of publicly held companies' earnings conference calls, including prepared remarks and analyst-Q-and-A sessions.

**Access pattern:** Multiple public sites publish transcripts free-of-charge. The article uses:
- *Motley Fool* (fool.com/earnings/call-transcripts/) — cleanest, free, full prepared remarks plus Q&A. Best source.
- *Insider Monkey* (insidermonkey.com) — full transcripts including Q&A, requires Chrome user-agent.
- *Yahoo Finance* (finance.yahoo.com) — republishes Insider Monkey but truncates Q&A; use only as last resort.
- *Seeking Alpha* (seekingalpha.com) — 403 forbidden to scripts; requires subscription.

**Conventions:** The article cites the date, speaker, role, and publishing-source URL for each transcript-derived quote. Source is the earnings call itself, not the transcript publisher; the publisher is identified as an accessor for verification convenience.

### 8. GAO, CRS, and CBO reports

**What it gives:** Authoritative U.S. government oversight, research, and budget analysis on submarine and shipbuilding programs.

**Access pattern:** GAO reports at <https://www.gao.gov/products/<report-id>>; some `/products/` pages are accessible to automated tools, but the underlying PDFs typically return HTTP 403 from automated requests against `.gov` domains. CRS reports are not officially published at congress.gov for automated access; the third-party mirror <https://www.everycrsreport.com/> archives them. CBO publications at <https://www.cbo.gov/>; some publication-landing pages are accessible.

**Conventions:** For PDF-level access where the `.gov` direct URL returns 403, the article uses the Internet Archive Wayback Machine: `https://web.archive.org/web/<year>/https://www.gao.gov/assets/<path>.pdf`. The Wayback accessor returns an older snapshot of the PDF, which is identical to the live PDF in content but may have minor formatting variation. Citations in this article reference the canonical report ID (e.g., GAO-21-257) and the canonical URL; the Wayback accessor is implementation detail.

## Multi-vintage reconciliation rule

The U.S. Department of the Navy publishes the SCN Justification Book annually. Per-fiscal-year cost figures are revised across vintages: a fiscal year that appears as the "estimate" column in one book becomes the "actual" column in the next book, often with material changes.

This article applies a **most-recent-PB-year-showing-target-FY-as-actual, defaulting to PB year ≥ FY+2** reconciliation rule:

- For settled actuals: use the most recent PB book that reports the target FY in its actual column. For example, FY2024 Columbia is taken from the FY2026 PB book (PB26), which is the first vintage to show FY2024 as a settled actual.
- For estimates: use the most recent PB book that reports the target FY at all.
- For outyears beyond the most recent budget submission's published outyear range: use the most recent PB book that publishes the year in its outyear range.

The rule is applied consistently across Exhibit P-40, P-5c, and P-10, and is used to reconcile the per-fiscal-year per-class top-line costs, cost-category breakdowns, and advance procurement bucket details documented in chapters 2 through 5.

## Dollar-bucketing conventions

The article uses the following dollar-bucketing conventions throughout:

- **FPDS prime-contract data:** Per-modification `obligatedAmount` summed by signed-date fiscal year, deduplicated by `(PIID, mod_number, signed_date)`. Not cumulative `totalObligatedAmount` (which would overstate window flow). U.S. federal fiscal years start October 1 of the prior calendar year.
- **FFATA subaward data:** Per-record `subAwardAmount` summed by `subAwardDate` fiscal year. Each `subAwardReportId` is unique across the SAM.gov database; no deduplication required.
- **Budget book data:** Nominal then-year dollars from each book's published exhibits. The article does not normalize to a base-year-dollar basis except where specific cross-vintage comparisons explicitly note the convention.
- **HII and GD segment-financial data:** Reconciled across multiple 10-K vintages using the same most-recent-vintage-shows-actual rule as the SCN Justification Books. Nominal then-year dollars unless otherwise stated.

## Known limitations and uncertainty

### Coverage limitations

1. **DoD daily-announcement corpus covers approximately calendar years 2022 through 2026.** Pre-2022 bulletins are not reachable through the routes used; the Internet Archive Wayback Machine returns very few defense.gov contract URLs before approximately mid-2022. The corpus is appropriate for "recent demonstration of structural shift," not multi-decade trend analysis. Calendar year 2022 coverage within the window is sparser than 2024-2026.
2. **DoD daily-announcement threshold is $7.5 million per action.** Actions below this threshold are not announced and are not in the article's primary-source measurement of outsourced share. Aggregate sub-threshold dollar value can be material on a per-fiscal-year basis but is not separately measured.
3. **Pre-FY2020 SCN Basic Construction detail is incomplete.** The most recent vintages of the Justification Books lump pre-FY2022 actuals into "Prior Years," limiting per-fiscal-year per-hull cost-category extraction for older procurement years. Older PB books (PB20, PB21) would close some of this gap but are not currently on hand for the article.
4. **FFATA reporting lag depresses FY2025 and FY2026 figures.** The reported FFATA-visible subaward flow for FY2025 is approximately $758 million, depressed by approximately 6 to 18 months of FFATA filing lag against a year of underlying prime-contract activity comparable to FY2024. The true FY2025 figure will revise upward as filings catch up over the following 12 to 18 months.

### Source caveats

5. **The 50-to-65-percent outsourced-band is analyst-consensus, not primary-source.** No GAO, CRS, CBO, or Navy publication directly states a make/buy ratio for the Virginia or Columbia prime construction contract. The band is an industry-analyst-consensus figure supported by five primary-source evidence pillars (chapter 6) but not directly stated as such by any single source.
6. **The Navy's 10-percent-to-50-percent distributed-shipbuilding target is for all Navy shipbuilding**, not submarine-specific. The Navy has not separately published a sub-specific number underneath the 50-percent target.
7. **HII's 30-percent year-over-year outsourcing-hours growth is a rate, not an absolute share.** HII does not disclose the base outsourcing percentage; the +30 percent is on whatever the current absolute share is.
8. **NAICS classification is corporate-primary, not work-specific.** The top FFATA-visible recipient by lifetime dollar value (Northrop Grumman) is classified at NAICS 336413 ("Aircraft Parts") because that is its predominant federal business activity, even though its submarine-relevant content is sonar, electronic warfare, and combat systems. NAICS provides directional work-type signal but is not a precise per-action classifier.
9. **Approximately 30 percent of the top-150 FFATA-visible vendors are "not found" in the SAM Entity Management API** as currently `samRegistered=Yes`. The NAICS coverage of the top-150 enriched vendors captures approximately 93.5 percent of dollar-weighted FFATA flow but only approximately 70 percent of unique vendor count.

### Methodological caveats

10. **The DoD-announcement parser treats single-supplier-site actions as 0 percent everywhere.** Approximately 17 actions ($1.6 billion of TAM-relevant value) in the corpus list a single supplier location without a percentage; the parser records 0 percent for that location. Parser-correction would lift the Other-US share of the corpus moderately. The reported 52-percent Outside-the-prime-team and 78-percent Outside-EB figures are floors.
11. **The 41-action `sub_other` residual category** in the DoD-announcement classification was not manually re-classified by program; some of these may be Virginia or Columbia actions the first-pass regex missed. Approximately $1.9 billion of corpus value. Marginal relative to the $25.4 billion TAM-relevant total but a tighter pass would slightly increase the TAM-relevant total.
12. **Geographic distribution from FFATA recipient registered address is not work location.** The state-by-state distribution in chapter 8 reflects where each vendor's registered office is, not where the vendor's submarine work is performed. The two diverge for primes with multi-state operations (Lockheed Martin's submarine work happens at Sunnyvale, California; California's 25.9-percent share of FFATA-visible dollars reflects this) but is structurally distinct from the DoD-announcement place-of-performance data in chapter 7.

### Future-work items

13. **Per-hull subaward attribution within the master PIIDs.** Many subaward filings reference hulls in their mod descriptions (e.g., "SSN 812 CONSTRUCTION (BOAT 2, FY 24)"). A systematic regex extractor could map subawards to specific hulls and split per-boat costs. This is labor-intensive and not currently in scope.
14. **Tightened pass on the DoD-announcement single-supplier-site parser** would resolve the $1.6-billion 0-percent-everywhere parser miss. Estimated at approximately 15 minutes of regex-correction work; not yet executed.
15. **Mod-description-level mining of GDEB prime-contract modifications** would identify hull-specific work content and would help close the per-hull-per-FY allocation gap. Public NAVSEA contract announcements occasionally provide this attribution.
16. **HII Newport News submarine-vs-carrier revenue disclosure** would resolve the largest single category of unseen flow (the HII team-build share quantified in chapter 11). HII does not currently publish this split.

## Cross-references

- For the cost-funnel framework that integrates all the data feeds: [Scope and the funnel framework](01-scope-and-funnel-framework.md) and [The outsourced layer within Basic Construction](06-outsourced-band-within-bc.md).
- For the principal primary-source measurements: [DoD contract announcement data](07-dod-contract-announcement-data.md) and [FFATA-visible first-tier subawards](08-ffata-visible-subawards.md).
- For the unseen layer's specific limitations: [The unseen layer](12-unseen-layer.md).
- For the HII visibility-gap quantification: [The HII Newport News visibility gap](11-hii-newport-news-gap.md).
- For the article's full reference list: [Index and references](INDEX.md#references).
