---
title: Scope and the funnel framework
---

# Scope and the funnel framework

This article uses a **cost-funnel decomposition** of the U.S. Navy's Shipbuilding and Conversion (SCN) appropriation for Arleigh Burke-class (DDG-51) destroyers to organize the question of how much destroyer new-construction value is performed by firms other than the two assembling shipyards. The funnel starts at the per-fiscal-year per-class top-line cost of the ship and descends through the budget-justification cost categories (Plan Costs, Government-Furnished Equipment, Other Cost, and Basic Construction), and then descends one further layer into Basic Construction itself, separating the share that each prime shipyard self-performs from the share it outsources to the broader supplier base. The outsourced layer within Basic Construction, plus the GFE layer in its entirety, is the principal object of the article; everything else in the funnel exists to size, contextualize, or qualify it.

This chapter defines the terminology, sets the scope window and the in-scope prime-contract identifiers, lays out the funnel structure, notes the dollar-bucketing conventions used throughout, and identifies the categories of destroyer-related work that are deliberately excluded from the scope of this article.

## The two-yard competitive structure

A reader coming to this article from the companion submarine analysis will notice an immediate structural difference: where the Virginia and Columbia submarine programs are organized around a single prime of record (General Dynamics Electric Boat) with Huntington Ingalls Newport News Shipbuilding as an invisible team-build partner under GDEB's prime contract, the DDG-51 program is organized around a **two-yard competitive procurement** in which both shipyards hold direct prime contracts with the U.S. Navy:

| Prime yard | Subsidiary parent | Primary location | Role |
|---|---|---|---|
| General Dynamics Bath Iron Works (GD-BIW) | General Dynamics Corporation, Marine Systems segment | Bath, Maine (with annex at Brunswick, Maine) | One of two DDG-51 prime yards; sole DDG-1000 / Zumwalt prime; DDG-51 class Design Agent |
| Huntington Ingalls Industries Ingalls Shipbuilding (HII-Ingalls) | Huntington Ingalls Industries, Inc., Ingalls Shipbuilding segment | Pascagoula, Mississippi | One of two DDG-51 prime yards; also builds the LPD-17 and LHA-8 amphibious programs and the U.S. Coast Guard National Security Cutter and Polar Security Cutter programs |

Each individual DDG-51 hull is awarded to one yard or the other on its own prime contract, and the multi-year procurement (MYP) blocks since FY18 have been structured as **two parallel prime contracts** — one per yard — rather than as a single umbrella prime with a teaming subcontract.[^myp-structure] This has two analytical consequences:

1. **No "invisible team-build partner" wrinkle.** What appears in FPDS as the vendor of record on each DDG-51 prime contract is in fact the yard performing the work. The submarine project's chapter on "the HII Newport News visibility gap" — quantifying the share of submarine value that flows through the GDEB prime to HII-NNS as a structurally invisible team-build subcontract — has no parallel in the destroyer program. Instead, each yard's first-tier subaward tree is independently visible in FFATA against its own prime PIIDs.
2. **A new categorical caveat: source-selection redaction.** The two-yard competitive procurement format triggers, under 41 U.S. Code § 2101 et seq. and Federal Acquisition Regulation (FAR) §§ 2.101 and 3.104, the designation of the multiyear master award dollar values as **source-selection sensitive information** that "will not be made public at this time." This is discussed in chapter 12. For now, it is enough to note that the FY23-27 DDG-51 multiyear master awards (BIW PIID `N00024-23-C-2305` and Ingalls PIID `N00024-23-C-2307`, both awarded in August 2023) appear in DoD daily contract announcement bulletins with explicit place-of-performance percentage breakdowns but with their dollar values redacted, while the same paragraphs in the submarine-program bulletins (which use a single-prime structure) disclose the dollar values.

## "Outsourced"

For the purposes of this article, **outsourced** describes any dollar of the SCN destroyer new-construction appropriation that ultimately flows to a firm other than the prime shipyard's own labor and overhead. Three categories are in scope:

1. **First-tier subcontracts and lower-tier subcontracts** — work that a prime yard hires another firm to perform under the yard's own contract. First-tier subcontracts above the FFATA reporting threshold (currently $30,000 per action) are reportable to the FFATA Subaward Reporting System (FSRS), accessed via SAM.gov, under FAR 52.204-10. Lower-tier subcontracts (a subcontract of a subcontract) are *not* reportable; FFATA only reaches one tier below the prime.[^far-52-204-10]
2. **Government-furnished equipment (GFE)** — major equipment that the U.S. government procures from a separate prime contractor and ships to the assembling yard for installation in the hull. From the perspective of destroyer production, the dollars are outsourced from the SCN appropriation perspective, even though they do not appear as subawards of the assembling yard. Aegis Combat System (Lockheed Martin Moorestown), AN/SPY-6(V)1 radar (Raytheon Andover), Mk 41 Vertical Launching System (Lockheed Martin), Mk 45 5-inch gun (BAE Systems), LM2500 main propulsion turbines (GE Aerospace), AN/SLQ-32 SEWIP (Northrop Grumman), and Mk 15 Phalanx CIWS (Raytheon) are all GFE.[^far-part-45]
3. **Plan Costs, lead-yard support, and class-design engineering** — engineering services performed by Bath Iron Works in its role as DDG-51 class Design Agent, plus separate planning-yard and lead-yard-support contracts that the Navy uses for sustained class-design work between procurement blocks.

The article does **not** treat as "outsourced":

- **Federal naval shipyard work** at Norfolk Naval Shipyard (Virginia), Portsmouth Naval Shipyard (Maine), Pearl Harbor Naval Shipyard & Intermediate Maintenance Facility (Hawaii), and Puget Sound Naval Shipyard & Intermediate Maintenance Facility (Washington). These yards perform depot maintenance and engineered overhauls on Navy surface combatants, but they are federal facilities staffed by federal employees; their work is funded as federal payroll, not as outsourced contract activity.
- **Federal employee labor at NAVSEA, PEO Ships, or the Aegis Technical Representative office.** Government program-office labor is not part of the outsourced flow.
- **Ship-repair and depot maintenance work at private yards** other than BIW or Ingalls — including BAE San Diego Ship Repair, BAE Jacksonville Ship Repair, BAE Norfolk Ship Repair, and BAE Southeast Shipyards Mayport. This work is in-scope for destroyer **sustainment** but out-of-scope for destroyer **new construction**, which is what this article addresses.
- **Standard Missile, ESSM, Tomahawk, and CIWS production and procurement** funded under the Weapons Procurement (WPN) and Other Procurement (OPN) appropriations rather than SCN. These weapons are loaded aboard destroyers but they are paid for from a different appropriation; including them would double-count against a different budget line. They are tagged `ddg_gfe_weapons` in the underlying classification and excluded from the headline TAM (target addressable market) gate by default.
- **Out-of-class destroyer work** — the Zumwalt-class (DDG-1000) program, which closed at three ships, all delivered. The remaining DDG-1000 flows are OPN-funded modernization (Conventional Prompt Strike installation on DDG 1002 and follow-on upgrades) rather than SCN new construction; see further discussion below.

## The Zumwalt (DDG-1000) exclusion

The Zumwalt-class (DDG-1000) is excluded from the headline scope of this article. Three ships were procured under SCN Line Item 2119 — DDG 1000 *Zumwalt*, DDG 1001 *Michael Monsoor*, and DDG 1002 *Lyndon B. Johnson* — and all three have been delivered. No further Zumwalt-class procurements are scheduled. Remaining work on the class flows through OPN-funded modernization contracts (most prominently the Conventional Prompt Strike installation on DDG 1002, a hypersonic-weapon-system retrofit) rather than SCN new-construction contracts.

The underlying classified dataset retains a separate `ddg1000` program tag and a `ddg_repair` work-type tag for completeness, but the headline TAM gate (`is_ddg_new_construction_tam == 'yes'`) excludes both. A reader interested in the full destroyer-class outsourcing flow including the Zumwalt-class remainder and the DDG-51 depot-sustainment stream — approximately $2.0 billion of `ddg_repair` actions across 23 records, plus a residual Zumwalt modernization flow — would need to relax the TAM gate, but doing so admits substantial methodological noise (LPD-17, LHA-8, Polar Security Cutter, and amphibious-warship maintenance at the same Pascagoula and San Diego facilities) and is not pursued here.

## "Subaward" and the FFATA reporting threshold

A **first-tier subaward** in this article means a subcontract reported under the Federal Funding Accountability and Transparency Act of 2006 (FFATA) via FAR clause 52.204-10. The reporting threshold is currently subcontract actions above **$30,000**, and the clause defines reportable first-tier subcontracts as direct contractor subcontracts for performance of a prime contract.[^far-52-204-10] Filings flow into the FFATA Subaward Reporting System (FSRS) and are accessible via SAM.gov.

Several categories are excluded from the FFATA first-tier definition:

- Long-term supplier agreements, blanket purchase agreements, and indefinite-delivery / indefinite-quantity supplier agreements that are not direct prime-contract subcontracts.
- Indirect and general-and-administrative (G&A) items.
- Lower-tier subcontracts beneath the FFATA first tier (a sub of a sub is not reportable to FSRS under this clause).
- Standing supply or material agreements that pre-exist the prime contract and are not subordinated to it.

Beyond these definitional exclusions, FFATA compliance is uneven across the federal supplier base. The gap between the FFATA-visible first-tier subaward stream and the actual yard-side outsourcing flow is the principal subject of chapter 9. The U.S. Government Accountability Office has separately found that "two of the shipbuilders we spoke with are already outsourcing work that would normally be done at their shipyards to their suppliers to overcome constrained physical space, with plans to expand the volume of material they are outsourcing" — a finding directly relevant to the gap between FFATA-visible subawards and the actual outsourced layer, as discussed in chapter 14.[^gao-25-106286]

## "GFP," "GFE," and "CFE"

The formal Federal Acquisition Regulation umbrella term is **Government-Furnished Property (GFP)**, defined under FAR Part 45 and contract clause FAR 52.245-1 as property in the possession of, or directly acquired by, the U.S. government and subsequently furnished to the contractor for performance of a contract.[^far-part-45] **Government-Furnished Equipment (GFE)** is the most commonly used label, particularly for major equipment-type GFP such as the Aegis Combat System, the AN/SPY-6 radar, and the LM2500 main propulsion turbines on a destroyer. The broader GFP category may also include government-furnished material, tooling, test equipment, information, and facilities; this article uses **GFE** in its narrow equipment sense throughout.

**Contractor-furnished equipment (CFE)** is equipment procured by the prime yard under its own contract and incorporated into the deliverable. For destroyer construction, the GFE / CFE allocation by major category is approximately:

| Category | Allocation | Examples |
|---|---|---|
| Combat system / electronics | GFE (overwhelmingly) | Aegis Combat System, AN/SPY-6 radar, Mk 41 VLS, AN/SLQ-32 SEWIP, AN/USG-2B/-3B CEC |
| Ordnance | GFE | Mk 45 5-inch gun, Mk 38 25mm gun, CIWS, VLS canisters |
| Propulsion | GFE | LM2500 gas turbines (four per ship), main reduction gears |
| Hull, mechanical, electrical (HM&E) | CFE | Hull steel, piping, ventilation, electrical systems, outfitting |
| Plan Costs | CFE / lead yard | Class design, planning yard support |

The GFE / CFE classification of a specific item is determined by the underlying contract and budget cycle, not by the item's intrinsic identity, and can change between budget cycles as Navy program-management arrangements evolve.

## The cost funnel

The funnel is the analytical spine of the article. At each level it cuts from the total figure to the addressable subset:

```text
TOTAL SHIP COST (per-class per-FY, from SCN P-5c Total Ship Estimate)
│
├── PLAN COSTS                     engineering, detail design, T&E, config mgmt;
│                                  Bath Iron Works in class Design Agent role
│
├── GOVERNMENT-FURNISHED EQUIPMENT  Navy procures separately, ships to yard:
│      ├── Aegis Combat System      (Lockheed Martin, Moorestown NJ)
│      ├── AN/SPY-6 radar            (Raytheon, Andover MA)
│      ├── Mk 41 VLS                  (Lockheed Martin)
│      ├── Mk 45 5-inch gun           (BAE Systems Land & Armaments)
│      ├── LM2500 propulsion          (GE Aerospace, Evendale OH)
│      ├── AN/SLQ-32 SEWIP            (Northrop Grumman)
│      ├── Mk 15 Phalanx CIWS          (Raytheon)
│      └── Other electronics           (L3Harris, DRS, NG, GD Mission Systems)
│
├── CHANGE ORDERS / OTHER          ECPs, block mods, reserves
│
└── BASIC CONSTRUCTION              the prime contract base — the dollars
   │                                that flow to BIW or Ingalls on the SCN PIID
   │
   ├── YARD SELF-PERFORMED          labor + overhead at Bath / Pascagoula
   │
   └── OUTSOURCED WITHIN BC          one of the principal objects of this article
         │
         ├── FFATA-visible           first-tier subawards reported under
         │                          FAR 52.204-10, published in SAM.gov FSRS
         │
         └── UNSEEN LAYER            ── beyond direct visibility:
              ├── Purchased material booked as direct material
              ├── Lower-tier subs (a sub's sub — not reportable)
              ├── FFATA non-compliance / under-reporting
              └── Long tail under the $30,000 threshold
```

A complete answer to "how much of the destroyer's cost is outsourced" requires a denominator statement: outsourced relative to what? The funnel makes four candidate denominators visible.

### Four denominators of "outsourced"

The choice of denominator is the choice of question. The article reports against each of them where the data supports it, and is explicit about which is being used at every point.

1. **Outsourced from the prime yard** — the share of each yard's own prime construction contract that the yard pays to other firms. The numerator is the yard's first-tier subaward tree under FAR 52.204-10, plus the larger unseen subset of the yard's purchased material and lower-tier subcontracting that is not captured under that clause. GFE primes (Lockheed Martin, Raytheon, GE, BAE for Mk 45) are *not* outsourced from the yard — the yard does not pay them; the Navy does, on a separate prime contract.
2. **Outsourced from the Navy / SCN perspective** — the share of the SCN appropriation that flows to firms other than the two assembling shipyards. This adds the GFE-prime flows to each yard's subaward tree. It is closest to the denominator the Navy's 30-Year Shipbuilding Plan implicitly uses when it discusses "distributed shipbuilding" and "outsourcing partners."[^navy-fy27-plan]
3. **Outside-the-yards** — measured directly per contract action from the U.S. Department of Defense daily contract-announcement press releases, which state explicit percentage breakdowns of where each action's work will be performed. This is the most direct primary-source measurement because it does not depend on accounting categorization at all; the announcement names the cities and the percentages. See [DoD contract announcement data](04-dod-contract-announcement-data.md). The headline 87-percent-outside-yards figure is computed against this denominator.
4. **Private-sector work outside the assembling yards** — any private-firm work not performed inside Bath, Maine (or the BIW Brunswick annex) or Pascagoula, Mississippi. This includes everything in (1) and (2), plus federally funded research and development center (FFRDC) and Department of Defense laboratory work funded outside SCN.

This article emphasizes denominators (2) and (3) in the headlines, and reports (1) explicitly throughout. Denominator (4) is discussed in [The MYP redaction and the unseen layer](12-myp-redaction-and-unseen-layer.md) but not aggregated.

## Scope: window, classes, and the in-scope PIID set

The article uses a **fiscal-year 2018 through fiscal-year 2027 signed-date window** for FPDS prime-contract data and a **fiscal-year 2002 through fiscal-year 2026 action-date window** for FFATA subaward data, where the wider subaward window captures pre-FY2018 actions on still-active master construction contracts. The article's primary substantive coverage is FY2020 forward, where the Justification Book data is complete; FY2018–FY2019 is included as a comparison baseline. The window was chosen to capture the FY18-22 multiyear master awards (DDGs 122–134, awarded September 2018), the FY23-27 multiyear master awards (DDGs 140–150, awarded August 2023), and the annual option-exercise structure that the program has used between MYP blocks.

The article scopes the outsourced-flow analysis to the **in-scope DDG-51 new-construction PIID set** maintained at `extracted/nc_scope_summary.json`. The set was derived by FPDS-search discovery — vendor-name and DDG-class description sweeps against the Navy contracting agency — followed by manual review and classification by program family and class. The set captures the two assembling yards (BIW and Ingalls), the major GFE primes (Lockheed Martin Aegis, Raytheon SPY-6 plus CIWS plus ESSM, GE LM2500, BAE Mk 45 and VLS canisters, Northrop Grumman SEWIP, DRS / Leonardo combat systems, GD Mission Systems, L3Harris CEC), and the smaller engineering and lead-yard-support PIIDs.

A summary of the in-scope set:

- **89 prime PIIDs** discovered and pulled through SAM.gov subaward reporting
- **22,235 in-scope records** kept after the new-construction classification pass
- **$13.8 billion** cumulative subaward dollar value across the in-scope PIID set, FY2002 through FY2026 action date
- **1,954 unique parent vendor UEIs** observed as recipients across the in-scope subaward stream

The PIID set is keyed by group as follows (counts of PIIDs per group):

| Group | PIIDs | Examples |
|---|---:|---|
| GD-BIW | 17 | `N00024-23-C-2305` (FY23-27 MYP master), `N00024-18-C-2305`, `N00024-13-C-2305` |
| HII-Ingalls | 9 | `N00024-23-C-2307` (FY23-27 MYP master), `N00024-18-C-2307`, `N00024-13-C-2307` |
| LM-Aegis | 15 | `N00024-13-C-5116` (Aegis CSEA), `N00024-20-C-5310` (Mk 41 VLS), `N00024-14-C-5114` (Aegis Hardware) |
| Raytheon | 14 | `N00024-22-C-5500` (SPY-6 FLT III), `N00024-18-C-5406` (CIWS), `N00024-21-C-5408` (ESSM) |
| BAE-Guns/VLS | 15 | `N00024-19-C-0004` (Mk 45 production via SPAWAR), `N00024-20-C-5380` (Mk 25 canisters), `N00024-13-C-5314` (Mk 21 canisters) |
| DRS / Leonardo combat systems | 5 | `N00024-20-C-5605`, `N00024-15-C-5228` (USG-3B CEC) |
| GE-Propulsion | 9 | `N00019-11-C-0045`, `N00019-23-C-0013`, `N00019-18-C-1007` (LM2500) |
| Northrop Grumman | 2 | `N00024-20-C-5519` (SEWIP Block 3), `N00024-15-C-5319` (SEWIP EMD) |
| GD Mission Systems | 2 | `N00024-04-C-6205`, `M67854-17-C-0261` |

The full PIID list with labels is preserved in `extracted/nc_scope_summary.json` in the project repository.

The article scope explicitly does **not** include:

- DDG-1000 / Zumwalt-class new construction (closed program; OPN-funded modernization only)
- Cruiser (CG) modernization and depot maintenance (separate appropriation; ship-class out of scope)
- Frigate (FF) / Constellation-class new construction (separate Fincantieri-Marinette prime; future article)
- Amphibious warship (LPD-17, LHA-8) new construction at Ingalls (separate SCN line items, shared Pascagoula labor force but distinct prime contracts)
- National Security Cutter / Polar Security Cutter at Ingalls (Coast Guard appropriation, not SCN)

## Dollar-bucketing conventions

Throughout the article, dollar figures follow these conventions unless explicitly noted otherwise:

- **FPDS prime obligations**: per-modification `obligatedAmount` summed by `signed_date` fiscal year. The cumulative `totalObligatedAmount` field from the FPDS Atom feed is *not* used as a window measurement because it represents the lifetime running total at the time of each modification, not the new dollars added by that modification.
- **FFATA subaward values**: as reported in SAM.gov FSRS, summed by `action_date` fiscal year. Deduplication is by `subAwardReportId` (SAM.gov assigns one unique identifier per published subaward action); duplicate IDs were not observed across the 24,559-record in-scope subaward pull.
- **DoD announcement values**: as reported in the bulletin paragraph. Source-selection-redacted values appear with empty `amount_usd` in the structured CSV and are excluded from dollar-weighted aggregations; their place-of-performance percentages are retained for separate analysis.
- **Currency**: U.S. dollars (USD), then-year (nominal) unless explicitly indexed to a base year.
- **Time horizons**: "Lifetime" means cumulative over the FY2002–FY2026 subaward window. "Annual" means a single fiscal year. "Window" means the FY2018–FY2027 signed-date window for primes and FY2016–FY2026 action-date window for subawards, unless a different window is specified.

[^myp-structure]: The two-yard parallel MYP structure is documented in the FY2027 SCN Justification Book Line Item 2122 P-21 Production Quantities and P-27 Ship Production Schedule exhibits, and in the August 1, 2023 (war.gov article 3479250) and August 11, 2023 (article 3491276) DoD daily contract announcement bulletins, which describe the two awards in parallel prose and explicitly reference the two distinct PIIDs.

[^far-52-204-10]: 48 C.F.R. § 52.204-10, "Reporting Executive Compensation and First-Tier Subcontract Awards." <https://www.acquisition.gov/far/52.204-10>.

[^far-part-45]: 48 C.F.R. Part 45 ("Government Property") and 48 C.F.R. § 52.245-1. <https://www.ecfr.gov/current/title-48/chapter-1/subchapter-G/part-45>; <https://www.acquisition.gov/far/52.245-1>.

[^gao-25-106286]: U.S. Government Accountability Office, *Shipbuilding and Repair: Navy Needs a Strategic Approach for Private Sector Industrial Base Investments*, GAO-25-106286 (February 27, 2025). <https://www.gao.gov/products/gao-25-106286>.

[^navy-fy27-plan]: U.S. Department of the Navy, Fiscal Year 2027 President's Budget, 30-Year Shipbuilding Plan ("Golden Fleet" Plan), April 2026. <https://www.secnav.navy.mil/fmc/fmb/>.
