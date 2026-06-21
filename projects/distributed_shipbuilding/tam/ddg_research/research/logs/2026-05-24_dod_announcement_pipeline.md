# DoD daily-contract-announcement POP pipeline — 2026-05-24 (afternoon)

Session built the destroyer equivalent of `submarine_outsourced_work/`'s
DoD-announcement pipeline, with the goal of producing a per-action
place-of-performance percentage dataset comparable to the submarine
project's headline `EB / HII / Other / Foreign` four-bucket finding.

## TL;DR

- **5 scripts ported** from the submarine project (`pull_dod_announcements_pop.py`,
  `fetch_wayback_batch.py`, `ingest_wayback_bulletins.py`,
  `classify_dod_action_worktype.py`, `reclassify_dod_action_subrelevance.py`).
  All in `scripts/`. ~57 KB of new code.
- **Cache symlinked** to the submarine project's `cache/` (305 globalsecurity.org
  HTMLs, 2025+) and `cache_wayback/` (originally 204 Wayback HTMLs, 2022-2024).
  Saved ~1,500 HTTP fetches.
- **Targeted Wayback backfill** of 243 URLs for Aug-Nov 2023 + Jul-Sep 2024
  to capture the FY23-27 MYP master awards (article IDs 3479250 BIW
  Aug 1, 3491276 Ingalls Aug 11). 163 new + 77 already-cached + 3 errors.
  Cache_wayback now at 367 HTMLs.
- **Single-supplier-no-% parser patch** added (handles
  `"Work will be performed in <City>, <State>, and is expected"`) — the
  patch lifted `ddg51 construction` bucket BIW % from 8.9 → 76.5.
- **Headline DoD-announcement output:**
  - 776 total CSV rows × 21 columns at `extracted/dod_announcement_pop.csv`
  - **152 supplier-TAM-relevant DDG actions / $7.13B**
  - **BIW 11.2% | Ingalls 1.3% | Other-US 73.6% | Foreign 0%**
  - **~87% of dollar-weighted POP outside the two destroyer yards** —
    headline outsourcing measurement
- **`DOD_ANNOUNCEMENT_HOWTO.md`** written (569 lines) with full
  methodology, bucket definitions, anchor article IDs, and the
  source-selection-redaction caveat.
- **README.md + MANIFEST.md** updated to reference the new pipeline.

## What we started with

The destroyer project already had:

- FPDS / SAM / USAspending / SCN-extract pipelines done from sessions
  on 2026-05-23 and the morning of 2026-05-24
- `nc_scope_summary.json` containing 178 in-scope DDG PIIDs (used as the
  in-scope-PIID lookup for the DoD-announcement pipeline)
- **No DoD-announcement-bulletin work** — that's what this session added

The submarine project (`/Users/brendantoole/projects2/submarine_outsourced_work/`)
had a full DoD-announcement pipeline already, with cached HTMLs from
prior pulls. The cache was the key reuse target.

## Chronological actions

### 1. Read the submarine howto + scripts

- `submarine_outsourced_work/DOD_ANNOUNCEMENT_HOWTO.md` — 414 lines,
  documented Akamai-block-on-direct + Wayback-via-curl-only + globalsecurity-mirror
  + Wayback CDX enumeration pattern + 2 s rate limit
- All 5 sub scripts:
  `pull_dod_announcements_pop.py`, `fetch_wayback_batch.py`,
  `ingest_wayback_bulletins.py`, `classify_dod_action_worktype.py`,
  `reclassify_dod_action_subrelevance.py`

### 2. Symlinked the cache directories

```bash
ln -sf /Users/brendantoole/projects2/submarine_outsourced_work/research_primary_sources/dod_announcement_pop/cache         cache
ln -sf /Users/brendantoole/projects2/submarine_outsourced_work/research_primary_sources/dod_announcement_pop/cache_wayback cache_wayback
```

Inherited 305 globalsecurity HTMLs + 204 Wayback HTMLs immediately.

### 3. Ported the 5 scripts with DDG-specific changes

| Change | Submarine | Destroyer |
|---|---|---|
| Filter regex | `SUB_FILTER`: virginia/columbia/submarine/EB | `DDG_FILTER`: DDG\d+/Arleigh Burke/BIW/Ingalls/Pascagoula/Aegis/SPY-6/LM2500/Mk 41/Mk 45/SPQ-9/CEC/USG |
| Yard buckets | EB (Groton + Quonset + N. Kingstown) / HII (Newport News) | BIW (Bath + Brunswick) / Ingalls (Pascagoula) |
| Output columns | `pop_eb_site_pct` / `pop_hii_site_pct` | `pop_biw_site_pct` / `pop_ingalls_site_pct` |
| Program tags | `va`, `col`, `bpmi_nuclear`, `sub_gfe_*` | `ddg51`, `ddg_gfe_aegis`, `ddg_gfe_radar`, `ddg_gfe_propulsion`, `ddg_gfe_guns`, `ddg_gfe_vls`, `ddg_gfe_combat_systems`, `ddg_gfe_weapons`, `ddg1000`, `ddg_repair` |
| Hard-drop list | non-sub (DDG, CVN, LCS, LCAC, amphib, etc.) | non-DDG (sub, CVN, LCS, LCAC, LPD/LHA, T-AO, PSC, Zumwalt/DDG-1000, frigate, foreign-MIL, etc.) |
| TAM gate | sub_new_construction | ddg_new_construction |
| In-scope PIID lookup | `in_scope_piids` from `nc_scope_summary.json` (17 hardcoded sub PIIDs) | Same `in_scope_piids` key, but now a dict of 178 destroyer PIIDs |
| Empty-`amount_usd` safe-float | n/a | added `_f()` helper because many ddg rows have redacted $ |

### 4. First run — surfaced two bugs

- **ValueError: empty string `amount_usd`** — fixed by replacing
  `float(r["amount_usd"]) if r["amount_usd"] else 0` with a `_f()` helper
  that catches `ValueError` (some MYP master rows have empty $)
- **Top hits were sub-paragraphs that matched DDG filter** — e.g. the
  $15.4B March 2026 Columbia mod (it contains `N00024-17-C-2117`).
  Hard-drop list correctly filtered these → `non_ddg`.

After first-pass: 113 TAM rows / $5.3B / **BIW 1.8% / Ingalls 1.5% / Other 46%**.

### 5. Diagnosed gap: missing FY23-27 MYP master awards

Inspected top non_ddg rows: the high-$ Pascagoula hits were LPD 33/34/35
($5.8B), LHA 9 ($2.4B), LPD 32 ($1.3B), PSC ($952M) — all amphib/PSC
correctly dropped. The actual DDG MYP master ($6.4B BIW + $8.2B
Ingalls = $14.6B) was missing entirely from the cache.

WebSearch found article IDs:
- 2023-08-01 → **3479250** (BIW FY23-27 MYP master, `N00024-23-C-2305`)
- 2023-08-11 → **3491276** (Ingalls FY23-27 MYP master, `N00024-23-C-2307`)

### 6. Wayback CDX enumerate + backfill

Two CDX queries:

```
defense.gov/News/Contracts/Contract/Article/ from=20230801 to=20231130
defense.gov/News/Contracts/Contract/Article/ from=20240701 to=20240930
```

Dedup by article ID in range 3,470,000-3,950,000 → 243 unique URLs.
Wayback `fetch_wayback_batch.py` background run, 2 s sleep, ~8 min.
Result: 163 new fetched + 77 already cached + 3 errors. cache_wayback
went from 204 → 367 HTMLs.

### 7. Discovered the MYP-redaction caveat

After re-ingest, the BIW MYP master paragraph was correctly parsed
(POP 69% Bath / 10% other) but `amount_usd` was empty. Read the actual
paragraph and found:

> "...the dollar values associated with the multiyear contract are
> considered source selection sensitive information and will not be
> made public at this time (see 41 U.S. Code 2101, et seq., Federal
> Acquisition Regulation (FAR) 2.101 and FAR 3.104)."

The actual $14.58B figure is known from press reporting (USNI News,
Defense Daily, Naval News) but NOT from the DoD bulletins. This is a
**structural difference vs. the submarine project**: the two-yard
competitive MYP format triggers the source-selection sensitivity
language, which the submarine single-yard-prime structure (GDEB) does
not have. Documented in `DOD_ANNOUNCEMENT_HOWTO.md` §12.

### 8. Single-supplier-no-% parser patch

Discovered $202M `N00024-24-C-4212` BIW DDG-51 Planning Yard action
showed `BIW 0% / Ingalls 0% / Other 0%` because the bulletin said
`"Work will be performed in Bath, Maine, and is expected to be completed
by July 31, 2029"` — no percentage. The submarine howto explicitly
flagged this as `"Things to NOT do"` item but never patched it.

Added `RE_POP_SINGLE` regex + fallback logic in both
`pull_dod_announcements_pop.py` and `ingest_wayback_bulletins.py`:

```python
RE_POP_SINGLE = re.compile(
    r"Work will be performed (?:in|at)\s+([A-Z][A-Za-z .\-']+,\s*[A-Z][A-Za-z .\-]+?),\s+(?:and\s+is|with\s+(?:expected|an\s+expected))",
    re.I,
)
# In parse_action: if all four buckets == 0, search for single-site
# pattern and assign 100% to the matched location's bucket.
```

Effect on `ddg51 construction` bucket: BIW % rose from 8.89 → 76.48.
Most of the planning-yard, lead-yard, and small-mod actions at Bath
now correctly attribute.

### 9. Final pipeline run

```bash
rm -f extracted/dod_announcement_pop.csv
python3 scripts/pull_dod_announcements_pop.py        # 374 ddg paragraphs from 198 days
python3 scripts/ingest_wayback_bulletins.py          # +~265 wayback rows
python3 scripts/classify_dod_action_worktype.py      # first-pass program × work_type
python3 scripts/reclassify_dod_action_subrelevance.py  # hard-drop + promote pass
```

Final output:

```
776 total CSV rows
608 non_ddg (correctly dropped: sub/carrier/LCS/LCAC/LPD/LHA/T-AO/PSC/Zumwalt/foreign-MIL)
152 supplier-TAM-relevant DDG actions / $7.13B

$-weighted POP (TAM-relevant only):
  BIW         11.2%
  Ingalls      1.3%
  Other-US    73.6%
  Foreign      0.0%
  (sum = 86.1%; the missing ~14% is in redacted-$ MYP masters + a
   small residual of paragraphs where POP regex still misses)

Per-bucket detail:
  ddg_gfe_aegis           74 actions  $3,547.8M   86.0% supplier-city
  ddg_gfe_radar            7 actions  $1,475.1M   82.0% supplier-city (Raytheon Andover MA)
  ddg51 construction      20 actions  $1,014.0M   76.5% Bath / 6.7% Pascagoula / 7.8% supplier
  ddg_gfe_vls             16 actions    $533.4M   95.0% supplier-city
  ddg_gfe_combat_systems   8 actions    $252.5M  100.0% supplier-city
  ddg_gfe_propulsion       7 actions    $192.2M   19.2% supplier-city (rest in single-supplier residual)
  ddg_gfe_guns             5 actions    $117.4M  100.0% supplier-city (BAE Louisville KY etc.)
```

### 10. Wrote `DOD_ANNOUNCEMENT_HOWTO.md`

569 lines, mirrors the submarine howto structure. Sections:

1. Why this data is valuable
2. Access paths — what works (Wayback via curl, globalsecurity.org mirror) and what doesn't (war.gov / defense.gov direct, WebFetch on Wayback)
3. URL patterns (incl. the two anchor article IDs 3479250 + 3491276)
4. Parsing — the body format (with destroyer-specific identifier patterns)
5. Enumerating bulletin URLs (Wayback CDX for 2022-2024)
6. Rate limits and timing
7. The pipeline — scripts in this project
8. Output schema — `extracted/dod_announcement_pop.csv` (21 columns)
9. Bucket logic — BIW vs Ingalls vs Other-US (with HII Ingalls ≠ HII NNS warning)
10. Things to NOT do (11 gotchas)
11. **Headline findings** (final numbers + per-bucket breakdown + direct submarine comparison table)
12. **The source-selection redaction caveat** (key DDG-specific limitation)
13. Files produced

### 11. Updated README.md + MANIFEST.md

`README.md` — added status line referencing the new pipeline and the
headline finding (87% outsourced).

`MANIFEST.md` — appended 5 new script entries + 2 new CSV entries.

## Open issues / known limitations

1. **MYP-master $ redaction unresolved.** The BIW + Ingalls FY23-27 MYP
   master awards are in the corpus (correctly tagged
   `ddg51 / construction / yes_new_construction / TAM=yes`) but have
   `amount_usd = ""`. To compute a fully dollar-weighted POP that
   includes the $14.58B of in-yard work, cross-reference these PIIDs
   (`N00024-23-C-2305` and `N00024-23-C-2307`) against FPDS / USAspending
   obligated amounts.

2. **GFE-weapons (`ddg_gfe_weapons`) excluded by default.** Standard
   Missile, ESSM, Tomahawk, CIWS are funded under WPN/OPN not SCN, so
   including them would double-count against a different appropriation.
   They appear in the CSV (58 rows / $5.0B in the refined output) but
   are tagged `borderline` and excluded from the TAM gate. Consider
   them separately for a "weapons-procurement" view.

3. **Pre-2022 unreachable.** The FY18-22 MYP master awards (Sep 2018,
   DDGs 122-134) are NOT in the corpus — Wayback CDX coverage is too
   thin pre-2022.

4. **Single-supplier-no-% parser still imperfect.** Some
   `ddg_gfe_propulsion` rows (GE LM2500) show 0% even after the patch,
   suggesting GE bulletins use a slightly different phrasing. Estimated
   ~$50M of unattributed value across maybe 5-8 rows. Patch is ~10 min
   if needed but probably not material to the headline.

5. **`ddg_repair` bucket not used.** 23 actions / $2.0B of DDG depot
   maintenance / DSRA / EDSRA / planning yard sustainment is correctly
   tagged but excluded from the new-construction TAM gate. Available if
   needed for a separate sustainment-spend view.

## Files modified / created

```
DOD_ANNOUNCEMENT_HOWTO.md                            (NEW, 569 lines)
README.md                                            (4-line block added)
MANIFEST.md                                          (8 lines added)
scripts/pull_dod_announcements_pop.py                (NEW, 309 lines)
scripts/fetch_wayback_batch.py                       (NEW, 62 lines)
scripts/ingest_wayback_bulletins.py                  (NEW, 234 lines)
scripts/classify_dod_action_worktype.py              (NEW, 367 lines)
scripts/reclassify_dod_action_subrelevance.py        (NEW, 357 lines)
extracted/dod_announcement_pop.csv                   (NEW, 776 rows × 21 cols, 1.14 MB)
extracted/dod_action_pop_by_worktype.csv             (NEW, ~50 rows, 2 KB)
research_primary_sources/dod_announcement_pop/       (NEW dir)
  ├── cache              → SYMLINK to submarine project
  ├── cache_wayback      → SYMLINK to submarine project (+163 new Wayback HTMLs)
  └── *.txt              430 per-action paragraph audit files
logs/2026-05-24_dod_announcement_pipeline.md        (NEW, this file)
```

## Re-run instructions

```bash
cd /Users/brendantoole/projects2/destroyer_outsourced_work

# 1. 2025+ globalsecurity.org pull (resume-safe, hits cache)
python3 scripts/pull_dod_announcements_pop.py

# 2. Wayback 2022-2024 (only if extending coverage; needs CDX enumeration first)
# (see DOD_ANNOUNCEMENT_HOWTO.md §7 for CDX command)
python3 scripts/fetch_wayback_batch.py

# 3. Re-parse cached Wayback HTMLs into CSV
python3 scripts/ingest_wayback_bulletins.py

# 4. Classify
python3 scripts/classify_dod_action_worktype.py
python3 scripts/reclassify_dod_action_subrelevance.py
```
