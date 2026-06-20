# Session 2026-04-18 (v): TAS / Appropriation-Color Pull - v2.76 unchanged

## Context

Follow-on to session (iv). `PLAN_BROADER_BUDGET_ANCHORS.md` asks to
broaden the top-down MRO reconciliation beyond OMN CE 928 ($2.4B) to
include all appropriations that actually fund FY25 MRO-PSC obligations.
Plan listed 3 blockers (ORATA/CE 928 overlap, SCN spillover measurement,
NDSF source location) and a rough magnitude estimate.

This session resolves the blockers with documentary evidence and pulls
per-award TAS (Treasury Account Symbol) data from USAspending to replace
the plan's rough appropriation estimates with measured numbers.

Ended with classifier artifacts in `data_pull/output/usaspending/` and a
data-driven FY25 MRO-PSC appropriation breakdown. No workbook changes;
v2.76 still current.

---

## Part A - Plan blockers resolved via documentary review

### Q1: ORATA vs OMN CE 928 overlap - ORATA IS INSIDE CE 928

Evidence:
- `sources/OMN_Book.txt` line 5608 (OP-5 Performance Criteria table
  for SAG 1B4B) lists ORATA as a workload category totaling $990M
  FY25.
- Line 6698 (OP-5 Cost Element table for same SAG) lists CE 928 Ship
  Maintenance By Contract at $2,228M FY25.
- Both tables sum to the same $11,763M SAG 1B4B total. They are two
  views of the same dollars: Workload view (what's being done) and
  Cost-Element view (how the dollars are categorized for reporting).
- Line 5518 narrative: "ORATA: Program increase in Outsourcing
  workload from the Naval Shipyards to the private sector... (Baseline:
  $990,461)" - outsourced workload means contract-directed, so inside
  CE 928.

Action: do NOT add ORATA as a separate additive anchor. Drops the
plan's expected top-down rollup by $990M.

### Q2: SCN spillover onto MRO PSCs - measured at $66M, not $200-500M

Empirical measurement using `contracting_office` filter against
MRO_PSCS rows in the Awards master:

- 26 rows / $66M total - $63M at SUP OF SHIPBUILDING CONV AND REPAIR,
  $3M at SUP OF SHIPBUILDING GROTON
- Composition: PDA (Post-Delivery Availability) + PSA (Post-Shakedown
  Availability) on newbuild LPD 29, DDG 128, LCS 36/38. Warranty-style
  work on recently-delivered ships, not RCOH modernization bundles.
- Top: LPD 29 PDA @ HII $20M (K019), DDG 128 PSA @ HII $19M (J019).

Later confirmed by TAS pull: SCN (017-1611) rolls up to only $40M
FY25 across all MRO PSCs, consistent with the SUPSHIP-filter measure.

Action: treat as ~$66M memo row, not a primary anchor section. Plan's
$200-500M estimate was high by 5-7x.

### Q3: NDSF data source - already captured in existing anchors

NDSF is primarily a strategic-sealift PROCUREMENT fund, in declining
use (ESD/ESB procurement has shifted to SCN BLI 3039 per SCN_Book
line 13818). NOT an MSC operating fund. The plan's "NDSF MSC
Operating Costs" conflation resolves to:

- MSC operations (CLF/APS/Special Mission/JHSV/Service Support) =
  OMN SAG 1B1B Navy Transportation ~$4.3B FY25 -> already captured
  via `OMN_1B1B_TOTAL_FY25`.
- MSC ship maintenance (ROH, MTA, SIA) = OMN SAG 1B4B Ship
  Maintenance (MSC section at OMN_Book line 5637) -> already captured
  via `OMN_1B4B_TOTAL_FY25`.

Action: drop NDSF section from the plan. No new data pull needed.

---

## Part B - TAS pull via USAspending `/api/v2/awards/funding/`

Pipeline README flagged this as a future pull: per-transaction TAS data
from the USAspending transactions / funding endpoints, which joins
FPDS action data to Treasury DAIMS filings. FPDS Atom feed's own TAS
column is ~3.5% populated with zero-dollar close-outs only.

### 1. Endpoint investigation

Tested both `/awards/accounts/` (lifetime TAS) and `/awards/funding/`
(per-transaction TAS). Picked `/funding/` because it adds
`reporting_fiscal_year`, `program_activity_code`, `object_class`, and
`disaster_emergency_fund_code` per transaction - useful beyond just
the account list.

Found a reporting-lag pattern: Treasury File C DAIMS submissions
lag FPDS by a quarter or more. Brand-new FY25 awards (N0002425C* PIIDs)
have no File C data yet. The ratios between accounts that DO report
are reliable; absolute $ totals are laggy.

### 2. Code additions

- `data_pull/usa_client.py` - new `get_award_funding(award_id, ...)`
  wrapping `/awards/funding/` with pagination + disk cache; filters
  out null-obligated quarterly GTAS rows.
- `data_pull/enrich_funding_accounts.py` - orchestrator: pulls for
  every MRO-PSC PIID via ThreadPoolExecutor, aggregates to
  `(award, fiscal_year, federal_account)` grain, writes summary +
  errors.
- `data_pull/classify_approp_colors.py` - applies classifier from
  the funding aggregate to FPDS FY25 $ via ratio-splitting.
- `/tmp/aggregate_funding_cache.py` - cache-only aggregator for
  resuming a partial pull.
- `/tmp/impute_approp.py` - imputer: for awards with no TAS data,
  assigns per-PSC-bucket appropriation ratios from the classified
  peer sample.

### 3. Pull run

Two passes at `enrich_funding_accounts.py`:
- concurrency=4 initial run: got 2,375 awards (~8 req/s for first
  5 min, then degraded to ~1 req/s as USAspending started dropping
  keepalive connections aggressively).
- concurrency=2 resume: got another 1,355 awards at similar ~1 req/s
  (server pushback same at either concurrency).

Stopped at 3,730 / 9,282 PIIDs cached (40.2% by PIID count). Pareto
dominance: these 3,730 represent **$7,288M / $7,406M = 98.4% of
FY25 MRO $ coverage**. Remaining 5,552 uncached are $118M tail.

Of the 3,730 cached, 2,827 returned zero funding rows (brand-new FY25
awards with no File C data yet). 903 have at least one row. The 903
cover enough $ to anchor a PSC-bucket classifier for the rest.

### 4. Final appropriation breakdown (FY25 MRO PSCs, 9,282 PIIDs)

Direct TAS-classified: 48% of $. PSC-bucket imputed: 52% of $.
Imputation ratios derived from classified peer sample per
J998/J999 + J-series + K-series + N-series + H-series + L-series +
M1 + M2 buckets.

| Federal Account | FY25 $M | % | Appropriation |
|---|---:|---:|---|
| 017-1804 | $2,794M | **37.7%** | **OMN (Operation & Maintenance, Navy)** |
| 017-1810 | $2,639M | **35.6%** | **OPN (Other Procurement, Navy)** |
| 097-0400 | $804M | 10.9% | RDT&E, Defense-Wide |
| 097-0100 | $185M | 2.5% | O&M, Defense-Wide |
| 057-3400 | $163M | 2.2% | OMAF (O&M, Air Force) |
| 097-0300 | $111M | 1.5% | Procurement, Defense-Wide |
| 070-0610 | $111M | 1.5% | USCG OE |
| 017-1319 | $92M | 1.2% | APN (Aircraft Procurement, Navy) |
| 017-1106 | $91M | 1.2% | Navy (other) |
| 021-2020 | $80M | 1.1% | OMA (O&M, Army) |
| 070-0613 | $76M | 1.0% | USCG AC&I |
| 017-1506 | $52M | 0.7% | Navy (other) |
| 017-1611 | $40M | 0.5% | **SCN** |
| 017-1507 | $36M | 0.5% | WPN |
| ... | ... | ... | 20 more accounts |
| **Total** | **$7,406M** | 100% | |

### 5. Per-PSC-bucket appropriation ratios (classified sample)

| PSC Bucket | Sample $M | Top 3 accounts |
|---|---:|---|
| J998/J999 Depot Ship Repair | $2,994M | OPN 70.5% + OMN 26.8% + USCG 1.0% |
| J-series Equip Maint | $1,068M | OMN 37.8% + RDT&E-DW 31.5% + OPN 8.7% |
| K-series Equip Mod | $298M | OMAF 21.8% + OMN 13.9% + Proc-DW 13.6% |
| N-series Install | $109M | OMN 67.5% + OPN 11.0% + OM-DW 9.4% |
| M2 Husbanding | $31M | OMN 89.2% + USCG 10.8% |
| L-series Tech Rep | $27M | OMN 97.1% + RDT&E-DW 2.8% |
| H-series QC/Test | $2M | USCG 73.6% + OMN 26.4% |

---

## Part C - Implications vs `PLAN_BROADER_BUDGET_ANCHORS.md`

### What the plan got right

- OPN is significant (plan estimated $883M Spares 9020).
- Appropriation-color mixing is the primary gap driver (not vintage).
- USCG OE depot earmark exists as its own flow.

### What the plan got wrong

1. **OPN sizing**: plan estimated $883M (just BA-8 Spares 9020).
   Actual OPN on MRO PSCs = **$2,639M** - 3x bigger. OPN funds
   DSRAs/DPIAs as modernization installs across multiple BAs, not
   just spares. J998/J999 Depot Ship Repair runs 70.5% OPN.

2. **SCN spillover**: plan estimated $200-500M. Actual = **$40-66M**.

3. **NDSF**: plan proposed as a $1-2B anchor. Actual = $0 additional
   (already inside OMN 1B1B+1B4B).

4. **ORATA**: plan proposed as a $990M additive anchor. Actually
   inside OMN CE 928 -> double-counts.

5. **Defense-Wide appropriations missing**: plan didn't list these.
   Actual Defense-Wide (RDT&E + Proc + O&M) = **$1,100M**, dominated
   by J014 Draper MK7 Trident sustainment ($318M RDT&E-DW) and
   other SMDC/SSP work.

### Revised rollup expectation

Plan projected top-down authority of $5.6-7.6B with residual $0-1.5B.

Data-driven top-down using only Navy OMN + Navy OPN summed across all
BAs (not just CE 928 and BA-8):
- OMN-Navy (017-1804) total FY25 BA: ~$56B (all BAs)
- OPN-Navy (017-1810) total FY25 BA: ~$13B (all BAs)
- FY25 MRO PSC obligations attributable to these 2 = $5.4B (73% of $7.4B)

The top-down anchor that MATCHES the FY25 MRO bottom-up is **not a
narrow single-cost-element slice** but the **portion of each
appropriation's BA actually directed at ship/equipment MRO
contracting**. That number is only cleanly measurable BY going through
FPDS TAS backwards - which is exactly what this pull does.

The more useful reconciliation is: here is the mix of appropriations
funding FY25 MRO PSCs ($7.4B). Here is the MRO-relevant subset of each
appropriation's top-down BA. Those should agree by construction once
we narrow the OMN and OPN top-down to the MRO-directed cost elements
and BAs.

---

## Files created

- `data_pull/output/usaspending/funding/<gid>.json` x 3,730 - per-award
  TAS caches (excluded from git via existing `usaspending/` gitignore
  pattern; verify if committing)
- `data_pull/output/usaspending/funding_accounts_agg.json` (1,547 rows)
- `data_pull/output/usaspending/funding_accounts_summary.json`
- `data_pull/output/usaspending/approp_attribution.json` - per-award
  FY25 $ split
- `data_pull/output/usaspending/approp_rollup.json` - direct rollup
- `data_pull/output/usaspending/approp_rollup_imputed.json` - direct +
  imputed rollup

Code additions:
- `data_pull/usa_client.py` - `get_award_funding()` method added
- `data_pull/enrich_funding_accounts.py` - new orchestrator
- `data_pull/classify_approp_colors.py` - new classifier

Scratch (not committed):
- `/tmp/aggregate_funding_cache.py`
- `/tmp/impute_approp.py`
- `/tmp/probe_scn_spillover.py`

## Files modified

None. No workbook changes. v2.76 still current.

## Memories added

None.

---

## Coverage caveats

- **Treasury File C lag**: 75% of cached MRO awards (2,827 of 3,730)
  returned zero File C rows. These are overwhelmingly brand-new FY25
  awards (PIIDs N0002425C*) that haven't yet populated DAIMS quarterly
  submissions. The imputer uses PSC-bucket ratios from the classified
  peers to assign them an appropriation mix.

- **Ratio-reliability assumption**: imputation assumes late-FY25 awards
  in each PSC bucket follow the same approp mix as earlier-vintage
  awards in the same bucket. Probably fine for J998/J999 (structural
  funding is stable), potentially noisy for narrow buckets (H-series
  QC/Test only has $2M classified sample).

- **Partial PIID coverage**: 40.2% of MRO PIIDs cached. Dollar
  coverage is 98.4% by construction (puller sorts FY25 $ desc).
  Remaining 5,552 PIIDs are long-tail small-$ awards ($118M total)
  that would marginally refine but not change the rollup.

- **Rate limit**: USAspending dropped keepalive connections
  aggressively under sustained 2-4 worker load, cutting effective
  rate to ~1 req/s. Completing the remaining 5,552 would take ~75
  more min at the degraded rate; not worth it for the marginal
  coverage gain.

---

## Open flags / follow-ups

1. **Plan revision**: `PLAN_BROADER_BUDGET_ANCHORS.md` should be
   rewritten to reflect the data-driven findings before further work
   against it. OPN sizing is the biggest correction.

2. **Workbook integration**: `approp_rollup_imputed.json` is ready to
   drive a new "TAS Attribution" section on Budget Anchors + Services.
   Would need a new data sheet plus a reconciliation block on Services.
   Not started.

3. **TAM framing decision** (`METHODOLOGY_TAM_FRAMING.md`): still
   pending. Related but orthogonal to this work.

4. **Completing the tail**: 5,552 uncached PIIDs for $118M / 1.6% of $.
   Low marginal value. Only worth doing if a follow-up pass wants
   100% direct-classified coverage instead of 48% direct + 52%
   imputed.

5. **Extending to newbuild PSCs**: the pull was MRO-only. Running on
   all ~24,618 PIIDs would let the same approach reconcile Product
   Procurement ($ heavy at SCN-backed HII NNS submarine + carrier
   programs). ~3 hours at current pace; probably worthwhile.
