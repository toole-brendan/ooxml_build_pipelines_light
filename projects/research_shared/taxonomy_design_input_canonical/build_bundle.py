"""Build the canonical taxonomy-design bundle.

Universe + dollars + program + dedup + pass-through/scope exclusion come ONLY from
_corpus.iter_records (the stream the award-analysis workbook actually consumes).
SAM NAICS-6 / NAICS list / PSC / org-structure are joined by UEI from the entity
enrichment, used purely as per-entity attributes (its dollars/programs are ignored).
Old role/bucket/basis are dropped so the prior scheme never leaks. LCS line-item
contamination is stripped by sub_report_id. Originals are left untouched.
"""
from __future__ import annotations
import csv, importlib.util, sys, shutil
from collections import defaultdict, Counter
from pathlib import Path

REPO = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
OLD  = REPO / "projects/research_shared/taxonomy_design_input"          # untouched source for HII/SWBS
ENR  = REPO / "projects/research_shared/sam_entity_enrichment"
OUT  = REPO / "projects/research_shared/taxonomy_design_input_canonical"
OUT.mkdir(parents=True, exist_ok=True)

def _load_corpus():
    spec = importlib.util.spec_from_file_location(
        "_corpus", REPO / "projects/distributed_shipbuilding/research/scripts/_corpus.py")
    m = importlib.util.module_from_spec(spec); sys.modules["_corpus"] = m
    spec.loader.exec_module(m); return m
CORP = _load_corpus()

def f(x):
    try: return float(x)
    except (TypeError, ValueError): return 0.0

# ---- 1. LCS exclusion set (sub_report_id) from the HII descriptions ----------------
hii_rows = list(csv.DictReader((OLD/"hii_ddg_record_components.csv").open(encoding="utf-8")))
LCS_IDS = {r["sub_report_id"].strip() for r in hii_rows
           if "LCS" in (r["raw_description"] or "").upper()}

# ---- 2. canonical record stream -> per-entity aggregation --------------------------
ent = defaultdict(lambda: {"name":"", "tot":0.0, "subs":0.0, "ddg":0.0, "rec":0, "foreign":False})
for program in ("submarines", "ddg"):
    for r in CORP.iter_records(program):
        if r["report_id"] in LCS_IDS:           # drop LCS line items
            continue
        key = (r["entity_uei"] or r["parent_uei"] or ("NAME:"+r["vendor"])).strip()
        e = ent[key]
        if not e["name"] or e["name"] == "-": e["name"] = r["vendor"]
        d = r["dollar_m"]
        e["tot"] += d
        e["subs" if program == "submarines" else "ddg"] += d
        e["rec"] += 1
        if r["foreign"]: e["foreign"] = True

# ---- 3. SAM enrichment as a per-UEI attribute lookup (ignore its $/programs) --------
ATTR = ["sam_match","reg_status","org_structure_desc","primary_naics_6","primary_naics_4",
        "naics_count","all_naics_6","psc_count","psc_list","immediate_owner","highest_owner",
        "cage","exclusion","business_types"]
enr = {r["uei"].strip(): r for r in csv.DictReader((ENR/"unique_uei_sam_enrichment.csv").open(encoding="utf-8-sig"))}
naics6_desc = {}
for r in csv.DictReader((ENR/"uei_naics_long.csv").open(encoding="utf-8-sig")):
    naics6_desc.setdefault(r["naics6"].strip(), r["desc"].strip())

# ---- 4. write uei_entity_profile.csv ----------------------------------------------
canon_ueis = set(ent)
cols = ["uei","name","dollars_total_$M","dollars_submarines_$M","dollars_ddg_$M",
        "records","foreign","enriched"] + ATTR
with (OUT/"uei_entity_profile.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(cols)
    for k, e in sorted(ent.items(), key=lambda kv: -kv[1]["tot"]):
        a = enr.get(k, {})
        row = [k, e["name"], round(e["tot"],3), round(e["subs"],3), round(e["ddg"],3),
               e["rec"], "yes" if e["foreign"] else "no", "yes" if a else "no"]
        row += [a.get(c,"") for c in ATTR]
        w.writerow(row)

# ---- 5. naics6_distribution.csv on the canonical $ --------------------------------
agg = defaultdict(lambda: [0.0, 0])   # $M, vendor_count
for k, e in ent.items():
    n6 = (enr.get(k, {}).get("primary_naics_6") or "").strip() or "(no_primary_naics6)"
    agg[n6][0] += e["tot"]; agg[n6][1] += 1
tot_all = sum(v[0] for v in agg.values())
with (OUT/"naics6_distribution.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["primary_naics_6","desc","vendors","dollars_$M","pct_dollars"])
    for n6, (m, vc) in sorted(agg.items(), key=lambda kv: -kv[1][0]):
        w.writerow([n6, naics6_desc.get(n6,""), vc, round(m,2), round(100*m/tot_all,2)])

# ---- 6. long-form NAICS / PSC filtered to canonical UEIs ---------------------------
for fn in ("uei_naics_long.csv","uei_psc_long.csv"):
    src = list(csv.DictReader((ENR/fn).open(encoding="utf-8-sig")))
    with (OUT/fn).open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=src[0].keys()); w.writeheader()
        for r in src:
            if r["uei"].strip() in canon_ueis: w.writerow(r)

# ---- 7. HII record file (LCS stripped) + regenerated code dictionary ---------------
keep = [r for r in hii_rows if r["sub_report_id"].strip() not in LCS_IDS]
with (OUT/"hii_ddg_record_components.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=hii_rows[0].keys()); w.writeheader(); w.writerows(keep)
code = defaultdict(lambda: {"n":0,"usd":0.0,"swbs":Counter(),"comp":Counter()})
for r in keep:
    c = r["code"].strip()
    if not c: continue
    d = code[c]; d["n"] += 1; d["usd"] += f(r["amount_usd"])
    if r["swbs_group"].strip(): d["swbs"][r["swbs_group"].strip()] += 1
    if r["component_text"].strip(): d["comp"][r["component_text"].strip()] += 1
with (OUT/"hii_ddg_code_dictionary.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh); w.writerow(["code","n_subawards","total_usd","modal_swbs_group","top_components"])
    for c, d in sorted(code.items(), key=lambda kv: -kv[1]["usd"]):
        modal = d["swbs"].most_common(1)[0][0] if d["swbs"] else ""
        top = "; ".join(x for x,_ in d["comp"].most_common(3))
        w.writerow([c, d["n"], round(d["usd"],2), modal, top])

# ---- 8. copy SWBS reference ---------------------------------------------------------
shutil.copy(OLD/"swbs_hierarchy.csv", OUT/"swbs_hierarchy.csv")

# ---- 9. reconciliation printout ----------------------------------------------------
subs = sum(e["subs"] for e in ent.values()); ddg = sum(e["ddg"] for e in ent.values())
enr_d = sum(e["tot"] for k,e in ent.items() if enr.get(k))
n6_d  = sum(e["tot"] for k,e in ent.items() if (enr.get(k,{}).get("primary_naics_6") or "").strip())
bf = sum(e["tot"] for k,e in ent.items() if k=="F8PEZKXES8B1")
print("=== CANONICAL bundle reconciliation ===")
print(f"total           ${subs+ddg:9,.0f}M   {len(ent)} UEIs")
print(f"  submarines    ${subs:9,.0f}M")
print(f"  ddg           ${ddg:9,.0f}M")
print(f"BlueForge       ${bf:9,.1f}M   (must be 0)")
print(f"LCS ids stripped: {len(LCS_IDS)}")
print(f"SAM-enriched $  ${enr_d:9,.0f}M  ({100*enr_d/(subs+ddg):.1f}% of $)")
print(f"has NAICS-6 $   ${n6_d:9,.0f}M  ({100*n6_d/(subs+ddg):.1f}% of $)")
print(f"not-enriched $  ${subs+ddg-enr_d:9,.0f}M  ({100*(subs+ddg-enr_d)/(subs+ddg):.1f}% of $)")
print("\ntop 15 NAICS-6 by canonical $:")
for n6,(m,vc) in sorted(agg.items(), key=lambda kv:-kv[1][0])[:15]:
    print(f"  {n6:14} {vc:4}v ${m:7,.0f}M  {naics6_desc.get(n6,'')[:46]}")
print(f"\nwrote bundle -> {OUT}")
