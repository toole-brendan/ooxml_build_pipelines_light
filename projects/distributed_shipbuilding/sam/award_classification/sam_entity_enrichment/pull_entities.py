#!/usr/bin/env python3
"""Pull + cache SAM entity data for every unique subawardee UEI (dollar-desc order).
Resumable: skips UEIs already cached in raw/. Stops cleanly on HTTP 429 (quota)."""
import urllib.request, urllib.parse, json, csv, time, os
BASE="/Users/brendantoole/projects3/ooxml_build_pipelines_light"
HERE=os.path.join(BASE,"projects/distributed_shipbuilding/sam/award_classification/sam_entity_enrichment")
RAW=os.path.join(HERE,"raw")
key=[l.strip().split("=",1)[1] for l in open(os.path.join(BASE,".env")) if l.startswith("SAM_API_KEY=")][0]
SECTIONS="entityRegistration,coreData,assertions,integrityInformation"

ueis=[]
with open(os.path.join(HERE,"unique_uei_corpus.csv")) as fh:
    for r in csv.DictReader(fh):
        ueis.append(r["uei"])

def progress(done,total,status):
    json.dump({"done":done,"total":total,"status":status},
              open(os.path.join(HERE,"_pull_progress.json"),"w"))

done=0; pulled=0; norec=0; err=0
for i,uei in enumerate(ueis):
    out=os.path.join(RAW,f"{uei}.json")
    if os.path.exists(out):
        done+=1; continue
    p=urllib.parse.urlencode({"ueiSAM":uei,"includeSections":SECTIONS,"api_key":key})
    url=f"https://api.sam.gov/entity-information/v3/entities?{p}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={"Accept":"application/json"}),timeout=45) as r:
            d=json.load(r)
        ed=d.get("entityData") or []
        if not ed:
            json.dump({"_no_record":True,"uei":uei}, open(out,"w")); norec+=1
        else:
            json.dump(ed[0], open(out,"w")); pulled+=1
        done+=1
    except urllib.error.HTTPError as e:
        if e.code==429:
            progress(done,len(ueis),f"STOPPED_429 at idx {i} ({uei})")
            print(f"429 quota hit at idx {i}; stopping cleanly. pulled={pulled} norec={norec}")
            raise SystemExit
        json.dump({"_http_error":e.code,"uei":uei}, open(out,"w")); err+=1; done+=1
    except Exception as e:
        err+=1  # transient: don't cache, will retry next run
    if i % 25 == 0:
        progress(done,len(ueis),f"running pulled={pulled} norec={norec} err={err}")
    time.sleep(0.12)
progress(done,len(ueis),f"DONE pulled={pulled} norec={norec} err={err}")
print(f"DONE pulled={pulled} norec={norec} err={err} done={done}/{len(ueis)}")
