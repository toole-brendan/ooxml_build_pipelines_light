#!/usr/bin/env python3
"""STAGE 5 - PRE-AWARD PIPELINE (SAM.gov Get Opportunities API).

Forward-looking signal: solicitations / presolicitations / sources-sought / award
notices for Army watercraft + USV programs -> the `pipeline_events` table and the
pre-award half of the recompete radar (the post-award half comes from Stage-2/3
period-of-performance dates).

This API is the painful one (see SAM_GOV_HOWTO.md) — design around it, don't fight it:
  * ~60 SECONDS per call regardless of limit. A handful of calls = minutes. Keep the
    query plan TIGHT; never run diagnostic calls casually.
  * TITLE-ONLY free-text (`title=<substring>`); no description/q search. Generic-titled
    notices are invisible — accept that gap.
  * `postedFrom`/`postedTo` are MM/dd/yyyy and may not span > 1 year -> we chunk by year.
  * `description` in responses is a URL, not text (fetching it costs +1 call each; skipped).
  * 1,000/day quota; `_common` traps 429 -> QuotaExhausted, halts cleanly.
  * Resumable: existing per-(term,year) files are skipped.

Run:  python3 pull_sam_opportunities.py             # full plan (SLOW: ~60s/call)
      python3 pull_sam_opportunities.py active      # forward pipeline: last 12 mo, all terms (~12 calls)
      python3 pull_sam_opportunities.py smoke       # one call only (validate)

`active` is the production mode for the recompete radar's pre-award half: it pulls a
single trailing-12-months posted window for every title term (one <=1yr call each), so
the leaf carries CURRENT notices. Open-vs-closed is NOT filtered here (faithful-raw
invariant) - it is derived downstream against the radar's As-of date.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import QuotaExhausted, env, http_get, slugify, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "sam_opportunities"
EXTRACT = ROOT / "extracted"
INDEX_OUT = EXTRACT / "_opportunities_index.json"
LOG = ROOT / "pull_logs" / "sam_opportunities.log"

BASE = "https://api.sam.gov/opportunities/v2/search"
# Title substrings — specific enough to keep result sets small (title-only search).
TITLE_TERMS = [
    "watercraft", "landing craft", "logistic support vessel", "maneuver support vessel",
    "lighterage", "causeway", "harbormaster", "surface vessel", "vessel modernization",
    "boat", "tug", "barge",
]
# DoD FY-ish posting windows; each <= 1 year (API hard limit).
YEAR_WINDOWS = [
    ("01/01/2021", "12/31/2021"), ("01/01/2022", "12/31/2022"),
    ("01/01/2023", "12/31/2023"), ("01/01/2024", "12/31/2024"),
    ("01/01/2025", "12/31/2025"), ("01/01/2026", "12/31/2026"),
]
LIMIT = 1000


def fetch(term, frm, to, api_key, log):
    params = {"api_key": api_key, "title": term, "postedFrom": frm, "postedTo": to,
              "limit": LIMIT, "offset": 0}
    url = f"{BASE}?{urlencode(params)}"
    txt, st = http_get(url, headers={"Accept": "application/json"}, timeout=120, tries=2)
    if txt is None:
        log(f"      '{term}' {frm}-{to}: HTTP {st} (no response)")
        return None
    try:
        body = json.loads(txt)
    except Exception:
        log(f"      '{term}' {frm}-{to}: bad JSON")
        return None
    return body


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    api_key = env("SAM_API_KEY")
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    smoke = mode == "smoke"
    if smoke:
        plan = [("watercraft", "01/01/2025", "12/31/2025")]
    elif mode == "active":
        # forward pipeline: notices posted in the trailing 12 months (one <=1yr window
        # per title term). Recent enough that anything still open is captured; closed-
        # but-recent notices are kept too (an imminent-award signal) and flagged later.
        # SAM rejects a span of exactly 1 year ("Date range must be null year(s)
        # apart"), so stay strictly under: 363 days back through today.
        today = date.today()
        frm = (today - timedelta(days=363)).strftime("%m/%d/%Y")
        to = today.strftime("%m/%d/%Y")
        plan = [(t, frm, to) for t in TITLE_TERMS]
    else:
        plan = [(t, frm, to) for t in TITLE_TERMS for (frm, to) in YEAR_WINDOWS]

    log(f"=== SAM opportunities (Stage 5) {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"plan={len(plan)} calls (~60s each => ~{len(plan)} min). smoke={smoke}. resumable.")

    index, seen_ids = [], set()
    try:
        for i, (term, frm, to) in enumerate(plan, 1):
            out_path = RAW / f"{slugify(term)}_{frm[-4:]}_{to[-4:]}.json"
            if out_path.exists():
                try:
                    data = json.loads(out_path.read_text()).get("opportunities", [])
                except Exception:
                    data = []
            else:
                body = fetch(term, frm, to, api_key, log)
                if body is None:
                    continue
                data = body.get("opportunitiesData") or []
                write_json(out_path, {"title_term": term, "posted_from": frm, "posted_to": to,
                                      "total_records": body.get("totalRecords"),
                                      "count": len(data), "opportunities": data})
                time.sleep(0.3)
            new = 0
            for o in data:
                nid = o.get("noticeId")
                if nid and nid in seen_ids:
                    continue
                if nid:
                    seen_ids.add(nid)
                new += 1
                index.append({
                    "notice_id": o.get("noticeId"), "title": o.get("title"),
                    "solicitation_number": o.get("solicitationNumber"),
                    "type": o.get("type"), "base_type": o.get("baseType"),
                    "posted_date": o.get("postedDate"),
                    "response_deadline": o.get("responseDeadLine"),
                    "naics": o.get("naicsCode"), "psc": o.get("classificationCode"),
                    "set_aside": o.get("typeOfSetAside"),
                    "department": o.get("fullParentPathName"),
                    "office": o.get("officeAddress", {}).get("city") if isinstance(o.get("officeAddress"), dict) else None,
                    "matched_term": term, "award_number": (o.get("award") or {}).get("number") if o.get("award") else None,
                })
            log(f"  [{i}/{len(plan)}] '{term}' {frm[-4:]}: {len(data)} notices ({new} new unique)")
    except QuotaExhausted as e:
        log(f"\n!! {e}\n!! Halting; {len(index)} notices captured. Re-run after midnight UTC (cached skipped).")

    write_json(INDEX_OUT, index)
    log(f"\n=== done. {len(index)} distinct opportunity notices indexed across {len(plan)} queries.")
    logf.close()


if __name__ == "__main__":
    main()
