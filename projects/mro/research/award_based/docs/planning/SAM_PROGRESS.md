# SAM Implementation Progress

Status of the Serviceable Addressable Market (SAM) build -- subaward
enrichment, ratio computation, and workbook integration.

---

## What We're Doing

Sizing the portion of Navy/CG spending that flows to subcontractors.
This is the addressable market for companies that don't hold prime ship
contracts but supply systems, components, or services to the primes.

The SAM is derived from three data signals already on every classified
award (from FPDS), plus subaward summary data pulled from USAspending's
detail endpoint:

| Signal | Source | Coverage |
|---|---|---|
| PSC code (19xx = vessel) | FPDS | Every award |
| GFE/GFP (govt-furnished equipment) | FPDS | Every award |
| Subcontracting plan (mandatory/not) | FPDS | Every award |
| Subaward count + amount (lifetime) | USAspending detail API | Top 250 per service |

---

## Plan (from SUBCONTRACT_DATA_PLAN.md)

| Phase | Description | Status |
|---|---|---|
| **1** | Enrichment script + Subcontract Data sheet | **Done** |
| **2** | Sub Ratios sheet (SUMIFS against SubAwards table) | **Done** |
| **3** | SAM formulas on Product Procurement / Services | Not started |
| **4** | Competitive Dynamics View 1 (prime x hull program) | Not started |
| **5** | Subcontractor landscape (individual subaward records) | Future |

---

## What Was Built

### Phase 1: Data Pull + Subcontract Data Sheet

**`data_pull/enrich_subawards.py`** -- Standalone enrichment script.

- Reads classified JSON (does not modify it)
- Sorts by FY2025 obligation, takes top N awards (default 250)
- Calls `usa_client.get_award_detail()` for each award (cached to disk)
- Extracts three USAspending-only fields: `subaward_count`,
  `total_subaward_amount`, `lifetime_obligation`
- Computes `sub_ratio` = total_subaward_amount / lifetime_obligation
- Writes enriched JSON to `data_pull/output/fpds/`

Usage:
```
python3 data_pull/enrich_subawards.py --top 250
python3 data_pull/enrich_subawards.py --top 250 --group cg
python3 data_pull/enrich_subawards.py --top 100 --dry-run
```

Output files:
- `data_pull/output/fpds/navy_fy2025_subaward_enriched.json` (247 awards)
- `data_pull/output/fpds/cg_fy2025_subaward_enriched.json` (249 awards)

**`sheets/subcontract_data.py`** -- Subcontract Data sheet builder.

- Loads both enriched JSON files
- 14 columns: Service, PIID, Vendor, Parent Company, Hull Program, PSC,
  PSC Description, GFE, Sub Plan, FY2025 Obligation, Lifetime Obligation,
  Subaward Count, Subaward Amount, Sub Ratio (formula)
- Excel table name: `SubAwards` (referenced by Sub Ratios sheet)
- 496 rows (247 Navy + 249 CG)

### Phase 2: Sub Ratios Sheet

**`sheets/sub_ratios.py`** -- Sub Ratios sheet builder.

Four sections, all computed via SUMIFS/COUNTIFS against the SubAwards table:

1. **Core SAM Ratios** (rows 6-10) -- the cells that Phase 3 SAM formulas
   will reference:
   - D6: Vessel GFE=Y ratio (low ratio)
   - D7: Vessel GFE=N ratio (standard ratio)
   - D8: Non-vessel w/ mandatory sub plan ratio
   - D9: Non-vessel no mandatory plan ratio
   - D10: Overall weighted average

2. **Ratios by Hull Program** (26 programs + Unclassified + Total)

3. **Ratios by Prime Contractor** (top 20 + Other + Total)

4. **Ratios by PSC Group** (18 groups + Other + Total)

### Workbook Updates

`build_from_data.py` updated. Current sheet order:

1. Overview (navy blue)
2. Product Procurement (green)
3. Services (green)
4. **Sub Ratios** (teal) -- new
5. Competitive Dynamics (dark red, still placeholder)
6. **Subcontract Data** (slate) -- new
7. Awards Data (slate)
8. Vessel Taxonomy (slate)

Current version: `output/08APR2028_Newbuild_and_MRO_Spend_v2.17.xlsx`

---

## Key Data Findings

### Enrichment Results

| Metric | Navy | Coast Guard |
|---|---|---|
| Awards enriched | 247 | 249 |
| % of total FY2025 $ covered | 83.4% | 86.9% |
| Awards with subaward reporting | 143 (58%) | 9 (4%) |
| Total subaward amount | $79.1B | $10.6M |
| Total lifetime obligation | $257.7B | $4.8B |
| Weighted ratio | **30.7%** | **0.2%** |
| Failed lookups | 3 | 1 |

CG subaward reporting is effectively nonexistent -- only 9 of 249 top
awards have any reported subawards. The SAM for CG will need to rely
entirely on the sub plan and GFE signals, not empirical subaward ratios.

### Navy Ratio Context

The 30.7% weighted average is higher than expected and is inflated by
outlier awards (see Issues below). Removing the 6 outlier awards drops
the ratio to approximately 17%.

---

## Issues and Limitations

### 1. Subaward Over-Reporting (6 awards with ratio > 100%)

Six Navy awards show subaward amounts exceeding their lifetime obligation,
sometimes dramatically:

| PIID | Vendor | Ratio | Sub Amount | Obligation |
|---|---|---|---|---|
| N0002418C2300 | Lockheed Martin (LCS) | 843% | $13.7B | $1.6B |
| N0002418C2301 | Lockheed Martin (LCS) | 610% | $20.5B | $3.4B |
| N0002417C6311 | Northrop Grumman | 302% | $1.5B | $0.5B |
| N0002424C4201 | QED Systems | 173% | $163M | $94M |
| N0001924F1885 | Rolls-Royce | 136% | $221M | $163M |
| N0002418C5218 | Lockheed Martin | 115% | $1.1B | $966M |

**Cause:** USAspending aggregates subaward reporting at the program level,
not the contract level. The LCS contracts show all program subawards under
one PIID even when they span multiple contracts or delivery orders.

**Impact:** These 6 awards contribute ~$37B to the $79B subaward total,
inflating the weighted ratio from ~17% to 30.7%.

**Fix (implemented in v2.17):** Added `Include in Ratio` boolean column
to SubAwards table (= Sub Ratio <= 100%). The 6 outlier awards are
flagged FALSE. All SUMIFS/COUNTIFS on the Sub Ratios sheet filter on
`SubAwards[Include in Ratio]=TRUE`, excluding the unreliable data
points entirely. Raw subaward amounts stay visible on Subcontract Data
for transparency -- nothing hidden, just flagged. The overall weighted
ratio with exclusions is ~17%.

### 2. Timing Asymmetry in Subaward vs Obligation Reporting

Both `total_obligation` and `total_subaward_amount` from USAspending are
cumulative-to-date, not lifetime projections. The ratio is
cumulative-over-cumulative at the same point in time -- apples-to-apples
for mature contracts.

However, there is a reporting lag:
- Obligations are recorded immediately when a contract mod is signed
- Subaward reporting lags -- primes have 30 days per FAR 52.204-10,
  but compliance varies

This means the ratio is **understated for newer contracts** where the
government has obligated money but the prime hasn't reported the
corresponding subawards yet. The overall weighted ratio is biased
slightly downward.

### 3. CG Subaward Data Is Effectively Useless

Only 9 of 249 top CG awards have any reported subawards, totaling $10.6M
against $4.8B in obligations. The 0.2% ratio is not a real
subcontracting ratio -- it reflects near-zero reporting.

For CG SAM sizing, we will need to rely on the subcontracting plan field
and possibly apply Navy-derived ratios as proxies, rather than using
CG-specific empirical ratios.

### 4. Parent Company Names Are Not Normalized

FPDS `ultimate_parent_name` has duplicates for the same corporate parent:
- "HUNTINGTON INGALLS INCORPORATED" / "HUNTINGTON INGALLS INDUSTRIES INC."
  / "HUNTINGTON INGALLS INC" (three entries, same company)
- "RAYTHEON COMPANY" / "RAYTHEON TECHNOLOGIES CORPORATION"
  (pre/post-merger names)
- "ELECTRIC BOAT CORPORATION" appears separately from
  "GENERAL DYNAMICS CORPORATION" despite being a GD subsidiary

This affects the Ratios by Prime section and will affect the Competitive
Dynamics sheet (Phase 4). Fixing this requires a manual parent-name
normalization mapping.

---

## Next Steps

### Phase 3: SAM Formulas on Product Procurement / Services

Add SAM calculation to the existing cross-tab sheets. Each cell currently
shows TAM (total spend by PSC x hull program). The SAM version applies
the ratio from the Sub Ratios sheet:

```
For vessel PSC (19xx):
  SAM = TAM * IF(GFE="Y", 'Sub Ratios'!D6, 'Sub Ratios'!D7)

For non-vessel PSC:
  SAM = TAM * 'Sub Ratios'!D8
```

Open question: whether to add SAM as a parallel table, a column next to
each hull program, or a separate row under each PSC row.

### Before Phase 3: Fix the Ratio

Need to decide on the capping approach for outlier awards. The uncapped
30.7% ratio is misleading; the capped ~17% ratio may be too conservative.
Options:

1. Cap subaward amount at lifetime obligation (floor ratio at 100%)
2. Exclude the 6 outlier awards entirely from ratio computation
3. Use the capped ratio as default but show both on Sub Ratios for
   transparency

### Phase 4: Competitive Dynamics

Build the prime x hull program cross-tab. Requires parent name
normalization first (Issue #4 above).

---

## Pipeline to Rebuild

Full rebuild from existing data (no API calls):
```
cd /Users/brendantoole/projects2 && python3 -m domnann.build_from_data
```

To re-run enrichment (uses cached API responses):
```
python3 data_pull/enrich_subawards.py --top 250
python3 data_pull/enrich_subawards.py --top 250 --group cg
```
