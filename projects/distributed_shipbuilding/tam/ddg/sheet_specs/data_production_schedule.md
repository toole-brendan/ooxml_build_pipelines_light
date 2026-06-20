Production Schedule
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_production_schedule.py

Purpose
DDG-51 hull schedule and in-window hull count; supplies the per-hull
denominators used in TAM Build.

Source
extracted/scn_li_production_schedule.csv  - one row per hull (Ship, Shipbuilder, FY,
   Contract Award, Start Construction, Delivery Date). Hull counts are computed in
   Python (base-free, no cell links).

Reads
- none (standalone hull-schedule extract; no sibling-sheet links)

Feeds
- TAM Build (per-hull TAM denominators)
- Native table: tbl_ddg_production
- Promoted accessors: hull_count (all FY), in_window_hull_count (award FY in 2022-2027)

On the sheet
§1  Hull schedule (hull -> yard -> FY)
    - Native table tbl_ddg_production: Ship, Shipbuilder, FY, Contract award, Start
      construction, Delivery (one row per CSV hull, all input values).

§2  Hull count by yard
    - Python-tallied count of hulls per Shipbuilder ("(unspecified)" when blank), sorted
      by count descending (static counts, not formulas).

§3  Model window
    - Hulls in schedule (all FY) = hull_count() = len(schedule); note cites
      scn_li_production_schedule.csv.
    - In-window hulls (award FY22-27) = in_window_hull_count() = count of hulls whose FY
      is a digit and falls in 2022..2027; consumed by TAM Build per-hull views.

Notes
- Native cell notes: none.
- Note column: none.
