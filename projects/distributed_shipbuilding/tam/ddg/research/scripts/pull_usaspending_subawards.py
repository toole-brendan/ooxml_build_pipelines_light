#!/usr/bin/env python3
"""
Pull first-tier subawards from USAspending for DDG-51 prime PIIDs.

Two-call pattern per Federal_Procurement_Research_Lessons_Learned.md section 5:
  1. POST /api/v2/search/spending_by_award/ with {award_ids: [PIID]} to get
     generated_internal_id
  2. POST /api/v2/subawards/ with {award_id: <gid>} to get subaward records

For PIIDs that don't resolve under the Contracts group [A,B,C,D], retry with the
IDV group. (HTTP 422 if you mix groups in one call.)

The /subawards/ endpoint caps at ~2,000 records per prime. For DDG MYP masters
(FY18-22 + FY23-27, two per MYP — one per yard) we may hit the cap. Sort by amount
desc to get top sub spend first; SAM.gov pull (sibling script) recovers the long tail.

Output: usaspending_subawards/<piid>_subawards.json (one file per PIID)
        usaspending_subawards/_seed_lookup.json
        usaspending_subawards/_summary.json

Run order:
  1. python3 pull_fpds_ddg_primes.py        (discovers candidate PIIDs)
  2. python3 pull_usaspending_subawards.py --discover
        ↑ --discover reads the FPDS pulls and picks the top DDG PIIDs as seeds.
        Without --discover, the SEED_PIIDS list is empty and nothing is fetched.
"""
import json
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

OUT_DIR = "/Users/brendantoole/projects2/destroyer_outsourced_work/usaspending_subawards"
os.makedirs(OUT_DIR, exist_ok=True)

BASE = "https://api.usaspending.gov/api/v2"
HDRS = {
    "Content-Type": "application/json",
    "User-Agent": "ddg-outsourcing-research/1.0",
    "Accept": "application/json",
}

# DDG-51 has NO pre-seeded PIID list (unlike subs, which had prior analysis with 17
# named PIIDs). Run with --discover to derive seed PIIDs from the FPDS pulls.
# Format: (PIID, label, vendor-group)
SEED_PIIDS = []


def post_json(url, payload, tries=3):
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(tries):
        try:
            req = Request(url, data=body, headers=HDRS, method="POST")
            with urlopen(req, timeout=90) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 422:
                err_body = e.read().decode("utf-8", errors="replace")[:500]
                return {"_error": f"HTTP 422: {err_body}"}
            if attempt == tries - 1:
                return {"_error": f"HTTP {e.code}: {e.reason}"}
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == tries - 1:
                return {"_error": str(e)}
            time.sleep(2 ** attempt)
    return {"_error": "exhausted retries"}


CONTRACTS_GROUP = ["A", "B", "C", "D"]
IDV_GROUP = ["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]


def find_generated_internal_id(piid):
    """Try Contracts group first, then IDV group. Return (gid, group, recipient,
    amount, full_record) or (None, None, None, None, None) if not found."""
    for group_name, group in (("contracts", CONTRACTS_GROUP), ("idvs", IDV_GROUP)):
        payload = {
            "filters": {
                "award_type_codes": group,
                "award_ids": [piid],
                "time_period": [{"start_date": "2007-10-01", "end_date": "2027-09-30"}],
            },
            "fields": ["Award ID", "generated_internal_id", "Recipient Name",
                       "Award Amount", "Total Outlays", "Description",
                       "Start Date", "End Date", "Awarding Agency"],
            "limit": 25,
            "page": 1,
        }
        data = post_json(f"{BASE}/search/spending_by_award/", payload)
        if "_error" in data:
            print(f"    [{piid}/{group_name}] lookup error: {data['_error']}", flush=True)
            continue
        results = data.get("results", [])
        if results:
            r = results[0]
            return (r.get("generated_internal_id"), group_name,
                    r.get("Recipient Name"), r.get("Award Amount"), r)
    return (None, None, None, None, None)


def fetch_subawards(gid, max_pages=25):
    """Pull all subawards for a generated_internal_id. Sort by amount desc to get
    top sub spend first (in case we hit the ~2000-record cap)."""
    out = []
    page = 1
    while page <= max_pages:
        payload = {
            "award_id": gid,
            "limit": 100,
            "page": page,
            "sort": "amount",
            "order": "desc",
        }
        data = post_json(f"{BASE}/subawards/", payload)
        if "_error" in data:
            print(f"      page {page} error: {data['_error']}", flush=True)
            break
        results = data.get("results", [])
        if not results:
            break
        out.extend(results)
        meta = data.get("page_metadata") or {}
        if not meta.get("hasNext"):
            break
        page += 1
        time.sleep(0.5)
    return out


# Vendor-name patterns for the DDG primes + GFE vendors. Discovery picks top DDG
# PIIDs from FPDS raw by these vendor groups.
DDG_VENDOR_GROUPS = {
    "HII-Ingalls": ("INGALLS SHIPBUILDING", "HUNTINGTON INGALLS"),
    "GD-BIW": ("BATH IRON WORKS",),
    "LM-Aegis": ("LOCKHEED MARTIN",),
    "Raytheon": ("RAYTHEON", "RTX"),
    "GE-Propulsion": ("GENERAL ELECTRIC", "GE AEROSPACE"),
    "BAE-Guns/VLS": ("BAE SYSTEMS",),
    "L3Harris": ("L3HARRIS", "L3 TECHNOLOGIES"),
    "NG": ("NORTHROP GRUMMAN",),
    "DRS": ("LEONARDO DRS", "DRS SYSTEMS", "DRS LAUREL", "DRS NAVAL"),
}


def vendor_to_group(vendor_name):
    if not vendor_name:
        return None
    upper = vendor_name.upper()
    for group, patterns in DDG_VENDOR_GROUPS.items():
        for pat in patterns:
            if pat in upper:
                return group
    return None


def discover_from_fpds(per_yard_top=30, per_other_top=15, min_dollar=50_000_000):
    """Read /fpds_raw/*_raw.json, aggregate by PIID, return top N PIIDs per vendor
    group. Yards (HII-Ingalls, GD-BIW) get a higher top-N because they're the
    in-scope DDG primes; GFE vendors get fewer (we want the DDG-tagged primes
    only)."""
    fpds_dir = "/Users/brendantoole/projects2/destroyer_outsourced_work/fpds_raw"
    if not os.path.isdir(fpds_dir):
        print(f"!! {fpds_dir} not present — run pull_fpds_ddg_primes.py first")
        return []
    by_piid = {}  # piid → {vendor, group, total_obligated, description, signed_date}
    for fname in sorted(os.listdir(fpds_dir)):
        if not fname.endswith("_raw.json") or fname.startswith("_"):
            continue
        with open(os.path.join(fpds_dir, fname)) as f:
            data = json.load(f)
        for r in data.get("records", []):
            p = r.get("piid")
            if not p:
                continue
            group = vendor_to_group(r.get("vendor_name"))
            if not group:
                continue
            # Keep the latest-mod (max signed_date) per PIID
            prev = by_piid.get(p)
            if prev is None or (r.get("signed_date") or "") > (prev.get("signed_date") or ""):
                by_piid[p] = {
                    "vendor": r.get("vendor_name"),
                    "group": group,
                    "total_obligated": r.get("total_obligated") or 0,
                    "description": (r.get("description") or "")[:120],
                    "signed_date": r.get("signed_date"),
                    "naics": r.get("naics"),
                    "psc": r.get("psc"),
                }
    # Bucket per group, take top per_yard_top for yards / per_other_top for others,
    # subject to min_dollar floor.
    by_group = {}
    for piid, meta in by_piid.items():
        if (meta["total_obligated"] or 0) < min_dollar:
            continue
        by_group.setdefault(meta["group"], []).append((piid, meta))
    seeds = []
    for group, lst in by_group.items():
        lst.sort(key=lambda kv: kv[1]["total_obligated"], reverse=True)
        cap = per_yard_top if group in ("HII-Ingalls", "GD-BIW") else per_other_top
        for piid, meta in lst[:cap]:
            label = f"{group}: {meta['description']}"
            seeds.append((piid, label, meta["vendor"]))
    return seeds


def main():
    discovered_pid_path = os.path.join(OUT_DIR, "_discovered_piids.json")
    piids = list(SEED_PIIDS)

    if "--discover" in sys.argv:
        new = discover_from_fpds()
        with open(discovered_pid_path, "w") as f:
            json.dump(new, f, indent=2)
        print(f"+ Discovered {len(new)} candidate DDG PIIDs from FPDS raw", flush=True)
        # Dedupe against any explicit SEED_PIIDS
        seen = {p[0] for p in piids}
        for tup in new:
            if tup[0] not in seen:
                piids.append(tup)
                seen.add(tup[0])

    if not piids:
        print("No PIIDs to process. Run with --discover after the FPDS pull completes.")
        return

    summary = {}
    seed_lookup = {}
    for piid, label, vendor in piids:
        print(f"\n[{piid}] {label[:80]}", flush=True)
        gid, group, recipient, amount, full_record = find_generated_internal_id(piid)
        if not gid:
            print(f"    !! no generated_internal_id found", flush=True)
            summary[piid] = {"label": label, "vendor": vendor, "found": False}
            continue
        print(f"    → gid={gid} ({group}) recipient={recipient} amount=${(amount or 0)/1e6:.1f}M",
              flush=True)
        seed_lookup[piid] = {
            "gid": gid,
            "group": group,
            "recipient": recipient,
            "amount": amount,
            "full_search_record": full_record,
        }
        subs = fetch_subawards(gid)
        print(f"    + pulled {len(subs)} subawards", flush=True)
        total_sub = sum((s.get("amount") or 0) for s in subs)
        by_recip = {}
        for s in subs:
            r = (s.get("recipient_name") or "UNKNOWN").upper().strip()
            by_recip.setdefault(r, {"count": 0, "amount": 0.0})
            by_recip[r]["count"] += 1
            by_recip[r]["amount"] += s.get("amount") or 0
        top5 = sorted(by_recip.items(), key=lambda kv: kv[1]["amount"], reverse=True)[:5]
        print(f"    TOP SUBS: " + "; ".join(
            f"{r[:40]}=${a['amount']/1e6:.1f}M" for r, a in top5
        ), flush=True)

        out_path = os.path.join(OUT_DIR, f"{piid}_subawards.json")
        with open(out_path, "w") as f:
            json.dump({
                "piid": piid,
                "label": label,
                "vendor": vendor,
                "gid": gid,
                "group": group,
                "prime_recipient": recipient,
                "prime_amount": amount,
                "subaward_count": len(subs),
                "subaward_total": total_sub,
                "subawards": subs,
            }, f, indent=2, default=str)
        summary[piid] = {
            "label": label,
            "vendor": vendor,
            "gid": gid,
            "group": group,
            "prime_recipient": recipient,
            "prime_amount": amount,
            "subaward_count": len(subs),
            "subaward_total": total_sub,
            "output_file": out_path,
            "found": True,
        }
        time.sleep(0.3)

    with open(os.path.join(OUT_DIR, "_seed_lookup.json"), "w") as f:
        json.dump(seed_lookup, f, indent=2, default=str)
    with open(os.path.join(OUT_DIR, "_summary.json"), "w") as f:
        json.dump({
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "piids": summary,
        }, f, indent=2, default=str)
    print(f"\nDone. Summary -> {OUT_DIR}/_summary.json", flush=True)


if __name__ == "__main__":
    main()
