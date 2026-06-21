#!/usr/bin/env python3
"""
Full-history SAM.gov subaward pull (no date window) for the 17 seed PIIDs.

Why a separate script (not a flag on the existing one):
  - Won't clobber `sam_subawards/` (the FY20-FY26 cache the deck currently uses).
  - Different output dir: `sam_subawards_fullhistory/`.
  - Heavier logging since this will run unattended for hours.

What this gets us beyond the FY20-FY26 pull:
  - Confirms the USAspending 2,500-record cap math empirically (N0002417C2100 should
    return ~5,681 records per the howto vs USA's 2,500).
  - Captures pre-FY20 activity that the windowed pull misses entirely — particularly
    Virginia Block IV (N0002412C2115) and any older Columbia design contracts.
  - Closes the FY20-FY21 visibility gap noted in the 2026-05-22 caveats.

Runtime: expect 6-12 hours total. Per-PIID logging includes wall-clock so a tail
of the log shows current progress without re-running.

Run:
    cd /Users/brendantoole/projects2/submarine_outsourced_work
    nohup python3 scripts/pull_sam_subawards_fullhistory.py \
        > sam_subawards_fullhistory.log 2>&1 &
    # then `tail -f sam_subawards_fullhistory.log` from anywhere to check progress
"""
import datetime as _dt
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

PROJECT_ROOT = "/Users/brendantoole/projects2/submarine_outsourced_work"
OUT_DIR = os.path.join(PROJECT_ROOT, "sam_subawards_fullhistory")
os.makedirs(OUT_DIR, exist_ok=True)

# Full-history window: 2008 is well before FSRS started accepting records (~2010-2011),
# so this captures everything. Cap toDate at today per the howto (future dates 400).
FROM_DATE = "2008-01-01"
TO_DATE = _dt.date.today().isoformat()

PAGE_SIZE = 1000
MAX_PAGES = 1000  # safety ceiling; even a 100k-record PIID is only 100 pages at pageSize=1000


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


def ts():
    return _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(msg):
    print(f"[{ts()}] {msg}", flush=True)


def load_api_key():
    env_path = Path(os.path.join(PROJECT_ROOT, ".env"))
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
    log(f"START full-history SAM pull. From={FROM_DATE} To={TO_DATE}")
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
