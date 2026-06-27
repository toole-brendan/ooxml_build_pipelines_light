#!/usr/bin/env python3
"""Build the provenance for the Army watercraft non-nuclear ship-repair multiple-award
IDIQ pool -- the awards-methodology slide example of a CONTESTABLE recompete (an
on-ramp), as opposed to the closed dual-source DDG-51 multi-year procurement.

Primary source is SAM.gov Contract Awards (the modern successor feed): it carries each
holder IDV's award type, the LAST DATE TO ORDER (ordering-period end, FAR 16.505), the
shared solicitation number, ceiling, competition, and the count/dollars of referencing
delivery orders. USAspending confirms the IDV dates/ceiling. The delivery-order money
and appropriations (TAS) live on the child orders -- a multiple-award IDV itself holds
$0 and reports no File-C -- so the realized-dollar + per-fiscal-year + TAS layer is
aggregated from the Army contracts extract (USAspending-lineage), and cross-checked
against SAM's referencing-orders totals.

Outputs (extracted/):
  shiprepair_pool_holders.csv       one row per holder IDV (every field)
  shiprepair_pool_summary.json      pool-level rollup (holders, solicitations, money)
  shiprepair_order_obligation_by_fy.csv   holder x fiscal-year realized obligation
Raw kept under sam_contract_awards/ and usaspending_raw/detail/.

Run:  python3 build_shiprepair_pool.py
"""
from __future__ import annotations

import csv
import json
import os
import sys
import time
import urllib.parse
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlencode

SCRIPTS = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/"
           "awards_methodology/saronic_specific_awards_data/research/contracts/scripts")
sys.path.insert(0, SCRIPTS)
from _common import env, http_get, http_post_json, write_json, QuotaExhausted  # noqa: E402

ARMY_CSV = ("/Users/brendantoole/projects3/ooxml_build_pipelines_light/projects/army/"
            "workbook/extracted/contract_awards.csv")
CA = "https://api.sam.gov/contract-awards/v1/search"
HERE = Path(__file__).resolve().parent
RAW_SAM = HERE / "sam_contract_awards"
RAW_USA = HERE / "usaspending_raw" / "detail"
EXTRACT = HERE / "extracted"

POOL_PREFIX = "W56HZV21DL"   # the Army watercraft ship-repair multiple-award family


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fed_fy(date_str):
    if not date_str or len(date_str) < 7:
        return None
    y, m = int(date_str[:4]), int(date_str[5:7])
    return y + 1 if m >= 10 else y


def deep(d, *p):
    for k in p:
        d = d.get(k) if isinstance(d, dict) else None
    return d


# ---- roster + delivery-order layer from the Army extract --------------------
def load_orders():
    rows = list(csv.DictReader(open(ARMY_CSV)))
    kids = defaultdict(list)
    for r in rows:
        if (r.get("parent_idv_piid") or "").startswith(POOL_PREFIX):
            kids[r["parent_idv_piid"]].append(r)
    holders = sorted(kids)
    return kids, holders


# ---- SAM Contract Awards: holder IDV authority + last date to order ---------
def sam_idv(piid, key):
    path = RAW_SAM / f"{piid}.json"
    if path.exists():
        return json.loads(path.read_text())
    url = CA + "?" + urlencode({
        "api_key": key, "piid": piid, "piidAggregation": "yes",
        "includeSections": "contractId,coreData,awardDetails", "limit": 100, "offset": 0})
    txt, st = http_get(url, headers={"Accept": "application/json"})
    if st == 429:
        raise QuotaExhausted("SAM 429 -- daily quota exhausted.")
    b = json.loads(txt) if (txt and st == 200) else {}
    out = {"piid": piid, "records": [r for r in (b.get("awardSummary") or [])
                                     if deep(r, "contractId", "piid") == piid],
           "piidAggregation": b.get("piidAggregation")}
    write_json(path, out)
    time.sleep(0.3)
    return out


def sam_extract(data):
    recs = data.get("records") or []
    if not recs:
        return {}
    base = min((r for r in recs if deep(r, "awardDetails", "dates", "dateSigned")),
               key=lambda r: deep(r, "awardDetails", "dates", "dateSigned"), default=recs[0])
    core = base.get("coreData") or {}
    det = base.get("awardDetails") or {}
    comp = core.get("competitionInformation") or {}
    fo = deep(core, "federalOrganization", "contractingInformation", "contractingOffice") or {}
    refs = deep(data, "piidAggregation", "referencingDosOrBpaCallsSummary") or {}
    return {
        "award_type": deep(core, "awardOrIDVType", "name"),
        "type_of_idc": deep(core, "acquisitionData", "typeOfIdc", "name"),
        "solicitation_id": core.get("solicitationId"),
        "last_date_to_order": (deep(det, "dates", "lastDateToOrder") or "")[:10] or None,
        "ordering_pop_start": (deep(det, "dates", "periodOfPerformanceStartDate") or "")[:10] or None,
        "pool_ceiling_$m": round((_f(deep(det, "totalContractDollars", "totalBaseAndAllOptionsValue")) or 0) / 1e6, 1),
        "extent_competed": deep(comp, "extentCompeted", "name"),
        "set_aside": deep(comp, "typeOfSetAside", "name"),
        "contracting_office": (f"{fo.get('code','')} {fo.get('name','')}").strip() or None,
        "sam_orders_count": refs.get("totalCount"),
        "sam_orders_$m": round((_f(refs.get("totalDollars")) or 0) / 1e6, 1),
    }


# ---- USAspending: confirm the IDV (holds $0; money is on the orders) --------
def usasp_idv(piid):
    gid = f"CONT_IDV_{piid}_9700"
    path = RAW_USA / f"{gid}.json"
    if path.exists():
        d = json.loads(path.read_text())
    else:
        txt, st = http_get("https://api.usaspending.gov/api/v2/awards/" + urllib.parse.quote(gid) + "/")
        d = json.loads(txt) if (txt and st == 200) else {}
        write_json(path, d)
        time.sleep(0.1)
    pop = d.get("period_of_performance") or {}
    return {
        "usasp_date_signed": d.get("date_signed"),
        "usasp_last_date_to_order": pop.get("end_date"),
        "usasp_idv_obligated_$m": round((_f(d.get("total_obligation")) or 0) / 1e6, 1),
    }


def main():
    for d in (RAW_SAM, RAW_USA, EXTRACT):
        d.mkdir(parents=True, exist_ok=True)
    key = env("SAM_API_KEY")
    kids, holders = load_orders()
    print(f"=== Army ship-repair pool ({POOL_PREFIX}*): {len(holders)} holder IDVs ===")

    rows, fy_rows = [], []
    for piid in holders:
        ch = kids[piid]
        sam = sam_extract(sam_idv(piid, key))
        usa = usasp_idv(piid)

        realized = sum(_f(c.get("obligation_amount")) or 0 for c in ch)
        dates = sorted(c.get("date_signed") for c in ch if c.get("date_signed"))
        tas = sorted({c.get("funding_tas") for c in ch if c.get("funding_tas")})
        tas_titles = sorted({c.get("funding_account_titles") for c in ch if c.get("funding_account_titles")})
        fair = sorted({c.get("fair_opportunity_limited") for c in ch if c.get("fair_opportunity_limited")})
        offers = sorted({c.get("number_of_offers") for c in ch if c.get("number_of_offers") not in (None, "", "0")})
        by_fy = defaultdict(float)
        for c in ch:
            fy = fed_fy(c.get("date_signed"))
            if fy:
                by_fy[fy] += _f(c.get("obligation_amount")) or 0
        for fy in sorted(by_fy):
            fy_rows.append({"piid": piid, "holder": ch[0].get("recipient_name"),
                            "fiscal_year": f"FY{fy}", "obligated_$m": round(by_fy[fy] / 1e6, 2)})

        rows.append({
            "piid": piid,
            "holder": ch[0].get("recipient_name"),
            "holder_uei": ch[0].get("recipient_uei"),
            "single_or_multiple_award": ch[0].get("single_or_multiple_award"),
            "award_type": sam.get("award_type"),
            "type_of_idc": sam.get("type_of_idc"),
            "solicitation_id": sam.get("solicitation_id"),
            "extent_competed": sam.get("extent_competed"),
            "set_aside": sam.get("set_aside"),
            "fair_opportunity_at_order": "; ".join(fair),
            "number_of_offers_at_order": "; ".join(str(o) for o in offers),
            "ordering_pop_start": sam.get("ordering_pop_start") or usa.get("usasp_date_signed"),
            "last_date_to_order": sam.get("last_date_to_order") or usa.get("usasp_last_date_to_order"),
            "pool_ceiling_$m": sam.get("pool_ceiling_$m"),
            "n_orders": len(ch),
            "realized_obligation_$m": round(realized / 1e6, 1),
            "first_order_date": dates[0] if dates else None,
            "last_order_date": dates[-1] if dates else None,
            "contracting_office": sam.get("contracting_office"),
            "psc": ch[0].get("psc_code"),
            "psc_desc": ch[0].get("psc_description"),
            "naics": ch[0].get("naics_code"),
            "tas_federal_accounts": "; ".join(tas),
            "tas_account_titles": "; ".join(tas_titles),
            "sam_orders_count": sam.get("sam_orders_count"),
            "sam_orders_$m": sam.get("sam_orders_$m"),
            "usasp_idv_obligated_$m": usa.get("usasp_idv_obligated_$m"),
        })
        print(f"  {piid} {(rows[-1]['holder'] or '?')[:24]:24} sol={sam.get('solicitation_id')} "
              f"LDO={rows[-1]['last_date_to_order']} ceil=${sam.get('pool_ceiling_$m')}M "
              f"orders={len(ch)} realized=${rows[-1]['realized_obligation_$m']}M")

    # ---- pool summary (ceilings are SHARED -> report tiers, never sum) -------
    by_sol = defaultdict(lambda: {"holders": [], "ceiling_$m": None})
    for r in rows:
        g = by_sol[r["solicitation_id"]]
        g["holders"].append(r["holder"])
        g["ceiling_$m"] = r["pool_ceiling_$m"]
    summary = {
        "pool_family": POOL_PREFIX,
        "n_holder_vehicles": len(rows),
        "n_distinct_vendors": len({r["holder"] for r in rows}),
        "vendors": sorted({r["holder"] for r in rows}),
        "common_last_date_to_order": sorted({r["last_date_to_order"] for r in rows if r["last_date_to_order"]}),
        "contracting_office": sorted({r["contracting_office"] for r in rows if r["contracting_office"]}),
        "competition": sorted({r["extent_competed"] for r in rows if r["extent_competed"]}),
        "route": "multiple-award IDIQ, FAR 16.505 fair-opportunity task orders (on-ramp at recompete)",
        "solicitation_tiers": {sol or "(none)": {"n_holders": len(g["holders"]),
                                                 "shared_ceiling_$m": g["ceiling_$m"],
                                                 "holders": sorted(set(g["holders"]))}
                               for sol, g in by_sol.items()},
        "total_realized_obligation_$m": round(sum(r["realized_obligation_$m"] for r in rows), 1),
        "total_orders": sum(r["n_orders"] for r in rows),
        "note": ("Ceilings are SHARED across holders within a solicitation tier -- never summed "
                 "(money-hygiene rule). Realized obligation = sum of delivery-order obligations, "
                 "the only summable measure."),
    }

    write_json(EXTRACT / "shiprepair_pool_summary.json", summary)
    cols = list(rows[0].keys())
    with open(EXTRACT / "shiprepair_pool_holders.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    with open(EXTRACT / "shiprepair_order_obligation_by_fy.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["piid", "holder", "fiscal_year", "obligated_$m"])
        w.writeheader()
        w.writerows(fy_rows)
    print(f"\n=== done. {len(rows)} holders, {summary['total_orders']} orders, "
          f"${summary['total_realized_obligation_$m']}M realized; "
          f"last date to order {summary['common_last_date_to_order']}; "
          f"{len(summary['solicitation_tiers'])} solicitation tier(s). ===")


if __name__ == "__main__":
    main()
