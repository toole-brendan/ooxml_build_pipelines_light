"""columbia_tam - the "Columbia TAM" tab (model group).

Columbia-class (LI 1045): BC stream only, on the announced Build I supplier
coefficient, plus the folded FY2028-31 outyear projection. Columbia has no OBBBA
mandatory award and (as a submarine) no broken-out AP/LLTM stream.
"""
from __future__ import annotations

from workbook_master_tam.sheets._program_tam import build_program_tam
from workbook_master_tam.sheets._tabs import TAB_COLUMBIA_TAM
from workbook_master_tam.sheets.place_of_performance import col_bc_coeff_cell

COLUMBIA_TAM, _A = build_program_tam(
    li=1045, name="Columbia", tab=TAB_COLUMBIA_TAM,
    intro="Columbia BC TAM, FY2022-31",
    bc_coeff_cell=col_bc_coeff_cell, obbba="none")

tam_cell = _A["tam_cell"]
cum_tam_cell = _A["cum_tam_cell"]
avg_annual_tam_cell = _A["avg_annual_tam_cell"]
applied_coeff_cell = _A["applied_coeff_cell"]
pen_fy2225_cell = _A["pen_fy2225_cell"]
outyear_low_avg_cell = _A["outyear_low_avg_cell"]
outyear_high_avg_cell = _A["outyear_high_avg_cell"]
outyear_low_cell = _A["outyear_low_cell"]
outyear_high_cell = _A["outyear_high_cell"]
