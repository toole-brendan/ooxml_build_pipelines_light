"""data_worktype_by_fy - the "Worktype by FY" tab (one module = one sheet).

The gated work-type share evidence, per class: supplier-addressable subaward
dollars by bucket and subaward action FY for Virginia and Columbia separately,
restricted to (1) GDEB construction/LLTM PIIDs (BPMI / LM / BAE / RR prime records
are excluded - reactor components and combat systems sit in streams the TAM
removes before the BC base) and (2) the FY2022-FY2025 action-year window (complete
reporting years inside the TAM window; FY2026 has no usable reporting yet).

Every figure is a live SUMPRODUCT over the Entity Master table's per-entity
Va/Col FY columns (the gate is visible per vendor there); §7 ties gated + excluded
dollars back to the Entity Master supplier-addressable total in live arithmetic.
The module's only Python pass is an import-time guard asserting no gated
class/bucket/FY cell is negative (de-obligations exceeding obligations).

Promoted accessors (consumed by SAM Build; cls in {'va', 'col'}):
  wt_fy_columns, wt_share_cell(cls, bucket, fy), wt_window_share_cell(cls, bucket),
  wt_addressable_cell(cls, fy), wt_window_addressable_cell(cls),
  wt_modular_share_cell(cls)
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_submarines.sheets.taxonomy import BUCKETS, BUCKET_KEYS, UNBUCKETED
from workbook_submarines.sheets.data_entity_master import (
    classified_records, _piid_meta, WT_FY_WINDOW, WT_CLASSES,
    role_range as _role, bucket_range as _bkt, ent_dollar_range as _dol,
    modular_range as _mod, gdeb_dollar_range as _gdeb, class_fy_range as _cfy,
)
from workbook_submarines.sheets._layout import RowCursor

_GROUP = "data"
_TAB = "Worktype by FY"
_NCOLS = 2 + len(WT_FY_WINDOW)                    # label + 4 FY + window total
_ROW_KEYS = BUCKET_KEYS + [UNBUCKETED]
_BUCKET_NAME = {k: name for k, name, _ in BUCKETS}
_BUCKET_NAME[UNBUCKETED] = "Unbucketed / ambiguous"
_FY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(WT_FY_WINDOW)}   # C..F
_WIN_COL = col_letter(2 + len(WT_FY_WINDOW))                             # G
_CLS_NAME = dict(WT_CLASSES)
_Q = '"'


def _sp(*m):
    return f"SUMPRODUCT({'*'.join(m)})"


def _supplier():
    return f"({_role()}={_Q}supplier{_Q})"


def _guard_no_negative_cells():
    """Import-time guard: no gated class/bucket/FY cell may be negative."""
    meta = _piid_meta()
    cls_key = {name: key for key, name in WT_CLASSES}
    M = {ck: {b: {fy: 0.0 for fy in WT_FY_WINDOW} for b in _ROW_KEYS}
         for ck, _n in WT_CLASSES}
    for rec in classified_records():
        prime, cls = meta.get(rec["piid"], ("", ""))
        ck = cls_key.get(cls)
        if (rec["role"] != "supplier" or prime != "GDEB" or ck is None
                or rec["fy"] not in WT_FY_WINDOW):
            continue
        M[ck][rec["bucket"]][rec["fy"]] += rec["dollar_m"]
    for ck, _n in WT_CLASSES:
        for b in _ROW_KEYS:
            for fy in WT_FY_WINDOW:
                assert M[ck][b][fy] >= 0.0, f"negative gated cell {ck}/{b}/{fy}: {M[ck][b][fy]}"


_guard_no_negative_cells()


def _make_worktype_by_fy():
    P: dict = {"dollar": {}, "dollar_total": {}, "share": {}, "mod_share": {}}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Evidence basis
    c.banner("§1 - Evidence basis (gated share evidence)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for field, value in [
        ("Source", "Entity Master per-entity Va/Col FY columns (live SUMPRODUCTs; no figures re-keyed here)"),
        ("Prime scope", "GDEB construction/LLTM PIIDs; BPMI / LM / BAE / RR prime records excluded"),
        ("Class split", "Virginia vs Columbia per the scope map's PIID class"),
        ("FY window", "FY2022-FY2025 subaward action years (complete reporting years; FY2026 has no usable reporting yet)"),
        ("Feeds", "SAM Build per-class per-FY bucket shares -> tab"),
    ]:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2/§3 Virginia, §4/§5 Columbia: $ grid + share grid per class
    section = 2
    for ck, cname in WT_CLASSES:
        c.banner(f"§{section} - {cname}: observed supplier $M by bucket x subaward FY (gated)",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Bucket"] + [f"FY{fy}" for fy in WT_FY_WINDOW] + ["FY22-25"],
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(WT_FY_WINDOW) + 1))
        P["dollar"][ck] = {}
        for b in _ROW_KEYS:
            bmask = f"({_bkt()}={_Q}{b}{_Q})"
            P["dollar"][ck][b] = c.write(
                [_BUCKET_NAME[b]]
                + [f"={_sp(_supplier(), bmask, _cfy(ck, fy))}" for fy in WT_FY_WINDOW]
                + [lambda r: f"=SUM(C{r}:{_FY_COL[WT_FY_WINDOW[-1]]}{r})"],
                styles=[S_DEFAULT] + [S_NUM] * (len(WT_FY_WINDOW) + 1), outline_level=1)
        d_first = P["dollar"][ck][_ROW_KEYS[0]]
        d_last = P["dollar"][ck][_ROW_KEYS[-1]]
        P["dollar_total"][ck] = c.total(
            [f"{cname} supplier-addressable total (gated)"]
            + [f"=SUM({_FY_COL[fy]}{d_first}:{_FY_COL[fy]}{d_last})" for fy in WT_FY_WINDOW]
            + [f"=SUM({_WIN_COL}{d_first}:{_WIN_COL}{d_last})"],
            styles=[S_DEFAULT] + [S_NUM] * (len(WT_FY_WINDOW) + 1), n_cols=_NCOLS)
        c.blank(2)
        section += 1

        c.banner(f"§{section} - {cname}: observed bucket shares by FY",
                 n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
        c.blank()
        c.write(["Bucket"] + [f"FY{fy}" for fy in WT_FY_WINDOW] + ["FY22-25"],
                styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(WT_FY_WINDOW) + 1))
        tot = P["dollar_total"][ck]
        P["share"][ck] = {}
        for b in _ROW_KEYS:
            dr = P["dollar"][ck][b]
            P["share"][ck][b] = c.write(
                [_BUCKET_NAME[b]]
                + [f"={col}{dr}/{col}${tot}" for col in
                   [_FY_COL[fy] for fy in WT_FY_WINDOW] + [_WIN_COL]],
                styles=[S_DEFAULT] + [S_PCT] * (len(WT_FY_WINDOW) + 1), outline_level=1)
        s_first = P["share"][ck][_ROW_KEYS[0]]
        s_last = P["share"][ck][_ROW_KEYS[-1]]
        c.total(["Total"]
                + [f"=SUM({col}{s_first}:{col}{s_last})" for col in
                   [_FY_COL[fy] for fy in WT_FY_WINDOW] + [_WIN_COL]],
                styles=[S_DEFAULT] + [S_PCT] * (len(WT_FY_WINDOW) + 1), n_cols=_NCOLS)
        c.blank(2)
        section += 1

    # §6 Modular tag per class (entity-flagged scenario evidence, same gate + window)
    c.banner(f"§{section} - Modular tag (gated window, per class)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    for ck, cname in WT_CLASSES:
        win_sum = "+".join(_cfy(ck, fy) for fy in WT_FY_WINDOW)
        r_mod = c.write([f"{cname} modular-flagged supplier $M (gated window)",
                         f"={_sp(_supplier(), f'({_mod()}=1)', f'({win_sum})')}"],
                        styles=[S_DEFAULT, S_NUM], outline_level=1)
        P["mod_share"][ck] = c.write(
            [f"{cname} modular share of gated window", f"=C{r_mod}/{_WIN_COL}{P['dollar_total'][ck]}"],
            styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank(2)
    section += 1

    # §7 Reconciliation to Entity Master (gated + excluded = supplier-addressable)
    c.banner(f"§{section} - Reconciliation to Entity Master", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    r_em = c.write(["Entity Master supplier-addressable total (all primes, all years)",
                    f"={_sp(_supplier(), _dol())}"],
                   styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_gdeb = c.write(["GDEB-PIID supplier $M (all years)", f"={_sp(_supplier(), _gdeb())}"],
                     styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_va = c.write(["Gated Virginia evidence base (in-window)",
                    f"={_WIN_COL}{P['dollar_total']['va']}"],
                   styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_col = c.write(["Gated Columbia evidence base (in-window)",
                     f"={_WIN_COL}{P['dollar_total']['col']}"],
                    styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_nongdeb = c.write(["Excluded - non-GDEB prime records (all years)", f"=C{r_em}-C{r_gdeb}"],
                        styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_oow = c.write(["Excluded - GDEB records outside FY2022-FY2025",
                     f"=C{r_gdeb}-C{r_va}-C{r_col}"],
                    styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.write(["Tie check (gated + excluded = supplier total)",
             f'=IF(ABS(C{r_va}+C{r_col}+C{r_nongdeb}+C{r_oow}-C{r_em})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 12, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def _check(cls: str, bucket: str | None = None, fy: int | None = None) -> None:
        if cls not in P["share"]:
            raise ValueError(f"Unknown class {cls!r}; expected 'va' or 'col'")
        if bucket is not None and bucket not in P["share"][cls]:
            raise ValueError(f"Unknown bucket {bucket!r}")
        if fy is not None and fy not in _FY_COL:
            raise ValueError(f"FY {fy!r} outside {WT_FY_WINDOW!r}")

    def wt_fy_columns() -> list:
        return list(WT_FY_WINDOW)

    def wt_share_cell(cls: str, bucket: str, fy: int) -> str:
        _check(cls, bucket, fy)
        return f"'{_TAB}'!{_FY_COL[fy]}{P['share'][cls][bucket]}"

    def wt_window_share_cell(cls: str, bucket: str) -> str:
        _check(cls, bucket)
        return f"'{_TAB}'!{_WIN_COL}{P['share'][cls][bucket]}"

    def wt_addressable_cell(cls: str, fy: int) -> str:
        _check(cls, fy=fy)
        return f"'{_TAB}'!{_FY_COL[fy]}{P['dollar_total'][cls]}"

    def wt_window_addressable_cell(cls: str) -> str:
        _check(cls)
        return f"'{_TAB}'!{_WIN_COL}{P['dollar_total'][cls]}"

    def wt_modular_share_cell(cls: str) -> str:
        _check(cls)
        return f"'{_TAB}'!C{P['mod_share'][cls]}"

    return (SheetEntry(_TAB, _GROUP, render), wt_fy_columns, wt_share_cell,
            wt_window_share_cell, wt_addressable_cell, wt_window_addressable_cell,
            wt_modular_share_cell)


(WORKTYPE_BY_FY, wt_fy_columns, wt_share_cell, wt_window_share_cell,
 wt_addressable_cell, wt_window_addressable_cell,
 wt_modular_share_cell) = _make_worktype_by_fy()
