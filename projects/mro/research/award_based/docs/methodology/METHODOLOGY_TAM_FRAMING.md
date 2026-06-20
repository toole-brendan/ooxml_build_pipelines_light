# Methodology: TAM Denominator Framing -- Contracting Activity vs Revenue Earned

**Status**: resolved 2026-04-18. Frame A (FY25 contracting activity,
$7.1B) is the workbook's primary TAM. This doc records the decision
plus the Frame B (FY25 revenue earned) sensitivity so readers can
translate between the two frames without redoing the apportionment
calculation. The workbook and deck are not modified; the sensitivity
lives only in this file.

**TL;DR**:
- Frame A (contracting activity, $7,067M) is the primary TAM. Every
  sheet and slide is computed under this frame.
- Frame B (FY25 service delivery / revenue earned) = **$3.27-3.75B
  across five plausible POP-apportionment methods**. Central estimate
  **~$3.5B / ~49%** of Frame A.
- The gap (~$3.3-3.8B, ~47-54% of Frame A) is real and driven by
  multi-year task orders whose FY25-dated obligations deliver service
  into FY26+. It is not a data error or coverage failure.

---

## The two framings

### Frame A: FY2025 contracting market activity

The $7,067M is the **net dollar value of contract mod actions dated
within FY25** on 65 MRO PSCs, post-exclusions. It reflects the
government's awarding decisions during FY25 -- what contractors
competed for, what primes won, what market share landed where.

- **Unit**: FY25-dated obligation transactions (net of positive mods
  and any de-obligations), aggregated by PIID -> PSC -> vessel ->
  contractor.
- **Answers**: "How big was the Navy + Coast Guard MRO contracting
  market in FY2025?"
- **Serves**: investors, acquirers, BD / capture teams sizing the
  annual awardable opportunity; market-share rollups; YoY trend
  tracking of awarding activity.
- **Why $7.1B is the right number under this frame**: FPDS FY25
  Obligation is exactly this -- all mod actions dated FY25, summed.
  No adjustment.

### Frame B: FY2025 contractor revenue earned (service delivered)

The $7.1B overstates contractor revenue earned in FY25 because a
meaningful portion of FY25-dated obligations fund multi-year task
orders whose actual service delivery -- and therefore contractor
revenue recognition -- extends into FY26+.

- **Unit**: value of service delivered within FY25, regardless of
  when the backing obligation was recorded.
- **Answers**: "How much revenue did MRO contractors recognize in
  FY2025?" Or "What was the P&L-relevant market size?"
- **Serves**: equity research analysts building contractor models;
  investment committees comparing FY revenue vs FY market size;
  anyone benchmarking against public-company segment revenue.
- **Adjustment needed**: apportion each PIID's FY25 obligation
  across its period-of-performance (POP) span.

---

## Frame B quantified

Every Services row in the Awards master (MRO PSC + shore/base
exclusions applied) carries `start_date` and `end_date` fields from
the FPDS pull -- 100% populated in the current dataset. That lets
us compute per-row FY25-delivered $ under several POP-apportionment
assumptions and see how much the answer moves.

### Five apportionment methods

FY25 window: 2024-10-01 to 2025-09-30.

| Method | Description | FY25 $M | % of Frame A |
|---|---|---:|---:|
| **M5 Cliff (Frame A)** | No apportionment. FY25-delivered = FY25 obligation. | **7,067** | **100.0%** |
| **M2 12-month cap** | Treat every award as if its effective POP is min(actual POP, 12 months) from start_date. Linear thereafter. | **3,747** | **53.0%** |
| **M3 18-month cap** | Same but cap at 18 months. | **3,499** | **49.5%** |
| **M1 Pure Linear** | Apportion each row's FY25 $ by (overlap days between POP and FY25 window) / (total POP days). | **3,354** | **47.5%** |
| **M4 Front-loaded 60/40** | 60% of value delivered linearly across first 12 months, 40% linearly over remainder. | **3,266** | **46.2%** |

**Range**: $3,266M - $3,747M. **Central estimate ~$3.5B / ~49% of Frame A.**

### By POP bucket

| POP Bucket | Rows | Frame A $M | M1 $M | M2 $M | M3 $M | M4 $M |
|---|---:|---:|---:|---:|---:|---:|
| <=13 months | 7,366 | 3,172 | 2,036 | 2,039 | 2,036 | 2,002 |
| 13-24 months | 551 | 2,208 | 897 | 1,262 | 990 | 866 |
| 2-5 years | 509 | 986 | 300 | 442 | 363 | 336 |
| >5 years | 140 | 699 | 122 | 5 | 111 | 62 |
| negative POP (data errors) | 6 | 1 | 0 | 0 | 0 | 0 |
| **Total** | **8,572** | **7,067** | **3,354** | **3,747** | **3,499** | **3,266** |

Read: short-POP (<=13 month) awards carry $3,172M of FY25 obligation
and apportion to ~$2,036M of FY25 delivery under linear -- a
65% apportionment rate, consistent with POP straddling FY24->FY25 or
FY25->FY26 halves. Long-POP awards (>2 yr) carry $1,685M of FY25
obligation and apportion only ~$422M to FY25 delivery under linear,
because most of their POP sits outside the FY25 window.

### By work segment

| Segment | Frame A $M | M1 $M | M1 % | M2 $M | M2 % |
|---|---:|---:|---:|---:|---:|
| Depot Ship Repair | 4,781 | 2,468 | 51.6% | 2,913 | 60.9% |
| Hull, Mechanical & Electrical (HM&E) | 938 | 363 | 38.7% | 394 | 42.1% |
| Combat Systems Sustainment | 585 | 112 | 19.1% | 34 | 5.8% |
| Port & Technical Services | 431 | 307 | 71.3% | 307 | 71.3% |
| Electronics & C4ISR Sustainment | 333 | 105 | 31.4% | 99 | 29.6% |

Notable:
- **Port & Technical Services** is ~71% apportioned under linear -
  husbanding + QC + tech-rep work is short-cycle, POP aligns with FY25.
- **Depot Ship Repair** is ~52% apportioned - standard 12-18 month
  availability cycle means a typical TO straddles one fiscal year
  boundary, cutting the FY25 share roughly in half.
- **Combat Systems Sustainment** is only ~19% apportioned because
  of multi-year Trident II / AEGIS integration work. Draper MK7
  LE2 alone ($318M FY25 obligation, >5 year POP) accounts for most
  of the low apportionment rate in this segment.
- Under M2 (12-month cap), Combat Systems drops further (19% -> 6%)
  because the cap puts the effective POP entirely pre-FY25 for awards
  with FY20-FY22 starts. The 12-month cap assumption doesn't hold
  for these contracts.

### By contract pricing type

Revenue recognition rules differ by pricing type, so this matters
for interpreting Frame B:

| Pricing | Rows | Frame A $M | M1 $M | M1 % |
|---|---:|---:|---:|---:|
| Firm Fixed Price (FFP) | 7,816 | 5,285 | 2,804 | 53.1% |
| Cost-reimbursable | 701 | 1,734 | 515 | 29.7% |
| Other Fixed Price | 45 | 42 | 34 | 80.2% |
| T&M / Labor Hours | 10 | 6 | 2 | 26.6% |

For **FFP contracts**, revenue is recognized as performance
milestones are met (percent-of-completion or delivery-based). Linear
POP apportionment is a crude proxy but directionally reasonable
because milestone billing usually tracks the POP.

For **cost-reimbursable contracts** (~25% of the Frame A $), revenue
recognizes as costs are incurred -- which typically front-loads
material purchases and ramp-up labor. Cost-reimb awards in the MRO
dataset skew long-POP (multi-year engineering and integration work),
pulling the linear apportionment rate down to 30%. For this slice,
linear under-represents FY25-delivered revenue somewhat because real
cost incurrence is likely higher early in a multi-year contract.

T&M / Labor Hours is a negligible slice (<$10M).

### Sanity checks

- **Missing POP dates**: 0 rows. All 8,572 Services rows with positive
  FY25 obligation have both start_date and end_date populated.
- **Negative POP (end before start, data errors)**: 6 rows / $1M.
  Negligible; apportioned to 0 under every method.
- **Start date > FY25 end**: 134 rows / $322M. These are awards whose
  FY25-dated obligation corresponds to work starting in FY26+ -
  typical for lump-sum-funded multi-year task orders. Apportioned to
  $0 under linear (correctly).
- **End date < FY25 start**: 166 rows / $14M. Cleanup obligations on
  already-completed work. Apportioned to $0 under linear (correctly).

### IDV-parent diagnostic

An earlier version of this doc speculated that the long-POP buckets
might be dominated by IDV *parent* records -- 5-10 year parent
vehicle POPs disguising short-term individual TO durations, which
would artificially depress the linear apportionment rate.

The data refutes this.

Rows where `piid == parent_idv_piid` (the signature of an IDV parent
record): **0 rows, $0M** across the entire MRO dataset. The
Awards master loader consumes the per-hull explosion from
`vessel_explode_v2.py`, which emits task-order / standalone-award
rows; it does not carry IDV parent-vehicle records.

Sample of the 10 largest >5-year-POP rows (confirming they are real
long-duration work, not IDV artifacts):

| PIID | FY25 $M | Recipient | Description |
|---|---:|---|---|
| N0003024C6001 | 318 | Draper Lab | MK7 LE2 SYSTEM REQUIREMENTS FY25 (Trident II) |
| N0002422C5231 | 56 | Leidos | SPARES & TACTICAL TRAINING EQUIPMENT |
| N0002418C6258 | 49 | Lockheed Martin | Combat system integration - delivery change |
| N0002420C4315 | 33 | Oceaneering | MGMT, ENG, TECH & LOGISTIC SUPP SERVICE |
| N0002421C5393 | 25 | BAE Systems | Material to support Item 1304 |
| N0002418C6413 | 20 | Oceaneering | DDS-02P ROH, TCHA, AND FIELD CHANGES |
| N0002421C2443 | 17 | HII | Industrial Post-Delivery Avail execution LP |
| N0002422C6418 | 16 | Northrop Grumman | Ceiling holder |
| N0002420C5603 | 16 | GD Mission Systems | Combat system development & integration |
| N0002420C5601 | 15 | Lockheed Martin | Combat system development & integration |

These are legitimate multi-year sustainment, integration, and
engineering-support contracts. The low linear apportionment rate for
long-POP rows is the correct Frame B answer, not an artifact to be
corrected.

### Front-loading direction

An earlier version of this doc speculated that a front-loaded
apportionment heuristic (more delivery in the first 12 months, less
in the tail) would *raise* Frame B above the pure-linear baseline.

The data refutes this too.

M4 Front-loaded 60/40 produces **$3,266M**, below M1 Pure Linear's
$3,354M. The reason: front-loading benefits contracts whose POP
*starts* within FY25. But the apportionment gap is driven by
contracts that started in FY22-FY24 and extend into FY25. For those,
front-loading pulls more delivery into the pre-FY25 segment of the
POP, *reducing* the FY25 share.

The range of plausible Frame B estimates therefore runs roughly
$3.27B to $3.75B, with the upper bound set by the 12-month POP cap
(M2), not by front-loading.

---

## Use cases per frame

| Use case | Frame A ($7.1B) | Frame B (~$3.5B) |
|---|:---:|:---:|
| "How big is the annual U.S. Navy + USCG MRO contracting market?" | **Yes** | No |
| "What did Navy + USCG award in FY2025?" | **Yes** | No |
| Market-share analysis (prime x PSC x FY) | **Yes** | Distorted |
| Year-over-year trend of awarding activity | **Yes** | Noisy |
| Contractor revenue-model calibration / benchmarking | Overstates | **Yes** |
| Comparison to public-company disclosed segment revenue | Overstates | **Yes** |
| Headline for an investor / M&A / sell-side deck | **Yes** | Unusual frame |

Frame A is the **contracting-market** frame. It is what the rest of
the workbook is built around (Services TAM, Product Procurement TAM,
contractor rankings by FY25 $M, the 7-slide deck, subcontracting
roll-ups). The TAS / appropriation attribution in Budget Anchors
(37.7% OMN + 35.6% OPN + 10.9% RDT&E-DW + seven smaller accounts =
$7.4B total) is measured on the same obligation base as Frame A and
reconciles to it by construction.

Frame B is the **revenue-recognition** frame. It is what a
traditional sell-side equity research / industry-analysis model
would produce. It is more rigorous for comparing to public-company
reported revenue but is not how federal-contracting TAM is typically
framed in investor pitches or market studies.

---

## Decision

**Frame A is the workbook's primary TAM.** All sheets, slides, and
derivative analyses continue to compute on FY25 obligation without
POP apportionment. Rationale:

1. **Industry convention.** PE / M&A / sell-side memos for federal
   contracting targets use contracting activity as TAM. Investor
   audiences expect this framing.
2. **Rework cost.** Switching to Frame B would require every SUMIFS
   in the workbook to become a SUMPRODUCT or precomputed per-row
   apportioned column on Awards. Contractor rankings shift (primes
   on long-POP Combat Systems work rank lower under Frame B); YoY
   trend tracking gets noisier; the deck narrative changes.
3. **Defensibility addressed here.** This document records the Frame
   B sensitivity ($3.3-3.8B range) for readers who need to translate
   between frames.

Readers needing a revenue-recognized number for a specific
contractor or segment should start from the Frame A figure on the
relevant sheet and apply the segment's M1 apportionment rate from
the table above (e.g., multiply Depot Ship Repair $M by 0.52 for
a first-order Frame B estimate).

---

## Reproducing the numbers

The computation lives in `/tmp/compute_tam_revenue_gap.py` (scratch).
Pattern:

```python
from domnann.sheets.awards import load_rows
from domnann.sheets.services import MRO_PSCS, SERVICE_CONDENSED_GROUPS

rows = load_rows()  # applies is_shore_base_excluded
mro_rows = [r for r in rows if (r.get('psc_code') or '') in set(MRO_PSCS)]

# Parse start_date / end_date per row; compute per-method FY25-delivered $
# against FY25 window (2024-10-01 to 2025-09-30).
```

Key inputs:
- `data_pull/output/fpds/navy_awards_master.json`
- `data_pull/output/fpds/cg_awards_master.json`
- `sheets/services.py::MRO_PSCS` (65 PSCs)
- `sheets/services.py::is_shore_base_excluded`
- `sheets/services.py::SERVICE_CONDENSED_GROUPS` (work-segment map)

Output headline numbers will shift by <$200M on any Awards refresh;
the ranges and bucket structure are stable.

---

## Related constructs and limitations

**FPDS "Obligation" is not "Expenditure".** Obligation = legal
commitment of funds (contract signed, money earmarked for payment
when performance is met). Expenditure = actual cash paid. Frame B
approximates expenditure from obligation data via POP apportionment;
Treasury DAIMS disbursement filings would be closer to expenditure
truth but are not joined into this workbook. The TAS attribution
pulled via USAspending in session (v) reports obligation flows per
federal account, not disbursements, so it sits on the Frame A side
of the obligation / expenditure divide.

**Contractor revenue recognition** differs from expenditure for
most contracts. FFP: revenue recognized as performance milestones
are met or as deliveries occur. Cost-reimbursable: revenue
recognized as costs are incurred. T&M: revenue as hours billed.
None of these mirror FPDS obligation directly. POP apportionment is
a crude proxy across all three.

**POP date quality.** `start_date` / `end_date` on FPDS award rows
are populated 100% of the time in the MRO dataset but can be
imprecise. Some PIIDs may report the parent vehicle's POP rather
than the individual task-order POP (though the IDV-parent diagnostic
above rules this out as a dominant factor). The 140 rows in the
>5-year bucket are real long-duration sustainment contracts per the
spot-check. POP dates on newly-awarded FY25 contracts may still be
revised in subsequent mods.

**True Frame B would require contractor-side data.** POP apportionment
is a directional sensitivity, not a substitute for actual billing /
earned-value data that only the contractors themselves have.
Contractor 10-K segment disclosures are the closest public proxy and
align better with Frame B than Frame A when compared directly.

---

## Cross-references

- `METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` -- per-appropriation
  attribution of the FY25 MRO $ (measured via TAS). Obligation-side
  breakdown; sits under Frame A.
- `METHODOLOGY_CVN_SSN_COVERAGE.md` -- parallel discussion of
  multi-year SCN obligation vintage dynamics on the newbuild side.
- `docs/planning/PLAN_BROADER_BUDGET_ANCHORS.md` -- plan for
  extending TAS attribution into the workbook; independent of this
  frame question.
- Workbook sheets `Services`, `Depot Ship Repair`, `Sub & Carrier
  Coverage` all compute under Frame A. None are modified by this
  document.
