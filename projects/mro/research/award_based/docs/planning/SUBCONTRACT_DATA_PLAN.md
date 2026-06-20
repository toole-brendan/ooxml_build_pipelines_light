# Subcontract Data and Ratio Calculation Plan

Two new sheets and the data pipeline that feeds them. The Subcontract
Data sheet holds the enriched award records. The Sub Ratios sheet
computes the ratios used by the SAM formulas on Product Procurement
and Services.

---

## Data Flow

```
USAspending detail API
    |
    v
enrich_subawards.py (new script)
    |
    v
navy_fy2025_subaward_enriched.json (new file, top ~250 awards)
    |
    v
sheets/subcontract_data.py (new sheet builder)
    |
    v
"Subcontract Data" sheet (Excel table: SubAwards)
    |
    v
sheets/sub_ratios.py (new sheet builder)
    |
    v
"Sub Ratios" sheet (summary ratio tables, referenced by SAM formulas)
    |
    v
Product Procurement / Services sheets (SAM = TAM * ratio from Sub Ratios)
```

---

## Step 1: Enrichment Script

### `data_pull/enrich_subawards.py` (new)

Standalone script that enriches the top N awards with subaward summary
data from the USAspending detail endpoint.

**Input:** `data_pull/output/fpds/navy_fy2025_deduped_classified.json`
(reads but does not modify)

**Process:**
1. Load classified JSON
2. Sort by `fy2025_obligation` descending
3. Take top N (default 250, configurable via `--top N`)
4. For each award, call `get_award_detail(generated_internal_id)`
   - Cached to `data_pull/output/fpds/detail/` (existing cache dir)
   - Skips already-cached awards (resumable)
5. Extract `subaward_count` and `total_subaward_amount` from response
6. Also extract `total_obligation` (lifetime) from response -- needed
   for ratio calculation (the `fy2025_obligation` on the award is
   FY-specific, but the ratio needs lifetime-over-lifetime)
7. Write enriched records to output file

**Output:** `data_pull/output/fpds/navy_fy2025_subaward_enriched.json`

Each record contains all fields from the classified award plus:
- `subaward_count` (int)
- `total_subaward_amount` (float, lifetime)
- `lifetime_obligation` (float, from detail endpoint)
- `sub_ratio` (float, = total_subaward_amount / lifetime_obligation)

**Usage:**
```
python data_pull/enrich_subawards.py --top 250
python data_pull/enrich_subawards.py --top 250 --group cg
python data_pull/enrich_subawards.py --top 100 --dry-run
```

**Performance:** 250 awards at ~0.15s rate limit = ~40 seconds. Most
will already be cached from the test run.

### CG enrichment

Same script, `--group cg` flag reads from
`cg_fy2025_deduped_classified.json` and outputs
`cg_fy2025_subaward_enriched.json`. CG has 4,667 awards; top 250
would cover the vast majority of dollars.

---

## Step 2: Subcontract Data Sheet

### `sheets/subcontract_data.py` (new)

Reads the enriched JSON and builds an Excel table with one row per
enriched award.

**Sheet name:** "Subcontract Data"

**Excel table name:** SubAwards

**Columns:**

| # | Column | Source | Width |
|---|---|---|---|
| 1 | Service | "Navy" or "Coast Guard" tag | 14 |
| 2 | PIID | `piid` | 20 |
| 3 | Vendor | `recipient_name` | 35 |
| 4 | Parent Company | `ultimate_parent_name` | 30 |
| 5 | Hull Program | `hull_program` | 10 |
| 6 | PSC | `psc_code` | 6 |
| 7 | PSC Description | `psc_description` | 30 |
| 8 | GFE | `gfe_gfp` | 5 |
| 9 | Sub Plan | `subcontracting_plan` | 25 |
| 10 | FY2025 Obligation | `fy2025_obligation` | 18 |
| 11 | Lifetime Obligation | `lifetime_obligation` | 18 |
| 12 | Subaward Count | `subaward_count` | 14 |
| 13 | Subaward Amount | `total_subaward_amount` | 18 |
| 14 | Sub Ratio | formula: col13/col11 | 10 |

Sorted by FY2025 Obligation descending. Both Navy and CG awards in one
table, distinguished by the Service column.

**Row count:** ~500 rows (top 250 Navy + top 250 CG). Small enough
that the sheet is readable; large enough to cover 80-90% of total
dollars.

---

## Step 3: Sub Ratios Sheet

### `sheets/sub_ratios.py` (new)

Computes summary ratios from the SubAwards table and presents them
in a format the SAM formulas can reference.

**Sheet name:** "Sub Ratios"

### Section 1: Core SAM Ratios (rows 3-8)

These are the three ratios from the SAM architecture that Product
Procurement and Services reference directly.

| Row | Segment | Filter | Formula |
|---|---|---|---|
| 3 | Vessel GFE=Y (low ratio) | PSC starts with 19, GFE=Y | SUMIFS(SubAwd $) / SUMIFS(Lifetime Oblg) |
| 4 | Vessel GFE=N (standard ratio) | PSC starts with 19, GFE=N | SUMIFS(SubAwd $) / SUMIFS(Lifetime Oblg) |
| 5 | Non-vessel w/ sub plan | PSC not 19xx, sub plan is mandatory | SUMIFS(SubAwd $) / SUMIFS(Lifetime Oblg) |
| 6 | Non-vessel no sub plan | PSC not 19xx, no mandatory plan | SUMIFS(SubAwd $) / SUMIFS(Lifetime Oblg) |
| 7 | Overall weighted average | All enriched awards | SUMIFS(SubAwd $) / SUMIFS(Lifetime Oblg) |

Columns: Segment | Lifetime Obligation | Subaward Amount | Ratio |
Award Count | Awards w/ Subs

### Section 2: Ratios by Hull Program (rows 12+)

| Hull Program | Lifetime Oblg | SubAwd $ | Ratio | # Awards | # w/ Subs |
|---|---|---|---|---|---|
| DDG | | | formula | | |
| SSN | | | formula | | |
| CVN | | | formula | | |
| SSBN | | | formula | | |
| ... | | | | | |

All computed via SUMIFS against the SubAwards table, filtered by
Hull Program.

### Section 3: Ratios by Prime (rows 30+)

| Parent Company | Lifetime Oblg | SubAwd $ | Ratio | # Awards | # w/ Subs |
|---|---|---|---|---|---|
| General Dynamics | | | formula | | |
| Huntington Ingalls | | | formula | | |
| RTX / Raytheon | | | formula | | |
| ... | | | | | |

### Section 4: Ratios by PSC Group (rows 48+)

| PSC Group | Lifetime Oblg | SubAwd $ | Ratio | # Awards | # w/ Subs |
|---|---|---|---|---|---|
| 19xx Vessels | | | formula | | |
| 58xx Electronics | | | formula | | |
| 28xx Engines | | | formula | | |
| 10xx/14xx Weapons/Missiles | | | formula | | |
| J998/J999 Ship Repair | | | formula | | |
| ... | | | | | |

---

## How SAM Formulas Reference This Sheet

On Product Procurement, a SAM version of each cell would look like:

```
For a vessel PSC (19xx), DDG column:
  = TAM_cell * IF(Awards[GFE]="Y",
      'Sub Ratios'!D3,     -- low ratio (vessel GFE=Y)
      'Sub Ratios'!D4)     -- standard ratio (vessel GFE=N)

For a non-vessel PSC (58xx), DDG column:
  = TAM_cell * 'Sub Ratios'!D5   -- non-vessel w/ sub plan ratio
```

Or, for more precision, use the hull-program-specific ratio:
```
  = TAM_cell * INDEX('Sub Ratios'!D12:D27,
      MATCH("DDG", 'Sub Ratios'!A12:A27, 0))
```

The exact formula structure depends on whether we add SAM as a parallel
table, a column next to each hull program column, or a separate SAM
row under each PSC row. To be decided during implementation.

---

## Implementation Sequence

### Phase 1: Data pull + Subcontract Data sheet (~1 hour)

1. Write `data_pull/enrich_subawards.py`
2. Run enrichment for Navy (top 250) and CG (top 250)
3. Write `sheets/subcontract_data.py`
4. Add to `build_from_data.py` sheet order
5. Rebuild workbook, verify data looks right

### Phase 2: Sub Ratios sheet (~1 hour)

1. Write `sheets/sub_ratios.py`
2. Build the four summary sections with SUMIFS against SubAwards table
3. Add to `build_from_data.py`
4. Rebuild, verify ratios match the test run numbers

### Phase 3: SAM formulas on Product Procurement / Services

1. Add SAM column or parallel table to `sheets/product_procurement.py`
2. Reference the Sub Ratios sheet for the multiplier
3. Same for `sheets/services.py`
4. Rebuild, verify SAM numbers

### Phase 4: Competitive Dynamics prime landscape

1. Build View 1 (prime x hull program cross-tab) in
   `sheets/competitive_dynamics.py`
2. Uses existing Awards table, no dependency on subaward data

### Phase 5 (future): Subcontractor landscape

1. Pull individual subaward records for top 50-100 contracts
2. Aggregate by subcontractor
3. Build View 2 on Competitive Dynamics sheet

---

## New Files Summary

| File | Type | Description |
|---|---|---|
| `data_pull/enrich_subawards.py` | Script | Pull subaward summary for top N awards |
| `data_pull/output/fpds/navy_fy2025_subaward_enriched.json` | Data | Enriched Navy awards |
| `data_pull/output/fpds/cg_fy2025_subaward_enriched.json` | Data | Enriched CG awards |
| `sheets/subcontract_data.py` | Sheet builder | Subcontract Data sheet |
| `sheets/sub_ratios.py` | Sheet builder | Sub Ratios sheet |

---

## Tab Colors and Sheet Order

Updated sheet order for `build_from_data.py`:

1. Overview (navy blue #1F314F)
2. Product Procurement (green #2E7D32)
3. Services (green #2E7D32)
4. Sub Ratios (teal #00695C)
5. Competitive Dynamics (dark red #8B0000)
6. Subcontract Data (slate #5B7A99)
7. Awards Data (slate #5B7A99)
8. Vessel Taxonomy (slate #5B7A99)
