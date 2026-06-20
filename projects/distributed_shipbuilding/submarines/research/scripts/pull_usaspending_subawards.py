#!/usr/bin/env python3
"""
Pull first-tier subawards from USAspending for known submarine prime PIIDs.

Two-call pattern per Federal_Procurement_Research_Lessons_Learned.md section 5:
  1. POST /api/v2/search/spending_by_award/ with {award_ids: [PIID]} to get
     generated_internal_id
  2. POST /api/v2/subawards/ with {award_id: <gid>} to get subaward records

For PIIDs that don't resolve under the Contracts group [A,B,C,D], retry with the
IDV group. (HTTP 422 if you mix groups in one call.)

The /subawards/ endpoint caps at ~2,000 records per prime. For the two big submarine
masters (N0002417C2100 + N0002417C2117) we'll hit the cap; that's a known limitation
documented in the lessons-learned. Sort by amount desc to get the top sub spend first.

Output: usaspending_subawards/<piid>_subawards.json (one file per PIID)
        usaspending_subawards/_seed_lookup.json (PIID → generated_internal_id mapping)
        usaspending_subawards/_summary.json (totals per PIID)
"""
import json
import os
import sys
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

OUT_DIR = "/Users/brendantoole/projects2/submarine_outsourced_work/usaspending_subawards"
os.makedirs(OUT_DIR, exist_ok=True)

BASE = "https://api.usaspending.gov/api/v2"
HDRS = {
    "Content-Type": "application/json",
    "User-Agent": "sub-outsourcing-research/1.0",
    "Accept": "application/json",
}

# Seed PIIDs from prior FY20-26 submarine analysis (Section "Key known PIIDs" in README)
SEED_PIIDS = [
    # ---- GDEB submarine construction primes ----
    ("N0002417C2100", "GDEB Virginia Block V / Block VI master", "GDEB"),
    ("N0002417C2117", "GDEB Columbia Build I + Build II", "GDEB"),
    ("N0002412C2115", "GDEB Virginia Block IV MYP", "GDEB"),
    ("N0002424C2110", "GDEB Virginia Block VI LLTM", "GDEB"),
    ("N0002409C2104", "GDEB Virginia Block II (residual)", "GDEB"),
    ("N0002413C2128", "GDEB Columbia Design Drawings", "GDEB"),
    ("N0002419C2125", "GDEB Virginia Tech Instructions / HPAD backfit", "GDEB"),
    ("N0002416C2111", "GDEB VPM Ventilation Valve", "GDEB"),
    ("N0002410C2118", "GDEB VPM Tube Fabrication", "GDEB"),
    ("N0002411C2109", "GDEB SSBN-R concept formulation", "GDEB"),
    ("N0002420C4312", "GDEB USS Hartford (SSN 768) EOH", "GDEB"),

    # ---- Bechtel Plant Machinery (naval reactor GFE) ----
    ("N0002419C2114", "BPMI Naval Reactor Components (Columbia)", "BPMI"),
    ("N0002419C2115", "BPMI Columbia Class Industrial Base Increase", "BPMI"),
    ("N0002424C2114", "BPMI S9G reactor (Virginia / Columbia)", "BPMI"),

    # ---- Other major GFE primes named in prior analysis ----
    ("N0002410C6266", "LM Virginia Combat Systems hardware/software", "Lockheed Martin"),
    ("N0002421C4106", "BAE SSN 812 Forward Subassembly", "BAE Systems"),
    ("N0002421C4111", "Rolls-Royce Virginia Class Submarine Rotor", "Rolls-Royce"),
]


def post_json(url, payload, tries=3):
    body = json.dumps(payload).encode("utf-8")
    for attempt in range(tries):
        try:
            req = Request(url, data=body, headers=HDRS, method="POST")
            with urlopen(req, timeout=90) as r:
                return json.loads(r.read())
        except HTTPError as e:
            if e.code == 422:
                # Bad payload shape — don't retry, return error info
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
    """Try Contracts group first, then IDV group. Return (gid, group, recipient, amount)
    or (None, None, None, None) if not found."""
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


def main():
    discovered_pid_path = os.path.join(OUT_DIR, "_discovered_piids.json")
    piids = list(SEED_PIIDS)

    # If --discover passed, also pull top PIIDs from the FPDS raw output and add to list
    if "--discover" in sys.argv:
        fpds_summary = "/Users/brendantoole/projects2/submarine_outsourced_work/fpds_raw/_summary.json"
        if os.path.exists(fpds_summary):
            # Look in each per-query raw file for big-dollar PIIDs we haven't already seeded
            seen = {p[0] for p in piids}
            new = []
            for slug in ("gdeb_navy", "bpmi_navy", "desc_virginia_class", "desc_columbia_class",
                         "desc_submarine_navy_big"):
                path = f"/Users/brendantoole/projects2/submarine_outsourced_work/fpds_raw/{slug}_raw.json"
                if not os.path.exists(path):
                    continue
                with open(path) as f:
                    data = json.load(f)
                # Aggregate by PIID using max-signed-date mod's totalObligated
                by_piid = {}
                for r in data.get("records", []):
                    p = r.get("piid")
                    if not p or p in seen:
                        continue
                    prev = by_piid.get(p)
                    if prev is None or (r.get("signed_date") or "") > (prev.get("signed_date") or ""):
                        by_piid[p] = r
                # Take top 20 by total_obligated
                top = sorted(by_piid.items(),
                              key=lambda kv: kv[1].get("total_obligated") or 0,
                              reverse=True)[:20]
                for p, r in top:
                    if (r.get("total_obligated") or 0) < 100_000_000:
                        continue  # skip <$100M
                    label = f"{slug}: {(r.get('description') or '')[:80]}"
                    vendor = r.get("vendor_name") or ""
                    new.append((p, label, vendor))
                    seen.add(p)
            piids.extend(new)
            with open(discovered_pid_path, "w") as f:
                json.dump(new, f, indent=2)
            print(f"+ Discovered {len(new)} additional PIIDs from FPDS raw")

    summary = {}
    seed_lookup = {}
    for piid, label, vendor in piids:
        print(f"\n[{piid}] {label}", flush=True)
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
        # Distinct recipients
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
