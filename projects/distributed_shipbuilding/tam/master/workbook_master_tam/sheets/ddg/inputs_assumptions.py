"""inputs_assumptions - the "Assumptions" tab (DDG, inputs group; one module = one sheet).

The editable control surface - the only place a model user changes numeric
assumptions (except raw data tabs, where extracted source values are intentionally
shown as hardcoded inputs). Seven sections (§1-§7): Run settings, Stream toggles,
AP/LLTM values, MYP masters, AP/LLTM knobs, Bucket adjustments, and Outlook
outyear bounds.

This is the former Control section of the composite Inputs tab, split out from the
scenario matrix (now its own ``scenarios`` tab) and expanded with two relocations:
  - Stream include-toggles moved here from TAM Build (include_bc_stream_cell,
    include_ap_lltm_stream_cell); TAM Build links to them.
  - The editable bucket-share Adjustment moved here from SAM Build's Subawards
    section (bucket_adjustment_cell). SAM Build computes modeled = observed + this.

Editable inputs carry a data validation (scenario dropdown, 0/1 toggles,
decimal-bounded knobs / POP % / adjustments).

Promoted accessors (cell refs into 'Assumptions'!):
  ap_lltm_base_cell, ap_gross_then_cell, myp_master_cell, myp_pop_cell,
  ap_supplier_coeff_cell, include_bc_stream_cell, include_ap_lltm_stream_cell,
  include_obbba_stream_cell, obbba_bc_share_cell, bucket_adjustment_cell,
  selected_scenario_cell, outlook_intent_uplift_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT, S_PCT_INPUT,
    S_LINK_NUM, S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.notes import ExcelNote
from workbook_core.groups import group_color
from workbook_master_tam.sheets.submarines.data_deflators import deflator_factor_cell
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "inputs"
_NCOLS = 7
_TAB = "DDG Assumptions"
_LI = 2122
_FY_COLUMNS = [2022, 2023, 2024, 2025, 2026, 2027]
_FY_COL_INDEX = {fy: 2 + i for i, fy in enumerate(_FY_COLUMNS)}   # C..H
_AP_CY = {2022: 0, 2023: 0, 2024: 0, 2025: 83.224, 2026: 1750.0, 2027: 0}
# P-10 "Ship Construction EOQ" line per FY (the supplier-addressable subset of CY AP).
# FY26 gross $1,750.0M also carries $450.0M congressional-add shipyard infrastructure and
# $300.0M wage enhancements (both excluded); FY25 gross $83.224M carries $41.724M NMT
# terminal GFE (excluded).
_AP_EOQ = {2022: 0, 2023: 0, 2024: 0, 2025: 41.5, 2026: 1000.0, 2027: 0}
# Master POP % = the award bulletins' announced split. FY23-27 masters: dollars redacted
# (reconstructed from FPDS + trade press), POP announced - BIW 69% Bath + 12% named
# supplier cities + 19% "other locations below 1%"; Ingalls 77% Pascagoula + 23%.
# FY18-22 masters (2018-09-27 bulletin, article 1647166): dollars AND POP announced -
# BIW $3,904.7M, Bath 61% + 19% named + 20% aggregate; Ingalls $5,104.7M, Pascagoula 91%
# + 9%. Below-1% aggregates count as other-US, mirroring the submarine corpus parse
# convention. The FY18-22 rows feed ONLY the FY2022-vintage BC coefficient (TAM Build
# §3a) - they predate the POP-corpus window and stay out of the corpus.
_MYP = {
    "biw":       ("BIW FY23-27 MYP master", "N00024-23-C-2305", 6400, 69, 0, 31, 0),
    "ingalls":   ("Ingalls FY23-27 MYP master", "N00024-23-C-2307", 8180, 0, 77, 23, 0),
    "biw18":     ("BIW FY18-22 MYP master", "N00024-18-C-2305", 3904.736, 61, 0, 39, 0),
    "ingalls18": ("Ingalls FY18-22 MYP master", "N00024-18-C-2307", 5104.669, 0, 91, 9, 0),
}
_MYP_COL = {"piid": 2, "master": 3, "biw": 4, "ingalls": 5, "other_us": 6, "foreign": 7}


def _fy_col(fy: int) -> str:
    return col_letter(_FY_COL_INDEX[fy])


def _dv_list(sqref: str, items: list[str]) -> str:
    return ('<dataValidation type="list" allowBlank="1" showInputMessage="1" '
            f'showErrorMessage="1" sqref="{sqref}">'
            f'<formula1>"{",".join(items)}"</formula1></dataValidation>')


def _dv_whole(sqref: str, lo: int, hi: int) -> str:
    return ('<dataValidation type="whole" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}"><formula1>{lo}</formula1>'
            f'<formula2>{hi}</formula2></dataValidation>')


def _dv_decimal(sqref: str, lo: float, hi: float) -> str:
    return ('<dataValidation type="decimal" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}"><formula1>{lo}</formula1>'
            f'<formula2>{hi}</formula2></dataValidation>')


def _make_inputs():
    P: dict = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Run settings
    c.banner("§1 - Run settings", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Setting", "Value"], styles=S_HEADER_LEFT)
    c.write(["Program", "DDG-51 Flight III"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["FY range start", 2022],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["FY range end", 2027],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.write(["Units", "Constant FY2026 $M (then-year source retained)"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Stream toggles (moved here from TAM Build)
    c.banner("§2 - Stream toggles", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Toggle", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["incl_bc"] = c.write(["Include BC stream", 1],
                           styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    P["incl_ap"] = c.write(["Include AP/LLTM stream", 1],
                           styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    P["incl_obbba"] = c.write(["Include OBBBA mandatory (Sec. 20002(17)) in BC stream", 1],
                              styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    c.blank(2)

    # §3 AP/LLTM values
    c.banner("§3 - AP/LLTM stream ($M, CY advance procurement)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Class"] + list(_FY_COLUMNS),
            styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(_FY_COLUMNS))
    P["ap_gross"] = c.write(["DDG-51 (LI 2122), CY AP gross then-year $ (P-1)"]
                            + [_AP_CY[fy] for fy in _FY_COLUMNS],
                            styles=[S_BOLD] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    P["ap_eoq"] = c.write(
        ["of which Ship Construction EOQ, then-year $ (P-10)"]
        + [_AP_EOQ[fy] for fy in _FY_COLUMNS],
        styles=[S_DEFAULT] + [S_NUM_INPUT] * len(_FY_COLUMNS), outline_level=1)
    # Constant-FY2026 AP base (P-10 EOQ then-year x Green Book Procurement deflator). This
    # row backs ap_lltm_base_cell, so the AP/LLTM stream TAM is the P-10-classified
    # supplier-addressable subset in constant FY2026 $.
    P["ap_base_const"] = c.write(
        ["Ship Construction EOQ, constant FY2026 $"]
        + [f"={_fy_col(fy)}{P['ap_eoq']}*{deflator_factor_cell(fy)}" for fy in _FY_COLUMNS],
        styles=[S_BOLD] + [S_LINK_NUM] * len(_FY_COLUMNS), outline_level=1)
    c.blank(2)

    # §4 MYP masters
    c.banner("§4 - MYP masters (POP % as announced; FY23-27 $ reconstructed, FY18-22 $ as announced)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Master", "PIID", "Master $M", "BIW %", "Ingalls %", "Other-US %", "Foreign %"],
            styles=[S_HEADER_LEFT] * 2 + [S_HEADER_CENTER] * 5)
    P["myp"] = {}
    _MYP18_NOTE = ("DoD announcement 2018-09-27 (defense.gov article 1647166, Wayback "
                   "20180928083950): BIW $3,904.7M, 4 ships FY19-22, 'Bath, Maine (61%)... "
                   "other locations below 1% (collectively totaling 20%)'; Ingalls "
                   "$5,104.7M, 6 ships FY18-22, 'Pascagoula, Mississippi (91%); Erie, "
                   "Pennsylvania (1%); other locations below 1% (8%)'. Feeds the "
                   "FY2022-vintage BC coefficient only; predates the POP-corpus window.")
    for yard in ("biw", "ingalls", "biw18", "ingalls18"):
        label, piid, master, biw, ing, ous, frn = _MYP[yard]
        P["myp"][yard] = c.write(
            [label, piid, master, biw / 100, ing / 100, ous / 100, frn / 100],
            styles=[S_BOLD, S_DEFAULT, S_NUM_INPUT, S_PCT_INPUT, S_PCT_INPUT, S_PCT_INPUT,
                    S_PCT_INPUT],
            outline_level=1)
    c.blank(2)

    # §5 AP/LLTM knobs
    c.banner("§5 - AP/LLTM classification knobs", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Knob", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["coeff"] = c.write(
        ["AP/LLTM supplier coefficient", 1.00],
        styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    # Sec. 20002(17) covers BC + GFE with no breakout; 0.628 = portfolio BC / (BC + GFE).
    P["obbba_bc_share"] = c.write(
        ["OBBBA BC share of award (BC vs GFE)", 0.628],
        styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)
    c.blank(2)

    # §6 Outlook outyear penetration bounds (Outlook §3 links here)
    c.banner("§6 - Outlook outyear penetration bounds", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Knob", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["intent_uplift"] = c.write(
        ["Outsourcing intent uplift vs FY22-25 average", 0.30],
        styles=[S_DEFAULT, S_PCT_INPUT], outline_level=1)

    _dvs = [
        _dv_whole(f"C{P['incl_bc']}:C{P['incl_obbba']}", 0, 1),
        _dv_decimal(f"E{P['myp']['biw']}:H{P['myp']['ingalls18']}", 0, 1),
        _dv_decimal(f"C{P['coeff']}:C{P['obbba_bc_share']}", 0, 1),
        _dv_decimal(f"C{P['intent_uplift']}", 0, 1),
    ]

    # Source/citation hovers on the cells they back (native notes, not visible text).
    _notes = [
        ExcelNote(f"B{P['ap_eoq']}",
                  "PB2027 SCN justification, Exhibit P-10 (Advance Procurement Requirements "
                  "Analysis), LI 2122 DDG-51, Vol 1 p.243: FY2026 $1,750.0M = Ship Construction "
                  "EOQ $1,000.0M + congressional adds excluded ($450.0M shipyard infrastructure, "
                  "$300.0M wage enhancements); FY2025 $83.224M = EOQ $41.5M + NMT terminal GFE "
                  "$41.7M excluded (PB2026 Vol 1 p.235)."),
        ExcelNote(f"B{P['myp']['biw18']}", _MYP18_NOTE),
        ExcelNote(f"C{P['coeff']}",
                  "1.00 by P-10 classification: the base is the 'Ship Construction EOQ' line only, "
                  "which the exhibit defines as Economic Order Quantity procurements of material "
                  "items (vendor-purchased); AWS EOQ, terminal GFE, and congressional adds are "
                  "already excluded at the line level. Haircut cases at Sensitivity §4."),
        ExcelNote(f"C{P['intent_uplift']}",
                  "Outlook upper bound = FY22-25 average penetration x (1 + this uplift). "
                  "Basis: stated industry intent to grow outsourced manhours ~30% "
                  "(HII statement; citation pending - swap in the source when confirmed)."),
    ]

    def render() -> WorksheetSpec:
        return WorksheetSpec(worksheet(c.rows, cols=[32, 18, 30, 13, 13, 13, 13],
                             tab_color=group_color(_GROUP), with_gutter=True,
                             data_validations=_dvs), notes=_notes)

    # ---- accessors (closures over captured rows) ----
    def ap_lltm_base_cell(li: int, fy: int) -> str:
        if li != _LI:
            raise ValueError(f"Unknown LI {li!r}; DDG program is {_LI}")
        if fy not in _FY_COL_INDEX:
            raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")
        return f"'{_TAB}'!{_fy_col(fy)}{P['ap_base_const']}"

    def ap_gross_then_cell(li: int, fy: int) -> str:
        if li != _LI:
            raise ValueError(f"Unknown LI {li!r}; DDG program is {_LI}")
        if fy not in _FY_COL_INDEX:
            raise ValueError(f"FY {fy!r} outside {_FY_COLUMNS!r}")
        return f"'{_TAB}'!{_fy_col(fy)}{P['ap_gross']}"

    def myp_master_cell(yard: str) -> str:
        if yard not in P["myp"]:
            raise ValueError(f"Unknown yard {yard!r}; expected 'biw' or 'ingalls'")
        return f"'{_TAB}'!{col_letter(_MYP_COL['master'])}{P['myp'][yard]}"

    def myp_pop_cell(yard: str, popclass: str) -> str:
        if yard not in P["myp"]:
            raise ValueError(f"Unknown yard {yard!r}")
        if popclass not in ("biw", "ingalls", "other_us", "foreign"):
            raise ValueError(f"Unknown popclass {popclass!r}")
        return f"'{_TAB}'!{col_letter(_MYP_COL[popclass])}{P['myp'][yard]}"

    def ap_supplier_coeff_cell() -> str:
        return f"'{_TAB}'!C{P['coeff']}"

    def include_bc_stream_cell() -> str:
        return f"'{_TAB}'!C{P['incl_bc']}"

    def include_ap_lltm_stream_cell() -> str:
        return f"'{_TAB}'!C{P['incl_ap']}"

    def include_obbba_stream_cell() -> str:
        return f"'{_TAB}'!C{P['incl_obbba']}"

    def obbba_bc_share_cell() -> str:
        return f"'{_TAB}'!C{P['obbba_bc_share']}"

    def outlook_intent_uplift_cell() -> str:
        return f"'{_TAB}'!C{P['intent_uplift']}"

    return (SheetEntry(_TAB, _GROUP, render),
            ap_lltm_base_cell, ap_gross_then_cell, myp_master_cell, myp_pop_cell,
            ap_supplier_coeff_cell,
            include_bc_stream_cell, include_ap_lltm_stream_cell,
            include_obbba_stream_cell, obbba_bc_share_cell,
            outlook_intent_uplift_cell)


(ASSUMPTIONS, ap_lltm_base_cell, ap_gross_then_cell, myp_master_cell, myp_pop_cell,
 ap_supplier_coeff_cell,
 include_bc_stream_cell, include_ap_lltm_stream_cell,
 include_obbba_stream_cell, obbba_bc_share_cell,
 outlook_intent_uplift_cell) = _make_inputs()
