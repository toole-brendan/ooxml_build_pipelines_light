# Submarine Outsourced Work -- Data Gathering

**Goal:** Identify how much money (work) is outsourced **per year** by the "primes"
building U.S. submarines.

**Status:** Initial data gathering effort. Created 2026-05-21.

---

## Who the "primes" are

U.S. nuclear submarines are built under a long-standing two-yard teaming arrangement.
The contractual prime of record is almost always **General Dynamics Electric Boat**.

| Prime | Role | Location |
|---|---|---|
| **General Dynamics Electric Boat (GDEB)** | Prime of record on all Virginia + Columbia construction contracts. Lead yard for Columbia. | Groton, CT + Quonset Point, RI |
| **HII Newport News Shipbuilding (HII-NNS)** | Team partner. ~50/50 work split on Virginia, ~78/22 (GDEB lead) on Columbia. Does NOT appear as prime in FPDS for submarine construction. | Newport News, VA |
| **Bechtel Plant Machinery Inc. (BPMI)** | Naval reactor components (S9G reactor for Virginia, generation-after for Columbia). NAVSEA 08 / Naval Reactors customer. | Monroeville, PA + Schenectady, NY |
| **Lockheed Martin** | Virginia combat systems hardware/software; Columbia common missile compartment integration; Trident D5 / D5LE2 missile (for Columbia SSBN). | Multiple |
| **Northrop Grumman** | AN/BLQ-10 EW; sonar arrays; combat systems work that appears as sub on GDEB primes. | Multiple |

The team build pattern means HII-NNS's submarine work flows **through** GDEB contracts
and shows up either as a subcontractor on EB primes or as routed via Northrop Grumman.
This is documented in `reference_prior_analysis/Federal_Procurement_Research_Lessons_Learned.md`,
Section 10.

---

## What "outsourced" means in this context

A submarine "prime" (GDEB) does NOT manufacture most of the boat in-house.
Work that flows out of the prime to others is the outsourced portion:

1. **First-tier subcontracts** -- the prime hires a vendor to build a component
   (Northrop Grumman sonar, BAE forward subassembly, L3Harris periscopes, MTU diesels,
   etc.). Reported (imperfectly) via USAspending `/api/v2/subawards/` against the
   prime PIID.

2. **Government-furnished equipment (GFE)** -- DoD/NAVSEA contracts another company
   directly and ships the result to GDEB to install. These are SEPARATE FPDS prime
   contracts to the GFE vendor (e.g., Bechtel naval reactors, LM Trident, LM Virginia
   combat systems). They show up as primes in FPDS, but the dollars are outsourced from
   the perspective of submarine production.

3. **Plans cost / lead-yard support / design** -- engineering services performed by
   the prime but also by various subs and FFRDCs (Penn State ARL, JHU APL, MIT LL).

4. **The Maritime Industrial Base (MIB) line** -- starting FY22 the Navy has put
   $1.3-3B+/year of supplier-development money into the budget. This is funded
   through GDEB but flows almost entirely OUT to suppliers (BlueForge Alliance,
   small machine shops, casting/forging vendors, workforce training partners).

The "annual outsourced work" we want is the sum of:
- Window-period subaward obligations on GDEB submarine PIIDs (first-tier visible subs)
- Window-period prime obligations to GFE vendors directly tied to a submarine line
- MIB supplier-development spend (visible in SCN 1045 P-5c "Plans Cost")

Caveats (per prior analysis):
- Subaward reporting is incomplete (FFATA $30K threshold + non-compliance gaps)
- USAspending caps subaward pulls at ~2,000 records per prime; the Virginia Block V
  master alone has >2,000 records so the long tail is truncated
- Federal naval-shipyard work (Norfolk, Portsmouth, Pearl Harbor, Puget Sound) is
  federal payroll, NOT outsourced -- excluded from this analysis but called out
- Classified payloads (intel community modules) are invisible
- Cumulative `totalObligatedAmount` from FPDS ≠ window-period spend; per-mod delta
  analysis is required to get true annual numbers

---

## Folder structure

```
submarine_outsourced_work/
├── README.md                          (this file)
├── budget_books/
│   ├── SCN_Book_FY27.pdf              (FY27 Navy SCN justification book — has FY25 actual + FY26 estimate + FY27 request columns; LI 1045 Columbia + LI 2013 Virginia)
│   ├── SCN_Book_FY27.txt              (layout-preserved text)
│   ├── 30_Year_Shipbuilding_Plan.pdf  (PB27 30-year shipbuilding plan)
│   └── 30_Year_Shipbuilding_Plan.txt
├── reference_prior_analysis/
│   ├── federal_procurement_data_guide.txt              (FPDS/USAspending/SAM.gov field reference)
│   ├── Federal_Procurement_Research_Lessons_Learned.md (gotchas from prior pulls — read first)
│   ├── Subaward_Pull_Lessons_Learned.md                (more subaward-specific gotchas)
│   └── SAM_Submarine_Cutter_Contract_Awards.md         (prior FY20-26 submarine analysis with PIIDs)
├── scripts/                           (Python scripts for pulling + parsing)
├── extracted/                         (parsed CSVs from budget books)
├── fpds_raw/                          (raw FPDS XML/JSON dumps by query)
└── usaspending_subawards/             (subaward JSON pulls keyed by PIID)
```

---

## Pull plan

### Sources

1. **FY27 SCN Book (Navy Shipbuilding & Conversion justification)** -- LI 1045 Columbia
   + LI 2013 Virginia P-5 / P-5a / P-5b / P-5c / P-21 exhibits. Has named contractor
   references (e.g., the Build I contract `N00024-17-C-2117`) and cost-category breakdowns
   that distinguish Basic Construction from Plans Cost from Electronics from Ordnance,
   etc.

2. **30-Year Shipbuilding Plan (PB27)** -- profile of planned procurement over FY27-FY56;
   Columbia + Virginia ramps; MIB investment narrative.

3. **FPDS Atom Feed** -- direct vendor-name pulls for GDEB, HII-NNS, BPMI, plus the
   specific known submarine PIIDs. Date window: FY18 signed (catches Block IV/V/Columbia
   Build I master vehicles that are still active) through present. Per-mod detail so we
   can compute annual obligation deltas.

4. **USAspending `/api/v2/subawards/`** -- subaward tree per major GDEB submarine PIID.
   This is the direct measure of first-tier outsourced $.

### Key known PIIDs (seed list from prior analysis)

| PIID | Prime | Scope | Notes |
|---|---|---|---|
| `N0002417C2100` | GDEB | Virginia Block V / Block VI master | $34.94B cumulative obligated; 2,000+ subs ($4.14B capped) |
| `N0002417C2117` | GDEB | Columbia Build I + Build II | $24-30B cumulative obligated; 2,000+ subs ($8.11B capped) |
| `N0002412C2115` | GDEB | Virginia Block IV MYP | $19.90B; mostly closed out |
| `N0002424C2110` | GDEB | Virginia Block VI LLTM | $4.96B; all window-real |
| `N0002419C2114` | BPMI | Naval reactor components (Columbia) | $3.38B (GFE) |
| `N0002419C2115` | BPMI | Columbia Class Industrial Base Increase | $3.00B (GFE) |
| `N0002424C2114` | BPMI | S9G reactor (Virginia)? | $2.54B (window-only per prior notes) |
| `N0002413C2128` | GDEB | Columbia Design Drawings | $3.07B; 608 subs ($274M) |
| `N0002419C2125` | GDEB | Virginia Tech Instructions / HPAD backfit | $1.37B; 1,292 subs ($241M) |
| `N0002416C2111` | GDEB | VPM Ventilation Valve | $1.47B |
| `N0002410C2118` | GDEB | VPM Tube Fabrication | $1.42B |
| `N0002420C4312` | GDEB | USS Hartford EOH (depot, not new) | $1.33B |
| `N0002410C6266` | LM | Virginia Combat Systems | $899M |
| `N0002421C4106` | BAE | SSN 812 Forward Subassembly | $85M |

### Process

1. **Extract** -- Pull Columbia (LI 1045) and Virginia (LI 2013) line item data from FY27
   SCN text into CSV. Capture the prior-year (FY25 actual + FY26 estimate) and FY27
   request columns at the cost-category level (Basic Construction, Plans Cost, Change
   Orders, Electronics, Ordnance, HM&E, Other Cost). Save to `extracted/`.

2. **FPDS pull** -- Run vendor-name searches against GDEB, HII-NNS, BPMI, and the named
   sub vendors (Lockheed Martin, BAE Systems, Northrop Grumman, L3Harris, Curtiss-Wright,
   Rolls-Royce) filtered to NAVY contracting agency (1700) or DEPARTMENT_ID 9700, with
   per-mod detail. Save raw JSON per query to `fpds_raw/`.

3. **Subaward pull** -- For each major submarine PIID, look up the
   `generated_internal_id` via USAspending `/api/v2/search/spending_by_award/`, then pull
   the full subaward tree via `/api/v2/subawards/` with `sort=action_date desc`. Save
   raw JSON to `usaspending_subawards/`.

4. **Manifest** -- After raw data is gathered, write `MANIFEST.md` listing every file,
   what's in it, the search query that produced it, and known caveats.

---

## Open methodology questions (flag for later)

- **Cumulative vs. window dollars:** FPDS `totalObligatedAmount` is the running total at
  the latest mod. For "annual outsourcing" we need either per-mod `obligatedAmount`
  summed by signed-date FY, or year-over-year deltas of the cumulative total. The
  former is more precise; the latter is faster. Default to per-mod sum.

- **GFE attribution:** When BPMI gets a $1B prime contract for Columbia reactor
  components, that's outsourced FROM the Navy POV but it's NOT outsourced from GDEB.
  Need to decide whether "outsourcing by primes" means (a) only what GDEB subs out, or
  (b) the total fraction of the SCN dollar going to anyone other than the assembling
  yard. The 30-year plan language ("outsourcing partners") suggests (b). Track both
  separately.

- **HII-NNS share:** Their team-build portion is largely invisible in FPDS. The only
  reliable source is HII 10-K segment disclosure (Newport News Shipbuilding segment
  revenue × an analyst estimate of submarine share). Out of scope for this initial
  gathering pass.

- **MIB / Maritime Industrial Base:** $1.3B in SCN FY26 (per FY26 book quotes); FY27
  request appears larger. This is a NEW major flow that didn't exist pre-2022.
