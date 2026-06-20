FYDP Outyears
Tab color: 7B1F3A (burgundy)  ·  group: Source data
Module: data_fydp_outyears.py

Purpose
Carries the PB2027 P-40 FYDP grid (FY2025-FY2031) for Virginia and Columbia and
converts it to constant FY2026 dollars. FY2028-FY2031 portfolio gross is the
budget-request basis the Outlook sheet multiplies by historical penetration to
imply future Outsourced BC.

Source
extracted/scn_li_resource_summary.csv (LI 2013 / LI 1045 rows) - the PB2027 P-40
Resource Summary.

Reads
- Deflators   constant-FY2026 factor per FY [deflator_factor_cell]

Feeds
- Outlook §4 (implied outyear Outsourced BC = constant portfolio gross x penetration)
- Producer cells: fydp_gross_then, fydp_gross (constant, per class), fydp_qty,
  fydp_portfolio_gross (constant, Va + Col)

On the sheet
§1  Source exhibit (P-40 Resource Summary, PB2027)
    - Provenance fields: exhibit / programs / vintage (PB2027, April 2026; outyears are
      the request, not appropriation) / column convention / PB2028 refresh trigger.
    §1a Virginia (LI 2013), then-year $M - Gross/Weapon System Cost, Procurement
        quantity, Net Procurement (P-1) (memo), Total Obligation Authority (memo),
        FY2025-FY2031. Virginia FY2026 gross is the $5,389.1M one-boat value the
        TAM Build tripwire pins.
    §1b Columbia (LI 1045), then-year $M - same rows.
    - FY2027 uses the "FY 2027 Total" column (Base + OOC), which ties to the SCN
      Budget P-5c Total Ship Estimate.

§2  Constant FY2026 $M (then-year x deflator)
    - Per-class gross x Deflators factor per FY, plus the portfolio (Va + Col) total
      row; FY2030-FY2031 factors are extrapolated (see Deflators tab Basis column).

Notes
- Native cell notes: none.
- Note column: none.
