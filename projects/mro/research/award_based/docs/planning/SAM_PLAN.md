# SAM Methodology -- Identifying Outsourceable Work

How to define and size the Serviceable Addressable Market (SAM) for subcontractors
and module suppliers within Navy and Coast Guard ship spending.

---

## Goal

Identify the portion of Navy/CG spending that is outsourceable -- work that is
or could be performed by subcontractors rather than the prime contractor. This
is the addressable market for companies that don't hold prime ship contracts but
supply systems, components, or services to the primes.

---

## Signals Available in the Data

Three fields in the FPDS-sourced awards data provide evidence of outsourcing:

### 1. Subcontracting Plan (strong signal)

The `subcontracting_plan` field records whether a contract has a formal
subcontracting plan. FY2025 Navy breakdown:

| Value | Awards | FY2025 $ | What it means |
|---|---|---|---|
| INDIVIDUAL SUBCONTRACT PLAN | 2,897 | $45.7B | Formal plan to subcontract -- prime is required to flow work to subs |
| DOD COMPREHENSIVE SUBCONTRACT PLAN | 404 | $12.6B | Company-wide sub plan (same implication, just structured differently) |
| PLAN NOT REQUIRED | 14,384 | $15.3B | Below threshold or small business -- these contractors often ARE the subs |
| COMMERCIAL SUBCONTRACT PLAN | 517 | $0.7B | Commercial-item subcontracting |
| PLAN REQUIRED - INCENTIVE NOT INCLUDED | 28 | $1.0B | Plan required but no incentive structure |
| NO SUBCONTRACTING POSSIBILITIES | 1,141 | $0.4B | Sole-source, no sub opportunity |

The $45.7B + $12.6B = $58.3B with mandatory subcontracting plans is the pool
where outsourced work lives. Industry benchmarks for major shipbuilding programs
indicate 40-60% of prime contract value flows to subcontractors.

### 2. GFE/GFP -- Government Furnished Equipment (structural signal)

The `gfe_gfp` field indicates whether the government furnishes equipment to the
contractor. This reveals the flow of modules between contracts:

| Scenario | FY2025 $ | Interpretation |
|---|---|---|
| 19xx vessel + GFE=Y | $8.6B | Shipyard receives govt-furnished modules for integration. Those modules were bought under separate contracts -- they ARE the outsourced module work. |
| 19xx vessel + GFE=N | $29.9B | Shipyard provides everything. Subcontracting happens internally (prime buys from its own supply chain). |
| Non-19xx + GFE=Y | $20.4B | Module contractor receives govt-furnished components to integrate into their deliverable. Integration at the module level. |
| Non-19xx + GFE=N | $16.8B | Module contractor provides everything. They are the full module supplier -- a subcontractor's customer or a direct Navy supplier. |

### 3. USAspending Subaward Data (ground truth, fragmented)

USAspending tracks reported first-tier subcontract awards under prime contracts.
Two levels of data are available:

**Award-level summary** (via `get_award_detail()`):
- `subaward_count`: number of reported subawards
- `total_subaward_amount`: sum of reported subaward dollars

**Individual subaward records** (via `get_subawards()`):
- `recipient_name`: who the subcontractor is
- `amount`: how much they received
- `description`: what the subcontracted work is
- `action_date`: when the subaward was made

**Coverage caveat**: Subaward reporting is mandatory for contracts over $30K, but
the quality and granularity of reporting varies dramatically by prime:
- **HII (Huntington Ingalls)**: Reports detailed subawards, often with SWBS-like
  descriptions. Best data source for understanding what work flows to subs on
  carrier and amphibious ship programs.
- **Electric Boat**: Moderate reporting. Some subawards identifiable.
- **BIW (Bath Iron Works)**: Poor reporting. Minimal subaward detail.
- **Combat system primes** (Raytheon, Lockheed Martin): Variable -- some programs
  report well, others don't.

Despite fragmentation, the subaward data is the only source that shows actual
subcontractor names and dollar flows. Even partial coverage on the top 50-100
contracts would reveal significant SAM structure.

---

## First Move: USAspending Subaward Pull

Before committing to a SAM methodology, pull the subaward data and see what it
gives us. The data quality will determine how much we can rely on it vs the
sub plan and GFE signals above.

### Step 1: Enrich awards with subaward summary

Run `--enrich` on the deduped Navy data to add `subaward_count` and
`total_subaward_amount` to each award. This uses the USAspending award detail
endpoint (`get_award_detail()`) and adds two fields per award.

This tells us: which awards have reported subawards, and how much total
subaward volume is reported.

**How to run:**

The existing `pull_fpds_v2.py --enrich` flag calls `enrich_with_detail()` which
hits USAspending's award detail API for each award. However, with 19,668 Navy
awards at 0.15s rate limiting, a full enrichment run would take ~50 minutes.

More practical approach: write a standalone enrichment script that:
1. Loads the deduped classified JSON (already has `generated_internal_id` per award)
2. Calls `get_award_detail()` for each award (cached to disk, skips already-fetched)
3. Writes `subaward_count` and `total_subaward_amount` back to the classified JSON
4. Outputs a summary: how many awards have subawards, total reported subaward dollars

Can be interrupted and resumed since each detail call is cached individually.

### Step 2: Pull individual subaward records for top contracts

For the top 50-100 awards by FY2025 obligation that have `subaward_count > 0`,
pull the full subaward detail using `get_subawards()`. This gives us individual
subcontractor names, amounts, and descriptions.

**How to run:**

Write a script that:
1. Loads enriched Navy JSON
2. Filters to awards with subaward_count > 0, sorted by FY2025 obligation
3. Calls `get_subawards(generated_internal_id)` for each (cached to disk)
4. Aggregates: top subcontractors by total subaward volume, most common work
   descriptions, subaward concentration (does 80% of sub spend go to 5 companies?)

### Step 3: Assess data quality and decide next steps

After Steps 1 and 2, we'll know:
- What % of Navy spending has reported subaward data
- Whether the descriptions are useful for SAM classification
- Which primes report well and which don't
- Whether subaward data alone can size the SAM or if we need the sub plan /
  GFE signals as supplements

Possible outcomes:
- **Subaward data is rich enough** -> build SAM directly from subaward records,
  with sub plan field as validation
- **Subaward data is fragmented** -> use sub plan field to identify contracts
  with outsourcing, apply industry subcontracting ratios (40-60%) to estimate
  SAM, use subaward data for the contracts where it's available as ground truth
- **Hybrid** -> use subaward data where available, fill gaps with sub plan +
  industry ratios, flag confidence level per contract

---

## Existing Infrastructure

All the API clients and caching are already built:

| Component | Location | Status |
|---|---|---|
| `get_award_detail()` | `data_pull/usa_client.py:243` | Working, caches to disk |
| `get_subawards()` | `data_pull/usa_client.py:448` | Working, caches to disk |
| `enrich_with_detail()` | `data_pull/pull_fpds_v2.py:780` | Working, adds subaward_count + total_subaward_amount |
| `generated_internal_id` | On every award in deduped JSON | The key for USAspending lookups |
| Detail cache dir | `data_pull/output/fpds/detail/` | Per-award JSON cache |
| Subaward cache dir | Needs to be defined | Per-award subaward JSON cache |

No new API clients needed. The `--enrich` flag on the pull script already does
Step 1, but a standalone script would be more practical for running against the
already-deduped data without re-pulling from FPDS.
