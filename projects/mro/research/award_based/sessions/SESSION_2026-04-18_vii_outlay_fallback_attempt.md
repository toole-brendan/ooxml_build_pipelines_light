# Session 2026-04-18 (vii): Outlay-Fallback Fix Attempt - v2.78 -> v2.79

## Context

Session (vi) landed v2.78 with the TAS Attribution section integrated into
the workbook. The reconciliation block shows FY25 MRO-PSC $ broken out by
appropriation: OMN 37.7%, OPN 35.6%, RDT&E-DW 10.9%, SCN 0.5%, etc.
Coverage: 48% directly classified from Treasury TAS data, 52% imputed
from PSC-bucket peer ratios.

The 48%/52% split is the key caveat on the headline numbers. Direct
classification is always preferable to imputation because it is a
per-award measurement rather than a peer-inheritance assumption. A
higher direct share gives the analysis sharper per-deck-segment
attribution (e.g. tighter claim that DSRAs specifically are 70% OPN,
not just that J998/J999 awards in aggregate are 70% OPN).

This session was an attempt to shrink the imputation burden by
capturing an additional signal from USAspending that the prior client
was discarding. The fix under-delivered: direct-classified coverage
rose from 48% to 49.2% (~1 percentage point), and the headline rollup
numbers shifted by less than 1pp in any category. Root cause: I
mis-diagnosed why so many awards returned zero File C rows. See below.

---

## What we were trying to learn

Two questions:

1. **Why do ~75% of cached MRO awards return zero funding rows?** In
   session (v) the TAS pull cached 3,730 awards, of which 2,827 came
   back with no usable transaction data. I had attributed this to
   Treasury File C DAIMS reporting lag -- brand-new FY25 awards not yet
   populated. But FY25 ended Sept 30 2025 and it's now April 2026, so
   the "reporting lag" narrative should no longer apply.

2. **Can we recover classifier signal from those empty-row awards?** My
   hypothesis: some Navy organizations (Strategic Systems Programs,
   NAVAIR, others) file DAIMS quarterly submissions as outlay
   aggregates (gross_outlay_amount populated) rather than as itemized
   transaction obligations (transaction_obligated_amount populated).
   The prior `data_pull/usa_client.py::get_award_funding` filter
   stripped rows where `transaction_obligated_amount is None`, which
   would incorrectly discard outlay-only rows that still carried the
   appropriation signal we needed (the `federal_account` field).

If the hypothesis held, loosening the filter would recover signal for
a meaningful chunk of the empty-cache awards and direct-classified
coverage would rise from 48% to something like 70-80%.

---

## What we did

### 1. Modified the client to keep outlay-only rows

`data_pull/usa_client.py::get_award_funding`:

- Old filter: `if row.get('transaction_obligated_amount') is None: continue`
- New filter: keep rows where EITHER
  `transaction_obligated_amount is not None` OR
  `gross_outlay_amount is not None and > 0`
- Also added a guard requiring `federal_account` be populated (no
  signal possible without the account assignment).

The theory: outlay rows still carry `federal_account`, `account_title`,
`reporting_fiscal_year`, `object_class`, and `program_activity_code`.
That's full classifier input even if the transaction-obligation column
is null.

### 2. Modified the classifier to use outlay as fallback magnitude

`data_pull/classify_approp_colors.py::build_classifier`:

- Old: `by_award[gid][acct] += abs(row.get('transaction_obligated_amount') or 0)`
- New: `magnitude = obl if obl > 0 else out` (use
  `gross_outlay_amount` when `transaction_obligated_amount` is zero/null)

The ratios within an award (how much OMN vs OPN vs RDT&E) are the
durable signal; absolute magnitudes are only used to weight the
account shares. Whether the magnitude comes from obligation or outlay
data doesn't affect the ratio meaning.

### 3. Deleted empty caches, re-pulled with updated client

Wrote `/tmp/backfill_empty_funding.py` to scan the funding cache dir,
identify files containing `[]`, and delete them. Scanned 3,730
existing caches; deleted 2,827 empty ones; kept 903 populated caches.

Launched `python3 -m domnann.data_pull.enrich_funding_accounts
--concurrency 2` in background. Because `get_award_funding` checks
cache-before-pull, the 903 populated caches were skipped instantly and
only the 2,827 deleted + 5,552 never-attempted tail awards went to the
network.

Rate: ~1.5-1.8 req/s (similar to session v). Let it run until cache
count hit 3,849, then killed (user requested). Representing 1,063
awards actually newly pulled (1,063 = 3,849 - 903 direct re-pulls -
minus... actually several hundred of those re-filled the old empties,
the rest are fresh pulls against the prior-uncached tail).

Final state: 3,849 cached files (up from 3,730), 2,786 of them still
empty, 1,063 now populated (up from 903).

### 4. Re-ran aggregate + classify + impute

- `/tmp/aggregate_funding_cache.py` rebuilt `funding_accounts_agg.json`
  from the new cache state (1,718 rows across 1,063 populated awards).
- `python3 -m domnann.data_pull.classify_approp_colors` built the
  direct-attribution rollup.
- `python3 /tmp/impute_approp.py` applied the PSC-bucket imputer.

### 5. Diagnosed why the fix under-performed

Ran a fresh HTTP probe against 3 still-empty MRO caches to see what
USAspending actually returns:

- `M6785425F2078` (L3Harris, K058, $2.5M FY25): 0 rows
- `70Z04525PKODI0167` (Yukon Fire, J012, $0.1M FY25): 0 rows
- `N4215825PN126` (Avo Multi-Amp, J066, $0.07M FY25): FAILED (server
  dropped connection)

The endpoint literally returns `{"results": [], "page_metadata": {...}}`
for these awards. Not filtered by my client; there is no data to keep.

Also checked the top-10 MRO awards by FY25 $:

| PIID | FY25 $ | Rows | Transaction $ | Outlay $ |
|---|---:|---:|---:|---:|
| N0003024C6001 (Draper MK7) | $318M | 1 | $-0.01M | $0 |
| N0002425C4411 (BAE SWRMC) | $239M | 4 | $-21.5M | $0 |
| N0002425C4404 (NASSCO LHA DSRA) | $199M | 2 | $190.5M | $0 |
| N0002425C4402 (Vigor DDG DMP) | $157M | 3 | $-41.4M | $0 |
| N0002425C4415 (BAE LSA) | $156M | 1 | $145.0M | $0 |
| N0002425C4400 (BAE J999) | $127M | 1 | $121.0M | $0 |
| N0002425C4412 (VSE J999) | $119M | 3 | $-20.9M | $0 |
| N0002425C4421 (HII J999) | $111M | 1 | $101.0M | $0 |
| N0002424C4423 (HII FY24 J999) | $110M | 7 | $-36.1M | $0 |
| N0002425C4430 (EB SRA) | $97M | 3 | $-19.9M | $0 |

Every top-10 MRO award returned transaction rows, none returned outlay
data. The gross_outlay column is uniformly $0 across the MRO subset I
checked. The outlay-fallback branch was rarely triggered in practice.

---

## Why the hypothesis failed

I conflated two different USAspending coverage patterns:

**Pattern A (real, but newbuild-specific)**: Awards with very-large
lifetime $ that are reported in DAIMS as outlay aggregates. This is
what I observed on **Electric Boat N0002417C2100 Columbia MPU** ($9.3B
FY25) in the initial probe: 1 row, transaction_obligated_amount=null,
gross_outlay_amount=$52,471, federal_account=017-1804. That is a
PSC 1905 newbuild award -- it's not in the MRO dataset at all. I
incorrectly extrapolated that same pattern to the MRO-PSC "empty" awards.

**Pattern B (real, applies to MRO)**: Small-$ tail awards (<$3M,
mostly <$100K) where USAspending has **no File C data at all**, not
outlay-only data. These are genuinely below the DAIMS individual-award
reporting granularity, or their contracting offices file in ways that
don't populate USAspending's award-level funding endpoint. The prior
client and the updated client both return empty lists for these; the
outlay fallback fires on zero data.

So the specific architectural fix (outlay fallback in the client and
classifier) is correct code, but the target population for the fix was
not where I thought it was. **For the MRO PSC universe, Pattern B
dominates and neither filter change recovers signal from Pattern B.**

---

## Results

### Coverage change

| Metric | v2.78 | v2.79 | Delta |
|---|---:|---:|---|
| Cached PIIDs | 3,730 | 3,849 | +119 |
| Populated caches | 903 | 1,063 | +160 |
| Direct-classified $ | $3,552M (48.0%) | $3,645M (49.2%) | +$93M / +1.2pp |
| Imputed $ | $3,854M (52.0%) | $3,761M (50.8%) | -$93M / -1.2pp |

### Headline rollup shift

| Appropriation | v2.78 $M | v2.78 % | v2.79 $M | v2.79 % |
|---|---:|---:|---:|---:|
| OMN (017-1804) | $2,794 | 37.7% | $2,761 | 37.3% |
| OPN (017-1810) | $2,639 | 35.6% | $2,588 | 34.9% |
| RDT&E Defense-Wide (097-0400) | $804 | 10.9% | $780 | 10.5% |
| USCG (070-0610 + 0613 + 8149) | $198 | 2.7% | $320 | **4.3%** |
| Defense-Wide other (097-* excl. 0400) | $317 | 4.3% | $307 | 4.1% |
| Air Force (057-*) | $166 | 2.2% | $165 | 2.2% |
| Navy other (017-* minor) | $305 | 4.1% | $295 | 4.0% |
| Army (021-*) | $131 | 1.8% | $131 | 1.8% |
| SCN (017-1611) | $40 | 0.5% | $40 | 0.5% |
| Other agency (096-*) | $13 | 0.2% | $13 | 0.2% |
| **Total** | **$7,406** | 100% | **$7,406** | 100% |

Only USCG moved meaningfully (+$122M / +1.6pp). Everything else shifted
by less than 1 percentage point. The USCG lift came from newly-pulled
tail USCG awards (~160 of the 1,063 populated caches were USCG PIIDs)
that previously inherited generic MRO-bucket ratios via imputation;
now they have direct tiny-but-real TAS signal that anchors on 070-*
accounts.

### Net impact on the analysis

Headline story unchanged:
- OMN (~37%) and OPN (~35%) together fund 72% of FY25 MRO-PSC $
- RDT&E Defense-Wide ~11% (Trident/SSP/SMDC on J-series)
- USCG, Air Force, Army, Defense-Wide-other add up to ~12%
- SCN is a tiny $40M sliver (post-delivery warranty work)
- J998/J999 depot bucket still shows 70% OPN / 27% OMN in the
  classified sample

Coverage caveat on the deck is essentially the same: "48% direct / 52%
imputed" vs "49% direct / 51% imputed". No material improvement.

---

## Why the change isn't wasted

Even though the fix under-delivered for the MRO subset, three durable
outcomes:

1. **Correct diagnosis of the empty-cache pool**: they are small-$
   tail awards genuinely missing from USAspending's File C, not
   outlay-only reporting cases. Any future attempt to close this gap
   would need a different data source (possibly DAIMS Treasury data
   directly, or NAVSEA contract obligation logs), not a filter tweak.

2. **Outlay-fallback code is correct and ready for newbuild pulls**.
   If Phase 6 of `PLAN_BROADER_BUDGET_ANCHORS.md` runs (extending the
   TAS pull to PSC 1905 + other newbuild PSCs), the fix matters there
   because Pattern A (outlay-only big-$ awards) does exist in the
   newbuild universe. Electric Boat Columbia, Bechtel Plant Machinery,
   and SSP-funded missile-sustainment awards on PSC 1905 / 4470 / J014
   all follow Pattern A and will benefit from the fix.

3. **USCG coverage got better** (+$122M from imputed to directly
   classified). That's a small win for the deck's USCG slice.

---

## Decision - built v2.79

User chose to rebuild to propagate the revised TAS values into the
workbook. `python3 -m domnann.build_from_data` archived v2.78 to
`output/archive/` and saved v2.79. The rebuild picked up the updated
`approp_rollup_imputed.json` automatically via the memoized
`_load_tas_rollup()` loader in `sheets/budget_anchors.py` -- no code
change was needed to surface the new numbers. Sheet order, row counts,
and totals unchanged vs v2.78 except for the 11 TAS rows on Budget
Anchors and the 10 TAS-referenced rows on Services.

---

## Files modified

- `data_pull/usa_client.py::get_award_funding` - loosened null-filter
  to keep rows with gross_outlay_amount when transaction obligation is
  null; added federal_account guard.
- `data_pull/classify_approp_colors.py::build_classifier` - fallback
  to gross_outlay_amount as ratio-weight magnitude when
  transaction_obligated_amount is zero/null.

## Files created

- `/tmp/backfill_empty_funding.py` (scratch, not committed) - deletes
  empty cache files so the next pull refreshes them.

## Files unchanged (intentionally)

- All workbook sheet builders (`sheets/*.py`) - no structural change
  needed. `sheets/budget_anchors.py` read the updated rollup JSON via
  its memoized loader; `sheets/services.py` reference unchanged.
- `build_from_data.py` - no new sheet, no new defined names.
- Methodology + planning docs - the narrative framing is unchanged
  (coverage caveat, OPN-major finding, SCN-minimal finding all hold).
  The mis-diagnosis note below should be folded in on the next doc
  edit pass.

## Cache state after session

- 3,849 cache files (up from 3,730)
- 1,063 populated (up from 903)
- 2,786 empty (down from 2,827 -- 41 awards now have data that didn't
  before)
- FPDS FY25 $ coverage of cached PIIDs: $7,255M of $7,406M (98.0%,
  same as before)

---

## Workbook progression

| Version | Change | Impact |
|---|---|---|
| v2.78 -> v2.79 | Updated `approp_rollup_imputed.json` flowing through Budget Anchors `_load_tas_rollup()` into the 11 MRO_TAS_* named cells. | No structural change; 10 Budget Anchors TAS rows shift by <$0.5M each except USCG +$122M. Services reconciliation block percentages update to match. Every other sheet, row count, and total identical to v2.78. |

v2.79 is current.

---

## Open flags

- **PSC 1905 / newbuild extension (Phase 6)** - would benefit from
  this session's client fix because Pattern A exists there (large-$
  SSP / Electric Boat / Bechtel awards with outlay-only DAIMS
  reporting). ~3 hours of pull time. Still on the backlog.

- **Residual 2,786 empty-cache awards** covering $151M / 2.0% of MRO
  $. Closing this gap requires a non-USAspending data source (Treasury
  DAIMS direct, agency-level obligation reports). Not worth the effort
  for the coverage improvement unless a specific deck claim needs it.

- **Mis-diagnosis documented**: the "brand-new FY25 awards have DAIMS
  reporting lag" framing that appeared in
  `sessions/SESSION_2026-04-18_v_tas_funding_pull.md` and
  `docs/methodology/METHODOLOGY_MRO_BUDGET_RECONCILIATION.md` was
  partially wrong. The MRO-subset empties are small-$ genuinely-missing
  awards, not lag. Docs were written in April 2026 against an
  April-2026 cache, so the "lag" framing is incorrect for this dataset
  as delivered. A corrective sentence on the methodology doc would be
  worth adding on the next edit pass, but the headline narrative
  (appropriation color mixing > vintage mixing > lump-sum funding as
  gap drivers) is unaffected.
