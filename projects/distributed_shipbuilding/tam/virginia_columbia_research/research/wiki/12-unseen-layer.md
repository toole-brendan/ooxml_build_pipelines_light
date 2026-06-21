---
title: The unseen layer
---

# The unseen layer

The FFATA-visible first-tier subaward stream captures approximately $1.0 to $1.5 billion per fiscal year of named-vendor subaward flow against the fifteen in-scope new-construction PIIDs at recent rates (chapter 8). The cost-funnel framework places the outsourced layer within Basic Construction at approximately 50 to 65 percent of Basic Construction value, which sizes the outsourced layer at approximately $5 to $7 billion per fiscal year (chapter 6). The direct primary-source measurement from the DoD daily-announcement corpus places the Outside-EB share at approximately 78 percent of dollar-weighted action value across the submarine-relevant supplier-targeted contract corpus (chapter 7). The most prominent single category not captured in the FFATA stream — the HII Newport News team-build share — is approximately $1.5 to $2.0 billion per fiscal year by itself (chapter 11).

This chapter inventories the categories of outsourced flow that sit outside the FFATA-visible stream: the categories that, together, account for the gap between approximately $1 to $1.5 billion of visible flow and the $5 to $7 billion implied outsourced layer. The categories fall into three groups: (a) categories that are *outside the FFATA definition* by FAR rule, (b) categories that are *within the FFATA definition* but are unreported because of compliance gaps or accessor cap limitations, and (c) categories that are *categorically excluded* from this article's outsourced-flow definition.

## Categories outside the FFATA definition by FAR rule

FAR 52.204-10 defines reportable first-tier subcontracts narrowly and excludes several categories that nonetheless represent dollar flow from the prime to outside firms:[^far-52-204-10]

### Purchased material booked as direct material cost

A prime contractor's accounting system distinguishes between direct material cost (items procured and consumed in performance of the contract) and subcontract cost (services or work performed under a separate contract with another firm). For complex shipbuilding, the boundary between these two categories is operationally fluid: a major component fabrication that one prime would book as a subcontract another might book as material purchase, depending on the supplier-contract structure. FFATA's first-tier definition reaches subcontracts but not material purchases per se.

For submarine construction, a significant share of supplier-delivered content is procured as material rather than as subcontract. Steel and aluminum stock; cast and forged structural components; off-the-shelf valves, pumps, and electrical components; specialty alloys and weldable materials — these are typically booked as material rather than as subcontract, even though they represent dollar flow to outside firms.

The dollar magnitude of submarine-construction purchased material booked as direct material cost is not separately disclosed by any prime, but it is structurally large. GDEB's Basic Construction line for a single Virginia Block VI hull at the two-per-year procurement rate is approximately $4-5 billion; the labor-and-overhead share of this is by industry convention 30-50 percent, implying that material and subcontract together represent approximately $2-3 billion per Virginia hull. With FFATA-visible subcontract content at well under $1 billion per hull on the named-vendor side, the residual purchased-material content is in the $1-2-billion-per-hull range.

### Long-term supplier agreements that pre-date the prime contract

FFATA does not require reporting of subcontracts under long-term supplier agreements that are not direct prime-contract subcontracts. For some specialty submarine components — particularly nuclear-grade pumps, valves, and forging-and-casting products — the supply relationship between the manufacturer and the prime is structured as a long-term agreement that the prime references in each fiscal year's procurement but does not separately execute as a new subcontract action.

### Indirect and general-and-administrative items

FAR 52.204-10 explicitly excludes indirect and G&A items from the FFATA first-tier definition. Some categories of outside-firm services to the prime — facilities engineering, contract management consulting, certain financial and administrative services — fall into the indirect category and are not reportable.

### Lower-tier subcontracts beneath the first tier

FFATA reaches only the first tier of subcontracts beneath the prime. A subcontract of a subcontract — material flowing from a tier-1 supplier to a tier-2 supplier — is not reportable to FSRS. For submarines, much of the deeper supplier base is at tier 2 or tier 3, particularly for specialty material (alloys, electronic components, fasteners) that flows through specialty distributors to the assembling primes.

The fraction of total outsourced flow occurring at tier 2 or below is not directly measurable, but for complex shipbuilding it is typically a meaningful share — perhaps 20 to 40 percent of total outsourced material flow.

## Categories within the FFATA definition but unreported

### Compliance gaps

While GDEB does file FFATA against its major submarine prime PIIDs, FFATA compliance is uneven across the broader federal supplier base. Companion research on Navy shipbuilding has documented that several major shipbuilding primes file zero FFATA subawards despite multi-billion-dollar prime obligations:[^repo-noncompliance]

- **Bath Iron Works (DDG-51 destroyers)** — zero FFATA first-tier subawards filed across a multi-year window despite billions in prime obligations.
- **Bollinger Shipyards** (U.S. Coast Guard Fast Response Cutter and Polar Security Cutter) — zero FFATA.
- **Birdon America** (U.S. Coast Guard Waterways Commerce Cutter) — zero FFATA.
- **Austal USA** (U.S. Coast Guard Offshore Patrol Cutter Stage 2) — zero FFATA.
- **Several foreign-headquartered primes** on specific submarine GFE work.

For submarines specifically, GDEB does file. But not every submarine-relevant prime files. The Lockheed Martin Virginia combat-systems prime `N0002410C6266`, the Virginia Payload Module Tube Fabrication prime `N0002410C2118`, the BPMI S9G reactor prime `N0002424C2114`, and several smaller GFE primes return zero FFATA-visible records across the article's full-history accessor window — despite operationally large prime obligations and clear use of supplier subcontracts. Whether this reflects compliance gaps, accounting categorization (subcontracts booked as material), or genuinely standing-agreement supplier arrangements is not separable from the visible data alone.

### The HII Newport News team-build share

The largest single in-scope category of FFATA-eligible-but-unreported flow is the Huntington Ingalls Newport News team-build share, addressed in detail in [The HII Newport News visibility gap](11-hii-newport-news-gap.md). Approximately $1.5 to $2.0 billion per fiscal year of HII-NNS submarine workshare flows through GDEB's prime construction contracts but does not appear in the FFATA-visible stream as HII-as-sub-of-GDEB; the visible flow is essentially zero in most fiscal years. Whether this is properly categorized as "outside the FFATA definition" (because the teaming agreement is a long-term standing arrangement) or "within the FFATA definition but unreported" is a structural question that this article does not resolve; the practical effect is the same.

### Actions below the $30,000-per-action threshold

The FFATA reporting threshold is currently $30,000 per subcontract action. Below the threshold, no filing is required. Across a multi-billion-dollar prime contract, the volume of small subaward actions below the threshold is large; their aggregate dollar value is typically a small fraction of total subcontract spend (because the largest individual subcontracts substantially exceed $30,000), but it is non-trivial on the long tail.

### USAspending retrieval cap

USAspending's `/api/v2/subawards/` endpoint caps record retrieval at approximately 2,500 records per prime contract. For the two largest submarine masters (Virginia Block V/VI `N0002417C2100` and Columbia Build I+II `N0002417C2117`), this cap was exceeded by fiscal year 2023; the long tail of small subawards on these masters is missing from USAspending's view. The SAM.gov FFATA accessor used by this article does not have this cap and recovers the long tail (chapter 8); but research that relies on USAspending alone would systematically under-count the small-subaward long tail by approximately 1,000 to 2,000 records per master.

### Reporting lag

FFATA filings carry an inherent 6-to-18-month lag between contract action and federal-system filing. For the article's coverage window through fiscal year 2026, the FY2025 figures are reporting-lag-depressed (chapter 8 reports approximately $758 million for FY2025; the true figure will revise upward as filings catch up), and FY2026 figures are essentially absent. The lag is a known and persistent feature of FFATA reporting; it does not represent a long-term gap, but for any analytical window ending within approximately 18 months of the current date, the most recent two fiscal years are under-reported by an unknowable specific amount.

## Categories categorically excluded from this article's definition

### Federal naval shipyard depot work

The four federal public naval shipyards — Norfolk Naval Shipyard (Virginia), Portsmouth Naval Shipyard (Maine), Pearl Harbor Naval Shipyard & Intermediate Maintenance Facility (Hawaii), and Puget Sound Naval Shipyard & Intermediate Maintenance Facility (Washington) — perform depot maintenance and engineered overhauls on Navy submarines. These yards are federal facilities staffed by federal employees, and their work is funded as federal payroll rather than as outsourced contract activity. They consume the bulk of the Navy's annual submarine depot maintenance budget — approximately $6 billion or more per fiscal year — but they are by definition not part of the outsourced flow.

The exclusion is by design: the article's scope is submarine new construction, and depot maintenance is a separate accounting category. The federal naval shipyards represent a counterpoint to the new-construction outsourcing trend that is the article's subject: depot maintenance has remained substantially insourced to federal facilities, while new construction has shifted toward outsourcing.

### Classified payload modules

Intelligence-community and special-mission payload modules are procured outside the public SCN appropriation under classified contracting authorities. These are by design not visible in federal procurement data systems and are explicitly outside the scope of this article. Submarines that carry classified payloads (the Block III-onward Virginia hulls with Virginia Payload Module capacity, and certain Columbia configurations) integrate the payload modules into the hull at the assembling yard, but the dollars associated with payload module fabrication and integration are not in the SCN line items this article addresses.

### Trident strategic weapon system

The Trident II D5 / D5LE2 strategic weapon system that arms Columbia is procured under separate Navy Strategic Systems Programs (SSP) line items, not under SCN Line Item 1045. Lockheed Martin Strategic Programs is the Trident prime; the dollar magnitude of the program is in the multiple-billion-dollar range across the Columbia fielding window. The Trident weapon system is GFE to GDEB (the Navy provides the weapon system to GDEB for integration into the missile compartment), but it is not in the cost-funnel framework's scope because it is funded outside SCN.

### Direct Navy R&D and program-office labor

Federal employee labor at NAVSEA, the Strategic Systems Programs office, the Program Executive Office Submarines, and the Naval Reactors program office is government payroll and not part of the outsourced flow. The Naval Reactors program in particular operates as a joint Navy / Department of Energy organization with a substantial federal workforce; its operational direction of BPMI is government work even though BPMI itself is a private firm.

## How big is the unseen layer

A rough decomposition of the implied outsourced layer in Basic Construction (at the 60-percent mid-case for FY2024 combined Virginia + Columbia Basic Construction of $15,427 million = approximately $9.3 billion):

```text
FY2024 implied outsourced from Basic Construction (mid-case):           ~$9,300M

minus the FFATA-visible (ex-MIB):                                       ~$1,300M
minus the implied HII-NNS submarine workshare at 30% midpoint:           ~$1,800M
                                                                         ────────
remaining unseen layer:                                                  ~$6,200M

   This unseen layer comprises (estimates, not separately measurable):
      Purchased material booked as direct material cost:               ~$3,000-4,000M
      Lower-tier subcontracts beneath the FFATA first tier:            ~$1,000-2,000M
      Long-term standing supplier agreements:                          ~$500-1,000M
      Other (sub-$30k actions, compliance gaps, etc.):                    ~$500M
```

The specific dollar magnitudes in the remaining unseen layer are not separately measurable from public data. The decomposition above is an illustrative breakdown using industry-typical proportions and is consistent with the cost-funnel-band 50-to-65-percent figure, the DoD-announcement 78-percent Outside-EB share, and the GAO finding that shipbuilders are expanding the volume of material flowing to suppliers.

The cleanest single-figure statement is: **the FFATA-visible first-tier subaward stream captures approximately 10 to 20 percent of the actual outsourced layer within Basic Construction.** The remaining 80 to 90 percent is unseen at the level of named-vendor first-tier subaward filings; it is, however, partially measurable through the DoD-announcement corpus (chapter 7), HII corporate-financial-segment disclosures (chapters 11 and 15), Navy and OSD policy documentation (chapters 6 and 14), and shipbuilder executive commentary (chapter 13).

## Confidence and what would improve it

Three forms of additional measurement would tighten the article's outsourced-flow estimate:

1. **A complete HII Newport News submarine-portion disclosure** would resolve the largest single category of unseen flow. HII does not currently publish a submarine-vs-carrier revenue split at the NNS segment level; if HII or its successor were to do so (or if the Navy were to publish per-class HII workshare data), the implied submarine portion currently estimated at 30 percent of NNS revenue would resolve to a definite figure.
2. **A fully cleaned multi-year retrospective FFATA accessor with v3 dedup applied to the largest masters** would tighten the visible-vendor side of the picture. The article's SAM.gov accessor uses the system's per-record `subAwardReportId` as the dedup key and does not require multi-stage dedup, but a USAspending-side comparison with v3 dedup would close the loop on what each of the two systems captures.
3. **Mod-description-level mining of GDEB prime-contract modifications** would identify per-hull supplier attribution and per-modification work-content descriptions. Public NAVSEA contract announcements occasionally do this (the "SSN 812 CONSTRUCTION (BOAT 2, FY 24)" pattern); a systematic application would lift the mod-level work-content visibility but is labor-intensive and not currently in scope.

These items are noted as potential extensions in [Data sources, pipeline, and limitations](16-data-sources-pipeline-limitations.md).

## Cross-references

- For the FFATA-visible first-tier subaward stream that this chapter's unseen layer surrounds: [FFATA-visible first-tier subawards](08-ffata-visible-subawards.md).
- For the HII Newport News team-build share in detail: [The HII Newport News visibility gap](11-hii-newport-news-gap.md).
- For the cost-funnel-band framework that sizes the implied total outsourced layer: [The outsourced layer within Basic Construction](06-outsourced-band-within-bc.md).
- For the direct primary-source measurement that confirms the gap exists: [DoD contract announcement data](07-dod-contract-announcement-data.md).
- For the methodology and dollar-bucketing conventions: [Data sources, pipeline, and limitations](16-data-sources-pipeline-limitations.md).

[^far-52-204-10]: 48 C.F.R. § 52.204-10, "Reporting Executive Compensation and First-Tier Subcontract Awards." Federal Acquisition Regulation contract clause implementing the Federal Funding Accountability and Transparency Act of 2006 (Pub. L. 109-282) as amended. Defines reportable first-tier subcontracts; sets the $30,000 per-action threshold; excludes long-term supplier agreements, indirect and G&A items, and lower-tier subcontracts. <https://www.acquisition.gov/far/52.204-10>.

[^repo-noncompliance]: Documentation of FFATA non-compliance by specific Navy shipbuilding primes draws on companion research into Navy surface-combatant and Coast Guard cutter procurement records, identifying primes with multi-billion-dollar prime obligations and zero FFATA subaward filings across multi-year windows. The pattern is consistent across program offices and is documented in industry-trade-press coverage of FFATA compliance gaps.
