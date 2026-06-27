# The Prime Route, Worked: A Multiple-Award On-Ramp — Slide 02 (two-routes set)

**Companion to slide 03 (the subcontractor route, DDG-51 supply chain).** Together they work
the two routes from slide 01: *compete as a prime* (this slide — seating onto a multiple-award
pool) versus *supply the prime* (slide 03 — a committed prime whose supply chain is open). This
slide is the prime route.

**What the slide demonstrates:** a multiple-award IDC is a prime opportunity — but a
holders-only one. Entry is by **seat on the pool (an on-ramp)** at re-solicitation, not by an
open proposal mid-term, and the vehicle's **ordering-period end is recorded on each award years
in advance**. Worked example: the U.S. Army's watercraft non-nuclear ship-repair pool
(TACOM, `W56HZV21DL`).

---

## Key takeaways

1. **A multiple-award IDC is a prime opportunity, gated to holders.** The Army watercraft
   ship-repair vehicle (`W56HZV21DL`, Army TACOM) seated **14 holder vehicles** under a single
   **ordering-period end of 2026-01-25** — recorded on each award in SAM Contract Awards,
   visible years ahead. The prime route in is a **seat on the pool**, won when the pool
   re-solicits.

2. **The route is open — an on-ramp, not a duopoly.** Competed full-and-open, with task orders
   placed on **FAR 16.505 fair opportunity** across **10 distinct vendors**. At re-solicitation
   a new entrant competes for a seat; in the interim it supplies a current holder.

3. **It is a recurring channel.** 74 delivery orders and **$416.8M obligated** through the pool
   to date; non-nuclear ship repair re-competes on a cycle, so a successor pool is expected.

4. **The opportunity is current.** The ordering period closed 2026-01-25 and **no successor
   pool is visible** in the data — the recompete is live (the "no successor seen → open
   turnover" gate, subject to the DoD 90-day backstop).

5. **Read the order layer, and respect the shared ceiling.** A multiple-award IDV holds **$0**
   itself — the obligations live on the delivery orders. The tier ceilings
   (**$529M / $216M / $186M**) are *shared across holders*, never summed.

---

## The pool — award data (rolled up to the three regional sub-pools)

One full-and-open competition (Army TACOM) seated holders in three sub-pools, each a
multiple-award group with its own *shared* ceiling and a common ordering-period end of
**2026-01-25**. This is the manager-requested data layer — ceiling, obligated, and TAS — at
summary altitude; the 14-holder roster sits in the backing CSV / speaker notes.

| Sub-pool (FAR 16.5 multiple-award) | Solicitation | Shared ceiling¹ | Holder seats | Delivery orders | Obligated to date² |
|---|---|--:|--:|--:|--:|
| CONUS | W56HZV20RL807 | $529.0M | 6 | 40 | $281.7M |
| Japan / Korea | W56HZV20RL806 | $216.0M | 3 | 18 | $123.2M |
| Forward (OCONUS) | W56HZV20RL805 | $186.0M | 5 | 16 | $11.9M |
| **Pool** | — | *shared — not summed* | **14 seats / 10 vendors** | **74** | **$416.8M** |

¹ **Ceiling = capacity, not spend.** Shared across the holders within a sub-pool — *never*
summed per holder (FAR Subpart 16.5 multiple-award). The three sub-pool ceilings are distinct
vehicles; even so, present them separately rather than as one figure.
² **Realized obligation** = the sum of each holder's delivery-order obligations (per-mod
`actionObligation`) — the only summable measure. Common ordering-period end
(`lastDateToOrder`) **2026-01-25** across all 14 vehicles; ordering-period start 2021-01-27.

## Structure & authority (from SAM Contract Awards)

| Attribute | Value | Native field · source |
|---|---|---|
| Vehicle type | Indefinite-delivery / indefinite-quantity (IDC) | `coreData.awardOrIDVType` / `acquisitionData.typeOfIdc` · SAM CA |
| Award structure | **Multiple award** | `acquisitionData.multipleOrSingleAwardIdc` · SAM CA |
| Competition | Full and open competition | `competitionInformation.extentCompeted` · SAM CA |
| Order route | **FAR 16.505 fair opportunity** (on every order) | `latest_transaction_contract_data.fair_opportunity_limited` · USAspending |
| Ordering-period end | **2026-01-25** | `awardDetails.dates.lastDateToOrder` · SAM CA |
| Ordering-period start | 2021-01-27 | `awardDetails.dates.periodOfPerformanceStartDate` · SAM CA |
| Contracting office | Army TACOM (W56HZV / W4GG) | `coreData.federalOrganization…contractingOffice` · SAM CA |
| Work | Non-nuclear ship repair — PSC J998 / J999 / J019; NAICS 336611 | `productOrServiceInformation` · SAM CA |

## The money — realized vs. shared ceiling

- **Realized obligation: $416.8M** across 74 delivery orders — the only summable measure
  (sum of per-order `actionObligation`).
- **Ceilings are shared per sub-pool** — $529M (CONUS, 6 holders), $216M (Japan/Korea, 3),
  $186M (forward, 5). These are pool capacity, *not* spend, and must never be summed across
  holders (a multiple-award IDV's ceiling is shared by all holders).
- The IDV vehicles themselves report **$0 obligated** and no appropriation — confirming the
  money sits on the child delivery orders.
- Orders were placed 2021 → 2026, up to the 2026-01-25 ordering-period end; per-holder ×
  fiscal-year detail in `shiprepair_order_obligation_by_fy.csv`.

## Appropriation tie-back (TAS)

Delivery orders are funded from **021 2020 Operation & Maintenance, Army** (sustainment — the
natural account for repair) and **021 2035 Other Procurement, Army**
(`/awards/funding` → `federal_account` / `account_title`, USAspending). The OCONUS forward-tier
orders frequently report **no File-C TAS** (funding lag / overseas reporting).

## Successor check (the "no successor seen" gate)

- **Army contracts extract (through 2026-06-20):** zero newer TACOM ship-repair IDVs.
- **Incumbents' complete footprint, SAM Contract Awards by awardee UEI** (Bay Ship & Yacht,
  Metal Trades, Yokohama Engineering): recent **delivery orders only — no new multiple-award
  IDV** has been awarded.
- **Conclusion:** the ordering period has closed and no successor pool is visible → the
  recompete is the live opportunity. *Caveat:* on a non-federal SAM key, a DoD award signed in
  the last ~90 days is hidden ("Unrevealed"); backstop with USAspending before acting on "no
  successor."

## Data provenance — field → source

| Field | Source · native field |
|---|---|
| vehicle type, multiple-award, competition | SAM Contract Awards · `awardOrIDVType`, `multipleOrSingleAwardIdc`, `extentCompeted` |
| ordering-period end | SAM Contract Awards · `lastDateToOrder` |
| shared ceiling, solicitation, contracting office | SAM Contract Awards · `totalBaseAndAllOptionsValue`, `solicitationId`, `contractingOffice` |
| holder roster, delivery orders, realized $, per-FY | Army contracts extract (USAspending-lineage) · `federal_action_obligation` × `action_date` |
| fair opportunity, # offers (order level) | Army contracts extract · `fair_opportunity_limited`, `number_of_offers_received` |
| appropriation (TAS) | USAspending `/awards/funding` · `federal_account`, `account_title` |
| successor check | SAM Contract Awards by awardee UEI; Army extract scan |

Backing (machine-readable): `research/recompete_radar_shiprepair/extracted/` —
`shiprepair_pool_holders.csv` (14 holders × 27 fields), `shiprepair_pool_summary.json`,
`shiprepair_order_obligation_by_fy.csv`. Pull script: `build_shiprepair_pool.py`.

## Honest caveats

- The **ordering-period end (2026-01-25) is date-certain and recorded**; the recompete itself
  (a successor pool) is **inferred** — none seen as of this pull.
- **DoD 90-day rule:** a successor signed in the last ~90 days may be hidden on a non-federal
  key — confirm before treating the opportunity as open.
- Tier ceilings are **shared** across holders — never summed; realized obligation ($416.8M) is
  the only summable measure.
- IDV authority + ordering-period end are from **SAM Contract Awards** (the current feed); the
  delivery-order dollars/TAS are from the USAspending-lineage Army extract.
- **Instrument note (sets up slide 03):** this is an **IDV**, so the money read is *shared
  ceiling vs. realized obligation*. Slide 03 works a **definitive multiyear contract**, which
  carries no IDV ceiling — there the read is *obligation + first-tier subaward*.

## Sources

SAM.gov Contract Awards — by PIID (vehicle type, ordering-period end, shared ceiling,
solicitation, contracting office, competition) and by awardee UEI (successor check);
USAspending /awards (IDV confirmation), /transactions (per-mod realized dollars), /awards/funding
(TAS). Route per FAR Subpart 16.5 (multiple-award) / 16.505 (fair opportunity). As of
2026-06-24.
