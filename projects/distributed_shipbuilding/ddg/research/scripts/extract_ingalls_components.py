#!/usr/bin/env python3
"""Mine the DDG subawardDescription component text from the raw SAM corpus.

The work-type classification pipeline deliberately discards subawardDescription
(it's "see below" junk for submarines). But for HII-Ingalls DDG hulls ~64% of
descriptions carry a usable component phrase behind a shipyard line-item code
(e.g. "01021-01 STRUCTURAL DOORS", "03063-01 BLEED AIR COOLERS"). This script
parses that field out of the raw subaward JSON we already pulled (no API call -
the by-PIID SAM endpoint now returns empty anyway) into a structured table that
could become a secondary, finer-than-NAICS capability tag for DDG lanes.

Reads:  ../sam_subawards_fullhistory/*_subawards.json   (raw SAM pull, verbatim)
Writes: ../ingalls_subaward_components.csv               (one row per subaward)
        ../ingalls_vendor_capabilities.csv               (per-vendor roll-up)
"""
from __future__ import annotations

import csv
import glob
import json
import os
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "sam_subawards_fullhistory")
OUT_ROWS = os.path.join(HERE, "..", "ingalls_subaward_components.csv")
OUT_VEND = os.path.join(HERE, "..", "ingalls_vendor_capabilities.csv")
OUT_CODE = os.path.join(HERE, "..", "ingalls_code_dictionary.csv")

# HII-Ingalls PIIDs (the others in the DDG corpus are GD-BIW); only Ingalls uses
# the NNNNN-NN line-item convention.
HII = {"N0002402C2304", "N0002411C2307", "N0002411C2309", "N0002412C2312",
       "N0002413C2307", "N0002418C2307", "N0002423C2307"}

CODE = re.compile(r"\b(\d{5}-\d{2})\b")                   # shipyard work-item code (ANYWHERE, not just start)
PS = re.compile(r"\bN?CSE\s+PS\s+(\d{3})-\d+[A-Z]?", re.I)  # CSE/NCSE purchase spec -> SWBS group
HULL = re.compile(r"\bDD?G?\s?\d{2,3}\b|\(DD\d+\)", re.I)   # hull / DD250 delivery tags
PAREN = re.compile(r"\([^)]*\)")
# admin / code tokens that are NOT component words
STOP = {"CSE", "NCSE", "PS", "FMR", "COSAL", "SRI", "NCR", "DD", "DDG", "REV",
        "QTY", "EA", "LOT", "FY", "CLIN", "PO", "REF", "SEE", "BELOW", "COMPLETE",
        "DESCRIPTION", "REMARKS", "TEXT", "ITEM", "VARIOUS", "MISC", "TBD", "TMR",
        "REBUY", "RTV", "LDD", "NES", "ES", "FOR", "AND", "THE", "WITH", "PER",
        "OF", "TO", "ON", "DEFIN", "WF", "HHIP"}


def fy(date: str) -> int | str:
    if not date or len(date) < 7:
        return ""
    y, m = int(date[:4]), int(date[5:7])
    return y + 1 if m >= 10 else y


def parse(desc: str) -> dict:
    """Return {code, family, swbs, hull, component, n_words} for a description.

    The HII work-item code can sit ANYWHERE - it is often behind a hull prefix,
    e.g. "DDG 146 03013-01 CSE PS 234-01B" - so search the whole string. Anchoring
    on ^ (the first cut) missed 533 rows / ~$877M: 64% -> 90% of HII dollars once
    the code is found anywhere. The PS spec is \\d{3}-..., so the \\d{5}-\\d{2}
    work-item pattern never collides with it."""
    d = (desc or "").strip()
    m = CODE.search(d)
    code = m.group(1) if m else ""
    family = code[:2] if code else ""
    swbs = ps.group(1) if (ps := PS.search(d)) else ""
    hull = (h.group(0) if (h := HULL.search(d)) else "").strip()
    # strip the structured tokens (the work-item code wherever it is, the hull
    # tag, the PS spec, parentheticals), keep the free-text remainder.
    rest = CODE.sub(" ", d)
    rest = PS.sub(" ", rest)
    rest = HULL.sub(" ", rest)
    rest = PAREN.sub(" ", rest)
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z&/-]{2,}", rest)
             if w.upper() not in STOP]
    component = " ".join(words).strip()
    return {"code": code, "family": family, "swbs": swbs, "hull": hull,
            "component": component, "n_words": len(words)}


def main() -> int:
    rows = []
    seen = set()
    for f in sorted(glob.glob(os.path.join(RAW, "*_subawards.json"))):
        piid = os.path.basename(f).replace("_subawards.json", "")
        builder = "HII-Ingalls" if piid in HII else "GD-BIW"
        data = json.load(open(f))
        for r in data.get("published", []):
            rid = r.get("subAwardReportId")
            if rid in seen:
                continue
            seen.add(rid)
            desc = (r.get("subawardDescription") or "").strip()
            p = parse(desc)
            rows.append({
                "piid": piid, "builder": builder, "sub_report_id": rid,
                "sub_date": r.get("subAwardDate", ""), "fy": fy(r.get("subAwardDate", "")),
                "amount_usd": float(r.get("subAwardAmount") or 0),
                "vendor_uei": r.get("subEntityUei", ""),
                "parent_uei": r.get("subParentUei", "") or "",
                "vendor_name": r.get("subEntityLegalBusinessName", ""),
                "raw_description": desc,
                "code": p["code"], "family": p["family"], "swbs_group": p["swbs"],
                "hull": p["hull"], "component_text": p["component"],
                "n_component_words": p["n_words"],
            })

    with open(OUT_ROWS, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    # per-vendor capability roll-up (HII only, where the tag exists)
    vend = defaultdict(lambda: {"name": "", "n": 0, "usd": 0.0, "comp": Counter()})
    for r in rows:
        if r["builder"] != "HII-Ingalls":
            continue
        v = vend[r["vendor_uei"]]
        v["name"] = r["vendor_name"]; v["n"] += 1; v["usd"] += r["amount_usd"]
        if r["component_text"]:
            v["comp"][r["component_text"]] += 1
    with open(OUT_VEND, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["vendor_uei", "vendor_name", "n_subawards", "total_usd",
                    "n_distinct_components", "top_components"])
        for uei, v in sorted(vend.items(), key=lambda kv: -kv[1]["usd"]):
            top = "; ".join(c for c, _ in v["comp"].most_common(6))
            w.writerow([uei, v["name"], v["n"], round(v["usd"], 2),
                        len(v["comp"]), top])

    # per-CODE dictionary (HII) - the curatable basis: a code recurs across hulls
    # and vendors, so top-N codes by $ are a hand-curatable code -> work-type map.
    code_agg = defaultdict(lambda: {"n": 0, "usd": 0.0, "family": "",
                                    "swbs": Counter(), "comp": Counter()})
    for r in rows:
        if r["builder"] != "HII-Ingalls" or not r["code"]:
            continue
        c = code_agg[r["code"]]
        c["n"] += 1; c["usd"] += r["amount_usd"]; c["family"] = r["family"]
        if r["swbs_group"]:
            c["swbs"][r["swbs_group"]] += 1
        if r["component_text"]:
            c["comp"][r["component_text"]] += 1
    with open(OUT_CODE, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["code", "family", "n_subawards", "total_usd",
                    "modal_swbs_group", "top_components"])
        for code, c in sorted(code_agg.items(), key=lambda kv: -kv[1]["usd"]):
            sw = c["swbs"].most_common(1)[0][0] if c["swbs"] else ""
            top = "; ".join(p for p, _ in c["comp"].most_common(4))
            w.writerow([code, c["family"], c["n"], round(c["usd"], 2), sw, top])

    # ---- console report -------------------------------------------------
    hii = [r for r in rows if r["builder"] == "HII-Ingalls"]
    biw = [r for r in rows if r["builder"] == "GD-BIW"]
    def pct(rs, key):
        return sum(1 for r in rs if r[key]) / max(len(rs), 1)
    print(f"deduped DDG subawards: {len(rows)}  (HII-Ingalls {len(hii)}, GD-BIW {len(biw)})")
    print(f"\nHII-Ingalls coverage:")
    print(f"  NNNNN-NN line code present : {pct(hii,'code'):.0%}")
    print(f"  >=1 component word         : {sum(1 for r in hii if r['n_component_words']>=1)/max(len(hii),1):.0%}")
    print(f"  >=2 component words        : {sum(1 for r in hii if r['n_component_words']>=2)/max(len(hii),1):.0%}")
    print(f"  CSE/NCSE PS (SWBS) tag     : {pct(hii,'swbs_group'):.0%}")
    print(f"GD-BIW NNNNN-NN present     : {pct(biw,'code'):.0%}  (expected ~0)")

    fam = defaultdict(Counter)
    for r in hii:
        if r["family"] and r["component_text"]:
            fam[r["family"]][r["component_text"]] += 1
    print(f"\nleading 2-digit family -> top component phrases (HII):")
    for f2 in sorted(fam, key=lambda k: -sum(fam[k].values()))[:8]:
        tops = "; ".join(c for c, _ in fam[f2].most_common(3))
        print(f"  {f2}xxx : {tops[:90]}")

    print(f"\ntop HII vendors by $ + their component tags:")
    for uei, v in sorted(vend.items(), key=lambda kv: -kv[1]["usd"])[:10]:
        top = "; ".join(c for c, _ in v["comp"].most_common(4)) or "(none parsed)"
        print(f"  {v['name'][:32]:32s} ${v['usd']/1e6:6.1f}M  {top[:70]}")

    coded = [r for r in hii if r["code"]]
    coded_usd = sum(r["amount_usd"] for r in coded)
    hii_usd = sum(r["amount_usd"] for r in hii)
    by_code_usd = sorted((c["usd"] for c in code_agg.values()), reverse=True)
    def topshare(n):
        return sum(by_code_usd[:n]) / max(hii_usd, 1)
    print(f"\ncode dictionary: {len(code_agg)} distinct HII codes cover "
          f"${coded_usd/1e6:,.0f}M ({coded_usd/hii_usd:.1%} of HII $)")
    print(f"  top-50 codes = {topshare(50):.1%} of HII $   top-100 = {topshare(100):.1%}")
    print(f"  top codes by $ (code | $ | modal SWBS | components):")
    for code, c in sorted(code_agg.items(), key=lambda kv: -kv[1]["usd"])[:8]:
        sw = c["swbs"].most_common(1)[0][0] if c["swbs"] else "--"
        top = "; ".join(p for p, _ in c["comp"].most_common(2)) or "(code-only)"
        print(f"    {code}  ${c['usd']/1e6:6.1f}M  SWBS {sw}  {top[:46]}")

    print(f"\nwrote {OUT_ROWS}\nwrote {OUT_VEND}\nwrote {OUT_CODE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
