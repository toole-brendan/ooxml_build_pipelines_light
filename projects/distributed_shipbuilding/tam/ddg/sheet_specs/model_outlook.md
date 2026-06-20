Outlook
Tab color: 1F4E5F (teal)  ·  group: Model
Module: model_outlook.py

Purpose
Outsourced BC penetration per FY and the FY2028-FY2031 outyear outlook: implied
Outsourced BC = PB2027 FYDP gross x a historical penetration assumption, shown as
a low/high range. Feeds the consolidated deck's Outsourced BC Annual TAM slide.

Reads
- TAM Build        per-FY total TAM [tam_total_cell]
- SCN Budget       constant-$ Total Ship Estimate per FY [scn_cell 'total']
- OBBBA Mandatory  constant-$ gross award [obbba_gross_cell]
- Assumptions      OBBBA include-toggle [include_obbba_stream_cell]
- FYDP Outyears    constant-$ FYDP gross FY2028-FY2031 [fydp_gross_cell]

Feeds
- z_ChartData §10-§12, Executive Summary §1, Figure Register
- Producer cells: penetration (per FY), pen_l6y, pen_2627, assum_lo/hi,
  oy_gross/lo/hi (per FY), oy_lo_avg/oy_hi_avg, tam_2225_avg

On the sheet
§1  Penetration & outyear outlook (at-a-glance; same-sheet refs)
§2  Outsourced BC penetration by FY (constant FY2026 $)
    - TAM (all streams) / (P-5c TSE + OBBBA gross), FY2022-FY2027; numerator and
      denominator both gate on the OBBBA include-toggle.
§3  Window-average penetration (ratio of sums)
    - FY22-27 and FY26-27 averages; low/high assumption = MIN/MAX of the two.
§4  Implied outyear Outsourced BC (FY2028-FY2031)
    - FYDP gross (constant) x low/high assumption; range row; FY28-31 averages.
§5  FY22-25 average annual TAM (the pre-OBBBA dashed-line reference)
§6  Checks
    - FY27 FYDP gross ties to SCN Budget FY27 TSE; penetration at or below 100%
      (REVIEW expected only with OBBBA toggled off); low at or below high.

Notes
- Native cell notes: none.
- Note column: none.
