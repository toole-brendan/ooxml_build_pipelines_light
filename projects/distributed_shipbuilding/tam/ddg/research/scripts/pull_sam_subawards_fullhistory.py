#!/usr/bin/env python3
"""
Full-history SAM.gov subaward pull (no date window) for the 24 shipbuilder-directed
DDG-51 PIIDs (GD-BIW + HII-Ingalls per workbook/extracted/nc_scope_summary.json).

Why a separate script (not a flag on the existing one):
  - Won't clobber `sam_subawards/` (the FY18+ windowed cache the deck currently uses).
  - Different output dir: `sam_subawards_fullhistory/`.
  - Brings DDG to parity with the submarines full-history corpus, which is the
    substrate for first-ever-award dating (competability signal 3) and cadence.

Scope note: GFE-prime PIIDs (BAE-Guns/VLS, LM-Aegis, Raytheon, GE, DRS, NG,
GD-MissionSys) are deliberately excluded — Navy-directed competition is outside the
competable pool. They can be appended to SEED_PIIDS later; the skip-if-file-exists
resume logic means already-pulled PIIDs never re-fetch.

Follows the patterns documented in ../SAM_GOV_HOWTO.md:
  - LOWERCASE `piid` filter (uppercase is silently dropped)
  - /prod/ in URL (the human docs show URLs without /prod/ which 404)
  - Verify filter honored by checking `nextPageLink` echoes `piid=`
  - Pull status=Published and status=Deleted separately
  - subAwardReportId is unique → no dedup needed (verified per-file anyway)
  - Numeric fields are strings → coerce
  - pageSize=1000 (max)
  - IPv4 monkeypatch (the submarines full-history script omitted it and paid
    ~225s/call on the macOS IPv6 stall)

Run:
    cd /Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/distributed_shipbuilding/tam/ddg/research
    nohup python3 scripts/pull_sam_subawards_fullhistory.py \
        > sam_subawards_fullhistory.log 2>&1 &
    # then `tail -f sam_subawards_fullhistory.log` from anywhere to check progress
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

# Force IPv4 for ALL Python socket lookups in this process.
# Why: api.sam.gov returns both AAAA (IPv6) and A (IPv4) records. On macOS, Python's
# urllib does a SEQUENTIAL "AAAA first, then A on failure" lookup, not curl-style
# Happy Eyeballs. When IPv6 is unreachable, urllib blocks ~225 seconds per request
# (3 × ~75s TCP SYN retransmit timeout) before falling back to IPv4.
_orig_getaddrinfo = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
HDRS = {"User-Agent": "ddg-outsourcing-research/1.0", "Accept": "application/json"}

REPO_ROOT = "/Users/brendantoole/projects3/ooxml_build_pipelines_light"
PROJECT_ROOT = os.path.join(REPO_ROOT, "projects", "distributed_shipbuilding", "tam", "ddg", "research")
OUT_DIR = os.path.join(PROJECT_ROOT, "sam_subawards_fullhistory")
os.makedirs(OUT_DIR, exist_ok=True)

# Full-history window: 2008 is well before FSRS started accepting records (~2010-2011),
# so this captures everything. Cap toDate at today per the howto (future dates 400).
FROM_DATE = "2008-01-01"
TO_DATE = _dt.date.today().isoformat()

PAGE_SIZE = 1000
MAX_PAGES = 1000  # safety ceiling; even a 100k-record PIID is only 100 pages at pageSize=1000


# The 24 shipbuilder-directed PIIDs from nc_scope_summary.json (groups GD-BIW + HII-Ingalls).
SEED_PIIDS = [
    ("N0002402C2303", "GD-BIW: CONTRACT CLOSEOUT"),
    ("N0002403C2306", "GD-BIW: CONTRACT CLOSEOUT"),
    ("N0002406C2303", "GD-BIW: CONSTRUCTION"),
    ("N0002409C2302", "GD-BIW: DIACAP SETTLEMENT"),
    ("N0002411C2305", "GD-BIW: CONSTRUCT FY11 DDG 51 CLASS GUIDED FMR 11622L"),
    ("N0002411C2306", "GD-BIW: FUNDING REALLOCATION DUE TO CANCELLATION"),
    ("N0002412C2313", "GD-BIW: FLIGHT III DESIGN"),
    ("N0002412C4311", "GD-BIW: SHIP ALTERATION WORK - SEVERABLE"),
    ("N0002413C2305", "GD-BIW: CONSTRUCTION OF DDG 51 SHIP FMR-12161M DEFIN FMR-12182MNO DEFIN"),
    ("N0002414C4313", "GD-BIW: PIO AND OTHER MATERIAL. DE-OBLIGATE EXCESS FUNDS ON VARIOUS CLINS."),
    ("N0002418C2305", "GD-BIW: CONSTRUCTION OF DDG 51 SHIP WF-3753 (FMR-12243N) FMR-12182MNO DEFIN"),
    ("N0002418C2313", "GD-BIW: CLASS CHANGES DESIGN SERVICES"),
    ("N0002418C4451", "GD-BIW: SHIP ALTERATION WORK - SEVERABLE"),
    ("N0002419C2322", "GD-BIW: ORDERS: WR22-029"),
    ("N0002419C4452", "GD-BIW: PROVISIONED ITEMS ORDERS (PIO)"),
    ("N0002423C2305", "GD-BIW: CONSTRUCTION OF DDG 51 SHIP"),
    ("N0002424C2313", "GD-BIW: DDG 51 CLASS LEAD YARD SUPPORT"),
    ("N0002402C2304", "HII-Ingalls: CONSTRUCTION OF FY02 ARLEIGH BURKE GUIDED MISSILE DESTROYER"),
    ("N0002411C2307", "HII-Ingalls: CONSTRUCT FY11 DDG 51 CLASS GUIDED MISSILE DESTROYER DDG 114"),
    ("N0002411C2309", "HII-Ingalls: CONSTRUCT FY10 DDG 51 CLASS"),
    ("N0002412C2312", "HII-Ingalls: FLIGHT III DESIGN"),
    ("N0002413C2307", "HII-Ingalls: CONSTRUCT FY17 DDG 51 CLASS GUIDED MISSILE DESTROYER (DDG 125)"),
    ("N0002418C2307", "HII-Ingalls: CONSTRUCT FIRM HHIP FY18 DDG 51 CLASS GUIDED MISSILE DESTROYER"),
    ("N0002423C2307", "HII-Ingalls: CONSTRUCTION OF DDG 51 SHIP"),
]


def ts():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    print(f"[{ts()}] {msg}", flush=True)


def load_api_key():
    if os.environ.get("SAM_API_KEY"):
        return os.environ["SAM_API_KEY"].strip()
    env_path = Path(os.path.join(REPO_ROOT, ".env"))
    for line in env_path.read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in .env")


def call(api_key, piid, page=0, status="Published"):
    params = {
        "api_key": api_key,
        "piid": piid,
        "pageNumber": page,
        "pageSize": PAGE_SIZE,
        "status": status,
        "fromDate": FROM_DATE,
        "toDate": TO_DATE,
    }
    url = f"{BASE}?{urlencode(params)}"
    req = Request(url, headers=HDRS, method="GET")
    try:
        with urlopen(req, timeout=420) as r:
            return json.loads(r.read())
    except HTTPError as e:
        if e.code == 429:
            body = e.read().decode("utf-8", errors="replace")[:300]
            raise SystemExit(f"HTTP 429 quota exhausted: {body}")
        raise


def fetch_all(api_key, piid, status="Published"):
    records = []
    page = 0
    while page < MAX_PAGES:
        t0 = time.time()
        body = call(api_key, piid, page=page, status=status)
        elapsed = time.time() - t0
        page_data = body.get("data") or []
        total_records = body.get("totalRecords")
        next_link = body.get("nextPageLink")
        log(f"    [{status}] page {page:>3}: {elapsed:>6.1f}s   {len(page_data):>4} recs   "
            f"running={len(records) + len(page_data):>5}/{total_records if total_records is not None else '?'}")

        if page == 0:
            if total_records and total_records > 200_000:
                log(f"    !! totalRecords={total_records:,} suspiciously huge — filter may have been dropped. Stopping.")
                return records
            if next_link and "piid=" not in next_link.lower():
                log(f"    !! nextPageLink missing piid= → filter was dropped. link={next_link[:200]}")
                return records
            if page_data and page_data[0].get("piid") and page_data[0]["piid"] != piid:
                log(f"    !! First record PIID {page_data[0]['piid']} != requested {piid}")
                return records
            log(f"    [{status}] totalRecords={total_records}  totalPages={body.get('totalPages')}")

        records.extend(page_data)

        if not next_link:
            break
        if not page_data:
            log(f"    [{status}] stop: empty page (nextPageLink overshoot)")
            break
        if total_records and len(records) >= total_records:
            log(f"    [{status}] stop: collected {len(records)} >= totalRecords {total_records}")
            break

        page += 1
        time.sleep(0.35)
    return records


def write_progress(piid_idx, current_piid, status_label):
    p = os.path.join(OUT_DIR, "_progress.json")
    with open(p, "w") as f:
        json.dump({
            "updated_at": ts(),
            "current_piid_index": piid_idx,
            "current_piid": current_piid,
            "total_piids": len(SEED_PIIDS),
            "status": status_label,
        }, f, indent=2)


def main():
    api_key = load_api_key()
    log(f"START DDG full-history SAM pull. From={FROM_DATE} To={TO_DATE}")
    log(f"Output dir: {OUT_DIR}")
    log(f"API key prefix: {api_key[:10]}...")

    overall_t0 = time.time()
    summary = {}

    for idx, (piid, label) in enumerate(SEED_PIIDS, start=1):
        out_path = os.path.join(OUT_DIR, f"{piid}_subawards.json")
        if os.path.exists(out_path):
            log(f"[{idx}/{len(SEED_PIIDS)}] {piid} — SKIP (already present at {out_path})")
            with open(out_path) as f:
                cached = json.load(f)
            summary[piid] = {
                "label": label,
                "published_count": cached.get("published_count"),
                "deleted_count": cached.get("deleted_count"),
                "published_total_$": cached.get("published_total_$"),
                "skipped": True,
                "output_file": out_path,
            }
            continue

        write_progress(idx, piid, "starting")
        log(f"\n[{idx}/{len(SEED_PIIDS)}] {piid}  {label}")
        piid_t0 = time.time()
        try:
            pub = fetch_all(api_key, piid, status="Published")
            write_progress(idx, piid, "published done, fetching deleted")
            det = fetch_all(api_key, piid, status="Deleted")
        except SystemExit as e:
            log(f"  HALTED: {e}")
            summary[piid] = {"label": label, "error": str(e), "halted": True}
            break
        except Exception as e:
            log(f"  ERROR on {piid}: {e!r}")
            summary[piid] = {"label": label, "error": repr(e)}
            continue

        piid_elapsed = time.time() - piid_t0
        ids = [r.get("subAwardReportId") for r in pub if r.get("subAwardReportId")]
        unique_ids = set(ids)
        dup_count = len(ids) - len(unique_ids)
        total_pub = sum(float(r.get("subAwardAmount") or 0) for r in pub)

        by_recip = {}
        for r in pub:
            name = (r.get("subEntityParentLegalBusinessName")
                    or r.get("subEntityLegalBusinessName")
                    or "UNKNOWN").upper().strip()
            by_recip.setdefault(name, 0.0)
            by_recip[name] += float(r.get("subAwardAmount") or 0)
        top5 = sorted(by_recip.items(), key=lambda kv: kv[1], reverse=True)[:5]

        log(f"  + published={len(pub)} (dup_subAwardReportId={dup_count})  deleted={len(det)}")
        log(f"  + total subAwardAmount = ${total_pub/1e6:,.1f}M  (elapsed {piid_elapsed/60:.1f} min)")
        log(f"  TOP: " + "; ".join(f"{n[:40]}=${a/1e6:.1f}M" for n, a in top5))

        with open(out_path, "w") as f:
            json.dump({
                "piid": piid,
                "label": label,
                "from_date": FROM_DATE,
                "to_date": TO_DATE,
                "fetched_at": ts(),
                "published_count": len(pub),
                "deleted_count": len(det),
                "published_total_$": total_pub,
                "duplicate_subAwardReportId_count": dup_count,
                "piid_elapsed_seconds": piid_elapsed,
                "published": pub,
                "deleted": det,
            }, f, indent=2, default=str)
        summary[piid] = {
            "label": label,
            "published_count": len(pub),
            "deleted_count": len(det),
            "published_total_$": total_pub,
            "duplicate_subAwardReportId_count": dup_count,
            "piid_elapsed_seconds": piid_elapsed,
            "output_file": out_path,
        }

        with open(os.path.join(OUT_DIR, "_summary.json"), "w") as f:
            json.dump({
                "updated_at": ts(),
                "completed_so_far": idx,
                "total": len(SEED_PIIDS),
                "from_date": FROM_DATE,
                "to_date": TO_DATE,
                "piids": summary,
            }, f, indent=2, default=str)

        time.sleep(0.5)

    overall_elapsed = time.time() - overall_t0
    log(f"\nDONE. Total elapsed: {overall_elapsed/60:.1f} min ({overall_elapsed/3600:.2f} hr)")
    write_progress(len(SEED_PIIDS), "—", "done")


if __name__ == "__main__":
    main()
