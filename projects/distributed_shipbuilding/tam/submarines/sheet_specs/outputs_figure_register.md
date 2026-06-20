Figure Register
Tab color: 2E7D4F (green)  ·  group: Outputs
Module: outputs_figure_register.py

Purpose
The deck-facing figure contract (formerly Deck_Outputs): one live cross-sheet link
per registered figure (DO-*), never a hardcoded value. Mechanical, not reader-facing
(the Executive Summary is the human answer page). Exposes value_cell / source_ref /
is_pct / REGISTRY (consumed by Number Audit) and publishes the workbook defined names.
DO-01 and portfolio_tam source from TAM Build cumulative TAM, not a TAM value carried
on the SAM tab.

Reads
- TAM Build           cumulative_tam_cell (DO-01), avg_annual_tam_cell (DO-09),
                      bc/ap_lltm/total-weighted supplier-coeff cells (DO-02/03/04),
                      tam_total_cell(fy) (DO-31..36), cumulative_bc_base_cell (DO-51),
                      removal_cell (DO-52), n_years_cell, FY_COLUMNS
- SAM Build           bucket_tam_cell(k) (DO-11..17), unbucketed_tam_cell (DO-18),
                      sam_cell(k) (DO-20..), avg_annual_sam_cell(k) (DO-10, DO-25..),
                      scenario_keys_ordered
- Entity Master       addressable_total_cell (DO-07)
- POP Source Audit    gated_dollar_cell (DO-05), gfe_excluded_dollar_cell (DO-06)
- AP Bridge             ap_bridge gross / gfe-removed / in-bc-removed / residual / base
                      cells (DO-53..57)
- Assumptions  scenario_name(k)
- SIB Excluded        sib_total_cell (DO-08)

Feeds
- Number Audit (§2 figure tie-out, via REGISTRY + value_cell / source_ref / is_pct)
- Native table: tbl_sub_figure_register
- Defined names (workbook-scoped, absolute targets): portfolio_tam_annual,
  portfolio_tam_cumulative, portfolio_tam, broad_sam_annual, broad_sam_cumulative,
  sam_broad, fiscal_year_count, bc_supplier_coeff, ap_lltm_supplier_coeff
- Accessors: value_cell(fid) -> 'Figure Register'!E<row>; source_ref(fid); is_pct(fid)
  (true for DO-02/03/04). Header row 15, first data row 16.

On the sheet
§1  At a glance: registered figure contract
    - Registered figures = len(REGISTRY); TAM figures / SAM figures = count of rows whose
      label contains "TAM" / "SAM"; defined names = 9. assert_all_links() fail-fast: every
      registry ref must contain "!".

§2  Figure registry (one live link per row, never hardcoded)
    - tbl_sub_figure_register: per figure (Figure ID, Slide, Label, Value, Unit, Source
      cell, Producer tab). Value = "=<source ref>" (green %-link for DO-02/03/04, else
      green $-link). Slides map to the 18-slide deck (4 Exec, 7 BC, 8 TAM bridge, 9 annual,
      10 coefficients, 11 AP/LLTM, 13 bucket, 14 SAM, 15 suppliers, 16 SIB). Registry rows:
        - DO-01 headline cumulative TAM      <- TAM Build cumulative_tam_cell
        - DO-09 avg annual TAM               <- TAM Build avg_annual_tam_cell
        - DO-10 avg annual broad SAM         <- SAM Build avg_annual_sam_cell("broad")
        - DO-02 BC supplier coeff (%)        <- TAM Build bc_supplier_coeff_cell
        - DO-03 AP/LLTM ref coeff (%)        <- TAM Build ap_lltm_supplier_coeff_cell
        - DO-04 total weighted coeff (%)     <- TAM Build total_weighted_coeff_cell
        - DO-05 gated POP corpus $M          <- POP Source Audit gated_dollar_cell
        - DO-06 GFE / excluded-scope $M      <- POP Source Audit gfe_excluded_dollar_cell
        - DO-07 supplier-addressable subaward $M <- Entity Master addressable_total_cell
        - DO-08 SIB exclusion $M             <- SIB Excluded sib_total_cell
        - DO-11..17 bucket TAM $M (per key)  <- SAM Build bucket_tam_cell(k)
        - DO-18 unbucketed residual TAM $M   <- SAM Build unbucketed_tam_cell
        - DO-20.. SAM $M (per scenario)      <- SAM Build sam_cell(sk)
        - DO-25.. avg annual SAM (per scen)  <- SAM Build avg_annual_sam_cell(sk)
        - DO-31..36 FY portfolio TAM $M      <- TAM Build tam_total_cell(fy)
        - DO-51 BC construction base $M      <- TAM Build cumulative_bc_base_cell
        - DO-52 POP removal $M               <- TAM Build removal_cell
        - DO-53..57 AP bridge stages $M      <- AP Bridge ap_bridge_* cells (gross -> base=0)

§3  Defined names (workbook-scoped)
    - name -> target cell -> meaning. Annual values are the primary headline; cumulative
      kept as supporting; legacy portfolio_tam / sam_broad stay as cumulative aliases:
        - portfolio_tam_annual     <- avg_annual_tam_cell        (headline avg annual TAM)
        - portfolio_tam_cumulative <- cumulative_tam_cell        (FY22-27 cumulative TAM)
        - portfolio_tam            <- cumulative_tam_cell        (alias of cumulative)
        - broad_sam_annual         <- avg_annual_sam_cell("broad")
        - broad_sam_cumulative     <- sam_cell("broad")
        - sam_broad                <- sam_cell("broad")          (alias of cumulative)
        - fiscal_year_count        <- n_years_cell
        - bc_supplier_coeff        <- bc_supplier_coeff_cell
        - ap_lltm_supplier_coeff   <- ap_lltm_supplier_coeff_cell
      Targets are absolutized ($A$1 form) when registered as defined names.

§4  Register coverage
    - Figure-count rollup by category: Headline TAM (DO-01/09), Supplier coefficients
      (DO-02/03/04), POP corpus (DO-05), Exclusions (DO-06/08), Supplier-addressable base
      (DO-07), Bucket TAM (DO-1*), SAM scenarios (DO-2*), Annual TAM (DO-3*), BC base / POP
      removal / AP bridge (DO-51..57).

Notes
- Native cell notes: none.
- Note column: none.
