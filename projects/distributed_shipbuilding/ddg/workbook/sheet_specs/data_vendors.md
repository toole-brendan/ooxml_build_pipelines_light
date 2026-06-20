Vendors
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_vendors.py

Purpose
Top FFATA-visible vendors by lifetime subaward $ and the concentration among
them; supplier-landscape evidence (visible floor, not the full market).

Source
extracted/nc_lifetime_vendors.csv  - lifetime vendor totals (vendor, foreign flag,
   amount_M_lifetime, records, piid_count). Sorted by $M descending; top 60 shown.

Reads
- none (standalone vendor extract; no sibling-sheet links)

Feeds
- none (reader / evidence support; does not drive the core model)
- Native table: tbl_ddg_top_vendors

On the sheet
§1  Top 60 vendors by lifetime $ (FFATA-visible)
    - Native table tbl_ddg_top_vendors: #, Vendor, Foreign, $M lifetime, Records, PIIDs
      (one row per vendor, top 60 by $M, all input values).

§2  Concentration (of the shown top vendors)
    - Top 10 / Top 25 / Top <shown> rows over the §1 $ column (col E):
    - $M lifetime = SUM(E first : E first+n-1)  - cumulative top-n $.
    - % of shown total = group $ / shown-total $  (each row over the Top-<shown> row).

Notes
- Native cell notes: none.
- Note column: none.
