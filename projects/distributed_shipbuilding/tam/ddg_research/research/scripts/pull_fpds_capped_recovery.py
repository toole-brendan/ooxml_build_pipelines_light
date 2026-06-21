#!/usr/bin/env python3
"""
Recovery pull for FPDS slugs that hit the 300-page cap in the original
pull_fpds_ddg_primes.py run. Uses recursive date-window bisection: if a query
estimate exceeds the per-call page cap, the SIGNED_DATE window is split in half
and each half is queried separately (recursive until each leaf is under cap).

SAFETY: writes to a SEPARATE output dir (fpds_raw_v2/) — never touches
fpds_raw/. Downstream scripts continue reading the original until you decide
to merge.

Slugs targeted (from pull_logs/fpds_pull.log analysis):
  - gd_biw_navy            (BATH IRON WORKS est 799pp, GD BIW est 3124pp — both capped at 300pp)
  - rolls_royce_navy_ddg   (ROLLS-ROYCE est 359pp, ROLLS ROYCE est 359pp — both capped at 300pp)

Output:
  fpds_raw_v2/<slug>_raw.json     -- merged records across all date-split sub-queries
  fpds_raw_v2/_summary.json       -- counts/totals + per-query split tree
  fpds_raw_v2/_pull_log.txt       -- timing/progress log w/ split tree

Run: python3 pull_fpds_capped_recovery.py [slug_filter]
"""
import json
import os
import re
import sys
import time
from collections import defaultdict
from datetime import datetime, timedelta
from urllib import parse
from urllib.request import urlopen, Request
from xml.etree.ElementTree import fromstring

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "ns1": "https://www.fpds.gov/FPDS",
}
BASE = "https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC"
HDRS = {"User-Agent": "ddg-outsourcing-research/1.0"}

OUT_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/fpds_raw_v2"
os.makedirs(OUT_DIR, exist_ok=True)

DATE_START = "2017/10/01"
DATE_END = "2026/12/31"
NAVY_FILTER = 'CONTRACTING_AGENCY_ID:"1700"'
MAX_PAGES_PER_CALL = 300
MAX_SPLIT_DEPTH = 6  # 2^6 = 64 leaves — way more than needed for 9.25-year window
FMT = "%Y/%m/%d"

# Only the 2 slugs that hit the cap. Other slugs in the original pull completed cleanly.
QUERIES = [
    ("gd_biw_navy", "GD Bath Iron Works — all Navy contracts (date-split recovery)", [
        f'VENDOR_NAME:"BATH IRON WORKS" {NAVY_FILTER}',
        f'VENDOR_NAME:"GENERAL DYNAMICS BATH IRON WORKS" {NAVY_FILTER}',
    ], "Bath Iron Works is the second DDG-51 prime + sole DDG-1000 prime. Both vendor-name queries hit the 300pp cap in original pull (est 799pp and 3124pp); date-splitting recovers the missing 28K+ records."),

    ("rolls_royce_navy_ddg", "Rolls-Royce — Navy DDG-related work (date-split recovery)", [
        f'VENDOR_NAME:"ROLLS-ROYCE" {NAVY_FILTER}',
        f'VENDOR_NAME:"ROLLS ROYCE" {NAVY_FILTER}',
    ], "Marine engine accessories. Both vendor-name queries hit 300pp cap (est 359pp each); date-splitting recovers ~1.2K missing records."),
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


def fpds_paginate_one(q, log_fn=print):
    """Fetch one query as-is. Returns (records, est_total_pages, was_capped)."""
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
        recs = extract_entries(text)
        records.extend(recs)
        pages_fetched += 1
        if not recs:
            break
        start += 10
        if start // 10 >= min(total_pages, MAX_PAGES_PER_CALL):
            break
        if pages_fetched % 50 == 0:
            log_fn(f"        ...{pages_fetched} pages, {len(records)} records so far")
        time.sleep(0.35)
    was_capped = (total_pages or 0) > MAX_PAGES_PER_CALL
    return records, (total_pages or 0), was_capped


def date_midpoint(d_start, d_end):
    a = datetime.strptime(d_start, FMT)
    b = datetime.strptime(d_end, FMT)
    mid = a + (b - a) / 2
    mid_a = mid.strftime(FMT)
    mid_b = (mid + timedelta(days=1)).strftime(FMT)
    return mid_a, mid_b


def fpds_paginate_with_splits(q_base, d_start, d_end, log_fn=print, depth=0, split_tree=None):
    """Recursive date-window splitter. Returns deduplicated records list."""
    if split_tree is None:
        split_tree = []
    indent = "  " * depth
    q = f"{q_base} SIGNED_DATE:[{d_start},{d_end}]"
    log_fn(f"      {indent}[d{depth}] window=[{d_start},{d_end}]")
    recs, est_pages, was_capped = fpds_paginate_one(q, log_fn=log_fn)
    node = {
        "depth": depth,
        "window": [d_start, d_end],
        "est_pages": est_pages,
        "was_capped": was_capped,
        "records_pulled": len(recs),
        "children": [],
    }
    split_tree.append(node)
    log_fn(f"      {indent}[d{depth}] est={est_pages}pp got={len(recs):,} recs"
           + (" (CAPPED — splitting)" if was_capped and depth < MAX_SPLIT_DEPTH else ""))
    if not was_capped:
        return recs
    if depth >= MAX_SPLIT_DEPTH:
        log_fn(f"      {indent}[d{depth}] !! reached max split depth — accepting truncation")
        return recs
    a_end = datetime.strptime(d_start, FMT)
    b_end = datetime.strptime(d_end, FMT)
    if b_end <= a_end:
        return recs
    mid_a, mid_b = date_midpoint(d_start, d_end)
    log_fn(f"      {indent}>> SPLIT @ {mid_a}")
    left_recs = fpds_paginate_with_splits(q_base, d_start, mid_a, log_fn, depth + 1, node["children"])
    right_recs = fpds_paginate_with_splits(q_base, mid_b, d_end, log_fn, depth + 1, node["children"])
    seen = set()
    combined = []
    for r in left_recs + right_recs:
        sig = (r.get("full_piid") or r.get("piid"), r.get("mod_number"), r.get("signed_date"))
        if sig in seen:
            continue
        seen.add(sig)
        combined.append(r)
    log_fn(f"      {indent}<< merged depth {depth}: {len(left_recs)}+{len(right_recs)} → {len(combined)} unique")
    return combined


def main():
    log_path = os.path.join(OUT_DIR, "_pull_log.txt")
    summary_path = os.path.join(OUT_DIR, "_summary.json")
    slug_filter = sys.argv[1] if len(sys.argv) > 1 else None
    summary = {}

    with open(log_path, "w") as logf:
        def log(msg):
            print(msg, flush=True)
            logf.write(msg + "\n")
            logf.flush()

        log(f"=== FPDS capped-slug recovery pull started {time.strftime('%Y-%m-%d %H:%M:%S')}")
        log(f"DATE_RANGE=[{DATE_START},{DATE_END}]  MAX_PAGES_PER_CALL={MAX_PAGES_PER_CALL}  MAX_SPLIT_DEPTH={MAX_SPLIT_DEPTH}")
        log(f"OUT_DIR={OUT_DIR}")

        for slug, label, queries, notes in QUERIES:
            if slug_filter and slug != slug_filter:
                continue
            t_slug = time.time()
            log(f"\n--- [{slug}] {label}")
            log(f"    notes: {notes}")
            all_records = []
            seen = set()
            query_trees = []
            for q_idx, q_base in enumerate(queries):
                log(f"    QUERY {q_idx+1}/{len(queries)}: {q_base[:90]}")
                tree = []
                recs = fpds_paginate_with_splits(q_base, DATE_START, DATE_END, log_fn=log, split_tree=tree)
                log(f"    -> {len(recs):,} unique records from this query (after intra-query dedup)")
                query_trees.append({"q_base": q_base, "tree": tree, "records_after_dedup": len(recs)})
                for r in recs:
                    sig = (r.get("full_piid") or r.get("piid"), r.get("mod_number"), r.get("signed_date"))
                    if sig in seen:
                        continue
                    seen.add(sig)
                    all_records.append(r)
            log(f"    [{slug}] {len(all_records):,} unique (PIID,mod,signed_date) records total across all queries")

            # Top vendors
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
            top = sorted(by_vendor.items(), key=lambda kv: kv[1]["total_obligated"], reverse=True)[:15]
            log(f"    TOP VENDORS (latest-mod totalObligated):")
            for v, a in top:
                log(f"      {v[:50]:50s}  ${a['total_obligated']/1e6:>12,.1f}M  {a['piid_count']:>4d} PIIDs")

            out_path = os.path.join(OUT_DIR, f"{slug}_raw.json")
            with open(out_path, "w") as f:
                json.dump({
                    "label": label,
                    "notes": notes,
                    "queries": queries,
                    "date_range": [DATE_START, DATE_END],
                    "max_pages_per_call": MAX_PAGES_PER_CALL,
                    "max_split_depth": MAX_SPLIT_DEPTH,
                    "record_count": len(all_records),
                    "unique_piids": len(by_piid),
                    "query_split_trees": query_trees,
                    "records": all_records,
                }, f, indent=2, default=str)
            summary[slug] = {
                "label": label,
                "queries": queries,
                "record_count": len(all_records),
                "unique_piids": len(by_piid),
                "output_file": out_path,
                "elapsed_sec": round(time.time() - t_slug, 1),
            }
            log(f"    Wrote {out_path}  ({len(all_records):,} records, {summary[slug]['elapsed_sec']:.1f}s)")

        with open(summary_path, "w") as f:
            json.dump({
                "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "date_range": [DATE_START, DATE_END],
                "navy_filter": NAVY_FILTER,
                "queries": summary,
            }, f, indent=2)
        log(f"\nWrote summary -> {summary_path}")


if __name__ == "__main__":
    main()
