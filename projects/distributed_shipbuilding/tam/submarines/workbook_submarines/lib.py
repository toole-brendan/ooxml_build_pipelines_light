"""Distributed Shipbuilding Submarines pipeline bindings.

The OOXML engine lives in the shared ``workbook_core`` package at the workspace
root. This module is intentionally thin: it binds the things specific to this
pipeline (the output path, the extracted-data dir, the docProps identity),
exposes a load_extracted_csv wrapper bound to this pipeline's data dir, and
packages the SHEETS module list via the shared packager.

The sheet modules import workbook_core.* directly; the workbook_core import path
is set up in workbook_submarines/__init__.py.
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

WORKBOOK_DIR = Path(__file__).resolve().parents[1]   # projects/distributed_shipbuilding/submarines/workbook/
PROJECT_DIR = Path(__file__).resolve().parents[1]    # projects/distributed_shipbuilding/submarines/   (build output lands here)
REPO_ROOT = Path(__file__).resolve().parents[5]      # ooxml_build_pipelines_light/
OUT = PROJECT_DIR / "20260601_Distributed Shipbuilding Submarines_vS.xlsx"
EXTRACTED = WORKBOOK_DIR / "extracted"
# Shared, project-level supplier evidence registry (operating-entity overrides keyed by UEI).
# Domain data lives at project level - never in workbook_core (locked-core rule).
REGISTRY_CSV = REPO_ROOT / "projects/distributed_shipbuilding/research_shared/supplier_bucketing/vendor_evidence_registry.csv"

_TITLE = "Distributed Shipbuilding Submarines - Outsourced Construction TAM & SAM"
_CREATOR = "workbook_submarines build_workbook.py"
_APP = "workbook_submarines"


def load_extracted_csv(name: str) -> tuple[list[str], list[list]]:
    """Load extracted/<name>.csv from this pipeline's data dir."""
    return _core_load_extracted_csv(name, EXTRACTED)


def build() -> int:
    """Render every registered sheet and package into the output xlsx."""
    from workbook_submarines.sheets import SHEETS
    return package_workbook(OUT, SHEETS, title=_TITLE, creator=_CREATOR,
                            app_name=_APP, normalize_dashes=True)
