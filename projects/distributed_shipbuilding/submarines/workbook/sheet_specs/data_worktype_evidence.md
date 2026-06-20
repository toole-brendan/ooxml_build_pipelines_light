Worktype Evidence
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_worktype_evidence.py

Purpose
Top vendors per work-type bucket plus an unbucketed watchlist - the reading evidence for
why each bucket's observed share looks the way it does. Pure consumer: every cell links
back to Entity Master; it exports no accessors of its own.

Reads
- Entity Master   ent_row_cell(i, key) - vendor / dollar / naics_desc / basis per row;
                  top_vendor_indices(bucket, n) + unbucketed_vendor_indices(n) - the
                  ranked supplier rows per bucket; observed_bucket_dollar_cell(b) - the
                  §4 supplier $ per bucket
- taxonomy.BUCKETS / UNBUCKETED - the 7 work-type buckets to iterate (display names)

Feeds
- none (leaf consumer; exposes no producer cells and registers no defined name)

On the sheet
§1  At a glance: supplier $ + top vendor per bucket
    - One row per bucket (then an unbucketed row): Bucket, Supplier $M, Top vendor,
      Evidence count.
        Supplier $M    = observed_bucket_dollar_cell(key)  <- Entity Master §4
        Top vendor     = ent_row_cell(top_vendor_indices(key, 1)[0], 'vendor')  (or "-")
        Evidence count = count of supplier rows in that bucket (len of top_vendor_indices)

§2  Top vendors per bucket (links to Entity Master)
    - One sub-section per bucket (§2a..§2g, in BUCKETS order), each "<bucket> (top 3 by
      subaward $)" with Rank, Vendor, $M, NAICS desc, Class rule. Each row =
      ent_row_cell(i, key) for i in top_vendor_indices(bucket, 3)  <- Entity Master (live
      links).
    §2h Unbucketed watchlist (top 10 supplier $, no clean bucket)
        Rank, Vendor, $M, NAICS desc, Why unbucketed - rows from
        ent_row_cell(i, key) for i in unbucketed_vendor_indices(10)  <- Entity Master.

Notes
- Native cell notes: none.
- Note column: none.
