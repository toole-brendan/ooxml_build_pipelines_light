---
title: Scope and the funnel framework
---

# Scope and the funnel framework

This article uses a **cost-funnel decomposition** of the U.S. Navy's Shipbuilding and Conversion (SCN) appropriation for Virginia-class and Columbia-class submarines to organize the question of how much submarine new-construction value is performed by firms other than the assembling shipyards. The funnel starts at the per-fiscal-year per-class top-line cost of the boat, descends through the budget-justification cost categories (Plans, Government-Furnished Equipment, Other, and Basic Construction), and then descends one further layer into Basic Construction itself, separating the share that the prime shipyard self-performs from the share it outsources to the broader supplier base. The outsourced layer within Basic Construction is the principal object of the article; everything else in the funnel exists to size, contextualize, or qualify it.

This chapter defines the terminology, sets the scope window and the in-scope prime-contract identifiers, lays out the funnel structure, and notes the dollar-bucketing conventions used throughout. The terminology is largely conventional within federal procurement and U.S. Navy shipbuilding, but several terms have specific meanings under the Federal Acquisition Regulation (FAR), the Federal Procurement Data System (FPDS), or the Federal Funding Accountability and Transparency Act of 2006 (FFATA) that differ from colloquial usage and that warrant clarification.

## The cost funnel

The funnel is the analytical spine of the article. At each level it cuts from the total figure to the addressable subset:

```text
TOTAL SHIP COST (per-class per-FY, from SCN P-5c Total Ship Estimate)
│
├── PLANS COSTS                    engineering, detail design, T&E, config mgmt
│
├── GOVERNMENT-FURNISHED EQUIPMENT  Navy procures separately, ships to yard:
│      ├── Naval reactor plant     (Bechtel Plant Machinery, Inc.)
│      ├── Combat systems           (Lockheed Martin, Virginia program)
│      ├── Sonar / EW               (Northrop Grumman)
│      ├── Ordnance / launch
│      ├── Periscopes / electronics (L3Harris and others)
│      └── HM&E components          (various)
│
├── CHANGE ORDERS / OTHER          ECPs, block mods, reserves
│
└── BASIC CONSTRUCTION              the prime contract base — the dollars
   │                                that flow to GDEB on the SCN PIID
   │
   ├── YARD SELF-PERFORMED          labor + overhead at Groton / Quonset / NNS
   │
   └── OUTSOURCED WITHIN BC          ── the principal object of this article
         │
         ├── FFATA-visible           first-tier subawards reported under
         │                          FAR 52.204-10, published in SAM.gov FSRS
         │
         └── UNSEEN LAYER            ── beyond direct visibility:
              ├── Purchased material booked as direct material
              ├── Lower-tier subs (a sub's sub — not reportable)
              ├── FFATA non-compliance / under-reporting
              ├── HII-NNS team-build share (flows through GDEB prime)
              └── Long tail under the $30,000 threshold
```

A complete answer to "how much of the submarine's cost is outsourced" requires a denominator statement: outsourced relative to what? The funnel makes four candidate denominators visible.

### Four denominators of "outsourced"

The choice of denominator is the choice of question. The article reports against each of them where the data supports it, and is explicit about which is being used at every point. None of the four is reducible to the others without loss of meaning.

1. **Outsourced from GDEB** — the share of GDEB's own prime construction contract that GDEB pays to other firms. The numerator is the GDEB first-tier subaward tree under FAR 52.204-10, plus the larger unseen subset of GDEB's purchased material and lower-tier subcontracting that is not captured under that clause. Bechtel reactor procurement is *not* outsourced from GDEB (GDEB does not pay Bechtel; the Navy does, on a separate prime contract). HII Newport News team-build *is* outsourced from GDEB, structurally, because the dollars flow through GDEB's prime even though only a small share appears as a visible HII-NNS subaward of GDEB.
2. **Outsourced from the Navy / SCN perspective** — the share of the SCN appropriation that flows to firms other than the assembling shipyards (GDEB plus the HII-NNS team-build share). This adds the GFE-prime flows — Bechtel, Lockheed Martin, Northrop Grumman — to the GDEB subaward tree. It is closest to the denominator the Navy's 30-Year Shipbuilding Plan implicitly uses when it discusses "distributed shipbuilding" and "outsourcing partners."[^navy-fy27-plan]
3. **Outside-the-yard / outside-the-prime-team** — measured directly per contract action from the U.S. Department of Defense daily contract-announcement press releases, which state explicit percentage breakdowns of where each action's work will be performed. This is the most direct primary-source measurement because it does not depend on accounting categorization at all; the announcement names the cities and the percentages. See [DoD contract announcement data](07-dod-contract-announcement-data.md).
4. **Private-sector work outside the assembling yard** — any private-firm work not performed inside the GDEB hull-construction yards in Groton, Connecticut and Quonset Point, Rhode Island. This includes everything in (1) and (2), plus the HII-NNS team-build share (work performed at a different private yard), plus federally funded research and development center (FFRDC) and Department of Defense laboratory work funded outside SCN.

This article emphasizes denominators (2) and (3) in the headlines, and reports (1) explicitly throughout. Denominator (4) is discussed in [Limitations and the unseen layer](12-unseen-layer.md) but not aggregated.

## "Prime" and "prime of record"

In federal procurement, the **prime contractor** is the firm holding a direct contract with the U.S. government. For Virginia-class and Columbia-class submarine construction, the **prime of record** on every active SCN Line Item 2013 (Virginia) and Line Item 1045 (Columbia) construction contract is **General Dynamics Electric Boat** (GDEB), headquartered in Groton, Connecticut and with major production at Quonset Point, Rhode Island. General Dynamics Corporation discloses GDEB's role as Columbia and Virginia prime, including the teaming arrangement with HII-NNS, in its Form 10-K filings with the U.S. Securities and Exchange Commission.[^gd-10k-fy21]

**Huntington Ingalls Industries Newport News Shipbuilding** (HII-NNS) participates as a team partner under a long-standing arrangement that publicly assigns it approximately half of Virginia-class construction and approximately a fifth of Columbia-class construction by physical workload share. HII-NNS does not appear as a prime in FPDS records for submarine construction; its work flows through the GDEB prime contracts and is recorded against GDEB as the vendor of record. HII publicly describes its Columbia role as constructing and delivering approximately six module sections per submarine — bow, stern, auxiliary machinery room, superstructure, missile compartment, and weapons modules — under subcontract to GDEB.[^hii-columbia-modules]

Several major component categories are procured directly by the Navy under separate prime contracts with other firms and ship the resulting equipment to GDEB for installation. These are referred to as **GFE primes** for the part of their work that is government-furnished to GDEB. The largest single GFE prime by dollar value is **Bechtel Plant Machinery, Inc.** (BPMI), which supplies the naval reactor plant under Naval Reactors' direction. Other GFE primes include Lockheed Martin (Virginia-class combat systems hardware and software; Trident II D5 / D5LE2 strategic weapon system for Columbia), Northrop Grumman (submarine sonar and electronic-warfare systems), Curtiss-Wright (nuclear pumps and valves), BAE Systems (deck modules and forward subassemblies in Jacksonville, Florida), L3Harris (photonic masts), and Rolls-Royce (propulsion components).[^bae-jax-modules]

## "Outsourced"

For the purposes of this article, **outsourced** describes any dollar of the SCN submarine new-construction appropriation that ultimately flows to a firm other than the assembling shipyard's own labor and overhead. Three categories are in scope:

1. **First-tier subcontracts and lower-tier subcontracts** — work that the prime hires another firm to perform under the prime's own contract. First-tier subcontracts above the FFATA reporting threshold (currently $30,000 per action) are reportable to the FFATA Subaward Reporting System (FSRS), accessed via SAM.gov, under FAR 52.204-10. Lower-tier subcontracts (a subcontract of a subcontract) are *not* reportable; FFATA only reaches one tier below the prime.[^far-52-204-10]
2. **Government-furnished equipment (GFE)** — major equipment that the U.S. government procures from a separate prime contractor and ships to the assembling yard for installation in the hull. From the perspective of submarine production, the dollars are outsourced from the SCN appropriation perspective, even though they do not appear as subawards of the assembling yard. The naval reactor plant (BPMI), the Virginia-class combat systems (Lockheed Martin), and major sonar and electronic-warfare elements (Northrop Grumman) are all GFE.[^far-part-45]
3. **Plans Costs, lead-yard support, and the Maritime Industrial Base (MIB) line** — engineering services performed by the prime or by partner organizations, and the Navy's recent supplier-development and workforce-training spending that funds capacity expansion across the broader submarine supplier base. Beginning in approximately fiscal year 2022, the MIB line has carried roughly $1.3 billion or more per year, contractually routed through the Columbia prime but distributed almost entirely outside the prime shipyard. The Maritime Industrial Base Program Office was established by Navy memorandum in June 2024 and began operating in September 2024, formally institutionalizing the MIB layer.[^gao-25-106286]

The article does **not** treat as "outsourced":

- **Federal naval shipyard work** at Norfolk Naval Shipyard (Virginia), Portsmouth Naval Shipyard (Maine), Pearl Harbor Naval Shipyard & Intermediate Maintenance Facility (Hawaii), and Puget Sound Naval Shipyard & Intermediate Maintenance Facility (Washington). These yards perform depot maintenance and engineered overhauls on Navy submarines, but they are federal facilities staffed by federal employees; their work is funded as federal payroll, not as outsourced contract activity.
- **Federal employee labor at NAVSEA, the Strategic Systems Programs office, or the Program Executive Office Submarines.** Government program-office labor is not part of the outsourced flow.
- **Classified payload work** — intelligence-community modules and special-mission payloads procured outside the public SCN appropriation are by design not visible in federal procurement data.

## "Subaward" and the FFATA reporting threshold

A **first-tier subaward** in this article means a subcontract reported under the Federal Funding Accountability and Transparency Act of 2006 (FFATA) via FAR clause 52.204-10. The reporting threshold is currently subcontract actions above **$30,000**, and the clause defines reportable first-tier subcontracts as direct contractor subcontracts for performance of a prime contract.[^far-52-204-10] Filings flow into the FFATA Subaward Reporting System (FSRS) and are accessible via SAM.gov.

Several categories are excluded from the FFATA first-tier definition:

- Long-term supplier agreements, blanket purchase agreements, and indefinite-delivery / indefinite-quantity supplier agreements that are not direct prime-contract subcontracts.
- Indirect and general-and-administrative (G&A) items.
- Lower-tier subcontracts beneath the FFATA first tier (a sub of a sub is not reportable to FSRS under this clause).
- Standing supply or material agreements that pre-exist the prime contract and are not subordinated to it.

Beyond these definitional exclusions, FFATA compliance is uneven across the federal supplier base. The reporting gap is documented further in [The unseen layer](12-unseen-layer.md). The U.S. Government Accountability Office has separately found that "two of the shipbuilders we spoke with are already outsourcing work that would normally be done at their shipyards to their suppliers to overcome constrained physical space, with plans to expand the volume of material they are outsourcing" — a finding directly relevant to the gap between FFATA-visible subawards and the actual outsourced layer.[^gao-25-106286]

## "GFP," "GFE," and "CFE"

The formal Federal Acquisition Regulation umbrella term is **Government-Furnished Property (GFP)**, defined under FAR Part 45 and contract clause FAR 52.245-1 as property in the possession of, or directly acquired by, the U.S. government and subsequently furnished to the contractor for performance of a contract.[^far-part-45] **Government-Furnished Equipment (GFE)** is the most commonly used label, particularly for major equipment-type GFP such as a naval reactor plant or a missile system. The broader GFP category may also include government-furnished material, tooling, test equipment, information, and facilities; this article uses **GFE** in its narrow equipment sense throughout.

**Contractor-furnished equipment (CFE)** is equipment procured by the prime contractor under its own contract and incorporated into the deliverable. For submarine construction, the major component categories that are GFE include the naval nuclear reactor plant (BPMI), the Trident II D5 / D5LE2 strategic weapon system for Columbia (Lockheed Martin Strategic Programs), and the AN/SQQ-89 / AN/BYG-1 combat-system elements (mixed). Items procured under the prime's basic-construction scope — including most hull material, structural fabrication, propulsion auxiliaries, and outfitting — are CFE. The GFE / CFE classification of a specific item is determined by the underlying contract and budget cycle, not by the item's intrinsic identity, and can change between budget cycles as Navy program-management arrangements evolve.

## Scope: window, classes, and the 15 new-construction PIIDs

The article uses a **fiscal-year 2018 through fiscal-year 2027 signed-date window** for FPDS prime-contract data and a **fiscal-year 2016 through fiscal-year 2026 action-date window** for FFATA subaward data, where the wider subaward window captures pre-FY2018 actions on still-active master construction contracts. The article's primary substantive coverage is FY2020 forward, where the Justification Book data is complete; FY2018–FY2019 is included as a comparison baseline. The window was chosen to capture one full Virginia procurement block (Block V, FY2019–FY2023) plus the start of Block VI, plus the Maritime Industrial Base era transition from pre-MIB (FY2020–FY2022) to MIB era (FY2023 onward).

The article scopes the outsourced-flow analysis to **fifteen submarine new-construction prime contract Procurement Instrument Identifiers** (PIIDs). The scope was deliberately narrowed from a broader inventory of submarine-related contracts to focus on new construction; depot maintenance, overhauls, and backfit-upgrade contracts are out of scope even though they are submarine-related. The fifteen in-scope PIIDs span the two construction primes (GDEB and HII-NNS as team partner), the four GFE primes that are dollar-material to the cost funnel (Bechtel Plant Machinery, Lockheed Martin, BAE Systems, and Rolls-Royce), and the Maritime Industrial Base layer routed through Columbia:

| PIID | Prime | Class | Description |
|---|---|---|---|
| `N0002417C2100` | GDEB | Virginia | Block V / VI master construction contract |
| `N0002417C2117` | GDEB | Columbia | Build I + II master construction contract |
| `N0002424C2110` | GDEB | Virginia | Block VI long-lead-time material |
| `N0002412C2115` | GDEB | Virginia | Block IV multi-year procurement |
| `N0002409C2104` | GDEB | Virginia | Block II residual |
| `N0002413C2128` | GDEB | Columbia | Design drawings |
| `N0002411C2109` | GDEB | Columbia | SSBN-R concept formulation |
| `N0002416C2111` | GDEB | Virginia | Virginia Payload Module vent valve (Block V) |
| `N0002410C2118` | GDEB | Virginia | Virginia Payload Module tube fabrication |
| `N0002419C2114` | BPMI | Columbia | Naval reactor components |
| `N0002419C2115` | BPMI | Columbia | Columbia Class Industrial Base Increase |
| `N0002424C2114` | BPMI | Virginia | S9G reactor |
| `N0002410C6266` | LM | Virginia | Combat systems hardware and software |
| `N0002421C4106` | BAE | Virginia | SSN 812 forward subassembly |
| `N0002421C4111` | RR | Virginia | Virginia-class submarine rotor |

Two submarine-related PIIDs that appear elsewhere in the federal procurement record are **explicitly excluded** from this scope because they fund depot maintenance or backfit upgrades rather than new construction:

- `N0002420C4312` — USS *Hartford* (SSN-768) Engineered Overhaul; excluded because it is an overhaul of an existing boat.
- `N0002419C2125` — Virginia Tech Instructions / HPAD backfit; excluded because it funds upgrades to existing boats.

Three subaward recipient parent legal entities are **excluded** from outsourcing-rate calculations as Maritime Industrial Base pass-throughs that fund supplier-development infrastructure and workforce training rather than component or services delivery into a hull:

- **BlueForge Alliance** (UEI F8PEZKXES8B1) — non-profit consortium pass-through routed primarily through Columbia Build I+II (`N0002417C2117`). Cumulative receipts FY2016–FY2025 of approximately $4.17 billion.
- **Training Modernization Group, Inc.** (UEI QLJZVM6XKR71) — workforce training, approximately $77 million cumulative.
- **Institute for Advanced Learning and Research** (UEI TCM3R4JPRKY4) — workforce training, approximately $1.5 million cumulative.

The Maritime Industrial Base layer is treated separately in [The Maritime Industrial Base layer](10-maritime-industrial-base.md); it is excluded from the headline outsourcing-rate measurement but reported alongside it. The BPMI `N0002419C2115` "Columbia Class Industrial Base Increase" PIID, although named to indicate it is in part a capacity-investment vehicle, remains in scope because BPMI's broader role is direct procurement of reactor-plant components rather than pass-through to other firms.

## Cumulative versus window-period dollars

The Federal Procurement Data System reports two distinct dollar fields per contract modification:

- **`obligatedAmount`** — the dollars added by this specific modification (this-action only).
- **`totalObligatedAmount`** — the cumulative total of all modifications up through this one, since the contract was originally awarded.

A contract with a 2017 base award that has been receiving modifications through 2026 will show a `totalObligatedAmount` at the latest modification that may be dominated by pre-window obligations. For annual rollups, this article uses **per-modification `obligatedAmount` summed by signed-date fiscal year**, not the latest cumulative total. The Virginia Block IV master construction contract `N0002412C2115` is the canonical example: at the latest modification it carries roughly $20 billion of cumulative obligation, but inside the FY2018–FY2026 signed-date window the per-modification flow is approximately two orders of magnitude smaller. Using cumulative `totalObligatedAmount` would massively overstate the window flow by counting pre-window obligations.

For subaward data, the article uses **per-record `subAwardAmount` summed by `subAwardDate` fiscal year**. The FFATA Subaward Reporting System assigns a unique `subAwardReportId` to each filed subaward action; the article relies on this uniqueness rather than on retroactive deduplication.

## Multi-vintage budget reconciliation

The U.S. Department of the Navy publishes the SCN Justification Book annually as part of the President's Budget submission. Each book reports approximately seven fiscal years of data per line item — prior years (lump sum), the most recent actual, the prior-year estimate, the budget-request year (base plus overseas operations cost plus total), and several outyears. The reported values for any given fiscal year get **revised in subsequent books**: a fiscal year shown as the "estimate" column in one book becomes the "actual" column in the next, often with material changes due to inflation, shipbuilder performance, or program-restructuring actions.

To produce a per-fiscal-year cost figure that reflects the most accurate available information, this article uses the most recent Justification Book that shows the target fiscal year as a settled actual, defaulting to a rule of *most recent PB year ≥ FY+2*. For example, the FY2024 Total Ship Estimate for the Columbia second hull (SSBN-827) is taken from the FY2026 PB book, which shows FY2024 in its prior-actual column. The full set of vintages consulted spans the FY2022 through FY2027 PB books.[^scn-fy27pb][^scn-fy22-fy26-pb]

P-1 line numbers drift across books (Virginia's P-1 line number was 5 in PB22 through PB25, 8 in PB26, and 6 in PB27), but the underlying Line Item numbers are stable: Columbia is Line Item 1045, Virginia is Line Item 2013. The article uses LI numbers throughout for cross-vintage stability.

## Article scope and distinctions

This article covers the structure of outsourced spending on Virginia-class and Columbia-class new construction: prime and team-build relationships, the major contract vehicles, the cost-category structure of the SCN line items, government-furnished equipment, publicly visible first-tier subawards, the Maritime Industrial Base flow, executive commentary on outsourcing strategy, Navy and Office of the Secretary of Defense policy, and the structural limitations of the visible data. Detailed engineering content, operational history, classified payload material, hull-level cost details below the SCN P-5c level, and supplier proprietary information are outside its scope.

This article is distinct from:

- **Submarine design and acquisition history** — addressed in the U.S. Navy's class fact files, Congressional Research Service program reports, and *Selected Acquisition Reports*.
- **Submarine operational history and deployments** — service history, mission tasking, and operational employment.
- **Surface-combatant industrial base** — DDG-51, FFG-62 Constellation, and aircraft-carrier industrial-base topics are treated separately.
- **Foreign submarine programs** — United Kingdom Astute and Dreadnought construction at BAE Systems Submarines (Barrow-in-Furness) and the broader AUKUS Pillar 1 effort. Some United Kingdom partner content appears in the Columbia subaward data (Babcock Marine Rosyth, Rolls-Royce UK) but the foreign programs themselves are not in scope.
- **Submarine depot maintenance and engineered overhauls** — performed primarily by the four public naval shipyards and excluded from the "outsourced" definition above.

## Cross-references

- For the per-class per-fiscal-year top-line cost: [Total ship cost](02-total-ship-cost.md).
- For Plans, GFE, and Other Costs: [Plans, GFE, and other layers](03-plans-gfe-and-other-layers.md).
- For Basic Construction sub-categories: [Basic Construction](04-basic-construction.md).
- For the long-lead and advance procurement detail: [Long-lead and advance procurement](05-long-lead-and-advance-procurement.md).
- For the 50-to-65-percent outsourced-band evidence: [The outsourced layer within Basic Construction](06-outsourced-band-within-bc.md).
- For the direct DoD-announcement measurement of outsourced share: [DoD contract announcement data](07-dod-contract-announcement-data.md).
- For the FFATA-visible first-tier subaward stream: [FFATA-visible first-tier subawards](08-ffata-visible-subawards.md).

[^scn-fy27pb]: U.S. Department of the Navy, Fiscal Year 2027 President's Budget, *Shipbuilding and Conversion, Navy* (SCN) Justification Book, April 2026. Line Item 1045 Columbia Class Submarine and Line Item 2013 Virginia Class Submarine. Available via the Office of the Assistant Secretary of the Navy (Financial Management & Comptroller) at <https://www.secnav.navy.mil/fmc/fmb/Pages/Fiscal-Year-2027.aspx>.

[^scn-fy22-fy26-pb]: U.S. Department of the Navy, *Shipbuilding and Conversion, Navy* Justification Books accompanying the fiscal-year 2022 through fiscal-year 2026 President's Budgets. Used for multi-vintage reconciliation. Available via the SECNAV/FMB site, prior-year archive.

[^navy-fy27-plan]: U.S. Department of the Navy, Fiscal Year 2027 President's Budget, *30-Year Shipbuilding Plan*, April 2026; and U.S. Department of the Navy, "Department of the Navy Releases Fiscal Year 2027 Shipbuilding Plan," press release. The plan articulates the goal of increasing the share of Navy shipbuilding occurring at "distributed sites" from approximately 10 percent to approximately 50 percent. <https://www.navy.mil/Press-Office/Press-Releases/display-pressreleases/Article/4483211/department-of-the-navy-releases-fiscal-year-2027-shipbuilding-plan/>.

[^gd-10k-fy21]: General Dynamics Corporation, Annual Report on Form 10-K for fiscal year 2021. SEC accession 0000040533-22-000007. Discloses that "[the Marine Systems segment has one primary competitor] with which it also partners on the Virginia-class submarine program, and to which it subcontracts on the Columbia-class submarine program." Available via SEC EDGAR at <https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000040533>.

[^hii-columbia-modules]: Huntington Ingalls Industries, Newport News Shipbuilding division, "Columbia-Class (SSBN)" product page. Public corporate page identifying Newport News Shipbuilding as constructing approximately six module sections per Columbia-class submarine under subcontract to General Dynamics Electric Boat. <https://www.hii.com/products/columbia-class>.

[^bae-jax-modules]: BAE Systems, Inc., "Submarine Products and Technology" product page. Public corporate page identifying BAE Systems' Jacksonville, Florida shipyard as building deck modules for Virginia- and Columbia-class submarines, plus weapons-handling and ordnance-system content. <https://www.baesystems.com/en-us/product/submarine-products-and-technology>.

[^far-52-204-10]: 48 C.F.R. § 52.204-10, "Reporting Executive Compensation and First-Tier Subcontract Awards." Federal Acquisition Regulation contract clause implementing the Federal Funding Accountability and Transparency Act of 2006 (Pub. L. 109-282) as amended. Defines reportable first-tier subcontracts; sets the $30,000 reporting threshold per subcontract action. <https://www.acquisition.gov/far/52.204-10>.

[^far-part-45]: 48 C.F.R. Part 45, "Government Property," and 48 C.F.R. § 52.245-1, "Government Property" contract clause. <https://www.ecfr.gov/current/title-48/chapter-1/subchapter-G/part-45>; <https://www.acquisition.gov/far/52.245-1>.

[^gao-25-106286]: U.S. Government Accountability Office, *Shipbuilding and Repair: Navy Needs a Strategic Approach for Private Sector Industrial Base Investments*, GAO-25-106286, February 27, 2025. Documents Department of Defense shipbuilding industrial base investment of $5.8 billion FY2014–FY2023 with $12.6 billion planned through FY2028; the Maritime Industrial Base Program Office established by Navy memorandum in June 2024 and operating since September 2024; BlueForge Alliance's role as a "nonprofit integrator"; and the finding that "two of the shipbuilders we spoke with are already outsourcing work that would normally be done at their shipyards to their suppliers to overcome constrained physical space, with plans to expand the volume of material they are outsourcing." <https://www.gao.gov/products/gao-25-106286>.
