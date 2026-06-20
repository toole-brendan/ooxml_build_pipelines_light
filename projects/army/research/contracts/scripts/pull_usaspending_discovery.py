#!/usr/bin/env python3
"""STAGE 1 - DISCOVERY. Find the candidate Army/USACE watercraft + USV prime-award
universe via USAspending `spending_by_award`.

Why USAspending (not FPDS) for discovery: FPDS Atom description search OR-tokenizes
multi-word phrases ("MANEUVER SUPPORT VESSEL" -> MANEUVER OR SUPPORT OR VESSEL ->
~1.6M records), so it's useless for our program-name discovery. USAspending keyword
search does a clean phrase match. FPDS is reserved for its real strength downstream:
authoritative per-mod action detail pulled by VENDOR_NAME (reliable).

Scope: Army + USACE/ERDC only (Navy dropped per direction). We pull DoD-wide /
unrestricted and POST-FILTER to Army+USACE on the awarding/funding agency strings,
so we never miss a watercraft award filed under an unexpected agency code, and we
learn the real agency labels empirically (logged).

Two axes:
  - KEYWORD  : program names + USV/autonomy terms (agency-unrestricted, post-filtered)
  - NAICS/PSC: shipbuilding/boat + small-craft/vessel codes (DoD-scoped to bound volume)

award_type contracts (A-D) and IDVs (IDV_*) are queried separately (mixing -> HTTP 422).

Outputs:
  usaspending_raw/discovery_<slug>_<contract|idv>.json   full returned records (raw tier)
  extracted/contracts_discovered_all.csv                 every hit + in_scope flag
  extracted/contracts_discovered.csv                     Army+USACE in-scope only
  extracted/_discovered_piids.json                       seed handles for stages 2-6
  pull_logs/usaspending_discovery.log
"""
from __future__ import annotations

import csv
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import http_post_json, slugify, write_json  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]            # research/contracts/
RAW = ROOT / "usaspending_raw"
EXTRACT = ROOT / "extracted"
LOG = ROOT / "pull_logs" / "usaspending_discovery.log"

ENDPOINT = "https://api.usaspending.gov/api/v2/search/spending_by_award/"
TIME_PERIOD = [{"start_date": "2015-01-01", "end_date": "2026-12-31"}]
FIELDS = ["Award ID", "Recipient Name", "Awarding Agency", "Awarding Sub Agency",
          "Funding Agency", "Funding Sub Agency", "Award Amount", "Description",
          "Contract Award Type", "Start Date", "End Date", "NAICS", "PSC"]
CONTRACT_CODES = ["A", "B", "C", "D"]
IDV_CODES = ["IDV_A", "IDV_B", "IDV_C", "IDV_D", "IDV_E"]
# Code-axis scope: awarding SUBTIER "Department of the Army". Calibration win
# (see log 2026-06-20) — USACE engineer-district awards (PIID W912xx) also file
# under this subtier, so it captures Army + USACE and excludes Navy. Scoping the
# code axis here (vs DoD-wide) makes the 1,500-record cap apply WITHIN Army, so
# the Army tail below top-1500-by-amount is no longer crowded out by Navy hulls
# (gotcha #6). NO toptier_name disambiguator on purpose: the subtier name alone
# is unique and resolves correctly (verified live), so the pull is immune to the
# DoD -> "Department of War" toptier rename (a "Department of War" toptier filter
# returns 0 rows today; "Department of Defense" works — but don't depend on either).
ARMY_SUBTIER = [{"type": "awarding", "tier": "subtier",
                 "name": "Department of the Army"}]

# anchor program names (from the funding layer) + USV/autonomy maritime terms
KEYWORD_QUERIES = [
    "maneuver support vessel", "army watercraft", "watercraft extended service",
    "modernized integrated bridge system", "harbormaster command and control",
    "landing craft utility", "logistic support vessel", "maneuver support vessel light",
    "modular causeway", "lighterage", "marine oriented logistics",
    "unmanned surface vessel", "autonomous surface vessel", "uncrewed surface vessel",
    "optionally manned surface", "robotic surface vessel",
]
# code axis: 336611 ship building, 336612 boat building; PSC 1905 combat ships &
# landing vessels, 1925 special service vessels, 1940 small craft, 1990 misc vessels,
# 2090 misc ship & marine equipment.
CODE_QUERIES = [("naics", "336611"), ("naics", "336612"),
                ("psc", "1905"), ("psc", "1925"), ("psc", "1940"),
                ("psc", "1990"), ("psc", "2090")]

KW_MAX_PAGES = 10
CODE_MAX_PAGES = 15
PAGE_SIZE = 100


def in_scope(rec: dict) -> bool:
    """Army + USACE/ERDC only. Match on awarding/funding agency strings."""
    blob = " ".join(str(rec.get(k) or "") for k in
                    ("Awarding Agency", "Awarding Sub Agency",
                     "Funding Agency", "Funding Sub Agency")).lower()
    return ("army" in blob) or ("corps of engineers" in blob) or ("engineer" in blob)


def run_query(label, base_filters, max_pages, log):
    """Run a single discovery query across both award-type groups; return all records
    (with provenance) and write the raw per-group responses."""
    out = []
    for grp_name, codes in (("contract", CONTRACT_CODES), ("idv", IDV_CODES)):
        filters = dict(base_filters)
        filters["time_period"] = TIME_PERIOD
        filters["award_type_codes"] = codes
        page = 1
        grp_records = []
        while page <= max_pages:
            body = {"filters": filters, "fields": FIELDS, "sort": "Award Amount",
                    "order": "desc", "limit": PAGE_SIZE, "page": page}
            data, status = http_post_json(ENDPOINT, body)
            if data is None:
                log(f"      [{grp_name}] page {page}: NO RESPONSE (status {status})")
                break
            if status != 200:
                detail = data.get("detail") or data.get("messages") or data
                log(f"      [{grp_name}] page {page}: HTTP {status}: {str(detail)[:160]}")
                break
            results = data.get("results", [])
            for r in results:
                r["_matched_query"] = label
                r["_award_type_group"] = grp_name
            grp_records.extend(results)
            has_next = (data.get("page_metadata") or {}).get("hasNext", False)
            if not results or not has_next:
                break
            page += 1
            time.sleep(0.25)
        log(f"      [{grp_name}] {len(grp_records)} records")
        write_json(RAW / f"discovery_{slugify(label)}_{grp_name}.json",
                   {"label": label, "filters": base_filters, "award_type_group": grp_name,
                    "record_count": len(grp_records), "results": grp_records})
        out.extend(grp_records)
    return out


def main():
    EXTRACT.mkdir(parents=True, exist_ok=True)
    LOG.parent.mkdir(parents=True, exist_ok=True)
    logf = open(LOG, "w")

    def log(msg):
        print(msg, flush=True)
        logf.write(msg + "\n")
        logf.flush()

    log(f"=== USAspending discovery {time.strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"time_period={TIME_PERIOD}")
    all_records = []

    log("\n# KEYWORD axis (agency-unrestricted, post-filtered to Army+USACE)")
    for kw in KEYWORD_QUERIES:
        log(f"  - keyword: {kw!r}")
        recs = run_query(kw, {"keywords": [kw]}, KW_MAX_PAGES, log)
        for r in recs:
            r["_matched_axis"] = "keyword"
        all_records.extend(recs)

    log("\n# NAICS/PSC axis (Army-subtier-scoped so the 1500 cap applies WITHIN Army)")
    for kind, code in CODE_QUERIES:
        label = f"{kind}:{code}"
        log(f"  - {label}")
        filt = {"agencies": ARMY_SUBTIER, (f"{kind}_codes"): [code]}
        recs = run_query(label, filt, CODE_MAX_PAGES, log)
        for r in recs:
            r["_matched_axis"] = label
        all_records.extend(recs)

    # ---- consolidate: dedup by generated_internal_id, union provenance ----
    by_id = {}
    agencies_seen = {}
    for r in all_records:
        gid = r.get("generated_internal_id") or r.get("Award ID")
        if not gid:
            continue
        sub = r.get("Awarding Sub Agency") or r.get("Awarding Agency") or "(none)"
        agencies_seen[sub] = agencies_seen.get(sub, 0) + 1
        cur = by_id.get(gid)
        if cur is None:
            r["_matched_queries"] = {r.get("_matched_query")}
            r["_matched_axes"] = {r.get("_matched_axis")}
            by_id[gid] = r
        else:
            cur["_matched_queries"].add(r.get("_matched_query"))
            cur["_matched_axes"].add(r.get("_matched_axis"))

    rows = []
    for gid, r in by_id.items():
        rows.append({
            "generated_internal_id": gid,
            "award_id": r.get("Award ID"),
            "recipient_name": r.get("Recipient Name"),
            "award_amount": r.get("Award Amount"),
            "contract_award_type": r.get("Contract Award Type"),
            "award_type_group": r.get("_award_type_group"),
            "awarding_agency": r.get("Awarding Agency"),
            "awarding_sub_agency": r.get("Awarding Sub Agency"),
            "funding_agency": r.get("Funding Agency"),
            "funding_sub_agency": r.get("Funding Sub Agency"),
            "naics": r.get("NAICS"),
            "psc": r.get("PSC"),
            "start_date": r.get("Start Date"),
            "end_date": r.get("End Date"),
            "in_scope": "yes" if in_scope(r) else "no",
            "matched_axes": "; ".join(sorted(a for a in r["_matched_axes"] if a)),
            "matched_queries": "; ".join(sorted(q for q in r["_matched_queries"] if q)),
            "description": (r.get("Description") or "")[:400],
        })
    rows.sort(key=lambda x: (x["in_scope"] != "yes", -(x["award_amount"] or 0)))

    cols = ["generated_internal_id", "award_id", "recipient_name", "award_amount",
            "contract_award_type", "award_type_group", "awarding_agency",
            "awarding_sub_agency", "funding_agency", "funding_sub_agency", "naics",
            "psc", "start_date", "end_date", "in_scope", "matched_axes",
            "matched_queries", "description"]

    def dump_csv(path, only_in_scope):
        with open(path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            for row in rows:
                if only_in_scope and row["in_scope"] != "yes":
                    continue
                w.writerow(row)

    dump_csv(EXTRACT / "contracts_discovered_all.csv", False)
    dump_csv(EXTRACT / "contracts_discovered.csv", True)

    seeds = [{"generated_internal_id": row["generated_internal_id"],
              "piid": row["award_id"], "recipient": row["recipient_name"],
              "award_amount": row["award_amount"], "matched_axes": row["matched_axes"]}
             for row in rows if row["in_scope"] == "yes"]
    write_json(EXTRACT / "_discovered_piids.json", seeds)

    n_in = sum(1 for r in rows if r["in_scope"] == "yes")
    log(f"\n=== consolidated: {len(rows)} unique awards; {n_in} in-scope (Army+USACE), "
        f"{len(rows) - n_in} out-of-scope.")
    log("\nTop awarding sub-agencies seen (calibration):")
    for sub, n in sorted(agencies_seen.items(), key=lambda kv: -kv[1])[:20]:
        log(f"  {n:5d}  {sub}")
    log("\nTop 25 in-scope awards by amount:")
    for row in [r for r in rows if r["in_scope"] == "yes"][:25]:
        amt = row["award_amount"] or 0
        log(f"  ${amt/1e6:>9,.1f}M  {(row['award_id'] or '')[:18]:18s}  "
            f"{(row['recipient_name'] or '')[:32]:32s}  {(row['awarding_sub_agency'] or '')[:28]:28s}  "
            f"{(row['matched_axes'] or '')[:40]}")
    logf.close()


if __name__ == "__main__":
    main()
