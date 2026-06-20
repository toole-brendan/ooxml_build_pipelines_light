"""_taxonomy - shared work-type bucket vocabulary + the subaward classifier (DDG).

NON-sheet helper module (renders nothing; NOT registered in SHEETS). It holds the
one load-bearing cross-sheet vocabulary of the DDG workbook - the seven work-type
buckets, the NAICS-4 crosswalk, the name-key lists, and
``classify()`` - so every sheet module that needs them (methodology renders them;
entities classifies vendors; inputs / scenarios / sam_build / bucket_evidence
iterate the bucket list; deck_outputs needs BUCKET_KEYS) imports from ONE place
instead of from a rendering module.

Keeping the vocabulary here (rather than inside methodology) means a sheet module
that consumes the taxonomy never has to import the methodology *renderer*, which
keeps the import graph clean: _taxonomy has no sheet dependencies, so it is a true
leaf every other module can depend on.

Classification is registry-led: the governing signal is the operating-entity NAICS
resolved by sub_entity_uei (applied in data_entity_master via the evidence registry).
``classify()`` here is the NAICS/name FALLBACK for entities not in the registry; it
still accepts a ``desc`` arg for signature compatibility but ignores it (the legacy
description-keyword step is dropped).
"""
from __future__ import annotations

# (key, display name, one-line definition)
BUCKETS: list[tuple[str, str, str]] = [
    ("structural", "Structural fabrication & modules",
     "hull sections, fabricated structural metal, deckhouse, pre-outfit modules"),
    ("machining", "Machining / mechanical / propulsion",
     "machine shops, precision machining, mechanical power transmission, propulsion machinery"),
    ("castings", "Castings & forgings",
     "iron/steel forging, steel foundries, cast components"),
    ("piping", "Piping / fluid handling",
     "industrial valves, pumps, manifolds, pipe & fittings, hydraulics"),
    ("electrical", "Electrical power / distribution / generation",
     "switchgear, switchboards, transformers, generators/motors, ship power distribution"),
    ("hvac", "HVAC / ventilation / chilled water",
     "air-conditioning, chilled water, warm-air heating, shipboard ventilation"),
    ("coatings", "Coatings / insulation / decking",
     "coatings, paint, deck covering, insulation, rubber/synthetic/composites"),
]
BUCKET_KEYS: list[str] = [b[0] for b in BUCKETS]
UNBUCKETED = "unbucketed"

DESC_BUCKET: dict[str, list[str]] = {
    "structural": ["structural", "fabricat", "weldment", "steel plate", "hull",
                   "deckhouse", "module", "foundation", "sheet metal", "girder"],
    "machining": ["machin", "machined part", "precision component", "cnc",
                  "gear", "shaft", "bearing"],
    "castings": ["casting", "forging", "forged", "cast ", "foundry"],
    "piping": ["valve", "pump", "piping", "pipe ", "fitting", "manifold",
               "hydraulic", "flange", "strainer"],
    "electrical": ["electric", "switchboard", "switchgear", "cable", "wiring",
                   "power distribution", "generator", "motor", "transformer",
                   "circuit", "controller"],
    "hvac": ["hvac", "ventilat", "air conditioning", "chilled water", "heating",
             "ahu", "fan coil", "ductwork"],
    "coatings": ["coating", "insulation", "paint", "deck covering", "rubber",
                 "composite", "non-skid", "preservation"],
}

NAICS4_BUCKET: dict[str, str] = {
    "3323": "structural", "3324": "structural", "3366": "structural",
    "3369": "structural",
    "3327": "machining", "3336": "machining",
    "3321": "castings", "3315": "castings", "3312": "castings",
    "3329": "piping", "3339": "piping", "4235": "piping",
    "3353": "electrical", "3359": "electrical",   # real ship-power equipment only
    # NOTE: 3364 (aerospace) and 3344 (electronic components) deliberately REMOVED -
    # they were a corporate-NAICS artifact that swept defense electronics into
    # "electrical". Those are now resolved per operating entity via the registry.
    "3334": "hvac",
    "3252": "coatings", "3259": "coatings", "3262": "coatings",
}
SERVICE_NAICS4: set[str] = {
    "5413", "5415", "5416", "5417", "5132", "6114", "4885", "4247",
    "2362", "4236", "8113", "5418", "5614", "5612", "5419", "5612",
}

PRIME_NAME_KEYS = ["BATH IRON WORKS", "GENERAL DYNAMICS", "HUNTINGTON INGALLS",
                   "INGALLS SHIPBUILDING", "INGALLS OPERATIONS"]
GFE_MIB_NAME_KEYS = ["LOCKHEED", "RAYTHEON", "RTX", "BAE SYSTEMS LAND",
                     "NORTHROP GRUMMAN SYSTEMS", "L3HARRIS TECHNOLOGIES"]
VENDOR_BUCKET_OVERRIDES: list[tuple[str, str]] = [
    ("CURTISS-WRIGHT", "piping"), ("CIRCOR", "piping"), ("LESLIE CONTROLS", "piping"),
    ("FAIRBANKS MORSE", "machining"), ("L-3 MARINE", "electrical"),
    ("DRS NAVAL", "electrical"), ("ROLLS-ROYCE", "machining"),
]


def classify(vendor: str, naics4: str = "", desc: str = "") -> tuple[str, str, str]:
    """Return (role, bucket, basis) for a DDG subaward record (FALLBACK ladder).

    The governing signal is the operating-entity registry (resolved upstream in
    data_entity_master by sub_entity_uei); this function is the fallback for records
    NOT in the registry. role in {supplier, prime, co_prime, gfe_mib, service,
    holding}; bucket in BUCKET_KEYS or UNBUCKETED.

    Precedence: prime/co-prime name, GFE/MIB name, vendor-name override, NAICS-4
    crosswalk (3364/3344 -> electrical REMOVED as an artifact), service NAICS, 5511
    holding, residual. The legacy description-keyword step is dropped (descriptions
    proved a weak, misleading signal); ``desc`` is accepted for signature
    compatibility but ignored.
    """
    v = (vendor or "").upper()
    n = (naics4 or "").strip()

    for k in PRIME_NAME_KEYS:
        if k in v:
            role = "co_prime" if "INGALLS" in v else "prime"
            return (role, "", "prime/co-prime name")
    for k in GFE_MIB_NAME_KEYS:
        if k in v:
            return ("gfe_mib", "", "GFE/MIB name")
    for k, b in VENDOR_BUCKET_OVERRIDES:
        if k in v:
            return ("supplier", b, "vendor-override")
    if n in NAICS4_BUCKET:
        return ("supplier", NAICS4_BUCKET[n], "naics4")
    if n in SERVICE_NAICS4:
        return ("service", "", "service NAICS")
    if n == "5511":
        return ("holding", "", "holding-co (5511)")
    return ("supplier", UNBUCKETED, "residual")
