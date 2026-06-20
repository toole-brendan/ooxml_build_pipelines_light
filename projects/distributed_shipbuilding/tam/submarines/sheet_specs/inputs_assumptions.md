Assumptions
Tab color: B8860B (ochre)  ·  group: Inputs & levers
Module: inputs_assumptions.py

Purpose
The single edit surface: run settings, stream controls, scenario selection, and
bucket adjustments the model reads. Also the PRODUCER of the modeled bucket shares
(modeled = observed + adjustment), consumed by SAM Build's allocation and QA.

Source
extracted/scn_p10_ap_long.csv - the P-10 "TOTAL: Advance Procurement" lines, latest
pb_year per (li, fy), loaded for the §3a gross-AP reference rows (LI 2013 / 1045, FY22-27).

Reads
- Entity Master  observed bucket share per bucket + unbucketed [observed_bucket_share_cell]
- SAM Build      selected-scenario readout for the §4 selector display [selected_sam_cell,
                 selected_sam_pct_cell, selected_avg_annual_sam_cell] - via a RENDER-time lazy
                 import that breaks the assumptions <-> sam_build cycle

Feeds
- AP Bridge, SAM Build, TAM Build, z_ChartData, Figure Register, Executive Summary,
  QA Reconciliation, Sensitivity
- Producer cells / accessors: fy_range start/end + n_years count formula, selected SAM scenario,
  BC + AP/LLTM include toggles, AP/LLTM additive base (per class/FY, confirmed 0), P-10 gross AP
  reference (per class/FY), scenario keys/names, scenario flag cell + range, bucket adjustment /
  observed / modeled share cells, bucket-share range, unbucketed + total modeled share
- Data-validation dropdowns on the editable Value cells: Default SAM scenario (scenario name list),
  Include BC / Include AP/LLTM (0,1)

On the sheet
§1  Run settings
    - Program (Submarine = Va LI 2013 + Col LI 1045), FY range start = 2022 [fy_start], FY range
      end = 2027 [fy_end], Units (Nominal $M), Default SAM scenario = "Broad component mfg"
      [default_scen, drives SAM Build §7 via INDEX/MATCH]. n_years_count_formula = fy_end - fy_start + 1.

§2  Stream controls
    - Include BC stream = 1 [incl_bc], Include AP/LLTM stream = 1 [incl_ap], Prior-year AP credit
      treatment = none (credits = 0). The include cells are read by TAM Build §2a toggles.

§3  AP/LLTM additive base ($M, confirmed 0)
    - Per class (Va LI 2013 / Col LI 1045) x FY22-27 input rows, all held at 0 [ap_base; ap_lltm_base_cell].
      Total (Va + Col) = N(Va) + N(Col) per FY. (Held at 0: supplier LLTM is already inside P-5c BC, so
      adding the P-10 gross would double-count.)
    §3a P-10 gross AP reference ($M, overlaps BC): per class x FY, loaded from scn_p10_ap_long.csv
        (latest pb_year per (li, fy)) [ap_gross; ap_gross_cell]. Reference only - overlaps BC, not additive.

§4  Scenario selector
    - Selected scenario = Default SAM scenario (C of default_scen); Cumulative SAM / % of TAM / Avg annual
      SAM each link back to SAM Build (selected_sam_cell / _pct_cell / _avg_annual_cell). This data row is
      deferred to render time and spliced in via the lazy SAM Build import.

§5  Target scenario matrix (1 = targets bucket)
    - Rows = buckets, columns = scenarios (Metal / HM&E / Electrical / Modular / Broad); each flag =
      1 if bucket in that scenario's membership set else 0 [matrix_first; scenario_flag_cell / _range].
      Membership: metal = {structural, castings, machining}; hme = {piping, hvac, machining};
      electrical = {electrical}; modular = {structural, coatings}; broad = all bucket keys.

§6  Bucket share adjustments (modeled = observed + adjustment)  [PRODUCER of modeled shares]
    - Per bucket: Observed share = observed_bucket_share_cell(b) <- Entity Master; Adjustment = 0 (input);
      Modeled share = C + D (observed + adjustment) [adj; bucket_adjustment_cell / observed_share_cell /
      modeled_share_cell]. Unbucketed modeled = 1 - SUM(bucket modeled shares) [adj_unb]. Total modeled
      share = SUM(buckets + unbucketed) [adj_total], ties to 1.

Notes
- Native cell notes: 2 -
    §1 (C): default SAM scenario drives the Selected-scenario readout on SAM Build via INDEX/MATCH
    §2 (C): the AP/LLTM stream toggle is ON, but the additive base is held at $0 (LLTM already in P-5c BC)
- Note column: none.
