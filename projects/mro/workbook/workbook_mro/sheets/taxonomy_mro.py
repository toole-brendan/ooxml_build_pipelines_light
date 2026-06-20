"""taxonomy_mro - the load-bearing MRO SAM vocabularies + atom classifiers.

A non-sheet helper (no SheetEntry), modelled on _crosstab.py: pure constants and
small pure functions that the SAM engine (data_tam_atoms / inputs_scenarios /
model_sam_build) and the deck chartdata share. These vocabularies used to live
scattered inside chartdata_output.py (RMC buckets, contractor tiers, IDV scopes,
marauder hulls, prime lists) and model_depot_ship_repair.py; consolidating them
here stops chartdata from being the hidden model brain and gives the atom layer a
single source of truth for every tag value.

The SAM model:
  * One headline TAM (Reconciled FPDS-visible MRO TAM).
  * SAM = scenario-selected subsets of mutually-exclusive TAM atoms. Each atom
    carries one bucket per AXIS; a scenario includes atoms whose <axis> tag is
    flagged 1 in the Scenarios matrix. Within an axis = OR; across axes = AND.
  * Scenario outputs are a MENU - never summed (overlapping options exceed TAM).

The seven AXES (every atom has exactly one bucket on each, so the AND-product
never silently drops a constraint):
  work_segment, hull, buyer_rmc, contractor_tier, idv_scope, scope_class, service

Depot-only axes (buyer_rmc / contractor_tier / idv_scope) carry the sentinel
"n/a" on non-depot atoms and "unmapped" on depot atoms with no J998J999 tag match
(so the enrichment delta is disclosed, not silently dropped).
"""
from __future__ import annotations

from workbook_mro.sheets._crosstab import WORK_SEGMENTS as _SVC_SEGMENTS, PSC_CODES

# ── Work segments ──────────────────────────────────────────────────────────
# The five services work segments (PSC partition, from _crosstab) + the embedded
# PSC 1905 segment. Embedded atoms tag work_segment = EMBEDDED_SEGMENT.
EMBEDDED_SEGMENT = "PSC 1905 Embedded MRO"
DEPOT_SEGMENT = "Depot Ship Repair"
WORK_SEGMENTS = list(_SVC_SEGMENTS) + [(EMBEDDED_SEGMENT, [])]
WORK_SEGMENT_LABELS = [name for name, _codes in WORK_SEGMENTS]
_PSC_TO_SEG = {psc: name for name, codes in _SVC_SEGMENTS for psc in codes}
DEPOT_PSCS = ("J998", "J999")


def work_segment_for_psc(psc: str) -> str:
    """Map a services PSC to its work segment (the 65-PSC partition is total)."""
    seg = _PSC_TO_SEG.get((psc or "").strip())
    if seg is None:
        raise KeyError(f"PSC {psc!r} not in the 65-PSC work-segment partition")
    return seg


# ── Sentinels for the depot-only axes on non-depot / un-enriched atoms ──────
NA = "n/a"               # axis does not apply (non-depot atom)
UNMAPPED = "unmapped"    # depot atom with no J998J999 PIID match (delta disclosed)
UNCLASSIFIED = "Unclassified"

# ── Buyer / RMC buckets (raw J998J999 RMC -> grouped bucket) ────────────────
RMC_BUCKET = {
    "SWRMC": "SWRMC", "MARMC": "MARMC", "SERMC": "SERMC",
    "NW RMC / Puget Sound": "NW RMC",
    "SRF-JRMC Yokosuka": "FDNF", "FDRMC Naples": "FDNF", "FLC Bahrain": "FDNF",
    "USCG SFLC": "USCG SFLC",
}
RMC_BUCKET_LABELS = ["SWRMC", "MARMC", "SERMC", "NW RMC", "FDNF", "USCG SFLC", "Other"]


def rmc_bucket(raw: str) -> str:
    """Group a raw J998J999 RMC into its bucket; unknowns fall to 'Other'."""
    return RMC_BUCKET.get((raw or "").strip(), "Other")


# ── Contractor tiers (raw J998J999 Contractor Tier, used verbatim) ──────────
CONTRACTOR_TIERS = [
    "Tier 1 - CONUS Complex Repair Prime",
    "Tier 2 - Regional Repair",
    "Tier 3 - Technical Services",
    "Tier 4 - FDNF Foreign Yard",
    "Other",
]
TIER_REGIONAL = "Tier 2 - Regional Repair"
TIER_TECH = "Tier 3 - Technical Services"

# ── IDV scope groups (raw J998J999 IDV Scope Group; "" -> Unclassified) ─────
IDV_SCOPE_GROUPS = [
    "Full-Ship Availability", "MSC Availability", "FDNF Foreign MSRA",
    "Planning & Engineering Support", "Other / Support Services", "Trade IDIQ",
    "USCG Cutter", UNCLASSIFIED,
]
IDV_MSC = "MSC Availability"

# ── Scope class (addressability flag, NOT a second TAM) ─────────────────────
SCOPE_ADDRESSABLE = "Addressable"
SCOPE_CAPTIVE = "Captive"
SCOPE_FMS = "FMS"
SCOPE_CLASSES = [SCOPE_ADDRESSABLE, SCOPE_CAPTIVE, SCOPE_FMS]
# Captive SUPSHIP complex-OH parents (matched as uppercased-substring against an
# embedded atom's ultimate parent); the single source of truth for the captive set.
CAPTIVE_PARENT_MARKERS = ("HUNTINGTON", "ELECTRIC BOAT", "GENERAL DYNAMICS", "FLUOR")
FMS_AVAILABILITY_GROUP = "Out of Scope (FMS)"


def scope_class_for(*, source_universe: str, ultimate_parent: str,
                    availability_group: str) -> str:
    """Addressable / Captive / FMS for one atom.

    Captive = embedded PSC 1905 MRO at a captive SUPSHIP parent (HII/GD/EB/Fluor);
    FMS = depot work booked under the Out-of-Scope (FMS) availability group; else
    Addressable. This is the single place the captive/FMS contestability exclusions
    live - SAM Build's 'Broad Addressable' rung is SUMPRODUCT over scope_class.
    """
    up = (ultimate_parent or "").upper()
    if source_universe == EMBEDDED_SEGMENT and any(m in up for m in CAPTIVE_PARENT_MARKERS):
        return SCOPE_CAPTIVE
    if (availability_group or "").strip() == FMS_AVAILABILITY_GROUP:
        return SCOPE_FMS
    return SCOPE_ADDRESSABLE


# ── Services (raw Awards Service) ───────────────────────────────────────────
SERVICES = ["Navy", "Coast Guard"]

# ── Hull groups (coarse, for display + the §5 hull drilldown) ───────────────
HULL_GROUP = {
    "DDG": "Surface Combatants", "CG": "Surface Combatants", "FFG": "Surface Combatants",
    "LCS": "Surface Combatants",
    "CVN": "Aircraft Carriers",
    "SSN": "Submarines", "SSBN": "Submarines",
    "LPD": "Amphibious & Expeditionary", "LSD": "Amphibious & Expeditionary",
    "LHA": "Amphibious & Expeditionary", "LHD": "Amphibious & Expeditionary",
    "LCC": "Amphibious & Expeditionary", "ESB": "Amphibious & Expeditionary",
    "T-ESB": "Amphibious & Expeditionary",
    "T-AO": "Combat Logistics & Auxiliary", "T-AKE": "Combat Logistics & Auxiliary",
    "T-AOE": "Combat Logistics & Auxiliary", "T-AH": "Combat Logistics & Auxiliary",
    "AS": "Combat Logistics & Auxiliary", "T-AKR": "Combat Logistics & Auxiliary",
    "T-EPF": "Combat Logistics & Auxiliary", "T-ARC": "Combat Logistics & Auxiliary",
    "T-ATF": "Combat Logistics & Auxiliary", "T-ARS": "Combat Logistics & Auxiliary",
    "T-ATS": "Combat Logistics & Auxiliary", "T-AGOS": "Combat Logistics & Auxiliary",
    "T-AGS": "Combat Logistics & Auxiliary",
    "WMSL": "Cutters & Boats", "NSC": "Cutters & Boats", "WMEC": "Cutters & Boats",
    "WPC": "Cutters & Boats", "FRC": "Cutters & Boats", "WLB": "Cutters & Boats",
    "WAGB": "Cutters & Boats", "OPC": "Cutters & Boats", "WIX": "Cutters & Boats",
    "WLIC": "Cutters & Boats",
}


def hull_program(raw: str) -> str:
    """Normalise a hull-program tag ('' -> Unclassified)."""
    return (raw or "").strip() or UNCLASSIFIED


HULL_GROUP_LABELS = [
    "Surface Combatants", "Aircraft Carriers", "Submarines",
    "Amphibious & Expeditionary", "Combat Logistics & Auxiliary",
    "Cutters & Boats", "Other / Unclassified",
]


def hull_group(raw: str) -> str:
    """Coarse hull group for display / drilldown; unknowns fall to a residual."""
    return HULL_GROUP.get((raw or "").strip(), "Other / Unclassified")


# Marauder-like target hull set (the demoted SAM funnel -> the target_hull scenario).
MARAUDER_HULLS = ["T-AO", "T-AKE", "ESB", "T-EPF", "WPC", "WLB", "T-ESB", "T-AKR",
                  "T-AK", "T-ESD", "LSM", "T-LSM", "LCU", "FRC"]

# ── Prime lists (deck chartdata; consolidated here so chartdata imports them) ─
PRIMES_TAM = [
    ("General Dynamics", "General Dynamics"),
    ("Huntington Ingalls Industries", "Huntington Ingalls Industries"),
    ("BAE Systems", "BAE Systems"),
    ("Vigor Marine LLC", "VIGOR MARINE LLC"),
    ("The Charles Stark Draper Laboratory Inc.", "THE CHARLES STARK DRAPER LABORATORY  INC."),
    ("Detyens Shipyards Inc.", "DETYENS SHIPYARDS  INC."),
    ("Epsilon Systems Solutions Inc.", "EPSILON SYSTEMS SOLUTIONS  INC."),
    ("Lockheed Martin Corporation", "LOCKHEED MARTIN CORPORATION"),
    ("East Coast Repair & Fabrication LLC", "EAST COAST REPAIR & FABRICATION  LLC"),
    ("S.C.A. - Shipping Consultants Associated Ltd.", "S.C.A. - SHIPPING CONSULTANTS ASSOCIATED LTD."),
]
PRIMES_DEPOT = [
    ("BAE Systems", "BAE Systems"),
    ("General Dynamics", "General Dynamics"),
    ("Huntington Ingalls Industries", "Huntington Ingalls Industries"),
    ("Vigor Marine LLC", "VIGOR MARINE LLC"),
    ("Detyens Shipyards Inc.", "DETYENS SHIPYARDS  INC."),
    ("East Coast Repair & Fabrication LLC", "EAST COAST REPAIR & FABRICATION  LLC"),
    ("Epsilon Systems Solutions Inc.", "EPSILON SYSTEMS SOLUTIONS  INC."),
    ("Pacific Shipyards International LLC", "PACIFIC SHIPYARDS INTERNATIONAL  LLC"),
    ("Colonna's Ship Yard Incorporated", "COLONNA'S SHIP YARD  INCORPORATED"),
    ("Amentum Services Inc.", "AMENTUM SERVICES  INC."),
]
# RMC buckets in the chartdata sense (label -> raw RMC list) for the depot geo charts.
RMC_BUCKETS = [
    ("SWRMC", ["SWRMC"]), ("MARMC", ["MARMC"]), ("SERMC", ["SERMC"]),
    ("NW RMC", ["NW RMC / Puget Sound"]),
    ("FDNF", ["SRF-JRMC Yokosuka", "FDRMC Naples", "FLC Bahrain"]),
    ("USCG SFLC", ["USCG SFLC"]),
    ("Other", ["Pearl Harbor RMC", "Military Sealift Cmd", "NAVSEA HQ", "Portsmouth NSY",
               "Norfolk NSY", "NUWC", "Army/USACE", "Other"]),
]
IDV_SCOPES = [
    ("Full-Ship Avail", ["Full-Ship Availability"]), ("MSC Avail", ["MSC Availability"]),
    ("FDNF", ["FDNF Foreign MSRA"]), ("Other / Sup Svc", ["Other / Support Services"]),
    ("Other IDVs", ["USCG Cutter", "Trade IDIQ", "Planning & Engineering Support"]),
]
CONTRACTOR_TIER_LABELS = [
    ("CONUS full-ship primes", "Tier 1 - CONUS Complex Repair Prime"),
    ("Regional yards", "Tier 2 - Regional Repair"),
    ("Technical services (non-shipyard)", "Tier 3 - Technical Services"),
    ("Foreign MSRA yards", "Tier 4 - FDNF Foreign Yard"),
    ("Other", "Other"),
]

# ── Axes (ordered; each maps to the atom field that feeds it) ────────────────
# axis key -> (display label, atom tag-field name on the TAMAtoms row dict)
AXES = [
    ("work_segment", "Work segment", "work_segment"),
    ("hull", "Hull program", "hull"),
    ("buyer_rmc", "Buyer / RMC", "buyer_rmc"),
    ("contractor_tier", "Contractor tier", "contractor_tier"),
    ("idv_scope", "IDV scope", "idv_scope"),
    ("scope_class", "Scope class", "scope_class"),
    ("service", "Service", "service"),
]
AXIS_KEYS = [k for k, _label, _field in AXES]
AXIS_LABEL = {k: label for k, label, _field in AXES}
AXIS_FIELD = {k: field for k, _label, field in AXES}

# ── Scenarios ───────────────────────────────────────────────────────────────
# (key, display name, interpretation). Order = the menu order.
SCENARIOS = [
    ("broad_tam", "Broad TAM", "Whole reconciled FPDS-visible MRO TAM (100%)."),
    ("broad_addressable", "Broad Addressable",
     "TAM less captive SUPSHIP complex-OH and FMS (private-contestable base)."),
    ("core_depot", "Core Depot", "Addressable depot ship-repair (J998/J999)."),
    ("regional_yard", "Regional Yard", "Addressable depot at Tier-2 regional repair yards."),
    ("uscg_cutter", "USCG Cutter", "Addressable U.S. Coast Guard MRO."),
    ("msc_aux", "MSC / Auxiliary", "Addressable depot MSC availabilities (auxiliary fleet)."),
    ("technical_services", "Technical Services", "Addressable port & technical services work."),
    ("electronics_c4isr", "Electronics & C4ISR", "Addressable electronics & C4ISR sustainment."),
    ("target_hull", "Target Hull Set Depot MRO",
     "Addressable depot MRO on the marauder-like target hull set (nested in TAM)."),
]
SCENARIO_KEYS = [k for k, _n, _i in SCENARIOS]
SCENARIO_NAME = {k: n for k, n, _i in SCENARIOS}
SCENARIO_INTERP = {k: i for k, _n, i in SCENARIOS}

# Per-scenario axis constraints: {scenario_key: {axis_key: set(target buckets)}}.
# An axis NOT listed for a scenario is non-constraining (all its buckets flag 1,
# including the n/a / unmapped sentinels). An axis that IS listed flags 1 only on
# the target buckets (so sentinels flag 0 -> non-applicable atoms drop out).
SCENARIO_SPEC = {
    "broad_tam": {},
    "broad_addressable": {"scope_class": {SCOPE_ADDRESSABLE}},
    "core_depot": {"work_segment": {DEPOT_SEGMENT}, "scope_class": {SCOPE_ADDRESSABLE}},
    "regional_yard": {"work_segment": {DEPOT_SEGMENT}, "contractor_tier": {TIER_REGIONAL},
                      "scope_class": {SCOPE_ADDRESSABLE}},
    "uscg_cutter": {"service": {"Coast Guard"}, "scope_class": {SCOPE_ADDRESSABLE}},
    "msc_aux": {"work_segment": {DEPOT_SEGMENT}, "idv_scope": {IDV_MSC},
                "scope_class": {SCOPE_ADDRESSABLE}},
    "technical_services": {"work_segment": {"Port & Technical Services"},
                           "scope_class": {SCOPE_ADDRESSABLE}},
    "electronics_c4isr": {"work_segment": {"Electronics & C4ISR Sustainment"},
                          "scope_class": {SCOPE_ADDRESSABLE}},
    "target_hull": {"work_segment": {DEPOT_SEGMENT}, "hull": set(MARAUDER_HULLS),
                    "scope_class": {SCOPE_ADDRESSABLE}},
}


def scenario_flag(scenario_key: str, axis_key: str, bucket: str) -> int:
    """The 0/1 flag for (scenario, axis, bucket) per SCENARIO_SPEC.

    Non-constraining axis -> 1 for every bucket; constraining axis -> 1 only on
    its target buckets (so n/a / unmapped sentinels resolve to 0).
    """
    spec = SCENARIO_SPEC[scenario_key]
    if axis_key not in spec:
        return 1
    return 1 if bucket in spec[axis_key] else 0
