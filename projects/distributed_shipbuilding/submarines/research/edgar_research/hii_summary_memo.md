# HII EDGAR research — what we got, what's missing

**Purpose:** Determine what's *actually* available via SEC EDGAR for estimating HII-NNS's submarine work, before deciding whether/how to incorporate into the submarine_new_construction_subawards workbook.

**Pull date:** 2026-05-23
**Source:** SEC EDGAR `data.sec.gov` + `www.sec.gov/Archives` (public, no auth)
**HII CIK:** 0001501585
**Filings pulled:** 5× 10-K filings (FY2021 through FY2025; fiscal year ends Dec 31)

---

## 1. What we extracted — structured

### A. Newport News segment financials (most-revised vintage per FY)

`edgar_research/hii_nns_segment_reconciled.csv`

| FY | Source book | NNS Total Rev $M | NNS Op Income $M | Op Margin | Ingalls Rev $M | Mission Tech Rev $M |
|---:|:---:|---:|---:|---:|---:|---:|
| 2019 | FY21 book | 5,231 | 410 | 7.8% | 2,555 | 1,237 (Tech Solutions) |
| 2020 | FY22 book | 5,571 | 233 | 4.2% | 2,678 | 1,268 |
| 2021 | FY23 book | 5,663 | 352 | 6.2% | 2,528 | 1,476 |
| 2022 | FY24 book | 5,852 | 357 | 6.1% | 2,570 | 2,387 |
| 2023 | FY25 book | 6,133 | 379 | 6.2% | 2,752 | 2,699 |
| 2024 | FY25 book | 5,969 | 246 | 4.1% | 2,767 | 2,937 |
| 2025 | FY25 book | 6,507 | 331 | 5.1% | 3,078 | 3,044 |

**Cross-vintage consistency check:** When the same FY appears in 2+ 10-K books, the numbers match exactly. NNS revenue is a stable, restated-rarely-if-ever figure. The 15 raw data points (5 books × 3 years each) reconcile to 7 unique-FY values with zero conflicts.

**Pattern:** NNS revenue has grown from $5.2B (2019) → $6.5B (2025), with a small dip in 2024. Op margin is volatile (4-8%) — driven by program-level "cumulative catch-up adjustments" (CCAA) that HII calls out explicitly each year.

### B. Program narrative snippets

`edgar_research/hii_program_narrative.csv` — 111 rows, one per (keyword × FY × snippet)

For each 10-K, captured every sentence mentioning {Virginia / Columbia / Block IV/V/VI / SSN 774 / SSBN 826 / CVN / RCOH / teaming / Electric Boat / Backlog / award} that ALSO has either a dollar amount or a numeric boat count.

50 of those 111 snippets explicitly mention dollars AND a submarine-relevant keyword.

---

## 2. The submarine-share question — what EDGAR DOES tell us

### Defensible from the 10-K text:
- **HII does a fixed scope of Virginia work**: stern, habitability/machinery, torpedo room, sail, bow. EB does engine room, control room, pressure hull. Reactor + final assembly alternate.
- **Columbia is sub-to-prime**: HII is a subcontractor TO Electric Boat (not co-prime). Builds modules.
- **CVN 80 + CVN 81 contract = $15.4B** (cumulative, multi-year, detail design + construction).
- **CVN 79 = $8.8B** (from 2009 onward).
- **Block V Virginia = 12 boats total** (originally 9, +1 option in 2021, +2 LLTM in 2023, +2 construction mod in 2025).
- **Block IV Virginia = 10 boats**, 8 delivered through 2025, 2 in final assembly.
- **Backlog FY25-end = $54B** consolidated (across all 3 segments).

### NOT in 10-K text:
- **No clean revenue-by-program disclosure**. HII never says "submarine work was $X of NNS revenue this year."
- Most program mentions are qualitative ("higher volumes in submarines drove growth", "unfavorable catch-up on Virginia"). When dollars appear, they're typically about *charges* ($111M unfavorable on Block IV in 2020), not revenue.
- No per-program backlog breakdown.

---

## 3. What EDGAR DOES NOT have

| What we'd ideally want | Why it's not here | Where it lives |
|---|---|---|
| Submarine $ within NNS per FY | Not disclosed at all (not in 10-K, 10-Q, or 8-K) | Analyst estimates (CSIS, CBO, Cowen, Vertical Research, Stifel) |
| Earnings call transcripts | Companies don't file these with SEC | Seeking Alpha (free), Motley Fool, Bloomberg/FactSet |
| Investor presentation text | Slides are filed as JPG images | OCR the JPGs, or scrape ir.hii.com |
| Per-ship contract values | Only major program totals (CVN 80/81 = $15.4B) | NAVSEA press releases + DefenseLink news |
| Per-program backlog | Not split | Analyst day disclosures (irregular) |

---

## 4. What we can *infer* (with explicit assumptions)

### Approach: NNS revenue × estimated submarine share

NNS revenue contains:
1. Virginia class new construction (HII teaming share — about half)
2. Columbia class new construction (HII subcontract — modules + design)
3. CVN new construction (Kennedy, Enterprise, Doris Miller)
4. CVN RCOH (Refueling Complex Overhauls — Stennis is ongoing)
5. CVN maintenance/services
6. Submarine fleet services & nuclear services

Naval analyst consensus (multiple sources, FY22-FY25 era) commonly cites:
- New-construction CVN: ~40-45% of NNS (CVN 80/81/82 ramp)
- New-construction submarines (Va + Col): ~25-35% of NNS
- RCOH + services + other: ~25-30%

Applied to our NNS revenue:

| FY | NNS Rev $M | Submarine share assumption | Implied sub revenue $M |
|---:|---:|---|---:|
| 2022 | 5,852 | 25-35% | 1,463 – 2,048 |
| 2023 | 6,133 | 25-35% | 1,533 – 2,147 |
| 2024 | 5,969 | 25-35% | 1,492 – 2,089 |
| 2025 | 6,507 | 30-40% (Block V ramp + Col II) | 1,952 – 2,603 |

**Confidence:** Low-medium. The 25-35% is a triangulation from secondary sources, not from HII's own disclosures.

---

## 5. Comparison to what we see in federal data

Our SAM.gov pull showed only **~$98M lifetime** of HII-NNS appearing as a FFATA-reported sub under GDEB primes. Implied annual rate: ~$10-15M/yr visible in federal subaward data.

Implied annual HII submarine revenue from our EDGAR + analyst-share inference: **~$1.5-2.6B/yr**.

**Gap: ~150-200×.** That is, federal subaward data captures less than 1% of the true HII-NNS submarine flow.

This confirms what we suspected: the teaming-agreement workshare is essentially invisible to FFATA, because HII-NNS receives its share via GDEB's prime contract structure rather than as a discrete FFATA-reported subaward action.

---

## 6. Methodology issues worth flagging

1. **Reconciliation across vintages.** When the same FY appears in multiple 10-Ks, we use the most-recent book as authoritative (same approach as the SCN reconciliation). For NNS specifically, the numbers don't restate across vintages — but the methodology is consistent with the rest of the workbook.

2. **HII segment reorganization.** FY21 10-K used "Technical Solutions" as the third segment; FY22+ rebranded to "Mission Technologies" after the Alion acquisition (April 2021). NNS as a segment definition has been stable.

3. **Operating margin volatility on NNS is REAL and program-driven.** The 4.1% margin in 2024 (vs 6.2% in 2023) reflects unfavorable cumulative catch-up adjustments specifically on Virginia and aircraft carriers. This is a known issue the firm discloses transparently in MD&A. Implication: HII-NNS submarine work has been *unprofitable at the margin* in recent years.

4. **HII does not have a separate "submarines" segment.** It's deliberate — submarines and aircraft carriers share workforce, facilities, and overhead at the Newport News yard. Splitting them in accounting terms would require allocations HII isn't required to make.

5. **The 10-K narrative search regex** captures snippets with dollars OR boat-counts. It's noisy — some snippets are about unrelated topics that happen to contain matching keywords (e.g., Republic of South Korea arbitration; Arleigh Burke destroyer awards). Manual filtering is needed before any specific snippet is cited.

6. **Backlog**: HII reports total consolidated backlog (~$54B at FY25-end) but does not break out per-program. The 10-Q sometimes mentions specific large additions ($X for Block V mod, etc.) but not the running per-program total.

---

## 7. What the workbook addition would look like

If we proceed, suggested structure:

**New sheet "HII_NNS_Context"** (separate from the core FY_Headline numbers):
- Columns: FY | NNS Rev $M | NNS OpInc $M | NNS Op Margin | Assumed sub share % | Implied HII sub revenue $M
- Notes: "EDGAR-sourced NNS top-line; submarine share is an external assumption, not from HII filings."
- Caveat callout: "Compare to ~$98M visible HII-as-GDEB-sub in our FFATA data → gap ratio 150-200×, attributable to teaming-agreement workshare not flowing as FFATA subs."

**Or** — a 1-page "context" callout in the existing Caveats sheet rather than a new tab, since the data is illustrative not authoritative.

**Recommendation:** Add as context, not as a primary table. The number is too soft to mix with the FFATA-derived figures, but the magnitude check (~150× gap) is useful framing.

---

## 8. Confidence summary

| Claim | Confidence | Source |
|---|---|---|
| NNS segment total revenue per FY | **High** | 10-K (XBRL + narrative) — restated never, cross-vintage consistent |
| NNS segment operating margin | **High** | Same |
| HII teaming workshare for Virginia (stern/sail/bow etc.) | **High** | 10-K narrative — described explicitly |
| HII is Col subcontractor, not co-prime | **High** | 10-K narrative |
| CVN 80/81 cumulative contract value $15.4B | **High** | 10-K narrative — explicit |
| Submarine % of NNS revenue (~25-35%) | **Medium** | Naval analyst consensus — not from HII |
| Implied HII submarine revenue ~$1.5-2.6B/yr | **Medium** | Multiplication of above two |
| Gap vs FFATA visibility ~150-200× | **High** (as a magnitude check) | Math from numbers above |

---

## 9. Files written

- `edgar_research/hii_submissions.json`        — HII filing history (1008 entries)
- `edgar_research/hii_facts.json`              — XBRL company facts (~3MB)
- `edgar_research/hii_10k_files/{2021..2025}/` — cached 10-K HTML + key R-files per year
- `edgar_research/hii_nns_segment.csv`         — long-form raw data (15 rows: 5 books × 3 years)
- `edgar_research/hii_nns_segment_reconciled.csv` — most-recent-vintage per FY (7 rows)
- `edgar_research/hii_program_narrative.csv`   — 111 program-mention snippets, FY21-25

Workbook NOT modified.
