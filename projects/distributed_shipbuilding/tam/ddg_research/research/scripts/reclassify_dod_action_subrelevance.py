#!/usr/bin/env python3
"""
Second-pass classifier for extracted/dod_announcement_pop.csv (DESTROYER).

The first-pass classifier (classify_dod_action_worktype.py) was based on
mechanical regex over the loose-filter pull. Many rows are surface-combat
sustainment, depot maintenance, missile production for FMS, or
non-destroyer surface combatant work that happened to mention DDG / Aegis
/ VLS keywords. This pass tightens via judgment rules.

  - HARD DROP rows that are clearly NOT destroyer new-construction work:
      submarine work (SSN/SSBN/Virginia/Columbia/Electric Boat/BPMI/NNS sub)
      carriers (CVN, Ford-class, Nimitz, RCOH)
      LCS, LCAC, Polar Security Cutter, Coast Guard, frigate (Constellation)
      amphibs (LHA, LPD, San Antonio, Wasp, T-AO oilers)
      airborne ASW (P-8A, helo) and unmanned surface
      Royal Navy / Japanese MOD / Korean POSCO foreign-customer FMS
      surface ship sustainment NOT on DDG (Ticonderoga CG sustainment etc.)
      ship maintenance availabilities (DSRA, SRA, EDSRA, voyage repair)
        — these are DDG-related but NOT new construction
      DDG-1000 Zumwalt (per project scope: only 3 ships, OPN not SCN)

  - PROMOTE ddg-relevant rows to refined tags:
      LM Aegis (Moorestown NJ, multi-ship combat system) → ddg_gfe_aegis
      Raytheon SPY-6 (Andover MA) → ddg_gfe_radar
      GE LM2500 (Evendale OH / Lynn MA / Hooksett NH) → ddg_gfe_propulsion
      BAE Mk 45 / Mk 38 / Mk 110 (Louisville KY / Minneapolis MN /
        Sterling Heights MI) → ddg_gfe_guns
      LM / BAE VLS Mk 41 / Mk 21 canisters → ddg_gfe_vls
      L3Harris CEC AN/USG-2B/3B → ddg_gfe_combat_systems
      NG SPQ-9B (Linthicum MD / Baltimore MD) → ddg_gfe_radar
      Raytheon SM-2/3/6/ESSM/Tomahawk → ddg_gfe_weapons (note: WPN funded
        not SCN, but appears in bulletins)

  - ddg_relevance final tag: yes_new_construction | yes_sustainment |
        yes_supplier_or_gfe | no | borderline

  - is_ddg_new_construction_tam recomputed: yes only if program in
        {ddg51, ddg_gfe_aegis, ddg_gfe_radar, ddg_gfe_propulsion,
         ddg_gfe_guns, ddg_gfe_vls, ddg_gfe_combat_systems}
        AND work_type in TAM_RELEVANT
        AND ddg_relevance in {yes_new_construction, yes_supplier_or_gfe}.

Outputs: rewrites extracted/dod_announcement_pop.csv with two new columns
appended (ddg_relevance, program_refined). Rebuilds rollup.
"""
import csv
import os
import re
from collections import defaultdict
from pathlib import Path

IN_CSV = Path("/Users/brendantoole/projects2/destroyer_outsourced_work/extracted/dod_announcement_pop.csv")
OUT_ROLLUP = Path("/Users/brendantoole/projects2/destroyer_outsourced_work/extracted/dod_action_pop_by_worktype.csv")

# ---- Strong NOT-DESTROYER markers — if any match, drop ----
# Order matters: more specific patterns first (we exit on first match).
HARD_DROP_PATTERNS = [
    # Submarine work — the entire submarine analytical scope is OUT for destroyers
    r"\bVirginia[- ]class\b",
    r"\bColumbia[- ]class\b",
    r"\bSSN[- ]?\d{3}\b",
    r"\bSSBN[- ]?\d{3}\b",
    r"\bElectric Boat\b",
    r"\bGDEB\b",
    r"\bBechtel Plant Machinery\b|\bBPMI\b",
    r"\bnaval nuclear propulsion\b",
    r"\bsubmarine\s+(?:electronic|combat|sonar|industrial|fiberglass|atmosphere|imaging|new[- ]construction|operational|electronic warfare)\b",
    r"\bNewport News Shipbuilding\b.{0,80}(?:submarine|SSN|SSBN|carrier)",
    r"submarine.+(?:Bechtel|Lockheed|Newport News|naval nuclear)",
    r"\bRolls[- ]Royce\b.+(?:submarine|nuclear propulsion)",
    r"\bAcoustic Device Countermeasures\b",
    r"\bIntegrated Submarine Imaging\b",
    r"\bSubmarine Combat System\b",
    r"\bAN/BLQ\b|\bAN/BYG\b|\bBLQ-10\b|\bBYG-1\b",  # Sub-specific electronics
    r"\bTrident\b",  # SSBN missile, sub-only
    r"\bSAFE-AND-ARM Generation\b",  # Trident
    r"\bSouth Yorkshire\b",  # Rolls-Royce sub-propulsion UK facility
    # Carriers
    r"\bCVN[- ]?\d{1,3}\b",
    r"\baircraft carrier\b",
    r"\bRCOH\b|\brefueling\s+and\s+complex\s+overhaul\b",
    r"\bFord[- ]class\b",
    r"\bNimitz[- ]class\b",
    # LCS / LCAC / frigates
    r"\bLittoral Combat Ship\b|\bLCS\b",
    r"\bLanding Craft, Air Cushion\b|\bLCAC\b|\bSSC\s+\d+\b|\bShip to Shore Connector\b",
    r"\bPolar Security Cutter\b|\bicebreaker\b",
    r"\bCoast Guard\b",
    r"\bConstellation[- ]class\b|\bConstellation[- ]Class\b",
    r"\b(?:F|FFG)[- ]?\d{2,3}\b",  # frigate hull numbers
    r"\bUSV\b|\bUnmanned Surface Vessel\b|\bunmanned surface vessels\b",
    # Amphibs / oilers
    r"\bLHA[- ]?\d+\b|\bLPD[- ]?\d+\b",
    r"\bamphibious\b",
    r"\bWasp[- ]class\b|\bSan Antonio[- ]class\b",
    r"\bT-AO[- ]?\d*\b|\boiler\b",
    r"\bLanding Helicopter Assault\b",
    r"\bexpeditionary\s+(?:sea\s+base|transfer)\b",
    # DDG-1000 Zumwalt (out of project scope per MANIFEST.md 2026-05-23 direction)
    r"\bDDG[- ]?100[0-9]\b",
    r"\bZumwalt[- ]class\b",
    # Aircraft / airborne ASW
    r"\bP-8A\b|\bP-8\b|\bMaritime Patrol\b",
    r"\bairborne anti-submarine warfare\b",
    r"\bAviation Systems Engineering\b",
    r"\bH-60\b|\bMH-60\b|\bSH-60\b",
    # Surface cruisers (Ticonderoga) — out of DDG scope
    r"\bTiconderoga[- ]class\b|\bCG[- ]?\d{2,3}\b",
    # Naval shipyard infrastructure unrelated to DDG construction
    r"\bsingle[- ]occupancy efficiency lodging\b",
    r"\bemergency ship salvage\b",
    r"\bFloating Drydock\b.+\bcontractor[- ]operated\b",
    # Surface combat sub-tier programs not exclusively DDG
    r"\bRGM-\d+\b",
    r"\bAN/SRQ-4\b|\bHawklink\b",  # surface combatants generally
    r"\bAN/SPS-73\b|\bSurface Search Radar\b",
    r"\bcombat systems engineering\b.+\bRoyal Navy ships\b",
    # University R&D labs unrelated to specific shipbuilding
    r"\bApplied Physics Laboratory\b.+University of Washington\b",
    r"\bApplied Research Lab(?:oratory)?\b.+University of Texas\b",
    # Generic cross-program research
    r"\bthroughout the (?:Department of (?:War|Defense)|DOD|DOW)\b",
    # Small boats / craft
    r"\bsmall (?:rigid hull|inflatable) boat\b|\bRIB\b|\b(?:rigid|combatant) craft\b",
    # MK weapon mounts that are non-DDG-only
    r"\bMK 6 Ammunition Hoist\b",
    # Foreign Royal Navy / FMS work (where the foreign partner is the customer)
    r"\bRoyal Navy\b",
    r"\bgovernment of (?:Germany|Japan|Korea|UK|United Kingdom|Australia)\b",
    r"\bForeign Military Financing\b",
    r"\bRepublic of (?:Korea|Japan|Australia)\b",
]
HARD_DROP_RX = [re.compile(p, re.I) for p in HARD_DROP_PATTERNS]

# ---- Strong DESTROYER-RELEVANT markers (reclassification) ----
# Each entry: (regex, program_refined, ddg_relevance, work_type_override or None)
DDG_RECLASS_RULES = [
    # GD-BIW construction of DDG-51 hull
    (re.compile(r"\bBath Iron Works\b.+(?:DDG|destroyer|Arleigh Burke)", re.I | re.S),
     "ddg51", "yes_new_construction", "construction"),
    (re.compile(r"\bGeneral Dynamics.+Bath Iron Works\b", re.I | re.S),
     "ddg51", "yes_new_construction", "construction"),
    # HII-Ingalls construction of DDG-51 hull
    (re.compile(r"\bIngalls Shipbuilding\b.+(?:DDG|destroyer|Arleigh Burke)", re.I | re.S),
     "ddg51", "yes_new_construction", "construction"),
    (re.compile(r"\bHuntington Ingalls Incorporated\b.+(?:Pascagoula|Ingalls|DDG|destroyer)", re.I | re.S),
     "ddg51", "yes_new_construction", "construction"),
    (re.compile(r"\bPascagoula\b.+(?:DDG|destroyer|Arleigh Burke)", re.I | re.S),
     "ddg51", "yes_new_construction", "construction"),
    # DDG hull-number explicit
    (re.compile(r"\bDDG\s*1[2-6]\d\b", re.I),  # DDG 120-169 series — recent / planned
     "ddg51", "yes_new_construction", None),
    # Lockheed Martin Aegis Combat System
    (re.compile(r"\bLockheed Martin\b.+(?:Aegis|combat system|combat ship|Moorestown)", re.I | re.S),
     "ddg_gfe_aegis", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bAegis\s+(?:Weapon System|Combat System|Baseline|Modernization|software|element)", re.I),
     "ddg_gfe_aegis", "yes_supplier_or_gfe", "component_procurement"),
    # Raytheon SPY-6 / AMDR / Air-Missile-Defense radar
    (re.compile(r"\bRaytheon\b.+(?:SPY[- ]?6|AMDR|Air and Missile Defense Radar)", re.I | re.S),
     "ddg_gfe_radar", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bAN/SPY[- ]?6\b|\bAir and Missile Defense Radar\b", re.I),
     "ddg_gfe_radar", "yes_supplier_or_gfe", "component_procurement"),
    # NG AN/SPQ-9B
    (re.compile(r"\bAN/SPQ[- ]?9B?\b", re.I),
     "ddg_gfe_radar", "yes_supplier_or_gfe", "component_procurement"),
    # GE LM2500 gas turbine
    (re.compile(r"\b(?:General Electric|GE Aviation|GE Aerospace)\b.+(?:LM2500|gas turbine|engine)", re.I | re.S),
     "ddg_gfe_propulsion", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bLM2500\b", re.I),
     "ddg_gfe_propulsion", "yes_supplier_or_gfe", "component_procurement"),
    # BAE 5-inch gun (Mk 45) / Mk 38 25mm / Mk 110 57mm
    (re.compile(r"\bBAE Systems\b.+(?:Mk[- ]?45|Mk[- ]?38|Mk[- ]?110|5[- ]?inch|gun mount)", re.I | re.S),
     "ddg_gfe_guns", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bMk[- ]?45\s*(?:Mod|gun)", re.I),
     "ddg_gfe_guns", "yes_supplier_or_gfe", "component_procurement"),
    # Mk 41 VLS launcher / canister assemblies
    (re.compile(r"\bMk[- ]?41\b.+(?:launcher|VLS|canister|launching\s+system)", re.I | re.S),
     "ddg_gfe_vls", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bMk\s*(?:21|25)\s*Mod\s*\d+\s+(?:canister|launch)", re.I),
     "ddg_gfe_vls", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bVertical Launching System\b", re.I),
     "ddg_gfe_vls", "yes_supplier_or_gfe", "component_procurement"),
    # L3Harris CEC
    (re.compile(r"\bAN/USG[- ]?[23]B?\b|\bCooperative Engagement Capability\b", re.I),
     "ddg_gfe_combat_systems", "yes_supplier_or_gfe", "component_procurement"),
    # Standard Missile / ESSM / Tomahawk / CIWS — weapons (typically WPN not SCN)
    (re.compile(r"\b(?:Standard Missile|SM[- ]?[23]|SM[- ]?6)\b", re.I),
     "ddg_gfe_weapons", "borderline", None),
    (re.compile(r"\b(?:Evolved Sea[Ss]parrow|ESSM|SeaSparrow)\b", re.I),
     "ddg_gfe_weapons", "borderline", None),
    (re.compile(r"\bTomahawk\b", re.I),
     "ddg_gfe_weapons", "borderline", None),
    (re.compile(r"\b(?:Close[- ]In Weapon System|CIWS|Phalanx|SeaRAM|Rolling Airframe Missile)\b", re.I),
     "ddg_gfe_weapons", "borderline", None),
    # DDG sustainment / depot maintenance (NOT new construction)
    (re.compile(r"\b(?:DSRA|EDSRA|SRA|Docking Selected Restricted Availability)\b.+(?:DDG|destroyer|Arleigh Burke)", re.I | re.S),
     "ddg_repair", "yes_sustainment", "repair_overhaul"),
    (re.compile(r"\b(?:DDG|destroyer)\b.+(?:DSRA|EDSRA|SRA|availability|overhaul|maintenance)", re.I | re.S),
     "ddg_repair", "yes_sustainment", "repair_overhaul"),
    (re.compile(r"\b(?:Arleigh Burke|DDG).+(?:depot|drydock)", re.I | re.S),
     "ddg_repair", "yes_sustainment", "repair_overhaul"),
    # DDG planning yard / design agent for in-service ships
    (re.compile(r"\b(?:planning yard|design agent)\b.+(?:DDG|destroyer)", re.I | re.S),
     "ddg_repair", "yes_sustainment", "lead_yard"),
    (re.compile(r"\b(?:DDG|destroyer)\b.+(?:planning yard|design agent)", re.I | re.S),
     "ddg_repair", "yes_sustainment", "lead_yard"),
]

TAM_RELEVANT_WORKTYPES = {
    "construction",
    "lltm_early_mfg",
    "advance_procurement",
    "eoq",
    "component_procurement",
}
TAM_RELEVANT_PROGRAMS = {
    "ddg51",
    "ddg_gfe_aegis", "ddg_gfe_radar", "ddg_gfe_propulsion",
    "ddg_gfe_guns", "ddg_gfe_vls", "ddg_gfe_combat_systems",
}


def reclassify_row(r):
    """Returns (program_refined, ddg_relevance, work_type_override_or_None)."""
    text = r["paragraph_text"]
    # First check hard-drop
    if any(rx.search(text) for rx in HARD_DROP_RX):
        return ("non_ddg", "no", None)
    # Check ddg-reclassification rules in order
    for rx, prog, relevance, wt in DDG_RECLASS_RULES:
        if rx.search(text):
            return (prog, relevance, wt)
    # If first-pass already tagged as a DDG family, keep
    if r["program_primary"] in TAM_RELEVANT_PROGRAMS:
        return (r["program_primary"], "yes_new_construction", None)
    if r["program_primary"] == "ddg_gfe_weapons":
        return ("ddg_gfe_weapons", "borderline", None)
    if r["program_primary"] == "ddg_repair":
        return ("ddg_repair", "yes_sustainment", None)
    # Otherwise — non-destroyer; drop
    return ("non_ddg", "no", None)


def main():
    with open(IN_CSV) as f:
        rows = list(csv.DictReader(f))

    overrides = {"dropped_non_ddg": 0, "reclassed_to_ddg_relevant": 0,
                 "kept_ddg_already": 0, "sustainment_or_borderline": 0}

    for r in rows:
        prog_refined, relevance, wt_over = reclassify_row(r)
        r["program_refined"] = prog_refined
        r["ddg_relevance"] = relevance
        if wt_over:
            r["work_type_primary"] = wt_over
        # Recompute TAM gate
        r["is_ddg_new_construction_tam"] = (
            "yes"
            if prog_refined in TAM_RELEVANT_PROGRAMS
                and r["work_type_primary"] in TAM_RELEVANT_WORKTYPES
                and relevance in ("yes_new_construction", "yes_supplier_or_gfe")
            else "no"
        )
        if prog_refined == "non_ddg":
            overrides["dropped_non_ddg"] += 1
        elif r["program_primary"] in ("unknown",) and prog_refined != r["program_primary"]:
            overrides["reclassed_to_ddg_relevant"] += 1
        elif r["program_primary"] in TAM_RELEVANT_PROGRAMS:
            overrides["kept_ddg_already"] += 1
        elif relevance in ("yes_sustainment", "borderline"):
            overrides["sustainment_or_borderline"] += 1

    print(f"Reclassification stats:")
    for k, v in overrides.items():
        print(f"  {k}: {v}")

    # Rewrite CSV with new columns
    fields = list(rows[0].keys())
    for ex in ("program_refined", "ddg_relevance"):
        if ex not in fields:
            fields.append(ex)
    with open(IN_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

    def _f2(v):
        try: return float(v)
        except (ValueError, TypeError): return 0.0
    # Rebuild rollup
    buckets = defaultdict(lambda: {"n": 0, "total": 0.0, "biw": 0.0, "ingalls": 0.0,
                                    "other_us": 0.0, "foreign": 0.0})
    for r in rows:
        amt = _f2(r["amount_usd"])
        if amt <= 0:
            continue
        key = (r["program_refined"], r["work_type_primary"])
        b = buckets[key]
        b["n"] += 1
        b["total"] += amt
        b["biw"] += amt * _f2(r["pop_biw_site_pct"])
        b["ingalls"] += amt * _f2(r["pop_ingalls_site_pct"])
        b["other_us"] += amt * _f2(r["pop_other_us_pct"])
        b["foreign"] += amt * _f2(r["pop_foreign_pct"])

    with open(OUT_ROLLUP, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "program_refined", "work_type_primary",
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
    prog_n = Counter(r["program_refined"] for r in rows)
    prog_d = Counter()
    for r in rows:
        prog_d[r["program_refined"]] += float(r["amount_usd"]) if r["amount_usd"] else 0
    print(f"\n=== refined program family distribution ===")
    for p in sorted(prog_n, key=lambda k: -prog_d[k]):
        print(f"  {p:<24}  {prog_n[p]:>4} rows  ${prog_d[p]/1e6:>11,.1f}M")

    def _f(v):
        try: return float(v)
        except (ValueError, TypeError): return 0.0
    tam_rows = [r for r in rows if r["is_ddg_new_construction_tam"] == "yes"]
    tam_total = sum(_f(r["amount_usd"]) for r in tam_rows)
    print(f"\n=== DDG-construction supplier-TAM-relevant actions (refined gate) ===")
    print(f"  {len(tam_rows)} rows, ${tam_total/1e6:,.1f}M total")
    if tam_rows and tam_total > 0:
        biw = sum(_f(r["amount_usd"]) * _f(r["pop_biw_site_pct"]) for r in tam_rows) / tam_total
        ing = sum(_f(r["amount_usd"]) * _f(r["pop_ingalls_site_pct"]) for r in tam_rows) / tam_total
        oth = sum(_f(r["amount_usd"]) * _f(r["pop_other_us_pct"]) for r in tam_rows) / tam_total
        for_ = sum(_f(r["amount_usd"]) * _f(r["pop_foreign_pct"]) for r in tam_rows) / tam_total
        print(f"  $-weighted POP: BIW {biw:.1f}% | Ingalls {ing:.1f}% | Other-US {oth:.1f}% | Foreign {for_:.1f}%")

    # Per-bucket detail for TAM-relevant
    print(f"\n=== TAM-relevant per-bucket POP ===")
    print(f"{'program':<24} {'work_type':<24} {'N':>3} {'$M':>10} {'BIW%':>6} {'Ing%':>6} {'Other%':>7}")
    with open(OUT_ROLLUP) as f:
        for r in csv.DictReader(f):
            if r["program_refined"] in TAM_RELEVANT_PROGRAMS and r["work_type_primary"] in TAM_RELEVANT_WORKTYPES:
                print(f"  {r['program_refined']:<22} {r['work_type_primary']:<24} {r['n_actions']:>3} "
                      f"{float(r['total_dollars_usd'])/1e6:>10.1f} {r['pop_biw_pct_w']:>6} {r['pop_ingalls_pct_w']:>6} {r['pop_other_us_pct_w']:>7}")


if __name__ == "__main__":
    main()
