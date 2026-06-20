"""validation_qa_reconciliation - the "QA Reconciliation" tab (one module = one sheet).

The official audit gate: core invariant checks across the corpus, the TAM/SAM
identities, the exclusions, and the audit chain. Imports the producer cells it
checks from across the workbook (TAM Build, POP Source Audit, Assumptions &
Controls, SAM Build, SIB Excluded, Number Audit, LLTM AP, OBBBA Mandatory).
Produces status_range.

QA-16 is the OBBBA double-count tripwire: the Virginia FY26 Total Ship Estimate is
pinned to the PB2027 one-boat value. If a future budget-book refresh (PB2028+)
restates FY26 to include the Sec. 20002(16) reconciliation boat, the check FAILs
and the OBBBA overlay must be zeroed or re-based before the model is read.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_PCT_INPUT, S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.model_tam_build import (
    anchor_ok_cell, va_bc_supplier_coeff_cell, cumulative_obbba_base_cell,
    cumulative_obbba_tam_cell, portfolio_obbba_base_cell,
)
from workbook_submarines.sheets.data_obbba_funding import (
    obbba_gross_total_cell, obbba_capacity_total_cell,
)
from workbook_submarines.sheets.data_scn_budget import scn_cell as _scn
from workbook_submarines.sheets.data_deflators import deflator_factor_cell
from workbook_submarines.sheets.inputs_assumptions import (
    obbba_bc_share_cell, obbba_spillover_cell,
)
from workbook_submarines.sheets.validation_pop_source_audit import (
    partition_ok_cell, coverage_cell, gfe_excluded_dollar_cell,
)
from workbook_submarines.sheets.model_sam_build import (
    portfolio_tam_cell, bucketed_total_cell, sam_cell, unbucketed_tam_cell,
    va_modeled_share_total_cell, col_modeled_share_total_cell,
)
from workbook_submarines.sheets.validation_sib_excluded import sib_total_cell
from workbook_submarines.sheets.validation_number_audit import fail_count_formula
from workbook_submarines.sheets.data_ap_bridge import ap_bridge_base_cell
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "validation"
_TAB = "QA Reconciliation"
_BASE = 10                                       # title(2) + blank + §1 at-a-glance(4-7) + 2 blanks
_SIB_ANCHOR = 4251.8
_GFE_ANCHOR = 1283.0
_NUCLEAR_GFE_ANCHOR = 4813.6
_OBBBA_GROSS_ANCHOR = 4600.0
_OBBBA_CAPACITY_ANCHOR = 2900.0
_VA_FY26_TSE_ANCHOR = 5389.109


def _build_qa(tab: str, base: int):
    port = portfolio_tam_cell()
    checks = [
        ("QA-01", "Anchor regression holds", "text", "OK", f"={anchor_ok_cell()}", None, S_DEFAULT, S_DEFAULT),
        ("QA-02", "POP partition: in-scope = BC or AP/LLTM", "text", "OK", f"={partition_ok_cell()}", None, S_DEFAULT, S_DEFAULT),
        ("QA-03", "Confirmation coverage = 100%", "num", 1.0, f"={coverage_cell()}", 0.001, S_PCT_INPUT, S_LINK_PCT),
        ("QA-04", "Virginia modeled shares sum to 100% (window vector)", "num", 1.0, f"={va_modeled_share_total_cell()}", 0.001, S_PCT_INPUT, S_LINK_PCT),
        ("QA-04b", "Columbia modeled shares sum to 100% (window vector)", "num", 1.0, f"={col_modeled_share_total_cell()}", 0.001, S_PCT_INPUT, S_LINK_PCT),
        ("QA-05", "Bucketed TAM = portfolio TAM", "num", f"={port}", f"={bucketed_total_cell()}", 0.5, S_LINK_NUM, S_LINK_NUM),
        ("QA-06", "Bucketed TAM <= TAM", "num", 1, f"=IF({bucketed_total_cell()}<={port}+0.5,1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-07", "Broad SAM <= TAM", "num", 1, f"=IF({sam_cell('broad')}<={port}+0.5,1,0)", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-08", "Broad SAM = TAM - unbucketed", "num", f"={port}-{unbucketed_tam_cell()}", f"={sam_cell('broad')}", 0.5, S_NUM, S_LINK_NUM),
        ("QA-09", "SIB exclusion ties to $4,251.8M", "num", _SIB_ANCHOR, f"={sib_total_cell()}", 0.5, S_NUM_INPUT, S_LINK_NUM),
        ("QA-10", "GFE + nuclear LLTM out of corpus", "num", _GFE_ANCHOR + _NUCLEAR_GFE_ANCHOR, f"={gfe_excluded_dollar_cell()}", 2.0, S_NUM_INPUT, S_LINK_NUM),
        ("QA-11", "Number Audit: 0 FAILs", "num", 0, f"={fail_count_formula()}", 0.5, S_NUM_INPUT, S_NUM),
        ("QA-12", "AP/LLTM additive base = 0", "num", 0, f"={ap_bridge_base_cell()}", 0.5, S_NUM_INPUT, S_LINK_NUM),
        ("QA-13", "OBBBA gross award ties to Sec. 20002(16) ($4,600.0M FY26)", "num", _OBBBA_GROSS_ANCHOR,
         f"={obbba_gross_total_cell()}", 0.5, S_NUM_INPUT, S_LINK_NUM),
        ("QA-14", "OBBBA TAM = OBBBA BC base x Virginia class coeff", "num",
         f"={cumulative_obbba_base_cell()}*{va_bc_supplier_coeff_cell()}",
         f"={cumulative_obbba_tam_cell()}", 0.5, S_NUM, S_LINK_NUM),
        ("QA-15", "OBBBA FY27 base = gross x share x spillover", "num",
         f"={obbba_gross_total_cell()}*{obbba_bc_share_cell()}*{obbba_spillover_cell()}*{deflator_factor_cell(2027)}",
         f"={portfolio_obbba_base_cell(2027)}", 0.5, S_NUM, S_NUM),
        ("QA-16", "Virginia FY26 TSE ties to PB2027 one-boat value (no restatement)", "num",
         _VA_FY26_TSE_ANCHOR, f"={_scn(2013, 2026, 'total')}", 1.0, S_NUM_INPUT, S_LINK_NUM),
        ("QA-17", "OBBBA capacity memo ties to $2,900.0M", "num", _OBBBA_CAPACITY_ANCHOR,
         f"={obbba_capacity_total_cell()}", 0.5, S_NUM_INPUT, S_LINK_NUM),
    ]
    c = RowCursor(base)
    c.banner("§2 - Core invariant checks (gate: all OK + Number Audit 0 FAIL)", n_cols=6,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Description", "Expected", "Actual", "Delta", "Status"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_LEFT])
    first = c.at()
    for cid, desc, kind, expected, actual, tol, exp_style, act_style in checks:
        if kind == "text":
            c.write([cid, desc, expected, actual, "n/a", lambda r: f'=IF(E{r}=D{r},"OK","FAIL")'],
                    styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, act_style, S_DEFAULT, S_DEFAULT], outline_level=1)
        else:
            c.write([cid, desc, expected, actual, lambda r: f"=E{r}-D{r}",
                     lambda r, t=tol: f'=IF(ABS(F{r})<{t},"OK","FAIL")'],
                    styles=[S_DEFAULT, S_DEFAULT, exp_style, act_style, S_NUM, S_DEFAULT], outline_level=1)
    last = c.at() - 1

    return c.rows, c.at(), dict(status_range=lambda: f"'{tab}'!G{first}:G{last}")


# ── Layout pass: checks first (promotes status_range), then at-a-glance ─────
_rows, _after, _acc = _build_qa(_TAB, _BASE)
status_range = _acc["status_range"]


def fail_count_qa_formula(): return f'COUNTIF({status_range()},"FAIL")'


def _render_qa() -> WorksheetSpec:
    n_cols = 6
    c = RowCursor(2)
    c.banner("QA Reconciliation", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Audit gate", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value", "Target"], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["QA FAIL count", f"={fail_count_qa_formula()}", "0 = all invariants hold"],
            styles=[S_BOLD, S_NUM, S_DEFAULT])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    return WorksheetSpec(worksheet(c.rows, cols=[10, 40, 14, 14, 12, 10],
                         tab_color=group_color(_GROUP), with_gutter=True))


QA_RECONCILIATION = SheetEntry(_TAB, _GROUP, _render_qa)
