Outlook
Tab color: 1F4E5F (teal)  ·  group: Model
Module: model_outlook.py

Purpose
Outsourced BC penetration per FY (portfolio: Virginia + Columbia) and the
FY2028-FY2031 outyear outlook: implied Outsourced BC = PB2027 FYDP portfolio
gross x a historical penetration assumption, shown as a low/high range. Feeds the
consolidated deck's Outsourced BC Annual TAM slide.

Reads
- TAM Build        per-FY total TAM, all streams incl. OBBBA [tam_total_cell]
- SCN Budget       constant-$ Total Ship Estimate per class per FY [scn_cell 'total']
- OBBBA Mandatory  then-year gross award per class [obbba_gross_cell]
- Assumptions      OBBBA include-toggle + FY27 execution spillover
- FYDP Outyears    constant-$ FYDP gross per class + portfolio [fydp_*]
- Deflators        constant-FY2026 factor for the OBBBA denominator term

Feeds
- z_ChartData §10-§12, Executive Summary §1, Figure Register
- Producer cells: penetration (per FY), pen_l6y, pen_2627, assum_lo/hi,
  oy_gross/lo/hi (per FY), oy_lo_avg/oy_hi_avg, tam_2225_avg

On the sheet
§1  Penetration & outyear outlook (at-a-glance; same-sheet refs)
§2  Outsourced BC penetration by FY (constant FY2026 $, portfolio)
    - TAM (all streams) / (Va + Col TSE + OBBBA gross), FY2022-FY2027; the OBBBA
      term is then-year x deflator, split FY26/FY27 by the spillover control and
      gated by the include-toggle, so numerator and denominator move together.
§3  Window-average penetration (ratio of sums)
    - FY22-27 and FY26-27 averages; low/high assumption = MIN/MAX of the two.
§4  Implied outyear Outsourced BC (FY2028-FY2031)
    - Portfolio FYDP gross (constant) x low/high assumption; per-class memos;
      range row; FY28-31 averages.
§5  FY22-25 average annual TAM (the pre-OBBBA dashed-line reference)
§6  Checks
    - FY27 FYDP gross ties to SCN Budget FY27 TSE per class; Virginia FY26 FYDP
      gross ties to the PB2027 $5,389.1M anchor; penetration at or below 100%;
      low at or below high.

Notes
- Native cell notes: none.
- Note column: none.
