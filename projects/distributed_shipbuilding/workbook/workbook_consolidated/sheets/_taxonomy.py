"""_taxonomy - shared work-type bucket vocabulary + the subaward classifier.

NON-sheet helper module (renders nothing; NOT registered in SHEETS). It holds the
one load-bearing cross-sheet vocabulary of the workbook - the seven work-type
buckets, the NAICS-4 -> bucket crosswalk, the name-key lists, and ``classify()`` -
so that every sheet module that needs them (methodology renders them; entity_master
classifies vendors; inputs / sam_build / worktype_evidence iterate the bucket list;
the register/validation tabs need BUCKET_KEYS) imports from ONE place instead of
from a rendering module.

Keeping the vocabulary here (rather than inside a renderer) keeps the import graph
clean: _taxonomy has no sheet dependencies, so it is a true leaf every other
module can depend on.

SCAFFOLD NOTE: the seven buckets, the NAICS-4 crosswalk and the SERVICE_NAICS4 set
are the shared cross-program vocabulary (identical to submarines / ddg). The
name-key lists (PRIME_NAME_KEYS, GFE_SIB_NAME_KEYS) and VENDOR_BUCKET_OVERRIDES
below are copied from the submarines pipeline as a starting point; for the
consolidated workbook (submarines + ddg) reconcile them to the UNION of both
programs' primes / co-primes / overrides when you wire the first data sheet.
"""
from __future__ import annotations

# (key, display name, one-line definition)
BUCKETS: list[tuple[str, str, str]] = [
    ("structural", "Structural fabrication & modules",
     "hull sections, fabricated structural metal, pre-outfit modules"),
    ("machining", "Machining / mechanical / propulsion",
     "machine shops, precision machining, mechanical power transmission, propulsion machinery"),
    ("castings", "Castings & forgings",
     "iron/steel forging, steel foundries, cast components"),
    ("piping", "Piping / fluid handling",
     "industrial valves, pumps, measuring/dispensing, pipe & fittings"),
    ("electrical", "Electrical power / distribution / generation",
     "switchgear, transformers, turbine generators, motors, ship power distribution"),
    ("hvac", "HVAC / ventilation / chilled water",
     "air-conditioning, warm-air heating, shipboard ventilation"),
    ("coatings", "Coatings / insulation / decking",
     "rubber/synthetic, composites, coatings & insulation"),
]
BUCKET_KEYS: list[str] = [b[0] for b in BUCKETS]
UNBUCKETED = "unbucketed"

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
    "2362", "4236", "8113", "5418", "5614", "5612", "5419",
}
PRIME_NAME_KEYS = ["ELECTRIC BOAT", "GENERAL DYNAMICS", "HUNTINGTON INGALLS",
                   "NEWPORT NEWS", "BAE SYSTEMS LAND"]
GFE_SIB_NAME_KEYS = ["LOCKHEED", "ULTRA ELECTRONICS", "RAYTHEON", "BLUEFORGE"]
VENDOR_BUCKET_OVERRIDES: list[tuple[str, str]] = [
    ("RHOADS METAL", "structural"), ("AUSTAL", "structural"),
    ("CP INDUSTRIES", "structural"),
    ("CURTISS-WRIGHT FLOW", "piping"), ("CIRCOR", "piping"),
    ("HUNT VALVE", "piping"), ("TIOGA PIPE", "piping"),
    ("OIL STATES", "coatings"),
    ("BWX", UNBUCKETED), ("ULTRA ELECTRONICS", UNBUCKETED),
    ("GOODRICH", UNBUCKETED), ("APCO", UNBUCKETED), ("L3HARRIS", UNBUCKETED),
]


def classify(vendor: str, naics4: str) -> tuple[str, str, str]:
    """Return (role, bucket, basis) for a subaward vendor (FALLBACK ladder).

    The governing signal is the operating-entity registry (resolved upstream in
    data_entity_master by sub_entity_uei); this function is the fallback for records
    NOT in the registry. role in {supplier, prime, co_prime, gfe_sib, service,
    holding}; bucket in BUCKET_KEYS or UNBUCKETED ("" for non-supplier roles).

    Precedence: prime/co-prime name, GFE/SIB name, vendor-name override, NAICS-4
    crosswalk (3364/3344 -> electrical REMOVED as an artifact), service NAICS, 5511
    holding, residual.
    """
    v = (vendor or "").upper()
    n = (naics4 or "").strip()
    for k in PRIME_NAME_KEYS:
        if k in v:
            role = "co_prime" if ("INGALLS" in v or "NEWPORT" in v) else "prime"
            return (role, "", "prime/co-prime name")
    for k in GFE_SIB_NAME_KEYS:
        if k in v:
            return ("gfe_sib", "", "GFE/SIB name")
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
