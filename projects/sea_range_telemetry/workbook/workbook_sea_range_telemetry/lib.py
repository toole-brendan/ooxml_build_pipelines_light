"""Sea Range Telemetry workbook pipeline bindings.

The OOXML engine lives in the shared ``workbook_core`` package at the workspace
root. This module is intentionally thin: it binds the things specific to this
pipeline (the output path, the extracted-data dir, the docProps identity),
exposes a load_extracted_csv wrapper bound to this pipeline's data dir, and
packages the SHEETS module list via the shared packager.

The sheet modules import workbook_core.* directly; the workbook_core import path
is set up in workbook_sea_range_telemetry/__init__.py.
"""
from __future__ import annotations

from pathlib import Path

from workbook_core.lib import (
    package_workbook,
    load_extracted_csv as _core_load_extracted_csv,
)

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

WORKBOOK_DIR = Path(__file__).resolve().parents[1]   # projects/sea_range_telemetry/workbook/
PROJECT_DIR = Path(__file__).resolve().parents[2]    # projects/sea_range_telemetry/   (build output lands here)
REPO_ROOT = Path(__file__).resolve().parents[4]      # ooxml_build_pipelines_light/
OUT = PROJECT_DIR / "20260607_Sea Range Telemetry_vS.xlsx"
EXTRACTED = WORKBOOK_DIR / "extracted"

_TITLE = "Sea Range Telemetry"
_CREATOR = "workbook_sea_range_telemetry build_workbook.py"
_APP = "workbook_sea_range_telemetry"


def load_extracted_csv(name: str) -> tuple[list[str], list[list]]:
    """Load extracted/<name>.csv from this pipeline's data dir."""
    return _core_load_extracted_csv(name, EXTRACTED)


def build() -> int:
    """Render every registered sheet and package into the output xlsx."""
    from workbook_sea_range_telemetry.sheets import SHEETS
    if not SHEETS:
        raise SystemExit(
            "workbook_sea_range_telemetry/sheets/__init__.py SHEETS is empty - add a sheet "
            "module before building. Start by copying "
            "workbook_core/sheet_base_template.py to "
            "workbook_sea_range_telemetry/sheets/<group>_<slug>.py, then register it in "
            "workbook_sea_range_telemetry/sheets/__init__.py SHEETS (in tab order)."
        )
    return package_workbook(OUT, SHEETS, title=_TITLE, creator=_CREATOR,
                            app_name=_APP, normalize_dashes=True)
