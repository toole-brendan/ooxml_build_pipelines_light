"""model_by_vessel - the "Vessel & Builder" cut sheet (compact).

One filterable native table: supplier $M and record counts split by submarine
class (Virginia / Columbia, program-keyed) and DDG builder (GD-BIW / HII-Ingalls,
builder-keyed). COMPACT (no 16-FY grid): both figures are black SUMIFS over the
Lane Detail leaf - program-keyed for the submarine classes, builder-keyed for the
DDG yards. The filter-aware SUBTOTAL Totals Row sums the four rows to the grand
supplier total (Virginia + Columbia + GD-BIW + HII-Ingalls = the full corpus).
With no FY grid there are no intra-block forward refs, so the old two-pass build
is gone.

Built at import via _make_by_vessel() into a standalone single-table sheet (its
own title banner, §1 section table, column widths and autofilter).

Promoted accessor (module-level, leaf-relative; imported by Checks):
  vessel_total_cell(program) - virginia / columbia / ddg supplier $M (SUMIFS over
                               Lane Detail; Checks).
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_INT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import ExcelTable, WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets.data_lane_detail import ld_cols
from workbook_award_analysis.sheets._widths import (
    W_BUILDER, W_DOLLAR, W_COUNT, header_styles,
)
from workbook_award_analysis.sheets._tabs import TAB_VESSEL_BUILDER

_GROUP = "model"
_TAB = TAB_VESSEL_BUILDER
_BANNER = "§1 - Vessel / builder"

_META = ["Class / builder", "$M", "Records"]
_NCOLS = len(_META)
_COLS = [W_BUILDER, W_DOLLAR, W_COUNT]
_DOL_COL = col_letter(2)                # C  ($M)
_REC_COL = col_letter(3)                # D  (Records)


def _make_by_vessel():
    """Build the Vessel / builder cut sheet: a row-2 title banner + the §1
    section table. Returns the SheetEntry (vessel_total_cell is module-level)."""
    c = RowCursor(2)
    c.banner(_TAB, n_cols=len(_COLS), style=S_TITLE_SHEET)
    c.blank()
    L = ld_cols()
    # (label, SUMIFS criteria) - submarine classes program-keyed, DDG yards
    # builder-keyed; the four sum to the grand supplier total.
    cuts = [
        ("Virginia",    f'{L["prog"]},"virginia"'),
        ("Columbia",    f'{L["prog"]},"columbia"'),
        ("GD-BIW",      f'{L["builder"]},"GD-BIW"'),
        ("HII-Ingalls", f'{L["builder"]},"HII-Ingalls"'),
    ]
    c.banner(_BANNER, n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_META, styles=header_styles(_META))
    f = hdr + 1
    last = hdr
    for label, crit in cuts:
        last = c.write(
            [label, f'=SUMIFS({L["dtot"]},{crit})',
             f'=SUMIFS({L["ntot"]},{crit})'],
            styles=[S_DEFAULT, S_NUM, S_INT], outline_level=1)
    table_ref = f"B{hdr}:{col_letter(_NCOLS)}{last}"
    c.total(
        ["Total",
         f"=SUBTOTAL(109,{_DOL_COL}{f}:{_DOL_COL}{last})",
         f"=SUBTOTAL(109,{_REC_COL}{f}:{_REC_COL}{last})"],
        styles=[S_BOLD, S_NUM, S_INT], n_cols=_NCOLS)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True)
        return WorksheetSpec(ws, tables=[
            ExcelTable(name="VesselDetail", ref=table_ref, headers=_META)])

    return SheetEntry(_TAB, _GROUP, render)


# --- module-level Class A accessor (leaf-relative; no own-row dependency) ------

def vessel_total_cell(program: str) -> str:
    L = ld_cols()
    return f'SUMIFS({L["dtot"]},{L["prog"]},"{program}")'


VESSEL_BUILDER = _make_by_vessel()
