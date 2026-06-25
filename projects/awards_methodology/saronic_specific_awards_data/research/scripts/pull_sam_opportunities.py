#!/usr/bin/env python3
"""
SAM.gov Get Opportunities pull — solicitations of interest to an autonomous
surface vessel (ASV/USV) maker. Pre-award pipeline data, NOT the FSRS subaward
(already-awarded) corpora used elsewhere in this repo.

Endpoint: https://api.sam.gov/opportunities/v2/search (no /prod/ segment on
this one — verified live 2026-06-12; the subaward API's /prod/ rule does not
apply here).

Follows projects/ddg/research/SAM_GOV_HOWTO.md:
  - IPv4 monkeypatch (macOS IPv6 stall)
  - api_key as query param, from repo-root .env
  - limit=1000 max, offset pagination
  - cache every response to disk, skip-if-exists resume
  - trap 429 and halt cleanly

Opportunities-API specifics (HOWTO "Painful Quirks" + live verification today):
  - title= is the only free-text filter, phrase-substring match on TITLE only
  - postedFrom/postedTo MM/dd/yyyy, max 1-year span
  - default result set appears to be ACTIVE notices only ("unmanned" over a
    1-year window returns 32, all active=Yes); we also pull status=inactive
    for the core queries to see what closed recently
  - the ~60s/call latency documented 2026-05 is gone — calls return in ~1-2s
  - description field is a URL, not text (fetched separately for shortlist)

Run:
    cd /Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/awards_methodology/saronic_specific_awards_data/research
    python3 scripts/pull_sam_opportunities.py
"""
import datetime as _dt
import json
import os
import socket
import sys
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# Force IPv4 — see SAM_GOV_HOWTO.md "Critical: Force IPv4 in Python on macOS".
_orig_getaddrinfo = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4

BASE = "https://api.sam.gov/opportunities/v2/search"
HDRS = {"User-Agent": "saronic-usv-research/1.0", "Accept": "application/json"}

REPO_ROOT = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
OUT_DIR = REPO_ROOT / "projects" / "awards_methodology" / "saronic_specific_awards_data" / "research" / "sam_opportunities"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Max allowed window is 1 year.
POSTED_FROM = "06/13/2025"
POSTED_TO = "06/12/2026"
PAGE_SIZE = 1000


def load_api_key():
    for line in (REPO_ROOT / ".env").read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in repo-root .env")


# (slug, param dict) — title keywords kept broad; relevance scoring is
# client-side in summarize_opportunities.py. ncode/ccode sweeps catch
# generically-titled vessel notices the title search can't see.
QUERIES = [
    ("title_unmanned",    {"title": "unmanned"}),
    ("title_autonomous",  {"title": "autonomous"}),
    ("title_uncrewed",    {"title": "uncrewed"}),
    ("title_usv",         {"title": "USV"}),
    ("title_vessel",      {"title": "vessel"}),
    ("title_maritime",    {"title": "maritime"}),
    ("title_autonomy",    {"title": "autonomy"}),
    ("title_boat",        {"title": "boat"}),
    ("title_swarm",       {"title": "swarm"}),
    ("naics_336612",      {"ncode": "336612"}),   # boat building
    ("naics_336611",      {"ncode": "336611"}),   # ship building & repairing
    ("psc_1940",          {"ccode": "1940"}),     # small craft
    ("psc_1905",          {"ccode": "1905"}),     # combat ships & landing vessels
]

def call(api_key, extra, offset=0):
    params = {
        "api_key": api_key,
        "postedFrom": POSTED_FROM,
        "postedTo": POSTED_TO,
        "limit": PAGE_SIZE,
        "offset": offset,
    }
    params.update(extra)
    req = Request(f"{BASE}?{urlencode(params)}", headers=HDRS, method="GET")
    for attempt in range(4):
        try:
            with urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 429:
                raise SystemExit("Quota exhausted (429); resume after midnight UTC")
            if e.code == 404:  # API uses 404 for "no data found"
                return {"totalRecords": 0, "opportunitiesData": []}
            if e.code >= 500 and attempt < 3:
                wait = 2 ** (attempt + 1)
                print(f"    HTTP {e.code}, retry in {wait}s", flush=True)
                time.sleep(wait)
                continue
            raise


def fetch_query(api_key, slug, extra):
    out_path = OUT_DIR / f"{slug}.json"
    if out_path.exists():
        cached = json.loads(out_path.read_text())
        print(f"  {slug}: cached ({len(cached['records'])} records)")
        return
    records, offset = [], 0
    while True:
        body = call(api_key, extra, offset=offset)
        data = body.get("opportunitiesData") or []
        records.extend(data)
        total = body.get("totalRecords") or 0
        if offset + PAGE_SIZE >= total or not data:
            break
        offset += PAGE_SIZE
        time.sleep(0.4)
    out_path.write_text(json.dumps(
        {"slug": slug, "params": extra, "postedFrom": POSTED_FROM,
         "postedTo": POSTED_TO, "totalRecords": total, "records": records},
        indent=2, default=str))
    print(f"  {slug}: {len(records)} records (totalRecords={total})")
    time.sleep(0.4)


if __name__ == "__main__":
    api_key = load_api_key()
    print(f"Posted window {POSTED_FROM} – {POSTED_TO}")
    print("— active (default) —")
    for slug, extra in QUERIES:
        fetch_query(api_key, slug, extra)
    # status allowed values (per live 400 message): Activelatest / Activeall /
    # Archived / Cancelled / Deleted — NOT the lowercase set in the docs.
    # status=Archived 500s server-side on every filter combination tried
    # (2026-06-12, title= and ncode= both), so the recently-closed context
    # pull is disabled; the dataset is the ACTIVE pipeline only.
    print("done")
