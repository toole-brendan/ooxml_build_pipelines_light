"""_taxonomy - the finalized 3-axis classification vocabulary (shared leaf).

NON-sheet helper module (renders nothing; NOT registered in SHEETS). It is the
single source of truth for the entity-level classification schema, so the two
guide sheets that present it - ``taxonomy`` (the legend) and ``guide_methodology``
(the method) - both import the SAME constants instead of retyping them. Mirrors
the ``_taxonomy`` leaf in the DDG/submarine workbooks: a true leaf with no sheet
dependencies, so any consumer can depend on it without importing a renderer.

The schema is three independent axes, each answering exactly one question, plus a
forced catch-all per axis so every UEI x Program receives exactly one label on
every axis (MECE):

  - Capability Domain (D, published) - what technical ship area the vendor supports
  - Operating Role     (R, internal) - what value-chain responsibility it owns
  - Primary Output     (P, published) - what physically leaves the vendor

Operating Role is an internal validation layer: it BOUNDS and VALIDATES the Primary
Output assignment (see ROLE_OUTPUT_LATTICE) and is not itself a published dimension.
Output is assigned from its own physical-form evidence; Role checks it, it does not
generate it. Off-lattice Role x Output cells are review flags, not errors.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# Grain / framing
# ---------------------------------------------------------------------------

GRAIN_INTRO = (
    "Entity- and transaction-level classification legends."
)

# Axis register (name, the one question it answers, published?) - rendered by the
# methodology sheet's "three axes" table.
AXES: list[tuple[str, str, str]] = [
    ("Capability Domain (D)", "What technical ship function or enabling capability does the vendor support?", "Published"),
    ("Operating Role (R)", "What value-chain responsibility does the vendor own?", "Internal (validation only)"),
    ("Primary Output (P)", "What actually leaves the vendor (physical form / integration level)?", "Published"),
]

# ---------------------------------------------------------------------------
# Section 1 - Capability Domain archetypes (published)   (code, name, definition)
# ---------------------------------------------------------------------------

DOMAIN_INTRO = (
    "The technical / material ship area the entity is competent in, inferred "
    "from work descriptions and NAICS. A published, pure technical-area axis - "
    "no role or production-mode meaning."
)

DOMAINS: list[tuple[str, str, str]] = [
    ("D1", "Hull, Structures & Marine Fabrication",
     "Hull, superstructure, decks, structural assemblies, weldments, foundations, and structural construction of the ship and its zones."),
    ("D2", "Propulsion & Power-Transmission Machinery",
     "Prime movers and mechanical/electric drive that propel the ship or transmit propulsive power: gas turbines, diesels, propulsion motors and drives, reduction gears, shafting, propulsors, bearings."),
    ("D3", "Electrical Power - Generation, Conversion & Distribution",
     "Generates, converts, switches, protects, or distributes ship-service electrical power: generator sets, switchboards, load centers, transformers, power electronics, switchgear, motor controls."),
    ("D4", "Fluid, Pressure & Piping Systems",
     "Moves, controls, or stores fluids and gases: valves, pumps, actuators, manifolds, compressors, high-pressure air, piping and fittings, seals, filtration."),
    ("D5", "Thermal, HVAC & Life-Support",
     "Transfers heat and conditions the shipboard environment: chillers, HVAC and refrigeration, heat exchangers, condensers, ventilation, atmosphere and life-support equipment."),
    ("D6", "Mission, Combat & Communications Systems",
     "System-level sensing, communications, control, and weapon systems: sonar/acoustic arrays, radar, electronic warfare, communications, mission and fire-control systems, imaging masts, and ordnance (naval guns, missile launch systems and tubes, weapon-handling). Ordnance is kept here rather than as a separate domain - see tie-breaks."),
    ("D7", "Electronic Components, Interconnect & Cable",
     "Component-level electrical/electronic hardware that connects and carries power or signal: hull penetrators, connectors, feedthroughs, cable and wire harnesses, circuit cards, and instrumentation components."),
    ("D8", "Mechanical Handling & Deck Machinery",
     "Shipboard handling and access machinery: davits, cranes, hoists, winches, capstans, elevators, boat- and weapons-handling gear, and specialty/hangar/access doors. Bounded to handling and access mechanisms - general fluid, thermal, or electrical machinery resolves to D4 / D5 / D3 by function, not here."),
    ("D9", "Specialty Materials & Precision Processes",
     "A material- or process-defined competence whose specific ship application is NOT determinable from the industry code: forging, casting, machining, rolled rings, composites, elastomers, acoustic/signature treatments, isolation mounts. This is a process/material axis, not a ship-system area - the same forging or composite feeds many systems. Assign a functional domain (D1-D8) whenever the ship application IS known; D9 is the application-agnostic fallback for material/process specialists."),
    ("D10", "Interiors, Habitability & Outfitting",
     "Shipboard interiors and habitability outfit: furniture and joinery, galley and berthing outfit, insulation and deck covering, and habitability / safety / egress gear. Bounded to interior and habitability outfitting - NOT a residual for otherwise-unclassified manufactured goods (those resolve by function or to D0)."),
    ("D11", "Services & Non-Material Support",
     "The entity's competence is non-material support rather than a ship technical/material area: engineering / test / R&D services, installation and field service, repair and overhaul, logistics and transportation, software and IT, training and workforce development, or facilities and construction. The domain-axis counterpart of Primary Output P6 - use when the deliverable is labor or an intangible, not a ship article. Pure material distributors are NOT here: they take the domain of the material they handle, or D0 if indeterminate (distribution is a role, not a service)."),
    ("D0", "Unresolved / Insufficient Evidence",
     "No single technical domain is defensible (a genuinely multi-domain firm with no primary, or insufficient evidence); still gives every UEI x Program exactly one domain label."),
]

# Domain boundary tie-breaks (situation, rule) - rendered as a sub-table.
DOMAIN_TIEBREAKS: list[tuple[str, str]] = [
    ("D2 vs D3 (turbine-generators)",
     "Ship-service power generation -> D3; main propulsion drive -> D2."),
    ("D6 vs D7 vs D3 (electronics)",
     "System-level sensing/combat/comms -> D6; component-level interconnect, cable, penetrators -> D7; ship-service power components -> D3. Classify by function and integration level."),
    ("D9 vs a system domain",
     "Classify by the vendor's differentiating competence: the material/process itself -> D9; a complete functional system -> the system domain (a sonar-array maker -> D6; a composite-acoustic-parts maker -> D9)."),
    ("D1 vs D4 (pressure boundaries)",
     "Structural / pressure-vessel fabrication -> D1; functional fluid/pressure equipment (valves, pumps) -> D4."),
    ("D2 vs D3 (electric drive & power)",
     "A firm whose output spans propulsion motors/drives (D2) and power generation, conversion, or distribution (D3) - e.g. an integrated electric-plant or motor-and-generator supplier (NAICS 335312) - is assigned by its dollar-dominant ship function, NEVER D0: propulsion-motor / electric-drive dominant -> D2; ship-service power dominant -> D3."),
    ("Ordnance",
     "Naval guns, missile launch systems and tubes, and weapon-handling stay in D6; there is no separate ordnance domain - under the hull-builder scope the dedicated weapons GFE primes are out of scope, so standalone ordnance content is sparse."),
    ("Service firms",
     "A service firm whose specialty maps unambiguously to one technical area keeps that area (a propulsion test house -> D2); a firm whose deliverable is general non-material support with no single technical area -> D11 Services (no longer D0)."),
    ("Pure distributors",
     "Assign the domain of the material handled and let Role R1 carry the pass-through signal; D0 only when even that is indeterminate."),
]

# ---------------------------------------------------------------------------
# Section 2 - Operating Role archetypes (internal)   (code, name, definition, validates)
# ---------------------------------------------------------------------------

ROLE_INTRO = (
    "The value-chain responsibility the entity owns - design authority and "
    "integration level. An internal validation layer, not published."
)

ROLES: list[tuple[str, str, str]] = [
    ("R1", "Build-to-Spec Manufacturer / Processor / Distributor",
     "Executes another party's drawings and specifications, or processes/resells others' material; supplies capacity, tradecraft, or material rather than an owned product design."),
    ("R2", "Product / Equipment OEM",
     "Owns the qualified design and configuration of its own finished equipment or product family."),
    ("R3", "Subsystem / Shipset Integrator",
     "Owns system-level integration and interface responsibility for a multi-item functional subsystem or shipset."),
    ("R4", "Module / Distributed Shipbuilder",
     "Performs shipyard-like structural construction and outfitting; delivers major ship modules or zone units."),
    ("R5", "Production, Test & Lifecycle Service Provider",
     "Delivers engineering, test/qualification, installation, repair, overhaul, or industrial labor; no new physical article."),
    ("R0", "Unresolved / Non-operating Attribution",
     "A holding, private-equity, or parent entity with no direct production, or insufficient evidence to assign an operating role."),
]

# ---------------------------------------------------------------------------
# Section 3 - Primary Output archetypes (published)   (code, name, definition)
# ---------------------------------------------------------------------------

OUTPUT_INTRO = (
    "The physical form and integration level of the entity's primary delivered "
    "article - a deliverable-maturity ladder (P1 lowest to P5 highest, P6 for "
    "labor-led handoffs). A published axis."
)

OUTPUTS: list[tuple[str, str, str]] = [
    ("P1", "Materials, Stock & Bulk Inputs",
     "Material not yet a finished ship item: requires substantial downstream machining, fabrication, or qualification (plate, bar, structural shapes, near-net forgings, rough castings, blanks, rolled rings), or is consumed in process (coatings, sealants, resins, welding consumables, gases, lubricants)."),
    ("P2", "Finished Parts & Fabricated Components",
     "Dimensionally complete or fit-ready parts and fabrications that install into a larger item and do not independently perform the principal shipboard function: machined parts, fittings, bearings, seals, mounts, gaskets, composite panels, weldments, pipe spools, foundations, harnesses."),
    ("P3", "Functional Equipment & Machinery",
     "A bounded, acceptance-testable unit that performs a defined function once connected or installed: engines, generator sets, reduction gears, pumps, valves, compressors, HVAC plants, switchboards, transformers, actuators, davits."),
    ("P4", "Integrated Systems & Configured Shipsets",
     "Multiple interdependent hardware, software, control, or sensor elements delivered as one configured solution with system-level integration or interface responsibility: sonar shipsets, integrated communications, electric-propulsion packages, fire-control, naval gun systems."),
    ("P5", "Outfitted Structures & Ship Modules",
     "A major structural section or spatially organized module assembled from multiple parts and trades, transferred as a defined shipbuilding unit: hull/superstructure units, outfitted modules, deck modules, completed submarine decks."),
    ("P6", "Services & Technical Work Products",
     "A labor-led or primarily intangible handoff used to construct, qualify, or support the vessel: engineering packages, test and qualification, calibration, installation, repair, production support, shipyard labor, standalone software or technical data."),
    ("P0", "Unresolved / Attribution-Only",
     "No defensible operating output can be assigned, or the record reflects a parent, investor, or holding-company attribution rather than an operating supplier."),
]

# Primary Output boundary tests (pair, test) - the MECE boundaries.
OUTPUT_BOUNDARIES: list[tuple[str, str]] = [
    ("P1 vs P2",
     "Substantial manufacturing remains after delivery (P1) vs. dimensionally complete / fit-ready (P2). A rough shaft forging is P1; a fully machined propulsion shaft is P2."),
    ("P2 vs P3",
     "Performs its function only after being built into another device (P2) vs. can be individually specified, acceptance-tested, and connected as a functional unit (P3). A gasket, bearing, or flange is P2; a valve, pump, or switchboard is P3."),
    ("P3 vs P4",
     "Requires ACTUAL functional integration, not mere co-delivery. 100 independent valves shipped together stay P3; a propulsion package with motor, drives, switchgear, controls and configured interfaces is P4. 'Shipset' alone does not trigger P4."),
    ("P4 vs P5",
     "Organized around a shipboard FUNCTION (P4) vs. a physical ship ZONE or structure (P5). A sonar array or electric-drive package is P4; an outfitted command-and-control deck module is P5, even though it contains functional equipment."),
    ("Hardware vs P6",
     "When hardware and services are bundled, classify the hardware output unless labor or technical work is clearly the principal contractual handoff. An OEM supplying an HVAC plant plus install support is P3; a firm engaged principally for test, repair, or industrial labor is P6."),
]

# ---------------------------------------------------------------------------
# Assignment rule + Role x Output validation lattice
# ---------------------------------------------------------------------------

ASSIGNMENT_RULE = (
    "For each UEI x Program, classify the most representative recurring "
    "program-specific output sold or transferred across the vendor's contractual "
    "boundary - not the most sophisticated item in the firm's general portfolio. "
    "Where several items are supplied, choose the highest integration level only "
    "when those items are actually delivered as one configured product or system."
)

# (role code, role short name, expected output) - the QA expectation; off-lattice
# combinations are legitimate review flags, not errors.
ROLE_OUTPUT_LATTICE: list[tuple[str, str, str]] = [
    ("R1", "Build-to-Spec Mfr / Processor / Distributor", "P1 / P2"),
    ("R2", "Product / Equipment OEM", "P2 / P3"),
    ("R3", "Subsystem / Shipset Integrator", "P4"),
    ("R4", "Module / Distributed Shipbuilder", "P5"),
    ("R5", "Production / Test / Lifecycle Service", "P6"),
    ("R0", "Unresolved / Non-operating", "P0"),
]

LATTICE_NOTE = (
    "The overlaps make this a QA check, not a 1:1 derivation: an output outside its "
    "role's expected set is a review flag, not an error. A build-to-print fabricator "
    "delivering a complete functional unit (R1 x P3) is a legitimate off-diagonal - "
    "it just means 'verify the vendor does not actually own the design (-> R2).'"
)

# ---------------------------------------------------------------------------
# Section 5 - Ship-System Application (SWBS) - transaction-level, HII-DDG only
# ---------------------------------------------------------------------------
#
# A different-grain COMPANION dimension, not a fourth entity archetype: it is
# carried on the subaward TRANSACTION (one HII-DDG subaward -> one ship-system
# application), where D / R / P are entity-level (UEI x Program). A UEI keeps one
# Capability Domain / Role / Output while its transactions hit many SWBS groups.

SWBS_INTRO = (
    "Which shipboard system a subaward supports, read from the observed SWBS code. "
    "Transaction-level and HII-DDG only - submarine subawards carry no SWBS "
    "equivalent, and SWBS is never compared across programs."
)

# (code, ship-system application, example subsystems / drill-down)
SWBS_GROUPS: list[tuple[str, str, str]] = [
    ("100", "Hull Structure",
     "Structural units, hull accesses, foundations, structural closures."),
    ("200", "Propulsion Plant",
     "234 propulsion gas turbines; 241 reduction gears; 244 shaft bearings; 245 propulsors; 262 lube oil."),
    ("300", "Electric Plant",
     "310 power generation; 314 power conversion; 324 switchgear and panels."),
    ("400", "Command, Control & Surveillance",
     "431 interior-comms switchboards; 433 announcing; 436 alarm/safety/warning; 451 radar; 475 degaussing."),
    ("500", "Auxiliary Systems",
     "Pumps, piping, ventilation, refrigeration, cooling water, compressed air, fire extinguishing, steering, deck handling."),
    ("600", "Outfit & Furnishings",
     "624 non-structural closures; 633 cathodic protection."),
    ("700", "Armament",
     "712 ammunition handling and other weapons-related system elements."),
    ("800", "Integration / Engineering",
     "Design integration, engineering, logistics, system-integration work. Program/contract decomposition, not an installed ship system."),
    ("900", "Ship Assembly & Support Services",
     "Ship assembly, production support, testing, trials, shipbuilder-support. Program/support activity, not an installed ship system."),
    ("X00", "Cross-Cutting Design & Construction Requirements",
     "Requirements applied across systems rather than installed as one - e.g. 730 -> 7300 Noise & Vibration. Bounded by an explicit code list, not 'anything that spans systems'."),
    ("L00", "Legacy / Unmapped SWBS Reference",
     "A plausible SWBS or product-structure reference that does not resolve against the current codebook (e.g. 351, pending validation)."),
    ("U00", "No SWBS Evidence",
     "No defensible ship-system application can be extracted or inferred."),
]

SWBS_HIERARCHY_NOTE = (
    "Hierarchy: SWBS major group -> 3-digit SWBS subsystem -> HII work-item code -> "
    "component text. The HII work-item code stays a drill-down and audit key, not the "
    "headline: it is finer than SWBS but proprietary to HII, so it is weaker for "
    "cross-prime / cross-program comparison."
)

# Mapping provenance (code, method) - rendered on the Methodology tab (§9a).
SWBS_MAPPING_METHOD: list[tuple[str, str]] = [
    ("E", "Explicit three-digit SWBS in the transaction description."),
    ("X", "Deterministic crosswalk from HII work-item code to an explicitly observed SWBS."),
    ("C", "Curated inference from HII code, component text, vendor evidence, and codebook."),
    ("L", "Legacy / codebook-version mismatch."),
    ("U", "Unresolved / no SWBS evidence."),
]

# Standing rules for the SWBS dimension - rendered on the Methodology tab (§9b).
SWBS_GUARDRAILS: list[str] = [
    "Grain is the subaward transaction, not the entity: a UEI's transactions can hit many SWBS groups, so SWBS is never collapsed to one-per-UEI.",
    "SWBS validates entity tags, it does not overwrite them: transaction evidence (HII code + component text, not the SWBS number itself) can flag a Capability Domain or Primary Output to revisit, but the published call stays the entity-level one.",
    "Present every cut as 'within mapped SWBS records' and show mapped-dollar coverage beside each FY / hull / PIID comparison; never treat unmapped records as zero system activity.",
    "Concentration measures (top-3 share, HHI) are within mapped dollars only - the uncoded long tail may hide alternate sources, so read them as an upper bound.",
    "The observed HII -> SWBS crosswalk is locked as observed-in-this-pull (no one-to-many conflicts in the current data is a sample property); version it and re-validate on new pulls.",
    "Subaward amount is an award/report amount, not a unit price; negative-amount records are treated as adjustments, not procurement.",
    "Three lookup exceptions are handled explicitly, not forced to the nearest headline: 436 via prefix-family (4361x); 730 -> 7300 Noise & Vibration (cross-cutting X00, not Armament); 351 kept Legacy until validated.",
]
