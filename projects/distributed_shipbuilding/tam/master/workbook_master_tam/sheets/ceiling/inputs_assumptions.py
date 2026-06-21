"""inputs_assumptions - the "Assumptions" tab (inputs group).

The SINGLE edit surface. Every number a reviewer would challenge is a blue input
here, each carrying its sourced basis as a native Excel Note (hover card) on the
value cell. Three sections:
  §1 Run settings        - scope / window / units / lead frame (labels).
  §2 Core parameters     - per class: h (outsourceable labor-hour share) and
                           L (shipyard labor share of BC); plus p (pass-through
                           material share, the bridge knob). core = L*(1-h),
                           ceiling = 1-core are derived downstream on Ceiling Model.
  §3 Current-state anchors- per-class current off-team POP %, and the make/buy
                           reference band (the footnote frame).

Accessors (load-bearing; consumed by Ceiling Model / Bridge / Headroom):
  core_h_cell(cls) / labor_share_cell(cls) / passthrough_cell() /
  pop_current_cell(cls) / makebuy_cell(bound).
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_PCT, S_PCT_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ceiling._layout import RowCursor
from workbook_master_tam.sheets.ceiling.data_cost_base import (
    bc_cumulative_cell, total_cumulative_cell,
)

_GROUP = "inputs"
_TAB = "Ceiling Assumptions"

CLASSES = ["Virginia", "Columbia", "DDG-51"]
_CLASS_COL = {cls: 2 + i for i, cls in enumerate(CLASSES)}   # Virginia=C, Columbia=D, DDG-51=E
_NCOLS = 1 + len(CLASSES)                                     # label + 3 classes (B..E)


def _ccol(cls: str) -> str:
    return col_letter(_CLASS_COL[cls])


def _dv_decimal(sqref: str, lo, hi) -> str:
    return (f'<dataValidation type="decimal" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}">'
            f'<formula1>{lo}</formula1><formula2>{hi}</formula2></dataValidation>')


def _build():
    P = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Run settings
    c.banner("§1 - Run settings", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Setting", "Value"], styles=[S_HEADER_LEFT, S_HEADER_LEFT])
    c.write(["Program scope", ", ".join(CLASSES)], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["FY window", "FY2022-2027"], styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Units", "Then-year $M (P-5c as reported); ratios unit-invariant"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Lead frame", "POP / distributed (make/buy = reference footnote)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Core parameters (per class)
    c.banner("§2 - Core parameters (share of Basic Construction)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Parameter"] + CLASSES,
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(CLASSES))
    P["h"] = c.write(["h - outsourceable labor-hour share", 0.50, 0.50, 0.55],
                     styles=[S_DEFAULT] + [S_PCT_INPUT] * len(CLASSES), outline_level=1)
    P["L"] = c.write(["L - shipyard labor share of BC", 0.50, 0.50, 0.45],
                     styles=[S_DEFAULT] + [S_PCT_INPUT] * len(CLASSES), outline_level=1)
    c.blank()
    c.write(["Selected material pass-through", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["p"] = c.write(["p - pass-through material in outsourced packages", 0.50],
                     styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    c.blank()

    # L rebase (reference, not a knob): the 40% labor figure (A2/A3) is of TOTAL
    # ship cost; BC excludes most GFE, so labor's share of BC is higher. Show the
    # implied upper bound (40% / BC-share-of-total) and the haircut to the selected
    # 50%/45%, so those L inputs are auditable rather than asserted.
    _bc_sum = "+".join(bc_cumulative_cell(cls) for cls in CLASSES)
    _tot_sum = "+".join(total_cumulative_cell(cls) for cls in CLASSES)
    c.write(["L rebase: 40% of total cost to share of BC", "Value"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _ls = c.write(["Labor share of total ship cost (CRS/CBO, A2/A3)", 0.40],
                  styles=[S_DEFAULT, S_PCT], outline_level=1)
    _bcsh = c.write(["Portfolio BC / total ship cost (Cost Base)",
                     f"=({_bc_sum})/({_tot_sum})"],
                    styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.write(["Implied L of BC if all labor sat in BC", f"=C{_ls}/C{_bcsh}"],
            styles=[S_DEFAULT, S_PCT], outline_level=1)
    c.write(["Selected L of BC: subs 50% / DDG 45% (see L above)"],
            styles=[S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 Current-state anchors
    c.banner("§3 - Current-state anchors (reference)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Anchor"] + CLASSES,
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(CLASSES))
    P["pop"] = c.write(["Current off-team work (announced POP)", 0.34, 0.22, 0.13],
                       styles=[S_DEFAULT] + [S_PCT_INPUT] * len(CLASSES), outline_level=1)
    c.blank()
    c.write(["Make/buy bought-out band (share of BC, all classes)", "Value"],
            styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["mb_low"] = c.write(["Low", 0.50], styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    P["mb_mid"] = c.write(["Mid", 0.60], styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    P["mb_high"] = c.write(["High", 0.65], styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)

    # Data-validation: every blue share lives in [0, 1].
    dvs = [
        _dv_decimal(f"C{P['h']}:E{P['L']}", 0, 1),
        _dv_decimal(f"C{P['p']}", 0, 1),
        _dv_decimal(f"C{P['pop']}:E{P['pop']}", 0, 1),
        _dv_decimal(f"C{P['mb_low']}:C{P['mb_high']}", 0, 1),
    ]

    # Source/basis hovers anchored on the value cells they explain.
    notes = [
        ExcelNote(f"C{P['h']}",
                  "Virginia/Columbia h=0.50: RADM Jon Rucker (PEO Attack Submarines), Defense News "
                  "2022-10-21 - EB+NNS outsourced hours grow 2M->5M = 'half the work to build a Virginia "
                  "submarine'. Labor-hours basis; a forward capacity-relief target, not a measured "
                  "make/buy split. See Sources A1."),
        ExcelNote(f"E{P['h']}",
                  "DDG-51 h=0.55 (analyst assumption, not the Rucker submarine figure): no reactor, larger "
                  "separable GFE, and more amenable to distributed block builds -> a higher outsourceable-"
                  "hour ceiling than the nuclear submarines. Carrier (CVN-80) ~20% of structural units "
                  "outsourced and rising is the nearest non-nuclear datapoint."),
        ExcelNote(f"C{P['L']}",
                  "L=0.50 of BC: O'Rourke (CRS, 2025-03-11) 'shipyard labor ~40% of a military ship's total "
                  "procurement cost'; since BC excludes most GFE, labor's share of BC is higher than 40%. "
                  "CBO Shipbuilding Composite Index (2024) puts shipbuilder labor at 39-48%. See Sources A2/A3."),
        ExcelNote(f"E{P['L']}",
                  "DDG-51 L=0.45 (analyst assumption): non-nuclear mix with a larger separable GFE layer, so "
                  "labor is a somewhat smaller share of BC than on the nuclear boats. Sensitivity tab sweeps L."),
        ExcelNote(f"C{P['p']}",
                  "p = share of an outsourced package's material that travels with it (a tier-2 fabricator "
                  "buys/installs its own steel, pipe, components). Bridge: outsourced $ = h*L*BC + p*(1-L)*BC. "
                  "p=0 labor-only (~25% of BC); p=1 material-inclusive (~75%). For a supplier-opportunity TAM, "
                  "p is high."),
    ]
    # POP note: anchored on each program's value cell (C/D/E) so a reviewer hovering
    # any one sees the basis, not just Virginia's cell.
    _pop_note = (
        "Current off-team share of construction work (announced place of performance): Virginia 34% "
        "(Block V, DoD 2019-12-02) / Columbia 22% (Build I, 2020-11-05) / DDG-51 ~13% (production-weighted "
        "blend: BIW ~20% off-Bath + Ingalls ~9% off-Pascagoula). The applied current-state floor the ceiling "
        "sits above. See Sources A5/A6/A7.")
    notes += [ExcelNote(f"{col}{P['pop']}", _pop_note) for col in ("C", "D", "E")]

    return P, c.rows, c.at(), dvs, notes


_P, _ROWS, _NEXT, _DVS, _NOTES = _build()


# ---- accessors ----
def core_h_cell(cls: str) -> str:
    if cls not in _CLASS_COL:
        raise ValueError(f"unknown class {cls!r}; expected one of {CLASSES}")
    return f"'{_TAB}'!{_ccol(cls)}{_P['h']}"


def labor_share_cell(cls: str) -> str:
    if cls not in _CLASS_COL:
        raise ValueError(f"unknown class {cls!r}; expected one of {CLASSES}")
    return f"'{_TAB}'!{_ccol(cls)}{_P['L']}"


def pop_current_cell(cls: str) -> str:
    if cls not in _CLASS_COL:
        raise ValueError(f"unknown class {cls!r}; expected one of {CLASSES}")
    return f"'{_TAB}'!{_ccol(cls)}{_P['pop']}"


def passthrough_cell() -> str:
    return f"'{_TAB}'!C{_P['p']}"


def pop_range() -> str:
    """The 3-class POP row (C:E), for dollar-weighted portfolio rollups in Tie-Outs."""
    return f"'{_TAB}'!{_ccol('Virginia')}{_P['pop']}:{_ccol('DDG-51')}{_P['pop']}"


def makebuy_cell(bound: str) -> str:
    key = {"low": "mb_low", "mid": "mb_mid", "high": "mb_high"}.get(bound)
    if key is None:
        raise ValueError(f"unknown bound {bound!r}; expected low/mid/high")
    return f"'{_TAB}'!C{_P[key]}"


def _render() -> WorksheetSpec:
    ws = worksheet(_ROWS, cols=[52, 13, 13, 13],
                   tab_color=group_color(_GROUP), with_gutter=True,
                   data_validations=_DVS)
    return WorksheetSpec(ws, notes=_NOTES)


ASSUMPTIONS = SheetEntry(_TAB, _GROUP, _render)
