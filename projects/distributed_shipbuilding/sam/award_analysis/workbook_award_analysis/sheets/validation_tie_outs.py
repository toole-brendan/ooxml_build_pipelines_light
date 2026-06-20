"""validation_tie_outs - the "Tie-Outs" tab.

Live cross-sheet reconciliation: the full-history supplier $M total of every
cut tab (By Role supplier row, By Work Type, By Vessel, By PIID, PIID x Work
Type lane $M, By Vendor) must be the same number per program (Virginia /
Columbia / DDG-51 - one column each). Each cell links the source tab's total
cell; the check row compares max vs min within $0.5M. §2 does the same for
supplier record counts (By Role supplier row, By Work Type count grid, By
PIID supplier records, PIID x Work Type, By Vendor SUMIF) - integer counts,
so the check is exact equality. With the roll-ups now formula-driven, the
legs ultimately tie the workbook's three independent leaf datasets: Lane
Detail (lane x FY), Lane Vendors (vendor x lane), and By Vendor (vendor x
FY). The raw Award Events leaf (one row per supplier record) reconciles on
both bases too - every supplier award lands there, so a SUMIF / COUNTIF over
it must hit the same per-program totals as every other cut.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_LINK_INT, S_LINK_NUM, S_NUM,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_award_analysis.sheets._widths import header_styles
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import PROGRAMS
from workbook_award_analysis.sheets.data_role_detail import (
    role_supplier_total_cell, role_supplier_records_cell,
)
from workbook_award_analysis.sheets.data_lane_vendor_fy import (
    lvf_total_cell, lvf_records_total_cell,
)
from workbook_award_analysis.sheets.data_award_waves import (
    aw_total_cell, aw_records_total_cell,
)
from workbook_award_analysis.sheets.data_wave_vendors import (
    wv_total_cell, wv_records_total_cell,
)
from workbook_award_analysis.sheets.data_award_events import (
    ae_total_cell, ae_records_total_cell,
)
from workbook_award_analysis.sheets.model_by_worktype import (
    wt_total_cell, wt_records_total_cell,
)
from workbook_award_analysis.sheets.model_by_vessel import vessel_total_cell
from workbook_award_analysis.sheets.model_by_piid import (
    piid_total_cell, piid_sup_records_cell,
)
from workbook_award_analysis.sheets.model_by_vendor import (
    vendor_total_cell, vendor_records_total_cell,
)
from workbook_award_analysis.sheets.model_piid_worktype import (
    pw_records_total_cell, pw_dollar_total_cell,
)
from workbook_award_analysis.sheets._tabs import TAB_CHECKS

_GROUP = "validation"
_TAB = TAB_CHECKS
_NCOLS = 1 + len(PROGRAMS)
_PCOL = [col_letter(2 + j) for j in range(len(PROGRAMS))]  # C, D, E

# (label, accessor, is_link). is_link=True legs are pure cross-sheet links to a
# leaf sheet's own total cell (green); is_link=False legs are SUMIFS recomputed
# over a leaf (black derived) - the independence lives in the leaves, so the
# cross-leaf check still holds.
_MEASURES = [
    ("Role detail - supplier $M", role_supplier_total_cell, False),
    ("Market Views - Work type $M", wt_total_cell, False),
    ("Market Views - Vessel $M", vessel_total_cell, False),
    ("Market Views - PIID $M", piid_total_cell, False),
    ("Supplier Lanes - lane $M", pw_dollar_total_cell, False),
    ("Market Views - Vendor $M (SUMIF)", vendor_total_cell, True),
    ("Detail Tables - Lane vendor FY $M (SUMIF)", lvf_total_cell, True),
    ("Detail Tables - Wave vendors $M (SUMIF)", wv_total_cell, True),
    ("Detail Tables - Award waves $M (rollup)", aw_total_cell, True),
    ("Detail Tables - Award events $M (SUMIF)", ae_total_cell, True),
]

_COUNT_MEASURES = [
    ("Role detail - supplier records", role_supplier_records_cell, False),
    ("Market Views - Work type records", wt_records_total_cell, False),
    ("Market Views - PIID records", piid_sup_records_cell, False),
    ("Supplier Lanes - records", pw_records_total_cell, False),
    ("Market Views - Vendor records (SUMIF)", vendor_records_total_cell, True),
    ("Detail Tables - Lane vendor FY records (SUMIF)", lvf_records_total_cell, True),
    ("Detail Tables - Wave vendors records (SUMIF)", wv_records_total_cell, True),
    ("Detail Tables - Award waves records (rollup)", aw_records_total_cell, True),
    ("Detail Tables - Award events records (COUNTIF)", ae_records_total_cell, True),
]


def _make_tie_outs():
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Supplier $M tie-out",
             n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Cut"] + [pname for _, pname in PROGRAMS],
            styles=header_styles(["Cut"] + [pname for _, pname in PROGRAMS]))
    first = last = None
    for label, cell, is_link in _MEASURES:
        leg = S_LINK_NUM if is_link else S_NUM
        r = c.write([label] + [f"={cell(prog)}" for prog, _ in PROGRAMS],
                    styles=[S_DEFAULT] + [leg] * len(PROGRAMS),
                    outline_level=1)
        first = first if first is not None else r
        last = r
    c.blank()
    c.write(["Tie check (max - min < $0.5M)"]
            + [f'=IF(MAX({col}{first}:{col}{last})-MIN({col}{first}:{col}{last})'
               f'<0.5,"OK","FAIL")' for col in _PCOL],
            styles=[S_BOLD] + [S_DEFAULT] * len(PROGRAMS))
    c.blank(2)
    c.banner("§2 - Supplier records tie-out",
             n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Cut"] + [pname for _, pname in PROGRAMS],
            styles=header_styles(["Cut"] + [pname for _, pname in PROGRAMS]))
    first = last = None
    for label, cell, is_link in _COUNT_MEASURES:
        leg = S_LINK_INT if is_link else S_INT
        r = c.write([label] + [f"={cell(prog)}" for prog, _ in PROGRAMS],
                    styles=[S_DEFAULT] + [leg] * len(PROGRAMS),
                    outline_level=1)
        first = first if first is not None else r
        last = r
    c.blank()
    c.write(["Tie check (exact)"]
            + [f'=IF(MAX({col}{first}:{col}{last})-MIN({col}{first}:{col}{last})'
               f'=0,"OK","FAIL")' for col in _PCOL],
            styles=[S_BOLD] + [S_DEFAULT] * len(PROGRAMS))
    c.blank(2)
    c.write(["Basis: nominal supplier $M, full FSRS history."],
            styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[42] + [14] * len(PROGRAMS),
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render, hidden=True)


TIE_OUTS = _make_tie_outs()
