# DoD Daily Contract Announcement — Place-of-Performance Pull

**Created:** 2026-05-24
**Scope:** Place-of-performance percentages for individual submarine new-construction
contract actions, as published in the DoD daily contract bulletins.

This folder consolidates what was reachable from this Claude Code session. The
full pull was scoped but not completed — see "Coverage gap" below.

---

## What's here

| File | Contents |
|---|---|
| `dod_pop_actions.csv` | 3 parsed contract actions with PIID, $, prime, expected completion, and POP split: EB-sites % / HII-sites % / Other-US % / Foreign % |
| `2026-03-18_dod-contracts_4437670.txt` | Raw submarine paragraph(s) — Columbia $15.38B mod |
| `2026-04-23_dod-contracts_4468224.txt` | Raw submarine paragraph(s) — EB FMS $196M |
| `2026-05-11_dod-contracts_4479470.txt` | Raw submarine paragraph(s) — Va Block VI LLTM $2.31B |

## Verified data (the three actions)

| Date | PIID | $ | Label | EB-sites | HII (NN) | Other-US | Foreign | In 17-PIID scope? |
|---|---|---:|---|---:|---:|---:|---:|:--:|
| 2026-03-18 | N00024-17-C-2117 | $15.38B | Columbia design + lead-yard + SIB mod | 25% | 6% | 69% | 0% | yes |
| 2026-04-23 | N00024-26-C-2132 | $196M | EB FMS — Va sustainment design | 77% | 0% | 9% | 13% | no (foreign sales) |
| 2026-05-11 | N00024-24-C-2110 | $2.31B | Va Block VI LLTM & early manufacturing | 0% | 2% | 98% | 0% | yes |

**Interpretation notes:**

- The March 18 Columbia mod includes design, lead-yard support, sustainment, and
  industrial-base supplier-development work. The 69% "other-US" share is heavily
  inflated by SIB / enterprise-plan activity rather than direct hull labor —
  don't read this as "69% of Columbia construction is outsourced." It's
  consistent with the framework's caveat that you must classify work-type
  before applying location splits.
- The May 11 Va Block VI LLTM action is the cleanest "outside-the-yards" signal
  in the set: **0% at Groton/Quonset, 2% at Newport News, 98% across 16 named
  supplier cities** (Sunnyvale, Chesapeake, Minneapolis, York PA, Tucson,
  Spring Grove IL, Jacksonville, Stoughton, Newport News, Warren MA, Windsor
  Locks, South El Monte, Portsmouth NH, Milwaukee, Goose Creek SC, El Cajon,
  plus 35% across all locations under 1%). For Saronic-relevant component-shop
  TAM this is the gold-standard action — the entire LLTM dollar pool goes to
  suppliers, not to the yards.
- The April 23 FMS action is out of scope (foreign military sales for an
  unspecified allied submarine program) but kept for reference because the
  paragraph mentions Virginia-class design.

## Access path

| Source | Result |
|---|---|
| war.gov direct (e.g. `https://www.war.gov/News/Contracts/Contract/Article/4437670/`) | HTTP 403 from this session (WebFetch + curl with browser UA) |
| Wayback Machine | Blocked from this session |
| **globalsecurity.org** (mirror) | **HTTP 200** — works |
| NewsAPI (eventregistry.org) with `sourceUri: "war.gov"` or `"globalsecurity.org"` | Works for 2025-2026 only; no coverage pre-2025 |

**globalsecurity.org URL pattern:**

1. Daily news index: `https://www.globalsecurity.org/military/library/news/YYYY/MM/MM-DD_index.htm`
2. Daily DoD contracts page (if mirrored): `https://www.globalsecurity.org/military/library/news/YYYY/MM/dod-contracts_<war_gov_article_id>.htm`

The contracts-page filename is `dod-contracts_<war.gov ID>.htm`. The
war.gov article ID is a 7-digit sequential number. You can't predict it
without first fetching the daily index and grepping for
`href="dod-contracts_<digits>\.htm"`.

## Coverage gap

This pull is **2025-2026 only**. The pre-2025 historical record is not
reachable from this session:

- `globalsecurity.org` has zero `dod-contracts_*` files in 2022/2023/2024
  month directories — they only began mirroring war.gov daily contract
  pages around 2025 (likely when war.gov launched as the rebranded DoD
  press URL).
- NewsAPI's index of these sources also starts ~2025.
- Wayback Machine + direct war.gov are both blocked from this Claude Code
  session.

If pre-2025 daily contract POP data is required, the options are:
1. Paste the relevant press-release URLs / text in from a non-blocked machine
2. Supply a fresh NewsAPI key with deeper historical coverage
3. Run the puller from a different environment (residential IP) that can
   reach war.gov directly

## How to extend (forward-going)

A complete 2025-2026 pull would crawl `01-01_index.htm` through today's
daily index, extract every `dod-contracts_*` href, fetch each contract page,
and filter for paragraphs matching `(virginia-class|columbia-class|submarine|electric boat)`.
Expected yield: ~30-60 submarine-relevant contract actions, each with
explicit POP %.

Rough sketch:

```python
import re, time, requests
BASE = "https://www.globalsecurity.org/military/library/news"
for d in date_range("2025-01-01", today):
    idx = requests.get(f"{BASE}/{d.year}/{d.month:02d}/{d.month:02d}-{d.day:02d}_index.htm",
                       headers={"User-Agent": "Mozilla/5.0"}).text
    for m in re.finditer(r'href="(dod-contracts_\d+\.htm)"', idx):
        page = requests.get(f"{BASE}/{d.year}/{d.month:02d}/{m.group(1)}", ...).text
        # parse submarine paragraphs as in dod_pop_actions.csv pipeline
    time.sleep(0.5)
```

## Parsing notes

- Each contract paragraph reliably ends with
  "Naval Sea Systems Command, Washington, D.C., is the contracting activity."
  Splitting on this sentinel gives one paragraph per action.
- POP percentages use the format `City, State (NN%);` separated by semicolons,
  with a final `and other locations less than 1% (NN%)` bucket.
- The HII-site set is `{Newport News}`. The EB-site set is
  `{Groton, Quonset Point, North Kingstown}`. Everything else aggregates to
  "Other-US" or "Foreign" (the latter via the `various foreign locations (NN%)` pattern).
- The 17 in-scope new-construction PIIDs from `nc_scope_summary.json` are used
  to flag whether each action is in the deck's analytical scope. New-PIID
  actions (e.g., the April 23 FMS PIID `N00024-26-C-2132`) appear as `no`.

## How this complements the parallel FPDS POP work

The other agent's FPDS extractor patch adds `pop_state_code` etc. at the
**action level** for every FPDS record going back to FY18 — that gives broad
historical depth, one principal POP state per action.

This pull adds **percentage breakdowns** for ~3 (eventually ~30-60) recent
high-value actions. Complementary, not duplicative:
- FPDS POP: depth (every action, no %)
- DoD announcement POP: detail (% split across cities, recent only)
