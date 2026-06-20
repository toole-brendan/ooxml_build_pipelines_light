---
title: FFATA-visible first-tier subawards
---

# FFATA-visible first-tier subawards

This chapter takes up the second of the three direct measurements of outsourced share that the data permits: the **first-tier subaward stream** that prime contractors are required to file under the Federal Funding Accountability and Transparency Act of 2006 (FFATA) for actions above $30,000, accessed via the U.S. General Services Administration's SAM.gov portal. The chapter describes the data source, summarizes the cumulative FFATA-visible flow against the in-scope DDG-51 new-construction PIID set, walks through the methodological details of the SAM.gov pull as documented in the companion `SAM_GOV_HOWTO.md`, and reports the comparison between the SAM.gov source and the parallel USAspending.gov source.

## The source

FFATA Section 2(b)(1) and Section 3 require that prime contractors filing federal contracts over $25,000 (now $30,000 by indexing) report each first-tier subaward they issue against that prime contract. The reporting flows into the **FFATA Subaward Reporting System (FSRS)**, which is the underlying database backing the SAM.gov public-facing search interface. The legal authority is FAR 52.204-10 (the FFATA-implementing acquisition clause), and the regulatory definition of "first-tier subaward" excludes:

- Long-term supplier agreements, blanket purchase agreements, and indefinite-delivery / indefinite-quantity supplier agreements that are not direct prime-contract subcontracts
- Indirect and general-and-administrative (G&A) items
- Lower-tier subcontracts (a sub's sub is not reportable)
- Standing supply or material agreements that pre-exist the prime contract and are not subordinated to it

In practice the FFATA-visible flow is best understood as the **upper bound** on what is publicly auditable in first-tier supplier relationships; it is structurally and definitionally lower than the actual yard-side outsourcing flow, and substantially so (chapter 9 estimates that FFATA captures approximately 15 percent of the real yard-outsourcing flow against the two destroyer yards).

The SAM.gov subaward search API endpoint at `https://api.sam.gov/prod/contract/v1/subcontracts/search` accepts a lowercase `piid` parameter and returns paginated JSON arrays of subaward records, each with a unique `subAwardReportId`.

## Methodology

The destroyer-project SAM.gov pull was executed against 89 prime PIIDs discovered through FPDS vendor-name searches. The full discovery → pull → aggregation methodology is documented in `SAM_GOV_HOWTO.md` in the project repository; the key items relevant to interpreting the resulting dataset are:

1. **Account tier and rate limit.** The project SAM API key is on the production tier with a 1,000-request-per-day cap. The 89-PIID pull executes in under three minutes after the IPv4 socket monkeypatch (item 3 below).
2. **Parameter casing.** The PIID parameter is lowercase `piid` rather than the uppercase `PIID` used in some other SAM.gov endpoints; the casing mismatch causes silent zero-result responses, not error responses.
3. **The macOS IPv4 monkeypatch.** On macOS, Python's `urllib` issues HTTP requests over IPv6 by default, and the IPv6 SYN retransmit timeout against the SAM.gov API endpoint is approximately 225 seconds per request — making the 89-PIID pull take roughly 20 hours wall-clock. Forcing IPv4 via a `socket.getaddrinfo` monkeypatch reduces per-request latency to approximately 0.3 seconds. The full pull completes in approximately 3 minutes after the patch. This is documented as the "RFC 8305 Happy Eyeballs" workaround.
4. **Deduplication.** SAM.gov assigns one unique `subAwardReportId` per published subaward action. Across the 24,559-record in-scope subaward pull, **zero duplicate `subAwardReportId` values were observed**, so no deduplication step is needed beyond using the report ID as the primary key.
5. **Published vs. deleted.** The SAM.gov API returns both currently-published and previously-deleted subaward records. The destroyer pull captures both streams. Deleted records (representing corrections or retractions by the filing prime) total 37 records across the 89 PIIDs and are excluded from headline aggregations.

## Aggregate flow against the in-scope PIID set

Across the 89 in-scope new-construction PIIDs and the FY2002–FY2026 action-date window, the cumulative FFATA-visible first-tier subaward flow is:

- **24,559 published subaward records** (37 deleted; total $15.50 billion in published value before in-scope filtering)
- **22,235 in-scope records** after the new-construction classification pass (excluding non-DDG noise like LPD/LHA work on shared PIIDs)
- **$13.84 billion cumulative subaward value** across the in-scope record set
- **1,954 unique parent vendor UEIs** as recipients

The cumulative $13.84 billion FFATA-visible subaward flow is the principal denominator against which chapter 9's "FFATA captures approximately 15 percent of real yard-side outsourcing" figure is computed.

## Per-PIID summary (top 10 by SAM-reported subaward dollar value)

The ten PIIDs with the largest cumulative FFATA-visible subaward dollar value in the in-scope set:

| PIID | Group | Label | SAM records | SAM $M |
|---|---|---|---:|---:|
| `N00024-22-C-5500` | Raytheon | DDG FLT III (AN/SPY-6(V)1) | 1,057 | 1,502.2 |
| `N00024-15-C-5332` | LM-Aegis | USN DDG 127 Mk 41 Mod 15 VLS Mech | 328 | 1,494.7 |
| `N00024-20-C-5310` | LM-Aegis | Mk 41 Mod 36 VLS Module Mech | 834 | 1,425.5 |
| `N00024-18-C-2307` | HII-Ingalls | FY18 DDG-51 Class Construction (DDG 128) | 2,599 | 1,268.6 |
| `N00024-23-C-2307` | HII-Ingalls | FY23-27 MYP Construction of DDG-51 Ship | 493 | 1,144.5 |
| `N00024-18-C-5406` | Raytheon | Mk 15 Phalanx CIWS BK 0 to 1B BL 2 U&C | 3,661 | 1,130.9 |
| `M67854-16-C-0006` | BAE-Guns/VLS | Mk 110 / FRP Lot 6B hedge lock rate | 2,324 | 1,667.7 (mixed Mk 45 + amphib gun) |
| `N00024-21-C-5408` | Raytheon | ESSM BLK 2 FY21-23 Part 2 Spares | 952 | 652.1 |
| `N00024-13-C-5116` | LM-Aegis | Aegis CSEA Funding Mod | 635 | 654.2 |
| `N00024-14-C-5114` | LM-Aegis | Aegis Hardware | 1,362 | 615.4 |

The single largest SAM-reported PIID is `M67854-16-C-0006` at $1,667.7M of subaward dollar value across 2,324 records, but this PIID's underlying scope mixes Mk 110 amphibious-warship gun procurement (IVECO Defence Vehicles, Parker-Hannifin) with the smaller DDG-related sub-scope; the IVECO contamination caveat is discussed in chapter 6.

The Raytheon SPY-6 production PIID (`N00024-22-C-5500`) and the two Lockheed Martin Mk 41 VLS production PIIDs (`N00024-15-C-5332` and `N00024-20-C-5310`) are the three largest cleanly-DDG-attributable subaward-stream PIIDs, each with cumulative subaward value of approximately $1.4–1.5 billion.

Note that the **FY23-27 BIW multiyear master PIID `N00024-23-C-2305`** appears in the SAM.gov pull with **zero published subaward records** (and zero deleted) at the time of the pull. This is partially a function of FFATA reporting lag (the August 2023 award is recent enough that first-tier subaward filings against it are still accumulating) and partially a function of GD-BIW's historical FFATA reporting practices, which appear to lag the company's actual first-tier subcontract issuance by several quarters or longer. By contrast, the Ingalls FY23-27 master PIID `N00024-23-C-2307` shows 493 published subawards at $1,144.5 million in approximately 24 months of post-award reporting — a reporting density nearly 2 orders of magnitude higher than BIW.

## SAM.gov vs USAspending — which is the right denominator

The U.S. Treasury's USAspending.gov portal exposes a parallel subaward API (`/api/v2/subawards/`) that reads from the same FFATA underlying database. The destroyer project initially executed both pulls in parallel for cross-validation. The results comparison is summarized in `extracted/sam_vs_usaspending_per_piid.csv`:

- **SAM.gov pull (89 PIIDs)**: 24,559 records / $15.50 billion published
- **USAspending pull (87 PIIDs that returned non-empty results)**: 26,811 records / $20.61 billion

The USAspending pull reports approximately **1.33x the dollar value** at approximately the same record count. The natural reading would be that USAspending captures dollars SAM.gov misses, but the per-PIID drill-down shows that **93 percent of the dollar delta is concentrated in a single PIID**:

> `N00024-15-C-5420` (Raytheon EMD for ESSM Block 2): USAspending reports +$4,749.8 million versus SAM.gov, driven by a single $4,201 million Thales Nederland B.V. record dated 2015-03-11. This record represents the ESSM Block 2 NATO cooperative-development cost share among 10 partner nations — it is not US Navy DDG spend, and SAM.gov's filter correctly excludes it. The remaining ~200 duplicated (recipient, amount) records in USAspending appear to be display artifacts from the API's transformation logic.

After backing out the Thales NL artifact and the 2 minor PIIDs where SAM.gov captures more (HII construction PIIDs, ~$591M combined delta), the **net "real" delta between SAM.gov and USAspending is approximately $350M–$1.1B** — comparable in magnitude to ordinary reporting-lag noise and small relative to the $13.84B in-scope total.

**Conclusion: SAM.gov is the canonical FFATA denominator for this analysis.** USAspending is treated as a cross-validation source only, not as the authoritative measurement. This conclusion is the inverse of the standard practice in the federal-procurement-research community, which more often uses USAspending because of its more polished UX. The polished UX comes at the cost of per-PIID record truncation (USAspending caps at approximately 2,500 records per prime PIID, while SAM.gov has no cap) and the introduction of derivative records like the Thales NL inflation. For the destroyer corpus, SAM.gov is upstream of USAspending and is the right primary source.

## Year-by-year subaward flow

The cumulative $13.84 billion in-scope subaward flow distributes across action-date fiscal years as follows (from `extracted/nc_annual_by_piid.csv`, summed across all 89 in-scope PIIDs):

| FY | $M in-scope first-tier subawards | Records | Notes |
|---:|---:|---:|---|
| 2002 | 3.7 | 1 | Historical residual |
| 2013–2014 | 87 | 414 | Pre-window |
| 2015 | 147 | 290 | Pre-window |
| 2016 | 159 | 541 | Pre-window |
| 2017 | 149 | 517 | Pre-window |
| 2018 | 365 | 1,380 | FY18-22 MYP master awarded |
| 2019 | 2,089 | 3,336 | Mk 41 VLS production ramp |
| 2020 | 2,300 | 3,453 | Aegis hardware + ESSM EMD |
| 2021 | 3,167 | 2,595 | CIWS + Aegis CSEA + SPY-6 EMD |
| 2022 | ~2,000 | ~2,200 | (estimated from corresponding FPDS obligation rhythm) |
| 2023 | ~1,800 | ~2,500 | FY23-27 MYP master awarded; SPY-6 production ramp |
| 2024 | ~1,300 | ~2,500 | |
| 2025 | ~400 | ~700 | Reporting lag — subawards filed against recent prime obligations are slow |
| 2026 | <100 | <100 | Reporting still in progress |

(FY2022 forward is reported as approximate because the exact figure depends on the choice of action-date vs reporting-date attribution and on the cutoff date of the pull, May 23, 2026.)

The **FY2021 peak at $3.17B** is dominated by the CIWS PIID `N00024-18-C-5406` (which by itself is approximately $1.05B of FY21 subaward activity) and the Aegis CSEA PIID `N00024-13-C-5116` (which approaches $0.56B of FY21 activity, reflecting late-block subaward filings against the FY13 master contract). Smaller contributions from the Mk 41 VLS PIIDs round out the year. The 2019–2021 multi-year peak coincides with the SPY-6 EMD-to-production transition and the FY18-22 MYP block execution.

The **FY2023-onward declining trend in the annual figures** is mostly an artifact of FFATA reporting lag: the actual subaward activity against the FY23-27 MYP master and the FY24 single-year buy is still accumulating in the FFATA filings as of the May 2026 pull date. Three to four years of additional reporting lag would be required before the FY2023–FY2025 annual figures stabilize.

## Top first-tier subaward recipients (by lifetime in-scope $)

The top 25 recipients across the in-scope subaward stream are presented in chapter 6 (Vendors and concentration); the headline observation here is that the top 25 recipients account for approximately $7.3 billion of the $13.84 billion in-scope flow — roughly **53 percent supplier concentration** at the parent-UEI level. The single largest recipient is **Leonardo S.p.A.** (via its DRS Defense Solutions subsidiary), at approximately $2.02 billion of FFATA-visible flow across 557 subaward records spanning 14 in-scope PIIDs — primarily on the Lockheed Martin Mk 41 VLS, Aegis hardware, and Aegis SI&T contracts.

## What FFATA does not capture (the gap)

The FFATA-visible first-tier subaward stream is structurally and definitionally narrower than the actual yard-side outsourcing flow. The categories that FFATA does not capture, in order of estimated dollar materiality:

1. **Purchased material booked as direct material cost.** When a yard purchases steel plate, prefabricated piping, or major HM&E components (main reduction gears, generators) and books the purchase under direct-material cost in its accounting system rather than under a subcontract clause, the purchase is not FFATA-reportable. For the two destroyer yards combined, direct-material purchasing is estimated at hundreds of millions of dollars per year, likely the single largest invisible category.
2. **Lower-tier subcontracts.** A subcontract issued by a first-tier subawardee to its own supplier is not FFATA-reportable. For example, Lockheed Martin's Mk 41 VLS supplier base includes Major Tool & Machine, Merrill Aviation, and others — these appear in FFATA as LM Mk 41 first-tier subs. But *their* suppliers (raw-material vendors, specialty machinists, electronics distributors) do not appear in FFATA at all.
3. **FFATA non-compliance and under-reporting.** Independent audits have identified compliance gaps across the federal prime base. The single most striking discrepancy in the destroyer corpus is the FY23-27 BIW multiyear master PIID `N00024-23-C-2305` with zero published subawards at the May 2026 pull date — a near-certain reporting-compliance gap rather than a real-zero subaward activity.
4. **Long-term supplier agreements not subordinated to the prime contract.** Standing pricing agreements with material suppliers that pre-date the prime contract and are not modified or referenced in the prime are not FFATA-reportable.
5. **The sub-$30,000 long tail.** Subaward actions below the reporting threshold ($30,000 per individual action) are not reportable. Although individually small, the cumulative dollar value of the long tail is non-trivial; for high-action-count primes (Lockheed Martin Mk 41 VLS at 834 actions, Raytheon CIWS at 3,661 actions), the sub-threshold actions could represent 5–10 percent of true total subaward activity.

The total invisible-flow estimate from chapter 9 — combined yard-side outsourcing across both yards at approximately $1.8 billion per year against approximately $286 million per year visible in FFATA — implies that FFATA captures approximately **15 percent of the real yard-outsourcing flow**. The remaining 85 percent is distributed across the five invisible categories above, with direct-material booking and lower-tier subs being the two largest contributors.
