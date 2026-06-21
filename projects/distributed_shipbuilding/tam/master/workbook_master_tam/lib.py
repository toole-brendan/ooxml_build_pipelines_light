"""Master TAM pipeline bindings.

The OOXML engine lives in the shared ``workbook_core`` package at the workspace
root. This module is intentionally thin: it binds the things specific to this
pipeline (the output path, the extracted-data ROOT, the docProps identity) and
packages the SHEETS module list via the shared packager.

Per-program extracted data is namespaced under ``extracted/{submarines,ddg,
ceiling}`` to avoid the filename collisions between the former workbooks (both
shipped e.g. ``cost_funnel_summary.csv`` with different contents). Each program
sub-package under ``sheets/`` has its own ``_bind.py`` that points ``EXTRACTED``
and ``load_extracted_csv`` at its slice of this root.
"""
from __future__ import annotations

from pathlib import Path

from workbook_core.lib import package_workbook

# ---------------------------------------------------------------------------
# Pipeline bindings
# ---------------------------------------------------------------------------

WORKBOOK_DIR = Path(__file__).resolve().parents[1]   # projects/distributed_shipbuilding/tam/master/  (build output lands here)
PROJECT_DIR = WORKBOOK_DIR                            # output lands at the master/ root
REPO_ROOT = Path(__file__).resolve().parents[5]      # ooxml_build_pipelines_light/
OUT = PROJECT_DIR / "20260620_Distributed Shipbuilding Master TAM_vS.xlsx"

# Namespaced extracted-data root; per-program slices live under it.
EXTRACTED = WORKBOOK_DIR / "extracted"

# Shared, project-level supplier evidence registry (operating-entity overrides keyed by UEI).
# Domain data lives at project level - never in workbook_core (locked-core rule).
REGISTRY_CSV = REPO_ROOT / "projects/distributed_shipbuilding/sam/award_classification/supplier_bucketing/vendor_evidence_registry.csv"

_TITLE = "Distributed Shipbuilding - Master TAM (Virginia / Columbia / DDG-51)"
_CREATOR = "workbook_master_tam build_workbook.py"
_APP = "workbook_master_tam"


def build() -> int:
    """Render every registered sheet and package into the output xlsx."""
    from workbook_master_tam.sheets import SHEETS
    return package_workbook(OUT, SHEETS, title=_TITLE, creator=_CREATOR,
                            app_name=_APP, normalize_dashes=True)
