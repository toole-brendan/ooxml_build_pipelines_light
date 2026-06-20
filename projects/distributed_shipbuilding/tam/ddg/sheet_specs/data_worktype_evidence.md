Worktype Evidence
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_worktype_evidence.py

Purpose
The work-type bucket map, the top vendors within each bucket, and the
classification evidence behind the bucket assignments. Conceptually linked to
Methodology but does not duplicate the long taxonomy prose.

Reads
- Entity Master   top-3 supplier rows per bucket [top_vendor_indices], live links to each
             vendor / $M / NAICS-desc cell [ent_row_cell]
- _taxonomy.BUCKETS  the seven work-type buckets (key, name, definition)

Feeds
- none

On the sheet
§1  Bucket map
    - One row per bucket from _taxonomy.BUCKETS: Bucket name + Definition (static
      taxonomy prose, not formula-driven).

§2  Top vendors by bucket (from Entity Master)
    - One sub-block §2a..§2g per bucket (a..g), header "<bucket> (top 3 by subaward $)".
    - Each lists up to 3 ranked supplier rows; the vendor index list comes from
      Entity Master top_vendor_indices(bucket_key, 3) (supplier-role rows in that bucket).
    - Vendor   = <- Entity Master ent_row_cell(i, 'vendor')
    - $M       = <- Entity Master ent_row_cell(i, 'dollar')
    - NAICS desc = <- Entity Master ent_row_cell(i, 'naics_desc')

§3  Classification evidence
    - Static arbiter table (how a bucket is assigned), mirroring the Entity Master classifier
      order: Description keyword (primary) -> Vendor-name override -> NAICS-4 fallback
      (used when the description is thin).

Notes
- Native cell notes: none.
- Note column: none.
