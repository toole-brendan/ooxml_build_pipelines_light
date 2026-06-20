SCN Budget
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_scn_budget.py

Purpose
The P-5c per-FY cost-category breakdown (Virginia + Columbia) with derived BC/GFE ratios
and a portfolio rollup; gives TAM Build a clean Basic-Construction budget base. Leaf
module (loads its CSV, no cross-sheet dependency).

Source
extracted/cost_funnel_with_subawards (via load_extracted_csv) - per (LI, FY) P-5c cost
categories: total_ship_estimate, plan_costs, propulsion, electronics, hme, ordnance,
other_cost, gfe_sum, change_orders, basic_construction ($M). LI 2013 = Virginia,
LI 1045 = Columbia; FY22-27.

Reads
- none (leaf module; loads its own P-5c CSV, depends on no other sheet)

Feeds
- TAM Build (Budget Normalized section - the BC base), z_ChartData
- Producer accessor: scn_cell(li, fy, metric) -> 'SCN Budget'!<FY col><row> for any of
  the §2/§3 metric rows (total, plans, propulsion, electronics, hme, ordnance,
  other_cost, gfe_sum, change_orders, basic, and the derived bc_pct / gfe_pct). Built at
  import so the row positions track the cursor that writes the cells.

On the sheet
§1  At a glance: Basic Construction & GFE by FY ($M)
    - Same-sheet rollup (black, not green links) of the §2/§3 detail: Virginia /
      Columbia / Portfolio Basic Construction and GFE sum per FY, with a Total column.
        per-ship row  = scn_cell(li, fy, metric)
        portfolio row = N(scn_cell(2013, fy, m)) + N(scn_cell(1045, fy, m))
        Total         = SUM(FY22:FY27 of that row)

§2  Virginia (LI 2013) SCN P-5c per FY ($M)
    - Total Ship Estimate, Plans Costs (input rows from the CSV per FY), then:
    §2a GFE components - Propulsion Equipment, Electronics, HM&E, Ordnance, Other Cost,
        GFE Sum (input rows).
    §2b Construction - Change Orders, Basic Construction (input rows).
    §2c Derived ratios:
        BC % of Total  = IF(Total = 0, "", Basic Construction / Total)  per FY
        GFE % of Total = IF(Total = 0, "", GFE Sum / Total)  per FY

§3  Columbia (LI 1045) SCN P-5c per FY ($M)
    - Same structure as §2 (§3a GFE components, §3b Construction, §3c Derived ratios)
      for LI 1045.

§4  Portfolio rollup (Virginia + Columbia, $M by FY)
    - Total Ship Estimate / GFE Sum / Basic Construction per FY = N(scn_cell(2013,...))
      + N(scn_cell(1045,...)), Total column = SUM across FY. Then:
        BC % of Total  = IF(Total = 0, "", Basic Construction / Total)  per FY + Total col
        GFE % of Total = IF(Total = 0, "", GFE Sum / Total)  per FY + Total col

§5  Sources
    - Source family / Source Index ID / Refresh: SCN P-5c (Basic Construction),
      Source Index §2, FY22-27 PB.

Notes
- Native cell notes: none.
- Note column: none.
