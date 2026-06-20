# NAICS Pull Strategy for USAspending Data Collections

Which NAICS codes to target, in what order, and why -- based on analysis of the 2022 NAICS Structure, verified field assignments on live contracts, and empirical NAICS distribution from 17,105 raw FPDS records across 11 vessel classes.

Last updated: 2026-04-15

---

## How NAICS Works for Our Purposes

NAICS classifies the **industry of the vendor performing the work**, not the work itself. A Raytheon combat system modernization contract and a Raytheon air defense radar for the Air Force both land under NAICS 334511 because Raytheon is in the "search, detection, navigation" manufacturing industry regardless of which service bought it.

This means:
- NAICS is excellent for capturing the **full universe** of a particular type of work (all combat electronics, all turbine manufacturing)
- NAICS requires a **service/agency filter** to isolate Navy-specific contracts from cross-service noise
- NAICS does **not** separate construction from MRO, newbuild GFE from fleet modernization, or one ship class from another -- those separations require PSC codes, description parsing, or DAP codes

The pull strategy below uses NAICS as the primary discovery axis, with PSC and agency filters to narrow results, and description-based classification (the existing SWBS regex) applied downstream.

---

## Tier 1 -- Core Collections (Pull First)

These three NAICS codes account for ~84% of all records and ~95%+ of all dollars in our existing FPDS data. They are the foundation of the USAspending re-pull.

### 336611 -- Ship Building and Repairing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 10,784 (63% of all records) |
| What it captures | ALL shipyard work -- construction, repair, RCOH, planning yard, lead yard, PSA, dismantlement |
| Key PSC pairings | 1905 (7,186), J999 (1,310), J998 (609), K019 (401), J019 (206), 2010 (122) |
| Key vendors | HII, EB, BIW, NASSCO, BAE, Fincantieri, Austal, Metro Machine, Marine Hydraulics |

**Why it matters:** This is the broadest single pull. One NAICS code captures every contract where the vendor is in the shipbuilding/ship repair industry. It picks up both construction primes and depot maintenance yards. The PSC code on each record then separates the work type: 1905/1901/1904 = vessel product work (construction, RCOH, etc.), J998/J999 = repair services, K019 = modification/alteration of ships.

**Filter:** NAICS 336611 + Navy subtier agency. No keyword needed -- the NAICS itself is specific enough.

**Limitation:** Misses contracts where the vendor is classified under a different industry even though the work is ship-related. A Raytheon contract to build SPY-6 radar arrays that go on DDGs will be coded 334511 (electronics manufacturing), not 336611. A GE contract to overhaul LM2500 gas turbines will be 333611 (turbine manufacturing). The ship system OEM universe is in Tier 1b and Tier 2, not here.

### 334511 -- Search, Detection, Navigation, Guidance, Aeronautical, and Nautical System and Instrument Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 306 |
| Estimated dollar value | $8-12B (based on known contracts: Aegis $1.8B, SEWIP $0.9B, SQQ-89 $1.2B, CEC $0.6B, etc.) |
| What it captures | ALL combat system electronics -- Aegis, SEWIP Block 2/3, SQQ-89, CEC, SSDS, SPY-1/SPY-6, BYG-1, SEWIP 1B3, Aegis CSEA |
| Key PSC pairings | 5845 (102), 1210, 5865, 5840, 3590, 1265 -- scattered across 5+ PSC codes |
| Key vendors | Lockheed Martin, Raytheon, Northrop Grumman, GDMS, DRS/Leonardo |

**Why it matters:** This is the single best filter for combat system modernization -- the segment that drives the 4xx Command & Surveillance and 7xx Armament SWBS groups in our model. The equivalent PSC approach requires enumerating 5+ codes (1210, 5865, 5840, 3590, 1265), each of which also returns Air Force/Army contracts. NAICS 334511 + Navy gives a clean combat system electronics universe in one query.

**Filter:** NAICS 334511 + Navy subtier agency.

**Limitation:** Does not distinguish Aegis from SEWIP from SQQ-89 -- still need description regex for SWBS sub-system classification. Also does not capture the VLS power supply (Laurel Technologies), which is coded 334519. Does not capture weapons (missiles, torpedoes) which are 336414.

### 541330 -- Engineering Services

| Metric | Value |
|--------|-------|
| Records in FPDS data | 3,293 (19% of all records) |
| What it captures | Engineering support, SPY-1 OEM services, design agent contracts, planning yard engineering, lifecycle engineering, DMSMS support, test and evaluation |
| Key PSC pairings | R425 (1,979), R499 (208), AC34 (152), R410 (88), J099 (87) |
| Key vendors | Raytheon (SPY-1 OEM), SAIC, Leidos, Serco, Booz Allen Hamilton, various small engineering firms |

**Why it matters:** Engineering services is the #2 NAICS code by record count. It captures the engineering support contracts that feed the "Sustainment Engineering / Planning" and "Cross-System Modernization Labor" rows in the MRO model. SPY-1 OEM services (Raytheon, $53M) are here, not under 334511, because the contract is for engineering services rather than manufacturing. CSEA engineering support from SAIC ($32M) is here.

**Filter:** NAICS 541330 + Navy subtier agency. This will be a large result set (potentially 5,000+ awards). Consider adding PSC filters (R425, R499, J099, AC34) to narrow to ship-relevant engineering vs. base/facility engineering.

**Limitation:** Very broad. "Engineering Services" covers everything from ship systems engineering to base infrastructure design. Navy-filtered results will still include pier construction engineering, environmental engineering, facilities engineering. Will need aggressive post-filtering by description to isolate ship system work.

---

## Tier 2 -- System-Specific Manufacturing (Pull Second)

These codes capture the OEM and component-level work that 336611 misses. Each maps to a specific SWBS group or sub-system. Lower record counts but critical for system-level traceability.

### 333611 -- Turbine and Turbine Generator Set Units Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 170 |
| Dollar value | $1,108M |
| SWBS mapping | 2xx Propulsion Plant |
| Key vendors | GE Aerospace, Rolls-Royce, MTU Maintenance, Air New Zealand Engineering, TUSAS, Wartsila |

**Why it matters:** This is the LM2500/MT30 gas turbine universe -- the entire propulsion OEM supply chain. GE production contracts, Air NZ/MTU/TUSAS overhaul contracts, and Rolls-Royce MT30 sustainment all land here. Maps directly to SWBS 2xx Propulsion and the "Repair Module Market" section of the Module & Integration sheet.

### 334419 -- Other Electronic Component Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 216 |
| Dollar value | $1,381M |
| SWBS mapping | 4xx Command & Surveillance (catch-all for electronics not in 334511) |

**Why it matters:** This is the overflow bucket for combat system electronics that don't fit neatly into 334511. Includes electronic warfare components, specialized sensor elements, and electronic subsystems. Often captures Tier 2/3 electronics vendors that aren't the prime system integrator.

### 334519 -- Other Measuring and Controlling Device Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 37 |
| Dollar value | $1,402M |
| SWBS mapping | Mixed -- VLS power supply (7xx), test equipment, control systems |
| Key vendors | Laurel Technologies (VLS), various instrument manufacturers |

**Why it matters:** Disproportionate dollar value for its record count ($38M per record average). The VLS programmable power supply contract (Laurel Technologies, $70M) is here. Also captures precision measurement and control equipment used in ship system testing and calibration.

### 335999 -- All Other Miscellaneous Electrical Equipment and Component Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 80 |
| Dollar value | $302M |
| Key PSC pairing | 5998 (70 records) |
| SWBS mapping | 3xx Electric Plant, 5xx Auxiliary Systems |

**Why it matters:** Catch-all for electrical equipment that doesn't fit into transformer, motor/generator, switchgear, or wire categories. Captures ship electrical system components, specialized power equipment, and electrical auxiliaries.

### 811310 -- Commercial and Industrial Machinery and Equipment Repair and Maintenance

| Metric | Value |
|--------|-------|
| Records in FPDS data | 87 |
| Dollar value | $505M |
| Key PSC pairing | J028 (71 records) |
| SWBS mapping | 2xx Propulsion (gas turbine overhaul), 5xx Auxiliary |

**Why it matters:** This is the machinery overhaul industry -- gas turbine overhaul contractors, diesel generator repair shops, pump/valve repair facilities. Maps directly to the repair module market. The J028 PSC pairing (maintenance of engines/turbines) confirms this is propulsion system MRO. Complements 333611 (turbine manufacturing) by capturing the repair/overhaul side of the propulsion supply chain.

### 336414 -- Guided Missile and Space Vehicle Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 271 |
| Dollar value | $120,481M |
| SWBS mapping | 7xx Armament |
| Key vendors | Lockheed Martin (Trident, Standard Missile), Raytheon (Tomahawk, SM-6), Northrop Grumman |

**Why it matters:** Massive dollar value -- $120B. This captures missile system procurement and sustainment (Trident II, Tomahawk, Standard Missile SM-2/SM-6, ESSM). Most of this is weapons procurement (WPN appropriation) rather than ship MRO, but the sustainment portion maps to 7xx Armament in the MRO model. Needs careful separation: production contracts vs. depot maintenance contracts. The budget data handles this via the WPN and OMN Weapons Maintenance line items; the FPDS data needs PSC-based work type separation.

**Caveat:** Many of these contracts serve multiple services (Army Patriot, Air Force programs). Navy agency filter is essential. Even with Navy filter, some contracts are joint programs. Dollar value is dominated by a few large production contracts.

### 336419 -- Other Guided Missile and Space Vehicle Parts and Auxiliary Equipment Manufacturing

| Metric | Value |
|--------|-------|
| Records in FPDS data | 11 |
| Dollar value | $620M |
| SWBS mapping | 7xx Armament (missile components, launchers) |

**Why it matters:** Missile subcomponents and auxiliary equipment. Complements 336414.

---

## Tier 3 -- Niche Component Manufacturing (Pull If Bandwidth Allows)

Each of these captures a specific ship system component type. Low record counts individually but collectively they fill in the SWBS map at the sub-system level. These are the codes where the contracting officer classified the vendor by their primary industry rather than the end item, producing contracts that 336611 and 334511 would miss.

### Propulsion and Mechanical (SWBS 2xx, 5xx)

| NAICS | Description | Records | Dollars | Ship relevance |
|-------|-------------|---------|---------|----------------|
| 333618 | Other Engine Equipment Manufacturing | 38 | $18M | Diesel engines, auxiliary propulsion |
| 333912 | Air and Gas Compressor Manufacturing | 9 | $11M | HP air compressors, HVAC compressors |
| 333914 | Measuring, Dispensing, and Other Pumping Equipment Mfg | 1 | <$1M | Fire pumps, ballast pumps, service pumps |
| 333995 | Fluid Power Cylinder and Actuator Manufacturing | 2 | $1M | Hydraulic actuators (steering, hatches) |
| 333996 | Fluid Power Pump and Motor Manufacturing | 6 | $1M | Hydraulic pumps and motors |
| 332410 | Power Boiler and Heat Exchanger Manufacturing | 4 | $4,192M | Heat exchangers, possibly nuclear propulsion |
| 339991 | Gasket, Packing, and Sealing Device Manufacturing | 3 | <$1M | Mechanical seals, gaskets |

**Note on 332410:** The $4.2B in 4 records is anomalous -- likely nuclear propulsion heat exchangers (Bechtel, BWX Technologies). Verify before including in MRO totals.

### Electrical (SWBS 3xx)

| NAICS | Description | Records | Dollars | Ship relevance |
|-------|-------------|---------|---------|----------------|
| 335312 | Motor and Generator Manufacturing | 14 | $6M | Ship service motor generators, emergency generators |
| 335311 | Power, Distribution, and Specialty Transformer Manufacturing | 6 | $1M | Power distribution transformers |
| 335313 | Switchgear and Switchboard Apparatus Manufacturing | 1 | <$1M | Main switchboards, load centers |
| 335314 | Relay and Industrial Control Manufacturing | 2 | <$1M | Control relays, programmable controllers |
| 335910 | Battery Manufacturing | 4 | $4M | Ship batteries, UPS systems |
| 335929 | Other Communication and Energy Wire Manufacturing | 5 | <$1M | Shipboard cabling |

### Electronics and Communications (SWBS 4xx)

| NAICS | Description | Records | Dollars | Ship relevance |
|-------|-------------|---------|---------|----------------|
| 334290 | Other Communications Equipment Manufacturing | 11 | $40M | Satellite comms, data links |
| 334220 | Radio and TV Broadcasting and Wireless Communications Equip Mfg | 4 | $2M | UHF/VHF radios, Link-16, SATCOM |
| 334418 | Printed Circuit Assembly (Electronic Assembly) Manufacturing | 1 | <$1M | Specialized circuit assemblies |
| 334413 | Semiconductor and Related Device Manufacturing | 1 | <$1M | Custom semiconductors for military electronics |

### Material Handling (SWBS 5xx, 9xx)

| NAICS | Description | Records | Dollars | Ship relevance |
|-------|-------------|---------|---------|----------------|
| 333923 | Overhead Traveling Crane, Hoist, and Monorail System Mfg | 16 | $16M | Shipyard cranes, weapons handling, UNREP equipment |

### Ordnance (SWBS 7xx)

| NAICS | Description | Records | Dollars | Ship relevance |
|-------|-------------|---------|---------|----------------|
| 325920 | Explosives Manufacturing | 36 | $109M | Propellant, warheads, demolition materials |

---

## Tier 4 -- Support and Services (Context, Not Core)

These are not manufacturing codes but show up heavily in ship-related FPDS searches. They represent the services side of the market.

| NAICS | Description | Records | Dollars | Role |
|-------|-------------|---------|---------|------|
| 541715 | R&D in Physical, Engineering, and Life Sciences | 129 | -- | Applied research, tech development |
| 541712 | R&D in Physical/Engineering/Life Sciences (pre-2022 code) | 151 | -- | Same as 541715, older NAICS version |
| 561210 | Facilities Support Services | 139 | -- | Base operating support, port services |
| 488310 | Port and Harbor Operations | 100 | -- | Port services, waterfront ops |
| 541511 | Custom Computer Programming Services | 20 | -- | Software development for ship systems |
| 541614 | Process, Physical Distribution, and Logistics Consulting | 23 | -- | Logistics engineering, supply chain |
| 488390 | Other Support Activities for Water Transportation | 22 | -- | Marine support services |
| 811210 | Electronic and Precision Equipment Repair and Maintenance | 2 | <$1M | Electronics depot repair |

**Note:** 541715 and 541712 together (280 records) represent the R&D contracts that the Navy places with defense labs, FFRDCs, and research contractors. These feed the engineering base but are generally excluded from TAM unless the scope includes R&D spending.

---

## Codes NOT in Our Data -- Gaps to Investigate

These NAICS codes are structurally relevant to ship systems but returned zero records in our existing FPDS keyword searches. This could mean (a) Navy contracts under these codes don't use the ship-class keywords we searched for, (b) the volume is very small, or (c) the work is captured under broader codes. Worth running targeted USAspending queries to check.

| NAICS | Description | Why it might matter |
|-------|-------------|---------------------|
| 332991 | Ball and Roller Bearing Manufacturing | Bearings are a major MRO consumable -- shaft bearings, pump bearings, motor bearings. Could be procured via DLA rather than NAVSEA, which would explain absence from our Navy-focused searches. |
| 332993 | Ammunition (except Small Arms) Manufacturing | Naval ammunition (5-inch, 76mm, CIWS rounds). May be captured under 336414 (guided missiles) or procured through Army/DLA. |
| 332994 | Small Arms, Ordnance, and Ordnance Accessories Manufacturing | Guns, mounts, ordnance accessories. CIWS gun barrels, MK45 gun components. May be under 336414 or captured as PSC 1005/1010/1015. |
| 335921 | Fiber Optic Cable Manufacturing | Fiber optic cable is a major modernization material (ship alterations often include fiber runs). May be procured as material within depot availability contracts rather than standalone. |
| 336415 | Guided Missile and Space Vehicle Propulsion Unit Mfg | Missile propulsion. Likely captured under 336414 (parent category). |
| 336612 | Boat Building | 47 records, $75M in our data. Covers small craft (LCAC, RHIBs, workboats). Relevant for USCG and expeditionary platforms. |

---

## Recommended Pull Sequence

### Phase 1: Four core collections

These provide the broadest coverage with the least query complexity.

| Collection | NAICS | Agency filter | Expected volume | Rationale |
|------------|-------|---------------|-----------------|-----------|
| shipbuilding | 336611 | Navy subtier | 3,000-8,000 | All shipyard work -- the backbone |
| combat_electronics | 334511 | Navy subtier | 500-2,000 | All combat system electronics |
| ship_repair_psc | (use PSC J998/J999) | DoD toptier | 3,000-5,000 | Clean MRO depot -- complements 336611 by catching J998 contracts coded to other NAICS |
| combat_vessels_psc | (use PSC 1901/1904/1905) | DoD toptier | 500-1,500 | All combat vessel product contracts -- for subaward discovery |

**Note:** ship_repair_psc and combat_vessels_psc use PSC rather than NAICS because PSC structurally encodes work type (J998 = repair) and vessel type (1905 = combat ship) in ways that NAICS does not. These are in the pull script already.

### Phase 2: System-specific manufacturing

Run after Phase 1 to fill in SWBS-level detail that 336611 and 334511 miss.

| Collection | NAICS codes | Agency filter | Expected volume |
|------------|-------------|---------------|-----------------|
| propulsion_oem | 333611, 333618 | Navy subtier | 200-400 |
| weapons_systems | 336414, 336419, 325920 | Navy subtier | 300-500 |
| electronics_components | 334419, 334519, 335999 | Navy subtier | 200-400 |
| machinery_repair | 811310 | Navy subtier | 100-200 |
| engineering_svc | 541330 | Navy subtier + PSC filter (R425, R499, J099) | 1,000-3,000 |

### Phase 3: Niche collections (optional)

Run these if Phase 2 reveals coverage gaps in specific SWBS groups.

| Collection | NAICS codes | Rationale |
|------------|-------------|-----------|
| electrical_plant | 335311, 335312, 335313, 335314, 335910, 335929 | SWBS 3xx -- generators, transformers, switchgear, batteries, cabling |
| hydraulics_mechanical | 333912, 333914, 333995, 333996, 332410, 332911, 332912 | SWBS 5xx -- pumps, compressors, hydraulics, valves, heat exchangers |
| comms_equipment | 334220, 334290 | SWBS 4xx -- radios, satellite comms, data links |
| cranes_handling | 333923 | SWBS 5xx/9xx -- shipyard and shipboard material handling |
| ordnance_components | 332993, 332994 | SWBS 7xx -- gun systems, ordnance hardware |

---

## NAICS Codes Explicitly Excluded

These appear in our data but are not useful for the market sizing model.

| NAICS | Description | Why excluded |
|-------|-------------|--------------|
| 236220 | Commercial and Institutional Building Construction | Base/facility construction, not ship work. Shows up because FPDS searches for ship names sometimes match pier/facility contracts. |
| 324191 | Petroleum Lubricating Oil and Grease Manufacturing | Ship lubricants. Consumable supply, not vessel work. |
| 611310 | Colleges, Universities, and Professional Schools | Research grants to universities. Not in TAM scope. |
| 921110-928120 | Public Administration codes | Government internal operations. |

---

## Key Insight: NAICS vs PSC as Discovery Axes

NAICS and PSC provide **orthogonal** classification:
- **NAICS** answers: "What industry is the vendor in?" (shipbuilder, electronics manufacturer, engineering firm)
- **PSC** answers: "What product or service is being bought?" (combat ship, ship repair, fire control radar, engineering support)

The most effective pull strategy uses **both**:
1. NAICS for **broad discovery** -- "find all Navy contracts with turbine manufacturers" captures contracts that keyword searches would miss
2. PSC for **work type separation** -- J998 = repair (clean MRO), 1905 = vessel product work (mixed), R425 = engineering support
3. Description regex for **system classification** -- neither NAICS nor PSC tells you which combat system or SWBS group; that comes from the contract description

The current FPDS pipeline (pull_mro.py) uses description search for discovery AND classification. The USAspending re-pull shifts discovery to NAICS/PSC structured codes and keeps description regex for classification only. This is why the per-NAICS collections above do not need to be pre-classified -- classification happens downstream using the same SWBS regex already built.
