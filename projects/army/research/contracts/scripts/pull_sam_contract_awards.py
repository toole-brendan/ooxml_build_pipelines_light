#!/usr/bin/env python3
"""STAGE 7 - PARENT-IDV HYDRATION + FAMILY RECONCILIATION (SAM.gov Contract Awards API).

The discovery/detail pipeline (Stages 1-2) leaves 171 of 241 referenced parent IDVs
WITHOUT a standalone contract_awards record, so the radar/calendar can't resolve a
vehicle's ordering-period end, ceiling, or an authoritative family obligation total.
This stage closes that gap using the SAM.gov Contract Awards API (the documented FPDS
replacement, v1.0 released 2025-12-05) and its PIID Aggregation feature.

For each contract FAMILY (key = parent_idv_piid for task orders, else the standalone
piid) above a materiality floor, one call returns:
  * piidAggregation.awardFamilySummary        -> the family's own records + $ obligated
    (an IDV obligates ~$0 itself; a definitive contract's family $ lives here)
  * piidAggregation.referencingDosOrBpaCallsSummary -> for an IDV, the count + $ of the
    delivery/task orders that reference it (THIS is where an IDV family's money lives)
  * awardSummary[].awardDetails.dates         -> lastDateToOrder (IDV ordering-period
    end), currentCompletionDate / ultimateCompletionDate (definitive PoP / potential),
    periodOfPerformanceStartDate, dateSigned
  * awardSummary[].awardDetails.totalContractDollars.totalBaseAndAllOptionsValue -> ceiling

WHY this is a THIRD reconciliation lens, not ground truth: the Contract Awards API is
new and serves REVEALED data only on a non-federal key -> it EXCLUDES DoD awards signed
< 90 days ago, and its delivery-order backfill can trail the legacy FPDS/USAspending
record we already hold (e.g. Vigor IDV W56HZV17D0086: SAM Revealed DO total ~$56.2M vs
our USAspending family ~$417.8M). The STRUCTURAL fields (ordering-period end, ceiling)
are reliable hydration; the dollar totals are a cross-check the workbook surfaces with
the divergence flagged - never silently overwritten onto our action sums.

SAM gotchas baked in (shared with the other SAM stages via _common):
  * `?api_key=` query param + Accept: application/json. 1,000 req/day on the entity-role
    key; `_common` traps 429 -> QuotaExhausted and HALTS CLEANLY. Resumable: existing
    per-PIID files are skipped. Families processed BIGGEST-FAMILY-$ FIRST so a mid-run
    halt keeps the material vehicles.
  * piidAggregation REQUIRES piid; if the piid is not unique SAM 400s asking for
    referencedIdvPiid - our family keys are parent-IDV / standalone PIIDs (near-always
    unique), so we log+skip the rare collision rather than guess a parent.
  * Forbidden chars in any param value: & | { } ^ \  (our PIIDs are alnum -> safe).
  * 204 = no content (PIID absent from the CA API, e.g. legacy-only) -> recorded not_found.

Scope control: only families with >= floor lifetime obligation (default $250k; ~446
families, comfortably < quota). The floor catches the materiality-floor radar vehicles
(>= $1M, 238) PLUS sub-floor lineage neighbours. Floor is LOGGED (never silent).

Run:  python3 pull_sam_contract_awards.py                 # all families >= $250k
      python3 pull_sam_contract_awards.py 1 W56HZV17D0086 # smoke one PIID
      MIN_OBL=1000000 python3 pull_sam_contract_awards.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import QuotaExhausted, env, http_get, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]            # research/contracts/
RAW = ROOT / "sam_contract_awards"
EXTRACT = ROOT / "extracted"
AWARDS_CSV = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light/"
                  "projects/army/workbook/extracted/contract_awards.csv")
INDEX_OUT = EXTRACT / "_contract_awards_agg_index.json"
LOG = ROOT / "pull_logs" / "sam_contract_awards.log"

BASE = "https://api.sam.gov/contract-awards/v1/search"
MIN_OBL = float(os.environ.get("MIN_OBL", "250000"))
SLEEP = 0.4


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def d10(s):
    """Normalize SAM's two date encodings ('YYYY-MM-DD HH:MM:SS.fff' and ISO-Z) to
    'YYYY-MM-DD'; None/blank -> None."""
    s = (s or "").strip()
    return s[:10] if len(s) >= 10 else None


def maxd(a, b):
    if a and b:
        return max(a, b)
    return a or b


def mind(a, b):
    if a and b:
        return min(a, b)
    return a or b


def family_keys():
    """Distinct family keys (parent_idv_piid else piid) with summed award obligation
    and a representative recipient; biggest-$ first."""
    oblig = defaultdict(float)
    recip = {}
    is_idv = set()                      # keys that appear as a parent_idv -> IDV family
    with open(AWARDS_CSV) as f:
        for r in csv.DictReader(f):
            pidv = (r.get("parent_idv_piid") or "").strip()
            key = pidv or (r.get("piid") or "").strip()
            if not key:
                continue
            oblig[key] += fnum(r.get("obligation_amount")) or 0.0
            recip.setdefault(key, r.get("recipient_name") or "")
            if pidv:
                is_idv.add(pidv)
    fams = [{"piid": k, "oblig": v, "recipient": recip.get(k, ""),
             "is_idv_family": k in is_idv} for k, v in oblig.items()]
    fams.sort(key=lambda d: -d["oblig"])
    return fams


def parse_response(body):
    """Pull the family rollup + structural dates/ceiling out of one CA-API response."""
    out = {"found": False, "award_or_idv": None, "n_records": body.get("totalRecords"),
           "family_count": None, "family_total_dollars": None,
           "ref_dos_base_count": None, "ref_dos_total_count": None,
           "ref_dos_total_dollars": None, "sam_family_obligated": None,
           "ordering_period_end": None, "current_completion_date": None,
           "ultimate_completion_date": None, "pop_start_date": None,
           "date_signed": None, "ceiling_value": None, "solicitation_id": None,
           "contracting_office": None}

    agg = body.get("piidAggregation") or {}
    fam = agg.get("awardFamilySummary") or {}
    ref = agg.get("referencingDosOrBpaCallsSummary") or {}
    if fam:
        out["family_count"] = fam.get("count")
        out["family_total_dollars"] = fnum(fam.get("totalDollars"))
    if ref:
        out["ref_dos_base_count"] = ref.get("baseCount")
        out["ref_dos_total_count"] = ref.get("totalCount")
        out["ref_dos_total_dollars"] = fnum(ref.get("totalDollars"))
    famd = out["family_total_dollars"] or 0.0
    refd = out["ref_dos_total_dollars"] or 0.0
    if fam or ref:
        out["sam_family_obligated"] = round(famd + refd, 2)

    recs = body.get("awardSummary") or []
    out["found"] = bool(recs)
    for rec in recs:
        core = rec.get("coreData") or {}
        det = rec.get("awardDetails") or {}
        dates = det.get("dates") or {}
        tot = det.get("totalContractDollars") or {}
        out["award_or_idv"] = out["award_or_idv"] or core.get("awardOrIDV")
        out["solicitation_id"] = out["solicitation_id"] or core.get("solicitationId")
        office = (((core.get("federalOrganization") or {}).get("contractingInformation")
                   or {}).get("contractingOffice") or {})
        out["contracting_office"] = out["contracting_office"] or office.get("code")
        out["ordering_period_end"] = maxd(out["ordering_period_end"], d10(dates.get("lastDateToOrder")))
        out["current_completion_date"] = maxd(out["current_completion_date"], d10(dates.get("currentCompletionDate")))
        out["ultimate_completion_date"] = maxd(out["ultimate_completion_date"], d10(dates.get("ultimateCompletionDate")))
        out["pop_start_date"] = mind(out["pop_start_date"], d10(dates.get("periodOfPerformanceStartDate")))
        out["date_signed"] = maxd(out["date_signed"], d10(dates.get("dateSigned")))
        ceil = fnum(tot.get("totalBaseAndAllOptionsValue"))
        if ceil is not None:
            out["ceiling_value"] = max(out["ceiling_value"] or 0.0, ceil)
    return out


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    api_key = env("SAM_API_KEY")
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    smoke_piid = sys.argv[2] if len(sys.argv) > 2 else None
    fams = family_keys()
    if smoke_piid:
        fams = [f for f in fams if f["piid"] == smoke_piid][:1]
        dropped = 0
    else:
        keep = [f for f in fams if f["oblig"] >= MIN_OBL]
        dropped = len(fams) - len(keep)
        fams = keep
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 and not smoke_piid else None
    if top_n:
        fams = fams[:top_n]

    log(f"=== SAM Contract Awards (Stage 7: parent-IDV hydration) {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"families selected={len(fams)} (floor=${MIN_OBL/1e6:.3f}M)"
        f"{'' if smoke_piid else f', dropped below floor={dropped}'}")
    log("REVEALED data only (non-federal key): DoD awards signed < 90 days ago are excluded.")
    log("quota=1000/day; biggest-family-first; resumable (existing per-PIID files skipped).")

    index = []
    try:
        for i, fm in enumerate(fams, 1):
            piid = fm["piid"]
            out_path = RAW / f"{piid}.json"
            if out_path.exists():
                try:
                    prev = json.loads(out_path.read_text())
                    index.append(prev.get("summary") or {"piid": piid, "cached": True})
                    continue
                except Exception:
                    pass
            params = {"api_key": api_key, "piid": piid, "piidAggregation": "yes", "limit": 10}
            url = f"{BASE}?{urlencode(params)}"
            txt, st = http_get(url, headers={"Accept": "application/json"})
            note = None
            parsed = {"found": False}
            if txt is None:
                note = f"no-response(status={st})"
            else:
                try:
                    body = json.loads(txt)
                except Exception:
                    body = None
                    note = "bad-json"
                if body is not None:
                    msg = (body.get("message") or "") if isinstance(body, dict) else ""
                    if "referencedIdvPiid" in msg or "not unique" in msg.lower():
                        note = "non-unique-piid (needs referencedIdvPiid) - skipped"
                    elif st == 204 or (isinstance(body, dict) and not body.get("awardSummary")
                                       and not body.get("piidAggregation")):
                        note = "no-content (absent from CA API / legacy-only)"
                    else:
                        parsed = parse_response(body)
            summary = {"piid": piid, "recipient": fm["recipient"],
                       "our_family_obligation": round(fm["oblig"], 2),
                       "our_is_idv_family": fm["is_idv_family"], "note": note,
                       "cached": False, **{k: v for k, v in parsed.items()}}
            write_json(out_path, {"piid": piid, "summary": summary,
                                  "raw": body if (txt is not None) else None})
            index.append(summary)
            if i % 25 == 0 or i == len(fams) or note or parsed.get("found"):
                samm = parsed.get("sam_family_obligated")
                log(f"  [{i}/{len(fams)}] {piid:18s} "
                    f"{(parsed.get('award_or_idv') or '?'):5s} "
                    f"sam=${(samm or 0)/1e6:>8,.1f}M  ours=${fm['oblig']/1e6:>8,.1f}M  "
                    f"ord_end={parsed.get('ordering_period_end') or '-'}"
                    f"{('  ['+note+']') if note else ''}")
            time.sleep(SLEEP)
    except QuotaExhausted as e:
        log(f"\n!! {e}\n!! Halting; {len(index)} families done. Re-run after midnight UTC (cached skipped).")

    write_json(INDEX_OUT, index)
    found = [x for x in index if x.get("found")]
    hydr = [x for x in index if x.get("ordering_period_end") and x.get("our_is_idv_family")]
    log(f"\n=== done. {len(index)} families processed; {len(found)} found in CA API; "
        f"{len(hydr)} IDV families got an ordering-period end (hydrated).")
    logf.close()


if __name__ == "__main__":
    main()
