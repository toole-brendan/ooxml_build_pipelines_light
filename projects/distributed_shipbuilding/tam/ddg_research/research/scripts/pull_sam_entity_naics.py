#!/usr/bin/env python3
"""
Enrich each in-scope parent UEI with its primary NAICS code via SAM Entity Management API.

Endpoint: https://api.sam.gov/entity-information/v3/entities
Filter:   api_key=<key>&ueiSAM=<UEI>&samRegistered=Yes
NAICS at: assertions.goodsAndServices.primaryNaics + naicsList[0].naicsDescription

Strategy:
  - read extracted/nc_lifetime_vendors.csv (produced by aggregate_new_construction.py)
  - take top-N by amount (default 150 to cover ~90% of $)
  - cache results to sam_entity_lookups/<uei>.json (one file per UEI for audit + resumability)
  - emit extracted/entity_naics_lookup.csv with: uei, vendor, primary_naics, naics_desc,
    naics_2digit, naics_4digit, naics_sector_label, status, cage_code, country
  - fallback: if samRegistered=Yes empty, skip (the No branch is too slow to use)

Quota: ~1,000/day on entity-role keys.  150 calls fits easily in one session.
"""
import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

REPO = Path("/Users/brendantoole/projects2/destroyer_outsourced_work")
CACHE = REPO / "sam_entity_lookups"
CACHE.mkdir(exist_ok=True)
OUT = REPO / "extracted"

BASE = "https://api.sam.gov/entity-information/v3/entities"
HDRS = {"User-Agent": "ddg-outsourcing-research/1.0", "Accept": "application/json"}

TOP_N = 150


def load_key():
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SAM_API_KEY not in .env")


NAICS_SECTORS = {
    "11": "Agriculture, Forestry, Fishing",
    "21": "Mining, Oil & Gas",
    "22": "Utilities",
    "23": "Construction",
    "31": "Manufacturing — Food/Beverage/Apparel",
    "32": "Manufacturing — Chemicals/Plastics/Metals",
    "33": "Manufacturing — Machinery/Electronics/Transport Eq",
    "42": "Wholesale Trade",
    "44": "Retail Trade",
    "45": "Retail Trade",
    "48": "Transportation",
    "49": "Transportation/Warehousing",
    "51": "Information",
    "52": "Finance & Insurance",
    "53": "Real Estate & Rental",
    "54": "Professional/Scientific/Technical Services",
    "55": "Management of Companies",
    "56": "Admin/Support/Waste/Remediation",
    "61": "Educational Services",
    "62": "Health Care",
    "71": "Arts/Entertainment/Recreation",
    "72": "Accommodation & Food Service",
    "81": "Other Services",
    "92": "Public Administration",
}


def call_entity(api_key, uei, sam_registered="Yes"):
    """Single Entity Management lookup via curl subprocess.

    Why curl: urllib on macOS appears to hit IPv6 fallback delay or similar
    slowness against api.sam.gov; curl is fast.
    """
    params = {"api_key": api_key, "ueiSAM": uei, "samRegistered": sam_registered}
    url = f"{BASE}?{urlencode(params)}"
    try:
        result = subprocess.run(
            ["curl", "-sS", "--max-time", "30", "-A", HDRS["User-Agent"], url],
            capture_output=True, text=True, timeout=35,
        )
        if result.returncode != 0:
            print(f"   curl rc={result.returncode} on {uei}: {result.stderr[:200]}", flush=True)
            return None
        return json.loads(result.stdout) if result.stdout else None
    except subprocess.TimeoutExpired:
        print(f"   timeout on {uei}", flush=True)
        return None
    except json.JSONDecodeError as e:
        print(f"   bad JSON on {uei}: {e}", flush=True)
        return None


def extract_naics(entity_data):
    if not entity_data:
        return None, None, None
    gs = (entity_data.get("assertions") or {}).get("goodsAndServices") or {}
    primary = gs.get("primaryNaics")
    description = None
    if primary and gs.get("naicsList"):
        for item in gs["naicsList"]:
            if item.get("naicsCode") == primary:
                description = item.get("naicsDescription")
                break
    if not description and gs.get("naicsList"):
        description = gs["naicsList"][0].get("naicsDescription")
    cage = (entity_data.get("entityRegistration") or {}).get("cageCode")
    return primary, description, cage


def lookup_uei(api_key, uei, vendor_name):
    cache_path = CACHE / f"{uei}.json"
    if cache_path.exists():
        cached = json.load(open(cache_path))
        body = cached.get("body")
    else:
        body = call_entity(api_key, uei, "Yes")
        json.dump({"uei": uei, "vendor": vendor_name, "body": body}, open(cache_path, "w"))
        time.sleep(0.2)

    if not body or not body.get("entityData"):
        return {
            "uei": uei, "vendor": vendor_name,
            "primary_naics": "", "naics_desc": "",
            "naics_2digit": "", "naics_4digit": "", "naics_sector_label": "Unknown",
            "cage": "", "country": "", "lookup_status": "not_found",
        }

    e = body["entityData"][0]
    naics_code, naics_desc, cage = extract_naics(e)
    naics_code = naics_code or ""
    naics_desc = naics_desc or ""
    country = ((e.get("coreData") or {}).get("physicalAddress") or {}).get("countryCode", "")
    sector_label = NAICS_SECTORS.get(naics_code[:2], "Unknown")
    return {
        "uei": uei, "vendor": vendor_name,
        "primary_naics": naics_code,
        "naics_desc": naics_desc,
        "naics_2digit": naics_code[:2] if naics_code else "",
        "naics_4digit": naics_code[:4] if naics_code else "",
        "naics_sector_label": sector_label,
        "cage": cage or "",
        "country": country,
        "lookup_status": "ok",
    }


def main():
    api_key = load_key()

    src = OUT / "nc_lifetime_vendors.csv"
    if not src.exists():
        raise SystemExit(f"Missing {src} — run aggregate_new_construction.py first")
    with open(src) as f:
        reader = csv.DictReader(f)
        vendors = list(reader)
    target = vendors[:TOP_N]
    total_top_n = sum(float(v["amount_M_lifetime"]) for v in target)
    total_all = sum(float(v["amount_M_lifetime"]) for v in vendors)
    print(f"Top {TOP_N} vendors cover ${total_top_n:,.1f}M of ${total_all:,.1f}M "
          f"= {100*total_top_n/total_all:.1f}% of in-scope lifetime $", flush=True)
    print(f"Calling SAM Entity API for {TOP_N} UEIs…\n", flush=True)

    rows = []
    for i, v in enumerate(target, start=1):
        uei = v["uei"]
        if not uei:
            continue
        row = lookup_uei(api_key, uei, v["vendor"])
        row["rank"] = int(v["rank"])
        row["amount_M_lifetime"] = float(v["amount_M_lifetime"])
        rows.append(row)
        if i % 10 == 0 or i == len(target):
            ok = sum(1 for r in rows if r["lookup_status"] == "ok")
            nf = sum(1 for r in rows if r["lookup_status"] == "not_found")
            print(f"  {i:>3}/{TOP_N}   ok={ok}  not_found={nf}", flush=True)

    rows.sort(key=lambda r: r["rank"])
    fields = ["rank", "uei", "vendor", "amount_M_lifetime",
              "primary_naics", "naics_desc",
              "naics_2digit", "naics_4digit", "naics_sector_label",
              "cage", "country", "lookup_status"]
    with open(OUT / "entity_naics_lookup.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})

    print(f"\nWrote {OUT/'entity_naics_lookup.csv'} ({len(rows)} rows)")

    from collections import defaultdict
    by_4 = defaultdict(lambda: {"amt": 0.0, "n": 0, "label": ""})
    for r in rows:
        k = r["naics_4digit"] or "UNKN"
        by_4[k]["amt"] += r["amount_M_lifetime"]
        by_4[k]["n"] += 1
        if not by_4[k]["label"] and r["naics_desc"]:
            by_4[k]["label"] = r["naics_desc"]
    print(f"\nTop 15 NAICS 4-digit buckets across the top-{TOP_N} vendors:")
    print(f"  {'NAICS':>5}  {'vendors':>7}  {'$M':>10}  description")
    for k, v in sorted(by_4.items(), key=lambda kv: -kv[1]["amt"])[:15]:
        print(f"  {k:>5}  {v['n']:>7}  {v['amt']:>10,.1f}  {v['label'][:60]}")


if __name__ == "__main__":
    main()
