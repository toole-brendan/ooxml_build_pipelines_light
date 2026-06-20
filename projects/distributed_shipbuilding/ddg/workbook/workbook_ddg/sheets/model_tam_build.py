"""model_tam_build - the "TAM Build" tab (DDG, model group; one module = one sheet).

The TAM calculation engine + audit-readable TAM bridge. Four sections built in
dependency order - §2 Normalized Budget (stream bases) -> §3 Coefficients (per-stream
supplier coefficients) -> §4 MYP correction -> §5 Model (TAM by FY + portfolio +
per-hull) - behind a §1 headline at-a-glance summary.

Stream include-toggles are pulled from Inputs (the single edit surface); the BC base
links from SCN Budget plus the OBBBA Mandatory BC bridge (Sec. 20002(17), toggle-
gated); the coefficients are computed over the POP Corpus ranges.
TAM Build is the TRUE portfolio-TAM producer (the portfolio_tam defined name and the
deck DO-01 source from here, not SAM).

Two-pass layout (mirrors workbook_submarines/tam_build): the four detail blocks are built at
import time (capturing load-bearing rows + promoting accessors); the at-a-glance is
built at render time and asserts it fills the rows reserved before _NB_BASE.

Promoted accessors keep their names; all references resolve to 'TAM Build'.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_PCT, S_PCT_INPUT, S_LINK_NUM, S_LINK_PCT, S_LABEL_INDENT_1,
    S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_ddg.sheets.data_scn_budget import scn_cell as _scn
from workbook_ddg.sheets.data_obbba_funding import obbba_bc_base_cell as _obbba
from workbook_ddg.sheets.data_production_schedule import in_window_hull_count as _hulls
from workbook_ddg.sheets.inputs_assumptions import (
    ap_lltm_base_cell as _cp_ap_base,
    ap_supplier_coeff_cell as _cp_ap_coeff,
    include_bc_stream_cell, include_ap_lltm_stream_cell, include_obbba_stream_cell,
)
from workbook_ddg.sheets.data_pop_corpus import (
    gate_range as _g, gfe_excl_range as _x, confirmed_range as _c,
    stream_range as _s, pop_dollar_range as _d, pct_range as _p,
    myp_master_range as _m,
)
from workbook_ddg.sheets._layout import RowCursor

_GROUP = "model"
_TAB = "TAM Build"
_NCOLS = 8
_LI = 2122
_FY_COLUMNS = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL_INDEX = {fy: 2 + i for i, fy in enumerate(_FY_COLUMNS)}   # C..H
_TOTAL_COL_IDX = 2 + len(_FY_COLUMNS)                            # I
_NB_BASE = 17   # title(2)+blank+§1 at-a-glance(4-14)+2 blanks; body begins at 17


def _fy_col(fy: int) -> str:
    return col_letter(_FY_COL_INDEX[fy])


def _total_col() -> str:
    return col_letter(_TOTAL_COL_IDX)


_LAST_FY_COL = col_letter(_TOTAL_COL_IDX - 1)   # H


def _check(li: int, fy: int) -> None:
    if li != _LI:
        raise ValueError(f"Unknown LI {li!r}; DDG program is {_LI}")
    if fy not in _FY_COL_INDEX:
        raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")


# ════════════════════════ §2 Normalized Budget ════════════════════════════════
def _build_normalized_budget(tab: str, base: int):
    pos: dict = {}
    c = RowCursor(base)
    incl_bc = include_bc_stream_cell()
    incl_ap = include_ap_lltm_stream_cell()
    incl_obbba = include_obbba_stream_cell()

    c.banner("§2 - Normalized budget (stream bases)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - Stream include-in-TAM toggles (1 = include)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Toggle", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Include BC stream", f"={incl_bc}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["Include AP/LLTM stream", f"={incl_ap}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.write(["Include OBBBA mandatory (Sec. 20002(17))", f"={incl_obbba}"],
            styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.blank(2)
    c.banner("§2b - DDG-51 (LI 2122) stream bases ($M, FY22-FY27)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Metric"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    pos["bc_raw"] = c.write(["BC base (P-5c Basic Construction)"]
                            + [f"={_scn(_LI, fy, 'basic')}" for fy in _FY_COLUMNS],
                            styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)
    pos["obbba_raw"] = c.write(["OBBBA mandatory BC base (Sec. 20002(17))"]
                               + [f"={_obbba(_LI, fy)}" for fy in _FY_COLUMNS],
                               styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)
    pos["ap_raw"] = c.write(["AP/LLTM base (P-10 Ship Construction EOQ)"]
                            + [f"={_cp_ap_base(_LI, fy)}" for fy in _FY_COLUMNS],
                            styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)
    pos["credit"] = c.write(["Less: prior-yr AP credit"] + [0] * len(_FY_COLUMNS),
                            styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    bc_in_vals = ["BC base in TAM (P-5c + OBBBA mandatory)"]
    ap_in_vals = ["AP/LLTM base in TAM (EOQ less PY credit)"]
    for fy in _FY_COLUMNS:
        col = _fy_col(fy)
        bc_in_vals.append(f'=IF(N({col}{pos["bc_raw"]})+N({col}{pos["obbba_raw"]})=0,"",'
                          f'{incl_bc}*N({col}{pos["bc_raw"]})'
                          f'+{incl_obbba}*N({col}{pos["obbba_raw"]}))')
        ap_in_vals.append(f'=IF({col}{pos["ap_raw"]}=0,"",'
                          f'{incl_ap}*({col}{pos["ap_raw"]}-{col}{pos["credit"]}))')
    pos["bc_in"] = c.write(bc_in_vals, styles=[S_DEFAULT] + [S_NUM] * len(_FY_COLUMNS), outline_level=1)
    pos["ap_in"] = c.write(ap_in_vals, styles=[S_DEFAULT] + [S_NUM] * len(_FY_COLUMNS), outline_level=1)
    tam_vals = ["TAM base (BC + AP/LLTM)"]
    for fy in _FY_COLUMNS:
        col = _fy_col(fy)
        tam_vals.append(f"=N({col}{pos['bc_in']})+N({col}{pos['ap_in']})")
    pos["tam_base"] = c.write(tam_vals, styles=[S_BOLD] + [S_NUM] * len(_FY_COLUMNS), outline_level=1)

    def bc_base_cell(li, fy):
        _check(li, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['bc_in']}"

    def ap_lltm_base_cell(li, fy):
        _check(li, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['ap_in']}"

    def tam_base_cell(li, fy):
        _check(li, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['tam_base']}"

    return c.rows, c.at(), dict(bc_base_cell=bc_base_cell,
                                ap_lltm_base_cell=ap_lltm_base_cell,
                                tam_base_cell=tam_base_cell)


# ════════════════════════════ §3 Coefficients ════════════════════════════════
def _build_coefficients(tab: str, base: int):
    pos: dict = {}
    c = RowCursor(base)
    _INSCOPE = f"{_g()}*(1-{_x()})*{_c()}"
    _BC = f'{_INSCOPE}*({_s()}="BC")'
    _BC_DISC = f'{_INSCOPE}*({_s()}="BC")*(1-{_m()})'
    _ALLGATED = _g()
    _ALLGATED_DISC = f"{_g()}*(1-{_m()})"

    def _coeff(mask):
        den = f"SUMPRODUCT({mask}*{_d()})"
        num = f'SUMPRODUCT({mask}*{_d()}*({_p("other")}+{_p("foreign")}))'
        return f'=IF({den}=0,"",{num}/{den})'

    def _share(which):
        den = f"SUMPRODUCT({_g()}*{_d()})"
        return f'=IF({den}=0,"",SUMPRODUCT({_g()}*{_d()}*{_p(which)})/{den})'

    def line(key, label, value, basis="", ls=S_DEFAULT, vs=S_PCT):
        pos[key] = c.write([label, value], styles=[ls, vs], outline_level=1)

    c.banner("§3 - Supplier coefficients", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§3a - Per-stream supplier coefficients (feed TAM; $-weighted, gated, non-GFE)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coefficient", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    line("bc", "BC stream coefficient (MYP-corrected; applied FY23-27)", _coeff(_BC),
         "other-US + foreign over non-GFE BC corpus incl. FY23-27 MYP masters", ls=S_BOLD)
    # FY2022 ships were funded under the FY18-22 MYP masters (announced $ AND POP,
    # 2018-09-27 bulletin); their dollar-weighted outside-yards share is the
    # FY2022-vintage coefficient. Computed from Inputs §4; out of the POP corpus.
    from workbook_ddg.sheets.inputs_assumptions import (
        myp_master_cell as _mm, myp_pop_cell as _mp,
    )
    _f22_num = (f"N({_mm('biw18')})*(N({_mp('biw18', 'other_us')})+N({_mp('biw18', 'foreign')}))"
                f"+N({_mm('ingalls18')})*(N({_mp('ingalls18', 'other_us')})+N({_mp('ingalls18', 'foreign')}))")
    _f22_den = f"N({_mm('biw18')})+N({_mm('ingalls18')})"
    line("bc_fy22", "BC coefficient, FY2022 vintage (FY18-22 masters)",
         f"=({_f22_num})/({_f22_den})",
         "announced POP of the FY18-22 masters; applied to FY2022 only", ls=S_BOLD)
    line("ap", "AP/LLTM stream coefficient (assumption)", f"={_cp_ap_coeff()}",
         "Inputs knob - no DDG AP POP corpus to SUMPRODUCT", ls=S_BOLD, vs=S_LINK_PCT)
    line("total", "Total weighted (corpus, display)", _coeff(_INSCOPE),
         "non-GFE in-scope confirmed - NOT base-weighted (see Model)")
    line("bc_disc", "BC stream, disclosed-only (masters excluded)", _coeff(_BC_DISC),
         "MYP masters are ~93% of the BC corpus; excluding them drops the coeff (see Sensitivity)")
    c.blank(2)
    c.banner("§3b - MYP correction - outside-yards POP",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    line("myp_disc", "Outside-yards, disclosed-only (artifact)", _coeff(_ALLGATED_DISC),
         "all-gated, MYP masters EXCLUDED (redaction over-weights GFE) (~87%)", ls=S_BOLD)
    line("myp_corr", "Outside-yards, MYP-corrected", _coeff(_ALLGATED),
         "all-gated, masters folded back at announced POP (~42%)", ls=S_BOLD)
    line("myp_swing", "Swing (disclosed - corrected)", f"=C{pos['myp_disc']}-C{pos['myp_corr']}",
         "the redaction artifact magnitude")
    c.blank(2)
    c.banner("§3c - All-gated POP shares (dollar-weighted, MYP-corrected)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["POP class", "Share"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    line("biw", "BIW site %", _share("biw"), "prime yard (Bath) - not addressable")
    line("ingalls", "Ingalls site %", _share("ingalls"), "co-prime yard - not addressable")
    line("other", "Other-US supplier %", _share("other"), "open supplier market")
    line("foreign", "Foreign %", _share("foreign"), "foreign suppliers")
    line("unparsed", "Unparsed %",
         f"=1-C{pos['biw']}-C{pos['ingalls']}-C{pos['other']}-C{pos['foreign']}",
         "residual (single-site / no-% parses)")
    c.blank(2)
    c.banner("§3d - Distributed-production view (appendix - broader than commercial TAM)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coefficient", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    line("dist_conf", "Distributed (away from BIW)",
         f"=C{pos['ingalls']}+C{pos['other']}+C{pos['foreign']}",
         "away from the Bath yard (incl Ingalls)", ls=S_BOLD)
    line("dist_unp", "Outside both yards (other + foreign)",
         f"=C{pos['other']}+C{pos['foreign']}",
         "the supplier-addressable share (= MYP-corrected outside-yards)", ls=S_BOLD)
    c.blank(2)
    c.banner("§3e - Anchor regression - MYP-corrected outside-yards near ~42%", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    pos["anchor_target"] = c.write(["Target (methodology)", 0.42],
                                   styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    line("anchor_calc", "Computed corrected outside-yards", f"=C{pos['myp_corr']}",
         "the live MYP-corrected figure")
    line("anchor_delta", "Delta", f"=C{pos['anchor_calc']}-C{pos['anchor_target']}", "computed - target")
    pos["anchor_ok"] = c.write(
        ["Anchor OK?", f'=IF(ABS(C{pos["anchor_delta"]})<0.05,"OK","REVIEW")'],
        styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    def _cell(key):
        return lambda: f"'{tab}'!C{pos[key]}"

    return c.rows, c.at(), dict(
        bc_supplier_coeff_cell=_cell("bc"),
        bc_supplier_coeff_fy22_cell=_cell("bc_fy22"),
        bc_supplier_coeff_disclosed_cell=_cell("bc_disc"),
        ap_lltm_supplier_coeff_cell=_cell("ap"),
        total_weighted_coeff_cell=_cell("total"),
        outside_yards_disclosed_cell=_cell("myp_disc"),
        outside_yards_corrected_cell=_cell("myp_corr"),
        anchor_ok_cell=_cell("anchor_ok"),
        # §3c all-gated, MYP-corrected POP site shares (deck CD04 distribution)
        biw_pop_share_cell=_cell("biw"),
        ingalls_pop_share_cell=_cell("ingalls"),
        other_pop_share_cell=_cell("other"),
        foreign_pop_share_cell=_cell("foreign"),
        unparsed_pop_share_cell=_cell("unparsed"),
    )


# ════════════════════════════ §4 MYP correction ══════════════════════════════
def _build_myp(tab: str, base: int, co: dict):
    from workbook_ddg.sheets.inputs_assumptions import myp_master_cell, myp_pop_cell
    pos: dict = {}
    c = RowCursor(base)
    out_disc = co["outside_yards_disclosed_cell"]
    out_corr = co["outside_yards_corrected_cell"]

    c.banner("§4 - MYP correction", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§4a - MYP master awards ($-redacted; announced POP)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Master", "PIID", "Master $M", "BIW %", "Ingalls %", "Other-US + Foreign %"],
            styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_CENTER] * 4)
    for label, piid, yard in [("BIW MYP", "N00024-23-C-2305", "biw"),
                              ("Ingalls MYP", "N00024-23-C-2307", "ingalls")]:
        outsh = f"=N({myp_pop_cell(yard, 'other_us')})+N({myp_pop_cell(yard, 'foreign')})"
        c.write([label, piid, f"={myp_master_cell(yard)}", f"={myp_pop_cell(yard, 'biw')}",
                 f"={myp_pop_cell(yard, 'ingalls')}", outsh],
                styles=[S_BOLD, S_DEFAULT, S_LINK_NUM, S_LINK_PCT, S_LINK_PCT, S_PCT],
                outline_level=1)
    c.write(["Combined master $M", "",
             f"=N({myp_master_cell('biw')})+N({myp_master_cell('ingalls')})", "", "", ""],
            styles=[S_BOLD, S_DEFAULT, S_NUM, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)
    c.banner("§4b - Outside-yards POP - disclosed artifact vs MYP-corrected", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    r_disc = c.write(["Disclosed-only (artifact)", f"={out_disc()}"],
                     styles=[S_BOLD, S_PCT], outline_level=1)
    r_corr = c.write(["MYP-corrected", f"={out_corr()}"],
                     styles=[S_BOLD, S_PCT], outline_level=1)
    pos["swing"] = c.write(["Swing (artifact - corrected)", f"=C{r_disc}-C{r_corr}"],
                           styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank(2)
    c.banner("§4c - Guardrail", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    for txt in [
        "Travel the POP-coefficient numbers together: disclosed artifact -> MYP-corrected outside-yards -> applied BC coefficient.",
        "Recovery basis: FPDS obligatedAmount + trade-press totals (USNI / Defense Daily).",
        "Per-hull allocation within a master PIID is not disclosed; the masters carry the bulletins' announced contract-level POP split.",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)

    def myp_swing_cell():
        return f"'{tab}'!C{pos['swing']}"

    return c.rows, c.at(), dict(
        myp_swing_cell=myp_swing_cell)


# ════════════════════════════ §5 Model (TAM by FY) ═══════════════════════════
def _build_model(tab: str, base: int, nb: dict, co: dict):
    pos: dict = {}
    c = RowCursor(base)
    bc_base_cell = nb["bc_base_cell"]
    ap_lltm_base_cell = nb["ap_lltm_base_cell"]
    bc_coeff = co["bc_supplier_coeff_cell"]()
    bc_coeff_fy22 = co["bc_supplier_coeff_fy22_cell"]()
    ap_coeff = co["ap_lltm_supplier_coeff_cell"]()

    c.banner("§5 - TAM by fiscal year", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§5a - TAM by FY ($M)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Stream"] + list(_FY_COLUMNS) + ["FY22-27"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(_FY_COLUMNS) + 1))
    bc_vals = ["BC stream (vintage-matched MYP-corrected coeff)"]
    for fy in _FY_COLUMNS:
        b = bc_base_cell(_LI, fy)
        cf = bc_coeff_fy22 if fy == 2022 else bc_coeff
        bc_vals.append(f'=IF(N({b})=0,"",N({b})*N({cf}))')
    bc_vals.append(lambda r: f"=SUM(C{r}:{_LAST_FY_COL}{r})")
    pos["bc"] = c.write(bc_vals, styles=[S_LABEL_INDENT_1] + [S_NUM] * (len(_FY_COLUMNS) + 1), outline_level=1)
    ap_vals = ["AP/LLTM stream (P-10 EOQ x coeff)"]
    for fy in _FY_COLUMNS:
        a = ap_lltm_base_cell(_LI, fy)
        ap_vals.append(f'=IF(N({a})=0,"",N({a})*N({ap_coeff}))')
    ap_vals.append(lambda r: f"=SUM(C{r}:{_LAST_FY_COL}{r})")
    pos["ap"] = c.write(ap_vals, styles=[S_LABEL_INDENT_1] + [S_NUM] * (len(_FY_COLUMNS) + 1), outline_level=1)
    tam_vals = ["TAM (BC + AP/LLTM)"]
    for fy in _FY_COLUMNS:
        col = _fy_col(fy)
        tam_vals.append(f"=N({col}{pos['bc']})+N({col}{pos['ap']})")
    tam_vals.append(lambda r: f"=SUM(C{r}:{_LAST_FY_COL}{r})")
    pos["tam"] = c.total(tam_vals, styles=[S_BOLD] + [S_NUM] * (len(_FY_COLUMNS) + 1),
                         n_cols=len(_FY_COLUMNS) + 2)
    c.blank(2)
    c.banner("§5b - Coefficients applied (live links to §3)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Coefficient", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["BC supplier coefficient (FY23-27)", f"={bc_coeff}"],
            styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.write(["BC supplier coefficient, FY2022 vintage", f"={bc_coeff_fy22}"],
            styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.write(["AP/LLTM supplier coefficient", f"={ap_coeff}"],
            styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank(2)
    # §5c is a single total row (no outlined detail rows), so no collapse marker.
    c.banner("§5c - Portfolio TAM (DDG-51, FY22-FY27)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION)
    c.blank()
    c.total(["Portfolio TAM ($M)", f"={_total_col()}{pos['tam']}"],
            styles=[S_BOLD, S_NUM], n_cols=2)
    c.blank(2)
    tam_tot = f"{_total_col()}{pos['tam']}"
    bc_tot = f"{_total_col()}{pos['bc']}"
    c.banner("§5d - Average-annual and per-hull views (FY22-FY27)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["View", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    pos["n_years"] = c.write(["Years in window (n)", len(_FY_COLUMNS)],
                             styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    pos["avg_annual"] = c.write(
        ["Average annual TAM ($M/yr)", f"={tam_tot}/C{pos['n_years']}"],
        styles=[S_BOLD, S_NUM], outline_level=1)
    pos["n_hulls"] = c.write(["In-window hulls (award FY22-27)", _hulls()],
                             styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    pos["per_hull"] = c.write(["Supplier TAM per hull ($M)", f"={tam_tot}/C{pos['n_hulls']}"],
                              styles=[S_BOLD, S_NUM], outline_level=1)
    pos["per_hull_bc"] = c.write(["BC TAM per hull ($M)", f"={bc_tot}/C{pos['n_hulls']}"],
                                 styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.blank(2)
    c.banner("§5e - TAM bridge components (BC base to supplier TAM)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    bc_base_sum = "+".join(f"N({bc_base_cell(_LI, fy)})" for fy in _FY_COLUMNS)
    pos["bc_base"] = c.write(["BC construction base ($M)", f"={bc_base_sum}"],
                             styles=[S_BOLD, S_NUM], outline_level=1)
    pos["removal"] = c.write(["POP removal: prime, co-prime, GFE ($M)", f"=C{pos['bc_base']}-{bc_tot}"],
                             styles=[S_DEFAULT, S_NUM], outline_level=1)

    def tam_cell(li, fy):
        _check(li, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['tam']}"

    def tam_total_cell(fy):
        _check(_LI, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['tam']}"

    def tam_bc_total_cell(fy):
        _check(_LI, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['bc']}"

    def tam_ap_total_cell(fy):
        _check(_LI, fy)
        return f"'{tab}'!{_fy_col(fy)}{pos['ap']}"

    return c.rows, c.at(), dict(
        tam_cell=tam_cell, tam_total_cell=tam_total_cell,
        tam_bc_total_cell=tam_bc_total_cell, tam_ap_total_cell=tam_ap_total_cell,
        portfolio_tam_cell=lambda: f"'{tab}'!{_total_col()}{pos['tam']}",
        portfolio_bc_tam_cell=lambda: f"'{tab}'!{_total_col()}{pos['bc']}",
        portfolio_ap_tam_cell=lambda: f"'{tab}'!{_total_col()}{pos['ap']}",
        avg_annual_tam_cell=lambda: f"'{tab}'!C{pos['avg_annual']}",
        n_years_cell=lambda: f"'{tab}'!C{pos['n_years']}",
        per_hull_tam_cell=lambda: f"'{tab}'!C{pos['per_hull']}",
        per_hull_bc_tam_cell=lambda: f"'{tab}'!C{pos['per_hull_bc']}",
        portfolio_bc_base_cell=lambda: f"'{tab}'!C{pos['bc_base']}",
        pop_removal_cell=lambda: f"'{tab}'!C{pos['removal']}")


# ── Layout pass (import time): build detail blocks, promote accessors ──────────
_nb_rows, _after_nb, _nb_acc = _build_normalized_budget(_TAB, _NB_BASE)
_CO_BASE = _after_nb + 2
_co_rows, _after_co, _co_acc = _build_coefficients(_TAB, _CO_BASE)
_MY_BASE = _after_co + 2
_my_rows, _after_my, _my_acc = _build_myp(_TAB, _MY_BASE, _co_acc)
_TM_BASE = _after_my + 2
_tm_rows, _after_tm, _tm_acc = _build_model(_TAB, _TM_BASE, _nb_acc, _co_acc)

bc_base_cell = _nb_acc["bc_base_cell"]
ap_lltm_base_cell = _nb_acc["ap_lltm_base_cell"]
tam_base_cell = _nb_acc["tam_base_cell"]
bc_supplier_coeff_cell = _co_acc["bc_supplier_coeff_cell"]
bc_supplier_coeff_fy22_cell = _co_acc["bc_supplier_coeff_fy22_cell"]
bc_supplier_coeff_disclosed_cell = _co_acc["bc_supplier_coeff_disclosed_cell"]
ap_lltm_supplier_coeff_cell = _co_acc["ap_lltm_supplier_coeff_cell"]
total_weighted_coeff_cell = _co_acc["total_weighted_coeff_cell"]
outside_yards_disclosed_cell = _co_acc["outside_yards_disclosed_cell"]
outside_yards_corrected_cell = _co_acc["outside_yards_corrected_cell"]
anchor_ok_cell = _co_acc["anchor_ok_cell"]
biw_pop_share_cell = _co_acc["biw_pop_share_cell"]
ingalls_pop_share_cell = _co_acc["ingalls_pop_share_cell"]
other_pop_share_cell = _co_acc["other_pop_share_cell"]
foreign_pop_share_cell = _co_acc["foreign_pop_share_cell"]
unparsed_pop_share_cell = _co_acc["unparsed_pop_share_cell"]
myp_swing_cell = _my_acc["myp_swing_cell"]
tam_cell = _tm_acc["tam_cell"]
tam_total_cell = _tm_acc["tam_total_cell"]
tam_bc_total_cell = _tm_acc["tam_bc_total_cell"]
tam_ap_total_cell = _tm_acc["tam_ap_total_cell"]
portfolio_tam_cell = _tm_acc["portfolio_tam_cell"]
portfolio_bc_tam_cell = _tm_acc["portfolio_bc_tam_cell"]
portfolio_ap_tam_cell = _tm_acc["portfolio_ap_tam_cell"]
avg_annual_tam_cell = _tm_acc["avg_annual_tam_cell"]
n_years_cell = _tm_acc["n_years_cell"]
per_hull_tam_cell = _tm_acc["per_hull_tam_cell"]
per_hull_bc_tam_cell = _tm_acc["per_hull_bc_tam_cell"]
portfolio_bc_base_cell = _tm_acc["portfolio_bc_base_cell"]
pop_removal_cell = _tm_acc["pop_removal_cell"]


def _render_tam_build() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - Headline TAM", n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    # At-a-glance summarizes THIS sheet's own producer cells (same-sheet refs), so
    # the values are black derived (S_NUM/S_PCT) - green is for cross-sheet links only.
    c.write(["Portfolio TAM (FY22-27, both streams) $M", f"={portfolio_tam_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["BC-stream TAM $M", f"={portfolio_bc_tam_cell()}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["AP/LLTM-stream TAM $M", f"={portfolio_ap_tam_cell()}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Average annual TAM $M/yr", f"={avg_annual_tam_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.write(["Supplier TAM per in-window hull $M", f"={per_hull_tam_cell()}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["BC TAM per in-window hull $M", f"={per_hull_bc_tam_cell()}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Applied BC supplier coefficient (FY23-27)", f"={bc_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_PCT])
    c.write(["AP/LLTM supplier coefficient", f"={ap_lltm_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_PCT])
    c.blank(2)
    assert c.at() == _NB_BASE, f"at-a-glance ends at {c.at()}, expected {_NB_BASE}"
    c.feed(_nb_rows, _after_nb)
    c.blank(2)
    c.feed(_co_rows, _after_co)
    c.blank(2)
    c.feed(_my_rows, _after_my)
    c.blank(2)
    c.feed(_tm_rows, _after_tm)

    ws = worksheet(c.rows, cols=[38, 14, 14, 14, 14, 14, 14, 14],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


TAM_BUILD = SheetEntry(_TAB, _GROUP, _render_tam_build)
