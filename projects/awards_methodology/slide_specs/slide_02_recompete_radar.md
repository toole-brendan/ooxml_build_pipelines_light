# Recompete Cadence → Supply-Chain Entry — Slide 02

**Companion to slide 03 (Recompete On-Ramp, Army ship-repair pool).** Together they show
two ways into a recompete: *supply the prime* (this slide — a closed prime whose supply
chain is open) versus *become a holder* (slide 03 — bid onto a multiple-award pool).

**What the slide demonstrates:** the DDG-51 prime is a closed two-yard duopoly you can't
win — but it re-buys on a fixed ~5-year cadence, and each block flows **~$1B+ to a visible
first-tier supplier base**. The cadence is the *timing engine*; the addressable move is to
supply the next block's sourcing wave, positioned years ahead.

---

## Key takeaways

1. **The cadence is the timing engine.** DDG-51 is bought as sequential multi-year
   procurements — FY13-17 → FY18-22 → FY23-27, awarded 2013 / 2018 / 2023. The next block
   (FY28-32) is due **~2028**, readable in the award record now.

2. **The prime is closed; the supply chain is the opening.** You can't win the prime (it
   re-ups to Huntington Ingalls + Bath Iron Works), but each block sub-contracts **~$1B+**
   to first-tier suppliers — **$3.47B reported across 521 suppliers** over the chain. That
   layer is enterable.

3. **The cadence makes the supplier opportunity *datable*.** Subaward dollars are
   front-loaded off each prime award — **~26% land in the award year, ~80% within four
   years** — so the FY28-32 buy (~2028) opens a dated supplier window **~2028–2031**.
   Position *ahead* of the surge instead of chasing it.

4. **The base is fragmented overall, but concentration is system-specific — that's the
   where-to-enter signal.** Overall supplier HHI is just 354, but **auxiliary systems
   ($948M, HHI 683, no supplier >16%) is the open lane**, while propulsion and electric are
   big but entrenched (GE 35%, Rolls-Royce 43% — teaming targets). 266 of 521 suppliers
   recur across ≥2 blocks — the established base you'd compete with or team with.

5. **Read it honestly.** First-tier (FFATA) subaward reporting is a **floor, not a census**
   — first-tier only, 6–18 month lag, and under-reported: **Bath Iron Works files <5% of
   Huntington Ingalls** on the same block, so its chain is essentially dark. And the timing
   is a **demand-surge forecast, not a bid deadline**.

---

## Supporting evidence

### The timing engine — the multi-year procurement cadence

DDG-51 is re-bought as 5-year multi-year procurements, dual-sourced HII + BIW from one
solicitation each cycle. (Full prime detail — authority, the §7 dollar measures, TAS — is
in the prime provenance CSV; here it is the backbone that *dates* the supplier waves.)

| Block | Awarded | Prime obligated to date (HII / BIW) | Next event |
|---|---|---|---|
| FY13-17 MYP | 2013-06-03 | $3.35B / $4.93B | — |
| FY18-22 MYP | 2018-09-27 | $6.83B / $5.34B | — |
| FY23-27 MYP | 2023-08-01 | $6.95B / $5.03B | — |
| **FY28-32 MYP** | **~2028 (forecast)** | **not yet awarded** | **next sourcing wave** |

Award cadence 2013 → 2018 → 2023 (~5 FY) → next buy **~2028**. The prime route is closed
(definitive contracts, no on-ramp); the *route in* is to supply a holder.

### The sourcing wave — first-tier subaward $ by block

| Block | Reported first-tier subaward $ | Distinct suppliers |
|---|--:|--:|
| FY11 single-ship | $51.7M | 144 |
| FY13-17 MYP | $942.3M | 320 |
| FY18-22 MYP | $1,327.2M | 344 |
| FY23-27 MYP (young, ramping) | $1,144.6M | 89 |
| **Total** | **$3,465.8M** | **521** |

Each new block re-opens ~$1B of first-tier supplier demand — the FY28-32 wave is the next.

### The supplier base — recurring suppliers (serve ≥2 blocks)

The established base: **266 suppliers** appear on ≥2 blocks (out of 521). These are the
incumbents you compete with or team with; top by reported $:

| Supplier | Blocks | Reported $ | Ship system |
|---|--:|--:|---|
| Rolls-Royce Marine North America | 3 | $384.7M | Propulsion (gas-turbine / mechanical) |
| General Electric | 3 | $333.1M | Propulsion (LM2500 gas turbines) |
| Johnson Controls Navy Systems | 3 | $178.0M | Auxiliary (HVAC / climate) |
| Timken Gears & Services | 3 | $169.2M | Propulsion (main reduction gears) |
| SOCAIL, LDA | 2 | $151.4M | Auxiliary |
| Northrop Grumman Systems | 4 | $123.1M | Command, control & surveillance |
| York International | 2 | $115.4M | Auxiliary (chilled water / AC) |
| Ellwood National Forge | 2 | $87.9M | Hull / propulsion forgings |

Full roster in `ddg_recurring_suppliers.csv`.

### What the dollars buy — SWBS ship-system map

Subaward dollars mapped to ship work-breakdown system (HII work-item crosswalk; 81% of
dollars map):

| SWBS major group | Ship system | Reported $ | % of total |
|---|---|--:|--:|
| 200 | Propulsion plant | $957.9M | 27.6% |
| 500 | Auxiliary systems | $947.5M | 27.3% |
| 300 | Electric plant | $750.8M | 21.7% |
| 600 | Outfit & furnishings | $62.4M | 1.8% |
| 400 | Command, control & surveillance | $47.5M | 1.4% |
| 100 | Hull structure | $24.3M | 0.7% |
| 700 | Armament | $1.5M | 0.0% |
| — | unmapped / non-Ingalls (incl. BIW) | $674.0M | 19.5% |

**Propulsion + auxiliary + electric = 76% of mapped dollars** — that's where the supplier
opportunity concentrates.

### Where and when to enter

**When — the award → wave lag.** Subawards are front-loaded off the prime award, so the
prime's date-certain contract timing dates the supplier window:

| Years after prime award | Share of first-tier subaward $ | Cumulative |
|---|--:|--:|
| year 0 | 26% | 26% |
| +1 | 16% | 42% |
| +2 | 15% | 58% |
| +3 | 11% | 69% |
| +4 | 10% | 79% |

→ the FY28-32 award (~2028) opens a supplier window **~2028–2031**; the time to be sourced
is *before* it opens. (Mature blocks FY13-17 + FY18-22; `ddg_subaward_lag_after_award.csv`.)

**Where — concentration by ship system (HHI).** Big *and* fragmented = most enterable;
big *and* concentrated = teaming target, not break-in:

| Ship system | $M | Suppliers | HHI | Read |
|---|--:|--:|--:|---|
| Auxiliary systems | 948 | 90 | 683 | **open lane** — no supplier >16% |
| Propulsion plant | 958 | 29 | 1,905 | entrenched (GE 35%) — team |
| Electric plant | 751 | 24 | 2,106 | entrenched (Rolls-Royce 43%) — team |
| Command, control & surveillance | 48 | 7 | 2,188 | concentrated, small |
| Armament | 2 | 2 | 6,561 | locked (Lake Shore 78%) |

**Longevity — which seats are sticky.** A subaward has no period of performance, so use the
count of unique subaward report IDs as a mock PoP, paired with the first→last date span:
Rolls-Royce (115 report IDs / 139 mo) and Northrop (69 / 138 mo) are deep, sustained seats;
Timken (8 report IDs but a 125-mo span) shows the count alone understates a few-big-orders
relationship — so both measures are kept (`ddg_subaward_supplier_mockpop.csv`).

### SAM corroboration & under-reporting

Pulled fresh from **SAM.gov Subaward Reporting** (the FFATA source) and reconciled to the
workbook — they agree to the dollar — and the same pull quantifies the under-reporting:

| Block | HII reported (SAM) | BIW reported (SAM) | BIW share |
|---|--:|--:|--:|
| FY13-17 MYP | $933.4M | $8.9M | 0.9% |
| FY18-22 MYP | $1,270.1M | $57.1M | 4.3% |
| FY23-27 MYP | $1,144.6M | $0.0M | 0.0% |

BIW's near-zero is a **reporting artifact, not its real supplier spend** — so the visible
base is effectively Ingalls'; Bath's chain is dark in FFATA.

### Appropriation, provenance & caveats

- **Prime appropriation:** the blocks fund from **SCN (Shipbuilding & Conversion, Navy,
  017-1611)** — the multi-year shipbuilding account (prime provenance CSV).
- **Provenance — field → source:** prime cadence, dollars, dates, TAS → SAM Contract
  Awards + USAspending (`ddg_myp_recompete_provenance.csv`); first-tier subawards (by block,
  by supplier, by SWBS, by year) → **SAM Subaward Reporting** corroborated against the
  Distributed Shipbuilding extract; SWBS via the workbook HII-code→SWBS crosswalk.
- **Honest caveats:** FFATA subawards are first-tier only, lag 6–18 months, and are
  under-reported (BIW ≪ HII) → every subaward total is a floor, and the HHI / where-to-enter
  read is on *reported* dollars. The supplier "recompete" is a **forecastable demand surge
  on the prime's cadence**, not a date-certain ordering-period end (a multi-year definitive
  contract records none — unlike slide 03's IDIQ); the **mock PoP (report-ID count) is a
  proxy**, not a contractual period of performance.

Backing: `research/recompete_cadence_ddg/extracted/` — `ddg_subaward_by_block.csv`,
`ddg_recurring_suppliers.csv`, `ddg_subaward_by_swbs.csv`, `ddg_subaward_wave_by_year.csv`,
`ddg_subaward_lag_after_award.csv`, `ddg_subaward_hhi_by_system.csv`,
`ddg_subaward_supplier_mockpop.csv`, `ddg_subaward_sam_corroboration.csv`, plus the prime
layer in `ddg_myp_recompete_provenance.csv`. Scripts: `build_ddg_subaward_evidence.py`,
`build_ddg_subaward_concentration.py`, `pull_ddg_sam_subawards.py`, `build_ddg_provenance.py`.

### Sources

Prime cadence & dollars: SAM.gov Contract Awards (by PIID) + USAspending (/awards,
/transactions, /awards/funding); multiyear basis 10 U.S.C. 3501 / FAR Subpart 17.1.
First-tier supplier base: SAM.gov Subaward Reporting (FFATA), corroborated against the
Distributed Shipbuilding subaward extract; SWBS ship-system crosswalk from the program
workbook. As of 2026-06-24.
