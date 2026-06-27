# 2026-06-24 — Session log (recompete examples — slides 02 & 03, real awards data)

Replaced the deck's weak "Recompete Radar" example (a 52-row small-craft table using the
non-term "clock") with **two complementary, fully-sourced worked examples** that cover two
routes into a recompete, and built the backing data pulls for each:

- **Slide 02 — Recompete Cadence → Supply-Chain Entry** (DDG-51 MYP): a closed two-yard
  prime whose 5-year cadence dates an *open* $3.47B first-tier supply chain. Route taught:
  *supply the prime*.
- **Slide 03 — Recompete On-Ramp** (Army watercraft ship-repair pool): a 14-holder
  multiple-award IDIQ with a date-certain last date to order. Route taught: *become a holder*.

All data pulled SAM-primary (SAM Contract Awards + SAM Subaward Reporting) + USAspending;
nothing leans on the legacy FPDS feed. Every figure traces to a CSV under
`research/recompete_cadence_ddg/` or `research/recompete_radar_shiprepair/`.

---

## What was created

**Slide specs** (`slide_specs/`):
- `slide_02_recompete_radar.md` — rewritten end-to-end (filename kept). Standard-markdown
  content brief: takeaways → evidence (cadence chain, sourcing wave, recurring suppliers,
  SWBS map, where-and-when-to-enter, SAM corroboration, provenance/caveats).
- `slide_03_recompete_onramp.md` — new; the contestable companion. Cross-referenced both ways.

**`research/recompete_cadence_ddg/`** (DDG-51 MYP):
- Scripts: `pull_ddg_myp_sam.py` (SAM CA by PIID), `build_ddg_provenance.py` (USAspending
  detail/transactions/funding + merge), `build_ddg_subaward_evidence.py` (block/recurring/
  SWBS/wave), `pull_ddg_sam_subawards.py` (fresh FFATA corroboration), 
  `build_ddg_subaward_concentration.py` (mock-PoP + HHI).
- Prime layer CSVs: `ddg_myp_recompete_provenance.csv` (35 cols), `ddg_myp_obligation_by_fy.csv`,
  `ddg_myp_fields.{json,csv}`.
- Subaward layer CSVs: `ddg_subaward_by_block.csv`, `ddg_recurring_suppliers.csv`,
  `ddg_subaward_by_swbs.csv`, `ddg_subaward_wave_by_year.csv`, `ddg_subaward_lag_after_award.csv`,
  `ddg_subaward_hhi_by_system.csv`, `ddg_subaward_supplier_mockpop.csv`,
  `ddg_subaward_sam_corroboration.{csv,json}`, `ddg_subaward_summary.json`,
  `ddg_subaward_concentration_summary.json`.
- Raw tiers: `sam_contract_awards/`, `usaspending_raw/{detail,transactions,funding}/`,
  `sam_subawards/`.

**`research/recompete_radar_shiprepair/`** (Army ship-repair pool):
- Script: `build_shiprepair_pool.py`.
- CSVs: `shiprepair_pool_holders.csv` (14 holders × 27 fields), `shiprepair_pool_summary.json`,
  `shiprepair_order_obligation_by_fy.csv`.
- Raw: `sam_contract_awards/`, `usaspending_raw/detail/`.

## How it was built

- **Reused the proven SAM/USAspending client** from `saronic_specific_awards_data/research/
  contracts/scripts/_common.py` (IPv4 force, `SAM_API_KEY` from root `.env`, bounded retry,
  429 halt) across all new pull scripts.
- **DDG prime chain**: 8 prime PIIDs (FY11 singles + FY13-17/18-22/23-27 MYP, HII+BIW). SAM
  CA carries the FPDS-native authority set (multiyear flag, pricing, competition, contracting
  office); USAspending gives exact dollars/dates/TAS and paginates transactions correctly.
  SAM's `piid` search caps at ~100 mods and ignores `offset` → used it for authority only,
  USAspending for the full per-mod series.
- **Ship-repair pool**: roster discovered from the Army contracts extract (`W56HZV21DL*`
  family, all `MULTIPLE AWARD` + `FAIR`); IDV authority + `lastDateToOrder` from SAM CA; the
  IDV holds $0 so realized $/TAS/per-FY come from the delivery-order layer (Army extract).
- **DDG supplier base**: FFATA transactions from the Distributed Shipbuilding extract; SWBS
  via the workbook's `Mapping - HII Code to SWBS` crosswalk (the raw SWBS columns are empty
  and the workbook's SWBS sheet stores formulas with no cached values, so the join was done
  from the HII work-item code). Fresh SAM Subaward Reporting pull corroborated the totals.

## Key findings (verified)

- **DDG cadence**: awards 2013-06-03 → 2018-09-27 → 2023-08-01 (~5 FY) → next buy ~2028. All
  blocks `multiyearContract = Y`, fixed-price-incentive, full-and-open after exclusion, **2
  offers per block from one solicitation** (dual-source). TAS = **SCN 017-1611** (Shipbuilding
  & Conversion, Navy). Dollars tie to the program of record exactly.
- **Recovered the missing BIW FY23-27 award** `N0002423C2305` ($5.0B obl / $13.8B ceiling) by
  a PIID-pattern probe (`…C2305` = Bath, `…C2307` = Ingalls) — absent from the shipbuilding pull.
- **DDG supply chain**: $3,465.8M reported first-tier subawards, 521 suppliers, **266 recurring
  across ≥2 blocks** (Rolls-Royce, GE, Timken, Johnson Controls, Northrop). SWBS: propulsion
  27.6% + auxiliary 27.3% + electric 21.7% = 76% of mapped $.
- **Award → wave lag**: ~26% of subaward $ in the award year, ~80% within +4 years → FY28-32
  (~2028) opens a supplier window ~2028–2031.
- **HHI concentration**: overall 354 (fragmented); **auxiliary $948M / HHI 683 = the open lane**;
  propulsion (HHI 1,905, GE 35%) and electric (HHI 2,106, Rolls-Royce 43%) entrenched; armament
  locked (HHI 6,561).
- **Under-reporting**: SAM-fresh ≈ workbook to the dollar; **BIW files 0.9% / 4.3% / 0.0% of HII**
  per block → the visible base is Ingalls'; Bath's chain is dark in FFATA.
- **Ship-repair pool**: 14 holders / 10 vendors, 3 regional tiers (CONUS $529M / Japan-Korea
  $216M / forward $186M — ceilings *shared*, not summed), common **last date to order 2026-01-25**,
  74 orders / **$416.8M realized**, funded O&M Army (021-2020) + Other Procurement Army (021-2035).
  Successor check: none visible → live recompete window (caveat: DoD 90-day rule).

## Methodology decisions / corrections (per user)

- **Dropped "clock"** → `ordering-period end` / `last date to order` for IDVs; `next buy /
  MYP cadence` for definitive contracts. A multi-year definitive contract records *no* ordering-
  period end (unlike the IDIQ pool) — that contrast is the slide pair's spine.
- **SAM Contract Awards primary** (FPDS phasing out); no field is described as an "FPDS field."
- **§7 money hygiene**: per-mod obligation is the only summable measure; cumulative/ceiling never
  summed; a multiple-award pool's ceiling is shared across holders (reported per tier).
- **Mock PoP** = count of unique subaward report IDs (workbook method), kept alongside the
  first→last date span (Timken: 8 report-IDs but 125-mo span shows the count alone misleads);
  flagged as a proxy, not a contractual PoP.
- **FFATA caveat**: first-tier only, 6–18 mo lag, under-reported → every subaward total is a floor.

## Notes / open items

- The DDG supplier base is effectively the **Ingalls** chain; Bath's first-tier suppliers are
  dark in FFATA, so the SWBS / recurring-supplier / HHI picture under-represents the Bath side.
- Slides 02 and 03 are deliberate **companions** (supply-the-prime vs become-a-holder); slide
  01's funnel covers both routes plus bid-direct and OT-consortium.
- No slide *modules* were built — these are spec/design-doc + data only; the deck still renders
  the three `contracts_*` slides. Building slide 02/03 would wire these CSVs into Python modules.
- Whole `awards_methodology/research/` tree is **untracked in git**.
- Re-runs: all pull scripts are resumable (skip-if-exists on raw files); SAM needs `SAM_API_KEY`
  in the repo-root `.env`; USAspending needs no key.
