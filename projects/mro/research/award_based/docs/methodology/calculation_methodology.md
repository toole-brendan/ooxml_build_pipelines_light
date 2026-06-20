# Calculation Methodology

How the workbook classifies and aggregates federal contract award data into market-sizing
categories. All calculations reference the Awards Data table (one row per contract award,
4,892 Navy FY2025 awards from FPDS).

---

## Data Source

All figures are derived from FPDS (Federal Procurement Data System) per-modification records
for FY2025 (October 2024 - September 2025). Per-modification obligation amounts are summed
by PIID to produce FY-specific obligation per award -- not cumulative contract totals.

Four FPDS collections are merged and deduplicated at the modification level to produce the
unified award set:

- **Shipbuilding** (NAICS 336611 + Navy) -- 13,718 mods
- **Ship Repair** (PSC J998/J999 + DoD) -- 9,569 mods
- **Combat Electronics** (NAICS 334511 + Navy) -- 4,707 mods
- **Combat Vessels** (PSC 1901/1904/1905 + DoD) -- 3,031 mods

After deduplication: 19,417 unique mods -> 4,892 awards with positive FY2025 obligations.

---

## Spend Type

Each award is classified into one spend type based on its PSC (Product or Service Code):

| Spend Type | Rule | Examples |
|---|---|---|
| **newbuild** | PSC starts with 19 (vessel product codes) | 1905 Combat Ships, 1901 Aircraft Carriers, 1925 Special Service Vessels |
| **mro** | PSC is J998/J999 (ship repair) or J0xx (equipment maint) or M2xx (husbanding) | J998 Non-Nuclear Ship Repair (East), J999 (West), J019 Ships Maint |
| **system_procurement** | Product-type PSC not in 19xx | 5840 Radar, 5845 Sonar, 1230 Fire Control, 6130 Electrical Converters |
| **modernization** | PSC starts with K0 (equipment modification) or N0 (equipment installation) | K010 Weapons Mod, K058 Comm/Detection Mod, N010 Weapons Install |
| **rd** | PSC starts with AC or AD (R&D services) | AC54 Weapons Engineering Dev, AC14 Defense R&D |
| **engineering_services** | PSC starts with R4/R7 (professional support) or H/L0 (inspection/tech rep) | R425 Engineering/Technical Support |
| **other** | Remaining service codes not matching above | Construction, salvage, misc |

**Newbuild TAM** in the workbook = newbuild + system_procurement. System procurement is
included because combat system buys (radar, sonar, fire control, missiles) are part of the
newbuild market even though they are coded to system-specific PSCs rather than vessel PSCs.

**MRO TAM** in the workbook = mro + modernization. Modernization (equipment modifications
and installations on existing ships) is grouped with MRO because it represents in-service
spending on the existing fleet.

---

## Work Role (Module vs Integration)

Each award is classified as integration, module, or unclassified. This is the primary
TAM-to-SAM filter -- module work represents the addressable market for subsystem suppliers
and subcontractors.

### Integration

The contractor manages ship-level work and receives/assembles subsystems. Criteria:

1. **Vessel-level PSC codes (19xx)** -- contracts for whole ships (DDG construction,
   CVN RCOH, submarine construction) are always integration regardless of other fields.

2. **Ship repair (J998/J999) classified to SWBS Group 8** (Integration/Engineering) --
   large depot-level availabilities (DSRA, DPIA, DMP, regular overhaul) where a shipyard
   manages the full availability and subcontracts system-level work. Identified by
   description patterns: "DSRA", "growth work", "CODE 4xx", "post-shakedown availability",
   "mid-term availability", etc.

3. **Ship repair (J998/J999) over $20M without SWBS classification** -- large availabilities
   that didn't match a specific SWBS description pattern are presumed integration based on
   dollar threshold.

4. **Ship repair with GFE=Y** (government furnishes equipment to the contractor) --
   indicates the contractor is integrating government-furnished modules.

### Module

The contractor delivers a discrete subsystem, component, or system-specific service.
Criteria:

1. **System-specific PSC codes mapped to SWBS Groups 1-7** -- radar (5840), sonar (5845),
   fire control (1230), missiles (1425), propulsion components (2010), electrical converters
   (6130), etc. The PSC code identifies the system area; the SWBS mapping confirms it's a
   discrete subsystem.

2. **Equipment maintenance/modification/installation (J0xx, K0xx, N0xx)** -- these service
   codes target specific equipment types (fire control, comm/detection, electrical) rather
   than whole ships.

3. **Ship repair (J998/J999) classified to SWBS Groups 1-7** -- system-specific repair
   work identified by description (e.g., "main engine overhaul" -> propulsion, "radar
   repair" -> C&S, "hull preservation" -> hull structure).

4. **Ship repair with GFE=N under $20M** -- smaller repair contracts where the contractor
   provides the equipment/materials, suggesting component-level work.

### Unclassified

Awards that don't clearly fit either category: engineering services (R4xx), R&D (ACxx),
inspection/QC (Hxxx), technical representatives (L0xx), and small MRO contracts with
generic descriptions.

---

## SWBS Group

Each award is assigned to an SWBS (Ship Work Breakdown Structure) group where identifiable.
SWBS classifies what system area the work covers, enabling SAM calculations by capability.

| Group | Name | What it covers |
|---|---|---|
| 1 | Hull Structure | Shell plating, bulkheads, decks, foundations, structural repair |
| 2 | Propulsion Plant | Main engines, reduction gears, propellers, shafting, nuclear plant |
| 3 | Electric Plant | Generators, switchboards, power distribution, transformers, motors |
| 4 | Command & Surveillance | Radar, sonar, EW, communications, fire control, navigation |
| 5 | Auxiliary Systems | HVAC, firemain, fuel/lube oil, compressed air, steering, cranes |
| 6 | Outfit & Furnishings | Habitability, lifesaving, fire fighting, painting, insulation |
| 7 | Armament | Missiles, torpedoes, gun systems, VLS, ordnance handling |
| 8 | Integration/Engineering | Ship-level programs, total ship testing, availability management |
| 9 | Ship Assembly/Support | Ship-level maintenance services, trade labor, fire watch |

### Classification method

Two-pass approach:

1. **PSC-to-SWBS mapping** (200+ PSC prefixes mapped, checked longest-prefix-first):
   - 58xx -> Group 4 (C&S)
   - 12xx -> Group 4 (fire control is part of C&S)
   - 13xx, 14xx, 10xx -> Group 7 (armament)
   - 20xx, 28xx, 44xx -> Group 2 (propulsion)
   - 61xx -> Group 3 (electric plant)
   - 19xx -> Group 8 (ship-level integration)
   - J0xx/K0xx/N0xx suffix codes -> mapped by equipment type suffix

2. **Description regex fallback** (for J998/J999 and other generic PSCs):
   - ~50 regex patterns scan the contract description for system-specific keywords
   - "hull preservation", "drydock", "nonskid" -> Group 1
   - "main engine", "propulsor", "gas turbine" -> Group 2
   - "generator", "switchboard", "shore power" -> Group 3
   - "radar", "sonar", "aegis", "fire control" -> Group 4
   - "HVAC", "firemain", "compressed air" -> Group 5
   - "torpedo", "missile", "CIWS", "VLS" -> Group 7
   - "DSRA", "growth work", "CODE 4xx", "availability" -> Group 8

Each SWBS assignment carries a confidence level (high/medium/low) based on whether it came
from a specific PSC mapping or a broader regex match.

---

## Vessel Class

Each award is assigned to a vessel class where identifiable. Three-pass approach:

1. **PIID lookup table** -- ~80 manually researched PIIDs for the largest unclassified
   contracts, mapped to vessel class based on mod-0 descriptions, recipient context, and
   contract announcements. Highest confidence.

2. **DAP field** (DoD Acquisition Program) -- when populated with a program code (DDG 51,
   SSN 774, CVN 78, etc.), maps directly to vessel class. High confidence but only
   populated on ~175 of 4,892 awards.

3. **Description regex** -- ~20 patterns scan the description for hull designators
   (DDG-51, CVN-72), ship names (USS KIDD, USNS JOHN LEWIS), and class names (Arleigh
   Burke, Virginia-class). Medium confidence.

Awards serving multiple vessel classes (e.g., SPY-6 radar production, Aegis fire control,
sonobuoys, CIWS) are tagged "multi-class" rather than forced into a single class.

Current coverage: 85.7% of FY2025 dollars classified by vessel, 14.3% unclassified
(mostly small MRO contracts with generic descriptions).

---

## How Presentation Sheets Use These Fields

### What the sheets cover and what they don't

The total FY2025 Navy obligation across all awards is $52.6B. This breaks down by spend type:

| Spend Type | FY2025 | Awards | Appears on |
|---|---|---|---|
| newbuild | $37.2B | 229 | Newbuild sheet |
| system_procurement | $9.0B | 1,302 | Newbuild sheet |
| mro | $5.5B | 3,099 | MRO sheet |
| modernization | $314M | 62 | MRO sheet |
| rd | $289M | 40 | Neither (not in TAM) |
| engineering_services | $276M | 144 | Neither (not in TAM) |
| other | $11M | 16 | Neither (not in TAM) |

R&D, engineering services, and other ($576M total, 1.1%) are excluded from both the
Newbuild and MRO TAMs. These are support activities (studies, tech rep services, QC) that
don't represent addressable construction or maintenance spending.

### Work role coverage within each sheet

Not all awards within a spend type are classifiable as module or integration:

**Newbuild + System Procurement ($46.2B):**
- Integration: $37.2B (80.5%) -- ship-level prime contracts
- Module: $8.7B (18.9%) -- subsystem deliveries
- Unclassified: $291M (0.6%) -- engineering labor ceiling holders, generic electronic
  assemblies, aircraft components used on ships. These are real spend that doesn't fit
  cleanly into module or integration.

**MRO + Modernization ($5.8B):**
- Integration: $3.9B (67%) -- large shipyard availabilities (DSRA, DMP, etc.)
- Module: $2.0B (34%) -- system-specific repair and modification
- Unclassified: $522M (~9%) -- small MRO contracts with generic descriptions

The unclassified work_role awards are shown on each sheet but not counted toward
integration or module totals, so the integration + module subtotals do not sum to the
TAM total. This is intentional -- forcing a classification would be misleading.

### Newbuild sheet

- **TAM by vessel class**: SUMIFS on spend_type IN (newbuild, system_procurement), grouped
  by vessel_class. Includes integration + module + unclassified.
- **Integration/Module split**: further filtered by work_role. Unclassified work_role
  awards contribute to the vessel class total but not to either sub-column.
- **Module SAM by SWBS**: SUMIFS on work_role = module, grouped by swbs_group

### MRO sheet

- **TAM by vessel class**: SUMIFS on spend_type IN (mro, modernization), grouped by
  vessel_class
- **Integration/Module split**: further filtered by work_role
- **MRO by SWBS**: SUMIFS on spend_type IN (mro, modernization), grouped by swbs_group

### Cross-tabs

Any combination of dimensions is available since all four classification fields
(spend_type, work_role, swbs_group, vessel_class) are on every row of the Awards Data
table. For example:

- "DDG-51 newbuild module work in SWBS Group 4" = vessel_class = DDG-51 AND spend_type
  = newbuild AND work_role = module AND swbs_group = 4
- "MRO integration spending on carriers" = vessel_class = CVN-68/78 AND spend_type = mro
  AND work_role = integration

All presentation sheet formulas use Excel structured table references
(e.g., `Awards[FY2025 Obligation]`, `Awards[Vessel Class]`) so they update automatically
if award classifications are changed on the Awards Data sheet.
