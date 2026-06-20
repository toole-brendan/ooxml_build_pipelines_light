#!/usr/bin/env python3
"""Task B - tail entity-resolution (>= $20M combined signed, DDG+subs).

Aggregates SIGNED subaward dollars by operating entity (sub_entity_uei, fallback
sub_parent_uei) across both projects' nc_records_long.csv, finds entities >= the
floor that are NOT already in the evidence registry, resolves each via the SAM
Entity API (cache-first; single-UEI live call only when uncached), and emits a
first-pass NAICS-based classification for review.

Output: tail_resolved.csv (facts + auto-classification) in this directory.
No workbook code touched. Read-only against the build; only writes the SAM cache
and tail_resolved.csv.
"""
from __future__ import annotations
import csv, json, os, subprocess, sys
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/ooxml_build_pipelines_light")
HERE = REPO / "projects/distributed_shipbuilding/sam/award_classification/supplier_bucketing"
REGISTRY = Path("/Users/brendantoole/projects2/vendor_evidence_registry.csv")
ENV = Path("/Users/brendantoole/projects2/distributed_shipbuilding/.env")
FLOOR = 20.0
PROJ = {"ddg": REPO / "projects/ddg", "subs": REPO / "projects/submarines"}
CACHE = {p: PROJ[p] / "research/sam_entity_lookups" for p in PROJ}
RECORDS = {p: PROJ[p] / "workbook/extracted/nc_records_long.csv" for p in PROJ}


def _f(x):
    try:
        return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError):
        return 0.0


def aggregate():
    """signed $M by uei per project + a representative name + foreign flag."""
    by = {p: defaultdict(float) for p in PROJ}
    name, foreign = {}, {}
    for p in PROJ:
        with RECORDS[p].open(encoding="utf-8-sig", newline="") as fh:
            for r in csv.DictReader(fh):
                eu = (r.get("sub_entity_uei") or "").strip()
                pu = (r.get("sub_parent_uei") or "").strip()
                uei = eu or pu or "-"
                by[p][uei] += _f(r.get("subAwardAmount_$")) / 1e6
                if uei not in name and (r.get("sub_name") or "").strip():
                    name[uei] = (r.get("sub_name") or "").strip()
                if (r.get("foreign") or "").strip():
                    foreign[uei] = True
    return by, name, foreign


def load_registry_ueis():
    if not REGISTRY.exists():
        return set()
    with REGISTRY.open(encoding="utf-8-sig") as fh:
        return {(r.get("uei") or "").strip() for r in csv.DictReader(fh)}


def read_key():
    for line in ENV.read_text().splitlines():
        if line.startswith("SAM_API_KEY"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("no SAM_API_KEY")


def cached_path(uei):
    for p in PROJ:
        f = CACHE[p] / f"{uei}.json"
        if f.exists():
            return f
    return None


def parse_sam(doc):
    """return (legalName, primaryNaics, country, registered) from either cache schema."""
    ed = doc.get("entityData") or (doc.get("body") or {}).get("entityData") or []
    if not ed:
        return ("", "", "", "no")
    e = ed[0]
    reg = e.get("entityRegistration", {}) or {}
    asr = (e.get("assertions", {}) or {}).get("goodsAndServices", {}) or {}
    core = (e.get("coreData", {}) or {})
    addr = (core.get("physicalAddress", {}) or {})
    return (reg.get("legalBusinessName", "") or "",
            asr.get("primaryNaics", "") or "",
            (addr.get("countryCode", "") or reg.get("ueiSAM", "") and ""),
            reg.get("samRegistered", "") or "no")


def live_call(uei, key, name):
    base = "https://api.sam.gov/entity-information/v3/entities"
    inc = "entityRegistration,coreData,assertions"
    for flag in ("Yes", "No"):
        url = f"{base}?api_key={key}&ueiSAM={uei}&samRegistered={flag}&includeSections={inc}"
        try:
            out = subprocess.run(["curl", "-sS", "--max-time", "30", url],
                                 capture_output=True, text=True, timeout=40)
            doc = json.loads(out.stdout or "{}")
        except Exception:
            doc = {}
        if doc.get("totalRecords", 0) and doc.get("entityData"):
            return {"uei": uei, "vendor": name, "body": doc}
    return {"uei": uei, "vendor": name, "body": doc if 'doc' in dir() else {}}


# ── NAICS-based first-pass classifier (mirrors the planned ladder; 3364/3344 NOT physical) ──
NAICS4_BUCKET = {
    "3323": "structural", "3324": "structural", "3366": "structural", "3369": "structural",
    "3327": "machining", "3336": "machining",
    "3321": "castings", "3315": "castings", "3312": "castings",
    "3329": "piping", "3339": "piping", "4235": "piping", "3328": "coatings",
    "3353": "electrical", "3359": "electrical", "3351": "electrical", "3352": "electrical",
    "3334": "hvac",
    "3252": "coatings", "3259": "coatings", "3262": "coatings", "3255": "coatings",
}
SERVICE_NAICS4 = {"5413", "5415", "5416", "5417", "5132", "6114", "4885", "4247",
                  "2362", "4236", "8113", "5418", "5614", "5612", "5419", "5611",
                  "5621", "4231", "4239", "8112", "5612", "4841", "4842", "5511"}
MISSION_NAICS4 = {"3344", "3345", "3342", "3343", "3341", "3364", "3346", "3399", "3372"}
# 5-digit refinements that ARE physical power equipment (override the 4-digit mission read)
POWER_NAICS5 = {"33531", "33591", "33592", "33611", "33612", "33531"}


def classify(naics, foreign, legal):
    n = (naics or "").strip()
    n4, n5 = n[:4], n[:5]
    if foreign:
        return ("foreign_fms", "", "med", "foreign flag")
    if n4 == "5511":
        return ("holding", "", "high", "NAICS 5511 holding")
    if n5 in POWER_NAICS5 or n4 in ("3353", "3359", "3351", "3352"):
        return ("supplier", "electrical", "high", f"NAICS {n} power equip")
    if n4 in NAICS4_BUCKET:
        return ("supplier", NAICS4_BUCKET[n4], "high", f"NAICS {n}")
    if n4 in MISSION_NAICS4:
        return ("mission_systems", "", "med", f"NAICS {n} electronics/aero")
    if n4 in SERVICE_NAICS4:
        return ("service", "", "high", f"NAICS {n} service")
    if n.startswith("33") and n4 in ("3311", "3313", "3314", "3261"):
        return ("supplier", "castings" if n4 in ("3311", "3313", "3314") else "coatings",
                "med", f"NAICS {n}")
    return ("residual", "", "low", f"NAICS {n or 'none'} unresolved")


def main():
    by, name, foreign = aggregate()
    ueis = set().union(*[set(by[p]) for p in PROJ])
    combined = {u: sum(by[p].get(u, 0.0) for p in PROJ) for u in ueis}
    reg = load_registry_ueis()
    tail = sorted([u for u in ueis if u != "-" and combined[u] >= FLOOR and u not in reg],
                  key=lambda u: -combined[u])
    print(f"tail entities >= ${FLOOR:.0f}M not in registry: {len(tail)}", file=sys.stderr)

    key = None
    rows = []
    live = 0
    for u in tail:
        cp = cached_path(u)
        if cp:
            doc = json.loads(cp.read_text())
        else:
            if key is None:
                key = read_key()
            doc = live_call(u, key, name.get(u, ""))
            live += 1
            # cache to each project where the entity has spend
            for p in PROJ:
                if by[p].get(u, 0.0) != 0:
                    (CACHE[p] / f"{u}.json").write_text(json.dumps(doc))
            print(f"  live[{live}] {u} {name.get(u,'')[:32]}", file=sys.stderr)
        legal, naics, country, registered = parse_sam(doc)
        is_foreign = bool(foreign.get(u)) or (country not in ("", "USA", "US"))
        role, bucket, conf, basis = classify(naics, is_foreign, legal)
        rows.append({
            "uei": u, "entity_name": name.get(u, ""), "sam_legal": legal,
            "primary_naics": naics, "naics4": (naics or "")[:4],
            "ddg_signed_$M": round(by["ddg"].get(u, 0.0), 1),
            "subs_signed_$M": round(by["subs"].get(u, 0.0), 1),
            "combined_$M": round(combined[u], 1),
            "foreign": "Y" if is_foreign else "",
            "registered": registered,
            "role": role, "bucket": bucket, "confidence": conf, "basis": basis,
        })

    out = HERE / "tail_resolved.csv"
    cols = ["uei", "entity_name", "sam_legal", "primary_naics", "naics4",
            "ddg_signed_$M", "subs_signed_$M", "combined_$M", "foreign",
            "registered", "role", "bucket", "confidence", "basis"]
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print(f"\nlive SAM calls made: {live}", file=sys.stderr)
    print(f"wrote {len(rows)} rows -> {out}", file=sys.stderr)
    # quick role tally
    tally = defaultdict(lambda: [0, 0.0])
    for r in rows:
        tally[r["role"]][0] += 1
        tally[r["role"]][1] += r["combined_$M"]
    for role, (n, d) in sorted(tally.items(), key=lambda kv: -kv[1][1]):
        print(f"  {role:16} {n:3}  ${d:8.1f}M", file=sys.stderr)


if __name__ == "__main__":
    main()
