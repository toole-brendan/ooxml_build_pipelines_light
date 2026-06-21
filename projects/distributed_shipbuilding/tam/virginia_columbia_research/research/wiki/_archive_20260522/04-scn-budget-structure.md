---
title: SCN budget structure and cost categories
---

# SCN budget structure and cost categories

The U.S. Navy funds Virginia-class and Columbia-class new construction through the **Shipbuilding and Conversion, Navy (SCN)** appropriation (Treasury account 1611N). Each class is a distinct SCN **line item** with its own multi-exhibit budget submission published annually in the President's Budget. This chapter describes the structure of the FY2027 President's Budget SCN justification book for the two submarine line items and tabulates the figures parsed into the repository's `extracted/scn_li_*.csv` files. Per-ship cost-category data from the P-5c Ship Cost Analysis exhibit is the most useful Navy view of in-house versus outsourced cost composition.

## Line item structure

Submarine new construction is split between two SCN line items, each with a base appropriation (used to fund the ship in its procurement year) and an Advance Procurement (AP) appropriation (used to fund long-lead-time material 1–3 years before the ship's procurement year):[^scn-fy27pb][^repo-scn-extract]

| Line item | Class | P-1 Line | Budget Activity | Sub-Activity | Description |
|---|---|---|---|---|---|
| **1045** | Columbia | #1 | 01 — Fleet Ballistic Missile Ships | 1 | COLUMBIA Class Submarine (base) |
| **1045** | Columbia | #2 | 01 — Fleet Ballistic Missile Ships | 1 | COLUMBIA Class Submarine, Advance Procurement |
| **2013** | Virginia | #6 | 02 — Other Warships | 1 | Virginia Class Submarine (base) |
| **2013** | Virginia | #7 | 02 — Other Warships | 1 | Virginia Class Submarine, Advance Procurement |

The two classes are funded under different budget activities (Columbia under BA-01 "Fleet Ballistic Missile Ships," Virginia under BA-02 "Other Warships") but share the same appropriation account (1611N).

## P-1 resource summary

The P-40 Budget Line Item Justification (or "resource summary") table presents class-level procurement quantity and dollar figures across the budget window (Prior Years / FY25 actual / FY26 estimate / FY27 base / FY27 Overseas Operations Costs (OOC) / FY27 Total / FY28–31 outyears / "To Complete" / class Total).[^repo-scn-extract]

### Columbia (LI 1045)

| Metric | Prior Yrs | FY25 | FY26 | FY27 Base | FY28 | FY29 | FY30 | FY31 | To Complete | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Procurement quantity (boats) | 2 | – | 1 | 1 | 1 | 1 | 1 | 1 | 4 | **12** |
| Gross / Weapon System Cost ($M) | 26,810 | 0 | 10,744 | 10,486 | 10,137 | 10,361 | 10,441 | 10,693 | 56,768 | **146,441** |
| Net Procurement (P-1) ($M) | — | 0 | 3,929 | 6,905 | 6,379 | 6,058 | 6,012 | 6,303 | 25,624 | **61,210** |
| Total Obligation Authority ($M) | 29,176 | 9,581 | 9,280 | 15,583 | 12,835 | 11,351 | 12,360 | 12,020 | 34,256 | **146,441** |

The Columbia class is sized for **12 boats** at a class total of approximately **$146.4 billion**. The 2-boat Prior Years quantity reflects SSBN 826 (FY21 procurement) and SSBN 827 (FY24 procurement), already funded.

### Virginia (LI 2013)

| Metric | Prior Yrs | FY25 | FY26 | FY27 Base | FY28 | FY29 | FY30 | FY31 | To Complete | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Procurement quantity (boats) | 40 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 6 | **58** |
| Gross / Weapon System Cost ($M) | 124,749 | 9,501 | 5,389 | 11,437 | 11,285 | 11,098 | 10,197 | 10,594 | 34,144 | **228,394** |
| Net Procurement (P-1) ($M) | 77,068 | 7,357 | 2,740 | 8,402 | 8,149 | 7,876 | 7,283 | 7,423 | 20,650 | **146,949** |
| Total Obligation Authority ($M) | 122,911 | 13,320 | 6,378 | 13,151 | 13,011 | 14,687 | 12,269 | 12,017 | 20,650 | **228,394** |

The Virginia class is sized for **58 boats** at a class total of approximately **$228.4 billion**. The 40-boat Prior Years quantity reflects SSN 774 through SSN 813 (everything through Block VI hull 2), already authorized.

## P-5c Ship Cost Analysis — cost-category breakdown

The P-5c Ship Cost Analysis exhibit decomposes each ship's total cost into seven cost categories (eight on Columbia with Technology Insertion separated; combined on Virginia). The categories themselves are a rough proxy for "what the prime does in-house versus what flows out as outsourced or GFE":[^scn-fy27pb][^repo-scn-extract]

| Cost category | Likely outsourced / in-house composition |
|---|---|
| **Plan Costs** | Lead-yard services, engineering, **Maritime Industrial Base supplier development** (the $1.3B+ MIB pass-through lives here on Columbia) |
| **Basic Construction / Conversion** | Shipyard labor + hull material; **largely in-house at GDEB / HII-NNS** |
| **Change Orders** | Mixed |
| **Electronics** | Largely outsourced (Lockheed Martin combat systems, Northrop Grumman sonar, L3Harris photonics) |
| **Propulsion Equipment** | Largely GFE (Bechtel Plant Machinery naval reactor) |
| **Hull, Mechanical, Electrical (HM&E)** | Mix of in-house and outsourced (Curtiss-Wright pumps and valves, piping, auxiliaries) |
| **Ordnance** | Strategic-weapons-system and launch-system-related ship integration / equipment (Columbia). Note: Trident II D5 / D5LE2 missile production itself is funded outside SCN under Strategic Systems Programs (SSP) contracts and is *not* the same as this SCN-line Ordnance row. |
| **Other Cost** | Miscellaneous |

The cost-category-to-outsourced mapping is interpretation, not a formal Navy taxonomy; the Navy publishes the categories but does not label any category as "outsourced" or "in-house." Several items have transitioned between categories across budget cycles as Navy program-management arrangements change.

### Columbia P-5c per-ship breakdown

The most recent published Columbia ships, with cost-category dollars in millions:[^repo-scn-extract]

| Cost category | SSBN 826 (FY21) | SSBN 827 (FY24) | SSBN 828 (FY26) | SSBN 829 (FY27) |
|---|---:|---:|---:|---:|
| Plan Costs | 6,946.282 | 1,443.300 | 1,095.773 | **861.527** |
| Basic Construction/Conversion | 5,979.402 | 6,356.087 | 7,159.768 | **6,853.733** |
| Change Orders | 238.476 | 143.242 | 217.392 | 207.129 |
| Electronics | 358.293 | 349.701 | 361.283 | 367.634 |
| Propulsion Equipment | 1,700.900 | 1,613.999 | 1,294.878 | **1,541.973** |
| Hull, Mechanical, and Electrical (HM&E) | 156.299 | 119.107 | 102.496 | 101.710 |
| Ordnance | 668.502 | 596.757 | 468.840 | 512.585 |
| Other Cost | 73.446 | 66.618 | 43.887 | 40.078 |
| **Total Ship Estimate** | **16,121.600** | **10,688.811** | **10,744.317** | **10,486.369** |

Two patterns stand out:

1. The **SSBN 826 Plan Costs line at $6.95 billion** is roughly **5–8× the comparable line on later boats** ($1.44B / $1.10B / $0.86B). This reflects the Columbia program's lead-ship engineering and supplier-development concentration: the bulk of the design, lead-yard support, and MIB capacity-build investment was loaded onto the first hull.
2. **Propulsion Equipment** runs at approximately **$1.3–1.7 billion per hull** — consistent with the BPMI naval-reactor-plant GFE flow visible in FPDS, which the FPDS aggregator shows at $1.4–2.2 billion per year of new-money obligation (the difference reflects multi-ship procurement years and timing).[^repo-fpds-annual]

### Virginia P-5c per-ship breakdown (selected years)

For Virginia, the SCN P-5c exhibit covers a longer historical span. Selected years:[^repo-scn-extract]

| Cost category (FY24 procurement) | Per-boat value ($M) |
|---|---:|
| Plan Costs | 207.166 |
| Basic Construction/Conversion | 9,070.762 |
| Change Orders | 185.118 |
| Electronics | 562.372 |
| Technology Insertion | 16.020 |
| Propulsion Equipment | 1,121.470 |
| Other Cost | 70.546 |
| **Total Ship Estimate** | **11,377.643** |

| Cost category (FY26 procurement) | Per-boat value ($M) |
|---|---:|
| Plan Costs | 219.603 |
| Basic Construction/Conversion | 3,136.792 |
| Change Orders | 159.052 |
| Electronics | 598.515 |
| Technology Insertion | 16.667 |
| Propulsion Equipment | 1,035.070 |
| HM&E | 150.015 |
| Other Cost | 73.395 |
| **Total Ship Estimate** | **5,389.109** |

| Cost category (FY27 procurement, per-boat for 2-boat year) | Per-boat value ($M) |
|---|---:|
| Plan Costs | 223.443 (across 2 boats) |
| Basic Construction/Conversion | 8,889.310 (combined 2 boats) |
| Change Orders | 181.415 |
| Electronics | 624.898 |
| Technology Insertion | 17.001 |
| Propulsion Equipment | 1,273.090 |
| HM&E | 153.016 |
| Other Cost | 74.863 |
| **Total Ship Estimate** | **11,437.036** |

Virginia Plan Costs run at roughly $200–250 million per boat — a small fraction of the Columbia lead-ship figure, reflecting that Virginia design is mature and the Plan Costs line is not carrying a large MIB or lead-yard load on Virginia.

## Production schedule (P-27)

The P-27 Ship Production Schedule exhibit names the shipbuilder, contract award date, start of construction, and delivery date for each hull. The repository's parsed `scn_li_production_schedule.csv` confirms that:[^repo-scn-extract]

- All **eight Columbia hulls** in the FY21–FY31 window (SSBN 826 through SSBN 833) name **General Dynamics Electric Boat** as the sole shipbuilder.
- All **30 Virginia hulls** in the FY17–FY31 window (SSN 799 through SSN 825 plus SSN 850) name the **EB/HII-NNS** team build.

The repository's parsed schedule covers contract award dates as old as April 2014 (the Block IV MYP signing) and delivery dates as far out as 2039.

## Outyears, "To Complete," and class totals

Both line items publish FY28–FY31 outyear figures and a "To Complete" figure that aggregates the remaining boats beyond the eight-year window. For Columbia, the "To Complete" quantity is **4 boats** at $56.8 billion; for Virginia, it is **6 boats** at $34.1 billion.[^repo-scn-extract]

The class total figures should be read as the Navy's planning total for the **currently approved program of record** — 12 Columbia hulls and 58 Virginia hulls — and not as a forecast of total submarine procurement to 2050. The 30-Year Shipbuilding Plan accompanying the same President's Budget submission provides the longer-horizon planning view.[^scn-30yr-pb27]

## How SCN cost categories map to outsourcing

The SCN P-5c structure gives the most reliable Navy-published view of where each per-ship dollar goes by *function*. The outsourcing mapping in companion documentation is:[^repo-readme][^repo-manifest]

- **Plan Costs** on Columbia is the contractual home of the Submarine Industrial Base supplier-development flow. The SSBN 826 figure of $6.95 billion is the dominant Plan Costs line in the dataset; the BlueForge Alliance $4.21 billion subaward cumulative on the Build I+II PIID is funded out of this category.
- **Basic Construction / Conversion** is the prime shipyard's own labor and CFE material — largely in-house at GDEB (plus the HII-NNS team-build share, which is also in-yard work but at a different yard).
- **Electronics** at $360–600M per hull on Columbia and Virginia is the home of Lockheed Martin combat systems, Northrop Grumman sonar and EW, and L3Harris photonic-mast work — all largely outsourced.
- **Propulsion Equipment** at $1.0–1.7 billion per hull is the BPMI naval-reactor GFE flow — completely outsourced from the GDEB perspective, although the dollars are GFE rather than first-tier subaward.
- **Ordnance** on Columbia at $469–668 million per hull is best described as strategic-weapons-system and launch-system-related ship integration and equipment (Trident launch tubes, missile-compartment outfitting, and related ordnance-system installation work). The actual Trident II D5 / D5LE2 missile production itself is funded outside SCN under separate Strategic Systems Programs (SSP) contracts and is *not* the same line item as this SCN P-5c Ordnance row.
- **HM&E** at $100–156 million per hull on Columbia is a mix of in-house and outsourced (Curtiss-Wright Electro-Mechanical at the top of the HM&E outsourced flow).

The full annual outsourced flow, combining first-tier subawards, BPMI GFE prime obligations, and the MIB pass-through, is constructed in [Annual outsourced flow estimate](08-annual-outsourced-flow.md).

[^scn-fy27pb]: U.S. Navy FY2027 PB SCN Justification Book. See full citation under [References](INDEX.md#references).

[^scn-30yr-pb27]: U.S. Navy FY2027 PB 30-Year Shipbuilding Plan. See full citation under [References](INDEX.md#references).

[^repo-scn-extract]: submarine_outsourced_work, parsed SCN extracts (`extracted/scn_li_*.csv`). See full citation under [References](INDEX.md#references).

[^repo-fpds-annual]: submarine_outsourced_work, "extracted/fpds_annual_by_prime.csv." See full citation under [References](INDEX.md#references).

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-manifest]: submarine_outsourced_work, "MANIFEST.md." See full citation under [References](INDEX.md#references).
