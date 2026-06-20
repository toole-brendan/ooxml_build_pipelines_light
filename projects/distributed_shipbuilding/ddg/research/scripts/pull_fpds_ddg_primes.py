#!/usr/bin/env python3
"""
Pull FPDS Atom Feed records for the major DDG primes + named GFE/sub vendors,
plus by-description sweeps for destroyer-specific PIIDs.

Per-mod records are PRESERVED (not deduped) so we can later compute annual obligation
deltas from per-mod obligatedAmount sums by signed-date FY.

Output:
  fpds_raw/<slug>_raw.json     -- per-query records
  fpds_raw/_summary.json       -- counts and totals per query
  fpds_raw/_pull_log.txt       -- timing/progress log

DDG-specific differences from the submarine version:
  - TWO yards instead of one (HII-Ingalls + GDBIW). Both are prime of record on
    individual ships.
  - HII-Ingalls and HII-NNS share a parent entity name; need to filter on
    contracting office/PSC to separate destroyer from carrier/sub work in the
    HII pull.
  - GFE vendors differ: Aegis (LM) and SPY-6 (Raytheon) and LM2500 (GE) instead of
    naval reactor (BPMI) and Trident (LM).

Vendor names tested per Federal_Procurement_Research_Lessons_Learned.md section 2:
  VENDOR_NAME:"..."  works reliably; UEI_NAME variants do not.
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
HDRS = {"User-Agent": "ddg-outsourcing-research/1.0"}

OUT_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/fpds_raw"
os.makedirs(OUT_DIR, exist_ok=True)

# Date window. FY18 = signed Oct 1, 2017+ catches the FY18-22 MYP master (Sep 2018
# award) AND the FY23-27 MYP master (Aug 2023 award).
DATE_WINDOW = "SIGNED_DATE:[2017/10/01,2026/12/31]"
NAVY_FILTER = 'CONTRACTING_AGENCY_ID:"1700"'


# (slug, label, [queries], notes)
QUERIES = [
    # ---- Prime yards ----
    ("hii_ingalls_navy", "HII Ingalls Shipbuilding — all Navy contracts", [
        f'VENDOR_NAME:"INGALLS SHIPBUILDING" {NAVY_FILTER}',
        f'VENDOR_NAME:"HUNTINGTON INGALLS INCORPORATED" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"HUNTINGTON INGALLS INCORPORATED" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH BURKE"',
        f'VENDOR_NAME:"HUNTINGTON INGALLS INCORPORATED" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
    ], "HII Ingalls is one of two DDG-51 primes. The 'HUNTINGTON INGALLS INCORPORATED' name appears for both Ingalls and NNS — narrow via description for DDG sweep."),

    ("gd_biw_navy", "GD Bath Iron Works — all Navy contracts", [
        f'VENDOR_NAME:"BATH IRON WORKS" {NAVY_FILTER}',
        f'VENDOR_NAME:"GENERAL DYNAMICS BATH IRON WORKS" {NAVY_FILTER}',
    ], "Bath Iron Works is the second DDG-51 prime + sole DDG-1000 prime."),

    # ---- Aegis Combat System (Lockheed Martin) ----
    ("lm_aegis_navy", "Lockheed Martin — Aegis / DDG-related Navy work", [
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"AEGIS"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VLS"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VERTICAL LAUNCH"',
        f'VENDOR_NAME:"LOCKHEED MARTIN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"MK 41"',
    ], "Aegis Combat System (AWS antennas, signal processors, Director, fire control) + Mk 41 VLS."),

    # ---- AN/SPY-6 AMDR radar + missiles (Raytheon) ----
    ("raytheon_navy_ddg", "Raytheon / RTX — DDG-related Navy work", [
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SPY-6"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"AMDR"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"STANDARD MISSILE"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"TOMAHAWK"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ESSM"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"CIWS"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"PHALANX"',
        f'VENDOR_NAME:"RAYTHEON" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SEWIP"',
    ], "SPY-6 AMDR radar; SM-2/3/6, ESSM, Tomahawk, Phalanx CIWS, SEWIP electronic warfare."),

    # ---- LM2500 gas turbines (GE Aerospace) ----
    ("ge_lm2500_navy", "GE Aerospace — LM2500 propulsion & Navy work", [
        f'VENDOR_NAME:"GENERAL ELECTRIC" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"LM2500"',
        f'VENDOR_NAME:"GENERAL ELECTRIC" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"GAS TURBINE"',
        f'VENDOR_NAME:"GE AEROSPACE" {NAVY_FILTER}',
        f'VENDOR_NAME:"GENERAL ELECTRIC" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"GENERAL ELECTRIC" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH"',
    ], "Four LM2500 gas turbines per DDG. GE Marine Lynn MA / Evendale OH facility."),

    # ---- Rolls-Royce (some marine engine components) ----
    ("rolls_royce_navy_ddg", "Rolls-Royce — Navy DDG-related work", [
        f'VENDOR_NAME:"ROLLS-ROYCE" {NAVY_FILTER}',
        f'VENDOR_NAME:"ROLLS ROYCE" {NAVY_FILTER}',
    ], "Marine engine accessories / submarine work overlap — check description."),

    # ---- BAE Systems (Mk 45 gun + VLS components + Bofors) ----
    ("bae_navy_ddg", "BAE Systems — DDG-related Navy work", [
        f'VENDOR_NAME:"BAE SYSTEMS LAND" {NAVY_FILTER}',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"MK 45"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"5 INCH"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VLS"',
        f'VENDOR_NAME:"BAE SYSTEMS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"VERTICAL LAUNCH"',
    ], "Mk 45 5-inch gun, Mk 38 25mm gun, VLS canisters, gun fire control."),

    # ---- Northrop Grumman (SPQ-9B X-band radar, AN/SLQ-32 / SEWIP, fire control) ----
    ("ng_navy_ddg", "Northrop Grumman — DDG-related Navy work", [
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SPQ-9"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"AEGIS"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SLQ-32"',
        f'VENDOR_NAME:"NORTHROP GRUMMAN" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"SEWIP"',
    ], "Surface ship work — SPQ-9B X-band radar, SEWIP EW, secondary fire control."),

    # ---- L3Harris (CEC USG-2B hardware, navigation, comms) ----
    ("l3harris_navy_ddg", "L3Harris — DDG-related Navy work", [
        f'VENDOR_NAME:"L3HARRIS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"L3HARRIS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"ARLEIGH"',
        f'VENDOR_NAME:"L3HARRIS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
        f'VENDOR_NAME:"L3HARRIS" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"CEC"',
        f'VENDOR_NAME:"L3 TECHNOLOGIES" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"L3 TECHNOLOGIES" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DESTROYER"',
    ], "USG-2B Cooperative Engagement Capability hardware, comms, navigation."),

    # ---- DRS / Leonardo DRS (combat systems, IFC) ----
    ("drs_navy_ddg", "DRS / Leonardo DRS — DDG combat systems", [
        f'VENDOR_NAME:"LEONARDO DRS" {NAVY_FILTER}',
        f'VENDOR_NAME:"DRS SYSTEMS" {NAVY_FILTER}',
        f'VENDOR_NAME:"DRS LAUREL" {NAVY_FILTER}',
        f'VENDOR_NAME:"DRS NAVAL" {NAVY_FILTER}',
    ], "DDG combat system components per FY27 SCN P-5b contractor table."),

    # ---- General Dynamics Mission Systems (separate from BIW; AWS Director) ----
    ("gd_mission_navy_ddg", "GD Mission Systems — DDG-related Navy work", [
        f'VENDOR_NAME:"GENERAL DYNAMICS MISSION" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DDG"',
        f'VENDOR_NAME:"GENERAL DYNAMICS MISSION" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"AEGIS"',
        f'VENDOR_NAME:"GENERAL DYNAMICS MISSION" {NAVY_FILTER} DESCRIPTION_OF_REQUIREMENT:"DIRECTOR"',
    ], "AWS Director/Director Controller per FY27 P-5b contractor table."),

    # ---- Description-keyword Round-1 sweeps for completeness (catch new PIIDs) ----
    ("desc_ddg51_class", "DESCRIPTION:DDG 51 / ARLEIGH BURKE class sweep", [
        f'DESCRIPTION_OF_REQUIREMENT:"DDG 51" {NAVY_FILTER}',
        f'DESCRIPTION_OF_REQUIREMENT:"DDG-51" {NAVY_FILTER}',
        f'DESCRIPTION_OF_REQUIREMENT:"ARLEIGH BURKE" {NAVY_FILTER}',
    ], "Catches anything with DDG-51 / Arleigh Burke in description regardless of vendor."),

    ("desc_destroyer_navy_big", "DESCRIPTION:DESTROYER $50M+ Navy floor sweep", [
        f'DESCRIPTION_OF_REQUIREMENT:"DESTROYER" {NAVY_FILTER} OBLIGATED_AMOUNT:[50000000,99999999999]',
    ], "Round-3 backstop per lessons learned: agency + dollar-floor catches new vehicles."),

    ("desc_flight_iii_navy", "DESCRIPTION:FLIGHT III sweep", [
        f'DESCRIPTION_OF_REQUIREMENT:"FLIGHT III" {NAVY_FILTER}',
    ], "DDG-51 Flight III is the current production variant — should hit FY18-22 MYP + later."),
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
            by_piid = {}
            if all_records:
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
