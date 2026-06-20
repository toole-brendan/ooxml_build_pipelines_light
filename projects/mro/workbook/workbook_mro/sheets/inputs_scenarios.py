"""Scenarios

INTENT
    The editable SAM inclusion matrix - "which atom buckets does each leadership
    scenario target?" An axis-based 0/1 matrix (one row per (axis, bucket), one
    column per scenario), rendered as a native, filterable table with whole-number
    0/1 data validation on the flag cells. "1 = the scenario includes atoms whose
    <axis> tag = <bucket>." Inclusion rule (realised in SAM Build): within an axis
    OR, across axes AND. A non-constraining axis flags all its buckets 1 (including
    the n/a / unmapped sentinels); a constraining axis flags only its target buckets,
    so non-applicable atoms drop out.

    The matrix ROWS are machine-derived from the atom tag sets (data_tam_atoms.
    distinct_tags) so every distinct tag - including n/a / unmapped - is guaranteed a
    row (no SUMIFS can silently miss a key). The flag DEFAULTS come from
    taxonomy_mro.SCENARIO_SPEC; an analyst can override any 0/1 in Excel and the SAM
    recomputes live.

    Promoted accessors (consumed by model_sam_build): scenario_keys, scenario_name,
    key_axis_range, flag_axis_range.

LAYOUT
    row 2 : title
    §1 scenario matrix (native tbl_mro_scenarios) · §2 definitions · §3 selected readout
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_mro.sheets._layout import RowCursor
from workbook_mro.sheets import taxonomy_mro as tx
from workbook_mro.sheets.data_tam_atoms import distinct_tags
from workbook_mro.sheets.inputs_assumptions import selected_scenario_cell

_GROUP = "inputs"
_TAB = "Scenarios"
_SCEN_KEYS = tx.SCENARIO_KEYS
_HEADERS = ["Axis", "Bucket"] + [tx.SCENARIO_NAME[k] for k in _SCEN_KEYS]
_NCOLS = len(_HEADERS)                          # 2 + 9 scenarios = 11 (B..L)
# Content begins at column B; scenario s (index j) sits at content column 3+j -> D.. .
_KEY_COL = col_letter(2)                         # "C" - the Bucket key column
_SCEN_COL = {k: col_letter(3 + j) for j, k in enumerate(_SCEN_KEYS)}


def _dv_whole(sqref: str, lo: int, hi: int) -> str:
    return ('<dataValidation type="whole" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}"><formula1>{lo}</formula1>'
            f'<formula2>{hi}</formula2></dataValidation>')


def _make():
    # Per-axis bucket lists (machine-derived from the atoms) + coverage assertion.
    axis_buckets = {axis: distinct_tags(axis) for axis in tx.AXIS_KEYS}
    for axis in tx.AXIS_KEYS:
        assert axis_buckets[axis], f"axis {axis!r} has no buckets"

    axis_rows: dict[str, tuple[int, int]] = {}   # axis -> (first_row, last_row)
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Scenario matrix (native table; 1 = scenario targets atoms with this bucket)
    c.banner("§1 - Scenario matrix (1 = scenario includes atoms whose axis tag = bucket)",
             n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    hdr = c.write(_HEADERS, styles=[S_HEADER_LEFT, S_HEADER_LEFT]
                  + [S_HEADER_CENTER] * len(_SCEN_KEYS))
    first_data = c.at()
    for axis in tx.AXIS_KEYS:
        a_first = c.at()
        for bucket in axis_buckets[axis]:
            flags = [tx.scenario_flag(k, axis, bucket) for k in _SCEN_KEYS]
            c.write([tx.AXIS_LABEL[axis], bucket] + flags,
                    styles=[S_DEFAULT, S_DEFAULT] + [S_NUM_INPUT] * len(_SCEN_KEYS),
                    outline_level=1)
        axis_rows[axis] = (a_first, c.at() - 1)
    last_data = c.at() - 1
    tables = [ExcelTable(name="tbl_mro_scenarios",
                         ref=f"B{hdr}:{col_letter(_NCOLS)}{last_data}", headers=_HEADERS)]
    c.blank(2)

    # §2 Scenario definitions
    c.banner("§2 - Scenario definitions", n_cols=_NCOLS, style=S_TITLE_SECTION,
             mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "Definition"] + [""] * (_NCOLS - 2),
            styles=[S_HEADER_LEFT] * _NCOLS)
    for k in _SCEN_KEYS:
        c.write([tx.SCENARIO_NAME[k], tx.SCENARIO_INTERP[k]] + [None] * (_NCOLS - 2),
                styles=[S_BOLD, S_DEFAULT] + [S_DEFAULT] * (_NCOLS - 2), outline_level=1)
    c.blank(2)

    # §3 Selected scenario (linked from Inputs; not summed - a menu)
    c.banner("§3 - Selected scenario (menu - do NOT sum scenario SAMs)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"] + [""] * (_NCOLS - 2),
            styles=[S_HEADER_LEFT, S_HEADER_LEFT] + [S_HEADER_LEFT] * (_NCOLS - 2))
    c.write(["Selected SAM scenario", f"={selected_scenario_cell()}"] + [None] * (_NCOLS - 2),
            styles=[S_DEFAULT, S_DEFAULT] + [S_DEFAULT] * (_NCOLS - 2), outline_level=1)

    _dvs = [_dv_whole(f"D{first_data}:{col_letter(_NCOLS)}{last_data}", 0, 1)]

    def render() -> WorksheetSpec:
        cols = [22, 30] + [15] * len(_SCEN_KEYS)
        ws = worksheet(c.rows, cols=cols, tab_color=group_color(_GROUP),
                       with_gutter=True, data_validations=_dvs)
        return WorksheetSpec(ws, tables=tables)

    def scenario_keys() -> list[str]:
        return list(_SCEN_KEYS)

    def scenario_name(k: str) -> str:
        return tx.SCENARIO_NAME[k]

    def scenario_col(k: str) -> str:
        return _SCEN_COL[k]

    def key_axis_range(axis: str) -> str:
        f, l = axis_rows[axis]
        return f"'{_TAB}'!${_KEY_COL}${f}:${_KEY_COL}${l}"

    def flag_axis_range(k: str, axis: str) -> str:
        f, l = axis_rows[axis]
        col = _SCEN_COL[k]
        return f"'{_TAB}'!${col}${f}:${col}${l}"

    def scenario_name_list() -> list[str]:
        return [tx.SCENARIO_NAME[k] for k in _SCEN_KEYS]

    def scenario_header_range() -> str:
        first = _SCEN_COL[_SCEN_KEYS[0]]
        last = _SCEN_COL[_SCEN_KEYS[-1]]
        return f"'{_TAB}'!${first}${hdr}:${last}${hdr}"

    acc = dict(scenario_keys=scenario_keys, scenario_name=scenario_name,
               scenario_col=scenario_col, key_axis_range=key_axis_range,
               flag_axis_range=flag_axis_range, scenario_name_list=scenario_name_list,
               scenario_header_range=scenario_header_range)
    return SheetEntry(_TAB, _GROUP, render), acc


SCENARIOS_ENTRY, _ACC = _make()

scenario_keys = _ACC["scenario_keys"]
scenario_name = _ACC["scenario_name"]
scenario_col = _ACC["scenario_col"]
key_axis_range = _ACC["key_axis_range"]
flag_axis_range = _ACC["flag_axis_range"]
scenario_name_list = _ACC["scenario_name_list"]
scenario_header_range = _ACC["scenario_header_range"]
