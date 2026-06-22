#!/usr/bin/env python3
"""Discover the COMPLETE set of GDEB (Electric Boat) NAVSEA submarine prime PIIDs.

Motivation: nc_scope_summary.json's in_scope_piids is a curated list (15 PIIDs); the
prior broad EB Navy FPDS sweep hit the 300-page (3000-mod) cap and silently dropped
PIIDs (e.g. the $4.3B Lead Yard Support N0002420C2120 was missing). This does a
NAICS-narrowed sweep so the mod count stays well under any cap, then aggregates to
distinct PIIDs. Construction (336611) + engineering/design (541330/541712/541715).

Keyless (FPDS Atom). Output: discover_eb_primes_fpds.json (distinct-PIID aggregates).
"""
import json, os, re, time
from collections import defaultdict
from urllib import parse
from urllib.request import urlopen, Request
from xml.etree.ElementTree import fromstring

NS = {"a": "http://www.w3.org/2005/Atom", "ns1": "https://www.fpds.gov/FPDS"}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "sub-outsourcing-research/1.0"}
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "fpds_raw", "discover_eb_primes_fpds.json")

DATE = "SIGNED_DATE:[2012/01/01,2026/12/31]"
NAVY = 'CONTRACTING_AGENCY_ID:"1700"'
QUERIES = [
    f'VENDOR_NAME:"ELECTRIC BOAT" {NAVY} PRINCIPAL_NAICS_CODE:"336611" {DATE}',
    f'VENDOR_NAME:"ELECTRIC BOAT" {NAVY} PRINCIPAL_NAICS_CODE:"541330" {DATE}',
    f'VENDOR_NAME:"ELECTRIC BOAT" {NAVY} PRINCIPAL_NAICS_CODE:"541712" {DATE}',
    f'VENDOR_NAME:"ELECTRIC BOAT" {NAVY} PRINCIPAL_NAICS_CODE:"541715" {DATE}',
]


def fetch(url, tries=3):
    for a in range(tries):
        try:
            with urlopen(Request(url, headers=HDRS), timeout=90) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            if a == tries - 1:
                print(f"   FAIL {e}"); return None
            time.sleep(2 ** a)


def total_pages(t):
    m = re.search(r'rel="last".*?start=(\d+)', t)
    return (int(m.group(1)) // 10) + 1 if m else 1


def field(e, p):
    f = e.find(p, NS); return f.text if f is not None and f.text else None


def entries(t):
    try:
        root = fromstring(t)
    except Exception as e:
        print(f"   xml err {e}"); return []
    out = []
    for entry in root.findall("a:entry", NS):
        c = entry.find("a:content", NS)
        if c is None: continue
        elem = c.find(".//ns1:award", NS) or c.find(".//ns1:IDV", NS)
        if elem is None: continue
        piid = None
        for p in (".//ns1:awardContractID/ns1:PIID", ".//ns1:IDVID/ns1:PIID"):
            piid = field(elem, p)
            if piid: break
        out.append({
            "piid": (piid or "").replace("-", "").upper(),
            "vendor": field(elem, ".//ns1:vendorName"),
            "naics": field(elem, ".//ns1:principalNAICSCode"),
            "psc": field(elem, ".//ns1:productOrServiceCode"),
            "signed_date": (field(elem, ".//ns1:signedDate") or "")[:10],
            "this_obligated": float(field(elem, ".//ns1:obligatedAmount") or 0),
            "desc": (field(elem, ".//ns1:descriptionOfContractRequirement") or "")[:90],
        })
    return out


def paginate(q, max_pages=800):
    recs, start, tp = [], 0, None
    while True:
        t = fetch(f"{BASE}&{parse.urlencode({'q': q})}&start={start}")
        if t is None: break
        if tp is None:
            tp = total_pages(t); print(f"   ~{tp} pages: {q[:70]}")
        page = entries(t)
        recs.extend(page)
        if not page: break
        start += 10
        if start // 10 >= min(tp, max_pages): break
        time.sleep(0.3)
    return recs


def main():
    agg = defaultdict(lambda: {"oblig": 0.0, "mods": 0, "sd": "", "desc": "", "naics": "", "psc": "", "vendor": ""})
    for q in QUERIES:
        for r in paginate(q):
            v = (r.get("vendor") or "").upper()
            if "ELECTRIC BOAT" not in v:   # post-filter the OR-tokenization
                continue
            p = r["piid"]
            if not p: continue
            a = agg[p]
            a["oblig"] += r["this_obligated"]; a["mods"] += 1
            if r["signed_date"] > a["sd"]:
                a["sd"] = r["signed_date"]; a["desc"] = r["desc"]; a["naics"] = r["naics"] or ""; a["psc"] = r["psc"] or ""
            a["vendor"] = v[:30]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump({"queries": QUERIES, "distinct_piids": len(agg), "piids": agg}, f, indent=2, default=str)
    print(f"\nDISTINCT EB PIIDs: {len(agg)} -> {OUT}")
    for p, a in sorted(agg.items(), key=lambda kv: -kv[1]["oblig"]):
        print(f"  {p:16} {a['oblig']/1e6:>11,.1f}M  {a['mods']:>4} mods  {a['naics']:7} {a['psc']:6} {a['sd']:11} {a['desc'][:55]}")


if __name__ == "__main__":
    main()
