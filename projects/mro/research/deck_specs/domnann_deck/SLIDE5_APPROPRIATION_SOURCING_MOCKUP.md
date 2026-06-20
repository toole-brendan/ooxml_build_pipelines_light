# Proposed Slide 5 - Appropriation Sourcing (MOCKUP - NOT YET DELIVERED)

**Status:** mockup / proposal. Not yet built in the deck. Supersedes
the earlier "Slide 3 Budget-Book Anchor callout" augmentation proposal
(folded here into its own standalone slide).

**Purpose:** defensibility slide. Anticipates the reader question "the
Navy's OMN 'Ship Maintenance By Contract' line item is only $2.4B FY25
- how do you get to a $7.1B MRO TAM?" The answer: FY25-dated FPDS
obligations on MRO PSCs are funded by ~10 appropriations, not just
OMN cost element 928. Shows the full appropriation stack so the $7.1B
ties to federal budget authority by construction.

**Related workbook support:** the `Budget Anchors` sheet carries 14
TAS-attributed named cells (`MRO_TAS_OMN_FY25`, `MRO_TAS_OPN_FY25`,
`MRO_TAS_OPN_BA7_FY25`, `MRO_TAS_OPN_BA8_FY25`, `MRO_TAS_OPN_BAOTHER_FY25`,
`MRO_TAS_RDTE_DW_FY25`, ..., `MRO_TAS_TOTAL_FY25`) plus an OMN / USCG
budget-book reference section. OPN is drilled to BA level because the
PA data is clean there; OMN, RDT&E-DW, and SCN stay at appropriation
level because their PA routing is noisy. The `Services` sheet carries
a "FY2025 MRO-PSC $ by Appropriation (TAS-measured)" block with the
OPN sub-rows nested inline. See
`docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` and
`docs/planning/PLAN_BROADER_BUDGET_ANCHORS.md` for narrative + pipeline.

---

## Title

Appropriation Sourcing | The $7.1B FY2025 Services MRO TAM is funded
across ~10 federal appropriations -- OMN and OPN each carry roughly
one-third, with Defense-Wide RDT&E a surprising 11%

## Subtitle

FY2025 MRO-PSC obligations by Treasury appropriation ($M, TAS-attributed
via USAspending funding endpoint); OPN drilled to Budget Activity

---

## Left visual - horizontal bar chart (nested)

Eight appropriation-level bars ranked largest to smallest, navy-to-
light-blue palette consistent with the rest of the deck. OPN bar split
into three Budget Activity sub-bars via a nested second tier. $ value
and % of total labeled to the right of each bar.

| Appropriation                                     | FY25 $M    | % of Total | % of OPN |
|---------------------------------------------------|-----------:|-----------:|---------:|
| OMN (Operation & Maintenance, Navy)               |    $2,761  |   37.3%    |      -   |
| **OPN (Other Procurement, Navy)**                 |  **$2,588**| **34.9%**  |  **100%**|
| &nbsp;&nbsp;BA-7 Personnel & Command Support Equip|    $1,591  |   21.5%    |   61.5%  |
| &nbsp;&nbsp;BA-8 Spares & Repair Parts            |      $825  |   11.1%    |   31.9%  |
| &nbsp;&nbsp;Other BAs (BA-1 + Undistributed)      |      $171  |    2.3%    |    6.6%  |
| RDT&E, Defense-Wide                               |      $780  |   10.5%    |      -   |
| USCG (OE + AC&I)                                  |      $320  |    4.3%    |      -   |
| Defense-Wide other (Proc + O&M + misc)            |      $307  |    4.1%    |      -   |
| Navy other (APN + WPN + other Navy)               |      $295  |    4.0%    |      -   |
| Air Force (OMAF + other AF)                       |      $165  |    2.2%    |      -   |
| Army (OMA + other Army)                           |      $131  |    1.8%    |      -   |
| SCN + Other agency (memo)                         |       $53  |    0.7%    |      -   |
| **Total FY2025 MRO-PSC universe**                 | **$7,406** | **100%**   |          |

Legend: navy = Navy-direct appropriations (OMN + OPN + Navy other =
76%); slate = Defense-Wide appropriations (RDT&E-DW + other = 15%);
light-blue = other agencies (USCG + AF + Army + SCN memo = 9%). OPN
sub-bars lighter-shaded variant of the OPN navy to signal the drill
hierarchy.

## Right visual - takeaways table

| Finding                                | Implication                                                                                                                                                                                       |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| OMN + OPN = 72% of MRO $               | Navy sustainment drives the market; the appropriation story is a *Navy* story, not a DoD-wide one.                                                                                                |
| OPN splits 62% Command Support Equip / 32% Spares | BA-7 ($1,591M) is installation + modernization electronics / C4ISR / combat system integration. BA-8 ($825M) is spares and consumable parts. Depot ship repair availabilities (DSRAs, DPIAs, CNO avails) are funded through BA-7, NOT through OMN CE 928 contract maintenance. |
| RDT&E Defense-Wide = $780M (11%)       | Almost entirely Trident II / SSP / SMDC sustainment on J-series PSCs. Draper MK7 Trident ($318M FY25) is the single-largest MRO PIID.                                                             |
| SCN on MRO PSCs = $40M                 | De minimis. Nuclear-platform MRO bundles under PSC 1905 shipbuilding, not onto MRO PSCs -- see Slide 7 for the full scope reconciliation.                                                         |

## Callout (light-blue, italic, below the right table)

Note: reconciling FPDS FY25 MRO $ to OMN cost-element 928 "Ship
Maintenance By Contract" ($2.4B across BA-1 Ship Operations) alone
leaves a naive $4.7B gap. The gap disappears once OPN, RDT&E-DW, USCG,
and the other appropriation colors are included -- FPDS MRO
obligations tie to the full appropriation stack by construction.

## Footnotes

- 49% of FY25 MRO $ directly TAS-attributed from Treasury File C
  submissions (USAspending `/api/v2/awards/funding/`); 51% imputed via
  per-PSC-bucket appropriation ratios from the directly-classified peer
  sample. Rollup totals stable across the direct + imputed split; per-
  bucket ratios noisier on narrow buckets (H-series QC/Test $2M
  classified sample).
- Account-level detail for the ~30 individual Treasury accounts that
  aggregate into these 9 buckets lives on the `Budget Anchors` sheet
  and in `data_pull/output/usaspending/approp_rollup_imputed.json`.
- Source: USAspending `/api/v2/awards/funding/` joined to FPDS FY2025
  contract obligations (U.S. Navy + U.S. Coast Guard, 68 services PSCs).
  Treasury File C DAIMS coverage lags FPDS by ~1 quarter for the
  smallest-$ tail. Data as of April 2026.

---

## Why this slide (audience motivation)

A diligent reader looking at Slides 1-4 will ask three variants of the
same question:

- "Your $7.1B TAM is ~3x the OMN 'Ship Maintenance By Contract' line.
  Is the FPDS number inflated?"
- "If not OMN, what federal appropriations actually fund this?"
- "How confident are you that these obligations are real FY25
  ship-maintenance dollars and not, say, mis-coded procurement or
  Defense-Wide line items sneaking into the PSC filter?"

This slide answers all three on one page. The headline finding -
appropriation-color mixing rather than a single OMN anchor - explains
why the naive top-down-vs-bottom-up gap is structural and not a data
error. The RDT&E-DW 11% finding is the specific piece that most
investor readers will *not* have anticipated.

## Build-out assets available in the workbook

The `Budget Anchors` sheet provides:

1. 14 TAS-attributed named cells -- 10 appropriation-level
   (`MRO_TAS_OMN_FY25` = $2,761K, etc.) plus 3 OPN Budget Activity
   sub-rows (`MRO_TAS_OPN_BA7_FY25` = $1,591K,
   `MRO_TAS_OPN_BA8_FY25` = $825K, `MRO_TAS_OPN_BAOTHER_FY25` = $171K)
   aggregating the ~30 underlying Treasury accounts plus OPN PA drill
   into a SUM-formula total (`MRO_TAS_TOTAL_FY25` = $7,406K).
2. OMN BA-1 Ship Operations section (1B1B / 1B2B / 1B4B / 1B5B totals
   plus CE 928 sub-rows) as context for the OMN slice.
3. USCG ISVS section (ISVS total + 47MLB + WMEC + HEALY line items).
4. NWCF memo row (public-shipyard labor cross-charging - flagged but
   not anchored to a specific figure because no published exhibit
   carves out the ship-maintenance-only slice).

The `Services` sheet provides:

5. FPDS Services TAM block (Navy + CG subtotal, `NAVY_TAM_SVC` +
   `CG_TAM_SVC` named cells) for the $7.1B denominator.
6. FY25 MRO-PSC $ by Appropriation (TAS-measured) block - 10 rows
   referencing the `MRO_TAS_*_FY25` defined names with `% of TAS Total`
   formulas; this is the direct source of the left-bar chart.
7. Top-down budget-book context (memo) - 3 rows (OMN CE 928 BA-1 total,
   OMN BA-1 grand total $23.2B, USCG ISVS $120M).

---

## What does NOT belong on this slide

- Vessel-category breakdown (belongs on Slide 2).
- Work-segment breakdown (belongs on Slide 3).
- Contractor rankings (belong on Slide 4).
- Submarine/carrier scope reconciliation (belongs on Slide 7).
- Public-yard labor as a specific figure (no published line; it shows
  up as a memo row on Budget Anchors but not on this slide).

## Status

Draft only. When the actual slide is designed in the deck app and a
screenshot is captured to `deck/`, move the content into `DECK.md` as
the new Slide 5 section (in the same prose-transcription style as
Slides 1-4) and delete this mockup file.
