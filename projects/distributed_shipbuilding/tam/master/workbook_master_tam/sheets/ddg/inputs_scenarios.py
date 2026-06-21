"""inputs_scenarios - the "Scenarios" tab (DDG, inputs group; one module = one sheet).

The editable SAM inclusion matrix - "which buckets are included in each leadership
scenario?" The former Scenarios section of the composite Inputs tab, now its own
tab. The matrix is a native Excel table (flat, editable, lookup-like) with a 0/1
data validation on the flag cells. A scenario definitions table, a selected-scenario
readout (linked from Inputs), and a per-scenario bucket count follow.

Promoted accessors (consumed by sam_build + deck_outputs):
  scenario_keys, scenario_name, scenario_flag_range
"""
from __future__ import annotations

from workbook_core.primitives import worksheet, col_letter
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_NUM_INPUT,
    S_TITLE_SHEET, S_TITLE_SECTION,
)
from workbook_core.tables import WorksheetSpec, ExcelTable, SheetEntry
from workbook_core.groups import group_color
from workbook_master_tam.sheets.ddg._taxonomy import BUCKETS, BUCKET_KEYS
from workbook_master_tam.sheets.ddg.inputs_assumptions import selected_scenario_cell
from workbook_master_tam.sheets.ddg._layout import RowCursor

_GROUP = "inputs"
_TAB = "DDG Scenarios"
_NCOLS = 6

# (key, display name, set-of-buckets, prose definition)
# NOTE: `modular` is ENTITY-driven - its SAM is computed in SAM Build from the
# registry modular flag (per operating entity), NOT from a bucket set. The sentinel
# set keeps its flag-matrix column all-zero; SAM Build special-cases it.
_MODULAR_ENTITY = {"_entity"}
SCENARIOS: list[tuple[str, str, set, str]] = [
    ("metal", "Metal components", {"structural", "castings", "machining"},
     "structural fab, castings/forgings, and machined components"),
    ("hme", "HM&E components", {"piping", "hvac", "machining", "electrical"},
     "hull/mechanical/electrical: piping/valves/pumps, HVAC, machining, ship power"),
    ("electrical", "Electrical / power", {"electrical"},
     "electrical power / distribution / generation only"),
    ("modular", "Modular assemblies", _MODULAR_ENTITY,
     "entity-flagged modular-assembly suppliers (registry flag, not a bucket union)"),
    ("broad", "Broad component mfg", set(BUCKET_KEYS),
     "all seven work-type buckets"),
]
SCENARIO_KEYS = [s[0] for s in SCENARIOS]
_FIRST_SCEN_COL = 2                                  # column C
_SCEN_COL = {k: _FIRST_SCEN_COL + i for i, k in enumerate(SCENARIO_KEYS)}


def _dv_whole(sqref: str, lo: int, hi: int) -> str:
    return ('<dataValidation type="whole" operator="between" allowBlank="1" '
            f'showErrorMessage="1" sqref="{sqref}"><formula1>{lo}</formula1>'
            f'<formula2>{hi}</formula2></dataValidation>')


def _make_scenarios():
    _bucket_name = {k: name for k, name, _ in BUCKETS}
    _matrix_headers = ["Bucket"] + [name for _k, name, _s, _d in SCENARIOS]
    tables: list[ExcelTable] = []
    c = RowCursor(2)
    c.banner(_TAB, n_cols=_NCOLS, style=S_TITLE_SHEET)
    c.blank()

    # §1 Scenario matrix (native table; 1 = scenario targets this bucket)
    c.banner("§1 - Scenario matrix (1 = scenario targets this bucket)", n_cols=_NCOLS,
             style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    _matrix_hdr = c.write(_matrix_headers, styles=[S_HEADER_LEFT] + [S_HEADER_CENTER] * len(SCENARIOS))
    _first_bucket = c.at()
    for k in BUCKET_KEYS:
        flags = [(1 if k in s else 0) for _k, _n, s, _d in SCENARIOS]
        c.write([_bucket_name[k]] + flags,
                styles=[S_DEFAULT] + [S_NUM_INPUT] * len(SCENARIOS), outline_level=1)
    _last_bucket = c.at() - 1
    _last_scen_col = col_letter(1 + len(SCENARIOS))
    tables.append(ExcelTable(
        name="tbl_ddg_scenarios",
        ref=f"B{_matrix_hdr}:{_last_scen_col}{_last_bucket}",
        headers=_matrix_headers))
    c.blank(2)

    # §2 Scenario definitions
    c.banner("§2 - Scenario definitions", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "Definition", "", "", ""], styles=S_HEADER_LEFT)
    for _k, name, _s, defn in SCENARIOS:
        c.write([name, defn, "", "", ""],
                styles=[S_BOLD, S_DEFAULT, S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §3 Selected scenario
    c.banner("§3 - Selected scenario", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Field", "Value"], styles=S_HEADER_LEFT)
    c.write(["Selected SAM scenario", f"={selected_scenario_cell()}"],
            styles=[S_DEFAULT, S_DEFAULT], outline_level=1)
    c.blank(2)

    # §4 Bucket count by scenario
    c.banner("§4 - Bucket count by scenario", n_cols=_NCOLS, style=S_TITLE_SECTION, mark_collapsible=True)
    c.blank()
    c.write(["Scenario", "# buckets", ""], styles=[S_HEADER_LEFT, S_HEADER_CENTER, S_HEADER_LEFT])
    for k, name, _s, _d in SCENARIOS:
        col = col_letter(_SCEN_COL[k])
        c.write([name, f"=SUM({col}{_first_bucket}:{col}{_last_bucket})", ""],
                styles=[S_DEFAULT, S_DEFAULT, S_DEFAULT], outline_level=1)

    _dvs = [_dv_whole(f"C{_first_bucket}:{_last_scen_col}{_last_bucket}", 0, 1)]

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[26, 22, 16, 16, 16, 16],
                       tab_color=group_color(_GROUP), with_gutter=True,
                       data_validations=_dvs)
        return WorksheetSpec(ws, tables=tables)

    def scenario_keys() -> list[str]:
        return list(SCENARIO_KEYS)

    def scenario_name(k: str) -> str:
        for key, name, _s, _d in SCENARIOS:
            if key == k:
                return name
        raise ValueError(f"Unknown scenario {k!r}")

    def scenario_flag_range(k: str) -> str:
        if k not in _SCEN_COL:
            raise ValueError(f"Unknown scenario {k!r}")
        col = col_letter(_SCEN_COL[k])
        return f"'{_TAB}'!{col}{_first_bucket}:{col}{_last_bucket}"

    return (SheetEntry(_TAB, _GROUP, render),
            scenario_keys, scenario_name, scenario_flag_range)


(SCENARIOS_ENTRY, scenario_keys, scenario_name, scenario_flag_range) = _make_scenarios()
