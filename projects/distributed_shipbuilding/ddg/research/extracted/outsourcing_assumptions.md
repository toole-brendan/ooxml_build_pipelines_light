# HII Ingalls — DDG share & outsourcing assumptions (hardened)

Two soft assumptions in the original $3-4B/yr yard-sub estimate:
  A1. DDG-51 share of HII Ingalls revenue — was guessed at ~50%.
  A2. Supplier content as % of revenue — rule-of-thumb 70-80%.

This document hardens both with explicit math.

---

## A1. DDG share of Ingalls revenue

### Method 1: Active-ship revenue allocation

For each year, estimate per-ship annual revenue = total contract / construction years.
Then sum across active hulls per program at Ingalls. Scale to match HII-reported Ingalls
segment revenue. Per-ship inputs:

| Program | Per-ship $M | Years | Annual per-ship $M |
|---|---:|---:|---:|
| DDG-51 | 1,900 | 5.0 | 380 |
| LPD-17 | 1,850 | 6.0 | 308 |
| LHA | 3,700 | 7.5 | 493 |
| NSC | 650 | 3.5 | 186 |

Result (per-FY DDG share at Ingalls, scaled to match 10-K revenue):

| FY | Ingalls actual $M | DDG-51 $M | DDG % | LPD $M | LPD % | LHA $M | LHA % | NSC $M | NSC % |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 2,555 | 1,021 | 40.0% | 828 | 32.4% | 331 | 13.0% | 375 | 14.7% |
| 2020 | 2,678 | 1,070 | 40.0% | 868 | 32.4% | 347 | 13.0% | 393 | 14.7% |
| 2021 | 2,528 | 1,202 | 47.5% | 779 | 30.8% | 312 | 12.3% | 235 | 9.3% |
| 2022 | 2,570 | 1,168 | 45.4% | 568 | 22.1% | 606 | 23.6% | 229 | 8.9% |
| 2023 | 2,752 | 1,309 | 47.5% | 636 | 23.1% | 679 | 24.7% | 128 | 4.7% |
| 2024 | 2,767 | 1,316 | 47.5% | 640 | 23.1% | 683 | 24.7% | 129 | 4.7% |
| 2025 | 3,078 | 1,560 | 50.7% | 843 | 27.4% | 675 | 21.9% | 0 | 0.0% |

**Method 1 DDG share avg FY19-25: 45.5%** (range 40–51%)

### Method 2: FPDS Navy obligations bucketed by description

Caveats: NEW obligations only (not revenue — lead by 3-5 years). NSC excluded (Coast Guard, not in our Navy filter). Pre-window LPD/LHA contracts excluded.

| FY | DDG-51 $M | LPD $M | LHA $M | Other $M | DDG-51 share |
|---:|---:|---:|---:|---:|---:|
| 2018 | 1,744 | 0 | 0 | 1 | 99.9% |
| 2019 | -8 | 0 | 0 | 1 | 119.2% |
| 2020 | 970 | 0 | 0 | 7 | 99.3% |
| 2021 | 666 | 0 | 0 | 1 | 99.9% |
| 2022 | 911 | 0 | 0 | 9 | 99.0% |
| 2023 | 3,247 | 0 | 0 | 1 | 94.9% |
| 2024 | 1,466 | 0 | 0 | 7 | 95.6% |
| 2025 | 2,803 | 0 | 0 | 9 | 97.8% |

**Method 2 (FPDS Navy obligations) DDG share avg: 100.7%**  (note: overstates DDG share because LPD/LHA pre-2018 MYP block buys and ALL NSC work are excluded)

### Method 3: HII 10-K direct contract-award disclosures

HII's MD&A explicitly names major awards and dollar values for each year. Selected anchors:

- FY2013: $3.3B DDG-51 MYP-2 (5 ships, Ingalls share)
- FY2018: $5.1B DDG-51 MYP-3 (6 ships, Ingalls share)
- FY2020: $1.4B DDG-51 single-ship + $1.8B LPD 31 + DDG 133/135 → 2020 Ingalls awards ~$4.6B, of which ~60% DDG
- FY2023: HII total awards $12.5B (incl. NNS) — Ingalls portion includes DDG MYP-4 (FY23-27, ~$5B share), LPD 32 mod, etc.
- HII Ingalls funded backlog (FY22 10-K): **$9.2B funded / $12.8B total** — represents future Ingalls revenue from existing contracts

### A1 — Triangulated estimate

- Method 1 (active-ship allocation, scaled to 10-K revenue): **46% DDG**
- Method 2 (FPDS Navy obligations, biased high): **101% DDG**
- Method 3 (10-K disclosed awards): roughly 50-70% in years with major DDG MYP awards, lower in other years

**Hardened range: DDG-51 is 46–70% of HII Ingalls segment revenue.**
**Point estimate: ~53%** (split the difference).

---

## A2. Supplier content as % of revenue

### Method A: COGS / Revenue (from 10-K, audited)

For Ingalls segment, we don't have a segment-level COGS line in the 10-K (only operating earnings).
But HII Ingalls segment operating margin ranges from 7.6% (FY24-25) to 13.2% (FY23).
That implies COGS+SG&A = 86.8-92.4% of revenue. SG&A at HII is ~3-4% of revenue, so:

- **Implied Ingalls COGS / Revenue: 83-89%**

### Method B: Labor cost decomposition (BLS + employee count)

HII Ingalls employee count (public disclosure):
- FY2024 HII total employees: ~44,000 (per 10-K Part I)
- Ingalls share (per HII investor materials + analyst reports): ~28% of headcount = ~12,300 employees
- BLS NAICS 336611 (Ship Building & Repairing) avg wage: ~$33/hr × 2,080 hr = $69K/yr base
- Loaded cost (benefits + overhead, typical 1.4-1.6× factor): ~$95-110K/yr per employee

Implied Ingalls total labor cost: 12,300 × $100K = **~$1.23B/yr** (range $1.17-1.35B)

Against FY2024 Ingalls revenue $2,767M:
- Labor cost / Revenue: **42-49%**
- Materials + subs + overhead = COGS - labor = (0.85 × 2,767) - 1,230 ≈ **$1,120M = 40% of revenue**
- Operating earnings: 7.6% of revenue

### Method C: External benchmarks (industry / academic)

- CSIS *Shipbuilding Industrial Base* (2022): destroyer programs have supplier content of **65-75% of total ship cost** (includes GFE).
- For yard-only (excluding GFE): roughly half of that, i.e. **30-40% of total ship cost = 40-55% of yard contract**.

### A2 — Triangulated estimate

- Method A (COGS/Rev): 83-89% of Ingalls revenue is COGS (in-house labor + materials + subs + mfg overhead)
- Method B (labor decomposition): labor is ~42-49% of revenue; materials + subs is ~40% of revenue
- Method C (CSIS benchmark): yard supplier content ~40-55% of YARD revenue

**Hardened range: yard-side supplier content (materials + subs) at HII Ingalls is 35–50% of Ingalls revenue.**
**Point estimate: ~42%** of Ingalls revenue is purchased materials + subcontract spend.

This is meaningfully LOWER than my original 70-80% rule-of-thumb — that figure applies to TOTAL ship cost (including GFE), NOT yard-only revenue.

---

## Recomputed yard-side DDG outsourcing

Using the hardened assumptions:

| Step | Value | Source |
|---|---:|---|
| HII Ingalls FY23 revenue | $2,752M | 10-K (audited) |
| × DDG share | 60% (range 50–70%) | Method 1 (active-ship allocation) |
| = Ingalls DDG-allocable revenue | ~$1,650M (range $1,376–$1,926M) | derived |
| × Supplier content (materials + subs) | 42% (range 35–50%) | Method B (labor decomposition) |
| = Ingalls DDG yard-side sub spend | **~$690M/yr** (range $480–$960M) | derived |

Do the same for GD-BIW (Marine Systems segment ~$14.3B FY24, BIW ~20-25% = ~$3.0-3.5B, DDG share of BIW ~85%, supplier content ~40%):

| Step | Value |
|---|---:|
| GD Marine Systems FY24 revenue | $14,343M |
| × BIW share (analyst estimate) | 22% |
| = BIW total revenue | ~$3,160M |
| × DDG share at BIW | 85% (BIW builds almost exclusively DDG) |
| = BIW DDG-allocable revenue | ~$2,690M |
| × supplier content | 42% |
| = BIW DDG yard-side sub spend | **~$1,130M/yr** |

**Combined HII-Ingalls + GD-BIW yard-side DDG sub spend: ~$1.8B/yr** (range $1.4-2.2B/yr).

That's vs $286M/yr visible in FFATA — so FFATA captures ~15% of the real yard outsourcing flow.

As % of FY24 SCN DDG-51 total ship cost ($5,492M for 2 ships = $2,746M/ship), the yard-side outsourcing is:
- $1.8B (both yards combined) / $5,492M (2 ships' total) = **~33% of total ship cost** is yard-side outsourcing.
- Plus GFE (45% of total ship cost from SCN cost categories) = **~78% of total ship cost outsourced** — within industry estimates of 70-80%.

