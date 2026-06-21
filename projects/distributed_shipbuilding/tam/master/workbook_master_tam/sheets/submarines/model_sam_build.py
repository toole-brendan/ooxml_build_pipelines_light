"""model_sam_build - the "SAM Build" tab (one module = one sheet).

The SAM calculation + explanation sheet, per class. Modeled bucket shares are
per-class per-FY vectors: the gated Worktype by FY observed shares (Virginia and
Columbia measured separately on GDEB-PIID subawards, FY2022-25 window) plus the
shared Assumptions adjustment. Each class's annual TAM (TAM Build tam_cell) is
allocated at its own FY's vector - FY2026-27 ride the FY22-25 window vector (no
usable subaward reporting there yet) - then the classes sum to the combined bucket
TAM. SAM scenario = SUMPRODUCT(combined bucket TAM, scenario flags); the modular
scenario is entity-tag-driven per class. §7 resolves the annual SAM cadence with
the same per-class per-FY vectors.

The body is built once at IMPORT time via a cursor, so the promoted accessors
(portfolio_tam_cell, bucket_tam_cell/range, unbucketed_tam_cell, bucketed_total_cell,
sam_cell, sam_pct_cell, avg_annual_sam_cell, scenario_keys_ordered, selected_* cells,
va_/col_modeled_share_total_cell) resolve from captured row positions regardless of
render order. The selected_* cells are read back by Assumptions & Controls's
selector display via a lazy import.
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_LINK_NUM, S_LINK_PCT, S_TITLE_SHEET, S_TITLE_SECTION, S_TITLE_SUBSECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines.taxonomy import BUCKETS, BUCKET_KEYS, UNBUCKETED
from workbook_master_tam.sheets.submarines import inputs_assumptions as _ac
from workbook_master_tam.sheets.submarines import data_entity_master as _em
from workbook_master_tam.sheets.submarines.data_worktype_by_fy import (
    wt_fy_columns, wt_share_cell, wt_window_share_cell, wt_modular_share_cell,
)
from workbook_master_tam.sheets.submarines.model_tam_build import tam_cell, tam_total_cell, n_years_cell
from workbook_master_tam.sheets.submarines._layout import RowCursor

_GROUP = "model"
_TAB = "Sub SAM Build"
_FY = [2022, 2023, 2024, 2025, 2026, 2027]
_BASE = 14                                       # title(2) + blank + §1 at-a-glance(4-11) + 2 blanks
_BUCKET_NAME = {k: name for k, name, _ in BUCKETS}
_SCEN_KEYS = _ac.scenario_keys()
_NCOLS = 2 + len(_SCEN_KEYS)            # full content width: label + annual TAM + scenarios (§7, the widest block)
_SHORT = {"metal": "Metal", "hme": "HM&E", "electrical": "Electrical",
          "modular": "Modular", "broad": "Broad"}
_XROLES = [("mission_systems", "Mission systems (combat/electronics)"),
           ("service", "Service / non-component / IT"), ("holding", "Holding / parent unknown"),
           ("foreign_fms", "Foreign / FMS"), ("prime", "Prime yard (final assembly)"),
           ("co_prime", "Co-prime yard"), ("gfe_sib", "GFE / SIB (Navy-directed, BlueForge)")]
_CLASSES = [("va", "Virginia", 2013), ("col", "Columbia", 1045)]
_FY_EVIDENCE = wt_fy_columns()                    # [2022..2025] - per-FY share vectors
# Modeled grid columns: B bucket, C Adj, D..G evidence FYs, H = FY22-25 window
_M_COL = {fy: col_letter(3 + i) for i, fy in enumerate(_FY_EVIDENCE)}     # D..G
_M_WIN = col_letter(3 + len(_FY_EVIDENCE))                                # H


def _m_col(fy: int) -> str:
    """Modeled-share column for an annual FY; FY2026-27 ride the window vector."""
    return _M_COL.get(fy, _M_WIN)


def _build_body(tab: str, base: int):
    pos = {}
    c = RowCursor(base)

    # §2 Scenario matrix (linked view of Assumptions & Controls)
    c.banner("§2 - Scenario matrix", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket"] + [_SHORT[k] for k in _SCEN_KEYS],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_SCEN_KEYS))
    for b in BUCKET_KEYS:
        c.write([_BUCKET_NAME[b]] + [f"={_ac.scenario_flag_cell(k, b)}" for k in _SCEN_KEYS],
                styles=[S_DEFAULT] + [S_LINK_NUM] * len(_SCEN_KEYS), outline_level=1)
    c.blank(2)

    # §3 Modeled shares by FY (gated Worktype by FY observed + shared adjustment)
    c.banner("§3 - Modeled bucket shares by FY (gated evidence + Inputs adjustment)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    share_cols = [_M_COL[fy] for fy in _FY_EVIDENCE] + [_M_WIN]
    pos["m_row"], pos["m_first"], pos["m_last"] = {}, {}, {}
    pos["m_unb"], pos["m_total"] = {}, {}
    sub = "a"
    for ck, cname, _li in _CLASSES:
        c.banner(f"§3{sub} - {cname} (= Worktype by FY observed + adjustment; FY26-27 use the window vector)",
                 n_cols=_NCOLS, style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Bucket", "Adj (Inputs)"] + [f"FY{fy}" for fy in _FY_EVIDENCE] + ["FY26-27 (window)"],
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (2 + len(_FY_EVIDENCE)))
        first = c.at()
        pos["m_row"][ck] = {}
        for b in BUCKET_KEYS:
            r = c.at()
            pos["m_row"][ck][b] = c.write(
                [_BUCKET_NAME[b], f"={_ac.bucket_adjustment_cell(b)}"]
                + [f"=N({wt_share_cell(ck, b, fy)})+$C{r}" for fy in _FY_EVIDENCE]
                + [f"=N({wt_window_share_cell(ck, b)})+$C{r}"],
                styles=[S_DEFAULT, S_LINK_PCT] + [S_PCT] * (1 + len(_FY_EVIDENCE)),
                outline_level=1)
        last = pos["m_row"][ck][BUCKET_KEYS[-1]]
        pos["m_first"][ck], pos["m_last"][ck] = first, last
        pos["m_unb"][ck] = c.write(
            ["Unbucketed / ambiguous", None]
            + [f"=1-SUM({col}{first}:{col}{last})" for col in share_cols],
            styles=[S_DEFAULT, S_DEFAULT] + [S_PCT] * len(share_cols), outline_level=1)
        pos["m_total"][ck] = c.total(
            ["Total modeled share", None]
            + [f"=SUM({col}{first}:{col}{pos['m_unb'][ck]})" for col in share_cols],
            styles=[S_BOLD, S_DEFAULT] + [S_PCT] * len(share_cols), n_cols=2 + len(share_cols))
        c.blank(2)
        sub = chr(ord(sub) + 1)

    # §3c Excluded roles (full corpus; from Entity Master)
    c.banner(f"§3{sub} - Excluded roles (full corpus - not supplier-addressable)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Role", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    for rk, label in _XROLES:
        c.write([label, f"={_em.role_dollar_cell(rk)}"], styles=[S_DEFAULT, S_LINK_NUM], outline_level=1)
    c.total(["Grand total (all recipients)", f"={_em.grand_total_cell()}"],
            styles=[S_BOLD, S_LINK_NUM], n_cols=2)
    c.blank(2)

    # §4 TAM bucket allocation (PRODUCER; per class at per-FY vectors, then combined)
    c.banner("§4 - TAM bucket allocation (annual class TAM x per-FY modeled share)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    tam_sum = "+".join(tam_total_cell(fy) for fy in _FY)
    pos["port_tam"] = c.write(["Portfolio TAM (Va + Col, both streams, FY22-27)", f"={tam_sum}"],
                              styles=[S_BOLD, S_NUM], outline_level=1)
    port = f"$C${pos['port_tam']}"
    c.blank()

    def _alloc(li: int, share_row: int) -> str:
        terms = [f"N({tam_cell(li, fy)})*{_m_col(fy)}{share_row}" for fy in _FY_EVIDENCE]
        terms.append(f"(N({tam_cell(li, 2026)})+N({tam_cell(li, 2027)}))*{_M_WIN}{share_row}")
        return "+".join(terms)

    sub = "a"
    pos["cls_alloc"], pos["cls_unb"], pos["cls_total"] = {}, {}, {}
    for ck, cname, li in _CLASSES:
        c.banner(f"§4{sub} - {cname} bucket TAM", n_cols=_NCOLS,
                 style=S_TITLE_SUBSECTION, mark_collapsible=True)
        c.blank()
        c.write(["Bucket", "Bucket TAM $M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
        first = c.at()
        pos["cls_alloc"][ck] = {}
        for b in BUCKET_KEYS:
            pos["cls_alloc"][ck][b] = c.write(
                [_BUCKET_NAME[b], f"={_alloc(li, pos['m_row'][ck][b])}"],
                styles=[S_DEFAULT, S_NUM], outline_level=1)
        pos["cls_unb"][ck] = c.write(
            ["Unbucketed / ambiguous", f"={_alloc(li, pos['m_unb'][ck])}"],
            styles=[S_DEFAULT, S_NUM], outline_level=1)
        pos["cls_total"][ck] = c.total(
            [f"{cname} TAM (all buckets)", f"=SUM(C{first}:C{pos['cls_unb'][ck]})"],
            styles=[S_BOLD, S_NUM], n_cols=2)
        c.blank()
        sub = chr(ord(sub) + 1)

    c.banner(f"§4{sub} - Combined bucket TAM (Virginia + Columbia)", n_cols=_NCOLS,
             style=S_TITLE_SUBSECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket", "Bucket TAM $M", "Effective share"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER])
    alloc = {}
    alloc_first = c.at()
    for b in BUCKET_KEYS:
        r = c.at()
        alloc[b] = c.write(
            [_BUCKET_NAME[b], f"=C{pos['cls_alloc']['va'][b]}+C{pos['cls_alloc']['col'][b]}",
             f"=C{r}/{port}"],
            styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    pos["alloc_unb"] = c.write(
        ["Unbucketed / ambiguous (not in scenario SAM)",
         f"=C{pos['cls_unb']['va']}+C{pos['cls_unb']['col']}", lambda r: f"=C{r}/{port}"],
        styles=[S_DEFAULT, S_NUM, S_PCT], outline_level=1)
    pos["alloc_total"] = c.total(["Total (7 buckets + unbucketed = TAM)",
                                  f"=SUM(C{alloc_first}:C{pos['alloc_unb']})", None],
                                 styles=[S_BOLD, S_NUM, S_DEFAULT], n_cols=3)
    pos["alloc"] = alloc
    pos["alloc_first"], pos["alloc_last"] = alloc_first, alloc[BUCKET_KEYS[-1]]
    c.blank(2)

    # §5 Scenario SAM output (PRODUCER; avg annual shown first per the deck contract)
    c.banner("§5 - Scenario SAM", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "Avg annual $M", "Cumulative SAM $M", "% of TAM"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    brange = f"'{tab}'!C{alloc_first}:C{pos['alloc_last']}"
    nyears = n_years_cell()
    scen = {}
    sam_first = c.at()
    for k in _SCEN_KEYS:
        if k == "modular":
            # entity-tag-driven per class: class TAM x gated modular share
            sam = (f"N(C{pos['cls_total']['va']})*N({wt_modular_share_cell('va')})"
                   f"+N(C{pos['cls_total']['col']})*N({wt_modular_share_cell('col')})")
        else:
            sam = f"SUMPRODUCT({brange},{_ac.scenario_flag_range(k)})"
        # C = avg annual (cumulative / n_years), D = cumulative SAM, E = % of TAM
        scen[k] = c.write([_ac.scenario_name(k), lambda r: f"=D{r}/{nyears}", f"={sam}",
                           lambda r: f"=D{r}/{port}"],
                          styles=[S_DEFAULT, S_NUM, S_NUM, S_PCT], outline_level=1)
    pos["scen"] = scen
    pos["sam_first"], pos["sam_last"] = sam_first, c.at() - 1
    c.blank(2)

    # §6 Selected scenario (PRODUCER; driven by the Default SAM scenario control)
    c.banner("§6 - Selected scenario", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Selected scenario", "Avg annual $M", "Cumulative SAM $M", "% of TAM"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_CENTER, S_HEADER_CENTER])
    sel = _ac.selected_sam_scenario_cell()
    nr = f"B{sam_first}:B{pos['sam_last']}"
    ar = f"C{sam_first}:C{pos['sam_last']}"     # avg annual
    sr = f"D{sam_first}:D{pos['sam_last']}"     # cumulative SAM
    pr = f"E{sam_first}:E{pos['sam_last']}"     # % of TAM
    pos["sel"] = c.write([f"={sel}", f"=INDEX({ar},MATCH({sel},{nr},0))",
                          f"=INDEX({sr},MATCH({sel},{nr},0))", f"=INDEX({pr},MATCH({sel},{nr},0))"],
                         styles=[S_DEFAULT, S_NUM, S_NUM, S_PCT], outline_level=1)
    c.blank(2)

    # §7 Annual SAM by FY (PRODUCER; per-class annual TAM x that FY's vectors)
    c.banner("§7 - Annual SAM by fiscal year", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Fiscal year", "Annual TAM $M"] + [_SHORT[k] for k in _SCEN_KEYS],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER] + [S_HEADER_CENTER] * len(_SCEN_KEYS))
    ann = {}
    ann_scen_col = {k: col_letter(3 + i) for i, k in enumerate(_SCEN_KEYS)}   # D, E, F, ...
    ann_first = c.at()

    def _cls_factor(ck: str, fy: int, k: str) -> str:
        col = _m_col(fy)
        return (f"SUMPRODUCT({col}{pos['m_first'][ck]}:{col}{pos['m_last'][ck]},"
                f"{_ac.scenario_flag_range(k)})")

    for fy in _FY:
        # annual scenario SAM = sum over classes of class TAM(fy) x SUMPRODUCT(that
        # FY's class vector, scenario flags); modular is entity-tag-driven per class
        vals = [f"FY{fy}", f"={tam_total_cell(fy)}"]
        for k in _SCEN_KEYS:
            if k == "modular":
                vals.append(f"=N({tam_cell(2013, fy)})*N({wt_modular_share_cell('va')})"
                            f"+N({tam_cell(1045, fy)})*N({wt_modular_share_cell('col')})")
            else:
                vals.append(f"=N({tam_cell(2013, fy)})*{_cls_factor('va', fy, k)}"
                            f"+N({tam_cell(1045, fy)})*{_cls_factor('col', fy, k)}")
        ann[fy] = c.write(vals, styles=[S_DEFAULT, S_LINK_NUM] + [S_NUM] * len(_SCEN_KEYS),
                          outline_level=1)
    pos["ann"], pos["ann_scen_col"] = ann, ann_scen_col
    pos["ann_first"], pos["ann_last"] = ann_first, c.at() - 1
    c.blank(2)

    # §8 SAM checks
    c.banner("§8 - SAM checks", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Check", "Status"], styles=S_HEADER_LEFT)
    bt = f"'{tab}'!C{pos['alloc_total']}"
    pt = f"'{tab}'!C{pos['port_tam']}"
    ut = f"'{tab}'!C{pos['alloc_unb']}"
    broad = f"'{tab}'!D{scen['broad']}"     # cumulative broad SAM (col D)
    for ck, cname, _li in _CLASSES:
        tr = pos["m_total"][ck]
        conds = ",".join(f"ABS({col}{tr}-1)<0.001" for col in share_cols)
        c.write([f"{cname} modeled shares sum to 100% (all FY columns)",
                 f'=IF(AND({conds}),"OK","FAIL")'],
                styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Bucketed TAM = portfolio TAM", f'=IF(ABS({bt}-{pt})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Broad SAM = TAM - unbucketed", f'=IF(ABS({broad}-({pt}-{ut}))<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Broad SAM <= TAM", f'=IF({broad}<={pt}+0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    _bc = ann_scen_col["broad"]
    _bsum = f"SUM({_bc}{ann_first}:{_bc}{pos['ann_last']})"
    c.write(["Annual broad SAM sums to cumulative", f'=IF(ABS({_bsum}-{broad})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    return c.rows, pos, c.at()


# ── Import-time layout pass ───────────────────────────────────────────────────
_body_rows, _P, _after_body = _build_body(_TAB, _BASE)


# ── Accessors (load-bearing) ─────────────────────────────────────────────────

def portfolio_tam_cell(): return f"'{_TAB}'!C{_P['port_tam']}"


def bucket_tam_cell(b):
    if b not in _P["alloc"]:
        raise ValueError(f"Unknown bucket {b!r}")
    return f"'{_TAB}'!C{_P['alloc'][b]}"


def bucket_tam_range(): return f"'{_TAB}'!C{_P['alloc_first']}:C{_P['alloc_last']}"
def unbucketed_tam_cell(): return f"'{_TAB}'!C{_P['alloc_unb']}"
def bucketed_total_cell(): return f"'{_TAB}'!C{_P['alloc_total']}"
def va_modeled_share_total_cell(): return f"'{_TAB}'!{_M_WIN}{_P['m_total']['va']}"
def col_modeled_share_total_cell(): return f"'{_TAB}'!{_M_WIN}{_P['m_total']['col']}"
def class_bucket_tam_cell(ck, b): return f"'{_TAB}'!C{_P['cls_alloc'][ck][b]}"
def class_unbucketed_tam_cell(ck): return f"'{_TAB}'!C{_P['cls_unb'][ck]}"
def class_tam_total_cell(ck): return f"'{_TAB}'!C{_P['cls_total'][ck]}"


def sam_cell(k):                                  # cumulative SAM (col D)
    if k not in _P["scen"]:
        raise ValueError(f"Unknown scenario {k!r}")
    return f"'{_TAB}'!D{_P['scen'][k]}"


def sam_pct_cell(k): return f"'{_TAB}'!E{_P['scen'][k]}"      # % of TAM (col E)
def avg_annual_sam_cell(k): return f"'{_TAB}'!C{_P['scen'][k]}"   # avg annual (col C)
def scenario_keys_ordered(): return list(_SCEN_KEYS)
def first_scenario_row(): return _P["sam_first"]
def last_scenario_row(): return _P["sam_last"]
def selected_sam_cell(): return f"'{_TAB}'!D{_P['sel']}"
def selected_sam_pct_cell(): return f"'{_TAB}'!E{_P['sel']}"
def selected_avg_annual_sam_cell(): return f"'{_TAB}'!C{_P['sel']}"


def annual_sam_cell(k, fy):
    """Annual scenario SAM for fiscal year fy (lumpy per-FY cadence; §7)."""
    if k not in _P["ann_scen_col"]:
        raise ValueError(f"Unknown scenario {k!r}")
    if fy not in _P["ann"]:
        raise ValueError(f"FY {fy!r} outside {_FY!r}")
    return f"'{_TAB}'!{_P['ann_scen_col'][k]}{_P['ann'][fy]}"


def annual_broad_sam_cell(fy): return annual_sam_cell("broad", fy)
def annual_sam_fy_columns(): return list(_FY)


# ── Render ───────────────────────────────────────────────────────────────────

def _render_sam_build() -> WorksheetSpec:
    n_cols = _NCOLS
    c = RowCursor(2)
    c.banner("SAM Build", n_cols=n_cols, style=S_TITLE_SHEET)
    c.blank()
    c.banner("§1 - SAM scenario menu", n_cols=n_cols, style=S_TITLE_SECTION)
    c.blank()
    c.write(["Measure", "Value"], styles=S_HEADER_LEFT)
    c.write(["Broad component-mfg SAM (avg annual FY22-27)", f"={avg_annual_sam_cell('broad')}"],
            styles=[S_BOLD, S_NUM])
    c.write(["Broad component-mfg SAM (FY22-27 cumulative)", f"={sam_cell('broad')}"],
            styles=[S_DEFAULT, S_NUM])
    c.write(["Broad SAM as % of TAM", f"={sam_pct_cell('broad')}"],
            styles=[S_DEFAULT, S_PCT])
    c.write(["Selected SAM scenario", f"={_ac.selected_sam_scenario_cell()}"],
            styles=[S_DEFAULT, S_LINK_NUM])
    c.write(["Selected SAM (avg annual)", f"={selected_avg_annual_sam_cell()}"],
            styles=[S_BOLD, S_NUM])
    c.blank(2)

    assert c.at() == _BASE, f"at-a-glance ends at {c.at()}, expected {_BASE}"
    c.feed(_body_rows, _after_body)

    return WorksheetSpec(worksheet(c.rows, cols=[44, 22, 14, 14, 14, 12, 12],
                         tab_color=group_color(_GROUP), with_gutter=True))


SAM_BUILD = SheetEntry(_TAB, _GROUP, _render_sam_build)
