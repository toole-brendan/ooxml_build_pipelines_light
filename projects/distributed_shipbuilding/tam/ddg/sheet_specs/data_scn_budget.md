SCN Budget
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_scn_budget.py

Purpose
DDG-51 (LI 2122) P-5c cost categories by fiscal year; the source of the Basic
Construction base used by TAM Build.

Source
extracted/cost_funnel_summary.csv  (via load_extracted_csv("cost_funnel_summary")) -
   P-5c cost-funnel rows filtered to LI 2122 and FY 2022-2027. Mapped metrics: total
   ship estimate, plans, electronics, ordnance, HM&E, other cost, GFE sum, change orders,
   basic construction ($M each).

Reads
- none (standalone SCN P-5c extract; no sibling-sheet links)

Feeds
- TAM Build (the BC stream base), Figure Register, z_ChartData
- Promoted accessor: scn_cell(li, fy, metric) - returns the cell for a given LI 2122 /
  FY 2022-2027 / metric (total, plans, electronics, ordnance, hme, other_cost, gfe,
  change_orders, basic, bc_pct, gfe_pct); raises on out-of-range li / fy / metric

On the sheet
§1  Cost categories (DDG-51 LI 2122, $M per FY)
    - Header: Metric + FY 2022..2027.
    - One input row per metric (CSV values): Total Ship Estimate, Plans Costs,
      Electronics, Ordnance, HM&E (missing pre-FY24), Other Cost, GFE Sum
      (Electronics + Ordnance), Change Orders, Basic Construction (BC base -> TAM Build).

§2  Derived ratios
    - BC % of Total  per FY = IF(Total = 0, "", Basic / Total)
    - GFE % of Total per FY = IF(Total = 0, "", GFE Sum / Total)
      (each = the §1 metric row over the §1 Total Ship Estimate row, guarded against /0).

Notes
- Native cell notes: none.
- Note column: none.
