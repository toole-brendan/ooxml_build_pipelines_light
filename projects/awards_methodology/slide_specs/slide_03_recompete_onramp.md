# Recompete On-Ramp — Slide 03

**Companion to slide 02 (Recompete Cadence → Supply-Chain Entry, DDG-51 MYP).** Together
they show two ways into a recompete: *supply the prime* (slide 02 — a closed prime whose
supply chain is open) versus *become a holder* (this slide — bid onto a multiple-award
pool). This slide is the on-ramp.

**What the slide demonstrates:** an expiring multiple-award IDIQ pool is a dated,
winnable recompete — its ordering-period end is recorded on each award years ahead, and
the route in is an open on-ramp, not a closed re-up. Worked example: the U.S. Army's
watercraft non-nuclear ship-repair pool (TACOM).

---

## Key takeaways

1. **An expiring multiple-award pool is a dated recompete you can see coming.** The Army
   watercraft ship-repair IDIQ (`W56HZV21DL`, Army TACOM) put 14 holder vehicles on
   contract with a single **last date to order: 2026-01-25** — recorded on each award in
   SAM Contract Awards, visible years in advance.

2. **The route is open — this is an on-ramp, not a duopoly.** It was competed full-and-open
   and runs task orders on FAR 16.505 fair opportunity across **10 distinct vendors**. At
   recompete you bid onto the next pool, or subcontract to a current holder — unlike the
   DDG line, which re-ups to the same two shipyards.

3. **It's a real, recurring channel.** 74 delivery orders and **$416.8M** obligated through
   the pool to date; ship repair re-competes on a cycle, so a follow-on pool is expected.

4. **The window is open now.** The ordering period closed 2026-01-25 and **no successor
   pool is visible** in the data — the recompete is live (the "no successor seen → open
   turnover" gate).

5. **Read the order layer, and mind the shared ceiling.** A multiple-award IDV holds $0
   itself — the money and appropriations live on the delivery orders. The tier ceilings
   ($529M / $216M / $186M) are *shared across holders*, never summed.

---

## Supporting evidence

### The pool — 14 holder vehicles in 3 regional tiers

One full-and-open competition (Army TACOM) seated holders in three sub-pools, each a
multiple-award group with its own *shared* ceiling and a common last date to order of
**2026-01-25**. Realized $ = sum of each holder's delivery orders.

| Tier (solicitation) | Holder | PIID | Orders | Realized | PSC |
|---|---|---|--:|--:|---|
| **CONUS — $529M shared** (W56HZV20RL807) | Bay Ship & Yacht | W56HZV21DL002 | 5 | $145.4M | J999 |
| | Metal Trades | W56HZV21DL010 | 18 | $58.9M | J998 |
| | Colonna's Ship Yard | W56HZV21DL003 | 6 | $52.9M | J998 |
| | Lyon Shipyard | W56HZV21DL008 | 3 | $11.9M | J998 |
| | Murtech | W56HZV21DL011 | 6 | $10.5M | J998 |
| | Yank Marine | W56HZV21DL015 | 2 | $2.1M | J019 |
| **Japan/Korea — $216M shared** (W56HZV20RL806) | Yokohama Engineering | W56HZV21DL024 | 15 | $114.5M | J999 |
| | Sunjin Entech | W56HZV21DL023 | 1 | $7.0M | J998 |
| | Sumitomo Heavy Industries | W56HZV21DL022 | 2 | $1.7M | J019 |
| **Forward — $186M shared** (W56HZV20RL805) | HII Fleet Support Group | W56HZV21DL031 | 6 | $2.7M | J999 |
| | Metal Trades | W56HZV21DL034 | 7 | $2.6M | J019 |
| | Yokohama Engineering | W56HZV21DL038 | 1 | $6.0M | J019 |
| | Sumitomo Heavy Industries | W56HZV21DL036 | 1 | $0.4M | J019 |
| | Lyon Shipyard | W56HZV21DL033 | 1 | $0.2M | J999 |
| **Pool total** | **10 distinct vendors** | | **74** | **$416.8M** | |

- **Common last date to order:** 2026-01-25 across all 14 vehicles — one ordering-period end.
- **Some vendors hold seats in more than one tier** (Metal Trades, Yokohama, Sumitomo,
  Lyon) — they compete across regions.

### Structure & authority (from SAM Contract Awards)

| Attribute | Value | Native field |
|---|---|---|
| Vehicle type | Indefinite-delivery / indefinite-quantity (IDC) | awardOrIDVType / typeOfIdc |
| Award structure | **Multiple award** | single_or_multiple_award |
| Competition | Full and open competition | extentCompeted |
| Order route | **FAR 16.505 fair opportunity** (on every order) | fair_opportunity |
| Ordering-period end | **Last date to order = 2026-01-25** | lastDateToOrder |
| Ordering-period start | 2021-01-27 | periodOfPerformanceStartDate |
| Contracting office | Army TACOM (W56HZV / W4GG) | contractingOffice |
| Work | Non-nuclear ship repair — PSC J998 / J999 / J019; NAICS 336611 | productOrService / principalNaics |

### The money — realized vs. shared ceiling

- **Realized obligation: $416.8M** across 74 delivery orders (the only summable measure —
  the sum of per-order obligations).
- **Ceilings are shared per tier** — $529M (CONUS, 6 holders), $216M (Japan/Korea, 3),
  $186M (forward, 5). These are pool capacity, *not* spend, and must never be summed
  across holders (a multiple-award IDV's ceiling is shared by all holders).
- The IDV vehicles themselves report **$0 obligated** and no appropriation — confirming
  the money sits on the child delivery orders.
- Orders were placed 2021 → 2026, right up to the 2026-01-25 ordering-period end;
  per-holder × fiscal-year detail in `shiprepair_order_obligation_by_fy.csv`.

### Successor check (the "no successor seen" gate)

- **Army contracts extract (through 2026-06-20):** zero newer TACOM ship-repair IDVs.
- **Incumbents' complete footprint, SAM Contract Awards by awardee UEI** (Bay Ship & Yacht,
  Metal Trades, Yokohama): recent **delivery orders only — no new multiple-award IDV** has
  been awarded.
- **Conclusion:** the ordering period has closed and no successor pool is visible → the
  recompete is the live opportunity. *Caveat:* on a non-federal SAM key, a DoD award signed
  in the last ~90 days is hidden ("Unrevealed"); backstop before acting on "no successor."

### Appropriation tie-back (TAS)

Delivery orders are funded from **021-2020 Operation & Maintenance, Army** (sustainment —
the natural account for repair) and **021-2035 Other Procurement, Army**. (The OCONUS
forward-tier orders frequently report no File-C TAS — funding lag / overseas reporting.)

### Data provenance — field → source

| Field | Source · native field |
|---|---|
| vehicle type, multiple-award, competition | SAM Contract Awards · awardOrIDVType, single_or_multiple_award, extentCompeted |
| **last date to order** (ordering-period end) | SAM Contract Awards · lastDateToOrder |
| shared ceiling, solicitation, contracting office | SAM Contract Awards · totalBaseAndAllOptionsValue, solicitationId, contractingOffice |
| holder roster, delivery orders, realized $, per-FY | Army contracts extract (USAspending-lineage) · obligation_amount × date_signed |
| fair opportunity, # offers (order level) | Army contracts extract · fair_opportunity_limited, number_of_offers |
| appropriation (TAS) | Army contracts extract · funding_tas, funding_account_titles |
| successor check | SAM Contract Awards by awardee UEI; Army extract scan |

Backing (machine-readable): `research/recompete_radar_shiprepair/extracted/`
`shiprepair_pool_holders.csv` (14 holders × 27 fields), `shiprepair_pool_summary.json`,
`shiprepair_order_obligation_by_fy.csv`. Pull script: `build_shiprepair_pool.py`.

### Honest caveats

- The **last date to order (2026-01-25) is date-certain and recorded**; the recompete
  itself (a successor pool) is **inferred** — none seen as of this pull.
- DoD 90-day rule: a successor signed in the last ~90 days may be hidden on a non-federal
  key — confirm before treating the window as open.
- Tier ceilings are **shared** across holders — never summed; realized obligation
  ($416.8M) is the only summable measure.
- IDV authority + last date to order are from **SAM Contract Awards** (the current feed);
  the delivery-order dollars/TAS are from the Army contracts extract (USAspending-lineage).

### Sources

SAM.gov Contract Awards — by PIID (vehicle type, last date to order, shared ceiling,
solicitation, contracting office, competition) and by awardee UEI (successor check);
USAspending /awards (IDV confirmation). Delivery-order realized dollars, fiscal-year
profile, and TAS from the Army contracts extract (USAspending-lineage). Route per FAR
Subpart 16.5 (multiple-award) / 16.505 (fair opportunity). As of 2026-06-24.
