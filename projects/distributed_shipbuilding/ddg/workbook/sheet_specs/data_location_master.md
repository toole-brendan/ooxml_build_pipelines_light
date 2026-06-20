Location Master
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_location_master.py

Purpose
Prime-site and domestic/foreign location evidence; foreign work is treated as
supplier-addressable (away from the two prime yards). Location is a HINT only -
the award-action scope controls, not the vendor's state.

Source
extracted/nc_lifetime_vendors.csv  - lifetime vendor $ with a foreign flag; aggregated
   in Python into a domestic vs foreign $M split (foreign flag in true/yes/y/1/t -> foreign).

Reads
- none (standalone location extract; no sibling-sheet links)

Feeds
- none (location is a HINT only; no major downstream accessors)

On the sheet
§1  Prime sites
    - Static table of the two prime-controlled final-assembly yards: GD Bath Iron Works
      (Maine) and HII Ingalls Shipbuilding (Mississippi). Work there is not addressable.

§2  Location principle
    - Static prose: location is a hint, the award-action scope controls; BIW + Ingalls
      are prime-controlled final-assembly sites.

§3  Domestic / foreign split (foreign = supplier-addressable)
    - Domestic (US) and Foreign rows: $M lifetime = Python-summed from the CSV foreign
      flag (input values), rounded to 1 decimal.
    - % of total = $M row / Total $M  (each origin row over the Total row).
    - Total row = SUM($ column) and SUM(% column) over the two origin rows.

Notes
- Native cell notes: none.
- Note column: none.
