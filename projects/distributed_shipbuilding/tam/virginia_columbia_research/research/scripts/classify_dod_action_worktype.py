#!/usr/bin/env python3
"""
Classify DoD daily-contract actions (from extracted/dod_announcement_pop.csv)
along two axes:

  1. PROGRAM FAMILY — which weapons system the action is for:
        va, col, va_or_col (multi), sub_other, cvn, ddg, lcs, missile_weapons,
        surface_other, unknown

  2. WORK TYPE — what kind of work the action covers (multi-label):
        construction, lltm_early_mfg, advance_procurement, eoq,
        component_procurement, lead_yard, design, sustainment_maintenance,
        sib_supplier_dev, facilities, repair_overhaul, fms, engineering,
        other

The original 389-row pull was filtered loosely (any paragraph mentioning
Electric Boat / submarine / N00024 PIID), so many rows are not actually
submarine new-construction. This script reclassifies to enable the
framework-style per-bucket POP analysis.

Outputs:
  - extracted/dod_announcement_pop.csv (in place: 4 new columns appended)
  - extracted/dod_action_pop_by_worktype.csv  ($-weighted POP shares per
        (program_family, work_type_primary) bucket)
"""
import csv
import os
import re
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/submarine_outsourced_work")
IN_CSV = REPO / "extracted" / "dod_announcement_pop.csv"
OUT_ROLLUP = REPO / "extracted" / "dod_action_pop_by_worktype.csv"

# ---- Program family rules (order matters; first match wins for primary,
#      but we record all matches in program_all) ----

PROGRAM_RULES = [
    ("va", [
        r"\bVirginia[- ]class\b",
        r"\bVCS\b",
        r"\bVa\s+Block\b",
        r"\bBlock\s+(?:IV|V|VI)\s+(?:Virginia|Va\b)",
        r"\bBlock\s+(?:IV|V|VI)\b.{0,80}Virginia",
        r"Virginia.{0,40}Block\s+(?:IV|V|VI)",
        r"\bSSN[- ]?\d{3}\b",  # SSN 812 etc. — almost always Va-class new construction
    ]),
    ("col", [
        r"\bColumbia[- ]class\b",
        r"\bCol\s+Build\b",
        r"\bSSBN[- ]?\d{3}\b",
        r"\bCommon Missile Compartment\b",
        r"\bCMC\b",
    ]),
    ("cvn", [
        r"\bCVN[- ]?\d{2,3}\b",
        r"\baircraft carrier\b",
        r"\bRCOH\b",
        r"\bFord[- ]class\b",
        r"\bNimitz[- ]class\b",
    ]),
    ("ddg", [
        r"\bDDG[- ]?\d{2,3}\b",
        r"\bArleigh Burke[- ]class\b",
        r"\bguided[- ]missile destroyer\b",
    ]),
    ("lcs", [
        r"\bLCS\b",
        r"\bLittoral Combat Ship\b",
    ]),
    ("missile_weapons", [
        r"\bStandard Missile\b",
        r"\bSM[- ]?[23456]\b",
        r"\bRolling Airframe Missile\b",
        r"\bRAM\b(?!.+missile)?",
        r"\bTomahawk\b",
        r"\bTrident\b",
        r"\bPatriot\b",
        r"\bRGM[- ]\d+\b",
    ]),
    ("surface_other", [
        r"\bLHA[- ]?\d+\b",
        r"\bLPD[- ]?\d+\b",
        r"\bamphibious\b",
        r"\bWasp[- ]class\b",
        r"\bSan Antonio[- ]class\b",
        r"\bT-AO\b",
        r"\boiler\b",
        r"\bexpeditionary\b",
        r"\bConstellation[- ]class\b",
        r"\bfrigate\b",
    ]),
    ("sub_other", [
        # mentions sub/EB/Newport News subs but no specific class
        r"\bsubmarine[s]?\b",
        r"\bElectric Boat\b",
        r"\bGDEB\b",
        r"\bNewport News Shipbuilding.{0,80}submarine\b",
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
        r"submarine\s+construction",
        r"\bconstruction\s+of\s+(?:the\s+|a\s+|an\s+|\d+\s+)",
        r"new\s+construction",
        r"\bConstruction\s+Spares\b",
        r"\bboat\s+\d\b",  # "construction boat 2 fy24" etc.
    ]),
    ("component_procurement", [
        r"\bprocurement\s+of\s+\d+\b",   # "procurement of 20 trim and drain pumps"
        r"\bshipset\s+of\b",
        r"\brepair\s+parts\b",
        r"\bspare\s+parts\b",
        r"\bnuclear\s+plant\s+(?:component|equipment)",
        r"\b(?:trim|drain)\s+(?:and\s+drain\s+)?pumps?\b",
        r"\bvalves?\b",
        r"\bforgings?\b",
        r"\bmissile\s+tubes?\b",
        r"\bgenerator\s+procurement\b",
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
    ]),
    ("sustainment_maintenance", [
        r"\bsustainment\b",
        r"\bmodernization\b",
        r"maintenance\s+(?:and\s+modernization|services)",
        r"\bavailabilit(?:y|ies)\b",
    ]),
    ("sib_supplier_dev", [
        r"submarine\s+industrial\s+base",
        r"industrial\s+base\s+(?:development|investment|supplier)",
        r"supplier\s+development",
        r"supplier\s+expansion",
        r"\bSIB\b",
        r"integrated\s+enterprise\s+plan",
        r"enterprise\s+initiatives",
        r"workforce\s+development",
    ]),
    ("facilities", [
        r"facility\s+(?:upgrade|expansion|modernization)",
        r"facilit(?:y|ies)\s+(?:work|construction)",
        r"\b(?:Pier|Drydock|Dry Dock|Building)\s+\w+\s+(?:upgrade|expansion|construction|replacement)",
        r"new\s+(?:construction|modernization)\s+of\s+(?:Pier|Drydock|Building)",
    ]),
    ("repair_overhaul", [
        r"\bRCOH\b",
        r"\bEOH\b",
        r"refueling\s+and\s+complex\s+overhaul",
        r"engineered\s+overhaul",
        r"depot\s+(?:maintenance|level)",
        r"\boverhaul\b",
        r"\bbackfit\b",
        r"\bSRA\b",  # selected restricted availability
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
    # If both va and col → flag as va_or_col multi (happens on big bundled mods)
    if "va" in hits and "col" in hits:
        primary = "va_or_col"
    else:
        # sub_other is the catchall — prefer specific class
        non_sub_other = [h for h in hits if h != "sub_other"]
        primary = non_sub_other[0] if non_sub_other else "sub_other"
    return (primary, hits)


def classify_worktype(text):
    """Return (primary_work_type, all_work_types_list, ambiguous_flag)."""
    hits = []
    for wt, patterns in WORKTYPE_RULES:
        if any(re.search(p, text, re.I) for p in patterns):
            hits.append(wt)
    if not hits:
        return ("other", [], False)
    # Primary = highest-priority match
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
        r["is_sub_new_construction_tam"] = (
            "yes"
            if prog_primary in ("va", "col", "va_or_col") and wt_primary in TAM_RELEVANT
            else "no"
        )
        new_rows.append(r)

    # Rewrite the CSV with new columns
    fields = list(rows[0].keys())
    extras = [
        "program_primary", "program_all",
        "work_type_primary", "work_type_all", "work_type_ambiguous",
        "is_sub_new_construction_tam",
    ]
    for ex in extras:
        if ex not in fields:
            fields.append(ex)
    with open(IN_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in new_rows:
            w.writerow({k: r.get(k, "") for k in fields})

    # ----- Rollup: $-weighted POP shares per (program_family, work_type_primary) bucket -----
    buckets = defaultdict(lambda: {"n": 0, "total": 0.0, "eb": 0.0, "hii": 0.0, "other_us": 0.0, "foreign": 0.0})
    for r in new_rows:
        amt = float(r["amount_usd"]) if r["amount_usd"] else 0.0
        if amt <= 0:
            continue
        key = (r["program_primary"], r["work_type_primary"])
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
            "program_family", "work_type_primary",
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
    prog_n = Counter(r["program_primary"] for r in new_rows)
    prog_d = Counter()
    for r in new_rows:
        prog_d[r["program_primary"]] += float(r["amount_usd"]) if r["amount_usd"] else 0
    print("=== program family distribution ===")
    for p in sorted(prog_n, key=lambda k: -prog_d[k]):
        print(f"  {p:<18}  {prog_n[p]:>4} rows  ${prog_d[p]/1e6:>11,.1f}M")

    wt_n = Counter(r["work_type_primary"] for r in new_rows if r["program_primary"] in ("va", "col", "va_or_col"))
    wt_d = Counter()
    for r in new_rows:
        if r["program_primary"] in ("va", "col", "va_or_col"):
            wt_d[r["work_type_primary"]] += float(r["amount_usd"]) if r["amount_usd"] else 0
    print(f"\n=== work-type breakdown — sub-program rows only ({sum(wt_n.values())} actions, ${sum(wt_d.values())/1e6:,.1f}M total) ===")
    for wt in sorted(wt_n, key=lambda k: -wt_d[k]):
        print(f"  {wt:<28}  {wt_n[wt]:>3} rows  ${wt_d[wt]/1e6:>10,.1f}M")

    print(f"\n=== sub-construction-supplier-TAM-relevant actions (yes-gate) ===")
    tam_rows = [r for r in new_rows if r["is_sub_new_construction_tam"] == "yes"]
    tam_total = sum(float(r["amount_usd"]) if r["amount_usd"] else 0 for r in tam_rows)
    print(f"  {len(tam_rows)} rows, ${tam_total/1e6:,.1f}M total")
    if tam_rows:
        eb = sum((float(r["amount_usd"]) if r["amount_usd"] else 0) * float(r["pop_eb_site_pct"]) for r in tam_rows) / tam_total
        hii = sum((float(r["amount_usd"]) if r["amount_usd"] else 0) * float(r["pop_hii_site_pct"]) for r in tam_rows) / tam_total
        oth = sum((float(r["amount_usd"]) if r["amount_usd"] else 0) * float(r["pop_other_us_pct"]) for r in tam_rows) / tam_total
        for_ = sum((float(r["amount_usd"]) if r["amount_usd"] else 0) * float(r["pop_foreign_pct"]) for r in tam_rows) / tam_total
        print(f"  $-weighted POP: EB {eb:.1f}% | HII {hii:.1f}% | Other-US {oth:.1f}% | Foreign {for_:.1f}%")

    print(f"\nWrote enriched CSV → {IN_CSV}")
    print(f"Wrote rollup → {OUT_ROLLUP}")


if __name__ == "__main__":
    main()
