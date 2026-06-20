"""model_tam_build - the "TAM Build" tab (one module = one sheet).

The TAM engine: Budget Normalized (stream bases per class/FY) +
POP Coefficients (per-stream supplier coefficients) + the portfolio TAM bridge +
annualization, behind a headline at-a-glance and followed by a local checks block.
Three stream bases: BC (P-5c, the headline), AP/LLTM (reference; base = 0), and
OBBBA mandatory (the Sec. 20002(16) BC base from the OBBBA Mandatory tab).
The OBBBA boat is a Virginia, so the OBBBA base rides the Virginia class
coefficient - no separate coefficient.

Applied BC coefficients are CLASS-VINTAGE: each class's funding construction
master's announced POP (Assumptions §5 - Virginia Block V 34%, Columbia Build I
22%). The pooled corpus measure stays in §3a as a reference.

Stream include-toggles and the fiscal-year count are pulled from Assumptions &
Controls (the single edit surface); the stream bases link from SCN Annual; the
corpus coefficients are computed over the POP Location Parse ranges. Each section is built
at import time via a cursor, so promoted accessors (cumulative_tam_cell,
tam_total_cell, bc_supplier_coeff_cell, ...) resolve from captured row positions.
FY_COLUMNS is exported (consumed by the register / validation tabs).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_LINK_NUM, S_LINK_PCT, S_PCT, S_PCT_INPUT, S_TITLE_SHEET, S_TITLE_SECTION,
    S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.data_scn_budget import scn_cell as _scn
from workbook_submarines.sheets.inputs_assumptions import (
    ap_lltm_base_cell as _ap_plc, include_bc_stream_cell, include_ap_lltm_stream_cell,
    include_obbba_stream_cell, n_years_count_formula,
    vintage_master_pop_cell as _vm,
)
from workbook_submarines.sheets.data_obbba_funding import obbba_bc_base_cell as _obbba_plc
from workbook_submarines.sheets.data_pop_corpus import (
    gate_range as _g, gfe_excl_range as _x, confirmed_range as _c,
    stream_range as _s, pop_dollar_range as _d, pct_range as _p,
)
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "model"
_TAB = "TAM Build"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_BN_BASE = 15                                   # title(2) + blank + §1 at-a-glance(4-12) + 2 blanks


def _fyc(fy): return col_letter(2 + _FY.index(fy))


# ── §2 Budget normalized ────────────────────────────────────────────────────

def _build_budget_normalized(tab: str, base: int):
    n_cols = 1 + len(_FY)
    fy_hdr = [S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY)
    INCL_BC, INCL_AP = include_bc_stream_cell(), include_ap_lltm_stream_cell()
    INCL_OBBBA = include_obbba_stream_cell()
    pos = {}
    c = RowCursor(base)

    c.banner("§2 - Budget normalized (TAM stream bases per class/FY)", n_cols,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - Applied stream toggles (1 = include)", n_cols,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Toggle", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Include BC stream", f"={INCL_BC}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["Include AP/LLTM stream", f"={INCL_AP}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["Include OBBBA mandatory (Sec. 20002(16))", f"={INCL_OBBBA}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.blank()

    def _class_block(li, letter, ship):
        c.banner(f"§2{letter} - {ship} stream bases ($M, FY22-27)", n_cols,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Metric"] + list(_FY), styles=fy_hdr)
        bc_raw = c.write(["BC base (P-5c Basic Construction)"] + [f"={_scn(li, fy, 'basic')}" for fy in _FY],
                         styles=[S_BOLD] + [S_LINK_NUM] * len(_FY), outline_level=1)
        ap_raw = c.write(["AP/LLTM base (P-10, confirmed 0)"] + [f"={_ap_plc(li, fy)}" for fy in _FY],
                         styles=[S_BOLD] + [S_LINK_NUM] * len(_FY), outline_level=1)
        credit = c.write(["Less: prior-yr AP credit"] + [0] * len(_FY),
                         styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY), outline_level=1)
        obbba_raw = c.write(["OBBBA mandatory BC base (Sec. 20002(16))"] + [f"={_obbba_plc(li, fy)}" for fy in _FY],
                            styles=[S_BOLD] + [S_LINK_NUM] * len(_FY), outline_level=1)
        bc_in = c.write(["BC base in TAM"]
                        + [f'=IF({_fyc(fy)}{bc_raw}=0,"",{INCL_BC}*{_fyc(fy)}{bc_raw})' for fy in _FY],
                        styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        ap_in = c.write(["AP/LLTM base in TAM"]
                        + [f'=IF({_fyc(fy)}{ap_raw}=0,"",{INCL_AP}*({_fyc(fy)}{ap_raw}-{_fyc(fy)}{credit}))' for fy in _FY],
                        styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        obbba_in = c.write(["OBBBA base in TAM"]
                           + [f'=IF(N({_fyc(fy)}{obbba_raw})=0,"",{INCL_OBBBA}*{_fyc(fy)}{obbba_raw})' for fy in _FY],
                           styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        tam = c.write(["TAM base (BC + AP/LLTM + OBBBA)"]
                      + [f"=N({_fyc(fy)}{bc_in})+N({_fyc(fy)}{ap_in})+N({_fyc(fy)}{obbba_in})" for fy in _FY],
                      styles=[S_BOLD] + [S_NUM] * len(_FY), outline_level=1)
        pos[(li, "bc_in_tam")] = bc_in
        pos[(li, "ap_in_tam")] = ap_in
        pos[(li, "obbba_in_tam")] = obbba_in
        pos[(li, "tam_base")] = tam
        c.blank()

    _class_block(2013, "b", "Virginia (LI 2013)")
    _class_block(1045, "c", "Columbia (LI 1045)")

    c.banner("§2d - Portfolio stream-base totals (Va + Col)", n_cols,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY), styles=fy_hdr)
    for label, metric, bold in [("BC base in TAM", "bc_in_tam", False),
                                ("AP/LLTM base in TAM", "ap_in_tam", False),
                                ("OBBBA base in TAM", "obbba_in_tam", False),
                                ("TAM base", "tam_base", True)]:
        vals = [label] + [f"=N({_fyc(fy)}{pos[(2013, metric)]})+N({_fyc(fy)}{pos[(1045, metric)]})" for fy in _FY]
        r = c.write(vals, styles=[S_BOLD if bold else S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        if metric == "bc_in_tam":
            pos["port_bc"] = r
        elif metric == "obbba_in_tam":
            pos["port_obbba"] = r

    def _check(li, fy):
        if li not in (2013, 1045):
            raise ValueError(f"Unknown LI {li!r}")
        if fy not in _FY:
            raise ValueError(f"FY {fy!r} outside {_FY!r}")

    def bc_base_cell(li, fy):
        _check(li, fy); return f"'{tab}'!{_fyc(fy)}{pos[(li, 'bc_in_tam')]}"

    def ap_lltm_base_cell(li, fy):
        _check(li, fy); return f"'{tab}'!{_fyc(fy)}{pos[(li, 'ap_in_tam')]}"

    def obbba_base_cell(li, fy):
        _check(li, fy); return f"'{tab}'!{_fyc(fy)}{pos[(li, 'obbba_in_tam')]}"

    def tam_base_cell(li, fy):
        _check(li, fy); return f"'{tab}'!{_fyc(fy)}{pos[(li, 'tam_base')]}"

    def portfolio_bc_base_cell(fy):
        if fy not in _FY:
            raise ValueError(f"FY {fy!r} outside {_FY!r}")
        return f"'{tab}'!{_fyc(fy)}{pos['port_bc']}"

    def portfolio_obbba_base_cell(fy):
        if fy not in _FY:
            raise ValueError(f"FY {fy!r} outside {_FY!r}")
        return f"'{tab}'!{_fyc(fy)}{pos['port_obbba']}"

    acc = dict(bc_base_cell=bc_base_cell, ap_lltm_base_cell=ap_lltm_base_cell,
               obbba_base_cell=obbba_base_cell, tam_base_cell=tam_base_cell,
               portfolio_bc_base_cell=portfolio_bc_base_cell,
               portfolio_obbba_base_cell=portfolio_obbba_base_cell)
    return c.rows, c.at(), acc


# ── §3 POP coefficients ─────────────────────────────────────────────────────

def _build_pop_coefficients(tab: str, base: int):
    R = {}
    c = RowCursor(base)

    _GATED = _g()
    _INSCOPE = f"{_g()}*(1-{_x()})*{_c()}"
    _BC = f'{_INSCOPE}*({_s()}="BC")'
    _AP = f'{_INSCOPE}*({_s()}="AP_LLTM")'
    _BC_INCLGFE = f'{_g()}*({_s()}="BC")'
    _GFEEXCL = f"{_g()}*(1-{_x()})"

    def _cell(key): return f"C{R[key]}"

    def _coeff(mask):
        den = f"SUMPRODUCT({mask}*{_d()})"
        num = f'SUMPRODUCT({mask}*{_d()}*({_p("other")}+{_p("foreign")}))'
        return f'=IF({den}=0,"",{num}/{den})'

    def _share(which, mask=_GATED):
        den = f"SUMPRODUCT({mask}*{_d()})"
        return f'=IF({den}=0,"",SUMPRODUCT({mask}*{_d()}*{_p(which)})/{den})'

    def line(key, label, value, basis="", ls=S_DEFAULT, vs=S_PCT):
        R[key] = c.write([label, value], styles=[ls, vs], outline_level=1)

    hdr = [S_HEADER_LEFT, S_HEADER_CENTER]
    c.banner("§3 - POP coefficients (per-stream TAM supplier coefficients)", n_cols=7,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§3a - Supplier coefficients (class-vintage applied; corpus measures reference)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coefficient", "Value"], styles=hdr)
    # Applied coefficients = each class's funding construction master's announced POP
    # (other-US + foreign), from Assumptions §5. The pooled corpus measure stays below
    # as a reference (it rests on the small disclosed BC-stream slice; the masters
    # predate the corpus window).
    line("bc_va", "Virginia BC coefficient (Block V announced POP; applied)",
         f"=N({_vm('va', 'other_us')})+N({_vm('va', 'foreign')})", ls=S_BOLD)
    line("bc_col", "Columbia BC coefficient (Build I announced POP; applied)",
         f"=N({_vm('col', 'other_us')})+N({_vm('col', 'foreign')})", ls=S_BOLD)
    line("bc", "Pooled corpus BC coefficient (reference; not applied)", _coeff(_BC),
         "construction + component_procurement; GFE + BPMI nuclear dropped (~35.0%)")
    line("ap", "AP/LLTM coefficient (reference; base = 0)", _coeff(_AP),
         "lltm + advance_procurement (~48.5%; not applied)", ls=S_BOLD)
    line("total", "Total weighted (corpus, display)", _coeff(_INSCOPE),
         "both streams, in-scope confirmed - not base-weighted")
    c.blank()
    c.banner("§3b - All-gated POP shares (dollar-weighted building blocks)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["POP class", "Share"], styles=hdr)
    line("eb", "EB site %", _share("eb"), "prime yard (Groton/Quonset) - not addressable")
    line("hii", "HII site %", _share("hii"), "co-prime (Newport News) - not addressable")
    line("other", "Other-US supplier %", _share("other"), "open supplier market")
    line("foreign", "Foreign %", _share("foreign"), "foreign suppliers")
    line("unparsed", "Unparsed %",
         f'=1-{_cell("eb")}-{_cell("hii")}-{_cell("other")}-{_cell("foreign")}', "single-site / no-% parses")
    c.blank()
    c.banner("§3c - Distributed-production view (appendix; broader than commercial TAM)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coefficient", "Value"], styles=hdr)
    line("dist_conf", "Distributed (confirmed)", f'={_cell("hii")}+{_cell("other")}+{_cell("foreign")}',
         "away from EB yard, confirmed (~68%)", ls=S_BOLD)
    line("dist_unp", "Distributed (incl-unparsed)", f'=1-{_cell("eb")}',
         "away from EB yard incl unparsed (~78%)", ls=S_BOLD)
    c.blank()
    c.banner("§3d - Reconciliation & scope variants (reference; not applied to TAM)", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Variant", "Value"], styles=hdr)
    line("v_bcgfe", "BC stream incl-GFE (handoff ref)", _coeff(_BC_INCLGFE), "GFE left in denominator (~61%)")
    line("v_gfeexcl", "All-gated, GFE-excluded", _coeff(_GFEEXCL), "both streams minus GFE (~54.5%)")
    c.blank()
    c.banner("§3e - Anchor regression", n_cols=7,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Value"], styles=hdr)
    R["anchor_pub"] = c.write(["Published anchor", 0.518],
                              styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    line("anchor_calc", "Computed all-gated primary", _coeff(_GATED), "supplier+foreign over ALL gated")
    line("anchor_delta", "Delta", f'={_cell("anchor_calc")}-{_cell("anchor_pub")}', "computed - published")
    R["anchor_ok"] = c.write(["Anchor OK?", f'=IF(ABS({_cell("anchor_delta")})<0.01,"OK","FAIL")'],
                             styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    acc = dict(
        bc_supplier_coeff_cell=lambda: f"'{tab}'!{_cell('bc')}",
        va_bc_supplier_coeff_cell=lambda: f"'{tab}'!{_cell('bc_va')}",
        col_bc_supplier_coeff_cell=lambda: f"'{tab}'!{_cell('bc_col')}",
        ap_lltm_supplier_coeff_cell=lambda: f"'{tab}'!{_cell('ap')}",
        total_weighted_coeff_cell=lambda: f"'{tab}'!{_cell('total')}",
        distributed_coeff_low_cell=lambda: f"'{tab}'!{_cell('dist_conf')}",
        distributed_coeff_high_cell=lambda: f"'{tab}'!{_cell('dist_unp')}",
        anchor_ok_cell=lambda: f"'{tab}'!{_cell('anchor_ok')}",
        primary_tam_coeff_cell=lambda: f"'{tab}'!{_cell('anchor_calc')}")
    return c.rows, c.at(), acc


# ── §4 TAM bridge (uses bn + pc accessors) ──────────────────────────────────

def _build_tam_model(tab: str, base: int, bn, pc):
    _bc_base, _ap_base, _bn_port_bc = bn["bc_base_cell"], bn["ap_lltm_base_cell"], bn["portfolio_bc_base_cell"]
    _obbba_base, _bn_port_obbba = bn["obbba_base_cell"], bn["portfolio_obbba_base_cell"]
    _bc_va, _bc_col = pc["va_bc_supplier_coeff_cell"], pc["col_bc_supplier_coeff_cell"]
    _ap_coeff = pc["ap_lltm_supplier_coeff_cell"]
    n_cols = 1 + len(_FY)
    fy_hdr = [S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY)
    pos = {}
    c = RowCursor(base)

    c.banner("§4 - TAM bridge", n_cols,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§4a - Applied per-stream supplier coefficients (class-vintage)", n_cols,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coefficient", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    bc_va_row = c.write(["Virginia BC coefficient (Block V announced POP)", f"={_bc_va()}"],
                        styles=[S_BOLD, S_PCT], outline_level=1)
    bc_col_row = c.write(["Columbia BC coefficient (Build I announced POP)", f"={_bc_col()}"],
                         styles=[S_BOLD, S_PCT], outline_level=1)
    ap_coeff_row = c.write(["AP/LLTM coefficient (reference; base = 0)", f"={_ap_coeff()}"],
                           styles=[S_BOLD, S_PCT], outline_level=1)
    BC_COEFF = {2013: f"$C${bc_va_row}", 1045: f"$C${bc_col_row}"}
    AP_COEFF = f"$C${ap_coeff_row}"
    c.blank()

    def _class_block(li, letter, ship):
        c.banner(f"§4{letter} - {ship} TAM ($M, FY22-27)", n_cols,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Metric"] + list(_FY), styles=fy_hdr)
        bc_base_r = c.write(["BC base"] + [f"={_bc_base(li, fy)}" for fy in _FY],
                            styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        tam_bc = c.write(["TAM - BC stream (class coeff)"]
                         + [f'=IF(N({_fyc(fy)}{bc_base_r})=0,"",N({_fyc(fy)}{bc_base_r})*{BC_COEFF[li]})' for fy in _FY],
                         styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        ap_base_r = c.write(["AP/LLTM base"] + [f"={_ap_base(li, fy)}" for fy in _FY],
                            styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        tam_ap = c.write(["TAM - AP/LLTM stream"]
                         + [f'=IF(N({_fyc(fy)}{ap_base_r})=0,"",N({_fyc(fy)}{ap_base_r})*{AP_COEFF})' for fy in _FY],
                         styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        obbba_base_r = c.write(["OBBBA base"] + [f"={_obbba_base(li, fy)}" for fy in _FY],
                               styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        tam_obbba = c.write(["TAM - OBBBA mandatory (class BC coeff)"]
                            + [f'=IF(N({_fyc(fy)}{obbba_base_r})=0,"",N({_fyc(fy)}{obbba_base_r})*{BC_COEFF[li]})' for fy in _FY],
                            styles=[S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
        tam = c.write(["TAM (all streams)"]
                      + [f"=N({_fyc(fy)}{tam_bc})+N({_fyc(fy)}{tam_ap})+N({_fyc(fy)}{tam_obbba})" for fy in _FY],
                      styles=[S_BOLD] + [S_NUM] * len(_FY), outline_level=1)
        pos[(li, "bc_base")] = bc_base_r
        pos[(li, "ap_base")] = ap_base_r
        pos[(li, "obbba_base")] = obbba_base_r
        pos[(li, "tam_bc")] = tam_bc
        pos[(li, "tam_ap")] = tam_ap
        pos[(li, "tam_obbba")] = tam_obbba
        pos[(li, "tam")] = tam
        c.blank()

    _class_block(2013, "b", "Virginia (LI 2013)")
    _class_block(1045, "c", "Columbia (LI 1045)")

    c.banner("§4d - Portfolio TAM + stream bridge (Virginia + Columbia)", n_cols,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY), styles=fy_hdr)
    for label, metric, bold, key in [("BC stream TAM", "tam_bc", False, "br_bc"),
                                     ("AP/LLTM stream TAM", "tam_ap", False, "br_ap"),
                                     ("OBBBA mandatory TAM", "tam_obbba", False, "br_obbba"),
                                     ("TAM (portfolio)", "tam", True, "br_tam")]:
        vals = [label] + [f"=N({_fyc(fy)}{pos[(2013, metric)]})+N({_fyc(fy)}{pos[(1045, metric)]})" for fy in _FY]
        pos[key] = c.write(vals, styles=[S_BOLD if bold else S_DEFAULT] + [S_NUM] * len(_FY), outline_level=1)
    br = pos["br_tam"]
    last = _fyc(_FY[-1])
    num = f"SUM(C{br}:{last}{br})"
    base_rows = [pos[(2013, "bc_base")], pos[(2013, "ap_base")], pos[(2013, "obbba_base")],
                 pos[(1045, "bc_base")], pos[(1045, "ap_base")], pos[(1045, "obbba_base")]]
    denom = "+".join(f"SUM(C{r}:{last}{r})" for r in base_rows)
    pos["tw_coeff"] = c.write(["Total weighted coefficient (TAM / TAM base, all FY)",
                               f'=IF(({denom})=0,"",{num}/({denom}))'],
                              styles=[S_BOLD, S_PCT], outline_level=1)
    c.blank()

    c.banner("§4e - Annualization + deck-bridge figures (FY22-27)", n_cols,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c_first = _fyc(_FY[0])
    pos["cumulative"] = c.write(["Cumulative portfolio TAM (FY22-27)", f"=SUM({c_first}{br}:{last}{br})"],
                                styles=[S_BOLD, S_NUM], outline_level=1)
    pos["n_years"] = c.write(["Number of fiscal years", f"={n_years_count_formula()}"],
                             styles=[S_DEFAULT, S_NUM], outline_level=1)
    pos["avg"] = c.write(["Average annual portfolio TAM", f"=C{pos['cumulative']}/C{pos['n_years']}"],
                         styles=[S_BOLD, S_NUM], outline_level=1)
    bc_base_sum = "+".join(f"N({_bn_port_bc(fy)})" for fy in _FY)
    pos["cum_bc"] = c.write(["Cumulative BC construction base (FY22-27)", f"={bc_base_sum}"],
                            styles=[S_DEFAULT, S_NUM], outline_level=1)
    obbba_base_sum = "+".join(f"N({_bn_port_obbba(fy)})" for fy in _FY)
    pos["cum_obbba_base"] = c.write(["Cumulative OBBBA mandatory BC base (FY22-27)", f"={obbba_base_sum}"],
                                    styles=[S_DEFAULT, S_NUM], outline_level=1)
    pos["cum_obbba_tam"] = c.write(["Cumulative OBBBA mandatory TAM (FY22-27)",
                                    f"=SUM({c_first}{pos['br_obbba']}:{last}{pos['br_obbba']})"],
                                   styles=[S_DEFAULT, S_NUM], outline_level=1)
    pos["removal"] = c.write(["Removed by POP (prime / co-prime / GFE)",
                              f"=C{pos['cum_bc']}+C{pos['cum_obbba_base']}-C{pos['cumulative']}"],
                             styles=[S_DEFAULT, S_NUM], outline_level=1)

    def tam_cell(li, fy):
        if li not in (2013, 1045):
            raise ValueError(f"Unknown LI {li!r}")
        if fy not in _FY:
            raise ValueError(f"FY {fy!r} outside {_FY!r}")
        return f"'{tab}'!{_fyc(fy)}{pos[(li, 'tam')]}"

    def tam_total_cell(fy):
        if fy not in _FY:
            raise ValueError(f"FY {fy!r} outside {_FY!r}")
        return f"'{tab}'!{_fyc(fy)}{pos['br_tam']}"

    acc = dict(
        tam_cell=tam_cell, tam_total_cell=tam_total_cell,
        tam_bc_total_cell=lambda fy: f"'{tab}'!{_fyc(fy)}{pos['br_bc']}",
        tam_ap_total_cell=lambda fy: f"'{tab}'!{_fyc(fy)}{pos['br_ap']}",
        tam_obbba_total_cell=lambda fy: f"'{tab}'!{_fyc(fy)}{pos['br_obbba']}",
        cumulative_tam_cell=lambda: f"'{tab}'!C{pos['cumulative']}",
        n_years_cell=lambda: f"'{tab}'!C{pos['n_years']}",
        avg_annual_tam_cell=lambda: f"'{tab}'!C{pos['avg']}",
        cumulative_bc_base_cell=lambda: f"'{tab}'!C{pos['cum_bc']}",
        cumulative_obbba_base_cell=lambda: f"'{tab}'!C{pos['cum_obbba_base']}",
        cumulative_obbba_tam_cell=lambda: f"'{tab}'!C{pos['cum_obbba_tam']}",
        removal_cell=lambda: f"'{tab}'!C{pos['removal']}",
        tam_bridge_cell=lambda: f"'{tab}'!C{pos['br_tam']}")
    return c.rows, c.at(), acc


# ── Layout pass: stack the three sections, promote accessors ────────────────
_bn_rows, _after_bn, _bn_acc = _build_budget_normalized(_TAB, _BN_BASE)
_PC_BASE = _after_bn + 2
_pc_rows, _after_pc, _pc_acc = _build_pop_coefficients(_TAB, _PC_BASE)
_TM_BASE = _after_pc + 2
_tm_rows, _after_tm, _tm_acc = _build_tam_model(_TAB, _TM_BASE, _bn_acc, _pc_acc)

bc_base_cell = _bn_acc["bc_base_cell"]; ap_lltm_base_cell = _bn_acc["ap_lltm_base_cell"]
obbba_base_cell = _bn_acc["obbba_base_cell"]
tam_base_cell = _bn_acc["tam_base_cell"]; portfolio_bc_base_cell = _bn_acc["portfolio_bc_base_cell"]
portfolio_obbba_base_cell = _bn_acc["portfolio_obbba_base_cell"]
bc_supplier_coeff_cell = _pc_acc["bc_supplier_coeff_cell"]; ap_lltm_supplier_coeff_cell = _pc_acc["ap_lltm_supplier_coeff_cell"]
va_bc_supplier_coeff_cell = _pc_acc["va_bc_supplier_coeff_cell"]
col_bc_supplier_coeff_cell = _pc_acc["col_bc_supplier_coeff_cell"]
total_weighted_coeff_cell = _pc_acc["total_weighted_coeff_cell"]; distributed_coeff_low_cell = _pc_acc["distributed_coeff_low_cell"]
distributed_coeff_high_cell = _pc_acc["distributed_coeff_high_cell"]; anchor_ok_cell = _pc_acc["anchor_ok_cell"]
primary_tam_coeff_cell = _pc_acc["primary_tam_coeff_cell"]
tam_cell = _tm_acc["tam_cell"]; tam_total_cell = _tm_acc["tam_total_cell"]; tam_bc_total_cell = _tm_acc["tam_bc_total_cell"]
tam_ap_total_cell = _tm_acc["tam_ap_total_cell"]; tam_obbba_total_cell = _tm_acc["tam_obbba_total_cell"]
cumulative_tam_cell = _tm_acc["cumulative_tam_cell"]
n_years_cell = _tm_acc["n_years_cell"]; avg_annual_tam_cell = _tm_acc["avg_annual_tam_cell"]
cumulative_bc_base_cell = _tm_acc["cumulative_bc_base_cell"]; removal_cell = _tm_acc["removal_cell"]
cumulative_obbba_base_cell = _tm_acc["cumulative_obbba_base_cell"]
cumulative_obbba_tam_cell = _tm_acc["cumulative_obbba_tam_cell"]
tam_bridge_cell = _tm_acc["tam_bridge_cell"]
FY_COLUMNS = _FY


def _render_tam_build() -> WorksheetSpec:
    n_cols = 7
    c = RowCursor(2)
    c.banner("TAM Build", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Headline TAM", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Cumulative portfolio TAM (FY22-27)", f"={cumulative_tam_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["Average annual portfolio TAM", f"={avg_annual_tam_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["incl. OBBBA mandatory TAM (Sec. 20002(16))", f"={cumulative_obbba_tam_cell()}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Virginia BC coefficient (Block V announced POP)", f"={va_bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_PCT])
    c.write(["Columbia BC coefficient (Build I announced POP)", f"={col_bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_PCT])
    c.write(["AP/LLTM reference coefficient", f"={ap_lltm_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_PCT])
    c.blank(2)

    assert c.at() == _BN_BASE, f"at-a-glance ends at {c.at()}, expected {_BN_BASE}"
    c.feed(_bn_rows, _after_bn)
    c.blank(2)
    c.feed(_pc_rows, _after_pc)
    c.blank(2)
    c.feed(_tm_rows, _after_tm)
    c.blank(2)

    # §5 TAM checks
    c.banner("§5 - TAM checks", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Status"], styles=S_HEADER_LEFT)
    _bc_sum = "+".join(f"N({tam_bc_total_cell(fy)})" for fy in _FY)
    _ap_sum = "+".join(f"N({tam_ap_total_cell(fy)})" for fy in _FY)
    _ob_sum = "+".join(f"N({tam_obbba_total_cell(fy)})" for fy in _FY)
    c.write(["Portfolio TAM = BC TAM + AP/LLTM TAM + OBBBA TAM",
             f'=IF(ABS(({cumulative_tam_cell()})-(({_bc_sum})+({_ap_sum})+({_ob_sum})))<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Average annual = cumulative / fiscal years",
             f'=IF(ABS(({avg_annual_tam_cell()})*({n_years_cell()})-({cumulative_tam_cell()}))<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Anchor regression holds", f"={anchor_ok_cell()}"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    # A PB2028+ refresh that restates FY26 to include the Sec. 20002(16) boat would
    # double-count the OBBBA overlay; this ties FY26 to the PB2027 one-boat value.
    c.write(["Virginia FY26 ship estimate ties to PB2027",
             f'=IF(ABS({_scn(2013, 2026, "total")}-5389.109)<1,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    return WorksheetSpec(worksheet(c.rows, cols=[40, 12, 14, 12, 12, 12, 12],
                         tab_color=group_color(_GROUP), with_gutter=True))


TAM_BUILD = SheetEntry(_TAB, _GROUP, _render_tam_build)
