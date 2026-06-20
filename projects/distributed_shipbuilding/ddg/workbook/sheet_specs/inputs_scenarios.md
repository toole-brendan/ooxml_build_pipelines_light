Scenarios
Tab color: B8860B (ochre)  ·  group: Inputs & levers
Module: inputs_scenarios.py

Purpose
Defines the SAM scenario menu: which work-type buckets each scenario targets.
The former Scenarios section of the composite Assumptions tab, now its own tab. The
matrix is a native Excel table (flat, editable, 0/1 data validation on the flags)
that drives SAM Build's scenario calculation.

Reads
- Assumptions   selected SAM scenario key (read-out only)  [selected_scenario_cell]

Feeds
- SAM Build, Figure Register, Executive Summary, z_ChartData
- Promoted accessors:
  - scenario_keys()        ordered scenario keys (metal, hme, electrical, modular, broad)
  - scenario_name(k)       display name per scenario
  - scenario_flag_range(k) the 0/1 flag column for scenario k (a SUMPRODUCT mask)
- Native table: tbl_ddg_scenarios (the §1 bucket x scenario matrix)

On the sheet
§1  Scenario matrix (1 = scenario targets this bucket)
    - Native Excel table tbl_ddg_scenarios: one row per work-type bucket, one column
      per scenario; flag = 1 if the bucket is in that scenario's set, else 0
      (metal = structural+castings+machining; hme = piping+hvac+machining;
      electrical = electrical only; modular = structural+coatings; broad = all 7).
      0/1 whole-number validation on the flag block. SAM Build SUMPRODUCTs each column
      against bucket TAM to get scenario SAM.

§2  Scenario definitions
    - Prose definition per scenario (e.g. metal = "structural fab, castings/forgings,
      and machined components"; broad = "all seven work-type buckets") - the reader-
      facing gloss of each flag column.

§3  Selected scenario
    - Selected SAM scenario = green link <- Assumptions selected_scenario_cell (edit on the
      Assumptions tab; SAM Build is the calculator).

§4  Bucket count by scenario
    - # buckets per scenario = SUM of that scenario's §1 flag column (a sanity read-out
      of how wide each scenario's target menu is).

Notes
- Native cell notes: none.
- Note column: none.
