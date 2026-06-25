"""summary_overview - the "Summary" tab: the subaward corpus at a glance.

Four short sections, nothing hardcoded - every figure is a live formula or a
cross-sheet link:
  §1 Scope          - source, FY window, programs and the data-currency date;
                      Window and As-of link to the Assumptions control cells so they
                      can't drift.
  §2 Corpus shape   - per-program supplier $M / records / supplier share /
                      unique vendors / PIID coverage / award span (links and
                      COUNTIF/MINIFS/MAXIFS over Market Views and Role Detail).
  §3 Supplier base structure - per-program multi- vs single-source lane counts
                      (multi keyed off the Assumptions vendor minimum) and top-vendor
                      share.
  §4 Indicator counts - per-program Concentration (top-1 >= the Assumptions cutoff),
                      Source diversification, the PERIODIC sourcing openings due
                      (eligible AND cadence-applicable AND window-due), the ACTIVE
                      continuous sourcing openings (continuous + still buying), and
                      two diagnostics beneath them - the broader structural
                      continuous multi-source lane count and the ungated date-only
                      timing signal - COUNTIFS / MAXIFS over the indicator screens
                      on the LIVE Assumptions windows/thresholds.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_INT, S_NUM, S_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_award_analysis.sheets._layout import RowCursor
from workbook_award_analysis.sheets._cuts import PROGRAMS, FY_LABELS
from workbook_award_analysis.sheets.model_by_worktype import (
    wt_total_cell, wt_records_total_cell,
)
from workbook_award_analysis.sheets.model_by_piid import piid_section_cols
from workbook_award_analysis.sheets.model_by_vendor import (
    bv_cols, vendor_total_cell,
)
from workbook_award_analysis.sheets.data_role_detail import rd_cols
from workbook_award_analysis.sheets.model_piid_worktype import (
    pw_multi_count, pw_single_count,
)
from workbook_award_analysis.sheets.model_rebuy_timing import (
    rb_due_count, rb_timing_due_count,
)
from workbook_award_analysis.sheets.model_continuous_sourcing import (
    cont_opening_count, cont_lane_count,
)
from workbook_award_analysis.sheets.model_concentrated_lanes import (
    cl_concentrated_count,
)
from workbook_award_analysis.sheets.model_source_concentration import (
    sc_emerging_count,
)
from workbook_award_analysis.sheets.summary_inputs import (
    input_asof_cell, input_recent_fy_cell,
)
from workbook_award_analysis.sheets._widths import header_styles
from workbook_award_analysis.sheets._tabs import TAB_SUMMARY

_GROUP = "summary"
_TAB = TAB_SUMMARY
_NCOLS = 1 + len(PROGRAMS)


def _make_overview():
    BV = bv_cols()
    R = rd_cols()
    n_prog = len(PROGRAMS)
    prog_names = [pname for _, pname in PROGRAMS]

    # --- §2 corpus-shape formulas ---
    def vendors_f(prog: str) -> str:
        return f'=COUNTIF({BV["prog"]},"{prog}")'

    def share_f(prog: str) -> str:
        sup = (f'SUMIFS({R["dtot"]},{R["prog"]},"{prog}",'
               f'{R["role"]},"Supplier")')
        allr = f'SUMIFS({R["dtot"]},{R["prog"]},"{prog}")'
        return f"=IF({allr}=0,0,{sup}/{allr})"

    def piids_f(prog: str) -> str:
        P = piid_section_cols(prog)
        return (f'=COUNTIF({P["status"]},"<>none")&" of "'
                f'&COUNTA({P["piid"]})')

    def span_f(prog: str) -> str:
        # MINIFS/MAXIFS are post-2007 functions: raw sheet XML must carry
        # the _xlfn. prefix or Excel shows #NAME?.
        crit = f'{BV["prog"]},"{prog}"'
        return (f'=TEXT(_xlfn.MINIFS({BV["first"]},{crit},{BV["first"]},"<>"),'
                f'"yyyy-mm-dd")&" to "'
                f'&TEXT(_xlfn.MAXIFS({BV["last"]},{crit},{BV["last"]},"<>"),'
                f'"yyyy-mm-dd")')

    note_f = ('="Vendors on both submarine classes count once per class ("'
              f'&COUNTIFS({BV["prog"]},"virginia",{BV["profile"]},"both")'
              '&" on both)."')

    # --- §3 supplier-base-structure formulas ---
    def multi_f(prog: str) -> str:
        return f"={pw_multi_count(prog)}"

    def single_f(prog: str) -> str:
        return f"={pw_single_count(prog)}"

    def top1_f(prog: str) -> str:
        # top vendor's $ Total over the program's supplier total, both off
        # By Vendor so numerator and denominator reconcile exactly.
        denom = vendor_total_cell(prog)
        return (f"=IF(({denom})=0,0,"
                f'_xlfn.MAXIFS({BV["tot"]},{BV["prog"]},"{prog}")/({denom}))')

    def concentrated_f(prog: str) -> str:
        return f"={cl_concentrated_count(prog)}"

    def emerging_f(prog: str) -> str:
        return f"={sc_emerging_count(prog)}"

    def rebuy_f(prog: str) -> str:
        return f"={rb_due_count(prog)}"

    def continuous_f(prog: str) -> str:
        return f"={cont_opening_count(prog)}"

    def continuous_lane_f(prog: str) -> str:
        return f"={cont_lane_count(prog)}"

    def timing_signal_f(prog: str) -> str:
        return f"={rb_timing_due_count(prog)}"

    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 - Scope
    c.banner("§1 - Scope",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Source", "FSRS reported subaward records (supplier role)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Window",
             f'="{FY_LABELS[0]} through {FY_LABELS[-1]} '
             f'(subaward action FY; FY26 partial); recent = FY"&'
             f'{input_recent_fy_cell()}&" onward"'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Programs", ", ".join(prog_names)],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["As of",
             f'=TEXT({input_asof_cell()},"yyyy-mm-dd")'
             '&" (latest reported award; Assumptions §3)"'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 - Corpus shape
    c.banner("§2 - Corpus shape",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write([""] + prog_names, styles=header_styles([""] + prog_names))
    c.write(["Supplier $M (full history)"]
            + [f"={wt_total_cell(prog)}" for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_NUM] * n_prog, outline_level=1)
    c.write(["Supplier records"]
            + [f"={wt_records_total_cell(prog)}" for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Supplier share of reported"]
            + [share_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_PCT] * n_prog, outline_level=1)
    c.write(["Unique supplier vendors"]
            + [vendors_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["PIIDs with FSRS records (of in-scope)"]
            + [piids_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] * (1 + n_prog), outline_level=1)
    c.write(["First / last subaward"]
            + [span_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] * (1 + n_prog), outline_level=1)
    c.write([note_f], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 - Supplier base structure
    c.banner("§3 - Supplier base structure",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write([""] + prog_names, styles=header_styles([""] + prog_names))
    c.write(["Multi-source lanes (≥ Assumptions min)"]
            + [multi_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Single-source lanes"]
            + [single_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Top vendor share of program $"]
            + [top1_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_PCT] * n_prog, outline_level=1)
    c.blank(2)

    # §4 - Indicator counts
    c.banner("§4 - Indicator counts",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write([""] + prog_names, styles=header_styles([""] + prog_names))
    c.write(["Concentration (top-1 ≥ cutoff)"]
            + [concentrated_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Source diversification lanes"]
            + [emerging_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Periodic sourcing openings due (eligible, cadence ≤ horizon)"]
            + [rebuy_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Active continuous sourcing openings (currently buying)"]
            + [continuous_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Continuous multi-source lanes (structural, diagnostic)"]
            + [continuous_lane_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)
    c.write(["Ungated timing signal (date only, diagnostic)"]
            + [timing_signal_f(prog) for prog, _ in PROGRAMS],
            styles=[S_DEFAULT] + [S_INT] * n_prog, outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[38] + [24] * n_prog,
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    return SheetEntry(_TAB, _GROUP, render)


OVERVIEW = _make_overview()
