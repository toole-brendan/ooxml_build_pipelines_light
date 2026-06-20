# USAspending Structured Fields -- PSC, NAICS, DoD Acquisition Program

Findings from exploring USAspending's structured classification fields as an alternative or complement to FPDS description-based searching.

Last updated: 2026-04-15

---

## The Three Classification Systems

### PSC (Product or Service Code) -- What specific product or service is being bought

- ~2,500 codes maintained by GSA
- Granular product/service codes: 1901 = "Aircraft Carriers", 1905 = "Combat Ships and Landing Vessels", J998 = "Non-Nuclear Ship Repair (East)", 5865 = "Electronic Countermeasures", 1210 = "Fire Control Directors"
- For shipyard work, PSC has two parallel tracks: product codes (19xx) classify by vessel type (1901 = carriers, 1905 = combat ships), while service codes (J998/J999) classify the work as ship repair. PSC 1905 is NOT "construction" -- it covers all work where the end item is a combat vessel (construction, RCOH, planning yard, lead yard, PSA, ship alterations, dismantlement, etc.). J998/J999 specifically means repair services. A DDG depot availability may be coded J998 or 1905 depending on how the contracting officer classified it
- For system-specific work, PSC codes are highly specific but scattered -- Aegis is PSC 1210 (fire control), SEWIP is PSC 5865 (ECM), SQQ-89 is PSC 3590 (misc service equip), CEC is PSC 1265 (fire control TX/RX). Each combat system ends up under a different PSC, and those PSCs also capture non-Navy contracts (Air Force EW, Army radar)

### NAICS (North American Industry Classification System) -- What type of work is being done

- ~1,000 codes, maintained by Census Bureau
- Describes the nature of the work/industry: 336611 = "Ship Building and Repairing", 334511 = "Search, Detection, Navigation, Guidance, Aeronautical, and Nautical System and Instrument Manufacturing", 541330 = "Engineering Services"
- More useful than initially expected: NAICS 334511 captures ALL combat system electronics work (Aegis, SEWIP, SQQ-89, CEC, SEWIP 1B3) under one code, regardless of which specific PSC the contracting officer chose. This is a cleaner way to pull the full combat system modernization universe than trying to enumerate individual PSC codes
- For shipyard work, NAICS 336611 covers both construction and repair -- does NOT distinguish between them. PSC is better for that split
- Also used for small business size standards

### DoD Acquisition Program (DAP) -- Which program is this for

- DoD-specific, ~300-400 codes
- Maps to Major Defense Acquisition Programs (MDAPs) and other tracked programs
- Examples: 223 = CVN 78, 180 = DDG 51, 110 = AEGIS, 582 = CEC
- Would be the most powerful filter if it were reliably populated -- but it isn't (see below)

---

## PSC Codes Relevant to Our Work

| PSC | Description | What it captures for us |
|-----|-------------|------------------------|
| 1901 | Aircraft Carriers | CVN construction contracts |
| 1905 | Combat Ships and Landing Vessels | All work where end item is a combat vessel -- construction, RCOH, planning yard, lead yard, PSA, alterations, dismantlement. NOT just construction. |
| J998 | Non-Nuclear Ship Repair (East/West) | Depot availabilities, MSMOs, SRAs -- pure MRO |
| J999 | Nuclear Ship Repair | Mix of nuclear + non-nuclear MSMOs |
| J019 | Ships, Small Craft, Pontoons (maint) | Additional ship maintenance contracts |
| 5865 | ECM/ECCM Equipment | SEWIP Block 2/3 (but also Air Force EW) |
| 5840 | Radar Equipment | SPY-1/SPY-6, Aegis CSEA (but also Army/AF radar) |
| 1210 | Fire Control Directors | Aegis mods, MK82/MK200 directors |
| 1265 | Fire Control TX/RX | CEC |
| 5999 | Misc Electrical Components | VLS power supply (catch-all) |
| 3590 | Misc Service Equipment | SQQ-89 (catch-all) |
| R425 | Engineering/Technical Support | SPY-1 OEM services (catch-all) |

## NAICS Codes Relevant to Our Work

| NAICS | Description | What it captures for us |
|-------|-------------|------------------------|
| 336611 | Ship Building and Repairing | ALL shipyard work -- construction AND repair. Does not distinguish between them. |
| 334511 | Search, Detection, Navigation, Guidance... Manufacturing | ALL combat system electronics: Aegis, SEWIP, SQQ-89, CEC, SEWIP 1B3. Single code covers what PSC scatters across 5865/5840/1210/1265/3590. |
| 334519 | Other Measuring and Controlling Device Manufacturing | VLS power supply (Laurel Technologies) |
| 541330 | Engineering Services | SPY-1 OEM engineering support (Raytheon) |

**Key insight: NAICS 334511 is the best single filter for "all combat system electronics work."** It captures every major combat system contract (Aegis, SEWIP Blk 2, SEWIP Blk 3, SQQ-89, CEC, SEWIP 1B3, Aegis CSEA) under one code. The equivalent PSC-based approach requires enumerating 5+ different PSC codes, each of which also returns non-Navy contracts. Combining NAICS 334511 + Navy agency filter would give a much cleaner combat system universe than any PSC-based query.

---

## DoD Acquisition Program Codes -- Verified on Live Awards

| DAP Code | Program | Where it appears |
|----------|---------|-----------------|
| 180 | DDG 51 | Construction primes only |
| 223 | CVN 78 | Construction primes (CVN-78 ship construction) |
| 110 | AEGIS | Aegis CSEA contract |
| 582 | CEC | CEC Design Agent contract |
| 000 | NONE | Most MRO contracts -- depot avails, SEWIP, SQQ-89, propulsion, VLS |

**Critical finding: DAP=000 on nearly all MRO contracts.** The field is only populated on major construction primes and a few tracked acquisition programs (Aegis, CEC). Cannot be used to pull "all DDG-51 MRO."

---

## DoD Claimant Code -- Useful as a Structural Separator

| Code | Description | What it separates |
|------|-------------|-------------------|
| A3 | SHIPS | Depot work, construction, lead yard services |
| A7 | ELECTRONICS AND COMMUNICATION EQUIPMENT | Combat system modernization (Aegis, SEWIP, SQQ-89, CEC, SPY) |

---

## Verified Field Assignments on Known Contracts

System-specific modernization contracts:

| Contract | Program | PSC | NAICS | DAP | Claimant |
|----------|---------|-----|-------|-----|----------|
| N0002414C5106 | Aegis Modernization (LM) | 1210 (Fire Control Directors) | 334511 | 000 (NONE) | A7 |
| N0002416C5363 | SEWIP Block 2 (LM) | 5865 (ECM/ECCM) | 334511 | 000 (NONE) | A7 |
| N0002420C5519 | SEWIP Block 3 (NG) | 5865 (ECM/ECCM) | 334511 | 000 (NONE) | A7 |
| N0002413C5225 | SQQ-89 (LM) | 3590 (Misc Service Equip) | 334511 | 000 (NONE) | A7 |
| N0002419C5200 | CEC Design Agent (RTX) | 1265 (Fire Control TX/RX) | 334511 | 582 (CEC) | A7 |
| N0002413C5116 | Aegis CSEA (LM) | 5840 (Radar) | 334511 | 110 (AEGIS) | A7 |
| N0002416C5352 | SEWIP Block 1B3 (GDMS) | 5865 (ECM/ECCM) | 334511 | 000 (NONE) | A7 |
| N6339420C0008 | VLS Power Supply (Laurel) | 5999 (Misc Elec Components) | 334519 | 000 (NONE) | A7 |
| N6339421C0004 | SPY-1 OEM Services (RTX) | R425 (Engineering/Tech Spt) | 541330 | 000 (NONE) | C9E |

Note: Every combat system contract except VLS and SPY-1 OEM has NAICS 334511. PSC codes are scattered across 5 different values (1210, 5865, 3590, 1265, 5840). NAICS is the better single filter for this category.

Depot availability contracts:

| Contract | Program | PSC | NAICS | DAP | Claimant |
|----------|---------|-----|-------|-----|----------|
| N0002420C4460 | DDG-87 Mason DMP (Metro Machine) | J998 | 336611 | 000 (NONE) | A3 |
| N0002423C4486 | DDG-82 Lassen DMP (BAE Jax) | J998 | 336611 | 000 (NONE) | -- |
| N0002410C4308 | DDG Docker Norfolk MSMO (BAE) | J998 | 336611 | 000 (NONE) | A3 |
| N0002411C4400 | CG San Diego MSMO (BAE) | J999 | 336611 | 000 (NONE) | A3 |
| N0002424C4418 | LHD-5 Bataan DSRA (Metro) | J998 | 336611 | 000 (NONE) | A3 |

Construction contracts:

| Contract | Program | PSC | NAICS | DAP | Claimant |
|----------|---------|-----|-------|-----|----------|
| N0002418C2307 | DDG-51 FY18-22 MYP (HII) | 1905 | 336611 | 180 (DDG 51) | A3 |
| N0002408C2110 | CVN-78 Construction (HII) | 1901 | 336611 | 223 (CVN 78) | A3 |
| N0002420C2300 | FFG-62 DD&C (Marinette) | 1905 | 336611 | 000 (NONE) | A3 |

---

## USAspending Query Results

### PSC J998 (Ship Repair) -- Full Universe

- 5,000+ awards, $23.1B+ (FY17-26, DoD)
- **Every result is a depot availability, MSMO, SRA, DSRA, DMP, or ship repair contract**
- Zero construction contamination -- PSC structurally separates repair from construction
- Filterable by keyword for ship class: "DDG" returns pure DDG depot work

### PSC J998 + keyword "DDG" -- DDG Depot MRO

Top results (all depot availabilities):

| PIID | Amount | Contractor | Description |
|------|--------|------------|-------------|
| N0002410C4308 | $1.02B | BAE Systems Norfolk | DDG Docker Norfolk MSMO |
| N0002417C4444 | $428M | HII | DDG62 Repair/Restoration/Modernization |
| N0002410C4406 | $374M | BAE Systems Jax | CG/DDG Mayport MSMO |
| N0002410C4405 | $279M | Marine Hydraulics | DDG Non-Docker Norfolk MSMO |
| N0002420C4468 | $209M | BAE Systems Jax | DDG-64 & DDG-81 Availabilities |
| N0002423C4412 | $168M | BAE Systems Norfolk | DDG-94 FY23 DMP |

$4.53B across top 40 results. Clean data, no construction contamination, no false positives.

### PSC 1905 (Combat Ships) -- Vessel Category, NOT Construction-Only

- Returns all contracts where the end item is a combat ship or landing vessel
- Includes construction, RCOH, planning yard, lead yard, PSAs, ship alterations, submarine maintenance, CVN PIAs, LCAC SLEPs, DDG(X) design engineering, ship dismantlement, MUSV DD&F
- PSC 1905 is a vessel-type filter, not a work-type filter -- it does NOT cleanly separate construction from MRO
- The distinction between 1905 and J998 is product code vs service code, not construction vs repair. Some depot/maintenance contracts are coded 1905, others J998

### Electronics PSCs (5865, 5840, 1210) -- System-Specific but Scattered

- Return relevant combat system contracts (SEWIP, SPY, Aegis)
- But each system lands under a different PSC code (SEWIP=5865, Aegis=1210, SQQ-89=3590, CEC=1265, Aegis CSEA=5840)
- Each PSC also returns non-Navy contracts (F-15 EW, Army radar, etc.)
- **NAICS 334511 is a better approach** -- one code covers all combat system electronics across all systems, and adding a Navy agency filter eliminates cross-service noise

---

## Assessment

### What PSC + NAICS filtering gives you

1. **Clean ship repair pulls.** PSC J998/J999 reliably identifies ship repair service contracts (depot availabilities, MSMOs, SRAs). Note: PSC 1905 is NOT the construction counterpart -- it's a vessel-type code that includes construction, RCOH, planning yard, and other work. J998 is the clean filter; 1905 is a broad vessel category.
2. **Cleaner depot availability pulls.** PSC J998 + class keyword = pure depot MRO for any ship class. 100 records/page vs FPDS's 10. JSON vs XML.
3. **No geographic false positives.** J998 is ship repair by definition -- no NAS Whidbey Island aviation contracts leaking in.
4. **Single-code combat system universe.** NAICS 334511 + Navy agency = all combat system electronics (Aegis, SEWIP, SQQ-89, CEC, etc.) in one query. Cleaner than enumerating 5+ PSC codes that each also return non-Navy contracts.

### What PSC + NAICS filtering doesn't give you

1. **System-level classification from top-level award data alone.** No SWBS field in any public procurement database. NAICS 334511 gets you all combat electronics but doesn't distinguish Aegis from SEWIP from SQQ-89. Still need description regex for SWBS mapping. **However:** USAspending's transactions endpoint provides per-modification descriptions that are rich enough for classification (see "Transaction-Level Data" section below).
2. **OT records.** USAspending has no dedicated OT award type code. FPDS remains the only reliable source for Other Transaction data (dedicated XML record types: OtherTransactionAward, OtherTransactionIDV).
3. **Ship class filtering without keywords.** PSC tells you what product/service, NAICS tells you what industry -- neither encodes ship class. DAP=000 on 76% of MRO contracts (13/17 sampled). Still need keywords to narrow to a specific class, with the caveat that two-character designators like "CG" get silently dropped by USAspending (use hull numbers instead).

---

## Transaction-Level Data -- The Missing Piece

**USAspending has per-modification data.** The `/api/v2/transactions/` endpoint returns every modification on a contract with its own description, obligation amount, and action date. This is the same data FPDS gives us, accessible through USAspending's JSON API.

This matters because top-level award descriptions are often generic ("LEAD YARD SUPPORT", "BASIC AWARD"), but modification descriptions name specific systems and work items. Example from EB Lead Yard Support (N0002420C2120, PSC 1905, $4.2B):

| Mod | Description | SWBS Signal |
|-----|-------------|-------------|
| A00001 | HOTWELL REDESIGN EFFORT | 2xx Propulsion |
| A00005 | COMMON WEAPONS LAUNCHER (CWL) HARDWARE | 7xx Armament |
| A00007 | REDESIGN OF CENTRAL ATMOSPHERIC MONITORING SYSTEM | 5xx Auxiliary |
| A00010 | SOFTWARE UPDATES | 4xx Cmd/Surv |
| A00015 | DIESEL GENERATOR OBSOLESCENCE | 3xx Electric |
| A00016 | COMMON WEAPONS LAUNCHER TECHNICAL INSERTION AND ADVANCED PROCESSOR BUILD | 7xx Armament |
| A00021 | SERVO-VALVE REDESIGN | 5xx Auxiliary |

A single "Lead Yard Support" contract that touches 5 different SWBS groups -- invisible from the top-level description, fully classifiable from modification descriptions.

**This means the entire pull-and-classify workflow can run through USAspending alone:**

1. **Discover contracts** via NAICS/PSC structured queries (JSON, 100/page)
2. **Pull modification descriptions** via the transactions endpoint per PIID
3. **Classify by SWBS** using the same regex we already have, applied to mod descriptions
4. **Deduplicate and aggregate** using the same logic (latest mod for dollars, all mods for classification)

FPDS is no longer required for mod-level descriptions. Its remaining unique value is OT records (dedicated XML types that USAspending doesn't track) and description-only search (DESCRIPTION_OF_REQUIREMENT as a dedicated field, vs USAspending keywords matching all fields). For everything else, USAspending can handle both discovery and classification.

---

## Recommendation: Hybrid Approach for Phase 3 Classes

Phase 1+2 data (2,539 contracts, 11 classes) is already pulled via FPDS and clean. No reason to redo. For Phase 3 classes (T-AO, T-AKE, T-AGOS, MCM, USCG cutters, MSC ships, unmanned), use a hybrid:

### Step 1 -- USAspending PSC J998/J999 for ship repair universe

Replaces FPDS Tier 2+3 action-verb searches:

```
PSC J998/J999 + keyword [class designator] + DoD + FY17-26
```

J998/J999 reliably identifies ship repair service contracts. Gets depot availabilities per class, 100 records/page, no geographic false positives. Massively simpler than crafting 15 FPDS action-verb searches per class.

**Keyword caveat:** Two-character class designators ("CG") get silently dropped by USAspending. Use hull numbers instead (e.g., "CG 58", "CG 69", etc.).

### Step 2 -- USAspending NAICS 334511 for combat system electronics universe

```
NAICS 334511 + Navy agency + FY17-26
```

A single NAICS code captures ALL combat system electronics work -- Aegis, SEWIP, SQQ-89, CEC, SEWIP 1B3, Aegis CSEA -- under one filter. The equivalent PSC approach requires 5+ separate codes (1210, 5865, 3590, 1265, 5840), each of which also returns non-Navy contracts. NAICS 334511 + Navy gives you a clean combat system universe in one query. Still need description regex to classify into SWBS sub-systems, but the discovery step is dramatically simpler.

### Step 3 -- FPDS for system-specific classification and OT data

Keep current Tier 1 approach for classification:

```
DESCRIPTION_OF_REQUIREMENT:"system name" + agency filter
```

FPDS description search remains the best way to classify contracts by specific system (Aegis vs SEWIP vs SQQ-89) and the only source for Other Transaction data. But the discovery role shifts to USAspending -- use FPDS to enrich/classify contracts already found via PSC/NAICS, rather than as the primary discovery tool.

### Step 4 -- USAspending as validation/discovery layer

Compare USAspending PSC/NAICS results against FPDS results. Any USAspending award not in the FPDS pull is a candidate that was missed.

### For existing Phase 1+2 data -- validation

Run the J998 query per class and compare against the FPDS-sourced depot contracts to check for coverage gaps.

---

## Newbuild Subawards -- PSC 1905 as a Discovery Tool

**This is the single clearest win from the USAspending structured approach.**

A single query -- PSC 1905 + DoD -- returns the complete universe of combat ship contracts (construction, RCOH, planning yard, and more). This is broader than just construction, but it captures every construction PIID along with related work. Our original FPDS keyword approach found 40 construction PIIDs to pull subawards for. PSC 1905 surfaces 79 additional contracts over $100M that we haven't checked for subaward data. Many of these are HII contracts (CVN-79 DD&C, CVN-80 Engineering, LHA-8 DD&C, LPD 33-35 DD&C, RCOH contracts) -- and HII is the one prime that reports rich, SWBS-coded subaward data.

The subaward reporting gap across primes is a reporting behavior issue, not a data source issue:

| Prime | Subaward Reporting Quality |
|-------|---------------------------|
| HII (Ingalls/Newport News) | Excellent. Thousands of subawards per contract, many coded to SWBS via "PS" codes in descriptions. 15-80% of contract value reported. |
| Electric Boat | High volume (10,000+) but generic descriptions. Mostly unclassifiable. |
| NASSCO | Moderate. 1,495 subawards on ESB-6, but descriptions are "NON-SPEC MATERIAL", "FOS MATERIAL". Vendor names provide some signal (Fairbanks Morse = diesels, Kloeckner = steel). |
| Textron (LCAC) | Good. 583-698 subawards with component-level descriptions (C4N kit, lift fan impellers, propeller pitch control, generators). Classifiable to systems. |
| BIW | Near-zero. 93 subawards totaling $6.7M on a $4.9B contract (0.14%). Only small-dollar vendor services and parts. |
| Marinette/Fincantieri (FFG-62) | Zero subawards reported. |
| Austal | Zero subawards reported. |
| Bollinger | Zero subawards reported. |

Switching to PSC-based discovery doesn't change what primes choose to report -- but it ensures we find every HII and Textron contract that does have rich data, without relying on keyword searches to discover them first.

**Action item:** Pull subawards for all HII construction PIIDs found via PSC 1905 that aren't in the existing 40-PIID set. Priority targets: CVN-79 (2,976 subs), CVN-80 (137,423 subs), LHA-8 (837 subs), LHA-9 (446 subs), LPD 33-35, and RCOH contracts.
