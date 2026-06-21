"""model_sam_build - the "SAM Build" tab (DDG, model group; one module = one sheet).

Converts TAM into bucket-level and scenario-level SAM. Three sections - §2 Modeled
shares (per-FY bucket vectors from the gated Worktype by FY evidence + the Inputs
adjustment) -> §3 Allocation (bucket TAM = sum over FY of annual TAM x that FY's
modeled share; FY2026-27 use the FY22-25 window vector, the gated corpus has no
subaward reporting there yet) -> §4 Scenarios (the SAM menu) - behind a §1 headline
at-a-glance scenario menu. §5 resolves the annual SAM cadence with the same per-FY
vectors.

The portfolio-TAM basis LINKS to TAM Build (the producer; not recomputed). The
editable bucket-share Adjustment lives on Inputs and applies uniformly to every FY
column. The modular scenario is entity-tag-driven from the gated window (Worktype
by FY §4).

Two-pass layout: the detail blocks build at import (capturing rows + promoting
accessors); the at-a-glance builds at render and asserts it fills the reserved rows.

Promoted accessors keep their names; share accessors resolve to the FY22-25 window
column (the forward vector).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_LABEL_INDENT_1, S_TITLE_SHEET,
    S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._taxonomy import BUCKETS, BUCKET_KEYS, UNBUCKETED
from workbook_master_tam.sheets.ddg.data_entity_master import (
    role_range as _role, ent_dollar_range as _dol,
)
from workbook_master_tam.sheets.ddg.data_worktype_by_fy import (
    wt_fy_columns, wt_share_cell, wt_window_share_cell, wt_modular_share_cell,
)
from workbook_master_tam.sheets.ddg.model_tam_build import (
    tam_total_cell as _tam_total, n_years_cell as _n_years,
    portfolio_tam_cell as _tam_portfolio,
)
from workbook_master_tam.sheets.ddg.inputs_scenarios import scenario_keys, scenario_name, scenario_flag_range
from workbook_master_tam.sheets.ddg.inputs_assumptions import bucket_adjustment_cell
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "model"
_TAB = "DDG SAM Build"
_NCOLS = 8
_Q = '"'
_BUCKET_NAME = {k: name for k, name, _ in BUCKETS}
_SCEN_KEYS = scenario_keys()
_SAM_BASE = 9 + len(_SCEN_KEYS)   # title(2)+blank+§1 menu+2 blanks; body begins here
_FY_ANNUAL = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_EVIDENCE = wt_fy_columns()                    # [2022..2025] - per-FY share vectors
# §2 modeled grid columns: B label, C Adj, D..G evidence FYs, H = FY22-25 window
_M_COL = {fy: col_letter(3 + i) for i, fy in enumerate(_FY_EVIDENCE)}     # D..G
_M_WIN = col_letter(3 + len(_FY_EVIDENCE))                                # H
_ANNUAL_COL = {fy: col_letter(2 + i) for i, fy in enumerate(_FY_ANNUAL)}   # C..H
_ANNUAL_TOTAL_COL = col_letter(2 + len(_FY_ANNUAL))                        # I
_ANNUAL_NCOLS = 2 + len(_FY_ANNUAL)   # label + 6 FY + total = 8 content cols


def _sp(*m):
    return f"SUMPRODUCT({'*'.join(m)})"


def _m_col(fy: int) -> str:
    """Modeled-share column for an annual FY; FY2026-27 ride the window vector."""
    return _M_COL.get(fy, _M_WIN)


def _roledollar(rk):
    return _sp(f"({_role()}={_Q}{rk}{_Q})", _dol())


# ════════════════════════════ §2 Modeled shares ═══════════════════════════════
def _build_shares(tab: str, base: int):
    c = RowCursor(base)
    c.banner("§2 - Supplier-addressable shares (gated evidence)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§2a - Modeled shares by FY (= Worktype by FY observed + Inputs adjustment)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Adj +/- (Inputs)"] + [f"FY{fy}" for fy in _FY_EVIDENCE] + ["FY26-27 (window)"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (2 + len(_FY_EVIDENCE)))
    first_bucket = c.at()
    m_row = {k: first_bucket + i for i, k in enumerate(BUCKET_KEYS)}
    unbk_row = first_bucket + len(BUCKET_KEYS)
    total_row = unbk_row + 1
    last_bucket = m_row[BUCKET_KEYS[-1]]
    for k in BUCKET_KEYS:
        r = m_row[k]
        c.write([_BUCKET_NAME[k], f"={bucket_adjustment_cell(k)}"]
                + [f"=N({wt_share_cell(k, fy)})+$C{r}" for fy in _FY_EVIDENCE]
                + [f"=N({wt_window_share_cell(k)})+$C{r}"],
                styles=[S_LABEL_INDENT_1, S_LINK_PCT] + [S_PCT] * (1 + len(_FY_EVIDENCE)),
                outline_level=1)
    share_cols = [_M_COL[fy] for fy in _FY_EVIDENCE] + [_M_WIN]
    c.write(["Unbucketed / ambiguous (not in scenario SAM)", None]
            + [f"=1-SUM({col}{first_bucket}:{col}{last_bucket})" for col in share_cols],
            styles=[S_LABEL_INDENT_1, S_DEFAULT] + [S_PCT] * len(share_cols), outline_level=1)
    c.total(["Total modeled share", None]
            + [f"=SUM({col}{first_bucket}:{col}{unbk_row})" for col in share_cols],
            styles=[S_BOLD, S_DEFAULT] + [S_PCT] * len(share_cols), n_cols=_NCOLS - 1)
    c.blank(2)
    c.banner("§2b - Excluded from the addressable base (full corpus audit - not supplier-addressable)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Role", "$M", "", "", ""], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT, S_HEADER_LEFT, S_HEADER_LEFT])
    addr_total_row = c.write(["Supplier (addressable, full corpus)", f"={_roledollar('supplier')}", None, None, None],
                             styles=[S_LABEL_INDENT_1, S_NUM, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    for rk, label in [("mission_systems", "Mission systems (combat/electronics - VLS, radar, EW)"),
                      ("service", "Service / non-component / IT"),
                      ("holding", "Holding / parent unknown"),
                      ("foreign_fms", "Foreign / FMS"),
                      ("prime", "Prime yard (Bath Iron Works)"),
                      ("co_prime", "Co-prime yard (HII Ingalls)"),
                      ("gfe_mib", "GFE / Navy-directed (Aegis/SPY-6/weapons)")]:
        c.write([label, f"={_roledollar(rk)}", None, None, None],
                styles=[S_LABEL_INDENT_1, S_NUM, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.total(["Grand total (all recipients)", f"={_sp(_dol())}", None, None, None],
            styles=[S_BOLD, S_NUM, S_DEFAULT, S_DEFAULT, S_DEFAULT], n_cols=5)

    acc = dict(
        modeled_share_cell=lambda b: f"'{tab}'!{_M_WIN}{m_row[b]}",
        modeled_share_fy_cell=lambda b, fy: f"'{tab}'!{_m_col(fy)}{m_row[b] if b in m_row else unbk_row}",
        observed_share_cell=lambda b: wt_window_share_cell(b),
        bucket_share_range=lambda: f"'{tab}'!{_M_WIN}{first_bucket}:{_M_WIN}{last_bucket}",
        unbucketed_share_cell=lambda: f"'{tab}'!{_M_WIN}{unbk_row}",
        addressable_total_cell=lambda: f"'{tab}'!C{addr_total_row}",
        modeled_share_total_cell=lambda: f"'{tab}'!{_M_WIN}{total_row}",
        _m_first=first_bucket, _m_last=last_bucket, _m_unbk=unbk_row, _m_row=m_row)
    return c.rows, c.at(), acc


# ════════════════════════════ §3 Bucket allocation ════════════════════════════
def _build_allocation(tab: str, base: int, sub: dict):
    c = RowCursor(base)
    m_row = sub["_m_row"]
    unbk = sub["_m_unbk"]
    c.banner("§3 - Bucket allocation", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§3a - Portfolio TAM basis (cumulative FY22-FY27)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    port_tam_row = c.write(["Portfolio TAM (DDG-51, both streams), FY22-27", f"={_tam_portfolio()}"],
                           styles=[S_BOLD, S_LINK_NUM], outline_level=1)
    PORT = f"$C${port_tam_row}"
    c.blank(2)
    c.banner("§3b - TAM by work-type bucket (annual TAM x per-FY modeled share)",
             n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Bucket TAM $M", "Effective share"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    alloc_first = c.at()
    alloc_bucket = {k: alloc_first + i for i, k in enumerate(BUCKET_KEYS)}

    def _alloc(share_row: int) -> str:
        terms = [f"N({_tam_total(fy)})*{_m_col(fy)}{share_row}" for fy in _FY_EVIDENCE]
        terms.append(f"(N({_tam_total(2026)})+N({_tam_total(2027)}))*{_M_WIN}{share_row}")
        return "+".join(terms)

    for k in BUCKET_KEYS:
        r = alloc_bucket[k]
        c.write([_BUCKET_NAME[k], f"={_alloc(m_row[k])}", f"=C{r}/{PORT}"],
                styles=[S_LABEL_INDENT_1, S_NUM, S_PCT], outline_level=1)
    alloc_unbk = c.write(["Unbucketed / ambiguous (not in scenario SAM)",
                          f"={_alloc(unbk)}", lambda r: f"=C{r}/{PORT}"],
                         styles=[S_LABEL_INDENT_1, S_NUM, S_PCT], outline_level=1)
    alloc_total = c.total(["Total (7 buckets + unbucketed = TAM)",
                           f"=SUM(C{alloc_first}:C{alloc_unbk})", f"=SUM(D{alloc_first}:D{alloc_unbk})"],
                          styles=[S_BOLD, S_NUM, S_PCT], n_cols=3)
    alloc_last_bucket = alloc_bucket[BUCKET_KEYS[-1]]

    acc = dict(
        bucket_tam_cell=lambda b: f"'{tab}'!C{alloc_bucket[b]}",
        bucket_tam_range=lambda: f"'{tab}'!C{alloc_first}:C{alloc_last_bucket}",
        unbucketed_tam_cell=lambda: f"'{tab}'!C{alloc_unbk}",
        portfolio_tam_cell=lambda: f"'{tab}'!C{port_tam_row}",
        bucketed_total_cell=lambda: f"'{tab}'!C{alloc_total}")
    return c.rows, c.at(), acc


# ════════════════════════════ §4 Scenarios (SAM menu) ═════════════════════════
def _build_scenarios_block(tab: str, base: int, alloc: dict):
    c = RowCursor(base)
    brange = alloc["bucket_tam_range"]()
    port = alloc["portfolio_tam_cell"]()
    nyr = _n_years()
    c.banner("§4 - Scenario calculation", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.banner("§4a - SAM by leadership scenario (subset of TAM)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "SAM $M", "% of TAM", "SAM $M/yr"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    scen_first = c.at()
    scen_row = {k: scen_first + i for i, k in enumerate(_SCEN_KEYS)}
    for k in _SCEN_KEYS:
        r = scen_row[k]
        if k == "modular":
            # entity-tag-driven: portfolio TAM x gated-window modular share
            sam = f"{port}*N({wt_modular_share_cell()})"
        else:
            sam = f"SUMPRODUCT({brange},{scenario_flag_range(k)})"
        c.write([scenario_name(k), f"={sam}", f"=C{r}/{port}", f"=C{r}/{nyr}"],
                styles=[S_DEFAULT, S_NUM, S_PCT, S_NUM], outline_level=1)
    c.blank(2)
    c.banner("§4b - Residual explanation", n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Broad SAM = TAM - unbucketed residual."],
            styles=[S_DEFAULT], outline_level=1)

    acc = dict(
        sam_cell=lambda k: f"'{tab}'!C{scen_row[k]}",
        sam_pct_cell=lambda k: f"'{tab}'!D{scen_row[k]}",
        sam_avg_annual_cell=lambda k: f"'{tab}'!E{scen_row[k]}",
        scenario_keys_ordered=lambda: list(_SCEN_KEYS))
    return c.rows, c.at(), acc


# ════════════════════ §5 Annual SAM by fiscal year ════════════════════════════
def _build_annual(tab: str, base: int, sub: dict):
    """Annual SAM by FY = annual portfolio TAM (TAM Build) x that FY's scenario factor.

    annual scenario SAM(fy) = TAM_total(fy) x SUMPRODUCT(modeled shares(fy),
    scenario flags); FY2026-27 use the FY22-25 window vector. The FY22-27 sum ties
    to the cumulative scenario SAM (§4) by construction. Broad SAM(fy) =
    annual TAM(fy) x (1 - unbucketed modeled share(fy))."""
    c = RowCursor(base)
    m_first, m_last = sub["_m_first"], sub["_m_last"]
    c.banner("§5 - Annual SAM by fiscal year",
             n_cols=_ANNUAL_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario"] + [f"FY{fy}" for fy in _FY_ANNUAL] + ["FY22-27"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(_FY_ANNUAL) + 1))
    ann_row: dict = {}
    for k in _SCEN_KEYS:
        vals = [scenario_name(k)]
        for fy in _FY_ANNUAL:
            if k == "modular":
                vals.append(f"={_tam_total(fy)}*N({wt_modular_share_cell()})")
            else:
                col = _m_col(fy)
                vals.append(f"={_tam_total(fy)}*SUMPRODUCT('{tab}'!{col}{m_first}:{col}{m_last},"
                            f"{scenario_flag_range(k)})")
        vals.append(lambda r: f"=SUM({_ANNUAL_COL[_FY_ANNUAL[0]]}{r}:{_ANNUAL_COL[_FY_ANNUAL[-1]]}{r})")
        ann_row[k] = c.write(vals, styles=[S_DEFAULT] + [S_NUM] * (len(_FY_ANNUAL) + 1),
                             outline_level=1)
    c.blank(2)
    c.banner("§5b - Annual tie-out (per-FY annual broad SAM sums to cumulative broad SAM)",
             n_cols=_ANNUAL_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    bri = ann_row["broad"]
    c.write(["Annual broad SAM FY22-27 (sum)", f"={_ANNUAL_TOTAL_COL}{bri}"],
            styles=[S_DEFAULT, S_NUM], outline_level=1)

    acc = dict(
        annual_sam_cell=lambda k, fy: f"'{tab}'!{_ANNUAL_COL[fy]}{ann_row[k]}",
        annual_broad_sam_cell=lambda fy: f"'{tab}'!{_ANNUAL_COL[fy]}{ann_row['broad']}")
    return c.rows, c.at(), acc


# ── Layout pass (import time) ─────────────────────────────────────────────────
_sub_rows, _after_sub, _sub_acc = _build_shares(_TAB, _SAM_BASE)
_AL_BASE = _after_sub + 2
_al_rows, _after_al, _al_acc = _build_allocation(_TAB, _AL_BASE, _sub_acc)
_SC_BASE = _after_al + 2
_sc_rows, _after_sc, _sc_acc = _build_scenarios_block(_TAB, _SC_BASE, _al_acc)
_AN_BASE = _after_sc + 2
_an_rows, _after_an, _an_acc = _build_annual(_TAB, _AN_BASE, _sub_acc)

modeled_share_cell = _sub_acc["modeled_share_cell"]
modeled_share_fy_cell = _sub_acc["modeled_share_fy_cell"]
observed_share_cell = _sub_acc["observed_share_cell"]
bucket_share_range = _sub_acc["bucket_share_range"]
unbucketed_share_cell = _sub_acc["unbucketed_share_cell"]
addressable_total_cell = _sub_acc["addressable_total_cell"]
modeled_share_total_cell = _sub_acc["modeled_share_total_cell"]
bucket_tam_cell = _al_acc["bucket_tam_cell"]
bucket_tam_range = _al_acc["bucket_tam_range"]
unbucketed_tam_cell = _al_acc["unbucketed_tam_cell"]
portfolio_tam_cell = _al_acc["portfolio_tam_cell"]
bucketed_total_cell = _al_acc["bucketed_total_cell"]
sam_cell = _sc_acc["sam_cell"]
sam_pct_cell = _sc_acc["sam_pct_cell"]
sam_avg_annual_cell = _sc_acc["sam_avg_annual_cell"]
scenario_keys_ordered = _sc_acc["scenario_keys_ordered"]
annual_sam_cell = _an_acc["annual_sam_cell"]
annual_broad_sam_cell = _an_acc["annual_broad_sam_cell"]


def _render_sam_build() -> WorksheetSpec:
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - SAM scenario menu", n_cols=_NCOLS, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Scenario", "SAM $M", "% of TAM", "SAM $M/yr"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    # At-a-glance links THIS sheet's own §4 scenario rows (same-sheet) -> black derived.
    for k in _SCEN_KEYS:
        c.write([scenario_name(k), f"={sam_cell(k)}", f"={sam_pct_cell(k)}", f"={sam_avg_annual_cell(k)}"],
                styles=[S_DEFAULT, S_NUM, S_PCT, S_NUM])
    c.blank(2)
    assert c.at() == _SAM_BASE, f"at-a-glance ends at {c.at()}, expected {_SAM_BASE}"
    c.feed(_sub_rows, _after_sub)
    c.blank(2)
    c.feed(_al_rows, _after_al)
    c.blank(2)
    c.feed(_sc_rows, _after_sc)
    c.blank(2)
    c.feed(_an_rows, _after_an)
    # 8 content cols (B-I): §2 uses B-H, §3-§4 use B-F, §5 uses B-I.
    ws = worksheet(c.rows, cols=[44, 14, 12, 12, 12, 12, 14, 13],
                   tab_color=group_color(_GROUP), with_gutter=True)
    return WorksheetSpec(ws)


SAM_BUILD = SheetEntry(_TAB, _GROUP, _render_sam_build)
