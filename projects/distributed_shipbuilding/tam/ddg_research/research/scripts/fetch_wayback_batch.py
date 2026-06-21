#!/usr/bin/env python3
"""Batch-fetch Wayback snapshots of defense.gov bulletin URLs.

Input:  /tmp/wayback_urls_to_fetch.txt  (tab-separated: aid<TAB>year<TAB>url)
Output: research_primary_sources/dod_announcement_pop/cache_wayback/defense_<YYYY>_<aid>.html

The cache_wayback dir is symlinked to submarine_outsourced_work's cache, so
prior pulls from that project are inherited. Re-fetches are skipped.

Uses --compressed flag to handle gzip responses (Wayback returns gzipped
content with no Content-Encoding header).
"""
import os
import subprocess
import sys
import time
from pathlib import Path

CACHE = Path("/Users/brendantoole/projects2/destroyer_outsourced_work/research_primary_sources/dod_announcement_pop/cache_wayback")
CACHE.mkdir(parents=True, exist_ok=True)

def fetch_one(aid, year, url):
    # year is the snapshot timestamp year; use the original article URL with id_ Wayback prefix
    out = CACHE / f"defense_{year}_{aid}.html"
    if out.exists() and out.stat().st_size > 5000:
        return "cached"
    wb_url = f"https://web.archive.org/web/{year}id_/{url}"
    try:
        r = subprocess.run(
            ["curl", "-sS", "-m", "45", "--compressed",
             "-A", "Mozilla/5.0", "-L", "-o", str(out), wb_url],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    if r.returncode != 0:
        return f"err{r.returncode}"
    if not out.exists() or out.stat().st_size < 2000:
        return f"toosmall_{out.stat().st_size if out.exists() else 0}"
    return "ok"


def main():
    with open("/tmp/wayback_urls_to_fetch.txt") as f:
        urls = [line.strip().split("\t") for line in f if line.strip()]
    print(f"Fetching {len(urls)} URLs", flush=True)
    stats = {"ok": 0, "cached": 0, "err": 0, "timeout": 0, "toosmall": 0}
    for i, (aid, year, url) in enumerate(urls, 1):
        result = fetch_one(aid, year, url)
        if result.startswith("err") or result.startswith("toosmall"):
            stats["err"] += 1
        else:
            base = result if result in stats else "err"
            stats[base] = stats.get(base, 0) + 1
        if i % 10 == 0:
            print(f"  {i}/{len(urls)}  ok={stats['ok']} cached={stats['cached']} err={stats['err']} timeout={stats['timeout']}", flush=True)
        time.sleep(2.0)  # Wayback rate limit — 2s lets us fit 200 URLs in 10-min budget
    print(f"\nDone. {stats}")


if __name__ == "__main__":
    main()
