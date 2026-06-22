"""virginia_tam - the "Virginia TAM" tab (model group).

Virginia-class (LI 2013): BC stream + OBBBA mandatory stream (Sec. 20002(16)), both
on the announced Block V supplier coefficient, plus the folded FY2028-31 outyear
projection. No AP/LLTM stream (P-10 supplier LLTM already inside P-5c BC for subs).
"""
from __future__ import annotations

from workbook_master_tam.sheets._program_tam import build_program_tam
from workbook_master_tam.sheets._tabs import TAB_VIRGINIA_TAM
from workbook_master_tam.sheets.place_of_performance import va_bc_coeff_cell

VIRGINIA_TAM, _A = build_program_tam(
    li=2013, name="Virginia", tab=TAB_VIRGINIA_TAM,
    intro="Virginia BC and OBBBA TAM, FY2022-31",
    bc_coeff_cell=va_bc_coeff_cell, obbba="spill")

tam_cell = _A["tam_cell"]
cum_tam_cell = _A["cum_tam_cell"]
avg_annual_tam_cell = _A["avg_annual_tam_cell"]
applied_coeff_cell = _A["applied_coeff_cell"]
pen_fy2225_cell = _A["pen_fy2225_cell"]
outyear_low_avg_cell = _A["outyear_low_avg_cell"]
outyear_high_avg_cell = _A["outyear_high_avg_cell"]
outyear_low_cell = _A["outyear_low_cell"]
outyear_high_cell = _A["outyear_high_cell"]
obbba_tam_cell = _A["obbba_tam_cell"]
