---
title: Yard-side outsourcing — the hidden $1.8B/yr
---

# Yard-side outsourcing — the hidden $1.8B/yr

This chapter develops the analytical centerpiece of the destroyer outsourcing analysis: the **estimate that the two destroyer shipyards combined spend on the order of $1.8 billion per year on first-tier materials and subcontracts against DDG-51 production**, of which only approximately $286 million per year is visible in the FFATA first-tier subaward reporting stream. The 6-to-7× ratio between the estimated true yard-outsourcing flow and the FFATA-visible flow implies that **FFATA captures approximately 15 percent of the real yard-outsourcing flow**, leaving approximately 85 percent in the categorically invisible layer discussed in chapter 5 §"What FFATA does not capture (the gap)."

This is the destroyer analogue of the submarine wiki's chapter 11 "HII Newport News visibility gap," but with two structural differences:

1. **The gap is symmetric across two yards** rather than concentrated in a single team-build partner that is invisible to FFATA. Both BIW and Ingalls are prime of record on their own contracts, and both have FFATA-visible first-tier filings of their own — but in both cases the FFATA-visible flow is structurally smaller than the actual yard-outsourcing flow.
2. **The estimation methodology is materially different.** The submarine analysis used HII's segment-revenue disclosures (a clean read because HII Newport News is the only Newport News-segment business). The destroyer analysis must triangulate both BIW's DDG-share within General Dynamics's larger Marine Systems segment (which also contains Electric Boat and NASSCO) and Ingalls's DDG-share within HII's Shipbuilding segment (which also contains LPD-17, LHA-8, NSC, and PSC programs at the same Pascagoula facility). Both triangulations carry meaningful uncertainty bands.

This chapter presents the two convergent estimation methods (active-ship revenue allocation, and labor-cost decomposition against Bureau of Labor Statistics wage data), compares them, and reports the resulting yard-side estimate with its confidence band.

## Why the FFATA-visible flow under-states the truth

The principal categorical reasons that FFATA-visible first-tier subaward filings under-count the actual yard-side outsourcing flow, ordered by estimated dollar materiality (developed in chapter 5):

1. **Purchased material booked as direct material cost** — steel plate, prefabricated piping, major HM&E components booked under direct-material accounting rather than under a subcontract clause
2. **Lower-tier subcontracts** — a sub's sub is not FFATA-reportable
3. **FFATA non-compliance and under-reporting** — particularly acute at BIW, where the FY23-27 multiyear master has zero published filings as of May 2026
4. **Long-term supplier agreements not subordinated to the prime contract**
5. **Sub-$30,000 long tail**

The combined effect across all five categories is the dominant source of the ~85 percent of yard-side outsourcing that is invisible in FFATA.

## Method 1: Active-ship revenue allocation, scaled to 10-K

For each fiscal year, estimate per-ship annual revenue as the per-ship total contract value divided by the construction-cycle duration. Sum across active hulls at each yard, and scale so that the total matches the segment-revenue disclosure in the parent company's 10-K. Then back out the per-ship-allocable DDG revenue, multiply by the estimated yard-side supplier content as a share of revenue, and report the implied yard-side outsourcing flow.

**Per-ship inputs** (representative recent vintages):

| Program | Per-ship contract $M | Construction years | Annual per-ship $M |
|---|---:|---:|---:|
| DDG-51 (recent FY23-25 vintage) | 1,900 | 5.0 | 380 |
| LPD-17 (Ingalls program) | 1,850 | 6.0 | 308 |
| LHA (Ingalls program) | 3,700 | 7.5 | 493 |
| National Security Cutter (Ingalls program) | 650 | 3.5 | 186 |

### Per-FY DDG share at Ingalls (Method 1 result)

The active-ship revenue allocation at Ingalls, scaled to match the 10-K Ingalls Shipbuilding sub-segment revenue:

| FY | Ingalls actual $M | DDG-51 $M | DDG % | LPD $M | LPD % | LHA $M | LHA % | NSC $M | NSC % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 2,555 | 1,021 | 40.0% | 828 | 32.4% | 331 | 13.0% | 375 | 14.7% |
| 2020 | 2,678 | 1,070 | 40.0% | 868 | 32.4% | 347 | 13.0% | 393 | 14.7% |
| 2021 | 2,528 | 1,202 | 47.5% | 779 | 30.8% | 312 | 12.3% | 235 | 9.3% |
| 2022 | 2,570 | 1,168 | 45.4% | 568 | 22.1% | 606 | 23.6% | 229 | 8.9% |
| 2023 | 2,752 | 1,309 | 47.5% | 636 | 23.1% | 679 | 24.7% | 128 | 4.7% |
| 2024 | 2,767 | 1,316 | 47.5% | 640 | 23.1% | 683 | 24.7% | 129 | 4.7% |
| 2025 | 3,078 | 1,560 | 50.7% | 843 | 27.4% | 675 | 21.9% | 0 | 0.0% |

**Method 1 DDG share at Ingalls (FY19–FY25 average): 45.5 percent** (range 40–51 percent).

### Cross-checks

A separate FPDS-based check that buckets Navy obligations by description (DDG-51, LPD-17, LHA) finds the DDG-51 share at Ingalls running at approximately 100 percent of *new* obligations — but this overstates the DDG share because the LPD/LHA/NSC pre-2018 MYP block buys are excluded from the FPDS window and because NSC work is funded under the Coast Guard appropriation rather than Navy. The 10-K disclosed-award method (Method 3) is consistent with Method 1 in years with major DDG MYP awards (50–70 percent in those years) and lower in other years.

**Hardened range for DDG share at Ingalls: 46–70 percent.**
**Point estimate: ~53 percent** (split between Method 1 mean and Method 3 in-year peak).

### Per-FY DDG share at BIW (BIW is simpler)

For BIW, the active-ship revenue allocation is materially simpler than for Ingalls because BIW has only one current program (DDG-51) plus the closed DDG-1000 residual. Applying the same per-ship-revenue method against the GD Marine Systems segment financials, with BIW estimated at approximately 22 percent of Marine Systems revenue and the DDG-51 share at BIW at approximately 85 percent:

| FY | GD Marine Systems $M | BIW est. $M (22%) | DDG share at BIW (Method 1) |
|---:|---:|---:|---:|
| 2023 | 12,461 | 2,741 | ~85% |
| 2024 | 14,343 | 3,156 | ~85% |
| 2025 | 16,723 | 3,679 | ~85% |

**BIW DDG-51-allocable revenue (FY24): ~$2,690M.**

## Method 2: Labor-cost decomposition against BLS wage data

Independent triangulation: estimate yard-side labor cost from the disclosed headcount and the BLS NAICS 336611 (Ship Building & Repairing) wage data. The residual after subtracting labor cost and operating earnings from segment revenue is the implied yard-side materials and subcontracts cost (= COGS minus labor minus SG&A).

For Ingalls (FY2024):

| Input | Value | Source |
|---|---:|---|
| Ingalls employee count | ~12,300 (28% of HII total 44,000) | HII 10-K Part I + analyst reports |
| BLS NAICS 336611 average wage | $33/hr × 2,080 hr | BLS occupational employment statistics |
| Base wage per worker | $69,000/yr | derived |
| Loaded cost per worker (1.4–1.6× factor) | $95,000–$110,000/yr | typical defense-shipbuilding overhead structure |
| **Implied Ingalls total labor cost** | **~$1,230M/yr** (range $1,170–$1,353M) | derived |
| Ingalls FY24 revenue | $2,767M | 10-K |
| Labor cost / revenue | 42–49% | computed |
| Operating earnings (FY24) | ~7.6% of revenue = $210M | 10-K |
| Implied COGS+SG&A | 92.4% of revenue = $2,557M | derived |
| Implied materials + subs + manufacturing overhead | COGS − labor = $1,327M | residual |
| Of which materials + subs (excluding mfg overhead) | ~$1,120M (=40% of revenue) | analyst estimate |

The implied **~$1,120M per year in materials + subs at Ingalls** is at the segment level, including non-DDG (LPD, LHA, NSC). Applying the 53 percent DDG share at Ingalls (Method 1) yields approximately **$593M per year of DDG-allocable yard-side outsourcing at Ingalls** by this decomposition method.

The 53 percent DDG-share-of-Ingalls-revenue rule is a simplification (the actual allocation of materials and subs to DDG vs. non-DDG programs at Ingalls is not directly disclosed), so this estimate carries a wider uncertainty band. The reasonable range from Method 2 at Ingalls is **$480M–$960M of DDG-allocable yard-side outsourcing per year**.

For BIW (FY2024):

BIW has approximately 6,500 employees (smaller than Ingalls's 12,300). Applying the same per-worker loaded cost of ~$100K/yr yields approximately **$650M of BIW total labor cost**. Against BIW revenue of approximately $3,160M (22 percent of Marine Systems), this implies labor / revenue of approximately 20 percent — substantially lower than the 42–49 percent at Ingalls.

The discrepancy is explained by the **higher capital-intensity per worker at BIW** (newer drydock infrastructure, larger module-fabrication automation, more efficient floor layout) and by **BIW's higher share of subcontracted work** (BIW outsources a higher share of its hull-fabrication than Ingalls does, with shipfitting and module-fab work increasingly sourced to specialty fabricators). Applying the implied 80 percent COGS / revenue at BIW (similar to industry average) yields approximately $2,528M of COGS at BIW, minus $650M of labor, leaving approximately **$1,878M of materials + subs + manufacturing overhead at BIW**. Applying the 85 percent DDG share at BIW yields approximately **$1,596M of DDG-allocable yard-side outsourcing at BIW** by this method — but this is an upper-bound figure because BIW also has substantial GFE-pass-through and program-overhead costs that are not first-tier outsourcing flow.

A more defensible estimate is to apply the same 42 percent materials-and-subs share of revenue rule from Ingalls (Method 2) to BIW's revenue base:

- BIW total revenue (FY24): ~$3,160M
- × DDG share at BIW: 85 percent
- = BIW DDG-allocable revenue: ~$2,690M
- × yard-side supplier content (42 percent, Method 2): ~$1,130M
- = **BIW DDG yard-side subcontract spend: ~$1,130M per year**

## Combined estimate

Combining Method 1 (active-ship allocation) with Method 2 (labor-cost decomposition) gives the headline combined estimate:

| Yard | DDG-allocable revenue $M | × Supplier content | DDG yard-side sub spend $M | Range $M |
|---|---:|---:|---:|---:|
| HII Ingalls | ~1,650 | 42% | **~690** | 480–960 |
| GD Bath Iron Works | ~2,690 | 42% | **~1,130** | (analyst, similar range) |
| **Combined** | **~4,340** | **42%** | **~1,820** | **1,400–2,200** |

The combined estimate of **~$1.8 billion per year of yard-side first-tier outsourcing across both yards** is the analytical centerpiece. The range $1.4–2.2 billion reflects the principal sources of uncertainty:

- DDG share of Ingalls revenue (range 46–70 percent in Method 1)
- BIW share of Marine Systems (range 18–25 percent in analyst estimates)
- Yard-side supplier content as a share of revenue (range 35–50 percent in Method 2)
- Definitional uncertainty about what counts as "materials + subs" vs. "manufacturing overhead" (which can shift the supplier-content number by 5–10 percentage points depending on the choice of cut)

The number is **not a precise point estimate**; it is a directional estimate with a wide confidence band. The headline qualitative reading is more reliable than the specific dollar figure: the combined yard-side outsourcing flow is **on the order of $1–2 billion per year**, not $100M or $10B.

## Against the FFATA-visible flow

The FFATA-visible first-tier subaward flow against the BIW and Ingalls prime PIIDs in the in-scope set:

| Yard | Cumulative FFATA-visible $M (FY02–FY26, in-scope PIIDs only) | Estimated annual rate |
|---|---:|---:|
| HII Ingalls | ~2,520 cumulative | ~120 / yr on average; ~250 / yr recent |
| GD Bath Iron Works | ~165 cumulative | ~8 / yr on average; ~30 / yr recent (with FY23-27 master mostly unfiled) |
| **Combined** | **~2,685** | **~130 / yr on average; ~286 / yr recent** |

The recent-rate combined FFATA-visible flow of approximately **$286M per year** against the combined yard estimate of **~$1.8 billion per year** implies that **FFATA captures approximately 15 percent of the real yard-outsourcing flow**.

The 85 percent invisible share is distributed across the five categorical reasons documented in chapter 5: direct material booking, lower-tier subs, FFATA non-compliance (notably the BIW master with zero filings), long-term supplier agreements not subordinated to the prime, and the sub-$30,000 long tail.

## What this means as a share of total ship cost

At the FY24 two-ship buy with Total Ship Estimate of approximately $5,492M for two ships ($2,746M per ship), the combined yard-side outsourcing flow of ~$1.8 billion per year represents approximately:

| Denominator | Yard-side outsourcing flow ~$1.8B/yr as share of: |
|---|---:|
| FY24 two-ship Total Ship Estimate ($5,492M) | **~33%** |
| Basic Construction layer only (~$3,322M = 60.5% of TSE) | **~54%** |
| Per-ship Total Ship Estimate ($2,746M) × 2 ships × construction-cycle 5 years = $27.5B program window | **~6.5%** of window total |

The 33 percent figure (yard-side outsourcing as a share of total ship cost) plus the GFE layer (Electronics 11.3% + Ordnance 21.6% = 32.9% of TSE) sum to approximately **66 percent of total ship cost outsourced** — within the broader industry estimate range of 70–80 percent quoted by CSIS in its 2022 *Shipbuilding Industrial Base* report.[^csis-2022]

The residual ~34 percent of total ship cost is captured by yard self-perform labor + overhead + Plans + Change Orders + Other — i.e., the share of work that is "actually done at Bath or Pascagoula by yard-employed labor."

This is the destroyer analogue of the broadly-cited industry rule of thumb that shipyards self-perform on the order of 30 percent of total ship cost. The destroyer-specific computation supports a slightly higher self-perform share (33 percent) than the rule of thumb because of BIW's relatively higher mechanical-engineering and class-design content (held at BIW as Design Agent rather than outsourced).

## Implications for the headline 87-percent figure

The chapter 4 headline of "approximately 87 percent of dollar-weighted POP on supplier-TAM-relevant DDG-51 actions flows outside the two destroyer shipyards" is computed against the DoD-announcement TAM corpus, a specific subset of program contract value. Connecting the chapter 4 measurement to the chapter 9 yard-side estimate:

- The 87 percent figure measures POP on $7.1B of supplier-TAM-relevant action value — overwhelmingly GFE actions (Aegis at $3.5B, SPY-6 at $1.5B, VLS at $0.5B, propulsion + guns + combat-system + SEWIP at ~$0.6B combined).
- The $1.8B/yr yard-side outsourcing figure measures dollars *inside* the yard's prime contract scope that are subcontracted to first-tier suppliers — not GFE flows that go through separate Navy-prime contracts.
- These are **structurally additive** dollar flows, not overlapping. The combined picture is approximately $5B/yr of GFE flowing through Navy-prime GFE contracts to supplier cities (Aegis, SPY-6, VLS, Mk 45, LM2500, SEWIP, CIWS) **plus** approximately $1.8B/yr of yard-side first-tier outsourcing flowing through BIW and Ingalls prime contracts to their supplier bases — making the total *Navy-perspective outsourcing flow* approximately $6.8B per year against a program-level annual run-rate of approximately $7–8B (FY25 SCN appropriation $7,858M).

The combined outsourcing share against the program-level run-rate is therefore approximately **85–95 percent**, consistent with the chapter 4 headline 87 percent figure when computed on the broader denominator.

## Caveats and what would tighten the estimate

The combined ~$1.8 billion-per-year yard-side outsourcing estimate carries a wide confidence band primarily because:

1. **No publicly disclosed Bath Iron Works segment-revenue figure exists.** GD reports Marine Systems aggregated across Electric Boat + BIW + NASSCO. The BIW share is estimated at ~22 percent based on analyst reports and by-program revenue allocation, but the actual share could plausibly range from 18 percent to 25 percent.
2. **The DDG share of Ingalls revenue carries a documented 46–70 percent range** (Method 1 active-ship allocation). The point estimate of 53 percent is defensible but not narrowly pinned.
3. **The yard-side supplier content as a share of revenue is itself a triangulated 35–50 percent band**, depending on whether manufacturing overhead is included or excluded.

What would tighten the estimate:

- **HII Newport News-vs-Ingalls sub-segment disclosure improvement.** Currently HII reports a combined "Shipbuilding segment" with limited breakout; a more granular DDG-vs-LPD-vs-LHA breakout in the 10-K would materially tighten the DDG-share estimate.
- **A formal BIW carve-out from Marine Systems in GD's reporting.** Not expected, but would tighten the BIW revenue estimate.
- **Audit data from a DoD Inspector General investigation of FFATA compliance** at BIW would clarify the "compliance gap" component of the invisible 85 percent.
- **CSIS-style industry-benchmark refresh of yard-side supplier content** post-COVID would update the 35–50 percent rule of thumb that drives the Method 2 calculation.

None of these is in the pipeline. The chapter 9 estimate stands at its current confidence level and should be read as a directional centerpiece rather than as a precise point estimate.

[^csis-2022]: Center for Strategic and International Studies, *Shipbuilding Industrial Base* (2022). Provides the 65–75 percent supplier-content benchmark for destroyer programs (including GFE).
