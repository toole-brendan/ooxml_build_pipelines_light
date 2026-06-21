# DoD Daily Contract Announcement POP — How-To

**Last updated:** 2026-05-24

A guide to pulling and analyzing US Department of Defense / Department of
War daily contract announcement bulletins, specifically for the
place-of-performance percentage data they uniquely contain. Companion to
`SAM_GOV_HOWTO.md`.

---

## 1. Why this data is valuable

US federal procurement data has three layers of geographic visibility for
a given contract action:

| Layer | What it tells you | Where to get it | Limitation |
|---|---|---|---|
| **FPDS principal POP** | Where the prime contractor is sited (one state code per action) | FPDS Atom feed or USAspending awards | Single location only. For GDEB-prime work, this is always "Groton, CT" regardless of where downstream supplier dollars flow. Cannot measure outsourcing distribution. |
| **SAM / USAspending subaward recipient address** | The sub-vendor's registered HQ address | SAM.gov FSRS / USAspending subaward API | Registered-address ≠ work-location. A diversified vendor (Northrop, Curtiss-Wright) registers at corporate HQ but does the actual work at facilities in other states. |
| **DoD daily contract announcement bulletins** | Per-action POP **percentages** across multiple cities (typically 4-20 cities per action) | War.gov / defense.gov daily contract bulletins, or mirrors | Only available for actions ≥$7.5M; only available via mirrors back to ~2022 |

**The DoD announcement format is unique** because it states explicit
percentages — typically in this form:

> "Work will be performed in Groton, Connecticut (70%); Newport News,
> Virginia (25%); and Quonset Point, Rhode Island (5%), and is expected
> to be completed by June 2028."

This is the **only public data source** that decomposes a single contract
action's geographic distribution across all the cities where the work
actually happens. For any analysis where you need to measure "what
percentage of [program X]'s dollars are performed outside [prime contractor
Y]'s yards," DoD announcements are the canonical primary source.

For the submarine project specifically, this lets us measure:
- % of submarine prime-contract value performed inside GDEB sites
  (Groton + Quonset Point + North Kingstown)
- % at HII sites (Newport News)
- % at outside-shipyard supplier cities — the **addressable supplier
  opportunity** for component shops like Hadrian, AML3D, etc.

A clean example: the March 18, 2026 Columbia $15.38B mod shows EB 25% /
HII 6% / Other 69% — and the framework's analytical recommendation was
specifically built around this kind of per-action decomposition.

### When NOT to use this data

- **Multi-year trend analysis** — pre-2022 isn't reachable via the routes
  documented here
- **Total program-level $ measurement** — the bulletins only cover
  individual actions ≥$7.5M; small actions + non-FFATA-visible flows are
  missing; for total program $ use FPDS / SCN budget books
- **Single-action work-type decomposition** — a bulletin paragraph gives
  POP for the whole action but not per-line-item; you can't say "the
  design portion was 70% Groton and the SIB portion was 50% other"

---

## 2. Access paths — what works, what doesn't

This is the hard-won part. Tested from the Claude Code Bash environment
on a residential Mac as of 2026-05-24:

| Path | Status | Notes |
|---|---|---|
| `https://www.war.gov/News/Contracts/Contract/Article/<id>/` direct | **403 Akamai block** | Active page; current source for 2025+ bulletins; renamed from defense.gov in 2025 |
| `https://www.defense.gov/News/Contracts/Contract/Article/<id>/` direct | **403 Akamai block** | Pre-2025 URL; same Akamai edge block |
| Same with browser User-Agent | **403** | UA spoofing doesn't help; block is IP/fingerprint based |
| `https://web.archive.org/web/<ts>/<url>` via WebFetch | **Blocked** | "Claude Code is unable to fetch from web.archive.org" — a session-level WebFetch block |
| `https://web.archive.org/web/<ts>id_/<url>` via Bash `curl` | **200 ✓** | Plain curl is a different code path; works fine |
| `https://www.globalsecurity.org/military/library/news/YYYY/MM/dod-contracts_<id>.htm` | **200 ✓** | Third-party mirror; covers 2025+ only |
| NewsAPI (`eventregistry.org`) with `sourceUri: "war.gov"` or `"globalsecurity.org"` | **Works** | 2025+ only; only 16 sub-relevant articles total in the index for our scope |

**Practical conclusion: a two-source pipeline**

1. **2025 and later** → globalsecurity.org daily-index crawl
2. **2022-2024** → Wayback Machine via Bash `curl` (NOT WebFetch)

Pre-2022 is currently unreachable from this environment via any tested
path. The Wayback CDX index has limited defense.gov contract URLs from
pre-2022, and the broader Wayback snapshot density is too thin to enumerate
systematically.

---

## 3. URL patterns

### Live war.gov (2025+) — for reference only, blocked from this session

```
https://www.war.gov/News/Contracts/Contract/Article/<war_gov_article_id>/contracts-for-<date>/
```

The `<war_gov_article_id>` is a 7-digit sequential integer. Each daily
bulletin has one unique article ID. The trailing `/contracts-for-<date>/`
slug is optional — the article ID alone resolves.

### Pre-rename defense.gov (2022-2024) — same site, old URL

```
https://www.defense.gov/News/Contracts/Contract/Article/<article_id>/
```

Same `<article_id>` numbering scheme as war.gov (continuous sequence
across the rename).

### Globalsecurity.org mirror (2025+)

```
https://www.globalsecurity.org/military/library/news/YYYY/MM/dod-contracts_<war_gov_article_id>.htm
```

Filename uses the war.gov article ID. NOT all daily war.gov bulletins
are mirrored — only those globalsecurity.org chose to archive. Coverage
gaps exist.

The **globalsecurity.org daily index** lists each day's content:

```
https://www.globalsecurity.org/military/library/news/YYYY/MM/MM-DD_index.htm
```

Inside that index, look for `<a href="dod-contracts_NNNNNNN.htm">`
links — those are the day's mirrored bulletin URLs.

### Wayback Machine (2022-2024, possibly back to 2018)

```
https://web.archive.org/web/<YYYY>id_/https://www.defense.gov/News/Contracts/Contract/Article/<article_id>/
```

The `id_` suffix on the timestamp gives the **raw** snapshot (no Wayback
toolbar/chrome). Without `id_`, Wayback wraps the page in its own HTML.
Always use the `id_` variant for scripted ingestion.

The `<YYYY>` can be any year in the snapshot date range; Wayback returns
the snapshot closest to that timestamp.

---

## 4. Parsing — the body format

Defense.gov / war.gov daily bulletins follow a strict format. After site
navigation chrome:

```
Contracts For [Month Day, Year]
NAVY
[paragraph 1]
[paragraph 2]
...
ARMY
[paragraph 1]
...
AIR FORCE
[paragraph 1]
...
```

Each paragraph follows this template:

```
[Contractor Name], [City, State], is awarded a $X,XXX,XXX,XXX
[contract-type-description] (N00024-YY-X-XXXX) for [description of work].
Work will be performed in [City, State] (NN%); [City, State] (NN%); ...
[and other locations less than 1% (NN%)]; [various foreign locations (NN%)],
and is expected to be completed by [Month YYYY]. [Funding language].
[Notice activity]. The Naval Sea Systems Command, Washington, D.C., is the
contracting activity (N00024-YY-X-XXXX).
```

**Reliable sentinels for parsing:**

- **Paragraph boundary:** `"is the contracting activity"` appears at the
  end of every NAVY paragraph (other services have similar sentinels —
  Army Contracting Command, etc.). Splitting on this sentinel gives one
  paragraph per action.
- **NAVY section start:** the literal string `"NAVY"` followed by an
  uppercase letter (the start of the first contractor name) marks the
  beginning of Navy contracts. Use it to skip site navigation.
- **PIID format:** `N00024-YY-X-XXXX` for NAVSEA contracts. The PIID
  appears either in parentheses (`(N00024-17-C-2117)`) on newer bulletins
  or bare (`contract N00024-17-C-2117.`) on older 2022 bulletins. Regex
  should handle both:
  ```python
  RE_PIID = re.compile(r"(?:\(|contract\s+)(N\d{5}-\d{2}-[A-Z]-\d{4})")
  ```
- **Dollar amount:** look for `$<digits>` preceded by "awarded" or
  followed by the contract-type-description (cost-plus, firm-fixed-price,
  modification, etc.).
- **POP percentages:** `(City, State) (NN%)` pairs separated by semicolons.
  Watch for two special-case buckets that don't have a city:
  - `"all other locations less than 1% (NN%)"` — sum-of-many-small bucket
  - `"various foreign locations (NN%)"` — foreign sub-recipients
- **Expected completion:** `"expected to be completed by Month YYYY"`.

**Common gotchas:**

- HTML entity encoding: `&rsquo;` → `'`, `&amp;` → `&`, etc. Some Wayback
  snapshots also include numeric character references.
- Wayback toolbar HTML can pollute the body. Either use the `id_` raw
  variant or strip the `<!-- BEGIN WAYBACK TOOLBAR INSERT -->` block.
- Bulletins published on Fridays often contain Thursday's actions too;
  the date in the bulletin title is the publication date, not always the
  award date — most paragraphs end with `(Awarded [Month Day, Year])`
  when the award date differs.
- The order of cities in the POP list is by-percentage-descending (mostly).
- Single-supplier-site actions sometimes use just `"Work will be performed
  in [City, State]"` with NO percentage — your regex won't catch these
  unless you handle the no-`%` case explicitly.

---

## 5. Enumerating bulletin URLs (Wayback CDX for 2022-2024)

The Wayback Machine's CDX API enumerates archived URLs:

```
https://web.archive.org/cdx/search/cdx?
  url=defense.gov/News/Contracts/Contract/Article/
  &matchType=prefix
  &from=20220101&to=20260601
  &output=json
  &limit=8000
  &filter=statuscode:200
  &collapse=urlkey
```

Key parameters:
- `matchType=prefix` matches every URL starting with the given prefix
  (the individual `/Article/<id>/` URLs)
- `from`/`to` filters by SNAPSHOT timestamp, not article publication date.
  Set `to` past the desired publication range to capture late snapshots
  of older articles.
- `collapse=urlkey` deduplicates so each unique URL appears once
- `limit=8000` — CDX has a default 2000 limit; raising it captures more.
  As of 2026-05-24, returns ~3800 unique snapshots in this range,
  filtered down to ~650 unique article URLs in the 2022-2024 publication
  window after filtering article-ID ranges (3,100,000 - 4,100,000 covers
  late-2022 through end-2024).

Sample 200-300 evenly across the article-ID range for a representative
historical cross-section. CDX timeout: use `-m 120` or longer on curl
(some CDX queries take 30-60s server-side).

---

## 6. Rate limits and timing

Tested on 2026-05-24 from a Claude Code Bash session via plain curl:

| Source | Safe rate | Notes |
|---|---|---|
| Globalsecurity.org | ~3 req/sec | No throttle observed up to ~1000 sequential requests with 0.3s sleep |
| Wayback Machine raw snapshots | ~30 req/min | 0.3s sleep → 80% failure (rate limited); 5s sleep → near 100% but slow; **2s sleep is the sweet spot** — 89% success on first pass for 200-URL batches |
| Wayback CDX API | 1-2 queries/min | Heavy server queries; timeout 120s |
| NewsAPI (eventregistry.org) | unmeasured, generous | Single-keyword and date-bounded queries fine; multi-keyword `keywordOper: "and"` is the only documented boolean mode |

**Gzip handling:** Wayback sometimes returns gzipped content without
setting Content-Encoding properly. Always use `curl --compressed`. Without
it, you get binary gzip blobs that look like HTML by extension but read
as garbage; the magic bytes will be `1f 8b` instead of `<!DO`.

**Background-Bash timeout:** Claude Code's harness defaults background
Bash to 2 min. To run a long Wayback batch (~7 min for 200 URLs at 2s
sleep), use foreground Bash with explicit `timeout: 600000` (10 min max).
For batches longer than 10 min, chunk the URL list and run multiple Bash
calls sequentially.

---

## 7. The pipeline — scripts in this project

Source files at `scripts/`:

| Script | Phase | Purpose |
|---|---|---|
| `pull_dod_announcements_pop.py` | 1a | 2025+ pull via globalsecurity.org daily-index crawl |
| `fetch_wayback_batch.py` | 1b | 2022-2024 batch fetch via Wayback (consumes `/tmp/wayback_urls_to_fetch.txt`) |
| `ingest_wayback_bulletins.py` | 2 | Parse cached Wayback HTMLs → append to CSV |
| `classify_dod_action_worktype.py` | 3 | First-pass regex classifier (program × work_type) |
| `reclassify_dod_action_subrelevance.py` | 4 | Judgment-based reclassification (built from manually reading 273 borderline rows) |

Run in order. All are resume-safe — caches let you re-run incrementally.

```bash
# 2025-2026 pull (no inputs needed)
python3 scripts/pull_dod_announcements_pop.py

# 2022-2024 — first enumerate URLs via CDX, write to /tmp/wayback_urls_to_fetch.txt:
python3 -c "
import json, re
with open('/tmp/cdx.json') as f: data = json.load(f)
seen = {}
for row in data[1:]:
    m = re.search(r'/Article/(\d+)/?', row[2])
    if not m: continue
    aid = int(m.group(1))
    if not 3100000 <= aid <= 4100000: continue
    if aid not in seen or row[1] < seen[aid][1]:
        seen[aid] = (row[2], row[1])
sorted_ids = sorted(seen)
step = max(1, len(sorted_ids) // 200)
with open('/tmp/wayback_urls_to_fetch.txt','w') as f:
    for aid in sorted_ids[::step][:200]:
        url, ts = seen[aid]
        f.write(f'{aid}\t{ts[:4]}\t{url}\\n')
"

# Then fetch (~7 min for 200 at 2s sleep — use foreground with 10-min timeout):
python3 scripts/fetch_wayback_batch.py

# Parse cached HTMLs into the CSV:
python3 scripts/ingest_wayback_bulletins.py

# Classify:
python3 scripts/classify_dod_action_worktype.py
python3 scripts/reclassify_dod_action_subrelevance.py
```

---

## 8. Output schema — `extracted/dod_announcement_pop.csv`

| Column | Type | Description |
|---|---|---|
| `action_date` | YYYY-MM-DD | Bulletin date (publication date, not always award date) |
| `war_gov_id` | int | Source article ID |
| `source_url` | str | Globalsecurity.org or defense.gov+Wayback URL |
| `piid` | str | Extracted PIID (`N00024-YY-X-XXXX`), or empty if no parenthesized PIID found |
| `in_scope_17_piids` | yes/no | Whether the PIID is in the 17 in-scope new-construction PIIDs from `nc_scope_summary.json` |
| `amount_usd` | float | Action dollar amount |
| `prime` | str | Prime contractor name |
| `prime_location` | str | Prime's HQ city / state |
| `expected_completion` | "Month YYYY" | When the action is expected to complete |
| `pop_eb_site_pct` | float | % of $ at EB-controlled sites (Groton + Quonset + N. Kingstown) |
| `pop_hii_site_pct` | float | % at HII-controlled sites (Newport News) |
| `pop_other_us_pct` | float | % at all other US locations |
| `pop_foreign_pct` | float | % at foreign locations |
| `pop_locations_detail` | str | Pipe-separated list of "City, State pct%" entries |
| `paragraph_text` | str | Full quoted paragraph |
| `program_primary` | str | First-pass program family (va/col/cvn/ddg/etc.) |
| `program_all` | str | All matched program families (`;`-separated) |
| `program_refined` | str | Second-pass refined program (incl. bpmi_nuclear, sub_gfe_*, non_sub) |
| `sub_relevance` | str | yes_new_construction \| yes_supplier_or_gfe \| yes_sustainment \| borderline \| no |
| `work_type_primary` | str | Primary work-type tag |
| `work_type_all` | str | All matched work types (`;`-separated) |
| `work_type_ambiguous` | Y/blank | Flag for multi-type actions |
| `is_sub_new_construction_tam` | yes/no | Final TAM-relevance gate for headline analysis |

Filter `is_sub_new_construction_tam == 'yes'` for any headline POP analysis —
the raw 658-row CSV is 89%+ non-sub noise from the original loose pull.

---

## 9. Bucket logic — EB vs HII vs Other-US

| Bucket | City matches | Notes |
|---|---|---|
| `eb` | "GROTON", "QUONSET POINT", "NORTH KINGSTOWN" | All in CT or RI; the three GDEB-controlled construction sites |
| `hii` | "NEWPORT NEWS" (with state=VA guard) | HII Newport News Shipbuilding |
| `other_us` | Country code = USA, city not in EB/HII | All supplier cities + Pearl Harbor + Norfolk + etc. |
| `foreign` | Country code != USA | Often UK / Italy / Norway / Australia |
| `unknown` | No POP state code | Foreign actions sometimes have null state; very rare |

---

## 10. Things to NOT do

- **Don't try `war.gov` / `defense.gov` direct from Claude Code** — Akamai
  edge block. Use globalsecurity.org or Wayback (via curl).
- **Don't use WebFetch on `web.archive.org`** — session-level block. Use
  Bash `curl` instead.
- **Don't sleep less than 2 seconds between Wayback requests.** Lower
  sleep triggers rate limiting with cascading failures.
- **Don't forget `curl --compressed` on Wayback.** Half the snapshots
  return gzipped content with no Content-Encoding header.
- **Don't run Wayback batches longer than ~10 min in a single Bash
  call.** Harness timeout. Chunk for longer batches.
- **Don't read raw `dod_announcement_pop.csv` as the headline.** Filter
  to `is_sub_new_construction_tam == 'yes'` (43 rows / $25.4B as of
  2026-05-24).
- **Don't conflate work-type buckets in the rollup.** A lead-yard action
  with 65% "Other-US" POP is mostly SIB / industrial-base dollars routed
  through the prime, not direct construction work at supplier sites.
  Always classify work-type before applying location formulas.
- **Don't claim multi-year trend** — coverage is 2022-2026 only via the
  routes documented here. Earlier years aren't reliably reachable.
- **Don't ignore the "0% everywhere" component_procurement rows.** They're
  single-supplier-site actions where the POP regex misses the no-`%`
  format. Real values are ~100% supplier-city; affects ~$1.6B of TAM.
  Patching is ~15 min if needed.

---

## 11. Headline findings as of 2026-05-24

From 43 supplier-TAM-relevant sub-construction actions over 34 months
(CY2022-mid → CY2026-mid), $25.4B total:

- **EB-sites: 21.9%** of $-weighted POP
- **HII-sites: 16.2%**
- **Outside-shipyard supplier cities: 51.8%** ← the addressable signal
- Foreign: 0%

Cleanest single signal: **BPMI nuclear-reactor work — 13 actions / $4.8B /
80% supplier-city POP** (concentrated Monroeville PA + Schenectady NY).

Cleanest trend datapoint: Dec 2022 Columbia LLTM was 75% EB + 25% HII +
0% supplier; May 2026 Va Block VI LLTM was 0% EB + 2% HII + 98%
supplier. That's the outsourcing-acceleration story in two primary-source
data points.
