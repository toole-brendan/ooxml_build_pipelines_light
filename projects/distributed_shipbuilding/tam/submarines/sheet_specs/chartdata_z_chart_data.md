z_ChartData
Tab color: 404040 (charcoal)  ·  group: Chart data
Module: chartdata_z_chart_data.py

Purpose
One think-cell paste block per native chart that renders in the deck, laid out the way
think-cell's embedded datasheet wants it: category / step labels ACROSS the top row,
values in the row(s) beneath (a small matrix when a chart has more than one series).
Each block is styled as a copy-paste-ready range - pale-yellow fill + thin black
perimeter (the S_PASTE_* styles) - so it can be pasted straight into a think-cell chart.
Values are live = links to producer cells; blocks are clean rectangles (no annotation
columns). The z_ prefix sorts the tab last. Deck-loader leaf: nothing in the workbook
imports it; this tab is a paste source / human-readable mirror, not a live feed.

think-cell waterfall convention: every data cell is a STEP, so a computed subtotal /
total is the literal text marker "e" (think-cell draws a calculated bar from the prior
steps; writing the numeric subtotal would double-count). $B blocks divide the model's $M
producers by 1000, and avg-annual blocks divide a cumulative producer by the fiscal-year
count, to match the deck chart's displayed magnitude.

Reads
- TAM Build      tam_total(fy), n years, bc / ap_lltm / primary supplier-coeff
- SAM Build      bucket_tam(b), avg_annual_sam(k), annual_broad_sam(fy)
- SCN Budget     scn_cell(li, fy, "basic") - Virginia (2013) + Columbia (1045) BC by FY
- AP Bridge      gross / gfe-removed / in-bc-removed / residual (removal cells are signed
                 negative on the tab, so they link straight through)
- Entity Master  ent_row_cell(i, vendor|dollar), top_supplier_indices(10)
- SIB Excluded   sib_entity_dollar_cell(0..2)  (BlueForge / TMG / IALR)

Feeds
- none (deck-loader leaf; nothing in the workbook imports it). Producer: CHART_DATA
  (SheetEntry). No native table.

Core dependency
The pale-yellow paste-range styles (S_PASTE_HEADER_*, S_PASTE_LABEL_*, S_PASTE_VAL_*_M/_B/_P)
live in workbook_core/styles.py (ported from the Sea Range Telemetry pipeline). Unit
suffix: _M = "$"#,##0"M", _B = "$"0.0"B", _P = 0.0%.

On the sheet
Sheet-title banner, then one collapsible section banner per rendered chart ("§N - name
(type)"), each followed by its paste rectangle (header row + value row(s)). Nine blocks,
slide order:
    §1 Basic Construction      stacked column, 3x7 - Virginia + Columbia BC by FY22-27 ($B)
        <- SCN Budget (scn / 1000).
    §2 Annual cadence          clustered column, 3x7 - annual TAM vs broad SAM by FY22-27
        ($B)  <- TAM Build / SAM Build.
    §3 Coefficient evidence    ranked column, 2x4 - POP anchor / AP-LLTM ref / Applied BC (%)
        <- TAM Build.
    §4 AP and LLTM bridge       waterfall, 2x6   - Gross AP -> -GFE/design/weapons -> -inside
        BC -> -overlap -> additive base("e", $0), $B  <- AP Bridge (cells / 1000).
    §5 Work-type (bucket) TAM  ranked column, 2x8 - seven work-type buckets, average annual $M
        <- SAM Build (bucket_tam / n_years).
    §6 SAM scenarios           ranked column, 2x6 - five scenario cuts, average annual SAM $M
        <- SAM Build.
    §7 Visible suppliers       bar, 10x2        - top-10 visible suppliers, names down the left
        column, visible subaward $M across  <- Entity Master.
    §8 SIB exclusion           waterfall, 2x5   - BlueForge + TMG + IALR build to total
        excluded("e"), $M  <- SIB Excluded.
    §9 Coefficient sensitivity ranked column, 2x4 - appendix coefficient ladder, same three
        coefficients as §3 (%)  <- TAM Build.

Notes
- Native cell notes: none. Note column: none. No block for cover / dividers / market_primer
  / sizing_boundary / executive_summary / demand_backdrop / methodology / tam_bridge /
  work_type_taxonomy / data_limits / implications / other appendix slides - those are shape /
  text exhibits, not native charts.
- sib_exclusion is now a waterfall (was a ranked bar / table), per the chart-conversion plan.
- Mirror, not a live feed: regenerate the affected block whenever the deck's rendered chart
  set changes. Block layouts follow the chart-conversion target types (docs/chart_conversion_spec.md).
