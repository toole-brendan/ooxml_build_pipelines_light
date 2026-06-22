"""model_budget_market - the funded-demand spine by program x fiscal year (live).

The Army watercraft FUNDED market, read straight from the budget funding facts as LIVE
SUMIFS - so every number traces to a budget-book cell on the Budget Facts leaf. Single
vintage (the latest PB book, FY2027) so no cross-vintage blending, and each FY shown in its
own money-type (PY actual -> CY enacted -> BY request -> outyears) so NOTHING double-counts
across amount_type / column_role. The anti-double-count rules are enforced in the formulas:
request uses column_role=request_total (NOT base+oco+total), each FY appears once.

  Forward FY27-31 $M = the BY request (FY27) + the four outyear estimates (FY28-31): the
  programmed forward spine, the gross funded universe the Market Size sheet sizes against.

Eligible watercraft lines roll up; the <$5M float/rail aggregate and the PE-total (context)
are shown as memo rows BELOW the total, excluded from the spine.
"""
from __future__ import annotations

from workbook_core.primitives import col_letter, worksheet
from workbook_core.styles import (
    S_BOLD, S_DEFAULT, S_NUM, S_TITLE_SECTION, S_TITLE_SHEET,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_army.sheets._layout import RowCursor
from workbook_army.sheets._italic import S_ITALIC
from workbook_army.sheets._widths import header_styles
from workbook_army.sheets._tabs import TAB_BUDGET_MARKET
from workbook_army.sheets.data_budget_facts import budget_facts_cols

_GROUP = "model"
_TAB = TAB_BUDGET_MARKET
_VINTAGE = "2027"               # latest PB book; single-vintage forward view (no blending)

_HEADERS = ["Program", "Line item", "Approp / measure", "FY25 actual", "FY26 enacted",
            "FY27 request", "FY28 (out)", "FY29 (out)", "FY30 (out)", "FY31 (out)",
            "Forward FY27-31 $M"]
_NCOLS = len(_HEADERS)
_COLS = [38, 20, 22, 12, 12, 12, 12, 12, 12, 12, 16]
assert len(_COLS) == _NCOLS, (len(_COLS), _NCOLS)
_CENTER = {h for h in _HEADERS[3:]}
_CL = {h: col_letter(i + 1) for i, h in enumerate(_HEADERS)}

# (label, line_item_id, approp/measure text, measure, eligible-for-rollup)
_ELIGIBLE = [
    ("MSV(L) - Maneuver Support Vessel (Light)", "8211R01001", "OPA / net P-1", "net_procurement_p1"),
    ("Army Watercraft ESP (SLEP)", "3569M11101", "OPA / net P-1", "net_procurement_p1"),
    ("Project 526 - Marine S&T (autonomy/C2)", "RDTE-0603804A-526", "RDT&E / cost", "rdte_cost"),
]
_MEMO = [
    ("Items < $5.0M (Float/Rail) - minor", "9552ML5355", "OPA / net P-1 (minor)", "net_procurement_p1"),
    ("PE 0603804A total (context only)", "RDTE-0603804A", "RDT&E / PE total (context)", "rdte_cost"),
]
# (column header, observed_fy, column_role)
_FYCOLS = [("FY25 actual", "2025", "actual"), ("FY26 enacted", "2026", "enacted"),
           ("FY27 request", "2027", "request_total"), ("FY28 (out)", "2028", "outyear"),
           ("FY29 (out)", "2029", "outyear"), ("FY30 (out)", "2030", "outyear"),
           ("FY31 (out)", "2031", "outyear")]


def _make_budget_market():
    FL = budget_facts_cols("line_item_id")
    FB = budget_facts_cols("source_book_fy")
    FM = budget_facts_cols("measure")
    FYr = budget_facts_cols("observed_fy")
    FR = budget_facts_cols("column_role")
    FA = budget_facts_cols("amount")

    def bcell(line, measure, fy, role):
        return (f'=SUMIFS({FA},{FL},"{line}",{FB},"{_VINTAGE}",{FM},"{measure}",'
                f'{FYr},"{fy}",{FR},"{role}")')

    F27, F31 = _CL["FY27 request"], _CL["FY31 (out)"]
    fwd_f = lambda r: f"=SUM({F27}{r}:{F31}{r})"

    def row_vals(label, line, approp, measure):
        cells = [bcell(line, measure, fy, role) for _h, fy, role in _FYCOLS]
        return [label, line, approp] + cells + [fwd_f]

    styles = [S_DEFAULT, S_DEFAULT, S_DEFAULT] + [S_NUM] * 8

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.write(["Army watercraft funded market by program x FY (live from Budget Facts). FYs "
             "are different money-types - never summed across types. Then-year $M."],
            styles=[S_ITALIC])
    c.blank(2)

    c.banner("§1 - Eligible watercraft funding lines", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    e_first = hdr + 1
    for label, line, approp, measure in _ELIGIBLE:
        c.write(row_vals(label, line, approp, measure), styles=styles)
    e_last = hdr + len(_ELIGIBLE)

    total_vals = [None] * _NCOLS
    total_vals[0] = "Gross funded spine (eligible)"
    for h in _HEADERS[3:]:
        cl = _CL[h]
        total_vals[_HEADERS.index(h)] = f"=SUM({cl}{e_first}:{cl}{e_last})"
    total_sty = [S_DEFAULT] * _NCOLS
    total_sty[0] = S_BOLD
    for h in _HEADERS[3:]:
        total_sty[_HEADERS.index(h)] = S_NUM
    tr = c.total(total_vals, styles=total_sty, n_cols=_NCOLS)
    refs = {"forward": f"'{_TAB}'!${_CL['Forward FY27-31 $M']}${tr}"}

    c.blank(2)
    c.banner("§2 - Memo (excluded from the spine)", n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(_HEADERS, styles=header_styles(_HEADERS, center_headers=_CENTER))
    for label, line, approp, measure in _MEMO:
        c.write(row_vals(label, line, approp, measure), styles=styles)

    c.blank(2)
    c.write(["Memo rows (float/rail < $5M; PE total) are excluded from the spine. Request "
             "uses request_total, never base+oco+total."], styles=[S_DEFAULT])
    c.write(["Funded $ is a demand signal - the Saronic share is applied on Market Size; "
             "never added to contract obligations."], styles=[S_DEFAULT])

    def render() -> WorksheetSpec:
        # Styled range (not a native table): row order is part of the model and the §2 memo
        # rows must not filter into the §1 spine. The header underline + total border carry it.
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render), refs


BUDGET_MARKET, TOTAL_REFS = _make_budget_market()
