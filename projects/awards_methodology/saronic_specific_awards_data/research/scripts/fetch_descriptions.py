#!/usr/bin/env python3
"""
Fetch description text for shortlisted notices (the `description` field in
search responses is a URL, not text — 1 API call per notice, so shortlist
only). Cached to descriptions/{noticeId}.json; skip-if-exists resume.

Shortlist = every STRONG/MEDIUM notice in opportunities_all.csv plus the
hand-picked OTHER-tier notice IDs below (autonomy-titled, domain ambiguous
from the title alone).
"""
import csv
import json
import re
import socket
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

_orig_getaddrinfo = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4

RESEARCH = Path(__file__).resolve().parents[1]
REPO_ROOT = RESEARCH.parents[3]   # research -> saronic_specific_awards_data -> awards_methodology -> projects -> repo root
CSV_PATH = RESEARCH / "extracted" / "opportunities_all.csv"
OUT_DIR = RESEARCH / "descriptions"
OUT_DIR.mkdir(exist_ok=True)

# OTHER-tier notices worth a description look (titles suggest possible
# maritime-autonomy content but the domain is not determinable from title).
EXTRA_TITLE_PATTERNS = [
    r"JATF Autonomous Warfare Proving Ground",
    r"J2 Integrated Survey Program",
    r"Unmanned Fusion Warfare Laboratory",
    r"DevX Autonomy",
    r"SEAGLIDER SGX",
]


def load_api_key():
    for line in (REPO_ROOT / ".env").read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in repo-root .env")


def main():
    api_key = load_api_key()
    rows = list(csv.DictReader(CSV_PATH.open()))
    extras = re.compile("|".join(EXTRA_TITLE_PATTERNS), re.I)
    targets = [r for r in rows if r["tier"] in ("STRONG", "MEDIUM")
               or extras.search(r["title"] or "")]
    print(f"{len(targets)} shortlisted notices")
    for r in targets:
        nid = r["notice_id"]
        out = OUT_DIR / f"{nid}.json"
        if out.exists():
            continue
        url = (f"https://api.sam.gov/prod/opportunities/v1/noticedesc?"
               + urlencode({"noticeid": nid, "api_key": api_key}))
        req = Request(url, headers={"User-Agent": "saronic-usv-research/1.0"})
        try:
            with urlopen(req, timeout=120) as resp:
                body = json.loads(resp.read())
        except HTTPError as e:
            if e.code == 429:
                raise SystemExit("Quota exhausted (429)")
            body = {"error": str(e)}
        out.write_text(json.dumps(
            {"notice_id": nid, "title": r["title"], "tier": r["tier"],
             "deadline": r["deadline"], "body": body}, indent=2))
        print(f"  fetched {nid}  {r['title'][:70]}")
        time.sleep(0.4)
    print("done")


if __name__ == "__main__":
    main()
