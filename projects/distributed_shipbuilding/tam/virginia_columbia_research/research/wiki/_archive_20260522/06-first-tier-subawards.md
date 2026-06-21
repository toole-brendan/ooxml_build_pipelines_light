---
title: First-tier subawards and supplier visibility
---

# First-tier subawards and supplier visibility

First-tier subawards reported under the U.S. Federal Funding Accountability and Transparency Act of 2006 (FFATA) provide the most direct public view of work that the General Dynamics Electric Boat prime shipyard pays to other firms on Virginia-class and Columbia-class new construction. This chapter inventories the subaward data pulled for 17 in-scope submarine prime PIIDs, identifies the top first-tier recipients, and documents the structural visibility gaps that affect any aggregate reading of the data.

## Pull design

The subaward pull uses USAspending.gov's two-call workflow:[^repo-usaspending-script][^repo-lessons-v1]

1. For each in-scope PIID, POST to `/api/v2/search/spending_by_award/` with the PIID in the `award_ids` filter and the Contracts award-type-code group `[A, B, C, D]`; if zero results, retry with the IDV group `[IDV_A, IDV_B, IDV_B_A, IDV_B_B, IDV_B_C, IDV_C, IDV_D, IDV_E]`. The response yields a `generated_internal_id` (gid) for the prime award.
2. POST to `/api/v2/subawards/` with that gid, `limit=100`, `sort=amount`, `order=desc`, and page until the `page_metadata.hasNext` flag is false (maximum 25 pages, approximately 2,500 records).

The seed list of 17 PIIDs covers the major GDEB submarine construction vehicles (11 PIIDs), the major Bechtel Plant Machinery naval reactor vehicles (3 PIIDs), the Lockheed Martin Virginia combat-system vehicle (1 PIID), the BAE Systems forward-subassembly vehicle (1 PIID), and the Rolls-Royce North America Virginia-class rotor vehicle (1 PIID).[^repo-readme][^repo-usaspending-summary]

The pull is sorted by amount descending — the top spend is captured first, in case the prime hits the approximately 2,500-record retrieval cap (25 pages × 100 records per page) that the pull script applies in practice on the largest primes.

## What the seed PIIDs returned

The 17 seed PIIDs returned a combined approximately **12,650 subaward records**. Of these:[^repo-usaspending-summary]

- **2 PIIDs hit the retrieval cap** at approximately 2,500 records each (the pull script's 25-pages × 100-records-per-page ceiling): the GDEB Virginia Block V/VI master `N0002417C2100` (subaward total $4.19 billion) and the GDEB Columbia Build I+II `N0002417C2117` (subaward total $8.17 billion). For these two PIIDs, the long tail of small subs is missing; the top spend is captured.
- **5 PIIDs returned zero subawards**: `N0002409C2104` (Virginia Block II residual, mostly closed out), `N0002410C2118` (VPM Tube Fabrication, $1.42B prime, no FFATA reporting), `N0002411C2109` (SSBN-R concept formulation), `N0002424C2114` (BPMI FY26 Virginia Component Funding, too new), and `N0002410C6266` (LM Virginia Combat Systems, $899M prime, no FFATA reporting in the reviewed window).
- The remaining 10 PIIDs returned non-zero subaward counts ranging from 7 (Rolls-Royce Virginia Class Submarine Rotor, $4.7M) to 1,622 (Virginia Block IV `N0002412C2115`, $234M).

A summary table:

| PIID | Prime vendor | Prime cumulative ($M) | Subaward count | Subaward total ($M) |
|---|---|---:|---:|---:|
| `N0002417C2100` | GDEB | 34,664 | 2,500 (cap) | **4,192** |
| `N0002417C2117` | GDEB | 26,700 | 2,500 (cap) | **8,175** |
| `N0002412C2115` | GDEB | 19,898 | 1,622 | 234 |
| `N0002424C2110` | GDEB | 4,960 | 367 | 417 |
| `N0002409C2104` | GDEB | 16,239 | 0 | 0 |
| `N0002413C2128` | GDEB | 3,146 | 608 | 273 |
| `N0002419C2125` | GDEB | 1,370 | 1,292 | 241 |
| `N0002416C2111` | GDEB | 1,469 | 772 | 285 |
| `N0002410C2118` | GDEB | 1,418 | 0 | 0 |
| `N0002411C2109` | GDEB | 480 | 0 | 0 |
| `N0002420C4312` | GDEB | 1,333 | 430 | 116 |
| `N0002419C2114` | BPMI | 3,376 | 49 | 146 |
| `N0002419C2115` | BPMI | 3,005 | 67 | 528 |
| `N0002424C2114` | BPMI | 2,543 | 0 | 0 |
| `N0002410C6266` | LM | 899 | 0 | 0 |
| `N0002421C4106` | BAE | 85 | 14 | 1 |
| `N0002421C4111` | Rolls-Royce (Bird-Johnson) | 29 | 7 | 5 |

## Top first-tier subaward recipients across all submarine PIIDs

Across all 17 in-scope PIIDs combined and across the full FY2013–FY2025 action-date window, the top 20 first-tier subaward recipients are:[^repo-subaward-top]

| Rank | Recipient | Cumulative subaward ($M) | Primary program(s) | Role |
|---:|---|---:|---|---|
| 1 | **BlueForge Alliance** | **4,213.96** | Columbia (`N0002417C2117`) | SIB consortium pass-through — workforce, supplier development, capacity expansion |
| 2 | **Northrop Grumman Systems Corporation** | **2,210.48** | Virginia, Columbia | Sonar arrays, AN/BLQ-10 EW, combat systems; possibly includes HII-NNS team-build flow-through |
| 3 | Curtiss-Wright Electro-Mechanical Corporation | 515.47 | Virginia, Columbia, BPMI reactors | Reactor coolant pumps, motors, valves |
| 4 | DRS Naval Power Systems Inc | 477.15 | Columbia | Switchboards, power distribution |
| 5 | Scot Forge Company | 355.30 | Virginia, Columbia | Forgings (shafts, hull rings, structural) |
| 6 | BAE Systems Land & Armaments L.P. | 355.27 | Virginia Block V/VI master | Forward subassemblies, weapons handling |
| 7 | BWXT Nuclear Operations Group, Inc. | 289.87 | BPMI reactor PIIDs | Reactor cores, fuel modules |
| 8 | DC Fabricators Inc | 254.78 | Virginia | Hull structures, fabrication |
| 9 | Babcock Marine (Rosyth) Limited | 240.47 | Columbia | UK partner — Columbia design support, propulsion components |
| 10 | Globe Composite Solutions, LLC | 223.06 | Virginia | Composite structures |
| 11 | Precision Custom Components, LLC | 214.53 | Virginia, Columbia | Machined components |
| 12 | APCO Technologies SA (Switzerland) | 202.36 | Columbia | Launch-tube structural components |
| 13 | Rhoads Metal Fabrications, Inc. | 149.52 | Virginia, Columbia | Hull / structural fabrication |
| 14 | Johnson Controls Navy Systems, LLC | 126.99 | Virginia, Columbia | HVAC, chilled water |
| 15 | Curtiss-Wright Flow Control Corporation | 126.49 | Reactor PIIDs | Reactor coolant valves |
| 16 | Portland Valve LLC | 117.33 | Virginia, Columbia | Valves |
| 17 | Vacco Industries | 109.96 | Virginia, Columbia | Fluid-system components |
| 18 | Oil States Industries, Inc. | 104.64 | Virginia, Columbia | Sealing systems |
| 19 | Teledyne Instruments Inc | 103.51 | Virginia | Instrumentation |
| 20 | Huntington Ingalls Inc | 98.09 | Virginia Block V/VI master | **HII-NNS team-build portion visible as a sub of GDEB — vastly under-reports real share** (see [Government-furnished equipment and the team-build pattern](05-gfe-and-team-build.md)) |

The top-20 list captures approximately **$10.5 billion** of the visible subaward flow. Approximately **two-thirds of this is BlueForge Alliance and Northrop Grumman Systems combined**, both routed through GDEB prime PIIDs. (See [Maritime Industrial Base and BlueForge Alliance](07-maritime-industrial-base.md) for the BlueForge breakdown.)

The tail beyond rank 20 includes a wide range of smaller suppliers — additional forgers, machined-component shops, valve manufacturers, marine hardware distributors, and engineering services firms — across approximately 200 named recipients in the extracted top-200 file.[^repo-subaward-top]

## Subaward flow by fiscal year

Aggregating the same subaward data by `action_date` fiscal year and prime PIID gives the per-FY direct outsourcing flow visible in USAspending across the 12 PIIDs that returned non-zero subaward counts:[^repo-subaward-annual]

| FY | Total subaward $ ($M) | Major driver |
|---|---:|---|
| FY2013 | 0.03 | (residual) |
| FY2015 | 0.13 | (residual) |
| FY2016 | 206.00 | Block IV ramp |
| FY2017 | 1,307.23 | Block V signing on `N0002417C2100` ($991M) |
| FY2018 | 1,027.59 | Block V continuation |
| FY2019 | 1,456.40 | Block V + Columbia Build I awards |
| FY2020 | 353.45 | Trough |
| FY2021 | 825.54 | |
| FY2022 | 696.33 | |
| FY2023 | **3,813.30** | **Columbia BlueForge MIB ramp begins** ($2,754.59M on `N0002417C2117`) |
| FY2024 | **4,161.90** | **Peak** ($3,649.74M on `N0002417C2117`) |
| FY2025 | 766.45 | Likely reporting lag — expected to climb 12–18 months out |

The dominant signal is the FY2023–FY2024 jump from approximately $700 million per year to approximately $4 billion per year, driven almost entirely by the BlueForge Alliance consortium subaward on the Columbia Build I+II PIID `N0002417C2117`. The FY2025 trough is consistent with the typical 6–18 month FFATA reporting lag for fresh prime contracts and is expected to be revised upward as the data ages.[^repo-lessons-v1]

Note that this table reports the **full 12-PIID** subaward universe, which includes the BPMI naval-reactor PIIDs' own first-tier subawards (about $462M in FY2019, $93M in FY2020, $119M in FY2021, and smaller amounts in other years). The headline in [Annual outsourced flow estimate](08-annual-outsourced-flow.md) uses the **GDEB-prime-only** subset of this column (8 of the 12 PIIDs), to avoid double-counting BPMI flow that is already captured under the BPMI FPDS prime obligations pillar.

## Per-PIID first-tier subaward composition

The top first-tier recipients differ substantially between the two large GDEB master vehicles.

### Virginia Block V/VI master (`N0002417C2100`)

Top recipients in companion analysis of this $4.14 billion visible subaward tree (record-cap hit):[^repo-sam-prior]

| Recipient | Subaward $ (M) | Role |
|---|---:|---|
| Northrop Grumman Systems | 1,270 | Sonar, electronics, mission systems |
| BAE Systems Land & Armaments | 355 | Propulsors, weapons handling |
| Curtiss-Wright Electro-Mechanical | 239 | Motors, valves, stators |
| DC Fabricators | 205 | Hull structures |
| Globe Composite Solutions | 197 | Composite materials |
| Scot Forge | 145 | Forgings (shafts, structural) |
| Johnson Controls Navy Systems | 80 | HVAC / chilled water |
| Teledyne Instruments | 78 | Instrumentation |

### Columbia Build I+II (`N0002417C2117`)

Top recipients in companion analysis of this $8.11 billion visible subaward tree (record-cap hit):[^repo-sam-prior]

| Recipient | Subaward $ (M) | Role |
|---|---:|---|
| **BlueForge Alliance** | **4,210** | Submarine Industrial Base (SIB) consortium |
| Northrop Grumman Systems | 669 | Combat, sonar, mission systems |
| DRS Naval Power Systems | 403 | Switchboards, power distribution |
| Curtiss-Wright Electro-Mechanical | 176 | Motors, valves, stators |
| Babcock Marine Rosyth (UK) | 172 | UK strategic-deterrent partner — propulsion components |
| Scot Forge | 171 | Forgings |
| APCO Technologies SA (Switzerland) | 131 | Launch-tube structural components |
| Rhoads Metal Fabrications | 124 | Hull/structural fabrication |

The Columbia top-eight is dominated by the BlueForge consortium pass-through, with Northrop Grumman Systems at approximately one-sixth of the BlueForge total but still the largest non-consortium recipient. The Columbia tree's appearance of foreign partners (Babcock Marine UK, APCO Switzerland) reflects the program's reliance on UK and European specialist suppliers for launch-tube and design work, partly tied to the joint US-UK Common Missile Compartment program with the Royal Navy's Dreadnought-class.[^repo-sam-prior]

## Structural visibility gaps in the subaward data

Five categories of activity are systematically missing from the first-tier subaward view.

**1. The ~2,500-record retrieval cap on USAspending.** Both GDEB master vehicles (Virginia Block V/VI and Columbia Build I+II) hit the pull script's practical ceiling of approximately 2,500 subaward records per prime (25 pages × 100 records). The pull sorts by amount descending so the top spend is captured; the long tail of small subs (typically below $100,000 each) is missing. For the two big masters, the visible $4.14 billion (Virginia) and $8.11 billion (Columbia) totals are conservative lower bounds on each PIID's true subaward delivery.[^repo-lessons-v1]

**2. The FFATA $30,000 reporting threshold and the FAR 52.204-10 scope exclusions.** Direct subcontract actions below approximately $30,000, indirect and general-and-administrative items, and long-term supplier agreements that are not direct prime-contract subcontracts are excluded from FFATA reporting by design.[^far-52-204-10]

**3. Reporting lag for fresh contracts.** Subaward reporting lags prime obligation by approximately 6–18 months. The Virginia Block VI LLTM `N0002424C2110` (awarded December 2023) shows 367 subs / $417 million as of the May 2026 pull — modest given a $4.96 billion cumulative prime obligation — and is expected to grow as the data ages. The FY2025 subaward action-date column ($766 million) is substantially under-reported for this reason.[^repo-lessons-v1]

**4. Zero-subaward primes.** Of the 17 in-scope PIIDs, five returned zero subaward records: `N0002409C2104` (Block II residual, closing out), `N0002410C2118` (VPM Tube Fabrication, $1.42B prime — non-reporting), `N0002411C2109` (SSBN-R concept), `N0002424C2114` (BPMI FY26 Virginia — too new), and `N0002410C6266` (LM Virginia Combat Systems, $899M prime — non-reporting). For the two large non-reporting primes — VPM Tube Fabrication and LM Virginia Combat Systems — the first-tier supplier base is invisible.[^repo-usaspending-summary]

**5. The USAspending cumulative-snapshot duplication bug.** The companion v2 lessons-learned material documents that USAspending's `/api/v2/subawards/` endpoint returns multiple records for the same `subaward_number` at different `action_date` values, with each record reporting a cumulative-style amount rather than the incremental value of that action. Naive sums of these records inflate true subaward delivery by a factor of approximately 5×–50×. The companion v2 file recommends a three-stage v3 dedup methodology: (Stage 1) for each `sub_id`, keep the record with the maximum amount; (Stage 2) collapse identical (recipient, amount) duplicates across different sub_ids; (Stage 3) cap any single (recipient, prime) pair at 1.0× the prime contract's total obligation and exclude any pair exceeding 2× prime. **The aggregator in this repository does not apply v3 dedup.** It performs only a naive sum of `amount` by `action_date` FY and by recipient. Reported subaward totals in `extracted/subaward_annual_by_prime.csv` and `extracted/subaward_top_recipients.csv` may therefore overstate true subaward delivery to recipients that have multiple cumulative-snapshot records under a single `sub_id`. (See [Data sources and methodology](09-data-sources-and-methodology.md#known-aggregator-limitation-no-v3-dedup) and [Limitations and blind spots](10-limitations-and-blind-spots.md#aggregator-does-not-apply-v3-subaward-dedup).)[^repo-lessons-v2][^repo-aggregate-script]

## How this chapter's data feeds the annual outsourced flow

The first-tier subaward data summarized here is one of the two pillars of the headline "annual outsourced flow" estimate in [Annual outsourced flow estimate](08-annual-outsourced-flow.md). The other pillar is the BPMI naval-reactor GFE prime flow visible in FPDS. The combined view adds the two, with the subaward column subject to the FY2025 reporting-lag adjustment and the v3-dedup caveat noted above.

[^repo-usaspending-script]: submarine_outsourced_work, `scripts/pull_usaspending_subawards.py`. See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-usaspending-summary]: submarine_outsourced_work, "usaspending_subawards/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-subaward-annual]: submarine_outsourced_work, "extracted/subaward_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^far-52-204-10]: 48 C.F.R. § 52.204-10. See full citation under [References](INDEX.md#references).

[^repo-lessons-v2]: Subaward Pull Lessons Learned (v2). See full citation under [References](INDEX.md#references).

[^repo-aggregate-script]: submarine_outsourced_work, `scripts/aggregate_annual_outsourcing.py`. See full citation under [References](INDEX.md#references).
