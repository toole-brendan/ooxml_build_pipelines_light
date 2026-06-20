FYDP Outyears
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_fydp_outyears.py

Purpose
Carries the PB2027 P-40 FYDP grid (FY2025-FY2031) for DDG-51 and converts it to
constant FY2026 dollars. FY2028-FY2031 gross is the budget-request basis the
Outlook sheet multiplies by historical penetration to imply future Outsourced BC.

Source
extracted/scn_li_resource_summary.csv (LI 2122 rows) - the PB2027 P-40 Resource Summary.

Reads
- Deflators   constant-FY2026 factor per FY [deflator_factor_cell]

Feeds
- Outlook §4 (implied outyear Outsourced BC = constant gross x penetration assumption)
- Producer cells: fydp_gross_then, fydp_gross (constant), fydp_qty

On the sheet
§1  Source exhibit (P-40 Resource Summary, PB2027)
    - Provenance fields: exhibit / program / vintage (PB2027, April 2026; outyears are
      the request, not appropriation) / column convention / PB2028 refresh trigger.
    - Then-year input rows FY2025-FY2031: Gross/Weapon System Cost, Procurement
      quantity, Net Procurement (P-1) (memo), Total Obligation Authority (memo).
    - FY2027 uses the "FY 2027 Total" column (Base + OOC), which ties to the SCN
      Budget P-5c Total Ship Estimate.

§2  Constant FY2026 $M (then-year x deflator)
    - Gross x Deflators factor per FY; FY2030-FY2031 factors are extrapolated
      (see Deflators tab Basis column).

Notes
- Native cell notes: none.
- Note column: none.
