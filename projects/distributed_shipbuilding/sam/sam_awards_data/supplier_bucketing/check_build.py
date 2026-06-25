#!/usr/bin/env python3
"""Validation oracle - reproduces each workbook's Entity Master aggregation using the
BUILD's own classify + registry, so the sums here equal the workbook SUMPRODUCT values.
Compares to the signed-off reconciliation (reconcile.py View 2). Read-only."""
from __future__ import annotations
import csv, sys, importlib.util
from collections import defaultdict
from pathlib import Path

REPO = Path("/Users/brendantoole/projects2/ooxml_build_pipelines_light")
BUCKETS = ["structural", "machining", "castings", "piping", "electrical", "hvac", "coatings"]
UNB = "unbucketed"

# import each project's build modules by path (no package install needed)
sys.path.insert(0, str(REPO / "projects/ddg/workbook"))
sys.path.insert(0, str(REPO / "projects/submarines/workbook"))

PROJ = {
    "DDG": dict(root=REPO / "projects/ddg",
                tax="workbook_ddg.sheets._taxonomy", reg="workbook_ddg.sheets._registry"),
    "Subs": dict(root=REPO / "projects/submarines",
                 tax="workbook_submarines.sheets.taxonomy", reg="workbook_submarines.sheets._registry"),
}
TARGET = {  # reconcile.py View 2 (signed-off), $M
    "DDG": dict(total=11202, physical=4005, mission=2665, service_holding=1741, foreign=359, prime_gfe=405, residual=2027),
    "Subs": dict(total=6139, physical=4779, mission=246, service_holding=175, foreign=185, prime_gfe=92, residual=663),
}
SUP = {"supplier"}
PRIME = {"prime", "co_prime", "gfe", "gfe_mib", "gfe_sib"}
MISSION = {"mission_systems"}
SVC = {"service", "holding"}
FGN = {"foreign_fms"}


def _f(x):
    try: return float(str(x).replace(",", "").strip())
    except (TypeError, ValueError): return 0.0


def run(book):
    import importlib
    cfg = PROJ[book]
    tax = importlib.import_module(cfg["tax"])
    reg = importlib.import_module(cfg["reg"]).load_registry()
    ext = cfg["root"] / "workbook/extracted"
    enr = {}
    with (ext / "entity_naics_lookup.csv").open(encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            u = (r.get("uei") or "").strip()
            if u: enr[u] = (r.get("naics_4digit") or "").strip()
    cat = defaultdict(float); buck = defaultdict(float); modular = vls = total = 0.0
    with (ext / "nc_records_long.csv").open(encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            vendor = (r.get("sub_name") or "").strip()
            eu = (r.get("sub_entity_uei") or "").strip(); pu = (r.get("sub_parent_uei") or "").strip()
            naics4 = enr.get(eu) or enr.get(pu) or ""
            amt = _f(r.get("subAwardAmount_$")) / 1e6
            total += amt
            hit = reg.get(eu) or reg.get(pu)
            if hit:
                role = hit["role"]; bucket = hit["bucket"] or (UNB if role == "supplier" else "")
                mod, v = hit["modular"], hit["vls"]
            else:
                if book == "DDG":
                    role, bucket, _ = tax.classify(vendor, naics4, "")
                else:
                    role, bucket, _ = tax.classify(vendor, naics4)
                bucket = bucket or UNB; mod = v = False
                if role == "supplier" and bucket == UNB and not naics4 and (r.get("foreign") or "").strip():
                    role, bucket = "foreign_fms", ""
            if v: vls += amt
            if role in SUP:
                if bucket in BUCKETS:
                    cat["physical"] += amt; buck[bucket] += amt
                    if mod: modular += amt
                else:
                    cat["residual"] += amt
            elif role in MISSION: cat["mission"] += amt
            elif role in SVC: cat["service_holding"] += amt
            elif role in FGN: cat["foreign"] += amt
            elif role in PRIME: cat["prime_gfe"] += amt
            else: cat["residual"] += amt
    return total, cat, buck, modular, vls


for book in (sys.argv[1:] or ["DDG", "Subs"]):
    total, cat, buck, modular, vls = run(book)
    t = TARGET[book]
    print(f"\n=== {book} (build classify) vs signed-off reconcile View 2 ===")
    print(f"{'category':18} {'build $M':>10} {'target $M':>10} {'delta':>8}")
    rows = [("total", total)] + [(k, cat.get(k, 0.0)) for k in
            ("physical", "mission", "service_holding", "foreign", "prime_gfe", "residual")]
    ok = True
    for k, v in rows:
        tg = t.get(k, 0); d = v - tg
        flag = "" if abs(d) < max(15, 0.03 * max(tg, 1)) else "  <-- CHECK"
        if flag: ok = False
        print(f"{k:18} {v:10.0f} {tg:10.0f} {d:8.0f}{flag}")
    addressable = cat.get("physical", 0) + cat.get("residual", 0)
    print(f"  addressable (phys+resid) = {addressable:.0f} | modular(entity) = {modular:.0f} | vls = {vls:.0f}")
    print(f"  buckets: " + ", ".join(f"{k}={buck.get(k,0):.0f}" for k in BUCKETS))
    print(f"  STATUS: {'OK' if ok else 'DELTAS PRESENT'}")
