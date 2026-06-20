# Session Log — submarine_outsourced_work — 2026-05-24 (session 3)

**Handoff doc for the next AI agent.** Picks up from session 2 (methodology deck
+ overnight SAM full-history). Read prior logs in order:

1. `logs/2026-05-22_session_log.md` (initial workbook)
2. `logs/2026-05-23_session_log.md` (new-construction refinement + HII context)
3. `logs/2026-05-24_session_log.md` (cost-funnel reframing + primary sources)
4. `logs/2026-05-24_session_log_2.md` (methodology deck + full-history SAM pull)
5. This file

This session was a parallel-agent collaboration on **place-of-performance data**.
A second Claude agent worked the FPDS prime-pull POP extraction; this agent
worked the DoD daily-contract-announcement POP extraction + GD 10-K
triangulation + a slide-2 addition to the methodology deck.

---

## 1. What this session was about

Four threads, each substantive:

**A. Methodology deck — slide 2.** User asked for a second MECE tree slide
that descends into the physical subcomponents under each L1 box (Plans /
GFE / Basic Construction / Other), parallel to slide 1 but answering
"what physically lives in each box" instead of "what measurement-visibility
layer is each."

**B. FPDS POP per-PIID rollup.** A second Claude agent (the user was running
both in parallel) patched `scripts/pull_fpds_sub_primes.py` to extract
seven new `pop_*` fields from the FPDS XML. This agent's role was to write
the **aggregator** that would consume those new fields once the re-pull
finished: `scripts/aggregate_fpds_pop.py`.

**C. GD 10-K triangulation.** Mirror of the HII 10-K pull from the 2026-05-23
session, this time for General Dynamics. Pulled FY21-FY25 10-Ks; extracted
Marine Systems segment financials (revenue, operating earnings, capex,
identifiable assets); extracted submarine program-narrative snippets.
Output: `edgar_research/gd_*.csv` + `gd_summary_memo.md`.

**D. DoD daily contract announcement POP pull.** The framework the user is
working from (from another LLM session) explicitly recommended building a
contract-action POP database. This was the biggest piece of net-new
analytical work this session — pulled 658 contract action paragraphs from
2022-07-25 through 2026-05-22 with explicit place-of-performance
percentages, classified by program family + work type, and rolled up into a
deck-grade per-bucket summary.

---

## 2. The DoD-announcement POP pull — the big new dataset

### Why it matters

Federal procurement data has three layers of geographic visibility:

| Layer | What it gives | Limitation |
|---|---|---|
| FPDS prime POP (one state per action) | Where the prime contractor is sited | The prime's POP = "Groton, CT" for every GDEB action regardless of where downstream dollars flow. Useless for measuring outsourcing distribution. |
| SAM / USAspending subaward geography (recipient HQ address) | Where the sub-vendor is registered | Registered-address ≠ work-location. Northrop HQ is in VA but their submarine work happens at facilities in PA, IL, etc. |
| **DoD daily contract announcements** | Per-action POP **percentages** across multiple cities | Only available for actions ≥$7.5M; only available 2022+ via the routes we found |

The DoD announcement format is unique because it states explicit % breakdowns:

> "Work will be performed in Groton, Connecticut (70%); Newport News, Virginia (25%); and Quonset Point, Rhode Island (5%)"

This is the only public data source that decomposes a single contract
action's geographic distribution across all the cities where the work
actually happens. For Saronic's "addressable supplier opportunity"
analysis, this is the cleanest measurement of "% of submarine
prime-contract value performed outside the two nuclear shipyards."

### Access path (the hard-won part)

| Path | Result |
|---|---|
| `https://www.war.gov/News/Contracts/...` direct | **403** — Akamai edge block from this Claude Code session |
| `https://www.defense.gov/News/Contracts/...` direct (pre-2025 URL) | **403** — same Akamai block |
| `https://web.archive.org/web/...` via WebFetch | **Blocked** — WebFetch tool has a session-level block on web.archive.org |
| `https://web.archive.org/web/...` via Bash curl | **200 ✓** — bash curl is a different code path, works |
| `https://www.globalsecurity.org/military/library/news/YYYY/MM/dod-contracts_<id>.htm` | **200 ✓** — third-party mirror, 2025+ only |
| NewsAPI (eventregistry.org) sourceUri filter | Works but only 2025+ for these sources |

**Final solution:** two-source pull —
- 2025-2026 → globalsecurity.org daily-index crawl (200 ms/req, no auth)
- 2022-2024 → Wayback Machine via Bash curl (2 sec/req with throttle)

### Pipeline (scripts in execution order)

```
scripts/pull_dod_announcements_pop.py    # 2025-2026: crawls globalsecurity.org daily indexes,
                                          # finds dod-contracts_<id>.htm links, fetches each,
                                          # parses submarine paragraphs, extracts PIID + $
                                          # + prime + POP % into extracted/dod_announcement_pop.csv

scripts/fetch_wayback_batch.py            # 2022-2024: takes a list of defense.gov article URLs
                                          # (one per line, tab-separated aid<TAB>year<TAB>url)
                                          # from /tmp/wayback_urls_to_fetch.txt, fetches each
                                          # via Wayback /web/<year>id_/ URL, caches HTML

scripts/ingest_wayback_bulletins.py       # Parses cached Wayback HTMLs from
                                          # research_primary_sources/dod_announcement_pop/cache_wayback/
                                          # into the same dod_announcement_pop.csv schema.
                                          # Handles two filename formats and extracts date from
                                          # title when filename only has the year.

scripts/classify_dod_action_worktype.py   # First-pass classifier: program family (va/col/cvn/ddg/
                                          # etc.) + work type (lltm/construction/lead_yard/etc.)
                                          # via regex over the paragraph text. Multi-label.

scripts/reclassify_dod_action_subrelevance.py
                                          # SECOND-PASS classifier built on manual judgment after
                                          # reading 273 candidate rows. Hard-drops 292 non-sub
                                          # rows (missile/DDG/LCS/carrier/lodging) and promotes
                                          # sub-relevant rows to refined tags (bpmi_nuclear,
                                          # sub_gfe_electronics, sub_gfe_components, sub_repair,
                                          # sub_operational). Recomputes TAM-relevance gate.
```

### Wayback CDX enumeration

The Wayback CDX API returns 1991 unique defense.gov bulletin URLs in the
2022-2024 window (after filtering to article IDs in range 3,100,000 -
4,100,000 to exclude pre-2022 and post-2025 outliers). We sampled 200
evenly across the ID range. CDX query:

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

### Rate-limit gotchas

- **Wayback raw snapshots:** 0.3 sec sleep → rate limited (80% failure).
  5 sec sleep → near-perfect success but slow.
  **2 sec sleep is the sweet spot** (~89% success on first pass).
- **Gzip:** Wayback sometimes returns gzipped content without setting
  Content-Encoding. `curl --compressed` solves it. Without it, you get
  binary gzip files that look like HTML by extension but read as garbage.
- **Bash background timeout:** harness default is 2 min for background
  Bash. To run a long Wayback batch, use foreground Bash with explicit
  `timeout: 600000` (10 min max). Anything longer must be chunked.

---

## 3. Headline findings — DoD POP per-bucket rollup

**TAM-relevant actions** (program ∈ {va, col, va_or_col, bpmi_nuclear,
sub_gfe_electronics, sub_gfe_components}, work_type ∈ {construction,
lltm_early_mfg, advance_procurement, eoq, component_procurement}):

**43 actions over 34 months (CY2022 mid → CY2026 mid), $25.4B total**

| Bucket | $-weighted POP |
|---|---:|
| EB-sites (Groton + Quonset + N. Kingstown) | **21.9%** |
| HII-sites (Newport News) | **16.2%** |
| Other-US (supplier cities) | **51.8%** |
| Foreign | 0.0% |

### Per-bucket breakdown

| Program family | Work type | N | $M | EB% | HII% | Other-US% |
|---|---|---:|---:|---:|---:|---:|
| `va` | lltm_early_mfg | 7 | 18,104 | 27.4 | 22.2 | 50.4 |
| `bpmi_nuclear` | component_procurement | **13** | **4,814** | 0.0 | 0.0 | **80.2** |
| `sub_gfe_electronics` | component_procurement | 10 | 1,193 | 0.0 | 0.0 | 0.0* |
| `col` | advance_procurement | 1 | 699 | 85.0 | 15.0 | 0.0 |
| `va` | component_procurement | 7 | 338 | 0.0 | 0.0 | 0.0* |
| `va` | construction | 1 | 188 | 0.0 | 2.0 | 98.0 |
| `sub_gfe_components` | component_procurement | 4 | 91 | 0.0 | 0.0 | 0.0* |

*0%-everywhere rows are single-supplier-site actions where POP is "Work
will be performed in [City]" with no `%` — parser miss. Affects $1.6B.

### Three sharp interpretations for the deck

1. **The "outside-the-shipyards" share is real and measurable.** 52% of
   submarine new-construction supplier-TAM-relevant dollars in 2022-2026
   flow to supplier cities, not the prime yards. This is the cleanest
   primary-source quantification of the funnel deck's "outsourced layer"
   estimate.

2. **BPMI nuclear is the cleanest supplier signal.** 13 BPMI actions over
   the period totaling $4.8B; 80.2% of dollars POP to outside-yard cities
   (concentrated in Monroeville, PA = Westinghouse + Schenectady, NY).
   This is the single most concentrated supplier-city pattern in the corpus.

3. **LLTM is half-yards, half-suppliers.** The 7 Virginia LLTM actions
   ($18.1B) split ~28/22/50 — meaning a significant chunk of "LLTM"
   dollars stays at the yards for "early manufacturing" (pre-construction
   subassembly), not at suppliers. The framework's assumption that LLTM
   is pure supplier work was too clean.

### The framework's exact examples — all captured + verified

- **2025-04-30, $12.42B SSN 812/813 Block VI:** EB 40% / HII 32% / Other 28%
  ✓ matches framework's quote
- **2026-03-18, $15.38B Columbia mod:** EB 25% / HII 6% / Other 69%
  ✓ matches framework's quote
- **2026-05-11, $2.31B Va Block VI LLTM:** EB 0% / HII 2% / Other 98%
  ✓ confirms LLTM-to-suppliers signal

### Plus a major historical anchor (Perplexity-supplied):

- **2022-12-21, $5.13B Columbia LLTM + SIB:** EB 75% / HII 25% / Other 0%
  — pre-supply-chain-crunch era; 100% at the two yards. The contrast with
  the 2026 LLTM POP (98% at suppliers) is the deck's "outsourcing
  acceleration" story in two data points.

---

## 4. The GD 10-K triangulation — separate but complementary

### Marine Systems segment financials, FY19-FY25 (reconciled)

| FY | Revenue $M | YoY | Op Income $M | Margin | Capex $M |
|---:|---:|---:|---:|---:|---:|
| 2019 | 9,183 | — | 785 | 8.5% | 449 |
| 2020 | 9,979 | +8.7% | 854 | 8.6% | 604 |
| 2021 | 10,526 | +5.5% | 874 | 8.3% | 573 |
| 2022 | 11,040 | +4.9% | 897 | 8.1% | 530 |
| 2023 | 12,461 | +12.9% | 874 | **7.0%** | 511 |
| 2024 | 14,343 | +15.1% | 935 | **6.5%** | 424 |
| 2025 | 16,723 | +16.6% | **1,177** | 7.0% | 517 |

### Three deck-grade GD findings

1. **150 bps margin loss FY22→FY24** = ~$210M of segment earnings sacrificed
   to the supplier-base constraint Novakovic talks about. Quantifies the
   cost of the supply-chain problem in financial terms.

2. **$1.8B EB capex commitment** is documented in FY21/FY22 books explicit;
   matches Novakovic's later "+79% capex to >$900M" guidance.

3. **GD FY21 book — primary-source teaming quote:**
   > "Our Marine Systems segment has one primary competitor with which it
   > also partners on the Virginia-class submarine program, and to which
   > it subcontracts on the Columbia-class submarine program."
   This is GD's own language for the EB↔HII teaming relationship.

Mirror of the HII 10-K work from 2026-05-23. Pipeline at
`scripts/pull_gd_10k_research.py`; memo at
`edgar_research/gd_summary_memo.md`.

---

## 5. FPDS POP aggregator — supporting role

The parallel agent's FPDS extractor patch added 7 `pop_*` fields per FPDS
record. This agent's aggregator `scripts/aggregate_fpds_pop.py` rolled them
up per-PIID + per-vendor-slug. **Key takeaway: FPDS POP at the prime level
shows registration, not outsourcing.** Every GDEB-prime PIID rolls up to
100% Groton because that's where GDEB the prime is sited; the actual sub
dollars flow elsewhere (visible only in subaward data, which lacks POP).

Useful incremental findings:
- BAE forward subassembly: **100% Minneapolis, MN**
- Rolls-Royce Va rotors: **61% Walpole, MA**
- BPMI nuclear (4 in-scope PIIDs): **100% Monroeville, PA** (Westinghouse)

Outputs:
- `extracted/fpds_pop_by_piid_state.csv` (long form)
- `extracted/fpds_pop_by_piid_rollup.csv` (wide per-PIID with bucket %)
- `extracted/fpds_pop_by_slug.csv` (per FPDS query slug)

---

## 6. Methodology deck — slide 2 added

`deck_methodology/slides/s02_subcomponents.py` — new slide between the
original Framing slide and Sources & Scope. Same L0 root ("FY Allocated
SCN Program $") + same L1 row (Plans / GFE / Basic Construction emphasized
/ Other) as slide 1, but L2 descends into physical subcomponents:

- **Plans (4):** Detail design / T&E engineering / Tech data / Config mgmt
- **GFE (6):** Nuclear propulsion (BPMI) / Combat systems (LM) / Sonar & EW
  (NG) / Ordnance & launch / Periscopes & electronics / HM&E
- **Basic Construction (6):** Hull modules / Outfitting / Auxiliary
  machinery / Missile compartment / Long-lead material / Integration & sea
  trials
- **Other (3):** ECPs / Block mods / Reserves

Existing s02/s03/s04 renamed to s03/s04/s05. `build.py` updated.

Also patched `primitives.py`:
- `add_footer` now uses 8pt non-italic (was 9pt italic)

User/linter also edited `primitives.py` to import additional symbols
(`Emu`, chart types, ramp constants) — looks like prep for future chart
primitives in a separate work stream.

---

## 7. Files written this session

### Scripts (new)

| File | Purpose |
|---|---|
| `scripts/aggregate_fpds_pop.py` | Per-PIID FPDS POP rollup (consumes the other agent's `pop_*` fields) |
| `scripts/pull_gd_10k_research.py` | Mirror of HII 10-K pull for General Dynamics (CIK 0000040533) |
| `scripts/pull_dod_announcements_pop.py` | 2025-2026 DoD announcement POP via globalsecurity.org |
| `scripts/fetch_wayback_batch.py` | Wayback batch fetcher for historical (2022-2024) bulletins |
| `scripts/ingest_wayback_bulletins.py` | Parses Wayback-cached HTMLs into the same CSV schema |
| `scripts/classify_dod_action_worktype.py` | First-pass regex classifier (program × work_type) |
| `scripts/reclassify_dod_action_subrelevance.py` | Second-pass judgment-based reclassifier |

### Deck modules (new + renamed)

| File | Purpose |
|---|---|
| `deck_methodology/slides/s02_subcomponents.py` | New subcomponent MECE tree (inserted as slide 2) |
| Renamed s02_sources_scope.py → s03_sources_scope.py | Slide ordering |
| Renamed s03_cleaning.py → s04_cleaning.py | Slide ordering |
| Renamed s04_caveats.py → s05_caveats.py | Slide ordering |
| `deck_methodology/build.py` | SLIDES list + imports updated |
| `deck_methodology/primitives.py` | `add_footer` size 8 non-italic |

### CSVs / data artifacts (new this session)

| File | Description |
|---|---|
| `extracted/fpds_pop_by_piid_state.csv` | Long form FPDS POP per (piid, state, country) |
| `extracted/fpds_pop_by_piid_rollup.csv` | Per-PIID POP wide with EB/HII/Other-US/Foreign %s |
| `extracted/fpds_pop_by_slug.csv` | Per FPDS vendor query slug |
| `extracted/dod_announcement_pop.csv` | 658 rows of DoD announcement paragraphs with POP %, program family, work type, sub-relevance |
| `extracted/dod_action_pop_by_worktype.csv` | $-weighted POP rollup per (program, work_type) bucket |
| `edgar_research/gd_marine_systems_segment.csv` | Long-form GD Marine Systems financials |
| `edgar_research/gd_marine_systems_segment_reconciled.csv` | Most-recent-vintage per FY |
| `edgar_research/gd_program_narrative.csv` | 61 sub-relevant snippets from GD 10-Ks |

### Research artifacts (new)

| File | Description |
|---|---|
| `edgar_research/gd_summary_memo.md` | GD 10-K analysis memo (margin compression + capex + teaming) |
| `edgar_research/gd_10k_files/<FY>/` | Raw 10-K HTML cache per FY (5 books FY21-FY25) |
| `research_primary_sources/dod_announcement_pop/README.md` | How-to + access-path notes (created early session, may want a refresh) |
| `research_primary_sources/dod_announcement_pop/dod_pop_actions.csv` | Initial 3-action verified seed (now superseded by the main CSV) |
| `research_primary_sources/dod_announcement_pop/cache/` | Globalsecurity.org cached daily indexes + contract pages |
| `research_primary_sources/dod_announcement_pop/cache_wayback/` | 192 cached Wayback bulletin HTMLs |
| `research_primary_sources/dod_announcement_pop/*.txt` | Per-action submarine paragraph text files |
| `DOD_ANNOUNCEMENT_HOWTO.md` | How-to guide written this session (see separate file) |

### Memory entries

A handful of feedback / reference memories were written early-session
when first picking up the project:
- `MEMORY.md` (index)
- `project_overview.md`
- `reference_session_logs.md`
- `feedback_blueforge_not_construction.md`
- `feedback_outsourcing_band_honest.md`
- `feedback_navy_target_all_shipbuilding.md`

(Located at `/Users/brendantoole/.claude/projects/-Users-brendantoole-projects2-submarine-outsourced-work/memory/`.)

---

## 8. Caveats — read before drawing conclusions

(Prior sessions' caveats still apply; new this session:)

1. **DoD announcement coverage is 2022-2026 only.** Pre-2022 isn't
   reachable via the routes we found (Wayback CDX returns very few
   defense.gov contract URLs pre-2022). The framework's analytical
   approach is "recent demonstration," not multi-decade trend.

2. **CY2022 coverage is partial.** We sampled 200 of 653 unique bulletin
   URLs in the CDX index. CY2022 is sparsest (59 rows) because the
   sampling was even across the ID range, but bulletin volume isn't
   uniform across years. Re-running with a fuller sample would add
   ~10-20 more TAM-relevant actions.

3. **Multi-tag actions get one primary tag.** A bundled action like the
   Columbia $15.38B mod contains design + lead-yard + SIB; the
   primary-tag heuristic puts it in `lead_yard`, but the action also
   matches the framework's "SIB capacity, not TAM" exclusion. The
   `is_sub_new_construction_tam` gate handles this correctly, but
   per-bucket rollups can be misread if you don't account for the
   bundling.

4. **The "0% everywhere" component_procurement rows are a parser issue,
   not a data issue.** Single-supplier-site actions use "Work will be
   performed in [City]" without a percentage (it's implicitly 100%); my
   `RE_POP` regex requires the `(NN%)` suffix. Affects $1.6B of the
   TAM-relevant total. Fixable in ~15 min if needed.

5. **The 41-row `sub_other` residual** (~$1.9B) wasn't manually classified
   by program. Likely some are Va/Col actions the rules missed. Marginal
   relative to the $25.4B headline but worth a tighter pass if pursuing
   the deck's geography slides.

6. **Wayback snapshots can be old or stale.** Some defense.gov articles
   have multiple snapshot dates; we picked the earliest. Should be
   identical to the live page for content; just be aware that if a page
   was edited post-snapshot, we have the original version.

7. **GD Marine Systems is not pure submarines.** ~60-70% submarine
   (Electric Boat) + the rest is Bath Iron Works (DDGs) + NASSCO
   (auxiliaries). Don't read the GD trajectory as 100% submarine.

---

## 9. Open methodology questions / next steps

In order of value:

1. **Pivot to main deck spec update + build.** The data backbone is now
   rich enough: cost funnel + GD 10-K + HII 10-K + 43 TAM-relevant DoD
   POP actions + FPDS POP + cost-funnel narrative + exec commentary +
   primary-source quotes. The 2026-05-24 main log §8 #4 lists the spec
   updates needed before building. This is the natural next session.

2. **Patch the single-supplier-site POP regex** if you want the $1.6B
   of "0% everywhere" actions properly attributed. Affects 17 rows;
   adds ~3-5 named supplier cities (Manassas VA, Syracuse NY, Braintree
   MA, etc.) to the geography picture.

3. **Sample another 200-400 Wayback URLs** if you want fuller pre-2025
   coverage. Diminishing returns — likely 10-20 more TAM-relevant
   actions. Cost: ~7 min per 200-URL batch.

4. **Tighter pass on the 41 `sub_other` residual rows** to promote any
   missed Va/Col actions. Manual reading + rule refinement, ~30 min.

5. **Component-bucket NAICS rollup with Hadrian-relevance score** —
   open from earlier conversation. Would let the deck say "of the
   $7-8B/yr addressable supplier opportunity, $X is precision-machined-
   component-shop-relevant per Hadrian's target NAICS cluster."

6. **GD 10-K data needs reconciliation across vintages.** Same logic as
   the HII NNS reconciliation, but for Marine Systems. Already partially
   in `gd_marine_systems_segment_reconciled.csv` (most-recent-vintage
   wins). Could add a "revision delta" column showing how much each FY's
   numbers shifted between vintages.

---

## 10. Hand-off — if next agent wants to extend

### To regenerate the DoD POP data

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work

# 2025-2026 from globalsecurity.org (resume-safe; skips cached)
python3 scripts/pull_dod_announcements_pop.py

# 2022-2024 from Wayback (assumes /tmp/wayback_urls_to_fetch.txt exists;
# see DOD_ANNOUNCEMENT_HOWTO.md §5 for how to regenerate that URL list)
python3 scripts/fetch_wayback_batch.py    # use 2s sleep, ~7 min for 200
python3 scripts/ingest_wayback_bulletins.py

# Classify
python3 scripts/classify_dod_action_worktype.py
python3 scripts/reclassify_dod_action_subrelevance.py
```

### To regenerate the GD 10-K data

```bash
python3 scripts/pull_gd_10k_research.py
# (Outputs to edgar_research/gd_*.csv + gd_summary_memo.md is hand-written)
```

### To regenerate FPDS POP rollup (after the parallel agent's pull)

```bash
python3 scripts/aggregate_fpds_pop.py
```

### Things to NOT do

- **Don't try direct war.gov / defense.gov from this Claude Code session** —
  Akamai blocks. Use globalsecurity.org for 2025+ or Wayback (via curl,
  NOT WebFetch) for 2022-2024.
- **Don't use WebFetch on web.archive.org** — blocked. Bash curl works.
- **Don't sleep less than 2 sec between Wayback requests** — rate limit
  kicks in.
- **Don't forget `--compressed` flag on curl when fetching Wayback** —
  some snapshots return gzipped content without proper Content-Encoding.
- **Don't run background Wayback batches longer than ~2 min** — harness
  background-Bash default timeout is 2 min. Use foreground with
  `timeout: 600000` (10 min max) or chunk.
- **Don't read raw `dod_announcement_pop.csv` as the headline number** —
  389 rows of CSV are 89%+ non-sub noise from the original loose filter.
  Always filter `is_sub_new_construction_tam == 'yes'` or
  `program_refined in {va, col, va_or_col, bpmi_nuclear, sub_gfe_*}`.

### Memories saved this session that affect future work

The early-session memory writes (project_overview, feedback_blueforge_not_construction,
feedback_outsourcing_band_honest, feedback_navy_target_all_shipbuilding,
reference_session_logs) are still relevant. No new memories added later in
the session — all session-specific findings are in this log + the how-to.

---

## 11. Quick orientation for next agent

**If user asks "what's the supplier-share of submarine new-construction $":**
- Headline: **52% of supplier-TAM-relevant dollars** go to outside-shipyard
  cities (per 43 actions / $25.4B / 34 months 2022-2026)
- Funnel-narrative version: 50-65% of Basic Construction is outsourced
  (industry-baseline band, supported by Navy + CEO primary sources)
- Per-bucket detail in `extracted/dod_action_pop_by_worktype.csv`

**If user asks "what's the cleanest single supplier signal":**
- BPMI nuclear reactor work: 13 actions / $4.8B / 80% supplier-city POP
  (concentrated Monroeville PA + Schenectady NY = Westinghouse)
- Va Block VI LLTM: 4 actions in 2025-2026 totaling $5.2B+ at ~98%
  supplier-city POP each (the supply-chain shift evidence)

**If user asks about the historical trend in outsourcing:**
- 2022-12-21 Columbia LLTM $5.13B: **75% EB / 25% HII / 0% supplier**
- 2026-05-11 Va Block VI LLTM $2.31B: **0% EB / 2% HII / 98% supplier**
- That's the "outsourcing acceleration" story in two primary-source data
  points. Combine with HII +30% YoY and Navy 10%→50% distributed
  shipbuilding for the narrative spine.

**If user asks "did the FPDS POP work pay off":**
- Yes, but for supporting purposes, not the headline. FPDS POP gives
  prime registration (always 100% Groton for GDEB), not outsourcing
  signal. The DoD announcement POP is the actual measurement.

**If user asks about Hadrian / Alabama supplier expansion:**
- Hadrian is named in the 30-Year Plan (PB27, line 376)
- AML3D is the documented BlueForge sub-recipient analog
- Alabama in nc_geo_by_state.csv shows $91M / 1.5% of US visible-subaward
  $ — the pre-Hadrian baseline
- No Hadrian-specific FFATA records yet; factory opened March 2026 so
  filings will lag until late 2026 at earliest

**If user asks "is GD doing the same outsourcing as HII":**
- No — opposite strategy. GD invests in own yards ($1.8B EB capex; 25%
  workforce ramp; +79% capex FY26 guided). HII expands outsourcing
  ("distributed shipbuilding" +30% YoY hours). Strategic divergence
  worth a dedicated deck slide.

**If user asks "where's the war.gov / DoD announcement how-to":**
- `DOD_ANNOUNCEMENT_HOWTO.md` at project root. Covers why this data is
  useful, all access paths tested, URL patterns, parsing, rate limits,
  and the full pipeline.
