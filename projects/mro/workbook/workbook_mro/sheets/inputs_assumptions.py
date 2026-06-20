"""Assumptions

INTENT
    The editable control surface - the only place a model user changes a numeric
    assumption (the raw data tabs intentionally show extracted source values as
    hardcoded inputs, and every other figure is a live SUMIFS or cross-sheet pull). The
    MRO model is overwhelmingly source-pinned, so the genuine tunable plugs are few: the
    two out-of-scope plan estimates that are NOT source-derivable - the WPN combat-
    systems sustainment estimate (~$500M, no clean WPN ship-MRO line item) and the FMS
    out-of-scope deduction (~-$100M) - plus the FY run anchor. WPN feeds the TAM Bridge
    memo line; FMS is retained as a reference plug (addressability / FMS exclusion is now
    handled on the TAM atoms scope_class -> SAM Build Broad Addressable). Editable cells
    carry a data validation (decimal-bounded plugs, whole-number FY).

    §3 adds the SAM scenario selector: a list-validated cell holding one of the SAM
    scenario names; SAM Build reads it via selected_scenario_cell() to drive the
    selected-scenario SAM + drilldowns.

    Accessors: wpn_estimate_cell, fms_estimate_cell, fy_anchor_cell, selected_scenario_cell.

LAYOUT
    row 2 : title
    B..C  : Setting / Value
    §1 run settings · §2 out-of-scope plan estimates ($M) · §3 SAM scenario selector
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets import taxonomy_mro as tx

_GROUP = "inputs"
_TAB = "Assumptions"
_NCOLS = 2                      # B..C: Setting / Value
_COLS = [38, 14]
_FY_ANCHOR = 2025


def _dv_whole(sqref: str, lo: int, hi: int) -> str:
    return ('<dataValidation type="whole" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}"><formula1>{lo}</formula1>'
            f'<formula2>{hi}</formula2></dataValidation>')


def _dv_decimal(sqref: str, lo: float, hi: float) -> str:
    return ('<dataValidation type="decimal" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}"><formula1>{lo}</formula1>'
            f'<formula2>{hi}</formula2></dataValidation>')


def _dv_list(sqref: str, items: list[str]) -> str:
    """A dropdown list validation; items must be comma-free. The joined list is the
    text of <formula1>, so XML-escape it (& -> &amp;) - e.g. 'Electronics & C4ISR'."""
    joined = ",".join(items)
    joined = joined.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return ('<dataValidation type="list" allowBlank="1" showErrorMessage="1" '
            f'sqref="{sqref}"><formula1>"{joined}"</formula1></dataValidation>')


def _make_inputs():
    P: dict[str, int] = {}
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Run settings
    c.banner("§1 - Run settings", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Setting", "Value"], styles=S_HEADER_LEFT)
    c.write(["Program", "U.S. Navy & USCG Vessel MRO"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    P["fy"] = c.write(
        ["FY anchor", _FY_ANCHOR],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    c.write(["Units", "Nominal $M"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §2 Out-of-scope plan estimates (the only non-source-pinned $ in the model)
    c.banner("§2 - Out-of-scope plan estimates ($M)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Plug", "$M"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["wpn"] = c.write(
        ["WPN combat-systems sustainment estimate", 500],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    P["fms"] = c.write(
        ["FMS (out of addressable scope)", -100],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)
    c.blank(2)

    # §3 SAM scenario selector (drives SAM Build's selected-scenario SAM + drilldowns)
    c.banner("§3 - SAM scenario selector", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Setting", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    _scen_names = [tx.SCENARIO_NAME[k] for k in tx.SCENARIO_KEYS]
    P["scenario"] = c.write(
        ["Selected SAM scenario", tx.SCENARIO_NAME["core_depot"]],
        styles=[S_DEFAULT, S_NUM_INPUT], outline_level=1)

    _dvs = [
        _dv_whole(f"C{P['fy']}", 2020, 2030),
        _dv_decimal(f"C{P['wpn']}", 0, 10000),
        _dv_decimal(f"C{P['fms']}", -2000, 0),
        _dv_list(f"C{P['scenario']}", _scen_names),
    ]

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=_COLS, tab_color=group_color(_GROUP),
                       with_gutter=True, data_validations=_dvs)
        return WorksheetSpec(ws)

    # accessors (closures over captured rows)
    def wpn_estimate_cell() -> str:
        return f"'{_TAB}'!C{P['wpn']}"

    def fms_estimate_cell() -> str:
        return f"'{_TAB}'!C{P['fms']}"

    def fy_anchor_cell() -> str:
        return f"'{_TAB}'!C{P['fy']}"

    def selected_scenario_cell() -> str:
        return f"'{_TAB}'!C{P['scenario']}"

    return (SheetEntry(_TAB, _GROUP, render),
            wpn_estimate_cell, fms_estimate_cell, fy_anchor_cell,
            selected_scenario_cell)


(ASSUMPTIONS, wpn_estimate_cell, fms_estimate_cell,
 fy_anchor_cell, selected_scenario_cell) = _make_inputs()
