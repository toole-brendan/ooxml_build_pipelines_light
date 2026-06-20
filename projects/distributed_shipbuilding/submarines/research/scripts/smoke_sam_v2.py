#!/usr/bin/env python3 -u
"""Smoke test v2: pageSize=1000 + requests.Session for HTTP keepalive."""
import sys, time, json
sys.path.insert(0, "/Users/brendantoole/projects2/submarine_outsourced_work/scripts")
from pull_sam_subawards import load_api_key, FROM_DATE, TO_DATE
import urllib.request, urllib.parse, http.client

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
api_key = load_api_key()
print(f"Window: {FROM_DATE} to {TO_DATE}", flush=True)

# Test A: pageSize=1000 with stdlib urllib (no keepalive)
print("\n=== Test A: pageSize=1000, stdlib urllib (new connection each call) ===", flush=True)
for page in range(6):
    t0 = time.time()
    params = {
        "api_key": api_key,
        "piid": "N0002417C2100",
        "pageNumber": page,
        "pageSize": 1000,
        "status": "Published",
        "fromDate": FROM_DATE,
        "toDate": TO_DATE,
    }
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "test/1.0"}, method="GET")
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.loads(r.read())
        elapsed = time.time() - t0
        data = body.get("data") or []
        total = body.get("totalRecords")
        print(f"  page {page}: {elapsed:>5.1f}s   {len(data):>4} recs   total={total}", flush=True)
    except Exception as e:
        print(f"  page {page}: {time.time()-t0:>5.1f}s   ERROR: {type(e).__name__}: {e}", flush=True)
        break
    time.sleep(0.35)

# Test B: pageSize=1000 with http.client persistent connection
print("\n=== Test B: pageSize=1000, http.client (persistent connection / keepalive) ===", flush=True)
conn = http.client.HTTPSConnection("api.sam.gov", timeout=60)
for page in range(6):
    t0 = time.time()
    params = {
        "api_key": api_key,
        "piid": "N0002417C2100",
        "pageNumber": page,
        "pageSize": 1000,
        "status": "Published",
        "fromDate": FROM_DATE,
        "toDate": TO_DATE,
    }
    path = f"/prod/contract/v1/subcontracts/search?{urllib.parse.urlencode(params)}"
    try:
        conn.request("GET", path, headers={"User-Agent": "test/1.0", "Connection": "keep-alive"})
        resp = conn.getresponse()
        raw = resp.read()
        body = json.loads(raw)
        elapsed = time.time() - t0
        data = body.get("data") or []
        total = body.get("totalRecords")
        print(f"  page {page}: {elapsed:>5.1f}s   status={resp.status}   {len(data):>4} recs   total={total}", flush=True)
    except Exception as e:
        print(f"  page {page}: {time.time()-t0:>5.1f}s   ERROR: {type(e).__name__}: {e}", flush=True)
        # Reset connection on error
        try: conn.close()
        except: pass
        conn = http.client.HTTPSConnection("api.sam.gov", timeout=60)
    time.sleep(0.35)
conn.close()
print("\nDone.", flush=True)
