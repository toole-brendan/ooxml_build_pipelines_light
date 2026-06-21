# Session Log — submarine_outsourced_work — 2026-05-22

**Handoff doc for the next AI agent.** This is what was done in the session that
started 2026-05-21 ~23:00 and ran through 2026-05-22 ~22:00. Read this FIRST before
touching anything in `/Users/brendantoole/projects2/submarine_outsourced_work/`.

---

## 1. Project context — what we're trying to do

**Goal:** Identify how much money/work is outsourced **per year** by the U.S.
nuclear submarine "primes" (General Dynamics Electric Boat = GDEB, and to a lesser
extent HII Newport News Shipbuilding = HII-NNS).

**Who the primes are:**
- **GDEB** — prime of record on ALL Virginia (SSN) + Columbia (SSBN) construction
  contracts. Lead yard for Columbia.
- **HII-NNS** — team partner. ~50/50 split on Virginia, ~78/22 (GDEB lead) on
  Columbia. Does NOT appear as prime in FPDS for submarine construction — work
  flows through GDEB via teaming agreement. This is a known visibility gap.
- **BPMI** (Bechtel Plant Machinery Inc.) — naval reactor components (GFE — Navy
  contracts BPMI directly, ships to GDEB to install).
- **Lockheed Martin, Northrop Grumman, BAE, L3Harris, Curtiss-Wright** — major
  sub vendors / GFE primes.

**What "outsourced" means in this project:**
1. First-tier subcontracts GDEB issues (visible in FFATA via SAM.gov + USAspending)
2. GFE primes (Navy → BPMI etc., separate from GDEB but still outsourced from a
   "what does the prime self-perform" POV)
3. Maritime Industrial Base (MIB) consortium pass-throughs (BlueForge Alliance) —
   but the user has clarified these should NOT count as construction outsourcing
   (see Section 5 below)

**Time window agreed:** FY20-FY26 (with FY27 included for the request year). User
chose this to capture one full Virginia block (Block V = FY19-23) plus the start
of Block VI, plus the MIB transition (pre-MIB FY20-22 vs MIB era FY23-26).
Avoids over-narrow window that would miss block dynamics and avoids over-wide
window that adds noise from a different procurement era.

---

## 2. What was already in place before this session

The folder `/Users/brendantoole/projects2/submarine_outsourced_work/` was created
in this session. But the project had heavy reference material from related prior
work elsewhere:

- `/Users/brendantoole/projects2/army_rdte/` — has FPDS pull scripts + the
  `federal_procurement_data_guide.txt` field reference + a
  `Federal_Procurement_Research_Lessons_Learned.md` doc with gotchas from prior
  pulls (this doc is gold — read sections 2, 5, 6, 10, 14).
- `/Users/brendantoole/projects2/buildco3/analysis/SAM_Submarine_Cutter_Contract_Awards.md`
  — prior FY20-26 submarine analysis with seed PIIDs and cumulative obligated $
  per PIID. Used as the SOURCE for the 17 seed PIIDs that drove the subaward pulls.
- `/Users/brendantoole/projects2/budget_books_cons/SCN/` — already had SCN_Book
  FY24, FY25, FY26 PDFs.

All four reference docs are now copied into `reference_prior_analysis/` so they
travel with the project.

---

## 3. Data sources used + their gotchas

### FPDS Atom Feed (no auth)
- Endpoint: `https://www.fpds.gov/ezsearch/FEEDS/ATOM?FEEDNAME=PUBLIC`
- Use `VENDOR_NAME:"..."` for vendor search — NOT `UEI_NAME` (latter silently
  returns 0 results despite being in the docs).
- `CONTRACTING_AGENCY_ID:"1700"` = Navy. Use this, not `AGENCY_CODE` (which
  doesn't work in the public Atom feed despite docs).
- Pagination is 10 records/page. Set a 0.3-0.5s delay between pages.
- PIID direct lookup does NOT work — must search by vendor/date and filter in code.

### USAspending /api/v2/subawards/ (no auth)
- **2-call pattern**: first `/api/v2/search/spending_by_award/` with `award_ids: [PIID]`
  to get `generated_internal_id`, then `/api/v2/subawards/` with `award_id: <gid>`.
- Try Contracts group `["A","B","C","D"]` first; fall back to IDV group
  `["IDV_A","IDV_B",...]` if no results. Cannot mix groups in one call (HTTP 422).
- **~2,500-record cap per prime** — silently truncates. We hit this on
  N0002417C2100 (Virginia Block V/VI master) and N0002417C2117 (Columbia Build I/II).
  Sort by `amount` desc so top dollars are kept when capped.

### SAM.gov Acquisition Subaward Reporting API (API key required)
- Endpoint: `https://api.sam.gov/prod/contract/v1/subcontracts/search` — keep
  `/prod/` in the URL (docs example drops it and 404s).
- **Parameter `piid` is LOWERCASE** — uppercase `PIID` is silently dropped (even
  though docs table shows uppercase). To verify your filter was honored: inspect
  `nextPageLink` in response body and check it contains `piid=`. If not, you're
  paginating the entire 2.7M-record dataset.
- **NO per-prime cap** (unlike USAspending). This is the main reason to use SAM
  for big-master PIIDs.
- **Numeric fields returned as strings** — coerce with `float()`.
- **subAwardReportId is unique** — no dedup needed (verified clean: 11,005
  records, 11,005 unique IDs, 0 collisions).
- API key in `.env`: `SAM_API_KEY=SAM-e57b65ab-7471-4f6b-8d9b-9adf288254db`
  (entity-role tier, 1,000/day quota).
- **Use `pageSize=1000`** (max). Smaller pageSize means MORE pages, and SAM has
  SPECIFIC slow pages on deep-paginated PIIDs (e.g., page 3 of N0002417C2100
  consistently takes ~3 min). With pageSize=1000, big masters are only ~5 pages
  so we hit at most ONE slow page per PIID instead of many.
- **API bug**: SAM keeps returning `nextPageLink` even when there's no more
  data (empty pages overshoot). MUST stop when `len(records) >= totalRecords`
  OR when page_data is empty. Otherwise the script wastes ~3 min per empty page.
- See `SAM_GOV_HOWTO.md` at the project root for full guide.

### SCN budget books (PDF justifications)
- 6 books on disk: PB22, PB23, PB24, PB25, PB26, PB27 (in `budget_books/`).
- Each book covers ~7 years: Prior Years (lump) | FY-2 actual | FY-1 estimate |
  FY request (Base + OCO/OOC + Total) | FY+1 outyear | ... | To Complete | Total.
- The TOA values for any given FY get REVISED in subsequent books — the most
  recent book with the FY as "actual" has the most-revised number. The
  `scn_per_fy_actual_toa.csv` does this reconciliation automatically.
- P-1 line numbers DRIFT across books (Virginia was #5 → #5 → #5 → #5 → #8 → #6)
  but LI numbers are stable: Columbia = LI 1045, Virginia = LI 2013.

---

## 4. What was built in this session

### Folder structure
```
submarine_outsourced_work/
├── README.md                          (project goal + plan)
├── MANIFEST.md                        (file inventory)
├── SUMMARY_INITIAL_FINDINGS.md        (headline tables + commentary)
├── SAM_GOV_HOWTO.md                   (user-provided SAM API guide)
├── .env                                (SAM API key)
├── logs/
│   └── 2026-05-22_session_log.md      (this file)
├── budget_books/
│   ├── SCN_Book_FY22.pdf + .txt       (April 2022 / PB22)
│   ├── SCN_Book_FY23.pdf + .txt
│   ├── SCN_Book_FY24.pdf + .txt
│   ├── SCN_Book_FY25.pdf + .txt
│   ├── SCN_Book_FY26.pdf + .txt
│   ├── SCN_Book_FY27.pdf + .txt       (April 2026 / PB27)
│   └── 30_Year_Shipbuilding_Plan.pdf + .txt
├── reference_prior_analysis/
│   ├── federal_procurement_data_guide.txt        (FPDS/USA/SAM field reference)
│   ├── Federal_Procurement_Research_Lessons_Learned.md (REQUIRED reading)
│   ├── Subaward_Pull_Lessons_Learned.md
│   └── SAM_Submarine_Cutter_Contract_Awards.md   (prior submarine analysis)
├── scripts/
│   ├── extract_scn_submarine_lines.py            (single-book FY27 extractor — legacy)
│   ├── extract_scn_multi_vintage.py              (P-40 Resource Summary across all books)
│   ├── extract_scn_p5c_multi_vintage.py          (P-5c cost categories across all books)
│   ├── pull_fpds_sub_primes.py                   (13 FPDS vendor/description queries)
│   ├── pull_usaspending_subawards.py             (17 seed PIIDs → /api/v2/subawards/)
│   ├── pull_sam_subawards.py                     (17 PIIDs via SAM.gov, FY20-26 window)
│   ├── smoke_sam.py                              (diagnostic — sequential page test)
│   ├── smoke_sam_v2.py                           (diagnostic — pageSize+keepalive test)
│   ├── aggregate_annual_outsourcing.py           (FPDS + USA rollup)
│   ├── aggregate_sam_subawards.py                (SAM rollup + USA comparison)
│   ├── consolidate_budget_vs_subawards.py        (v1: TOA vs subs)
│   └── consolidate_v2_basic_construction.py      (v2: Basic Construction vs non-BlueForge subs)
├── extracted/                          (parsed CSVs — see Section 6)
├── fpds_raw/                           (13 FPDS pulls — 21,553 records / 6,816 PIIDs)
├── usaspending_subawards/              (17 PIID subaward JSON files + summary)
└── sam_subawards/                      (17 PIID subaward JSON files + summary)
```

### Sequence of work (chronological)
1. **Discovered** `army_rdte/` FPDS guide + `buildco3/analysis/` prior submarine analysis
   already had FY20-26 work covering same primes — used as seed for PIID list.
2. **Copied** FPDS guide + lessons-learned + prior analysis into
   `reference_prior_analysis/`.
3. **User provided** FY27 SCN_Book + 30-Year Shipbuilding Plan PDFs. Converted to
   layout text via `pdftotext --layout`.
4. **Wrote** `extract_scn_submarine_lines.py` (FY27 book only) — pulled Columbia
   LI 1045 + Virginia LI 2013 line items.
5. **Wrote + ran** `pull_fpds_sub_primes.py` (~30 min wall time, 13 queries,
   21,553 records). User declined to wait for SAM at first attempt due to hangs.
6. **Wrote + ran** `pull_usaspending_subawards.py` (~5 min, 17 PIIDs). USA cap
   hit on 2 big masters (2,500 records each).
7. **Generated** v1 `annual_budget_vs_subawards.csv` using FY27 book TOA + USA subs.
8. **User asked** to add FY22-FY27 SCN books for multi-vintage actuals. User
   provided FY22 + FY23 PDFs from Downloads (rest were copied from
   `budget_books_cons/SCN/`).
9. **Wrote** `extract_scn_multi_vintage.py` (P-40 Resource Summary across 6 books)
   + reconciliation logic that picks most-recent-book showing each FY as actual.
10. **User asked** to add SAM.gov as a third subaward source (per `SAM_GOV_HOWTO.md`).
11. **Wrote** `pull_sam_subawards.py`. First attempt hung (pageSize=1000, no
    per-page logging — I had no visibility into where it was stuck). User
    correctly intuited it might be misuse.
12. **Diagnostic smoke tests** found: SAM has SPECIFIC slow pages on deep-paginated
    PIIDs (page 3 of N0002417C2100 always takes ~3 min). With pageSize=100 we
    hit MORE slow pages; pageSize=1000 minimizes them. Also: SAM keeps returning
    `nextPageLink` past `totalRecords` (empty-page overshoot bug).
13. **Patched** `pull_sam_subawards.py` with `pageSize=1000` + per-page logging
    + empty-page/overshoot stop conditions.
14. **Set up Monitor** on the SAM pull output so I'd get pushed events on
    each PIID start/stop/error — no polling required by user.
15. **Ran SAM pull** to completion (~30 min wall time). 11,005 records across
    17 PIIDs. Recovered ~3,500 long-tail records from the 2 capped USA PIIDs.
16. **Wrote** `aggregate_sam_subawards.py` — dedup verification (clean),
    parent-UEI rollup, SAM-vs-USA comparison per PIID.
17. **User asked** for Basic Construction vs subs (not TOA). I (wrongly) said I
    only had P-5c for FY27; user correctly pointed out it's a line item I should
    have extracted across vintages.
18. **Wrote** `extract_scn_p5c_multi_vintage.py` — Basic Construction +
    Plan Costs + other cost categories per ship per FY across all 6 books.
19. **Wrote** `consolidate_v2_basic_construction.py` with three ratios:
    - A: All subs / TOA
    - B: (Subs - BlueForge) / (TOA - Plan Costs)
    - C: (Subs - BlueForge) / Basic Construction
20. **User clarified**: BlueForge is workforce/training/supplier infrastructure,
    NOT construction. So the right ratio is **Non-BlueForge subs ÷ Basic
    Construction = 15.4% cumulative FY21-FY25**. Saved to memory:
    `~/.claude/projects/-Users-brendantoole-projects2/memory/feedback_blueforge_not_construction.md`.

---

## 5. Headline findings

### Per-FY budget allocation (reconciled across PB22-PB27 books)

| FY | Columbia TOA $M | Virginia TOA $M | Total Sub SCN $M | Source vintage |
|---|---:|---:|---:|---|
| FY20 | 1,821 | 8,335 | 10,156 | PB22 book (actuals) |
| FY21 | 4,122 | 6,776 | 10,899 | PB23 book |
| FY22 | 4,777 | 6,340 | 11,117 | PB24 book |
| FY23 | 5,858 | 6,865 | 12,722 | PB25 book |
| FY24 | 7,789 | 10,657 | 18,446 | PB26 book |
| FY25 | 9,581 | 13,320 | 22,901 | PB27 book |
| FY26 | 9,280 | 6,378 | 15,657 | PB27 book (estimate) |
| FY27 | 15,583 | 13,151 | 28,734 | PB27 book (request) |

**Notable revisions across vintages:**
- Virginia FY24 actual was $10.7B; PB23 had estimated only $8.3B (+$2.3B revision)
- Virginia FY25 actual was $13.3B; PB23 had estimated only $8.7B (+$4.6B revision)
- Columbia FY24 actual $7.8B vs PB23 estimate $5.8B (+$2.0B)
- Columbia FY25 actual $9.6B vs PB23 estimate $7.2B (+$2.4B)

These upward revisions are driven by inflation, shipbuilder performance issues
on SSBN 826/827 (consumed all schedule margin), and the MIB ramp.

### Subaward $ per FY (SAM.gov, FY20-26 window)

| FY | Total subs $M | BlueForge $M | Non-BlueForge $M |
|---|---:|---:|---:|
| FY20 | 372 | 0 | 372 |
| FY21 | 599 | 0 | 599 |
| FY22 | 675 | 0 | 675 |
| **FY23** | **3,727** | **1,514** | 2,213 |
| **FY24** | **4,013** | **2,659** | 1,354 |
| FY25 | 780 (lag) | 0 | 780 (lag) |
| FY26 | 0 (no data) | 0 | 0 |

### Construction outsourcing ratio (THE answer)

**Cumulative FY21-FY25** (FY20 excluded because we don't have Basic Construction
detail for FY20 — earlier books needed):

| Measure | $M |
|---|---:|
| Sum Basic Construction (Col + Va ships authorized FY21-FY25) | 36,586 |
| Sum non-BlueForge subs FY21-FY25 | 5,621 |
| **Non-BlueForge subs ÷ Basic Construction = 15.4%** | |

Per-FY breakdown is lumpy because of temporal mismatch (Basic Construction is
per-ship as-of-authorization; subaward $ is cash flow that FY across all active
ships and blocks):

| FY | Non-BF subs / Basic |
|---|---:|
| FY21 | 10.0% |
| FY22 | 14.2% |
| FY23 | 43.4% ← spike is real (conventional, not MIB consortium) |
| FY24 | 8.8% (Block VI big Basic Construction inflated denominator) |
| FY25 | 14.6% (lag-affected) |

### Top sub recipients FY20-26 (SAM, parent-UEI rolled)

| Rank | Parent | $M | Notes |
|---:|---|---:|---|
| 1 | BlueForge Alliance | 4,173 | **MIB pass-through — workforce/training, NOT construction** |
| 2 | Northrop Grumman Systems | 1,485 | Sonar, EW, combat systems |
| 3 | Leonardo SPA (IT) | 491 | Likely electronics/propulsion |
| 4 | Curtiss-Wright Electro-Mechanical | 316 | Nuclear pumps |
| 5 | Globe Composite Solutions | 248 | Composite structures |
| 6 | Scot Forge | 200 | Large forgings |
| 7 | D.C. Fabricators | 163 | Hull fabrication |
| 8 | Rhoads Metal Fabrications | 142 | Metalwork |
| 9 | CIRCOR International | 102 | Valves |
| 10 | The Graham Corporation | 89 | Heat exchangers |
| 11 | Austal USA | 88 | Surprising — appears as a SUB |
| 12 | L3Harris Maritime Power | 85 | Power conversion |
| 13 | Rosyth Royal Dockyard (UK) | 84 | UK partner |
| 14 | W International | 83 | Machining |
| 15 | Teledyne Technologies | 78 | Sensors |

Full top-200 in `extracted/sam_subaward_top_parents.csv`.

---

## 6. Files generated in `extracted/` (CSVs)

| File | Generated by | What's in it |
|---|---|---|
| `scn_li_resource_summary.csv` | extract_scn_submarine_lines.py | Single-book FY27 only. P-40 Resource Summary rows × FY columns for Columbia + Virginia. |
| `scn_li_cost_categories.csv` | extract_scn_submarine_lines.py | Single-book FY27 only. P-5c cost categories per ship. |
| `scn_li_production_schedule.csv` | extract_scn_submarine_lines.py | Single-book FY27. Hull × shipbuilder × dates. |
| `scn_li_per_fy_long.csv` | extract_scn_multi_vintage.py | Long-form (vintage, li, p1_section, row_label, fy_label, value) across all 6 books × all P-40 rows. |
| `scn_per_book_columns.csv` | extract_scn_multi_vintage.py | Diagnostic — each book's detected column schema. |
| `scn_per_fy_actual_toa.csv` | extract_scn_multi_vintage.py | **THE per-FY TOA reconciliation** — for each (LI, FY, row), the most-revised value across vintages + the source vintage. |
| `scn_p5c_per_fy_long.csv` | extract_scn_p5c_multi_vintage.py | Long-form P-5c cost categories × FY × vintage. |
| `scn_p5c_per_fy_reconciled.csv` | extract_scn_p5c_multi_vintage.py | **THE per-FY Basic Construction / Plan Costs / etc. reconciliation**. |
| `fpds_annual_by_prime.csv` | aggregate_annual_outsourcing.py | Per-FY sum of FPDS this-mod obligated $ by vendor group. |
| `subaward_annual_by_prime.csv` | aggregate_annual_outsourcing.py | Per-FY × per-PIID USAspending subaward $. |
| `subaward_top_recipients.csv` | aggregate_annual_outsourcing.py | Top 200 USA sub recipients. |
| `sam_subaward_annual_by_prime.csv` | aggregate_sam_subawards.py | Per-FY × per-PIID SAM subaward $. |
| `sam_subaward_top_parents.csv` | aggregate_sam_subawards.py | Top 200 SAM sub recipients (parent UEI rolled). |
| `sam_subaward_full_dedup_check.txt` | aggregate_sam_subawards.py | Verifies SAM is dedup-clean (11,005 records, 11,005 unique subAwardReportIds). |
| `sam_vs_usaspending_per_piid.csv` | aggregate_sam_subawards.py | Side-by-side per PIID. |
| `annual_budget_vs_subawards.csv` | consolidate_budget_vs_subawards.py | v1 — TOA vs subs (uses SAM as authoritative + USA for cross-validation). |
| `annual_budget_vs_subawards_v2.csv` | consolidate_v2_basic_construction.py | **v2 — THE headline table with 3 ratios** (TOA / TOA-Plans / Basic Construction). |

---

## 7. Caveats — read before drawing conclusions

1. **HII-NNS submarine share is invisible.** Per teaming agreement HII-NNS does
   ~50% of Virginia + ~22% of Columbia. But in FPDS only GDEB shows as prime
   on submarine contracts. HII-NNS work either shows as sub of GDEB (some —
   $98M visible per USAspending data; vastly understates real share) OR is
   routed through Northrop Grumman (some of the NG sub $ might be HII work).
   Real HII share only available from HII 10-K segment disclosures + analyst
   estimates.

2. **USAspending 2,500-record cap.** Hit on N0002417C2100 + N0002417C2117. SAM
   recovers the long-tail (~3,500 more records) but mostly small subs.

3. **SAM date filter** = FY20-26 means older block contracts (e.g., Virginia
   Block IV N0002412C2115) appear empty in SAM but had real pre-FY20 activity.
   For full-history pull, remove `fromDate`/`toDate` in `pull_sam_subawards.py`.

4. **Subaward reporting lag.** FY25 subaward $ is heavily lag-depressed
   (~6-18 month FFATA filing lag). Expect FY25 to climb 2-4x as filings catch up.
   FY26 essentially empty for same reason.

5. **FFATA non-compliance.** Some primes systematically under-report. GDEB does
   report; some other primes (Bollinger, BIW, etc.) don't.

6. **MIB / BlueForge ≠ construction outsourcing.** User explicitly clarified
   this. BlueForge $4.17B is workforce + supplier infrastructure pass-through.
   Should be excluded from "% of construction subawarded" calculations. Saved
   to memory: `feedback_blueforge_not_construction.md`.

7. **Basic Construction is per-ship-authorization, NOT per-FY cash flow.** A
   FY23 sub action might be material installed on SSN 802 (FY19 Block V auth).
   Per-FY ratios C are lumpy; cumulative ratio (15.4%) is the cleaner read.

8. **No FY20 Basic Construction available** in our books. PB22 book's earliest
   "actual" column is FY20 but for ships that are now lumped into Prior Years.
   To get FY20-FY21 Virginia Basic Construction, need PB20 and PB21 SCN books.

9. **Cumulative vs window dollars in FPDS.** `totalObligatedAmount` is the
   running cumulative total at the latest mod — NOT the FY's spend. My
   `aggregate_annual_outsourcing.py` correctly uses per-mod `this_obligated`
   summed by signed-date FY. Don't change this.

10. **Federal naval shipyards** (Norfolk, Portsmouth, Pearl Harbor, Puget Sound)
    do depot maintenance with federal payroll. Not in scope, not in our subaward
    data — explicitly excluded.

---

## 8. Open methodology questions / next steps

These were flagged but NOT done in this session:

1. **Pull SAM with no date filter** to confirm USAspending cap math and get
   the full ~5,681-record history on N0002417C2100 (per howto). Useful for
   cross-validation.

2. **Per-ship attribution within window** — the subaward data is per PIID
   (which often covers multiple ships in a block). Mapping per-FY subaward $
   back to specific hulls would require parsing mod descriptions for hull refs
   (e.g., "SSN 812 CONSTRUCTION (BOAT 2, FY 24)").

3. **HII-NNS estimate from 10-K segment data** — not done. Would require
   pulling HII Newport News Shipbuilding segment revenue + analyst breakdowns.

4. **Get PB20 + PB21 SCN books** for FY20-FY21 Basic Construction at full
   detail. Currently those years' Basic Construction is lumped into "Prior Years"
   in the books we have.

5. **What does BlueForge distribute to?** They're a consortium pass-through.
   Their own subaward filings (or DPA Title III award announcements) would
   show where the $4.17B actually went (small/mid-tier shops, workforce
   training programs, facility build-outs). Out of scope this session.

6. **Compare to commercial shipyard outsourcing rates** for context. E.g.,
   what % of a commercial product tanker's build cost is outsourced by HMD/SHI/DSME?
   15% would seem low for shipbuilding generally, suggesting GDEB's vertical
   integration is unusually high OR our visible subaward data is missing a lot.

7. **30-Year Shipbuilding Plan extraction** — converted to text but never
   systematically parsed. The PB27 plan has procurement profile by class
   through FY56 plus MIB narrative. Could enrich the analysis.

---

## 9. Bugs encountered + fixed in this session

| Bug | Symptom | Fix |
|---|---|---|
| SAM pull hung with no visibility | Wall time 18 min, only "PIID 1 start" in log | Added per-page logging (timing + record count); diagnosed as SAM's specific-slow-pages behavior, not actual hang. |
| Switched to pageSize=100 thinking it would help | Made it WORSE — 44 pages × random slow pages vs 5 pages × 1 slow page | Reverted to pageSize=1000 per howto recommendation. |
| SAM API returns `nextPageLink` past `totalRecords` | Script wandering into empty pages, each taking ~3 min | Added stop conditions: empty `page_data` OR `len(records) >= totalRecords`. |
| SCN extractor `"Resource Summary"` matched the parenthetical note line | Header silently clobbered → 0 FY columns detected | Only parse FIRST "Resource Summary" occurrence; ignore later ones. |
| FY column tags drifted across books | Virginia P-1 # was 5/5/5/5/8/6 across PB22-PB27 | Use LI number (1045/2013), which is stable. Detect FY columns from header line per book. |
| FY request year had Base/OOC/Total sub-columns inserted oddly | Order of columns wrong | Walk header FYs in order; insert request-year sub-cols in the gap between FY-1 and FY+1. |
| Page-marker regex required leading slash | Virginia P-5c not detected (BSA name "Other" jams against LI #) | Changed `/\s*{li}` to `\b{li}` word boundary. |
| `rm -f *.json` failed on empty glob in zsh | Command failed before pull could start | Skipped the rm; restarted directly. |
| Initial monitor command timed out at 30 min | Pull was still running; missed the "Done." event | Could re-arm with longer timeout next time. Output file was preserved so re-check worked. |

---

## 10. Hand-off — if next agent wants to extend

**To re-run the entire pipeline from scratch:**
```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work

# Budget extraction (fast)
python3 scripts/extract_scn_multi_vintage.py
python3 scripts/extract_scn_p5c_multi_vintage.py

# FPDS (slow ~30 min)
python3 scripts/pull_fpds_sub_primes.py

# USAspending subawards (medium ~5-10 min)
python3 scripts/pull_usaspending_subawards.py

# SAM.gov subawards (slow ~30 min — be patient through the slow pages)
python3 scripts/pull_sam_subawards.py

# Aggregations + final tables
python3 scripts/aggregate_annual_outsourcing.py
python3 scripts/aggregate_sam_subawards.py
python3 scripts/consolidate_budget_vs_subawards.py
python3 scripts/consolidate_v2_basic_construction.py
```

**Things to NOT do:**
- Don't switch SAM pageSize away from 1000 — smaller is slower (more pages = more slow-page encounters).
- Don't include BlueForge in any "construction outsourcing rate" calc — user has clarified this is not construction.
- Don't try to dedup SAM `subAwardReportId` — already unique (verified).
- Don't kill the SAM pull when it looks "stuck" — page 3 of the big masters always takes ~3 min; that's expected.
- Don't pull SAM with date window crossing today's date — `toDate` must not exceed current date (HTTP 400).

**Memories saved this session that affect future work:**
- `~/.claude/projects/-Users-brendantoole-projects2/memory/feedback_blueforge_not_construction.md` — BlueForge / MIB consortium ≠ construction outsourcing
- (existing) `feedback_no_extra_fields.md`
- (existing) `project_scf_routes.md`
- (existing) `reference_commercial_strategy_decks.md`

---

## 11. Final state of task list

| # | Subject | Status |
|---|---|---|
| 1 | Set up submarine_outsourced_work folder with plan + sources index | ✓ completed |
| 2 | Extract submarine line items from FY27 SCN book + 30-year plan | ✓ completed |
| 3 | Pull FPDS atom feed for submarine prime contracts (GDEB + HII-NNS) | ✓ completed |
| 4 | Pull subaward data from USAspending (first-tier subs of GDEB + HII-NNS) | ✓ completed |
| 5 | Write summary index + raw data manifest in submarine_outsourced_work/ | ✓ completed |
| 8 | Convert FY22-FY26 SCN PDFs to layout text | ✓ completed |
| 9 | Extend SCN extractor to handle multi-vintage books + reconcile per-FY actuals | ✓ completed |
| 10 | Run narrowed SAM.gov pull (FY20-26, smaller pageSize) | ✓ completed |
| 11 | Aggregate SAM data + comparison vs USAspending + update final budget vs subawards table | ✓ completed |

Tasks #6 and #7 were created and then deleted (they were earlier attempts at the SAM pull that got halted; superseded by #10).

---

## 12. Quick orientation for next agent

**If user asks "what's the outsourcing rate":** Cite **15.4% (cumulative FY21-FY25)** — that's
non-BlueForge subs ÷ Basic Construction. See `extracted/annual_budget_vs_subawards_v2.csv`.

**If user asks for "the headline table":** `extracted/annual_budget_vs_subawards_v2.csv`.

**If user asks "where's the data":** `SUMMARY_INITIAL_FINDINGS.md` for narrative;
`extracted/` for CSVs; `sam_subawards/` + `usaspending_subawards/` + `fpds_raw/` for raw JSON.

**If user asks to add a new PIID:** Add to `SEED_PIIDS` list in
`pull_usaspending_subawards.py` AND `pull_sam_subawards.py`, then re-run both
and re-aggregate.

**If user asks "what about HII-NNS share":** Not in federal data — see Caveat #1.
Out of scope for this session.

**If user asks about a different program (e.g., DDG, CVN):** This project is
submarine-only. Could repurpose scripts but would need new seed PIIDs from
prior analyses (`buildco3/analysis/`).
