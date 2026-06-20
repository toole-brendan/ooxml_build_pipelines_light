#!/usr/bin/env python3
"""
Second-pass classifier for extracted/dod_announcement_pop.csv.

The first-pass classifier (classify_dod_action_worktype.py) was based on
mechanical regex over the original loose-filter pull. After reading the
text of all 273 'unknown'+'sub_other' rows, I'm applying tightened
judgment rules:

  - HARD DROP rows that are clearly NOT submarine work:
      surface missiles / radars (SM-2/3/6, SeaSparrow, SPY-6, SEWIP, AEGIS,
      Patriot, Tomahawk, RAM, Standard Missile, MK 41, MK 45, MK 53/54)
      surface combatants (DDG, Arleigh Burke, Zumwalt, frigate, Ticonderoga,
      LCS, LCAC, Landing Craft, Polar Security Cutter, Coast Guard)
      amphibs / oilers / LPDs / LHAs / T-AO
      aircraft / airborne (P-8A anti-sub, mine detection, helo programs)
      carriers (CVN, Ford-class, Nimitz, RCOH)
      escort / auxiliary (T-AGSE, naval shipyard lodging)
      surface combat systems sustainment (River Class Destroyer)

  - PROMOTE sub-relevant rows to specific tags:
      BPMI / Bechtel Plant Machinery Inc. → bpmi_nuclear (sub GFE)
      Lockheed Submarine Imaging / BLQ-10 EW / new-construction sub
        electronics → sub_gfe_electronics
      Sub-specific components (fiberglass, atmosphere monitor, Acoustic
        Device Countermeasures, etc.) → sub_gfe_components
      Sub operational / sustainment (planning yard, drydock, in-service
        sub valves) → sub_sustainment (not new construction)

  - sub_relevance final tag: yes_new_construction | yes_sustainment |
        yes_supplier_or_gfe | no | borderline

  - is_sub_new_construction_tam recomputed: yes only if program in
        {va, col, va_or_col, bpmi_nuclear, sub_gfe_electronics,
         sub_gfe_components} AND work_type in TAM_RELEVANT
        AND sub_relevance in {yes_new_construction, yes_supplier_or_gfe}.

Outputs: rewrites extracted/dod_announcement_pop.csv with two new columns
appended (sub_relevance, program_refined). Rebuilds rollup.
"""
import csv
import os
import re
from collections import defaultdict
from pathlib import Path

IN_CSV = Path("/Users/brendantoole/projects2/submarine_outsourced_work/extracted/dod_announcement_pop.csv")
OUT_ROLLUP = Path("/Users/brendantoole/projects2/submarine_outsourced_work/extracted/dod_action_pop_by_worktype.csv")

# ---- Strong NOT-SUBMARINE markers — if any match, drop ----
HARD_DROP_PATTERNS = [
    # Surface combat systems / missiles / radars
    r"\bStandard Missile\b",
    r"\bSM[- ]?[2-9]\b",
    r"\bSeaSparrow\b|\bSEASPARROW\b|\bEvolved\s+Sea[Ss]parrow\b",
    r"\bSPY[- ]?\d+\b|\bAN/SPY-6\b",
    r"\bSEWIP\b|\bSurface Electronic Warfare\b",
    r"\bAEGIS\b",
    r"\bMK\s*4[15]\b|\bMK\s*5[34]\b|\bMK\s*46\b|\bMK\s*48\b",
    r"\bClose-In Weapon System\b|\bCIWS\b|\bMK\s*15\b",
    r"\bTomahawk\b",
    r"\bRolling Airframe Missile\b|\bSeaRAM\b|\bNATO Sea[Ss]parrow\b",
    r"\bPatriot\b",
    r"\bRiver[- ]Class Destroyer\b|\bRiver Class Destroyer\b",
    r"\bAir(?:borne)?\s+(?:Laser\s+)?Mine\s+(?:Detection|Neutralization)\b",
    r"\bUnmanned Surface Vessel\b|\bunmanned surface vessels\b",
    # Surface ships
    r"\bDDG[- ]?\d{1,3}\b|\bArleigh Burke[- ]class\b|\bguided[- ]missile destroyer\b",
    r"\bZumwalt[- ]class\b",
    r"\bTiconderoga[- ]class\b",
    r"\bLittoral Combat Ship\b|\bLCS\b",
    r"\bLanding Craft, Air Cushion\b|\bLCAC\b|\bSSC\s+\d+\b|\bShip to Shore Connector\b",
    r"\bPolar Security Cutter\b|\bicebreaker\b",
    r"\bCoast Guard\b",
    r"\bfrigate\b|\bConstellation[- ]class\b",
    r"\bWaterborne Security Barrier\b|\bsecurity barrier\b",
    # Amphibs
    r"\bLHA[- ]?\d+\b|\bLPD[- ]?\d+\b|\bamphibious\b|\bWasp[- ]class\b|\bSan Antonio[- ]class\b",
    r"\bT-AO[- ]?\d*\b|\boiler\b|\bConstellation\b|\bexpeditionary\b",
    r"\bLanding Helicopter Assault\b",
    # Aircraft / airborne / hunting subs
    r"\bP-8A\b|\bP-8\b|\bMaritime Patrol\b",
    r"\bairborne anti-submarine warfare\b",  # planes hunting subs ≠ submarine work
    r"\bAviation Systems Engineering\b",
    # Carriers
    r"\bCVN[- ]?\d{1,3}\b|\baircraft carrier\b|\bRCOH\b|\bFord[- ]class\b|\bNimitz[- ]class\b",
    # Escort / facilities / lodging
    r"\bT-AGSE\b|\bTransportation Auxiliary General Submarine Escort\b",
    r"\bsingle[- ]occupancy efficiency lodging\b",  # naval shipyard temp lodging
    r"\bemergency ship salvage\b",
    # Surface combat sub-tier programs
    r"\bRGM-\d+\b",
    r"\bAN/SRQ-4\b|\bRadio Terminal Set Common Data Link Hawklink\b",  # surface combatants
    r"\bAN/SPS-73\b|\bSurface Search Radar\b",
    r"\bShip Self-Defense System\b",
    r"\bcombat systems engineering\b.+\bRoyal Navy ships\b",  # Canadian Royal Navy work
    # University R&D labs supporting cross-DOD work (not sub-specific)
    r"\bApplied Physics Laboratory\b.+University of Washington\b",
    r"\bApplied Research Lab(?:oratory)?\b.+University of Texas\b",
    # Generic cross-program research
    r"\bthroughout the (?:Department of (?:War|Defense)|DOD|DOW)\b",
    # Boats / small craft
    r"\bsmall (?:rigid hull|inflatable) boat\b|\bRIB\b|\b(?:rigid|combatant) craft\b",
    # MK weapon mounts / gun systems
    r"\bMK 45[- ]gun mount\b|\bgun mount\b",
    r"\bMK 6 Ammunition Hoist\b",
    r"\bVertical Launching System\b|\bVLS\b",
    # Generic non-sub Navy modernization
    r"\bArleigh Burke\b",
    r"\bOver[- ]The[- ]Horizon Weapon\b",
    r"\bUSV\b|\bunmanned surface\b",
    # Foreign military work (where the foreign partner is the customer)
    r"\bRoyal Navy\b|\bgovernment of (?:Germany|Japan|Canada|Australia|Korea|UK|United Kingdom)\b",
    r"\bForeign Military Financing\b",
    # Misc
    r"\bFloating Drydock\b.+\bcontractor[- ]operated\b",
]
HARD_DROP_RX = [re.compile(p, re.I) for p in HARD_DROP_PATTERNS]

# ---- Strong SUBMARINE-RELEVANT markers (reclassification) ----
# Each entry: (regex, program_refined, sub_relevance, work_type_override or None)
SUB_RECLASS_RULES = [
    # BPMI / nuclear propulsion components — sub GFE, biggest single GFE line
    (re.compile(r"\bBechtel Plant Machinery Inc\.?\b.+naval nuclear propulsion components?\b", re.I | re.S),
     "bpmi_nuclear", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bBPMI\b.+naval nuclear\b", re.I | re.S),
     "bpmi_nuclear", "yes_supplier_or_gfe", "component_procurement"),
    # Submarine electronic warfare GFE (Lockheed BLQ-10, AN/BLQ-10)
    (re.compile(r"submarine\s+electronic\s+warfare\s+systems.+new[- ]construction", re.I | re.S),
     "sub_gfe_electronics", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bAN/BLQ[- ]?10\b", re.I),
     "sub_gfe_electronics", "yes_supplier_or_gfe", "component_procurement"),
    # Submarine sonar / imaging GFE
    (re.compile(r"Integrated Submarine Imaging System.+new[- ]construction", re.I | re.S),
     "sub_gfe_electronics", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"\bSound Navigation and Ranging\b.+submarine|submarine.+\bSONAR\b", re.I | re.S),
     "sub_gfe_electronics", "yes_supplier_or_gfe", "engineering"),
    # Sub-specific components (fiberglass, atmosphere monitor, ADCs)
    (re.compile(r"submarine fiberglass fabrication", re.I),
     "sub_gfe_components", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"atmosphere monitor.+submarine|Spectroscopic Total Air Monitor.+submarine", re.I | re.S),
     "sub_gfe_components", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"Acoustic Device Countermeasures.+submarine", re.I | re.S),
     "sub_gfe_components", "yes_supplier_or_gfe", "component_procurement"),
    (re.compile(r"Common Infrastructure Services.+submarine", re.I | re.S),
     "sub_gfe_electronics", "yes_supplier_or_gfe", "engineering"),
    # Sub repair / sustainment (NOT new construction)
    (re.compile(r"\brepair, maintenance, and modernization of nuclear[- ]powered.+submarine", re.I | re.S),
     "sub_repair", "yes_sustainment", "repair_overhaul"),
    (re.compile(r"planning and design yard activities for standard navy valves.+submarine", re.I | re.S),
     "sub_repair", "yes_sustainment", "design"),
    (re.compile(r"design agent, and planning yard support for operational.+submarine", re.I | re.S),
     "sub_operational", "yes_sustainment", "lead_yard"),
    (re.compile(r"floating dry dock.+Shippingport", re.I | re.S),
     "sub_repair", "yes_sustainment", "repair_overhaul"),
    (re.compile(r"Docking Selected Restricted Availability.+Los Angeles[- ]class submarine", re.I | re.S),
     "sub_repair", "yes_sustainment", "repair_overhaul"),
    # Undersea warfare combat systems (Metron, surface AND sub) — borderline; flag
    (re.compile(r"Undersea Warfare.+(Surface Ship and )?Submarine systems", re.I | re.S),
     "sub_gfe_electronics", "borderline", "engineering"),
]

TAM_RELEVANT_WORKTYPES = {
    "construction",
    "lltm_early_mfg",
    "advance_procurement",
    "eoq",
    "component_procurement",
}
TAM_RELEVANT_PROGRAMS = {
    "va", "col", "va_or_col",
    "bpmi_nuclear", "sub_gfe_electronics", "sub_gfe_components",
}


def reclassify_row(r):
    """Returns (program_refined, sub_relevance, work_type_override_or_None)."""
    text = r["paragraph_text"]
    # First check hard-drop
    if any(rx.search(text) for rx in HARD_DROP_RX):
        return ("non_sub", "no", None)
    # Check sub-reclassification rules in order
    for rx, prog, relevance, wt in SUB_RECLASS_RULES:
        if rx.search(text):
            return (prog, relevance, wt)
    # If it's already va/col, keep
    if r["program_primary"] in ("va", "col", "va_or_col"):
        return (r["program_primary"], "yes_new_construction", None)
    # Default: leave as-is but mark borderline if sub_other
    if r["program_primary"] == "sub_other":
        return ("sub_other", "borderline", None)
    # Otherwise it's unknown and unmatched — assume non-sub
    return ("non_sub", "no", None)


def main():
    with open(IN_CSV) as f:
        rows = list(csv.DictReader(f))

    overrides = {"dropped_non_sub": 0, "reclassed_to_sub_relevant": 0,
                 "kept_sub_already": 0, "sustainment_or_borderline": 0}

    for r in rows:
        prog_refined, relevance, wt_over = reclassify_row(r)
        r["program_refined"] = prog_refined
        r["sub_relevance"] = relevance
        if wt_over:
            r["work_type_primary"] = wt_over
        # Recompute TAM gate
        r["is_sub_new_construction_tam"] = (
            "yes"
            if prog_refined in TAM_RELEVANT_PROGRAMS
                and r["work_type_primary"] in TAM_RELEVANT_WORKTYPES
                and relevance in ("yes_new_construction", "yes_supplier_or_gfe")
            else "no"
        )
        if prog_refined == "non_sub":
            overrides["dropped_non_sub"] += 1
        elif r["program_primary"] in ("unknown", "sub_other") and prog_refined != r["program_primary"]:
            overrides["reclassed_to_sub_relevant"] += 1
        elif r["program_primary"] in ("va","col","va_or_col"):
            overrides["kept_sub_already"] += 1
        elif relevance in ("yes_sustainment", "borderline"):
            overrides["sustainment_or_borderline"] += 1

    print(f"Reclassification stats:")
    for k, v in overrides.items():
        print(f"  {k}: {v}")

    # Rewrite CSV with new columns
    fields = list(rows[0].keys())
    for ex in ("program_refined", "sub_relevance"):
        if ex not in fields:
            fields.append(ex)
    with open(IN_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

    # Rebuild rollup
    buckets = defaultdict(lambda: {"n": 0, "total": 0.0, "eb": 0.0, "hii": 0.0,
                                    "other_us": 0.0, "foreign": 0.0})
    for r in rows:
        amt = float(r["amount_usd"]) if r["amount_usd"] else 0.0
        if amt <= 0:
            continue
        key = (r["program_refined"], r["work_type_primary"])
        b = buckets[key]
        b["n"] += 1
        b["total"] += amt
        b["eb"] += amt * float(r["pop_eb_site_pct"])
        b["hii"] += amt * float(r["pop_hii_site_pct"])
        b["other_us"] += amt * float(r["pop_other_us_pct"])
        b["foreign"] += amt * float(r["pop_foreign_pct"])

    with open(OUT_ROLLUP, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([
            "program_refined", "work_type_primary",
            "n_actions", "total_dollars_usd",
            "pop_eb_pct_w", "pop_hii_pct_w", "pop_other_us_pct_w", "pop_foreign_pct_w",
        ])
        for (prog, wt) in sorted(buckets, key=lambda k: -buckets[k]["total"]):
            b = buckets[(prog, wt)]
            tot = b["total"] or 1
            w.writerow([
                prog, wt, b["n"], round(b["total"], 2),
                round(b["eb"] / tot, 2),
                round(b["hii"] / tot, 2),
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
        print(f"  {p:<22}  {prog_n[p]:>4} rows  ${prog_d[p]/1e6:>11,.1f}M")

    tam_rows = [r for r in rows if r["is_sub_new_construction_tam"] == "yes"]
    tam_total = sum(float(r["amount_usd"]) if r["amount_usd"] else 0 for r in tam_rows)
    print(f"\n=== Sub-construction supplier-TAM-relevant actions (refined gate) ===")
    print(f"  {len(tam_rows)} rows, ${tam_total/1e6:,.1f}M total")
    if tam_rows and tam_total > 0:
        eb = sum((float(r["amount_usd"]) or 0) * float(r["pop_eb_site_pct"]) for r in tam_rows) / tam_total
        hii = sum((float(r["amount_usd"]) or 0) * float(r["pop_hii_site_pct"]) for r in tam_rows) / tam_total
        oth = sum((float(r["amount_usd"]) or 0) * float(r["pop_other_us_pct"]) for r in tam_rows) / tam_total
        for_ = sum((float(r["amount_usd"]) or 0) * float(r["pop_foreign_pct"]) for r in tam_rows) / tam_total
        print(f"  $-weighted POP: EB {eb:.1f}% | HII {hii:.1f}% | Other-US {oth:.1f}% | Foreign {for_:.1f}%")

    # Per-bucket detail for TAM-relevant
    print(f"\n=== TAM-relevant per-bucket POP ===")
    print(f"{'program':<24} {'work_type':<24} {'N':>3} {'$M':>10} {'EB%':>6} {'HII%':>6} {'Other%':>7}")
    with open(OUT_ROLLUP) as f:
        for r in csv.DictReader(f):
            if r["program_refined"] in TAM_RELEVANT_PROGRAMS and r["work_type_primary"] in TAM_RELEVANT_WORKTYPES:
                print(f"  {r['program_refined']:<22} {r['work_type_primary']:<24} {r['n_actions']:>3} "
                      f"{float(r['total_dollars_usd'])/1e6:>10.1f} {r['pop_eb_pct_w']:>6} {r['pop_hii_pct_w']:>6} {r['pop_other_us_pct_w']:>7}")


if __name__ == "__main__":
    main()
