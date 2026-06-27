# The Subcontractor Route, Worked: A Committed Prime's Supply Chain — Slide 03 (two-routes set)

**Companion to slide 02 (the prime route, Army ship-repair on-ramp).** Together they work the
two routes from slide 01: *compete as a prime* (slide 02 — a multiple-award pool) versus
*supply the prime* (this slide — a closed prime whose supply chain is open).

**What the slide demonstrates:** the DDG-51 prime is a closed two-shipyard arrangement a new
entrant cannot win — but it is re-procured on a fixed multiyear cadence, and each block flows
**~$1B+ to a visible first-tier supplier base**. The re-procurement cadence dates the supplier
opportunity; the addressable move is to be sourced into the next block's first-tier demand,
positioned years ahead. Within that demand, two angles pick *where* to aim: **compete into the
fragmented work-types**, or **offer a second source where a single vendor dominates a critical
one.**

---

## Key takeaways

1. **The prime is closed; the supply chain is open.** A new entrant cannot win the prime
   (it re-ups to Huntington Ingalls + Bath Iron Works), but each block sub-contracts **~$1B+**
   to first-tier suppliers — **$3.47B reported across 521 suppliers** over the chain. That layer
   is addressable.

2. **The re-procurement cadence dates the supplier opportunity.** DDG-51 is bought as sequential
   multiyear procurements — FY13-17 → FY18-22 → FY23-27, awarded 2013 / 2018 / 2023. The next
   block (FY28-32) is due **~2028**, readable in the award record now.

3. **The first-tier demand is front-loaded off each prime award.** **~26% of subaward dollars
   land in the award year, ~80% within four years** — so the FY28-32 award opens a first-tier
   sourcing cycle **~2028–2031**. The time to be sourced is *before* it opens.

4. **Concentration is system-specific — and it cuts two ways.** Overall supplier HHI is low
   (354), but each work-type is either fragmented or dominated, and **both are entry signals.**
   *Big, fragmented systems are open lanes* to compete into — **auxiliary systems ($947.5M,
   90 suppliers, top vendor 15.9%)**. *Big systems held by a single dominant supplier are
   second-source targets*, where the prime and the Navy have a motive to qualify an alternative —
   **electric plant (Rolls-Royce 42.6% of $750.8M)**. **266 of 521 suppliers recur across
   ≥2 blocks** — the established base a new entrant competes with or teams with.

5. **Read it as a floor.** First-tier (FFATA) subaward reporting is **first-tier only, lags
   6–18 months, and is under-reported** — **Bath Iron Works files <5% of Huntington Ingalls** on
   the same block, so its chain is essentially dark. And the timing is a **forecastable demand
   cycle, not a date-certain ordering-period end.**

---

## The cadence and the supplier demand — award data by block

DDG-51 is re-bought as 5-year multiyear procurements, dual-sourced HII + BIW from one
solicitation each cycle. This is the manager-requested data layer — prime obligation, first-tier
subaward dollars, and TAS.

| Block (MYP) | Awarded | Prime obligated to date (HII / BIW)¹ | First-tier subawards² | Distinct suppliers |
|---|---|--:|--:|--:|
| FY13-17 | 2013-06-03 | $3.35B / $4.93B | $942.3M | 320 |
| FY18-22 | 2018-09-27 | $6.83B / $5.34B | $1,327.2M | 344 |
| FY23-27 | 2023-08-01 | $6.95B / $5.03B | $1,144.6M | 89 |
| **FY28-32** | **~2028 (forecast)** | **not yet awarded** | **next sourcing cycle** | **—** |
| **Chain total** | — | — | **$3,465.8M³** | **521³** |

¹ **Cumulative obligation to date** per shipyard (`total_obligation` · USAspending /
`totalActionObligation` · SAM CA) — a restated snapshot, **never summed across modifications.**
A definitive multiyear contract carries **no IDV ceiling** (contrast slide 02's shared ceiling).
² **Reported first-tier (FFATA) subaward dollars** (`subAwardAmount` · SAM Subaward Reporting).
³ Chain total includes a FY11 single-ship buy ($51.7M / 144 suppliers). **521 = distinct
suppliers** (they recur across blocks, so the column does not sum).

**TAS:** the blocks fund from **SCN (Shipbuilding & Conversion, Navy), 017-1611** — the
multiyear shipbuilding account (prime provenance CSV; USAspending `/awards/funding`).

## What the dollars buy — SWBS ship-system map

Subaward dollars mapped to ship work-breakdown system (HII work-item crosswalk; 81% of dollars
map). Compressed to the dominant systems:

| SWBS group | Ship system | Reported $ | % of total |
|---|---|--:|--:|
| 200 | Propulsion plant | $957.9M | 27.6% |
| 500 | Auxiliary systems | $947.5M | 27.3% |
| 300 | Electric plant | $750.8M | 21.7% |
| — | unmapped / non-Ingalls (incl. BIW) | $674.0M | 19.5% |

**Propulsion + auxiliary + electric = 76% of mapped dollars** — where the supplier opportunity
concentrates. (Full eight-group table — outfit, C4ISR, hull, armament — in the backing CSV.)

## Where and when to enter

**When — the award → demand lag.** Subawards are front-loaded off the prime award, so the
prime's date-certain contract timing dates the supplier sourcing cycle:

| Years after prime award | Share of first-tier subaward $ | Cumulative |
|---|--:|--:|
| year 0 | 26% | 26% |
| +1 | 16% | 42% |
| +2 | 15% | 58% |
| +3 | 11% | 69% |
| +4 | 10% | 79% |

→ the FY28-32 award (~2028) opens a first-tier sourcing cycle **~2028–2031**; the time to be
sourced is *before* it opens. (Mature blocks FY13-17 + FY18-22; `ddg_subaward_lag_after_award.csv`.)

**Where — two angles on the same concentration screen.** Both angles read the two metrics the
SAM award-classification workbook pairs — **HHI** and **Top-1 share** (the largest single
vendor's share) — by work-type, at both operating-entity (UEI) and ultimate-parent grain
(workbook labels: *Lower / Moderate / High concentration*; the annual *Structure Class* codes
`HHI-H / Inc-H` …). *Large and fragmented* and *large and single-vendor-dominated* are opposite
reads of that screen, and each is a distinct way in.

- **Angle 1 — compete into a fragmented system (the open lane).** Big work-types with many
  suppliers and no dominant one (*Lower concentration* — low Top-1 share, high effective-firm
  count); entry is on merit, and the fragmentation leaves room for another qualified supplier.
- **Angle 2 — offer a second source where one vendor dominates.** Big, critical work-types held
  by a single dominant supplier (*High concentration* — Top-1 share ≥ ~60% or HHI ≥ 0.40). Here
  the entry is enabled by the prime's — and the Navy's — own motive to **reduce a single-source
  dependency**: a new entrant pitches **second-source qualification**, frequently sponsored under
  industrial-base-resilience programs. High concentration is not only a teaming wall; it is a
  second-source opening.

| Ship system | $M | Suppliers | Top-1 share | HHI† | Read — which angle |
|---|--:|--:|--:|--:|---|
| Auxiliary systems | 947.5 | 90 | 15.9% (Johnson Controls) | 683 | **Angle 1 — open lane:** fragmented, compete in |
| Electric plant | 750.8 | 24 | 42.6% (Rolls-Royce) | 2,106 | **Angle 2 — second source:** big, single-supplier-exposed |
| Propulsion plant | 957.9 | 29 | 34.7% (General Electric) | 1,905 | Angle 2 watch — large, GE-led |
| Command, control & surveillance | 47.5 | 7 | 37.5% (EMS Development) | 2,188 | concentrated, smaller $ |
| Armament | 1.5 | 2 | 77.9% (Lake Shore) | 6,561 | single-source extreme (small $) |

† HHI on the 0–10,000 scale; the workbook's *High concentration* line (HHI ≥ 0.40) ≡ 4,000 here,
or Top-1 share ≥ 60%.

- **Angle 1 worked:** auxiliary systems — **$947.5M across 90 suppliers, top vendor 15.9%** — is
  the clearest open lane. (At the finer Capability-Domain grain, fluid / pressure / piping is even
  more contestable — Top-1 8.6% across 55 suppliers.)
- **Angle 2 worked:** electric plant — **Rolls-Royce at 42.6% of $750.8M** — and propulsion — GE
  at 34.7% of $957.9M — are the large-dollar systems most exposed to one supplier, the practical
  second-source targets. The screen's formal *High concentration* extremes are armament (Lake
  Shore 77.9%, but only $1.5M) and, at the vendor-level Capability-Domain grain, **mission, combat
  & communications — one vendor at 74.5% of reported scope (HHI 0.57)** — a textbook single-source
  dependency.
- **Parent-grain sharpening:** a work-type that looks contestable across operating entities but
  collapses to one corporate parent (high **HHI uplift** / **Firm reduction**) is a hidden
  second-source candidate — DDG specialty materials crosses the 0.40 HHI line only once UEIs roll
  up to their parent.

## SAM corroboration & under-reporting

Pulled fresh from **SAM.gov Subaward Reporting** (the FFATA source) and reconciled to the
workbook — they agree to the dollar — and the same pull quantifies the under-reporting:

| Block | HII reported (SAM) | BIW reported (SAM) | BIW share |
|---|--:|--:|--:|
| FY13-17 MYP | $933.4M | $8.9M | 0.9% |
| FY18-22 MYP | $1,270.1M | $57.1M | 4.3% |
| FY23-27 MYP | $1,144.6M | $0.0M | 0.0% |

BIW's near-zero is a **reporting artifact, not its real supplier spend** — so the visible base
is effectively Ingalls'; Bath's chain is dark in FFATA.

## Appropriation, provenance & caveats

- **Prime appropriation:** the blocks fund from **SCN (Shipbuilding & Conversion, Navy),
  017-1611** — the multiyear shipbuilding account (prime provenance CSV).
- **Provenance — field → source:** prime cadence, dollars, dates, TAS → SAM Contract Awards +
  USAspending (`ddg_myp_recompete_provenance.csv`); first-tier subawards (by block, by supplier,
  by SWBS, by year) → **SAM Subaward Reporting** corroborated against the Distributed
  Shipbuilding extract; SWBS via the workbook HII-code → SWBS crosswalk.
- **Concentration method (both angles):** HHI paired with **Top-1 share**, at operating-entity
  (UEI) and ultimate-parent grain, with *Lower / Moderate / High concentration* and annual
  *Structure Class* (`HHI-H / Inc-H` …) labels — per the SAM award-classification workbook
  (`projects/distributed_shipbuilding/sam/sam_awards_data/workbook_award_classification_refactor`,
  sheets *Domain Concentration* / *Where to Play*; Capability-Domain D1–D11 and parent-grain cuts
  from the same workbook). The labels are an **analyst-defined screen on observed, reported
  concentration — not a market test**; shares are *% of reported first-tier scope*, not of total
  construction.
- **Honest caveats:** FFATA subawards are first-tier only, lag 6–18 months, and are
  under-reported (BIW ≪ HII) → every subaward total is a **floor**, and the HHI / where-to-enter
  read is on *reported* dollars. The supplier "recompete" is a **forecastable demand cycle on
  the prime's cadence**, not a date-certain ordering-period end (a definitive multiyear contract
  records none — unlike slide 02's IDV); the **mock period-of-performance (subaward report-ID
  count) is a proxy**, not a contractual period of performance.

Backing: `research/recompete_cadence_ddg/extracted/` — `ddg_subaward_by_block.csv`,
`ddg_recurring_suppliers.csv`, `ddg_subaward_by_swbs.csv`, `ddg_subaward_wave_by_year.csv`,
`ddg_subaward_lag_after_award.csv`, `ddg_subaward_hhi_by_system.csv`,
`ddg_subaward_supplier_mockpop.csv`, `ddg_subaward_sam_corroboration.csv`, plus the prime layer
in `ddg_myp_recompete_provenance.csv`. Scripts: `build_ddg_subaward_evidence.py`,
`build_ddg_subaward_concentration.py`, `pull_ddg_sam_subawards.py`, `build_ddg_provenance.py`.

## Sources

Prime cadence & dollars: SAM.gov Contract Awards (by PIID) + USAspending (/awards,
/transactions, /awards/funding); multiyear basis 10 U.S.C. 3501 / FAR Subpart 17.1. First-tier
supplier base: SAM.gov Subaward Reporting (FFATA), corroborated against the Distributed
Shipbuilding subaward extract; SWBS ship-system crosswalk from the program workbook. As of
2026-06-24.
