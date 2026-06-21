---
title: Procurement and prime contracts
---

# Procurement and prime contracts

Virginia-class and Columbia-class submarines are procured by the U.S. Navy through the Naval Sea Systems Command (NAVSEA) under fixed-price-incentive multi-year procurement (MYP) prime contracts to General Dynamics Electric Boat. Major component categories — the naval reactor plant, the Trident II strategic weapon system, the Virginia-class combat system, and selected hull subassemblies — are funded through separate prime contracts with their own contracting paths. This chapter inventories the major submarine-related prime contract vehicles visible in the Federal Procurement Data System and USAspending data and documents what each one covers.

## How submarine procurement contracts are structured

The Navy procures submarines under **multi-year procurement (MYP)** authority, in which Congress authorizes the Navy to commit to a multi-year run of ships in advance in exchange for an expectation of unit-cost stability and supplier-base benefits. Each block of Virginia-class submarines and each Columbia build is funded under its own MYP authorization and gets its own master contract vehicle, although master vehicles are sometimes extended across blocks through modifications. The Virginia-class block structure and the Columbia build structure are:[^repo-sam-prior]

| Class | Block / Build | Hulls | Procurement years | Master vehicle |
|---|---|---|---|---|
| Virginia | Block I | SSN 774–779 | FY99–FY03 | (closed out) |
| Virginia | Block II | SSN 780–785 | FY04–FY08 | `N0002409C2104` (residual) |
| Virginia | Block III | SSN 786–791 | FY09–FY13 | (residual sustainment only) |
| Virginia | Block IV | SSN 792–801 | FY14–FY18 | `N0002412C2115` |
| Virginia | Block V | SSN 802–811 (5 with VPM) | FY19–FY23 | `N0002417C2100` |
| Virginia | Block VI | SSN 812–820 | FY24–FY28 (planned) | `N0002417C2100` (master extended) + `N0002424C2110` (LLTM) |
| Columbia | Build I | SSBN 826 (USS *District of Columbia*) | — | `N0002417C2117` |
| Columbia | Build II | SSBN 827 (USS *Wisconsin*) | — | `N0002417C2117` |

The Virginia-class block and Columbia build assignment of a PIID is **not reliably encoded in the PIID year prefix**. The Block V/VI master vehicle `N0002417C2100` carries a year-2017 prefix but its modifications now include scope for SSN 812 (the second Block VI hull, FY24 procurement). The reliable way to identify which block or build a contract is funding is to read modification descriptions for hull-number references — described in detail in [Data sources and methodology](09-data-sources-and-methodology.md#reading-mod-descriptions-to-identify-programs) and in companion lessons-learned material.[^repo-lessons-v1]

## Master construction contract vehicles

The major active master construction vehicles, ranked by cumulative obligated dollars at the latest in-window modification, are:[^repo-sam-prior][^repo-usaspending-summary]

| PIID | Vendor | Cumulative obligated (latest mod) | Ceiling | Block / build | Notes |
|---|---|---:|---:|---|---|
| **`N0002417C2100`** | GD Electric Boat | **$34.94B** | **$40.78B** | Virginia Block V → Block VI master | Earliest mods reference "DIVERT BLOCK V FOUNDATIONS"; latest in-window mod (2026-01-06) references "SSN 812 CONSTRUCTION (BOAT 2, FY 24)". Multi-block master vehicle. |
| **`N0002417C2117`** | GD Electric Boat | **$24.21B–$30.83B** (climbing rapidly) | **$42.18B** | Columbia Build I + Build II | Receives billion-dollar mods on a roughly monthly cadence as Build I + Build II construction ramps. SSBN 826 USS *District of Columbia* (Build I) and SSBN 827 USS *Wisconsin* (Build II). |
| **`N0002412C2115`** | GD Electric Boat | **$19.90B** | $19.93B | Virginia Block IV | Mostly closed out; in-window per-modification new-money flow is only approximately $22M against the $19.90B cumulative, per the Block IV worked example in companion lessons-learned material. |
| **`N0002409C2104`** | GD Electric Boat | $16.24B | $21.96B | Virginia Block II (residual) | "NO COST GOVERNMENT PROPERTY TRANSFER FROM THIS CONTRACT TO THE BLOCK V CONTRACT" — being mined for parts; no in-window subaward records. |
| **`N0002424C2110`** | GD Electric Boat | **$4.96B** | **$5.13B** | Virginia Block VI Long Lead Time Material | New (FY24 award). Window-native (all $4.96B is in window). Latest available mods reference "SSN 814 LONG LEAD TIME MATERIAL" — the fourth Block VI hull. |

The Block V/VI master `N0002417C2100` is the largest single submarine construction PIID in the dataset by cumulative obligated dollars. Its USAspending subaward tree contains approximately **2,000+ first-tier subaward records hitting the API's record cap**, with a total visible subaward value of approximately **$4.14 billion** (sorted by amount descending, the top spend is captured but the long tail of small subs is truncated).[^repo-usaspending-summary][^repo-lessons-v1]

The Columbia Build I+II master `N0002417C2117` similarly hits the subaward record cap at approximately 2,500 records / **$8.17 billion** total visible subaward value, dominated by the BlueForge Alliance consortium pass-through at $4.21 billion across just 7 reported subaward actions.[^repo-usaspending-summary][^repo-subaward-top]

## Virginia Payload Module component contracts

The Virginia Payload Module (VPM) is an 84-foot midbody insert that carries Tomahawk and Conventional Prompt Strike hypersonic weapons on Block V boats. VPM components are funded through separate GDEB component contracts that pre-date Block V awards:[^repo-sam-prior]

| PIID | Vendor | Cumulative obligated | Description |
|---|---|---:|---|
| **`N0002416C2111`** | GD Electric Boat | **$1.47B** | VPM Ventilation Valve (FY16 award) |
| **`N0002410C2118`** | GD Electric Boat | **$1.42B** | VPM Tube Fabrication (FY10 award — oldest VPM contract) |

A small number of smaller VPM support equipment contracts are held by Redstone Defense Systems and Benaka Inc. under low-million-dollar task orders.[^repo-sam-prior]

## Virginia-class sustainment, modernization, and depot work

Virginia-class sustainment, modernization installations, and depot work appear under several GDEB PIIDs and one Lockheed Martin combat-system PIID:[^repo-sam-prior][^repo-usaspending-summary]

| PIID | Vendor | Cumulative obligated | Ceiling | Description |
|---|---|---:|---:|---|
| **`N0002419C2125`** | GD Electric Boat | $1.37B | $1.39B | Virginia Class Block I–III High Pressure Air Dehydrators (HPAD) backfit |
| **`N0002420C4312`** | GD Electric Boat | $1.33B | $1.36B | USS *Hartford* (SSN 768) Engineered Overhaul (EOH) execution — depot, not new construction |
| **`N0002410C6266`** | Lockheed Martin | $899M | $1.37B | Virginia Class Combat Systems Hardware/Software |
| **`N0002421C4106`** | BAE Systems Land & Armaments | $85M | $86M | SSN 812 Forward Subassembly (Block VI hull components) |
| **`N0002421C4111`** | Rolls-Royce North America (Bird-Johnson Propeller) | $29M | $37M | Virginia Class Submarine Rotor |

## Columbia-class support and design contracts

Beyond the Build I+II master, Columbia has two earlier-stage design and concept-formulation vehicles:[^repo-sam-prior]

| PIID | Vendor | Cumulative obligated | Ceiling | Description |
|---|---|---:|---:|---|
| **`N0002413C2128`** | GD Electric Boat | **$3.07B** | $3.13B | Columbia Class Design Drawing Revisions (Columbia design predecessor) |
| **`N0002411C2109`** | GD Electric Boat | $480M | $845M | SSBN-R concept formulation ("SEA073R SSBN REPLACEMENT CONCEPT FORMULA") |

The Columbia Design Drawings PIID `N0002413C2128` is closed but had 608 reported first-tier subawards totaling $274 million across the FY16–FY25 window, dominated by United Kingdom design partner Babcock Marine (Rosyth) at $68 million, BWXT Nuclear Operations Group at $18 million, Lockheed Martin at $17 million, and Swiss firm APCO Technologies SA at $14 million.[^repo-sam-prior][^repo-usaspending-summary]

## Bechtel Plant Machinery naval reactor PIIDs

The Naval Reactors program funds reactor plant components for both Virginia and Columbia hulls under separate Navy prime contracts with Bechtel Plant Machinery, Inc. Several of these are active simultaneously, covering different reactor-component categories or fiscal-year shipsets. The dollar-largest BPMI vehicles in the FY18–FY26 window are:[^repo-sam-prior][^repo-usaspending-summary]

| PIID | Cumulative obligated | Ceiling | Description |
|---|---:|---:|---|
| **`N0002419C2114`** | **$3.38B** | $3.66B | Naval Reactor Components (Columbia) |
| **`N0002419C2115`** | **$3.00B** | $3.00B | Columbia Class Industrial Base Increase |
| **`N0002416C2106`** | $2.71B | $2.71B | Naval Reactor Components |
| **`N0002424C2114`** | **$2.54B** | $2.54B | FY26 Virginia Class Component Funding — fully window-native; an unambiguous FY26 obligation mod signed 2025-12-17 added $928M ("FY26 SHIPSET OF VIRGINIA CLASS COMPONENT FUNDING MOD") |
| **`N0002424C2115`** | $2.03B | $2.37B | Reactor Components |
| **`N0002412C2106`** | $1.32B | $1.32B | OPN Reactor Components |
| **`N0002407C2102`** | $1.18B | $1.20B | Reactor Components |
| **`N0002419C2112`** | $1.05B | $1.05B | Reactor Components |
| **`N0002413C2121`** | $662M | $662M | Reactor Components |
| **`N0002417C2110`** | $621M | $621M | Reactor Components |

The Bechtel column in the parsed FY-by-FY aggregator (`extracted/fpds_annual_by_prime.csv`) shows stable per-modification new-money obligation of approximately **$1.4–2.2 billion per year** across FY18–FY26, making BPMI the most consistent annual outsourced flow in the dataset.[^repo-fpds-annual] First-tier subawards under the Columbia Industrial Base contract `N0002419C2115` (67 subs / $528M) are dominated by BWXT Nuclear Operations Group at $272M, DRS Naval Power Systems at $56M, BWX Technologies at $53M, and Curtiss-Wright Electro-Mechanical at $42M.[^repo-sam-prior][^repo-usaspending-summary]

## Trident II D5 strategic weapon system

The Trident II D5 submarine-launched ballistic missile is the strategic weapon carried by Ohio-class and Columbia-class SSBNs and by the UK Royal Navy's Vanguard and Dreadnought SSBNs. Trident procurement is managed by the Navy's Strategic Systems Programs (SSP) office and is sole-source to Lockheed Martin Space. Trident procurement is funded outside the SCN appropriation and is treated separately from Columbia hull construction. The major Trident production PIIDs in the window are:[^repo-sam-prior]

| PIID | Cumulative obligated | Ceiling | Description |
|---|---:|---:|---|
| **`N0003023C0100`** | **$1.20B** | $1.23B | Lockheed Martin — FY24 Trident Production & Deployed Systems Support |
| **`N0003019C0100`** | **$1.12B** | $1.29B | Lockheed Martin — FY20 Trident Production & Deployed Systems Support |
| **`N0003020C0100`** | **$1.12B** | $1.36B | Lockheed Martin — FY21 Trident Production & Deployed Systems Support |
| `N0003022C2001` | $391M | $458M | L3Harris Interstate Electronics — Follow-on Engineering Services for SSP-owned Flight Test Instrumentation |
| `N0003020C0101` | $216M | $217M | Lockheed Martin — TRIDENT II D5LE2 SPALT Advanced Development |

The Trident D5 supplier base — dominated by Northrop Grumman (formerly ATK Launch Systems, solid rocket motors), Aerojet Rocketdyne (post-boost propulsion), and a long tail of mission-electronics and propellant suppliers — is documented in companion analysis.[^repo-sam-prior]

## Per-FY annual new-money obligation by vendor group

The parsed FY-by-FY annual roll-up across all 13 FPDS pulls, with `(PIID, mod_number, signed_date)` deduplication, gives the following per-modification new-money obligation by vendor group:[^repo-fpds-annual]

| FY | GDEB ($M) | BPMI ($M) | LM ($M) | NG ($M) | BAE ($M) | L3Harris ($M) | C-W ($M) | R-R ($M) | BlueForge ($M) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 3,518.41 | 416.21 | 54.15 | 7.37 | 472.55 | 0.06 | 36.35 | 438.32 | 0.00 |
| 2019 | 532.05 | 1,912.07 | 271.61 | 48.32 | 444.65 | -0.03 | 40.01 | 436.26 | 0.00 |
| 2020 | 230.74 | 1,290.84 | 19.46 | 58.19 | 623.07 | 25.71 | 28.24 | 434.01 | 0.00 |
| 2021 | 376.61 | 2,000.47 | 116.97 | 68.97 | 732.12 | 0.00 | 33.45 | 590.36 | 0.00 |
| 2022 | 334.53 | 2,119.41 | 48.49 | 0.88 | 316.40 | 0.00 | 62.57 | 593.07 | 0.00 |
| 2023 | 301.75 | 1,429.55 | 119.44 | 53.70 | 306.74 | 2.21 | 125.03 | 483.27 | 0.00 |
| 2024 | 384.19 | 2,181.73 | 185.92 | 17.70 | 371.02 | 4.32 | 99.09 | 407.43 | 537.88 |
| 2025 | 839.96 | 2,145.00 | 35.12 | 33.14 | 238.82 | 2.41 | 60.91 | 756.65 | 366.11 |
| 2026 | 285.81 | 1,897.45 | 31.20 | 0.00 | 78.24 | 0.20 | 7.15 | 162.25 | 19.10 |

Several patterns merit comment:

1. **GDEB FY18 spike ($3.52 billion)** is dominated by a single large modification against an existing master vehicle. Later years show much lower per-modification obligation against the GDEB line because the masters are funded incrementally and many subsequent mods are SLIN-level paperwork adjustments. GDEB's true total work is best measured via the cumulative `totalObligatedAmount` on the master PIIDs (the $34.94 billion on Block V/VI master, the climbing $24–30 billion on Columbia Build I+II) plus the first-tier subaward tree, *not* via this per-modification sum. (See [Cumulative versus window-period dollars](01-terminology-and-scope.md#cumulative-versus-window-dollars).)
2. **BPMI shows $1.4–2.2 billion per year consistently** — the most stable annual outsourced flow in the dataset.
3. **BlueForge** appears beginning in FY2024 ($538M) and continues into FY2025 ($366M) and FY2026 ($19M to date). The flow is concentrated on a single PIID (`N0002417C2117`) and a single recipient (`BLUEFORGE ALLIANCE`).[^repo-subaward-top] Approximately 3,901 records / 1,972 PIIDs from the broader `VENDOR_NAME:"BLUE FORGE"` substring query are matches on unrelated "Blue *" vendors (Blue Tech, Blue Rock, etc.); the genuine BlueForge Alliance prime activity is much smaller and is captured under the one true PIID.[^repo-fpds-summary]
4. **HII-NNS, Northrop Grumman, BAE, L3Harris, Curtiss-Wright, and Rolls-Royce** columns are reported in the annual roll-up but with important caveats discussed in [Prime shipbuilders and major suppliers](02-prime-shipbuilders.md). HII-NNS shows small negative obligations (de-obligations on carrier contracts). The C-W and R-R columns over-count non-submarine Navy work because their queries lacked description filters.[^repo-fpds-summary]

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-usaspending-summary]: submarine_outsourced_work, "usaspending_subawards/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-fpds-summary]: submarine_outsourced_work, "fpds_raw/_summary.json." See full citation under [References](INDEX.md#references).
