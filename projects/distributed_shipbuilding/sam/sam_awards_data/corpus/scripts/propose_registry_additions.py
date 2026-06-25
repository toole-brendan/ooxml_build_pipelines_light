#!/usr/bin/env python3
"""
Build the registry-additions worksheet from the adjudicated unclassified queue (B3).

Adjudications below were made 2026-06-11 from SAM NAICS priors + targeted web
evidence (cited per row). One worksheet row per UEI; firms with several UEIs
(entity + parent variants) get one row each so the registry's entity-first lookup
hits every flow. Vendors left out of ADJUDICATIONS stay unbucketed deliberately:
L3HARRIS (taxonomy pins it unbucketed), ESI Acquisition (machinery wholesaler,
work type unidentifiable), HTP Meds (medical tubing, scope unclear), SGL Automation
(no public footprint), MMC Metrology / NAG (instruments — no bucket), J.F. Lehman
(PE parent; operating entity unidentified), Hitachi/Fortive/Carlyle (conglomerate
keys, small dollars).

Output: extracted/registry_additions_worksheet.csv (full vendor_evidence_registry
schema). Review, then apply with merge_registry_additions.py.
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import EXTRACTED

BASE_FLAGS = {
    "structural": "metal,broad",
    "machining": "metal,hme,broad",
    "castings": "metal,broad",
    "piping": "hme,broad",
    "electrical": "electrical,hme,broad",
    "hvac": "hme,broad",
    "coatings": "broad",
}

# firm -> (ueis, display_name, bucket, confidence, basis, evidence_source, notes)
ADJUDICATIONS = [
    (["EGAVSJTA2D81", "CBMZJ3Z5SC89"], "GOODRICH CORP", "coatings", "med",
     "Goodrich EPP Jacksonville - submarine bow/sonar dome elastomer & composite structures",
     "SAM 3261 + agent", "Collins Aerospace Engineered Polymer Products"),
    (["UHXFGP3DCRK7"], "HANSOME ENERGY SYSTEMS, INC.", "hvac", "high",
     "Hansome Linden NJ - vane axial fans, Virginia-class atmosphere control ($31M NTE award)",
     "web (Defense Daily contract award) + agent",
     "core line is precision electrical machinery; the EB flow is ventilation fans"),
    (["D77VA4G9VJG8", "N9K8Y7U3RGA9", "C9C6HPQLL4A8"], "CATERPILLAR INC", "electrical", "med",
     "CAT marine diesel generator sets (Virginia-class emergency diesel)",
     "SAM 3331 + agent", ""),
    (["FMC8BKMNMKF2"], "FLUID CONDITIONING PRODUCTS, INC.", "piping", "med",
     "FCP Lancaster PA - hydraulic filters / fluid conditioning hardware",
     "SAM 3399 + agent", ""),
    (["XDF1FRDG8KK4"], "FOSTER-MILLER, INC.", "electrical", "med",
     "QinetiQ US - electrical/electromechanical systems for VA/Columbia (Electronic Grounding Unit)",
     "web (QinetiQ/EB press releases) + agent", ""),
    (["FWF8QBPCGLG3"], "GENERAL TOOL COMPANY", "machining", "med",
     "GTC Cincinnati - large precision machining/weldments (launch & handling systems)",
     "SAM 3364(corporate) + agent", "3364 is a corporate artifact; work is precision machining"),
    (["CT5WNUADNZ44", "PQNBC8KG93R3", "WREEAHYMRQ45"], "AMPHENOL CORPORATION", "electrical", "med",
     "Amphenol - mil-spec interconnects/connectors", "SAM 3344 + agent", ""),
    (["RXA2JHPN9JD3", "TUJCSP9NJ6V5", "KMDLJAJQ4UM1"], "BRANTNER AND ASSOCIATES, INC.", "electrical", "high",
     "SEACON Brantner El Cajon - underwater electrical connectors/penetrators",
     "SAM 3344 + agent", ""),
    (["NTREK31GP8N3", "DY2JXQ22MA14"], "KSARIA CORPORATION", "electrical", "high",
     "kSARIA - Navy-qualified fiber/copper cable assemblies & harnesses",
     "SAM 3344 + agent", ""),
    (["E9DKKLZNCQS9"], "TRIDENT MARITIME SYSTEMS UK LIMITED", "electrical", "low",
     "Trident Maritime (Callenberg) UK - marine electrical/electronic outfitting",
     "SAM 334419 + agent", "low conf: TMS group also does interiors/HVAC"),
    (["EVP4KM37YU23", "VUNMXC2JLBY3", "Y7N4SPXNK115", "X3DBJSMT83N5"], "CLEVELAND-CLIFFS INC.",
     "structural", "med",
     "Cleveland-Cliffs / CC Plate - HY-grade hull steel plate (mill)",
     "SAM 331110 + agent", "raw-material mill feeding structural fabrication"),
    (["SSD8KRDXKG46", "ZXMJM9MBXBQ4", "FQJTKZNF6GY5"], "THE HILLER COMPANIES, LLC", "piping", "med",
     "Hiller Mobile AL - shipboard fire suppression fluid systems (foam/CO2) on USN combatants",
     "SAM 2382 + web (hillerfire.com marine)", ""),
    (["SKKACASET588", "PU6TDFGSJQA3"], "DYNALEC CORPORATION", "electrical", "high",
     "Dynalec Sodus NY - shipboard electrical control/announcing systems",
     "SAM 3342 + agent", ""),
    (["DQ35GXAUTW61"], "INDUSTRIAL CORROSION CONTROL, INC.", "coatings", "high",
     "ICC - marine painting/corrosion-control contractor", "SAM 2383 + agent", ""),
    (["NG7TY7BYU9R7", "HUYTR5ZGSSN6", "V91WXBJ7WKL1", "LGVPVLMRHH51"], "W. & O. SUPPLY, INC.",
     "piping", "high",
     "W&O - marine pipe, valve & fitting distribution", "SAM 4238 + agent", ""),
    (["C7QHHMJEALN1"], "MONROE CABLE COMPANY, INC.", "electrical", "med",
     "Monroe Cable - shipboard electrical cable (copper wire & cable mfg)",
     "SAM 331420 + agent", ""),
    (["K48HS3521BC4", "D5NGX38L5EC9", "N6P1AGPMV456"], "EVAC NORTH AMERICA INC", "piping", "med",
     "Evac - marine vacuum sanitation/waste fluid systems", "SAM 3333 + agent", ""),
]


def main() -> int:
    with (EXTRACTED / "coverage_unclassified_top.csv").open(encoding="utf-8-sig", newline="") as fh:
        queue = list(csv.DictReader(fh))
    # per-UEI program dollars (vendor_key rows; entity UEIs may repeat across keys)
    dollars = defaultdict(lambda: {"submarines": 0.0, "ddg": 0.0})
    for r in queue:
        for u in {r["vendor_key_uei"], r["entity_uei"], r["parent_uei"]}:
            if u:
                dollars[u][r["program"]] = max(dollars[u][r["program"]],
                                               float(r["dollars_all_$M"] or 0))

    rows = []
    for ueis, name, bucket, conf, basis, source, notes in ADJUDICATIONS:
        subs = max(dollars[u]["submarines"] for u in ueis)
        ddg = max(dollars[u]["ddg"] for u in ueis)
        platform = "both" if (subs and ddg) else ("subs" if subs else "ddg")
        for uei in ueis:
            rows.append({
                "uei": uei, "entity_name": name, "parent_or_display_name": name,
                "platform": platform,
                "ddg_signed_$M": round(ddg, 1), "subs_signed_$M": round(subs, 1),
                "role": "supplier", "bucket": bucket, "in_physical_base": "yes",
                "scenario_flags": BASE_FLAGS[bucket], "confidence": conf,
                "basis": basis, "evidence_source": source,
                "override_grain": "firm_entity", "notes": notes,
            })

    out = EXTRACTED / "registry_additions_worksheet.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"Wrote {out} ({len(rows)} UEI rows, {len(ADJUDICATIONS)} firms)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
