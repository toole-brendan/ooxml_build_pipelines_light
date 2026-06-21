"""data_worktype_by_fy - the "Worktype by FY" tab (DDG, data group; one module = one sheet).

The gated work-type share evidence: supplier-addressable subaward dollars by bucket
and subaward action FY, restricted to (1) yard construction PIIDs (GD-BIW +
HII-Ingalls prime groups - GFE / combat-system prime chains are excluded because the
TAM removes the GFE stream before the BC base) and (2) the FY2022-FY2025 action-year
window (complete reporting years inside the TAM window; partial FY2026 excluded).

Every figure is a live SUMPRODUCT over the Entity Master table's per-entity Yard
columns (the gate is visible per vendor there); §5 ties gated + excluded dollars
back to the Entity Master supplier-addressable total in live arithmetic. The
module's only Python pass is an import-time guard asserting no gated bucket/FY
cell is negative (de-obligations exceeding obligations).

Promoted accessors (consumed by SAM Build):
  wt_fy_columns, wt_share_cell(bucket, fy), wt_window_share_cell(bucket),
  wt_addressable_cell(fy), wt_window_addressable_cell, wt_modular_share_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_PCT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._taxonomy import BUCKETS, BUCKET_KEYS, UNBUCKETED
from workbook_master_tam.sheets.ddg.data_entity_master import (
    classified_records, _piid_groups, YARD_GROUPS, WT_FY_WINDOW,
    role_range as _role, bucket_range as _bkt, ent_dollar_range as _dol,
    modular_range as _mod, yard_dollar_range as _yard, yard_fy_range as _yfy,
)
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "data"
_TAB = "DDG Worktype by FY"
_NCOLS = 2 + len(WT_FY_WINDOW)                    # label + 4 FY + window total
_ROW_KEYS = BUCKET_KEYS + [UNBUCKETED]
_BUCKET_NAME = {k: name for k, name, _ in BUCKETS}
_BUCKET_NAME[UNBUCKETED] = "Unbucketed / ambiguous"
_FY_COL = {fy: col_letter(2 + i) for i, fy in enumerate(WT_FY_WINDOW)}   # C..F
_WIN_COL = col_letter(2 + len(WT_FY_WINDOW))                             # G
_Q = '"'


def _sp(*m):
    return f"SUMPRODUCT({'*'.join(m)})"


def _supplier():
    return f"({_role()}={_Q}supplier{_Q})"


def _guard_no_negative_cells():
    """Import-time guard: no gated bucket/FY cell may be negative."""
    grp = _piid_groups()
    M = {b: {fy: 0.0 for fy in WT_FY_WINDOW} for b in _ROW_KEYS}
    for rec in classified_records():
        if (rec["role"] != "supplier" or grp.get(rec["piid"]) not in YARD_GROUPS
                or rec["fy"] not in M[rec["bucket"]]):
            continue
        M[rec["bucket"]][rec["fy"]] += rec["dollar_m"]
    for b in _ROW_KEYS:
        for fy in WT_FY_WINDOW:
            assert M[b][fy] >= 0.0, f"negative gated cell {b}/{fy}: {M[b][fy]}"


_guard_no_negative_cells()


def _make_worktype_by_fy():
    P: dict = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Evidence basis
    c.banner("§1 - Evidence basis (gated share evidence)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    for field, value in [
        ("Source", "Entity Master per-entity Yard columns (live SUMPRODUCTs; no figures re-keyed here)"),
        ("Prime scope", "Yard construction PIIDs (GD-BIW + HII-Ingalls); GFE / combat-system prime chains excluded"),
        ("FY window", "FY2022-FY2025 subaward action years (complete reporting years; partial FY2026 excluded)"),
        ("Feeds", "SAM Build per-FY bucket shares -> tab"),
    ]:
        c.write([field, value], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Observed supplier $ by bucket x FY (gated; live over Entity Master)
    c.banner("§2 - Observed supplier $M by bucket x subaward FY (gated)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket"] + [f"FY{fy}" for fy in WT_FY_WINDOW] + ["FY22-25"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(WT_FY_WINDOW) + 1))
    P["dollar"] = {}
    for b in _ROW_KEYS:
        bmask = f"({_bkt()}={_Q}{b}{_Q})"
        P["dollar"][b] = c.write(
            [_BUCKET_NAME[b]]
            + [f"={_sp(_supplier(), bmask, _yfy(fy))}" for fy in WT_FY_WINDOW]
            + [lambda r: f"=SUM(C{r}:{_FY_COL[WT_FY_WINDOW[-1]]}{r})"],
            styles=[S_DEFAULT] + [S_NUM] * (len(WT_FY_WINDOW) + 1), outline_level=1)
    d_first, d_last = P["dollar"][_ROW_KEYS[0]], P["dollar"][_ROW_KEYS[-1]]
    P["dollar_total"] = c.total(
        ["Supplier-addressable total (gated)"]
        + [f"=SUM({_FY_COL[fy]}{d_first}:{_FY_COL[fy]}{d_last})" for fy in WT_FY_WINDOW]
        + [f"=SUM({_WIN_COL}{d_first}:{_WIN_COL}{d_last})"],
        styles=[S_DEFAULT] + [S_NUM] * (len(WT_FY_WINDOW) + 1), n_cols=_NCOLS)
    c.blank(2)

    # §3 Observed shares by FY (= column $ / column addressable)
    c.banner("§3 - Observed bucket shares by FY", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Bucket"] + [f"FY{fy}" for fy in WT_FY_WINDOW] + ["FY22-25"],
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * (len(WT_FY_WINDOW) + 1))
    tot = P["dollar_total"]
    P["share"] = {}
    for b in _ROW_KEYS:
        dr = P["dollar"][b]
        P["share"][b] = c.write(
            [_BUCKET_NAME[b]]
            + [f"={col}{dr}/{col}${tot}" for col in
               [_FY_COL[fy] for fy in WT_FY_WINDOW] + [_WIN_COL]],
            styles=[S_DEFAULT] + [S_PCT] * (len(WT_FY_WINDOW) + 1), outline_level=1)
    s_first, s_last = P["share"][_ROW_KEYS[0]], P["share"][_ROW_KEYS[-1]]
    c.total(["Total"]
            + [f"=SUM({col}{s_first}:{col}{s_last})" for col in
               [_FY_COL[fy] for fy in WT_FY_WINDOW] + [_WIN_COL]],
            styles=[S_DEFAULT] + [S_PCT] * (len(WT_FY_WINDOW) + 1), n_cols=_NCOLS)
    c.blank(2)

    # §4 Modular tag (entity-flagged scenario evidence, same gate + window)
    c.banner("§4 - Modular tag (gated window)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    win_sum = "+".join(_yfy(fy) for fy in WT_FY_WINDOW)
    r_mod = c.write(["Modular-flagged supplier $M (flagged entities sit under GFE-chain primes)",
                     f"={_sp(_supplier(), f'({_mod()}=1)', f'({win_sum})')}"],
                    styles=[S_DEFAULT, S_NUM], outline_level=1)
    P["mod_share"] = c.write(["Modular share of gated window", f"=C{r_mod}/{_WIN_COL}{tot}"],
                             styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.blank(2)

    # §5 Reconciliation to Entity Master (gated + excluded = supplier-addressable)
    c.banner("§5 - Reconciliation to Entity Master", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Measure", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    r_em = c.write(["Entity Master supplier-addressable total (all primes, all years)",
                    f"={_sp(_supplier(), _dol())}"],
                   styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_yard = c.write(["Yard-PIID supplier $M (all years)", f"={_sp(_supplier(), _yard())}"],
                     styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_gated = c.write(["Gated evidence base (in-window yard supplier $)", f"={_WIN_COL}{tot}"],
                      styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_nonyard = c.write(["Excluded - GFE / combat-system prime chains (all years)",
                         f"=C{r_em}-C{r_yard}"],
                        styles=[S_DEFAULT, S_NUM], outline_level=1)
    r_oow = c.write(["Excluded - yard records outside FY2022-FY2025", f"=C{r_yard}-C{r_gated}"],
                    styles=[S_DEFAULT, S_NUM], outline_level=1)
    c.write(["Tie check (gated + excluded = supplier total)",
             f'=IF(ABS(C{r_gated}+C{r_nonyard}+C{r_oow}-C{r_em})<0.5,"OK","FAIL")'],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 12, 12, 12, 12, 12],
                       tab_color=group_color(_GROUP), with_gutter=True)
        return WorksheetSpec(ws)

    def _check(bucket: str, fy: int | None = None) -> None:
        if bucket not in P["share"]:
            raise ValueError(f"Unknown bucket {bucket!r}")
        if fy is not None and fy not in _FY_COL:
            raise ValueError(f"FY {fy!r} outside {WT_FY_WINDOW!r}")

    def wt_fy_columns() -> list:
        return list(WT_FY_WINDOW)

    def wt_share_cell(bucket: str, fy: int) -> str:
        _check(bucket, fy)
        return f"'{_TAB}'!{_FY_COL[fy]}{P['share'][bucket]}"

    def wt_window_share_cell(bucket: str) -> str:
        _check(bucket)
        return f"'{_TAB}'!{_WIN_COL}{P['share'][bucket]}"

    def wt_addressable_cell(fy: int) -> str:
        if fy not in _FY_COL:
            raise ValueError(f"FY {fy!r} outside {WT_FY_WINDOW!r}")
        return f"'{_TAB}'!{_FY_COL[fy]}{P['dollar_total']}"

    def wt_window_addressable_cell() -> str:
        return f"'{_TAB}'!{_WIN_COL}{P['dollar_total']}"

    def wt_modular_share_cell() -> str:
        return f"'{_TAB}'!C{P['mod_share']}"

    return (SheetEntry(_TAB, _GROUP, render), wt_fy_columns, wt_share_cell,
            wt_window_share_cell, wt_addressable_cell, wt_window_addressable_cell,
            wt_modular_share_cell)


(WORKTYPE_BY_FY, wt_fy_columns, wt_share_cell, wt_window_share_cell,
 wt_addressable_cell, wt_window_addressable_cell,
 wt_modular_share_cell) = _make_worktype_by_fy()
