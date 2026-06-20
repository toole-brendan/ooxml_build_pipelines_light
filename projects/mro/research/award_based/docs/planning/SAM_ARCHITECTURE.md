# SAM Architecture Plan

How to compute the Serviceable Addressable Market (SAM) on the Product
Procurement and Services sheets using fields already in the classified
awards data.

---

## Definition

SAM = the portion of Navy/CG spending that flows to subcontractors.
This is the addressable market for companies that don't hold prime ship
contracts but supply systems, components, or services to the primes.

---

## Formula

```
SAM = (GFE=Y vessel * low_ratio)
    + (GFE=N vessel * standard_ratio)
    + (non-vessel with sub plan * standard_ratio)
```

### Bucket 1: GFE=Y vessel contracts (19xx PSC, gfe_gfp=Y)

The government already purchased modules separately and furnished them
to the shipyard. The vessel contract dollar value is mostly integration
and assembly -- less work flows to the prime's subs because the module
procurement was pulled out. Apply a **low ratio**.

FY2025 Navy: ~$8.6B

### Bucket 2: GFE=N vessel contracts (19xx PSC, gfe_gfp=N)

The shipyard provides everything -- hull, modules, systems. They
source modules through their own supply chain, so a larger share of
contract value flows to subcontractors. Apply the **standard ratio**.

FY2025 Navy: ~$29.9B

### Bucket 3: Non-vessel contracts with sub plan (non-19xx PSC, subcontracting_plan has mandatory plan)

Electronics, propulsion, weapons, auxiliary systems, and service
contracts where the prime has a mandatory subcontracting plan. These
include the contracts that supply GFE modules to the shipyards --
they're captured here, not in Bucket 1, so there is no double-counting.

Mandatory sub plan values:
- INDIVIDUAL SUBCONTRACT PLAN
- DOD COMPREHENSIVE SUBCONTRACT PLAN
- PLAN REQUIRED - INCENTIVE NOT INCLUDED
- PLAN REQUIRED - INCENTIVE INCLUDED

FY2025 Navy: subset of ~$37.2B in non-vessel spend (filtered to those
with mandatory sub plans)

---

## Ratio Derivation

The subcontracting ratio is derived empirically from USAspending
subaward data, not industry benchmarks.

Method: for each award with subaward reporting, compute
`total_subaward_amount / total_obligation` (both lifetime figures,
so the ratio is apples-to-apples).

### Observed ratios (top 20 Navy contracts, 2026-04-15 test)

| Vendor | Hull | Total Oblg | SubAwd $ | Ratio |
|---|---|---|---|---|
| HUNTINGTON INGALLS | CVN | $11.9B | $9,586M | 81% |
| BOEING | - | $1.6B | $1,080M | 70% |
| RAYTHEON | - | $3.3B | $1,415M | 43% |
| ELECTRIC BOAT | SSBN | $24.5B | $7,749M | 32% |
| ELECTRIC BOAT | SSN | $4.2B | $1,018M | 24% |
| TEXTRON SYSTEMS | LCAC | $1.4B | $247M | 17% |
| ELECTRIC BOAT | SSN | $34.7B | $4,176M | 12% |
| HUNTINGTON INGALLS | DDG | $7.0B | $758M | 11% |
| HUNTINGTON INGALLS | LHA | $3.2B | $333M | 11% |

Weighted average across contracts with subaward data: **22%**

This is a **floor**, not an estimate. Primes with poor subaward
reporting (BIW: 0 reported on $5B DDG contract; Fluor/Bechtel: 0
reported on $16B nuclear propulsion) drag the average down. The true
ratio is higher.

### Ratio refinement approach

To improve the ratio estimate:
1. Enrich the top 200-300 awards by FY2025 obligation with subaward
   summary data via `get_award_detail()` (~2 min of API calls)
2. Compute ratios segmented by prime contractor, hull program, and
   PSC group
3. Use the segmented ratios where coverage is good; fall back to the
   weighted average where it isn't
4. The low_ratio for GFE=Y vessel contracts can be derived by comparing
   GFE=Y vs GFE=N contracts from the same prime on the same hull program

---

## Data Already Available

All fields needed for the SAM formula are already on every award in
the classified JSON. No new data pulls are required for the base
calculation.

| Field | Source | On every award? |
|---|---|---|
| `psc_code` | FPDS | Yes |
| `gfe_gfp` | FPDS | Yes |
| `subcontracting_plan` | FPDS | Yes |
| `hull_program` | Classifier | Yes |
| `fy2025_obligation` | FPDS (aggregated) | Yes |

The only new input is the ratio, which requires enriching a subset of
awards with `subaward_count` and `total_subaward_amount` from the
USAspending detail endpoint.

---

## Implementation on Sheets

### Product Procurement sheet

Currently: 132 PSC rows x hull program columns, each cell is a SUMIFS
on the Awards table.

Add a SAM column (or parallel SAM table) where each cell applies the
formula:
- If PSC is 19xx (vessel): split by GFE, apply low_ratio or standard_ratio
- If PSC is non-19xx and sub plan is mandatory: apply standard_ratio
- If PSC is non-19xx and no sub plan: $0 (not addressable)

### Services sheet

Same structure. 54 service PSC rows x hull programs. Apply
standard_ratio to rows with mandatory sub plans.

---

## What This Does NOT Cover

- **Actual subcontractor names and flows** -- requires pulling individual
  subaward records (137K on HII CVN alone). This is a separate analysis
  that could feed the Competitive Dynamics sheet.
- **FY-specific subaward dollars** -- the ratio uses lifetime figures.
  Individual subaward records have `action_date` for FY filtering but
  that's a much larger data pull.
- **Sub-tier subcontracting** -- USAspending only reports first-tier
  subawards. The true supply chain runs deeper.
