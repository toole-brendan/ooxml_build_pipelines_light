Entity Master
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_entity_master.py

Purpose
Record-level subaward classification (description-led) by vendor and bucket; the
evidence base for bucket shares and supplier roles. Every FFATA subaward record is
classified (role / bucket / basis), then aggregated to one row per (vendor, UEI,
role, bucket), so a vendor splits across buckets when its descriptions support that.

Source
extracted/nc_records_long.csv  - every FFATA subaward record (the record-level corpus).
extracted/entity_naics_lookup.csv - the ~150-vendor UEI -> NAICS-4 / NAICS desc /
   country enrichment lookup (the NAICS-4 fallback arbiter).
Classification by _taxonomy.classify(vendor, naics4, desc): award description is the
primary arbiter, NAICS-4 the fallback. Records aggregated by (vendor, UEI, role,
bucket); $ converted to $M; basis = the dominant arbiter (+N when records mixed);
rows sorted by subaward $ descending.

Reads
- none (standalone record-level subaward source; enriched only by the NAICS lookup CSV)

Feeds
- Worktype Evidence (top vendors per bucket), SAM Build (role/bucket SUMPRODUCT shares),
  z_ChartData
- Native table: tbl_ddg_entity_master
- Promoted accessors: ent_dollar_range, role_range, bucket_range, country_range,
  naics_range, ent_first_data_row, ent_last_data_row, ent_row_cell, top_vendor_indices,
  top_supplier_indices, observed_addressable_total (sum of supplier-role $M)

On the sheet
§1  Subaward classification (description-led; record-level, by vendor-bucket)
    - Native table tbl_ddg_entity_master: one row per (vendor, UEI, role, bucket).
    - Columns: Vendor, UEI, Country, NAICS-4, NAICS desc, $M, Role, Bucket, Arbiter.
    - $M = subAwardAmount_$ / 1e6 summed per group; Country <- enrichment lookup, else
      "Foreign" when the record's foreign flag is set, else "-".
    - Role / Bucket / Arbiter = classify(vendor, naics4, desc); Arbiter shows the dominant
      arbiter with "+N" appended when a group mixes multiple arbiters.
    - The dollar / role / bucket / country / naics4 columns are exposed as ranges for
      the downstream SUMPRODUCT masks.

§2  Role summary
    - One row per role: Supplier (addressable), Prime yard, Co-prime yard,
      GFE / MIB / Navy-directed, Service / non-component.
    - $M lifetime = SUMPRODUCT((role_range = role) x ent_dollar_range)  - dollar-weighted
      roll-up of the §1 table by role.

§3  Bucket summary
    - One row per bucket key (BUCKET_KEYS, from _taxonomy.BUCKETS).
    - Supplier $M = SUMPRODUCT((role_range = "supplier") x (bucket_range = bucket) x
      ent_dollar_range)  - supplier-only subaward $ in each work-type bucket.

Notes
- Native cell notes: none.
- Note column: none.
