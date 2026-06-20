# Proposed Slide 8 - TAM Framing (MOCKUP - NOT YET DELIVERED)

**Status:** mockup / proposal. Not yet built in the deck.

**Purpose:** defensibility slide. Anticipates the reader question "Is
the $7.1B FY25 MRO TAM comparable to a contractor's FY25 revenue,
or does it overstate because multi-year task orders obligate lump-sum
in FY25 but deliver service across multiple years?" The answer: it
does overstate by ~2x under any reasonable POP-apportionment
assumption. Workbook intentionally uses Frame A (contracting
activity, $7.1B) because that is the industry convention for federal
contracting TAM; Frame B (revenue earned, ~$3.5B) is disclosed here
as a sensitivity so readers can translate between the two.

**Related methodology:**
`docs/methodology/METHODOLOGY_TAM_FRAMING.md` -- full analytical write-up
(5 apportionment methods, segment-level rates, contract-pricing-type
breakdown, data diagnostics that refute two earlier speculation errors).

---

## Title

TAM Framing | The $7.1B FY25 contracting-market TAM apportions to a
~$3.3-3.8B range of FY25-delivered contractor revenue under POP
apportionment; the workbook presents Frame A (contracting activity)
by convention

## Subtitle

FY2025 Services MRO TAM under alternative period-of-performance
apportionment methods ($M)

---

## Left visual - vertical bar chart (5 bars, ranked)

Frame A anchor bar on the left in dark navy (emphasis). Four Frame B
method bars to the right in slate-gray (sensitivity range). Horizontal
reference line at the central estimate (~$3.5B) across all four
Frame B bars to highlight the range.

| Method                              | FY25 $M | % of Frame A | Notes                                                                 |
|-------------------------------------|--------:|-------------:|-----------------------------------------------------------------------|
| **M5 Frame A - no apportionment**   | **7,067**| **100.0%**  | **FY25 contracting activity (workbook headline)**                     |
| M2 12-month POP cap                 |  3,747  |    53.0%     | Treat every award as 12-mo from start; upper Frame B bound            |
| M3 18-month POP cap                 |  3,499  |    49.5%     | Same but 18-mo                                                        |
| M1 Pure Linear                      |  3,354  |    47.5%     | Linear split of FY25 $ across actual POP; central Frame B estimate   |
| M4 Front-loaded 60/40               |  3,266  |    46.2%     | 60% over first 12mo, 40% over tail; lower Frame B bound               |

**Central Frame B estimate: ~$3.5B (49% of Frame A).**

## Right visual - apportionment rate by work segment

Segment-level linear apportionment rate, ranked from most to least
frame-sensitive. Shows where the gap concentrates.

| Segment                             | Frame A $M | Frame B M1 $M | Apport % |
|-------------------------------------|-----------:|--------------:|---------:|
| Port & Technical Services           |      431   |         307   |   71.3%  |
| Depot Ship Repair                   |    4,781   |       2,468   |   51.6%  |
| Hull, Mechanical & Electrical (HM&E)|      938   |         363   |   38.7%  |
| Electronics & C4ISR Sustainment     |      333   |         105   |   31.4%  |
| Combat Systems Sustainment          |      585   |         112   |   19.1%  |
| **Total**                           |  **7,067** |     **3,354** | **47.5%**|

Read: Combat Systems apportions at only 19% because Trident II /
AEGIS integration work runs on 5-10 year POPs (Draper MK7 LE2 alone
is $318M with POP starting FY24 and extending into FY29). Port &
Technical apportions at 71% because husbanding and QC work is
short-cycle and POP aligns with FY25.

## Callout (light-blue, italic, below the right table)

Note: Frame A (contracting activity) is the industry convention for
federal contracting TAM in PE / M&A / sell-side diligence. Frame B
(revenue earned) is closer to a contractor's reported P&L but is not
how federal markets are typically sized. Workbook stays on Frame A;
readers modeling a specific contractor can multiply the relevant
segment $ by the apportionment rate above for a first-order Frame B
estimate.

## Footnotes

- FY25 window: 2024-10-01 to 2025-09-30. POP apportionment uses
  `start_date` / `end_date` fields on FPDS award rows (100% populated).
- M1 Pure Linear is the primary Frame B estimate; M2-M4 are bounds.
  Range holds across any reasonable apportionment assumption.
- Two prior speculation errors are refuted by the data: (a) long-POP
  rows are NOT dominated by IDV parent-vehicle records (0 rows with
  `piid == parent_idv_piid` in the MRO universe), so linear rate is
  not artificially depressed; (b) front-loading the apportionment
  curve *lowers* Frame B rather than raising it, because the gap is
  driven by contracts that started in FY22-FY24 and extend into FY25,
  not by contracts starting within FY25.
- True Frame B would require contractor-side billing / earned-value
  data unavailable in federal sources. POP apportionment is a
  directional sensitivity.
- Source: FPDS FY2025 contract obligations (U.S. Navy + U.S. Coast
  Guard, 65 services PSCs, post-exclusions). Period-of-performance
  dates per FPDS. Data as of April 2026.

---

## Why this slide (audience motivation)

A diligent reader looking at Slides 1-4 will ask:

- "Your $7.1B TAM is an annual market-activity number. If I'm modeling
  a specific contractor's FY25 revenue, is that the same thing?"
- "Multi-year IDIQs obligate lump-sum and deliver over years -- does
  your FY25 obligation double-count that service delivery?"
- "What's the sensitivity to how you handle period-of-performance?"

This slide answers all three on one page. The central finding -
~$3.5B FY25 revenue-delivered estimate, roughly half of Frame A -
is directionally the same under every plausible apportionment
method, so the sensitivity is well-bounded even if POP dates are
imprecise.

## Build-out assets available

No workbook changes were made for this slide; the analysis lives in
`docs/methodology/METHODOLOGY_TAM_FRAMING.md` and the supporting
script `compute_tam_revenue_gap.py`. If the slide moves to delivery,
the Services sheet already carries `NAVY_TAM_SVC` + `CG_TAM_SVC`
defined cells for the Frame A anchor; Frame B values would need to be
baked into the slide as static numbers (or added as a small sensitivity
block on Services, a deliberate choice we did NOT make to keep the
workbook scope-paring direction honest).

---

## What does NOT belong on this slide

- Contractor-level Frame A vs Frame B rankings (would require per-row
  apportionment join to the contractor rollup -- larger rework).
- Budget-authority cross-reference (lives on Slide 5 Appropriation
  Sourcing; different question).
- Public-yard labor reconciliation (Slide 7 territory).
- Year-over-year Frame B trend (would require re-apportioning FY24
  and FY23 Awards data, not currently loaded).

## Status

Draft only. When the actual slide is designed in the deck app and a
screenshot is captured to `deck/`, move the content into `DECK.md` as
the new Slide 8 section (in the same prose-transcription style as
Slides 1-4) and delete this mockup file.
