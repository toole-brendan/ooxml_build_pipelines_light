# Methodology

End-to-end methodology for sizing the U.S. Navy newbuild and MRO market from federal
contract award data.

---

## 1. Why Awards Data

The previous version of this model (v1.x) combined top-down budget exhibits from Navy
justification books with bottom-up FPDS contract data from keyword searches. That approach
had structural problems:

- **Incommensurable units.** Budget authority is annual and per fiscal year. FPDS
  obligations are cumulative over the contract lifetime. The two can only be compared as
  percentage shares, not dollar values, which makes reconciliation fragile and misleading.

- **Granularity mismatch.** Budget data classifies at the vessel type level (e.g.,
  "Surface Combatants") while contract data classifies at the hull class level (e.g.,
  DDG-51). No budget-side per-class split exists, so the top-down and bottom-up views
  can't be joined at the same resolution.

- **Keyword search gaps.** FPDS keyword searches required 187 queries across 11 vessel
  classes and still left 25% of contracts unclassifiable because contract descriptions are
  inconsistent.

The awards-only approach solves these problems. USAspending and FPDS structured fields
(NAICS, PSC, DoD Acquisition Program) return the full universe of relevant contracts in
a few broad queries. Per-modification obligation data from FPDS gives true FY-specific
spending without the cumulative/period ambiguity. Budget data may be reintroduced later
as a validation layer, but it is not needed for the core model.

---

## 2. Data Gathering

### Source

FPDS Atom Feed -- the federal government's per-modification contract record system. Each
record represents one contract action (award, modification, exercise of option) with a
signed date, obligation amount, and ~60 structured fields.

FPDS was chosen over USAspending as the primary source because:
- Per-modification records carry per-mod obligation amounts and signed dates, enabling
  direct FY decomposition without a separate transaction enrichment step
- FPDS has fields not available in USAspending: GFE/GFP (government-furnished equipment),
  ultimate parent company, CAGE codes, UCA (undefinitized contract action) status
- Single paginated query replaces the three-step USAspending pipeline (award search +
  transaction pull + FPDS enrichment) that took ~45 min per collection per FY

USAspending is used as an optional enrichment layer for subaward counts, PSC hierarchy,
and business categories not available in FPDS.

### Discovery filters

Contracts are discovered by NAICS code and PSC code -- not keyword search. This captures
the full universe of relevant contracts without relying on description text.

Four collections cover the core market:

| Collection | Filter | What it captures |
|---|---|---|
| Shipbuilding | NAICS 336611 + Navy | All shipyard work -- newbuild, repair, planning yard |
| Combat Electronics | NAICS 334511 + Navy | Radar, sonar, EW, fire control, navigation |
| Ship Repair | PSC J998/J999 + DoD | Ship repair services coded to non-shipbuilding NAICS |
| Combat Vessels | PSC 1901/1904/1905 + DoD | Combat vessel product contracts |

These overlap by design (a DDG construction contract coded NAICS 336611 + PSC 1905 appears
in both Shipbuilding and Combat Vessels). Deduplication happens downstream.

### FY decomposition

FPDS per-modification records carry a signed date and per-mod obligation amount. The pull
script filters by signed date range (e.g., 2024-10-01 to 2025-09-30 for FY2025) to get
only modifications signed in the target fiscal year. The per-mod obligation amounts are
then summed by PIID to get the FY-specific obligation per contract -- the actual amount
the Navy obligated on that contract in that fiscal year.

This is different from the cumulative "total obligation" field, which reflects lifetime
spending across all fiscal years. FY-specific obligation is the correct measure for annual
market sizing.

### Deduplication

The four collections are merged at the modification level. A modification is identified by
the tuple (PIID, mod_number, date_signed). When the same modification appears in multiple
collections (because the contract matches multiple discovery filters), duplicates are
removed, keeping the record with the most populated fields.

After deduplication, modifications are re-aggregated into per-award records. Each award
carries the latest modification's metadata (recipient, PSC, description, etc.) and
the summed FY obligation from all its deduplicated modifications.

Result for FY2025: 31,025 raw modifications -> 19,417 unique modifications -> 4,892
awards with positive FY2025 obligations totaling $52.6B.

---

## 3. Classification

Each award is tagged along four dimensions. The dimensions were chosen because they answer
the questions that matter for market sizing:

| Dimension | Question it answers | Why it matters |
|---|---|---|
| **Spend type** | Is this new construction, repair, or something else? | Separates the newbuild market from the MRO market |
| **Work role** | Is this ship-level integration or a discrete module? | Defines the SAM -- module work is the addressable market for subsystem suppliers |
| **SWBS group** | What ship system area does this work cover? | Sizes specific capability markets (radar, propulsion, hull, etc.) within the SAM |
| **Vessel class** | Which ship program is this for? | Enables per-program market views and tracks where investment is concentrated |

### Spend type

Determined from the PSC (Product or Service Code), which is a federal classification of
what was purchased:

- **Newbuild**: PSC 19xx (vessel products) -- new ship construction
- **System procurement**: any other product-type PSC (58xx radar, 12xx fire control, etc.)
  -- subsystem purchases that are part of the newbuild or fleet modernization pipeline
- **MRO**: PSC J998/J999 (ship repair), J0xx (equipment maintenance), M2xx (husbanding)
- **Modernization**: PSC K0xx (equipment modification), N0xx (equipment installation)
- **R&D**: PSC ACxx/ADxx (research and development services)
- **Engineering services**: PSC R4xx/R7xx (professional/technical support), Hxxx/L0xx
  (inspection, QC, tech rep)

PSC is used rather than description text because it is a structured, standardized field
assigned at contract award. Description text is used for finer-grained classification
within spend types (e.g., which SWBS group a ship repair contract falls in).

### Work role (module vs integration)

This is the TAM-to-SAM filter. The logic uses multiple signals because no single field
is definitive:

**Integration signals:**
- PSC 19xx (vessel-level product) -- you're buying a whole ship
- SWBS Group 8 from description (availability management, ship testing) -- ship-level work
- Ship repair over $20M without specific system description -- large depot availabilities
- GFE=Y on ship repair -- contractor receives government-furnished modules to integrate

**Module signals:**
- System-specific PSC mapped to SWBS Groups 1-7 -- you're buying a radar, engine, etc.
- Equipment maintenance/modification/installation PSCs (J0xx, K0xx, N0xx) -- work on
  specific equipment, not whole ships
- Ship repair with system-specific description -- "main engine overhaul", "radar repair"
- GFE=N on smaller ship repair -- contractor provides the parts, suggesting component work

**Why GFE matters:** Government Furnished Equipment (GFE=Y) means the government provides
equipment to the contractor for integration. On a shipyard contract, GFE=Y means the
shipyard is receiving radar arrays, propulsion modules, etc. from module suppliers and
integrating them into the ship. This is a strong signal that the contract is integration
work. Conversely, GFE=N on a system-specific PSC means the contractor is delivering a
complete module -- they are the module supplier.

### SWBS group

SWBS (Ship Work Breakdown Structure) is the Navy's standard system for classifying ship
systems into functional groups. It maps the "what" of each contract to a system area:

| Group | Name | Example contracts |
|---|---|---|
| 1 | Hull Structure | Structural steel, deck repair, drydocking, hull preservation |
| 2 | Propulsion Plant | Main engines, reduction gears, propellers, nuclear reactor plant |
| 3 | Electric Plant | Generators, power distribution, switchboards, transformers |
| 4 | Command & Surveillance | Radar, sonar, EW, fire control, communications, navigation |
| 5 | Auxiliary Systems | HVAC, firemain, hydraulics, steering, compressed air, cranes |
| 6 | Outfit & Furnishings | Habitability, lifesaving, insulation, painting |
| 7 | Armament | Missiles, torpedoes, gun systems, VLS, ordnance handling |
| 8 | Integration/Engineering | Ship-level design, testing, availability management |
| 9 | Ship Assembly/Support | Trade labor, fire watch, scaffolding, ship-level services |

Classification uses a two-pass approach:

1. **PSC-to-SWBS mapping** (200+ prefix rules). PSC codes are federal product/service
   classifications that map well to SWBS groups. For example, PSC 5840 (Radar Equipment)
   maps to SWBS Group 4 (C&S) with high confidence. This handles ~70% of awards.

2. **Description regex** (~50 patterns). For generic PSCs like J998/J999 (ship repair),
   the contract description is scanned for system-specific keywords. "Main engine overhaul"
   maps to Group 2; "hull preservation" maps to Group 1; "DSRA" maps to Group 8. This
   handles another ~20% of awards.

The remaining ~10% of awards have generic descriptions ("SHIP REPAIR", "FUNDING MOD") that
don't match any pattern. These are left unclassified rather than forced into a group.

**Why SWBS matters for SAM:** Without SWBS, the model can say "there is $10.7B in module
work." With SWBS, it can say "there is $7.8B in C&S modules, $1.3B in armament modules,
$386M in propulsion modules." A company maps its capabilities to specific SWBS groups to
calculate the market it can actually address.

### Vessel class

Determined by a three-pass approach, prioritized by confidence:

1. **PIID lookup table** (~80 manually researched contracts). The largest unclassified
   contracts were identified by PIID and matched to vessel class using mod-0 descriptions,
   recipient context, and public contract announcements. This recovers ~$15B in vessel
   classification on contracts whose latest modification has a generic description like
   "FUNDING" or "INC FUNDING" that obscures the program identity.

2. **DoD Acquisition Program field.** When FPDS populates this field with a program code
   (DDG 51, SSN 774, CVN 78), it maps directly to a vessel class. High confidence but only
   populated on ~4% of awards.

3. **Description regex** (~20 patterns). Hull designators (DDG-51, CVN-72), ship names
   (USS KIDD, USNS JOHN LEWIS), and class names (Arleigh Burke, Virginia-class) are
   extracted from contract descriptions.

Contracts that serve multiple vessel classes (SPY-6 radar, Aegis fire control, sonobuoys,
CIWS) are tagged "multi-class" rather than attributed to a single program.

Current coverage: 85.7% of FY2025 dollars classified by vessel class.

---

## 4. Output

The classified award data feeds an Excel workbook with formula-driven presentation sheets.

### Awards Data sheet

The foundation. One row per award (4,892 rows), 32 columns including all four classification
fields. Formatted as an Excel Table named "Awards" so presentation sheets can reference it
with structured formulas like `SUMIFS(Awards[FY2025 Obligation], Awards[Vessel Class], "DDG-51 Arleigh Burke")`.

### Output sheet (waterfall)

Shows where all $52.6B lands:
- Spend type breakdown (newbuild, system procurement, MRO, modernization, R&D, engineering
  services, other)
- TAM groupings (Newbuild TAM = $46.2B, MRO TAM = $5.8B, excluded = $576M)
- Work role split (integration $41.1B, module $10.7B, unclassified $813M)
- Module SAM by SWBS group

### Newbuild sheet

- TAM by vessel class with integration/module split
- Module SAM by SWBS group (which subsystem markets exist within newbuild)

### MRO sheet

- TAM by vessel class with integration/module split
- MRO by SWBS group (which system areas drive maintenance spending)

### All formulas reference Awards Data

Every number on the presentation sheets is a SUMIFS or COUNTIFS formula pointing at the
Awards table. If a classification is changed on the Awards Data sheet (e.g., reclassifying
an award from "unclassified" to "module"), all presentation sheets update automatically.
No hardcoded values.

---

## 5. Known Limitations

1. **Single fiscal year.** The model currently covers FY2025 only. FY2022-2024 data can be
   pulled with the same scripts to show market trends. FY2026 is a partial year.

2. **Navy only.** Coast Guard data has been pulled but not yet deduplicated, classified, or
   included in the workbook.

3. **No subcontract SAM.** The current SAM (module work_role) captures direct module
   procurement. It does not capture work subcontracted by integration primes to module
   suppliers. This is a significant gap -- major shipbuilding programs subcontract 40-60%
   of contract value. Closing this gap requires subaward data from USAspending.

4. **Description-dependent classification.** ~30% of SWBS and vessel class assignments
   depend on contract description text, which varies in quality. Some contracts have
   descriptions like "FUNDING" or "CODE 440A" that carry no system or vessel information.
   The PIID lookup table addresses the highest-value cases but thousands of smaller
   contracts remain unclassifiable.

5. **FY obligation vs actual spend.** FPDS obligation amounts reflect what the government
   committed to pay, not what was actually disbursed. Deobligations (negative modifications)
   are excluded from the positive-obligation set, but the remaining obligations may include
   amounts that are later deobligated in future fiscal years.

6. **Latest-mod metadata.** Award-level metadata (recipient, PSC, description) is taken
   from the latest modification. If a contract changes contractors or scope over its
   lifetime, the latest mod's metadata may not reflect the full history. The PIID lookup
   table and raw mod scanning partially address this.
