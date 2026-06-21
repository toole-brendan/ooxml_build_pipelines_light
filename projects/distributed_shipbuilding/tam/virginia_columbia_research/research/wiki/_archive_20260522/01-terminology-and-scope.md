---
title: Terminology and scope
---

# Terminology and scope

Terminology used in connection with **outsourced work on U.S. nuclear submarine construction** overlaps with the broader vocabulary of federal procurement, U.S. Navy shipbuilding, and defense industrial-base analysis. Several terms have specific meanings under the Federal Acquisition Regulation, the Federal Procurement Data System, or USAspending.gov that differ from their colloquial sense and that warrant clarification before the contracting and dollar-flow material in later sections.

## "Prime" and "prime of record"

In federal procurement, the **prime contractor** is the firm holding a direct contract with the U.S. government. For Virginia-class and Columbia-class submarine construction, the **prime of record** on every active SCN 1045 (Columbia) and SCN 2013 (Virginia) construction contract is **General Dynamics Electric Boat** (Groton, Connecticut; Quonset Point, Rhode Island).[^repo-readme] HII Newport News Shipbuilding (Newport News, Virginia) participates as a team partner with a workload share publicly described as approximately 50% on Virginia construction and approximately 22% on Columbia construction, but does not appear as a prime in Federal Procurement Data System records for submarine construction.[^repo-lessons-v1] (See [Government-furnished equipment and the team-build pattern](05-gfe-and-team-build.md).)

This article treats **GDEB** as the singular prime for visibility purposes, while flagging the HII-NNS share as a structural data-visibility gap. Separately, several major component categories are procured by the Navy directly under their own prime contracts — Bechtel Plant Machinery, Lockheed Martin, and others — and these are referred to here as **GFE primes** for the part of their work that the Navy ships to the GDEB shipyard for integration.

## "Outsourced"

For the purposes of this article, **outsourced** describes any dollar of the U.S. Navy's submarine new-construction appropriation that ultimately flows to a firm other than the GDEB shipyard's own labor and overhead. Three categories are in scope:

1. **First-tier subcontracts** — work that the prime hires a vendor to perform under the prime's own contract. These are reported, imperfectly, via USAspending's `/api/v2/subawards/` endpoint against the prime's Procurement Instrument Identifier (PIID).[^usaspending-api]
2. **Government-furnished equipment (GFE)** — equipment that the U.S. government procures under a separate prime contract with another firm and ships to the GDEB shipyard for installation in the hull. From the perspective of submarine production, the dollars are outsourced from the SCN line, even though they do not appear as subawards of GDEB. Bechtel Plant Machinery naval reactor components, Lockheed Martin Virginia-class combat systems, and Lockheed Martin Trident II D5 / D5LE2 missiles for Columbia all fall in this category.[^repo-readme]
3. **Plans Cost, lead-yard support, and the Maritime Industrial Base (MIB) line** — engineering services performed by the prime or by federally-funded research and development centers (FFRDCs) and other partners, plus the Navy's recent supplier-development line that funds capacity expansion and workforce training across the broader submarine supplier base. Beginning in approximately FY2022, the MIB line has carried roughly $1.3 billion or more per year, contractually routed through GDEB but distributed almost entirely outside the prime shipyard.[^repo-readme]

The article does **not** treat as "outsourced":

- **Federal naval shipyard work** at Norfolk Naval Shipyard (Virginia), Portsmouth Naval Shipyard (Maine), Pearl Harbor Naval Shipyard & Intermediate Maintenance Facility (Hawaii), and Puget Sound Naval Shipyard & Intermediate Maintenance Facility (Washington). These yards perform depot maintenance and engineered overhauls on Navy submarines, but they are federal facilities staffed by federal employees and their work is funded as federal payroll rather than as outsourced contract activity.[^repo-lessons-v1]
- **Federal employee labor at NAVSEA, the Strategic Systems Programs office, or the Program Executive Office Submarines.** Government program-office labor is not part of the outsourced flow.
- **Classified payload work** — intelligence-community modules and special-mission payloads procured outside the public SCN appropriation are by design not visible in federal procurement data.[^repo-lessons-v1]

## "Subaward" and the FFATA reporting threshold

A **first-tier subaward** in this article means a subcontract reported under the Federal Funding Accountability and Transparency Act of 2006 (FFATA) via FAR clause 52.204-10. The reporting threshold is currently subcontract actions above **$30,000**, and the clause defines reportable first-tier subcontracts as direct contractor subcontracts for performance of a prime contract.[^far-52-204-10]

Several categories are excluded from the FFATA first-tier definition:

- Long-term supplier agreements, blanket purchase agreements, and indefinite-delivery / indefinite-quantity supplier agreements that are not direct prime-contract subcontracts.
- Indirect and general-and-administrative (G&A) items.
- Lower-tier subcontracts beneath the FFATA first tier (a sub of a sub is not reportable to USAspending under this clause).
- Long-term standing supply or material agreements that pre-exist the prime contract and are not subordinated to it.

Beyond these definitional exclusions, FFATA compliance is uneven across the federal supplier base. Several major Navy shipbuilding primes are documented in companion research as reporting **zero first-tier subawards** despite multi-billion-dollar prime obligations, including (in the surface-combatant and cutter context) Bath Iron Works on DDG-51, Bollinger Shipyards on the Fast Response Cutter and Polar Security Cutter, Birdon America on the Waterways Commerce Cutter, Austal USA on Offshore Patrol Cutter Stage 2, and several foreign-headquartered primes.[^repo-lessons-v1] In the submarine context, GDEB does report subawards on its major Virginia and Columbia prime PIIDs, but the visible coverage is incomplete (see [First-tier subawards and supplier visibility](06-first-tier-subawards.md) and the ~2,500-record retrieval cap discussion in [Limitations and blind spots](10-limitations-and-blind-spots.md)).

## "GFP," "GFE," and "CFE"

The formal Federal Acquisition Regulation umbrella term is **Government-Furnished Property (GFP)**, defined under FAR Part 45 and contract clause FAR 52.245-1 as property in the possession of, or directly acquired by, the U.S. government and subsequently furnished to the contractor for performance of a contract.[^far-part-45] **Government-Furnished Equipment (GFE)** is the most commonly used label, particularly for major equipment-type GFP such as a naval reactor plant or a missile system. The broader GFP category may also include government-furnished material, tooling, test equipment, information, and facilities; this article uses **GFE** in its narrow equipment sense throughout, with the understanding that the underlying FAR authority is the broader GFP framework.

**Contractor-furnished equipment (CFE)** is equipment procured by the prime contractor under its own contract and incorporated into the deliverable. For submarine construction, the major component categories that are clearly GFE include the naval nuclear reactor plant (Bechtel Plant Machinery), the Trident II D5 / D5LE2 strategic weapon system for Columbia (Lockheed Martin Strategic Programs), and the AN/SQQ-89 / AN/BYG-1 combat-system elements (mixed). Items procured under the prime's basic-construction scope — including most hull material, structural fabrication, propulsion auxiliaries, and outfitting — are CFE.

The GFE / CFE classification of a specific item is determined by the underlying contract and budget cycle, not by the item's intrinsic identity. The same physical component can transition between GFE and CFE status across budget cycles as Navy program-management arrangements change, as has been documented in companion research on the DDG-51 program. (For a parallel treatment in the surface-combatant context, see [Construction of Arleigh Burke-class destroyers, GFE and CFE chapter](../../DDG%20Blocks/wiki_ddg_construction/wiki/07-gfe-and-cfe.md).)

## Three denominators of "outsourced"

Much of the ambiguity around whether to count BPMI, HII-NNS, BlueForge, or Lockheed Martin flows as "outsourced" disappears once it is recognized that there are three distinct denominators in play, each appropriate for a different analytical question:

1. **Outsourced from GDEB** — the share of GDEB's own construction prime contract that GDEB pays to other firms. This is the GDEB first-tier subaward tree. BPMI naval reactor procurement is *not* outsourced from GDEB (GDEB does not pay BPMI; the Navy does, on a separate prime). HII-NNS team-build *is* outsourced from GDEB, structurally, even though only $98M shows up as a visible HII-NNS subaward of GDEB.
2. **Outsourced from the Navy / SCN perspective** — the share of the SCN appropriation that flows to firms other than the assembling shipyards (GDEB plus the HII-NNS team-build share). This adds the GFE-prime flows (BPMI, Lockheed Martin combat systems, etc.) to the GDEB subaward tree. It is the denominator the Navy's own 30-Year Shipbuilding Plan implicitly uses when it discusses "outsourcing partners."
3. **Private-sector work outside the assembling yard** — any private-firm work not performed inside the GDEB hull-construction yards in Groton and Quonset Point. This includes (1) and (2), plus the HII-NNS team-build share (work performed at a different private yard), plus all FFRDC and DoD-lab work funded outside SCN.

This article tracks (1) and (2) explicitly. The HII-NNS team-build share is flagged as a known understatement of (3). The headline annual outsourced flow estimate in [chapter 8](08-annual-outsourced-flow.md) is a combined (1) + (2) view, with explicit caveats about overlap. The three denominators are non-nested in their visibility patterns, which is why a single all-purpose "outsourced share" number is misleading without a clear denominator statement.

## Cumulative versus window-period dollars

The Federal Procurement Data System reports two distinct dollar fields per contract modification:

- **`obligatedAmount`** — the dollars added by this specific modification (this-action only).
- **`totalObligatedAmount`** — the cumulative total of all modifications up through this one, since the contract was originally awarded.

A contract with a 2014 base award that has been receiving small administrative modifications through 2026 will show a `totalObligatedAmount` at the latest modification that is dominated by pre-2018 obligations. For annual outsourcing rollups, this article uses **per-modification `obligatedAmount` summed by signed-date fiscal year**, not the latest cumulative total. The methodology is documented in companion lessons-learned material, which traces a Block IV worked example showing that the Virginia Block IV contract `N0002412C2115` carries a cumulative $19.90 billion that, inside a FY18–FY26 window, represents only approximately $22 million of actual new-money obligation; the remainder was committed pre-2018.[^repo-lessons-v1]

The aggregator in this repository implements the per-modification summation, deduplicating by `(PIID, mod_number, signed_date)` before bucketing into signed-date fiscal years.[^repo-aggregate-script] (See [Data sources and methodology](09-data-sources-and-methodology.md#cumulative-versus-window-dollars).)

## Physical-build terminology: "module" versus "block"

Public sources describe the physical construction of U.S. nuclear submarines using a small but specific vocabulary that should not be confused with the procurement-block terminology used elsewhere in this article:

- **Module / module section / major assembly / deck module / super module / outfitting** — the **physical** construction units of the hull. HII Newport News Shipbuilding publicly describes itself as constructing and delivering approximately **six module sections per Columbia submarine** under contract to General Dynamics Electric Boat, including the bow, stern, auxiliary machinery room, superstructure, missile compartment, and weapons modules. BAE Systems describes its Jacksonville, Florida shipyard as building **deck modules** for Virginia- and Columbia-class submarines. Below the module section level, the same vocabulary uses **major assembly** and **outfitting** for the equipment and piping installed inside each module before final hull joining.[^hii-columbia-modules][^bae-jax-modules]
- **Block** — by contrast, in the Virginia-class context, "Block" denotes a **procurement and design increment** (Block I, II, III, IV, V, VI), each corresponding to a multi-year procurement authorization for a run of hulls (see [Procurement and prime contracts](03-procurement-and-contracts.md)). The Columbia equivalent terminology is "Build" (Build I = SSBN 826, Build II = SSBN 827).

A reader who hears that "HII builds the stern block for Virginia" should interpret "block" in that sentence as **module**, not as the procurement increment. The two senses of "block" share a word but mean different things: physical construction units versus contract-procurement boundaries. This article uses **block** only in its Virginia procurement-increment sense and uses **module section** or **major assembly** for physical construction units.

## Scope window

The article uses a **FY2018 through FY2026 signed-date window** for FPDS data. The window starts in FY2018 because the largest still-active master construction contracts — Virginia Block V at `N0002417C2100` and Columbia Build I+II at `N0002417C2117`, both signed in 2017 — need to be captured with all of their subsequent modifications. Earlier contracts (Block IV at `N0002412C2115` signed in 2012; Block II at `N0002409C2104` signed in 2009) appear in the window through their post-2018 modifications. USAspending subaward records, which are keyed on `action_date` rather than signed date, are reported by action-date fiscal year and extend back to approximately FY2013 where the underlying prime is older than the window.[^repo-subaward-annual]

## Scope of the article

This article covers the structure of outsourced spending on Virginia-class and Columbia-class new construction: prime and team-build relationships, the major contract vehicles, the cost-category structure of the SCN line items, government-furnished equipment, publicly visible first-tier subawards, the Maritime Industrial Base flow, an annual outsourced-flow estimate, the data sources and methodology, and the structural limitations of the visible data. Detailed engineering content, operational history, classified payload material, hull-level cost details below the SCN P-5c level, and supplier proprietary information are outside its scope.

## Distinction from related fields

This article is distinct from:

- **Submarine design and acquisition history** — naval architecture and the historical acquisition narrative of the Virginia and Columbia programs are addressed in the U.S. Navy's class fact files, Congressional Research Service program reports, and *Selected Acquisition Reports*, and are not duplicated here.
- **Submarine operational history and deployments** — service history, mission tasking, and operational employment are out of scope.
- **Surface-combatant industrial base** — DDG-51, FFG-62 Constellation, and aircraft-carrier industrial-base topics are treated separately. The companion DDG-51 wiki at [Construction of Arleigh Burke-class destroyers](../../DDG%20Blocks/wiki_ddg_construction/wiki/INDEX.md) covers the surface-combatant analog of the topics here.
- **Foreign submarine programs** — including United Kingdom Astute/Dreadnought construction at BAE Systems Submarines (Barrow-in-Furness), Australian SSN-AUKUS, and other nuclear-powered submarine programs. Some United Kingdom partner content appears in the Columbia subaward data (Babcock Marine Rosyth, Rolls-Royce UK) but the foreign programs themselves are not in scope.
- **Submarine depot maintenance and engineered overhauls** — except where private-sector primes appear (for example, the USS Hartford Engineered Overhaul on `N0002420C4312`), depot maintenance is performed by the four public naval shipyards and is excluded from the "outsourced" definition above.

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^usaspending-api]: USAspending.gov REST API. See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^far-52-204-10]: 48 C.F.R. § 52.204-10. See full citation under [References](INDEX.md#references).

[^far-part-45]: FAR Part 45 / FAR 52.245-1, Government Property. See full citation under [References](INDEX.md#references).

[^hii-columbia-modules]: HII (Huntington Ingalls Industries), Newport News Shipbuilding, "Columbia-Class (SSBN)" product page. See full citation under [References](INDEX.md#references).

[^bae-jax-modules]: BAE Systems, "Submarine Products and Technology" page describing the Jacksonville, Florida shipyard's deck-module construction work for Virginia- and Columbia-class submarines. See full citation under [References](INDEX.md#references).

[^repo-aggregate-script]: submarine_outsourced_work, `scripts/aggregate_annual_outsourcing.py`. See full citation under [References](INDEX.md#references).

[^repo-subaward-annual]: submarine_outsourced_work, "extracted/subaward_annual_by_prime.csv." See full citation under [References](INDEX.md#references).
