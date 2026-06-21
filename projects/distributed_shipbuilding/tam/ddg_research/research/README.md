# Destroyer Outsourced Work -- Data Gathering

**Goal:** Identify how much money (work) is outsourced **per year** by the "primes"
building U.S. destroyers.

**Status:** Initial data gathering effort. Created 2026-05-23. DoD daily contract
announcement POP pipeline added 2026-05-24 (see `DOD_ANNOUNCEMENT_HOWTO.md`).

Companion to `submarine_outsourced_work/` — same methodology, different ship class.
The submarine project's `SAM_GOV_HOWTO.md` and `reference_prior_analysis/` are reused
verbatim (linked in here). The DoD-announcement scripts (5 of them at
`scripts/{pull_dod_announcements_pop,fetch_wayback_batch,ingest_wayback_bulletins,classify_dod_action_worktype,reclassify_dod_action_subrelevance}.py`)
parallel the submarine project's versions with destroyer-specific filters and
buckets (BIW + Ingalls instead of EB + HII). The cache directories are
**symlinked** to the submarine project so 305 globalsecurity HTMLs +
367 Wayback HTMLs are reused without re-fetching.

**Headline (corrected 2026-05-28 — read `METHODOLOGY.md` §2a before citing any outsourcing number):**

The defensible measure is the **cost funnel**: roughly **~78% of DDG-51 total ship
cost is outsourced** — the GFE layer (Aegis, SPY-6, LM2500, VLS, guns) plus the
yard-side materials/subcontract layer. The FFATA-visible first-tier subaward stream
is only the **~15% floor** of the yard-side piece (~$0.29B/yr visible vs ~$1.8B/yr
modeled yard-side; see `extracted/outsourcing_assumptions.md` and the funnel CSV).

For the **geographic lens** (where work is physically performed), the DoD-announcement
place-of-performance measure is **~33% outside the two yards** once the redacted
FY23-27 MYP master awards (~$14.58B across BIW + Ingalls) are folded back in.

> ⚠️ **Do NOT headline the older "~87% outside-yards" figure.** It is computed on the
> *disclosed-only* DoD-announcement corpus with the MYP master dollars redacted out, so
> it is a **redaction artifact** biased toward suppliers (it over-weights GFE, which is
> inherently ~100% supplier-performed, because the big in-yard MYP masters dropped out).
> The disclosed-corpus numbers (152 actions / $7.13B / 11.2% BIW / 1.3% Ingalls /
> 73.6% Other-US / 0% Foreign) are valid only as "disclosed-corpus POP," not as the
> program outsourcing rate. See `wiki_ddg/12-myp-redaction-and-unseen-layer.md` and
> `DOD_ANNOUNCEMENT_HOWTO.md` §12.

---

## Who the "primes" are

Unlike submarines (single contractually-prime yard, GDEB), U.S. destroyers are built
under a **two-yard competitive procurement** with each ship awarded individually to
either yard. Both yards are prime of record on their hulls — no umbrella teaming.

| Prime | Role | Location |
|---|---|---|
| **HII Ingalls Shipbuilding (HII-Ingalls)** | One of two yards building DDG-51 Arleigh Burke class. Subsidiary of Huntington Ingalls Industries — DISTINCT from HII Newport News Shipbuilding (which builds CVN + submarines). | Pascagoula, MS |
| **General Dynamics Bath Iron Works (GDBIW / BIW)** | The other DDG-51 yard. Design Agent for DDG-51 (per SCN P-40). | Bath, ME |

**Out of scope:** DDG-1000 (Zumwalt class, LI 2119) — only 3 ships, all delivered;
remaining work flows through OPN (CPS install on DDG 1002), not SCN.

Both yards receive ships under the same multi-year procurement (MYP) umbrella but each
has its own per-ship FPDS prime contract. There is NO submarine-style sub-of-sub
teaming pattern — what you see in FPDS is what was contracted.

**Key DDG GFE / sub vendors (per FY27 SCN LI 2122 contract data tables):**

| Vendor | What | Cost Category |
|---|---|---|
| **Lockheed Martin** | Aegis Combat System (AWS), Aegis Baseline, fire control electronics, Mk 41 VLS canisters | Electronics |
| **Raytheon (RTX)** | AN/SPY-6(V)1 AMDR radar, SPY-6 X-band, fire control transmitter, missile launchers, MK 38 GWS | Electronics + Ordnance |
| **BAE Systems** | Mk 45 5-inch gun, GFM (gun fire control), various smaller mounts | Ordnance |
| **L3 Technologies / L3Harris** | USG-2B CEC hardware, electronics suite | Electronics |
| **DRS Systems / DRS Laurel Technologies** (Leonardo DRS) | Combat system components, IFC (Information & Fire Control) | Electronics |
| **General Electric (GE Aerospace)** | LM2500 gas turbine engines (4 per ship) | Propulsion |
| **Rolls-Royce** | Some LM2500-class engine components; gas turbine accessories | Propulsion |
| **Northrop Grumman** | AN/SPQ-9B X-band radar (FY19+), navigation, mission systems | Electronics |
| **General Dynamics (separate from BIW)** | AWS Director/Director Controller (per FY27 P-5b page) | Electronics |
| **NSWC Pt Hueneme** | Combat systems engineering / integration support (work request, not prime) | Plan Costs |

---

## What "outsourced" means in this context

The DDG prime (HII-Ingalls or GDBIW) does NOT manufacture most of the ship in-house.
The outsourced flows are:

1. **First-tier subcontracts** — the prime hires a vendor for HM&E components, hull
   steel, piping, fittings, etc. Reported via FFATA / SAM.gov Acquisition Subaward
   Reporting + USAspending `/api/v2/subawards/` against the prime PIID.

2. **Government-furnished equipment (GFE)** — the Navy contracts the major mission
   systems directly and ships them to the yard for installation:
   - Aegis Combat System suite (Lockheed Martin prime)
   - SPY-6 AMDR radar (Raytheon prime)
   - LM2500 gas turbines (GE Aerospace prime)
   - Mk 45 gun (BAE prime)
   - VLS launcher cells (Lockheed Martin / BAE prime)
   - Standard Missiles SM-2/3/6, ESSM, Tomahawk (Raytheon prime — funded under WPN, not SCN)
   - CIWS Phalanx (Raytheon prime)
   These appear as separate FPDS prime contracts but the dollars are outsourced from
   the perspective of "destroyer production" — they show up in the SCN P-5b/P-5c
   Electronics / Propulsion / Ordnance / HM&E cost categories.

3. **Plans cost / lead-yard support / design** — engineering services performed by
   the prime (BIW as Design Agent) plus FFRDCs and shipyard infrastructure support.

4. **Maritime Industrial Base (MIB) / mandatory funding** — starting FY26, the
   destroyer budget line carries large "mandatory funds" for industrial-base
   productivity ($5,400,000 thousand in FY26 estimate, $314,000 thousand in FY27).
   This flows through the prime to suppliers (similar to MIB on submarines but
   smaller scale).

The "annual outsourced work" we want is the sum of:
- Window-period subaward obligations on DDG primes (first-tier visible subs)
- Window-period prime obligations to GFE vendors tied to DDG line
- MIB-equivalent supplier-development spend

Caveats (carry-overs from submarine project):
- Subaward reporting incomplete (FFATA $30K threshold + non-compliance)
- USAspending `/api/v2/subawards/` caps at ~2,500 records per prime — SAM.gov
  recovers the long tail
- Federal naval-shipyard work (Norfolk, Portsmouth, Pearl Harbor, Puget Sound) is
  federal payroll, NOT outsourced
- Cumulative `totalObligatedAmount` from FPDS ≠ window-period spend; per-mod delta
  analysis is required

**Two-yard wrinkle (DDG-specific):**
Because both HII-Ingalls and GDBIW are prime of record on their own ships, the
"annual outsourcing" rollup has TWO prime aggregation buckets, not one. They should
be analyzed in parallel — direct comparison of in-house vs outsourced ratios is the
interesting analytical question (does one yard outsource more than the other?).

---

## Folder structure

```
destroyer_outsourced_work/
├── README.md                          (this file)
├── SAM_GOV_HOWTO.md                   (copy of submarine project's guide)
├── .env                                (SAM API key; same as submarine project)
├── budget_books/                       (SYMLINK to submarine_outsourced_work/budget_books)
│   ├── SCN_Book_FY27.pdf
│   ├── SCN_Book_FY27.txt
│   ├── SCN_Book_FY22-FY26.{pdf,txt}
│   └── 30_Year_Shipbuilding_Plan.{pdf,txt}
├── reference_prior_analysis/          (SYMLINK to submarine project's references)
├── scripts/                           (Python pull + parse scripts)
├── extracted/                         (parsed CSVs)
├── fpds_raw/                          (raw FPDS Atom JSON dumps by query)
├── usaspending_subawards/             (USAspending subaward JSON pulls per PIID)
├── sam_subawards/                     (SAM.gov subaward JSON pulls per PIID)
├── sam_entity_lookups/                (SAM Entity Management cache, by UEI)
├── edgar_research/                    (HII + GD 10-K extracts for segment disclosure)
├── hii_earnings_transcripts/          (HII earnings call transcripts)
├── gd_earnings_transcripts/           (GD earnings call transcripts)
├── logs/                              (per-session markdown logs)
└── pull_logs/                         (background-process stdout: FPDS / SAM / USAspending / NAICS / transcript scrapers)
```

---

## Pull plan

### Sources (same as submarine project)

1. **FY27 SCN Book — LI 2122 DDG-51 (P-1 Lines 13 main + 14 AP)** —
   P-5/P-5a/P-5b/P-5c/P-21/P-27 exhibits with named contractor references and
   cost-category breakdowns.

2. **30-Year Shipbuilding Plan (PB27)** — DDG-51 production ramp through FY56;
   DDG(X) future destroyer in design phase (not in scope here).

3. **FPDS Atom Feed** — vendor-name pulls for HII-Ingalls, GDBIW, LM (Aegis/VLS),
   Raytheon (SPY-6/missiles), GE (LM2500), Rolls-Royce, BAE (Mk 45/VLS), L3Harris,
   Northrop Grumman, plus DDG description sweeps. Date window: FY18 signed (catches
   FY18-22 MYP master + FY23-27 MYP master).

4. **USAspending `/api/v2/subawards/`** — subaward tree per major DDG prime PIID
   (discovered from FPDS).

5. **SAM.gov Acquisition Subaward Reporting** — per the howto, recovers the long
   tail that USAspending truncates.

### Known DDG contract structure (to be confirmed against FPDS)

| Contract structure | Notes |
|---|---|
| FY18-22 MYP (10 ships + options) | Awarded Sep 2018. Two separate prime contracts — one to HII-Ingalls, one to GDBIW. Per FY27 P-40: DDG 130, 131, 132, 133, 134, 136, 137, 138, 139 awarded Sep/Dec 2018. |
| FY23-27 MYP (9 ships + options) | Awarded Aug 2023. Two separate prime contracts. DDG 140-147, 149, 150 awarded Aug 2023. |
| Annual option exercises | DDG 148 (FY25-3 Option) awarded Jul 2025. |
| Pre-MYP individual ships | DDG 126 (Jun 2013), DDG 127 (Sep 2017), DDG 135 (Jun 2020), etc. |

Seed PIID lookup is via FPDS vendor-name searches → identify the master MYP PIIDs.
The destroyer project does NOT have a pre-seeded PIID list (unlike submarines, which
inherited 17 PIIDs from prior analysis). The first step is FPDS discovery.

### Process

1. **Extract** — Parse LI 2122 (DDG-51) from SCN_Book_FY27.txt into CSVs. Capture
   P-40 Resource Summary, P-5c Ship Cost Analysis (cost categories per ship hull),
   P-27 Production Schedule (ship × shipbuilder × FY).

2. **FPDS pull** — Vendor-name + DDG-description searches. Save raw JSON per query
   to `fpds_raw/`. Discover DDG MYP master PIIDs from the results.

3. **Seed-PIID derivation** — From the FPDS pull, identify the top ~15-25 DDG
   prime PIIDs by `totalObligatedAmount`. These become the seeds for subaward pulls.

4. **Subaward pull** — For each seed PIID, pull USAspending (`/api/v2/subawards/`)
   and SAM.gov (`/contract/v1/subcontracts/search`) in parallel. Save raw to
   `usaspending_subawards/` and `sam_subawards/`.

5. **NAICS enrichment** — For top-N sub recipients by lifetime $, call SAM Entity
   Management API to get primary NAICS code. Save to `sam_entity_lookups/`.

6. **Manifest** — Write `MANIFEST.md` listing every file, its source query, and
   known caveats.

---

## Open methodology questions (flag for later)

- **Per-yard outsourcing ratio.** Does HII-Ingalls outsource a different fraction of
  the ship than GDBIW does? Comparing per-yard subaward $ / per-yard prime $ is the
  question of analytical interest.

- **GFE attribution.** When LM gets a multi-year Aegis prime, that's outsourced
  from the Navy POV but it's NOT outsourced from HII or BIW. Track GFE separately
  from yard-level subawards (same convention as submarine project).

- **Two-tier MYP structure.** Each MYP block is actually TWO prime contracts (one
  per yard). Need to bucket subaward pulls by yard correctly.

- **Cumulative vs. window dollars.** Same FPDS gotcha as submarines — must use
  per-mod `obligatedAmount` summed by signed_date FY, not the cumulative
  totalObligatedAmount.

- **HII Ingalls vs HII NNS in vendor name.** HII has two main yards. In FPDS,
  "HUNTINGTON INGALLS INCORPORATED" can refer to either. Need to disambiguate via
  contracting office + product description to separate destroyer work from
  carrier/sub work.

- **DDG(X)** — the future destroyer is in design phase under a separate RDTE line,
  not SCN. May appear as a small amount in FY26-27 SCN if any Advance Procurement
  is in scope. Out of scope unless it shows up in the FPDS sweeps.

---

## How to re-run (once scripts are written)

```bash
cd /Users/brendantoole/projects2/destroyer_outsourced_work

# 1. Extract DDG line items from SCN PDF (cheap)
python3 scripts/extract_scn_destroyer_lines.py

# 2. Pull FPDS (slow, 20-30 min)
python3 scripts/pull_fpds_ddg_primes.py

# 3. Discover PIIDs from FPDS, then pull subawards
python3 scripts/pull_usaspending_subawards.py --discover
python3 scripts/pull_sam_subawards.py --discover

# 4. NAICS enrichment (requires aggregate first)
python3 scripts/aggregate_new_construction.py
python3 scripts/pull_sam_entity_naics.py

# 5. Aggregate everything
python3 scripts/aggregate_annual_outsourcing.py
python3 scripts/aggregate_sam_subawards.py
```
