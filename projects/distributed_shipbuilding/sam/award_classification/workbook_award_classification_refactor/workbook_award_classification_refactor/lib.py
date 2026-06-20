"""Award Classification Refactor pipeline bindings.

The OOXML engine lives in the shared ``workbook_core`` package at the workspace
root. This module is intentionally thin: it binds the things specific to this
pipeline (the output path, the extracted-data dir, the docProps identity),
exposes a load_extracted_csv wrapper bound to this pipeline's data dir, and
packages the SHEETS module list via the shared packager.

The extracted/ dir holds the per-sheet raw CSVs written verbatim from the manual
workbook by ``extract_classification_cuts.py`` (re-run only if the manual source
changes). Cell values are stored as strings so identifiers keep their exact form
(Work-type ID "01", CAGE "90099"); the sheet modules cast the numeric columns.

The build always writes the canonical ``award_classification_refactor.xlsx`` at the
project root.
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

WORKBOOK_DIR = Path(__file__).resolve().parents[1]   # projects/distributed_shipbuilding/sam/award_classification/workbook_award_classification_refactor/
PROJECT_DIR = Path(__file__).resolve().parents[2]    # projects/distributed_shipbuilding/sam/award_classification/   (build output lands here)
REPO_ROOT = Path(__file__).resolve().parents[6]      # ooxml_build_pipelines_light/
OUT = PROJECT_DIR / "award_classification_refactor.xlsx"
EXTRACTED = WORKBOOK_DIR / "extracted"

_TITLE = "Award Classification Refactor - New-Construction Subaward Vendor Classification"
_CREATOR = "workbook_award_classification_refactor build_workbook.py"
_APP = "workbook_award_classification_refactor"


def load_extracted_csv(name: str) -> tuple[list[str], list[list]]:
    """Load extracted/<name>.csv from this pipeline's data dir (numeric-coerced)."""
    return _core_load_extracted_csv(name, EXTRACTED)


def build() -> int:
    """Render every registered sheet and package into the output xlsx.

    normalize_dashes stays OFF: the manual workbook's em/en dashes and curly
    quotes are part of the reconstructed content and are preserved verbatim.
    """
    from workbook_award_classification_refactor.sheets import SHEETS
    return package_workbook(OUT, SHEETS, title=_TITLE, creator=_CREATOR,
                            app_name=_APP, normalize_dashes=False)
