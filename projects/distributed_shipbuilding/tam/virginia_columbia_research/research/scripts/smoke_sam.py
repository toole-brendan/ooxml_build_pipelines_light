#!/usr/bin/env python3 -u
"""Diagnostic smoke test for SAM.gov pull. Sequential pages with timing."""
import sys
import time
sys.path.insert(0, "/Users/brendantoole/projects2/submarine_outsourced_work/scripts")
from pull_sam_subawards import load_api_key, call, FROM_DATE, TO_DATE

api_key = load_api_key()
print(f"Window: {FROM_DATE} to {TO_DATE}", flush=True)
print(f"Testing N0002417C2100 sequential pages 0-7 @ pageSize=100", flush=True)
print(flush=True)

for page in range(8):
    t0 = time.time()
    try:
        body = call(api_key, "N0002417C2100", page=page, page_size=100)
        elapsed = time.time() - t0
        data = body.get("data") or []
        total = body.get("totalRecords")
        nl_present = "yes" if body.get("nextPageLink") else "no"
        print(f"  page {page}: {elapsed:>5.1f}s   {len(data):>4} recs   "
              f"totalRecords={total}   nextPage={nl_present}", flush=True)
    except Exception as e:
        elapsed = time.time() - t0
        print(f"  page {page}: {elapsed:>5.1f}s   ERROR: {type(e).__name__}: {e}", flush=True)
        break
    time.sleep(0.35)

print(flush=True)
print("Done. If pages averaged 1-3s, prior pull was just silent. "
      "If they hung, API itself is slow/throttling.", flush=True)
