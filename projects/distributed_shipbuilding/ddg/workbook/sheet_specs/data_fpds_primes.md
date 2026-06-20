FPDS Primes
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_fpds_primes.py

Purpose
Annual prime obligations by vendor group (de-capped) as context; not a direct
TAM input, used to frame the prime-yard layer and support MYP reconstruction.

Source
extracted/fpds_annual_by_prime.csv  - FPDS prime obligations by FY; each vendor-group
   column is named "<group>_obligated_$M". Groups are ordered to a fixed prime list
   (GD-BIW, HII-Ingalls, Rolls-Royce, GE-Propulsion, LM-Aegis, Raytheon, BAE-Guns/VLS,
   NG, GD-MissionSys, DRS, L3Harris), any extra column appended after.

Reads
- none (standalone FPDS extract; no sibling-sheet links)

Feeds
- none (de-capped prime pulls size obligations + MYP reconstruction; NOT a direct SAM
  bucket-allocation source)
- Native table: tbl_ddg_fpds_primes

On the sheet
§1  Annual obligations ($M by FY x vendor group; de-capped)
    - Native table tbl_ddg_fpds_primes: header "FY" + one column per vendor group.
    - One data row per FY from the CSV; each cell = the group's obligated $M (blank when 0).
    - Total row = SUM(column first_data:last_data) per vendor-group column.

§2  Use in model
    - Static caveat: de-capped prime pulls size obligations and MYP reconstruction;
      NOT a direct SAM bucket source.

Notes
- Native cell notes: none.
- Note column: none.
