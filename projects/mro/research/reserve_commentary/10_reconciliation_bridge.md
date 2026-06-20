# Slide 10 — Reconciliation Bridge (module: `reconciliation_bridge.py`)

> Breadcrumb: TAM › Reconciliation Bridge · 7-row bridge table + oval markers · `_chart_xml/slide10_table.xml` + `slide10.xml`

## On-slide claims (verbatim)

- **Takeaway:** "Top-down (**$17.0B**) and bottom-up (**$9.0B**) reconcile across 7 bridge
  components, with Public Naval Shipyard labor (**$7.49B**) the structural FPDS-invisible gap."
- **Bridge table** (Component | Top-down $M | Bottom-up $M | Gap TD−BU | Explanation):
  | # | Component | TD | BU | Gap | Note |
  |---|---|---:|---:|---:|---|
  | 1 | Navy private 1B4B (avail subtotal) | 4,279 | 3,493 | +786 | Primary recon test. PB26 forecast vs FPDS actuals |
  | 2 | Navy Public NSY (4 yards) | 7,485 | 0 | +7,485 | STRUCTURAL: federal civilian workforce, FPDS-invisible |
  | 3 | OPN LI 1000 Ship Maint Repair & Mod | 2,392 | (in PSCs) | ~+1,500 | NEW source-pinned. Modernization side, separate appropriation |
  | 4 | MSC M&R (1B1B FY25 → 1B4B FY26) | 1,240 | 694 | +546 | MSC HQ contracting flow. Reconciles within ±15% |
  | 5 | SCN CVN RCOH (LI 2086) | 1,480 | 2,057 | −577 | Multi-year incremental vs single-FY FPDS. PSC 1905 sees more |
  | 6 | USCG cutter MRO | 120 | 273 | −153 | TD anchor (ISVS floor) known low. FPDS sees actual awards |
  | 7 | Other (RDT&E-DW Strategic, AF/Army cross-svc) | n/a | ~1,520 | −1,520 | BU captures Strategic Systems (Draper Trident), AF/Army |
  | | **Total** | **16,996** | **8,971** | **+8,025** | Public NSY $7,485M + Private TD $9,511M vs BU $8,971M = +$540M (~6%) |
- **Footer:** "Source: workbook_build TAM Bridge sheet (corrected 2026-04-27); plan section 2.3.
  … WPN combat-systems sustainment intentionally excluded from top-down (no Table-IV-equivalent
  in WPN P-40); FPDS captures the WPN flow on combat-system PSCs (J012, J014, K010, K012) within
  Narrative A. Data as of April 2026."

## Claim-by-claim sourcing

All rows come from `workbook_mro/sheets/model_tam_bridge.py` (TD via OP-5 / MSC-SCN-USCG / OPN
accessors; BU via FPDS SUMIFS over RMC offices and PSC subsets). Key anchors:

| Component | TD source | BU source |
|---|---|---|
| Navy private 1B4B | `op5_private_cell()` ($4,279M) | FPDS SUMIFS, RMC offices ($3,493M) |
| Public NSY | `op5_public_nsy_cell()` ($7,485M) | $0 by construction |
| OPN LI 1000 | `opn_li1000_cell(2025)` ($2,392M) | embedded in PSC obligations |
| MSC M&R | `msc_mr_fy25_transfer_cell()` ($1,240M) | FPDS SUMIFS ($694M) |
| SCN CVN RCOH | `scn_cvn_rcoh_li2086_cell(2025)` ($1,480M) | PSC 1905 carrier SUMIFS ($2,057M) |
| USCG cutter | `uscg_isvs_floor_cell()` ($120M) | USCG services TAM ($273M, ties to awards.csv CG $272.6M) |
| "Other" | n/a | RDT&E-DW + AF + Army + DW-other + Navy-other (≈$1,520M) |

- The **+$8,025M total gap is structurally Public NSY ($7,485M)**. Net of Public NSY: TD private
  **$9,511M** vs BU **$8,971M** = **+$540M (~6%)** — the real reconciliation residual.
- Reconciliation logic / why FPDS ≠ OMN: `research/award_based/docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md`;
  cross-checks in `research/budget_method/topdown_gold/reconciliation.md`.

## Reserve facts (could be added)

- **Row 5 is the most interesting sign-flip:** TD SCN RCOH $1,480M < BU $2,057M. The bottom-up
  sees *more* carrier RCOH because PSC 1905 captures multi-year HII Newport News work that the
  single-FY SCN line understates ($2,057M is the PSC 1905 carrier **upper bound**).
- **The "Other" row ($1,520M BU)** is the ~6% residual personified: RDT&E-DW Strategic Systems
  (**Draper Trident $318M**), Air Force ($164M), Army ($129M), DW-other ($312M), Navy-other
  ($299M) cross-service flows that hit MRO PSCs but sit in no OP-5/MSC/SCN/USCG anchor
  (`model_reconciliation.py` §2 TAS rows).
- **WPN handling:** the bridge intentionally drops WPN from the top-down (no Table-IV equivalent
  exists in WPN P-40); FPDS still captures the WPN combat-systems flow on PSCs **J012, J014,
  K010, K012** inside Narrative A. So WPN isn't missing — it's on the bottom-up side.

## Quotable stats & attributions

- "Two independent methods reconcile across 7 components; the +$8.0B gross gap is structurally
  Public NSY labor (**$7.49B**), and net of that the private estimates agree within **~6%**
  ($9,511M TD vs $8,971M BU)." (deck, slide 10)
- "Bottom-up sees *more* CVN RCOH than the SCN line ($2,057M vs $1,480M) because PSC 1905
  captures multi-year HII Newport News work." (bridge row 5)

## Source line — ready to use

> Sources: (1) FPDS FY2025 contract obligations, U.S. Navy and U.S. Coast Guard; (2) PB26 budget anchors (OMN OP-5, OPN BA-1 P-40 LI 1000, SCN P-40 LI 2086, USCG Justification); (3) Treasury TAS appropriation attribution

## Caveats / confidence / staleness flags

- **Confidence: high** on the totals and on Public NSY; **medium** on individual BU component
  cuts (the per-row BU values are matched subsets, so they don't sum cleanly to $8,971M — the
  Total-row BU $8,971M is the authoritative bottom-up).
- `[!]` **The on-slide bridge has 7 rows ending in "Other"; the workbook `model_tam_bridge.py`
  carries a WPN row instead (with a $500M plug).** The deck (footer "corrected 2026-04-27")
  drops WPN from TD and shows "Other" as a BU-only row. If someone opens the workbook TAM Bridge
  sheet they'll see a WPN line that isn't on the slide — same reconciliation, different
  presentation of the WPN flow.
- "Gap (TD−BU)" of +786 on row 1 is the **primary reconciliation test** (PB26 forecast vs FPDS
  actuals); ±15–20% on a single category is expected and acceptable.
</content>
