#!/usr/bin/env python3
"""Profile cached SAM entity data + corpus weights -> taxonomy-design tables."""
import json, csv, os, glob
from collections import defaultdict
HERE=os.path.dirname(os.path.abspath(__file__))
RAW=os.path.join(HERE,"raw")

# ---- v1 crosswalks (from ddg/submarines _taxonomy.py) for comparison column ----
NAICS4_BUCKET={"3323":"structural","3324":"structural","3366":"structural","3369":"structural",
 "3327":"machining","3336":"machining","3321":"castings","3315":"castings","3312":"castings",
 "3329":"piping","3339":"piping","4235":"piping","3353":"electrical","3359":"electrical",
 "3334":"hvac","3252":"coatings","3259":"coatings","3262":"coatings"}
SERVICE_NAICS4={"5413","5415","5416","5417","5132","6114","4885","4247","2362","4236","8113","5418","5614","5612","5419"}
def v1cat(n4):
    if n4 in NAICS4_BUCKET: return NAICS4_BUCKET[n4]
    if n4 in SERVICE_NAICS4: return "service"
    if n4=="5511": return "holding"
    return "unbucketed/other"

# ---- corpus weights ----
W={}
with open(os.path.join(HERE,"unique_uei_corpus.csv")) as fh:
    for r in csv.DictReader(fh):
        W[r["uei"]]={"dollars":float(r["dollars"]),"records":int(r["records"]),
                     "name":r["name"],"programs":r["programs"],"foreign":r["foreign"]}

def g(d,*path):
    for k in path:
        if not isinstance(d,dict): return None
        d=d.get(k)
    return d
def D(x): return x if isinstance(x,dict) else {}
def L(x): return x if isinstance(x,list) else []

rows=[]; naics_long=[]; psc_long=[]
n_files=n_norec=n_active=0
for u,w in W.items():
    p=os.path.join(RAW,f"{u}.json")
    if not os.path.exists(p): continue
    n_files+=1
    d=json.load(open(p))
    if d.get("_no_record") or d.get("_http_error"):
        n_norec+=1
        rows.append({"uei":u,"name":w["name"],"dollars":w["dollars"],"records":w["records"],
            "programs":w["programs"],"foreign":w["foreign"],"sam_match":"NO_RECORD",
            "reg_status":"","org_structure_desc":"","primary_naics_6":"","primary_naics_4":"",
            "naics_count":0,"all_naics_6":"","psc_count":0,"psc_list":"",
            "immediate_owner":"","highest_owner":"","cage":"","exclusion":"","v1_cat_from_primary4":"NO_RECORD"})
        continue
    reg=D(d.get("entityRegistration"))
    if reg.get("registrationStatus")=="Active": n_active+=1
    gs=D(g(d,"assertions","goodsAndServices"))
    naics=[x for x in L(gs.get("naicsList")) if isinstance(x,dict) and x.get("naicsCode")]
    psc=[x for x in L(gs.get("pscList")) if isinstance(x,dict) and x.get("pscCode")]
    prim6=str(gs.get("primaryNaics") or "").strip()
    prim4=prim6[:4]
    org=g(d,"coreData","generalInformation","organizationStructureDesc") or ""
    io=g(d,"integrityInformation","corporateRelationships","immediateOwner","legalBusinessName") or ""
    ho=g(d,"integrityInformation","corporateRelationships","highestOwner","legalBusinessName") or ""
    bt=[b.get("businessTypeDesc") for b in L(g(d,"coreData","businessTypes","businessTypeList")) if isinstance(b,dict) and b.get("businessTypeDesc")]
    all6=[str(n.get("naicsCode")).strip() for n in naics]
    for n in naics:
        naics_long.append({"uei":u,"naics6":str(n.get("naicsCode")).strip(),
            "desc":n.get("naicsDescription") or "","is_primary":"Y" if str(n.get("naicsCode")).strip()==prim6 else "",
            "dollars":w["dollars"]})
    for x in psc:
        psc_long.append({"uei":u,"psc":str(x.get("pscCode")).strip(),"desc":x.get("pscDescription") or "","dollars":w["dollars"]})
    rows.append({"uei":u,"name":w["name"],"dollars":w["dollars"],"records":w["records"],
        "programs":w["programs"],"foreign":w["foreign"],"sam_match":reg.get("registrationStatus") or "?",
        "reg_status":reg.get("registrationStatus") or "","org_structure_desc":org,
        "primary_naics_6":prim6,"primary_naics_4":prim4,"naics_count":len(naics),
        "all_naics_6":";".join(all6),"psc_count":len(psc),
        "psc_list":";".join(str(x.get("pscCode")).strip() for x in psc),
        "immediate_owner":io,"highest_owner":ho,"cage":reg.get("cageCode") or "",
        "exclusion":reg.get("exclusionStatusFlag") or "","business_types":";".join(bt),
        "v1_cat_from_primary4":v1cat(prim4)})

def write(name,fieldnames,data):
    with open(os.path.join(HERE,name),"w",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=fieldnames,extrasaction="ignore"); w.writeheader()
        for r in data: w.writerow(r)

rows.sort(key=lambda r:-r["dollars"])
write("unique_uei_sam_enrichment.csv",list(rows[0].keys()),rows)
write("uei_naics_long.csv",["uei","naics6","desc","is_primary","dollars"],naics_long)
write("uei_psc_long.csv",["uei","psc","desc","dollars"],psc_long)

TOT=sum(r["dollars"] for r in rows)
# primary NAICS-6 profile
prof=defaultdict(lambda:{"d":0.0,"v":0,"desc":"","v1":""})
descmap={}
for r in rows:
    n=r["primary_naics_6"]
    if not n: n="(none)"
    prof[n]["d"]+=r["dollars"]; prof[n]["v"]+=1; prof[n]["v1"]=r["v1_cat_from_primary4"]
for nl in naics_long:
    if nl["is_primary"]=="Y": descmap[nl["naics6"]]=nl["desc"]
p6=[{"primary_naics_6":k,"desc":descmap.get(k,""),"vendors":v["v"],"dollars_$M":round(v["d"]/1e6,2),
     "pct_dollars":round(100*v["d"]/TOT,2),"v1_cat":v["v1"]} for k,v in sorted(prof.items(),key=lambda x:-x[1]["d"])]
write("naics6_primary_profile.csv",["primary_naics_6","desc","vendors","dollars_$M","pct_dollars","v1_cat"],p6)

# PSC profile (where present)
pscp=defaultdict(lambda:{"d":0.0,"v":0,"desc":""})
for x in psc_long:
    pscp[x["psc"]]["d"]+=x["dollars"]; pscp[x["psc"]]["v"]+=1; pscp[x["psc"]]["desc"]=x["desc"]
pp=[{"psc":k,"desc":v["desc"],"vendors":v["v"],"assoc_dollars_$M":round(v["d"]/1e6,2)} for k,v in sorted(pscp.items(),key=lambda x:-x[1]["d"])]
write("psc_profile.csv",["psc","desc","vendors","assoc_dollars_$M"],pp)

# org structure distribution
org=defaultdict(lambda:{"d":0.0,"v":0})
for r in rows:
    o=r["org_structure_desc"] or "(none/no-record)"
    org[o]["d"]+=r["dollars"]; org[o]["v"]+=1
orgp=[{"org_structure":k,"vendors":v["v"],"dollars_$M":round(v["d"]/1e6,2),"pct_dollars":round(100*v["d"]/TOT,2)} for k,v in sorted(org.items(),key=lambda x:-x[1]["d"])]
write("org_structure_profile.csv",["org_structure","vendors","dollars_$M","pct_dollars"],orgp)

# ---- coverage summary ----
def share(pred):
    d=sum(r["dollars"] for r in rows if pred(r)); return 100*d/TOT
matched=[r for r in rows if r["sam_match"]!="NO_RECORD"]
print(f"=== COVERAGE (of ${TOT/1e6:,.0f}M, {len(rows)} UEIs cached) ===")
print(f"SAM matched:            {len(matched):4d} UEIs  {share(lambda r:r['sam_match']!='NO_RECORD'):5.1f}% of $")
print(f"  active registration:  {n_active:4d} UEIs  {share(lambda r:r['reg_status']=='Active'):5.1f}% of $")
print(f"has primary NAICS-6:    {sum(1 for r in matched if r['primary_naics_6']):4d} UEIs  {share(lambda r:bool(r['primary_naics_6'])):5.1f}% of $")
print(f"has >=1 PSC:            {sum(1 for r in matched if r['psc_count']):4d} UEIs  {share(lambda r:r['psc_count']>0):5.1f}% of $")
print(f"has org-structure:      {sum(1 for r in matched if r['org_structure_desc']):4d} UEIs  {share(lambda r:bool(r['org_structure_desc'])):5.1f}% of $")
print(f"has immediate owner:    {sum(1 for r in matched if r['immediate_owner']):4d} UEIs  {share(lambda r:bool(r['immediate_owner'])):5.1f}% of $")
print(f"NO SAM record:          {n_norec:4d} UEIs  {share(lambda r:r['sam_match']=='NO_RECORD'):5.1f}% of $")
print(f"\n=== current-v1-category from primary NAICS-4 (dollar-weighted) ===")
v1=defaultdict(float)
for r in rows: v1[r["v1_cat_from_primary4"]]+=r["dollars"]
for k,v in sorted(v1.items(),key=lambda x:-x[1]): print(f"  {k:20s} {100*v/TOT:5.1f}%  (${v/1e6:,.0f}M)")
print(f"\n=== TOP 25 primary NAICS-6 by dollars ===")
for r in p6[:25]:
    print(f"  {r['primary_naics_6']:7s} {r['pct_dollars']:5.1f}%  v={r['vendors']:3d}  [{r['v1_cat']:16s}] {r['desc'][:46]}")
print(f"\nwrote: unique_uei_sam_enrichment.csv, uei_naics_long.csv, uei_psc_long.csv,")
print(f"       naics6_primary_profile.csv, psc_profile.csv, org_structure_profile.csv")
