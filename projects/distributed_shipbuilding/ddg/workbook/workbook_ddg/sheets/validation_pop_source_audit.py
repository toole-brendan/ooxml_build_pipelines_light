"""validation_pop_source_audit - the "POP Source Audit" tab (DDG, validation group; one module = one sheet).

Confidence + partition audit for the POP corpus. Risk-weighted confirmation,
coverage roll-up over the gated corpus, and the risk ratios + stream partition.

It reads the POP Corpus ranges and owns the coverage/$/partition cells consumed by
Deck Outputs, QA Checks, and Sensitivity.

Promoted accessors:
  coverage_cell, partition_ok_cell, gated_dollar_cell, gfe_excluded_dollar_cell,
  masters_dollar_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LABEL_INDENT_1, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets.data_pop_corpus import (
    gate_range as _g, gfe_excl_range as _x, confirmed_range as _c,
    stream_range as _s, pop_dollar_range as _d, myp_master_range as _m,
)
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "validation"
_TAB = "POP Source Audit"
_NCOLS = 3
_Q = '"'


def _make_pop_audit():
    pos: dict = {}
    c = RowCursor(2)

    def _sp(*masks):
        return f"SUMPRODUCT({'*'.join(masks)})"

    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Confirmation approach
    c.banner("§1 - Confirmation approach (risk-weighted)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    for txt in [
        "Tier 1 - top-$ actions covering ~90-95% of the weighted pool; all $250M+ / $100M+.",
        "Tier 2 - the two MYP masters ($ reconstructed from FPDS + trade press; POP as announced); all AP/EOQ.",
        "Tier 3 - POP not summing ~100% (high unparsed); GFE-suspect; any coefficient-mover.",
        "Confirmed = gated AND in-scope (non-GFE) AND manual_review_status<>unresolved (default 1).",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Coverage
    c.banner("§2 - Coverage (gated corpus, incl. MYP masters)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Actions", "$M"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    inscope = f"{_g()}*(1-{_x()})"
    conf = f"{inscope}*{_c()}"

    def cov(key, label, af, df, ls=S_DEFAULT):
        pos[key] = c.write([label, f"={af}", f"={df}"],
                           styles=[ls, S_NUM, S_NUM], outline_level=1)

    cov("gated", "Gated TAM corpus", _sp(_g()), _sp(_g(), _d()), ls=S_BOLD)
    cov("gfe", "less: GFE / Navy-directed scope", _sp(_g(), _x()), _sp(_g(), _x(), _d()),
        ls=S_LABEL_INDENT_1)
    cov("inscope", "In-scope (non-GFE) gated", _sp(inscope), _sp(inscope, _d()), ls=S_BOLD)
    cov("confirmed", "confirmed", _sp(conf), _sp(conf, _d()), ls=S_LABEL_INDENT_1)
    cov("bc", "of which BC stream", _sp(conf, f'({_s()}={_Q}BC{_Q})'),
        _sp(conf, f'({_s()}={_Q}BC{_Q})', _d()), ls=S_LABEL_INDENT_1)
    cov("masters", "MYP masters (reconstructed)", _sp(_g(), _m()), _sp(_g(), _m(), _d()), ls=S_BOLD)
    cov("disclosed", "Disclosed (excl. masters)", _sp(_g(), f"(1-{_m()})"),
        _sp(_g(), f"(1-{_m()})", _d()))
    c.blank(2)

    # §3 Risk ratios + partition
    c.banner("§3 - Risk ratios + partition", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    pos["coverage"] = c.write(
        ["Confirmation coverage (% of in-scope $)",
         f"=IF(C{pos['inscope']}=0,0,D{pos['confirmed']}/D{pos['inscope']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)
    pos["partition"] = c.write(
        ["Stream partition OK? (every in-scope action is BC)",
         f'=IF(C{pos["bc"]}=C{pos["confirmed"]},{_Q}OK{_Q},{_Q}FAIL{_Q})'],
        styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    pos["myp_share"] = c.write(
        ["MYP masters as % of gated $",
         f"=IF(D{pos['gated']}=0,0,D{pos['masters']}/D{pos['gated']})"],
        styles=[S_DEFAULT, S_PCT], outline_level=1)

    def render() -> WorksheetSpec:
        return WorksheetSpec(worksheet(c.rows, cols=[44, 12, 12],
                             tab_color=group_color(_GROUP), with_gutter=True))

    def coverage_cell() -> str:            return f"'{_TAB}'!C{pos['coverage']}"
    def partition_ok_cell() -> str:        return f"'{_TAB}'!C{pos['partition']}"
    def gated_dollar_cell() -> str:        return f"'{_TAB}'!D{pos['gated']}"
    def gfe_excluded_dollar_cell() -> str: return f"'{_TAB}'!D{pos['gfe']}"
    def masters_dollar_cell() -> str:      return f"'{_TAB}'!D{pos['masters']}"

    return (SheetEntry(_TAB, _GROUP, render),
            coverage_cell, partition_ok_cell, gated_dollar_cell,
            gfe_excluded_dollar_cell, masters_dollar_cell)


(POP_SOURCE_AUDIT, coverage_cell, partition_ok_cell, gated_dollar_cell,
 gfe_excluded_dollar_cell, masters_dollar_cell) = _make_pop_audit()
