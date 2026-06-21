---
title: FFATA-visible first-tier subawards
---

# FFATA-visible first-tier subawards

The Federal Funding Accountability and Transparency Act of 2006 (FFATA, Pub. L. 109-282) and its implementing Federal Acquisition Regulation clause FAR 52.204-10 require prime contractors on federally funded contracts to report each first-tier subaward action above the $30,000 threshold to the federal government. The filings flow into the FFATA Subaward Reporting System (FSRS) and are made publicly accessible via SAM.gov. The FFATA stream is the most directly named-vendor source of information about which firms the prime contractor pays under its prime contracts.

This chapter sets out what the FFATA-visible first-tier subaward stream reports for the fifteen in-scope submarine new-construction PIIDs, excluding the three named Maritime Industrial Base recipient parent legal entities (BlueForge Alliance, Training Modernization Group, Institute for Advanced Learning and Research). The principal headlines are that the publicly visible FFATA stream captures approximately **$6.1 billion of cumulative subaward value FY2016 through FY2026 across approximately 759 unique parent vendors**, that the year-over-year stream shows a sharp inflection in fiscal year 2023 that is independent of (and additional to) the Maritime Industrial Base ramp, and that the cumulative FY2022 through FY2024 visible-subaward-to-Basic-Construction ratio is approximately **20.2 percent** — a measurement that should be read as a floor, not a ceiling, on the true outsourced share within Basic Construction (which the cost-funnel framework places at 50 to 65 percent).

## Why SAM.gov FFATA / FSRS is the authoritative source

Two separate publicly accessible federal data systems carry subaward data: the FFATA Subaward Reporting System accessed via SAM.gov, and USAspending.gov's `/api/v2/subawards/` endpoint. The two systems originate from the same underlying FFATA filings but differ materially in their data-handling characteristics.

The article uses **SAM.gov FFATA / FSRS as the authoritative source** for two reasons:

1. **SAM.gov has no per-prime retrieval cap.** USAspending's subawards endpoint imposes a practical limit of approximately 2,000 records per prime contract. Both Virginia Block V / VI master `N0002417C2100` and Columbia Build I + II master `N0002417C2117` exceeded this cap by the FY2023 reporting cycle. SAM.gov, by contrast, returns the full per-prime record count — 5,681 records for `N0002417C2100` and 5,208 records for `N0002417C2117` at the full-history (FY2008 through May 2026) accessor cycle. The long tail of small subawards on the two largest masters is captured in SAM.gov and not in USAspending.[^sam-vs-usaspending]
2. **SAM.gov filings carry a unique `subAwardReportId` per filed action**, which provides a clean primary key for deduplication without requiring multi-stage cumulative-snapshot resolution.

For the per-fiscal-year figures presented below, this article uses SAM.gov FFATA records filtered to the fifteen in-scope new-construction PIIDs and excluded for the three named MIB pass-through parent legal entities, summed by `subAwardDate` fiscal year and by class-of-prime PIID.

## Per-fiscal-year visible subaward flow

The table reports the per-fiscal-year aggregate of all SAM.gov FFATA-visible first-tier subaward dollars filed against the fifteen in-scope new-construction PIIDs, with the three named Maritime Industrial Base recipient parents excluded. All values are in nominal millions of dollars.

| FY | Virginia $M | Columbia $M | Other class $M | All in-scope $M |
|---:|---:|---:|---:|---:|
| 2016 | 0.9 | 3.4 | -0.1 | 4.4 |
| 2017 | 173.8 | 1.2 | 0.0 | 175.0 |
| 2018 | 44.0 | 8.1 | 0.0 | 52.2 |
| 2019 | 223.2 | 116.6 | 0.0 | 339.8 |
| 2020 | 198.9 | 154.4 | 0.0 | 353.3 |
| 2021 | 430.9 | 144.0 | 0.0 | 574.9 |
| 2022 | 240.8 | 293.0 | 0.3 | 534.1 |
| 2023 | 939.6 | 1,107.6 | 0.3 | 2,047.5 |
| 2024 | 461.9 | 838.0 | 0.4 | 1,300.2 |
| 2025 | 256.6 | 495.8 | 5.3 | 757.6 |
| 2026 | 0.0 | 0.0 | 0.3 | 0.3 |

Five observations:

1. **The fiscal-year 2023 inflection is real and additional to BlueForge.** The published headline that "BlueForge drives the FY2023-FY2024 ramp" applies to the broader subaward dataset that includes Maritime Industrial Base pass-throughs. After BlueForge, Training Modernization Group, and Institute for Advanced Learning and Research are excluded, the residual ex-MIB ramp still shows a 4× increase between FY2022 and FY2023 (from $534 million to $2,048 million). The non-MIB ramp is driven by Northrop Grumman, the Curtiss-Wright family of firms, Scot Forge, ESCO Technologies, and the broader conventional supplier base — not by the consortium pass-through.
2. **FY2025 is reporting-lag-depressed.** The reported $758 million for FY2025 is consistent with approximately 6 to 18 months of FFATA reporting lag against a year of FPDS prime-contract activity comparable to FY2024. The true FY2025 figure will revise upward as filings catch up over the following 12 to 18 months.
3. **FY2026 is essentially empty for the same reason.** Only $0.3 million is reported as of May 2026, reflecting actions on the BAE forward-subassembly PIID. The bulk of FY2026 subaward activity will appear in the FFATA stream over fiscal years 2027 and 2028 as filings catch up.
4. **The Columbia share dominates from FY2023 onward.** Through FY2022, Virginia subaward dollars exceeded Columbia. From FY2023 onward, Columbia subaward dollars exceed Virginia by approximately 2x even after the BlueForge pass-through is excluded — consistent with the Columbia program being in its lead-boat-plus-second-hull construction phase with concentrated component procurement.
5. **Most of the in-scope PIIDs contribute nothing to the FFATA-visible stream.** Of the fifteen in-scope new-construction PIIDs, only seven contribute non-zero FFATA-visible subaward dollars across the FY2016-FY2026 window. PIIDs that returned zero records include the Lockheed Martin Virginia combat-systems prime `N0002410C6266`, the Virginia Payload Module Tube Fabrication prime `N0002410C2118`, the BPMI S9G reactor prime `N0002424C2114`, and several smaller GFE primes. The zero-record observation is itself diagnostic: some primes either do not pass the $30,000-per-action threshold often, do not file FFATA in compliance, or route their subawards through standing supply agreements that fall outside the FFATA definition.

## The two main masters carry the bulk of the visible flow

Two prime PIIDs account for the majority of the FFATA-visible subaward flow across the window:

- **`N0002417C2100`** — Virginia Block V / VI master, awarded to GDEB in 2017. Lifetime FFATA-visible subaward total approximately $2.15 billion in scope (ex-MIB).
- **`N0002417C2117`** — Columbia Build I / II master, awarded to GDEB in 2017. Lifetime FFATA-visible subaward total approximately $2.75 billion in scope (ex-MIB).

The two together account for approximately $4.9 billion of the in-scope $6.1 billion cumulative FFATA-visible flow, or 80 percent. The remaining 20 percent distributes across smaller GDEB construction primes (Virginia Block VI LLTM `N0002424C2110`, Virginia Payload Module Vent Valve `N0002416C2111`, Columbia Design Drawings `N0002413C2128`), the BPMI Columbia Industrial Base Increase prime `N0002419C2115`, the BPMI Naval Reactor Components prime `N0002419C2114`, and the smaller BAE / Rolls-Royce / Lockheed primes.

The concentration of FFATA-visible flow on the two largest masters mirrors the structure of submarine procurement itself — the two block-level master contracts are where the construction-phase work content is contractually concentrated — but is also a function of the FFATA reporting threshold. Larger primes with larger subcontracts more frequently exceed the $30,000-per-action threshold and so populate the FFATA stream more densely.

## Pre-FY2020 history and the Block IV recovery

A separate full-history accessor cycle against SAM.gov FFATA covering action dates back to fiscal year 2008 (the start of FSRS coverage) recovers an additional 5,114 records and approximately $3.4 billion of pre-FY2020 subaward activity across the in-scope PIIDs. Most notably, the Virginia Block IV master `N0002412C2115` — which returned zero records in a fiscal-year-2020-onward windowed pull despite being a real and active multi-billion-dollar submarine construction contract — recovers 1,622 records totaling approximately $234 million in the full-history accessor. The pre-FY2020 records are not included in the per-fiscal-year table above because the article's substantive coverage starts FY2018, but they confirm that the per-fiscal-year FFATA stream is consistent with the broader history of these prime contracts.

## Visible-subaward-to-Basic-Construction ratio

The FFATA-visible first-tier subaward stream can be expressed as a percentage of the SCN Exhibit P-5c Basic Construction line for the same fiscal year and class. The per-fiscal-year ratio is lumpy because Basic Construction is a per-ship-as-of-authorization figure while subaward dollars are cash-flow that fiscal year across all active ships and blocks; a cumulative ratio across a multi-year window is the cleaner measurement.

| FY | Combined Basic Construction $M | Combined visible subs $M | Visible / BC % |
|---:|---:|---:|---:|
| 2021 | 5,979 (Col only) | 575 | 9.6% |
| 2022 | 4,758 (Va only) | 534 | 11.2% |
| 2023 | 5,095 (Va only) | 2,048 | 40.2% |
| 2024 | 15,427 (Va + Col) | 1,300 | 8.4% |
| 2025 | 5,327 (Va only) | 758 | 14.2% (lag) |
| 2026 | 10,297 (Va + Col) | 0.3 | ~0% (lag) |
| **FY22-FY24 cumulative** | **25,280** | **3,882** | **15.4%** |
| **FY22-FY24 cumulative (Va + Col procurement years only, more stable)** | **19,259** | **3,882** | **20.2%** |

The cumulative FY2022 through FY2024 visible-to-BC ratio of approximately **20.2 percent** is the most stable single measurement of the visible-FFATA layer relative to Basic Construction. It reflects three full fiscal years of activity before the reporting-lag impact on FY2025 and FY2026, and it averages across the per-fiscal-year procurement-cadence lumpiness. The FY2023 spike of 40.2 percent is real (the genuine FY23 inflection noted above) but is sensitive to the mismatch between which class procures in which year.

The 20.2 percent FFATA-visible / Basic Construction ratio is approximately one-third of the 60-percent mid-case outsourced share derived from the cost-funnel framework in [chapter 6](06-outsourced-band-within-bc.md) and approximately one-quarter of the 78-percent Outside-EB share documented in the DoD-announcement corpus in [chapter 7](07-dod-contract-announcement-data.md). The gap is the unseen layer addressed in [chapter 12](12-unseen-layer.md).

## SAM.gov compared to USAspending

A side-by-side comparison of the SAM.gov FFATA / FSRS data against the USAspending `/api/v2/subawards/` data for the same prime PIIDs illustrates the per-prime retrieval-cap problem that motivates this article's use of SAM.gov as the authoritative source:

| PIID | USAspending records | USAspending $M | SAM.gov records (full history) | SAM.gov $M (full history) |
|---|---:|---:|---:|---:|
| `N0002417C2100` (Va V/VI master) | 2,500 (cap) | ~4,190 | 5,681 | 4,176 |
| `N0002417C2117` (Col Build I+II master) | 2,500 (cap) | ~8,170 | 5,208 | 7,749 |
| `N0002412C2115` (Va Block IV MYP) | 0 (no records returned) | 0 | 1,622 | 234 |
| `N0002424C2110` (Va Block VI LLTM) | 367 | 417 | 367 | 417 |
| `N0002413C2128` (Col Design Drawings) | 54 | 12 | 608 | 274 |
| `N0002419C2114` (BPMI Reactor Components) | 39 | 91 | 49 | 146 |
| `N0002419C2115` (BPMI Col Class IBI) | 44 | 166 | 67 | 528 |

The retrieval-cap and date-window differences between the two sources are systematic. USAspending caps at approximately 2,500 records per prime in the available paginated retrieval; SAM.gov has no per-prime cap. USAspending's accessor is more easily integrable for many use cases but cannot be used as the authoritative source for the largest submarine masters. The SAM.gov full-history accessor recovers the long tail (approximately 3,500 records on `N0002417C2100`) and the entire Virginia Block IV history that USAspending returns as empty.

## Geographic registration

The geographic distribution of the FFATA-visible first-tier subaward stream by recipient registered address — separate from the place-of-performance data in [chapter 7](07-dod-contract-announcement-data.md) — concentrates in a small number of U.S. states. Across the in-scope FFATA records:

| State | Cumulative $M | Share of US-vendor $ |
|---|---:|---:|
| California | 1,539 | 25.9% |
| Pennsylvania | 760 | 12.8% |
| Massachusetts | 579 | 9.7% |
| Wisconsin | 473 | 8.0% |
| New Jersey | 301 | 5.1% |
| New York | 295 | 5.0% |
| Illinois | 220 | 3.7% |
| Connecticut | 196 | 3.3% |
| Virginia | 185 | 3.1% |
| Florida | 159 | 2.7% |
| Alabama | 91 | 1.5% |
| (other states, each <2.5%) | ~1,140 | ~19% |

The top five states (California, Pennsylvania, Massachusetts, Wisconsin, New Jersey) account for approximately 60 percent of the U.S.-vendor visible dollars. The geographic distribution **reflects vendor registered address, not work location**: a firm headquartered in California may perform work at facilities in Pennsylvania (as is the case for portions of Lockheed Martin's submarine combat-systems content) or at other sites. Connecticut at 3.3 percent reflects the fact that GDEB itself is the prime contractor, not a subaward recipient; subaward dollars flowing to firms in Connecticut are a small share of the total.

Foreign-registered vendor share is approximately 3 percent of total FFATA-visible flow, distributed as follows: United Kingdom $161 million (principally Babcock Marine Rosyth and Rolls-Royce UK content); Switzerland $33 million (APCO Technologies SA — Common Missile Compartment launch-tube content); Canada $8 million; smaller amounts to Denmark, Brazil, and China. Foreign content is concentrated on Columbia (Babcock Rosyth, APCO Technologies) rather than Virginia, reflecting the Columbia program's shared design lineage with the United Kingdom Dreadnought class.

## What the FFATA stream does not capture

By construction, the FFATA first-tier subaward stream excludes several categories of dollars that are nonetheless part of the outsourced layer:

1. **Purchased material booked as direct material** rather than as subcontract — for example, raw material, parts, and components procured under standing supply agreements that pre-date the prime contract or that are formally categorized as material rather than subcontract.
2. **Lower-tier subcontracts beneath the FFATA first tier** — a subcontract of a subcontract is not reportable. Material that flows GDEB → tier-1 supplier → tier-2 supplier is captured at the tier-1 level only.
3. **Indirect and general-and-administrative items**, which are explicitly excluded by FAR 52.204-10.
4. **The portion of the HII Newport News team-build share that flows through GDEB as the vendor of record but is not separately filed as an HII-as-sub-of-GDEB subaward**. The FFATA-visible HII-as-sub flow is approximately $98 million cumulative across the FY2016-FY2026 window — vastly understating the true HII workshare. See [The HII Newport News visibility gap](11-hii-newport-news-gap.md).
5. **Actions below the $30,000 per-action threshold**, which can collectively account for material total dollars on a long-tail basis.
6. **Filings by primes that systematically under-report.** GDEB does file FFATA on its major submarine primes. Several other Navy shipbuilders — including Bath Iron Works on DDG-51, Bollinger Shipyards on certain U.S. Coast Guard cutter contracts, and several foreign-headquartered primes on specific submarine GFE work — are documented as filing zero FFATA subawards despite multi-billion-dollar prime obligations. See [The unseen layer](12-unseen-layer.md).

The next chapter takes the visible-vendor stream documented here and characterizes the supplier base it surfaces: top vendors by parent legal entity, North American Industry Classification System work-type mix, and the trajectory of supplier-base structure over the FY2016-FY2026 window.

## Cross-references

- For the cost-funnel framework that this stream sizes against: [The outsourced layer within Basic Construction](06-outsourced-band-within-bc.md).
- For the direct primary-source measurement of outsourced share: [DoD contract announcement data](07-dod-contract-announcement-data.md).
- For vendor characterization (NAICS, concentration, top vendors): [Vendors and concentration](09-vendors-and-concentration.md).
- For the Maritime Industrial Base pass-through layer (BlueForge, TMG, IALR): [The Maritime Industrial Base layer](10-maritime-industrial-base.md).
- For the HII Newport News team-build gap: [The HII Newport News visibility gap](11-hii-newport-news-gap.md).
- For the broader unseen layer: [The unseen layer](12-unseen-layer.md).
- For the SAM.gov FSRS / SAM Entity Management API methodology: [Data sources, pipeline, and limitations](16-data-sources-pipeline-limitations.md).

[^sam-vs-usaspending]: The 2,500-record practical retrieval cap on USAspending's `/api/v2/subawards/` endpoint is observed empirically across multiple submarine PIIDs and is consistent with the 25-page-by-100-record pagination structure exposed by the endpoint. The SAM.gov FFATA subcontracts search API exposes per-record `subAwardReportId` as a primary key and returns paginated record counts up to the system-of-record total per prime PIID.
