#!/usr/bin/env python3
"""
Pull FPDS Atom Feed records for the major submarine primes + named GFE/sub vendors,
plus by-PIID sweeps for the known major submarine contract vehicles.

Per-mod records are PRESERVED (not deduped) so we can later compute annual obligation
deltas from per-mod obligatedAmount sums by signed-date FY.

Output:
  fpds_raw/<slug>_raw.json     -- per-query records
  fpds_raw/_summary.json       -- counts and totals per query
  fpds_raw/_pull_log.txt       -- timing/progress log

Vendor names tested per Federal_Procurement_Research_Lessons_Learned.md section 2:
  VENDOR_NAME:"..."  works reliably; UEI_NAME variants do not.

PIID lookup does NOT work directly in FPDS Atom (per lessons learned), so by-PIID
sweeps use vendor + signed-date + PIID substring filter in Python.
"""
import json
import os
import re
import sys
import time
from collections import defaultdict
from urllib import parse
from urllib.request import urlopen, Request
from xml.etree.ElementTree import fromstring

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "ns1": "https://www.fpds.gov/FPDS",
}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "sub-outsourcing-research/1.0"}

OUT_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/fpds_raw"
os.makedirs(OUT_DIR, exist_ok=True)

# Date window. Goes back far enough to capture the still-active Block IV Virginia
# master (signed 2014) and Columbia Build I master (signed 2017), but window for
# "annual" rollup will be sliced by signed_date FY downstream.
DATE_WINDOW = "SIGNED_DATE:[2018/01/01,2026/12/31]"
NAVY_FILTER = 'CONTRACTING_AGENCY_ID:"1700"'

# Per-mod amount floor — set to 0 to keep everything; raise to drop noise.
MIN_RECORDS_KEPT = 0


# (slug, label, [queries], notes)
# Each query gets DATE_WINDOW appended. Most are vendor-name searches
# narrowed to the Navy contracting agency where appropriate.
QUERIES = [
    ("gdeb_navy", "GD Electric Boat — all Navy contracts FY18+", [
        f'VENDOR_NAME:"ELECTRIC BOAT" {NAVY_FILTER}',
        f'VENDOR_NAME:"GENERAL DYNAMICS ELECTRIC BOAT" {NAVY_FILTER}',
    ], "Prime of record for Virginia + Columbia. Includes some misc Navy work."),

    ("hii_nns_navy", "HII Newport News — all Navy contracts FY18+ (mostly CVN, but check for sub work)", [
        f'VENDOR_NAME:"NEWPORT NEWS SHIPBUILDING" {NAVY_FILTER}',
        f'VENDOR_NAME:"HUNTINGTON INGALLS INCORPORATED" {NAVY_FILTER}',
    ], "Most NNS Navy work is CVN refueling/RCOH; submarine work flows through GDEB teaming."),

    ("bpmi_navy", "Bechtel Plant Machinery — Naval Reactors FY18+", [
        f'VENDOR_NAME:"BECHTEL PLANT MACHINERY" {NAVY_FILTER}',
        f'VENDOR_NAME:"BECHTEL PLANT MACHINERY, INC." {NAVY_FILTER}',
    ], "S9G reactor components (Virginia); Columbia reactor components; GFE."),

    ("lockheed_navy_sub", "Lockheed Martin — Navy submarine-related FY18+", [
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VIRGINIA"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"COLUMBIA"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SUBMARINE"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"TRIDENT"',
    ], "LM Virginia combat systems hardware/software; Trident D5/D5LE2 for Columbia."),

    ("northrop_navy_sub", "Northrop Grumman — Navy submarine-related FY18+", [
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SUBMARINE"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VIRGINIA"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"COLUMBIA"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SONAR"',
    ], "Sonar arrays, EW (AN/BLQ-10), combat systems."),

    ("bae_navy_sub", "BAE Systems — Navy submarine subassemblies FY18+", [
        f'VENDOR_NAME:"BAE SYSTEMS LAND" {NAVY_FILTER}',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SUBASSEMBLY"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VIRGINIA"',
    ], "BAE Systems Land & Armaments builds forward subassemblies (per prior analysis)."),

    ("l3harris_navy_sub", "L3Harris — submarine periscopes & electronics FY18+", [
        f'VENDOR_NAME:"L3HARRIS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SUBMARINE"',
        f'VENDOR_NAME:"L3HARRIS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"PHOTONIC"',
        f'VENDOR_NAME:"L3 TECHNOLOGIES" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SUBMARINE"',
        f'VENDOR_NAME:"KOLLMORGEN" {NAVY_FILTER}',
    ], "Photonic masts (replaced periscopes on Virginia)."),

    ("curtiss_wright_navy", "Curtiss-Wright — Navy nuclear FY18+", [
        f'VENDOR_NAME:"CURTISS-WRIGHT" {NAVY_FILTER}',
        f'VENDOR_NAME:"CURTISS WRIGHT" {NAVY_FILTER}',
    ], "Nuclear pumps, valves; major submarine component supplier."),

    ("rolls_royce_navy_sub", "Rolls-Royce — Navy submarine rotors FY18+", [
        f'VENDOR_NAME:"ROLLS-ROYCE" {NAVY_FILTER}',
        f'VENDOR_NAME:"ROLLS ROYCE" {NAVY_FILTER}',
    ], "Submarine main engine/rotor components."),

    ("blueforge_navy", "BlueForge Alliance — MIB consortium FY22+", [
        f'VENDOR_NAME:"BLUEFORGE ALLIANCE" {NAVY_FILTER}',
        f'VENDOR_NAME:"BLUE FORGE" {NAVY_FILTER}',
    ], "Maritime Industrial Base supplier-development consortium. Real flow-through to small shops."),

    # ---- Description-keyword Round-1 sweeps for completeness (catch new PIIDs) ----
    ("desc_virginia_class", "DESCRIPTION:VIRGINIA CLASS sweep Navy FY18+", [
        f'DESCRIPTION_OF_REQUIREMENT:"VIRGINIA CLASS" {NAVY_FILTER}',
    ], "Catches anything with Virginia Class in description regardless of vendor."),

    ("desc_columbia_class", "DESCRIPTION:COLUMBIA CLASS sweep Navy FY18+", [
        f'DESCRIPTION_OF_REQUIREMENT:"COLUMBIA CLASS" {NAVY_FILTER}',
        f'DESCRIPTION_OF_REQUIREMENT:"COLUMBIA SSBN" {NAVY_FILTER}',
    ], "Catches anything with Columbia Class in description."),

    ("desc_submarine_navy_big", "DESCRIPTION:SUBMARINE Navy $50M+ floor sweep FY18+", [
        f'DESCRIPTION_OF_REQUIREMENT:"SUBMARINE" {NAVY_FILTER} OBLIGATED_AMOUNT:[50000000,99999999999]',
    ], "Round-3 backstop per lessons learned: agency + dollar-floor catches new vehicles."),
]


def fetch(url, tries=3):
    for attempt in range(tries):
        try:
            req = Request(url, headers=HDRS)
            with urlopen(req, timeout=90) as r:
                return r.read().decode("utf-8")
        except Exception as e:
            if attempt == tries - 1:
                print(f"    FAIL: {e}", flush=True)
                return None
            time.sleep(2 ** attempt)
    return None


def parse_total_pages(xml_text):
    m = re.search(r'rel="last".*?start=(\d+)', xml_text)
    return (int(m.group(1)) // 10) + 1 if m else 1


def extract_field(elem, path):
    f = elem.find(path, NS)
    return f.text if f is not None and f.text else None


def extract_attr(elem, path, attr):
    f = elem.find(path, NS)
    return f.get(attr) if f is not None else None


def extract_entries(xml_text):
    try:
        root = fromstring(xml_text)
    except Exception as e:
        print(f"    XML parse error: {e}", flush=True)
        return []
    out = []
    for entry in root.findall("a:entry", NS):
        content = entry.find("a:content", NS)
        if content is None:
            continue
        award = content.find(".//ns1:award", NS)
        ot_award = content.find(".//ns1:OtherTransactionAward", NS)
        ot_idv = content.find(".//ns1:OtherTransactionIDV", NS)
        idv = content.find(".//ns1:IDV", NS)
        elem = award or ot_award or ot_idv or idv
        if elem is None:
            continue
        record_type = (
            "award" if award is not None else
            "OtherTransactionAward" if ot_award is not None else
            "OtherTransactionIDV" if ot_idv is not None else
            "IDV"
        )

        direct_piid = None
        for p in (
            ".//ns1:awardContractID/ns1:PIID",
            ".//ns1:OtherTransactionAwardContractID/ns1:PIID",
            ".//ns1:OtherTransactionIDVContractID/ns1:PIID",
            ".//ns1:IDVID/ns1:PIID",
        ):
            direct_piid = extract_field(elem, p)
            if direct_piid:
                break
        ref_idv = extract_field(elem, ".//ns1:referencedIDVID/ns1:PIID")
        piid = direct_piid
        full_piid = f"{ref_idv}/{direct_piid}" if (ref_idv and direct_piid and ref_idv != direct_piid) else direct_piid

        out.append({
            "record_type": record_type,
            "piid": piid,
            "referenced_idv_piid": ref_idv,
            "full_piid": full_piid,
            "mod_number": extract_field(elem, ".//ns1:modNumber") or "",
            "vendor_name": extract_field(elem, ".//ns1:vendorName"),
            "vendor_alt_name": extract_field(elem, ".//ns1:vendorAlternateName"),
            "vendor_uei": extract_field(elem, ".//ns1:UEI"),
            "this_obligated": float(extract_field(elem, ".//ns1:obligatedAmount") or 0),
            "total_obligated": float(extract_field(elem, ".//ns1:totalObligatedAmount") or 0),
            "base_and_exercised": float(extract_field(elem, ".//ns1:baseAndExercisedOptionsValue") or 0),
            "base_and_all_options": float(extract_field(elem, ".//ns1:baseAndAllOptionsValue") or 0),
            "total_base_and_all_options": float(extract_field(elem, ".//ns1:totalBaseAndAllOptionsValue") or 0),
            "signed_date": extract_field(elem, ".//ns1:signedDate"),
            "effective_date": extract_field(elem, ".//ns1:effectiveDate"),
            "current_completion_date": extract_field(elem, ".//ns1:currentCompletionDate"),
            "ultimate_completion_date": extract_field(elem, ".//ns1:ultimateCompletionDate"),
            "fiscal_year": extract_field(elem, ".//ns1:fiscalYear"),
            "contracting_agency_id": extract_attr(elem, ".//ns1:contractingOfficeAgencyID", "name"),
            "contracting_office_id": extract_attr(elem, ".//ns1:contractingOfficeID", "name"),
            "funding_agency_id": extract_attr(elem, ".//ns1:fundingRequestingAgencyID", "name"),
            "funding_office_id": extract_attr(elem, ".//ns1:fundingRequestingOfficeID", "name"),
            "naics": extract_field(elem, ".//ns1:principalNAICSCode"),
            "naics_desc": extract_attr(elem, ".//ns1:principalNAICSCode", "description"),
            "psc": extract_field(elem, ".//ns1:productOrServiceCode"),
            "psc_desc": extract_attr(elem, ".//ns1:productOrServiceCode", "description"),
            "contract_action_type": extract_attr(elem, ".//ns1:contractActionType", "description"),
            "pricing_type": extract_attr(elem, ".//ns1:typeOfContractPricing", "description"),
            "extent_competed": extract_attr(elem, ".//ns1:extentCompeted", "description"),
            "description": (extract_field(elem, ".//ns1:descriptionOfContractRequirement") or "")[:800],
            "pop_state_code": extract_field(elem, ".//ns1:placeOfPerformance/ns1:principalPlaceOfPerformance/ns1:stateCode"),
            "pop_state_name": extract_attr(elem, ".//ns1:placeOfPerformance/ns1:principalPlaceOfPerformance/ns1:stateCode", "name"),
            "pop_country_code": extract_field(elem, ".//ns1:placeOfPerformance/ns1:principalPlaceOfPerformance/ns1:countryCode"),
            "pop_city": extract_attr(elem, ".//ns1:placeOfPerformance/ns1:placeOfPerformanceZIPCode", "city"),
            "pop_county": extract_attr(elem, ".//ns1:placeOfPerformance/ns1:placeOfPerformanceZIPCode", "county"),
            "pop_zip": extract_field(elem, ".//ns1:placeOfPerformance/ns1:placeOfPerformanceZIPCode"),
            "pop_congressional_district": extract_field(elem, ".//ns1:placeOfPerformance/ns1:placeOfPerformanceCongressionalDistrict"),
        })
    return out


def fpds_paginate(q, max_pages=300, log_fn=print):
    records = []
    start = 0
    total_pages = None
    pages_fetched = 0
    while True:
        url = f"{BASE}&{parse.urlencode({'q': q})}&start={start}"
        text = fetch(url)
        if text is None:
            break
        if total_pages is None:
            total_pages = parse_total_pages(text)
            log_fn(f"    ~{total_pages} pages ({total_pages*10} records max) for: {q[:80]}")
            if total_pages > max_pages:
                log_fn(f"    !! capping at {max_pages} pages")
        recs = extract_entries(text)
        records.extend(recs)
        pages_fetched += 1
        if not recs:
            break
        start += 10
        if start // 10 >= min(total_pages, max_pages):
            break
        if pages_fetched % 25 == 0:
            log_fn(f"    ...{pages_fetched} pages, {len(records)} records so far")
        time.sleep(0.35)
    return records


def main():
    log_path = os.path.join(OUT_DIR, "_pull_log.txt")
    summary = {}
    slug_filter = sys.argv[1] if len(sys.argv) > 1 else None

    with open(log_path, "w") as logf:
        def log(msg):
            print(msg, flush=True)
            logf.write(msg + "\n")
            logf.flush()

        log(f"=== FPDS pull started {time.strftime('%Y-%m-%d %H:%M:%S')}")
        log(f"DATE_WINDOW={DATE_WINDOW}")
        for slug, label, queries, notes in QUERIES:
            if slug_filter and slug != slug_filter:
                continue
            log(f"\n--- [{slug}] {label}")
            log(f"    notes: {notes}")
            all_records = []
            seen = set()
            for q_base in queries:
                q = f"{q_base} {DATE_WINDOW}"
                recs = fpds_paginate(q, max_pages=300, log_fn=log)
                log(f"    -> {len(recs)} records from this query")
                for r in recs:
                    sig = (r.get("full_piid") or r.get("piid"), r.get("mod_number"), r.get("signed_date"))
                    if sig in seen:
                        continue
                    seen.add(sig)
                    all_records.append(r)
            log(f"    [{slug}] {len(all_records)} unique (PIID,mod,signed_date) records total")
            if all_records:
                # quick aggregate: top vendors by total_obligated on latest mod per PIID
                by_piid = {}
                for r in all_records:
                    p = r.get("full_piid") or r.get("piid")
                    if not p:
                        continue
                    prev = by_piid.get(p)
                    if prev is None or (r.get("signed_date") or "") > (prev.get("signed_date") or ""):
                        by_piid[p] = r
                by_vendor = defaultdict(lambda: {"total_obligated": 0.0, "ceiling": 0.0, "piid_count": 0})
                for r in by_piid.values():
                    v = (r.get("vendor_name") or "").upper().strip()
                    if not v:
                        continue
                    by_vendor[v]["total_obligated"] += r.get("total_obligated") or 0
                    by_vendor[v]["ceiling"] += r.get("total_base_and_all_options") or 0
                    by_vendor[v]["piid_count"] += 1
                top = sorted(by_vendor.items(), key=lambda kv: kv[1]["total_obligated"], reverse=True)[:10]
                log("    TOP VENDORS (latest-mod totalObligated):")
                for v, a in top:
                    log(f"      {v[:50]:50s}  ${a['total_obligated']/1e6:>12,.1f}M  {a['piid_count']:>4d} PIIDs")

            # save raw
            out_path = os.path.join(OUT_DIR, f"{slug}_raw.json")
            with open(out_path, "w") as f:
                json.dump({
                    "label": label,
                    "notes": notes,
                    "queries": queries,
                    "date_window": DATE_WINDOW,
                    "record_count": len(all_records),
                    "records": all_records,
                }, f, indent=2, default=str)
            summary[slug] = {
                "label": label,
                "queries": queries,
                "record_count": len(all_records),
                "unique_piids": len(by_piid) if all_records else 0,
                "output_file": out_path,
            }

        summary_path = os.path.join(OUT_DIR, "_summary.json")
        with open(summary_path, "w") as f:
            json.dump({
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "date_window": DATE_WINDOW,
                "navy_filter": NAVY_FILTER,
                "queries": summary,
            }, f, indent=2)
        log(f"\nWrote summary -> {summary_path}")


if __name__ == "__main__":
    main()
