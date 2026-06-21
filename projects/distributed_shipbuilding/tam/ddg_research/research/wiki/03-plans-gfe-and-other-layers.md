---
title: Plans, GFE, and other layers
---

# Plans, GFE, and other layers

This chapter takes up the cost-category layers above Basic Construction in the cost funnel — Plan Costs, the Electronics-plus-Ordnance Government-Furnished Equipment (GFE) bulge, Hull-Mechanical-Electrical (HM&E), Change Orders, and Other Cost. For DDG-51, the GFE layer is structurally larger than for nuclear submarines, accounting for roughly a third of every ship's Total Ship Estimate on recent vintages, and it is the principal driver of the headline outside-yards measurement reported in chapter 4. Within the GFE layer this chapter introduces the major government-furnished subsystems and their associated prime contractors; the detailed deep dive on each subsystem lives in chapters 10 and 11.

## Plan Costs

**Plan Costs** are the engineering and detail-design work, configuration management, test-and-evaluation, and lead-yard support associated with a specific ship's design and procurement. For the DDG-51 program, the dominant Plans flow occurs through a separate **class Design Agent** contract held by General Dynamics Bath Iron Works covering across-class engineering services — class design, system engineering, integration with the Aegis baseline and SPY-6 deltas, and configuration management — that are not tied to any individual hull but that benefit the program as a whole.

In the per-ship P-5c reporting, Plan Costs appear as a relatively small line: approximately **1.5 percent of Total Ship Estimate** on the FY24 vintage (~$83M across two ships), with a similar share in adjacent vintages. The reason this number is small is that most class-design work is captured in the separate Design Agent and Class Changes Design Services contracts (BIW PIIDs `N00024-18-C-2313` "CLASS CHANGES DESIGN SERVICES" and `N00024-12-C-2313` "FLIGHT III DESIGN" in the in-scope set, plus `N00024-24-C-2313` "DDG 51 CLASS LEAD YARD SUPPORT"). The per-ship P-5c Plan Costs line picks up only the incremental class-design work attributable to that specific ship's contract scope.

A separate Flight III design contract appears in the in-scope set under both BIW (`N00024-12-C-2313`) and Ingalls (`N00024-12-C-2312`) to cover the Flight III variant transition design work (SPY-6 integration, electrical-plant uprating, structural changes to accommodate the larger combat-system suite). These contracts are first-pull-discovered through the FPDS vendor-name search and inherit the lead-yard-support and design-agent role-allocation typical of two-yard programs.

## Government-Furnished Equipment (GFE) — the dominant outsourced layer

For DDG-51, GFE is the principal outsourced layer by dollar weight, both at the per-ship level (Electronics + Ordnance = ~33% of Total Ship Estimate on the FY24 vintage) and at the supplier-TAM-relevant DoD-announcement corpus level (Aegis + SPY-6 alone = ~$5.0B of $7.13B = ~70% of the corpus, per chapter 4).

The major GFE categories, the prime contractor associated with each, and the relevant in-scope PIIDs:

### Aegis Combat System (Lockheed Martin)

The **Aegis Combat System** is the integrated weapon system that ties together the destroyer's sensors (SPY-6 radar, AN/SPS-67 surface radar, AN/SQQ-89 sonar), command-and-decision computers, fire-control systems (Mk 99), and weapons (Mk 41 VLS, Mk 45 gun, CIWS). Lockheed Martin Rotary and Mission Systems (RMS) is the Aegis prime, with the principal facility at **Moorestown, New Jersey** (with additional Aegis work at the LM Owego, NY and LM Manassas, VA sites).

The in-scope Aegis-related PIIDs include `N00024-13-C-5116` (Aegis CSEA Funding Mod), `N00024-14-C-5114` and `N00024-14-C-5106` (Aegis Hardware), `N00024-15-C-5151` (Aegis Ship Integration), `N00024-16-C-5103` (Aegis Implementation Studies), `N00024-19-C-5102` (Korea Batch II Aegis Combat System K2 — a foreign military sales export contract), `N00024-20-C-5105` (International Aegis Fire Control Loop), `N00024-13-C-5132` (Aegis Development and Test Sites Operation and Maintenance), `N00024-14-C-5104` (Aegis SI&T Installation/Modernization), and `N00024-15-C-5332` (USN DDG 127 Mk 41 Mod 15 VLS Mech).

DoD-announcement actions tagged `ddg_gfe_aegis` total **74 actions / $3,547.8M** in the supplier-TAM-relevant corpus. Dollar-weighted POP distribution: BIW 0.7%, Ingalls 0.7%, Other-US suppliers 86.0%, Foreign 0% — the most outside-yards-concentrated bucket in the entire corpus.

### AN/SPY-6(V)1 Air and Missile Defense Radar (Raytheon)

The **AN/SPY-6(V)1** is the Flight III variant DDG-51 primary radar — a phased-array S-band radar that replaced the AN/SPY-1D used on Flight IIA destroyers and earlier. It is roughly 30 times more sensitive than the SPY-1D and was developed under the Air and Missile Defense Radar (AMDR) program. The prime contractor is **Raytheon, an RTX business**, with the principal facility at **Andover, Massachusetts**.

The in-scope SPY-6-related PIIDs include `N00024-22-C-5500` ("DDG FLT III (AN/SPY-6(V)1)") — the principal Flight III production contract — and `N00024-14-C-5315` ("AMDR EMD (BASE)"), the original engineering, manufacturing, and development contract under which the radar was developed.

DoD-announcement actions tagged `ddg_gfe_radar` total **7 actions / $1,475.1M** in the supplier-TAM-relevant corpus. Dollar-weighted POP distribution: BIW 0%, Ingalls 0%, Other-US 82.0%, Foreign 0%.

### Mk 41 Vertical Launching System (Lockheed Martin)

The **Mk 41 Vertical Launching System (VLS)** is the destroyer's missile launcher — a multi-cell vertical launcher that fires Standard Missile-2/3/6, Evolved Sea Sparrow Missile (ESSM), and Tomahawk land-attack cruise missile. Each Flight IIA DDG carries 96 VLS cells (32 forward + 64 aft); Flight III carries the same. Lockheed Martin Rotary and Mission Systems is the prime for the launcher mechanical assembly, with structural manufacturing performed by subcontractors including **Major Tool & Machine** (Indianapolis, IN), **Leonardo S.p.A.** (via DRS Defense Solutions subsidiary), and **Merrill Aviation** (Saginaw, MI).

The in-scope Mk 41-related PIIDs include `N00024-20-C-5310` ("MK 41 MOD 36 VLS MODULE MECH") and `N00024-23-C-5325` ("MK 41 VLS MODULE AND ANCILLARY EQUIPMENT").

DoD-announcement actions tagged `ddg_gfe_vls` total **16 actions / $533.4M** in the supplier-TAM-relevant corpus. Dollar-weighted POP distribution: BIW 0.2%, Ingalls 0.2%, Other-US 95.0%, Foreign 0% — the highest outside-yards share of any bucket.

### Mk 45 5-inch / 62-caliber gun (BAE Systems)

The **Mk 45 5-inch / 62-caliber naval gun** is the DDG-51's primary surface-fire gun. The Mod 4 variant is the current production model. BAE Systems Land & Armaments holds the prime contract, with production at **Louisville, Kentucky** (Mk 45 mount and gun barrel) and **Minneapolis, Minnesota** (gun fire-control electronics). The in-scope Mk 45 PIID is `N00024-19-C-0004` ("MK45 PRODUCTION CONTRACT") under the Naval Sea Systems Command Indian Head contracting office (PIID prefix `N00174`).

DoD-announcement actions tagged `ddg_gfe_guns` total **5 actions / $117.4M** in the supplier-TAM-relevant corpus. Dollar-weighted POP: BIW 0%, Ingalls 0%, Other-US 100% (all at BAE Louisville and Minneapolis).

BAE Systems also holds the VLS canister contracts (Mk 13, Mk 21, Mk 25 canisters that hold the missile in the VLS cell), with PIIDs `N00024-20-C-5380` (Mk 25 Mod 1 canisters), `N00024-13-C-5314` (Mk-21 Mod 3 canisters), `N00024-24-C-5324` (Mk 21 Mod 4 canisters with PHS&T), and `N00024-12-C-5311` (FPI final price revision). These are tagged as a separate bucket (`ddg_gfe_vls` canister sub-bucket).

### LM2500 Marine Gas Turbines (GE Aerospace)

The **LM2500 marine gas turbine** is the DDG-51's main propulsion engine. Each destroyer carries **four LM2500-class turbines** (two per shaft, twin-shaft configuration) producing approximately 26,250 shaft horsepower each. GE Aerospace (spun off from General Electric Company in April 2024) holds the prime contract, with production at **Evendale, Ohio** and **Lynn, Massachusetts**.

The LM2500 PIIDs are issued under the Naval Air Systems Command (NAVAIR) contracting office (PIID prefix `N00019`) rather than NAVSEA — historical artifact of the LM2500's origin as an adapted CF6 commercial jet engine that NAVAIR's aviation logistics community has long managed. The in-scope LM2500 PIIDs include `N00019-23-C-0013`, `N00019-18-C-1007`, `N00019-18-C-1061`, and `N00019-23-F-0642`.

DoD-announcement actions tagged `ddg_gfe_propulsion` total **7 actions / $192.2M** in the supplier-TAM-relevant corpus. Dollar-weighted POP: BIW 0%, Ingalls 0%, Other-US 19.2%, Foreign 0% — the apparent underweighting reflects an open parser issue with single-supplier-no-percentage bulletin paragraphs that have not been fully attributed (see chapter 12 §The single-supplier-no-% parser caveat).

### AN/SLQ-32 SEWIP electronic warfare (Northrop Grumman)

The **AN/SLQ-32 Surface Electronic Warfare Improvement Program (SEWIP)** is the destroyer's primary electronic-warfare suite. SEWIP Block 3 is the current major upgrade providing active electronic attack capability. Northrop Grumman Systems Corporation is the prime, with the in-scope PIIDs `N00024-20-C-5519` ("SEWIP BLOCK 3 DMS LIFETIME BUY AWARD AND OTHER ADMINISTRATIVE CHANGES") and `N00024-15-C-5319` ("EMD - AN/SLQ-32(V)Y SEWIP BLOCK 3"). The SEWIP Block 3 production contract carries a cumulative FFATA-subaward total of approximately $38.6M against the principal `N00024-20-C-5519` PIID.

### Other combat-system electronics

A miscellany of smaller GFE flows complete the combat-system layer:

- **AN/SPQ-9B X-band horizon-search radar** (Northrop Grumman, Linthicum, MD) — Flight III addition, surface and low-altitude threat detection
- **AN/USG-2B and AN/USG-3B Cooperative Engagement Capability (CEC)** hardware (DRS Laurel Technologies, a Leonardo DRS subsidiary, plus L3Harris) — networked fire-control data sharing across multiple Aegis ships
- **AN/SQQ-89 anti-submarine warfare combat system** (Lockheed Martin) — sonar plus undersea-warfare integration
- **AWS Director / Director Controller** (per the FY27 SCN P-5b contractor table) — General Dynamics Mission Systems

DoD-announcement actions tagged `ddg_gfe_combat_systems` (a catchall for the smaller combat-system flows) total **8 actions / $252.5M** in the supplier-TAM-relevant corpus. Dollar-weighted POP: BIW 0%, Ingalls 0%, Other-US 100%.

### Mk 15 Phalanx Close-In Weapon System (Raytheon)

The **Mk 15 Phalanx CIWS** is the destroyer's terminal-defense gun system against anti-ship missiles. Raytheon is the prime. The CIWS PIID `N00024-18-C-5406` ("MK15 PHALANX BK 0 TO 1B BL 2 U&C") carries approximately $1.13 billion of cumulative FFATA subaward value across 3,661 records — the largest single PIID in the in-scope subaward stream.

CIWS is, however, funded under Weapons Procurement (WPN) and Other Procurement (OPN) rather than SCN, so it is tagged `ddg_gfe_weapons` and **excluded from the headline TAM gate** (`is_ddg_new_construction_tam == 'no'`). Including it would double-count against a different appropriation. Similar logic applies to Standard Missile, ESSM, and Tomahawk procurement, all of which use Raytheon prime contracts and which appear in DoD bulletins but are tagged `borderline` and excluded from the SCN-scope analysis.

## Hull, Mechanical, and Electrical (HM&E)

The **HM&E** cost-category line first appears as a distinct line in the FY24 SCN P-5c vintage. It captures the major hull, mechanical, and electrical equipment that is not captured under either Electronics or Ordnance: main reduction gears, generators, switchboards, large-diameter piping, ventilation, deck machinery, anchor windlass, steering gear, and fixed-pitch propellers.

For FY24 (the first vintage with HM&E broken out separately), HM&E was reported at $100.7M across two ships — approximately **1.8 percent of Total Ship Estimate**. The actual flow of HM&E procurement is larger than this because most HM&E components are procured *by the yard* rather than as government-furnished equipment, and therefore flow through the Basic Construction line rather than the HM&E line. The HM&E P-5c line picks up only the government-furnished HM&E items: most prominently the main reduction gears (Timken Gears & Services), some generators, and selected propulsion-auxiliary equipment.

## Change Orders and Other Cost

**Change Orders** capture engineering change proposals (ECPs), block modifications, and post-award scope changes against the basic construction contract. They run at approximately 1.7 percent of Total Ship Estimate on recent vintages.

**Other Cost** is a small residual category — approximately 1.6 percent of Total Ship Estimate — capturing program management reserves, transition costs, and miscellaneous items not elsewhere classified.

Together, Change Orders plus Other Cost run at approximately 3 percent of Total Ship Estimate, comparable to the same residual in the submarine programs.

## Summary: where the dollars go

For the FY24 two-ship buy at $5,492.3M of Total Ship Estimate, the layered allocation:

| Layer | Share | $M (FY24 both ships) | Outsourced status |
|---|---:|---:|---|
| Plan Costs | 1.5% | 82.7 | Mixed (BIW Design Agent + per-ship Plans) |
| Basic Construction/Conversion | 60.5% | 3,322.5 | Yard self-perform + yard first-tier subs |
| Change Orders | 1.7% | 91.6 | Mixed |
| Electronics (Aegis, SPY-6, etc.) | 11.3% | 619.8 | **GFE — outsourced to Navy-procured primes** |
| HM&E | 1.8% | 100.7 | Mostly yard CFE; small GFE share |
| Ordnance (Mk 41 VLS, Mk 45, CIWS, missiles) | 21.6% | 1,187.5 | **GFE — outsourced to Navy-procured primes (excl. CIWS/missiles funded WPN)** |
| Other Cost | 1.6% | 87.7 | Mixed |
| **Total Ship Estimate** | **100.0%** | **5,492.3** | |

The roughly **33 percent of total ship cost flowing through Electronics plus Ordnance** is the structural reason that DDG-51 outsourcing is GFE-heavy. The subsequent chapter (chapter 4, DoD contract announcement data) measures the actual place-of-performance of this GFE flow plus the smaller flow through the yard subaward trees, and reports the headline: approximately **87 percent of dollar-weighted POP** on supplier-TAM-relevant actions occurs outside the two destroyer shipyards — overwhelmingly at the Lockheed Martin Moorestown and Raytheon Andover GFE supplier sites.

The remaining roughly 60 percent of total ship cost — Basic Construction — is split between yard self-perform (labor and overhead in Bath, ME, and Pascagoula, MS) and yard first-tier subcontracts (hull steel, HM&E, electrical, outfitting). The yard self-perform share is *not* directly measurable from federal procurement data; chapter 9 estimates it via the residual implied by Huntington Ingalls's segment 10-K disclosures and a labor-cost decomposition against Bureau of Labor Statistics wage data.
