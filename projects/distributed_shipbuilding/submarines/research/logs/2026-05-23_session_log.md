# Session Log — submarine_outsourced_work — 2026-05-23

**Handoff doc for the next AI agent.** This session ran 2026-05-23, picking up from
where the 2026-05-22 session left off. Read both logs in order:
1. `logs/2026-05-22_session_log.md` (prior session — initial workbook build)
2. This file

---

## 1. What this session was about

Two distinct work threads, both extending the prior session's analysis:

**Thread A: Refine the submarine subaward analysis to new-construction scope only**
- User clarified: BlueForge / MIB pass-throughs should NOT count
- User clarified: only new-construction (not overhaul or backfit) should count
- Built a focused workbook (`submarine_new_construction_subawards.xlsx`)

**Thread B: Add HII context for the "true outsourcing" picture**
- The prior session noted HII-NNS team-build (~50% of Virginia work) is invisible to FFATA
- Pulled SEC EDGAR (10-Ks + XBRL) to get HII NNS segment revenue
- Scraped 23 HII earnings call transcripts for CEO/CFO commentary
- Added 4 new sheets to the workbook: Trends, Geographic, HII_NNS_Context, CEO_Commentary

The workbook is now deck-ready (13 sheets total).

---

## 2. Audit of prior session's SAM.gov usage

Before doing new work, audited whether the prior agent was using the SAM.gov API correctly.

**Verdict: Yes.** Empirically confirmed:
- Endpoint `https://api.sam.gov/prod/contract/v1/subcontracts/search` ✓ matches official
- `piid` lowercase is correct (matches OpenAPI/Swagger spec; web docs showing uppercase
  `PIID` are wrong)
- `pageSize=1000` (max) ✓
- `pageNumber` 0-indexed ✓
- Date format `yyyy-MM-dd` ✓
- `subAwardReportId` confirmed unique across all 11,005 records (no dedup needed)
- Per-PIID `totalRecords` is sensible (4,389 for biggest master) — filter was honored

**Discovery: PSC is NOT in the SAM.gov subaward API response.** Verified with a fresh
single-record API call — the response has exactly 28 fields, none PSC-related. No nested
PSC field anywhere. Recursive search for any field with "psc"/"product"/"service"/
"category"/"contractor" returned zero matches.

This is structural — PSC is a federal procurement-action field for the PRIME contract,
not the sub's action. To get work-type signal at the sub level, we used **vendor
primary NAICS via the SAM Entity Management API** (separate endpoint).

---

## 3. Cross-validation against another AI agent's analysis

User shared `/Users/brendantoole/Downloads/20260522_Submarine_Outsourced_Construction_vS.xlsx`
produced by a different AI agent with the same task. Compared two sheets:
- `Subaward_Annual` — uses USAspending data (older)
- `Va_Col_FY_Breakdown` — uses SAM.gov data (matches our methodology)

**Result: Numbers reconcile cleanly.** Differences are scope, not data quality:

| FY | Other agent (narrower scope) | This repo (broader) | Δ explained |
|---|---:|---:|---|
| FY22 | $543.98M | $675M | +$131M = Hartford EOH ($64.5M) + Va Tech Instructions ($66.7M) |
| FY23 | $3,630.25M | $3,727M | minor |
| FY24 | $3,959.70M | $4,013M | minor |
| FY25 | $757.62M | $780M | minor |
| FY26 | $0.30M | $0 | trivial |

Other agent had 3 PIIDs we didn't (`N0002412C2106`, `N0002414C2104`, `N0002415C4300`)
but their total contribution in our window was <$0.5M lifetime — not worth a separate pull.

Spot-check on BlueForge $ matched exactly: FY23 $1,514M; FY24 $2,659M. Both agents
hit the same SAM endpoint with the same approach.

---

## 4. The new-construction workbook

### Scope rules (locked in)

**In-scope: 15 PIIDs (new-construction only)**

| PIID | Prime | Class | Label |
|---|---|---|---|
| N0002417C2100 | GDEB | Virginia | Va Block V/VI master |
| N0002417C2117 | GDEB | Columbia | Col Build I/II master |
| N0002424C2110 | GDEB | Virginia | Va Block VI LLTM |
| N0002412C2115 | GDEB | Virginia | Va Block IV MYP |
| N0002409C2104 | GDEB | Virginia | Va Block II residual |
| N0002413C2128 | GDEB | Columbia | Col Design Drawings |
| N0002411C2109 | GDEB | Columbia | SSBN-R concept |
| N0002416C2111 | GDEB | Virginia | VPM Vent Valve |
| N0002410C2118 | GDEB | Virginia | VPM Tube Fab |
| N0002419C2114 | BPMI | Columbia | Naval Reactor Components |
| N0002419C2115 | BPMI | Columbia | Col Class IBI |
| N0002424C2114 | BPMI | Virginia | S9G reactor |
| N0002410C6266 | LM | Virginia | Va Combat Systems HW/SW |
| N0002421C4106 | BAE | Virginia | SSN 812 Forward Subassembly |
| N0002421C4111 | RR | Virginia | Va Class Rotor |

**Excluded PIIDs (2):**
- `N0002420C4312` Hartford EOH — overhaul, not new construction
- `N0002419C2125` Va Tech Instructions / HPAD backfit — upgrades, not new build

**Excluded MIB / workforce pass-through vendors (by parent UEI):**
- `F8PEZKXES8B1` BlueForge Alliance ($4,173M lifetime)
- `QLJZVM6XKR71` Training Modernization Group ($77M)
- `TCM3R4JPRKY4` Institute for Advanced Learning and Research ($1.5M)

### Workbook sheets (13 total, current state)

| # | Sheet | Contents |
|---|---|---|
| 1 | Cover | Headline numbers + sheet index |
| 2 | Scope_PIIDs | 15 in-scope PIIDs + 2 excluded + 3 MIB exclusions |
| 3 | FY_Headline | Per-FY: visible subs $ vs SCN Basic Construction → ratio |
| 4 | **Trends** (new) | YoY % change, HHI, top-5 share, vendor-base size, NAICS mix |
| 5 | FY_By_NAICS | Work-type breakdown via NAICS 4-digit |
| 6 | FY_By_Vendor | Top 20 vendors per FY |
| 7 | FY_By_PIID | Which prime drives each FY's cash flow |
| 8 | **Geographic** (new) | $ by US state + country, foreign share by FY |
| 9 | Lifetime_Vendors | Top 100 vendors across the window |
| 10 | **HII_NNS_Context** (new) | NNS seg rev + implied sub share + FFATA gap |
| 11 | **CEO_Commentary** (new) | 26 curated quotes from earnings calls |
| 12 | NAICS_Lookup | UEI → primary NAICS audit trail |
| 13 | Caveats | Methodology + known gaps |

---

## 5. Headline findings (refined to new-construction)

### Per-FY visible subs ÷ Basic Construction

| FY | Va BCC $M | Col BCC $M | Total BCC $M | Visible subs $M | % of BCC |
|---|---:|---:|---:|---:|---:|
| 2021 | — | 5,979 | 5,979 | 575 | 9.6% |
| 2022 | 4,758 | — | 4,758 | 534 | 11.2% |
| 2023 | 5,095 | — | 5,095 | 2,048 | 40.2% |
| 2024 | 9,071 | 6,356 | 15,427 | 1,300 | 8.4% |
| 2025 | 5,327 | — | 5,327 | 758 | 14.2% (lag) |
| 2026 | 3,137 | 7,160 | 10,297 | 0.3 | 0.0% (lag) |

**Cumulative FY22-FY24 (stable window): 20.2%** ($3,882M subs / $19,259M BCC)

### Trends (the YoY narrative)

- **Supplier base expansion**: 1 unique parent UEI (FY16) → 371 (FY23) — **370× growth**
- **Concentration falling**: top-5 share 99% (FY16) → 31% (FY22) → climbed back ~50% (FY23-FY25)
- **HHI**: from 6,620 (highly concentrated, 2018) → 322 (competitive, 2022)
- **FY23 inflection**: $2,048M visible subs (+283% YoY) is the MIB-era ramp showing
  up in FFATA *even after stripping BlueForge*

### Top vendors lifetime (in-scope, MIB-stripped)

| Rank | Vendor | $M | NAICS | Industry |
|---:|---|---:|---|---|
| 1 | Northrop Grumman | 1,427 | 336413 | Aircraft Parts (corp-level NAICS) |
| 2 | Leonardo SPA (Italy) | 491 | 336411 | Aircraft Mfg |
| 3 | Curtiss-Wright Electro-Mech | 198 | 333914 | Pumping Equip |
| 4 | Scot Forge Co | 198 | 332111 | Iron/Steel Forging |
| 5 | ESCO Technologies | 189 | (varied) | |
| 6 | DC Fabricators | 163 | 332311 | Fabricated Metal |
| 7 | Rhoads Metal Fabrications | 142 | (332xxx) | |
| 8 | Curtiss-Wright Corp | 111 | 333914 | Pumping Equip |
| 9 | The Graham Corp | 89 | 333411 | Heat Exchangers |
| 10 | Austal USA | 88 | 336611 | Ship Building & Repair |

### Geographic distribution

- 97% US, 3% foreign
- **Top 5 states (60% of US-vendor $):** CA ($1,539M, 26%), PA ($760M, 13%),
  MA ($579M, 10%), WI ($473M, 8%), NJ ($301M, 5%)
- **Foreign breakdown:** UK $161M (BAE / Rosyth / Goodwin Steel), Switzerland $33M
  (likely components), Canada $8M, Denmark $0.5M, Brazil $0.1M, China $0.05M
- **CT only 3%** — because subs flow upstream of GDEB, not in CT itself; GDEB isn't
  a "recipient" in this data

### HII visibility gap (the most important finding)

| FY | HII NNS segment rev $M | Implied sub @ 30% $M | FFATA visible HII-as-sub $M | Gap ratio |
|---|---:|---:|---:|---:|
| 2021 | 5,663 | 1,699 | 15.6 | 109× |
| 2022 | 5,852 | 1,756 | 6.0 | 293× |
| 2023 | 6,133 | 1,840 | 0.19 | 9,810× |
| 2024 | 5,969 | 1,791 | 0.18 | 9,690× |
| 2025 | 6,507 | 1,952 | -0.02 | ∞ |

**Federal first-tier subaward data captures <1% of actual HII-NNS submarine
workshare.** The 20.2% FY22-FY24 ratio is a floor, not a ceiling. Adding HII implied
submarine revenue to the visible subs:
- Real "outsourced from VA prime team" in FY23-FY25 is **~$2.5-4B/yr range**

---

## 6. New scripts written this session

| Script | Purpose | Output |
|---|---|---|
| `scripts/aggregate_new_construction.py` | Filter SAM data to new-construction scope, strip MIB | `extracted/nc_*.csv` (4 files) |
| `scripts/pull_sam_entity_naics.py` | Enrich top-150 vendors with NAICS via SAM Entity Management API | `extracted/entity_naics_lookup.csv` + `sam_entity_lookups/` cache |
| `scripts/build_new_construction_workbook.py` | Assemble 13-sheet Excel workbook | `extracted/submarine_new_construction_subawards.xlsx` |
| `scripts/pull_hii_10k_research.py` | Pull HII 10-K filings (FY21-FY25) via SEC EDGAR | `edgar_research/hii_*.csv` + cached HTML |
| `scripts/scrape_hii_transcripts.py` | Scrape HII earnings call transcripts | `hii_earnings_transcripts/*.txt` + .meta.json |
| `scripts/build_workbook_context_sheets.py` | Build Trends + Geographic + HII context CSVs | `extracted/nc_trends.csv`, `nc_geo_by_*.csv`, `hii_context.csv` |
| `scripts/mine_hii_transcript_quotes.py` | Topic-score + curate quotes from transcripts | `extracted/hii_curated_quotes.csv` |

---

## 7. New data folders

| Folder | Contents |
|---|---|
| `edgar_research/` | HII 10-K data + XBRL company facts + per-FY HTML cache + summary memo |
| `hii_earnings_transcripts/` | 23 scraped transcripts (FY19 Q4 → FY26 Q1) + raw HTML cache + index CSV + README |
| `sam_entity_lookups/` | One JSON per UEI from SAM Entity Management API (150 files) |

---

## 8. Data sources used + their gotchas (incremental to prior session)

### SAM.gov Entity Management API (NEW — different from subaward API)
- Endpoint: `https://api.sam.gov/entity-information/v3/entities`
- Same API key (`.env: SAM_API_KEY`)
- Filter: `ueiSAM=<UEI>&samRegistered=Yes`
- NAICS at: `assertions.goodsAndServices.primaryNaics` + `naicsList[0].naicsDescription`
- **CRITICAL: use curl subprocess, not Python urllib.** urllib has slow IPv6 fallback
  against api.sam.gov — 90s/call vs curl's 0.3s/call. We confirmed this empirically.
- `samRegistered=No` retry is VERY slow (server-side full-table scan). Skip it. Accept
  not-found for inactive entities (30% miss rate in our top-150 — likely deactivated).
- Same 1,000/day quota as the subaward API; 150 calls fits comfortably.

### SEC EDGAR `data.sec.gov` (NEW)
- No auth, no API key required. Just User-Agent header.
- HII CIK = `0001501585`
- **Two formats for segment tables in HII 10-Ks**:
  - FY21/FY22/FY23 books: years-as-columns single table (`Newport News $ 5,852 $ 5,663 $ 5,571`)
  - FY24/FY25 books: segments-as-columns, separate table per year
  - Parser in `pull_hii_10k_research.py` handles both
- **R-file IDs in MetaLinks** are already `R9`/`R15`/`R16` etc — don't prepend another `R`
- `companyfacts` API only returns CONSOLIDATED facts (per the docs:
  "Apply to the entire filing entity") — segment-level XBRL is in the raw filing
  but not surfaced by this endpoint
- Earnings call transcripts are NOT in EDGAR. 8-K earnings releases ARE — they
  have segment financials + qualitative program commentary but no Q&A.

### Public transcript sites
- **Motley Fool** (`fool.com/earnings/call-transcripts/...`): cleanest, free, full Q&A.
  Works with Chrome User-Agent. Best source.
- **Insider Monkey** (`insidermonkey.com/blog/.../earnings-call-transcript-<ID>/`):
  full transcripts, requires Chrome UA, slightly more ad noise.
- **Yahoo Finance** (republishes Insider Monkey but TRUNCATES Q&A — only prepared
  remarks). Use only as last resort.
- **Seeking Alpha**: 403 forbidden to scripts. Requires login.
- **MarketScreener / MarketBeat / mlq.ai / roic.ai**: 403 or paywall. Don't bother.

### RapidAPI earnings-call-transcripts1
- User registered an account, got key `RAPIDAPI_KEY` in `.env`
- The free tier ("BASIC") does NOT include any transcript-fetching endpoints —
  all useful endpoints return "This endpoint is disabled for your subscription" (HTTP 401)
- Upgrade would unlock, but we proceeded with free scraping instead

---

## 9. Bugs encountered + fixed this session

| Bug | Symptom | Fix |
|---|---|---|
| Python 3.9 doesn't support `int \| None` syntax | TypeError on aggregator script | Removed type hints |
| SAM Entity Management API takes 90s/call with urllib | NAICS pull would have taken 4 hours | Switched to curl subprocess (`subprocess.run`) — 0.5s/call |
| MetaLinks R-file IDs already prefixed with `R` | `RR15.htm` 404s | Use rid directly (`R15.htm` not `R{rid}` of `R15`) |
| HII 10-K segment table format changed between FY21/22/23 and FY24/25 | 0 rows parsed from old books | Wrote two regex strategies; detect by which marker pattern appears |
| Transcript "Prepared Remarks" clip caught lowercase body mention | Over-clipped transcripts to ~20KB starting mid-Q&A | Removed start-clip entirely; only end-clip the bottom ads |
| Yahoo Finance / Insider Monkey paywall on Q&A | Q1 2024 + Q4 2022 only had prepared remarks | Documented as `*_yahoo_partial.txt`; flagged in README |
| FY2022 Q1/Q2/Q3 transcripts unavailable for free | Seeking Alpha + mlq.ai 403, MarketBeat paywall | Documented gap in `hii_earnings_transcripts/README.md` |
| Country names had case-variation duplicates ("USA"/"United States" + "USA"/"UNITED STATES") | Geo aggregation had 10 rows when it should be 7 | Added `COUNTRY_CANON` normalization map |

---

## 10. Files written this session

### Workbook output
- `extracted/submarine_new_construction_subawards.xlsx` — the deliverable

### CSVs (new this session)
- `extracted/nc_annual_by_piid.csv` — per FY × PIID
- `extracted/nc_annual_by_vendor.csv` — per FY × vendor
- `extracted/nc_lifetime_vendors.csv` — top vendors lifetime
- `extracted/nc_records_long.csv` — every in-scope record (audit)
- `extracted/nc_scope_summary.json` — scope audit trail
- `extracted/entity_naics_lookup.csv` — top-150 vendors → primary NAICS
- `extracted/nc_trends.csv` — YoY trends, HHI, top-5 share, vendor base size
- `extracted/nc_geo_by_state.csv` — $ by US state
- `extracted/nc_geo_by_country.csv` — $ by country
- `extracted/nc_foreign_share_by_fy.csv` — foreign vendor share per FY
- `extracted/hii_context.csv` — NNS revenue + implied sub share + FFATA gap
- `extracted/hii_curated_quotes.csv` — 26 CEO/CFO quotes by topic
- `extracted/hii_all_quote_candidates.csv` — 324 quote candidates (audit)

### EDGAR research
- `edgar_research/hii_submissions.json` — HII filing history (1008 entries)
- `edgar_research/hii_facts.json` — XBRL company facts (3MB)
- `edgar_research/hii_nns_segment.csv` — raw segment data (15 rows: 5 books × 3 years)
- `edgar_research/hii_nns_segment_reconciled.csv` — most-revised per FY (7 rows)
- `edgar_research/hii_program_narrative.csv` — 111 program-narrative snippets
- `edgar_research/hii_summary_memo.md` — full writeup of EDGAR research
- `edgar_research/hii_10k_files/{2021..2025}/` — cached 10-K HTML per FY

### Earnings call transcripts
- `hii_earnings_transcripts/_index.csv` — master index (23 rows)
- `hii_earnings_transcripts/README.md` — coverage + caveats
- `hii_earnings_transcripts/FY*_Q*_*.txt` — 23 transcript text files
- `hii_earnings_transcripts/*.meta.json` — fetch metadata + keyword counts per transcript
- `hii_earnings_transcripts/_raw_html/*.html` — raw HTML cache

### Entity API cache
- `sam_entity_lookups/{UEI}.json` — 150 SAM Entity Management API responses

---

## 11. Caveats — read before drawing conclusions

(Most of the prior session's caveats still apply. New/refined ones this session:)

1. **HII visibility gap is HUGE.** Federal FFATA captures <1% of true HII-NNS submarine
   workshare. Our "% of BCC" headlines (e.g., 20.2% FY22-FY24) are floors. Adding
   HII implied submarine revenue raises the real "outsourced" figure to ~$2.5-4B/yr
   in FY23-FY25.

2. **NAICS classification is corporate-primary, not work-specific.** Northrop Grumman
   classifies as 336413 "Aircraft Parts" because that's their corporate-level NAICS,
   even though they do submarine sonar/combat systems work. NAICS gives directional
   work-type signal but isn't a precise per-action classifier.

3. **30% of top-150 vendors are "not found" in SAM Entity API.** Likely deactivated /
   expired UEIs. They show as "UNENR" in the NAICS work-type breakdown. The 4-digit
   NAICS coverage is 93.5% of $ but only 70% of vendors.

4. **Geographic data reflects registered-address, not work location.** California's
   26% share is partly Northrop's corporate HQ effect. CT being only 3% reflects that
   GDEB itself is a prime (not a recipient), and sub work upstream of GDEB happens
   elsewhere.

5. **FY2022 Q1/Q2/Q3 earnings call transcripts are unavailable** without paid
   subscriptions. Q4 2022 and Q1 2024 have prepared remarks only (Yahoo truncates
   Q&A behind a click-through to Insider Monkey).

6. **CEO_Commentary quotes are auto-scored, not human-curated.** The selection is
   based on a topic-keyword + dollar-figure + forward-language scoring heuristic.
   Sometimes the highest-scoring quote isn't the most quotable — review before
   citing in a deck.

7. **Trends sheet FY16-FY18 data is sparse and unrepresentative.** Pre-FFATA-maturity
   era; small absolute $; high HHI is mostly an artifact of small N. The substantive
   trend story starts FY19 onward.

---

## 12. Open methodology questions / next steps

These were flagged but NOT done this session:

1. **HII Q&A content for FY22 Q1-Q3 + Q1 2024 + Q4 2022.** Currently we have prepared
   remarks only for two of these. Could be sourced via Seeking Alpha subscription or
   by upgrading the RapidAPI plan to PRO ($5-25/mo typical).

2. **NAICS enrichment for the 45 unenriched vendors.** They didn't show up in
   `samRegistered=Yes`. Could re-run with `samRegistered=No` filter but that endpoint
   is very slow (~30s/call). Or accept the gap.

3. **Per-ship attribution.** Subaward descriptions occasionally name hulls (e.g.,
   "SSN 812 CONSTRUCTION BOAT 2 FY 24"). A regex extractor could map subs to specific
   boats and split per-boat costs. Not done — descriptions are too sparse (~80%
   placeholder text).

4. **Commercial shipbuilding benchmark** for the outsourcing rate. We say ~15-30% is
   "the answer" but lack context for whether that's high/low/normal. Would need
   external research (HMD / SHI / DSME segment data, or US commercial yards like
   Bollinger / Eastern).

5. **HII segment operating margin volatility.** NNS margin fell from 6.2% (FY23) to
   4.1% (FY24). HII attributes this to unfavorable cumulative catch-up adjustments
   on Virginia and aircraft carriers. The CEO_Commentary has quotes about productivity
   being below pre-pandemic. Worth a deeper dive if the analysis pivots to "is the
   industrial base healthy?"

6. **BlueForge downstream tracking.** BlueForge received $4.17B over the window as
   a pass-through. Where does it distribute to? Not in scope for this analysis but
   would close a real visibility loop. Would require pulling BlueForge's own FFATA
   filings (they're a prime in some FPDS records).

7. **Update the `consolidate_v2_basic_construction.py` from prior session** to use
   the new narrower scope (15 PIIDs instead of 17). Currently the FY_Headline sheet
   computes ratios using the in-scope $; the prior script's v2 CSV was based on the
   broader scope. Mild inconsistency.

---

## 13. Hand-off — if next agent wants to extend

**To regenerate the entire workbook from scratch:**

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work

# Step 1: SAM subaward data is already pulled (prior session) — no re-pull needed
# Step 2: Aggregate to new-construction scope
python3 scripts/aggregate_new_construction.py

# Step 3: Enrich top-150 vendors with NAICS (uses curl subprocess for speed)
python3 scripts/pull_sam_entity_naics.py

# Step 4: Pull HII 10-K data from SEC EDGAR
python3 scripts/pull_hii_10k_research.py

# Step 5: Scrape HII earnings call transcripts
python3 scripts/scrape_hii_transcripts.py

# Step 6: Build derived context CSVs
python3 scripts/build_workbook_context_sheets.py

# Step 7: Mine + curate transcript quotes
python3 scripts/mine_hii_transcript_quotes.py

# Step 8: Build the workbook
python3 scripts/build_new_construction_workbook.py
```

**Things to NOT do:**

- Don't use Python `urllib` for SAM Entity Management API — it's 100-300× slower
  than curl. Always use `subprocess.run(['curl', ...])`.
- Don't trust web-docs parameter casing — Swagger/OpenAPI YAML is authoritative.
- Don't re-run `samRegistered=No` on the 45 not-found UEIs without budgeting hours.
- Don't include BlueForge/TMG/IALR in any "construction outsourcing" calculation —
  they're MIB pass-throughs, not construction.
- Don't strip the start of transcript HTML — site headers are small and start-clipping
  risks losing prepared remarks. Only trim the bottom (ads, related articles).
- Don't expect EDGAR XBRL `companyfacts` API to give segment data — it only returns
  consolidated facts. Segment data requires parsing the actual 10-K HTML.

**Memories saved this session that affect future work:**

None (no new long-term memories — all session-specific findings are in this log and
in the codebase).

---

## 14. Final state of task list

| # | Subject | Status |
|---|---|---|
| 1 | Build new-construction aggregator | ✓ completed |
| 2 | Enrich top-100 vendors with primary NAICS via SAM Entity API | ✓ completed |
| 3 | Build the Excel workbook | ✓ completed |
| 4 | Pull 5 years of HII 10-K data + write up findings | ✓ completed |
| 5 | Scrape HII earnings call transcripts | ✓ completed |
| 6 | Build Trends sheet data | ✓ completed |
| 7 | Build Geographic + foreign content data | ✓ completed |
| 8 | Mine + curate CEO transcript quotes | ✓ completed |
| 9 | Add 4 new sheets to workbook | ✓ completed |

---

## 15. Quick orientation for next agent

**If user asks "what's the new-construction outsourcing rate":** Cite **20.2%
cumulative FY22-FY24** (non-MIB visible subs ÷ Basic Construction). See
`extracted/submarine_new_construction_subawards.xlsx` → FY_Headline sheet.

**If user asks "what about HII":** Open the HII_NNS_Context sheet. NNS revenue
~$6B/yr, implied submarine portion ~$1.5-2B/yr at 30% midpoint, FFATA-visible
HII-as-sub is essentially $0 → gap ratio 100-9,800×. The "true outsourced from
VA prime team" figure including HII is $2.5-4B/yr in FY23-FY25.

**If user asks for "the headline table":** `extracted/submarine_new_construction_subawards.xlsx`
sheet "FY_Headline".

**If user asks "what does the CEO say":** Open CEO_Commentary sheet — 26 curated
quotes across 6 topics from earnings calls FY22-FY26.

**If user asks "where does the work go":** Geographic sheet — CA dominates (26%
of US $), top 5 states = 60%, foreign 3%.

**If user asks "is it getting more or less concentrated":** Trends sheet — supplier
base grew 370× (1 → 371 unique parent UEIs); HHI fell from 6,620 → 322; top-5
share fell from 99% → 31%, then climbed back to ~50% in MIB era.

**If user asks "what about Q1 2022 commentary":** Not available — FY22 Q1/Q2/Q3
transcripts are behind paywalls. See `hii_earnings_transcripts/README.md`.

**If user asks "where's the underlying data":** Three places:
- `sam_subawards/` — raw subaward JSONs (prior session)
- `edgar_research/` — HII 10-K data
- `hii_earnings_transcripts/` — 23 scraped earnings calls
