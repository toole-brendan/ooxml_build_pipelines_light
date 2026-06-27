"""ddg_module_cost pipeline bindings.

The OOXML engine lives in the shared ``workbook_core`` package at the workspace
root. This module is intentionally thin: it binds the things specific to this
pipeline (the output path, the extracted-data dir, the docProps identity, the tab
palette), and packages the SHEETS module list via the shared packager.

The extracted/ dir holds one clean CSV (``ddg_ship_cost.csv``) written by
``build_extracted.py`` - the DDG-51 SCN-budget slice pulled from the Master TAM
workbook. The sheet modules read it through ``_cuts`` (raw strings; numeric
columns cast via as_float / as_int).
"""
from __future__ import annotations

from pathlib import Path

from workbook_core.lib import package_workbook
import workbook_core.groups as _groups

# ---------------------------------------------------------------------------
# Tab palette - per-build override (THIS workbook only)
# ---------------------------------------------------------------------------
# Mirror the muted black / teal / olive / navy scheme used by the sibling
# distributed-shipbuilding workbooks (the shared workbook_core palette reads
# "loud"). group_color() reads workbook_core's _COLOR dict at render time, so
# mutating it here - before build() packages the sheets - repaints the tabs with
# no change to any sheet module. This mutates the shared dict IN THIS PROCESS
# ONLY; every other pipeline builds in its own process and keeps its own colors.
_TAB_PALETTE = {
    "summary":    "262626",   # black / charcoal - the answer page (Module Cost)
    "guide":      "2C5E5E",   # muted teal       - hierarchy + method/caveats
    "inputs":     "556B2F",   # olive green      - the editable levers (Assumptions)
    "model":      "48596B",   # slate            - (unused; kept for parity)
    "data":       "203864",   # navy blue        - cost basis + outfit context
    "validation": "595959",   # muted gray       - live in-workbook checks (Checks)
}
_groups._COLOR.update(_TAB_PALETTE)

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

WORKBOOK_DIR = Path(__file__).resolve().parents[1]   # ddg_module_cost/  (build output lands here)
PROJECT_DIR = WORKBOOK_DIR
REPO_ROOT = Path(__file__).resolve().parents[4]      # ooxml_build_pipelines_light/
OUT = PROJECT_DIR / "20260625_DDG-51 Module Cost_vS.xlsx"

EXTRACTED = WORKBOOK_DIR / "extracted"

_TITLE = "DDG-51 Cost per Module - top-down allocation over the HII modular build hierarchy"
_CREATOR = "workbook_ddg_module_cost build_workbook.py"
_APP = "workbook_ddg_module_cost"


def build_model() -> list:
    """The registered sheets, in DISPLAY (tab) order, ready to package.

    Dependency order is one-directional and self-enforced by Python's import
    graph (a consumer cannot import a producer's accessor until the producer has
    built at import):

        ship_cost_basis (per-ship BC)  -> assumptions (counts, weights, anchor)
                                       -> module_cost (the cascade answer)
                                       -> checks (live ties)
    """
    from workbook_ddg_module_cost.sheets import SHEETS
    return SHEETS


def build() -> int:
    """Render every registered sheet and package into the output xlsx."""
    return package_workbook(OUT, build_model(), title=_TITLE, creator=_CREATOR,
                            app_name=_APP, normalize_dashes=True)
