Figure Register
Tab color: 2E7D4F (green)  ·  group: Outputs
Module: outputs_figure_register.py

Purpose
The deck-facing figure contract: one cross-sheet link per slide figure, so deck
values never hardcode and always trace to a producer cell. A native no-format
table; stays separate from Executive Summary (the human-readable answer page). It
also declares the workbook defined names, repointed to PRODUCER cells so the
headline portfolio_tam (and DO-01) source from TAM Build, not the SAM layer.

Reads
- TAM Build      portfolio / BC- / AP-stream TAM, avg-annual TAM, n years, per-hull
                 TAM, BC base, POP removal, BC & AP/LLTM coeffs, outside-yards
                 corrected/disclosed, TAM-by-FY  [avg_annual_tam_cell, portfolio_tam_cell,
                 tam_cell, ...]
- SAM Build      addressable total, bucket TAM (per work-type), unbucketed residual,
                 SAM & SAM-avg-annual per scenario, scenario_keys_ordered  [sam_cell,
                 bucket_tam_cell, ...]
- POP Source Audit      gated $, GFE-excluded $, MYP-masters $  [gated_dollar_cell,
                 gfe_excluded_dollar_cell, masters_dollar_cell]
- SCN Budget     FY24 total / basic / GFE ship-estimate cells  [scn_cell]
- Scenarios      display names for SAM scenarios  [scenario_name]
- taxonomy       BUCKETS / BUCKET_KEYS (work-type buckets for slide 11)

Feeds
- Number Audit (every DO row is tied back to its source cell there)
- Defined names: portfolio_tam (DO-01 headline; TAM Build producer, not SAM),
  portfolio_tam_annual, portfolio_tam_cumulative, broad_sam_annual,
  broad_sam_cumulative, fiscal_year_count, portfolio_bc_tam, portfolio_ap_tam,
  bc_supplier_coeff, sam_broad  (all absolutized to producer cells)
- Producer accessors: REGISTRY, value_cell, source_ref, is_pct
- Native table: tbl_ddg_deck_figures

On the sheet
§1  Deck figures (one cross-sheet link per slide figure)
    - Native table, columns: Figure ID, Slide, Label, Value, Source cell.
    - Each row is value = ref where ref is a producer cell on another tab; the
      Source-cell column repeats ref as plain text for audit. DO ids assigned
      sequentially (DO-01..DO-NN) in registry order. Build guard: every figure
      must carry a cross-sheet link (ref contains "!"), else ValueError.
    - DO rows by slide:
      slide 3 (exec headline)  avg-annual portfolio TAM <- TAM Build; avg-annual
        broad SAM <- SAM Build; cumulative portfolio TAM <- TAM Build; cumulative
        broad SAM <- SAM Build; BC- and AP/LLTM-stream TAM <- TAM Build; n years.
      slide 5 (cost funnel)    FY24 total / Basic-Construction / GFE ship estimate,
        all <- SCN Budget scn_cell(2122, 2024, ...).
      slide 6 (MYP trapdoor)   outside-yards corrected (%) and disclosed-artifact
        (%, DO NOT HEADLINE) <- TAM Build; MYP masters $ and gated POP $ <- POP
        Audit; GFE / Navy-directed $ dropped <- POP Source Audit.
      slide 7                  supplier-addressable subaward $ <- SAM Build.
      slide 8 (bridge)         BC construction base and POP removal <- TAM Build;
        BC coeff (%) and AP/LLTM coeff (%) <- TAM Build; supplier-TAM-per-hull and
        BC-TAM-per-hull <- TAM Build.
      slide 9                  TAM FY22..FY27 (one row per FY) <- TAM Build tam_cell.
      slide 11                 bucket TAM per work-type (loop over BUCKET_KEYS) +
        unbucketed residual <- SAM Build.
      slide 12 (SAM menu)      per-scenario SAM (cumulative) and SAM avg-annual,
        looped over scenario_keys_ordered, names <- Scenarios.
    - is_pct flags the % figures (coeffs, outside-yards) for the % link style.

Notes
- Native cell notes: none.
- Note column: none.
