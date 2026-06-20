"""validation_qa_reconciliation - the "QA Reconciliation" tab (DDG, validation group; one module = one sheet).

The phase gate / all-clear sheet, with a status block on top. Links to TAM Build,
SAM Build, POP Audit, AP Bridge, Figure Audit. The figure-audit fail count LINKS to
Figure Audit's rendered cell (not recomputed).

Promoted accessors:
  fail_count_qa_formula, qa_fail_count_cell, qa_status_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT, S_PCT_INPUT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets.model_tam_build import (
    anchor_ok_cell, outside_yards_disclosed_cell, outside_yards_corrected_cell,
    portfolio_bc_tam_cell, portfolio_ap_tam_cell, bc_base_cell,
)
from workbook_ddg.sheets.data_scn_budget import scn_cell
from workbook_ddg.sheets.data_obbba_funding import obbba_gross_cell, obbba_bc_base_cell
from workbook_ddg.sheets.model_sam_build import (
    portfolio_tam_cell, modeled_share_total_cell, bucketed_total_cell,
    unbucketed_tam_cell, sam_cell,
)
from workbook_ddg.sheets.validation_pop_source_audit import (
    partition_ok_cell, coverage_cell, gfe_excluded_dollar_cell,
)
from workbook_ddg.sheets.data_ap_bridge import cy_ap_inwindow_cell, ap_tam_cell
from workbook_ddg.sheets.validation_number_audit import fail_count_formula, fail_count_cell as _fig_fail_cell
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "validation"
_TAB = "QA Reconciliation"
_NCOLS = 6
_Q = '"'
_QA_STATUS_ROW = 7
_QA_FAIL_ROW = 8
_CHECKS_FIRST = 17               # §2 reconciliation-check data rows
_N_CHECKS = 16
_CHECKS_LAST = _CHECKS_FIRST + _N_CHECKS - 1


def fail_count_qa_formula():
    return f'COUNTIF(\'{_TAB}\'!G{_CHECKS_FIRST}:G{_CHECKS_LAST},{_Q}FAIL{_Q})'


def qa_fail_count_cell():
    return f"'{_TAB}'!C{_QA_FAIL_ROW}"


def qa_status_cell():
    return f"'{_TAB}'!C{_QA_STATUS_ROW}"


def _render_qa_checks() -> WorksheetSpec:
    port = portfolio_tam_cell()
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Status
    c.banner("§1 - Status", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    qa_status = c.write(["QA status", f'=IF({fail_count_qa_formula()}=0,{_Q}OK{_Q},{_Q}FAIL{_Q})'],
                        styles=[S_BOLD, S_DEFAULT], outline_level=1)
    assert qa_status == _QA_STATUS_ROW, f"qa status at {qa_status}, expected {_QA_STATUS_ROW}"
    c.write(["Number of failed checks", f"={fail_count_qa_formula()}"],
            styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.write(["Figure audit fails", f"={_fig_fail_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["POP partition status", f"={partition_ok_cell()}"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["POP coverage", f"={coverage_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT], outline_level=1)
    c.blank(2)

    # §2 Reconciliation checks
    c.banner("§2 - Reconciliation checks (all OK + Number Audit 0 FAIL)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Description", "Expected", "Actual", "Delta", "Status"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    checks = [
        ("QA-01", "Anchor: MYP-corrected outside-yards near ~42%", "text", "OK", f"={anchor_ok_cell()}", None, S_DEFAULT, S_DEFAULT),
        ("QA-02", "POP stream partition OK (every in-scope action BC)", "text", "OK", f"={partition_ok_cell()}", None, S_DEFAULT, S_DEFAULT),
        ("QA-03", "Confirmation coverage of in-scope corpus = 100%", "num", 1.0, f"={coverage_cell()}", 0.001, S_PCT_INPUT, S_LINK_PCT),
        ("QA-04", "Modeled bucket shares (7 + residual, window vector) sum to 100%", "num", 1.0, f"={modeled_share_total_cell()}", 0.001, S_PCT_INPUT, S_LINK_PCT),
        ("QA-05", "Sum of bucketed TAM = portfolio TAM", "num", f"={port}", f"={bucketed_total_cell()}", 0.5, S_LINK_NUM, S_LINK_NUM),
        ("QA-06", "Sum of bucketed TAM <= TAM", "num", 1, f"=IF({bucketed_total_cell()}<={port}+0.5,1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-07", "Broad-component SAM <= TAM (SAM subset of TAM)", "num", 1, f"=IF({sam_cell('broad')}<={port}+0.5,1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-08", "Broad SAM = TAM - unbucketed residual", "num", f"={port}-{unbucketed_tam_cell()}", f"={sam_cell('broad')}", 0.5, S_NUM, S_LINK_NUM),
        ("QA-09", "MYP correction real (disclosed > corrected)", "num", 1, f"=IF({outside_yards_disclosed_cell()}>{outside_yards_corrected_cell()},1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-10", "GFE / Navy-directed scope dropped (> 0)", "num", 1, f"=IF({gfe_excluded_dollar_cell()}>0,1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-11", "Figures: every deck figure ties to source (0 FAILs)", "num", 0, f"={_fig_fail_cell()}", 0.5, S_NUM_INPUT, S_LINK_NUM),
        ("QA-12", "Portfolio TAM = BC stream + AP/LLTM stream", "num", f"={port}", f"={portfolio_bc_tam_cell()}+{portfolio_ap_tam_cell()}", 0.5, S_LINK_NUM, S_NUM),
        ("QA-13", "AP/LLTM stream TAM <= in-window CY AP gross", "num", 1, f"=IF({ap_tam_cell()}<={cy_ap_inwindow_cell()}+0.5,1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-14", "OBBBA gross award ties to Sec. 20002(17) ($5,400.0M FY26)", "num", 5400.0, f"={obbba_gross_cell(2122, 2026)}", 0.5, S_NUM_INPUT, S_LINK_NUM),
        ("QA-15", "FY26 BC base in TAM = P-5c BC + OBBBA BC (toggles on)", "num", f"=N({scn_cell(2122, 2026, 'basic')})+N({obbba_bc_base_cell(2122, 2026)})", f"=N({bc_base_cell(2122, 2026)})", 0.5, S_NUM, S_NUM),
        ("QA-16", "OBBBA FY2027 funding = 0", "num", 0, f"=N({obbba_gross_cell(2122, 2027)})", 0.5, S_NUM_INPUT, S_NUM),
    ]
    for i, (cid, desc, kind, expected, actual, tol, exp_style, act_style) in enumerate(checks):
        r = c.at()
        if i == 0:
            assert r == _CHECKS_FIRST, f"checks first at {r}, expected {_CHECKS_FIRST}"
        if kind == "text":
            status = f'=IF(E{r}=D{r},{_Q}OK{_Q},{_Q}FAIL{_Q})'
            c.write([cid, desc, expected, actual, "n/a", status],
                    styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, act_style, S_DEFAULT, S_DEFAULT], outline_level=1)
        else:
            status = f'=IF(ABS(F{r})<{tol},{_Q}OK{_Q},{_Q}FAIL{_Q})'
            c.write([cid, desc, expected, actual, f"=E{r}-D{r}", status],
                    styles=[S_DEFAULT, S_DEFAULT, exp_style, act_style, S_NUM, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 Failure detail
    c.banner("§3 - Failure detail", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Any FAIL is a gate stop; the Status column names the failing check."],
            styles=[S_DEFAULT], outline_level=1)

    return WorksheetSpec(worksheet(c.rows, cols=[12, 46, 14, 14, 12, 10],
                         tab_color=group_color(_GROUP), with_gutter=True))


QA_RECONCILIATION = SheetEntry(_TAB, _GROUP, _render_qa_checks)
