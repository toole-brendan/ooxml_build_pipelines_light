"""validation_sensitivity - the "Sensitivity" tab (one module = one sheet).

The swings that move TAM/SAM: the coefficient ladder, the nuclear-boundary BPMI
exclusion (applied), the resulting TAM impact, and the real P-10 gross AP reference.
Imports TAM Build (the applied coefficients + BC stream TAM), POP Location Parse
(the corpus ranges), and Assumptions & Controls (the gross-P10 reference).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT, S_LINK_NUM,
    S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines.model_tam_build import (
    bc_supplier_coeff_cell, ap_lltm_supplier_coeff_cell, tam_bc_total_cell,
)
from workbook_master_tam.sheets.submarines.data_pop_corpus import (
    gate_range, gfe_excl_range, confirmed_range, stream_range, program_range,
    pop_dollar_range, pct_range,
)
from workbook_master_tam.sheets.submarines.inputs_assumptions import ap_gross_cell
from workbook_master_tam.sheets.submarines.data_entity_master import (
    addressable_total_cell as _addr, observed_bucket_dollar_cell as _bkt_dollar,
    vls_boundary_dollar_cell as _vls_dollar,
)
from workbook_master_tam.sheets.submarines.taxonomy import UNBUCKETED
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "validation"
_TAB = "Sub Sensitivity"
_Q = '"'
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_BASE = 13                                       # title(2) + blank + §1 at-a-glance(4-10) + 2 blanks


def _build_sensitivity(tab: str, base: int):
    _g, _x, _c, _s, _prog = gate_range, gfe_excl_range, confirmed_range, stream_range, program_range
    _d, _p = pop_dollar_range, pct_range
    _SUPP = f"({_p('other')}+{_p('foreign')})"

    def _coeff(mask):
        den = f"SUMPRODUCT({mask}*{_d()})"
        num = f"SUMPRODUCT({mask}*{_d()}*{_SUPP})"
        return f'=IF({den}=0,"",{num}/{den})'

    bc_incl_bpmi = (f'{_g()}*{_c()}*((1-{_x()})*({_s()}={_Q}BC{_Q})'
                    f'+({_prog()}={_Q}bpmi_nuclear{_Q}))')
    bc_tam_sum = "+".join(f"N({tam_bc_total_cell(fy)})" for fy in _FY)
    gross_sum = "+".join(f"N({ap_gross_cell(li, fy)})" for li in (2013, 1045) for fy in _FY)

    c = RowCursor(base)
    c.banner("§2 - Coefficient ladder (the swings that move TAM/SAM)", n_cols=2,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Variant", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["All-gated POP anchor (not applied)", _coeff(_g())],
            styles=[S_DEFAULT, S_PCT], outline_level=1)
    r_headline = c.write(["Pooled corpus coeff (non-nuclear; reference)", f"={bc_supplier_coeff_cell()}"],
                         styles=[S_BOLD, S_LINK_PCT], outline_level=1)
    r_ap = c.write(["AP/LLTM coeff (reference; base=0)", f"={ap_lltm_supplier_coeff_cell()}"],
                   styles=[S_BOLD, S_LINK_PCT], outline_level=1)
    r_delta = c.write(["BC - AP/LLTM delta", lambda r: f"=C{r_headline}-C{r_ap}"],
                      styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank()
    c.banner("§2a - Nuclear-boundary BPMI exclusion (corpus measure)", n_cols=2,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["BC coefficient under each attribution", "Value"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    r_inclbpmi = c.write(["BC coeff incl. BPMI (sensitivity)", _coeff(bc_incl_bpmi)],
                         styles=[S_DEFAULT, S_PCT], outline_level=1)
    r_hl_bpmi = c.write(["Pooled corpus coeff (BPMI excluded; reference)", f"={bc_supplier_coeff_cell()}"],
                        styles=[S_BOLD, S_LINK_PCT], outline_level=1)
    r_swing = c.write(["BC swing (BPMI removal)", lambda r: f"=C{r_inclbpmi}-C{r_hl_bpmi}"],
                      styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.write(["BPMI $ (now GFE-excluded)",
             f'=SUMPRODUCT({_g()}*({_prog()}={_Q}bpmi_nuclear{_Q})*{_d()})'],
            styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.blank()
    c.banner("§2b - TAM impact (headline vs pre-boundary sensitivity; AP base=0)", n_cols=2,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    r_hl_tam = c.write(["Headline non-nuclear supplier TAM (cum.)", f"={bc_tam_sum}"],
                       styles=[S_BOLD, S_NUM], outline_level=1)
    r_sens_tam = c.write(["Pre-boundary sensitivity TAM",
                          lambda r: f"=C{r_hl_tam}*(C{r_inclbpmi}/C{r_hl_bpmi})"],
                         styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_gross = c.write(["Real P-10 gross AP (FY22-27, ref)", f"={gross_sum}"],
                      styles=[S_DEFAULT, S_NUM], outline_level=1)

    acc = dict(headline_cell=lambda: f"'{tab}'!C{r_headline}", ap_cell=lambda: f"'{tab}'!C{r_ap}",
               delta_cell=lambda: f"'{tab}'!C{r_delta}", sens_tam_cell=lambda: f"'{tab}'!C{r_sens_tam}",
               gross_cell=lambda: f"'{tab}'!C{r_gross}", bc_swing_cell=lambda: f"'{tab}'!C{r_swing}")
    return c.rows, c.at(), acc


# ── Layout pass ──────────────────────────────────────────────────────────────
_rows, _after, _acc = _build_sensitivity(_TAB, _BASE)
bc_swing_cell = _acc["bc_swing_cell"]
headline_coeff_cell = _acc["headline_cell"]      # applied BC coeff (sensitivity view)
ap_coeff_cell = _acc["ap_cell"]                  # AP/LLTM reference coeff
sens_tam_cell = _acc["sens_tam_cell"]            # pre-boundary sensitivity TAM
gross_ap_cell = _acc["gross_cell"]               # real P-10 gross AP (reference)


def _render_sensitivity() -> WorksheetSpec:
    n_cols = 2
    c = RowCursor(2)
    c.banner("Sensitivity", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - The swings", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    c.write(["Pooled corpus supplier coefficient (reference)", f"={bc_supplier_coeff_cell()}"],
            styles=[S_BOLD, S_LINK_PCT])
    c.write(["AP/LLTM reference coefficient", f"={ap_lltm_supplier_coeff_cell()}"],
            styles=[S_DEFAULT, S_LINK_PCT])
    _sens_row = c.write(["Pre-boundary sensitivity TAM $M", f"={_acc['sens_tam_cell']()}"],
            styles=[S_DEFAULT, S_NUM])
    _gross_row = c.write(["Real P-10 gross AP $M (reference)", f"={_acc['gross_cell']()}"],
            styles=[S_DEFAULT, S_NUM])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_rows, _after)
    c.blank(2)

    # §3 Sensitivity guardrails
    c.banner("§3 - Sensitivity guardrails", n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    for txt in [
        "Sensitivity values are not headline.",
        "The BPMI-included coefficient (~75.7%) is not applied.",
        "The AP/LLTM coefficient is reference-only while the additive base is zero.",
    ]:
        c.write([txt], styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 VLS launch-control sensitivity (market-definition boundary; ~negligible on subs)
    c.banner("§4 - VLS launch-control sensitivity (boundary launcher electronics: out vs in)",
             n_cols=n_cols, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    r_base = c.write(["Physical supplier base (VLS launch-control OUT - base case)",
                      f"={_addr()}-{_bkt_dollar(UNBUCKETED)}"], styles=[S_BOLD, S_NUM], outline_level=1)
    r_vls = c.write(["+ VLS launch-control boundary (mission_systems)", f"={_vls_dollar()}"],
                    styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.write(["= Physical supplier base (VLS launch-control IN - sensitivity)", f"=C{r_base}+C{r_vls}"],
            styles=[S_BOLD, S_NUM], outline_level=1)

    ws = worksheet(c.rows, cols=[44, 16], tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


SENSITIVITY = SheetEntry(_TAB, _GROUP, _render_sensitivity)
