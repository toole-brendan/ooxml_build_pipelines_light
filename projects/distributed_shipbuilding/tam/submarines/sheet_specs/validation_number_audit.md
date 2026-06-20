Number Audit
Tab color: 6E6E6E (gray)  ·  group: Validation
Module: validation_number_audit.py

Purpose
Ties every registered Figure Register figure (and every deck chart headline value)
back to its producer cell: deck value (the registry link) vs source value (the producer
cell), with a delta and a pass/fail status. Produces fail_count_formula / status_range,
consumed by QA Reconciliation and Executive Summary.

Reads
- Figure Register     REGISTRY, value_cell(fid), source_ref(fid), is_pct(fid)  [§2]
- z_ChartData          chart_audit_links() -> one headline (chart_id, value cell,
                      producer ref) per CD block  [§4]

Feeds
- Executive Summary, QA Reconciliation (both read fail_count_formula / status_range)
- Native table: tbl_sub_number_audit
- Accessors: status_range() -> 'Number Audit'!G<first>:G<last> (the §2 status column);
  fail_count_formula() -> COUNTIF(status_range, "FAIL")
- Constant: tolerance _TOL = 0.01

On the sheet
(Layout note: §2 tie-out is built first so fail_count_formula is promoted before §1.)

§1  At a glance: figure tie-out
    - Figures tested = len(REGISTRY).
    - FAIL count  = COUNTIF(§2 status column, "FAIL")    (target 0)
    - Status      = IF(FAIL count = 0, "OK", "FAIL")      (tolerance 0.01)

§2  Figure tie-out (every registered figure vs its producer cell)
    - tbl_sub_number_audit, one row per Figure Register row:
        - Deck value   = "=<value_cell(fid)>"  <- Figure Register E column (% or $ link)
        - Source value = "=<source_ref(fid)>"  <- the producer cell (% or $ link)
        - Delta  = Deck value - Source value          (D - E)
        - Status = IF(ABS(Delta) < 0.01, "OK", "FAIL")
      is_pct(fid) drives %-vs-$ styling (true for DO-02/03/04).

§3  Exceptions
    - Static row: "None / No exceptions while FAIL count = 0 / n/a" (placeholder list of
      any figure that needs manual reconciliation).

§4  z_ChartData tie-out (deck chart values vs producer cells)
    - One row per CD block headline link (from chart_audit_links()):
        - Chart value    = "=<chart value cell>"  <- z_ChartData Value column (H)
        - Producer value = "=<producer ref>"      <- the producer cell
        - Delta  = Chart value - Producer value          (C - D)
        - Status = IF(ABS(Delta) < 0.01, "OK", "FAIL")
      The remaining chart rows are guaranteed by z_ChartData assert_links() (every link row
      carries a real producer ref), so only one headline link per block is re-checked here.

Notes
- Native cell notes: none.
- Note column: none.
