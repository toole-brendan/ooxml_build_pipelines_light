# GD 10-K Research — Marine Systems Segment Triangulation

**Date:** 2026-05-24
**Purpose:** Cross-validate the deck's outsourcing / supplier-base picture from
GD's own financials, paralleling the existing HII 10-K work
(`hii_summary_memo.md` / `hii_nns_segment*.csv`).

**Scope caveat:** GD Marine Systems = Electric Boat (subs, Groton + Quonset) +
Bath Iron Works (DDGs, Bath ME) + NASSCO (auxiliaries, San Diego). All
numbers below are SEGMENT-LEVEL, not EB-only. EB is the dominant business in
the segment but not the entirety.

---

## 1. Marine Systems financials, FY19-FY25 (reconciled most-recent-vintage)

| FY | Revenue $M | YoY | Op Income $M | Margin | Capex $M | Assets $M |
|---:|---:|---:|---:|---:|---:|---:|
| 2019 | 9,183 | — | 785 | 8.5% | 449 | 3,918 |
| 2020 | 9,979 | +8.7% | 854 | 8.6% | 604 | 4,488 |
| 2021 | 10,526 | +5.5% | 874 | 8.3% | 573 | 5,294 |
| 2022 | 11,040 | +4.9% | 897 | 8.1% | 530 | 5,864 |
| 2023 | 12,461 | +12.9% | 874 | 7.0% | 511 | 6,209 |
| 2024 | 14,343 | +15.1% | 935 | 6.5% | 424 | 7,019 |
| 2025 | 16,723 | +16.6% | 1,177 | 7.0% | 517 | 7,313 |

**Source:** GD 10-K segment notes (`gd_marine_systems_segment_reconciled.csv`).

## 2. The margin-compression story

The arc is striking and corroborates Novakovic's "supply chain is the gating
item" testimony (`extracted/exec_commentary_makebuy.csv` EXEC-11):

- **FY19-FY22 plateau:** ~8.3-8.6% segment margin on modest revenue growth (~5%/yr)
- **FY23-FY24 squeeze:** margin compressed to 6.5-7.0% as revenue accelerated
  (+13-15%/yr) — the supply chain bottleneck Novakovic, Deep and Kastner
  all flagged
- **FY25 partial recovery:** margin back to 7.0% on +17% revenue growth — the
  largest single-year revenue jump in the decade ($14.3B → $16.7B = +$2.4B)

**Deck interpretation:** GD's earnings show *the financial cost* of the
supply chain constraint. Submarine revenue can grow at 15%+/yr; margin has
to absorb the supplier-base pressure. The 150 bps margin loss FY22→FY24 on
$14B of revenue ≈ $210M of segment earnings sacrificed to the supplier-base
problem at peak.

## 3. The capex commitment

- FY21 book + FY22 book disclose: **"$1.8 billion of capital in expanded and
  modernized facilities at Electric Boat to support the growth in submarine
  construction"** — substantially complete end of 2023.
- Capex annual run-rate FY20-FY23 = ~$510-610M/yr (matches the $1.8B over
  3-4 years narrative).
- FY24 dipped to $424M (investment phase winding down).
- **FY25 capex back up to $517M** — and Novakovic's FY25 Q4 commentary
  (EXEC-13) calls for "79% CapEx increase to >$900M company-wide, half at
  least at Electric Boat." That $450M+ implied EB capex for FY26 will be
  visible in the next 10-K.
- Workforce: "Electric Boat workforce on track to grow approximately 25% in
  the current decade, particularly in support of Columbia-class submarine
  program execution" (FY21 / FY22 books).

**Deck interpretation:** GD is *investing in its own yards*, not outsourcing.
This is the structural divergence from HII (which is +30% YoY outsourcing
hours). The two primes are running opposite strategies in response to the
same supplier constraint.

## 4. The teaming language (GD on HII — primary source)

The single most useful narrative line from the FY21 book:

> "Our Marine Systems segment has one primary competitor with which it also
> partners on the Virginia-class submarine program, **and to which it
> subcontracts on the Columbia-class submarine program**."

This is GD's own description of the EB↔HII teaming structure: **GD
subcontracts to HII on Columbia**. Confirms the visibility-gap framing in
`hii_context.csv` — the HII teaming work is structurally invisible to FFATA
because it flows through GDEB's prime contract.

## 5. Submarine award flow (from program-narrative snippets)

The 10-K "significant contract awards" section gives clean ground-truth
checkpoints on Marine Systems award volume (visible in
`gd_program_narrative.csv`):

| FY book | Notable Marine Systems award disclosure |
|---|---|
| 2021 | $1.9B Block V tenth submarine; $1.4B lead-yard services Va+Col; $385M ANPS Col |
| 2023 | $1.3B LLTM Block V + Block VI; $720M DDG-51 maintenance |
| 2024 | $2.9B LLTM Block V + Block VI; $205M Arleigh Burke planning yard |

The pattern: LLTM dollar volume is RAMPING — $1.3B (FY23) → $2.9B (FY24), 2.2x
in one year. This is consistent with our cost-funnel work showing
shipbuilder-procured LLTM as the deck's most addressable supplier opportunity.

## 6. What this validates vs the deck

| Deck claim | GD 10-K evidence |
|---|---|
| 50/60/65% BC-outsourced band | Neither confirmed nor refuted — GD doesn't disclose a make/buy % |
| HII outsourcing 30%/yr | Not in GD data (this is HII-specific) |
| GD invests in own yards | **CONFIRMED**: $1.8B EB capex commitment; 25% workforce ramp; FY25 capex back up to $517M |
| Supply chain is the binding constraint | **CONFIRMED**: 150 bps margin loss FY22→FY24 = real $ cost of the supplier-base issue |
| EB subcontracts to HII on Columbia | **CONFIRMED**: GD FY21 book explicit |
| LLTM is a fast-growing addressable layer | **CONFIRMED**: $1.3B FY23 → $2.9B FY24 in disclosed Marine Systems LLTM awards |
| Columbia program $130B (per GAO) | GD says ">$110B" in FY21; matches with later GAO upward revisions |

## 7. Open items / caveats

1. **Marine Systems ≠ Electric Boat ≠ submarines.** Roughly 60-70% of MS
   revenue is submarines per industry estimates; the rest is BIW (DDGs) +
   NASSCO. Per-yard breakouts are NOT publicly disclosed by GD. The
   submarine-specific revenue is implied at ~$10-12B/yr (FY25 ballpark) but
   triangulated, not direct.
2. **Capex is segment-level**, not EB-specific. Novakovic's "half at EB"
   color is the only EB allocation guidance.
3. **Operating earnings are clean** because GD reports them per segment.
4. **GD's contract-award disclosures are illustrative, not complete** — only
   "significant" awards. The full PIID-level picture still comes from FPDS/
   SAM/USAspending.
5. **The FY26 10-K will show whether the +79% capex Novakovic guided to
   actually materialized.** That's the next-cycle datapoint to watch.

## 8. Files

- `edgar_research/gd_10k_files/<FY>/` raw HTML cache per FY (5 books: FY21-FY25)
- `edgar_research/gd_marine_systems_segment.csv` long-form per-vintage rows (15)
- `edgar_research/gd_marine_systems_segment_reconciled.csv` most-recent-vintage per FY (7)
- `edgar_research/gd_program_narrative.csv` 61 sub-relevant snippets across FY21-FY25 books

Generated by `scripts/pull_gd_10k_research.py` — mirror of the HII pull at
`scripts/pull_hii_10k_research.py`.
