#!/usr/bin/env python3
"""
Extend the per-program SAM entity NAICS lookups using the unclassified queue (Phase B2).

Reads coverage_unclassified_top.csv (from measure_classification_coverage.py) and,
per program, looks up the top-N unbucketed vendors' UEIs against the SAM Entity
Management API — entity UEI first, parent UEI as fallback when the entity record is
absent. Results cache one-file-per-UEI into the program's existing
research/sam_entity_lookups/ dir and are APPENDED to the program's
research/extracted/entity_naics_lookup.csv (the enrichment _corpus.py reads).

The program workbooks' extracted/ copies are deliberately NOT touched — improving
enrichment there would silently move live workbook/deck numbers; that change is for
the user to take deliberately after the findings review.

Endpoint and curl-subprocess pattern follow scripts/pull_sam_entity_naics.py in the
program research dirs (curl avoids the macOS IPv6 stall; samRegistered=Yes only —
the =No branch is a full-dataset scan and brutally slow).

Usage: python3 extend_entity_lookups.py [--top-n 150] [--programs submarines,ddg]
"""
from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _corpus import EXTRACTED, PROGRAMS, REPO

BASE = "https://api.sam.gov/entity-information/v3/entities"
UA = "consolidated-competability-research/1.0"

CACHE_DIRS = {
    "submarines": REPO / "projects/distributed_shipbuilding/submarines/research/sam_entity_lookups",
    "ddg": REPO / "projects/distributed_shipbuilding/ddg/research/sam_entity_lookups",
}

NAICS_SECTORS = {
    "11": "Agriculture, Forestry, Fishing", "21": "Mining, Oil & Gas",
    "22": "Utilities", "23": "Construction",
    "31": "Manufacturing — Food/Beverage/Apparel",
    "32": "Manufacturing — Chemicals/Plastics/Metals",
    "33": "Manufacturing — Machinery/Electronics/Transport Eq",
    "42": "Wholesale Trade", "44": "Retail Trade", "45": "Retail Trade",
    "48": "Transportation", "49": "Transportation/Warehousing",
    "51": "Information", "52": "Finance & Insurance", "53": "Real Estate & Rental",
    "54": "Professional/Scientific/Technical Services",
    "55": "Management of Companies", "56": "Admin/Support/Waste/Remediation",
    "61": "Educational Services", "62": "Health Care",
    "71": "Arts/Entertainment/Recreation", "72": "Accommodation & Food Service",
    "81": "Other Services", "92": "Public Administration",
}


def load_key():
    for line in (REPO / ".env").read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip()
    raise SystemExit("SAM_API_KEY not in .env")


def call_entity(api_key, uei):
    params = {"api_key": api_key, "ueiSAM": uei, "samRegistered": "Yes"}
    url = f"{BASE}?{urlencode(params)}"
    try:
        result = subprocess.run(
            ["curl", "-sS", "--max-time", "30", "-A", UA, url],
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


def cached_lookup(api_key, cache_dir: Path, uei: str, vendor: str):
    """Return the raw entity body for a UEI, fetching + caching when absent."""
    cache_path = cache_dir / f"{uei}.json"
    if cache_path.exists():
        return json.load(open(cache_path)).get("body"), False
    body = call_entity(api_key, uei)
    json.dump({"uei": uei, "vendor": vendor, "body": body}, open(cache_path, "w"))
    time.sleep(0.2)
    return body, True


def body_to_row(uei, vendor, body):
    if not body or not body.get("entityData"):
        return {"uei": uei, "vendor": vendor, "primary_naics": "", "naics_desc": "",
                "naics_2digit": "", "naics_4digit": "", "naics_sector_label": "Unknown",
                "cage": "", "country": "", "lookup_status": "not_found"}
    e = body["entityData"][0]
    gs = (e.get("assertions") or {}).get("goodsAndServices") or {}
    primary = gs.get("primaryNaics") or ""
    desc = ""
    for item in gs.get("naicsList") or []:
        if item.get("naicsCode") == primary:
            desc = item.get("naicsDescription") or ""
            break
    if not desc and gs.get("naicsList"):
        desc = gs["naicsList"][0].get("naicsDescription") or ""
    cage = (e.get("entityRegistration") or {}).get("cageCode") or ""
    country = ((e.get("coreData") or {}).get("physicalAddress") or {}).get("countryCode", "")
    return {"uei": uei, "vendor": vendor, "primary_naics": primary,
            "naics_desc": desc, "naics_2digit": primary[:2], "naics_4digit": primary[:4],
            "naics_sector_label": NAICS_SECTORS.get(primary[:2], "Unknown"),
            "cage": cage, "country": country, "lookup_status": "ok"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top-n", type=int, default=150)
    ap.add_argument("--programs", default="submarines,ddg")
    args = ap.parse_args()
    api_key = load_key()

    queue_path = EXTRACTED / "coverage_unclassified_top.csv"
    with queue_path.open(encoding="utf-8-sig", newline="") as fh:
        queue = list(csv.DictReader(fh))

    for program in [p.strip() for p in args.programs.split(",") if p.strip()]:
        cache_dir = CACHE_DIRS[program]
        cache_dir.mkdir(exist_ok=True)
        lookup_csv = Path(PROGRAMS[program]["naics_csv"])
        with lookup_csv.open(encoding="utf-8-sig", newline="") as fh:
            reader = csv.DictReader(fh)
            fields = reader.fieldnames
            existing = list(reader)
        known = {r["uei"] for r in existing}

        rows = [r for r in queue if r["program"] == program][:args.top_n]
        print(f"\n[{program}] queue top {len(rows)}; {len(known)} UEIs already enriched")
        added, fetched, nf = [], 0, 0
        for i, q in enumerate(rows, start=1):
            vendor = q["vendor_name"]
            # entity UEI first (operating-entity NAICS), parent as fallback
            tried_ok = False
            for uei in (q["entity_uei"], q["parent_uei"]):
                uei = (uei or "").strip()
                if not uei or uei in known:
                    continue
                body, was_fetch = cached_lookup(api_key, cache_dir, uei, vendor)
                fetched += was_fetch
                row = body_to_row(uei, vendor, body)
                row["rank"] = ""
                row["amount_M_lifetime"] = q["dollars_all_$M"]
                added.append(row)
                known.add(uei)
                if row["lookup_status"] == "ok":
                    tried_ok = True
                    break  # entity record found; parent fallback unnecessary
                nf += 1
            if i % 25 == 0 or i == len(rows):
                print(f"  {i:>4}/{len(rows)}  new_rows={len(added)}  fetched={fetched}  not_found={nf}",
                      flush=True)
            _ = tried_ok

        if added:
            with lookup_csv.open("a", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=fields)
                for r in added:
                    w.writerow({k: r.get(k, "") for k in fields})
        ok = sum(1 for r in added if r["lookup_status"] == "ok")
        print(f"[{program}] appended {len(added)} rows to {lookup_csv} "
              f"(ok={ok}, not_found={len(added) - ok})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
