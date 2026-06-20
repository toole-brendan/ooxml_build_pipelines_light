# Slide 08 — Top-Down Composition (module: `topdown_detail.py`)

> Breadcrumb: TAM › Top-Down Detail · static stacked bar + rollup table · `_chart_xml/slide08.xml` + `slide08_table.xml`

## On-slide claims (verbatim)

- **Takeaway:** "The **$17.0B** budget-anchored MRO decomposes into Public NSY (**$7.49B,
  44%**), OMN 1B4B private availabilities (**$4.28B, 25%**), and non-1B4B anchors (**$5.23B,
  31%**)."
- **Chart:** "FY2025 MRO Top-Down TAM by Budget Source ($M)" · **Total = $16,996M.**
- **Rollup table (Category | FY2025 $M | PB26 PDF Source):**
  | Line | $M | Source |
  |---|---:|---|
  | OMN 1B4B Total | 11,764 | OMN OP-5, p.157 |
  | — Private avail subtotal | 4,279 | (Table IV detail below) |
  | — Public NSY (4 yards) subtotal | 7,485 | |
  | OPN LI 1000: Ship Maint, Repair and Mod | 2,392 | OPN BA-1 P-40, p.521 |
  | MSC M&R (1B1B FY2025 transfer) | 1,240 | OMN OP-5, p.129 |
  | SCN LI 2086 CVN RCOH (HII NNS) | 1,480 | SCN P-40, p.175 |
  | USCG ISVS (PC&I floor) | 120 | USCG Justification, p.6 |
  | **MRO Total (Top-Down)** | **16,996** | |
- **Private-avail Table-IV detail ($M):** IL Non-depot/Intermediate 1,429 · ORATA Misc
  Restricted/Trade 990 · CM Continuous (CMAV) 663 · SRA Selected Restricted 384 · PIA Planned
  Incremental 322 · OH Overhauls 250 · ERATA Emergent 136 · SIA Surface Incremental 64 · SCO
  Service Craft OH 23 · CIA Carrier Incremental 16 · PMA Planned Maint 0.

## Claim-by-claim sourcing

Every anchor is source-pinned to a **PB26 budget-book PDF page** and to a workbook cell:

| Anchor | Workbook ($K, FY25 Enacted) | Accessor | Budget source |
|---|---:|---|---|
| OMN 1B4B total | 11,763,594 | `model_op5…` `op5_total_cell()` | OMN OP-5 Table IV, p.157 (SRC-04) |
| Public NSY (4 yards) | 7,484,837 | `op5_public_nsy_cell()` | OP-5 Table IV public split |
| OPN LI 1000 | 2,392,190 | `model_msc_scn_uscg…` `opn_li1000_cell(2025)` | OPN BA-1 P-40 p.521 (SRC-07) |
| MSC M&R | 1,239,846 | `msc_mr_fy25_transfer_cell()` | OMN OP-5 p.129 / OMN_Book line 4467 (SRC-05) |
| SCN LI 2086 CVN RCOH | 1,480,314 | `scn_cvn_rcoh_li2086_cell(2025)` | SCN P-40 LI 2086 p.175 (SRC-06) |
| USCG ISVS | 120,000 | `uscg_isvs_floor_cell()` | USCG Justification p.6 (SRC-09) |

**Sum: 11,764 + 2,392 + 1,240 + 1,480 + 120 = $16,996M.** (Within OMN 1B4B: private $4,279M +
public NSY $7,485M = $11,764M.)

- **Public NSY by yard** (`model_op5_navy_topdown.py`): Puget Sound **$2,741M** · Norfolk
  **$1,790M** · Pearl Harbor **$1,486M** · Portsmouth **$1,468M** = **$7,485M**.
- **Private avail categories** are OP-5 Table IV availability lines (OH/SRA/PIA/CMAV/IL/…) —
  `model_op5_navy_topdown.py`.

## Reserve facts (could be added)

- **Why OPN LI 1000 is a separate $2.39B:** it is the **modernization side** of availabilities,
  funded from the **1810N OPN** appropriation (distinct from OMN 1B4B), established by the
  **Consolidated Appropriations Act 2020 (PL 116-93)** — workbook CITE-01 / SRC-07. This is the
  "no-double-count" boundary between OMN and OPN.
- **Public NSY is federal-civilian labor, FPDS-invisible** — reimbursed through the Navy
  Working Capital Fund (NWCF), cross-charged into OMN via customer rates. All-in public-yard
  activity is **$12–15B** including mission funding (`public_naval_shipyard_revenue.md`;
  `model_reconciliation.py` `PUBLIC_SHIPYARD_NWCF` note). This is the structural gap that
  slides 09–10 strip out.
- **SCN LI 2086 = CVN-74 Stennis RCOH** at HII Newport News, $1,480M FY25 (net of AP/SFF);
  CVN-75 Truman RCOH ramps to $1,779M in FY26 (`model_reconciliation.py` §2).
- **MSC M&R is mid-migration:** FY25 executes out of **1B1B**, transfers to **1B4B in FY26** —
  why FY26 top-down inflates ~$1.6B (`budget_method/topdown_gold/summary.md`).
- Full top-down budget context (7-bucket ~$74.9B full universe, ~$28.6B in-service) is in
  `research/budget_method/topdown_gold/` (summary.md, tam_table.md, bucket docs).

## Quotable stats & attributions

- "**$17.0B** budget-anchored FY2025 MRO: Public NSY **$7.49B (44%)**, OMN 1B4B private avails
  **$4.28B (25%)**, non-1B4B anchors **$5.23B (31%)**." (deck, slide 08)
- "Public naval shipyards consumed **$7.49B** of OMN 1B4B in FY25 — Puget Sound $2.74B, Norfolk
  $1.79B, Pearl Harbor $1.49B, Portsmouth $1.47B." (`model_op5_navy_topdown.py`)
- "Every top-down anchor is pinned to a specific PB26 budget-book PDF page (OP-5 p.157, OPN P-40
  p.521, SCN P-40 p.175, USCG p.6)." (deck table)

## Source line — ready to use

> Sources: (1) PB26 OMN OP-5 (p.157, MSC p.129); (2) PB26 OPN BA-1 P-40 LI 1000 (p.521); (3) PB26 SCN P-40 LI 2086 (p.175); (4) PB26 USCG Justification (p.6)

## Caveats / confidence / staleness flags

- **Confidence: high** — every figure is a published budget-book line, source-pinned.
- `[!]` **No WPN plug in this $16,996M.** WPN combat-systems sustainment is *intentionally
  excluded* from the top-down (no Table-IV equivalent in WPN P-40; see slide 10 note). The
  workbook's TAM Bridge / `inputs_assumptions.py` still carries a **$500M WPN plug** as an
  editable input — but the deck's pinned-anchor total is $16,996M *without* it. Don't add the
  $500M on top of $17.0B.
- The $K workbook values round to the $M shown (e.g. 11,763,594K → $11,764M).
</content>
