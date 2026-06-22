# SAM.gov API — Practical Guide

How to pull federal procurement data from SAM.gov's public APIs **correctly the first time**, written from production experience including every gotcha that cost us calls.

Last updated: 2026-06-21 — **the `piid` filter casing REVERSED** (see the ⚠ box directly below); also retains the 2026-05-23 macOS IPv6 / Python urllib slowness diagnosis (see "Critical: Force IPv4 in Python on macOS" below), confirmed across submarine + DDG-51 destroyer outsourcing pulls.

> ## ⚠⚠ BREAKING CHANGE 2026-06-21: the `piid` filter is now case-SENSITIVE and wants UPPERCASE
>
> The subaward-search `piid` filter flipped casing semantics between 2026-05 and 2026-06.
> **As of 2026-06-21, you MUST send the PIID in UPPERCASE, no dashes** (`N0002417C2100`):
>
> | form sent | result (2026-06-21) |
> |---|---|
> | `piid=N0002417C2100` (UPPERCASE, no dash) | **5687 records** ✅ |
> | `piid=n0002417c2100` (lowercase, no dash) | **0 records** — filter is echoed in `nextPageLink` but matches nothing, **silently** |
> | `piid=N00024-17-C-2100` / `n00024-17-c-2100` (dashed) | **HTTP 400 Bad Request** |
>
> This is the exact OPPOSITE of what the 2026-05 version of this guide said (lowercase).
> The failure mode is nasty: lowercase returns a clean `200` with `totalRecords: 0`, so it
> looks like "this prime has no subawards" rather than "your filter was mis-cased." If a PIID
> you expect to have subs returns 0, **re-test in UPPERCASE before concluding the gap is real.**
> Every code/table claim below that says "lowercase" is superseded by this box.

Companion to the broader FPDS / USAspending / SAM.gov field guide at `reference_prior_analysis/federal_procurement_data_guide.txt`.

---

## TL;DR

1. **You probably want the Acquisition Subaward Reporting API**, not the Opportunities API, if you're trying to fill subaward visibility gaps. It returns first-tier subcontract records and is the upstream source for USAspending's `/api/v2/subawards/` endpoint.
2. **Get an entity-role account** at sam.gov before pulling anything — the daily quota jumps from 10/day (personal) to 1,000/day (entity-role) or 10,000/day (federal system account).
3. **The `piid` filter is case-sensitive and now wants UPPERCASE no-dash** (`N0002417C2100`) — see the ⚠ box above. (The 2026-05 guide said lowercase; that reversed on 2026-06-21. Dashed PIIDs now 400.) The filter name itself is lowercase `piid`, not `PIID`.
4. **The production endpoint is `https://api.sam.gov/prod/…`.** The docs' example URLs drop `/prod/` and return 404 in production. Keep `/prod/`.
5. **Python on macOS: force IPv4** (`socket.getaddrinfo` monkeypatch) or every request hangs ~225s on IPv6 SYN-retransmit. **This is the single biggest performance gotcha in this guide.** See section below.
6. **SAM.gov subaward data is clean of revision-stacking dedup problems.** Every `subAwardReportId` is unique. Verified on 17,945+ records: zero collisions.
7. **No per-prime record cap** (unlike USAspending's ~2,500-cap). Pulled 5,681 records on a single PIID without truncation.

---

## ⚠ CRITICAL: Force IPv4 in Python on macOS

If your Python script is taking ~225 seconds per page when `curl` returns in 0.3-0.5 seconds, **this is your bug**. Reproducible, deterministic, easy to fix.

### The diagnosis

`api.sam.gov` publishes both `AAAA` (IPv6) and `A` (IPv4) DNS records. Python's `urllib`/`urllib3`/`requests` all use a SEQUENTIAL fallback: try IPv6 first, fall back to IPv4 on failure. On many macOS networks (corporate VPNs, ISPs with broken IPv6, Wi-Fi routers without working v6), the IPv6 connection silently hangs instead of refusing — and the kernel retransmits the SYN three times at ~75-second intervals before giving up.

Result: **~225 seconds per request**, every request. The connection eventually succeeds via IPv4, so the response data is correct — but throughput drops 500×.

`curl` uses RFC 8305 "Happy Eyeballs" (parallel v4/v6 attempts with a short head start for whichever resolves first), so curl is unaffected.

### Verified evidence (2026-05-23, DDG-51 pull)

Same machine, same URL, same SAM key, same time-of-day:

| Method | First call | Second call | Third call |
|---|---:|---:|---:|
| `curl -sS …` | 0.51s | 0.31s | 0.42s |
| Python `urlopen(req)` default | **225.4s** | **225.4s** | **225.3s** |
| Python with `socket.getaddrinfo` AF_INET monkeypatch | **0.43s** | **0.31s** | 0.31s |

### The fix (drop into top of any SAM-calling Python script)

```python
import socket

# Force IPv4 for ALL socket lookups in this process — avoids macOS IPv6 hang.
_orig = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4
```

That's it. Put this BEFORE any `import urllib.request` calls execute, and SAM.gov pages come back in ~0.3-0.5s instead of 225s.

### Alternative: shell out to curl

If you can't or don't want to monkeypatch, shell out to curl via `subprocess.run`. This is what `pull_sam_entity_naics.py` does — entity lookups were the first place we noticed the slowness and the fix predates the broader diagnosis above.

Pattern:

```python
import json, subprocess
from urllib.parse import urlencode
result = subprocess.run(
    ["curl", "-sS", "--max-time", "30", "-A", "myproject/1.0",
     f"https://api.sam.gov/prod/contract/v1/subcontracts/search?{urlencode(params)}"],
    capture_output=True, text=True, timeout=35,
)
body = json.loads(result.stdout) if result.stdout else None
```

The IPv4 monkeypatch is preferred because:
- No subprocess overhead per call
- Standard Python error handling (HTTPError, etc.) keeps working
- Easier retry / backoff / streaming logic

### Why didn't we catch this in the submarine pull?

The submarine pull (2026-05-22) ran on the same machine and timings looked OK at the time. The submarine `pull_sam_entity_naics.py` shelled out to curl specifically because entity-API requests took "1-2 minutes" via urllib — that was a partial workaround for the same root cause but applied at the wrong layer (only entity lookups, not the much larger subaward pulls). When the DDG pull launched the next day on a network where IPv6 was even worse, every subaward request was hitting the full 225s timeout. The diagnosis below should have been applied to all SAM-calling scripts from the start.

**Don't trust "it was fast yesterday."** Add the IPv4 monkeypatch unconditionally; it's a no-op on networks where IPv6 works fine, and it saves ~225s/request when it doesn't.

---

## When to Use SAM.gov vs FPDS vs USAspending

| Source | Auth | Best for | Avoid for |
|---|---|---|---|
| **FPDS Atom Feed** | None (public) | Prime contract data, OT awards, description-level keyword search, authoritative dollar values | Subaward data (none here), forward-looking pipeline |
| **USAspending API** | None (public) | Aggregated views, spending trends, recipient rollups, **subawards on small primes** | Subaward data on large primes (~2,500-record retrieval cap silently truncates the long tail), reliable OT detection |
| **SAM.gov Subaward Reporting** | API key | **Subaward data on any prime, no cap**, parent-UEI normalization, deleted-record audit trail | Aggregated trends (record-level only), forward pipeline |
| **SAM.gov Opportunities** | API key | Solicitations, pre-award notices, award notices (pipeline-side data) | Contract execution data, anything quota-intensive |

**Key insight:** SAM.gov is the **upstream FFATA source** for USAspending's subaward data. Same underlying records, different API behavior. USAspending applies a ~2,500-record pagination cap; SAM.gov does not.

---

## Getting Started — Account Tiers & API Keys

### Account types and daily limits

| Account type | Personal API key | System Account key |
|---|---:|---:|
| Non-federal, **no entity role** | 10/day | n/a |
| Non-federal, **with entity role** | **1,000/day** | 1,000/day |
| Federal user | 1,000/day | **10,000/day** |

"Entity role" = your SAM.gov account is linked to a registered SAM.gov entity (e.g., your employer's CAGE-coded entity registration) and you have a role on that entity. **Get this set up before you start pulling**; the personal-tier 10/day is brutally tight and a single diagnostic mistake burns 10-30% of your budget.

### Getting your key

1. Register / log in at sam.gov
2. Account Details → "Public API Key" → request
3. Keys are prefixed `SAM-` followed by a UUID, e.g. `SAM-e57b65ab-7471-4f6b-8d9b-9adf288254db`
4. The key is sent as a `?api_key=...` query parameter on every request (NOT a header)
5. Store in a `.env` at your project root and load via your script — never commit it

### Watching your quota

There is no documented quota-check endpoint. The 429 response tells you when you've exceeded:

```json
{
  "code": "900804",
  "message": "Message throttled out",
  "description": "You have exceeded your quota. You can access API after [date] 00:00:00+0000 UTC",
  "nextAccessTime": "[date] 00:00:00+0000 UTC"
}
```

Quota resets at midnight UTC daily. **Always trap HTTP 429 and halt cleanly** — don't keep hammering after exhaustion.

---

## The SAM.gov API Family

From the GSA API directory, the SAM.gov-namespaced APIs are:

| API | Purpose | Notes |
|---|---|---|
| **Acquisition Subaward Reporting** | First-tier contract subaward data (FFATA) | ⭐ The big one. See deep dive below. |
| Assistance Subaward Reporting | First-tier subaward data for grants/cooperative agreements (FAIN-based) | Skip if you're tracking contracts |
| **Contract Awards** | Prime-contract award notices | Use FPDS instead unless you specifically need SAM's award-notice view |
| **Get Opportunities** | Solicitations, pre-solicitations, award notices | Pipeline-side. Notorious quirks — see Opportunities section below |
| Opportunity Management | Submit/manage opportunities (authoring) | Only for federal users posting opportunities |
| **Entity Management** | Vendor / entity registration details (including NAICS) | Useful for resolving UEI → company info |
| Exclusions | Debarment / exclusion records | Niche use |
| Entity/Exclusions Extracts Download | Bulk download of entity + exclusion files | For large-scale entity DB construction |
| Federal Hierarchy Public | Federal org structure to office level | Useful for resolving agency codes |
| Federal Hierarchy FOUO | Same, FOUO version | Federal users only |
| Subaward Reporting Bulk Upload | Submit subaward reports (publishing) | For primes filing reports, not consumers |
| Product Service Codes (PSC) | PSC catalog lookup | Annual snapshot also distributed as xlsx |
| Public Location Services | Location lookup for opportunities | Internal-use helper |
| Assistance Listings Public | CFDA-style assistance program catalog | Grants-side |

Most of these are niche. The three with broad analytical value are **Acquisition Subaward Reporting**, **Entity Management** (for NAICS lookup by UEI), and **Get Opportunities**.

---

## Acquisition Subaward Reporting API — Deep Dive

This is the one you'll spend the most time with for procurement analytics.

### Endpoint

```
Production:    https://api.sam.gov/prod/contract/v1/subcontracts/search
Alpha/staging: https://api-alpha.sam.gov/prodlike/contract/v1/subcontracts/search
```

**⚠ Watch the `/prod/` segment.** The docs page's example URLs drop it (`https://api.sam.gov/contract/v1/…`) — that returns **HTTP 404**. Production *requires* `/prod/`. The OpenAPI YAML only documents the alpha URL, which has its own path prefix (`/prodlike/`).

### Authentication

API key as `?api_key=SAM-...` on the query string. No Authorization header, no OAuth, no signed requests.

### Query Parameters — THE SOURCE OF TRUTH IS THE OPENAPI SPEC

The human-readable docs page at `open.gsa.gov/api/acquisition-subaward-reporting-api/` has a parameter table that is **partially wrong**. The OpenAPI YAML at `v1/subawardreportingpublicapi.yaml` is correct.

**Authoritative param list (per OpenAPI spec):**

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `api_key` | string | yes | Your SAM key |
| `pageNumber` | string | no | Default '0'. **Zero-indexed.** |
| `pageSize` | string | no | Default '100', max **1,000** |
| `status` | string | no | `Published` (default) or `Deleted`. Query each separately for full audit trail. |
| `uniqueAwardKey` | string | no | Unique business key per prime contract |
| **`piid`** | string | no | **UPPERCASE, no dashes** as of 2026-06-21 (`N0002417C2100`) — case-SENSITIVE; lowercase silently returns 0, dashed returns HTTP 400. (The filter *name* is lowercase `piid`; its *value* must be uppercase. This reversed from the 2026-05 lowercase rule — see the ⚠ box at top.) |
| `agencyId` | string | no | Awarding agency code (numeric string like "1700" for DON, "9700" for DoD) |
| `referencedIDVPIID` | string | no | Parent IDV PIID (note: docs table inconsistently shows "referencedIdvPIID" mixed-case; actual example URL uses all-caps "IDV") |
| `referencedIDVAgencyId` | string | no | Parent IDV agency code |
| `primeAwardType` | string | no | Award type code |
| `fain` | string | no | Federal Award Identification Number (assistance variant; ignore for contracts) |
| `agencyCode` | string | no | Alternative agency code parameter |
| `fromDate` | string | no | `yyyy-MM-dd` |
| `toDate` | string | no | `yyyy-MM-dd`, must not exceed current date |

**Filter behavior**: AND-only. Multiple filters combine restrictively. No OR logic available.

**Restricted characters in values**: cannot contain `&`, `|`, `{`, `}`, `^`, `\`.

### How to tell if your filter was actually applied

This is the single most important debugging trick:

**Inspect `nextPageLink` in the response body.** It echoes the parameters the API recognized as filters. If you sent `piid=N0002417C2117` and the `nextPageLink` doesn't contain `piid=`, then your filter was silently dropped and you're paginating the entire 2.7M-record dataset.

Real example:

```json
// We sent: ?api_key=...&PIID=N0002417C2117&pageSize=1000&status=Published
// Response:
{
  "totalRecords": 2706620,
  "nextPageLink": "https://api.sam.gov/prod/contract/v1/subcontracts/search?pageNumber=1&pageSize=1000&status=Published"
}
// → PIID is missing from nextPageLink. The filter was ignored.

// After switching to lowercase piid:
// We sent: ?api_key=...&piid=N0002417C2117&pageSize=10&status=Published
// Response:
{
  "totalRecords": 5208,
  "data": [{ "piid": "N0002417C2117", "subEntityLegalBusinessName": "ZAPATA INCORPORATED", ... }]
}
// → 5208 records, first record's PIID matches target. Filter worked.
```

### PIID format

Use the **UPPERCASE no-dash format**: `N0002417C2117`, not `N00024-17-C-2117` and not `n0002417c2117`. SAM.gov stores PIIDs uppercase without dashes, and as of 2026-06-21 matches them **case-sensitively** — lowercase silently returns 0 records, and the dashed form now returns **HTTP 400** (it used to be accepted). See the ⚠ box at the top of this guide.

PIIDs starting with `M67854` are MARCORSYSCOM (Marine Corps Systems Command) — they ARE under DON (1700) for FPDS contracting-agency purposes, but most aren't Navy ships. The vendor-name filter on FPDS will sometimes pull Marine Corps land-vehicle programs (AAV / ACV / JLTV at BAE Land & Armaments) into a "Navy" sweep — confirmed during 2026-05-23 DDG-51 discovery when `M6785416C0006` surfaced with IVECO Defence Vehicles as top sub. Filter by description or PIID prefix downstream.

### Pagination

```
pageNumber=0..N    (zero-indexed)
pageSize=1..1000   (max 1,000 — use it; 1 page of 1000 beats 10 pages of 100)
```

Response includes `totalPages`, `totalRecords`, and `nextPageLink` / `previousPageLink`. **Stop when `nextPageLink` is absent or null** — that's the canonical "no more pages" signal.

**No documented per-PIID record cap.** Pulled 5,681 records on a single prime PIID (`N0002417C2100`) without truncation. This is the biggest reason to use SAM.gov over USAspending's `/api/v2/subawards/` for large primes.

### Response Schema

The OpenAPI spec doesn't fully define the response body, but actual records contain these fields (selected high-value subset):

```json
{
  "primeContractKey": "CONT_AWD_N0002417C2117_9700_-NONE-_-NONE-",
  "piid": "N0002417C2117",
  "agencyId": "9700",
  "referencedIDVPIID": null,
  "referencedIDVAgencyId": null,

  "subAwardReportId": "20960949",                 // ⭐ Stable integer ID per sub action
  "subAwardReportNumber": "a7fedca6-fcba-11ef-...", // UUID for the FFATA report
  "submittedDate": "2019-06-10",                  // When prime filed the report
  "subAwardNumber": "SNF063=025",                 // Prime's own sub PO number
  "subAwardAmount": "328000.0",                   // Dollar value (as STRING — coerce)
  "subAwardDate": "2019-03-29",                   // Action date (use for FY attribution)
  "subawardDescription": "MISSILE TUBE DRAWING REVISIONS",  // Often a placeholder

  "subEntityLegalBusinessName": "ZAPATA INCORPORATED",
  "subEntityUei": "MWJTQK36KMG3",                 // Sub's UEI
  "subEntityDoingBusinessAsName": "...",
  "subParentUei": "NRFJMVNYQ6C3",                 // ⭐ Use for parent-UEI rollup
  "subEntityParentLegalBusinessName": "ZAPATA GROUP, INC.",

  "primeAwardType": "AWARD",
  "totalContractValue": "1.358659769E10",         // Prime contract total (also a string)
  "primeEntityUei": "E7BEKJ4V9528",
  "primeEntityName": "ELECTRIC BOAT CORPORATION",
  "baseAwardDateSigned": "2019-05-31",
  "descriptionOfRequirement": "MISSILE TUBE DRAWING REVISIONS",  // Prime-level description

  "primeNaics": { "code": "541330", "description": "..." },
  "primeOrganizationInfo": {
    "fundingAgency":     { "code": "1700", "name": "DEPT OF THE NAVY" },
    "fundingOffice":     { "code": "N62797", "name": "..." },
    "contractingAgency": { "code": "1700", "name": "..." },
    "contractingOffice": { "code": "N62789", "name": "..." },
    "fundingDepartment": { "code": "9700", "name": "DEPT OF DEFENSE" },
    "contractingDepartment": { "code": "9700", "name": "..." }
  },
  "entityPhysicalAddress": {
    "streetAddress": "...", "city": "...",
    "state": { "code": "CO", "name": "Colorado" },
    "country": { "code": "USA", "name": "..." },
    "zip": "...", "congressionalDistrict": "06"
  },
  "subBusinessType": [
    { "code": "23", "name": "Minority-Owned business" }, ...
  ],
  "subContractorNaics": { ... },                  // Sub's NAICS (sometimes missing)
  "subContractorTopPayEmployee": [                // Top-5 paid employees, when reported
    { "name": "...", "salary": "..." }
  ]
}
```

**Numeric fields are returned as strings.** `subAwardAmount`, `totalContractValue`, `agencyId` all come back as strings. Always wrap in `float()` or `int()` before arithmetic.

### Dedup Behavior — VERIFIED CLEAN

Unlike USAspending's `/api/v2/subawards/`, SAM.gov does **not** exhibit revision-stacking duplication. Verified on the full 17,945-record submarine pull:

- 17,945 records, **17,945 unique `subAwardReportId` values, zero collisions**

This means **the naive sum of `subAwardAmount` equals the deduped sum**. Don't apply USAspending-style v3 dedup logic to SAM.gov data — there's nothing to dedup.

The same `subAwardNumber` (prime's own PO) *does* sometimes appear in multiple records (e.g., 208 repeating pairs in FY24 totaling ~$1.2B), but each has a distinct `subAwardReportId` and represents a separate FFATA-reportable transaction (e.g., multiple delivery orders under one umbrella PO). These are legitimate distinct records, not duplicates.

### Published vs Deleted

```
?status=Published  → live records (default)
?status=Deleted    → records the prime retracted after submission
```

Query both separately for a complete audit trail. In the submarine pull, `status=Deleted` returned essentially nothing (1 record total across 42 PIIDs) — the audit trail is clean. Cost: 1 extra call per PIID.

---

## Entity Management API — NAICS Enrichment

For NAICS-code enrichment of UEIs identified in your subaward pull.

```
GET https://api.sam.gov/entity-information/v3/entities?api_key=<key>&ueiSAM=<UEI>&samRegistered=Yes
```

Response: `body.entityData[0].assertions.goodsAndServices.{primaryNaics, naicsList[]}`.

Gotchas:

- The `samRegistered=No` branch is **dramatically** slower (server appears to do a full-dataset scan when no filter narrows results). Don't fall back to it; just record UEIs that miss `Yes` as `not_found`.
- 1,000/day quota on entity-role keys; tightly scoped pulls (top-150 vendors covers ~90% of dollar volume) fit easily.
- Same IPv4 caveat as the subaward API — force IPv4 in Python or shell out to curl. (The submarine `pull_sam_entity_naics.py` does the latter.)

---

## Opportunities API — Painful Quirks to Know

The Opportunities API (`https://api.sam.gov/opportunities/v2/search`) is forward-pipeline data: solicitations, presolicitations, award notices. It has different behavior from the subaward API and is **much harder to use**.

| Quirk | Impact |
|---|---|
| **~60-second backend latency per call** | Regardless of `limit` or window. A 30-call pull takes ~30 minutes wall clock. |
| **Title-only keyword search** | No `q=` parameter, no description search. `title=<substring>` is the only free-text filter. Generic-titled opportunities are invisible. |
| **Max 1-year date window** | `postedFrom` / `postedTo` cannot span > 1 year. Multi-year pulls must be split. |
| **`postedDate` = last-mod date** | Rolling BAAs that have been live for years only show recent `postedDate` if they have a recent amendment. Dormant BAAs are invisible to recent-window queries. |
| **Description URL, not text** | The `description` field in responses is a URL pointing to the description HTML, not the text itself. Fetching adds 1 call per opportunity. |
| **Personal-tier 10/day quota** | The 10/day ceiling is brutally tight given 60s/call and no description search. Plan obsessively before you call. |

If you're forced to use it, follow these rules:

- Use `title=<specific keyword>` over NAICS pagination — orders of magnitude fewer results per call
- Use `limit=1000` (max) to minimize pagination
- Pre-design your full query plan; never run "diagnostic" queries on a fresh key
- Treat every call like gold; cache aggressively; never re-fetch

---

## Cross-API Patterns Worth Knowing

### Vendor-name normalization via parent UEI

The same firm appears in subaward data under multiple legal-entity names (e.g., "CURTISS-WRIGHT ELECTRO-MECHANICAL CORPORATION" vs "CURTISS-WRIGHT ELECTRO-MECHANICAL CORP" vs "CURTISS-WRIGHT FLOW CONTROL CORPORATION"). For rollups, use `subParentUei` as the canonical key:

```python
def recipient_key(rec):
    if rec.get("subParentUei"):
        return f"UEI:{rec['subParentUei'].strip()}"
    return f"UEI:{rec['subEntityUei'].strip()}"
```

**Caveat — partial fragmentation persists.** Some records have `subParentUei` populated and others don't, even for the same firm. A second pass that builds `{subEntityUei → subParentUei}` from records that DO have both, then back-maps records that lack parent UEI, helps:

```python
def build_sub_to_parent_lookup(all_records):
    lookup = {}
    for rec in all_records:
        sub = rec.get("subEntityUei")
        parent = rec.get("subParentUei")
        if sub and parent:
            lookup.setdefault(sub, parent)
    return lookup
```

Even after this, ~5-10% of large firms still fragment (the same UEI appears as a parent in one record and a sub in another). For deck-quality output, plan on a final name-similarity merge pass.

### Treat `subAwardDate` as the canonical FY attribution

`subAwardDate` = sub's action date. `submittedDate` = when the prime filed the FFATA report (often 1-6 months later). For fiscal-year buckets, **always use `subAwardDate`**:

```python
def is_in_fy(date_str, fy):
    # DoD FY runs Oct 1 of prior year through Sep 30 of FY year
    return f"{fy-1}-10-01" <= date_str[:10] <= f"{fy}-09-30"
```

### Expect FY reporting lag

Subaward filings lag prime contract activity by 6-18 months. The most recent FY in any pull will be **substantially incomplete**. Example from submarine pull on 2026-05-22:

| FY | Records | Total $M | Lag status |
|---|---:|---:|---|
| FY22 | 1,465 | 544 | Stable |
| FY23 | 2,153 | 3,630 | Stable |
| FY24 | 1,836 | 3,960 | ~Stable, may still rise modestly |
| FY25 | 927 | 758 | **Heavily lag-depressed** |
| FY26 | 1 | 0.3 | Essentially empty |

Don't read short-term trends off the most-recent FY data — it will mostly fill in over the following 12-18 months.

---

## Comparison to USAspending Subawards (Same Data, Different API)

For the same submarine pull scope, compared head-to-head:

| Metric | USAspending `/api/v2/subawards/` | SAM.gov `/contract/v1/subcontracts/search` |
|---|---|---|
| Auth | None | API key |
| Max page size | 100 | **1,000** (10× better) |
| Per-prime record cap | **~2,500 records** (silent truncation) | None observed |
| Dedup needed | Yes (v3 logic for revision-stacking) | **No** — `subAwardReportId` is unique |
| Parent UEI field | Limited / inconsistent | `subParentUei` available |
| NAICS sub-side | Often missing | `subContractorNaics` available |
| Top-5 employee data | No | Yes when reported |
| Deleted-record audit | No | Yes via `status=Deleted` |
| Response latency (curl) | ~1-2s/page | ~0.1-0.5s/page (much faster — **IF IPv4 enforced in Python**) |
| Quota | None documented | 10/day personal, 1,000/day entity, 10,000/day federal |

**Practical recommendation:** Use SAM.gov as the primary subaward source for any prime where USAspending might be capped (> 2,500 records). Use USAspending for quick aggregation queries where the cap won't bite.

In the submarine pull, the cap difference was material: USAspending returned ~2,500 records each on the two big GDEB masters (capped). SAM.gov returned 5,681 on N0002417C2100 and 5,208 on N0002417C2117 — recovering **~5,800 records of long tail** USAspending was hiding.

---

## Practical Workflow

### Recommended pull sequence for a subaward analysis

1. **Discover relevant PIIDs from FPDS first.** SAM.gov can't filter by description; you need PIIDs going in. FPDS Atom Feed handles this well.
2. **Confirm entity-role on your SAM key.** 10/day vs 1,000/day is the difference between possible and impossible.
3. **Smoke-test with a single PIID** at `pageSize=10` to validate filter behavior. Inspect `nextPageLink` to confirm the filter was honored. This costs 1 call.
4. **Sanity-check Python speed with a `curl` baseline.** If curl returns in <1s but your Python script takes ~225s per page, you have the macOS IPv6 bug — add the IPv4 monkeypatch.
5. **Full pull with `pageSize=1000`**, paginate until `nextPageLink` is null. Pull `status=Published` and `status=Deleted` separately.
6. **Save raw responses to disk** before any processing. Cache aggressively. Never re-fetch.
7. **Roll up by `subParentUei`** with the two-pass back-map for vendor normalization.
8. **Attribute to FY using `subAwardDate`**, not `submittedDate`.
9. **Don't dedup `subAwardReportId`** — already unique. Don't apply USAspending-style v3 dedup.

### Polite use

- 0.3-0.5s delay between page calls is plenty (the API is fast; rate limiting is per-day, not per-second)
- Set a `User-Agent` header identifying your client
- Trap HTTP 429 explicitly; halt cleanly on quota exhaustion
- Implement exponential-backoff retry on 5xx errors (2s, 4s, 8s)

---

## Code Pattern (Python, stdlib-only, IPv4-safe)

```python
import json, os, socket, time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError

# ⚠ MUST come before any network calls — see "Critical: Force IPv4" section above
_orig_getaddrinfo = socket.getaddrinfo
def _force_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _force_ipv4

BASE = "https://api.sam.gov/prod/contract/v1/subcontracts/search"
HDRS = {"User-Agent": "myproject/1.0", "Accept": "application/json"}

def load_api_key(env_path=".env"):
    for line in Path(env_path).read_text().splitlines():
        if line.startswith("SAM_API_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit("SAM_API_KEY not in .env")

def call(api_key, piid, page=0, page_size=1000, status="Published"):
    params = {
        "api_key": api_key,
        "piid": piid.upper(),   # NB: UPPERCASE no-dash as of 2026-06-21 (was lowercase pre-2026-06; see ⚠ box at top)
        "pageNumber": page,
        "pageSize": page_size,
        "status": status,
    }
    url = f"{BASE}?{urlencode(params)}"
    req = Request(url, headers=HDRS, method="GET")
    try:
        with urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except HTTPError as e:
        if e.code == 429:
            raise SystemExit("Quota exhausted; resume after midnight UTC")
        raise

def fetch_all(api_key, piid, status="Published"):
    records = []
    page = 0
    while True:
        body = call(api_key, piid, page=page, status=status)
        data = body.get("data") or []
        records.extend(data)
        if not body.get("nextPageLink"):
            break
        # Confirm the filter was honored
        if "piid=" not in (body.get("nextPageLink") or ""):
            raise RuntimeError("PIID filter was silently dropped — check casing")
        page += 1
        time.sleep(0.3)
    return records

if __name__ == "__main__":
    api_key = load_api_key()
    for piid in ("N0002417C2117", "N0002417C2100"):
        pub = fetch_all(api_key, piid, status="Published")
        det = fetch_all(api_key, piid, status="Deleted")
        out = {"piid": piid, "published": pub, "deleted": det}
        Path(f"sam_subawards/{piid}_subawards.json").write_text(
            json.dumps(out, indent=2, default=str)
        )
        print(f"{piid}: {len(pub)} published, {len(det)} deleted")
```

With the IPv4 monkeypatch in place, expect ~0.3-0.5s/page. Without it, expect ~225s/page. There is no middle ground.

---

## Troubleshooting

### Every Python request takes ~225 seconds, but curl is fast

**This is the macOS IPv6 / urllib trap.** Add the IPv4 monkeypatch at the top of your script. See the "Critical: Force IPv4 in Python on macOS" section above. The 225s number is a tell — it's `3 × ~75s` TCP SYN retransmits.

Quick repro to confirm before applying the fix:

```bash
# curl: should be <1s
time curl -sS "https://api.sam.gov/prod/contract/v1/subcontracts/search?api_key=$KEY&piid=N0002417C2117&pageSize=10" > /dev/null

# Python without fix: should hang for ~225s
time python3 -c "
from urllib.request import Request, urlopen
from urllib.parse import urlencode
url = 'https://api.sam.gov/prod/contract/v1/subcontracts/search?' + urlencode({'api_key':'$KEY','piid':'N0002417C2117','pageSize':10})
with urlopen(Request(url, headers={'User-Agent':'test'})) as r: r.read()
"
```

If curl is fast and Python is slow, apply the monkeypatch and re-run; should drop to <1s.

### "totalRecords is impossibly large (millions)" or "first record's PIID doesn't match my filter"

Your filter was silently dropped. **Check case-sensitivity** — most common cause is `PIID` (uppercase) instead of `piid` (lowercase). Confirm by inspecting `nextPageLink` in the response body; it echoes only the filters the API recognized.

### HTTP 404 "Page Not Found"

You're hitting the wrong endpoint path. Production must include `/prod/`:
- ✅ `https://api.sam.gov/prod/contract/v1/subcontracts/search`
- ❌ `https://api.sam.gov/contract/v1/subcontracts/search` (this is what the docs examples show)

### HTTP 429 with code "900804"

Quota exhausted. The response includes `nextAccessTime` (typically midnight UTC). Halt cleanly. If you're hitting this on personal-tier 10/day, set up entity-role to get 1,000/day.

### `subAwardAmount` arithmetic returning weird results

Numeric fields are returned as **strings** (e.g., `"328000.0"`, `"1.358659769E10"`). Always coerce with `float()` before arithmetic.

### Vendor counts don't match between two pulls of the same data

`subParentUei` is sometimes populated and sometimes blank for the same firm — depends on what the prime entered in their FFATA filing. Use the two-pass sub→parent lookup pattern (see "Vendor-name normalization" above) to get consistent rollups.

### Empty result on a PIID you expect to have subs

Two possibilities, both common:
- **Genuine zero**: pre-FY2010 contracts predate FFATA; some primes never file at the prime-master level (Lockheed Martin is a known offender)
- **FY lag**: very recent contracts (last 6-18 months) may not have flowed through to FFATA yet

Cross-check against USAspending to disambiguate. If both return zero, the gap is real, not an API artifact.

### A PIID surfaced that isn't a Navy-ship contract (Marine Corps / NAVAIR)

DON (Department of the Navy, contracting-agency 1700) covers BOTH the Navy AND the Marine Corps. PIIDs prefixed `M67854` are MARCORSYSCOM contracts — still under 1700 but for land vehicles, not ships. Similarly, PIIDs prefixed `N00019` are NAVAIR (aviation) and `N62269/N62793/N00024` are NAVSEA (ships).

When a vendor like "BAE SYSTEMS LAND & ARMAMENTS" or "ROLLS-ROYCE" surfaces in a ship-focused sweep, check the PIID prefix. They likely have land-vehicle (BAE) or aviation (Rolls-Royce) work that matched the agency filter but isn't relevant to ships.

---

## References

- **OpenAPI spec (authoritative):** `https://open.gsa.gov/api/acquisition-subaward-reporting-api/v1/subawardreportingpublicapi.yaml`
- Human-readable docs (treat with caution — some errors): `https://open.gsa.gov/api/acquisition-subaward-reporting-api/`
- Get an API key / register entity: `https://sam.gov` → Account Details
- GSA API directory (full list of federal APIs): `https://open.gsa.gov/api/`
- Companion field guide covering FPDS + USAspending: `reference_prior_analysis/federal_procurement_data_guide.txt`
- FPDS Atom Feed howto (separate doc, if present): `../FPDS_ATOM_FEED_HOWTO.md`
- RFC 8305 "Happy Eyeballs Version 2" (what curl does, what Python doesn't): https://datatracker.ietf.org/doc/html/rfc8305

---

## Document history

- **2026-05-22** — Initial version, based on a working production pull of 17,945 first-tier subaward records across 42 submarine prime PIIDs (Va Block I-VI + Col Build I-II + BPMI reactor + Va GFE primes). Corrected the OPS quota figures and parameter casing claims in the older `federal_procurement_data_guide.txt`.
- **2026-05-23** — Added the **macOS IPv6 / Python urllib slow-page diagnosis** (225s per page → 0.3-0.5s with `socket.getaddrinfo` AF_INET monkeypatch). Diagnosed during the DDG-51 outsourced-work pull when the same urllib code that ran "OK" in the submarine pull began consistently timing out. The fix is now the recommended default; the curl-subprocess workaround used in `pull_sam_entity_naics.py` is documented as an alternative. Added MARCORSYSCOM / NAVAIR PIID-prefix gotcha after Marine Corps land-vehicle contracts surfaced in a Navy-only sweep.
- **2026-06-21** — **`piid` filter casing REVERSED to UPPERCASE no-dash** (case-sensitive; lowercase silently → 0 records, dashed → HTTP 400). Discovered while completing the Electric Boat submarine-prime denominator: a sweep written to the old lowercase rule returned `totalRecords: 0` for *every* PIID including masters known to have thousands of subs (`N0002417C2100` → 0 lowercase vs **5687** uppercase). Added the ⚠ breaking-change box at top and corrected the TL;DR, parameter table, PIID-format section, and code pattern. Lesson reinforced: **a 0-record response is ambiguous between "no subs" and "mis-cased filter" — always re-test in uppercase before declaring a reporting gap real.**
