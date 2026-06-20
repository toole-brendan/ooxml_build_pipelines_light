# Competitive Dynamics Sheet Plan

The Product Procurement and Services sheets answer **what** is being
bought. Competitive Dynamics answers **who** is buying and selling.

---

## View 1: Prime Landscape

A cross-tab of prime contractor (rows) x hull program (columns),
each cell = FY2025 obligation.

### Structure

**Navy table:**

| Parent Company | DDG | SSN | SSBN | CVN | LHA | LPD | FFG | ... | Non-vessel | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| General Dynamics | BIW $ | EB $ | EB $ | | | | | | GD subs $ | |
| Huntington Ingalls | HII $ | | | HII $ | HII $ | HII $ | | | HII subs $ | |
| RTX / Raytheon | | | | | | | | | Aegis $ | |
| L3Harris | | | | | | | | | electronics $ | |
| ... | | | | | | | | | | |

**Coast Guard table:** Same structure with CG hull programs (OPC, NSC,
FRC, WMEC, etc.)

### Key design decisions

- **Roll up by parent company.** The `ultimate_parent_name` field from
  FPDS traces corporate ownership (EB, BIW, NASSCO all show under
  General Dynamics). Use parent for row grouping, show subsidiary in
  a detail column.
- **Non-vessel column.** Primes that appear on vessel contracts often
  also hold electronics, propulsion, or service contracts. A non-vessel
  column captures their full footprint.
- **Top N cutoff.** Show the top 15-20 parent companies by total FY2025
  obligation. Roll the rest into "Other."

### Data requirements

All data is already in the classified JSON:
- `recipient_name`, `ultimate_parent_name` (from FPDS)
- `hull_program` (from classifier)
- `fy2025_obligation` (from FPDS aggregation)
- `psc_code` (from FPDS) -- to separate vessel vs non-vessel

Buildable with SUMIFS on the existing Awards table. No new data pulls.

### Implementation

New sheet builder: `sheets/competitive_dynamics.py`

Replace the current placeholder stub. Build two Excel tables (Navy, CG)
using SUMIFS formulas against the Awards table, same pattern as Product
Procurement and Services.

One complexity: parent company rollup. The Awards table has
`recipient_name` but not `ultimate_parent_name`. Options:
1. Add `ultimate_parent_name` as a column on the Awards Data sheet
2. Use a lookup table on the Competitive Dynamics sheet itself
3. Hard-code the top 15-20 parent-to-subsidiary mappings

Option 1 is cleanest -- add the column to `awards_data.py` and use
SUMIFS against it.

---

## View 2: Subcontractor Landscape

The unique insight: who are the actual subcontractors, what do they
supply, and which programs do they serve?

### Structure

**Top subcontractors table:**

| Subcontractor | Total SubAwd $ | Programs Served | Primary System |
|---|---|---|---|
| NORTHROP GRUMMAN | $X | CVN, DDG, LHA | Electronics, Radar |
| ROLLS-ROYCE | $X | DDG, FFG | Propulsion |
| ... | | | |

**Subcontractor concentration:**

| Metric | Value |
|---|---|
| Top 5 subs share of reported sub $ | X% |
| Top 10 subs share | X% |
| Top 20 subs share | X% |
| Total unique subcontractors | N |

**By hull program:** For each major hull program, top 5 subcontractors
and their share.

### Data requirements

Requires pulling individual subaward records via `get_subawards()`
for the top 50-100 contracts by FY2025 obligation. The HII CVN
contract alone has 137K subaward records. Coverage varies by prime:

| Prime | Reporting quality | Expected yield |
|---|---|---|
| HII | Excellent | Full supply chain visibility |
| Electric Boat | Moderate | Partial |
| BIW | Poor | Minimal |
| Raytheon | Variable | Program-dependent |

### Implementation

This is Phase 2 -- depends on the subaward record pull described in
the Subcontract Data plan. Build after the ratio sheet is working
and subaward records have been pulled and assessed for quality.

The sheet builder would read from a subaward aggregation JSON (not
the raw 137K records, but a pre-aggregated summary by subcontractor).

---

## Sheet Layout

```
Competitive Dynamics
  Row 1:    Sheet title
  Row 3:    "Prime Contractor Landscape - U.S. Navy"
  Row 4:    Column headers (Parent Company | DDG | SSN | ...)
  Rows 5+:  Top 15-20 parent companies + Other + Total
  
  Gap
  
  Row N:    "Prime Contractor Landscape - U.S. Coast Guard"
  ...same structure...
  
  Gap (Phase 2)
  
  Row M:    "Subcontractor Landscape"
  ...top subs table, concentration metrics, by-program breakdowns...
```

Tab color: dark red (#8B0000) -- already assigned in build_from_data.py.
