#!/usr/bin/env python3
"""
Classify DoD daily-contract actions (from extracted/dod_announcement_pop.csv)
along two axes — DESTROYER version.

  1. PROGRAM FAMILY — which weapons system the action is for:
        ddg51, ddg_gfe_aegis, ddg_gfe_radar, ddg_gfe_propulsion,
        ddg_gfe_guns, ddg_gfe_combat_systems, ddg_gfe_weapons,
        ddg_repair, ddg1000, va, col, sub_other, cvn, lcs,
        surface_other, missile_weapons, unknown

     ddg_gfe_* tags are for GFE primes (LM Aegis, Raytheon SPY-6, GE LM2500,
     BAE Mk 45/VLS, NG SPQ-9B, L3Harris CEC) that flow into DDG hulls.
     Note these primes also serve other ships, so reclassify-pass tightens.

  2. WORK TYPE — what kind of work the action covers (multi-label):
        construction, lltm_early_mfg, advance_procurement, eoq,
        component_procurement, lead_yard, design, sustainment_maintenance,
        sib_supplier_dev, facilities, repair_overhaul, fms, engineering,
        other

The first-pass DDG_FILTER from the pull script is loose (any paragraph
mentioning DDG/Aegis/Mk 41 VLS keywords). Many rows are surface-combat
sustainment or missile work that's NOT new-construction-DDG. This script
applies regex to enable the framework-style per-bucket POP analysis,
followed by a manual second-pass tightening in
reclassify_dod_action_subrelevance.py.

Outputs:
  - extracted/dod_announcement_pop.csv (in place: 6 new columns appended)
  - extracted/dod_action_pop_by_worktype.csv  ($-weighted POP shares per
        (program_family, work_type_primary) bucket)
"""
import csv
import os
import re
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
IN_CSV = REPO / "extracted" / "dod_announcement_pop.csv"
OUT_ROLLUP = REPO / "extracted" / "dod_action_pop_by_worktype.csv"

# ---- Program family rules (order matters; first match wins for primary,
#      but we record all matches in program_all) ----

PROGRAM_RULES = [
    ("ddg51", [
        r"\bDDG[- ]?(?:51|5[2-9]|[6-9]\d|1[0-5]\d|16[0-9])\b",  # DDG 51-169
        r"\bArleigh Burke[- ]class\b",
        r"\bArleigh Burke\b",
        r"\bguided[- ]missile destroyer\b",
        r"\bFlight\s+I{2,3}\b.{0,40}(?:destroyer|DDG)",
        r"\b(?:Bath Iron Works|BIW)\b",
        r"\bIngalls Shipbuilding\b",
        r"\bHII\s+Ingalls\b",
        r"destroyer.{0,40}(?:Bath|Pascagoula)",
    ]),
    ("ddg1000", [
        r"\bDDG[- ]?100[0-9]\b",  # DDG 1000-1009 (Zumwalt)
        r"\bZumwalt[- ]class\b",
    ]),
    ("ddg_gfe_aegis", [
        # Aegis Combat System (combat-system software / OFP / baseline)
        r"\bAegis\s+(?:Combat System|Weapon System|Baseline|Modernization|software)\b",
        r"\bAegis\s+Technical\s+Representative\b",
        r"\bAEGIS\s+TI[- ]\d+\b",
        r"\bAegis\s+Ashore\b",
    ]),
    ("ddg_gfe_radar", [
        # Air & Missile Defense Radar / SPY-6 (Raytheon)
        r"\bAN/SPY[- ]?6\b",
        r"\bSPY[- ]?6\b",
        r"\bAir and Missile Defense Radar\b|\bAMDR\b",
        r"\bAN/SPQ[- ]?9B\b",  # X-band horizon-search (NG)
    ]),
    ("ddg_gfe_propulsion", [
        # LM2500 gas turbines + accessories (GE Aerospace / Rolls-Royce)
        r"\bLM2500\b",
        r"\bMarine Gas Turbine\b.{0,40}(?:destroyer|DDG|cruiser)",
        r"\bAllison\s+501\b",  # gas turbine generator
    ]),
    ("ddg_gfe_guns", [
        # Mk 45 5-inch gun (BAE) + Mk 38 25mm (BAE) + Mk 110 57mm (BAE)
        r"\bMk[- ]?45\b|\bMK[- ]?45\b",
        r"\bMk[- ]?38\b|\bMK[- ]?38\b",
        r"\b5[- ]?inch\s+gun\b",
        r"\bMk[- ]?110\b|\bMK[- ]?110\b",  # 57mm
    ]),
    ("ddg_gfe_vls", [
        # Vertical Launching System / Mk 41 launcher / Mk 25 canister (LM/BAE)
        r"\bVertical Launching System\b|\bVLS\b",
        r"\bMk[- ]?41\b|\bMK[- ]?41\b",
        r"\bMk[- ]?25\s*Mod\b",  # MK 25 canister assemblies
        r"\bMk[- ]?21\s*Mod\b",  # MK 21 canister assemblies
    ]),
    ("ddg_gfe_combat_systems", [
        # CEC (L3Harris USG-2B/3B), DRS combat systems pieces
        r"\bCooperative Engagement Capability\b|\bCEC\b",
        r"\bAN/USG[- ]?[23]\b",
        r"\bIntegrated Fire Control\b|\bNIFC[- ]?CA\b",
        r"\bShip Self[- ]Defense System\b|\bSSDS\b",
        r"\bMk\s*[0-9]+\s*Identification Friend\s+or\s+Foe\b|\bMk\s*XII\b",
    ]),
    ("ddg_gfe_weapons", [
        # Munitions / interceptors that arm DDG (typically WPN, not SCN,
        # but appear in DoD bulletins and bear flagging)
        r"\bStandard Missile\b",
        r"\bSM[- ]?[23]\b|\bSM[- ]?6\b",
        r"\bEvolved Sea[Ss]parrow\b|\bESSM\b",
        r"\bSeaSparrow\b",
        r"\bClose[- ]In Weapon System\b|\bCIWS\b|\bPhalanx\b",
        r"\bRolling Airframe Missile\b|\bSeaRAM\b",
        r"\bTomahawk\b",
        r"\bMk\s*54\b",  # lightweight torpedo (DDG carries; Raytheon)
        r"\bMk\s*46\b",  # legacy lightweight torpedo
    ]),
    ("va", [
        r"\bVirginia[- ]class\b",
        r"\bVCS\b",
        r"\bVa\s+Block\b",
        r"\bBlock\s+(?:IV|V|VI)\s+(?:Virginia|Va\b)",
        r"\bSSN[- ]?\d{3}\b",
    ]),
    ("col", [
        r"\bColumbia[- ]class\b",
        r"\bSSBN[- ]?\d{3}\b",
        r"\bCommon Missile Compartment\b|\bCMC\b",
    ]),
    ("cvn", [
        r"\bCVN[- ]?\d{2,3}\b",
        r"\baircraft carrier\b",
        r"\bRCOH\b",
        r"\bFord[- ]class\b",
        r"\bNimitz[- ]class\b",
    ]),
    ("lcs", [
        r"\bLCS\b",
        r"\bLittoral Combat Ship\b",
    ]),
    ("surface_other", [
        r"\bLHA[- ]?\d+\b",
        r"\bLPD[- ]?\d+\b",
        r"\bamphibious\b",
        r"\bWasp[- ]class\b",
        r"\bSan Antonio[- ]class\b",
        r"\bT-AO\b",
        r"\bConstellation[- ]class\b",
        r"\bfrigate\b",
        r"\bexpeditionary\b",
        r"\bRiver[- ]Class\b",
    ]),
    ("sub_other", [
        r"\bsubmarine[s]?\b",
        r"\bElectric Boat\b",
        r"\bGDEB\b",
        r"\bBechtel Plant Machinery\b|\bBPMI\b",
        r"\bnaval nuclear propulsion\b",
    ]),
]

# ---- Work-type rules (multi-label; an action can have multiple) ----

WORKTYPE_RULES = [
    ("lltm_early_mfg", [
        r"long[- ]lead\s+(?:time\s+)?material",
        r"long[- ]lead\s+items?",
        r"\bLLTM\b",
        r"early\s+manufacturing",
        r"early\s+production",
        r"preliminary\s+construction",
        r"pre[- ]construction",
    ]),
    ("advance_procurement", [
        r"advance\s+procurement",
        r"advance\s+construction",
    ]),
    ("eoq", [
        r"economic\s+order\s+quantit",
        r"\bEOQ\b",
    ]),
    ("construction", [
        r"for\s+the\s+construction\s+of",
        r"destroyer\s+construction",
        r"\bconstruction\s+of\s+(?:the\s+|a\s+|an\s+|\d+\s+)",
        r"new\s+construction",
        r"\bConstruction\s+Spares\b",
        r"\bDDG[- ]?\d+\b.{0,40}construction",
        r"\bFY\s*\d{2}\s+(?:DDG|destroyer)",
    ]),
    ("component_procurement", [
        r"\bprocurement\s+of\s+\d+\b",
        r"\bshipset\s+of\b",
        r"\brepair\s+parts\b",
        r"\bspare\s+parts\b",
        r"\bgas\s+turbine\b",
        r"\bcanisters?\b",
        r"\bgun\s+mounts?\b",
        r"\bvalves?\b",
        r"\bforgings?\b",
        r"\bradar\s+(?:array|set|sensor)s?\b",
        r"\bgenerator\s+procurement\b",
        r"\bmissile\s+(?:procurement|production)\b",
    ]),
    ("lead_yard", [
        r"lead\s+yard\s+(?:support|services)",
        r"class\s+lead\s+yard",
        r"design\s+agent",
        r"planning\s+yard",
    ]),
    ("design", [
        r"\bdesign\s+(?:efforts?|services|work|studies|development|transfer|drawings)\b",
        r"engineering\s+design",
        r"design\s+and\s+development",
        r"detail(?:ed)?\s+design",
        r"\bFlight\s+III\s+design\b",
    ]),
    ("sustainment_maintenance", [
        r"\bsustainment\b",
        r"\bmodernization\b",
        r"maintenance\s+(?:and\s+modernization|services)",
        r"\bavailabilit(?:y|ies)\b",
        r"\bship\s+alteration\b",
    ]),
    ("sib_supplier_dev", [
        r"submarine\s+industrial\s+base",  # in case mis-tagged DDG
        r"surface\s+industrial\s+base",
        r"maritime\s+industrial\s+base",
        r"industrial\s+base\s+(?:development|investment|supplier)",
        r"supplier\s+development",
        r"supplier\s+expansion",
        r"\bSIB\b|\bMIB\b",
        r"workforce\s+development",
        r"shipyard\s+infrastructure",
    ]),
    ("facilities", [
        r"facility\s+(?:upgrade|expansion|modernization)",
        r"facilit(?:y|ies)\s+(?:work|construction)",
        r"\b(?:Pier|Drydock|Dry Dock|Building)\s+\w+\s+(?:upgrade|expansion|construction|replacement)",
        r"new\s+(?:construction|modernization)\s+of\s+(?:Pier|Drydock|Building)",
    ]),
    ("repair_overhaul", [
        r"\bDSRA\b|\bDocking Selected Restricted Availability\b",
        r"\bEDSRA\b|\bExtended Docking\b",
        r"\bSRA\b",
        r"\bCNO\s+(?:scheduled\s+)?availability\b",
        r"depot\s+(?:maintenance|level)",
        r"\boverhaul\b",
        r"\bbackfit\b",
        r"engineered\s+overhaul",
        r"\bRCOH\b|\bEOH\b",
        r"\bdry[- ]?docking\b",
        r"\bvoyage\s+repair\b",
    ]),
    ("fms", [
        r"Foreign\s+Military\s+Sales?",
        r"\bFMS\b",
        r"Foreign\s+Partner",
        r"foreign\s+military\s+financing",
    ]),
    ("engineering", [
        r"engineering\s+(?:and\s+technical|services|support|design,?\s+development)",
        r"technical\s+(?:support|services)",
        r"design,?\s+(?:development,?\s+)?(?:and\s+production|engineering)",
    ]),
]

# Priority order for primary work_type (most TAM-relevant first)
PRIORITY = [
    "construction",
    "lltm_early_mfg",
    "advance_procurement",
    "eoq",
    "component_procurement",
    "facilities",
    "lead_yard",
    "design",
    "sib_supplier_dev",
    "sustainment_maintenance",
    "repair_overhaul",
    "fms",
    "engineering",
    "other",
]

# Define which work types count as new-construction-supplier-TAM-relevant
TAM_RELEVANT = {
    "construction",
    "lltm_early_mfg",
    "advance_procurement",
    "eoq",
    "component_procurement",
}


def classify_program(text):
    """Return (primary_family, all_families_list)."""
    hits = []
    for fam, patterns in PROGRAM_RULES:
        if any(re.search(p, text, re.I) for p in patterns):
            hits.append(fam)
    if not hits:
        return ("unknown", [])
    # If both ddg51 and a sub-program → DDG wins (those are dual-purpose primes)
    # Primary = first hit in declared PROGRAM_RULES order (already prioritized)
    primary = hits[0]
    return (primary, hits)


def classify_worktype(text):
    """Return (primary_work_type, all_work_types_list, ambiguous_flag)."""
    hits = []
    for wt, patterns in WORKTYPE_RULES:
        if any(re.search(p, text, re.I) for p in patterns):
            hits.append(wt)
    if not hits:
        return ("other", [], False)
    primary = next((wt for wt in PRIORITY if wt in hits), hits[0])
    ambiguous = len(hits) >= 2
    return (primary, hits, ambiguous)


def main():
    with open(IN_CSV) as f:
        rows = list(csv.DictReader(f))

    new_rows = []
    for r in rows:
        p = r["paragraph_text"]
        prog_primary, prog_all = classify_program(p)
        wt_primary, wt_all, wt_amb = classify_worktype(p)
        r["program_primary"] = prog_primary
        r["program_all"] = ";".join(prog_all)
        r["work_type_primary"] = wt_primary
        r["work_type_all"] = ";".join(wt_all)
        r["work_type_ambiguous"] = "Y" if wt_amb else ""
        # TAM relevance gate — DDG-51 program + GFE component primes
        DDG_TAM_PROGRAMS = {
            "ddg51",
            "ddg_gfe_aegis", "ddg_gfe_radar", "ddg_gfe_propulsion",
            "ddg_gfe_guns", "ddg_gfe_vls", "ddg_gfe_combat_systems",
        }
        r["is_ddg_new_construction_tam"] = (
            "yes"
            if prog_primary in DDG_TAM_PROGRAMS and wt_primary in TAM_RELEVANT
            else "no"
        )
        new_rows.append(r)

    # Rewrite the CSV with new columns
    fields = list(rows[0].keys())
    extras = [
        "program_primary", "program_all",
        "work_type_primary", "work_type_all", "work_type_ambiguous",
        "is_ddg_new_construction_tam",
    ]
    for ex in extras:
        if ex not in fields:
            fields.append(ex)
    with open(IN_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in new_rows:
            w.writerow({k: r.get(k, "") for k in fields})

    def _f(v):
        try: return float(v)
        except (ValueError, TypeError): return 0.0
    # ----- Rollup: $-weighted POP shares per (program_family, work_type_primary) bucket -----
    buckets = defaultdict(lambda: {"n": 0, "total": 0.0, "biw": 0.0, "ingalls": 0.0, "other_us": 0.0, "foreign": 0.0})
    for r in new_rows:
        amt = _f(r["amount_usd"])
        if amt <= 0:
            continue
        key = (r["program_primary"], r["work_type_primary"])
        b = buckets[key]
        b["n"] += 1
        b["total"] += amt
        b["biw"] += amt * _f(r["pop_biw_site_pct"])
        b["ingalls"] += amt * _f(r["pop_ingalls_site_pct"])
        b["other_us"] += amt * _f(r["pop_other_us_pct"])
        b["foreign"] += amt * _f(r["pop_foreign_pct"])

    with open(OUT_ROLLUP, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "program_family", "work_type_primary",
            "n_actions", "total_dollars_usd",
            "pop_biw_pct_w", "pop_ingalls_pct_w", "pop_other_us_pct_w", "pop_foreign_pct_w",
        ])
        for (prog, wt) in sorted(buckets, key=lambda k: -buckets[k]["total"]):
            b = buckets[(prog, wt)]
            tot = b["total"] or 1
            w.writerow([
                prog, wt, b["n"], round(b["total"], 2),
                round(b["biw"] / tot, 2),
                round(b["ingalls"] / tot, 2),
                round(b["other_us"] / tot, 2),
                round(b["foreign"] / tot, 2),
            ])

    # Console summary
    from collections import Counter
    prog_n = Counter(r["program_primary"] for r in new_rows)
    prog_d = Counter()
    for r in new_rows:
        prog_d[r["program_primary"]] += _f(r["amount_usd"])
    print("=== program family distribution ===")
    for p in sorted(prog_n, key=lambda k: -prog_d[k]):
        print(f"  {p:<24}  {prog_n[p]:>4} rows  ${prog_d[p]/1e6:>11,.1f}M")

    DDG_FAM = {"ddg51", "ddg_gfe_aegis", "ddg_gfe_radar", "ddg_gfe_propulsion",
               "ddg_gfe_guns", "ddg_gfe_vls", "ddg_gfe_combat_systems"}
    wt_n = Counter(r["work_type_primary"] for r in new_rows if r["program_primary"] in DDG_FAM)
    wt_d = Counter()
    for r in new_rows:
        if r["program_primary"] in DDG_FAM:
            wt_d[r["work_type_primary"]] += _f(r["amount_usd"])
    print(f"\n=== work-type breakdown — DDG-program rows only ({sum(wt_n.values())} actions, ${sum(wt_d.values())/1e6:,.1f}M total) ===")
    for wt in sorted(wt_n, key=lambda k: -wt_d[k]):
        print(f"  {wt:<28}  {wt_n[wt]:>3} rows  ${wt_d[wt]/1e6:>10,.1f}M")

    print(f"\n=== DDG-construction-supplier-TAM-relevant actions (first-pass yes-gate) ===")
    tam_rows = [r for r in new_rows if r["is_ddg_new_construction_tam"] == "yes"]
    tam_total = sum(_f(r["amount_usd"]) for r in tam_rows)
    print(f"  {len(tam_rows)} rows, ${tam_total/1e6:,.1f}M total")
    if tam_rows and tam_total > 0:
        biw = sum(_f(r["amount_usd"]) * _f(r["pop_biw_site_pct"]) for r in tam_rows) / tam_total
        ing = sum(_f(r["amount_usd"]) * _f(r["pop_ingalls_site_pct"]) for r in tam_rows) / tam_total
        oth = sum(_f(r["amount_usd"]) * _f(r["pop_other_us_pct"]) for r in tam_rows) / tam_total
        for_ = sum(_f(r["amount_usd"]) * _f(r["pop_foreign_pct"]) for r in tam_rows) / tam_total
        print(f"  $-weighted POP: BIW {biw:.1f}% | Ingalls {ing:.1f}% | Other-US {oth:.1f}% | Foreign {for_:.1f}%")

    print(f"\nWrote enriched CSV → {IN_CSV}")
    print(f"Wrote rollup → {OUT_ROLLUP}")


if __name__ == "__main__":
    main()
