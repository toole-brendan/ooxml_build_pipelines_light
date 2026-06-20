#!/usr/bin/env python3
"""
Pull first-tier subaward records from SAM.gov Acquisition Subaward Reporting API
for submarine prime PIIDs.

Why: USAspending /api/v2/subawards/ silently truncates at ~2,500 records per prime.
The two big GDEB masters (N0002417C2100 Virginia Block V/VI; N0002417C2117 Columbia
Build I/II) both hit that cap in our earlier pull. SAM.gov is the upstream FFATA
source with NO per-prime cap (verified 5,681 records on a single PIID in the howto).

Follows the patterns documented in SAM_GOV_HOWTO.md:
  - LOWERCASE `piid` filter (uppercase is silently dropped)
  - /prod/ in URL (the human docs show URLs without /prod/ which 404)
  - Verify filter honored by checking `nextPageLink` echoes `piid=`
  - Pull status=Published and status=Deleted separately
  - subAwardReportId is unique → no dedup needed
  - Numeric fields are strings → coerce
  - pageSize=1000 (max)

Output: sam_subawards/<PIID>_subawards.json   {piid, published: [...], deleted: [...]}
        sam_subawards/_summary.json
"""
import json
import os
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
HDRS = {"User-Agent": "sub-outsourcing-research/1.0", "Accept": "application/json"}

OUT_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/sam_subawards"
os.makedirs(OUT_DIR, exist_ok=True)

# Date window: subaward ACTION DATE (subAwardDate field) must fall in this range.
# FY20-FY26 = Oct 1, 2019 through Sep 30, 2026 — but per the howto, toDate must
# not exceed the current date, so cap at today.
import datetime as _dt
FROM_DATE = "2019-10-01"
TO_DATE   = _dt.date.today().isoformat()

# pageSize: 1000 (max) is correct per OpenAPI spec + howto. SAM has SPECIFIC slow
# pages on some PIIDs (e.g. page 3 of N0002417C2100 consistently takes ~3 min), but
# with pageSize=1000 the big masters are only ~5 pages, so at most one slow page is
# encountered per PIID. Smaller pageSize means MORE pages = MORE slow pages.
# This is server-side deep-pagination behavior; nothing to fix client-side except wait.
PAGE_SIZE = 1000


def load_api_key():
    env_path = Path("/Users/brendantoole/projects2/submarine_outsourced_work/.env")
    for line in env_path.read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in .env")


# Same 17 seed PIIDs as the USAspending pull, so we can compare apples-to-apples
# and recover the long-tail data USAspending truncated.
SEED_PIIDS = [
    ("N0002417C2100", "GDEB Virginia Block V / Block VI master"),
    ("N0002417C2117", "GDEB Columbia Build I + Build II"),
    ("N0002412C2115", "GDEB Virginia Block IV MYP"),
    ("N0002424C2110", "GDEB Virginia Block VI LLTM"),
    ("N0002409C2104", "GDEB Virginia Block II (residual)"),
    ("N0002413C2128", "GDEB Columbia Design Drawings"),
    ("N0002419C2125", "GDEB Virginia Tech Instructions / HPAD backfit"),
    ("N0002416C2111", "GDEB VPM Ventilation Valve"),
    ("N0002410C2118", "GDEB VPM Tube Fabrication"),
    ("N0002411C2109", "GDEB SSBN-R concept formulation"),
    ("N0002420C4312", "GDEB USS Hartford (SSN 768) EOH"),
    ("N0002419C2114", "BPMI Naval Reactor Components (Columbia)"),
    ("N0002419C2115", "BPMI Columbia Class Industrial Base Increase"),
    ("N0002424C2114", "BPMI S9G reactor"),
    ("N0002410C6266", "LM Virginia Combat Systems hardware/software"),
    ("N0002421C4106", "BAE SSN 812 Forward Subassembly"),
    ("N0002421C4111", "Rolls-Royce Virginia Class Submarine Rotor"),
]


def call(api_key, piid, page=0, page_size=PAGE_SIZE, status="Published"):
    params = {
        "api_key": api_key,
        "piid": piid,             # LOWERCASE per OpenAPI spec — uppercase silently dropped
        "pageNumber": page,
        "pageSize": page_size,
        "status": status,
        "fromDate": FROM_DATE,    # subAwardDate >= this
        "toDate":   TO_DATE,      # subAwardDate <= this
    }
    url = f"{BASE}?{urlencode(params)}"
    req = Request(url, headers=HDRS, method="GET")
    # Use 300s timeout — SAM's deep-pagination slow pages can take ~3 min on
    # specific page numbers for big PIIDs (reproducible behavior).
    try:
        with urlopen(req, timeout=300) as r:
            return json.loads(r.read())
    except HTTPError as e:
        if e.code == 429:
            body = e.read().decode("utf-8", errors="replace")[:300]
            raise SystemExit(f"!! HTTP 429 quota exhausted: {body}")
        raise


def fetch_all(api_key, piid, status="Published", max_pages=300):
    records = []
    page = 0
    while page < max_pages:
        t0 = time.time()
        body = call(api_key, piid, page=page, status=status)
        elapsed = time.time() - t0
        page_data = body.get("data") or []
        print(f"    page {page:>2}: {elapsed:>6.1f}s   {len(page_data):>4} recs "
              f"   running={len(records) + len(page_data):>5}/{body.get('totalRecords', '?')}",
              flush=True)
        data = body.get("data") or []
        records.extend(data)
        total_records = body.get("totalRecords")
        total_pages = body.get("totalPages")
        next_link = body.get("nextPageLink")
        if page == 0:
            # Sanity check: confirm the filter was honored. If
            # totalRecords is 2M+ or first record's piid doesn't match,
            # something is wrong.
            if total_records and total_records > 100_000:
                print(f"    !! totalRecords={total_records:,} on PIID {piid} — "
                      f"filter may have been dropped. Stopping.", flush=True)
                return records
            if next_link and "piid=" not in next_link.lower():
                print(f"    !! nextPageLink missing piid= → filter was dropped. "
                      f"link={next_link[:200]}", flush=True)
                return records
            if data and data[0].get("piid") and data[0]["piid"] != piid:
                print(f"    !! First record PIID {data[0]['piid']} != requested {piid}",
                      flush=True)
                return records
            print(f"    totalRecords={total_records:,}  totalPages={total_pages}",
                  flush=True)
        # Stop conditions:
        # 1. No nextPageLink in response (canonical "no more pages")
        # 2. Empty page_data (SAM bug: it sometimes keeps returning nextPageLink
        #    even when totalRecords has been exhausted — empty pages still take
        #    minutes due to deep-pagination scan)
        # 3. We've collected >= totalRecords (additional safety)
        if not next_link:
            break
        if not page_data:
            print(f"    stop: empty page (SAM nextPageLink overshoot)", flush=True)
            break
        if total_records and len(records) >= total_records:
            print(f"    stop: collected {len(records)} >= totalRecords {total_records}",
                  flush=True)
            break
        page += 1
        time.sleep(0.35)
    return records


def main():
    api_key = load_api_key()
    print(f"Using SAM key prefix: {api_key[:10]}...", flush=True)

    summary = {}
    for piid, label in SEED_PIIDS:
        print(f"\n[{piid}] {label}", flush=True)
        try:
            pub = fetch_all(api_key, piid, status="Published")
            det = fetch_all(api_key, piid, status="Deleted")
        except SystemExit as e:
            print(f"  HALTED: {e}", flush=True)
            break
        except Exception as e:
            print(f"  ERROR on {piid}: {e}", flush=True)
            summary[piid] = {"label": label, "error": str(e)}
            continue

        # Verify dedup-clean per howto
        ids = [r.get("subAwardReportId") for r in pub if r.get("subAwardReportId")]
        unique_ids = set(ids)
        dup_count = len(ids) - len(unique_ids)

        total_pub = sum(float(r.get("subAwardAmount") or 0) for r in pub)

        # Top recipients (use subParentUei when present, else subEntityUei)
        by_recip = {}
        for r in pub:
            name = (r.get("subEntityParentLegalBusinessName") or
                    r.get("subEntityLegalBusinessName") or "UNKNOWN").upper().strip()
            by_recip.setdefault(name, 0.0)
            by_recip[name] += float(r.get("subAwardAmount") or 0)
        top5 = sorted(by_recip.items(), key=lambda kv: kv[1], reverse=True)[:5]

        print(f"  + published={len(pub)} (dup_subAwardReportId={dup_count})  deleted={len(det)}",
              flush=True)
        print(f"  + total subAwardAmount = ${total_pub/1e6:,.1f}M", flush=True)
        print(f"  TOP: " + "; ".join(
            f"{n[:40]}=${a/1e6:.1f}M" for n, a in top5
        ), flush=True)

        out_path = os.path.join(OUT_DIR, f"{piid}_subawards.json")
        with open(out_path, "w") as f:
            json.dump({
                "piid": piid,
                "label": label,
                "published_count": len(pub),
                "deleted_count": len(det),
                "published_total_$": total_pub,
                "duplicate_subAwardReportId_count": dup_count,
                "published": pub,
                "deleted": det,
            }, f, indent=2, default=str)
        summary[piid] = {
            "label": label,
            "published_count": len(pub),
            "deleted_count": len(det),
            "published_total_$": total_pub,
            "duplicate_subAwardReportId_count": dup_count,
            "output_file": out_path,
        }
        time.sleep(0.3)

    summary_path = os.path.join(OUT_DIR, "_summary.json")
    with open(summary_path, "w") as f:
        json.dump({
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "piids": summary,
        }, f, indent=2, default=str)
    print(f"\nDone. Summary -> {summary_path}", flush=True)


if __name__ == "__main__":
    main()
