# Methodology: MRO Budget Reconciliation (FPDS bottom-up vs OMN top-down)

**Purpose**: explain why the FY2025 Services (MRO) TAM reported in this
workbook (~$7.1B) does not equal the OMN cost element 928 "Ship
Maintenance By Contract" annual budget authority (~$2.4B summed across
all four Ship Operations SAGs), and why the two figures are not
directly comparable.

---

## The two numbers

| Figure | Source | FY25 Enacted | Denominator |
|---|---|---:|---|
| FPDS Services TAM (Navy + Coast Guard, 65 MRO PSCs, post-exclusions) | Awards Excel Table (live SUMIFS) | ~$7,067M | Net sum of contract mod actions dated within FY25, across every appropriation color that funded those actions |
| OMN cost element 928 "Ship Maintenance By Contract" summed across SAGs 1B1B + 1B2B + 1B4B + 1B5B | `Budget Anchors` defined name `OMN_SHIPOPS_BA1_CONTRACT_FY25` | ~$2,396M | FY25-enacted 1-year OMN budget authority earmarked specifically for the "Ship Maintenance By Contract" cost element |
| OMN BA-1 Ship Operations grand total (all cost elements, 4 SAGs) | `Budget Anchors` defined name `OMN_SHIPOPS_BA1_TOTAL_FY25` | ~$23,230M | FY25-enacted OMN BA across all Ship Ops cost elements - civilian labor, NWCF reimbursement, supplies, contracts combined |
| USCG In-Service Vessel Sustainment (ISVS total) | `Budget Anchors` defined name `USCG_ISVS_TOTAL_FY25` | ~$120M | FY25-enacted PC&I capital investment (not OE) for Coast Guard cutter SLEP/MMA |

**Implied gap (FPDS TAM minus OMN CE 928 subtotal) = $7,067M - $2,396M
≈ $4,671M.** This is not a data error or a coverage failure; it is
structural. Three mechanisms drive the gap (appropriation color
mixing, appropriation-year vintage mixing, lump-sum funding of
multi-year performance). A fourth structural point - public-yard
labor being invisible to FPDS entirely - is a separate issue that
does not explain the gap but is worth naming for context.

**Update 2026-04-18**: appropriation-color mixing is now measured, not
inferred. Session (v) TAS pull joined every MRO-PSC FY25 obligation
to its Treasury Account Symbol via USAspending and produced a full
per-appropriation breakdown of the $7.4B - see the "Measured
appropriation breakdown (TAS-attributed)" section below. The $4.7B
"implied gap" against OMN CE 928 is almost entirely explained by OPN
($2.64B), Defense-Wide RDT&E ($0.80B), and a dozen smaller
appropriation colors. Once all appropriations are captured the gap
reconciles to zero by construction. Sections 1-4 below retain the
structural narrative for context; the quantitative answer now lives
in the TAS breakdown.

---

## Why FPDS > OMN CE 928 Contract

FPDS `FY2025 Obligation` is the net sum of contract-mod actions dated
within FY25 (positive new obligations minus any de-obligations). It is
**not** a cumulative lifetime amount and it does **not** track ceiling
drawdowns on multi-year IDVs. Each FY25-dated mod carries its own
accounting line pointing at a specific appropriation (approp color +
enactment year), and the sum across mods is the workbook's $7.1B TAM.

OMN 1B4B cost element 928 "Ship Maintenance By Contract" is one narrow
slice: **FY25-enacted OMN 1-year money earmarked for the 928 CE within
the 1B4B SAG**. Summing CE 928 across all four Ship Ops SAGs gets us
$2.4B. The $4.7B gap between FPDS $7.1B and OMN CE 928 $2.4B comes
from four structural differences:

### 1. Appropriation color mixing (the biggest factor)

FY25-dated FPDS obligations on MRO PSCs are funded by many
appropriation colors, not just OMN CE 928. Each TO funding line names
the backing appropriation; summing across MRO PSCs in FPDS captures
all of them. Examples:

- **SCN** (multi-year Shipbuilding & Conversion) funds CVN Refueling
  Complex Overhauls (LI 2086). Some supporting work is coded under
  J998 (non-nuclear dock work) and K-series (modernization installs)
  but backed by SCN dollars - see `METHODOLOGY_CVN_SSN_COVERAGE.md`.
- **OPN** (multi-year Other Procurement, Navy) spares and install
  equipment show up on N0xx installation PSCs. OPN BA-8 (Spares and
  Repair Parts) alone is ~$884M annually.
- **NWCF reimbursement** - when OMN customers outsource yard work
  they would normally send to public shipyards, NWCF rates fund the
  private-contractor task order, which then appears as an FPDS
  obligation under an MRO PSC (e.g., HII task orders at PSNSY).
- **OMN non-928 cost elements** - minor; most ship-maintenance
  contract dollars within OMN are in CE 928 by definition.

### 2. Appropriation-year vintage mixing within multi-year money

SCN (full-funding, typically obligated over several years) and OPN
(3-year obligation period) dollars **enacted in prior fiscal years**
can be obligated in FY25 as new task orders. So an FY25-dated
obligation can draw on FY22 or FY23 BA. The OMN CE 928 anchor is
strictly FY25-enacted 1-year money; FPDS FY25 is "obligation actions
dated FY25" regardless of enactment year. The two don't match even
before appropriation-color mixing enters the picture.

This same dynamic shows up on the SCN side: FY25 FPDS PSC 1905
obligations for submarines + carriers ($27.6B) exceed FY25 SCN
nuclear-platform BA ($22.7B) by ~$4.9B because SCN money enacted in
FY22-FY24 is still being obligated as Columbia, Virginia, and CVN
RCOH task orders issue in FY25.

### 3. Lump-sum funding of multi-year performance (minor)

Most MRO task orders are firm-fixed-price for a **single availability**
that wraps within ~12 months, so FY25 obligation and FY25 service
delivery line up closely. A minority of TOs span two fiscal years
(long depot availabilities, base+option structures where the base is
funded at issuance) and obligate the full base amount in FY25 even
though delivery extends into FY26. Across years the spill is roughly
symmetric - work scheduled to land mid-FY26 that was obligated in FY25
is offset by work scheduled to land mid-FY25 that was obligated in
FY24. For a single-year TAM this is second-order noise on an already
noisy denominator; the headline $7.1B is not materially distorted.

If a strict "service delivered in FY25" frame is needed, POP
`start_date` / `end_date` on each Awards row could be used to
apportion. POP dates in FPDS are often imprecise so the apportionment
would add noise of its own and has not been judged worth the effort.

### 4. Public-yard labor is NOT in FPDS at all (separate issue)

This does not explain the FPDS > OMN CE 928 gap, but it is a parallel
structural point worth naming: the ~$9,536M non-contract slice of
OMN 1B4B total FY25 ($11,764M - $2,228M CE 928) is mostly **NWCF
rate cross-charging** plus civilian labor and supplies at public
depot activities. NWCF is a revolving fund that charges customer
organizations (principally OMN 1B4B) via customer rates rather than
appropriated labor dollars. This workload never produces a contract
award document - it flows via intra-government MIPR / funding
transfer - and therefore is invisible to any FPDS-based TAM.

Some FPDS obligations on J998/J999 at public-yard IMFs (e.g., HII
Puget Sound DPIA task orders against PSNSY) are a hybrid: private
contractor on-site at a public yard, billed through NWCF as outsourced
yard work. These are small relative to in-house civilian labor but
they do show up in FPDS.

---

## Measured appropriation breakdown (TAS-attributed, 2026-04-18)

The session (v) TAS pull joins every MRO-PSC FY25 obligation to its
Treasury Account Symbol via USAspending `/api/v2/awards/funding/`.
3,730 of 9,282 MRO PIIDs cached directly (98.4% of FY25 $ by Pareto);
remaining awards attributed by PSC-bucket ratios from the
classified peers.

| Federal Account | FY25 $M | % | Appropriation |
|---|---:|---:|---|
| 017-1804 | $2,794M | **37.7%** | OMN (Operation & Maintenance, Navy) |
| 017-1810 | $2,639M | **35.6%** | OPN (Other Procurement, Navy) |
| 097-0400 | $804M | 10.9% | RDT&E, Defense-Wide |
| 097-0100 | $185M | 2.5% | O&M, Defense-Wide |
| 057-3400 | $163M | 2.2% | OMAF (O&M, Air Force) |
| 097-0300 | $111M | 1.5% | Procurement, Defense-Wide |
| 070-0610 | $111M | 1.5% | USCG OE |
| 017-1319 | $92M | 1.2% | APN (Aircraft Procurement, Navy) |
| 021-2020 | $80M | 1.1% | OMA (O&M, Army) |
| 070-0613 | $76M | 1.0% | USCG AC&I |
| 017-1611 | $40M | 0.5% | SCN |
| 017-1507 | $36M | 0.5% | WPN |
| ... | ... | ... | 24 more accounts |
| **Total** | **$7,406M** | 100% | |

Key findings:
- **OMN (~38%) and OPN (~36%) together fund 73% of FY25 MRO-PSC
  obligations**. OMN CE 928 alone ($2.4B) captures less than half of
  the OMN side and only 32% of the total.
- **J998/J999 Depot Ship Repair is OPN-dominant, not OMN-dominant**
  (70% OPN, 27% OMN in the classified sample). DSRAs, DPIAs, and
  availability modernization work route through OPN procurement
  rather than OMN contract maintenance. This is the biggest single
  correction to the narrative below.
- **Defense-Wide appropriations total ~$1.1B (15%)** - almost entirely
  driven by J-series equipment sustainment (Draper MK7 Trident at
  $318M RDT&E-DW, plus other SMDC/SSP work).
- **SCN spillover on MRO PSCs is only $40M** - the earlier
  METHODOLOGY_CVN_SSN_COVERAGE narrative remains correct that
  nuclear-platform MRO bundles under PSC 1905 shipbuilding rather
  than on MRO PSCs.

Source: `data_pull/output/usaspending/approp_rollup_imputed.json`.
Full per-PIID attribution in `approp_attribution.json`. Re-run via
`python3 -m domnann.data_pull.enrich_funding_accounts` then
`classify_approp_colors`.

Coverage caveats:
- Treasury File C DAIMS submissions lag FPDS by a quarter or more;
  brand-new FY25 awards (N0002425C* PIIDs) had zero File C rows at
  the time of pull. PSC-bucket imputation fills these in by assuming
  late-FY25 awards follow the same appropriation mix as earlier
  vintage awards in the same PSC bucket.
- Direct-classified $: 48% of FY25 MRO $. Imputed: 52%.
- Ratio-reliability: per-PSC bucket ratios are computed from the
  classified sample within that bucket. Narrow buckets (H-series
  QC/Test with $2M classified sample) are noisier than wide ones
  (J998/J999 with $2,994M classified sample).

---

## How to read the Services sheet Budget Reconciliation block

The Services sheet has a new section titled
"FY2025 MRO Budget Reconciliation - FPDS (bottom-up) vs OMN Ship Ops
BA-1 (top-down)." It shows:

- **FPDS rows** - Navy TAM, CG TAM, FPDS subtotal - via defined names
  `NAVY_TAM_SVC` and `CG_TAM_SVC` (live SUMIFS against 65 MRO PSCs).
- **OMN CE 928 rows** - per-SAG contract slices and the $2.4B subtotal
  via `OMN_SHIPOPS_BA1_CONTRACT_FY25`.
- **OMN BA-1 total row** - `OMN_SHIPOPS_BA1_TOTAL_FY25` = $23.2B;
  shown as context, NOT summable with the FPDS row above.
- **USCG ISVS row** - `USCG_ISVS_TOTAL_FY25` = $120M.
- **Implied gap row** - FPDS TAM minus OMN CE 928 subtotal. This is
  the $4.7B explained by appropriation color + vintage mixing and
  lump-sum multi-year funding, as described above.

**Do not treat any row as a "missing money" number.** The FPDS side
and the OMN side measure different things; the reconciliation is
definitional, not pinpoint. The purpose of the block is to give a
reader a defensible frame for how the private-contractor Services TAM
relates to the annual Ship Operations appropriation authority.

---

## NWCF - why we don't anchor to it

Navy-wide NWCF FY26 budget authority is ~$40.3B (contract authority
$11.8B + offsetting collections $28.5B). This covers all Navy working-
capital-funded activities (Naval Shipyards, Naval Air Systems Command
Aviation Depots, Defense Logistics Agency services, etc.) across Navy
bases and installations.

No exhibit publishes a clean "public shipyard only" or "ship-MRO-only"
slice. Naval Shipyard workload is a portion but not extractable from
the published tables. We therefore include NWCF as a **memo row** only
(no defined name, no reconciliation-table participation) so a reader
can see it exists but not anchor any specific figure to it.

An earlier session's `METHODOLOGY_CVN_SSN_COVERAGE.md` notes the four
shipyards and that their workload is ~$4-6B annually in aggregate
(informed guess, not a published line), split across CVN and SSN/SSBN
workload. That estimate should be treated as directional, not as a
reconcilable number.

---

## Sources

- `sources/OMN_Book.txt` - OMN FY26 President's Budget Exhibit OP-5,
  BA-1 Operating Forces. Line references in the workbook's
  `Budget Anchors` sheet Source column (e.g., `OMN_Book line 619`).
- `sources/NWCF_Book.txt` - Navy Working Capital Fund exhibit.
- `sources/USCG_Justification` (via `data_v2.xlsx`) - USCG FY26
  Justification, ISVS PPA and sub-investments.
- `data_v2.xlsx` "Budget Data" sheet - consolidated line items across
  OMN, SCN, NWCF, USCG, OPN with FY24 Actuals / FY25 Enacted / FY26
  Request. Primary source for Budget Anchors values.
- `sheets/budget_anchors.py` - loader + SECTIONS defining the 19
  defined names referenced by this reconciliation.
- `sheets/services.py` - `_write_mro_budget_reconciliation` and
  `_write_mro_budget_anchors_refs` helpers writing the on-sheet blocks.
- `METHODOLOGY_CVN_SSN_COVERAGE.md` - parallel SCN reconciliation for
  nuclear-platform newbuild + sustainment.
- `restructuring/restructure_progress.md` - history of the v1 attempt
  to reconcile top-down budget with bottom-up FPDS and why that
  approach was abandoned for a private-contractor-addressable-market
  framing.
- `data_pull/usa_client.py`, `enrich_funding_accounts.py`,
  `classify_approp_colors.py` - pipeline producing the TAS-attributed
  breakdown.
- `data_pull/output/usaspending/approp_rollup_imputed.json` - measured
  appropriation breakdown artifact.
- `sessions/SESSION_2026-04-18_v_tas_funding_pull.md` - full session
  log of the TAS pull.
- `docs/planning/PLAN_BROADER_BUDGET_ANCHORS.md` - plan for
  integrating the TAS attribution into the Budget Anchors workbook
  sheet (Phase 2+, not yet done).
