"""validation_pop_source_audit - the "POP Source Audit" tab (one module = one sheet).

The risk-weighted manual-confirmation audit of the POP corpus: coverage summary,
risk ratios, and the top-$ action register. Reads the POP corpus ranges (and the
gated-row register) from pop_location_parse; its own coverage / partition / unparsed
/ concentration figures are computed in-sheet.

Confirmation protocol (kept here in source, not as cell prose):
  - Tier 1 - top-$ actions covering ~90-95% of the weighted pool; all $250M+; all $100M+.
  - Tier 2 - redacted / missing-$; all MYP masters; all AP/LLTM / EOQ actions.
  - Tier 3 - POP not summing ~100% (unparsed >1-2%); GFE / SIB-suspect; any coefficient-mover.
  - Confirmed rows = gated AND in-scope (non-GFE) AND manual_review_status<>unresolved.

Promoted accessors (consumed by Methodology & Scope, Figure Register, QA): coverage,
partition_ok, gated_dollar, gfe_excluded_dollar (names unchanged from corpus_sheets).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT, S_LINK_NUM,
    S_LINK_PCT, S_LABEL_INDENT_1, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines import data_pop_corpus as _pop
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "validation"
_TAB = "Sub POP Source Audit"
_BASE = 15                              # title(2) + blank + §1 at-a-glance(4-12) + 2 blanks
_N_TOP = 10


def _build_pop_source_audit(tab: str, base: int, pop):
    _g, _x, _c, _s = pop["gate_range"], pop["gfe_excl_range"], pop["confirmed_range"], pop["stream_range"]
    _dol, _p, _grow = pop["pop_dollar_range"], pop["pct_range"], pop["gated_row_cell"]

    def _sp(*m): return f"SUMPRODUCT({'*'.join(m)})"

    R = {}
    c = RowCursor(base)

    # §2 Confirmation coverage
    c.banner("§2 - Confirmation coverage (gated corpus)", n_cols=7,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric", "Actions", "$M"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    inscope = f"{_g()}*(1-{_x()})"
    conf = f"{inscope}*{_c()}"

    def cov(key, label, af, df, bold=False, indent=False):
        lab = S_LABEL_INDENT_1 if indent else (S_BOLD if bold else S_DEFAULT)
        R[key] = c.write([label, f"={af}", f"={df}"],
                         styles=[lab, S_NUM, S_NUM], outline_level=1)

    cov("gated", "Gated TAM corpus", _sp(_g()), _sp(_g(), _dol()), bold=True)
    cov("gfe", "less: GFE / excluded", _sp(_g(), _x()), _sp(_g(), _x(), _dol()),
        indent=True)
    cov("inscope", "In-scope (non-GFE)", _sp(inscope), _sp(inscope, _dol()),
        bold=True)
    cov("confirmed", "confirmed", _sp(conf), _sp(conf, _dol()),
        indent=True)
    cov("unresolved", "unresolved", _sp(inscope, f"(1-{_c()})"),
        _sp(inscope, f"(1-{_c()})", _dol()), indent=True)
    cov("bc", "BC stream (confirmed)", _sp(conf, f'({_s()}="BC")'),
        _sp(conf, f'({_s()}="BC")', _dol()))
    cov("ap", "AP/LLTM (confirmed)", _sp(conf, f'({_s()}="AP_LLTM")'),
        _sp(conf, f'({_s()}="AP_LLTM")', _dol()))
    cov("redacted", "Redacted / missing-$", _sp(_g(), f"({_dol()}=0)"),
        _sp(_g(), f"({_dol()}=0)", _dol()))
    c.blank()

    # §2a Risk ratios
    c.banner("§2a - Risk ratios", n_cols=7, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Ratio", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])

    def _gd(): return f"D{R['gated']}"

    def ratio(key, label, vf):
        R[key] = c.write([label, f"={vf}"], styles=[S_DEFAULT, S_PCT],
                         outline_level=1)

    ratio("coverage", "Confirmation coverage", f"D{R['confirmed']}/D{R['inscope']}")
    _unp = f"(1-{_p('eb')}-{_p('hii')}-{_p('other')}-{_p('foreign')})"
    ratio("unparsed", "Unparsed share (gated)", f"{_sp(_g(), _dol(), _unp)}/{_gd()}")
    ratio("concentration", "Largest-action conc.", f"{_grow(0, 'dollar')}/{_gd()}")
    R["partition"] = c.write(
        ["Stream partition check",
         f'=IF(ABS(D{R["confirmed"]}-(D{R["bc"]}+D{R["ap"]}))<0.1,"OK","FAIL")'],
        styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank()

    # §2b High-$ action register
    c.banner(f"§2b - High-$ action register (top {_N_TOP} by $, Tier-1 confirmed)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Rank", "PIID", "Program", "$M", "Stream", "Scope Class", "Conf"],
            styles=[S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER,
                    S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_CENTER])
    for i in range(_N_TOP):
        c.write([i + 1, f"={_grow(i, 'piid')}", f"={_grow(i, 'program')}", f"={_grow(i, 'dollar')}",
                 f"={_grow(i, 'stream')}", f"={_grow(i, 'scope_class')}", f"={_grow(i, 'confirmed')}"],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT, S_LINK_NUM, S_DEFAULT, S_DEFAULT, S_LINK_NUM],
                outline_level=1)

    acc = dict(
        coverage_cell=lambda: f"'{tab}'!C{R['coverage']}",
        partition_ok_cell=lambda: f"'{tab}'!C{R['partition']}",
        gated_dollar_cell=lambda: f"'{tab}'!D{R['gated']}",
        gfe_excluded_dollar_cell=lambda: f"'{tab}'!D{R['gfe']}",
        inscope_dollar_cell=lambda: f"'{tab}'!D{R['inscope']}",
        unparsed_share_cell=lambda: f"'{tab}'!C{R['unparsed']}",
        concentration_cell=lambda: f"'{tab}'!C{R['concentration']}")
    return c.rows, c.at(), acc


# ── Layout pass: audit first (promotes accessors), at-a-glance wraps it ──────
_pop_acc = dict(
    gate_range=_pop.gate_range, gfe_excl_range=_pop.gfe_excl_range,
    confirmed_range=_pop.confirmed_range, stream_range=_pop.stream_range,
    pop_dollar_range=_pop.pop_dollar_range, pct_range=_pop.pct_range,
    gated_row_cell=_pop.gated_row_cell)
_rows, _after, _acc = _build_pop_source_audit(_TAB, _BASE, _pop_acc)

coverage_cell = _acc["coverage_cell"]; partition_ok_cell = _acc["partition_ok_cell"]
gated_dollar_cell = _acc["gated_dollar_cell"]; gfe_excluded_dollar_cell = _acc["gfe_excluded_dollar_cell"]
_inscope_dollar_cell = _acc["inscope_dollar_cell"]; _unparsed_share_cell = _acc["unparsed_share_cell"]
_concentration_cell = _acc["concentration_cell"]


def _render_pop_source_audit() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner("POP Source Audit", n_cols=7, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Confirmation & risk", n_cols=7, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value", "Status / note"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    c.write(["Gated TAM corpus $M", f"={gated_dollar_cell()}", "the gated POP pool"],
            styles=[S_BOLD, S_NUM, S_DEFAULT])
    c.write(["In-scope non-GFE $M", f"={_inscope_dollar_cell()}", "coefficient corpus"],
            styles=[S_DEFAULT, S_NUM, S_DEFAULT])
    c.write(["Confirmation coverage", f"={coverage_cell()}", "% of in-scope $; target ~90%+"],
            styles=[S_BOLD, S_PCT, S_DEFAULT])
    c.write(["Unparsed share (gated)", f"={_unparsed_share_cell()}", ">1-2% warrants review"],
            styles=[S_DEFAULT, S_PCT, S_DEFAULT])
    c.write(["Largest-action concentration", f"={_concentration_cell()}", "top action / gated pool"],
            styles=[S_DEFAULT, S_PCT, S_DEFAULT])
    c.write(["Stream partition check", f"={partition_ok_cell()}", "in-scope conf = BC + AP"],
            styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)

    ws = worksheet(c.rows, cols=[34, 14, 14, 30, 14, 14, 12],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


POP_SOURCE_AUDIT = SheetEntry(_TAB, _GROUP, _render_pop_source_audit)
