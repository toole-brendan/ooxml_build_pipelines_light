#!/usr/bin/env python3
"""
Pull first-tier subaward records from SAM.gov Acquisition Subaward Reporting API
for DDG-51 prime PIIDs.

Why: USAspending /api/v2/subawards/ silently truncates at ~2,500 records per prime.
For DDG-51 MYP masters (one per yard per MYP block — 4 main contracts in window)
we may hit the cap on the FY18-22 and FY23-27 MYP masters. SAM.gov is the upstream
FFATA source with NO per-prime cap (verified 5,681 records on a single sub PIID).

Follows the patterns documented in SAM_GOV_HOWTO.md:
  - LOWERCASE `piid` filter (uppercase is silently dropped)
  - /prod/ in URL (the human docs show URLs without /prod/ which 404)
  - Verify filter honored by checking `nextPageLink` echoes `piid=`
  - Pull status=Published and status=Deleted separately
  - subAwardReportId is unique → no dedup needed
  - Numeric fields are strings → coerce
  - pageSize=1000 (max)

Seed PIIDs are derived from the standalone discovery script.
Run order:
  1. python3 pull_fpds_ddg_primes.py
  2. python3 discover_ddg_piids.py     ← writes extracted/_discovered_piids.json
  3. python3 pull_sam_subawards.py     ← reads that file

Output: sam_subawards/<PIID>_subawards.json
        sam_subawards/_summary.json
"""
import json
import os
import socket
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Force IPv4 for ALL Python socket lookups in this process.
# Why: api.sam.gov returns both AAAA (IPv6) and A (IPv4) records. On macOS, Python's
# urllib does a SEQUENTIAL "AAAA first, then A on failure" lookup, not curl-style
# Happy Eyeballs. When IPv6 is unreachable, urllib blocks ~225 seconds per request
# (3 × ~75s TCP SYN retransmit timeout) before falling back to IPv4. This makes
# every SAM page take ~225s instead of ~0.5s — a 500× slowdown.
#
# Forcing AF_INET in getaddrinfo skips the IPv6 attempt entirely. Verified on
# 2026-05-23: with this monkeypatch, page fetches drop from 225s → 0.3-0.5s.
_orig_getaddrinfo = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
HDRS = {"User-Agent": "ddg-outsourcing-research/1.0", "Accept": "application/json"}

OUT_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/sam_subawards"
os.makedirs(OUT_DIR, exist_ok=True)

import datetime as _dt
FROM_DATE = "2017-10-01"
TO_DATE   = _dt.date.today().isoformat()

PAGE_SIZE = 1000


def load_api_key():
    env_path = Path("/Users/brendantoole/projects2/destroyer_outsourced_work/.env")
    for line in env_path.read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in .env")


def load_seed_piids():
    """Pull seed PIIDs from the standalone discovery output.

    Reads extracted/_discovered_piids.json — produced by discover_ddg_piids.py
    (which scans fpds_raw/ and picks top-N DDG PIIDs per vendor group).
    """
    disc_path = "/Users/brendantoole/projects2/destroyer_outsourced_work/extracted/_discovered_piids.json"
    if os.path.exists(disc_path):
        with open(disc_path) as f:
            disc = json.load(f)
        if disc:
            return [(p[0], p[1]) for p in disc]
    return []


def call(api_key, piid, page=0, page_size=PAGE_SIZE, status="Published"):
    params = {
        "api_key": api_key,
        "piid": piid,             # LOWERCASE per OpenAPI spec
        "pageNumber": page,
        "pageSize": page_size,
        "status": status,
        "fromDate": FROM_DATE,
        "toDate":   TO_DATE,
    }
    url = f"{BASE}?{urlencode(params)}"
    req = Request(url, headers=HDRS, method="GET")
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

    seed_piids = load_seed_piids()
    if not seed_piids:
        print("No seed PIIDs available. Run discover_ddg_piids.py first.")
        return
    print(f"Loaded {len(seed_piids)} DDG PIIDs to pull from SAM.gov", flush=True)

    summary = {}
    for piid, label in seed_piids:
        print(f"\n[{piid}] {label[:80]}", flush=True)
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

        ids = [r.get("subAwardReportId") for r in pub if r.get("subAwardReportId")]
        unique_ids = set(ids)
        dup_count = len(ids) - len(unique_ids)
        total_pub = sum(float(r.get("subAwardAmount") or 0) for r in pub)

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
