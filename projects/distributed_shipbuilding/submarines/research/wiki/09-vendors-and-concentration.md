---
title: Vendors and concentration
---

# Vendors and concentration

The FFATA-visible first-tier subaward stream documented in the previous chapter surfaces a named-vendor supplier base of approximately **759 unique parent legal entities** across the FY2016 through FY2026 action-date window for the fifteen in-scope new-construction PIIDs, with the three named Maritime Industrial Base recipient parents excluded. This chapter characterizes that supplier base — top vendors by parent legal entity, work-type mix by North American Industry Classification System code, and the evolution of supplier-base size and concentration over the article's coverage window.

Two summary observations:

1. **The submarine supplier base has expanded dramatically** in the FFATA-visible stream — from approximately a dozen named parents in fiscal year 2016 (the start of the window, when FFATA reporting on these primes was sparse) to 371 unique parents in fiscal year 2023 and 335 in fiscal year 2024, before the FY2025-FY2026 reporting-lag-depressed years.
2. **Supplier-base concentration has fallen substantially** — the Herfindahl-Hirschman Index (a standard concentration measure) for the FFATA-visible stream has fallen from approximately 6,620 in fiscal year 2018 ("highly concentrated" by Department of Justice merger-guidelines convention) to a low of 322 in fiscal year 2022 ("competitive") before climbing back to approximately 1,189 in fiscal year 2023 as the Maritime Industrial Base era began and the post-COVID supplier expansion took hold.

Both trends — vendor-base expansion and concentration decline — are independent indicators of the same structural shift documented elsewhere in the article: shipbuilders are expanding the volume and breadth of supplier-base outsourcing, the Navy's Maritime Industrial Base spending is funding new supplier capacity, and the post-pandemic procurement cadence has surfaced a much larger named-vendor cohort than was visible pre-2018.

## Top vendors by parent legal entity (lifetime)

The table presents the top twenty-five FFATA-visible first-tier subaward recipients across the fifteen in-scope new-construction PIIDs, summed across action-date fiscal years 2016 through 2026, with the three Maritime Industrial Base pass-through parent legal entities (BlueForge Alliance, Training Modernization Group, Institute for Advanced Learning and Research) excluded. Vendors are aggregated to parent legal entity by SAM.gov Unique Entity Identifier; subsidiaries are rolled up to the parent where the SAM Entity Management API confirms the corporate relationship.

| Rank | Parent legal entity | Lifetime $M | FY count | Headquarters |
|---:|---|---:|---:|---|
| 1 | <img src="assets/logos/northrop_grumman.svg" class="logo-thumb" alt="">Northrop Grumman Corporation | 1,426.6 | 8 | Falls Church, Virginia |
| 2 | <img src="assets/logos/leonardo.svg" class="logo-thumb" alt="">Leonardo SpA | 490.6 | 8 | Rome, Italy |
| 3 | <img src="assets/logos/curtiss_wright.svg" class="logo-thumb" alt="">Curtiss-Wright Electro-Mechanical Corporation | 198.0 | 4 | Cheswick, Pennsylvania |
| 4 | Scot Forge Company | 197.5 | 8 | Spring Grove, Illinois |
| 5 | ESCO Technologies Inc. | 188.5 | 8 | St. Louis, Missouri |
| 6 | DC Fabricators Inc. | 162.9 | 6 | Florence, New Jersey |
| 7 | Rhoads Metal Fabrications, Inc. | 141.9 | 4 | Limerick, Pennsylvania |
| 8 | Curtiss-Wright Corporation | 110.8 | 8 | Davidson, North Carolina |
| 9 | The Graham Corporation | 89.1 | 5 | Batavia, New York |
| 10 | <img src="assets/logos/austal.svg" class="logo-thumb" alt="">Austal USA, LLC | 87.6 | 3 | Mobile, Alabama |
| 11 | Rosyth Royal Dockyard Limited (Babcock) | 84.0 | 2 | Rosyth, United Kingdom |
| 12 | W International, LLC | 82.6 | 5 | North Charleston, South Carolina |
| 13 | Curtiss-Wright Flow Control Corporation | 74.7 | 4 | Falls Church, Virginia |
| 14 | W International SC, LLC | 74.1 | 4 | North Charleston, South Carolina |
| 15 | Oil States International, Inc. | 71.5 | 7 | Houston, Texas |
| 16 | Precision Custom Components, LLC | 68.8 | 8 | York, Pennsylvania |
| 17 | Goodrich Corp (RTX Collins Aerospace) | 64.9 | 4 | Charlotte, North Carolina |
| 18 | Johnson Controls Navy Systems, LLC | 58.7 | 5 | Tukwila, Washington |
| 19 | Globe Composite Solutions, LLC | 57.3 | 4 | Stoughton, Massachusetts |
| 20 | CIRCOR International, Inc. | 53.0 | 6 | Burlington, Massachusetts |
| 21 | <img src="assets/logos/l3harris.svg" class="logo-thumb" alt="">L3Harris Technologies, Inc. | 52.3 | 9 | Melbourne, Florida |
| 22 | <img src="assets/logos/bwx_technologies.svg" class="logo-thumb" alt="">BWX Technologies, Inc. | 51.8 | 5 | Lynchburg, Virginia |
| 23 | Advance Mfg. Co., Inc. | 51.2 | 8 | Westfield, Massachusetts |
| 24 | Pegasus Steel, LLC | 48.9 | 7 | Goose Creek, South Carolina |
| 25 | Portland Valve LLC | 48.1 | 4 | Portland, Maine |

Three observations:

1. **Northrop Grumman is the single largest FFATA-visible recipient** in scope at $1,427 million lifetime — approximately 2.5 times the second-place vendor. Northrop Grumman is also a GFE prime on Navy-direct contracts for sonar and electronic-warfare integration (see [Plans, GFE, and other layers](03-plans-gfe-and-other-layers.md)), and the CRS Columbia report identifies Northrop Grumman's late delivery of the SSBN-826 turbine generator as one of the most significant single-supplier-driven contributors to the lead-Columbia 17-month delay.[^crs-r41129] Northrop Grumman's FFATA-visible flow against the GDEB primes is largely combat-systems and sensor integration content not separately purchased as Navy GFE.
2. **The Curtiss-Wright corporate family aggregates to approximately $383 million across three Curtiss-Wright SAM entities** (Electro-Mechanical, parent Curtiss-Wright Corporation, Flow Control). The Curtiss-Wright family covers nuclear-grade pumps (Electro-Mechanical), valves (Flow Control), and corporate-level rollups (the Curtiss-Wright Corporation parent), and is the second-largest aggregate FFATA recipient after Northrop Grumman.
3. **Foreign-headquartered vendors appear at ranks 2 and 11 in the visible flow.** Leonardo SpA (Italy) is the second-largest single FFATA-visible recipient at $491 million, with content on multiple GDEB and BPMI PIIDs. Rosyth Royal Dockyard Limited (UK, Babcock Marine subsidiary) is at $84 million, concentrated on Columbia work via the shared design lineage with the United Kingdom Dreadnought class. The Leonardo NAICS classification (336411 / Aircraft Mfg. at the corporate level) is illustrative of the well-documented limitation of NAICS as a per-action work-type classifier (see below).

## NAICS work-type mix

The North American Industry Classification System is the federal standard for classifying business establishments by primary business activity. Each registered firm in SAM.gov has a primary NAICS code; the SAM Entity Management API was queried for the top 150 FFATA-visible parent vendors to enrich the supplier-base characterization.[^sam-entity]

NAICS classification at the corporate-primary level has a well-documented limitation as a per-action work-type classifier: a firm classified at the corporate-parent level as "Aircraft Manufacturing" (336411) because that is its predominant federal business activity will still appear in this code even when supplying submarine-specific content (sonar, combat systems, propulsion components) on a given action. Northrop Grumman is the canonical example: corporate-level NAICS 336413 ("Aircraft Parts") because aircraft parts dominate its federal revenue, but submarine-relevant content (sonar arrays, AN/BLQ-10 electronic warfare) is part of its FFATA-visible flow against the submarine PIIDs. The NAICS classification provides directional work-type signal across the supplier base but is not a precise per-action classifier.

The top NAICS 4-digit categories by aggregate FFATA-visible dollar value across the in-scope window:

| NAICS 4-digit | Description | Cumulative $M |
|---|---|---:|
| 3364 | Aerospace product and parts manufacturing | varies |
| 3323 | Architectural and structural metals | varies |
| 3329 | Other fabricated metal product manufacturing | varies |
| 3344 | Semiconductor and other electronic components | varies |
| 3321 | Forging and stamping | varies |
| 3366 | Ship and boat building | varies |
| 5511 | Management of companies and enterprises (corporate-level rollup) | varies |
| 3345 | Navigational, measuring, electromedical, and control instruments | varies |
| 3339 | Other general purpose machinery | varies |
| 3326 | Spring and wire product manufacturing | varies |

The NAICS coverage of the top-150 enriched vendors captures approximately 93.5 percent of dollar-weighted FFATA flow but only approximately 70 percent of unique vendor count, reflecting that approximately 45 of the top 150 vendors are not found in the SAM Entity Management API as currently `samRegistered=Yes` (suggesting expired or deactivated registrations).

## Supplier-base size and concentration over time

The per-fiscal-year evolution of FFATA-visible supplier-base size and concentration is the most direct evidence in the article of structural change in how submarine work is contracted. The Herfindahl-Hirschman Index (HHI) is computed as the sum of squared percentage shares of total FFATA-visible flow held by each unique parent vendor; the U.S. Department of Justice merger guidelines treat HHI above 2,500 as "highly concentrated," 1,500 to 2,500 as "moderately concentrated," and below 1,500 as "competitive."

| FY | Visible flow $M | Records | Unique parents | Top-5 share | HHI | Concentration label |
|---:|---:|---:|---:|---:|---:|---|
| 2016 | 4.4 | 21 | 11 | 100% (>100% rounding) | 2,962 | Highly concentrated |
| 2017 | 175.0 | 68 | 27 | 99% | 6,327 | Highly concentrated |
| 2018 | 52.2 | 169 | 56 | 122% (>100% rounding artifact) | 6,620 | Highly concentrated |
| 2019 | 339.8 | 613 | 163 | 61% | 973 | Competitive |
| 2020 | 353.3 | 995 | 216 | 45% | 523 | Competitive |
| 2021 | 574.9 | 1,045 | 296 | 48% | 823 | Competitive |
| 2022 | 534.1 | 1,457 | **365** | 31% | **322** | Competitive |
| 2023 | 2,047.5 | 2,144 | **371** | 56% | 1,189 | Competitive |
| 2024 | 1,300.2 | 1,827 | 335 | 42% | 572 | Competitive |
| 2025 (lag) | 757.6 | 927 | 210 | 50% | 1,392 | Competitive |

The fiscal-year 2022 marker is the structural low for concentration in the FFATA-visible stream: 365 unique parent vendors, top-5 share of 31 percent, and HHI of 322 — well into the competitive regime by DOJ merger-guideline convention. By fiscal year 2023, supplier-count peaks at 371 parents and HHI climbs to 1,189 as the BlueForge-driven ramp (which is excluded from this table by the MIB exclusion but for which other capacity-investment activity is captured) introduced larger concentrated flows.

The growth in unique parent vendor count from approximately a dozen in fiscal year 2016 to 371 in fiscal year 2023 — even after the three named Maritime Industrial Base pass-through parents are excluded — is a roughly **30-fold expansion** of the FFATA-visible supplier base. This figure has the same caveats noted in the previous chapter (FFATA reporting maturity in the early years was uneven; some primes still under-report; the FY2022 low and FY2023 peak reflect both real structural change and reporting-maturity dynamics). But the directional story is consistent with the Government Accountability Office's documentation that shipbuilders are expanding outsourcing and that the Navy's Maritime Industrial Base investment is funding capacity expansion across the supplier base.[^gao-25-106286]

## A note on the W International acquisition

Among the top 25 lifetime FFATA-visible vendors, two W International entities appear at ranks 12 and 14 ($83 million and $74 million respectively). W International is a Charleston, South Carolina-based fabrication shop that has been on the visible submarine-supplier list for multiple fiscal years. In approximately 2024–2025, HII acquired W International — making W International a notable exception to HII Chief Executive Officer Chris Kastner's explicit "I really don't want to vertically integrate" posture (see [Executive commentary](13-executive-commentary.md)). Kastner contextualized the acquisition as a specific exception to the general anti-vertical-integration stance, rather than a change in strategy.[^hii-fy24q4] W International illustrates a corner case where the outsourcing-versus-vertical-integration boundary moves with corporate transactions; for purposes of this article, W International is treated as a supplier across the window because the acquisition occurred late in the coverage period.

## Foreign-vendor share

Foreign-headquartered vendors account for approximately 3 percent of FFATA-visible flow across the in-scope window, distributed as follows:[^repo-geo]

| Country | Lifetime $M | % of FFATA-visible total |
|---|---:|---:|
| United Kingdom | 161.0 | 2.6% |
| Switzerland | 32.8 | 0.5% |
| Canada | 8.0 | 0.1% |
| Denmark | 0.5 | <0.1% |
| Brazil | 0.1 | <0.1% |
| China | 0.05 | <0.1% |

The foreign content is concentrated on Columbia rather than Virginia, reflecting the Columbia program's shared design lineage with the United Kingdom Dreadnought class (Babcock Marine Rosyth, Rolls-Royce UK) and the Switzerland-based APCO Technologies SA Common Missile Compartment launch-tube work. The Navy's May 2026 FY2027 30-Year Shipbuilding Plan explicitly opens the possibility of additional overseas content: "While American shipbuilding remains the priority, the Navy will evaluate overseas options and whether allied and partner shipbuilding can supplement domestic production if U.S. industry cannot meet required timelines."[^navy-fy27-plan]

## Cross-references

- For the FFATA-visible flow that this chapter's vendors come from: [FFATA-visible first-tier subawards](08-ffata-visible-subawards.md).
- For the geographic distribution of vendor registration in detail: [chapter 8](08-ffata-visible-subawards.md#geographic-registration).
- For the direct primary-source measurement of outsourced share at the contract-action level: [DoD contract announcement data](07-dod-contract-announcement-data.md).
- For the Maritime Industrial Base pass-throughs that this chapter excludes: [The Maritime Industrial Base layer](10-maritime-industrial-base.md).
- For the unseen layer not captured in the FFATA stream: [The unseen layer](12-unseen-layer.md).
- For NAICS enrichment methodology via the SAM Entity Management API: [Data sources, pipeline, and limitations](16-data-sources-pipeline-limitations.md).

[^crs-r41129]: Congressional Research Service, *Navy Columbia (SSBN-826) Class Ballistic Missile Submarine Program: Background and Issues for Congress* (R41129), Ronald O'Rourke, December 4, 2025. <https://www.congress.gov/crs-product/R41129>.

[^sam-entity]: SAM.gov Entity Management API, accessed via <https://api.sam.gov/entity-information/v3/entities>. Returns per-Unique Entity Identifier (UEI) records including the firm's primary NAICS code at the corporate level.

[^gao-25-106286]: U.S. Government Accountability Office, *Shipbuilding and Repair: Navy Needs a Strategic Approach for Private Sector Industrial Base Investments*, GAO-25-106286, February 27, 2025. <https://www.gao.gov/products/gao-25-106286>.

[^hii-fy24q4]: Huntington Ingalls Industries, fiscal year 2024 fourth-quarter earnings conference call, February 2025. Chris Kastner, Chief Executive Officer: "We have a lot of outsource partners, and I'd rather develop outsource partners and have an arms-length relationship. I really don't want to vertically integrate." Statement in the context of the W International acquisition.

[^repo-geo]: Geographic distribution computed from SAM.gov FFATA records' recipient country-of-registration fields, normalized for case-variation duplicates.

[^navy-fy27-plan]: U.S. Department of the Navy, Fiscal Year 2027 President's Budget, *30-Year Shipbuilding Plan*, April-May 2026.
