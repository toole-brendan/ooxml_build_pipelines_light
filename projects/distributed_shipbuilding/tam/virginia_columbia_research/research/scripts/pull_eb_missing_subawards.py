#!/usr/bin/env python3
"""Pull SAM.gov first-tier subawards for candidate EB NAVSEA primes missing from
nc_scope_summary.json, to (1) complete the EB-reported denominator and (2) re-test
whether HII Newport News (UEI WMXDDH6HJNA5) appears anywhere in the full EB prime set.

Writes raw JSON ({piid, published[], deleted[]}) into sam_subawards_fullhistory/ in
the SAME shape build_program_transactions.py expects. Files for PIIDs not yet in
in_scope_piids are simply ignored by the generator until added to scope.

HOWTO-compliant: IPv4 monkeypatch (macOS IPv6 hang), lowercase piid, /prod/ path,
nextPageLink filter check, Published+Deleted, no dedup (subAwardReportId unique).
"""
import socket
# Force IPv4 BEFORE urllib import — see SAM_GOV_HOWTO.md (else ~225s/page on macOS).
_orig = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4

import datetime as _dt
import json, os, sys, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
HDRS = {"User-Agent": "sub-outsourcing-research/1.0", "Accept": "application/json"}
REPO = Path("/Users/brendantoole/projects3/ooxml_build_pipelines_light")
ENV = REPO / ".env"
OUT_DIR = REPO / "projects/distributed_shipbuilding/tam/virginia_columbia_research/research/sam_subawards_fullhistory"
HII_UEI = "WMXDDH6HJNA5"
PAGE_SIZE = 1000
FROM_DATE, TO_DATE = "2008-01-01", _dt.date.today().isoformat()

# Candidate EB NAVSEA primes (from discover_eb_primes_fpds + cached broad pull).
# C2xxx = new-construction series (in-scope class); C2120 = doc-claimed "Lead Yard"
# (FPDS-invisible — test directly). Maintenance C4xxx / SSP N00030 deliberately omitted.
CANDIDATES = [
    "N0002420C2120",  # "Lead Yard Support" $4.3B — 670 subs — ADD (same class as in-scope C2111/C2118)
    "N0002414C2104",  # "Submarine Planning Yard" $922M — 1093 subs — ADD
    "N0002421C2103",  # "FY21 CONFORM" $194M — 64 subs — verify construction vs reactor
    "N0002420C2114",  # "NAVAL REACTORS" $212M — 39 subs — pull to confirm reactor → exclude
]


def load_key():
    for line in ENV.read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in .env")


def call(key, piid, page, status):
    # NB casing FLIPPED since SAM_GOV_HOWTO.md (2026-05): as of 2026-06-21 the piid
    # filter is case-SENSITIVE and wants UPPERCASE no-dash (lowercase → 0 records
    # silently; dashed → HTTP 400). Verified: N0002417C2100 upper=5687 / lower=0.
    params = {"api_key": key, "piid": piid.upper(), "pageNumber": page,
              "pageSize": PAGE_SIZE, "status": status,
              "fromDate": FROM_DATE, "toDate": TO_DATE}
    req = Request(f"{BASE}?{urlencode(params)}", headers=HDRS, method="GET")
    try:
        with urlopen(req, timeout=120) as r:
            return json.loads(r.read())
    except HTTPError as e:
        if e.code == 429:
            raise SystemExit(f"HTTP 429 quota exhausted: {e.read()[:200]}")
        raise


def fetch_all(key, piid, status):
    recs, page = [], 0
    while True:
        body = call(key, piid, page, status)
        data = body.get("data") or []
        nxt = body.get("nextPageLink") or ""
        if page == 0 and nxt and "piid=" not in nxt.lower():
            raise RuntimeError(f"{piid}: piid filter dropped (nextPageLink={nxt[:120]})")
        recs.extend(data)
        if not nxt or not data:
            break
        page += 1
        time.sleep(0.35)
    return recs


def main():
    key = load_key()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"key prefix {key[:9]}...  out={OUT_DIR}\n")
    summary = []
    for piid in CANDIDATES:
        out = OUT_DIR / f"{piid}_subawards.json"
        tag = " (exists, repull)" if out.exists() else ""
        try:
            pub = fetch_all(key, piid, "Published")
            det = fetch_all(key, piid, "Deleted")
        except SystemExit as e:
            print(f"HALT on {piid}: {e}"); break
        tot = sum(float(r.get("subAwardAmount") or 0) for r in pub)
        hii = [r for r in pub if (r.get("subEntityUei") or "") == HII_UEI
               or (r.get("subParentUei") or "") == HII_UEI]
        hii_det = [r for r in det if (r.get("subEntityUei") or "") == HII_UEI
                   or (r.get("subParentUei") or "") == HII_UEI]
        hii_tot = sum(float(r.get("subAwardAmount") or 0) for r in hii)
        # top vendors
        by = {}
        for r in pub:
            n = (r.get("subEntityParentLegalBusinessName") or r.get("subEntityLegalBusinessName") or "?").upper()[:34]
            by[n] = by.get(n, 0.0) + float(r.get("subAwardAmount") or 0)
        top = sorted(by.items(), key=lambda kv: -kv[1])[:4]
        out.write_text(json.dumps({
            "piid": piid, "fetched_at": _dt.datetime.now().isoformat(),
            "from_date": FROM_DATE, "to_date": TO_DATE,
            "published_count": len(pub), "deleted_count": len(det),
            "published_total_$": tot, "hii_record_count": len(hii),
            "hii_total_$": hii_tot, "published": pub, "deleted": det,
        }, indent=2, default=str))
        print(f"{piid}{tag}: pub={len(pub):>5}  ${tot/1e6:>9,.1f}M  del={len(det):>3}  "
              f"HII={len(hii)} (${hii_tot/1e6:,.2f}M, del {len(hii_det)})")
        print(f"     top: " + "; ".join(f"{n[:28]}=${a/1e6:.1f}M" for n, a in top))
        summary.append({"piid": piid, "pub": len(pub), "total_$M": tot / 1e6,
                        "hii_recs": len(hii), "hii_$M": hii_tot / 1e6})
    print("\n=== SUMMARY ===")
    for s in summary:
        print(f"  {s['piid']}: {s['pub']:>5} subs  ${s['total_$M']:>9,.1f}M  "
              f"HII {s['hii_recs']} recs ${s['hii_$M']:,.2f}M")
    tot_hii = sum(s["hii_recs"] for s in summary)
    print(f"\nHII RE-TEST across {len(summary)} candidate primes: "
          f"{tot_hii} HII subaward records found"
          + ("" if tot_hii else "  → still ZERO; 'exhausted' conclusion strengthened"))


if __name__ == "__main__":
    main()
