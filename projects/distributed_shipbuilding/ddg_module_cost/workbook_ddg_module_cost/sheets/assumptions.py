"""assumptions - the "Assumptions" tab (inputs group; the single edit surface).

The one place a user changes the model's levers:
  §1 Cost anchor   - which fiscal-year buy the per-ship Basic Construction comes
                     from (default FY2025, the 3-ship rate). The resolved per-ship
                     BC is the numerator every level of the cascade divides.
  §2 Structural counts - HII's modular build hierarchy: 4 modules / 21 grand
                     blocks / 72 structural units. Editable, cited to HII.
  §3 Module weights - relative weight per module; DEFAULT EQUAL, which makes the
                     module breakout an even split. Raise a module's weight to
                     load it heavier (e.g. the machinery-dense aft module).

Editable knob cells carry a pale-yellow input fill (ICAEW Financial Modelling Code).

Promoted accessors (cell refs into 'Assumptions'!):
  anchor_fy_cell, numerator_cell, count_cell(kind),
  weight_cells() -> [(label, ref), ...], weight_total_cell
"""
from __future__ import annotations

from workbook_core.primitives import worksheet
from workbook_core.styles import (
    S_DEFAULT, S_BOLD, S_NOTE, S_HEADER_LEFT, S_HEADER_CENTER, S_NUM, S_LINK_NUM,
)
from workbook_core.tables import WorksheetSpec, SheetEntry
from workbook_core.groups import group_color

from workbook_ddg_module_cost.sheets._layout import RowCursor
from workbook_ddg_module_cost.sheets._inputfill import (
    S_NUM_INPUT_FILL, S_INT_INPUT_FILL, S_YEAR_INPUT_FILL,
)
from workbook_ddg_module_cost.sheets._tabs import TAB_ASSUMPTIONS
from workbook_ddg_module_cost.sheets.ship_cost_basis import (
    per_ship_bc_range, fy_axis_range,
)

_GROUP = "inputs"
_NCOLS = 2   # content columns (gutter mode): B = label, C = value

_MODULES = ["Hull module 1 (forward)", "Hull module 2 (midship)",
            "Hull module 3 (aft)", "Deckhouse (module 4)"]


def _make():
    P: dict = {}
    c = RowCursor(2)
    c.title(TAB_ASSUMPTIONS, _NCOLS)
    c.caption("Cost anchor, HII structural counts, and module weights")
    c.blank(2)

    # §1 Cost anchor ------------------------------------------------------------------
    c.section("§1 - Cost anchor", _NCOLS)
    c.blank()
    c.write(["Knob", "Value"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["anchor_fy"] = c.write(
        ["Anchor fiscal year (FY2025 = 3-ship; FY2027 = 1-ship)", 2025],
        styles=[S_DEFAULT, S_YEAR_INPUT_FILL])
    # Resolved numerator: per-ship Basic Construction for the anchor FY (const FY2026 $M).
    # Green cross-sheet font: it resolves live from Ship Cost Basis.
    P["numerator"] = c.write(
        ["Per-ship Basic Construction (const FY2026 $M)",
         f"=INDEX({per_ship_bc_range()},MATCH(C{P['anchor_fy']},{fy_axis_range()},0))"],
        styles=[S_BOLD, S_LINK_NUM])
    c.blank(2)

    # §2 Structural counts ------------------------------------------------------------
    c.section("§2 - Structural counts (HII modular build hierarchy)", _NCOLS)
    c.blank()
    c.write(["Level", "Count"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["modules"] = c.write(["Modules (hull 1-3 + deckhouse)", 4],
                           styles=[S_DEFAULT, S_INT_INPUT_FILL])
    P["blocks"] = c.write(["Grand blocks", 21],
                          styles=[S_DEFAULT, S_INT_INPUT_FILL])
    P["units"] = c.write(["Structural units (assemblies)", 72],
                         styles=[S_DEFAULT, S_INT_INPUT_FILL])
    c.blank(2)

    # §3 Module weights ---------------------------------------------------------------
    c.section("§3 - Module relative weights", _NCOLS)
    c.blank()
    c.write(["Module", "Relative weight"], styles=[S_HEADER_LEFT, S_HEADER_CENTER])
    P["weights"] = []
    for label in _MODULES:
        r = c.write([label, 1.00], styles=[S_DEFAULT, S_NUM_INPUT_FILL])
        P["weights"].append((label, r))
    w_first, w_last = P["weights"][0][1], P["weights"][-1][1]
    P["wtotal"] = c.total(
        ["Total weight", f"=SUM(C{w_first}:C{w_last})"],
        styles=[S_BOLD, S_NUM], n_cols=_NCOLS)
    c.write(["Default equal weights = even split. Raise a module's weight to load it "
             "heavier (e.g. the machinery-dense aft module / deckhouse)."],
            styles=[S_NOTE])

    def render() -> WorksheetSpec:
        ws = worksheet(c.rows, cols=[46, 18],
                       tab_color=group_color(_GROUP), with_gutter=True,
                       show_outline_symbols=False)
        return WorksheetSpec(ws)

    def anchor_fy_cell() -> str:
        return f"'{TAB_ASSUMPTIONS}'!C{P['anchor_fy']}"

    def numerator_cell() -> str:
        return f"'{TAB_ASSUMPTIONS}'!C{P['numerator']}"

    def count_cell(kind: str) -> str:
        if kind not in ("modules", "blocks", "units"):
            raise ValueError(f"unknown count kind {kind!r}")
        return f"'{TAB_ASSUMPTIONS}'!C{P[kind]}"

    def weight_cells() -> list:
        return [(label, f"'{TAB_ASSUMPTIONS}'!C{r}") for label, r in P["weights"]]

    def weight_total_cell() -> str:
        return f"'{TAB_ASSUMPTIONS}'!C{P['wtotal']}"

    return (SheetEntry(TAB_ASSUMPTIONS, _GROUP, render),
            dict(anchor_fy_cell=anchor_fy_cell, numerator_cell=numerator_cell,
                 count_cell=count_cell, weight_cells=weight_cells,
                 weight_total_cell=weight_total_cell))


(ASSUMPTIONS, _A) = _make()
anchor_fy_cell = _A["anchor_fy_cell"]
numerator_cell = _A["numerator_cell"]
count_cell = _A["count_cell"]
weight_cells = _A["weight_cells"]
weight_total_cell = _A["weight_total_cell"]
