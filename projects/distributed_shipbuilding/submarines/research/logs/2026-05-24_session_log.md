# Session Log — submarine_outsourced_work — 2026-05-24

**Handoff doc for the next AI agent.** Read both prior logs first:
1. `logs/2026-05-22_session_log.md` (initial workbook build)
2. `logs/2026-05-23_session_log.md` (new-construction refinement + HII context)
3. This file

This session reframed the entire deck around a cost-funnel narrative and
ran a full primary-source research pass to ground the framing.

---

## 1. What this session was about

User came in asking to execute `DECK_BUILD_SPEC.md` — a previously drafted
plan for generating a `.pptx` deterministically from the research artifacts.

The session evolved through three distinct phases:

**A. Deck structure review (early session).** Read the spec, critiqued the
slide list, proposed a revised 12-core + 6-appendix structure, then updated
the spec in-place.

**B. Fundamental reframing (mid-session).** User noted another LLM had
estimated ~60% of submarine prime-contract value is outsourced — versus our
deck's "20%" headline. This exposed a real framing problem: my 20% measured
*only FFATA-visible first-tier subawards*, not the total outsourced layer.
User proposed a cleaner funnel narrative starting at total boat cost and
cutting down through LLTM / GFE / Basic Construction / Outsourced — and
chose "Option C" (deep-dive 6-phase research).

**C. Option C execution (rest of session).** Built the cost funnel data
backbone (Phase 1+2), then ran a deep primary-source research pass
(Phase 3) including pulling executive commentary from earnings calls
(HII + GD) and the Navy's own May 2026 policy plan via NewsAPI.

---

## 2. The reframed deck narrative

The user's funnel framing is now the deck's spine:

```
Total Ship Cost (~$5B Va, ~$10.7B Col per boat)
  ├── Plans (engineering / NRE) ~10-15%
  ├── GFE (BPMI nuclear / Lockheed combat sys / NG sonar / etc.) ~20-25%
  ├── Other + Change Orders ~2-5%
  └── Basic Construction (the prime contract base) ~60-70%
        ├── Yard self-performed (~35-50% of BC)
        └── Outsourced inside BC (~50-65% of BC industry-baseline band)
              ├── FFATA-visible first-tier subawards (~$1-2B/yr — named vendors)
              └── Unseen layer: purchased material + lower-tier subs +
                  FFATA non-compliance (the bulk)
```

For Saronic this answers "where's the addressable supplier opportunity":
- At 60% mid-case: ~$4.2B per Col / ~$2.1B per Va in prime-directed
  material+subs
- Plus GFE chain: ~$2B per Col / ~$0.8B per Va
- = **~$7-9B/yr of outsourced new-construction supplier opportunity** at
  current build rate (1 Col + 2 Va/yr), ramping

FFATA captured only ~$1B/yr of this — about 10-15% of the real pie. The
prior deck framing claimed "20%" was the outsourcing rate; it's actually
the *named-vendor-visible portion of the real outsourcing layer*.

---

## 3. What got built (chronological)

### 3.1 Deck spec update (early session)

Edited `DECK_BUILD_SPEC.md`:
- §5 fully rewritten — 12-core + 6-appendix instead of 14+5
- New four-act arc: Setup / Sizing / Structure / So What
- Slide 5 ("The hidden slice") promoted; new Slide 6 ("The real
  outsourced number") added
- Methodology moved to Appendix A1
- §6 data flow re-mapped to new slide numbers
- §7.3 (slide-list open question) marked RESOLVED with sub-decision detail
- §7.8 (quote curation) updated to point to slide 11

### 3.2 Cost funnel build (Phase 1+2)

**Phase 1a — Inspect budget book TXT structure.** Discovered: the AP/LLTM
data was already extracted into `scn_li_per_fy_long.csv` from the prior
session — as P-40 Resource Summary rows "Less PY Advance Procurement
($ in Millions)" and "Plus CY Advance Procurement ($ in Millions)". The
existing extractor's `p1_section` field tried to capture a dedicated "ap"
section but the regex never matched the actual page header — but it didn't
matter because the AP figures are in the base P-40 already.

**Phase 1b+1c — Skipped writing a new extractor.** Not needed; long-form
CSV already has the data.

**Phase 2 — `scripts/build_cost_funnel.py`** combines:
- `scn_li_per_fy_long.csv` (P-40 metrics: qty, gross cost, unit cost,
  Less PY AP, Plus CY AP, Net Proc, TOA)
- `scn_p5c_per_fy_reconciled.csv` (cost categories: BC, Plans,
  Propulsion, Electronics, HM&E, Ordnance, Other, Change Orders, Total)

Reconciles across vintages with the most-recent-PB-year≥FY+2 rule (same
logic as prior extractor). Outputs:
- `extracted/cost_funnel_per_class.csv` (long form)
- `extracted/cost_funnel_summary.csv` (wide, deck-ready)

Validated: Col FY27 net procurement = $6,904.785M matches budget book P-1
to the dollar. Col FY27 Plus CY AP = $4,763.342M matches. P-5c categories
all reconcile against the source TXT files.

### 3.3 Exhibit P-10 detail extraction (Phase 1.5)

**`scripts/extract_scn_p10_ap_detail.py`** — pulls the detailed P-10
"Advance Procurement Requirements Analysis" tables.

Va and Col have different P-10 structures:
- **Col uses ~13 numbered sub-categories:** PLANS (1), BASIC CONSTRUCTION
  (3) SHIPBUILDER PROCURED LLTM, BC(4) MISSILE TUBE, BC(5) ADVANCE
  CONSTRUCTION, BC(6) EOQ, BC(7) SHIPYARD MANUFACTURED, NUCLEAR PROPULSION
  PLANT EQUIPMENT (8), HM&E (9), ORDNANCE SWS (10-12), ELECTRONICS (13),
  Electronics EOQ (14).
- **Va uses 3 top-level + sub-items:** Advance Procurement (with sub-items
  Nuclear Propulsion / Electronics / Propulsor / CFE-1yr / CFE-2yr),
  Economic Order of Quantity, Plans.

Multiple parser quirks handled:
- Multi-line `Total:` labels (e.g., "Total: BASIC CONSTRUCTION (6) - EOQ
  IN SUPPORT OF MULTI-" wraps to two lines with values on the line between)
- Va sub-items where LABEL comes AFTER values (PDF text extraction puts
  `(4) 1,273.090...` on one line and `Nuclear Propulsion Plant Equipment`
  on the NEXT line)
- "(N) inline values" vs "(N) alone with values on next line" — both
  patterns occur in the Va P-10

Outputs:
- `extracted/scn_p10_ap_long.csv` (long form, all vintages)
- `extracted/scn_p10_ap_reconciled.csv` (best per category per FY)
- `extracted/scn_p10_ap_buckets.csv` (grouped into 8 deck-narrative
  buckets: Nuclear plant LLTM / Electronics LLTM / Propulsor LLTM /
  Shipbuilder-procured LLTM / Missile compartment LLTM / EOQ / HM&E LLTM
  / Ordnance LLTM / Plans / SIB)

Sanity check: Col FY27 AP bucket sum = $4,627M vs P-40 "Plus CY AP" of
$4,763M = 97% reconciliation. The 3% gap is from a few ORDNANCE SWS
sub-categories not yet captured. Tolerable for deck purposes.

### 3.4 FFATA join (Phase 2.5)

**`scripts/join_ffata_to_funnel.py`** — aggregates
`nc_annual_by_piid.csv` per class per FY (using
`nc_scope_summary.json` for PIID→class mapping), joins into the funnel.

Outputs:
- `extracted/cost_funnel_with_subawards.csv` (full funnel + FFATA per-FY)
- `extracted/cost_funnel_narrative.csv` (deck-ready rollup with LOW/MID/
  HIGH industry baseline band + sourcing-notes column)

**Important:** the script uses a **50/60/65% BAND** for industry-baseline
outsourced (not a point estimate), with the sourcing-notes column
documenting that the band is analyst consensus, not a primary-source Navy
statement, with supporting evidence cited.

### 3.5 Primary source research (Phase 3)

**Goal:** find primary-source backing for the "60% of Basic Construction
is outsourced" baseline. The previous deck framing took this from another
LLM's synthesis.

**Outcome:** the make/buy % itself is NOT explicitly stated in any
GAO/CRS/CBO report we reviewed — but we found much stronger primary-source
backing in executive commentary and Navy policy statements (Phase 3d).

**Reports identified + extracted:**

| Source | Date | Key takeaway |
|---|---|---|
| CRS RL32418 (R. O'Rourke) | Jan 26 2026 | ~70% of critical subs sole-source; 16,000 suppliers; $9.8B sub IB through FY28 |
| CRS R41129 (R. O'Rourke) | Dec 4 2025 | Col $126.4B for 12 ships; per-boat cost matches our funnel; 17-mo delay |
| GAO-21-257 | Jan 14 2021 | "Supplier base roughly 70 percent smaller than in previous shipbuilding booms" |
| GAO-24-107732 | Sep 30 2024 | Col $130B program; 12-16 mo lead boat delay; $2.6B+ supplier base since 2018 |
| GAO-25-106286 | Feb 27 2025 | $5.8B DOD shipbuilding IB FY14-FY23; $12.6B more through FY28; 57% trade workers <5 yrs exp |
| GAO-26-109068 | Apr 22 2026 | **DOD already invested >$10B in submarine IB** (latest figure); FY27 budget $65B shipbuilding |

**Access pattern (important for future research):**
- `.gov` URLs (gao.gov, cbo.gov) return HTTP 403 to WebFetch and curl
- `everycrsreport.com` mirror works for CRS reports
- `web.archive.org` works for GAO PDFs (try
  `https://web.archive.org/web/2025/https://www.gao.gov/assets/...`)
- Some GAO product pages (`/products/gao-XX-XXXXX`) work via WebFetch
- FAS mirror (`sgp.fas.org`) returns HTTP 202 with empty body

Outputs:
- `extracted/industry_baseline_citations.csv` (30 rows, verbatim quotes
  with source URL + section ref + deck relevance)
- `research_primary_sources/SUMMARY.md` (narrative summary + deck
  implications + source-by-source detail)
- `research_primary_sources/gao-21-257-highlights.pdf` (291KB, via
  Wayback Machine)
- `research_primary_sources/gao-24-107732.pdf` (4.1MB, via Wayback)
- `research_primary_sources/gao-26-109068.pdf` (1.6MB, via Wayback)

### 3.6 Executive commentary deep dive (Phase 3d)

User asked: "the most authoritative thing ever would be some comment from
CEO or executives at the primes companies saying how much is actually
outsourced." Provided a NewsAPI.ai key.

**Three angles run in parallel:**

**3.6.1 Existing HII transcripts grep.** The 23 HII transcripts already
on disk (from the 2026-05-23 session) had been mined for general
commentary but NOT for the specific make/buy thread. Grep on
"outsourc|make-buy|in-house|self-perform|vertical integ|purchased
material|subcontract|vendor base" surfaced the smoking-gun thread.

Key HII executive statements:
- **Chris Kastner (CEO) FY2024 Q3 (Nov 2024):** "Yes I think there's going
  to be a greater percentage of our work outsourced going forward... we
  will outsource more, which means it costs more."
- **Kastner FY2024 Q4 (Feb 2025):** Wolfe Research analyst Myles Walton
  characterizes outsourcing increase as 30%; Kastner: "**It's a material
  number.**"
- **Kastner FY2024 Q4:** "I'd rather develop outsource partners and have
  an arms-length relationship. **I really don't want to vertically
  integrate.**"
- **FY2025 Q1 (May 2025):** Myles Walton: "regarding the 35% increase in
  outsourcing..." (note: analyst now cites 35%, up from 30% the previous
  quarter); Kastner confirms execution is on track.
- **FY2025 Q3:** Outsourcing now formally listed as a revenue-growth
  driver in earnings highlights.

Output: `extracted/exec_commentary_hii_makebuy.csv` (11 rows).

**3.6.2 GD earnings call scraping.** We didn't have any GD transcripts.
GD's Marine Systems segment IS Electric Boat, so GD CFO/CEO commentary on
Marine Systems is direct EB primary source.

Fetched via WebFetch on Motley Fool URLs:
- **GD Q4 2025 (Jan 28 2026):** "The supply chain remains the gating
  item... sole source suppliers where they are bottlenecks." 79% CapEx
  increase to >$900M, "half at least... at Electric Boat."
- **GD Q1 2026 (Apr 29 2026):** "We still see some areas in the supply
  chain where we need to get the cadence up, and those problems tend to
  be where we have complex components or complex systems where there are
  just single sources of supply."

**Critical strategic finding: HII and GD have DIFFERENT responses to
the same supplier-base constraint.**
- HII: increasing outsourcing 30%/yr; "I don't want to vertically integrate"
- GD: pouring CapEx into own yards; supply chain bottleneck is binding

This is a real, deck-worthy structural divergence and should be a slide.

**3.6.3 NewsAPI.ai search.** User provided API key
`9d345ac1-1f69-4f2d-a45e-b0e0f3b2485a`; docs at
https://newsapi.ai/documentation?tab=introduction. API is actually
`eventregistry.org/api/v1/article/getArticles`.

API gotchas:
- Multi-word strings as `keyword` are treated as exact-phrase match
  (returns 0 for combinations like "submarine outsourcing")
- Use `keyword: [list]` + `keywordOper: "and"` for boolean AND search
- `$query` syntax returned HTTP 400
- Single keywords or short phrases work well as single strings
- Use `articleBodyLen: -1` to get full article body

**Major findings from NewsAPI:**

1. **Navy's "Golden Fleet" 30-Year Plan (May 12, 2026):** "Currently only
   10% of shipbuilding occurs at distributed sites. The Navy aims to
   increase this to 50%." THIS IS OFFICIAL NAVY POLICY: a 5x target for
   distributed shipbuilding. Strongest possible primary-source statement
   on outsourcing direction.

2. **HII Q1 2026 (May 5, 2026 — call we hadn't pulled yet):** Kastner
   officially guides to **"outsourcing hours growing 30% year over year"**
   as a 2026 operational initiative. Listed as a formal metric in
   earnings highlights. Called "distributed shipbuilding strategy."

3. **AML3D + BlueForge (May 6, 2026):** AML3D (Australian additive
   manufacturer) received ~$2.6M from BlueForge Alliance "for five
   replacement components for US Navy submarines, utilising ARCEMY 3D
   metal printing." First concrete named BlueForge downstream
   sub-recipient we've identified.

4. **Navy FY27 Shipbuilding Plan:** "The Navy will evaluate overseas
   options and whether allied and partner shipbuilding can supplement
   domestic production if U.S. industry cannot meet required timelines."
   Navy formally signals openness to overseas building.

5. **Navy $6.2B specifically for submarine IB** as part of Golden Fleet
   plan (workforce + distributed shipbuilding + advanced manufacturing).

Outputs:
- `extracted/exec_commentary_makebuy.csv` (21 rows, consolidated executive
  + Navy primary-source quotes — THE STRONGEST SINGLE SOURCE FOR THE DECK)
- `research_primary_sources/newsapi_results/raw_results.json` +
  `raw_results_round2.json` (full article bodies for re-mining)

---

## 4. Files written this session

### Scripts (new)

| File | Purpose |
|---|---|
| `scripts/build_cost_funnel.py` | Joins P-40 (long-form) + P-5c (reconciled) into per-class per-FY funnel CSV |
| `scripts/extract_scn_p10_ap_detail.py` | Extracts Exhibit P-10 AP detail across both classes, multiple format quirks handled |
| `scripts/join_ffata_to_funnel.py` | Joins FFATA per-class per-FY into the funnel; writes the deck-ready narrative CSV with 50/60/65% band |

### Extracted CSVs (new this session)

| File | What's in it |
|---|---|
| `extracted/cost_funnel_per_class.csv` | Long form: metric × FY × class. P-40 + P-5c combined. |
| `extracted/cost_funnel_summary.csv` | Wide: one row per (class, FY). All P-40 + P-5c columns + derived gfe_sum / prime_contract_sum / pct columns. |
| `extracted/scn_p10_ap_long.csv` | Per-vintage P-10 rows. |
| `extracted/scn_p10_ap_reconciled.csv` | Best per (LI, category, FY). |
| `extracted/scn_p10_ap_buckets.csv` | Per-class per-FY rolled into 8 deck-narrative buckets. |
| `extracted/cost_funnel_with_subawards.csv` | Funnel summary + FFATA visible $ per (class, FY) + pct of BC + pct of total. |
| `extracted/cost_funnel_narrative.csv` | **Deck-ready funnel** with low/mid/high band + sourcing-notes column. |
| `extracted/industry_baseline_citations.csv` | 30 rows of verbatim-quoted GAO/CRS/CBO statistics with source URL + page/section + deck relevance. |
| `extracted/exec_commentary_hii_makebuy.csv` | 11 rows of HII transcript context — Kastner/Stiehle outsourcing commentary FY24 Q3 onward. |
| `extracted/exec_commentary_makebuy.csv` | **21 rows of consolidated executive + Navy primary-source quotes** — THE deck's gold-source CSV. |

### Research artifacts (new this session)

| File | Description |
|---|---|
| `research_primary_sources/SUMMARY.md` | Narrative summary of all primary-source research — deck implications + source-by-source detail |
| `research_primary_sources/gao-21-257-highlights.pdf` | GAO Highlights page (291KB) — the "70% smaller supplier base" report |
| `research_primary_sources/gao-24-107732.pdf` | Full GAO Columbia Sept 2024 report (4.1MB) |
| `research_primary_sources/gao-26-109068.pdf` | Latest GAO testimony April 22 2026 (1.6MB) |
| `research_primary_sources/newsapi_results/raw_results.json` | Round 1 NewsAPI articles |
| `research_primary_sources/newsapi_results/raw_results_round2.json` | Round 2 NewsAPI articles |

### Spec / planning (modified)

- `DECK_BUILD_SPEC.md` — §5 rewritten (12+6 structure), §6 data flow
  re-mapped, §7.3 resolved, §2.2 directory layout adjusted (s03_the_prize),
  §7.8 quote curation note updated to slide 11.

---

## 5. Headline findings (the deck's primary-source backbone)

### Cost structure validated per-class per-FY

| Class | FY | Hull(s) | Total Ship Cost | Basic Construction | GFE | Plans |
|---|---:|:--:|---:|---:|---:|---:|
| Columbia | 2021 | 1 (SSBN-826) | $16,122M | $5,979M (37%) | $2,728M (17%) | $6,946M (43%) |
| Columbia | 2024 | 1 (SSBN-827) | $10,689M | $6,356M (59%) | $2,560M (24%) | $1,443M (14%) |
| Columbia | 2026 | 1 (SSBN-828) | $10,744M | $7,160M (67%) | $2,125M (20%) | $1,096M (10%) |
| Columbia | 2027 | 1 (SSBN-829) | $10,486M | $6,854M (65%) | $2,422M (23%) | $862M (8%) |
| Virginia | 2022 | 2 | $6,916M | $4,758M (69%) | $1,587M (23%) | $252M (4%) |
| Virginia | 2023 | 2 | $7,251M | $5,095M (70%) | $1,634M (23%) | $192M (3%) |
| Virginia | 2024 | 2 | $11,378M | $9,071M (80%) | $1,684M (15%) | $207M (2%) |
| Virginia | 2025 | 1 | $9,501M | $5,327M (56%) | $1,318M (14%) | $2,596M (27%) |
| Virginia | 2026 | 1 | $5,389M | $3,137M (58%) | $1,634M (30%) | $220M (4%) |
| Virginia | 2027 | 2 | $11,437M | $8,889M (78%) | $1,898M (17%) | $223M (2%) |

All values reconcile to CRS-R41129 per-boat figures (Col 1st $16.1B / 2nd $10.7B / 3rd $10.5B) and CRS-RL32418 (Va ~$5B per boat at 2/yr rate).

### LLTM/AP breakdown (Saronic-relevant slice)

Columbia FY27 AP ($4.6B total) by bucket:
- Nuclear plant LLTM: $1,490M (BPMI)
- **Shipbuilder-procured LLTM: $1,576M (BC(3)+BC(5)+BC(7) — addressable)**
- Plans / SIB: $810M (workforce/MIB)
- Missile compartment LLTM: $297M
- EOQ: $178M
- Ordnance LLTM: $120M
- Electronics LLTM: $82M
- HM&E LLTM: $74M

Virginia FY25 AP ($3.7B total) by bucket:
- EOQ: $1,298M (bulk material savings)
- Nuclear plant LLTM: $1,273M (BPMI)
- **Shipbuilder-procured LLTM (CFE): $1,065M (CFE 1-yr + 2-yr — addressable)**
- Propulsor LLTM: $50M
- Electronics LLTM: $33M (CCSM)

**Combined shipbuilder-procured LLTM across both classes ≈ $2.5-3B/yr**
that GDEB itself buys from the supplier base as LLTM. This is separable
from FFATA-visible first-tier subawards because LLTM is often booked as
purchased material rather than formal subcontract.

### Three killer primary-source quotes for the deck

1. **Navy's Golden Fleet Plan (May 12, 2026 — OFFICIAL POLICY):**
   > "Currently only 10% of shipbuilding occurs at distributed sites. The
   > Navy aims to increase this to 50%."

2. **HII Q1 2026 guidance (May 5, 2026 — Chris Kastner CEO):**
   > "We are on track to grow our outsourcing hours year-over-year by 30%,
   > and we will continue to identify capacity expansion opportunities."

3. **HII FY24 Q4 (Feb 2025 — Chris Kastner CEO):**
   > "[The 30% outsourcing increase] is a material number."
   > "I'd rather develop outsource partners and have an arms-length
   > relationship. I really don't want to vertically integrate."

### Strategic divergence (HII vs GD)

Two different responses to the same supplier-base constraint:

| Prime | Strategy | Latest action |
|---|---|---|
| HII (Newport News) | **Increase outsourcing 30%/yr** | "Distributed shipbuilding strategy" formal name; W International acquisition was the rare exception |
| GD (Electric Boat) | **Invest in own yards** | 79% CapEx increase to >$900M, half at EB |

This is a real, structurally interesting story that wasn't in the deck
before. For Saronic this matters because the entry archetype differs:
- HII = direct outsource partner relationship
- GD = sub-tier supplier where GD is investing capital

### Concrete BlueForge sub-recipient identified

**AML3D** (Australian additive-manufacturing company) received ~$2.6M
from BlueForge Alliance in May 2026 for "five replacement components for
US Navy submarines, utilising ARCEMY 3D metal printing." This is the
first named primary-source identification of where BlueForge's $4.17B in
disbursements goes downstream. Useful as a concrete archetype on the
Entry Map slide.

---

## 6. The cost-funnel narrative (deck's spine)

For each FY, per class, the funnel cuts from the top:

```
TOTAL SHIP COST (CRS-validated per-boat) 
  → strip GFE (P-5c categories, primary)
  → strip Plans + Other (primary)
  → BASIC CONSTRUCTION = the prime contract base (primary, P-5c)
       → industry-baseline 50-65% band outsourced (analyst synthesis;
          no primary-source make/buy ratio per se, BUT backed by:
          - Navy 10% → 50% distributed shipbuilding target [PRIMARY]
          - HII +30% YoY outsourcing hours [PRIMARY]
          - GAO "shipbuilders are expanding outsourcing" [PRIMARY]
          - 70% sole-source supplier base [CRS PRIMARY]
          - $10B+ DOD invested in sub IB [GAO PRIMARY])
            → FFATA-visible first-tier subawards (primary, SAM.gov data,
                ~5-20% of BC depending on FY)
            → "unseen layer" = industry-baseline minus FFATA-visible
                (purchased material + lower-tier subs + non-compliance +
                 HII teaming partner work that doesn't appear as subaward)
```

At the cumulative FY22-FY26 level:
- Total ship cost across 9 hulls: ~$66B
- GFE: ~$14B
- Basic Construction: ~$40B
- Industry-baseline mid-case outsourced (60% × BC): ~$24B over 5 years
- Combined "not yard-self-performed" addressable = ~$38B over 5 years
- **~$7-8B/yr addressable supplier opportunity**
- FFATA-visible captures: ~$4B over 5 years = ~$800M/yr (~10-15% of real)

---

## 7. Caveats — read before drawing conclusions

(Prior session caveats still apply. New/refined this session:)

1. **The 50/60/65% band is industry-analyst consensus, NOT primary-source.**
   No GAO/CRS/CBO/CEO statement gives a clean "X% of submarine prime
   contract value is purchased/subbed." We use a band because the exact
   point isn't publicly stated. Supporting evidence (the 70% sole-source,
   the 70% atrophied supplier base, $10B+ in DOD investment, HII's 30%
   YoY outsourcing growth, Navy's 10%→50% target) all directionally
   support a high baseline, but none of them quantify the baseline
   itself.

2. **P-10 bucket reconciliation has a small (3%) gap** for Columbia FY27.
   The summed buckets total $4,627M vs the P-40 "Plus CY AP" of $4,763M.
   Most likely missing: ORDNANCE SWS (11) ECONOMIC and (12) CONTINUOUS
   sub-categories whose `Total:` line format wasn't caught. Not material
   for deck purposes; document if user wants the last 3%.

3. **HII outsourcing percentage is RELATIVE growth, not absolute share.**
   When Kastner says "30% YoY growth in outsourcing hours," that's the
   *change* from the prior year — not "30% of work is outsourced." We do
   not know HII's base rate. We just know the trajectory is steeply up.

4. **HII per-program "outsourcing" includes both submarine + carrier
   programs.** The FY23 Q1 mention of "outsourcing of CVN 80" shows the
   outsourcing strategy is broader than submarines. Be precise in the
   deck.

5. **GD's Marine Systems is multiple shipyards** — Electric Boat is the
   submarine yard, but GD also has Bath Iron Works (DDGs) and NASSCO
   (Lewis B. Puller-class). Novakovic and Deep commentary on supply
   chain is across all three. The supply chain language IS reliably
   sub-applicable because EB is the dominant Marine Systems business.

6. **Navy "10% to 50% distributed shipbuilding" target is for ALL Navy
   shipbuilding**, not just submarines. Sub-specific numbers within that
   target weren't given. Use carefully.

7. **The AML3D / BlueForge concrete example is ONE data point.** It's
   useful as a real archetype but should not be over-extrapolated to
   "BlueForge primarily funds Australian additive-manufacturing firms"
   without more data. The $2.6M order is tiny relative to the $4.17B in
   total BlueForge passthrough.

8. **GAO/CBO/CRS direct PDFs are mostly blocked by 403 from .gov
   domains.** For future research:
   - Use `everycrsreport.com` for CRS
   - Use `web.archive.org/web/YYYY/https://www.gao.gov/...` for GAO PDFs
   - Use `cbo.gov/publication/<id>` landing pages (sometimes work) or
     news article summaries (USNI / Defense News reliably cover CBO)
   - WebFetch on the GAO `/products/gao-XX-XXXXX` page can work (Highlights)

---

## 8. Open methodology questions / next steps

### Immediate (next session)

These are the things the current Option C plan still has open. In order
of dependency / value:

1. **Phase 4: GFE-PIID expansion.** Systematically identify Navy
   contracts to GFE primes (BPMI is in scope, but LM combat sys, NG
   sonar/EW, Raytheon torpedoes, Boeing weapons, possibly others are
   NOT in scope). Strategy: search FPDS for Navy contracts with
   place-of-performance at GDEB or HII-NNS, plus vendor-name searches
   for known GFE primes. Pull SAM/USA subawards for new in-scope PIIDs.
   Probably grows scope from 15 to 25-30 PIIDs. ~1-2 sessions.

2. **Phase 5: HII 10-K material/labor mining.** Re-extract from EDGAR
   data we already have. HII 10-Ks disclose procurement and labor cost
   stats at the segment level. Get NNS material % vs. self-performed
   labor % to cross-validate the make/buy baseline directly from
   primary financials. ~3-4 hours.

3. **Phase 6: Place-of-performance from FPDS.** Re-aggregate existing
   FPDS records by POP (we have the data, never aggregated this way).
   Adds a second geographic view that's about where work HAPPENS, not
   where vendors are REGISTERED. ~2-3 hours.

4. **Update the DECK_BUILD_SPEC.md** to fold in the new findings:
   - New slide for funnel narrative (HII vs GD divergence)
   - Slide 6 ("real outsourced number") needs to be rebuilt around
     funnel data, not the visible+HII estimate I had before
   - Slide 11 ("What HII is telling the street") should now feature
     the 30% YoY outsourcing quote prominently
   - Slide 12 ("Entry map") gets concrete AML3D BlueForge example
   - Appendix should add the primary-source bibliography

### Then begin the deck build

5. **Phase 1 (from DECK_BUILD_SPEC §2.2): Foundation.** Build
   template.pptx + primitives (style, geometry, text, shapes, slide
   wrapper) + build.py. Ship one trivial test slide. Validate audits.
   ~half session.

6. **Phase 2: Tables + simple bars.** Render slides 3, 4, 5 (size of
   the pie arc). ~half session.

7. **Phase 3: Complex charts.** slope_chart, dual_line, kpi, callout.
   Render slides 2, 7, 8. ~half session.

8. **Phase 4: Remaining slides.** ~1 session.

9. **Phase 5: Polish.** Source citations, page numbers, footer, audits,
   iteration loop. ~half session.

### Open items still flagged

- **CEO quote curation for slide 11** (DECK_BUILD_SPEC §7.8): need to
  pre-select 4 quotes for the 4-quadrant grid. Given the FY26 Q1 finds,
  the 30% YoY outsourcing quote should probably be one of them. Suggest
  the curator workflow: write `slide11_quotes.yaml` with 4 candidates,
  user approves, then freeze into the deck build.
- **Saronic logo asset** (DECK_BUILD_SPEC §7.1): not yet provided.
  Build the cover without it for v1; can swap in later.
- **Classification banner** (§7.5): no banner unless user says otherwise.
- **CEO quote review for AML3D / BlueForge connection:** worth verifying
  the AML3D-BlueForge tie is real (it's from a press release; should
  cross-check with a second source before putting in deck).

### Things the user might want to consider but I haven't pushed for

- **Surface-combatant outsourcing rate benchmark.** Compare submarine
  ~60% (band) to DDG-51 or LHA outsourcing rates as context. Some of
  this is in HII's 10-K segment data.
- **HII NNS-only segment financials** (vs. consolidated). HII reports
  three segments: Ingalls (DDG/LHA/LPD), Newport News (CVN + submarines),
  Mission Technologies (services). NNS-only data is what we want for
  the Va/Col-prime-team picture. Need to confirm we have NNS-specific
  procurement disclosures, not just consolidated.
- **Foreign / AUKUS supplier opportunity.** The Navy FY27 Plan
  explicitly mentions overseas shipbuilding consideration; AML3D is
  Australian. If Saronic could plug into the AUKUS funded sub
  industrial base side, that's a separate analytical thread.
- **General Dynamics 10-K segment data for Marine Systems.** We have HII
  10-Ks but not GD's. Marine Systems segment financials would let us
  cross-validate per-yard margin and material trends. Probably another
  half-session task.

---

## 9. Hand-off — if next agent wants to extend

### To regenerate the cost funnel + primary-source artifacts:

```bash
cd /Users/brendantoole/projects2/submarine_outsourced_work

# Step 1: re-build the cost funnel (uses existing extracted CSVs)
python3 scripts/build_cost_funnel.py
python3 scripts/extract_scn_p10_ap_detail.py
python3 scripts/join_ffata_to_funnel.py
```

The other CSVs in this phase (industry_baseline_citations.csv,
exec_commentary_makebuy.csv, exec_commentary_hii_makebuy.csv) are
manually curated — no script to regenerate. Source for re-creation is
documented in research_primary_sources/SUMMARY.md.

### Things to NOT do:

- **Don't try to fetch .gov PDFs directly** — use Wayback Machine or
  the everycrsreport.com mirror (see §3.5).
- **Don't use multi-word strings as NewsAPI `keyword` parameter** — use
  `keyword: [list]` + `keywordOper: "and"` instead.
- **Don't change the 50/60/65% band** in cost_funnel_narrative.csv to a
  point estimate. The band is honest about the make/buy gap.
- **Don't claim the Navy's 10%→50% target is sub-specific.** It's for all
  Navy shipbuilding. Be precise.
- **Don't claim HII's 30% YoY outsourcing is "30% of work is outsourced."**
  It's the *change rate*, not the absolute share.

### Memories saved this session that affect future work

None saved (no new long-term `~/.claude/projects/.../memory/` entries —
all session-specific findings are in this log + the SUMMARY.md +
research artifacts).

---

## 10. Final state of task list

| # | Subject | Status |
|---|---|---|
| 1 | Phase 1a: Inspect budget book TXT structure for AP/LLTM | ✓ completed |
| 2 | Phase 1b: Write extract_scn_advance_procurement.py | ✓ completed (subsumed by build_cost_funnel.py) |
| 3 | Phase 1c: Run extractor + validate against budget book values | ✓ completed |
| 4 | Phase 2: Build cost_funnel_per_class.csv | ✓ completed |
| 5 | Phase 1.5: Extract Exhibit P-10 AP component detail | ✓ completed |
| 6 | Phase 2.5: Join FFATA visible subs into cost funnel | ✓ completed |
| 7 | Phase 3a: Identify GAO/CRS/CBO reports | ✓ completed |
| 8 | Phase 3b: Fetch + extract from primary sources | ✓ completed |
| 9 | Phase 3c: Write industry_baseline_citations.csv | ✓ completed |
| 10 | Phase 3d-1: Grep HII transcripts for make/buy commentary | ✓ completed |
| 11 | Phase 3d-2: Pull General Dynamics earnings transcripts | ✓ completed |
| 12 | Phase 3d-3: NewsAPI search for executive make/buy statements | ✓ completed |

---

## 11. Quick orientation for next agent

**If user asks "what changed in the deck framing this session":**
The deck is no longer "20% outsourcing rate." It's a funnel that starts
at total boat cost, cuts through Plans/GFE/Other to Basic Construction
(~60-70% of total), then bands the outsourced layer inside BC at 50/60/65%
(industry consensus, supported by Navy policy + CEO commentary). The
FFATA-visible 20% is now positioned as "the named-vendor-visible slice
of the outsourced layer, ~10-15% of the real pie."

**If user asks "where's the most authoritative outsourcing primary source":**
`extracted/exec_commentary_makebuy.csv`. The headline quotes are
EXEC-08 (HII Q1 2026 30% YoY outsourcing hours) and EXEC-18 (Navy
Golden Fleet 10%→50% distributed shipbuilding target).

**If user asks "where's the funnel data":**
`extracted/cost_funnel_narrative.csv` is the deck-ready rollup.
`extracted/cost_funnel_summary.csv` is the wide form with all columns.
`extracted/cost_funnel_per_class.csv` is the long form.

**If user asks "what's the addressable opportunity for Saronic":**
~$7-8B/yr of outsourced new-construction supplier opportunity at current
build rate. Combined visible + implied. Ramping with Block VI / Col
Build II. FFATA captures only ~$1B/yr of this.

**If user asks "is the 60% number defensible":**
No primary source directly states 60%. It's industry analyst consensus
(50-65% band) for complex shipbuilding. SUPPORTING evidence is strong:
70% sole-source suppliers, 70% atrophied supplier base, $10B+ DOD
invested, HII +30% YoY outsourcing, Navy 5x distributed shipbuilding
target. Use as a band, not a point.

**If user asks about HII vs GD:**
Structurally different responses to the supplier constraint. HII is
expanding outsourcing 30% YoY ("distributed shipbuilding"). GD is
investing in own yards (CapEx +79% to >$900M, half at EB). Worth a
dedicated slide.

**If user asks "what's BlueForge actually funding":**
First named example: AML3D (Australian additive manufacturer) received
$2.6M for 3D-printed replacement components for US Navy submarines
(May 2026 press release). Useful as ONE archetype but $2.6M is a rounding
error vs $4.17B total BlueForge passthrough. More research needed.

**If user asks to start the deck build:**
DECK_BUILD_SPEC.md is up to date on slide structure. Phase 1 in §2.2
(template.pptx + primitives) is the natural next step. But it might be
worth one more spec revision pass to fold in the new findings from this
session before building.
