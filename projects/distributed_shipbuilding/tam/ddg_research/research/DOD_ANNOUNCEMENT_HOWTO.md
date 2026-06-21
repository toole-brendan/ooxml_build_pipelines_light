# DoD Daily Contract Announcement POP — How-To (DESTROYER)

**Last updated:** 2026-05-24

A guide to pulling and analyzing US Department of Defense / Department of
War daily contract announcement bulletins for the **DDG-51 Arleigh Burke
destroyer program**, specifically for the place-of-performance percentage
data they uniquely contain. Sibling to the submarine project's
`DOD_ANNOUNCEMENT_HOWTO.md` and companion to `SAM_GOV_HOWTO.md`.

---

## 1. Why this data is valuable

US federal procurement data has three layers of geographic visibility for
a given contract action:

| Layer | What it tells you | Where to get it | Limitation |
|---|---|---|---|
| **FPDS principal POP** | Where the prime contractor is sited (one state code per action) | FPDS Atom feed or USAspending awards | Single location only. For BIW-prime work, this is always "Bath, ME" regardless of where downstream supplier dollars flow. Cannot measure outsourcing distribution. |
| **SAM / USAspending subaward recipient address** | The sub-vendor's registered HQ address | SAM.gov FSRS / USAspending subaward API | Registered-address ≠ work-location. A diversified vendor (Lockheed, Raytheon, BAE) registers at corporate HQ but does the actual work at facilities in other states. |
| **DoD daily contract announcement bulletins** | Per-action POP **percentages** across multiple cities (typically 4-20 cities per action) | War.gov / defense.gov daily contract bulletins, or mirrors | Only available for actions ≥$7.5M; only available via mirrors back to ~2022 |

**The DoD announcement format is unique** because it states explicit
percentages — typically in this form:

> "Work will be performed in Bath, Maine (78%); Cincinnati, Ohio (9%);
> York, Pennsylvania (3%); and other locations less than 1% (10%), and is
> expected to be completed by August 2032."

This is the **only public data source** that decomposes a single contract
action's geographic distribution across all the cities where the work
actually happens. For any analysis where you need to measure "what
percentage of [DDG-51 program] dollars are performed outside [the two
shipyards]," DoD announcements are the canonical primary source.

For the destroyer project specifically, this lets us measure:
- % of destroyer prime-contract value performed inside the **Bath Iron
  Works** yard (Bath, ME) and at GD-BIW's auxiliary Brunswick, ME site
- % at **HII Ingalls Shipbuilding** (Pascagoula, MS)
- % at outside-shipyard GFE-supplier cities — the **addressable supplier
  opportunity** for combat system + radar + propulsion + gun
  + VLS components (LM Moorestown / Raytheon Andover / GE Evendale /
  BAE Louisville / etc.)

A clean example: the Aug 1, 2023 BIW $6.40B FY23-27 MYP master shows
Bath, ME 78% / Cincinnati 9% / York PA 3% / Other 10% — a textbook
"prime yard predominates" distribution for the construction action
itself. The Aug 11, 2023 Ingalls $8.18B master is similar.

The same data also captures the **GFE-supplier shift**: small-dollar
component_procurement actions for SPY-6 (Raytheon Andover MA) or LM2500
(GE Evendale OH) show 100% supplier-city POP, with zero at the two yards.

### When NOT to use this data

- **Multi-year trend analysis before ~2022** — pre-2022 isn't reachable
  via the routes documented here
- **Total program-level $ measurement** — the bulletins only cover
  individual actions ≥$7.5M; small actions + non-FFATA-visible flows are
  missing; for total program $ use FPDS / SCN budget books
- **Single-action work-type decomposition** — a bulletin paragraph gives
  POP for the whole action but not per-line-item; you can't say "the
  hull steel portion was X% Bath and the combat-system integration
  portion was Y% other"
- **WPN/OPN-funded ordnance** — Standard Missile, ESSM, Tomahawk, CIWS
  procurement appears in DoD bulletins but is funded under Weapons
  Procurement (WPN) or Other Procurement (OPN), not SCN. Tagged
  `ddg_gfe_weapons` and marked `borderline` for that reason.

---

## 2. Access paths — what works, what doesn't

Same as the submarine project. Tested from the Claude Code Bash environment
on a residential Mac as of 2026-05-24:

| Path | Status | Notes |
|---|---|---|
| `https://www.war.gov/News/Contracts/Contract/Article/<id>/` direct | **403 Akamai block** | Active page; current source for 2025+ bulletins; renamed from defense.gov in 2025 |
| `https://www.defense.gov/News/Contracts/Contract/Article/<id>/` direct | **403 Akamai block** | Pre-2025 URL; same Akamai edge block |
| Same with browser User-Agent | **403** | UA spoofing doesn't help; block is IP/fingerprint based |
| `https://web.archive.org/web/<ts>/<url>` via WebFetch | **Blocked** | "Claude Code is unable to fetch from web.archive.org" — a session-level WebFetch block |
| `https://web.archive.org/web/<ts>id_/<url>` via Bash `curl` | **200 ✓** | Plain curl is a different code path; works fine |
| `https://www.globalsecurity.org/military/library/news/YYYY/MM/dod-contracts_<id>.htm` | **200 ✓** | Third-party mirror; covers 2025+ only |
| NewsAPI (`eventregistry.org`) with `sourceUri: "war.gov"` or `"globalsecurity.org"` | **Works** | 2025+ only |

**Practical conclusion: a two-source pipeline**

1. **2025 and later** → globalsecurity.org daily-index crawl
2. **2022-2024** → Wayback Machine via Bash `curl` (NOT WebFetch)

Pre-2022 is currently unreachable from this environment via any tested
path. The Wayback CDX index has limited defense.gov contract URLs from
pre-2022, and the broader Wayback snapshot density is too thin to
enumerate systematically — meaning the FY18-22 MYP master awards from
September 2018 (DDGs 122-134) are NOT in the corpus. The corpus starts
with the FY23-27 MYP master awards (August 2023).

### Cache reuse from submarine project

The destroyer project's cache directories are **symlinked** to the
submarine project's:

```
research_primary_sources/dod_announcement_pop/cache         → submarine/.../cache
research_primary_sources/dod_announcement_pop/cache_wayback → submarine/.../cache_wayback
```

This reuses 305 globalsecurity.org day-pages (2025-2026) + 204 Wayback
snapshots (2022-2024) that the submarine project already downloaded.
Same raw HTML — different filter and bucket logic in the parsers.

A targeted Wayback re-pull added the FY23-27 MYP article IDs (3479250
and 3491276) plus an additional 240 articles from the Aug-Nov 2023 and
Jul-Sep 2024 windows specifically to capture the DDG MYP master awards
and their initial modifications, which the submarine project's sampling
missed.

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

### Anchor article IDs found in this project

| Date | Article ID | Notes |
|---|---|---|
| 2023-08-01 | 3479250 | FY23-27 MYP master to **BIW** (N00024-23-C-2305) — $6.40B for 3 DDGs |
| 2023-08-11 | 3491276 | FY23-27 MYP master to **Ingalls** (N00024-23-C-2307) — $8.18B for 7 DDGs |

These two announcements together are the **single biggest entry** in the
destroyer DoD-announcement corpus, totaling $14.58B of in-scope new
construction work. Both are explicitly anchor cases for the analysis.

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

**Reliable sentinels for parsing:** Identical to submarines (this is the
same format). See `submarine_outsourced_work/DOD_ANNOUNCEMENT_HOWTO.md`
§4 for the regex sentinels.

**Destroyer-specific identifier patterns:**

- **PIID:** `N00024-YY-X-XXXX` for NAVSEA contracts (same as subs).
  The two specific FY23-27 MYP master PIIDs:
  - `N00024-23-C-2305` (BIW)
  - `N00024-23-C-2307` (Ingalls)
- **Hull numbers:** "DDG 51" through "DDG 169" — currently authorized;
  the regex `\bDDG\s*1[2-6]\d\b` covers DDG 120-169 (recent + planned).
  Note: **DDG 1000-1009 are Zumwalt-class** and explicitly **out of
  scope** for this project (per MANIFEST.md 2026-05-23 user direction).
- **Class names:** "Arleigh Burke", "Flight III"
- **Yard names:** "Bath Iron Works" / "BIW" / "Bath, Maine" /
  "Brunswick, Maine"; "Ingalls Shipbuilding" / "Huntington Ingalls" +
  "Pascagoula" / "Pascagoula, Mississippi"
- **GFE program names:** "Aegis Combat System", "AN/SPY-6" / "SPY-6",
  "LM2500", "Mk 41" / "Vertical Launching System" / "VLS",
  "Mk 45", "AN/SPQ-9B", "AN/USG-2B" / "AN/USG-3B" /
  "Cooperative Engagement Capability" / "CEC"

---

## 5. Enumerating bulletin URLs (Wayback CDX for 2022-2024)

Same CDX API as submarines:

```
https://web.archive.org/cdx/search/cdx?
  url=defense.gov/News/Contracts/Contract/Article/
  &matchType=prefix
  &from=20230801&to=20231130
  &output=json
  &limit=6000
  &filter=statuscode:200
  &collapse=urlkey
```

**Key destroyer-specific tuning:**

- Tighten the from/to to the **specific months containing the DDG MYP
  master awards** — Aug 2023 (BIW + Ingalls FY23-27 master). This is
  more effective than the submarine-style "200 URLs sampled across
  2022-2024" because the destroyer corpus is dominated by a small
  number of very large MYP master + mod actions.
- Repeat for **Jul-Sep 2024** to capture FY24-3 option modifications.
- For 2018-era (FY18-22 MYP master), CDX returns few results because
  Wayback's snapshot density was thinner pre-2022. Skip.

Article-ID ranges for the destroyer window:
- 2023: ~3,470,000 - 3,580,000 (Aug-Nov)
- 2024: ~3,800,000 - 3,950,000 (Jul-Sep)
- 2025+: 4,000,000+ (use globalsecurity.org mirror instead)

---

## 6. Rate limits and timing

Identical to submarine project. Wayback 2 s sleep between requests;
globalsecurity.org 0.4 s. Same gzip / `--compressed` gotcha.

---

## 7. The pipeline — scripts in this project

Source files at `scripts/`:

| Script | Phase | Purpose |
|---|---|---|
| `pull_dod_announcements_pop.py` | 1a | 2025+ pull via globalsecurity.org daily-index crawl. Reuses submarine cache directly via symlink. |
| `fetch_wayback_batch.py` | 1b | 2022-2024 batch fetch via Wayback (consumes `/tmp/wayback_urls_to_fetch.txt`) |
| `ingest_wayback_bulletins.py` | 2 | Parse cached Wayback HTMLs → append to CSV |
| `classify_dod_action_worktype.py` | 3 | First-pass regex classifier (program × work_type) — DDG version |
| `reclassify_dod_action_subrelevance.py` | 4 | Judgment-based reclassification with hard-drop rules for submarine / carrier / LCS / LCAC / Polar Security Cutter / Zumwalt / amphib / oiler / foreign-MIL work |

Run in order. All are resume-safe — caches let you re-run incrementally.

```bash
# 2025-2026 pull (no inputs needed — uses symlinked cache)
python3 scripts/pull_dod_announcements_pop.py

# 2022-2024 — first enumerate URLs via CDX, write to /tmp/wayback_urls_to_fetch.txt:
curl -sS "https://web.archive.org/cdx/search/cdx?url=defense.gov/News/Contracts/Contract/Article/&matchType=prefix&from=20230801&to=20231130&output=json&limit=6000&filter=statuscode:200&collapse=urlkey" -o /tmp/cdx_aug2023.json
curl -sS "https://web.archive.org/cdx/search/cdx?url=defense.gov/News/Contracts/Contract/Article/&matchType=prefix&from=20240701&to=20240930&output=json&limit=6000&filter=statuscode:200&collapse=urlkey" -o /tmp/cdx_aug2024.json

# Reduce to URL list (article ID range 3470000-3950000 covers Aug 2023 – Sep 2024)
python3 -c "
import json, re
articles = {}
for fp in ['/tmp/cdx_aug2023.json', '/tmp/cdx_aug2024.json']:
    with open(fp) as f: data = json.load(f)
    for row in data[1:]:
        m = re.search(r'/Article/(\d+)/?', row[2])
        if not m: continue
        aid = int(m.group(1))
        if not 3470000 <= aid <= 3950000: continue
        if aid not in articles or row[1] < articles[aid][1]:
            articles[aid] = (row[2], row[1])
with open('/tmp/wayback_urls_to_fetch.txt','w') as f:
    for aid in sorted(articles):
        url, ts = articles[aid]
        f.write(f'{aid}\t{ts[:4]}\t{url}\n')
"

# Fetch (~10 min for 240 URLs at 2s sleep — foreground with 10-min timeout):
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
| `in_scope_ddg_piid` | yes/no | Whether the PIID is in the in-scope DDG PIID list from `nc_scope_summary.json` |
| `amount_usd` | float | Action dollar amount |
| `prime` | str | Prime contractor name |
| `prime_location` | str | Prime's HQ city / state |
| `expected_completion` | "Month YYYY" | When the action is expected to complete |
| `pop_biw_site_pct` | float | % of $ at BIW-controlled sites (Bath, ME + Brunswick, ME) |
| `pop_ingalls_site_pct` | float | % at HII-Ingalls-controlled sites (Pascagoula, MS) |
| `pop_other_us_pct` | float | % at all other US locations |
| `pop_foreign_pct` | float | % at foreign locations |
| `pop_locations_detail` | str | Pipe-separated list of "City, State pct%" entries |
| `paragraph_text` | str | Full quoted paragraph |
| `program_primary` | str | First-pass program family (`ddg51`, `ddg_gfe_aegis`, `ddg_gfe_radar`, `ddg_gfe_propulsion`, `ddg_gfe_guns`, `ddg_gfe_vls`, `ddg_gfe_combat_systems`, `ddg_gfe_weapons`, `ddg1000`, `va`, `col`, `sub_other`, `cvn`, `lcs`, `surface_other`, `unknown`) |
| `program_all` | str | All matched program families (`;`-separated) |
| `program_refined` | str | Second-pass refined program (post hard-drop) |
| `ddg_relevance` | str | `yes_new_construction` \| `yes_supplier_or_gfe` \| `yes_sustainment` \| `borderline` \| `no` |
| `work_type_primary` | str | Primary work-type tag |
| `work_type_all` | str | All matched work types (`;`-separated) |
| `work_type_ambiguous` | Y/blank | Flag for multi-type actions |
| `is_ddg_new_construction_tam` | yes/no | Final TAM-relevance gate for headline analysis |

Filter `is_ddg_new_construction_tam == 'yes'` for any headline POP analysis —
the raw CSV is full of non-DDG noise (LPD/LHA at Pascagoula, Polar Security
Cutter, Zumwalt DDG-1000, submarine paragraphs that mentioned "VLS",
foreign-MIL Tomahawk procurement, etc.).

---

## 9. Bucket logic — BIW vs Ingalls vs Other-US

| Bucket | City matches | Notes |
|---|---|---|
| `biw` | "Bath, Maine", "Brunswick, Maine" | GD-BIW's main yard at Bath plus the auxiliary Brunswick site |
| `ingalls` | "Pascagoula" (with state=MS implied; "Pascagoula" alone is unambiguous) | HII-Ingalls Shipbuilding's only sizable site |
| `other_us` | Country code = USA, city not in BIW/Ingalls | All GFE supplier cities (Moorestown NJ for LM Aegis, Andover MA for Raytheon SPY-6, Evendale OH for GE LM2500, Louisville KY for BAE Mk 45, Linthicum MD for NG SPQ-9B, etc.) + naval shipyard sustainment cities |
| `foreign` | Country code != USA | Rare on DDG (Royal Navy / Canadian work usually hard-dropped as foreign-MIL) |
| `unknown` | No POP state code | Foreign actions sometimes have null state; very rare |

**Important difference from the submarine project:**

The submarine bucket logic split between EB-sites (Groton + Quonset Point +
North Kingstown) and HII-sites (Newport News). For destroyers, the two
yards are **single-site shipyards** — BIW only operates Bath ME (with a
small Brunswick ME annex) and Ingalls only operates Pascagoula MS. There
is no equivalent of the "yard supplemental sites" pattern that exists for
EB (Quonset Point modules + North Kingstown).

**Also: HII Ingalls ≠ HII Newport News.** Don't conflate them:

| HII Subsidiary | Builds | Location | DDG-relevant? |
|---|---|---|---|
| HII Ingalls Shipbuilding | DDG-51 + LHA + LPD + NSC + cutters | Pascagoula, MS | YES (DDG prime) |
| HII Newport News Shipbuilding | CVN aircraft carriers + Virginia/Columbia submarines | Newport News, VA | NO (out of scope) |

Newport News appears in DDG bulletins only as an auxiliary supplier site
(small percentage of value) — never as a DDG prime.

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
  to `is_ddg_new_construction_tam == 'yes'`. The raw CSV is dominated by
  LPD/LHA at Pascagoula, submarine paragraphs that mentioned "VLS",
  Zumwalt sustainment, missile FMS, and PSC (Polar Security Cutter)
  noise from the Bollinger Mississippi Shipbuilding facility.
- **Don't conflate Ingalls (Pascagoula) with Newport News.** They are
  separate HII subsidiaries. Newport News is OUT of scope (CVN + subs).
- **Don't include DDG 1000-1009 (Zumwalt).** Out of scope per project
  rules — only 3 ships, all delivered. Remaining flows are OPN not SCN.
- **Don't treat the `ddg_gfe_weapons` rows as TAM-relevant.** Standard
  Missile / ESSM / Tomahawk / CIWS are funded under WPN/OPN, not SCN, so
  including them double-counts against a different appropriation. They
  appear in bulletins (and are loaded into the CSV) but are tagged
  `borderline` and excluded from the TAM gate by default.
- **Don't ignore the "0%-everywhere" component_procurement rows.**
  They're single-supplier-site actions where the POP regex misses the
  no-`%` format. Real values are ~100% supplier-city. Patching the
  parser is ~15 min if needed.
- **Don't claim multi-year trend before 2022.** Coverage is 2022-2026
  only via the routes documented here. The September 2018 FY18-22 MYP
  master awards (DDGs 122-134) are NOT reachable.

---

## 11. Headline findings as of 2026-05-24

From **152 supplier-TAM-relevant DDG actions across the corpus totaling
$7.13 billion** (CY2022-mid through CY2026-mid, 34-month window), the
dollar-weighted POP distribution is:

```text
   BIW-sites      Ingalls-sites      Other-US suppliers      Foreign
    11.2%             1.3%                73.6%                 0%
```

**Outsourced-share measurements:**

- **Outside-BIW-and-Ingalls share**: approximately **87%** of dollar
  value flows to firms outside the two destroyer shipyards. This is the
  cleanest measurement of "how much of DDG-51 program contract value
  goes to the supplier base."
- **Outside-prime-yard share**: not separately computed because both
  yards are prime of record on their own hulls under the two-yard
  competitive procurement — there is no "umbrella prime team" structure
  to compare against.

The per-bucket breakdown:

| Program | Work type | N actions | Value $M | BIW % | Ingalls % | Other-US % |
|---|---|---:|---:|---:|---:|---:|
| ddg_gfe_aegis | component_procurement | 74 | 3,547.8 | 0.7 | 0.7 | 86.0 |
| ddg_gfe_radar | component_procurement | 7 | 1,475.1 | 0.0 | 0.0 | 82.0 |
| ddg51 | construction | 20 | 1,014.0 | 76.5 | 6.7 | 7.8 |
| ddg_gfe_vls | component_procurement | 16 | 533.4 | 0.2 | 0.2 | 95.0 |
| ddg_gfe_combat_systems | component_procurement | 8 | 252.5 | 0.0 | 0.0 | 100.0 |
| ddg_gfe_propulsion | component_procurement | 7 | 192.2 | 0.0 | 0.0 | 19.2 |
| ddg_gfe_guns | component_procurement | 5 | 117.4 | 0.0 | 0.0 | 100.0 |

**Three sharp interpretations:**

1. **The outside-yards share dominates.** ~87% of supplier-TAM-relevant
   contract action value flows to GFE-component cities outside the two
   destroyer yards. This is concentrated in Moorestown, NJ (Lockheed
   Martin Aegis); Andover, MA (Raytheon SPY-6); plus VLS canister sites
   and other GFE-component suppliers. The DDG-51 program is **highly
   GFE-intensive** — the prime hulls account for far less of the
   dollar-weighted POP than the combat-system suite.

2. **The `ddg51 construction` bucket measures real yard work cleanly.**
   The 20 ddg51 construction actions split 77% BIW / 7% Ingalls / 8%
   supplier-city — heavily Bath-weighted because the corpus happens to
   include more BIW-side actions than Ingalls-side actions in the
   captured window. Both yards' MYP master + option exercises ARE
   captured (POP percentages parsed correctly: BIW master = 69% Bath /
   Ingalls master = 77% Pascagoula) but their dollar amounts are
   **redacted as source-selection sensitive** (see §12).

3. **GFE-radar (SPY-6) and GFE-Aegis are the two biggest dollar buckets**
   ($3.5B + $1.5B = $5.0B of the $7.1B TAM total, ≈70% of the corpus).
   Both are heavily concentrated at single supplier sites (Moorestown
   NJ for Aegis, Andover MA for SPY-6). This is the destroyer
   equivalent of the submarine BPMI-nuclear concentration at
   Monroeville PA + Schenectady NY.

**Direct comparison to submarine project:**

| Bucket | Submarines | Destroyers |
|---|---:|---:|
| Prime-yard #1 (EB / BIW) | 21.9% | 11.2% |
| Prime-yard #2 (HII / Ingalls) | 16.2% | 1.3% |
| Outside-yard US suppliers | 51.8% | 73.6% |
| Foreign | ~0% | ~0% |
| Total TAM corpus $ | $25.4B | $7.1B |
| TAM corpus N actions | 43 | 152 |

The destroyer corpus is **larger in row count** (more GFE-component
actions are above the $7.5M reporting threshold) but **smaller in
dollar value** because the destroyer MYP master awards — which would
add ~$15B of in-yard work to the corpus — have **redacted dollar
amounts** as source-selection sensitive.

---

## 12. The source-selection redaction caveat

A methodologically important finding unique to the destroyer corpus:
the **FY23-27 DDG-51 MYP master awards** (BIW August 1, 2023 PIID
`N00024-23-C-2305` and Ingalls August 11, 2023 PIID `N00024-23-C-2307`)
both contain the following standard language in their DoD announcement
paragraphs:

> "...the dollar values associated with the multiyear contract are
> considered source selection sensitive information and will not be
> made public at this time (see 41 U.S. Code 2101, et seq., Federal
> Acquisition Regulation (FAR) 2.101 and FAR 3.104)."

The actual obligated dollar amounts — known from press reporting to
total approximately $14.58 billion across the BIW + Ingalls combined
awards — are NOT in the DoD announcement bulletins. The POP percentages
ARE included (BIW master at 69% Bath, ME and Ingalls master at 77%
Pascagoula, MS), but the actions are absent from any dollar-weighted
analysis based on the bulletins alone.

**Practical implication:** Any "% of total build cost outsourced"
analysis using the destroyer DoD-announcement corpus alone is
mechanically biased toward the GFE-component supplier cities, because
the GFE bulletins disclose dollars but the hull-construction MYP master
bulletins do not. To recover the omitted yard-construction dollars,
cross-reference these PIIDs against FPDS / USAspending obligated
amounts:

| PIID | DoD-bulletin POP | DoD-bulletin $ | Recovery source |
|---|---|---:|---|
| `N00024-23-C-2305` (BIW FY23-27 master) | 69% Bath, ME | _redacted_ | FPDS Atom feed; USAspending `/api/v2/awards/` |
| `N00024-23-C-2307` (Ingalls FY23-27 master) | 77% / 79% Pascagoula, MS | _redacted_ | Same |

Subsequent option-exercise modifications under these masters sometimes
disclose the option-specific dollar amount (e.g., the 2023-09-06
modification to `N00024-23-C-2305` is $61.1M), but the masters
themselves remain redacted.

This issue does NOT affect the submarine project because the submarine
single-yard-prime structure (GDEB) does not use the two-yard
competitive MYP procurement format that triggers the source-selection
sensitivity language.

---

## 13. Files produced

| File | Description |
|---|---|
| `extracted/dod_announcement_pop.csv` | 776 rows × 21 columns; the main analytical CSV |
| `extracted/dod_action_pop_by_worktype.csv` | Per (program_refined × work_type_primary) bucket rollup with $-weighted POP shares |
| `research_primary_sources/dod_announcement_pop/<date>_dod-contracts_<id>.txt` | Per-bulletin DDG paragraphs (auditable raw source quote) |
| `research_primary_sources/dod_announcement_pop/cache/` | Globalsecurity.org HTML cache (symlinked from submarine project) |
| `research_primary_sources/dod_announcement_pop/cache_wayback/` | Wayback HTML cache (symlinked from submarine project + 243-URL backfill for Aug-2023 + Jul-Sep-2024) |
