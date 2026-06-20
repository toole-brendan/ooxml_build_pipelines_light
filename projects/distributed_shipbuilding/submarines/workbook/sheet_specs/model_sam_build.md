SAM Build
Tab color: 34406B (indigo)  ·  group: Model (TAM/SAM)
Module: model_sam_build.py

Purpose
Allocates each class's annual TAM into work-type buckets at per-class per-FY share
vectors (the gated Worktype by FY evidence + the shared Assumptions adjustment),
sums the classes to the combined bucket TAM, and computes scenario SAM as
SUMPRODUCT(combined bucket TAM, scenario flags); no capture/win-probability
haircut. FY2026-27 ride the FY22-25 window vector (no usable subaward reporting).
The editable controls (scenario matrix, bucket-share adjustments) live on
Assumptions & Controls.

Reads
- Worktype by FY          per-class per-FY observed shares + window shares + modular
                          tag  [wt_share_cell, wt_window_share_cell, wt_modular_share_cell]
- Entity Master           role $ (prime / co-prime / GFE-SIB / service), grand total
                          [role_dollar_cell, grand_total_cell]
- Assumptions             scenario flag cells/ranges, bucket adjustments, scenario
                          names/keys, selected SAM scenario  [whole-module import `_ac`]
- TAM Build               per-class per-FY TAM [tam_cell], portfolio per-FY TAM
                          [tam_total_cell], n_years [n_years_cell]

Feeds
- Assumptions (the §4 selector display reads selected_sam / _pct / _avg back via a
  function-local lazy import - breaks the import cycle), z_ChartData, Figure Register, Slide Data,
  Executive Summary, QA Reconciliation
- Producer cells: portfolio_tam, per-bucket TAM + range (combined), per-class bucket TAM
  [class_bucket_tam_cell / class_unbucketed_tam_cell / class_tam_total_cell], unbucketed TAM,
  bucketed total, va_/col_modeled_share_total, per-scenario cumulative SAM / % of TAM /
  avg-annual SAM, selected-scenario cells, annual SAM by FY (+ annual broad),
  scenario_keys_ordered, first/last scenario row

On the sheet
§1  At a glance: SAM scenario menu
    - Same-sheet summary: broad SAM avg annual (= cumulative / n_years), broad SAM cumulative,
      broad SAM as % of TAM (subset of TAM, no haircut), selected SAM scenario <- Assumptions &
      Controls, selected SAM (avg annual).

§2  Scenario matrix (linked from Assumptions)
    - One row per bucket, one column per scenario (Metal / HM&E / Electrical / Modular / Broad);
      each cell = scenario_flag_cell(k, bucket)  <- Assumptions (1 = bucket in scenario).

§3  Modeled bucket shares by FY (gated evidence + Inputs adjustment)
    §3a Virginia / §3b Columbia: per bucket, Adj = bucket_adjustment_cell(b) <- Assumptions
        (one knob, both classes), then per FY column FY22..FY25 + FY26-27 (window):
        modeled = N(Worktype by FY observed share) + Adj. Unbucketed = 1 - SUM(bucket
        column); Total modeled share row per column ties to 1
        [va_/col_modeled_share_total_cell point at the window column].
    §3c Excluded roles (full corpus - not supplier-addressable): each = role_dollar_cell(rk)
        <- Entity Master; grand total = grand_total_cell (all recipients).

§4  TAM bucket allocation (annual class TAM x per-FY modeled share)  [PRODUCER]
    - Portfolio TAM (Va + Col, both streams, FY22-27) = sum of TAM Build tam_total_cell over FY22-27
      [defined name portfolio_tam].
    §4a Virginia / §4b Columbia bucket TAM: bucket TAM = sum over FY of
        N(tam_cell(li, fy)) x that FY's modeled share (FY26-27 at the window vector);
        class total = SUM (= the class's cumulative TAM since shares sum to 1).
    §4c Combined bucket TAM = Virginia + Columbia per bucket + unbucketed; Effective
        share = bucket TAM / portfolio TAM; Total (7 buckets + unbucketed) = SUM, ties
        to TAM. Promotes bucket_tam_cell/range, unbucketed_tam_cell, bucketed_total_cell.

§5  Scenario SAM = SUMPRODUCT(combined bucket TAM, scenario flags)  [PRODUCER]
    - Per scenario k (col layout C=avg annual, D=cumulative, E=% of TAM):
        - Cumulative SAM (D)  = SUMPRODUCT(combined bucket-TAM range, scenario_flag_range(k));
          modular = class TAM x class modular share, summed over classes (entity-tag-driven)
        - Avg annual (C)      = D / n_years  <- TAM Build n_years_cell
        - % of TAM (E)        = D / portfolio_TAM
      Promotes sam_cell (D), sam_pct_cell (E), avg_annual_sam_cell (C), first/last scenario row.

§6  Selected scenario (driven by Default SAM scenario)  [PRODUCER]
    - Selected = selected_sam_scenario_cell <- Assumptions; the avg-annual / cumulative /
      %-of-TAM readouts each = INDEX(§5 column, MATCH(selected, §5 name column, 0)).
      Promotes selected_sam_cell / _pct_cell / _avg_annual_cell (read back by Assumptions §4).

§7  Annual SAM by fiscal year (per-class annual TAM x that FY's vectors)  [PRODUCER]
    - Per FY: Annual TAM = tam_total_cell(fy) <- TAM Build; per scenario column = sum over
      classes of N(tam_cell(li, fy)) x SUMPRODUCT(that FY's class share column,
      scenario_flag_range(k)); modular per class via the gated modular shares.
      Lumpy per-FY cadence. Promotes annual_sam_cell, annual_broad_sam_cell, annual_sam_fy_columns.

§8  SAM checks
    - Va / Col modeled shares sum to 100% (all FY columns)  = IF(AND(per-column ABS<0.001),"OK","FAIL")
    - Bucketed TAM = portfolio TAM  = IF(ABS(bucketed_total - portfolio_tam) < 0.5,"OK","FAIL")
    - Broad SAM = TAM - unbucketed  = IF(ABS(broad_cum - (portfolio - unbucketed)) < 0.5,"OK","FAIL")
    - Broad SAM <= TAM  = IF(broad_cum <= portfolio + 0.5,"OK","FAIL")
    - Annual broad SAM sums to cumulative  = IF(ABS(sum §7 broad column - broad_cum) < 0.5,"OK","FAIL")

Notes
- Native cell notes: none.
- Note column: none.
