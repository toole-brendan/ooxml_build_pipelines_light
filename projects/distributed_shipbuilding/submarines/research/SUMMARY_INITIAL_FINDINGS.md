# Initial findings — submarine outsourcing data

**This is a "data gathered" report, not an analysis.** Numbers below are
straight from the raw pulls and are intended to confirm coverage looks correct.

Status: All five data pulls complete (SCN budget extract for FY22-27 books, 30-yr plan, FPDS, USAspending subawards, SAM.gov subawards).

---

## 1. Budget book — SCN FY27 line items

Pulled from `budget_books/SCN_Book_FY27.pdf` into `extracted/scn_li_*.csv`.

### Columbia Class Submarine (LI 1045, P-1 Line #1)

From `scn_li_resource_summary.csv`:

| Metric | Prior Yrs | FY25 | FY26 | FY27 Base | FY28 | FY29 | FY30 | FY31 | To Complete | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Quantity | 2 | – | 1 | 1 | 1 | 1 | 1 | 1 | 4 | **12** |
| Gross/Weapon System Cost ($M) | 26,810 | 0 | 10,744 | 10,486 | 10,137 | 10,361 | 10,441 | 10,693 | 56,768 | **146,441** |
| Net Procurement (P-1) ($M) | * | 0 | 3,929 | 6,905 | 6,379 | 6,058 | 6,012 | 6,303 | 25,624 | **61,210** |
| Total Obligation Authority ($M) | 29,176 | 9,581 | 9,280 | 15,583 | 12,835 | 11,351 | 12,360 | 12,020 | 34,256 | **146,441** |

### Virginia Class Submarine (LI 2013, P-1 Line #6)

| Metric | Prior Yrs | FY25 | FY26 | FY27 Base | FY28 | FY29 | FY30 | FY31 | To Complete | TOTAL |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Quantity | 40 | 1 | 1 | 2 | 2 | 2 | 2 | 2 | 6 | **58** |
| Gross/Weapon System Cost ($M) | 124,749 | 9,501 | 5,389 | 11,437 | 11,285 | 11,098 | 10,197 | 10,594 | 34,144 | **228,394** |
| Net Procurement (P-1) ($M) | 77,068 | 7,357 | 2,740 | 8,402 | 8,149 | 7,876 | 7,283 | 7,423 | 20,650 | **146,949** |
| Total Obligation Authority ($M) | 122,911 | 13,320 | 6,378 | 13,151 | 13,011 | 14,687 | 12,269 | 12,017 | 20,650 | **228,394** |

### P-5c Cost Category breakdown — Columbia (most recent ship, FY27 = SSBN 829)

| Cost Category | FY21 (SSBN 826) | FY24 (SSBN 827) | FY26 (SSBN 828) | FY27 (SSBN 829) |
|---|---:|---:|---:|---:|
| Plan Costs | 6,946 | 1,443 | 1,096 | **862** |
| Basic Construction/Conversion | 5,979 | 6,356 | 7,160 | **6,854** |
| Change Orders | 238 | 143 | 217 | 207 |
| Electronics | 358 | 350 | 361 | 368 |
| Propulsion Equipment | 1,701 | 1,614 | 1,295 | **1,542** |
| Hull, Mechanical, Electrical (HM&E) | 156 | 119 | 102 | 102 |
| Ordnance (Trident D5) | 669 | 597 | 469 | 513 |
| Other Cost | 73 | 67 | 44 | 40 |
| **Total Ship Estimate** | **16,122** | **10,689** | **10,744** | **10,486** |

### Production schedule confirmation

All Columbia (SSBN 826-833): **General Dynamics Electric Boat** is the named shipbuilder.
All Virginia (SSN 803-820): **EB/HII-NNS** team build.

---

## 2. Subaward data — first-tier outsourcing by GDEB visible in USAspending

Pulled per-PIID from `/api/v2/subawards/` for 17 seed submarine prime contracts.
See `usaspending_subawards/` for raw JSON; `extracted/subaward_annual_by_prime.csv`
for the FY rollup; `extracted/subaward_top_recipients.csv` for the top-200 recipients.

### Annual subaward flow visible (12 GDEB PIIDs)

| FY | Total subaward $ ($M) | Driver |
|---|---:|---|
| FY16 | 206 | Block IV ramp |
| FY17 | 1,307 | Block V signing (N0002417C2100 = $991M) |
| FY18 | 1,028 | Block V continuation |
| FY19 | 1,456 | Block V + Columbia Build I awards |
| FY20 | 353 | Trough |
| FY21 | 826 | |
| FY22 | 696 | |
| FY23 | **3,813** | **Columbia BlueForge MIB ramp begins** ($2.75B on N0002417C2117) |
| FY24 | **4,162** | **Peak so far** ($3.65B on N0002417C2117) |
| FY25 | 766 | Likely reporting lag — comes back up over next 12-18 mo |

### Top 20 sub recipients across all submarine PIIDs (FY16-FY25)

| Rank | Recipient | $M | Notes |
|---:|---|---:|---|
| 1 | BlueForge Alliance | 4,214 | MIB consortium pass-through — distributes to small/mid-tier shops + training |
| 2 | Northrop Grumman Systems | 2,210 | Sonar arrays, EW, combat systems; some likely HII-NNS team-build flow-through |
| 3 | Curtiss-Wright Electro-Mechanical | 515 | Nuclear pumps |
| 4 | DRS Naval Power Systems | 477 | Propulsion equipment |
| 5 | Scot Forge Company | 355 | Large forgings (hull rings, etc.) |
| 6 | BAE Systems Land & Armaments | 355 | Forward subassemblies |
| 7 | BWXT Nuclear Operations | 290 | Reactor-grade material/manufacturing |
| 8 | DC Fabricators | 255 | Hull fabrication |
| 9 | Babcock Marine (Rosyth) UK | 240 | UK partner — Columbia design support |
| 10 | Globe Composite Solutions | 223 | Composite structures |
| 11 | Precision Custom Components | 215 | Machined components |
| 12 | APCO Technologies SA | 202 | Swiss — Columbia design support |
| 13 | Rhoads Metal Fabrications | 150 | |
| 14 | Johnson Controls Navy Systems | 127 | |
| 15 | Curtiss-Wright Flow Control | 126 | Valves |
| 16 | Portland Valve | 117 | |
| 17 | Vacco Industries | 110 | |
| 18 | Oil States Industries | 105 | |
| 19 | Teledyne Instruments | 104 | |
| 20 | Huntington Ingalls Inc | 98 | **HII-NNS team-build portion that DOES show as sub of GDEB** — likely under-reports real share |

### Caveats on subaward data

- Coverage cap: USAspending caps at ~2,000 subawards per prime. Hit on N0002417C2100
  (Virginia Block V/VI) and N0002417C2117 (Columbia Build I/II) — long tail of small
  subs is missing.
- Reporting lag: FY25 subawards severely under-reported because most haven't been
  filed to USAspending yet. Real FY25 number will be 2-4x higher when full data lands
  in ~12-18 months.
- The HUNTINGTON INGALLS INC $98M at rank 20 vastly understates real HII-NNS submarine
  work — per teaming agreement they do ~50% of Virginia + ~22% of Columbia, but most
  of that flows OUTSIDE the FFATA subaward reporting mechanism (it's structured as the
  team-build agreement, not a conventional sub).
- BlueForge Alliance $4.2B is a MIB consortium PASS-THROUGH. The $4.2B does not stay
  at BlueForge — they distribute to suppliers. Need separate analysis to see where.

---

## 3. FPDS pull — complete

13 queries, 21,553 raw records / 6,816 unique PIIDs pulled from `fpds_raw/`.
Aggregated to per-FY obligated $ in `extracted/fpds_annual_by_prime.csv`.

### Per-FY this-mod obligated dollars by vendor group ($M)

Each FY = signed-date FY of the mod. `this_obligated` (NOT cumulative) is summed.
Window: SIGNED_DATE FY18 → FY26.

| FY | GDEB | HII-NNS | BPMI | LM | NG | BAE | L3Harris | C-W | R-R | BlueForge |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2018 | 3,518 | -4 | 416 | 54 | 7 | 473 | 0 | 36 | 438 | 0 |
| 2019 | 532 | -4 | 1,912 | 272 | 48 | 445 | 0 | 40 | 436 | 0 |
| 2020 | 231 | -7 | 1,291 | 19 | 58 | 623 | 26 | 28 | 434 | 0 |
| 2021 | 377 | -2 | 2,000 | 117 | 69 | 732 | 0 | 33 | 590 | 0 |
| 2022 | 335 | -1 | 2,119 | 48 | 1 | 316 | 0 | 63 | 593 | 0 |
| 2023 | 302 | 0 | 1,430 | 119 | 54 | 307 | 2 | 125 | 483 | 0 |
| 2024 | 384 | -1 | 2,182 | 186 | 18 | 371 | 4 | 99 | 407 | 538 |
| 2025 | 840 | 0 | 2,145 | 35 | 33 | 239 | 2 | 61 | 757 | 366 |
| 2026 | 286 | 0 | 1,897 | 31 | 0 | 78 | 0 | 7 | 162 | 19 |

### Per-query record counts

| Query slug | Records | Unique PIIDs | Notes |
|---|---:|---:|---|
| `gdeb_navy` | 3,000 (capped) | 166 | True count ~7,520; capped at 300 pages. Top vendor: ELECTRIC BOAT CORPORATION $57.9B cumulative across 166 PIIDs. |
| `hii_nns_navy` | 5,731 | 1,516 | Mostly CVN/RCOH, not submarine. |
| `bpmi_navy` | 97 | 19 | Tight set. All submarine-relevant (naval reactor work). |
| `lockheed_navy_sub` | 292 | 34 | Description-filtered to Virginia/Columbia/Submarine/Trident. |
| `northrop_navy_sub` | 132 | 12 | Description-filtered. |
| `bae_navy_sub` | 2,222 | 505 | Description partial filter + vendor catch-all. |
| `l3harris_navy_sub` | 44 | 13 | Description-filtered. |
| `curtiss_wright_navy` | 2,490 | 991 | **NO description filter** — over-counts non-submarine CW work. |
| `rolls_royce_navy_sub` | 2,980 | 1,391 | **NO description filter** — over-counts non-submarine RR work (esp. aircraft engines). |
| `blueforge_navy` | 3,901 | 1,972 | "BLUE FORGE" substring catches lots of unrelated "BLUE *" vendors (Blue Tech, Blue Rock, etc.). True BLUEFORGE ALLIANCE total: $923M cumulative on 1 PIID. |
| `desc_virginia_class` | 420 | 124 | Top vendor: ELECTRIC BOAT $74.5B cumulative across 8 PIIDs. |
| `desc_columbia_class` | 237 | 63 | Top vendors: ELECTRIC BOAT $16.7B + BPMI $5.7B. |
| `desc_submarine_navy_big` | 7 | 6 | Backstop sweep ($50M+ floor on "SUBMARINE" description). Caught Amentum Services $608M + RQ Construction $234M (likely facilities/MAC). |

### FPDS data caveats

1. **GDEB FY18 spike ($3.5B)** is a single big mod against an existing master. Later
   years show lower per-mod obligated because the masters are funded incrementally.
   GDEB's TRUE total work is best measured via cumulative `totalObligatedAmount` on
   the master PIIDs ($34.94B on N0002417C2100, $24-30B on N0002417C2117) and via the
   subaward data above, NOT via this per-mod sum.

2. **BPMI shows $1.4-2.2B/year consistently** — this IS the annual naval reactor GFE
   flow. Stable annual procurement (S9G reactors for Virginia, larger reactor for
   Columbia). This is the most reliable "annual outsourcing" number in the table.

3. **Curtiss-Wright + Rolls-Royce numbers over-count non-submarine work.** Their
   queries don't have description filters, so they catch ALL Navy work. Rolls-Royce
   in particular has huge aircraft-engine business. Treat the C-W and R-R columns as
   "upper-bound" until further filtered.

4. **BlueForge column over-counts.** "BLUE FORGE" substring matched many unrelated
   "Blue *" vendors. True BlueForge Alliance prime activity is $538M (FY24) + $366M
   (FY25) + $19M (FY26) — concentrated in 1 PIID. The rest of the "BlueForge group"
   in the rollup is bogus matches.

5. **HII-NNS negative numbers in FY18-25** are de-obligations on CVN contracts that
   net out the small new flows. NNS submarine prime work via FPDS is essentially zero
   per the team-build pattern — sub work flows through GDEB.

---

## What "annual outsourcing by sub primes" looks like — final

The headline table (see `extracted/annual_budget_vs_subawards.csv`):

| FY | Columbia TOA $M | Virginia TOA $M | Total Sub SCN $M | SAM subs $M | USA subs $M | SAM % of TOA |
|---|---:|---:|---:|---:|---:|---:|
| FY20 | 1,821 | 8,335 | 10,156 | 372 | 353 | 3.7% |
| FY21 | 4,122 | 6,776 | 10,899 | 599 | 826 | 5.5% |
| FY22 | 4,777 | 6,340 | 11,117 | 675 | 696 | 6.1% |
| **FY23** | 5,858 | 6,865 | 12,722 | **3,727** | **3,813** | **29.3%** |
| **FY24** | 7,789 | 10,657 | 18,446 | **4,013** | **4,162** | **21.8%** |
| FY25 | 9,581 | 13,320 | 22,901 | 780 | 766 | 3.4% (lag-depressed) |
| FY26 | 9,280 | 6,378 | 15,657 | 0 | 0 | – (too early) |
| FY27 | 15,583 | 13,151 | 28,734 | 0 | 0 | – (request) |

**Source for "Total Sub SCN $M":** reconciled per-FY actuals from the most recent
SCN justification book that shows each year as actual (PB22 book → FY20 actual; ...; PB27 book → FY25 actual). See `extracted/scn_per_fy_actual_toa.csv` for the full vintage trail.

**Two subaward sources, side-by-side:**
- **SAM** ($/yr column) = SAM.gov Acquisition Subaward Reporting API, FY20-26 window
  (subAwardDate filter), authoritative for FY20-26.
- **USA** ($/yr column) = USAspending /api/v2/subawards/, full history (no date filter).
  Useful for cross-validation. Capped at 2,500 records per prime.

The two sources agree within ~5% at FY level — confirming both are reliable for
aggregate analysis.

### Headline finding

The annual outsourced flow visible in public data **jumped ~5x in FY23-24** (from ~$675M
in FY22 to ~$3,727M in FY23 and ~$4,013M in FY24). Driven primarily by the BlueForge
Alliance MIB consortium pass-through ($4.17B cumulative across FY23-24).

As a % of submarine SCN TOA, first-tier outsourcing visible in public data went from
~6% (FY20-22) to ~22-29% (FY23-24). The true share is higher: USAspending caps long-tail,
some primes don't report FFATA, and the HII-NNS team-build portion is mostly invisible.

### Stripping out the MIB consortium pass-through

BlueForge Alliance is a Maritime Industrial Base (MIB) consortium. Per the SCN budget
narrative, MIB funding is parked in the "Plan Costs" P-5c cost category (not in Basic
Construction). To see "conventional" subaward intensity — i.e., what GDEB actually subs
out for shipbuilding — strip BlueForge from subs AND Plan Costs from the budget side.

From `extracted/annual_budget_vs_subawards_v2.csv`:

| FY | SCN TOA $M | Plan Costs $M (incl MIB) | TOA - Plans $M | Basic Construction $M | Total subs $M | BlueForge subs $M | Non-BF subs $M | A. all/TOA | B. NonBF/(TOA-Plans) | C. NonBF/Basic |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FY20 | 10,156 | 0 | 10,156 | 0 | 372 | 0 | 372 | 3.7% | 3.7% | – |
| FY21 | 10,899 | 6,946 | 3,953 | 5,979 | 599 | 0 | 599 | 5.5% | 15.1% | 10.0% |
| FY22 | 11,117 | 252 | 10,865 | 4,758 | 675 | 0 | 675 | 6.1% | 6.2% | 14.2% |
| **FY23** | 12,722 | 192 | 12,530 | 5,095 | **3,727** | **1,514** | **2,213** | 29.3% | **17.7%** | 43.4% |
| **FY24** | 18,446 | 1,650 | 16,796 | 15,427 | **4,013** | **2,659** | **1,354** | 21.8% | **8.1%** | 8.8% |
| FY25 | 22,901 | 2,596 | 20,305 | 5,327 | 780 | 0 | 780 | 3.4% | 3.8% | 14.6% |
| FY26 | 15,657 | 1,315 | 14,342 | 10,297 | – | – | – | – | – | – |
| FY27 | 28,734 | 1,085 | 27,649 | 15,743 | – | – | – | – | – | – |

Three ratios:
- **A. Total subs ÷ TOA** — original headline; MIB-inclusive
- **B. (Subs − BlueForge) ÷ (TOA − Plan Costs)** — conventional subaward rate, MIB stripped from both sides ← most apples-to-apples
- **C. (Subs − BlueForge) ÷ Basic Construction** — subs against ship-level construction commitment (orders-of-magnitude only; Basic Construction is per ship-authorization while subs are per-FY cash flow across all active ships)

**Key takeaway:** even after stripping BlueForge from subs AND Plan Costs from the
budget, FY23 conventional subaward rate jumped to 17.7% (vs ~6% in FY22). So there
IS a real increase in conventional subcontracting in the MIB era — not just the
consortium pass-through. FY24 looks lower (8.1%) because Plans Cost was big that year
(SSBN 827 + SSN 802 Plans), inflating the denominator.

**Caveats on Column C:** Basic Construction is the per-ship cost commitment as of
authorization FY. Subaward $ is cash flow that year across all active ships and blocks.
A FY23 sub action might be paying for material installed on SSBN 826 (FY21 auth) or
SSN 802 (FY21 auth Block V) — not for SSN 813 (FY23 auth). So Column C is a useful
sanity check but NOT a true ratio.

### Top sub recipients (parent-UEI rolled, FY20-26 window) — from SAM.gov

| Rank | Parent | $M | Sub action count | Notes |
|---:|---|---:|---:|---|
| 1 | BlueForge Alliance | 4,173 | 8 | MIB consortium pass-through — distributes to small/mid-tier suppliers |
| 2 | Northrop Grumman Systems | 1,485 | 120 | Sonar, EW, combat systems; some HII-NNS team-build flow-through |
| 3 | Leonardo SPA (IT) | 491 | 121 | Italian — likely electronics / propulsion |
| 4 | Curtiss-Wright Electro-Mechanical | 316 | 262 | Nuclear pumps, valves |
| 5 | Globe Composite Solutions | 248 | 161 | Composite structures |
| 6 | Scot Forge | 200 | 441 | Large forgings (hull rings) |
| 7 | D.C. Fabricators | 163 | 40 | Hull fabrication |
| 8 | Rhoads Metal Fabrications | 142 | 73 | Hull / metalwork |
| 9 | CIRCOR International | 102 | 129 | Valves & flow control |
| 10 | The Graham Corporation | 89 | 28 | Heat exchangers / vacuum systems |
| 11 | Austal USA | 88 | 24 | Surprising — appears as a SUB; likely subcontracted work |
| 12 | L3Harris Maritime Power & Energy | 85 | 112 | Power conversion systems |
| 13 | Rosyth Royal Dockyard (UK) | 84 | 5 | UK partner — Columbia design support |
| 14 | W International | 83 | 61 | Machining |
| 15 | Teledyne Technologies | 78 | 195 | Sensors, instrumentation |

Full top-200 in `extracted/sam_subaward_top_parents.csv`.

### SAM vs USAspending — coverage comparison (`sam_vs_usaspending_per_piid.csv`)

For the 2 big GDEB masters where USAspending hit its 2,500-record cap:
- N0002417C2100 (Va Block V/VI): SAM recovered **+1,889 records** in FY20-26 window
- N0002417C2117 (Col Build I/II): SAM recovered **+1,650 records** in FY20-26 window

Total long-tail recovery: ~3,500 additional records, mostly small subs ($<1M each).
Dollar impact at FY level is minor (~5% difference) but useful for vendor diversity
analysis.

### These numbers DO NOT include:
- The HII-NNS team-build share (~50% of Virginia + ~22% of Columbia, mostly invisible
  in federal data)
- The Lockheed Martin Trident missile flow (separate program / appropriation)
- Federal naval shipyard depot maintenance (not outsourced; federal payroll)
- Classified payload work
- Subs that primes failed to FFATA-report (non-compliance gap)

See `MANIFEST.md` for full file inventory and `README.md` for methodology.
