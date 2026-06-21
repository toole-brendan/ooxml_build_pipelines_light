---
title: Data sources and methodology
---

# Data sources and methodology

This chapter describes the three public data sources used to construct the visible annual outsourced-flow estimate for U.S. nuclear submarine construction, the pull strategies for each, and the aggregation methodology applied to the raw data. The companion lessons-learned material in `reference_prior_analysis/Federal_Procurement_Research_Lessons_Learned.md` and `reference_prior_analysis/Subaward_Pull_Lessons_Learned.md` provides the underlying field-tested gotchas; this chapter summarizes the parts that affect the visible outsourced-flow numbers in this wiki.

## Three primary sources

The visible outsourced flow is constructed from three public sources:[^repo-readme][^repo-manifest][^repo-guide]

1. **U.S. Navy FY2027 President's Budget Shipbuilding and Conversion (SCN) Justification Book and 30-Year Shipbuilding Plan** — the authoritative source for class-level dollar totals, per-ship cost-category breakdowns, production schedules, and the contractual home of the Maritime Industrial Base supplier-development flow. The repository extracts this into `extracted/scn_li_*.csv` via the parser at `scripts/extract_scn_submarine_lines.py`.[^scn-fy27pb][^scn-30yr-pb27][^repo-scn-extract][^repo-scn-script]
2. **Federal Procurement Data System (FPDS) Atom Feed** — the authoritative public source for federal prime contract action records, used to capture prime obligations on GDEB submarine contracts, Bechtel Plant Machinery naval-reactor contracts, Lockheed Martin combat-system and Trident contracts, and the broader supplier-prime universe. The repository pulls FPDS via `scripts/pull_fpds_sub_primes.py` and stores raw JSON in `fpds_raw/`.[^fpds-atom][^repo-fpds-script]
3. **USAspending.gov `/api/v2/subawards/` endpoint** — the public source for first-tier subaward records under FFATA-reportable prime contracts, used to capture the first-tier supplier base under each in-scope submarine prime PIID. The repository pulls subawards via `scripts/pull_usaspending_subawards.py` and stores per-PIID JSON in `usaspending_subawards/`.[^usaspending-api][^repo-usaspending-script]

A fourth source — **SAM.gov Opportunities API** for pre-award solicitations and pipeline analysis — is documented in the companion field guide but is not used for the current outsourcing measurement, which is execution-focused.[^repo-guide]

## FPDS pull strategy

The companion lessons-learned material recommends a three-round FPDS search pattern for any new program domain:[^repo-lessons-v1]

1. **Description-keyword sweeps** to find the prime contractors associated with the program.
2. **Vendor-name sweeps** for the primes identified in round 1, to catch contracts with vague or non-matching descriptions.
3. **Agency + dollar-floor backstop sweep** to catch contracts that fell through both keyword and vendor cracks.

The submarine pull applies this pattern across 13 named queries, all with `SIGNED_DATE:[2018/01/01,2026/12/31]` and `CONTRACTING_AGENCY_ID:"1700"` (U.S. Navy):[^repo-fpds-summary][^repo-fpds-script]

| Query slug | Type | Records | Unique PIIDs |
|---|---|---:|---:|
| `gdeb_navy` | Vendor (Electric Boat) | 3,000 (capped at 300 pages) | 166 |
| `hii_nns_navy` | Vendor (Newport News + Huntington Ingalls) | 5,731 | 1,516 |
| `bpmi_navy` | Vendor (Bechtel Plant Machinery) | 97 | 19 |
| `lockheed_navy_sub` | Vendor + description (Virginia/Columbia/Submarine/Trident) | 292 | 34 |
| `northrop_navy_sub` | Vendor + description (Submarine/Virginia/Columbia/Sonar) | 132 | 12 |
| `bae_navy_sub` | Vendor + description (Subassembly/Virginia) | 2,222 | 505 |
| `l3harris_navy_sub` | Vendor + description (Submarine/Photonic) + Kollmorgen | 44 | 13 |
| `curtiss_wright_navy` | Vendor only | 2,490 | 991 |
| `rolls_royce_navy_sub` | Vendor only | 2,980 | 1,391 |
| `blueforge_navy` | Vendor only | 3,901 | 1,972 |
| `desc_virginia_class` | Description (Virginia Class) | 420 | 124 |
| `desc_columbia_class` | Description (Columbia Class / Columbia SSBN) | 237 | 63 |
| `desc_submarine_navy_big` | Description (SUBMARINE) + OBLIGATED_AMOUNT $50M+ | 7 | 6 |

The vendor field used throughout is `VENDOR_NAME:"..."` rather than `UEI_NAME` or `VENDOR_FULL_NAME`. Companion testing documented in v1 of the lessons-learned file shows that `VENDOR_NAME:` is the only reliable vendor field — `UEI_NAME` returns partial matches, `VENDOR_FULL_NAME` and `LEGAL_BUSINESS_NAME` return zero results, and direct `VENDOR_UEI:` lookups on numeric UEI codes also fail.[^repo-lessons-v1]

Three queries lack description filters and over-collect: `curtiss_wright_navy`, `rolls_royce_navy_sub`, and `blueforge_navy`. Their record counts include substantial non-submarine activity (Curtiss-Wright Navy nuclear work generally, Rolls-Royce Navy aircraft engines, and substring matches on unrelated "Blue *" vendors). The annual obligation columns for these three vendor groups in `extracted/fpds_annual_by_prime.csv` should be treated as upper bounds, not as net submarine exposure.[^repo-fpds-summary]

The GDEB query is capped at the script's 300-page pagination limit, returning 3,000 records against an estimated true count of approximately 7,520 records. This affects the latest-mod cumulative aggregate displayed in the pull log, but does not affect the per-modification annual aggregation because the latter aggregates at the modification level rather than at the latest-mod level.[^repo-fpds-summary][^repo-fpds-script]

## USAspending subaward pull strategy

The subaward pull uses the two-call workflow documented in v1 of the lessons-learned material:[^repo-lessons-v1][^repo-usaspending-script]

1. For each in-scope PIID, POST to `/api/v2/search/spending_by_award/` with `filters.award_ids` containing the PIID and `filters.award_type_codes` containing the Contracts group `["A", "B", "C", "D"]`. If the response has zero results, retry with the IDV group `["IDV_A", "IDV_B", "IDV_B_A", "IDV_B_B", "IDV_B_C", "IDV_C", "IDV_D", "IDV_E"]`. The response yields a `generated_internal_id` (gid).
2. POST to `/api/v2/subawards/` with `award_id` set to the gid, `limit=100`, `page=1`, `sort=amount`, `order=desc`. Page until the response's `page_metadata.hasNext` is false, with a maximum of 25 pages.

The 17 seed PIIDs cover the major GDEB submarine PIIDs, the major Bechtel naval-reactor PIIDs, and several other GFE-prime PIIDs (LM Virginia combat systems, BAE forward subassembly, Rolls-Royce rotor). Of the 17, two hit the script's approximately 2,500-record retrieval cap (25 pages × 100 records: the GDEB Virginia Block V/VI master and the GDEB Columbia Build I+II), five returned zero subawards (Block II residual, VPM Tube Fabrication, SSBN-R concept, BPMI FY26 Virginia, LM Virginia combat systems), and ten returned non-zero counts between 7 and 1,622 records.[^repo-usaspending-summary]

The sort-by-amount-descending strategy maximizes the dollar value captured when the cap is hit, at the cost of losing the long tail of small subs. The companion v1 lessons-learned material documents this as a deliberate trade-off: for a top-spend analysis, the largest subs are what matter; for a complete supplier-count, the cap is a hard limit.[^repo-lessons-v1]

## SCN PDF extraction

The FY2027 President's Budget SCN Justification Book is delivered as a roughly 700-page PDF. The repository script `scripts/extract_scn_submarine_lines.py` parses the layout-preserved `pdftotext --layout` rendering and extracts three tables for each of two line items (LI 1045 Columbia, LI 2013 Virginia):[^repo-scn-script]

- The **P-40 Budget Line Item Justification** resource summary (Prior Years / FY25 actual / FY26 estimate / FY27 base / FY27 OOC / FY27 total / FY28–31 outyears / "To Complete" / class Total).
- The **P-5c Ship Cost Analysis** per-hull cost-category breakdown (Plan Costs, Basic Construction/Conversion, Change Orders, Electronics, Technology Insertion, Propulsion Equipment, Hull-Mechanical-Electrical, Ordnance, Other Cost, Total Ship Estimate).
- The **P-27 Ship Production Schedule** (hull number, shipbuilder, fiscal year, contract award date, start of construction, delivery date).

The parser is line-grep-based — not a fully robust PDF parser — and is intended for the specific layout of the FY27 PB SCN book. Re-running against a different PB cycle would likely require parser updates. Output is written to `extracted/scn_li_resource_summary.csv`, `extracted/scn_li_cost_categories.csv`, and `extracted/scn_li_production_schedule.csv`.[^repo-scn-extract]

## Aggregation methodology

The repository's aggregator at `scripts/aggregate_annual_outsourcing.py` produces three CSV outputs:[^repo-aggregate-script]

1. `extracted/fpds_annual_by_prime.csv` — per-fiscal-year sum of per-modification `obligatedAmount` (this-action only, **not cumulative**) on all FPDS raw records, deduplicated by `(full_piid, mod_number, signed_date)`, bucketed by signed-date fiscal year, and grouped into 10 vendor groups via regex on the `vendor_name` field (GDEB, HII-NNS, BPMI, LM, NG, BAE, L3Harris, Curtiss-Wright, Rolls-Royce, BlueForge).
2. `extracted/subaward_annual_by_prime.csv` — per-fiscal-year sum of USAspending subaward `amount` values bucketed by `action_date` fiscal year and by prime PIID, across the 12 in-scope PIIDs with non-zero subaward records.
3. `extracted/subaward_top_recipients.csv` — top 200 first-tier subaward recipients across all in-scope PIIDs combined, summed across the FY13–FY25 action-date window.

### Cumulative versus window dollars

For the FPDS per-vendor-group annual roll-up, the aggregator sums per-modification `obligatedAmount` (`this_obligated` in the parsed JSON) by signed-date fiscal year. It does **not** use the `totalObligatedAmount` field (cumulative since contract inception), which would massively over-count for contracts that started before the FY2018 window.

The companion v1 lessons-learned material documents this with a Block IV worked example: contract `N0002412C2115` (Virginia Block IV) carries a $19.90 billion cumulative `totalObligatedAmount` at its latest in-window modification, but the **true new-money obligation inside the FY18–FY26 window is only approximately $22 million**. The remainder was committed before the window. Naive cumulative aggregation would overstate Block IV's window outsourcing by approximately 900×.[^repo-lessons-v1]

For the USAspending subaward roll-up, the aggregator sums `amount` values by `action_date` fiscal year. Subaward `action_date` is the date the sub action was reported, not the prime modification's signed date; the two can differ by months. The aggregator treats them as equivalent for fiscal-year bucketing purposes, which is appropriate for a smoothed annual view.

### Vendor-group regex

The aggregator's vendor-group regex patterns are:[^repo-aggregate-script]

```
GDEB        = ELECTRIC BOAT
HII-NNS     = NEWPORT NEWS SHIPBUILDING | HUNTINGTON INGALLS
BPMI        = BECHTEL PLANT MACHINERY
LM          = LOCKHEED MARTIN
NG          = NORTHROP GRUMMAN
BAE         = BAE SYSTEMS
L3Harris    = L3HARRIS | L-?3 TECHNOLOGIES | KOLLMORGEN
Curtiss-W   = CURTISS.?WRIGHT
Rolls-R     = ROLLS.?ROYCE
BlueForge   = BLUEFORGE | BLUE FORGE
```

These match against the `vendor_name` field on each FPDS record. Records that do not match any pattern are silently dropped from the vendor-group roll-up but retained in the underlying per-mod records. The patterns do **not** apply parent-company normalization: General Dynamics Mission Systems, GDIT, NASSCO, and other GD entities are not rolled up to General Dynamics; Aerojet Rocketdyne (now part of L3Harris) is not rolled up to L3Harris; Marinette Marine (Fincantieri) is not rolled up to its parent. For a top-line view of the submarine industrial base, this is acceptable because the dominant primes appear under their dominant submarine-related legal entity names. For cross-program rollups, a hand-curated parent-company mapping table would be required, as described in v2 of the lessons-learned material.[^repo-lessons-v2]

### Reading mod descriptions to identify programs

The companion v1 lessons-learned material documents a separate analytical technique that is not applied in the current aggregator but is worth noting for any future refinement: **reading FPDS modification descriptions for hull-number references** to identify which block, build, or program a contract is funding.[^repo-lessons-v1]

Modification descriptions frequently include strings like `"SSN 792 CONSTRUCTION (BOAT 1, FY14)"`, `"SSN 812 CONSTRUCTION (BOAT 2, FY 24)"`, `"MOUNTING BOX PROCEDURE CHANGE SSBN 826/827"`, `"USS HARTFORD (SSN 768) EOH EXECUTION"`, and so on. These unambiguously identify which boat the modification is funding. The Virginia block crosswalk is:

| Hull | Block |
|---|---|
| SSN 774–779 | Block I |
| SSN 780–785 | Block II |
| SSN 786–791 | Block III |
| SSN 792–801 | Block IV |
| SSN 802–811 | Block V |
| SSN 812–820 | Block VI |

For Columbia, SSBN 826 is Build I (USS *District of Columbia*) and SSBN 827 is Build II (USS *Wisconsin*).

The reliable rule is that **the PIID year prefix is not a reliable indicator of which block or build the contract funds**. A contract with a year-2017 PIID prefix (`N0002417C2100`) is currently funding Block VI Boat 2 hull work in FY26 through extended modifications. Only the mod description reliably tells you which hull and which block.

## Known aggregator limitation — no v3 dedup

The aggregator's USAspending subaward summation is a **naive sum** of the `amount` field across all returned subaward records, with no per-`sub_id` MAX dedup, no identical-amount collapse across different sub_ids, and no cap at the prime contract's total value.[^repo-aggregate-script]

The companion v2 lessons-learned material documents that this approach can inflate apparent subaward totals by **5×–50×** when the underlying USAspending records exhibit the cumulative-snapshot duplication pattern: the same `subaward_number` appearing at multiple `action_date` values, each at a slightly different cumulative-style amount. A worked example in the v2 file shows that a $500M Marinette Marine subcontract on a Lockheed Martin Littoral Combat Ship prime was naively summed to $47.17 billion, with v3 dedup correcting it to $2.49 billion.[^repo-lessons-v2]

The corrective methodology is a three-stage dedup:

1. **Stage 1: Per `sub_id`, take MAX amount.** Handles cumulative-snapshot duplicates with the same `sub_id` (the most common failure mode).
2. **Stage 2: Per `(recipient, amount)`, keep one record.** Handles cases where USAspending issues separate `sub_id` values for the same underlying subcontract under different prime modifications, at the same cumulative amount.
3. **Stage 3: Per `(recipient, prime)`, cap at 1.0× prime size and exclude any pair exceeding 2× prime size.** Handles phantom-amount data corruption — for example, the documented "phantom $920M" case in which five unrelated recipients each reported the same impossible $920 million on a $197M depot prime.

The submarine subaward dataset has not yet been re-run through v3 dedup. The top-recipient and per-FY subaward totals reported in this wiki are naive sums and may be overstated for the largest recipients with the longest-running primes (BlueForge Alliance, Northrop Grumman Systems, BAE Systems Land & Armaments, Curtiss-Wright Electro-Mechanical). The BlueForge $4.21 billion figure is reported across 7 subaward actions, which is structurally inconsistent with the cumulative-snapshot pattern (the pattern requires many actions on one `sub_id`), so the BlueForge figure is more likely to be roughly correct than the others. The Northrop Grumman $2.21 billion figure spans many more actions (84 combined Virginia and Columbia per companion analysis) and is more likely to have cumulative-snapshot inflation.[^repo-lessons-v2][^repo-subaward-top][^repo-sam-prior]

A future revision applying v3 dedup would tighten the headline subaward totals downward by an unknown but potentially material factor. This is flagged in [Annual outsourced flow estimate](08-annual-outsourced-flow.md#confidence-and-what-would-improve-it) and [Limitations and blind spots](10-limitations-and-blind-spots.md).

## Politeness, rate limits, and incremental save

The FPDS Atom Feed is paginated at 10 records per page. The repository pull script uses a 0.35-second delay between pages and supports up to 300 pages per query (3,000 records). The User-Agent header identifies the client.[^repo-fpds-script]

The USAspending API has no documented rate limit. The repository pull script uses a 0.5-second delay between pages of the same PIID and a 0.3-second delay between PIIDs.[^repo-usaspending-script]

Neither script implements the **incremental cache + `_complete` flag** resumability pattern recommended in v2 of the lessons-learned material for long-running pulls.[^repo-lessons-v2] For the 17-PIID submarine pull, the full run is approximately 5–10 minutes, so single-run completion is reliable in practice.

## Re-running the pulls

The pulls are re-runnable via:

```bash
# 1. Re-extract from the SCN PDF (~1 second)
python3 scripts/extract_scn_submarine_lines.py

# 2. Re-pull FPDS (~20–30 minutes due to pagination + politeness delays)
python3 scripts/pull_fpds_sub_primes.py

# To re-run only one FPDS query:
python3 scripts/pull_fpds_sub_primes.py gdeb_navy

# 3. Re-pull USAspending subawards (~5–10 minutes)
python3 scripts/pull_usaspending_subawards.py

# To also pull subawards for top PIIDs discovered in the FPDS data:
python3 scripts/pull_usaspending_subawards.py --discover

# 4. Aggregate everything (<30 seconds)
python3 scripts/aggregate_annual_outsourcing.py
```

The repository script paths in the existing files reference `/Users/brendantoole/projects2/submarine_outsourced_work/`, the macOS path under which the original pull was performed.[^repo-fpds-script][^repo-usaspending-script][^repo-aggregate-script]

[^repo-readme]: submarine_outsourced_work, "README.md." See full citation under [References](INDEX.md#references).

[^repo-manifest]: submarine_outsourced_work, "MANIFEST.md." See full citation under [References](INDEX.md#references).

[^repo-guide]: Federal Procurement Data Pull — Practical Guide (April 2026). See full citation under [References](INDEX.md#references).

[^scn-fy27pb]: U.S. Navy FY2027 PB SCN Justification Book. See full citation under [References](INDEX.md#references).

[^scn-30yr-pb27]: U.S. Navy FY2027 PB 30-Year Shipbuilding Plan. See full citation under [References](INDEX.md#references).

[^repo-scn-extract]: submarine_outsourced_work, parsed SCN extracts. See full citation under [References](INDEX.md#references).

[^repo-scn-script]: submarine_outsourced_work, `scripts/extract_scn_submarine_lines.py`. See full citation under [References](INDEX.md#references).

[^fpds-atom]: U.S. GSA, FPDS Atom Feed. See full citation under [References](INDEX.md#references).

[^repo-fpds-script]: submarine_outsourced_work, `scripts/pull_fpds_sub_primes.py`. See full citation under [References](INDEX.md#references).

[^usaspending-api]: USAspending.gov REST API. See full citation under [References](INDEX.md#references).

[^repo-usaspending-script]: submarine_outsourced_work, `scripts/pull_usaspending_subawards.py`. See full citation under [References](INDEX.md#references).

[^repo-lessons-v1]: Federal Procurement Research — Lessons Learned & Best Practices (v1). See full citation under [References](INDEX.md#references).

[^repo-fpds-summary]: submarine_outsourced_work, "fpds_raw/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-usaspending-summary]: submarine_outsourced_work, "usaspending_subawards/_summary.json." See full citation under [References](INDEX.md#references).

[^repo-aggregate-script]: submarine_outsourced_work, `scripts/aggregate_annual_outsourcing.py`. See full citation under [References](INDEX.md#references).

[^repo-lessons-v2]: Subaward Pull Lessons Learned (v2). See full citation under [References](INDEX.md#references).

[^repo-subaward-top]: submarine_outsourced_work, "extracted/subaward_top_recipients.csv." See full citation under [References](INDEX.md#references).

[^repo-sam-prior]: SAM Submarine & Cutter Contract Awards (April 2026). See full citation under [References](INDEX.md#references).
