# Below the Waterline — What Awards & Subawards Data Reveal in the USV Market That SAM.gov Opportunities Does Not

**Market:** unmanned surface vessels / autonomous maritime + the small-craft and vessel universe (NAICS 336611/336612; PSC 1905/1925/1940/1990/2090).
**Question:** can awards/subawards data surface real opportunities the SAM.gov *Opportunities* portal misses? **Answer: yes, decisively — and for Saronic's own market the portal is nearly blind.**
**Data pulled:** 2026‑06‑23, federal FY2015–FY2026. Sources: USAspending (prime awards, transactions, funding), SAM.gov Subaward Reporting (first‑tier FFATA), and **SAM.gov Contract Awards — the single most complete prime feed, the only one that includes Other Transactions** (queried by awardee UEI; see Finding 2) — against the 669 SAM Opportunities notices already on hand for this market.

---

## Bottom line (for leadership)

1. **The portal advertises the wrong things.** Of 669 maritime notices the portal showed over 12 months, **65% are recurring ship repair & sustainment** and only **2–7% touch USV/autonomy**. The portal is a sustainment-notice stream, not a USV opportunity radar.
2. **Our market runs on OTAs — invisible to the portal *and* to a standard FPDS pull, but recoverable from awards data if you pull the right layer.** In the standard prime‑contract feed (FPDS / USAspending award types A–D + IDV — the usual market‑intel default) Saronic shows **$0**. Yet Saronic's **$457M‑ceiling Navy Other Transaction Agreement (PIID N000242596305, base signed 2025‑05‑16, $296.5M obligated to date)** is right there in the SAM.gov *Contract Awards* OT records — along with $374M of Saronic OTs in total. The portal never shows it; a naïve FPDS pull misses it; **only the OT layer of awards data surfaces it.** *Watch the wrong layer and you don't see your own contracts.*
3. **Awards data nonetheless reveals four classes of real opportunity the portal can't:** 52 pre‑recompete vehicles (12–36 months of lead time, 100% with no notice), a vehicle‑gated market locked under a handful of incumbents, a mappable subaward supply chain (681 teaming edges), and a measurable program‑expansion signal.
4. **Quantified incompleteness:** **13.8%** of conventional addressable award dollars flow through FAR 16.5 task orders the portal is *structurally exempt* from showing — and **123 of 125 ($93M, 99.9%)** addressable awards signed inside the portal's own 12‑month window had **no** matching notice.

---

## Data & method (and the honest caveats)

- **Market tiers** (`extracted/market_tiers.csv`, `market_structure_summary.json`). USAspending discovery returned **5,760 in‑scope sea‑service awards**, which split into:
  | tier | awards | obligated | what it is |
  |---|--:|--:|---|
  | **USV / autonomy** | 86 | **$0.45B** | the visible USV prime market (R&D‑heavy) |
  | **small craft** (NAICS 336612 / PSC 1940) | 1,682 | $4.35B | boats & small craft — Saronic‑adjacent |
  | **other small vessels** (PSC 1925/1990) | 280 | $6.70B | special‑service / misc vessels |
  | **broad maritime** (capital ships) | 3,712 | $399.1B | submarines/carriers/destroyers — *not* Saronic's market |
  - **Saronic‑addressable = USV + small + other‑small = 2,048 awards / ~$11.5B.** The $399B of capital ships is excluded from the addressable analysis (it would swamp the USV signal with submarines).
- **Coverage.** Award *detail* (per‑mod obligations, solicitation IDs, PoP dates) covers the **full 2,048 addressable awards = $11.50B**; numbers below are final, not a sample.
- **Money hygiene.** Every dollar is a **sum of per‑modification obligations** (`federal_action_obligation`); cumulative/ceiling fields are never summed (per the Awards Methodology deck's obligated‑vs‑ceiling rule).
- **A pull‑scope correction, stated up front (it's load‑bearing).** Stage‑1 discovery used USAspending award types **A–D + IDV only**, which *structurally excludes Other Transactions* — so it reported the USV production primes as "$0 / absent." That is a **pull artifact, not reality**: OTs are fully present in awards data via the SAM Contract Awards API (pulled by awardee UEI in `pull_ota_layer.py`, Finding 2). The two are reconciled there. Take it as the cautionary lesson, not a contradiction: *the default contract feed silently drops the exact layer the USV market runs on.*
- **What awards data still can't do:** first‑tier subawards are a reported **floor**, not a census (FFATA lags, some primes file nothing); the OT layer here samples 13 named vendors, not the whole consortium universe; PoP end dates are recompete *indicators*, not guaranteed dates. Claims are framed accordingly.

---

## Finding 1 — The portal is a sustainment stream, nearly blind to USV
`extracted/portal_content.csv`, `portal_content_summary.json`

The 669 notices, categorized by what is actually being bought:

| subject | notices | share |
|---|--:|--:|
| ship repair & maintenance | 313 | **46.8%** |
| marine components / parts | 121 | 18.1% |
| *(recurring sustainment subtotal)* | *434* | **64.9%** |
| USV / autonomy | 49 | 7.3% |
| vessel procurement | 25 | 3.7% |
| services / RDT&E | 35 | 5.2% |
| other | 126 | 18.8% |

Only **13 of 669 notices (2%)** are unambiguously USV‑specific; at most **49 (7%)** mention any autonomy term. The portal's NAVSEA/PEO‑USC notices are dominated by the **R44xx ship‑repair availability series** (USS Iwo Jima SRA, USS Truxtun modernization). The **small‑boat/USV procurement line (R22xx series)** — where Saronic's competitors actually win — **does not appear in the portal at all.**

> **Takeaway:** watching the portal tells you when a ship needs a drydock, not where the USV money is going.

---

## Finding 2 — Saronic's market lives in the OTA layer: invisible to the portal *and* to a standard contract pull, but recoverable from awards data
`extracted/ota_absence.csv` (the gap) and `extracted/ota_layer.csv`, `ota_layer_summary.json` (the recovery)

Two facts that look contradictory but aren't — and the reconciliation is the whole point:

**(a) In the standard prime‑contract universe** (USAspending/FPDS award types **A–D + IDV** — exactly what a market‑intel team pulls by default, and what this project's Stage‑1 discovery pulled), the USV production players show **nothing**:

| company | awards in standard A–D/IDV universe |
|---|--:|
| Saronic / Metal Shark / Sea Machines / Blue Water Autonomy | **0 / $0 each** |

**(b) Yet the same companies' awards are fully present in awards data — in the OT layer.** Pulling SAM.gov *Contract Awards* by awardee UEI recovers **$0.50B obligated / $0.69B ceiling** of USV Other Transactions across 13 vendors, led by:

| vendor | PIID | type | base signed | obligated / ceiling |
|---|---|---|---|--:|
| **Saronic** | **N000242596305** | **OT Agreement (Navy/PEO‑USC)** | **2025‑05‑16** | **$296.5M / $457.0M** |
| Textron Systems | W15QKN239C001 | OT Agreement | 2022‑11‑08 | $82.7M / $82.7M |
| Saronic | HQ08452490056 | OT Agreement (MDA) | 2024‑07‑03 | $44.2M / $50.3M |
| Saronic | H92405249P013 | OT IDV (DIU/DARPA) | 2024‑07‑31 | $27.2M / $31.0M |
| HII Unmanned | HQ08451990004 | OT Agreement | 2022‑09‑23 | $10.7M / $13.0M |
| Sea Machines | HQ00342090028 | OT Agreement | 2020‑07‑17 | $4.1M / $10.4M |

Saronic alone carries **$374M of OT obligations**. The reconciliation: **USV production is bought through Other Transactions**, which (i) never appear as a SAM Opportunities notice and (ii) are **excluded from the standard A–D/IDV contract feed** most FPDS‑based market views use. They surface only if you deliberately pull the OT layer.

> **Takeaway:** the lesson is sharper than "awards data beats the portal." A *naïve* awards pull (FPDS / standard contract types) would have told us USV is a $0.45B declining R&D niche (`usv_market.csv` — visible prime spend peaked at $116M in FY21, fell to $12M in FY25) **and missed Saronic's own $457M Navy production OT.** And the fix is **one query, not three datasets**: **SAM.gov Contract Awards, `awardeeUniqueEntityId` = the vendor's UEI(s), returns the complete prime footprint** — OTs, GSA schedule, and conventional orders alike. USAspending/FPDS silently drops the OTs; the Opportunities portal shows none of it.

Saronic's whole footprint, all returned by that **single** query and *none* of it in the portal (8 award families under UEI JZ14WLJDYM71):

| channel | example PIID | also in USAspending/FPDS? |
|---|---|---|
| OT agreement — Navy production | N000242596305 ($457M ceiling) | **no** (OTs dropped) |
| OT IDV — DIU/DARPA | H92405249P013 ($31M) | **no** |
| conventional delivery order — MDA SHIELD (10‑yr IDC) | HQ085926FE712 | yes |
| GSA Schedule — software (MAS) | 47QTCA26D003X | yes |

Configuring the market‑intel function around that **single source (SAM Contract Awards, by UEI)** — instead of FPDS/USAspending, which drop the OT layer the USV market runs on — is the most important choice we make.

---

## What awards data DOES reveal — the four mechanisms

### Mechanism 1 — Pre‑recompete radar (12–36 months of lead time)
`extracted/recompete_radar.csv`

**52 addressable vehicles ≥$5M hit their recompete clock within the next 36 months — 100% of them with NO portal notice yet.** A sample of the Saronic‑relevant signals:

| recompete clock | $M | incumbent | access gate | vehicle |
|---|--:|---|---|---|
| 2025‑12‑30 (overdue) | 117.8 | Gravois Aluminum Boats | holders‑only (FAR 16.5) | N0002417D2209 |
| 2026‑03‑15 | 16.2 | Silver Ships | open / standalone | N0002422C2223 |
| 2026‑09‑30 | 77.1 | Penn State (USV) | holders‑only | N0002418D6401 |
| 2026‑09‑30 | 27.5 | RIBCRAFT USA | holders‑only | N0002419D2220 |
| 2026‑10‑30 | 66.9 | Vigor Works | holders‑only | H9222211D0080 |
| 2027‑01‑31 | 98.7 | NASSCO | open / standalone | N0002422C2505 |

These are exactly Saronic's competitive set (small‑boat and USV builders). The clock is the *vehicle's* end (IDV ordering‑period / PoP potential end), per the Awards Methodology deck's rule; each still needs the **successor** and **access** gates applied before it's addressable (the radar flags holders‑only vehicles where the route is an on‑ramp or teaming, not an open bid).

### Mechanism 2 — Vehicle‑gated market (the route matters more than the requirement)
`extracted/prime_concentration.csv`

Every tier of the maritime market is **locked under a handful of incumbents**:

| tier | top‑5 prime share | HHI |
|---|--:|--:|
| USV / autonomy | 63.0% | 1,041 |
| small craft | 56.6% | 1,160 |
| other small vessels | 90.3% | 2,424 |
| broad maritime | 77.8% | 1,736 |

The small‑boat line runs through **R22xx IDVs** (Gravois, Silver Ships, Metalcraft, RIBCRAFT, ReconCraft, SAFE Boats): competed once years ago, then orders flow under FAR 16.5 with no new notices. The decision a startup faces is therefore **not "bid/no‑bid"** but **route**: get on the on‑ramp, sub to a holder, or wait for the recompete — a distinction awards data makes visible and the portal cannot.

### Mechanism 3 — Prime/subaward teaming map (route‑to‑market as a supplier)
`extracted/subaward_edges.csv`, `teaming_summary.csv`, `teaming_summary.json`

The first‑tier subaward pull maps **681 prime→sub edges, 202 distinct suppliers, $131.7M** (a reported floor; ~1.5‑month median FFATA lag here — more current than the typical 6–18 mo).
- **Teaming‑target integrators** (who sub the work out): **Teledyne Brown ($45.7M), Raytheon ($43.7M on a USV contract), HII ($13.1M), SAAB ($5.6M), Leidos ($4.4M).**
- **The established USV supply chain** (recurring suppliers across ≥2 primes): **Exail Defense** (autonomy/software), **Teledyne Technologies** (propulsion, 3 primes), EdgeOne, General Dynamics, Woods Hole Oceanographic. The very first sub under Raytheon's USV contract is literally *"Unmanned Systems Source LLC."*

> **Takeaway:** a public solicitation may never be addressed to us; the addressable opportunity is often a subsystem purchased by an integrator — and that map only exists in subaward data.

### Mechanism 4 — Program expansion / adjacency
`market_structure_summary.json` (USV‑by‑year), `award_opp_match.csv` (offices)

The conventional‑channel USV obligation curve (peak FY21, declining) read alongside the OTA absence is itself the expansion thesis: demand is migrating *out* of the visible contract channel into OTAs and into the small‑craft IDVs. The buying nodes are concentrated and nameable — NAVSEA/PEO‑USC (N00024), NIWC Pacific/Atlantic (N66001), NUWC (N66604), NSWC — the precise account map a portal‑only view ("the Navy") can't produce.

---

## Incompleteness, quantified
`extracted/incompleteness_summary.json`

- **Metric A — structural blind spot.** Of $11.50B in addressable buys, **$1.58B (13.8%, 630 actions)** flowed via **FAR 16.5 task/delivery orders under IDVs** — synopsis‑exempt by law, so the portal *cannot* show them. (OTAs add an entire further layer not even counted here — see Finding 2.)
- **Metric B — empirically dark in the portal's own window.** Of the **125 addressable awards signed inside the portal's 12‑month posting window ($93M), 123 (99.9% of dollars) had no matching notice** — including 97 of 99 definitive (synopsizable) contracts. Verified by hand: their solicitations (e.g. N0002425R2231, the competed NASSCO/VARD award with 7 offers; the R22xx small‑boat series) appear **nowhere** in the 669 notices. The portal showed R44xx repair availabilities while the boats were bought on R22xx vehicles it never surfaced. (Two awards *did* match a notice — confirming the matcher finds real links when they exist.)

---

## So what — for Saronic

1. **Stand up an awards‑based opportunity radar, not a portal watch.** The portal is a lagging sustainment feed; the recompete radar (`recompete_radar.csv`) is a 12–36‑month forward pipeline of exactly our competitors' vehicles.
2. **Pull the OTA layer by default, not as an afterthought.** SAM Contract Awards by awardee UEI (`pull_ota_layer.py`) recovers our own $457M Navy OT and ~$0.5B of USV OTs across 13 vendors that FPDS and the portal both miss. Next step: enumerate the unmanned‑maritime OT *vehicles* (the consortia/agreements themselves) and their on‑ramps, so we can get on them.
3. **Use the teaming map for channel strategy** — Teledyne, Raytheon, HII, SAAB and Leidos are sub‑ing out USV work today; that's a route to revenue that never appears as a solicitation.

---

## Phase‑2 (designed, not yet run): the historical‑replay backtest

To convert "awards data reveals more" into "awards data would have flagged opportunity X *N months early*," the next phase replays 24–30 known maritime solicitations frozen at t‑6/‑12/‑18 months and scores whether the four mechanisms would have surfaced each. The design (event selection, point‑in‑time reconstruction with the look‑ahead traps — cumulative restatement, later mods, **subaward reporting lag** — handled, the scoring, and the lead‑time/precision metrics vs. SAM/naïve/random baselines) is specified in the project plan. The ground‑truth bridge is the SAM CA `solicitationId` → solicitation linkage; subaward signals are gated on **report date**, not award date, with a 6/12/18‑month lag sweep. Expected to confirm a positive median lead time on the recompete mechanism (the R22xx IDVs above already demonstrate the principle).

---

## Reproduce
All pulls are resumable and live under `projects/awards_methodology/saronic_specific_awards_data/research/contracts/`:
```
scripts/pull_usaspending_discovery.py   # market universe + seeds (free)
scripts/pull_usaspending_detail.py      # per-award structure + transactions (free)
scripts/pull_sam_subawards.py           # first-tier subawards (SAM key)
scripts/analyze_opportunities.py        # Finding 1 (portal blindness)
scripts/analyze_market_structure.py     # Mechanism 2 + the A-D/IDV "absence" (concentration)
scripts/pull_ota_layer.py               # Finding 2 RECOVERY: OT layer by awardee UEI (SAM CA)
scripts/match_awards_to_opps.py         # incompleteness Metrics A & B
scripts/build_recompete_radar.py        # Mechanism 1
scripts/build_teaming_map.py            # Mechanism 3
```
Evidence tables land in `extracted/`. Headline figures are in the four `*_summary.json` files.
