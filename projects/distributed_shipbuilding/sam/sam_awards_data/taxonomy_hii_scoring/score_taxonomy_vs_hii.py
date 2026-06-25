#!/usr/bin/env python3
"""
Score agent A's NAICS-6 -> work-type taxonomy against the HII-DDG ground truth.

Implements §6 of logs/2026-06-18_taxonomy_and_vendor_registry_agent_handoff.md.

HII-Ingalls DDG subawards carry an observed SWBS ship-system group (where the work
lands on the ship). The taxonomy assigns each vendor a PROCESS category from its
primary NAICS-6. This script measures, on the HII slice only:

  1. NAICS-internal SWBS purity (taxonomy-agnostic): for each primary NAICS-6, how
     concentrated is the observed ship-system work? (modal SWBS one-digit share +
     entropy). A coherent NAICS lands its dollars in one place; a mushy one scatters.

  2. Per-category SWBS agreement (taxonomy-graded, SYSTEM categories only): of the
     HII dollars the taxonomy assigns to category C, what share land on the SWBS
     group you'd expect for C? PROCESS-ONLY categories (forgings, machining,
     coatings, electronic components, services...) are NOT SWBS-graded -- they
     legitimately scatter across ship systems; they are assessed via component_text
     coverage + NAICS-internal purity instead, and flagged 'process_not_swbs_gradable'.

  3. Low-purity flag list = the registry-research / enrichment queue: NAICS-6 codes
     with material HII dollars that either scatter (low concentration) or whose modal
     observed SWBS implies a DIFFERENT category than the taxonomy assigned.

CRITICAL CAVEATS (carried from the handoff, do not misuse the referee):
  - HII is ~13% of corpus $, one builder, one program, a SYSTEM axis. Use to
    calibrate/validate, never to redefine categories.
  - Process != system. Only system-ish categories align with SWBS. Do not penalize
    castings/forgings/machining/coatings for SWBS "mismatch".
"""
import csv, math, collections, os

CB   = "/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/distributed_shipbuilding/sam/sam_awards_data/taxonomy_design_input_canonical"
TAX  = "/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/distributed_shipbuilding/sam/sam_awards_data/taxonomy_design_output"
OUT  = "/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/distributed_shipbuilding/sam/sam_awards_data/taxonomy_hii_scoring"

# ---------------------------------------------------------------- load taxonomy
# category_id -> name
catname = {}
for r in csv.DictReader(open(f"{TAX}/navy_work_type_schema.csv", encoding="utf-8-sig")):
    catname[r["category_id"].strip()] = r["category"].strip()
catname.setdefault("99", "Unresolved capability / insufficient evidence")

# primary NAICS-6 -> taxonomy category_id (the baseline NAICS map we are grading)
naics2cat = {}
for r in csv.DictReader(open(f"{TAX}/navy_all_observed_naics_crosswalk.csv", encoding="utf-8-sig")):
    naics2cat[r["naics6"].strip()] = r["category_id"].strip()

# ---------------------------------------------------------------- vendor -> primary NAICS / category
uei_primary_naics, uei_name = {}, {}
for r in csv.DictReader(open(f"{CB}/uei_entity_profile.csv", encoding="utf-8-sig")):
    uei_primary_naics[r["uei"].strip()] = r["primary_naics_6"].strip()
    uei_name[r["uei"].strip()] = r["name"].strip()

def uei_category(uei):
    n = uei_primary_naics.get(uei, "")
    if not n:
        return "99"
    return naics2cat.get(n, "99")

# ---------------------------------------------------------------- SWBS -> expected process category
# Per-category predicate, grounded in ESWBS 3-digit nomenclature (not tuned to results):
#   5xx Auxiliary Systems splits: 51x ventilation/AC/refrigeration + 531 distilling = THERMAL(04);
#   504 instrument boards = INSTRUMENTS(10); 57x/58x = material HANDLING(11);
#   everything else in 5xx (50x pumps/piping, 52x firemain/cooling, 53x cooling water,
#   54x fuel, 55x compressed air/fire-ext, 56x steering/hydraulic, 59x pollution) = FLUID(03).
def d2(g): return g[:2]
def is_thermal(g):  return d2(g) == "51" or g == "531"
def is_handling(g): return d2(g) in ("57", "58")
def is_fluid(g):    return g[0] == "5" and not is_thermal(g) and not is_handling(g) and g != "504"
EXPECTED_SWBS = {
    "01": lambda g: g[0] == "3",                 # Electrical power  -> Electric Plant 3xx
    "02": lambda g: g[0] == "2",                 # Propulsion        -> Propulsion Plant 2xx
    "03": is_fluid,                              # Fluid/piping      -> Aux fluid systems
    "04": is_thermal,                           # HVAC/thermal      -> Aux climate/refrigeration/distilling
    "05": lambda g: g[0] == "1",                 # Structural        -> Hull Structure 1xx  (see NOT_OBSERVABLE)
    "10": lambda g: g[0] == "4" or g == "504",   # Sensors/controls  -> C4ISR 4xx + instrument boards (see NOT_OBSERVABLE)
    "11": is_handling,                          # Industrial machy  -> handling/replenishment 57x/58x
    "12": lambda g: g[0] == "7",                 # Ordnance          -> Armament 7xx
    "18": lambda g: g[0] == "6",                 # Interiors/outfit  -> Outfit & Furnishings 6xx
}
SYSTEM_GRADABLE = set(EXPECTED_SWBS)          # categories that align with the system axis

# Two system categories whose ship-system home cannot appear in the HII subaward slice,
# so a low SWBS agreement is a DATA artifact, not a taxonomy fault:
NOT_OBSERVABLE = {
    "05": "hull structure (1xx) is fabricated in-house by Ingalls; subcontracted structural metal "
          "appears as foundations/tanks/uptakes coded to the system it serves, not 1xx",
    "10": "combat / C4ISR (4xx) is GFE and excluded upstream; only residual ship-control & "
          "instrument work remains, landing in auxiliary systems",
}
# Everything else is PROCESS-ONLY (scatters across ship systems on purpose):
# 06 metals/forgings, 07 machining, 08 polymers/coatings, 09 electronic components,
# 13 shipyard, 14 engineering, 15 install/repair, 16 distribution, 17 workforce, 99 unresolved.

ONE_DIGIT_NAME = {"1":"Hull Structure","2":"Propulsion Plant","3":"Electric Plant",
                  "4":"Command/Control/Surveillance","5":"Auxiliary Systems",
                  "6":"Outfit & Furnishings","7":"Armament","8":"Integration/Eng",
                  "9":"Ship Assembly/Support"}
# Which category does an observed SWBS group most imply? (for mismatch flagging)
SWBS1_TO_CAT = {"1":"05","2":"02","3":"01","4":"10","6":"18","7":"12"}  # 5xx handled by sub-split

def swbs_implied_cat(g):
    d1 = g[0]
    if d1 == "5":
        if is_thermal(g):   return "04"
        if is_handling(g):  return "11"
        if g == "504":      return "10"
        return "03"
    return SWBS1_TO_CAT.get(d1, "")

# ---------------------------------------------------------------- load HII records
recs = list(csv.DictReader(open(f"{CB}/hii_ddg_record_components.csv", encoding="utf-8-sig")))
def amt(r): return float(r["amount_usd"] or 0)
HII_TOTAL = sum(amt(r) for r in recs)

# gradable universe = rows with a resolved swbs_group
swbs_rows = [r for r in recs if r["swbs_group"].strip()]
SWBS_TOTAL = sum(amt(r) for r in swbs_rows)

def entropy(dist):
    tot = sum(dist.values())
    if tot <= 0: return 0.0
    h = -sum((v/tot)*math.log2(v/tot) for v in dist.values() if v > 0)
    return h

# ================================================================ OUTPUT 1: per-NAICS-6 SWBS purity
# Group HII swbs dollars by the vendor's PRIMARY naics-6.
naics_swbs1 = collections.defaultdict(lambda: collections.Counter())  # naics -> {one-digit: $}
naics_swbs3 = collections.defaultdict(lambda: collections.Counter())  # naics -> {3-digit: $}
naics_records = collections.Counter()
naics_hii_dollars = collections.Counter()
for r in swbs_rows:
    n = uei_primary_naics.get(r["vendor_uei"].strip(), "") or "(no_primary)"
    g = r["swbs_group"].strip()
    naics_swbs1[n][g[0]] += amt(r)
    naics_swbs3[n][g] += amt(r)
    naics_records[n] += 1
    naics_hii_dollars[n] += amt(r)

rows1 = []
for n, d1 in naics_swbs1.items():
    tot = sum(d1.values())
    modal1, modal1_d = max(d1.items(), key=lambda x: x[1])
    d3 = naics_swbs3[n]
    modal3, modal3_d = max(d3.items(), key=lambda x: x[1])
    cat = naics2cat.get(n, "99") if n != "(no_primary)" else "99"
    observable = cat in SYSTEM_GRADABLE and cat not in NOT_OBSERVABLE
    # agreement = share of this NAICS's HII$ landing on the category's expected SWBS
    if observable:
        pred = EXPECTED_SWBS[cat]
        agree = sum(v for g, v in d3.items() if pred(g)) / tot
    else:
        agree = None
    grad_label = ("system_home_not_observable" if cat in NOT_OBSERVABLE
                  else "system" if cat in SYSTEM_GRADABLE
                  else "process_not_swbs_gradable")
    implied = swbs_implied_cat(modal3)
    rows1.append({
        "naics6": n,
        "desc": "",
        "assigned_cat": cat,
        "assigned_cat_name": catname.get(cat, ""),
        "gradable": grad_label,
        "hii_records": naics_records[n],
        "hii_dollars_$M": round(tot/1e6, 3),
        "modal_swbs1": modal1, "modal_swbs1_name": ONE_DIGIT_NAME.get(modal1, ""),
        "modal_swbs1_share": round(modal1_d/tot, 3),
        "modal_swbs3": modal3, "modal_swbs3_share": round(modal3_d/tot, 3),
        "swbs1_entropy_bits": round(entropy(d1), 3),
        "category_swbs_agreement": (round(agree, 3) if agree is not None else ""),
        "swbs_implied_cat": implied,
        "swbs_implied_cat_name": catname.get(implied, ""),
        "mismatch": ("yes" if (observable and implied and implied != cat) else ""),
    })
rows1.sort(key=lambda x: -x["hii_dollars_$M"])

# add NAICS descriptions from crosswalk
naics_desc = {}
for r in csv.DictReader(open(f"{TAX}/navy_all_observed_naics_crosswalk.csv", encoding="utf-8-sig")):
    naics_desc[r["naics6"].strip()] = r["desc"].strip()
for row in rows1:
    row["desc"] = naics_desc.get(row["naics6"], "")

with open(f"{OUT}/naics6_hii_purity.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows1[0].keys())); w.writeheader(); w.writerows(rows1)

# ================================================================ OUTPUT 2: per-category SWBS agreement
cat_dollars = collections.Counter()       # category -> HII$ with swbs
cat_agree_dollars = collections.Counter()  # category -> HII$ landing on expected swbs
cat_records = collections.Counter()
cat_comp_dollars = collections.Counter()   # category -> HII$ with component_text (for process cats)
cat_all_hii = collections.Counter()        # category -> all HII$ (swbs or not)
for r in recs:
    cat = uei_category(r["vendor_uei"].strip())
    cat_all_hii[cat] += amt(r)
    if r["component_text"].strip():
        cat_comp_dollars[cat] += amt(r)
    if r["swbs_group"].strip():
        cat_dollars[cat] += amt(r); cat_records[cat] += 1
        if cat in SYSTEM_GRADABLE and EXPECTED_SWBS[cat](r["swbs_group"].strip()):
            cat_agree_dollars[cat] += amt(r)

rows2 = []
for cat in sorted(set(cat_all_hii) | set(catname)):
    tot_swbs = cat_dollars[cat]
    observable = cat in SYSTEM_GRADABLE and cat not in NOT_OBSERVABLE
    agree = (cat_agree_dollars[cat]/tot_swbs) if (observable and tot_swbs > 0) else None
    ctype = ("system_home_not_observable" if cat in NOT_OBSERVABLE
             else "system" if cat in SYSTEM_GRADABLE else "process_not_swbs_gradable")
    rows2.append({
        "category_id": cat,
        "category": catname.get(cat, ""),
        "type": ctype,
        "hii_dollars_total_$M": round(cat_all_hii[cat]/1e6, 3),
        "hii_dollars_with_swbs_$M": round(tot_swbs/1e6, 3),
        "hii_records_with_swbs": cat_records[cat],
        "component_text_coverage": (round(cat_comp_dollars[cat]/cat_all_hii[cat], 3) if cat_all_hii[cat] > 0 else ""),
        "swbs_agreement": (round(agree, 3) if agree is not None else ""),
        "expected_swbs": {"01":"3xx","02":"2xx","03":"5xx fluid","04":"51x+531","05":"1xx",
                          "10":"4xx+504","11":"57-58x","12":"7xx","18":"6xx"}.get(cat, "n/a (process)"),
        "note": NOT_OBSERVABLE.get(cat, ""),
    })
rows2.sort(key=lambda x: -x["hii_dollars_total_$M"])
with open(f"{OUT}/category_hii_agreement.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows2[0].keys())); w.writeheader(); w.writerows(rows2)

# ================================================================ OUTPUT 3: low-purity flag list (enrichment queue)
# Flag a NAICS-6 if it carries material HII$ AND (scatters OR modal SWBS implies another category).
MATERIAL = 5.0   # $M of HII coverage to be worth flagging
flags = []
for row in rows1:
    if row["naics6"] == "(no_primary)":
        continue
    if row["hii_dollars_$M"] < MATERIAL:
        continue
    scatter = row["modal_swbs1_share"] < 0.70
    mism = row["mismatch"] == "yes"
    lowagree = row["category_swbs_agreement"] != "" and float(row["category_swbs_agreement"]) < 0.60
    if scatter or mism or lowagree:
        reasons = []
        if mism: reasons.append(f"modal SWBS implies {row['swbs_implied_cat']} ({row['swbs_implied_cat_name']}) not assigned {row['assigned_cat']}")
        if lowagree: reasons.append(f"low category agreement {row['category_swbs_agreement']}")
        if scatter: reasons.append(f"scattered (modal one-digit share {row['modal_swbs1_share']}, entropy {row['swbs1_entropy_bits']} bits)")
        flags.append({**{k: row[k] for k in
            ("naics6","desc","assigned_cat","assigned_cat_name","gradable","hii_dollars_$M",
             "modal_swbs1","modal_swbs1_name","modal_swbs1_share","swbs1_entropy_bits",
             "category_swbs_agreement","swbs_implied_cat","swbs_implied_cat_name")},
            "flag_reason": "; ".join(reasons)})
flags.sort(key=lambda x: -x["hii_dollars_$M"])
with open(f"{OUT}/low_purity_flags.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(flags[0].keys())); w.writeheader(); w.writerows(flags)

# ================================================================ console summary
print("="*78)
print("TAXONOMY vs HII-DDG SCORING  (referee = ~13% of corpus, one builder, one program)")
print("="*78)
print(f"HII-DDG total $:                 ${HII_TOTAL/1e6:,.1f}M")
print(f"  with resolved SWBS group:      ${SWBS_TOTAL/1e6:,.1f}M ({SWBS_TOTAL/HII_TOTAL*100:.1f}% of HII)")
gradable_dollars = sum(cat_dollars[c] for c in SYSTEM_GRADABLE)
print(f"  in SYSTEM-gradable categories: ${gradable_dollars/1e6:,.1f}M ({gradable_dollars/SWBS_TOTAL*100:.1f}% of SWBS$)")
print()
print("SYSTEM categories -- SWBS agreement (share of HII$ landing on expected ship system):")
for r in rows2:
    if r["type"] == "system" and r["hii_dollars_with_swbs_$M"] > 0:
        print(f"  {r['category_id']} {r['category'][:44]:44} ${r['hii_dollars_with_swbs_$M']:7.1f}M  agree={r['swbs_agreement']}  (exp {r['expected_swbs']})")
print()
print("SYSTEM categories whose ship-system home is NOT observable in HII (agreement N/A -- data artifact):")
for r in rows2:
    if r["type"] == "system_home_not_observable" and r["hii_dollars_total_$M"] >= 1:
        print(f"  {r['category_id']} {r['category'][:44]:44} ${r['hii_dollars_with_swbs_$M']:7.1f}M  -- {r['note']}")
print()
print("PROCESS-ONLY categories (NOT SWBS-graded; component_text coverage shown):")
for r in rows2:
    if r["type"] == "process_not_swbs_gradable" and r["hii_dollars_total_$M"] >= 1:
        print(f"  {r['category_id']} {r['category'][:44]:44} ${r['hii_dollars_total_$M']:7.1f}M  comp_text={r['component_text_coverage']}")
print()
print(f"LOW-PURITY FLAGS (>= ${MATERIAL}M HII, scattered or category-mismatch) -> enrichment queue: {len(flags)}")
for r in flags[:20]:
    print(f"  {r['naics6']} {r['desc'][:34]:34} cat {r['assigned_cat']} ${r['hii_dollars_$M']:6.1f}M | {r['flag_reason']}")
print()
print("Wrote: naics6_hii_purity.csv, category_hii_agreement.csv, low_purity_flags.csv  ->", OUT)
