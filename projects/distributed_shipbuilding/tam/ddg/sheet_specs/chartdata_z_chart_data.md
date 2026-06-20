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
imports it, and each native deck chart embeds its own data, so this tab is a paste
source / human-readable mirror, not a live feed.

think-cell waterfall convention: every data cell is a STEP, so a computed subtotal /
total is the literal text marker "e" (think-cell draws a calculated bar from the prior
steps; writing the numeric subtotal would double-count). Avg-annual blocks divide a
cumulative producer by the fiscal-year count to match the deck chart's displayed value.

Source
extracted/cost_funnel_summary.csv (LI 2122 FFATA-gap bands, summed for §9) - the one
exhibit with no model producer, written as numeric inputs rather than links.

Reads
- TAM Build      BC base, POP removal, AP-stream TAM, n years, BC/AP per-FY totals,
                 BIW / Ingalls / other-US / foreign / unparsed POP shares, outside-yards
                 corrected / disclosed
- SAM Build      bucket TAM per key, unbucketed residual, SAM avg-annual per scenario
- SCN Budget     FY24 total / gfe / basic cost cells  [scn_cell]
- Entity Master  top-10 supplier rows (vendor / dollar)  [ent_row_cell, top_supplier_indices]

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
    §1 Cost funnel              waterfall, 2x5   - Total ship -> -GFE -> -other -> Basic
        Construction("e")  <- SCN Budget (Less other = total - GFE - basic).
    §2 MYP POP distribution     stacked column, 6x2 - BIW / Ingalls / Other-US / Foreign /
        Unparsed POP shares (%)  <- TAM Build.
    §3 MYP outside-yards split  stacked column, 2x3 - MYP-corrected (~33%) vs disclosed
        artifact (~74%/87%) outside-yards share (%)  <- TAM Build.
    §4 Annual TAM build         waterfall, 2x6   - BC base -> -non-supplier -> BC stream("e")
        -> +AP/LLTM -> Portfolio TAM("e"), average annual $M  <- TAM Build (cum / n_years).
    §5 TAM by fiscal year       stacked column, 3x7 - BC + AP/LLTM stream by FY22-27 ($M)
        <- TAM Build.
    §6 Work-type allocation     ranked column, 2x9 - Unbucketed residual (hero) + 7 work-type
        buckets, average annual $M  <- SAM Build (bucket TAM / n_years).
    §7 SAM scenarios            ranked column, 2x6 - five scenario cuts, average annual SAM $M
        <- SAM Build.
    §8 Supplier landscape       bar, 10x2        - top-10 visible suppliers, names down the
        left column, lifetime visible flow $M across  <- Entity Master.
    §9 FFATA visibility gap     column, 2x5      - visible flow vs low / mid / high outsourcing
        bands ($M), numeric inputs from cost_funnel_summary.csv (no model producer).

Notes
- Native cell notes: none. Note column: none. No block for cover / dividers /
  market_primer / scope / tam_methodology / sam_taxonomy / market_direction / implications
  / appendix slides - those are shape / text exhibits or equation engines, not native charts.
- executive_summary has no block: its chart was removed (the slide is a KPI board).
- Mirror, not a live feed: regenerate the affected block whenever the deck's rendered chart
  set changes. Block layouts follow the chart-conversion target types (docs/chart_conversion_spec.md).
